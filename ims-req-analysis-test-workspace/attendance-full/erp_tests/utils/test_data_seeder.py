"""Test Data Seeder — Auto-seed attendance data into SIT when empty.

Strategy (each step times out quickly, falls through gracefully):
  1. Extract existing 日考勤数据 → if found, use directly.
  2. Check 考勤登记 for raw records → if found, suggest manual 日考勤计算.
  3. Try 快速补卡 on visible rows → if works, re-extract.
  4. All fail → return empty dataset (tests skip cleanly).
"""

import json
import time
from pathlib import Path
from playwright.sync_api import Page

DATA_DIR = Path(__file__).parent / "extracted_data"
DATA_DIR.mkdir(exist_ok=True)

BASE = "http://test.fj.dtsimple.pro"
DAILY = f"{BASE}/#/personnel/workAttendance/dailyReportNew"
DETAIL = f"{BASE}/#/personnel/workAttendance/detail"


def _wait_stable(page: Page, ms: int = 2000):
    try:
        page.wait_for_load_state("networkidle", timeout=5000)
    except Exception:
        pass
    page.wait_for_timeout(ms)


# ── Strategy 1: extract existing ────────────────────────────────────────────

def _try_extract(page: Page) -> tuple[bool, dict]:
    from utils.test_data_extractor import build_test_dataset
    try:
        ds = build_test_dataset(page)
        return ds["metadata"]["total_records"] > 0, ds
    except Exception:
        return False, {}


# ── Strategy 2: check raw records ───────────────────────────────────────────

def _count_raw_records(page: Page) -> int:
    """Count raw attendance records in 考勤登记."""
    try:
        page.goto(DETAIL, timeout=10000)
        _wait_stable(page, 2000)
        _click_if_exists(page, "button:has-text('查询')")
        page.wait_for_timeout(2000)

        rows = page.locator(".ant-table-tbody tr, table tbody tr")
        real = 0
        for i in range(min(rows.count(), 10)):
            text = rows.nth(i).inner_text().strip()
            if text and all(kw not in text for kw in ["暂无", "No Data", "Loading"]):
                real += 1
        return real
    except Exception:
        return 0


def _click_if_exists(page: Page, selector: str) -> bool:
    el = page.locator(selector).first
    if el.count() > 0:
        try:
            el.click(timeout=3000)
            return True
        except Exception:
            pass
    return False


# ── Strategy 3: quick mend card on existing employee rows ────────────────────

def _try_quick_mend(page: Page) -> bool:
    """Try clicking a 快速补卡 button on an enabled row."""
    try:
        page.goto(DAILY, timeout=10000)
        _wait_stable(page, 2000)
        _click_if_exists(page, "button:has-text('查询')")
        page.wait_for_timeout(2000)

        # Try 早班上班补卡 if enabled
        for btn_text in ["早班上班补卡", "早班下班补卡"]:
            btns = page.locator(f"button:has-text('{btn_text}')")
            for i in range(min(btns.count(), 5)):
                btn = btns.nth(i)
                if btn.is_enabled():
                    btn.click(timeout=3000)
                    page.wait_for_timeout(1500)
                    # Accept any confirm dialog
                    try:
                        dialog = page.wait_for_event("dialog", timeout=2000)
                        dialog.accept()
                    except Exception:
                        pass
                    page.wait_for_timeout(1500)
                    return True
        return False
    except Exception:
        return False


# ── Main ─────────────────────────────────────────────────────────────────────

def ensure_test_data(page: Page) -> dict:
    """Try to ensure SIT has data. Returns dataset dict.

    Fast-fail: each step times out in <15s. If all strategies fail,
    returns empty dataset so tests skip cleanly.
    """
    from utils.test_data_extractor import build_test_dataset

    _empty = lambda: {
        "metadata": {"extracted_at": "", "total_records": 0},
        "summary": {"normal": 0, "late": 0, "early_leave": 0, "absent": 0, "missing_card": 0, "shifts": {}},
        "samples": {"normal_employee": None, "late_employee": None, "absent_employee": None, "missing_card_employee": None},
        "employees_for_leave": [],
        "by_shift": {},
    }

    # Step 1: extract
    has_data, ds = _try_extract(page)
    if has_data:
        print(f"[seeder] Found {ds['metadata']['total_records']} records — using existing data.")
        return ds

    # Step 2: raw records
    raw_count = _count_raw_records(page)
    print(f"[seeder] Raw records in 考勤登记: {raw_count}")

    if raw_count > 0:
        print("[seeder] Raw records exist but no daily stats. "
              "Run 日考勤计算 manually in SIT to generate stats, then re-run tests.")
        return _empty()

    # Step 3: try quick mend
    print("[seeder] No raw records. Trying quick mend card...")
    if _try_quick_mend(page):
        print("[seeder] Mend card succeeded. Trying daily calculation...")
        try:
            page.goto(DAILY, timeout=10000)
            _wait_stable(page, 2000)
            # Try triggering 日考勤计算
            if _click_if_exists(page, "button:has-text('日考勤计算')"):
                page.wait_for_timeout(1500)
                _click_if_exists(page, ".ant-btn-primary")
                page.wait_for_timeout(8000)
            # Re-extract
            ds = build_test_dataset(page)
            if ds["metadata"]["total_records"] > 0:
                print(f"[seeder] Success! {ds['metadata']['total_records']} records after seeding.")
                return ds
        except Exception as e:
            print(f"[seeder] Daily calc failed: {e}")

    print("[seeder] Unable to auto-seed. Tests requiring data will skip.")
    return _empty()
