"""Extract daily attendance data from 日考勤统计 and categorize employees.

Usage:
    python extract_daily_stats.py --env sit
"""

import json
import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ENVIRONMENTS = {
    "sit": {"url": "http://test.fj.dtsimple.pro", "name": "SIT"},
    "uat": {"url": "http://uat.fj.dtsimple.pro", "name": "UAT"},
    "xinji": {"url": "http://bak.xinji.dtsimple.pro", "name": "新基"},
    "jingmen": {"url": "http://bak.jmym.dtsimple.pro", "name": "荆门"},
    "ajn": {"url": "http://bak.ajn.dtsimple.pro", "name": "安吉纳"},
}

OUTPUT_DIR = Path(__file__).parent / "erp_tests" / "utils" / "extracted_data"
DAILY_URL = "/#/personnel/workAttendance/dailyReportNew"


def click_button_by_text(page, keyword: str) -> bool:
    for i in range(page.locator("button:visible").count()):
        try:
            if keyword in page.locator("button:visible").nth(i).inner_text():
                page.locator("button:visible").nth(i).click()
                return True
        except:
            pass
    return False


def extract_daily_stats(env: dict) -> list[dict]:
    """Extract daily attendance records from 日考勤统计 page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        # Login
        page.goto(f"{env['url']}/")
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

        # Navigate to daily report
        page.goto(f"{env['url']}{DAILY_URL}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        if "ErrorPage" in page.title():
            print("Daily report page not accessible")
            browser.close()
            return []

        # Click query
        click_button_by_text(page, "查")
        page.wait_for_timeout(3000)

        # Read table headers
        headers = page.locator(".ant-table-thead th").all_inner_texts()
        headers = [h.strip() for h in headers if h.strip()]
        print(f"Headers ({len(headers)}): {headers[:15]}...")

        # Map key columns (+1 offset for selection column)
        col_map = {}
        for i, h in enumerate(headers):
            for key in ["工号", "姓名", "日期", "部门", "组别", "班次", "考勤异常",
                        "出勤时数", "正班时数", "迟到", "早退", "工作时数",
                        "带薪假时数", "请假时数", "回工时数"]:
                if key in h:
                    col_map[key] = i + 1

        print(f"Column mapping: {col_map}")

        # Get total pages
        total_el = page.locator(".ant-pagination-total-text").first
        total = 0
        if total_el.count() > 0:
            nums = re.findall(r'\d+', total_el.inner_text())
            total = int(nums[-1]) if nums else 0
        print(f"Total records: {total}")

        # Extract all pages
        records = []
        max_pages = min(20, (total // 50) + 2)

        for page_num in range(1, max_pages):
            if page_num > 1:
                page_btn = page.locator(f".ant-pagination-item-{page_num}")
                if page_btn.count() > 0:
                    page_btn.click()
                    page.wait_for_timeout(2000)

            rows = page.locator(".ant-table-tbody tr.ant-table-row")
            for i in range(rows.count()):
                try:
                    cells = rows.nth(i).locator("td")
                    row = {}
                    for key, idx in col_map.items():
                        try:
                            val = cells.nth(idx).inner_text().strip()
                            row[key] = val
                        except:
                            row[key] = ""
                    if row.get("工号"):
                        records.append(row)
                except:
                    pass

            if rows.count() < 50 or page_num >= max_pages - 1:
                break

        browser.close()
        return records


def categorize(records: list[dict]) -> dict:
    """Categorize records by attendance type for data-driven testing."""
    result = {
        "metadata": {"total_records": len(records)},
        "summary": {},
        "samples": {},
        "by_shift": {},
        "all_records": records,
    }

    categories = {
        "normal_employees": [],
        "late_employees": [],
        "absent_employees": [],
        "missing_card_employees": [],
    }

    for r in records:
        exc = r.get("考勤异常", "")
        if exc == "没上班":
            categories["absent_employees"].append(r)
        elif exc == "缺卡":
            categories["missing_card_employees"].append(r)
        else:
            try:
                late = int(r.get("迟到", "0"))
                if late > 0:
                    categories["late_employees"].append(r)
                else:
                    categories["normal_employees"].append(r)
            except ValueError:
                categories["normal_employees"].append(r)

        shift = r.get("班次", "未知")
        result["by_shift"].setdefault(shift, []).append(r)

    result["summary"] = {k: len(v) for k, v in categories.items()}
    result["summary"]["shifts"] = {k: len(v) for k, v in result["by_shift"].items()}

    result["samples"] = {
        "normal_employee": categories["normal_employees"][0] if categories["normal_employees"] else None,
        "late_employee": categories["late_employees"][0] if categories["late_employees"] else None,
        "absent_employee": categories["absent_employees"][0] if categories["absent_employees"] else None,
        "missing_card_employee": categories["missing_card_employees"][0] if categories["missing_card_employees"] else None,
    }

    return result


def main():
    env_name = "sit"
    if len(sys.argv) > 2 and sys.argv[1] == "--env":
        env_name = sys.argv[2]

    env = ENVIRONMENTS.get(env_name, ENVIRONMENTS["sit"])
    print(f"Environment: {env['name']} ({env['url']})")

    records = extract_daily_stats(env)
    if not records:
        print("No daily stats found. Run 日考勤计算 first.")
        return

    dataset = categorize(records)

    out_path = OUTPUT_DIR / f"daily_stats_{env_name}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Saved to {out_path}")
    print(f"  Total: {dataset['metadata']['total_records']}")
    print(f"  Normal: {dataset['summary'].get('normal_employees', 0)}")
    print(f"  Late: {dataset['summary'].get('late_employees', 0)}")
    print(f"  Absent: {dataset['summary'].get('absent_employees', 0)}")
    print(f"  MissingCard: {dataset['summary'].get('missing_card_employees', 0)}")
    s = dataset["samples"]
    if s["normal_employee"]:
        print(f"  Sample normal: 工号={s['normal_employee']['工号']}")

    # Also save employees from daily stats for import testing
    emp_list = [{"工号": r.get("工号", ""), "姓名": r.get("姓名", "")} for r in records]
    emp_path = OUTPUT_DIR / f"employees_{env_name}.json"
    with open(emp_path, "w", encoding="utf-8") as f:
        json.dump(emp_list, f, ensure_ascii=False, indent=2)
    print(f"  Employees saved: {emp_path} ({len(emp_list)} records)")


if __name__ == "__main__":
    main()
