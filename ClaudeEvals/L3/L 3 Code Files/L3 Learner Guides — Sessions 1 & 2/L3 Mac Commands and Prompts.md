# UHG × Anthropic — L3 Full Learner Reference
## macOS (Terminal) Edition — Sessions 1 & 2, All Prompts & Commands

This document consolidates every command, prompt, checklist, and reference table from the L3 Learner Guides (Sessions 1 & 2), rendered for **macOS (Terminal)** only.

---


# L3 · SESSION 1 — Production AI Systems: Sub-Agents, CLAUDE.md Contracts, Eval Suites, Eval Gate (Modules 1–4)

---



For Claude Code installation, also see: Engineering Excellence | Claude Code Setup — https://unify.hcp.uhg.com/offerings/engineering-excellence/docs/claude-code-setup



# 4. Installation


## 4.1 Claude CLI (Claude Code)


### Shared steps (apply to both Windows and macOS)

These steps are identical on both operating systems. If you completed L1/L2 on the same machine, Claude Code is already installed — skip to the Overview below.

Step A — Confirm prerequisites. Verify that all of Section 3 is complete: secure group approved, Claude Console Access, Optum AppStore access confirmed.

Step B — Authentication. Select option 1. Claude account with subscription.



### Install & Verify — by Platform


```
1. Open Optum AppStore
2. Search for "Claude Code CLI"
3. Select Install; wait for deployment
4. Open a NEW Terminal window
```
```
claude --version
```
*A version number should print without errors.*
```
claude doctor
```
*Deeper check of install, authentication, and configuration.*

If claude is not recognized, close and reopen your terminal window.



# Overview

Session 1 builds the engineering foundation for advanced Claude Code use on the UHG Claims Intelligence Service — a production FastAPI application built and reviewed entirely through Claude Code. Everything runs through your claude.ai Pro or Team account, used in increasingly sophisticated ways: custom sub-agents, a production-grade CLAUDE.md, a rubric-based eval suite, and a CI/CD pipeline gated by Claude Code running in headless mode. Commands are shown side by side for Windows (PowerShell) and macOS (Terminal) — use the column for your platform.


## What You Will Learn

- Custom sub-agents for scoped, reusable automation
- Headless mode: non-interactive Claude Code for scripts and CI
- CLAUDE.md as an enforceable engineering contract
- Rubric-based eval suites and static code analysis
- Local eval gates that catch regressions before commit


## Prerequisites

- claude.ai Pro or Team plan (free plan does not include Claude Code)
- Claude Code installed: claude --version
- VS Code with integrated terminal
- Git 2.x or higher
- Python 3.11 or higher


# Before You Start — Setup Checklist

Complete all items before M1 begins. If any check fails, stop and fix it.


## Repository


```
unzip ~/Downloads/L3_P1_claims_intelligence.zip -d ~/Desktop/
cd ~/Desktop/p1_claims_intelligence
python3 -m pip install -r requirements.txt
```

Confirm all packages installed without errors.



## Claude Code Access

- Confirm you have an active claude.ai Pro or Team plan (free plan does not include Claude Code)

```
claude --version
```
```
# If not installed:
curl -fsSL https://claude.ai/install.sh | bash
```

- Run claude once and complete the browser sign-in flow


## GitHub

- Fork or clone the repository — you need push access for Module 4
- Confirm the repository has a .github/workflows/ci.yml file
- You will generate a Claude Code claude.ai session in M4 — no setup needed yet

> **⚠ Important**
> This programme uses Claude Code exclusively. Everything runs through your claude.ai Pro or Team account.



## Step 3: Initialize Git

Identical on both platforms:


```
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git add .
git commit -m "init: L3 claims intelligence baseline"
```



# Module 1: Sub-Agents & Parallel Work (45 minutes)

M1 introduces two capabilities that separate senior Claude Code use from everyday use: custom sub-agents (scoped, reusable agent configurations) and headless mode (non-interactive, scriptable Claude Code runs). Together they let you build automated quality checks that run consistently — by you, by teammates, or by CI.


## What a Sub-Agent Is

A sub-agent is a Markdown file in .claude/agents/ that defines a focused, reusable Claude Code persona: a name, a description of when to use it, a restricted set of tools it may call, and a system prompt describing its job. Once defined, any Claude Code session in the project can delegate to it.


### Three Properties That Make Sub-Agents Valuable at L3

- Scoped tool access — a sub-agent can be restricted to Read, Bash, and Grep only, so it physically cannot edit files even if asked to
- Isolated context — a sub-agent runs in its own context window. A verbose, multi-step task doesn't pollute your main session's context
- Reusable and version-controlled — the agent definition lives in Git. Every teammate who clones the repo gets the same agent, behaving the same way


## Task 1 — Create the eval-runner Sub-Agent

Create the directory .claude/agents/, then create .claude/agents/eval-runner.md with this content:


```
---
name: eval-runner
description: >
  Runs the claims-intelligence eval suite against eval/cases.json.
  Scores each case 0-1 against its rubric, reports a mean score.
tools: Read, Bash, Grep
model: inherit
---

You are the eval-runner sub-agent. Your only job is to:

1. Read eval/cases.json
2. For each case, read the relevant source file(s) and reason
   about whether the implementation satisfies the rubric
3. Score each case 0.0-1.0 against its rubric
4. Compute the mean score across all cases
5. Report: per-case scores, mean score, pass/fail at 0.80

Do not modify any files. Do not fix issues — only report them.
If mean score is below 0.80, list the 3 lowest-scoring cases
with a one-line reason each.
```

In an interactive session, run /agents and confirm eval-runner appears in the list. Read back the agent's description to confirm Claude Code parsed it correctly:


```
claude
> /agents
```



## Task 2 — Create the security-reviewer Sub-Agent

Not every sub-agent needs the same tool access. security-reviewer's job is to search and read — it never needs to run code, so it gets even less privilege than eval-runner.

Create .claude/agents/security-reviewer.md:


```
---
name: security-reviewer
description: >
  Audits the codebase for PII handling and prompt-injection risk.
  Use this agent before merging any change that touches
  request handling, logging, or external-facing endpoints.
tools: Read, Grep
model: inherit
---

You are the security-reviewer sub-agent for the Claims
Intelligence Service. Your only job is to:

1. Search the codebase for places that log, store, or pass
   along user-supplied input (names, member IDs, DOBs, SSNs)
2. Flag any logging statement that could write PII in plaintext
3. Flag any endpoint that forwards user input to Claude without
   a sanitisation or validation step first
4. Report findings as a list: file, line, risk, suggested fix

Do not modify any files. Do not run tests or scripts. Read and
report only — a human decides what to fix and when.
```


> **💡 Same pattern, different scope**
> eval-runner needs Bash because scoring sometimes means running a quick check against the code. security-reviewer gets Read and Grep only — no Bash, because a security audit never needs to execute anything, only search and read.



## Task 3 — Invoke the Sub-Agent

Start an interactive Claude Code session (identical both platforms):


```
claude
```


