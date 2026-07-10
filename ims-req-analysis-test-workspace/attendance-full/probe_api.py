"""Catch the actual import API by triggering Excel upload in UI."""
from playwright.sync_api import sync_playwright
import json

UPLOAD_APIS = []

def capture_req(request):
    url = request.url
    if "/api/" in url and request.method == "POST":
        try:
            body = request.post_data
            if body:
                UPLOAD_APIS.append({"url": url, "body": body[:500]})
        except:
            pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.on("request", capture_req)

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

    # Clear previous APIs
    UPLOAD_APIS.clear()

    # Go to 考勤登记
    page.goto("http://test.fj.dtsimple.pro/#/personnel/workAttendance/detail")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # Find and click Excel导入
    for btn_text in ["Excel导入", "导入", "Txt导入"]:
        btns = page.locator(f"button:has-text('{btn_text}')")
        if btns.count() > 0:
            print(f"Clicked '{btn_text}'")
            btns.first.click()
            page.wait_for_timeout(2000)
            break

    # Upload file
    file_input = page.locator("input[type='file']")
    if file_input.count() > 0:
        print("Uploading Excel...")
        file_input.first.set_input_files(
            str("erp_tests/utils/extracted_data/test_attendance_import.xlsx")
        )
        page.wait_for_timeout(3000)

    # Click any confirm buttons
    for sel in ["button:has-text('确认')", ".ant-btn-primary", "button:has-text('导入')", "button:has-text('确定')"]:
        btn = page.locator(sel).first
        if btn.count() > 0:
            try:
                btn.click(timeout=3000)
                page.wait_for_timeout(3000)
                print(f"Clicked '{sel}'")
            except:
                pass

    page.wait_for_timeout(5000)
    browser.close()

    print(f"\n=== Upload APIs ({len(UPLOAD_APIS)}) ===")
    for api in UPLOAD_APIS:
        print(f"  {api['url']}")
        print(f"  Body: {api['body'][:300]}")
        print()
