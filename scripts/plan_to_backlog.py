#!/usr/bin/env python3
"""Convert docs/PLAN.yaml to .agent_state/backlog.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load_plan(path: Path) -> dict:
    raw = path.read_text(encoding='utf-8')
    try:
        import yaml  # type: ignore
        return yaml.safe_load(raw) or {}
    except ModuleNotFoundError:
        # Fallback: support JSON-compatible YAML so script has no hard dependency.
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                'PyYAML not installed and PLAN.yaml is not JSON-compatible YAML. '
                'Install pyyaml or emit PLAN.yaml as JSON-compatible YAML.'
            ) from exc


def validate_task(task: dict, idx: int) -> None:
    required = [
        'id', 'title', 'goal', 'files_touched', 'acceptance',
        'test_plan', 'dependencies', 'risk'
    ]
    missing = [k for k in required if k not in task]
    if missing:
        raise ValueError(f'task#{idx} missing fields: {", ".join(missing)}')
    if not isinstance(task['acceptance'], list) or not task['acceptance']:
        raise ValueError(f"task#{idx} acceptance must be non-empty list")
    if not isinstance(task['test_plan'], list) or not task['test_plan']:
        raise ValueError(f"task#{idx} test_plan must be non-empty list")
    if not isinstance(task['files_touched'], list):
        raise ValueError(f"task#{idx} files_touched must be list")
    if not isinstance(task['dependencies'], list):
        raise ValueError(f"task#{idx} dependencies must be list")
    if not isinstance(task['risk'], str):
        raise ValueError(f"task#{idx} risk must be string")


def main() -> int:
    in_path = Path(sys.argv[1] if len(sys.argv) > 1 else 'docs/PLAN.yaml')
    out_path = Path(sys.argv[2] if len(sys.argv) > 2 else '.agent_state/backlog.json')

    if not in_path.exists():
        raise FileNotFoundError(f'{in_path} not found')

    data = load_plan(in_path)
    tasks = data.get('tasks', [])
    if not isinstance(tasks, list) or not tasks:
        raise ValueError('PLAN.yaml must contain non-empty tasks list')

    backlog = {'source': str(in_path), 'tasks': []}
    task_ids: set[str] = set()
    for i, task in enumerate(tasks, start=1):
        validate_task(task, i)
        task_id = str(task['id'])
        if task_id in task_ids:
            raise ValueError(f'duplicate task id found: {task_id}')
        task_ids.add(task_id)
        backlog['tasks'].append({
            **task,
            'id': task_id,
            'status': 'todo',
            'attempts': 0,
            'notes': ''
        })

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(backlog, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'wrote {out_path} with {len(backlog["tasks"])} tasks')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
