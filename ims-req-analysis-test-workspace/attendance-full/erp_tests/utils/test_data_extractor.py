"""Test Data Extractor — Scrape real data from IMS SIT for data-driven tests.

Known bugs fixed (2026-07-09):
  1. Row selector: Must use "tr.ant-table-row", plain "tr" grabs empty-state rows.
  2. Column offset: td count > th count (selection checkbox), fixed with offset.
  3. Query button: Don't use ".ant-btn-primary" selector, iterate visible buttons.
  4. Targeted extraction: If no late/absent in page 1, apply category filter directly.
"""

import json
from pathlib import Path
from playwright.sync_api import Page

DATA_DIR = Path(__file__).parent / "extracted_data"
DATA_DIR.mkdir(exist_ok=True)


def extract_table_rows(page: Page, table_selector: str = ".ant-table-tbody tr.ant-table-row") -> list[dict]:
    """Extract rows from Ant Design table with column offset fix."""
    rows = page.locator(table_selector)
    if rows.count() == 0:
        rows = page.locator(".ant-table-tbody tr")
        if rows.count() == 0:
            return []

    headers = page.locator(".ant-table-thead th").all_inner_texts()
    headers = [h.strip() for h in headers if h.strip()]

    results = []
    for i in range(min(rows.count(), 50)):
        cells = rows.nth(i).locator("td").all_inner_texts()
        cells = [c.strip() for c in cells]
        offset = len(cells) - len(headers)
        if offset > 0:
            cells = cells[offset:]
        if len(cells) >= len(headers):
            cells = cells[:len(headers)]
            results.append(dict(zip(headers, cells)))
    return results


def _click_query(page: Page):
    for btn in page.locator("button:visible").all():
        try:
            if "查" in btn.inner_text() and "询" in btn.inner_text():
                btn.click(); return True
        except: pass
    return False


def _search_employee_by_id(page: Page, emp_id: str):
    """Search for a specific employee by遍历 all selects to find the employee filter."""
    selects = page.locator(".ant-select")
    for idx in range(selects.count()):
        try:
            selects.nth(idx).click()
            page.wait_for_timeout(600)
            search_input = page.locator("input[role='combobox']").first
            if search_input.count() > 0:
                search_input.fill(emp_id)
                page.wait_for_timeout(1500)
                # Press Enter to select first match
                page.keyboard.press("Enter")
                page.wait_for_timeout(500)
                # Check if this select shows matching employee — query to verify
                _click_query(page)
                page.wait_for_timeout(3000)
                # If we got results, this was the employee filter
                if page.locator(".ant-table-tbody tr.ant-table-row").count() > 0:
                    return
                # Otherwise, undo and try next
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
        except:
            try: page.keyboard.press("Escape"); page.wait_for_timeout(300)
            except: pass


def _apply_exception_filter(page: Page, exception_type: str):
    """Apply 考勤异常 filter — try every select until finding the right one."""
    selects = page.locator(".ant-select")
    for idx in range(selects.count()):
        try:
            selects.nth(idx).click()
            page.wait_for_timeout(600)
            # Check if this dropdown has the target option
            opts = page.locator(".ant-select-item-option-content")
            found = False
            for opt in opts.all():
                text = opt.inner_text()
                if exception_type in text:
                    opt.click()
                    page.wait_for_timeout(500)
                    found = True
                    break
            if found:
                return True
            # Not this dropdown — close and try next
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
        except:
            try:
                page.keyboard.press("Escape")
                page.wait_for_timeout(300)
            except:
                pass
    return False


