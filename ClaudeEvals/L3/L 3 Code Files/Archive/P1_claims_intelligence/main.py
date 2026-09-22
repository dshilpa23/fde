"""
main.py — UHG Claims Intelligence Service (L3)

FastAPI entrypoint. Exposes read-only endpoints over the seed claims
data. No Anthropic API key, no LLM calls in this file — at L3, Claude
is used as your engineering tool (via Claude Code), not as a runtime
dependency of the service itself.

Endpoints:
  /health           - present from the start (M5 containerises this)
  /claims/*         - basic read endpoints over seed data (this file)

Governance note (M7/M8): this service does NOT have a separate
/audit endpoint or AuditRecord database table. Per CLAUDE.md and the
Session 2 governance module, Git history is the audit trail — every
change to claims_service.py is already traceable via `git log`. A
parallel logging system would duplicate information Git already has.

Observability note (M9/M10): observability here is `scripts/
code_health.sh` (coverage, lint, eval score over commits), not a
live /metrics HTTP endpoint.
"""

import hashlib
import logging
import re

from fastapi import FastAPI, HTTPException

from services.claims_service import (
    count_claims_by_status,
    total_billed_for_status,
    claims_for_member,
    is_out_of_network,
    claim_status_history,
    VALID_STATUSES,
)

app = FastAPI(title="UHG Claims Intelligence Service", version="1.0.0")

logger = logging.getLogger("claims_intelligence")


def _safe_log_id(raw_id: str) -> str:
    """Hash an identifier before logging - never log raw IDs.

    CLAUDE.md forbidden action: never log a raw member_id, claim_id,
    name, DOB, or SSN. Every route below that logs a path parameter
    must pass it through this function first (M7).
    """
    return hashlib.sha256(raw_id.encode()).hexdigest()[:12]


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/claims/count")
def claims_count(status: str):
    if status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Unknown status: {status}")
    return {"status": status, "count": count_claims_by_status(status)}


@app.get("/claims/total-billed")
def claims_total_billed(status: str):
    if status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Unknown status: {status}")
    return {"status": status, "total_billed": total_billed_for_status(status)}


@app.get("/claims/member/{member_id}")
def member_claims(member_id: str):
    logger.info(f"member_claims request: id_hash={_safe_log_id(member_id)}")
    try:
        return {"member_id": member_id, "claims": claims_for_member(member_id)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/claims/{claim_id}/status")
def claim_status(claim_id: str):
    # Spec-driven (M6) — contract lives in openapi.yaml, not memory.
    # Pattern and 404 response are both defined there.
    logger.info(f"claim_status request: id_hash={_safe_log_id(claim_id)}")
    if not re.match(r"^CLM-[0-9]+", claim_id):
        raise HTTPException(status_code=400, detail="claim_id must match ^CLM-[0-9]+")
    try:
        return claim_status_history(claim_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/claims/{claim_id}/network")
def claim_network(claim_id: str):
    logger.info(f"claim_network request: id_hash={_safe_log_id(claim_id)}")
    try:
        return {"claim_id": claim_id, "out_of_network": is_out_of_network(claim_id)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
