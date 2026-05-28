# 步骤3：收集审核范围

## 获取已完成提案

从 `Record/state.json` 获取所有 `status: review` 的功能提案列表。

## 获取变更文件清单

对每个提案，读取 `Record/impl/{proposal_id}-impl.md`，汇总所有 `files_changed`。

## 读取 scope 配置

对每个提案，读取 `Record/plan/{proposal_id}-scope.md`，获取：
- `allowed_paths`
- `forbidden_patterns`
- 技术要求/代码规范
