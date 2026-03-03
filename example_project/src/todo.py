from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


class TodoStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _read(self) -> list[Task]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [Task(**item) for item in data]

    def _write(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(t) for t in tasks]
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_tasks(self) -> list[Task]:
        return self._read()

    def add_task(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("title cannot be empty")
        tasks = self._read()
        next_id = max((t.id for t in tasks), default=0) + 1
        task = Task(id=next_id, title=title)
        tasks.append(task)
        self._write(tasks)
        return task

    def mark_done(self, task_id: int) -> Task:
        tasks = self._read()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                self._write(tasks)
                return task
        raise ValueError(f"task id not found: {task_id}")
