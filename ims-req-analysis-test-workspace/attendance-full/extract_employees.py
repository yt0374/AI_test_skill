"""Environment-aware employee collector and data generator.

Usage:
    python extract_employees.py --env sit     # Extract from SIT
    python extract_employees.py --env uat     # Extract from UAT
    python extract_employees.py --env jingmen # Extract from 荆门

Environment configs from environments/*.json in skill root.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

# Environment definitions (mirrors environments/*.json)
ENVIRONMENTS = {
    "sit": {
        "url": "http://test.fj.dtsimple.pro",
        "name": "SIT测试环境",
        "employee_page": "/#/personnel/staffManagement/staffFile",
    },
    "uat": {
        "url": "http://uat.fj.dtsimple.pro",
        "name": "UAT验收环境",
        "employee_page": "/#/personnel/staffManagement/staffFile",
    },
    "xinji": {
        "url": "http://bak.xinji.dtsimple.pro",
        "name": "新基(柬埔寨)",
        "employee_page": "/#/personnel/staffManagement/staffFile",
    },
    "jingmen": {
        "url": "http://bak.jmym.dtsimple.pro",
        "name": "荆门鹰美",
        "employee_page": "/#/personnel/staffManagement/staffFile",
    },
    "ajn": {
        "url": "http://bak.ajn.dtsimple.pro",
        "name": "安吉纳",
        "employee_page": "/#/personnel/staffManagement/staffFile",
    },
}

OUTPUT_DIR = Path(__file__).parent / "extracted_data"
OUTPUT_DIR.mkdir(exist_ok=True)

# Import template lookup
SKILL_ROOT = Path(__file__).parent.parent.parent.parent.parent  # up to .claude/skills
ATTENDANCE_DIR = Path(__file__).parent.parent  # attendance-full/
TEMPLATE_DIR = OUTPUT_DIR


def get_env(env_name: str) -> dict:
    """Get environment config by name. Defaults to sit."""
    env = ENVIRONMENTS.get(env_name)
    if not env:
        print(f"Unknown env '{env_name}'. Available: {list(ENVIRONMENTS.keys())}")
        sys.exit(1)
    return env


def extract_employees(env: dict) -> list[dict]:
    """Extract employee {工号, 姓名} from staff archive."""
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

        # Navigate to employee archive
        page.goto(f"{env['url']}{env['employee_page']}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        if "ErrorPage" in page.title():
            print(f"Employee page not accessible at {env['employee_page']}")
            browser.close()
            return []

        # Click query
        for i in range(page.locator("button:visible").count()):
            try:
                if "查" in page.locator("button:visible").nth(i).inner_text():
                    page.locator("button:visible").nth(i).click()
                    break
            except:
                pass
        page.wait_for_timeout(3000)

        # Identify column indices from headers
        headers = page.locator(".ant-table-thead th").all_inner_texts()
        headers = [h.strip() for h in headers if h.strip()]
        id_col = next((i for i, h in enumerate(headers) if "工号" in h), 0) + 1  # +1 for selection col
        name_col = next((i for i, h in enumerate(headers) if "姓名" in h), 1) + 1

        # Get total count
        total_el = page.locator(".ant-pagination-total-text").first
        total = 0
        if total_el.count() > 0:
            import re
            nums = re.findall(r'\d+', total_el.inner_text())
            total = int(nums[-1]) if nums else 0

        # Extract
        employees = []
        for page_num in range(1, min(6, (total // 50) + 2)):
            if page_num > 1:
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

        browser.close()
        return employees


def main():
    env_name = "sit"
    if len(sys.argv) > 2 and sys.argv[1] == "--env":
        env_name = sys.argv[2]

    env = get_env(env_name)
    print(f"Environment: {env['name']} ({env['url']})")

    # Extract
    employees = extract_employees(env)
    if not employees:
        print("No employees extracted — page may not be accessible")
        return

    # Save per-environment
    out_path = OUTPUT_DIR / f"employees_{env_name}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(employees, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved {len(employees)} employees to {out_path}")
    print(f"  Sample: 工号={employees[0]['工号']}, 姓名={employees[0]['姓名']}")


if __name__ == "__main__":
    main()
