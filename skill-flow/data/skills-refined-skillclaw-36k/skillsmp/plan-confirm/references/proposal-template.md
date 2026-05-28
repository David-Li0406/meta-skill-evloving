# Proposal 模板（OpenSpec 版）

子代理启动时没有上下文，必须通过提案文档完整理解任务。提案必须足够详细，确保子代理不跑题。

## 提案目录结构

```
openspec/changes/{proposal_id}/
├── proposal.md      # 提案内容（背景、目标、门禁、验收）
├── tasks.md         # 任务清单（子代理执行时更新 [ ] → [x]）
├── design.md        # 技术设计（可选）
└── specs/           # 规范 delta（如有变更）
```

---

## proposal.md 模板

```markdown
# Proposal: {proposal_id}

## 元信息

- **proposal_id**: {任务名称}-{子代理名}
- **plan_version**: {active_plan_version}
- **required_agent**: {子代理名}
- **depends_on**: []  # 依赖的提案列表，无依赖则为空
- **created_at**: {ISO8601}

## 项目背景

### 项目名称
{项目名称}

### 项目目标
{整体项目要实现什么，1-3句话}

### 当前阶段
{当前处于什么阶段，本提案在整体项目中的位置}

## 本提案任务

### 任务目标
{本提案具体要完成什么，详细描述}

### 功能需求
1. {需求1：详细描述}
2. {需求2：详细描述}
3. {需求3：详细描述}

### 技术要求
- 语言/框架：{如 Python 3.10+, FastAPI}
- 代码规范：{如 注释用中文，使用完整路径}
- 其他约束：{如 不使用某库，必须兼容某版本}

## 门禁配置

```json
{
  "allowed_paths": [
    "src/xxx/"
  ],
  "forbidden_patterns": [
    "*.secret",
    ".env*"
  ]
}
```

**注意**：`allowed_paths` 不能与其他并行提案重叠，如有重叠必须在 `depends_on` 中声明依赖。

## 相关文件（必读）

子代理启动后必须先阅读以下文件：

| 文件路径 | 说明 | 必读 |
|---------|------|------|
| Record/plan/{plan_version}-final.md | 确定方案 | 是 |
| src/xxx/existing.py | 需要参考的现有代码 | 是 |

## 接口约定

### 与其他模块的交互

| 交互对象 | 接口类型 | 说明 |
|---------|---------|------|
| {模块A} | 函数调用 | 调用 `module_a.func()` 获取数据 |

### 输入输出格式

输入：
```
{输入数据格式示例}
```

输出：
```
{输出数据格式示例}
```

## 验收口径

- [ ] {验收条件1：具体可验证}
- [ ] {验收条件2：具体可验证}
- [ ] {验收条件3：具体可验证}

## 风险与注意事项

- {风险1：描述及应对}
- {禁止事项：明确列出不能做什么}
```

---

## tasks.md 模板

```markdown
# Tasks: {proposal_id}

## 任务概述

{一句话描述任务目标}

## 任务清单

> 子代理执行时逐项完成并标记 [x]

## 1. {阶段1名称}
- [ ] 1.1 {任务描述}
- [ ] 1.2 {任务描述}

## 2. {阶段2名称}
- [ ] 2.1 {任务描述}
- [ ] 2.2 {任务描述}

## 3. {阶段3名称}
- [ ] 3.1 {任务描述}
- [ ] 3.2 {任务描述}

## 预期产出

| 文件路径 | 类型 | 说明 |
|---------|------|------|
| src/xxx/module.py | created | {说明} |
| src/xxx/utils.py | modified | {说明} |

## 执行记录

> 子代理执行时填写

- **开始时间**:
- **完成时间**:
- **产出文件**:
- **遇到问题**:
```

---

## 修复提案额外内容

如果是修复提案（proposal_id 包含 `-fix-`），proposal.md 需额外包含：

```markdown
## 修复背景

### 原提案
- proposal_id: {原proposal_id}
- 子代理: {原子代理}

### 审核问题

| 问题编号 | 文件 | 行号 | 问题描述 | 严重程度 |
|---------|------|------|---------|---------|
| 1 | {文件} | {行号} | {描述} | 高 |
| 2 | {文件} | {行号} | {描述} | 中 |
```

---

## 子代理启动检查清单

子代理启动后必须执行以下检查：

1. **身份确认**：确认自己是 proposal.md 中指定的子代理
2. **版本确认**：确认 `plan_version` 与 `Record/state.json` 的 `active_plan_version` 一致
3. **文件阅读**：阅读"相关文件（必读）"中标记为"是"的所有文件
4. **Scope 自检**：确认 allowed_paths/forbidden_patterns 与自身能力匹配
5. **任务理解**：用一句话复述任务目标，确保理解正确

如果任何检查不通过，立即停止并报错（中文说明原因）。

---

## 子代理完成任务后的 Git 提交

子代理完成所有任务后，必须执行本地提交：

### 提交前检查

```bash
git status
```

确认：
- 只包含本提案 scope 内的文件
- 没有敏感信息（密钥、密码等）
- tasks.md 已全部标记为 [x]

### 执行提交

```bash
git add {源代码文件}
git add openspec/changes/{proposal_id}/
git commit -m "feat: {一句话描述}"
```

### 提交规范

- **类型**：`feat`/`fix`/`refactor`
- **禁止**：AI 署名（Co-Authored-By、Signed-off-by）
- **禁止**：`git push`

### 提交后通知

```
提案 {proposal_id} 已完成并本地提交，请通知 plan-agent 审核。
```

### 追加项目记录

提交成功后，追加记录到 `Record/record.md`：

```markdown
## YYYY-MM-DD HH:MM 子代理完成
提案：{proposal_id}
子代理：{子代理名}
commit：{commit_hash}
提交信息：{commit_message}
```

获取 commit hash：
```bash
git log -1 --format="%H"
```

---

## OpenSpec 常用命令

```bash
# 查看活跃提案
openspec list

# 查看已有规范（创建提案前检查）
openspec list --specs

# 查看提案详情
openspec show {proposal_id}

# 验证提案格式（必须使用 --strict）
openspec validate {proposal_id} --strict

# 归档提案（项目完成时）
openspec archive {proposal_id} --yes

# 调试：查看提案的 delta 解析结果
openspec show {proposal_id} --json --deltas-only
```
