---
name: doc-smith-create
description: "Generate and update comprehensive documentation from workspace data sources, including code repositories, text files, and media assets. Use this skill when the user requests to: (1) create or generate documentation from code or files, (2) build document structure or details, (3) update, modify, or improve existing documentation, (4) rewrite specific sections or paragraphs, (5) process changeset files or PATCH-marked modification requests. Supports technical documentation, user guides, API references, and general documentation needs."
---

# DocSmith

从工作区数据源生成和更新结构化文档。

## 概述

DocSmith 分析数据源内容（代码、文件、媒体）并生成：
1. 用户意图描述（`user-intent.md`）
2. 文档结构计划（`document-structure.yaml`）
3. 按层次组织的 Markdown 文档文件

所有输出都创建在独立的 `.aigne/doc-smith` 目录中。

**任务规划机制**：DocSmith 使用持久化的任务规划文件来跟踪执行进度，确保长时间任务的可追溯性和可恢复性。

## 使用场景

### 场景 A：生成新文档

当 `.aigne/doc-smith/docs/` 目录不存在或用户明确要求重新生成时，使用 **文档生成流程**（步骤 1-6）。

**适用情况：**
- 首次为项目生成文档
- 完全重建文档结构
- 用户说"重新生成所有文档"

### 场景 B：更新已有文档

当 `.aigne/doc-smith/docs/` 目录已存在且用户要求修改时，使用 **文档更新流程**（步骤 7）。

**适用情况：**
- 用户提出自然语言修改请求（如"统一术语"、"补充章节"、"修正错误"）
- 用户提供 changeset 文件路径
- 文档中存在 `::: PATCH` 标记
- 用户说"更新文档"、"修改文档"、"应用修改"
- 用户希望更新文档中的图片，比希望在某篇文档中新增图片、删除图片或编辑某张图片

## 工作流程

按以下步骤依次执行：

### 任务规划初始化

**在开始任何实际工作前，必须先初始化任务规划文件。**

在 `.aigne/doc-smith/cache`目录创建 `.aigne/doc-smithtask_plan.md` 文件，如果文件已存在，可以覆盖之前的文件，内容模板：

```markdown
# DocSmith Task Plan

## Goal
[One sentence describing the final goal of this task, e.g., Generate complete Chinese technical documentation for XXX project]

## Execution Phases (Identify whether generating new or updating docs, refer to the appropriate template)

New Document Generation Template:
- [ ] Phase 0: Workspace check, read reference files, ensure config.yaml and sources data are complete
- [ ] Phase 1: Analyze data sources
- [ ] Phase 2: Infer user intent and confirm with user
- [ ] Phase 3: Plan document structure
- [ ] Phase 4: Generate document-structure.yaml
- [ ] Phase 5: Confirm document structure
- [ ] Phase 6: Generate document content
- [ ] Phase 7: Check for `AFS Image Slot`, if exists call `generate-slot-image` SubAgent to generate images
- [ ] Phase 7.5: Verify image slots have been replaced
- [ ] Phase 9: Confirm all tasks are completed before finishing
- [ ] Phase 10: (Additional user requirements, extend this list as needed)


Document Update Template:
- [ ] Phase 0: Workspace check, read reference files, ensure config.yaml and sources data are complete
- [ ] Phase 1: Analyze update requirements (identify changeset files, PATCH markers, or natural language requests)
- [ ] Phase 2: Check if document structure needs modification, if so update document-structure.yaml and validate
- [ ] Phase 3: Apply document content updates
- [ ] Phase 4: Process PATCH markers in documents
- [ ] Phase 5: Whenever documents are added or updated, check for new `AFS Image Slot`, if exists call `generate-slot-image` to generate images
- [ ] Phase 5.5: Verify image slots have been replaced
- [ ] Phase 6: Execute document structure and content validation
- [ ] Phase 7: Confirm all update tasks are completed
- [ ] Phase 8: (Additional user requirements, extend this list as needed)

## Key Decisions
[Record important decisions made during execution and their rationale]

## Errors Encountered
[Record errors encountered and solutions, format: Error description -> Solution]

## Current Status
**Executing Phase 0** - Preparing to initialize workspace
```

