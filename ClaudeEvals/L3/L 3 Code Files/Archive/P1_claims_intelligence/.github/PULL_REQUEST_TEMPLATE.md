## What does this PR do?

[Brief description of changes]

## Risk tier

- [ ] 🔴 **HIGH** — touches claim status transitions, payment amounts, or member PII handling
- [ ] 🟡 **LIMITED** — touches status display, member/provider lookups, or read-only aggregation
- [ ] 🟢 **MINIMAL** — touches tests, docs, or non-functional refactors

## Escalation

_Required if tier is HIGH, or if eval-runner's mean score is below 0.80, or if
security-reviewer flags a HIGH-risk pattern. Optional otherwise._

Escalation: [what a human reviewer checked before merge, and why]

## Checklist

- [ ] Tests passing (`pytest tests/ -v`)
- [ ] Eval gate passing (`./scripts/run_eval_gate.sh`)
- [ ] `security-reviewer` run on the diff for any change touching request
      handling, logging, or external endpoints
- [ ] No hardcoded secrets or credentials
- [ ] PII properly hashed/masked in logs (`_safe_log_id()`, see CLAUDE.md)
- [ ] CLAUDE.md updated if this PR adds a new domain rule or Lessons Learned entry

## Reviewer notes

[Any additional context for reviewers]
