"""
services/claims_service.py — UHG Claims Intelligence Service (L3)

Core business logic for querying claims data. This module is the primary
target of the M3 eval suite and the M4 CI eval gate.

NOTE FOR INSTRUCTORS: this file contains one deliberate bug, intentionally
left in for the M3 lab ("Fix the lowest scorer"):

  total_billed_for_status() sums billed_amount using float() instead of
  keeping it as Decimal. This is a real-world bug class — float arithmetic
  on currency values accumulates rounding error. eval-002 in eval/cases.json
  is written specifically to catch this. Do not "fix" it before the
  workshop runs — participants are meant to find and fix it themselves.
"""

from typing import Optional

from seed_data import CLAIMS, MEMBERS, PROVIDERS

VALID_STATUSES = {"submitted", "in_review", "approved", "denied", "pending_info"}


def _provider_lookup(provider_id: str) -> Optional[dict]:
    return next((p for p in PROVIDERS if p["provider_id"] == provider_id), None)


def _member_lookup(member_id: str) -> Optional[dict]:
    return next((m for m in MEMBERS if m["member_id"] == member_id), None)


def count_claims_by_status(status: str) -> int:
    """Count claims with an exact status match. Does not substring-match,
    so 'in_review' never accidentally counts 'pending_info' rows."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Unknown status: {status}")
    return sum(1 for c in CLAIMS if c["status"] == status)


def total_billed_for_status(status: str) -> float:
    """Sum billed_amount for all claims with the given status.

    BUG (deliberate, for M3 lab): returns float, and casts each Decimal
    to float before summing. This loses precision and is not acceptable
    for monetary values in a production claims system. The fix is to
    keep everything as Decimal and only convert at the API boundary,
    if at all.
    """
    matching = [c for c in CLAIMS if c["status"] == status]
    total = 0.0
    for c in matching:
        total += float(c["billed_amount"])   # <-- precision-losing cast
    return total


def claims_for_member(member_id: str) -> list[dict]:
    """Return all claims for a given member_id. Returns an empty list
    (not None, not an error) if the member has no claims."""
    if _member_lookup(member_id) is None:
        raise ValueError(f"Unknown member_id: {member_id}")
    return [c for c in CLAIMS if c["member_id"] == member_id]


def is_out_of_network(claim_id: str) -> bool:
    """True if the claim's provider is out-of-network."""
    claim = next((c for c in CLAIMS if c["claim_id"] == claim_id), None)
    if claim is None:
        raise ValueError(f"Unknown claim_id: {claim_id}")
    provider = _provider_lookup(claim["provider_id"])
    return provider is not None and not provider["in_network"]


def claim_status_history(claim_id: str) -> dict:
    """Return the current status and a human-readable summary for a claim.
    This is a simplified stand-in for what would be a real audit trail
    query in production."""
    claim = next((c for c in CLAIMS if c["claim_id"] == claim_id), None)
    if claim is None:
        raise ValueError(f"Unknown claim_id: {claim_id}")
    oon = is_out_of_network(claim_id)
    return {
        "claim_id": claim_id,
        "status": claim["status"],
        "out_of_network": oon,
        "note": "Out-of-network claims are routed to pending_info." if oon else "",
    }