**规划文件使用规则**：
1. **每个阶段开始前**：读取 `.aigne/doc-smith/task_plan.md` 刷新目标和上下文
2. **每个阶段完成后**：立即更新 `.aigne/doc-smith/task_plan.md`，标记该阶段为 [x]，更新"当前状态"
3. **做出重要决策时**：记录到"关键决策"部分
4. **遇到错误时**：记录到"遇到的错误"部分，包括错误描述和解决方案

### 0. Workspace 检测

**执行任何操作前，首先检测 workspace。**

请阅读下面的参考检查 config.yaml 文件和 sources 数据是否完整。
**workspace 检查流程参考**: `references/workspace-initialization.md`

### 1. 分析数据源

使用 Glob/Grep/Read 工具探索项目根目录。

了解项目目的、结构、主要模块、现有文档和媒体资源。

### 2. 推断用户意图

首先检查用户意图文件是否已存在，如果存在向用户问询是否需要修改。
用户意图格式**必须**参考： `references/user-intent-guide.md`

### 3. 规划文档结构

首先检查文档结构文件是否已存在，如果存在执行第 5 步骤 ，向用户问询是否需要修改。
文档结构规划要求**必须**参考： `references/structure-planning-guide.md`

### 4. 生成 document-structure.yaml

4.1 **生成 YAML 文件**

文档结构数据结构**必须**参考： `references/document-structure-schema.md`

生成文件到: `planning/document-structure.yaml`

4.2 **立即执行程序化校验**

生成 YAML 后，必须立即调用校验工具进行检查：

**调用方式**：使用 `doc-smith-check` 技能进行结构校验

```bash
/doc-smith-check --structure
```

**校验结果处理**:

- ✅ **成功（valid: true）**: 继续执行步骤 5

- ❌ **失败（valid: false）**:
  1. 分析错误报告（errors 字段），理解哪些字段或格式不正确
  2. 阅读 `references/document-structure-schema.md`
  3. 修复错误或重新生成 `.aigne/doc-smith/planning/document-structure.yaml`
  4. 重新调用 `/doc-smith-check --structure`
  5. 如果连续 3 次失败，向用户报告错误并询问如何处理

**重要提醒**:
- 不要跳过校验步骤
- 当工具返回 `fixed: true` 时，**必须**重新读取文件以获取最新内容
- 校验失败时必须采取行动（修复或重新生成），不能忽略错误

### 5. 确认文档结构

5.1: 向用户展示的结构**必须**参考： `references/structure-confirmation-guide.md`
5.2: 确认文档结构符合指定的数据结构，参考：`references/document-structure-schema.md`
5.3: 如果用户提出修改意见，修改之后需要再次调用 `/doc-smith-check --structure` 检查更新后的文档结构。

### 6. 生成文档内容

使用 `doc-smith-content` **子代理**为文档结构中的每个文档生成内容。

**调用方式**：

```
# 生成单个文档
使用 doc-smith-content 子代理生成 /api/overview 文档

# 带自定义要求
使用 doc-smith-content 子代理生成 /api/authentication 文档，重点说明安全注意事项
```

**批量并行生成**（推荐）：

```
使用单独的 doc-smith-content 子代理并行生成以下文档：
- /overview
- /api/authentication
- /guides/getting-started
```

每个子代理完成后会返回摘要，包含：文档路径、主题概述、章节列表、image slots、校验结果。

### 7. 更新已有文档

仅当 `.aigne/doc-smith/docs/` 目录已存在时处理文档更新、文档中图片更新。

**更新流程参考：**
- 整体流程与输入识别：`references/update-workflow.md`
- Changeset 文件处理：`references/changeset-guide.md`
- PATCH 标记处理 (每次文档更新都需要检查文档中是否有 PATCH 需要处理)：`references/patch-guide.md`
- 文档内容要求：`references/document-content-guide.md`

