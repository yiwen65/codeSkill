#!/usr/bin/env bash
set -euo pipefail

if [[ -f package.json ]]; then
  if command -v pnpm >/dev/null 2>&1 && [[ -f pnpm-lock.yaml ]]; then
    pnpm test
  else
    npm test
  fi
  exit 0
fi

if [[ -f pyproject.toml || -f pytest.ini || -d tests ]]; then
  python3 -m pytest -q
  exit 0
fi

if [[ -f go.mod ]]; then
  go test ./...
  exit 0
fi

if [[ -f Cargo.toml ]]; then
  cargo test
  exit 0
fi

echo "No recognized test stack. Add task-specific test_plan commands in docs/PLAN.yaml."
exit 0
