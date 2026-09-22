"""
tests/test_claims_service.py - UHG Claims Intelligence Service (L3)

Starter test suite. Covers the basic happy paths only - deliberately
incomplete. Part of M3/M4 is noticing what's missing (e.g. there is no
test asserting total_billed_for_status returns a precise Decimal, which
is exactly the bug eval-002 is designed to catch).
"""

import pytest

from services.claims_service import (
    count_claims_by_status,
    total_billed_for_status,
    claims_for_member,
    is_out_of_network,
    claim_status_history,
)


def test_count_in_review():
    assert count_claims_by_status("in_review") == 3


def test_count_approved():
    assert count_claims_by_status("approved") == 2


def test_count_denied():
    assert count_claims_by_status("denied") == 2


def test_count_pending_info():
    assert count_claims_by_status("pending_info") == 2


def test_count_unknown_status_raises():
    with pytest.raises(ValueError):
        count_claims_by_status("not_a_real_status")


def test_total_billed_for_denied():
    # NOTE: this only checks the numeric value, not the type.
    # It currently passes even though total_billed_for_status()
    # returns a float, not a Decimal. That's the bug eval-002
    # is designed to surface - this test is not strict enough yet.
    assert total_billed_for_status("denied") == 10450.00


def test_claims_for_member():
    claims = claims_for_member("MBR-001")
    assert len(claims) == 2
    assert {c["claim_id"] for c in claims} == {"CLM-001", "CLM-003"}


def test_claims_for_unknown_member_raises():
    with pytest.raises(ValueError):
        claims_for_member("MBR-999")


def test_out_of_network_true():
    assert is_out_of_network("CLM-003") is True


def test_out_of_network_false():
    assert is_out_of_network("CLM-001") is False


def test_claim_status_history():
    result = claim_status_history("CLM-003")
    assert result["status"] == "pending_info"
    assert result["out_of_network"] is True