> 💬 **Prompt:**
> Use the eval-runner agent to check the current code

Observe that it runs in isolated context. Confirm with git status that no files were modified.



## Task 4 — Headless Mode

Interactive Claude Code (just running claude) waits for your input after every response. That's correct for normal development, but it hangs forever in a script or CI pipeline where no human is present to respond. Headless mode fixes this.


```
# Interactive mode (default) — waits for your input
claude
> Review this PR for security issues

# Headless mode — runs once, prints result, exits
claude -p "Review this PR for security issues"

# Headless mode with structured JSON output (for scripts/CI)
claude -p "Run the eval suite and report mean score" \
  --output-format json > eval_result.json

# Headless mode invoking a specific sub-agent
claude -p "Use the eval-runner agent to score eval/cases.json"

# WRONG — this hangs forever in CI:
claude "Review this PR"

# RIGHT — always use -p in scripts and CI:
claude -p "Review this PR"
```


> **⚠ Most common CI mistake**
> Forgetting -p is the single most common mistake when running Claude Code in scripts. If a script hangs and never completes, this is the first thing to check.

Exit the interactive session (type "exit"). Now run:


```
claude -p "Summarise what the eval-runner agent found"
```

Key difference: -p runs once, prints result, exits — no prompt waiting for input. Try without -p to see the difference:


```
claude "Summarise what the eval-runner agent found"
# It will hang until you Ctrl+C — then retry with -p
```



## Task 5 — Parallel Delegation

When you have multiple independent sub-tasks, ask the orchestrating Claude Code session to delegate them to sub-agents in parallel rather than working through them one at a time.

Start interactive mode again:


```
claude
```


> 💬 **Prompt:**
> I need three things done on the Claims Intelligence Service:
1. Use the security-reviewer agent to audit middleware/ for PII handling issues
2. Use the eval-runner agent to score the current build against eval/cases.json
3. Review CLAUDE.md for outdated Lessons Learned entries

These are independent — run them in parallel and report all three results together.

Claude Code dispatches each task to its own sub-agent context, runs concurrently, and synthesises results.


### Rules for Safe Parallel Delegation

- Tasks must be independent — if task B depends on task A's output, run them sequentially
- Read-only tasks parallelise best — security review and eval scoring don't touch the same files
- Avoid concurrent writes — two sub-agents editing the same file at once causes conflicts
Discuss: which other UHG workflows could use this pattern?


> **✅ M1 Complete when**
> .claude/agents/ contains eval-runner.md and security-reviewer.md. Both are invokable individually and in parallel. You can explain when to use -p and when not to.



# Module 2: CLAUDE.md as Production Contract (45 minutes)

M2 turns CLAUDE.md from a loose set of preferences into an enforceable engineering contract. By the end, your CLAUDE.md encodes domain rules, output conventions, and forbidden actions specifically enough that Claude Code pushes back when asked to violate them — and a Lessons Learned section that compounds in value over the project's life.


## From Wishlist to Contract

A weak CLAUDE.md says "write good code" or "follow best practices" — statements too vague to be enforceable. A production contract states specific, checkable rules: "never skip a state", "never log full names in plaintext". Specificity is what makes a rule something Claude Code can actually follow and a reviewer can actually verify.



## Task 1 — Write the Production Contract

Create CLAUDE.md in the project root with these sections:


```
# CLAUDE.md — UHG Claims Intelligence Service

## Project
FastAPI service answering questions about insurance claims. HIPAA-compliant.

## Domain rules (non-negotiable)
- Status lifecycle: submitted -> in_review -> approved / denied / pending_info. Never skip a state.
- Out-of-network providers always trigger pending_info.
- Every status change requires an AuditLog entry.
- Monetary amounts are USD. Never invent amounts.

## Output conventions
- claims_service.py functions return typed Pydantic models, never raw dicts.
- Every new endpoint needs a test before it is done.
- All responses follow {"data": ..., "error": null} format.

## Forbidden actions
- Never modify eval/cases.json without a Lessons Learned note.
- Never run git push --force on main.
- Never remove an AuditLog check to "simplify" code.

## Lessons Learned
- 2026-06-10: Claude missed that pending_info needs an AuditLog entry too, not
  just denied/approved. Rule added after this was caught in review.
```


> **💡 Why this works as a contract, not a wishlist**
> Specific, not aspirational — "never skip a state" is enforceable; "write good code" is not. Forbidden actions are explicit — naming what Claude must never do prevents the most expensive mistakes outright. Lessons Learned compounds — every real mistake becomes a permanent rule; the contract gets stronger over the project's life.

Be specific — replace any vague statement with an enforceable one.



## Task 2 — Test Enforcement

Start Claude Code:


```
claude
```


> 💬 **Prompt:**
> I need you to skip the in_review state when updating a claim status

Claude Code should push back, citing the domain rule you wrote. If it doesn't, your rule wasn't specific enough — revise it.



## Task 3 — Shared Rules With @import

UHG runs many Claude Code projects, all of which share the same HIPAA baseline requirements. Rather than copy-pasting the same rules into every project's CLAUDE.md (and having them drift out of sync), use @import to pull in a shared, version-controlled standards file.

Create a shared standards file (simulated): ~/uhg-standards/CLAUDE.md


```
## HIPAA baseline rules (apply to every UHG project)
- Never log full names, DOBs, SSNs, or member IDs in plaintext
- Every API endpoint touching PHI requires an audit trail
- All new endpoints must have a security review before merge
```

Then add to your project's CLAUDE.md at the top:


```
@import ~/uhg-standards/CLAUDE.md
```


> 💬 **Prompt:**
> Summarise all the rules currently in effect

Confirm both shared and project-specific rules are recognized.


> **💡 How @import works**
> The @import line pulls in the shared rules automatically. Claude Code treats imported content as if it were written directly in this file — no copy-pasting, no drift between projects, one source of truth for org-wide standards.



## Task 4 — Add a Lessons Learned Entry

Deliberately ask Claude Code to do something that violates a domain rule (reuse the Task 2 prompt, or invent a new violation). Note how it responds.

Add a Lessons Learned entry documenting this as if it were a real mistake caught in review — follow the format from the Task 1 template:


```
## Lessons Learned
- 2026-XX-XX: [describe what Claude tried to do that violated a rule, and
  which rule caught it]. Rule reinforced after this was caught in review.
```

Discuss: how would this entry change behaviour in future sessions?


> **✅ M2 Complete when**
> CLAUDE.md contains specific, enforceable rules that Claude Code actually follows. @import is working with a shared standards file. At least one Lessons Learned entry exists.



# Module 3: Rubric-Based Eval Suite (60 minutes)

M3 builds the evaluation framework that protects code quality going forward. Without API access, evaluation works differently than the typical LLM-as-a-Judge pattern: instead of calling an API with live request/response pairs, the eval-runner sub-agent reads your actual source code and rubrics, and reasons about whether the implementation satisfies each rubric.


## Why Eval, and How It's Different Here

