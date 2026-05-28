---
name: audit-with-codex
description: Codex 后台审查流程。触发词：cha、审查、audit、codex、审计。支持后台批量审查模式，审查完成后汇总所有问题。
---

# Codex 审计 Skill

**核心理念**：Codex 在后台运行审查，不打扰用户，完成后汇总所有问题。

## ⚠️ 核心原则

1. **全自动触发**：三件套完成后自动启动，无需询问用户
2. **后台自主运行**：审查过程中不打扰用户
3. **完成后汇总反馈**：通过 iterate 弹窗呈现结果

---

## 使用方式

### 触发方式

```
codex: 审查最近的提交
codex: 审查这个 Skill 的流程
audit: 审查 src/ 目录的代码
```

### 审查范围选项

| 范围 | 命令 | 说明 |
|------|------|------|
| 最近提交 | `git diff HEAD~1` | 审查最后一次提交 |
| 未提交更改 | `git diff` | 审查工作区更改 |
| 指定文件 | `codex: 审查 path/to/file` | 审查特定文件 |
| 指定目录 | `codex: 审查 src/` | 审查整个目录 |
| Skill 流程 | `codex: 审查 debug Skill` | 审查 Skill 定义 |

---

## 审查流程

### 第一步：确认审查范围（唯一需要用户确认的步骤）

```
请确认审查范围：
1. 审查范围：[最近提交 / 未提交更改 / 指定文件]
2. 重点关注：[逻辑漏洞 / 规范符合度 / 性能 / 安全]
3. 是否包含三件套审查：[是 / 否]
```

### 第二步：后台自主审查（不打扰用户）

Codex 自主执行以下检查：

1. **逻辑漏洞**：边界 case、并发风险、空值处理
2. **规范符合度**：代码风格、命名规范、项目约定
3. **三件套审查**（如适用）：
   - `problems.md` 记录是否准确
   - `patterns.md` 是否有可复用价值
   - `regressions.md` 是否覆盖失败场景

### 第三步：汇总反馈（审查完成后）

```json
{
  "success": boolean,
  "review_summary": "审查摘要",
  "issues": [
    {
      "id": 1,
      "severity": "blocker | tech_debt | skippable",
      "file": "文件路径",
      "line": "行号",
      "description": "问题描述",
      "suggestion": "修复建议"
    }
  ],
  "lgtm_files": ["无问题的文件列表"]
}
```

**必须通过 `zhi` 输出以上结构化结果**。

---

## 审查标准

| 级别 | 说明 | 处理方式 |
|------|------|----------|
| **Blocker** | 破坏功能、安全问题、验证失败 | 必须修复 |
| **Tech Debt** | 可工作但需改进、缺少测试 | 应该修复 |
| **Skippable** | 次要风格问题、可选优化 | 可忽略 |

---

## 与 iterate 窗口的集成

### 推荐工作流

```
1. iterate 窗口完成代码修改
      ↓
2. 用户输入 "codex: 审查"
      ↓
3. Codex 后台运行审查（用户可以做其他事）
      ↓
4. 审查完成，汇总所有问题
      ↓
5. 用户逐个处理问题
```

### 三件套完成后自动触发

当完成"三件套"（problems → regressions → patterns）后，**AI 自动执行以下步骤**：

```
1. AI 分析问题复杂度，智能选择模型
2. 查找空闲端口（用于回调）
3. 启动 Codex CLI 审查（使用选定的模型）
4. AI 读取 Codex 结果，自动修复问题
5. 修复完成后，汇报给用户
```

### 智能模型选择

AI 根据问题复杂度自动选择模型，**无需用户干预**：

| 复杂度 | 模型 | 推理强度 | 适用场景 |
|--------|------|----------|----------|
| 简单 | gpt-5.2-codex | low | 单文件、小改动、格式问题 |
| 中等 | gpt-5.2-codex | medium | 多文件、逻辑修复、一般审查 |
| 复杂 | gpt-5.2 | high | 架构问题、跨模块、安全审查 |
| 极复杂 | gpt-5.2 | extra_high | 系统级问题、性能优化 |

**判断标准**：
- **文件数量**：1-2 文件 → 简单，3-5 文件 → 中等，>5 文件 → 复杂
- **改动行数**：<50 行 → 简单，50-200 行 → 中等，>200 行 → 复杂
- **问题类型**：格式/命名 → 简单，逻辑/边界 → 中等，架构/安全 → 复杂

