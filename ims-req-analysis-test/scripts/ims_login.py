"""
Shared login helper for IMS environments.
Handles enterprise selector (SIT) vs direct login (xinji).
"""
import time, json
from pathlib import Path

ENV_DIR = Path(__file__).parent.parent / "environments"

def load_env(env_name: str) -> dict:
    """Load environment config."""
    path = ENV_DIR / f"{env_name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Environment '{env_name}' not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def login(page, env_name: str = "sit", enterprise: str = None):
    """
    Login to IMS environment. Handles enterprise selector if needed.

    Args:
        page: Playwright page object
        env_name: 'sit' or 'xinji'
        enterprise: enterprise name for SIT (default: first available)
    """
    env = load_env(env_name)
    login_cfg = env["login"]
    url = env["url"]

    page.goto(f"{url}/#/login", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    # Get password (may vary by enterprise for UAT)
    password = env["credentials"]["password"]
    if login_cfg.get("password_by_enterprise"):
        pw_map = login_cfg["password_by_enterprise"]
        target_ent = enterprise or login_cfg.get("enterprise_default", "")
        password = pw_map.get(target_ent, pw_map.get("_default", password))

    # Fill username/password
    page.fill(login_cfg["username_selector"], env["credentials"]["username"])
    page.fill(login_cfg["password_selector"], password)
    time.sleep(0.5)

    # Handle enterprise selector (SIT only)
    if login_cfg.get("has_enterprise_selector"):
        # Click the selector (focuses search input automatically)
        page.locator(".ant-select-selector").first.click()
        time.sleep(1)

        # Scroll virtual list with mouse wheel to load ALL hidden options
        # (rc-virtual-list only renders ~9 items; mouse wheel triggers loading)
        dropdown = page.locator(".ant-select-dropdown:not(.ant-select-dropdown-hidden) .rc-virtual-list-holder")
        if dropdown.count() > 0:
            dropdown.first.hover()
            for i in range(10):
                page.mouse.wheel(0, 200)
                time.sleep(0.2)

        # Select enterprise: type to search, then press Enter
        target = enterprise or login_cfg.get("enterprise_default", "")
        if target:
            page.keyboard.type(target, delay=50)
            time.sleep(1)
            page.keyboard.press("Enter")
            time.sleep(0.5)

    # Click login
    page.click(login_cfg["submit_selector"])
    time.sleep(5)
    page.wait_for_load_state("networkidle", timeout=15000)

    return page.title()
