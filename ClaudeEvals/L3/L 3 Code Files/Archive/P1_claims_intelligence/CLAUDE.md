# CLAUDE.md — UHG Claims Intelligence Service

## Project

FastAPI service answering questions about insurance claims.
HIPAA-compliant environment. No Anthropic API key or SDK anywhere in
this project — Claude Code (claude.ai Pro/Team) is the engineering
layer, not a runtime dependency of the service.

## Domain rules (non-negotiable)

- Status lifecycle: submitted -> in_review -> approved / denied /
  pending_info. Never skip a state.
- Out-of-network providers always trigger pending_info.
- Every status change requires an AuditLog entry.
- Monetary amounts are USD. Never invent amounts.

## Output conventions

- claims_service.py functions return typed Pydantic models, never
  raw dicts.
- Every new endpoint needs a test before it is done.

## Forbidden actions

- Never modify eval/cases.json without a Lessons Learned note.
- Never run `git push --force` on main.
- Never remove an AuditLog check to "simplify" code.
- Never log a raw member_id, claim_id, name, DOB, or SSN — always
  hash or mask first (see `_safe_log_id()` in main.py, added M7).

## Lessons Learned

- 2026-06-10: Claude missed that pending_info needs an AuditLog
  entry too, not just denied/approved. Rule added after this was
  caught in review.

## Risk tiers (EU AI Act-aligned)

- **HIGH**: touches claim status transitions, payment amounts, or
  member PII handling. Requires security-reviewer sign-off and an
  Escalation line in the PR description.
- **LIMITED**: touches status display, member/provider lookups, or
  read-only aggregation. Standard review checks required; single
  human reviewer sufficient.
- **MINIMAL**: touches tests, docs, or non-functional refactors.

## Escalation rule

If a change is tagged HIGH risk, or if the eval-runner agent
reports a mean score below 0.80, or if the security-reviewer agent
flags a HIGH-risk pattern, the PR description must include an
"Escalation:" line explaining what a human reviewer checked before
merge.

## Spec-driven engineering (M6)

- The claim-status lookup contract (`/claims/{claim_id}/status`) is
  spec-driven — `openapi.yaml` is the source of truth. Run "Read
  openapi.yaml and review main.py, flag any drift" before merging
  any change to this route.
- Read-only aggregation endpoints (`/claims/count`,
  `/claims/total-billed`) are simple enough that CLAUDE.md's domain
  rules are sufficient; they are not currently spec-driven.
