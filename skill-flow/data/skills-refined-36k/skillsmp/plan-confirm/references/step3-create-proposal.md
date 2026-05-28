# 步骤3：创建提案

## 并发冲突规避（必须遵守）

**文件独占规则**：
- 每个提案的 `allowed_paths` 不能与其他并行提案重叠
- 如有重叠，必须声明 `depends_on`，强制串行执行

| 情况 | 处理方式 |
|------|---------|
| 无文件重叠 | 可并行执行 |
| 有文件重叠 | 必须串行，后者 `depends_on` 前者 |

## proposal_id 命名

格式：`{任务名称}-{子代理名}`
示例：`add-login-python-agent`

## 提案目录结构

```
openspec/changes/{proposal_id}/
├── proposal.md
├── tasks.md
├── design.md（可选）
└── specs/
```

## 更新 state.json

在 `proposals` 中添加每个提案记录。

**模板**：见 `proposal-template.md`、`build-proposal-template.md`
