# DESIGN - Example Project (Todo CLI)

## Architecture
- `example_project/src/todo.py`: 领域模型与存储逻辑
- `example_project/src/cli.py`: 命令行入口与参数解析
- `example_project/tests/test_todo.py`: 单元测试

## Data Model
```json
{"id": 1, "title": "示例", "done": false}
```

## Design Choices
- 采用 Python 标准库（`argparse`, `json`, `pathlib`），降低依赖复杂度。
- 存储层与 CLI 分离，便于测试与扩展。
