#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path('.').resolve()

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

print(json.dumps({'root': str(ROOT), 'stacks': detected}, ensure_ascii=False))
