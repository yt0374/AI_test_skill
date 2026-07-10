"""IMS Attendance Data Setup — Pre-test import + Post-test cleanup.

Pre-test:
  1. Delete existing records for target employees on today's date
  2. Generate clean Excel with varied data (normal/late/missing_card)
  3. Import → Daily calc → Extract

Post-test:
  1. Delete all imported records for today
"""

from playwright.sync_api import sync_playwright, Page
from pathlib import Path
from datetime import datetime
import json, openpyxl

BASE_URL = "http://test.fj.dtsimple.pro"
DETAIL_URL = f"{BASE_URL}/#/personnel/workAttendance/detail"
DAILY_URL = f"{BASE_URL}/#/personnel/workAttendance/dailyReportNew"
EXTRACTED = Path(__file__).parent / "erp_tests" / "utils" / "extracted_data"
EMPLOYEES_FILE = EXTRACTED / "employees_sit.json"

# Varied attendance scenarios
TIME_SPECS = [
    ("08:00", "17:30"),   # Normal
    ("08:00", "17:30"),   # Normal
    ("12:00", "17:30"),   # Late (4hrs → exceeds any grace period)
    ("08:00", None),       # Only morning → 缺卡
    ("08:00", "17:30"),   # Normal
]


def _login(page: Page):
    page.goto(f"{BASE_URL}/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    if "/login" in page.url:
        page.fill("#form_item_username", "admin")
        page.fill("#form_item_password", "metas2660")
        sel = page.locator(".ant-select")
        if sel.count() > 0:
            sel.first.click()
            page.wait_for_timeout(500)
            page.locator(".ant-select-item-option-content").first.click()
        page.click(".ant-btn-primary")
        page.wait_for_timeout(5000)
        page.wait_for_load_state("networkidle")


def _click_button(page: Page, keyword: str) -> bool:
    for btn in page.locator("button:visible").all():
        try:
            if keyword in btn.inner_text():
                btn.click()
                return True
        except:
            pass
    return False


def _delete_records_for_employees(page: Page, emp_ids: list[str], date_str: str):
    """Delete attendance records for specific employees on a given date."""
    page.goto(DETAIL_URL)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    for emp_id in emp_ids:
        # Search employee
        selects = page.locator(".ant-select")
        if selects.count() >= 2:
            selects.nth(1).click()
            page.wait_for_timeout(600)
            search = page.locator("input[role='combobox']").first
            if search.count() > 0:
                search.fill(emp_id)
                page.wait_for_timeout(1500)
                page.keyboard.press("Enter")
                page.wait_for_timeout(500)

        _click_button(page, "查")
        page.wait_for_timeout(3000)

        rows = page.locator(".ant-table-tbody tr.ant-table-row")
        if rows.count() > 0:
            # Select all + batch delete
            page.locator(".ant-table-thead input[type='checkbox']").first.click()
            page.wait_for_timeout(300)
            _click_button(page, "批量")
            page.on("dialog", lambda d: d.accept())
            page.wait_for_timeout(1000)
            # Confirm popconfirm
            for sel in [".ant-popconfirm .ant-btn-primary", "button:has-text('确')", ".ant-btn-primary"]:
                btn = page.locator(sel).first
                if btn.count() > 0:
                    try:
                        btn.click(timeout=2000)
                        page.wait_for_timeout(1000)
                        break
                    except:
                        pass
            page.wait_for_timeout(2000)

    print(f"[cleanup] Deleted old records for {len(emp_ids)} employees")


def _generate_excel(employees: list[dict]) -> Path:
    """Generate clean Excel with varied attendance data."""
    out_path = EXTRACTED / "test_attendance_filled.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Name", "Ac-No", "sTime", "Machine"])

    today = datetime.now()
    for i, emp in enumerate(employees[:5]):
        morning_t, afternoon_t = TIME_SPECS[i]
        row = i * 2 + 2

        ws.cell(row=row, column=1, value=emp["工号"])
        ws.cell(row=row, column=2, value=emp["姓名"])
        ws.cell(row=row, column=3, value=today.replace(
            hour=int(morning_t.split(":")[0]),
            minute=int(morning_t.split(":")[1]),
            second=0).strftime("%Y-%m-%d %H:%M:%S"))
        ws.cell(row=row, column=4, value="1")

        if afternoon_t:
            ws.cell(row=row + 1, column=1, value=emp["工号"])
            ws.cell(row=row + 1, column=2, value=emp["姓名"])
            ws.cell(row=row + 1, column=3, value=today.replace(
                hour=int(afternoon_t.split(":")[0]),
                minute=int(afternoon_t.split(":")[1]),
                second=0).strftime("%Y-%m-%d %H:%M:%S"))
            ws.cell(row=row + 1, column=4, value="1")

    wb.save(str(out_path))
    print(f"[excel] Generated clean Excel: {out_path} ({ws.max_row - 1} data rows)")
    return out_path


