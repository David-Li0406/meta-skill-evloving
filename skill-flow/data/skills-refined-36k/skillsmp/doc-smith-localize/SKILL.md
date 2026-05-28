---
name: doc-smith-localize
description: Translate Doc-Smith generated documentation into multiple languages. Use this skill when the user requests document translation, localization, or multi-language support. Supports batch translation of documents and images.
---

# Doc-Smith 文档翻译

将文档翻译成多种语言，支持批量翻译和术语一致性。

## Usage

```bash
# 翻译所有文档到指定语言
/doc-smith-localize --lang en
/doc-smith-localize -l en

# 翻译到多个语言
/doc-smith-localize --lang en --lang ja
/doc-smith-localize -l en -l ja

# 只翻译指定文档
/doc-smith-localize --lang en --path /overview
/doc-smith-localize -l en -p /overview

# 翻译多个指定文档
/doc-smith-localize --lang en --path /overview --path /api/auth

# 强制重新翻译（覆盖已有翻译）
/doc-smith-localize --lang en --force
/doc-smith-localize -l en -f

# 跳过图片翻译
/doc-smith-localize --lang en --skip-images
```

## Options

| Option | Alias | Description |
|--------|-------|-------------|
| `--lang <code>` | `-l` | 目标语言代码（可多次使用），如 en, ja, fr, de |
| `--path <docPath>` | `-p` | 指定要翻译的文档路径（可多次使用），不指定则翻译全部 |
| `--force` | `-f` | 强制重新翻译，覆盖已存在的翻译文件 |
| `--skip-images` | | 跳过图片翻译，只翻译文档内容 |

## 触发场景

- 用户要求翻译文档到其他语言
- 用户说"翻译"、"本地化"、"多语言"
- 批量翻译多篇文档
- 优化某篇文档的翻译质量

## 工作流程

**任务规划机制**：翻译任务涉及多个文档和图片，使用持久化的任务规划文件来跟踪执行进度，确保长时间任务的可追溯性和可恢复性。

### 任务规划初始化

**在开始任何实际工作前，必须先初始化任务规划文件。**

在 `.aigne/doc-smith/cache` 目录创建 `translate_task_plan.md` 文件，如果文件已存在，可以覆盖之前的文件，内容模板：

```markdown
# Document Translation Task Plan

## Goal
[One sentence describing this task, e.g., Translate all documents into English and Japanese]

## Configuration
- Source language: zh
- Target languages: en, ja
- Document scope: All / Specified paths
- Force re-translation: No
- Skip images: No

## Execution Phases

- [ ] Phase 1: Detect Workspace
- [ ] Phase 2: Read configuration and validate parameters
- [ ] Phase 3: Load glossary
- [ ] Phase 4: Batch translate documents
  - [ ] Document 1: /overview → en
  - [ ] Document 1: /overview → ja
  - [ ] Document 2: /api/auth → en
  - [ ] ... (expand based on actual document list)
- [ ] Phase 5: Translate images (if not skipped)
  - [ ] Image 1: arch → en
  - [ ] Image 2: flow → en
  - [ ] ... (expand based on actual image list)
- [ ] Phase 6: Update image references in documents
- [ ] Phase 7: Update config.yaml
- [ ] Phase 8: Generate translation report
- [ ] Phase 9: Commit changes to Git

## Execution Statistics
- Total documents: 0
- Documents translated: 0
- Documents skipped: 0
- Documents failed: 0
- Total images: 0
- Images translated: 0
- Images skipped: 0
- Images failed: 0

## Key Decisions
[Record important decisions made during execution and their rationale]

## Errors Encountered
[Record errors encountered and solutions, format: Error description -> Solution]

## Current Status
**Executing Phase 1** - Detecting Workspace
```

