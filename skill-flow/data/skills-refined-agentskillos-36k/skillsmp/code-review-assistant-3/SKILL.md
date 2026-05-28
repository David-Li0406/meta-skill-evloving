---
name: code-review-assistant
description: 代码审核辅助工具，支持本地 Git 库和 Gerrit Review。支持审核当前最新 commit、暂存的修改、未暂存的修改等，也支持 Golang、Qt/C++、Ansible 等多语言的 Gerrit Code Review。提供"必须修复/建议修复/可选改进"三级分级审核，生成 Markdown 报告。
category: review
tags:
  - code-review
  - gerrit
  - git
  - golang
  - cpp
  - qt
  - ansible
---

# Code Review Assistant

## Overview

提供结构化的代码审核工作流程，支持两种审核模式：

### 本地 Git 模式
- 审核当前最新 commit
- 审核暂存的修改 (`git add` 的文件)
- 审核未暂存的修改（工作区变更）
- 审核指定 commit 的 diff

### Gerrit Review 模式
- 通过 Gerrit Change ID 进行代码审核
- 自动获取 Change 详情和文件变更
- 支持自动发布评审到 Gerrit

**支持的语言**：
- Golang（完整支持）
- Qt/C++（完整支持）
- Ansible（完整支持）

## Review 评分规则

| 问题类型 | 建议 Score | 说明 |
|---------|-----------|------|
| 无问题 | **+1** | 代码质量优秀 |
| 仅有 Nice to Have | **-1** | 有改进空间但不影响功能 |
| 有 Should Fix | **-2** | 应该修复的问题 |
| 有 Must Fix | **-2** | 必须修复的严重问题 |

## 使用方式

### 本地 Git 审核用例

```
/code-review-assistant HEAD          # 审核最新 commit
/code-review-assistant --staged       # 审核暂存的修改
/code-review-assistant --unstaged     # 审核未暂存的修改
/code-review-assistant HEAD~1        # 审核上一个 commit
/code-review-assistant abc1234       # 审核指定 commit hash
```

### Gerrit Review 用例

```
/code-review-assistant <change_id>   # 审核 Gerrit Change
```

### 自动发布评论（仅 Gerrit 模式）

如果用户提示词中包含明确的发布请求（如"发布评论"、"提交评审"、"post review"、"发布到 Gerrit"等关键词），skill 会自动使用 Gerrit MCP 工具发布带评分的评论。

## 审核范围规范

### 支持的本地 Git 审核范围

| 用例 | Git 命令 | 说明 |
|------|----------|------|
| 最新 commit | `HEAD` | 审核最新的提交记录 |
| 上一个 commit | `HEAD~1` 或 `HEAD^` | 审核倒数第二次提交 |
| 指定 commit | `<commit_hash>` | 审核指定的某次提交 |
| 暂存的修改 | `--staged` 或 `--cached` | 审核已 `git add` 但未提交的变更 |
| 未暂存的修改 | `--unstaged` 或 `--working` | 审核工作区的变更 |
| 两次 commit 之间 | `<commit_a>...<commit_b>` | 审核两个 commit 之间的差异 |

### 不支持的审核范围

以下范围**不支持**，需要提醒用户提供更准确的范围：

- 多个 commit：如 `最近的5次提交`、`最近10次commit`、`所有提交`
- 指定范围的多次提交：如 `HEAD~5..HEAD` (除非用户明确表示可以接受)
- 整个仓库历史：如 `整个分支`、`所有变更`
- 大量的连续 commits

### 范围验证流程

当用户给出审核范围时：

1. **识别审核模式**：是本地 Git 还是 Gerrit Change ID
2. **验证范围有效性**：
   - 本地 Git：检查是否为 commit hash、`HEAD`、`--staged`、`--unstaged` 等
   - Gerrit：检查是否为有效的 Change ID 格式
3. **检查范围大小**：
   - 如果检测到多个 commit（如 `HEAD~10`），提醒用户建议审核单个 commit 或差异范围
   - 如果范围过大，提示用户缩小范围
4. **执行审核**：验证通过后开始审核流程

**范围不合理的提示模板**：
```
检测到您要求审核范围较大：{用户输入的范围}

建议使用以下更精确的范围：
- HEAD                    # 审核最新一次 commit
- HEAD~1                  # 审核上一次 commit
- --staged                # 审核暂存的修改
- --unstaged              # 审核未暂存的修改
- abc1234                 # 审核指定 commit hash

请选择一个合适的范围，或者明确输入具体的 commit hash。
```

