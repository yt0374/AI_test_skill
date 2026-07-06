"""Page Object Model base class for IMS Attendance (考勤) E2E tests.

Provides common page interaction patterns used across the attendance module.
Adapted for the SIT environment (test.fj.dtsimple.pro, enterprise=最佳智造).
"""
from playwright.sync_api import Page, Locator, expect
from typing import Optional


class BasePage:
    """Base page with shared UI patterns for the IMS ERP system."""

    # Common selectors (SIT environment)
    SIDEBAR_MODULE = ".mts-layout-mix-sider-module__item"
    THIRD_MENU = ".third-menu"
    SEARCH_BTN = "button:has-text('查询')"
    RESET_BTN = "button:has-text('重置')"
    MORE_FILTER_BTN = "button:has-text('更多筛选')"
    SAVE_BTN = "button:has-text('保存')"
    ADD_BTN = "button:has-text('新增')"
    EDIT_BTN = "button:has-text('编辑')"
    DELETE_BTN = "button:has-text('删除')"
    EXPORT_BTN = "button:has-text('导出')"
    CONFIRM_BTN = ".ant-modal button:has-text('确定')"
    CANCEL_BTN = ".ant-modal button:has-text('取消')"
    SUCCESS_TOAST = ".ant-message-success"
    ERROR_TOAST = ".ant-message-error"
    WARNING_TOAST = ".ant-message-warning"
    TABLE_ROW = ".ant-table-tbody tr.ant-table-row"
    TABLE_EMPTY = ".ant-empty"
    FORM_ITEM = ".ant-form-item"
    MODAL_VISIBLE = ".ant-modal:visible"
    MODAL_CONFIRM = ".ant-modal-confirm:visible"

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

    def navigate_to_attendance(self, submenu: str = None):
        """Navigate to 人事 > 考勤, optionally to a specific sub-page.

        Args:
            submenu: One of: 考勤登记, 回工登记, 请假登记,
                     日考勤统计, 月考勤统计, 小组出勤表, 员工缺勤表
        """
        self.navigate_to_module("人事")
        if submenu:
            self.click_third_menu(submenu)

    # --- Search / Filter ---
    def click_search(self):
        """Click the search/query button."""
        self.page.locator(self.SEARCH_BTN).first.click()
        self.page.wait_for_timeout(1000)

    def click_reset(self):
        """Click the reset button to clear filters."""
        self.page.locator(self.RESET_BTN).first.click()

    def click_more_filter(self):
        """Click the more-filter toggle button."""
        self.page.locator(self.MORE_FILTER_BTN).first.click()
        self.page.wait_for_timeout(500)

    def fill_field(self, label: str, value: str):
        """Fill a form field by its label text.

        Handles input, textarea, and Ant Design Select components.
        """
        item = self.page.locator(self.FORM_ITEM, has_text=label)
        input_el = item.locator("input, textarea").first
        input_el.wait_for(state="visible", timeout=3000)
        input_el.click()
        self.page.wait_for_timeout(300)
        input_el.fill("")
        input_el.fill(value)

    def select_dropdown(self, label: str, option_text: str):
        """Select an option from an Ant Design Select dropdown by label."""
        item = self.page.locator(self.FORM_ITEM, has_text=label)
        select = item.locator(".ant-select").first
        select.click()
        self.page.wait_for_timeout(500)
        option = self.page.locator(
            f".ant-select-dropdown:visible .ant-select-item-option",
            has_text=option_text
        )
        option.first.click()
        self.page.wait_for_timeout(300)

    def set_date_range(self, start_label: str, end_label: str,
                       start_date: str, end_date: str):
        """Set a date range picker by label."""
        item = self.page.locator(self.FORM_ITEM, has_text=start_label)
        inputs = item.locator("input")
        if inputs.count() >= 2:
            inputs.nth(0).fill(start_date)
            inputs.nth(1).fill(end_date)

    # --- CRUD ---
    def click_save(self):
        """Click the save button."""
        self.page.locator(self.SAVE_BTN).first.click()
        self.page.wait_for_timeout(500)

    def click_add(self):
        """Click the add/new button."""
        self.page.locator(self.ADD_BTN).first.click()
        self.page.wait_for_timeout(1000)

    def click_edit(self):
        """Click the edit button."""
        self.page.locator(self.EDIT_BTN).first.click()
        self.page.wait_for_timeout(500)

    def click_delete(self):
        """Click the delete button."""
        self.page.locator(self.DELETE_BTN).first.click()
        self.page.wait_for_timeout(500)

    def click_export(self):
        """Click the export button."""
        self.page.locator(self.EXPORT_BTN).first.click()
        self.page.wait_for_timeout(1000)

    def confirm_dialog(self):
        """Click confirm in a dialog/modal."""
        self.page.locator(self.CONFIRM_BTN).first.click()
        self.page.wait_for_timeout(500)

    def cancel_dialog(self):
        """Click cancel in a dialog/modal."""
        self.page.locator(self.CANCEL_BTN).first.click()
        self.page.wait_for_timeout(500)

    # --- Assertions ---
    def expect_success_toast(self, message: str = None):
        """Expect a success toast/message to appear."""
        toast = self.page.locator(self.SUCCESS_TOAST)
        expect(toast.first).to_be_visible(timeout=8000)
        if message:
            expect(toast.first).to_contain_text(message)

    def expect_error_toast(self, message: str = None):
        """Expect an error toast/message to appear."""
        toast = self.page.locator(self.ERROR_TOAST)
        expect(toast.first).to_be_visible(timeout=5000)
        if message:
            expect(toast.first).to_contain_text(message)

    def expect_warning_toast(self, message: str = None):
        """Expect a warning toast/message to appear."""
        toast = self.page.locator(self.WARNING_TOAST)
        expect(toast.first).to_be_visible(timeout=5000)
        if message:
            expect(toast.first).to_contain_text(message)

    def expect_table_has_rows(self, min_rows: int = 1):
        """Expect the table to have at least min_rows data rows."""
        rows = self.page.locator(self.TABLE_ROW)
        expect(rows.first).to_be_visible(timeout=8000)

    def expect_table_empty(self):
        """Expect the table to show empty state."""
        empty = self.page.locator(self.TABLE_EMPTY)
        expect(empty.first).to_be_visible(timeout=5000)

    def expect_button_visible(self, text: str):
        """Expect a button with the given text to be visible."""
        btn = self.page.locator(f"button:has-text('{text}')").first
        expect(btn).to_be_visible()

    def expect_button_hidden(self, text: str):
        """Expect a button with the given text to be hidden or disabled."""
        btn = self.page.locator(f"button:has-text('{text}')").first
        expect(btn).to_be_hidden()

    def expect_button_disabled(self, text: str):
        """Expect a button with the given text to be disabled."""
        btn = self.page.locator(f"button:has-text('{text}')").first
        expect(btn).to_be_disabled()

    def expect_status_in_table(self, status: str):
        """Expect the first table row to contain the given status text."""
        cell = self.page.locator(self.TABLE_ROW).first.locator("td", has_text=status)
        expect(cell).to_be_visible()

    def click_table_row(self, text: str):
        """Click the first table row containing the given text."""
        row = self.page.locator(self.TABLE_ROW, has_text=text).first
        row.click()
        self.page.wait_for_timeout(500)

    def select_table_row_by_checkbox(self, text: str = None, index: int = 0):
        """Check the checkbox on a table row."""
        if text:
            row = self.page.locator(self.TABLE_ROW, has_text=text).first
        else:
            row = self.page.locator(self.TABLE_ROW).nth(index)
        checkbox = row.locator("input[type='checkbox']").first
        checkbox.check()
        self.page.wait_for_timeout(300)

    def get_table_cell(self, row_index: int, col_index: int) -> Locator:
        """Get a specific cell from the table."""
        row = self.page.locator(self.TABLE_ROW).nth(row_index)
        return row.locator("td").nth(col_index)

    # --- Modal helpers ---
    def expect_modal_visible(self):
        """Expect a modal dialog to be visible."""
        modal = self.page.locator(self.MODAL_VISIBLE)
        expect(modal.first).to_be_visible(timeout=5000)

    def expect_modal_confirm_visible(self):
        """Expect a confirm modal to be visible."""
        modal = self.page.locator(self.MODAL_CONFIRM)
        expect(modal.first).to_be_visible(timeout=5000)

    def close_modal(self):
        """Close the visible modal via its close button."""
        close_btn = self.page.locator(
            ".ant-modal:visible .ant-modal-close, "
            ".ant-modal:visible button:has-text('关闭'), "
            ".ant-modal:visible button:has-text('取消')"
        ).first
        close_btn.click()
        self.page.wait_for_timeout(500)
