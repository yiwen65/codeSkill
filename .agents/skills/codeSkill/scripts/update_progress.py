#!/usr/bin/env python3
"""Update one task status in backlog.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 4:
        print('usage: update_progress.py <backlog.json> <task-id> <status> [note]')
        return 2

    backlog_path = Path(sys.argv[1])
    task_id = sys.argv[2]
    status = sys.argv[3]
    note = sys.argv[4] if len(sys.argv) > 4 else ''

    valid = {'todo', 'doing', 'done', 'blocked'}
    if status not in valid:
        raise ValueError(f'status must be one of: {", ".join(sorted(valid))}')

    data = json.loads(backlog_path.read_text(encoding='utf-8'))
    for task in data.get('tasks', []):
        if task.get('id') == task_id:
            task['status'] = status
            task['attempts'] = int(task.get('attempts', 0)) + 1 if status in {'doing', 'blocked'} else task.get('attempts', 0)
            if note:
                task['notes'] = note
            backlog_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
            print(f'updated {task_id} => {status}')
            return 0

    raise ValueError(f'task id not found: {task_id}')


if __name__ == '__main__':
    raise SystemExit(main())
