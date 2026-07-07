"""Page Object Model base page for IMS ERP."""
from playwright.sync_api import Page, expect


class BasePage:
    """Base page with common IMS ERP interactions."""

    def __init__(self, page: Page):
        self.page = page

    # -- Navigation --
    def navigate_to_module(self, module_name: str):
        """Click a sidebar module by its text content."""
        self.page.wait_for_selector(".mts-layout-mix-sider-module__item", timeout=15000)
        modules = self.page.locator(".mts-layout-mix-sider-module__item")
        modules.filter(has_text=module_name).first.click()
        self.page.wait_for_timeout(500)

    def navigate_to_submenu(self, submenu_text: str):
        """Click a sub-menu item (third-menu panel for jingmen)."""
        self.page.wait_for_selector(".third-menu", timeout=10000)
        item = self.page.locator(".third-menu").locator(f"text={submenu_text}")
        item.first.click()
        self.page.wait_for_timeout(500)

    def navigate_to_report(self, report_name: str):
        """Navigate directly to a report in the reports module."""
        self.navigate_to_module("报表")
        self.page.wait_for_timeout(1000)
        # Try to find and click the report link
        report_link = self.page.get_by_text(report_name, exact=False)
        if report_link.count() > 0:
            report_link.first.click()
            self.page.wait_for_load_state("domcontentloaded")
        return self

    # -- Common interactions --
    def click_button(self, button_text: str):
        """Click a button by its text."""
        btn = self.page.locator("button").filter(has_text=button_text).first
        btn.click()
        self.page.wait_for_timeout(500)

    def fill_field(self, label: str, value: str):
        """Fill a form field by its label text."""
        field = self.page.locator(f".ant-form-item:has-text('{label}') input").first
        field.fill(value)

    def select_date_range(self, start_date: str, end_date: str):
        """Select date range in a date picker."""
        start_input = self.page.locator("input[placeholder='开始日期']").first
        if start_input.count() > 0:
            start_input.fill(start_date)
        end_input = self.page.locator("input[placeholder='结束日期']").first
        if end_input.count() > 0:
            end_input.fill(end_date)

    def wait_for_table(self, timeout: int = 15000):
        """Wait for the Ant Design table to load."""
        self.page.wait_for_selector(".ant-table-tbody", timeout=timeout)
        self.page.wait_for_timeout(500)

    def get_table_rows(self):
        """Get all rows from the currently visible Ant Design table."""
        return self.page.locator(".ant-table-tbody tr.ant-table-row")

    def get_table_cell(self, row_index: int, col_index: int):
        """Get text content of a specific table cell."""
        rows = self.get_table_rows()
        cells = rows.nth(row_index).locator("td")
        return cells.nth(col_index).text_content()

    def get_column_headers(self):
        """Get all column header texts."""
        headers = self.page.locator(".ant-table-thead th")
        return [h.text_content() for h in headers.all()]

    def assert_table_has_columns(self, expected_columns: list):
        """Assert the table contains all expected column headers."""
        actual_headers = self.get_column_headers()
        for col in expected_columns:
            assert any(col in h for h in actual_headers), \
                f"Column '{col}' not found in headers: {actual_headers}"

    def assert_page_loaded(self, expected_text: str = None):
        """Assert page has loaded correctly."""
        if expected_text:
            expect(self.page.locator("body")).to_contain_text(expected_text, timeout=15000)

    def close_modal(self):
        """Close any open modal/dialog."""
        modal_close = self.page.locator(".ant-modal-close").first
        if modal_close.is_visible():
            modal_close.click()
            self.page.wait_for_timeout(300)

    def take_screenshot(self, name: str):
        """Take a screenshot for debugging/reporting."""
        self.page.screenshot(path=f"screenshots/{name}.png", full_page=True)