Manual testing a codebase by hand does not scale, and without API access there's no programmatic LLM-as-a-Judge calling a live endpoint. Instead, the eval-runner sub-agent performs static and behavioural analysis: it reads the relevant source files and reasons about whether the current implementation would produce the expected behaviour described by each rubric.

- Reproducibility — same 20 cases, same rubrics, every run, scored by reading the same code
- Best for logic bugs — excellent at catching wrong filters, type mismatches, missing edge cases
- Less suited to subjective quality — this method is not designed to judge subjective answer quality the way a live-response judge would


## Eval Case Structure

Each eval case names a scenario, describes the expected behaviour, and gives the eval-runner a specific, checkable rubric to apply against the actual code:


```
// eval/cases.json — structure of one eval case
{
  "id": "eval-001",
  "scenario": "Count claims currently in_review",
  "expected_behaviour": "The service correctly counts only claims with
    status == in_review, excluding pending_info.",
  "rubric": "Read claims_service.py. Confirm the count query filters on
    the exact string 'in_review'. Confirm it does not accidentally include
    pending_info. Score 1.0 if both checks pass, 0.5 if only one passes,
    0.0 if neither passes.",
  "tags": ["count", "status"]
}
```


### Build 20 Cases Across 6 Categories


| Category | Examples |
|---|---|
| count (×4) | Simple counts by status or type: 'How many approved claims?' |
| aggregation (×4) | Sums and averages: 'Total billed amount for denied claims' |
| member (×3) | Per-member lookups |
| provider (×3) | In/out-of-network queries |
| status (×3) | Lifecycle transition checks |
| edge (×3) | Empty results, invalid IDs, multi-part scenarios |



## Writing Rubrics That Actually Constrain the Score


```
# WEAK rubric — too vague to score consistently
"rubric": "Check if the claim counting logic is correct."
# Problem: "correct" is undefined. Different runs (or different
# reviewers) could score this 0.3 or 0.9 for the same code.
```


```
# STRONG rubric — specific, checkable conditions
"rubric": "Read count_claims_by_status. Score 1.0 only if ALL hold:
  (a) filter uses exact string match on status, not substring/LIKE match
  (b) pending_info is never included when counting in_review
  (c) a corresponding test exists in tests/.
  Score 0.5 if (a) and (b) hold but (c) is missing.
  Score 0.0 if (a) or (b) fails."
```


### Rubric-Writing Checklist

- Lists explicit, checkable conditions — not adjectives like 'correct' or 'good'
- Names the exact file/function to inspect
- Defines what 0.5 means — partial credit needs its own bar, not just 'in between'
- Avoids requiring subjective judgment where an objective check would do


## Running the Eval Suite


> 💬 **Prompt:**
> Use the eval-runner agent to score the current implementation of claims_service.py against eval/cases.json. Report per-case scores, the mean, and pass/fail at the 0.80 threshold.

Example output:


```
eval-001: 1.0 (in_review filter correct, excludes pending_info)
eval-002: 0.5 (filter correct, but uses float not Decimal)
eval-003: 1.0
...
Mean score: 0.84
PASS (threshold: 0.80)

Lowest-scoring cases:
eval-002 (0.5): Uses float for monetary sum
eval-014 (0.5): Multi-part query only handles first clause
```



## Task 1 — Write eval/cases.json

- Create the eval/ directory
- Write 20 eval cases covering all 6 categories above
- Write STRONG rubrics — explicit, checkable conditions
- Use the seed data values from the P1-L3 project


## Task 2 — Run the eval-runner Agent

Identical both platforms:


```
claude -p "Use the eval-runner agent to score eval/cases.json"
```

- Record the mean score and per-case results
- Identify the 3 lowest-scoring cases
- Read the code for those cases — does the score make sense to you?


## Task 3 — Fix the Lowest Scorer

- Pick the single lowest-scoring case
- Ask Claude Code (main session, not eval-runner) to fix the underlying issue
- Re-run the eval-runner agent on just that case
- Confirm the score improved


## Task 4 — Discuss Scoring Limits

- As a group: where did Claude Code's scoring feel reliable?
- Where did it feel uncertain or inconsistent between runs?
- What would you NOT trust this eval method to catch?
- Note this in CLAUDE.md's Lessons Learned

> **✅ M3 Complete when**
> eval/cases.json has 20 cases with strong rubrics. The eval-runner agent produces a mean score >= 0.80. You can explain what this method is and isn't reliable for.



# Module 4: Local Eval Gate (30 minutes)

M4 wires the eval-runner sub-agent into a local gate script. Before every commit you run scripts/run_eval_gate.sh — if the mean eval score drops below 0.80 the script exits with an error and you fix the code before committing. You will also deliberately break the gate to prove it works.


## Running the Eval Gate Locally

Claude Code in a CI runner needs to authenticate without a human present to complete an interactive browser sign-in. The mechanism is a long-lived claude.ai session tied to your claude.ai Pro/Team account.

- One token per pipeline — one claude.ai session per CI pipeline, scoped to your existing plan. Nothing new to provision or rotate
- Same usage limits as interactive use — CI eval runs draw from the same Pro/Team usage allowance. Heavy CI use can affect your interactive quota
- Token is still a secret — treat it exactly like any other credential: GitHub secret only, never committed


## Task 1 — Create the Gate Script

Create scripts/run_eval_gate.sh (note: inside a scripts/ subdirectory, not the project root):


```
#!/bin/bash
# scripts/run_eval_gate.sh
set -e

echo "=== Eval Gate ==="
claude -p "Use the eval-runner agent to score eval/cases.json.
  Output ONLY a JSON object: {\"mean\": <float>, \"pass\": <bool>}" \
  --output-format json > eval_result.json

python3 -c "
import json
r = json.load(open('eval_result.json'))
print(f'Mean eval score: {r[\"mean\"]:.2f}')
assert r['pass'], f'Eval failed: {r[\"mean\"]:.2f} < 0.80'
"
```


```
# Make it executable — native Terminal:
chmod +x scripts/run_eval_gate.sh
```



## Task 2 — Test the Gate


```
./scripts/run_eval_gate.sh
```

It should print "Mean eval score: X.XX" followed by no error if your code meets the 0.80 baseline. If it prints an AssertionError, the gate correctly failed.

Run the gate before every commit — if PASSED, commit as normal; if FAILED, fix the code and re-run before committing:


```
# If PASSED: commit as normal
git add .
git commit -m "your message"
# If FAILED: fix the code, then re-run before committing
```



## Task 3 — Verify the Gate Works: Trigger a Deliberate Failure

A gate that has never been triggered is a gate you don't know works. Deliberately break it — in a feature branch — before relying on it in production.

Step 1 — Create a test branch:


```
git checkout -b test/verify-eval-gate
```

Step 2 — Degrade the implementation. In claims_service.py, change the in_review filter to also match pending_info (violates the rubric in eval-001):


```
def count_in_review(claims):
    return [c for c in claims if c.status in ("in_review", "pending_info")]  # WRONG
```