**如果涉及文档结构的修改**：
- 文档结构数据结构参考： `references/document-structure-schema.md`
- 向用户展示的结构请参考： `references/structure-confirmation-guide.md`
- 新增文档时，使用 `doc-smith-content` 子代理生成内容：

```
# 为新增的文档生成内容
使用 doc-smith-content 子代理并行生成以下文档：
- /new-section/overview
- /new-section/details
```

### 8. 结束前确认任务都已完成

8.1 **重新执行文档结构校验**

在结束前，必须再次校验文档结构文件的完整性：

**调用方式**：

```bash
/doc-smith-check --structure
```

如果校验失败，按照步骤 4.2 的错误处理流程处理。

8.2 **执行文档内容检查**

在结束前，必须执行文档内容检查：

**调用方式**：

```bash
/doc-smith-check --content
```

- ✅ **成功（valid: true）**: 继续后续流程

- ❌ **失败（valid: false）**:
  1. 分析错误报告，理解问题所在
  2. 根据错误类型采取行动：
     - 文档缺失：生成缺失的文档
     - 链接错误：修正链接路径
     - 图片问题：提供图片或修正路径
     - 空文档：补充内容
  3. 修复后重新调用 `/doc-smith-check --content`
  4. 如果连续 3 次失败，向用户报告错误并询问如何处理

**重要提醒**:
- 不要跳过内容检查步骤
- 检查失败时必须采取行动（修复或重新生成），不能忽略错误

8.4 **检查是否存在 AFS Image Slot 需要生成图片**

当检测到文档需要展示技术类图片，但是数据源中没有提供的时候，会生成 `AFS Image Slot` 占位符，参考 `references/document-content-guide.md`。

文档生成结束之后，扫描本次生成的文档中是否包含 `AFS Image Slot`：

**Slot 格式**：
```markdown
<!-- afs:image id="architecture-overview" desc="系统架构图，展示各模块关系" -->
<!-- afs:image id="data-flow" key="shared-data-flow" desc="数据流向图" -->
```

需要忽略代码示例中的`AFS Image Slot` 占位符，确保真的是文档中需要展示的图片。

**使用 `generate-slot-image` 子代理并行生成图片**：

```
使用单独的 generate-slot-image 子代理并行生成以下图片：
- docPath=/overview, slotId=architecture-overview, slotDesc="系统架构图，展示各模块关系"
- docPath=/api/auth, slotId=auth-flow, slotDesc="认证流程图", aspectRatio=16:9
- docPath=/guides/start, slotId=setup-steps, slotDesc="安装步骤示意图"
```

**子代理的优势**：
- 每个子代理独立处理一个 slot，有独立的上下文窗口
- 可以并行执行多个子代理，加快生成速度
- 子代理在前台执行，确保权限缺失时，可以向用户确认权限
- 子代理自动处理图片保存和 meta 文件创建

生成的图片会保存在 `.aigne/doc-smith/assets/{key}/images/` 目录。

8.5 **校验图片 slot 已替换（阶段 7.5 / 5.5）**

图片生成完成后，执行 slot 替换校验：

**调用方式**：
```bash
/doc-smith-check --content --check-slots
```

**校验内容**：
- 文档中不存在未替换的 `<!-- afs:image ... -->` 占位符
- 图片引用的相对路径层级正确
- 引用的图片文件存在

**失败处理**：
1. 分析错误报告
2. 对于未替换的 slot：重新调用 `generate-slot-image` 生成
3. 对于路径错误：手动修正文档中的图片路径
4. 修复后重新执行校验

8.6 **核对完成清单**

- [ ] 文档结构校验通过
- [ ] 文档内容检查通过
- [ ] 确认所有生成的文档所在文件夹路径与 `document-structure.yaml` 中的 path 字段一致，并存在 .meta.yaml 文件和主语言文件
- [ ] 确认文档内部链接都有效
- [ ] 确认图片路径正确且文件存在
- [ ] 检查是否存在 `AFS Image Slot` 并生成图片
- [ ] 图片 slot 替换校验通过（`/doc-smith-check --content --check-slots`）

