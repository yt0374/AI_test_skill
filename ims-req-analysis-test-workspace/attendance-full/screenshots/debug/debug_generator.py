"""Quick debug: test the generator pipeline step by step."""
import sys
sys.path.insert(0, "erp_tests")

from playwright.sync_api import sync_playwright
from utils.test_data_generator import (
    _extract_available_employees,
    _generate_excel,
    _upload_excel,
    generate_and_import,
)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    # Login
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
        print("Logged in")

    # Run the pipeline
    ds = generate_and_import(page)
    print(f"\nResult: {ds['metadata']['total_records']} records, "
          f"normal={ds['summary'].get('normal', 0)}")

    browser.close()
