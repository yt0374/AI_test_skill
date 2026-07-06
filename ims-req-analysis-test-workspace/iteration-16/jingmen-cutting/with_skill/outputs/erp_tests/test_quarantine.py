"""Quarantine file for flaky or unstable tests.

Tests that exhibit intermittent failures are moved here with @pytest.mark.skip
until the root cause is resolved. Each skipped test must include a reason
and a ticket/issue reference.

Review cadence: weekly (every Friday).
"""

import pytest


@pytest.mark.quarantine
@pytest.mark.skip(reason="QUAR-001: Add flaky tests here when identified during execution")
def test_placeholder_quarantine():
    """Placeholder for quarantined tests.

    When a test fails intermittently during CI/CD execution:
    1. Move it to this file
    2. Add @pytest.mark.skip with reason and ticket reference
    3. Create a bug ticket for investigation
    4. Review weekly to determine if fix is deployed and test can be restored
    """
    pass


# Example quarantine entries (uncomment when needed):
#
# @pytest.mark.quarantine
# @pytest.mark.skip(reason="QUAR-002: test_concurrent_bed_creation - Race condition in layer calculation, ticket BUG-2026-001")
# def test_concurrent_bed_creation_flaky():
#     ...
#
# @pytest.mark.quarantine
# @pytest.mark.skip(reason="QUAR-003: test_ticket_print_timeout - Network timeout on ticket generation, ticket BUG-2026-002")
# def test_ticket_print_timeout():
#     ...