**文档更新的场景**：
- [ ] 用户要求的变更都已处理
- [ ] 文档中的 `::: PATCH` 标记都已处理
- [ ] 如果修改了文档结构，重新执行 YAML 校验
- [ ] 如果修改了文档内容，重新执行内容检查
- [ ] 检查是否新生成了 `AFS Image Slot`, 如果存在则生成图片
- [ ] 图片 slot 替换校验通过

## 自动提交变更

每次完成用户要求的任务，导致 workspace 变化，都自动提交 commit。
```bash
git add .
git commit -m "docsmith: xxxx(合适的标题)"
```

## Workspace 目录结构参考

用户在项目根目录执行 `/doc-smith`，workspace 创建在 `.aigne/doc-smith/` 目录：

```
my-project/                        # 用户的项目目录（cwd）
├── .aigne/
│   └── doc-smith/                 # DocSmith workspace
│       ├── config.yaml            # workspace 配置文件
│       ├── intent/
│       │   └── user-intent.md     # 用户意图描述
│       ├── planning/
│       │   └── document-structure.yaml  # 文档结构计划
│       ├── docs/                  # 生成的文档
│       │   ├── overview/
│       │   │   ├── .meta.yaml     # 元信息 (kind/source/default)
│       │   │   └── zh.md          # 语言版本文件
│       │   └── api/
│       │       └── authentication/
│       │           ├── .meta.yaml
│       │           └── zh.md
│       ├── assets/                # 生成的图片资源
│       │   └── project-architecture/
│       │       ├── .meta.yaml
│       │       └── images/
│       │           └── zh.png
│       └── cache/                 # 缓存数据
│           └── task_plan.md       # 任务规划文件
├── src/                           # 项目源代码（数据源）
├── README.md
└── ...
```

**数据源**：项目本身，从 workspace 通过 `../../` 相对路径访问

## 关键原则

- **Workspace 优先**：执行任何操作前必须先检测和初始化 workspace
- **任务规划先行**：开始工作前必须创建 `.aigne/doc-smith/task_plan.md`，每个阶段前读取，每个阶段后更新
- **持久化记录**：将关键决策、错误和解决方案记录到 `.aigne/doc-smith/task_plan.md`，确保任务可追溯
- **参考引用文件**：执行到每个步骤时，如果提供了参考文件，必须先阅读参考文件中的要求
- **文档内容要求**：执行任何文档相关的生成、更新，都需要参考`references/document-content-guide.md`，确保文档符合要求
- **基于用户意图**：所有规划和生成都应参考 `.aigne/doc-smith/intent/user-intent.md`
- **最小必要原则**：只生成用户意图中明确需要的文档
- **批量执行**：生成文档内容时优先批量执行，缩短执行时间
- **Git 版本管理**：生成/更新/翻译完成后自动将所有变更提交到 Git

## 相关技能

本技能在执行过程中会调用以下技能：

| 技能 | 用途 | 调用示例 |
|------|------|----------|
| `doc-smith-content` | 生成单篇文档内容 | `/doc-smith-content /api/overview` |
| `generate-slot-image` | 生成文档中的图片 | `generate-slot-image docPath=/overview, slotId=architecture-overview, slotDesc="系统架构图，展示各模块关系"`|
| `doc-smith-check` | 校验文档结构和内容 | `/doc-smith-check` 或 `/doc-smith-check --structure` |

以下技能由用户按需独立调用：

| 技能 | 用途 | 调用示例 |
|------|------|----------|
| `doc-smith-localize` | 翻译文档到其他语言 | `/doc-smith-localize --lang en` |
| `doc-smith-publish` | 发布文档到平台 | `/doc-smith-publish --url https://...` |
| `doc-smith-clear` | 清除授权和配置 | `/doc-smith-clear` |
