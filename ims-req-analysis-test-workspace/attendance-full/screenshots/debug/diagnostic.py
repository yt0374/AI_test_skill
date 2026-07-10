"""Quick diagnostic: capture IMS SIT page structure."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://test.fj.dtsimple.pro/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    url = page.url
    title = page.title()
    print(f"URL: {url}")
    print(f"Title: {title}")

    # Check for login elements
    for sel in ["#form_item_username", "#form_item_password",
                "input[type='text']", "input[type='password']",
                ".ant-input", ".ant-btn-primary",
                "text=登录", "text=麦塔西"]:
        count = page.locator(sel).count()
        if count > 0:
            print(f"  {sel}: {count} found")

    # Get sidebar modules
    sidebar = page.locator(".mts-layout-mix-sider-module__item")
    print(f"\nSidebar modules: {sidebar.count()}")
    for i in range(min(sidebar.count(), 5)):
        text = sidebar.nth(i).inner_text()
        print(f"  [{i}] {text}")

    # Check for 人事 module
    renshi = page.locator("text=人事")
    if renshi.count() > 0:
        print("\n✓ '人事' module found!")

    # Screenshot for debugging
    page.screenshot(path="diagnostic_screenshot.png")
    print("\nScreenshot saved to diagnostic_screenshot.png")

    browser.close()
