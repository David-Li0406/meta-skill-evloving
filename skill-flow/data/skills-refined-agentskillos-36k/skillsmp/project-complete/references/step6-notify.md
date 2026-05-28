# 步骤6：通知用户

## 执行

1. 更新 `Record/Memory/plan-agent.md`：
   - 追加"会话记录摘要"章节：
     ```markdown
     ### YYYY-MM-DD HH:MM 项目完成
     - 做了什么：
       - {功能1}
       - {功能2}
     - 结论：项目已完成
     - 下一步：无
     ```
   - 更新"待处理事项"章节，标记已完成的任务

2. 追加记录到 `Record/record.md`：
   ```markdown
   ## YYYY-MM-DD HH:MM 项目完成
   版本：{plan_version}
   提交：{commit SHA}
   归档提案数：{N}
   ```

## 输出格式

```
项目已完成！

版本：{plan_version}
提交：{commit SHA}

变更摘要：
- {功能1}
- {功能2}

归档提案数：{N}
变更文件数：{N}

OpenSpec 规范已更新：openspec/specs/

已推送到远程仓库。
```
