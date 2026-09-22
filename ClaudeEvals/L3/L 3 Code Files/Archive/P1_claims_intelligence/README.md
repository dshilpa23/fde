# UHG Claims Intelligence Service — L3 Reference Build

This project matches `L3_Session1_LabGuide_Final.docx` and
`L3_Session2_LabGuide_Final.docx` module-for-module. It is the
**finished end state** — every artefact both lab guides ask
participants to build is present and implemented to the guides'
exact specs, so it can be used as:

- a **facilitator answer key** to check participant work against, or
- a **CI/regression baseline** to confirm the labs' exercises still
  work as written before running the workshop.

To hand this to participants as the *starting* point instead, strip
back to: `main.py`, `seed_data.py`, `services/`, `tests/`,
`requirements.txt`, `.gitignore`, and a `.github/workflows/ci.yml`
with the M4/M5/M7 steps commented out. (See "What each module
built" below for the exact per-file boundary.)

## What each module built

**Session 1 — `L3_Session1_LabGuide_Final.docx`**

| Module | Built | File(s) |
|---|---|---|
| M1 — Sub-Agents & Parallel Work | Two sub-agents, scoped tool access | `.claude/agents/eval-runner.md` (Read, Bash, Grep), `.claude/agents/security-reviewer.md` (Read, Grep) |
| M2 — CLAUDE.md as Production Contract | Domain rules, output conventions, forbidden actions, Lessons Learned | `CLAUDE.md` |
| M3 — Rubric-Based Eval Suite | 20 cases, 6 categories (count×4, aggregation×4, member×3, provider×3, status×3, edge×3), rubric-scored 0.0–1.0 | `eval/cases.json` |
| M4 — Local Eval Gate | Runs eval-runner headless, exits 1 below 0.80 mean | `scripts/run_eval_gate.sh`, eval-gate step in `.github/workflows/ci.yml` |

**Session 2 — `L3_Session2_LabGuide_Final.docx`**

| Module | Built | File(s) |
|---|---|---|
| M5 — Deployment Concepts | Two-service compose (api + Postgres db, healthcheck), `verify-container` CI job | `Containerfile`, `podman-compose.yml`, `.github/workflows/ci.yml` |
| M6 — Spec-Driven Engineering | `openapi.yaml` as source of truth for `/claims/{claim_id}/status`; implementation matches the spec's parameter pattern and both response codes | `openapi.yaml`, `main.py` |
| M7 — Security via Sub-Agent | `_safe_log_id()` PII-safe logging (hash, never raw IDs), wired into every route that logs a path param; non-blocking `security-review` CI job | `main.py`, `.github/workflows/ci.yml` |
| M8 — Governance via Git & CLAUDE.md | HIGH/LIMITED/MINIMAL risk tiers (EU AI Act-aligned) + escalation rule in CLAUDE.md; PR template with Risk tier + Escalation fields. No AuditRecord DB — Git history is the audit trail | `CLAUDE.md`, `.github/PULL_REQUEST_TEMPLATE.md` |
| M9 — Multi-Agent Orchestration | No new files — hub-and-spoke design exercise, run interactively | — |
| M10 — Observability & Capstone | Coverage + lint + eval-score trend report | `scripts/code_health.sh` |

## Project layout

```
p1_claims_intelligence/
├── .claude/agents/
│   ├── eval-runner.md          M1
│   └── security-reviewer.md    M1
├── .github/
│   ├── workflows/ci.yml        starter + M4 + M5 + M7
│   └── PULL_REQUEST_TEMPLATE.md M8
├── eval/cases.json             M3 — 20 rubric-based cases
├── scripts/
│   ├── run_eval_gate.sh        M4
│   └── code_health.sh          M10
├── services/claims_service.py  starter — contains the deliberate
│                                float/Decimal bug eval-008 catches
├── tests/test_claims_service.py starter
├── main.py                     starter + M6 (spec-driven status route)
│                                        + M7 (_safe_log_id logging)
├── seed_data.py                starter — 5 members, 5 providers, 10 claims
├── openapi.yaml                M6
├── Containerfile                M5
├── podman-compose.yml           M5
├── CLAUDE.md                    M2 + M8
└── requirements.txt             starter — no LLM SDK needed
```

## Quick start

```bash
pip install -r requirements.txt
pytest tests/ -v
uvicorn main:app --reload
curl http://localhost:8000/health
```

## A note on the deliberate bug — still present, on purpose

`services/claims_service.py` still contains the intentional bug in
`total_billed_for_status()` — it sums monetary values using `float`
instead of `Decimal`. **This is left unfixed deliberately.** Per the
lab guides, `eval-008` in `eval/cases.json` exists specifically to
catch it, and the M3 lab exercise is for participants to find and
fix it themselves using the eval suite. If you fix it before running
the workshop, that exercise has nothing left to find.

## How Claude access works

This project uses Claude Code, authenticated via your claude.ai Pro
or Team account — no Anthropic API key or SDK anywhere in this
project. CI authenticates the same way, using a token from
`claude setup-token`, stored as the `CLAUDE_CODE_OAUTH_TOKEN` secret
(Session 1, M4).
