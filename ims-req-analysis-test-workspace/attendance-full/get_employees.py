"""Fix: extract correct Name column from employee archive."""
from playwright.sync_api import sync_playwright
import json, re
from pathlib import Path

OUTPUT = Path(r"C:\Users\yanta\.claude\skills\ims-req-analysis-test-workspace\attendance-full\erp_tests\utils\extracted_data\employees.json")

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

    page.goto("http://test.fj.dtsimple.pro/#/personnel/staffManagement/staffFile")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # Find and click query button by iterating visible buttons
    for i in range(page.locator("button:visible").count()):
        try:
            text = page.locator("button:visible").nth(i).inner_text()
            if "查询" in text or "查" in text:
                page.locator("button:visible").nth(i).click()
                print(f"Clicked query: '{text}'")
                break
        except:
            pass
    page.wait_for_timeout(3000)

    # Get table headers to identify columns
    headers = page.locator(".ant-table-thead th").all_inner_texts()
    headers = [h.strip() for h in headers if h.strip()]
    print(f"Headers ({len(headers)}): {headers}")

    # Find indices for 工号 and 姓名 in header
    id_col = next((i for i, h in enumerate(headers) if "工号" in h), 0)
    name_col = next((i for i, h in enumerate(headers) if "姓名" in h), 1)
    print(f"Header indices: 工号={id_col}, 姓名={name_col}")

    # Ant Design tables may have extra leading columns (selection, row num)
    # Adjust: shift +1 for selection checkbox column
    id_col += 1
    name_col += 1
    print(f"Adjusted: 工号={id_col}, 姓名={name_col}")

    # Extract from first page — use cell-level access
    employees = []
    rows = page.locator(".ant-table-tbody tr.ant-table-row")
    print(f"Rows found: {rows.count()}")
    for i in range(min(rows.count(), 100)):
        try:
            cells = rows.nth(i).locator("td")
            emp_id = cells.nth(id_col).inner_text().strip()
            name = cells.nth(name_col).inner_text().strip()
            # Debug first few
            if i < 3:
                print(f"  Row {i}: cells={cells.count()}, id='{emp_id}', name='{name}'")
            if emp_id and name and "暂无" not in emp_id:
                employees.append({"工号": emp_id, "姓名": name})
        except Exception as e:
            if i < 3:
                print(f"  Row {i} error: {e}")

    print(f"Extracted from page 1: {len(employees)}")

    # Get more pages
    total_text = page.locator(".ant-pagination-total-text").first
    if total_text.count() > 0:
        t = total_text.inner_text()
        nums = re.findall(r'\d+', t)
        total = int(nums[-1]) if nums else 0
    else:
        total = len(employees)

    for page_num in range(2, min(6, (total // 50) + 2)):
        page_btn = page.locator(f".ant-pagination-item-{page_num}")
        if page_btn.count() > 0:
            page_btn.click()
            page.wait_for_timeout(2000)

        rows = page.locator(".ant-table-tbody tr.ant-table-row")
        for i in range(rows.count()):
            try:
                cells = rows.nth(i).locator("td")
                emp_id = cells.nth(id_col).inner_text().strip()
                name = cells.nth(name_col).inner_text().strip()
                if emp_id and name and "暂无" not in emp_id:
                    employees.append({"工号": emp_id, "姓名": name})
            except:
                pass

    # Save
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(employees, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Saved {len(employees)} employees")
    for emp in employees[:10]:
        print(f"  工号={emp['工号']}, 姓名={emp['姓名']}")

    page.screenshot(path=str(Path(__file__).parent / "screenshots" / "debug" / "staff_correct.png"))
    browser.close()