## 完整工作流程

### 阶段 1: 模式识别与获取变更

1. **识别审核模式**：
   - 如果输入是有效的 Git commit hash 或 `HEAD`、`~` 相关表达式 → 本地 Git 模式
   - 如果输入包含 `--staged`、`--unstaged`、`--cached`、`--working` → 本地 Git 模式
   - 如果输入是 Gerrit Change ID 格式 → Gerrit 模式
   - 如果范围不合理，提示用户提供更精确的范围

2. **获取变更信息**：
   - **本地 Git 模式**：使用 `git` 命令获取
     - `git show --stat <ref>` - 获取 commit 信息和变更文件列表
     - `git show <ref> -- <file>` 或 `git diff <ref~1> <ref> -- <file>` - 获取文件差异
     - `git diff --cached` - 暂存区差异
     - `git diff` - 工作区差异
   - **Gerrit 模式**：使用 Gerrit MCP 工具获取
     - `get_change_details` - 获取变更详情
     - `list_change_files` - 获取修改的文件列表
     - `get_commit_message` - 获取提交信息

### 阶段 2: 代码获取与解析（含自我审阅触发判断）

**重要说明**：本地 Git 模式会在阶段 4.5 执行自我审阅，通过读取源文件上下文验证发现的问题是否准确。

对每个修改的文件：
1. 获取文件的差异内容（diff）
2. 识别文件类型（.go、.cpp、.hpp、.yml、.yaml 等）
3. 应用排除规则（vendor、generated 等目录）
4. 将文件分发给对应语言的分析器

### 阶段 3: 语言专项检查

#### Golang 分析器

检查规则详见 [references/golang-checks.md](references/golang-checks.md)。

**排除规则**：
- `vendor/` 目录及其所有文件不进行审核
- 不提示关于 vendor 目录存储方式的改进建议

**按严重程度分类**：
- 🔴 **Must Fix** (-2): 错误处理缺失、SQL 注入、竞态条件、资源泄漏、空指针解引用
- 🟡 **Should Fix** (-2): 命名规范、函数过长、魔法数字、缺少注释、过度嵌套
- 🔵 **Nice to Have** (-1): 可用 stdlib、未使用变量/导入、可简化拼接

#### Qt/C++ 分析器

检查规则详见 [references/cpp-checks.md](references/cpp-checks.md)

**排除规则**：
- `vendor/`、`third_party/`、`3rdparty/` 目录
- 自动生成的文件（`moc_*.cpp`、`ui_*.h`、`qrc_*.cpp`）

#### Ansible 分析器

检查规则详见 [references/ansible-checks.md](references/ansible-checks.md)

**排除规则**：
- `galaxy_roles/`、`collections/`、`vendor/` 第三方目录
- 主机清单文件（`inventory/`、`hosts`）的敏感内容

### 阶段 4: 问题聚合与分级

1. 将各语言检查结果汇总
2. 按严重程度分类（Must Fix / Should Fix / Nice to Have）
3. 去重和优先级排序
4. 计算 Review 评分：
   - 有 Must Fix 或 Should Fix → `-2`
   - 仅有 Nice to Have → `-1`
   - 无问题 → `+1`

### 阶段 4.5: 自我审阅（仅本地 Git 模式）

**目的**：减少误判，确保审核发现的每个问题都是真实存在且准确的。

**触发条件**：仅在**本地 Git 模式**下执行。

**执行步骤**：

1. **检查是否处于项目源码目录**：
   - 判断当前目录是否包含项目结构（如 `go.mod`、`CMakeLists.txt`、`main.yml` 等）
   - 如果不是项目目录，跳过自我审阅阶段

2. **对每个发现的问题进行上下文验证**：
   - 使用 `Read` 工具读取问题所在文件的完整代码
   - 根据问题报告的文件路径和行号，定位到具体代码位置
   - 结合 git diff 的变更上下文，重新分析问题是否确实存在

3. **审阅重点**：

   | 问题类型 | 审阅策略 |
   |---------|---------|
   | Must Fix | 严格验证 - 必须确认问题真实存在，否则移除或降级 |
   | Should Fix | 适度验证 - 结合完整代码确认问题合理性 |
   | Nice to Have | 轻量验证 - 确认建议确实可改进 |

4. **审阅操作**：

   - **确认问题真实**：保留原问题，标记"✓ 已验证"
   - **问题不存在**：从问题列表中移除，记录"✗ 误判 - 原因"
   - **需要降级**：调整问题等级（如 Must Fix → Should Fix），添加说明
   - **需要调整描述**：优化问题描述，使其更准确