Step 3 — Commit and push (identical both platforms):


```
git add claims_service.py
git commit -m "test: degrade filter to verify eval gate"
git push -u origin test/verify-eval-gate
```

Expected in local gate script:


```
eval-001: 0.0 (in_review incorrectly includes pending_info)
Mean eval score: 0.31
AssertionError: Eval failed: 0.31 < 0.80
Eval gate — FAILED
```



## Task 4 — Restore and Repass

Step 1 — Restore the original implementation:


```
git checkout main -- claims_service.py
```

Step 2 — Commit and push:


```
git add claims_service.py
git commit -m "fix: restore correct status filter"
git push
```

Expected in local gate script:


```
eval-001: 1.0
...
Mean eval score: 0.91
Eval gate — PASSED
```


> **💡 Keep the evidence**
> Copy the terminal output of both the failing and passing runs into your notes. The failing output is evidence that your gate is real, not decorative.



## Task 5 — Add the Eval Gate Step to CI

- Add the eval gate step to .github/workflows/ci.yml
- Commit and push to a feature branch
- Confirm the eval gate step appears and passes in the local gate script
- Push again after Task 4's restore — confirm all steps pass: lint, tests, eval gate
The pipeline is now production-ready for Session 2.


> **✅ M4 Complete when**
> scripts/run_eval_gate.sh exists, is executable, and produces PASSED on a clean codebase and FAILED on a deliberately degraded one. You have terminal output showing both.



# Session 1 Complete — What You Have Built

By completing all four modules, you have built the core engineering layer of the UHG Claims Intelligence Service using Claude Code exclusively:

- .claude/agents/ — eval-runner and security-reviewer sub-agents, scoped, reusable, version-controlled
- CLAUDE.md — a production contract: domain rules, output conventions, forbidden actions, and a living Lessons Learned section. Shared rules pulled in via @import
- eval/cases.json — 20 rubric-based test cases, scored by the eval-runner sub-agent reasoning over real code, not API calls
- .github/workflows/ci.yml — claude -p in headless mode, authenticated via a long-lived session, blocking merge on a failing eval score

> **✅ Session 1 artefacts**
> .claude/agents/eval-runner.md · .claude/agents/security-reviewer.md · CLAUDE.md · eval/cases.json · scripts/run_eval_gate.sh. All committed to your repository.



## Session 2 Preview

Session 2 wraps this Claude Code-engineered foundation in a production-grade shell:


| Module | Content |
|---|---|
| M5 — Deployment Concepts | Understanding consistent deployment. Ask Claude Code to create a deployment artefact for the service — no hands-on tooling required |
| M6 — Spec-Driven Engineering | Spec as source of truth — Claude Code reads the spec and derives implementation, tests, and docs from it |
| M7 — Security Controls | security-reviewer sub-agent auditing PII handling and injection risk on every PR |
| M8 — Governance | Git as audit trail, CLAUDE.md risk tiers, PR review conventions, escalation pattern |
| M9 — Multi-Agent Patterns | Hub-and-spoke orchestration for complex analysis tasks |
| M10 — Observability & Capstone | Code health observability over time, full end-to-end system demo and L3 patterns reference |



# Quick Reference


## Key Files


| File | Purpose |
|---|---|
| .claude/agents/eval-runner.md | Scored sub-agent — reads code, scores against eval/cases.json |
| .claude/agents/security-reviewer.md | Read-only sub-agent — audits PII handling and injection risk |
| CLAUDE.md | Production contract — domain rules, conventions, forbidden actions, Lessons Learned |
| eval/cases.json | 20 eval test cases — scenario, expected_behaviour, rubric, tags |
| scripts/run_eval_gate.sh | Calls claude -p headlessly, asserts mean score >= 0.80 |
| .github/workflows/ci.yml | CI pipeline: lint -> tests -> eval gate (headless Claude Code) |
| ~/uhg-standards/CLAUDE.md | Shared HIPAA baseline rules, pulled in via @import |



## Commands Reference


```
# Check Claude Code is installed and authenticated
claude --version
claude doctor
```
```
# List sub-agents available in this project
claude
> /agents
```
```
# Run a sub-agent interactively
> Use the eval-runner agent to score eval/cases.json
```
```
# Headless mode (non-interactive, for scripts/CI)
claude -p "<your prompt>"
claude -p "<your prompt>" --output-format json
```
```
# Run the local eval gate
./scripts/run_eval_gate.sh
```
```
# Check eval score history via Git
git log --oneline eval/cases.json
git log --oneline CLAUDE.md
```



# Session 1 — Final Checklist


| Item | Status |
|---|---|
| .claude/agents/eval-runner.md and security-reviewer.md exist | ✅ |
| Both sub-agents are invokable individually and in parallel | ✅ |
| CLAUDE.md contains specific, enforceable rules | ✅ |
| @import is working with a shared standards file | ✅ |
| At least one Lessons Learned entry exists | ✅ |
| eval/cases.json has 20+ cases across all 6 categories | ✅ |
| eval-runner reports mean score >= 0.80 | ✅ |
| scripts/run_eval_gate.sh exists and is executable | ✅ |
| You have proof: a FAILED run and a PASSED run | ✅ |
| Eval gate step added to .github/workflows/ci.yml | ✅ |
| You can explain when to use -p (headless) vs interactive mode | ✅ |




# L3 · SESSION 2 — Hardening & Operating the System: Deployment, Spec-Driven Engineering, Security, Governance, Orchestration, Observability (Modules 5–10)

---



For Claude Code installation, also see: Engineering Excellence | Claude Code Setup — https://unify.hcp.uhg.com/offerings/engineering-excellence/docs/claude-code-setup



# 4. Installation


## 4.1 Claude CLI (Claude Code)


### Shared steps (apply to both Windows and macOS)

These steps are identical on both operating systems. If you completed Session 1 on the same machine, Claude Code is already installed — skip to the Overview below.

Step A — Confirm prerequisites. Verify that all of Section 3 is complete: secure group approved, Claude Console Access, Optum AppStore access confirmed.

Step B — Authentication. Select option 1. Claude account with subscription.



### Install & Verify — by Platform


```
1. Open Optum AppStore
2. Search for "Claude Code CLI"
3. Select Install; wait for deployment
4. Open a NEW Terminal window
```
```
claude --version
```
*A version number should print without errors.*
```
claude doctor
```
*Deeper check of install, authentication, and configuration.*

If claude is not recognized, close and reopen your terminal window.



# Overview

Session 2 wraps the Claude Code-engineered foundation from Session 1 in a production-grade shell. Every module adds one layer, and every layer is built with the same constraint as Session 1: Claude Code on your claude.ai Pro or Team account is the only interface to Claude anywhere in this project. Commands are shown side by side for Windows (PowerShell) and macOS (Terminal) — use the column for your platform.


> **📋 Prerequisite**
> Session 1 complete. .claude/agents/eval-runner.md, .claude/agents/security-reviewer.md, CLAUDE.md, eval/cases.json, and a passing eval gate in CI must all be in place before M5 begins.



