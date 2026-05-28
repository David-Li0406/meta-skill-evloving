---
name: sa-isolation
description: 当开始撰写需要与当前工作区隔离的新章节，或在执行撰写计划之前使用——通过智能目录选择和安全验证创建隔离的草稿分支
---

# 使用草稿分支 (Using Draft Branches)

## 概述

草稿分支创建共享同一存储库的隔离工作区，允许同时处理多个章节的草稿而无需切换上下文。

**核心原则：** 系统化目录选择 + 安全验证 = 可靠的写作隔离。

**开始时声明：** “我正在使用 isolation 技能来设置隔离的写作工作区。”

## 目录选择流程

遵循此优先级顺序：

### 1. 检查现有目录

```bash
# 按优先级检查
ls -d .worktrees 2>/dev/null     # 首选 (隐藏)
ls -d worktrees 2>/dev/null      # 替代
```

**如果找到：** 使用该目录。如果两者都存在，`.worktrees` 优先。

### 2. 检查 CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**如果指定了偏好：** 直接使用，无需询问。

### 3. 询问研究者

如果不存在目录且无 CLAUDE.md 偏好：

```
未找到草稿目录。我应该在哪里创建草稿分支？

1. .worktrees/ (项目本地，隐藏)
2. ~/.config/superpowers/worktrees/<project-name>/ (全局位置)

你倾向于哪个？
```

## 安全验证

### 对于项目本地目录 (.worktrees 或 worktrees)

**必须在创建工作树之前验证目录是否被忽略：**

```bash
# 检查目录是否被忽略（遵守本地、全局和系统 gitignore）
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果未被忽略：**

根据“立即修复损坏的东西”规则：
1. 向 .gitignore 添加相应的行
2. 提交更改
3. 继续创建工作树

**为什么关键：** 防止意外将临时草稿目录提交到存储库。

### 对于全局目录 (~/.config/superpowers/worktrees)

不需要 .gitignore 验证——完全在项目之外。

## 创建步骤

### 1. 检测项目名称

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. 创建工作树

```bash
# 确定完整路径
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# 创建带有新分支的工作树
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. 运行项目设置

自动检测并运行适当的设置（针对学术写作环境，如 LaTeX 或 Markdown）：

```bash
# LaTeX 项目
if [ -f main.tex ]; then echo "LaTeX project detected"; fi

# Markdown/Pandoc 项目
if [ -f Makefile ]; then make setup; fi
```

### 4. 验证干净基线

运行验证脚本以确草稿从干净状态开始：

```bash
# 示例
make verify
# 或
./scripts/validate_structure.sh
```

**如果验证失败：** 报告失败，询问是否继续或调查。

**如果验证通过：** 报告准备就绪。

### 5. 报告位置

```
草稿工作区就绪于 <full-path>
基线检查通过
准备撰写 <chapter-name>
```

## 快速参考

| 情况 | 行动 |
|-----------|--------|
| `.worktrees/` 存在 | 使用它（验证已忽略） |
| `worktrees/` 存在 | 使用它（验证已忽略） |
| 两者都存在 | 使用 `.worktrees/` |
| 都不存在 | 检查 CLAUDE.md → 询问用户 |
| 目录未忽略 | 添加到 .gitignore + 提交 |
| 基线验证失败 | 报告失败 + 询问 |

## 常见错误

### 跳过忽略验证

- **问题：** 草稿目录被跟踪，污染 git 状态
- **修复：** 创建项目本地工作树前始终使用 `git check-ignore`

### 假设目录位置

- **问题：** 造成不一致，违反项目惯例
- **修复：** 遵循优先级：现有 > CLAUDE.md > 询问

### 在验证失败时继续

- **问题：** 无法区分新的逻辑漏洞和预先存在的问题
- **修复：** 报告失败，获得明确许可才能继续

## 示例工作流

```
你: 我正在使用 isolation 技能来设置隔离的写作工作区。

[检查 .worktrees/ - 存在]
[验证已忽略 - git check-ignore 确认 .worktrees/ 已忽略]
[创建工作树: git worktree add .worktrees/chapter2 -b draft/chapter2]
[运行基线检查 - 通过]

草稿工作区就绪于 /Users/researcher/thesis/.worktrees/chapter2
基线检查通过
准备撰写第二章
```

## 危险信号

**绝不：**
- 未验证是否被忽略就创建工作树（项目本地）
- 跳过基线验证
- 在验证失败时未经询问就继续
- 模棱两可时假设目录位置
- 跳过 CLAUDE.md 检查

**始终：**
- 遵循目录优先级
- 验证目录已忽略
- 验证干净的基线

## 集成

**调用者：**
- **ideation** (第 4 阶段) - 必需，当大纲获批且随后的撰写开始时
- 任何需要隔离写作空间的技能

**配对：**
- **finalization** - 必需，用于工作完成后的清理
- **execution** 或 **drafting** - 写作发生在工作树中