5. **更新统计**：
   - 根据审阅后的最终问题列表重新计算各等级数量
   - 相应调整最终的 Review 推荐分数

**自我审阅模板记录**：
```
[自我审阅]
- 审阅文件数：N 个
- 原发现问题数：M 个
- 移除误判：A 个
- 降级调整：B 个
- 最终确认：M-A 个
```

**重要原则**：
- 只在能读取到项目源码时执行自我审阅
- 审阅是为了减少误判，不是为了减少问题
- 对于不确定的问题，倾向于保留而不是移除
- 自我审阅的结果应当体现专业性，提高审核可信度

### 阶段 5: 生成输出

生成 Markdown 审核报告，格式见下方"输出格式"章节。

**注**：最终报告中的问题数量和评分应为阶段 4.5 自我审阅后的结果。

### 阶段 6: 条件性发布评审（仅 Gerrit 模式）

**检测用户意图**：检查用户提示词是否包含以下关键词之一：
- "发布评论"
- "提交评审"
- "post review"
- "发布到 Gerrit"
- "submit review"

**如明确要求，使用 Gerrit MCP 工具发布**：

**发布方式**：一次性发布完整评论，包含 Code Review Summary 和逐条问题说明。

使用 `post_review_comment` 工具发布**一条评论**（不设置 `file_path` 和 `line_number`，仅设置 `message` 作为 Change 级别评论），**必须**在 `labels` 参数中设置 `Code-Review` 分数：

| 参数 | 值 | 说明 |
|------|-----|------|
| `change_id` | Change ID | Gerrit Change 的标识符 |
| `message` | 评论内容 | 完整的评论文本，格式见下方 |
| `labels.Code-Review` | `-2` / `-1` / `+1` | 根据审核结果计算的评分 |

**重要提醒**：
- **只发布一次评论**，不针对每个问题单独发布行级评论
- 使用 Change 级别评论（不设置 `file_path` 和 `line_number`）
- 每次调用 `post_review_comment` 时，**必须**设置 `labels.Code-Review`
- 分数根据汇总 Summary 计算
- Verified 字段不设置，由 Gerrit 默认处理

## 输出格式

### 审核输出说明

审核工作完成后生成两种输出：

1. **Markdown 审核报告**（始终生成）：在本地终端完整展示，适用于本地代码审核
2. **Gerrit Review 评论**（可选，仅在 Gerrit 模式且用户明确要求时发布）：发布到 Gerrit Change

### Markdown 审核报告（本地输出）

适用于本地 Git 模式或 Gerrit 模式，作为完整的技术审核报告。

```markdown
# Code Review Report

## Metadata
- **Review Type**: Local Git / Gerrit
- **Commit/Change**: xxx
- **Author**: xxx
- **Subject**: xxx
- **Files Changed**: xx (xx insertions, xx deletions)

---

## Summary
总问题数: N (Must Fix: A, Should Fix: B, Nice to Have: C)

**推荐 Score**: -2 / +1

[可选] **正面评价**:
• 添加了完整的测试用例
• 使用接口抽象依赖

---

## 📌 Must Fix (-2) - A items

### [app/api/service/eia.go:239] 日志中使用未定义的变量

**问题描述**:
`departmentIDs` 在内部作用域定义但最后被引用，会导致编译错误。

**代码片段**:
```go
if len(departmentIDs) > 0 {
    // ... departmentIDs 在此作用域
}
// 最后的 log 引用了 departmentIDs - 错误!
log.Info("...", log.Any("departmentIDs", departmentIDs))
```

**Suggestion**: 修复日志语句，移除或使用正确的变量。

---

## 📌 Should Fix (-2) - B items

### [pkg/middleware/auth.go:45] 命名不符合规范

**问题描述**:
函数名使用匈牙利命名法，不符合 Go 命名约定。

**Suggestion**: 改用驼峰命名，如 `getAuthToken` → `GetAuthToken`。

---

## 📌 Nice to Have (-1) - C items

### [main.go:120] 可使用标准库功能

**问题描述**:
自定义的字符串分割函数可被 `strings.Split` 替代。

**Suggestion**: 直接使用 `strings.Split`。

---

## ✅ 无问题
代码质量优秀，以上仅列出改进建议。
```

### Gerrit Review 评论格式（发布到 Gerrit）

仅在 Gerrit 模式下，当用户明确要求（如"发布评论"、"post review"等）时，将审核结果发布为 Change 级别评论。

