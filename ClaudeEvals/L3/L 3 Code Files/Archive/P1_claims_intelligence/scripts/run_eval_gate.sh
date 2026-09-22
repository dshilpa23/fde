#!/bin/bash
# scripts/run_eval_gate.sh
#
# Local eval gate (M4). Run this before every commit. If the eval-runner
# sub-agent's mean score drops below 0.80, this script exits 1 and you
# fix the code before committing. No CI runner, no API key, no secrets —
# authenticates via your existing claude.ai Pro/Team session (or, in CI,
# a long-lived token from `claude setup-token`).

set -e

echo "=== Eval Gate ==="

claude -p "Use the eval-runner agent to score eval/cases.json. Output ONLY a JSON object: {\"mean\": <float>, \"pass\": <bool>}" \
  --output-format json > eval_result.json

python3 -c "
import json, sys
r = json.load(open('eval_result.json'))
print(f'Mean eval score: {r[\"mean\"]:.2f}')
if not r['pass']:
    print(f'FAILED -- score {r[\"mean\"]:.2f} is below 0.80')
    print('Fix the lowest-scoring cases before committing.')
    sys.exit(1)
print('PASSED -- safe to commit')
"
