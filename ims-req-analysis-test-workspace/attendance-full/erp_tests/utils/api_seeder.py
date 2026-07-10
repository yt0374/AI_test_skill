"""API-based test data seeder for IMS attendance module.

Uses IMS REST API directly — no UI interaction needed.

Flow:
  1. Login → get auth token
  2. Get employees → POST /api/low-code/dataTypeClassification/commonPullDownList
  3. Import attendance → POST /api/ims-auth/attendance/item/import

Usage:
    from api_seeder import seed_attendance_data
    dataset = seed_attendance_data()
"""

import json
import httpx
from datetime import datetime
from pathlib import Path

BASE = "http://test.fj.dtsimple.pro"
LOGIN_URL = f"{BASE}/api/ims-auth/auth/login"
EMPLOYEE_URL = f"{BASE}/api/low-code/dataTypeClassification/commonPullDownList"
IMPORT_URL = f"{BASE}/api/ims-auth/attendance/item/import"
ITEM_PAGE_URL = f"{BASE}/api/ims-auth/attendance/item/page"

DATA_DIR = Path(__file__).parent / "extracted_data"
DATA_DIR.mkdir(exist_ok=True)


class IMSClient:
    """Lightweight IMS API client with auth token management."""

    def __init__(self):
        self.client = httpx.Client(timeout=30, verify=False)
        self.token = None

    def login(self, username="admin", password="metas2660"):
        """Login and store auth token. Password is MD5 hashed."""
        import hashlib
        pw_hash = hashlib.md5(password.encode()).hexdigest()

        resp = self.client.post(LOGIN_URL, json={
            "username": username,
            "password": pw_hash,
        })
        resp.raise_for_status()
        data = resp.json()
        self.token = data.get("data", {}).get("token")
        if self.token:
            self.client.headers["Authorization"] = self.token
            print(f"[API] Logged in, token: {self.token[:40]}...")
            return True
        print(f"[API] Login failed — response: {data.get('message', 'unknown')}")
        return False

    def get_employees(self, limit=10):
        """Get employee list from the system."""
        resp = self.client.post(EMPLOYEE_URL, json={
            "search": {"selectType": "no", "limit": limit},
            "dataTypeCode": "employee_new_L100",
            "filter": {},
        })
        data = resp.json()
        records = data.get("data", [])
        employees = []
        for r in records:
            employees.append({
                "工号": r.get("no", ""),
                "姓名": r.get("name", ""),
                "label": r.get("label", ""),
            })
        print(f"[API] Found {len(employees)} employees")
        return employees

    def import_attendance_items(self, employees, date_str=None):
        """Import attendance records for the given employees on a date."""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")

        # Build attendance records: morning in + afternoon out for each employee
        info_list = []
        for emp in employees[:10]:  # Max 10 employees, 2 records each = 20 records
            info_list.append({
                "工号": emp["工号"],
                "姓名": emp["姓名"],
                "考勤时间": f"{date_str} 08:00",
                "类型": "正常",
                "来源": "导入",
            })
            info_list.append({
                "工号": emp["工号"],
                "姓名": emp["姓名"],
                "考勤时间": f"{date_str} 17:30",
                "类型": "正常",
                "来源": "导入",
            })

        payload = {
            "route": {"query": {}},
            "templateKey": "sys_attendance",
            "infoList": info_list,
        }

        resp = self.client.post(IMPORT_URL, json=payload)
        data = resp.json()
        success = data.get("success", data.get("code") == 0)
        msg = data.get("message", "")
        print(f"[API] Import {len(info_list)} records: success={success}, msg={msg}")
        return success

    def query_attendance_items(self, date_str=None):
        """Query attendance items for a date to verify import."""
        if date_str is None:
            date_str = datetime.now().strftime("%Y/%m/%d")

        resp = self.client.post(ITEM_PAGE_URL, json={
            "page": 1,
            "size": 50,
            "search": {
                "attendanceDate": [
                    {"key": "attendanceDate", "value": date_str},
                    {"key": "attendanceDate", "value": date_str},
                ]
            },
            "searchType": {"attendanceDate": "between"},
            "order": {"attendanceTime": "asc"},
            "filter": {},
            "filterType": {},
        })
        data = resp.json()
        records = data.get("data", {}).get("records", [])
        print(f"[API] Query {date_str}: {len(records)} attendance items")
        return records


def seed_attendance_data() -> dict:
    """API-based seeding: login → get employees → import → verify.

    Returns a dataset dict compatible with the test fixtures.
    """
    client = IMSClient()

    # 1. Login
    if not client.login():
        return _empty_dataset()

    # 2. Get employees
    employees = client.get_employees(limit=10)
    if not employees:
        print("[API] No employees — cannot seed data.")
        return _empty_dataset()

    # 3. Import attendance for today
    today = datetime.now().strftime("%Y-%m-%d")
    ok = client.import_attendance_items(employees, today)
    if not ok:
        print("[API] Import failed — trying with first 3 employees...")
        ok = client.import_attendance_items(employees[:3], today)

    # 4. Verify
    records = client.query_attendance_items(today)
    print(f"[API] After import: {len(records)} attendance items in system")

    # 5. Save dataset
    dataset = {
        "metadata": {
            "extracted_at": datetime.now().isoformat(),
            "total_records": len(records),
            "source": "api_import",
        },
        "summary": {"normal": len(records) // 2, "late": 0, "early_leave": 0, "absent": 0, "missing_card": 0, "shifts": {}},
        "samples": {"normal_employee": None, "late_employee": None, "absent_employee": None, "missing_card_employee": None},
        "employees_for_leave": [{"display": f"{e['工号']}-{e['姓名']}"} for e in employees],
        "by_shift": {},
    }

    with open(DATA_DIR / "api_seeded_dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    return dataset


def _empty_dataset():
    return {
        "metadata": {"extracted_at": "", "total_records": 0},
        "summary": {"normal": 0, "late": 0, "early_leave": 0, "absent": 0, "missing_card": 0, "shifts": {}},
        "samples": {"normal_employee": None, "late_employee": None, "absent_employee": None, "missing_card_employee": None},
        "employees_for_leave": [],
        "by_shift": {},
    }
