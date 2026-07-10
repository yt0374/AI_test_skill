"""Generate test attendance Excel and upload to SIT via 导入.

Two-step process:
  1. Extract available employees from SIT → generate Excel with today's times
  2. Upload the Excel via 考勤登记 → Excel导入 → trigger 日考勤计算
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from playwright.sync_api import Page

DATA_DIR = Path(__file__).parent / "extracted_data"
DATA_DIR.mkdir(exist_ok=True)

BASE = "http://test.fj.dtsimple.pro"
DETAIL = f"{BASE}/#/personnel/workAttendance/detail"
DAILY = f"{BASE}/#/personnel/workAttendance/dailyReportNew"
LEAVE = f"{BASE}/#/personnel/workAttendance/leave"

TEST_EXCEL_PATH = DATA_DIR / "test_attendance_import.xlsx"


# ── Step 1: Extract employees from SIT ──────────────────────────────────────

def _extract_available_employees(page: Page) -> list[dict]:
    """Get real employee IDs + names from the 请假登记 employee dropdown."""
    page.goto(LEAVE, timeout=10000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    add_btn = page.locator("button:has-text('新增')")
    if add_btn.count() > 0:
        add_btn.first.click()
        page.wait_for_timeout(1500)

    # Open employee select and read options
    selects = page.locator(".ant-select")
    employees = []
    if selects.count() > 0:
        selects.first.click()
        page.wait_for_timeout(1000)
        options = page.locator(".ant-select-item-option-content")
        for i in range(min(options.count(), 10)):
            text = options.nth(i).inner_text().strip()
            if text and "-" in text:
                parts = text.split("-", 1)
                employees.append({"工号": parts[0].strip(), "姓名": parts[1].strip()})
        page.keyboard.press("Escape")

    # Close add form
    cancel = page.locator("button:has-text('取消'), button:has-text('关闭')").first
    if cancel.count() > 0:
        cancel.click()
        page.wait_for_timeout(500)

    print(f"[generator] Extracted {len(employees)} employees from SIT")
    return employees


# ── Step 2: Generate Excel with test attendance data ─────────────────────────

def _generate_excel(employees: list[dict]) -> Path:
    """Generate an Excel file with test attendance records for today.

    Creates records for morning shift (早班) for each employee:
      工号, 姓名, 考勤时间 (yyyy-MM-dd HH:mm), 类型=正常, 来源=导入

    Uses openpyxl if available, falls back to CSV.
    """
    today = datetime.now()
    # Morning shift: 08:00 check-in, 17:30 check-out
    morning_in = today.replace(hour=8, minute=0, second=0)
    morning_out = today.replace(hour=17, minute=30, second=0)

    try:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "考勤导入"
        ws.append(["工号", "姓名", "考勤时间", "类型", "来源"])

        for emp in employees:
            ws.append([emp["工号"], emp["姓名"],
                       morning_in.strftime("%Y-%m-%d %H:%M"), "正常", "导入"])
            ws.append([emp["工号"], emp["姓名"],
                       morning_out.strftime("%Y-%m-%d %H:%M"), "正常", "导入"])

        wb.save(str(TEST_EXCEL_PATH))
        print(f"[generator] Generated Excel: {TEST_EXCEL_PATH} "
              f"({len(employees) * 2} records for {len(employees)} employees)")
        return TEST_EXCEL_PATH

    except ImportError:
        # Fallback: write CSV
        csv_path = TEST_EXCEL_PATH.with_suffix(".csv")
        with open(csv_path, "w", encoding="utf-8-sig") as f:
            f.write("工号,姓名,考勤时间,类型,来源\n")
            for emp in employees:
                f.write(f"{emp['工号']},{emp['姓名']},"
                        f"{morning_in.strftime('%Y-%m-%d %H:%M')},正常,导入\n")
                f.write(f"{emp['工号']},{emp['姓名']},"
                        f"{morning_out.strftime('%Y-%m-%d %H:%M')},正常,导入\n")
        print(f"[generator] Fallback CSV: {csv_path}")
        return csv_path


# ── Step 3: Upload via IMS Excel导入 ────────────────────────────────────────

def _upload_excel(page: Page, filepath: Path) -> bool:
    """Upload the generated Excel via 考勤登记 → Excel导入."""
    page.goto(DETAIL, timeout=10000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Find Excel导入 button (footnote 7 in the prototype)
    import_btn = page.locator("button:has-text('Excel导入'), button:has-text('导入')")
    if import_btn.count() == 0:
        import_btn = page.locator("text=Excel导入, text=导入").first

    if import_btn.count() == 0:
        print("[generator] Excel导入 button not found")
        return False

    import_btn.first.click()
    page.wait_for_timeout(2000)

    # Look for file input — Playwright can set files directly
    file_input = page.locator("input[type='file']")
    if file_input.count() > 0:
        file_input.first.set_input_files(str(filepath))
        page.wait_for_timeout(2000)
        print(f"[generator] File uploaded: {filepath.name}")

        # Try to find and click confirm button
        confirm_selectors = [
            "button:has-text('确认')",
            ".ant-btn-primary:has-text('确')",
            "button:has-text('导入')",
            ".ant-modal-footer .ant-btn-primary",
            ".ant-modal button.ant-btn-primary",
        ]
        for sel in confirm_selectors:
            btn = page.locator(sel).first
            if btn.count() > 0:
                try:
                    btn.click(timeout=5000)
                    page.wait_for_timeout(3000)
                    break
                except Exception:
                    continue

        # Accept any dialogs
        try:
            dialog = page.wait_for_event("dialog", timeout=2000)
            dialog.accept()
        except Exception:
            pass
        page.wait_for_timeout(2000)
        return True  # File was uploaded — consider it successful

    print("[generator] Upload form not found or missing file input")
    return False


# ── Step 4: Trigger 日考勤计算 ──────────────────────────────────────────────

def _trigger_daily_calc(page: Page) -> bool:
    """Trigger 日考勤计算 to generate stats from imported raw records."""
    page.goto(DAILY, timeout=10000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    calc_btn = page.locator("button:has-text('日考勤计算')")
    if calc_btn.count() == 0:
        print("[generator] 日考勤计算 button not found — daily stats may auto-generate after import")
        return True  # Some systems auto-calculate on import

    calc_btn.first.click()
    page.wait_for_timeout(1500)

    confirm = page.locator(".ant-btn-primary").first
    if confirm.count() > 0:
        confirm.click()
        print("[generator] Triggered 日考勤计算 — waiting for completion...")
        page.wait_for_timeout(10000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        return True

    return False


def _trigger_daily_calc_in_session(page: Page) -> bool:
    """Run 日考勤计算 within the current browser session.

    CRITICAL: Must follow the correct IMS flow:
      1. Set date filter + click 查询 (establishes query context)
      2. Click 日考勤计算 (inherits context)
      3. Confirm with default dates
      4. Poll for 任务完成
      5. Close modal

    The daily calc results are visible only in the session that ran them.
    """
    from datetime import datetime
    today_str = datetime.now().strftime("%Y/%m/%d")

    page.goto(f"{BASE}/#/personnel/workAttendance/dailyReportNew")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # Step 1: Set filter + query (establishes context)
    # Open date picker, select today
    picker = page.locator(".ant-picker").first
    if picker.count() > 0:
        picker.click()
        page.wait_for_timeout(1000)
        day_cells = page.locator(".ant-picker-cell-inner")
        today_day = str(datetime.now().day)
        for i in range(day_cells.count()):
            try:
                if day_cells.nth(i).inner_text() == today_day:
                    day_cells.nth(i).click()
                    break
            except:
                pass
        page.wait_for_timeout(500)

    # Click 查询
    for i in range(page.locator("button:visible").count()):
        try:
            t = page.locator("button:visible").nth(i).inner_text()
            if "查" in t and "询" in t:
                page.locator("button:visible").nth(i).click()
                break
        except:
            pass
    page.wait_for_timeout(3000)
    print("[daily-calc] Step 1: Query done")

    # Step 2: Open 日考勤计算
    for i in range(page.locator("button:visible").count()):
        try:
            if "日考勤计算" in page.locator("button:visible").nth(i).inner_text():
                page.locator("button:visible").nth(i).click()
                break
        except:
            pass
    page.wait_for_timeout(2000)

    # Step 3: Confirm (dates inherited from query context)
    confirm_btn = page.locator(".ant-modal .ant-btn-primary").first
    if confirm_btn.count() == 0:
        print("[daily-calc] Confirm button not found")
        return False
    confirm_btn.click()
    print("[daily-calc] Step 2: Confirmed, polling...")

    # Step 4: Poll for 任务完成
    for attempt in range(90):
        page.wait_for_timeout(2000)
        if "任务完成" in page.locator("body").inner_text():
            print(f"[daily-calc] Step 3: 任务完成 at {attempt + 1}")
            break
        if attempt % 15 == 14:
            print(f"  still waiting...")
    else:
        print("[daily-calc] Timeout waiting for completion")
        return False

    # Step 5: Close modal
    page.locator(".ant-modal-close").first.click()
    page.wait_for_timeout(2000)
    return True


# ── Main entry point ────────────────────────────────────────────────────────

def generate_and_import(page: Page) -> dict:
    """Full pipeline: extract employees → import → daily calc (same session) → extract.

    Returns the final dataset (same format as build_test_dataset).
    """
    from utils.test_data_extractor import build_test_dataset

    # 1. Fast check: already have COMPLETE data? (threshold: >= 10 records)
    try:
        ds = build_test_dataset(page)
        if ds["metadata"]["total_records"] >= 10:
            print(f"[generator] Data already complete ({ds['metadata']['total_records']} records).")
            return ds
        else:
            print(f"[generator] Data exists but incomplete ({ds['metadata']['total_records']} records < 10). "
                  "Running daily calc to refresh...")
    except Exception as e:
        print(f"[generator] Fast extract failed: {e}")
        ds = {"metadata": {"total_records": 0}, "samples": {}, "summary": {}}

    # 2. No data — try running daily calc in this session
    print("[generator] No daily stats found. Running 日考勤计算 in session...")
    if _trigger_daily_calc_in_session(page):
        try:
            ds = build_test_dataset(page)
            if ds["metadata"]["total_records"] > 0:
                print(f"[generator] After daily calc: {ds['metadata']['total_records']} records.")
                return ds
        except Exception as e:
            print(f"[generator] Re-extract failed: {e}")

    # 3. If still no data, try full import pipeline
    print("[generator] Daily calc didn't help — trying full import pipeline...")

    # 2. Extract employees
    print("\n[generator] === Generating test attendance data ===")
    employees = _extract_available_employees(page)
    if not employees:
        print("[generator] No employees available — cannot generate test data.")
        return ds

    # 3. Generate Excel
    filepath = _generate_excel(employees)

    # 4. Upload
    if not _upload_excel(page, filepath):
        print("[generator] Upload failed — tests will skip.")
        return ds

    # 5. Verify import: check raw records in 考勤登记
    from utils.test_data_seeder import _count_raw_records
    raw_count = _count_raw_records(page)
    print(f"[generator] Raw records after import: {raw_count}")

    if raw_count > 0:
        # 6. Try triggering daily calculation
        print("[generator] Triggering 日考勤计算...")
        try:
            page.goto(DAILY, timeout=10000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            calc_btn = page.locator("button:has-text('日考勤计算')")
            if calc_btn.count() > 0:
                calc_btn.first.click(timeout=5000)
                page.wait_for_timeout(2000)
                confirm = page.locator(".ant-btn-primary:has-text('确')").first
                if confirm.count() > 0:
                    confirm.click(timeout=5000)
                    print("[generator] Waiting for daily calculation...")
                    page.wait_for_timeout(15000)
        except Exception as e:
            print(f"[generator] Daily calc trigger failed: {e}")

    # 7. Re-extract
    print("\n[generator] === Re-extracting after import ===")
    try:
        ds = build_test_dataset(page)
    except Exception as e:
        print(f"[generator] Re-extract failed: {e}")
    print(f"[generator] Final dataset: {ds['metadata']['total_records']} records, "
          f"normal={ds['summary'].get('normal', 0)}, late={ds['summary'].get('late', 0)}, "
          f"absent={ds['summary'].get('absent', 0)}")

    return ds