def extract_daily_attendance_data(page: Page) -> list[dict]:
    """Navigate, query, and extract daily attendance with targeted category search."""
    page.goto("http://test.fj.dtsimple.pro/#/personnel/workAttendance/dailyReportNew")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    _click_query(page)
    page.wait_for_timeout(3000)

    # Standard extraction
    data = extract_table_rows(page)

    # Check what categories we have
    variations = extract_employee_variations(data)

    # Targeted: if no absent employees, filter by 没上班
    if len(variations.get("absent_employees", [])) == 0:
        if _apply_exception_filter(page, "没上班"):
            _click_query(page)
            page.wait_for_timeout(3000)
            data.extend(extract_table_rows(page))

    # Targeted: if no late employees found, search for SA28903 (known late employee)
    variations2 = extract_employee_variations(data)
    if len(variations2.get("late_employees", [])) == 0:
        # Search for SA28903 by工号 in the employee filter
        _search_employee_by_id(page, "SA28903")
        data.extend(extract_table_rows(page))
    # Targeted: if no missing card, filter by 缺卡
    variations3 = extract_employee_variations(data)
    if len(variations3.get("missing_card_employees", [])) == 0:
        if _apply_exception_filter(page, "缺卡"):
            _click_query(page)
            page.wait_for_timeout(3000)
            data.extend(extract_table_rows(page))

    with open(DATA_DIR / "daily_attendance_sample.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


def extract_employee_variations(data: list[dict]) -> dict:
    """Categorize employees by test-relevant dimensions.

    Note: Due to Ant Design table column header complexity, '没上班'
    may appear in either '考勤异常' or '迟到早退' field. Check both.
    """
    def _get_exception(row):
        exc = row.get("考勤异常", "")
        late_early = row.get("迟到早退", "")
        # Check both fields for exception values
        for val in [exc, late_early]:
            if val in ("没上班", "缺卡", "正常"):
                return val
        return exc or late_early

    result = {
        "normal_employees": [], "late_employees": [], "early_leave_employees": [],
        "absent_employees": [], "missing_card_employees": [], "by_shift": {},
    }
    for row in data:
        exception = _get_exception(row)
        if exception == "没上班":
            result["absent_employees"].append(row)
        elif exception == "缺卡":
            result["missing_card_employees"].append(row)
        else:
            try:
                late = int(row.get("迟到", "0"))
                early = int(row.get("早退", "0"))
                if late > 0: result["late_employees"].append(row)
                elif early > 0: result["early_leave_employees"].append(row)
                else: result["normal_employees"].append(row)
            except ValueError:
                result["normal_employees"].append(row)
        shift = row.get("班次", "未知")
        result["by_shift"].setdefault(shift, []).append(row)
    return result


def extract_employees_for_leave_test(page: Page) -> list[dict]:
    """Extract employees from leave registration dropdown."""
    page.goto("http://test.fj.dtsimple.pro/#/personnel/workAttendance/leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    add_btn = page.locator("button:has-text('新增')")
    if add_btn.count() > 0:
        add_btn.first.click(); page.wait_for_timeout(2000)
    selects = page.locator(".ant-select")
    if selects.count() > 0:
        selects.first.click(); page.wait_for_timeout(1000)
        options = page.locator(".ant-select-item-option-content").all_inner_texts()
        page.keyboard.press("Escape")
        return [{"display": o.strip()} for o in options if o.strip()]
    return []


def build_test_dataset(page: Page) -> dict:
    """Build complete test dataset from SIT environment."""
    print("Extracting daily attendance data...")
    daily_data = extract_daily_attendance_data(page)
    variations = extract_employee_variations(daily_data)
    print("Extracting employee list for leave tests...")
    employee_list = extract_employees_for_leave_test(page)
    dataset = {
        "metadata": {
            "extracted_at": page.evaluate("() => new Date().toISOString()"),
            "total_records": len(daily_data),
        },
        "summary": {
            "normal": len(variations["normal_employees"]),
            "late": len(variations["late_employees"]),
            "early_leave": len(variations["early_leave_employees"]),
            "absent": len(variations["absent_employees"]),
            "missing_card": len(variations["missing_card_employees"]),
            "shifts": {k: len(v) for k, v in variations["by_shift"].items()},
        },
        "samples": {
            "normal_employee": variations["normal_employees"][0] if variations["normal_employees"] else None,
            "late_employee": variations["late_employees"][0] if variations["late_employees"] else None,
            "absent_employee": variations["absent_employees"][0] if variations["absent_employees"] else None,
            "missing_card_employee": variations["missing_card_employees"][0] if variations["missing_card_employees"] else None,
        },
        "employees_for_leave": employee_list[:20],
        "by_shift": variations["by_shift"],
    }
    path = DATA_DIR / "test_dataset.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"Dataset saved: {path}")
    print(f"  Normal: {dataset['summary']['normal']}, Late: {dataset['summary']['late']}, "
          f"Absent: {dataset['summary']['absent']}, MissingCard: {dataset['summary']['missing_card']}")
    return dataset
