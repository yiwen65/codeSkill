# Implementation Plan

## Milestones
- M1: 搭建 todo 领域模型与 JSON 存储
- M2: 实现 CLI 与测试

## Task Breakdown

### TASK-001: 实现任务存储与领域逻辑
- Goal: 支持新增、查询、完成任务
- Files touched: `example_project/src/todo.py`
- Acceptance:
  - [ ] 可新增任务并生成递增 ID
  - [ ] 可读取任务列表
  - [ ] 可按 ID 标记任务完成
- Test plan:
  - `python3 -m unittest discover -s example_project/tests -p 'test_*.py'`
- Dependencies:
- Risk: JSON 文件损坏导致读取失败

### TASK-002: 实现 CLI 与示例测试
- Goal: 提供 add/list/done 命令并验证主要行为
- Files touched: `example_project/src/cli.py`, `example_project/tests/test_todo.py`
- Acceptance:
  - [ ] add/list/done 可用
  - [ ] 错误输入返回可读信息
  - [ ] 自动化测试通过
- Test plan:
  - `python3 -m unittest discover -s example_project/tests -p 'test_*.py'`
- Dependencies: TASK-001
- Risk: 参数解析失败导致命令行为不一致
