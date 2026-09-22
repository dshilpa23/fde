#!/bin/bash
# scripts/code_health.sh
# Run after every merge to main, before a release, or weekly to spot
# slow drift before it becomes a crisis (M10).

echo "=== Code Health Report ==="

echo
echo "Test coverage:"
pytest tests/ --cov=. --cov-report=term-missing | tail -3

echo
echo "Lint issues:"
flake8 . --max-line-length=100 | wc -l

echo
echo "Eval score (current commit):"
claude -p "Use the eval-runner agent to score eval/cases.json. Output ONLY the mean score as a number." --output-format text

echo
echo "Recent eval score history (from commit messages):"
git log --oneline --grep="eval:" -10