**规划文件使用规则**：
1. **每个阶段开始前**：读取 `.aigne/doc-smith/cache/translate_task_plan.md` 刷新目标和上下文
2. **每个阶段完成后**：立即更新规划文件，标记该阶段为 [x]，更新"当前状态"和"执行统计"
3. **每个子任务完成后**：更新对应的子任务状态（文档翻译、图片翻译）
4. **做出重要决策时**：记录到"关键决策"部分
5. **遇到错误时**：记录到"遇到的错误"部分，包括错误描述和解决方案

### 1. 检测 Workspace

检查当前目录是否为有效的 Doc-Smith workspace：

```bash
ls -la .aigne/doc-smith/config.yaml .aigne/doc-smith/planning/document-structure.yaml .aigne/doc-smith/docs/
```

如果不存在，提示用户先使用 `doc-smith` 生成文档。

### 2. 读取配置

从 `.aigne/doc-smith/config.yaml` 读取：
- `locale`：源语言代码

从 `.aigne/doc-smith/planning/document-structure.yaml` 读取：
- 所有文档路径列表（遍历 documents 数组提取 path 字段）

### 3. 验证参数

**验证目标语言**：
- 过滤掉与源语言相同的语言
- 如果过滤后为空，提示用户："所有目标语言都与源语言相同，请指定不同的目标语言"

**验证文档路径**（如果指定了 `--path`）：
- 检查路径是否存在于 document-structure.yaml 中
- 如果路径无效，提示用户哪些路径不存在

### 4. 加载术语表

检查是否存在术语表文件：
- `.aigne/doc-smith/glossary.yaml`
- `.aigne/doc-smith/glossary.md`

如果存在，读取术语表内容供翻译使用。

### 5. 批量翻译文档

使用 `translate-document` 子代理批量翻译文档。

**生成翻译任务列表**：

对于每个文档和每种目标语言，创建一个翻译任务：

```
文档列表: [/overview, /api/auth, /guides/start]
目标语言: [en, ja]

任务列表:
1. docPath=/overview, targetLanguage=en
2. docPath=/overview, targetLanguage=ja
3. docPath=/api/auth, targetLanguage=en
4. docPath=/api/auth, targetLanguage=ja
5. docPath=/guides/start, targetLanguage=en
6. docPath=/guides/start, targetLanguage=ja
```

**并行调用子代理**：

```
使用单独的 translate-document 子代理并行翻译以下文档：
- docPath=/overview, targetLanguage=en, sourceLanguage=zh, force=false
- docPath=/overview, targetLanguage=ja, sourceLanguage=zh, force=false
- docPath=/api/auth, targetLanguage=en, sourceLanguage=zh, force=false
```

**注意**：
- 每个子代理处理一个文档到一种语言的翻译
- 子代理会检查 hash 避免重复翻译（除非 force=true）
- 建议每批并行 3-5 个子代理，避免上下文过载
- 子代理在前台运行，当有权限确认时，用户可响应权限确认操作

### 6. 翻译图片（可选）

如果未指定 `--skip-images`，扫描并翻译需要本地化的图片。

#### 6.1 扫描图片资源

查找所有图片的 `.meta.yaml` 文件：

```bash
find .aigne/doc-smith/assets -name ".meta.yaml" -type f
```

#### 6.2 检查图片是否需要翻译

对每个图片资源，读取 `.meta.yaml`：

**跳过条件**（满足任一则跳过）：
- `generation.shared` 为 `true`（跨语言共享的图片，如纯图标、无文字图表）
- `languages` 数组已包含目标语言（已翻译）
- 源语言图片不存在

**需要翻译的条件**：
- `generation.shared` 不为 `true`（或不存在）
- `languages` 数组不包含目标语言
- 源语言图片存在

#### 6.3 翻译图片

对需要翻译的图片，调用 `doc-smith-images` 的 `--update` 功能：

```bash
/doc-smith-images "将图片中的文字从 {sourceLanguage} 翻译成 {targetLanguage}，保持图片的布局和风格不变" \
  --update .aigne/doc-smith/assets/{key}/images/{sourceLanguage}.png \
  --savePath .aigne/doc-smith/assets/{key}/images/{targetLanguage}.png \
  --locale {targetLanguage}
```

