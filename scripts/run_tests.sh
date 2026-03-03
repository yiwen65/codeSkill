#!/usr/bin/env bash
set -euo pipefail

run_cmd() {
  local cmd="$1"
  echo "> $cmd"
  eval "$cmd"
}


has_npm_script() {
  local name="$1"
  if [[ ! -f package.json ]]; then
    return 1
  fi
  node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts['$name'] ? 0 : 1)" >/dev/null 2>&1
}

if [[ -f package.json ]]; then
  PM="npm"
  if command -v pnpm >/dev/null 2>&1 && [[ -f pnpm-lock.yaml ]]; then
    PM="pnpm"
  fi

  echo "Detected Node stack ($PM). Running quality gates..."
  if has_npm_script format; then run_cmd "$PM run format"; else echo "- skip format (script missing)"; fi
  if has_npm_script lint; then run_cmd "$PM run lint"; else echo "- skip lint (script missing)"; fi
  if has_npm_script typecheck; then run_cmd "$PM run typecheck"; else echo "- skip typecheck (script missing)"; fi
  if has_npm_script test; then run_cmd "$PM test"; else echo "- skip test (script missing)"; fi
  exit 0
fi

if [[ -f pyproject.toml || -f pytest.ini || -d tests ]]; then
  echo "Detected Python stack. Running quality gates..."

  if command -v ruff >/dev/null 2>&1; then
    run_cmd "ruff check ."
  else
    echo "- skip ruff (not installed)"
  fi

  if command -v mypy >/dev/null 2>&1 && [[ -f mypy.ini || -f pyproject.toml ]]; then
    run_cmd "python3 -m mypy ."
  else
    echo "- skip mypy (not installed or not configured)"
  fi

  run_cmd "python3 -m pytest -q"
  exit 0
fi

if [[ -f go.mod ]]; then
  echo "Detected Go stack. Running quality gates..."
  if command -v gofmt >/dev/null 2>&1; then
    run_cmd "gofmt -w ."
  else
    echo "- skip gofmt (not installed)"
  fi
  run_cmd "go test ./..."
  exit 0
fi

if [[ -f Cargo.toml ]]; then
  echo "Detected Rust stack. Running quality gates..."
  run_cmd "cargo fmt --check"
  run_cmd "cargo clippy -- -D warnings"
  run_cmd "cargo test"
  exit 0
fi

echo "No recognized test stack. Add task-specific test_plan commands in docs/PLAN.yaml."
exit 0
