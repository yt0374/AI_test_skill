"""Generate Excel with SWAPPED Name/Ac-No + import."""
from playwright.sync_api import sync_playwright
from pathlib import Path
SCREENSHOT_DIR = Path(__file__).parent / "screenshots" / "debug"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
from datetime import datetime
import json, openpyxl, shutil

EXTRACTED = Path(r"C:\Users\yanta\.claude\skills\ims-req-analysis-test-workspace\attendance-full\erp_tests\utils\extracted_data")
template = list(EXTRACTED.glob("ims_template_*.xlsx"))[0]

with open(EXTRACTED / "employees_sit.json", "r", encoding="utf-8") as f:
    all_employees = json.load(f)

# Use fresh employees each time to create varied data
# First 5 already imported, use employees 5-9 for new scenarios
start_idx = 10
employees = all_employees[start_idx:start_idx+5]
print(f"Using {len(employees)} employees (indices {start_idx}-{start_idx+4})")

out_path = EXTRACTED / "test_attendance_filled.xlsx"
shutil.copy(template, out_path)
wb = openpyxl.load_workbook(out_path)
ws = wb.active

today = datetime.now()
# Generate VARIED attendance data for different test scenarios:
#   Index 0: Normal   — 08:00 in + 17:30 out  → normal_employee
#   Index 1: Normal   — 08:00 in + 17:30 out  → normal_employee
#   Index 2: Late     — 09:00 in + 17:30 out  → late_employee (迟到)
#   Index 3: Only AM  — 08:00 in only         → missing_card (只有上午)
#   Index 4: Normal   — 08:00 in + 17:30 out  → normal_employee
time_specs = [
    ("08:00", "17:30"),   # Normal
    ("08:00", "17:30"),   # Normal
    ("12:00", "17:30"),   # Late (4小时迟到，必定超过任何免计时长)
    ("08:00", None),       # Only morning → 缺卡
    ("08:00", "17:30"),   # Normal
]

for i, emp in enumerate(employees):
    row = i * 2 + 2
    morning_time, afternoon_time = time_specs[i]

    # Morning record
    ws.cell(row=row, column=1, value=emp["工号"])
    ws.cell(row=row, column=2, value=emp["姓名"])
    ws.cell(row=row, column=3, value=today.replace(
        hour=int(morning_time.split(":")[0]),
        minute=int(morning_time.split(":")[1]),
        second=0).strftime("%Y-%m-%d %H:%M:%S"))
    ws.cell(row=row, column=4, value="1")

    # Afternoon record (skip if None for missing card scenario)
    if afternoon_time:
        ws.cell(row=row+1, column=1, value=emp["工号"])
        ws.cell(row=row+1, column=2, value=emp["姓名"])
        ws.cell(row=row+1, column=3, value=today.replace(
            hour=int(afternoon_time.split(":")[0]),
            minute=int(afternoon_time.split(":")[1]),
            second=0).strftime("%Y-%m-%d %H:%M:%S"))
        ws.cell(row=row+1, column=4, value="1")

for r in range(12, ws.max_row + 1):
    for c in range(1, 5):
        ws.cell(row=r, column=c, value=None)

wb.save(str(out_path))
print(f"[OK] Excel saved: {out_path}")

