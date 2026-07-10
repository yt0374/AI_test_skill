"""IMS ERP Attendance — Page Object Model Helpers

Reusable page interaction patterns for IMS attendance pages.
"""

from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Base page with common IMS ERP interactions."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str):
        """Navigate to a path relative to base URL."""
        self.page.goto(path)
        self.page.wait_for_load_state("networkidle")

    def select_dropdown(self, label: str, value: str):
        """Select a value from a labeled dropdown."""
        dropdown = self.page.locator(f'select:has(option:first-child:text-is("{label}"))')
        if dropdown.count() == 0:
            # Try alternative: find by preceding label
            dropdown = self.page.locator(f'label:has-text("{label}") + select')
        dropdown.select_option(value)

    def fill_date_range(self, prefix: str, start: str, end: str):
        """Fill a date range field (start/end dates)."""
        date_inputs = self.page.locator('input[type="date"]')
        if date_inputs.count() >= 2:
            date_inputs.nth(0).fill(start)
            date_inputs.nth(1).fill(end)

    def click_button(self, text: str):
        """Click a button by its visible text."""
        btn = self.page.locator(f'button:has-text("{text}")')
        btn.click()

    def confirm_dialog(self, accept: bool = True):
        """Handle confirm dialog."""
        self.page.on("dialog", lambda dialog: dialog.accept() if accept else dialog.dismiss())

    def wait_for_toast(self, text: str, timeout: int = 5000):
        """Wait for a toast/notification message."""
        toast = self.page.locator(f'.toast:has-text("{text}"), .message:has-text("{text}"), .notification:has-text("{text}")')
        expect(toast.first).to_be_visible(timeout=timeout)


class AttendanceRegistrationPage(BasePage):
    """考勤登记页面"""

    def query(self, date_start: str, date_end: str, group: str = None):
        self.fill_date_range("考勤日期", date_start, date_end)
        if group:
            self.select_dropdown("组别", group)
        self.click_button("查询")

    def delete_record(self, row_index: int = 0):
        """Delete a record (non-system source)."""
        self.page.locator('table tbody tr').nth(row_index).locator('button:has-text("删除")').click()
        self.confirm_dialog(accept=True)


class DailyStatisticsPage(BasePage):
    """日考勤统计页面"""

    def query(self, date_start: str, date_end: str, exception: str = None):
        self.fill_date_range("日期", date_start, date_end)
        if exception:
            self.select_dropdown("考勤异常", exception)
        self.click_button("查询")

    def quick_mend_early_start(self, row_index: int = 0):
        """Click 早班上班补卡 button on a row."""
        self.page.locator('table tbody tr').nth(row_index).locator('button:has-text("早班上班补卡")').click()

    def batch_mend(self, date: str, shift: str, mend_type: str):
        """Open batch mend dialog and configure."""
        self.click_button("补卡")
        # Validate same date/shift check
        self.select_dropdown("补卡类型", mend_type)


class LeaveRegistrationPage(BasePage):
    """请假登记页面"""

    def add_leave(self, employee: str, leave_type: str, duration: str,
                  start_date: str, end_date: str, reason: str = ""):
        self.click_button("新增")
        # Fill employee (fuzzy match input)
        self.page.locator('input[placeholder*="员工"]').first.fill(employee)
        self.select_dropdown("假类", leave_type)
        self.select_dropdown("请假时长", duration)
        if reason:
            self.page.locator('textarea[placeholder*="事由"]').first.fill(reason)
        # Fill dates
        date_inputs = self.page.locator('input[type="date"]')
        if date_inputs.count() >= 2:
            date_inputs.nth(0).fill(start_date)
            date_inputs.nth(1).fill(end_date)
        self.click_button("确认")

    def reverse_effective(self, row_index: int = 0):
        """反生效 a leave record."""
        self.page.locator('table tbody tr').nth(row_index).locator('button:has-text("反生效")').click()
        self.confirm_dialog(accept=True)


class ReturnWorkPage(BasePage):
    """回工登记页面"""

    def add_return_work(self, date: str, duration: str, dept: str, group: str):
        self.click_button("新增")
        self.select_dropdown("回工时长", duration)
        self.select_dropdown("部门", dept)
        self.select_dropdown("组别", group)
        # Select employees
        self.click_button("全选")
        self.click_button("确认")

    def make_effective(self, row_index: int = 0):
        """生效 a draft return work record."""
        self.page.locator('table tbody tr').nth(row_index).locator('button:has-text("生效")').click()