**设计原则**：简明扼要，重点突出，便于在 Gerrit Web 界面快速阅读。

```
=== Code Review Summary ===

Found Issues:
🔴 Must Fix: 3 items
🟡 Should Fix: 1 items
🔵 Nice to Have: 2 items
Recommended Score: -2 (需修复严重问题后合并)

Positive Points:
• 添加了完整的测试用例覆盖新增功能
• 使用接口抽象依赖，便于测试和维护
• 密码修改流程有完整的降级机制
• 日志记录详尽，便于排查问题

---

### Must Fix Issues

1. [app/api/service/eia.go:239] 日志中使用未定义变量 `departmentIDs`
   Suggestion: 修复日志语句，移除或使用正确的变量。

2. [app/api/service/uim_client.go:57] 全局变量缺少并发安全保护
   ```go
   var globalEIAAuthChecker EIAAuthChecker = NewEIAAuthChecker()
   ```
   Suggestion: 使用 `sync.RWMutex` 保护访问，或使用 `atomic.Value`。

3. [app/web/handler/user.go:1227] 用户ID检查逻辑不正确
   Suggestion: 修复 ID 验证逻辑，添加边界检查。

---

### Should Fix Issues

1. [pkg/middleware/auth.go:45] 函数命名不符合 Go 规范
   Suggestion: 使用驼峰命名 `getAuthToken` → `GetAuthToken`。

---

### Nice to Have Issues

1. [main.go:120] 可使用标准库 `strings.Split` 替代自定义实现

2. [utils/string.go:78] 删除未使用的辅助函数
```

**格式规范**：

| 部分 | 说明 | 格式 |
|------|------|------|
| 标题 | `=== Code Review Summary ===` | 标题分隔符 |
| Found Issues | 统计各等级问题数量 | emoji + items |
| Recommended Score | 建议分数 | 文字说明 |
| Positive Points | 正面评价 | 项目符号 `•` |
| 各等级问题 | 按 Must Fix / Should Fix / Nice to Have 分组 | `###` 分组标题 |
| 具体问题 | 编号 + 文件:行号 + 描述 | 数字编号 |
| 代码示例 | 仅必要时展示 | 代码块 |
| Suggestion | 修改建议 | 加粗文本 |

**与 Markdown 报告的区别**：

| 特性 | Markdown 报告 | Gerrit 评论 |
|------|-------------|------------|
| 目标 | 本地完整技术审核 | Gerrit Web 快速阅读 |
| 详细程度 | 详细，包含代码片段、完整描述 | 简明，重点突出 |
| 组织方式 | 按问题分类，每个问题独立分块 | 先分组，问题列表形式 |
| Positive Points | 独立章节 | 用项目符号简洁列出 |
| 文件定位 | 每个问题开头 | 集中列举序号 |
| 代码块 | 每个问题都可能有 | 仅必要时展示 |

## 检查规则参考

- [references/golang-checks.md](references/golang-checks.md) - Golang 检查规则
- [references/cpp-checks.md](references/cpp-checks.md) - Qt/C++ 检查规则
- [references/ansible-checks.md](references/ansible-checks.md) - Ansible 检查规则

### Golang 检查项索引

#### 🔴 Must Fix (-2)

| ID | 问题描述 | 检测方式 |
|----|---------|---------|
| GO-MF001 | 错误处理缺失 | 检测未处理的返回值 `err` |
| GO-MF002 | SQL 注入风险 | 检测字符串拼接构建 SQL |
| GO-MF003 | 竞态条件 | 检测未保护的共享变量访问 |
| GO-MF004 | 资源泄漏 | 检测未关闭的 `defer` 缺失 |
| GO-MF005 | 空指针解引用 | 检测未检查 nil 的指针操作 |

#### 🟡 Should Fix (-2)

| ID | 问题描述 | 检测方式 |
|----|---------|---------|
| GO-SF001 | 命名不符合规范 | 检测非规范命名（包/变量/函数） |
| GO-SF002 | 函数过长 | 统计函数行数 > 100 |
| GO-SF003 | 魔法数字 | 检测数字字面量（非 0/1） |
| GO-SF004 | 缺少注释的复杂逻辑 | 检测复杂判断/循环无注释 |
| GO-SF005 | 过度嵌套 | 检测嵌套层级 > 3 |

#### 🔵 Nice to Have (-1)

