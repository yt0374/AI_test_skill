"""Last attempt: capture ALL IMS routes by intercepting menu API data."""
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    # Intercept network requests to find menu/route data
    menu_data = []

    def handle_response(response):
        url = response.url
        if any(kw in url for kw in ['menu', 'Menu', 'nav', 'route', 'permission', 'module']):
            try:
                body = response.json()
                menu_data.append({"url": url, "body_keys": list(body.keys()) if isinstance(body, dict) else type(body).__name__,
                                  "body_preview": str(body)[:300]})
            except:
                pass

    page.on("response", handle_response)

    page.goto("http://test.fj.dtsimple.pro/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    if "/login" in page.url:
        page.fill("#form_item_username", "admin")
        page.fill("#form_item_password", "metas2660")
        sel = page.locator(".ant-select")
        if sel.count() > 0:
            sel.first.click()
            page.wait_for_timeout(800)
            page.locator(".ant-select-item-option-content").first.click()
        page.click(".ant-btn-primary")
        page.wait_for_timeout(5000)
        page.wait_for_load_state("networkidle")

    print("=== Menu/Route API calls ===")
    for item in menu_data:
        print(f"  URL: {item['url']}")
        print(f"  Keys: {item['body_keys']}")
        print(f"  Preview: {item['body_preview'][:500]}")
        print()

    # Also try to access all available routes from the Vue router
    all_routes = page.evaluate("""() => {
        try {
            const app = document.querySelector('#app').__vue_app__;
            const router = app.config.globalProperties.$router;
            const routes = router.getRoutes();
            return JSON.stringify(routes.map(r => ({path: r.path, name: r.name, meta: r.meta})));
        } catch(e) {
            return 'Error: ' + e.message;
        }
    }""")
    print(f"All router routes: {all_routes[:2000]}")

    # Try accessing the menu/permission store
    store_data = page.evaluate("""() => {
        try {
            const app = document.querySelector('#app').__vue_app__;
            const pinia = app.config.globalProperties.$pinia;
            if (pinia) {
                const stores = pinia._s;
                const storeInfo = {};
                for (const [id, store] of stores) {
                    storeInfo[id] = Object.keys(store.$state || {}).slice(0, 20);
                }
                return JSON.stringify({type: 'pinia', stores: storeInfo});
            }
        } catch(e) {}
        try {
            // Try Vuex
            const app = document.querySelector('#app').__vue_app__;
            const store = app.config.globalProperties.$store;
            if (store) {
                return JSON.stringify({type: 'vuex', state: Object.keys(store.state || {}).slice(0, 20)});
            }
        } catch(e) {}
        return 'No store found';
    }""")
    print(f"Store: {store_data}")

    browser.close()
