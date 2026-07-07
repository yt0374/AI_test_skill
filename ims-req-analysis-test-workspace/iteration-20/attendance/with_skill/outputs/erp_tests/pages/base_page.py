# erp_tests/pages/base_page.py — Page Object Model helpers for 考勤模块
"""Base page object with common actions for attendance module."""

from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Common page actions shared across all attendance pages."""

    def __init__(self, page: Page):
        self.page = page

    def wait_for_table(self, timeout: int = 10_000):
        """Wait for the ant-design table to render."""
        self.page.wait_for_selector(".ant-table", timeout=timeout)

    def click_button(self, text: str):
        """Click a button by its text content."""
        btn = self.page.locator(f".ant-btn:has-text('{text}')")
        btn.click()
        self.page.wait_for_timeout(300)

    def confirm_dialog(self, confirm: bool = True):
        """Handle ant-design modal confirm/cancel."""
        if confirm:
            self.page.click(".ant-modal-confirm-btns .ant-btn-primary")
        else:
            self.page.click(".ant-modal-confirm-btns .ant-btn:not(.ant-btn-primary)")

    def expect_message(self, text: str):
        """Assert a message/toast is visible."""
        expect(self.page.locator(f".ant-message:has-text('{text}')")).to_be_visible(
            timeout=5_000
        )

    def expect_modal_text(self, text: str):
        """Assert modal body contains text."""
        expect(
            self.page.locator(f".ant-modal-body:has-text('{text}')")
        ).to_be_visible()

    def fill_date_range(self, start_field_label: str, end_field_label: str,
                        start_date: str, end_date: str):
        """Fill a date range picker (Ant Design RangePicker)."""
        # Click the date range input
        self.page.click(f".ant-picker-range")
        # Clear and fill start
        start_input = self.page.locator(".ant-picker-range input").first
        start_input.fill(start_date)
        # Fill end
        end_input = self.page.locator(".ant-picker-range input").last
        end_input.fill(end_date)
        self.page.keyboard.press("Enter")

    def select_dropdown(self, field_label: str, option_text: str):
        """Select an option from an ant-select dropdown."""
        # Click the select to open dropdown
        selector = f".ant-select:has(.ant-select-selection-placeholder:has-text('{field_label}')), .ant-select:has(.ant-select-selection-item:has-text('{field_label}'))"
        # Fallback: find by nearby label
        try:
            self.page.locator(selector).click()
        except Exception:
            # Try clicking select near the label
            self.page.locator(f"text={field_label}").locator("..").locator(".ant-select").click()
        self.page.wait_for_timeout(200)
        self.page.click(f".ant-select-item-option-content:has-text('{option_text}')")

    def get_table_rows(self) -> Locator:
        """Get all data rows in the ant-table body."""
        return self.page.locator(".ant-table-tbody tr.ant-table-row")

    def get_column_text(self, row_index: int, column_class: str) -> str:
        """Get text from a specific column in a table row."""
        row = self.get_table_rows().nth(row_index)
        return row.locator(f".{column_class}").inner_text()

    def select_checkbox_by_row(self, row_index: int):
        """Select the checkbox in a specific table row."""
        row = self.get_table_rows().nth(row_index)
        row.locator(".ant-checkbox-input").click()


class AttendanceRegistrationPage(BasePage):
    """考勤登记 page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.module = "考勤登记"

    def query_today(self):
        """Query today's attendance records."""
        self.click_button("查询")


class DailyAttendancePage(BasePage):
    """日考勤统计 page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.module = "日考勤统计"

    def click_quick_fix_morning_in(self):
        """Click 早班上班补卡 button."""
        self.click_button("早班上班补卡")

    def click_quick_fix_morning_out(self):
        """Click 早班下班补卡 button."""
        self.click_button("早班下班补卡")


class LeaveRegistrationPage(BasePage):
    """请假登记 page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.module = "请假登记"


class MonthlyAttendancePage(BasePage):
    """月考勤统计 page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.module = "月考勤统计"
