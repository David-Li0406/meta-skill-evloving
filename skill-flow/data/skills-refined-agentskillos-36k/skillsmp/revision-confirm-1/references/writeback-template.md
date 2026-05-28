# 回写模板（追加到 draft-plan.md）

> 说明：请把本节追加到 `Record/plan/draft-plan.md` 末尾。此文件用于 analysis-agent 与 plan-agent 之间的"通讯"。

## 硬性禁止

- **禁止修改 status 字段**
- **禁止写入"用户最终确认"章节**
- **禁止代替 plan-agent 执行任何确认操作**

```markdown
## analysis-agent确认意见

### 对plan-agent修订的分析

| 序号 | plan-agent修订项 | analysis-agent分析结论 | 说明 |
|------|-----------------|----------------------|------|
| 1 | ... | 认可/接受修正/有异议/需补充 | ... |
| 2 | ... | 认可/接受修正/有异议/需补充 | ... |

### 异议项（如有）

- **plan-agent修订**：...
- **analysis-agent异议理由**：...
- **建议处理方式**：...

### 需补充项（如有）

- **遗漏内容**：...
- **建议补充**：...

### 当前状态

- status: ready | need_revision
- 原因（中文）: ...
```

## 回写后的下一步（直接告知，不写入文件）

- **如果status=ready**：告知"请启动 plan-agent 执行 plan-finalize"
- **如果status=need_revision**：告知需要通知 plan-agent 再次修订，并说明原因