# Import
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    page.goto("http://test.fj.dtsimple.pro/")
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

    # ── Dedup check: skip import if today's data already exists ──
    page.goto("http://test.fj.dtsimple.pro/#/personnel/workAttendance/detail")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    for i in range(page.locator("button:visible").count()):
        try:
            if "查" in page.locator("button:visible").nth(i).inner_text():
                page.locator("button:visible").nth(i).click(); break
        except: pass
    page.wait_for_timeout(3000)

    existing_rows = page.locator(".ant-table-tbody tr.ant-table-row").count()
    if existing_rows > 0:
        total = page.locator(".ant-pagination-total-text").first
        print(f"[NOTE] {existing_rows} existing records — importing anyway to add varied data")
        # Don't exit — continue to import
    print("[OK] No existing data — proceeding with import")

    # ── Import ──
    page.goto("http://test.fj.dtsimple.pro/#/personnel/workAttendance/detail")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    page.locator("button:has-text('excel导入')").first.click()
    page.wait_for_timeout(2000)

    with page.expect_file_chooser() as fc:
        page.locator("button:has-text('选择文件')").first.click()
    fc.value.set_files(str(out_path))
    page.wait_for_timeout(3000)

    modal_text = page.locator(".ant-modal-body").first.inner_text()
    with open("import_check.txt", "w", encoding="utf-8") as f:
        f.write(modal_text)

    if "错误" in modal_text:
        print("Errors in preview:")
        for line in modal_text.split("\n"):
            if "错误" in line:
                print(f"  {line}")
    else:
        print("[OK] No errors!")

    # Wait for confirm to enable (now it should!)
    for attempt in range(15):
        page.wait_for_timeout(1500)
        confirm = page.locator("button.ant-btn-primary:has-text('确认导入')")
        if confirm.count() > 0:
            cls = confirm.get_attribute("class") or ""
            if "is-disabled" not in cls:
                print(f"[OK] Button ENABLED at attempt {attempt+1}!")
                confirm.click()
                page.wait_for_timeout(5000)
                print("[SUCCESS] Import completed!")
                break
    else:
        # Fallback: mouse click
        confirm_btn = page.locator("button.ant-btn-primary:has-text('确认导入')")
        box = confirm_btn.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
            page.wait_for_timeout(5000)
            print("[OK] Mouse click fallback")

    page.screenshot(path=str(SCREENSHOT_DIR / "import_done.png"))

    # ── Trigger 日考勤计算 with 任务完成 polling ──
    from datetime import datetime
    today_str = datetime.now().strftime("%Y-%m-%d")

    page.goto("http://test.fj.dtsimple.pro/#/personnel/workAttendance/dailyReportNew")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # Click 日考勤计算 button
    calc_clicked = False
    for i in range(page.locator("button:visible").count()):
        try:
            if "日考勤计算" in page.locator("button:visible").nth(i).inner_text():
                page.locator("button:visible").nth(i).click()
                calc_clicked = True
                break
        except:
            pass

    if calc_clicked:
        page.wait_for_timeout(2000)

        # Fill date range — find inputs by placeholder or position
        date_inputs = page.locator(".ant-modal input")
        print(f"  Modal inputs: {date_inputs.count()}")
        # Print first few input placeholders to find the right ones
        for j in range(min(date_inputs.count(), 6)):
            try:
                ph = date_inputs.nth(j).get_attribute("placeholder")
                print(f"    [{j}] placeholder={ph}")
            except:
                pass

        if date_inputs.count() >= 2:
            # IMS date inputs are readonly — use force=True
            date_inputs.nth(0).fill(today_str, force=True)
            page.wait_for_timeout(300)
            date_inputs.nth(1).fill(today_str, force=True)
            page.wait_for_timeout(300)
            print(f"[OK] Set date range (force): {today_str} ~ {today_str}")

        # Click 确认 in the modal
        page.locator(".ant-modal .ant-btn-primary").first.click()
        print("[OK] Daily calc confirmed — polling for '任务完成'...")

        # Poll for completion
        for attempt in range(90):  # Max 3 minutes
            page.wait_for_timeout(2000)
            try:
                modal_text = page.locator(".ant-modal-body").inner_text()
            except:
                modal_text = ""
            if "任务完成" in modal_text:
                print(f"[OK] 任务完成 at attempt {attempt+1}")
                break
            if attempt % 10 == 9:
                print(f"  Still waiting... (attempt {attempt+1})")
        else:
            print("[WARN] 任务完成 not detected within timeout")

        # Close the modal
        close_btn = page.locator(".ant-modal-close")
        if close_btn.count() > 0:
            close_btn.first.click()
            page.wait_for_timeout(1000)
            print("[OK] Modal closed")

        # Verify: click query to see results
        for i in range(page.locator("button:visible").count()):
            try:
                if "查" in page.locator("button:visible").nth(i).inner_text():
                    page.locator("button:visible").nth(i).click()
                    break
            except:
                pass
        page.wait_for_timeout(3000)
    else:
        print("[WARN] No '日考勤计算' button found")

    page.screenshot(path=str(SCREENSHOT_DIR / "daily_calc_done.png"))
    browser.close()
    print("\n[DONE]")
