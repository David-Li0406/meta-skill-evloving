# 步骤2：归档提案执行记录

## 归档位置

`Record/impl/` 目录下的所有 `{proposal_id}-impl.md`

## 归档检查

对每个提案：
1. 确认 `Record/impl/{proposal_id}-impl.md` 存在
2. 确认任务清单全部完成（所有 `[ ]` 都变成 `[x]`）
3. 确认 `files_changed` 列表完整

## 生成归档摘要

创建 `Record/impl/{plan_version}-archive.md`：
- 列出所有已完成提案
- 汇总所有变更文件
- 记录归档时间
