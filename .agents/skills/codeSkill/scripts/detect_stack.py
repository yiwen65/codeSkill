#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess


def repo_root() -> Path:
    try:
        out = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
        return Path(out)
    except Exception:
        return Path('.').resolve()


ROOT = repo_root()

checks = {
    'node': ['package.json'],
    'python': ['pyproject.toml', 'requirements.txt', 'pytest.ini'],
    'go': ['go.mod'],
    'rust': ['Cargo.toml'],
}

detected = []
for name, markers in checks.items():
    if any((ROOT / m).exists() for m in markers):
        detected.append(name)

print(json.dumps({'project_root': str(ROOT), 'stacks': detected}, ensure_ascii=False))