#### 6.4 更新图片 .meta.yaml

翻译完成后更新图片的元信息：

```yaml
languages:
  - zh
  - en  # 新增
translations:
  en:
    sourceHash: "abc123..."
    translatedAt: "2026-01-21T10:00:00.000Z"
```

### 7. 更新文档中的图片引用

翻译后的文档需要引用对应语言的图片。

**替换逻辑**：

在翻译后的文档中，检查图片引用并更新语言后缀：

```markdown
# 原文档（zh.md）中的图片引用
![架构图](../../assets/arch/images/zh.png)

# 翻译后文档（en.md）中应更新为
![Architecture](../../assets/arch/images/en.png)
```

**处理逻辑**：

1. 使用正则匹配文档中的图片引用：`!\[.*?\]\((.*?/images/)(\w+)(\.png|\.jpg)\)`
2. 检查目标语言图片是否存在
3. 如果存在，替换语言后缀
4. 如果不存在（shared=true 或跳过图片翻译），保持原语言后缀

### 8. 更新 config.yaml

将新的目标语言添加到 `translateLanguages` 数组：

读取 `.aigne/doc-smith/config.yaml`，更新：

```yaml
translateLanguages:
  - en
  - ja  # 新增
```

**注意**：避免重复添加已存在的语言。

### 9. 生成翻译报告

返回翻译结果摘要：

```
翻译完成:

配置:
- 源语言: zh
- 目标语言: en, ja

文档翻译:
- 总数: 10
- 已翻译: 7
- 跳过（未变化）: 3
- 失败: 0

图片翻译:
- 总数: 5
- 已翻译: 3
- 跳过（shared）: 1
- 跳过（已存在）: 1
- 失败: 0
```

## 翻译质量要求

- **术语一致性**：使用术语表保持专业术语统一
- **格式保持**：保持原文的 Markdown 格式
- **上下文理解**：根据技术文档语境选择合适译法
- **自然流畅**：翻译结果应符合目标语言习惯

## 错误处理

### Workspace 不存在

```
错误: Doc-Smith workspace 不存在

当前目录下未找到 .aigne/doc-smith/ 目录。
请先使用 /doc-smith 生成文档。
```

### 目标语言无效

```
错误: 所有目标语言都与源语言 (zh) 相同

请指定不同的目标语言，例如: /doc-smith-localize -l en
```

### 文档路径无效

```
错误: 以下文档路径不存在于文档结构中:
- /invalid/path
- /another/invalid

有效的文档路径包括:
- /overview
- /api/auth
- /guides/start

请检查文档路径是否正确。
```

### 翻译部分失败

```
翻译完成（部分失败）:

成功: 8/10 个文档
失败:
- /api/complex: 内容过长，翻译超时
- /guides/advanced: 源文件不存在

建议: 使用 --path 参数单独重试失败的文档
```

## 示例

**翻译所有文档到英文和日文**：
```bash
/doc-smith-localize -l en -l ja
```

**翻译指定文档到英文**：
```bash
/doc-smith-localize -l en -p /overview -p /api/auth
```

**强制重新翻译（覆盖已有）**：
```bash
/doc-smith-localize -l en --force
```

**只翻译文档，跳过图片**：
```bash
/doc-smith-localize -l en --skip-images
```

## 关键原则

- **任务规划先行**：开始工作前必须创建 `.aigne/doc-smith/cache/translate_task_plan.md`，每个阶段前读取，每个阶段后更新
- **持久化记录**：将关键决策、错误和解决方案记录到规划文件，确保任务可追溯
- **增量翻译**：通过 sourceHash 比对避免重复翻译，节省时间和资源
- **批量执行**：翻译文档时优先批量并行执行，缩短执行时间
- **子代理隔离**：每个文档的翻译由独立子代理处理，避免上下文膨胀