| ID | 问题描述 | 检测方式 |
|----|---------|---------|
| GO-NH001 | 可使用 stdlib | 检测自实现有 stdlib 等效功能的函数 |
| GO-NH002 | 变量未使用 | 检测声明但未使用的变量 |
| GO-NH003 | 导入未使用 | 检测未使用的 import |
| GO-NH004 | 可简化的字符串拼接 | 检测可用 `+` 简化的 `fmt.Sprintf` |

### Qt/C++ 检查项索引

#### 🔴 Must Fix (-2)

| ID | 问题描述 |
|----|---------|
| CPP-MF001 | 内存泄漏 |
| CPP-MF002 | 使用未初始化的变量 |
| CPP-MF003 | 数组越界访问 |
| CPP-MF004 | 空指针解引用 |
| CPP-MF005 | 竞态条件 - 线程安全问题 |
| CPP-MF006 | SQL 注入风险 |
| CPP-MF007 | 信号槽参数不匹配 |
| CPP-MF008 | QObject 对象销毁后使用 |

#### 🟡 Should Fix (-2)

| ID | 问题描述 |
|----|---------|
| CPP-SF001 | 命名不符合规范 |
| CPP-SF002 | 函数过长 |
| CPP-SF003 | 魔法数字 |
| CPP-SF004 | 缺少注释的复杂逻辑 |
| CPP-SF005 | 过度嵌套 |
| CPP-SF006 | 不必要的父类成员函数遮蔽 |
| CPP-SF007 | QString::number 不必要转换 |
| CPP-SF008 | 硬编码的文件路径 |
| CPP-SF009 | 未检查操作结果 |

#### 🔵 Nice to Have (-1)

| ID | 问题描述 |
|----|---------|
| CPP-NH001 | 可使用现有 Qt 工具类 |
| CPP-NH002 | 未使用的变量或函数 |
| CPP-NH003 | 冗余的 const |
| CPP-NH004 | 可以使用 auto 简化类型声明 |
| CPP-NH005 | 可以使用 lambda 替代函数对象 |
| CPP-NH006 | QString 重复使用 toUtf8().constData() |

### Ansible 检查项索引

#### 🔴 Must Fix (-2)

| ID | 问题描述 |
|----|---------|
| ANS-MF001 | 明文存储敏感信息 |
| ANS-MF002 | Shell 模块未使用幂等性检查 |
| ANS-MF003 | 使用 sudo/su 而非 become |
| ANS-MF004 | 未处理任务失败 |
| ANS-MF005 | 循环性能问题 |
| ANS-MF006 | 未检查目标系统支持 |
| ANS-MF007 | 配置文件修改未备份 |

#### 🟡 Should Fix (-2)

| ID | 问题描述 |
|----|---------|
| ANS-SF001 | 使用弃用的语法或模块 |
| ANS-SF002 | 缺少元数据 |
| ANS-SF003 | 魔法变量值 |
| ANS-SF004 | 未使用标签 (Tags) |
| ANS-SF005 | 循环或条件变量命名混淆 |
| ANS-SF006 | 未声明依赖关系 |
| ANS-SF007 | 未使用 Jinja2 过滤器 |
| ANS-SF008 | 注释不够或缺失 |
| ANS-SF009 | 未使用 Handler 实现幂等性 |

#### 🔵 Nice to Have (-1)

| ID | 问题描述 |
|----|---------|
| ANS-NH001 | 未使用的变量 |
| ANS-NH002 | 可以使用内置模块代替 shell |
| ANS-NH003 | 重复的代码可以提取 |
| ANS-NH004 | 可以合并相似任务 |
| ANS-NH005 | YAML 过于冗长 |
| ANS-NH006 | 未使用社区集合 (Collections) |
| ANS-NH007 | 可以使用内置 Facts 而非 shell 命令 |
| ANS-NH008 | 变量定义分散 |

## 扩展指南

### 添加新的检查规则

在对应语言的 `references` 文件中添加检查项，格式：
```markdown
### [检查ID] 检查名称

- **描述**: 检查项的详细描述
- **严重程度**: Must Fix / Should Fix / Nice to Have
- **检测方式**: 如何通过代码分析发现此问题
- **示例**:
  ```go
  // Bad
  // ...
  // Good
  // ...
  ```
- **建议修改**: 具体的修改建议
```

### 添加新语言支持

1. 创建 `references/<lang>-checks.md` 文件
2. 按三级分类组织检查项
3. 更新本文档"阶段 3: 语言专项检查"部分
4. 在"检查规则参考"章节添加该语言的检查项索引
