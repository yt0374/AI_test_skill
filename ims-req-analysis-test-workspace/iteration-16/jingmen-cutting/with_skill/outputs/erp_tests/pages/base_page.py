# =============================================================================
# base_page.py - Page Object Model 基类
# 荆门鹰美裁剪系统 2.0 Playwright 测试项目
# =============================================================================

from typing import Optional, Union, List
from playwright.sync_api import Page, Locator, expect, TimeoutError as PlaywrightTimeoutError


class BasePage:
    """所有 Page Object 的基类，提供通用页面操作封装。

    封装原则:
    - 所有查找使用 locator（惰性求值），不使用 element_handle
    - 所有等待依赖 Playwright 自动等待机制
    - 操作失败抛出明确的中文错误信息
    """

    def __init__(self, page: Page):
        self.page = page
        self._default_timeout = 15000

    # ------------------------------------------------------------------
    # 导航
    # ------------------------------------------------------------------
    def navigate_to(self, url: str, wait_until: str = "domcontentloaded") -> None:
        """导航到指定 URL。

        Args:
            url: 目标路径（相对路径如 /cutting/task 或完整 URL）
            wait_until: 等待策略，默认 domcontentloaded
        """
        self.page.goto(url, wait_until=wait_until)
        self.page.wait_for_load_state(wait_until)

    def navigate_to_relative(self, path: str) -> None:
        """导航到基础 URL 的相对路径。

        Args:
            path: 相对路径，如 /cutting/task
        """
        from utils.test_data import ENV_CONFIG
        full_url = f"{ENV_CONFIG['base_url']}{path}"
        self.navigate_to(full_url)

    def get_current_url(self) -> str:
        """获取当前页面 URL。"""
        return self.page.url

    def reload(self) -> None:
        """刷新页面。"""
        self.page.reload(wait_until="domcontentloaded")

    # ------------------------------------------------------------------
    # 元素交互
    # ------------------------------------------------------------------
    def click_button(
        self,
        selector: str,
        timeout: Optional[int] = None,
        force: bool = False,
    ) -> None:
        """点击按钮。

        Args:
            selector: CSS/XPath/Text 选择器
            timeout: 超时毫秒数，默认使用类级别超时
            force: 是否强制点击（跳过可见性检查）

        Raises:
            AssertionError: 按钮不可见或不可点击时抛出
        """
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=t)
            if not force:
                expect(locator).to_be_enabled(timeout=t)
            locator.click(force=force)
        except (PlaywrightTimeoutError, AssertionError) as e:
            raise AssertionError(f"点击按钮失败 [{selector}]: {e}")

    def fill_input(
        self,
        selector: str,
        value: str,
        clear_first: bool = True,
        timeout: Optional[int] = None,
    ) -> None:
        """填写输入框。

        Args:
            selector: 输入框选择器
            value: 要填入的值
            clear_first: 是否先清空再填写
            timeout: 超时毫秒数
        """
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=t)
            if clear_first:
                locator.clear()
            locator.fill(value)
        except PlaywrightTimeoutError as e:
            raise AssertionError(f"填写输入框失败 [{selector}]: {e}")

    def select_option(
        self,
        selector: str,
        value: Optional[str] = None,
        label: Optional[str] = None,
        index: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> None:
        """选择下拉选项。

        Args:
            selector: 下拉框选择器
            value: 按 option value 选择
            label: 按 option 文本选择
            index: 按索引选择
        """
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=t)
            if value is not None:
                locator.select_option(value=value, timeout=t)
            elif label is not None:
                locator.select_option(label=label, timeout=t)
            elif index is not None:
                locator.select_option(index=index, timeout=t)
        except PlaywrightTimeoutError as e:
            raise AssertionError(f"选择下拉选项失败 [{selector}]: {e}")

    def check_checkbox(self, selector: str, timeout: Optional[int] = None) -> None:
        """勾选复选框（仅在未勾选时操作）。"""
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=t)
        if not locator.is_checked():
            locator.check(timeout=t)

    def uncheck_checkbox(self, selector: str, timeout: Optional[int] = None) -> None:
        """取消勾选复选框（仅在勾选时操作）。"""
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=t)
        if locator.is_checked():
            locator.uncheck(timeout=t)

    # ------------------------------------------------------------------
    # 等待
    # ------------------------------------------------------------------
    def wait_for_toast(
        self,
        expected_text: Optional[str] = None,
        toast_selector: str = ".ant-message-notice-content, .ant-notification-notice, .el-message, .toast, [role='alert']",
        timeout: Optional[int] = None,
    ) -> str:
        """等待 Toast 消息出现并返回其文本内容。

        Args:
            expected_text: 可选，断言 Toast 包含指定文本
            toast_selector: Toast 容器选择器（支持 Ant Design / Element 等常见 UI 库）
            timeout: 超时毫秒数

        Returns:
            Toast 消息文本

        Raises:
            AssertionError: 超时未出现或文本不匹配时抛出
        """
        t = timeout or min(self._default_timeout, 10000)
        locator = self.page.locator(toast_selector).first
        try:
            locator.wait_for(state="visible", timeout=t)
            text = locator.inner_text().strip()
            if expected_text:
                assert expected_text in text, \
                    f"Toast 文本不匹配: 期望包含 '{expected_text}', 实际 '{text}'"
            return text
        except PlaywrightTimeoutError:
            raise AssertionError(f"等待 Toast 超时 [{toast_selector}]")

    def wait_for_element(
        self,
        selector: str,
        state: str = "visible",
        timeout: Optional[int] = None,
    ) -> Locator:
        """等待元素达到指定状态并返回 Locator。

        Args:
            selector: 元素选择器
            state: 目标状态 (attached/visible/hidden/detached)
            timeout: 超时毫秒数

        Returns:
            目标元素的 Locator
        """
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        locator.wait_for(state=state, timeout=t)
        return locator

    def wait_for_url_contains(self, fragment: str, timeout: Optional[int] = None) -> None:
        """等待 URL 包含指定片段。"""
        t = timeout or self._default_timeout
        self.page.wait_for_url(f"**{fragment}**", timeout=t)

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """获取元素文本内容。

        Args:
            selector: 元素选择器
            timeout: 超时毫秒数

        Returns:
            元素 inner_text，去首尾空白
        """
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=t)
            return locator.inner_text().strip()
        except PlaywrightTimeoutError:
            return ""

    def get_text_all(self, selector: str) -> List[str]:
        """获取所有匹配元素的文本列表。"""
        locators = self.page.locator(selector).all()
        return [el.inner_text().strip() for el in locators]

    def get_input_value(self, selector: str, timeout: Optional[int] = None) -> str:
        """获取输入框的当前值。"""
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=t)
        return locator.input_value()

    def get_attribute(
        self,
        selector: str,
        attribute: str,
        timeout: Optional[int] = None,
    ) -> Optional[str]:
        """获取元素属性值。"""
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        try:
            locator.wait_for(state="attached", timeout=t)
            return locator.get_attribute(attribute)
        except PlaywrightTimeoutError:
            return None

    # ------------------------------------------------------------------
    # 状态判断
    # ------------------------------------------------------------------
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """检查元素是否可见。

        Args:
            selector: 元素选择器
            timeout: 超时毫秒数

        Returns:
            True 如果元素可见
        """
        t = timeout or 3000
        try:
            self.page.locator(selector).first.wait_for(state="visible", timeout=t)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_enabled(self, selector: str, timeout: Optional[int] = None) -> bool:
        """检查元素是否可交互（visible + enabled）。"""
        t = timeout or 3000
        try:
            locator = self.page.locator(selector).first
            locator.wait_for(state="visible", timeout=t)
            return locator.is_enabled()
        except PlaywrightTimeoutError:
            return False

    def is_hidden(self, selector: str, timeout: Optional[int] = None) -> bool:
        """检查元素是否隐藏。"""
        t = timeout or 3000
        try:
            self.page.locator(selector).first.wait_for(state="hidden", timeout=t)
            return True
        except (PlaywrightTimeoutError, AssertionError):
            return self.page.locator(selector).first.is_hidden()

    def count_elements(self, selector: str) -> int:
        """返回匹配选择器的元素数量。"""
        return self.page.locator(selector).count()

    # ------------------------------------------------------------------
    # 高级操作
    # ------------------------------------------------------------------
    def press_key(self, key: str, selector: Optional[str] = None) -> None:
        """按下键盘按键。

        Args:
            key: 按键名称，如 'Enter', 'Escape', 'Tab', 'ArrowDown'
            selector: 可选，先聚焦该元素再按键
        """
        if selector:
            self.page.locator(selector).first.focus()
        self.page.keyboard.press(key)

    def hover_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """鼠标悬停到元素上。"""
        t = timeout or self._default_timeout
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=t)
        locator.hover()

    def drag_and_drop(self, source_selector: str, target_selector: str) -> None:
        """拖拽操作。"""
        source = self.page.locator(source_selector).first
        target = self.page.locator(target_selector).first
        source.drag_to(target)

    def scroll_into_view(self, selector: str) -> None:
        """滚动页面使元素可见。"""
        self.page.locator(selector).first.scroll_into_view_if_needed()

    def take_screenshot(self, name: str) -> str:
        """截图并保存到 screenshots 目录。

        Args:
            name: 截图文件名（不含扩展名）

        Returns:
            截图文件完整路径
        """
        from conftest import SCREENSHOTS_DIR
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        filepath = SCREENSHOTS_DIR / f"{name}.png"
        self.page.screenshot(path=str(filepath), full_page=False)
        return str(filepath)

    # ------------------------------------------------------------------
    # 表格操作（裁剪系统常用）
    # ------------------------------------------------------------------
    def get_table_row_count(self, table_selector: str = ".ant-table-tbody") -> int:
        """获取表格行数。"""
        rows = self.page.locator(f"{table_selector} tr.ant-table-row").all()
        return len(rows)

    def get_table_cell_text(self, row_index: int, col_index: int) -> str:
        """获取指定单元格文本（基于 ant-design 表格）。"""
        cell = self.page.locator(
            f".ant-table-tbody tr.ant-table-row:nth-child({row_index + 1}) "
            f"td:nth-child({col_index + 1})"
        ).first
        return cell.inner_text().strip() if cell.is_visible() else ""

    def click_table_row(self, row_index: int, col_index: int = 0) -> None:
        """点击表格指定行的第一列。"""
        cell = self.page.locator(
            f".ant-table-tbody tr.ant-table-row:nth-child({row_index + 1}) "
            f"td:nth-child({col_index + 1})"
        ).first
        cell.click()

    def select_table_row_checkbox(self, row_index: int) -> None:
        """勾选表格某一行的复选框。"""
        checkbox = self.page.locator(
            f".ant-table-tbody tr.ant-table-row:nth-child({row_index + 1}) "
            f"td:first-child input[type='checkbox']"
        ).first
        if not checkbox.is_checked():
            checkbox.check()

    # ------------------------------------------------------------------
    # 模态框操作
    # ------------------------------------------------------------------
    def confirm_modal(
        self,
        modal_selector: str = ".ant-modal",
        confirm_text: str = "确定",
    ) -> None:
        """在模态框中点击确认按钮。"""
        self.page.locator(f"{modal_selector} button:has-text('{confirm_text}')").first.click()
        self.page.wait_for_timeout(500)

    def cancel_modal(self, modal_selector: str = ".ant-modal") -> None:
        """在模态框中点击取消按钮。"""
        self.page.locator(f"{modal_selector} button:has-text('取消')").first.click()
        self.page.wait_for_timeout(500)

    def close_modal(self, modal_selector: str = ".ant-modal") -> None:
        """关闭模态框（点击 X 按钮）。"""
        self.page.locator(f"{modal_selector} .ant-modal-close").first.click()
        self.page.wait_for_timeout(500)

    def get_modal_title(self, modal_selector: str = ".ant-modal") -> str:
        """获取模态框标题。"""
        return self.page.locator(f"{modal_selector} .ant-modal-title").first.inner_text().strip()
