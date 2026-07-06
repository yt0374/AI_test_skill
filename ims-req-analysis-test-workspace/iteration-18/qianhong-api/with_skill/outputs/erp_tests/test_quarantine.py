"""
Quarantine file for flaky IMS API tests.
Tests here are skipped by default in CI. Review weekly.

To run quarantined tests:
    pytest erp_tests/test_quarantine.py -v --no-skip

Criteria for quarantine:
    - Failed > 3 times in the last 7 days with non-deterministic patterns
    - Root cause identified as environment/data issue (not code bug)
    - Failure rate > 30% in recent runs
"""
import pytest


@pytest.mark.quarantine
@pytest.mark.skip(reason="Quarantined — review required")
class TestQuarantined:
    """Placeholder for quarantined flaky tests."""

    def test_placeholder(self):
        """Add flaky tests here after identification."""
        pass