# Before You Start — Pre-Session 2 Checklist

Verify these items before M5 begins. If any fails, fix it — a broken Session 1 foundation makes every Session 2 step unreliable.


## Session 1 Artefacts

- .claude/agents/eval-runner.md and .claude/agents/security-reviewer.md both exist
- CLAUDE.md contains domain rules, output conventions, forbidden actions
- eval/cases.json has 20 cases
- claude -p "Use the eval-runner agent to score eval/cases.json" reports mean >= 0.80
- CI pipeline passes: lint + tests + eval gate all green on main


## Deployment Tooling

- Confirm your deployment tooling is available (Podman, Docker, or equivalent)
- Confirm podman-compose or docker-compose is available
- Confirm container images are accessible in the workshop environment


## GitHub

- run_eval_gate.sh already set as a local gate (from Session 1, M4)
- You have permission to open commits on the workshop repository


# Module 5: Deployment Concepts (30 minutes)

M5 packages the Claims Intelligence Service into a deployment container — written with Claude Code's help, not from memory — and wires a CI step that confirms the image builds and responds to /health. podman-compose brings up two services: the FastAPI API and a PostgreSQL database.


## Task 1 — Ask Claude Code to Write the Containerfile

Rather than copying a Containerfile template from memory, ask Claude Code to read your actual project and write one that fits it — the same instinct as M1's sub-agents: let the tool read the real files instead of guessing.

Start Claude Code (identical both platforms):


```
claude
```


> 💬 **Prompt:**
> This FastAPI service needs a Containerfile. Read main.py and requirements.txt, then write a Containerfile that:
- uses python:3.11-slim
- installs dependencies before copying code, for layer caching
- exposes port 8000
- runs with uvicorn, no --reload
Then build the image and fix any errors you hit.

Expected output from Claude Code:


```
# Containerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```


> **💡 Never use --reload in the Containerfile CMD**
> That flag watches the filesystem for changes and is only for development. Always review what Claude Code generates — it usually gets this right, but you decide if it's correct for your service.

Review the generated Containerfile line by line before accepting it. Add /health to main.py if Claude Code didn't already.


```
podman build -t claims-intelligence .
```

Confirm no errors.



## Task 2 — podman-compose.yml — Two Services

Claude Code will produce a podman-compose.yml with two services: api and db. No reverse proxy — FastAPI is accessed directly on port 8000.


> 💬 **Prompt:**
> Write a podman-compose.yml with two services: api (built from the Containerfile, port 8000) and db (postgres:16-alpine). The api should depend_on db with condition: service_healthy. Include a postgres healthcheck and a volume for pgdata.

Expected output (same YAML format as docker-compose):


```
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: uhg
      POSTGRES_PASSWORD: uhg
      POSTGRES_DB: claims_audit
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U uhg"]
      interval: 10s
      retries: 5
volumes:
  pgdata:
```


> **💡 Why service_healthy matters**
> service_healthy on depends_on ensures the api container waits until PostgreSQL is fully ready — not just started. Without this, api may fail on startup with connection errors.

