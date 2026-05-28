# 步骤6：输出确定方案

## 执行

1. 追加记录到 `Record/record.md`：
   ```markdown
   ## YYYY-MM-DD HH:MM 方案确定
   方案版本：{plan_version}
   任务数：{提案数量}个提案
   子代理分工：{子代理列表}
   ```

2. 更新 `Record/Memory/plan-agent.md`：
   - 更新"关键决策"章节，记录本次确定的技术栈和架构决策
   - 格式：
     ```markdown
     | YYYY-MM-DD | {决策内容} | {决策原因} | plan-agent |
     ```
   - 示例：
     ```markdown
     | 2026-01-05 | 使用Rust实现核心模块 | 性能要求高，需要内存安全 | plan-agent |
     | 2026-01-05 | 采用模块化架构 | 便于子代理并行开发 | plan-agent |
     ```

3. 告知用户：
   - 方案已定稿，plan_version已冻结
   - 详细列出子代理分工（含运行槽位）
   - 下一步：进入循环B（openspec+提案→子代理执行→审核）