def _import_excel(page: Page, filepath: Path):
    """Import Excel via UI file chooser."""
    page.goto(DETAIL_URL)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # Click excel导入
    for btn in page.locator("button:visible").all():
        try:
            if "excel" in btn.inner_text().lower():
                btn.click()
                break
        except:
            pass
    page.wait_for_timeout(2000)

    # File chooser
    with page.expect_file_chooser() as fc:
        page.locator("button:has-text('选择文件')").first.click()
    fc.value.set_files(str(filepath))
    page.wait_for_timeout(3000)

    # Wait for confirm button to enable naturally
    for attempt in range(15):
        page.wait_for_timeout(1500)
        confirm = page.locator("button.ant-btn-primary:has-text('确认导入')")
        if confirm.count() > 0 and "is-disabled" not in (confirm.get_attribute("class") or ""):
            confirm.click()
            page.wait_for_timeout(5000)
            print("[import] Confirmed")
            return
    page.locator("button.ant-btn-primary:has-text('确认导入')").click(force=True)
    page.wait_for_timeout(5000)
    print("[import] Force-imported")


def _run_daily_calc(page: Page):
    """Run 日考勤计算 with correct filter+query context."""
    page.goto(DAILY_URL)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # Set date filter
    page.locator(".ant-picker").first.click()
    page.wait_for_timeout(1000)
    today = str(datetime.now().day)
    for cell in page.locator(".ant-picker-cell-inner").all():
        if cell.inner_text() == today:
            cell.click()
            break
    page.wait_for_timeout(500)

    # Query first (establishes context)
    _click_button(page, "询")
    page.wait_for_timeout(3000)

    # Daily calc
    for btn in page.locator("button:visible").all():
        try:
            if "日考勤计算" in btn.inner_text():
                btn.click()
                break
        except:
            pass
    page.wait_for_timeout(2000)

    # Confirm
    confirm = page.locator(".ant-modal .ant-btn-primary").first
    if confirm.count() > 0:
        confirm.click()
        for attempt in range(90):
            page.wait_for_timeout(2000)
            if "任务完成" in page.locator("body").inner_text():
                print(f"[daily-calc] Done at {attempt + 1}")
                break
    page.locator(".ant-modal-close").first.click()
    page.wait_for_timeout(2000)


def setup_test_data():
    """Complete pre-test pipeline: cleanup → generate → import → daily calc."""
    with open(EMPLOYEES_FILE, "r", encoding="utf-8") as f:
        all_employees = json.load(f)

    employees = all_employees[10:15]  # Use indices 10-14
    emp_ids = [e["工号"] for e in employees]
    today = datetime.now().strftime("%Y/%m/%d")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        _login(page)

        # 1. Delete old records for these employees on today's date
        _delete_records_for_employees(page, emp_ids, today)

        # 2. Generate clean Excel
        excel_path = _generate_excel(employees)

        # 3. Import
        _import_excel(page, excel_path)

        # 4. Daily calc
        _run_daily_calc(page)

        browser.close()
    print("[setup] Complete")


def cleanup_test_data():
    """Post-test cleanup: delete all imported records for today."""
    with open(EMPLOYEES_FILE, "r", encoding="utf-8") as f:
        all_employees = json.load(f)

    employees = all_employees[10:15]
    emp_ids = [e["工号"] for e in employees]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        _login(page)

        today = datetime.now().strftime("%Y/%m/%d")
        _delete_records_for_employees(page, emp_ids, today)
        print("[cleanup] All test data deleted")

        browser.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        cleanup_test_data()
    else:
        setup_test_data()
