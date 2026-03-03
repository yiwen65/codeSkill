import tempfile
import unittest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from todo import TodoStore
from cli import main


class TodoStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db = Path(self.tmpdir.name) / "todo.json"
        self.store = TodoStore(self.db)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_add_and_list(self) -> None:
        self.store.add_task("learn ai")
        tasks = self.store.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "learn ai")
        self.assertFalse(tasks[0].done)

    def test_mark_done(self) -> None:
        task = self.store.add_task("write tests")
        done = self.store.mark_done(task.id)
        self.assertTrue(done.done)


class CliTests(unittest.TestCase):
    def test_cli_flow(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / "todo.json"
            self.assertEqual(main(["--db", str(db), "add", "task one"]), 0)
            self.assertEqual(main(["--db", str(db), "done", "1"]), 0)
            self.assertEqual(main(["--db", str(db), "list"]), 0)


if __name__ == "__main__":
    unittest.main()
