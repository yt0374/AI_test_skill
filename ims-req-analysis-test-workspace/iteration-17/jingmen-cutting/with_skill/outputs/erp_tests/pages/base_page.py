"""Page Object Model base class for Jingmen IMS ERP.

Provides common page interaction patterns used across all modules.
"""
from playwright.sync_api import Page, Locator, expect
from typing import Optional


class BasePage:
    """Base page with shared UI patterns for the IMS ERP system."""

    # Common selectors (Jingmen environment)
    SIDEBAR_MODULE = ".mts-layout-mix-sider-module__item"
    THIRD_MENU = ".third-menu"
    SEARCH_BTN = "button:has-text('查询')"
    RESET_BTN = "button:has-text('重置')"
    MORE_FILTER_BTN = "button:has-text('更多筛选')"
    SAVE_BTN = "button:has-text('保存')"
    CONFIRM_BTN = ".ant-modal button:has-text('确定')"
    CANCEL_BTN = ".ant-modal button:has-text('取消')"
    SUCCESS_TOAST = ".ant-message-success"
    ERROR_TOAST = ".ant-message-error"
    TABLE_ROW = ".ant-table-tbody tr.ant-table-row"
    FORM_ITEM = ".ant-form-item"

    def __init__(self, page: Page):
        self.page = page

    # --- Navigation ---
    def navigate_to_module(self, module_name: str):
        """Click a module in the sidebar."""
        item = self.page.locator(self.SIDEBAR_MODULE, has_text=module_name)
        item.click()
        self.page.wait_for_timeout(800)

    def click_third_menu(self, *items: str):
        """Navigate through third-menu hierarchy."""
        for item in items:
            menu = self.page.locator(self.THIRD_MENU).locator(f"text={item}")
            menu.click()
            self.page.wait_for_timeout(500)

    # --- Search / Filter ---
    def click_search(self):
        self.page.locator(self.SEARCH_BTN).click()
        self.page.wait_for_timeout(1000)

    def click_reset(self):
        self.page.locator(self.RESET_BTN).click()

    def fill_field(self, label: str, value: str):
        """Fill a form field by its label text."""
        item = self.page.locator(self.FORM_ITEM, has_text=label)
        input_el = item.locator("input, textarea, .ant-select")
        input_el.click()
        self.page.wait_for_timeout(300)
        input_el.fill(value)

    # --- CRUD ---
    def click_save(self):
        self.page.locator(self.SAVE_BTN).click()
        self.page.wait_for_timeout(500)

    def click_add(self):
        self.page.locator("button:has-text('新增')").click()
        self.page.wait_for_timeout(1000)

    def click_edit(self):
        self.page.locator("button:has-text('编辑')").click()
        self.page.wait_for_timeout(500)

    def click_delete(self):
        self.page.locator("button:has-text('删除')").click()
        self.page.wait_for_timeout(500)

    def confirm_dialog(self):
        self.page.locator(self.CONFIRM_BTN).click()
        self.page.wait_for_timeout(500)

    def cancel_dialog(self):
        self.page.locator(self.CANCEL_BTN).click()
        self.page.wait_for_timeout(500)

    # --- Assertions ---
    def expect_success_toast(self, message: str = None):
        toast = self.page.locator(self.SUCCESS_TOAST)
        expect(toast).to_be_visible(timeout=5000)
        if message:
            expect(toast).to_contain_text(message)

    def expect_error_toast(self, message: str = None):
        toast = self.page.locator(self.ERROR_TOAST)
        expect(toast).to_be_visible(timeout=5000)
        if message:
            expect(toast).to_contain_text(message)

    def expect_table_has_rows(self, min_rows: int = 1):
        rows = self.page.locator(self.TABLE_ROW)
        expect(rows).to_have_count(min_rows, timeout=5000)

    def expect_button_visible(self, text: str):
        btn = self.page.locator(f"button:has-text('{text}')")
        expect(btn).to_be_visible()

    def expect_button_hidden(self, text: str):
        btn = self.page.locator(f"button:has-text('{text}')")
        expect(btn).to_be_hidden()

    def expect_status_in_table(self, status: str):
        cell = self.page.locator(self.TABLE_ROW).first.locator("td", has_text=status)
        expect(cell).to_be_visible()

    def click_table_row(self, text: str):
        """Click the first table row containing the given text."""
        row = self.page.locator(self.TABLE_ROW, has_text=text).first
        row.click()
        self.page.wait_for_timeout(500)

    # --- PAD-specific (simulated on PC viewport) ---
    def pad_click_button(self, text: str):
        """Click a PAD-style button (may be a card or large touch target)."""
        btn = self.page.locator(f"button:has-text('{text}'), .card:has-text('{text}')")
        btn.click()
        self.page.wait_for_timeout(500)

    def pad_scan_barcode(self, barcode: str):
        """Simulate barcode scanning by pasting into scan input."""
        scan_input = self.page.locator("input[placeholder*='扫描'], input[placeholder*='条码']")
        scan_input.fill(barcode)
        scan_input.press("Enter")
        self.page.wait_for_timeout(500)

    def pad_input_number(self, label: str, value: int):
        """Fill a numeric input field on PAD interface."""
        item = self.page.locator(self.FORM_ITEM, has_text=label)
        input_el = item.locator("input[type='number'], input")
        input_el.fill(str(value))
        self.page.wait_for_timeout(300)