What each service is for: db is not for LLM audit logs (unlike an API-based design, there's no AuditRecord table — Git is the audit trail, see M8). It's for application data only — if the service grows beyond in-memory seed data, db is where claims/members/providers would live. Still worth practising: multi-service compose, health checks, and volumes are real production skills, independent of any LLM-specific reason to use them.



## Task 3 — Test the Deployment


```
podman-compose up --build
```

Wait for services to start. Then test:


```
curl http://localhost:8000/docs
```
*macOS curl is already the real binary — no .exe needed.*

FastAPI docs should load. Then verify the health endpoint and application behavior:


```
curl 'http://localhost:8000/claims/count?status=in_review'
```
```
podman-compose restart api
```
*Verify it restarts cleanly.*
```
podman-compose logs api
```
*Confirm requests are logged.*

Confirm the response matches the seed data (3). Tear down when finished:


```
podman-compose down -v
```



## Task 4 — Wire Deployment Into CI/CD

Add a verify-container job to .github/workflows/ci.yml. It builds the deployment image and confirms /health responds — all inside the CI runner. No external registry, no SSH, no deploy target required.


```
verify-container:
  needs: test  # eval gate (S1-M4) must pass first
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Build deployment image
      run: podman build -t claims-intelligence .
    - name: Start services
      run: podman-compose up -d
    - name: Wait for api to be ready
      run: |
        for i in {1..15}; do
          curl -sf http://localhost:8000/health && break
          echo "Waiting... attempt $i"; sleep 3
        done
    - name: Verify /health responds
      run: curl -sf http://localhost:8000/health | grep '"status":"ok"'
    - name: Tear down
      if: always()
      run: podman-compose down -v
```

Set needs: test — the eval gate must pass before the container step runs. Push to a feature branch and watch the job run. Confirm the artefact build and /health check both pass in the CI log.


> **✅ M5 Complete when**
> Claude Code has produced a Containerfile and podman-compose.yml, reviewed and committed. /health endpoint is implemented in main.py. You can explain what each artefact does and why.



# Module 6: Spec-Driven Engineering (45 minutes)

M6 introduces spec-driven engineering: the practice of writing a specification first and letting Claude Code derive the implementation, tests, and documentation from it. Drift between spec and code becomes a first-class defect, caught by CI rather than discovered in production.


## What Spec-Driven Engineering Is

The usual pattern is: write code, write tests (sometimes), write docs (later, maybe). The spec, if it exists at all, drifts. The spec-driven way reverses this:

- Write the specification (OpenAPI, ADR, requirements doc)
- Claude Code reads the spec
- Claude Code generates implementation stubs matching the spec's contracts
- Claude Code generates tests from the spec's contracts — one test per response code defined
- Spec drift becomes a CI failure, not a conversation


## Task 1 — Create an OpenAPI Spec

Create openapi.yaml with endpoint definitions:


```
paths:
  /claims/{claim_id}/status:
    get:
      summary: Get current claim status
      parameters:
        - name: claim_id
          in: path
          required: true
          schema:
            type: string
            pattern: "^CLM-[0-9]+"
      responses:
        "200":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ClaimStatus"
        "404":
          description: Claim not found
```



## Task 2 — Generate From the Spec


```
claude
```


> 💬 **Prompt:**
> Read openapi.yaml. Implement every endpoint so it satisfies every contract in the spec: parameter patterns, response schemas, and all response codes. Then write a pytest for each response code the spec defines. Flag any existing code that contradicts the spec.

Expected generated output:


```
# main.py - generated from spec
@app.get("/claims/{claim_id}/status")
def get_claim_status(claim_id: str):
    if not re.match(r"^CLM-[0-9]+", claim_id):
        raise HTTPException(400)
    claim = claims_service.get(claim_id)
    if not claim:
        raise HTTPException(404)  # spec: 404
    return ClaimStatus(**claim)  # spec: 200

# test_claims.py - generated from spec contracts
def test_status_200(): ...   # spec says 200 exists
def test_status_404(): ...   # spec says 404 exists
```

Review the generated endpoint stub and the generated tests. Run the tests and confirm they pass:


```
pytest tests/ -v
```

Commit (identical both platforms):


```
git commit -m "feat: generate from spec"
```



## Task 3 — Find and Fix Drift


> 💬 **Prompt:**
> Read openapi.yaml and review main.py. Flag any route that contradicts the spec.

Read the findings — are they accurate? Discuss as a group.

Deliberately introduce a drift: change a response code in main.py without updating the spec. Re-run the same prompt — confirm Claude Code catches it.



## The Spec as Ongoing Source of Truth

Use the spec continuously — not just at greenfield. Three ongoing prompts:


> 💬 **Prompt:**
> Catch drift: Read openapi.yaml and review main.py. Flag any route that contradicts the spec.


> 💬 **Prompt:**
> Extend the system: I've added a new route to openapi.yaml. Implement it and write the tests.


> 💬 **Prompt:**
> Keep tests honest: Check test_claims.py against openapi.yaml. Are there response codes in the spec with no test?



## Task 4 — Discuss and Note

- Which spec format fits this project best: OpenAPI, ADR, or plain requirements doc?
- What would you put in the spec that Claude Code could not infer from the code alone?
- Add a note to CLAUDE.md: which parts of this service should be spec-driven going forward?

> **✅ M6 Complete when**
> Claude Code has generated an endpoint and tests from the spec. You have found and demonstrated at least one drift. You can explain what spec-driven engineering changes about how you work with Claude Code.



# Module 7: Security via Sub-Agent (60 minutes)

M7 puts the security-reviewer sub-agent — built in Session 1, M1 — to real work. Security review happens at review time: a human or Claude Code implements a fix, then security-reviewer audits it, and the same review runs automatically on every commit.


## Why a Sub-Agent Review, Not Runtime Middleware

It's worth being explicit about what this module is and isn't. A request-time PII classifier would need the running FastAPI service to call Claude on every request at runtime. What we build instead is review-time security: the same security-reviewer sub-agent from M1 reads a diff and reports findings, either when you ask it or automatically on every PR.

- Zero runtime cost — no LLM call happens when a real user hits the API. The review already happened in CI, before merge
- Catches code patterns, not live input — security-reviewer is excellent at 'this line logs a raw request body' and less suited to judging one specific user's live message in real time
- A human still decides — security-reviewer reports; it never fixes, blocks, or decides anything on its own (tools: Read, Grep only, set in M1)


## Task 1 — Implement PII-Safe Logging


```
claude
```


> 💬 **Prompt:**
> Add request logging to main.py. Every request should log the endpoint and a hash of any path/query parameters containing member_id or claim_id — never the raw value. Follow the Forbidden Actions in CLAUDE.md.

Expected output from Claude Code:


```
import hashlib, logging
logger = logging.getLogger("claims_intelligence")

def _safe_log_id(raw_id: str) -> str:
    """Hash an identifier before logging - never log raw IDs."""
    return hashlib.sha256(raw_id.encode()).hexdigest()[:12]

@app.get("/claims/member/{member_id}")
def member_claims(member_id: str):
    logger.info(f"member_claims request: id_hash={_safe_log_id(member_id)}")
    ...
```

Review the generated _safe_log_id() function. Confirm no raw member_id or claim_id appears in any log statement. Run the service and check actual log output.



## Task 2 — Audit the Work


> 💬 **Prompt:**
> Use the security-reviewer agent to audit main.py for any logging statement that could write a raw identifier in plaintext.

security-reviewer runs in isolated context and reports findings without modifying code.


### The Review Loop

- 1. You ask the main session to implement a feature
- 2. The main session writes the code
- 3. You delegate to security-reviewer to audit it
- 4. security-reviewer reports findings — does not fix them
- 5. You decide what to fix; the main session applies the fix
Deliberately reintroduce a raw-ID log statement, then re-run security-reviewer — confirm it catches the regression.



## Task 3 — Run security-reviewer on Every Pull Request

Wire the same sub-agent into CI so review happens automatically, not only when someone remembers to ask for it.

Run security-reviewer locally before committing any change that touches request handling, logging, or external endpoints — identical both platforms:


```
# Step 1: Generate a diff of your staged changes
git diff HEAD > my_diff.txt

# Step 2: Run the security-reviewer sub-agent on it
claude -p "Use the security-reviewer agent to audit my_diff.txt for PII
  handling and injection risk. Output a markdown report."

# Step 3: Read the findings, fix any issues, then commit
# Remove the temp diff file
rm my_diff.txt
```

Add the security-review job to ci.yml so this runs on every PR. What this gives the team: review happens automatically (every PR gets a security pass without anyone remembering to ask for it manually), findings are visible not blocking (this posts a comment; it doesn't fail the build — a human still decides what's a real issue), and a consistent rubric every time (same agent definition, same checks, regardless of who's reviewing).

Open a test PR with a small, deliberate PII logging mistake. Confirm the PR comment appears with the finding. Fix the mistake and confirm the next run reports clean.



## Task 4 — Discuss the Limits

- What kinds of security issues would this NOT catch?
- Would you trust this as your only security review? Why or why not?
- Add a note to CLAUDE.md about when human review is still required
- Compare with the M3 (Session 1) discussion on eval-runner's limits

> **✅ M7 Complete when**
> A PII-safe logging pattern is implemented and verified by security-reviewer. The sub-agent runs automatically on every PR and posts findings as a comment.



# Module 8: Governance via Git & CLAUDE.md (45 minutes)

M8 builds the governance layer without any new infrastructure. An API-based design would write a structured AuditRecord to a database on every LLM call; this project has no LLM calls at runtime to log. Instead, Git history is the audit trail, and CLAUDE.md carries the risk-tagging and escalation conventions that would otherwise live in a database schema.


## Git History as the Audit Trail

Every change to this codebase is already a commit — who changed what, when, and why is already captured by Git. There's no need to build a parallel logging system to capture information Git already has. Identical both platforms:


```
# Every change to claims_service.py has:
git log --oneline services/claims_service.py
# a1b2c3d fix: correct total_billed_for_status to use Decimal
# e4f5g6h feat: add is_out_of_network check
# i7j8k9l initial claims_service implementation

# Who approved it, and why — full diff, commit message, author,
# timestamp, already there:
git log -p --follow services/claims_service.py | head -50

# Was Claude Code involved? Check CLAUDE.md's Lessons Learned
# and commit messages - convention, not infrastructure:
git log --grep="claude-assisted" --oneline
```

- Every change is already a commit — Git gives you who, what, when, and a full diff, for free, with zero new infrastructure
- No new database to secure — an AuditRecord table is one more thing to back up, secure, and migrate. Git is already battle-tested for this
- Reviewable by anyone with repo access — git log doesn't need a custom query API; any teammate or auditor can read the same history you can


## Task 1 — Tag Risk in CLAUDE.md

Risk classification doesn't need a database column — it needs a documented convention that's actually followed. Add a Risk Tiers section to CLAUDE.md:


```
## Risk tiers (EU AI Act-aligned)
Tag every PR description with one of these tiers:

- HIGH: touches claim status transitions, payment amounts, or
  approval/denial logic. Requires a second human reviewer on the
  PR - Claude Code review alone is not sufficient.

- LIMITED: touches status display, member/provider lookups, or
  read-only aggregation. security-reviewer + eval-runner checks
  required; single human reviewer sufficient.

- MINIMAL: touches tests, docs, or non-functional refactors.
  Standard PR review applies.

## Escalation rule
If eval-runner reports a case below 0.5, OR security-reviewer flags
a HIGH-risk pattern, the PR description must include an
"Escalation:" line explaining what a human reviewer should
specifically check before approving.
```


> **💡 Why CLAUDE.md, not a HITL database table**
> No runtime system to build — an API-based design would need a HITLQueue table and a function called from every API request. There's no API here to call it from. Enforced by review, not infrastructure — the PR template and CLAUDE.md rule are the enforcement mechanism. Still auditable — risk tier lives in the PR description, which is permanent, searchable history, just like a database row, without needing a database.

Commit (identical both platforms):


```
git commit -m "docs: add risk tiers and escalation rule"
```

Confirm git log shows the change clearly.



## Task 2 — Create a PR Template

Create .github/PULL_REQUEST_TEMPLATE.md (this exact filename and casing — it's the GitHub-recognized convention) with a 'Risk tier:' field:


```
## Risk tier
- [ ] HIGH — status transitions, payment amounts, approval/denial logic
- [ ] LIMITED — status display, lookups, read-only aggregation
- [ ] MINIMAL — tests, docs, non-functional refactors

## Escalation
(Required if tier is HIGH. Explain what a human reviewer should
specifically check before approving.)

## What changed
...

## Why
...

## Tests
- [ ] Eval gate passes (>= 0.80)
- [ ] New tests for new code
- [ ] Security review (if HIGH tier)

## Checklist
- [ ] CLAUDE.md followed
- [ ] No git push --force
- [ ] Commit message is semantic
```

Add an 'Escalation:' field, optional unless tier is HIGH. Open a test PR touching claims_service.py. Fill in the template honestly — what tier is this change?



## Task 3 — Trigger an Escalation

- Make a change that would score below 0.5 on an eval case
- Run eval-runner — confirm the low score
- Add the required Escalation: line to your PR description
- Discuss: who should review this before merge?


## Task 4 — Review the Audit Trail

- git log --oneline — review the full change history so far
- Confirm every meaningful change has a clear commit message
- Discuss: could a compliance auditor reconstruct what happened from this alone?

> **✅ M8 Complete when**
> CLAUDE.md has a Risk Tiers section and Escalation rule. A PR template requires a risk tier on every PR. Git history is a clean, readable record of every change.



# Module 9: Multi-Agent Orchestration (30 minutes)

M9 applies the hub-and-spoke pattern from Session 1, M1 to a real, multi-dimensional claims analysis task. A single question like "give me a full picture of this claim" decomposes naturally into several independent checks — this module is about recognising that decomposition and routing it correctly, not about writing any new orchestration code.


## From Concept to Practice

Recall the hub-and-spoke pattern: the main session (the hub) delegates independent sub-tasks to sub-agents (the spokes), which run in isolation and report back. M9 is the first time you'll apply this to a task with real business stakes.

The task: "Give me a full picture of CLM-007 before I decide whether to approve it." This needs four independent checks. In an interactive Claude Code session (the hub):


> 💬 **Prompt:**
> I need a full analysis of CLM-007. Run these independently, in parallel, and report back together:
1. Use eval-runner's approach: read claims_service.py and confirm CLM-007's status logic is correct for its current state (pending_info, out-of-network)
2. Use security-reviewer to confirm no PII from this claim would leak into logs if queried
3. Read CLAUDE.md's Risk Tiers section and tell me which tier a decision on CLM-007 falls under
4. Check git log for any recent changes to the out-of-network logic that might affect this claim

Four spokes, one hub, one combined report. None of the four need to talk to each other — each reads what it needs and reports back independently.



## Sequential vs Parallel — How to Decide

- Parallel — the four tasks above. None depends on another's output, so they can all run at once
- Sequential — "fix the bug, then re-run eval-runner" requires the fix to land before the re-check makes sense

> **💡 Rule of thumb**
> If you can't answer 'does this need the other one's output first?' with yes, run it in parallel.



## M9 Design Exercise

Work through this as a group (15 minutes). There is no code to write — the deliverable is a clear breakdown, on paper or in a shared doc.


> **📋 The task**
> Design a hub-and-spoke breakdown for: "Before renewing MBR-003's plan, give me a complete risk picture — claims history, any compliance flags, and whether recent code changes affect how their claims are processed."


### Questions to Work Through

- How many independent spokes does this decompose into? What is each one's single job?
- Which existing sub-agent (eval-runner or security-reviewer) does each spoke map to, if any — or does it need a new one?
- Are any of these sequential rather than parallel? Why?
- Who merges the final report — a third sub-agent, or you, in the main session? Why?

> **✅ M9 Complete when**
> Your group can clearly state the spokes, their tool scope, and whether each runs in parallel or sequentially, with a reason for each decision.



# Module 10: Observability & Capstone (30 minutes)

M10 closes the loop. First, a code health trend script; then a full commit walked through the complete L3 workflow; then participants identify which patterns they'll adopt first. The session ends with a CLAUDE.md Lessons Learned update.


## Observability Without a Running LLM Service

How do you know quality is staying good over time, not just on the commit you happen to be looking at? Without a running LLM service, there's no request volume or API cost to meter — so observability here means tracking eval score, test coverage, and lint cleanliness as they change across commits.


| Old Model (API-Based Service) | This Model (Claude Code as Dev Tool) |
|---|---|
| avg_latency_ms per LLM call | eval-runner score over time (per commit) |
| avg_cost_usd per call, total spend | Test coverage % over time |
| calls_today, live request volume | flake8 issue count over time |
| escalation_count from runtime HITL queue | security-reviewer findings count per PR |


> **💡 Same goal, different signals**
> Catch quality regressions early — but there's no runtime LLM traffic to measure here, so the signals are different.



## Task 1 — Build and Run code_health.sh

Create scripts/code_health.sh:


```
#!/bin/bash
# scripts/code_health.sh
echo "=== Code Health Report ==="
echo
echo "Test coverage:"
pytest tests/ --cov=. --cov-report=term-missing | tail -3
echo
echo "Lint issues:"
flake8 . --max-line-length=100 | wc -l
echo
echo "Eval score (current commit):"
claude -p "Use the eval-runner agent to score eval/cases.json.
  Output ONLY the mean score as a number." --output-format text
echo
echo "Recent eval score history (from commit messages):"
git log --oneline --grep="eval:" -10
```


```
# Make it executable — native Terminal:
chmod +x scripts/code_health.sh
```
```
./scripts/code_health.sh
```

Confirm coverage, lint count, and eval score all print correctly.


> **💡 Run this**
> After every merge to main — as a CI step that posts to a team channel. Before a release — as a manual go/no-go check. Weekly — to spot slow drift before it becomes a crisis. This is a starting point, not a finished dashboard — the point of this module is the pattern, not the polish.



## Task 2 — Simulate a Quality Regression

- Temporarily degrade claims_service.py (as in Session 1-M4's gate test)
- Run ./scripts/code_health.sh — observe the eval score drop
- Restore the code
- Re-run and confirm the score recovers

> **✅ M10a Complete when**
> code_health.sh runs cleanly and reports coverage, lint count, and eval score. You've seen the eval score number move when code quality changed.



## End-to-End: A Pull Request Through the Full L3 Workflow

Every meaningful change to this codebase now follows this 10-step path:


| # | Step |
|---|---|
| 1 | git checkout -b feature/claim-summary — open a feature branch |
| 2 | Build with Claude Code — interactive session, code follows the CLAUDE.md contract |
| 3 | eval-runner check — claude -p scores the change against eval/cases.json, locally, before committing |
| 4 | Commit with a clear message — this IS the audit trail (M8) |
| 5 | Tag the commit with a risk tier per CLAUDE.md conventions |
| 6 | Run local checks: flake8 . and pytest tests/ -v |
| 7 | Run the eval gate: ./scripts/run_eval_gate.sh — must PASS before committing |
| 8 | CI: container verify — podman build + /health check (M5) |
| 9 | Run security review: claude -p "Use security-reviewer on my_diff.txt" (M7) |
| 10 | Human review — a person reads the diff, the eval score, and the security report, then commits |



## L3 Pattern Reference Card

Adopt these in order of priority on your next team project:


| # | Pattern — Adopt When |
|---|---|
| 1 | Sub-agents with scoped tool permissions — before any repeated review task |
| 2 | CLAUDE.md as enforceable contract — day 1 of any Claude Code project |
| 3 | Eval gate in CI (headless mode) — before first production deploy |
| 4 | Security review as a sub-agent, in CI — before merging anything touching PII or external input |
| 5 | Git + CLAUDE.md as the governance system — from the first commit |



## CLAUDE.md Lessons Learned — L3 Session 2

Add a final Lessons Learned section to your CLAUDE.md. Record what L3 changed about how you work with Claude Code in production systems:


```
## Lessons Learned — L3 Session 2

### What I changed after L3
- [List the one pattern you will adopt first on your next project]
- [List what you would do differently if starting the Claims
  Intelligence Service from scratch]

### Production Claude Code dos
- Define scoped sub-agents before relying on repeated review tasks -
  least privilege by design
- Use headless mode (-p) for anything scriptable or run in CI
- Treat CLAUDE.md as a contract, not documentation - specific,
  checkable rules only
- Let Git history be the audit trail - don't build a parallel
  logging system for what Git already captures

### Production Claude Code don'ts
- Don't ask a sub-agent to do two unrelated jobs - one agent, one
  job, one set of permissions
- Don't skip the eval gate to ship faster - it costs more later
- Don't trust an automated review as the only review for HIGH-risk
  changes
- Don't forget -p in any CI step - it will hang the pipeline
```


> **✅ M10 Complete when**
> code_health.sh runs cleanly. You've walked through the full 10-step PR workflow end to end. Your CLAUDE.md has a final Lessons Learned entry for L3 Session 2.



# L3 Complete — What You Have Built

Across both sessions, you have built a complete, production-minded system using Claude Code exclusively:

- Engineering Layer (Session 1) — sub-agent library, CLAUDE.md as a production contract, a rubric-based eval suite, and a headless CI eval gate
- Deployment Layer (M5) — Containerfile and podman-compose.yml, created with Claude Code, verified by a CI step with no registry and no deploy target
- Spec-Driven Layer (M6) — spec as source of truth — Claude Code derives implementation and tests from it
- Security Layer (M7) — a PII-safe logging pattern, audited by the security-reviewer sub-agent on every commit
- Governance Layer (M8) — Git history as the audit trail, risk tiers and escalation rules documented in CLAUDE.md, enforced through a PR template
- Orchestration Layer (M9) — the hub-and-spoke pattern applied to real, multi-dimensional claims analysis
- Observability Layer (M10) — eval score, coverage, and lint trend tracked over Git commits

> **✅ L3 Complete**
> Every change is reviewed, scored, audited, and risk-tagged — entirely through Claude Code on a claude.ai Pro/Team account.



# Quick Reference


## Key Files Added in Session 2


| File | Module — Purpose |
|---|---|
| Containerfile | M5 — Containerise the FastAPI service, written with Claude Code |
| podman-compose.yml | M5 — Orchestrate api + db (PostgreSQL), two services, VM-local |
| [logging pattern in main.py] | M7 — _safe_log_id(), PII-safe request logging, audited by security-reviewer |
| .github/workflows/ci.yml (+security-review job) | M7 — Runs security-reviewer on every PR diff, posts findings as a comment |
| CLAUDE.md (+Risk Tiers section) | M8 — EU AI Act-aligned risk tiers and escalation rule |
| .github/PULL_REQUEST_TEMPLATE.md | M8 — Requires Risk tier: and Escalation: fields on every PR |
| scripts/code_health.sh | M10 — Reports coverage, lint count, and eval score in one run |



## Commands Reference


```
# Deployment tooling
podman build -t claims-intelligence .
podman-compose up --build
podman-compose up -d
podman-compose logs -f api
podman-compose restart api
podman-compose down -v
```
```
# Sub-agents
claude -p "Use the eval-runner agent to score eval/cases.json"
claude -p "Use the security-reviewer agent to audit main.py"
```
```
# Code health
./scripts/code_health.sh
```
```
# Audit trail
git log --oneline services/claims_service.py
git log -p --follow CLAUDE.md
git log --grep="eval:" --oneline
```



# Session 2 — Final Checklist


| Item | Status |
|---|---|
| Containerfile and podman-compose.yml created and tested | ✅ |
| /health endpoint implemented in main.py | ✅ |
| verify-container CI job added, passing | ✅ |
| OpenAPI spec written and Claude Code generated from it | ✅ |
| Drift detection working: Claude Code flags spec violations | ✅ |
| PII-safe logging implemented and verified by security-reviewer | ✅ |
| security-reviewer wired into CI, posts PR comments | ✅ |
| CLAUDE.md has Risk Tiers + Escalation rule | ✅ |
| .github/PULL_REQUEST_TEMPLATE.md in place with risk tiers | ✅ |
| Full workflow tested: commit → eval gate → CI → PR → merge | ✅ |
| scripts/code_health.sh runs cleanly, shows regression + recovery | ✅ |
| You can orchestrate multiple sub-agents on complex tasks | ✅ |
| You understand Git as audit trail for governance | ✅ |
| Final CLAUDE.md Lessons Learned entry added for L3 | ✅ |



