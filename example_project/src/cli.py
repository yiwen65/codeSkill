from __future__ import annotations

import argparse
from pathlib import Path

from todo import TodoStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple todo CLI example")
    parser.add_argument("--db", default=str(Path("example_project") / "todo.json"))

    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")

    sub.add_parser("list", help="list tasks")

    done = sub.add_parser("done", help="mark task done")
    done.add_argument("id", type=int)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = TodoStore(args.db)

    if args.command == "add":
        task = store.add_task(args.title)
        print(f"added: [{task.id}] {task.title}")
        return 0

    if args.command == "list":
        tasks = store.list_tasks()
        if not tasks:
            print("no tasks")
            return 0
        for t in tasks:
            status = "x" if t.done else " "
            print(f"[{status}] {t.id}: {t.title}")
        return 0

    if args.command == "done":
        task = store.mark_done(args.id)
        print(f"done: [{task.id}] {task.title}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
