"""IMS Attendance — Quarantined Flaky Tests

Tests with known intermittent failures, isolated here with @pytest.mark.skip.
Review weekly; fix and promote back to main test files.
"""

import pytest


@pytest.mark.quarantine
@pytest.mark.skip(reason="Quarantined — flaky: 考勤机Access连接超时导致偶发失败")
class TestQuarantinedAttendanceSync:
    """考勤同步 — 隔离的flaky测试"""

    def test_sync_from_access_db(self):
        """考勤机数据库同步 — 隔离中"""
        pass


@pytest.mark.quarantine
@pytest.mark.skip(reason="Quarantined — flaky: 日考勤计算大数据量时偶发超时")
class TestQuarantinedDailyCalc:
    """日考勤计算 — 隔离的flaky测试"""

    def test_large_dataset_calculation(self):
        """大批量日考勤计算 — 隔离中"""
        pass
