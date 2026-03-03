# Interview Notes

## Round 1
- Problem: 给新手一个“可直接跑通”的 AI 协作开发示例。
- User: 编程初学者，期望低门槛启动。
- Platform: 本地终端，Python 3。
- Constraints: 结构清晰、命令简单、必须可测试。
- Non-goals: 复杂 Web 框架与部署流程。

## Round 2
- Happy path: 通过 CLI 添加待办、查看列表、标记完成。
- Input/Output: 命令行参数输入，终端文本输出。
- Edge cases: 空标题、非法任务 ID、空列表状态。

## Round 3
- MVP acceptance: 支持 add/list/done 三个命令；持久化到 JSON 文件；有自动化测试。
- Mandatory tests: 单元测试覆盖核心仓储与命令行为。
- Extra: 提供一键运行示例命令。
