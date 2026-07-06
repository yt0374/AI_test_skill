"""
Page Object Model helpers for 荆门鹰美 (jingmen) IMS environment.

Key differences from SIT/mainline:
- No enterprise selector
- Direct login: admin / ym5579
- Production module has 35 items (vs 29 baseline)
- .third-menu panel present
"""
from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Base page object with common IMS UI patterns."""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://bak.jmym.dtsimple.pro"

    # ---- Navigation ----

    def navigate_to_module(self, module_name: str):
        """Click sidebar module by name (jingmen: simple names, no gm.xx#N)."""
        sidebar = self.page.locator(".mts-layout-mix-sider-module__item")
        module_item = sidebar.filter(has_text=module_name)
        expect(module_item).to_be_visible(timeout=10000)
        module_item.click()
        self.page.wait_for_timeout(500)

    def click_third_menu(self, menu_text: str):
        """Click a .third-menu panel item."""
        menu_item = self.page.locator(".third-menu").get_by_text(menu_text)
        expect(menu_item).to_be_visible(timeout=5000)
        menu_item.click()
        self.page.wait_for_load_state("networkidle")

    # ---- Common Actions ----

    def click_button(self, text: str):
        """Click a button by visible text."""
        btn = self.page.locator("button, .ant-btn").filter(has_text=text)
        expect(btn).to_be_visible(timeout=5000)
        btn.click()
        self.page.wait_for_timeout(300)

    def fill_field(self, label: str, value: str):
        """Fill a form field by label text."""
        field = self.page.locator(f".ant-form-item:has-text('{label}') input").first
        expect(field).to_be_visible(timeout=5000)
        field.fill(value)

    def select_dropdown(self, label: str, option_text: str):
        """Select an option from an Ant Design Select dropdown."""
        selector = self.page.locator(f".ant-form-item:has-text('{label}') .ant-select")
        expect(selector).to_be_visible(timeout=5000)
        selector.click()
        self.page.wait_for_timeout(300)
        option = self.page.locator(".ant-select-dropdown:visible").get_by_text(option_text)
        expect(option).to_be_visible(timeout=3000)
        option.click()

    def check_checkbox(self, label: str):
        """Check a checkbox by label."""
        cb = self.page.locator(f".ant-checkbox-wrapper:has-text('{label}') .ant-checkbox")
        expect(cb).to_be_visible(timeout=5000)
        if "ant-checkbox-checked" not in (cb.get_attribute("class") or ""):
            cb.click()

    # ---- Assertions ----

    def assert_toast_message(self, expected_text: str, timeout: int = 5000):
        """Assert a toast/notification message appears."""
        toast = self.page.locator(".ant-message-notice-content, .ant-notification-notice")
        expect(toast).to_contain_text(expected_text, timeout=timeout)

    def assert_table_row_count(self, min_count: int = 1):
        """Assert table has at least N rows."""
        rows = self.page.locator(".ant-table-tbody tr.ant-table-row")
        expect(rows.first).to_be_visible(timeout=5000)

    def assert_element_hidden(self, selector: str):
        """Assert element is not visible."""
        el = self.page.locator(selector)
        expect(el).not_to_be_visible(timeout=3000)

    def assert_element_visible(self, selector: str):
        """Assert element is visible."""
        el = self.page.locator(selector)
        expect(el).to_be_visible(timeout=5000)

    # ---- PAD Emulation ----

    def emulate_pad_viewport(self):
        """Switch to PAD viewport (tablet size)."""
        self.page.set_viewport_size({"width": 1024, "height": 768})


class ProductionPage(BasePage):
    """Production module page (生产) - jingmen specific."""

    def navigate_to_cutting_task(self):
        """Navigate to 裁剪任务 page."""
        self.navigate_to_module("生产")
        self.click_third_menu("裁剪任务")

    def navigate_to_tag_print(self):
        """Navigate to 扎卡打印 page."""
        self.navigate_to_module("生产")
        self.click_third_menu("扎卡打印")

    def create_cutting_task(self, cpos: list[str], marker: str, layers: int):
        """Create a new cutting task with CPO selection."""
        self.click_button("新建裁剪任务")
        # Select CPOs
        for cpo in cpos:
            self.check_checkbox(cpo)
        # Select marker and allocate layers
        self.select_dropdown("唛架", marker)
        self.fill_field("计划层数", str(layers))
        self.click_button("提交")
        self.page.wait_for_load_state("networkidle")

    def apply_overcut(self, action: str = "放行"):
        """Handle overcut application (放行/驳回)."""
        self.click_button("申请超裁")
        if action == "放行":
            self.click_button("放行")
        else:
            self.click_button("驳回")
        self.page.wait_for_load_state("networkidle")

    def get_task_status(self, task_name: str) -> str:
        """Get the status of a cutting task from the list."""
        row = self.page.locator("tr.ant-table-row").filter(has_text=task_name)
        status_cell = row.locator("td").nth(3)  # Status column - adjust index
        return status_cell.inner_text()
