# 步骤6：创建修复提案（审核不通过时）

## 修复提案命名规则

格式：`{原proposal_id}-fix-{N}`

示例：
- 原提案：`impl-module-a-python-agent`
- 第一次修复：`impl-module-a-python-agent-fix-1`

## 修复提案内容

必须包含：
- `parent_proposal`: 原提案ID
- `fix_round`: 修复轮次
- 审核问题列表（文件、行号、问题描述、严重程度）
- 修复任务清单
- 验收口径

## 更新 state.json

在 `proposals` 中添加修复提案记录。

## 子代理识别修复提案

子代理通过以下方式识别：
1. proposal_id 包含 `-fix-` 后缀
2. 有 `parent_proposal` 字段
3. 有"审核问题"章节