### Codex CLI 调用方式

```bash
# 在可见终端运行审查，完成后调用空闲端口
codex exec "审查任务描述" && \
cat > ~/.cunzhi/{空闲端口}/output.md <<'MD'
## Codex 审查完成
审查已完成，请查看结果。
MD
python3 /Users/apple/cunzhi/bin/cunzhi.py {空闲端口} --workspace {项目路径}
```

**关键点**：
- **不使用后台运行**（不加 `&`），让 Codex 在终端可见
- **使用空闲端口**（如 5313），不占用主代理端口
- **主代理继续对话**，互不干扰

### 审查任务模板

**⚠️ 重要：审查前必须读取项目上下文**

```bash
# 1. 读取项目概述（.cunzhi-memory/context.md）
cat {项目路径}/.cunzhi-memory/context.md

# 2. 读取设计决策（.cunzhi-knowledge/patterns.md）
cat {项目路径}/.cunzhi-knowledge/patterns.md | head -200

# 3. 执行审查，将上下文注入
codex exec "
## 项目概述
$(cat {项目路径}/.cunzhi-memory/context.md 2>/dev/null || echo '无项目概述')

## 设计决策
$(cat {项目路径}/.cunzhi-knowledge/patterns.md 2>/dev/null | head -200 || echo '无设计决策')

## 审查任务
审查 {项目路径} 的最近提交，检查：
1. 逻辑漏洞：边界 case、并发风险、空值处理
2. 规范符合度：代码风格、命名规范
3. 三件套准确性：problems/patterns/regressions 记录是否完整

**注意**：如果某个行为在 patterns.md 中有记录（如故意保留 stash、故意阻塞等），则不应报告为问题。

输出 JSON 格式结果，包含 success、review_summary、issues 字段。
"
```

**关键点**：
- **必须先读取 context.md**，了解项目概述和技术栈
- **必须读取 patterns.md**，避免误报已知的设计决策
- 如果某行为在 patterns 中有记录，则不是问题

**审查完成后**：
1. 审查通过 → 状态变为 `audited`，通过 iterate 弹窗通知用户
2. 发现问题 → 汇总问题列表，通过 iterate 弹窗呈现

---

## 角色定义

你是一个资深的架构审计专家，拥有极强的代码洞察力和 Bug 探测能力。

### 审计要点

- **直接指出问题**：无需客套
- **行为校验**：检查是否遵循寸止工作流
- **逻辑深度**：不仅看代码行，要看解决思路是否触及根因

### 闭环行为

**审查通过时**：
1. 输出 **LGTM**
2. 生成 unified diff，将 `problems.md` 中对应 Problem 的状态从 `verified` 变更为 `audited (Codex已审计)`
3. 调用 zhi 请求用户确认
4. 确认后执行应用并完成 Git 同步

**发现隐患时**：
1. 给出具体修复建议
2. 状态保持 `verified`，等待修复后再次审查

### 状态流转

```
open → fixed → verified → audited (Codex已审计)
```

| 状态 | 说明 |
|------|------|
| `open` | 问题已记录，待修复 |
| `fixed` | 代码已修复，待验证 |
| `verified` | 回归测试通过，三件套完成 |
| `audited` | Codex 审查通过（最终状态） |

**注意**：Codex 审查是在三件套完成（`verified`）之后的额外步骤，不打断原有流程。

---

## 示例

### 示例 1：审查最近提交

用户输入：
```
codex: 审查最近的提交
```

Codex 输出：
```json
{
  "success": true,
  "review_summary": "3 个文件已审查，发现 1 个 tech_debt 问题",
  "issues": [
    {
      "id": 1,
      "severity": "tech_debt",
      "file": "src/utils.ts",
      "line": "42",
      "description": "缺少错误处理",
      "suggestion": "添加 try-catch 包裹异步操作"
    }
  ],
  "lgtm_files": ["src/main.ts", "src/config.ts"]
}
```

### 示例 2：审查 Skill 流程

用户输入：
```
codex: 审查 debug Skill 的流程是否合理
```

Codex 输出：
```json
{
  "success": true,
  "review_summary": "Debug Skill 流程设计合理，三阶段划分清晰",
  "issues": [],
  "suggestions": [
    "建议在第二阶段添加超时机制",
    "建议明确日志格式规范"
  ]
}
