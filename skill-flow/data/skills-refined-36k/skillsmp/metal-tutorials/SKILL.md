---
name: metal-tutorials
description: 专门处理 Metal 渲染相关的教程文档和参考资料。当用户询问关于 Metal、Metal 渲染、Metal API、渲染管线、着色器、GPU 编程、Metal 代码示例、Metal 最佳实践、Metal 性能优化等 Metal 相关技术问题时自动使用此 skill。自动查找项目 references/ 文件夹中的 Metal 相关 Markdown 文件，基于这些提炼好的文档内容给出精准答案。
---

# Metal 教程 Skill

专门用于处理 Metal 渲染相关的教程文档和参考资料。所有文档都是提炼好的 Markdown 格式，专注于 Metal 渲染管线相关技术。

## 工作流程

当用户询问关于 Metal 相关技术问题时：

1. **自动识别 Metal 相关文档**
   - **优先查找** `references/` 文件夹中的所有 `.md` 文件
   - 如果 `references/` 文件夹不存在或为空，再查找项目根目录中的 `.md` 文件
   - 优先查找文件名包含 "metal"、"Metal"、"tutorial"、"教程" 等关键词的文件
   - 支持多个 Markdown 文件，可以跨文件搜索相关内容
   - 常见文件示例（位于 `references/` 文件夹）：
     - `references/Metal.by.Tutorials.4th.2023.12.md`
     - `references/metal-rendering-guide.md`
     - `references/metal-api-reference.md`
     - `references/metal-best-practices.md`
     - 其他 Metal 相关的 .md 文件

2. **处理文档内容**
   - 直接读取 Markdown 文件内容（所有文档都是提炼好的 .md 格式）
   - 对于大型文档，可以分段处理或按章节搜索
   - 支持跨多个文档搜索相关内容
   - 根据问题关键词智能选择最相关的文档

3. **基于文档内容回答问题（重要：必须明确标注来源）**
   - **必须明确说明答案来源**：
     - 如果答案来自 `references/` 文件夹中的文档，必须明确标注：
       - 📚 **来源文档**：`references/文件名.md`
       - 📖 **具体章节**：如 "Chapter 3: The Rendering Pipeline"
       - 📄 **代码位置**：如果引用了代码，说明代码所在的章节或位置
     - 如果多个文档都有相关内容，列出所有来源
   - 仔细阅读相关文档内容
   - 从文档中查找准确答案
   - 引用具体的章节标题、代码示例或 API 说明
   - 如果多个文档都有相关内容，可以综合引用
   - **如果文档中没有相关信息**：
     - ❌ **明确告知用户**：在 `references/` 文件夹中没有找到相关信息
     - ❓ **询问用户**：是否希望我：
       - 1. 通过网络搜索查找相关信息
       - 2. 基于大模型的通用知识来回答
       - 3. 或者等待用户提供更多信息
     - **不要**在没有明确说明来源的情况下，直接使用网络或大模型的知识回答

## 回答格式要求

### 当找到参考文档时

回答格式示例：

```
📚 **来源**：`references/Metal.by.Tutorials.4th.2023.12.md`
📖 **章节**：Chapter 3: The Rendering Pipeline

[答案内容]

**代码示例**（来自 Chapter 1）：
```swift
[代码内容]
```
```

### 当找不到参考文档时

回答格式示例：

```
❌ **未找到参考**

在 `references/` 文件夹中没有找到关于 [问题主题] 的相关信息。

❓ **请选择**：
1. 通过网络搜索查找相关信息
2. 基于大模型的通用知识来回答（可能不够准确）
3. 等待您提供更多信息或添加相关文档

请告诉我您希望使用哪种方式？
```

## 文档存放位置

**所有 Metal 相关的 Markdown 文档应该放在 `references/` 文件夹中**：

```
project-root/
├── references/                    # Metal 文档存放文件夹
│   ├── Metal.by.Tutorials.4th.2023.12.md
│   ├── metal-rendering-guide.md
│   ├── metal-api-reference.md
│   └── [其他 Metal 相关的 .md 文件]
├── .cursor/
│   └── skills/
│       └── metal-tutorials/
└── ...
```

## 支持的文档类型

此 skill 专门处理以下类型的 Metal 相关文档：

- **教程文档**：如 Metal by Tutorials 等系统教程
- **API 参考**：Metal API 使用说明和示例
- **最佳实践**：Metal 性能优化和最佳实践指南
- **代码示例**：Metal 代码示例和实现细节
- **概念解释**：Metal 渲染管线、着色器等核心概念

所有文档都应该是提炼好的 Markdown 格式（.md 文件），存放在 `references/` 文件夹中。

## 使用方法

### 直接提问

用户可以直接提问，skill 会自动识别并使用 `references/` 文件夹中的相关文档：

- "Metal 的渲染管线是什么？"
- "如何创建 MTLDevice？"
- "Command Buffer 和 Command Queue 有什么区别？"
- "第 3 章的主要内容是什么？"
- "Metal 中如何处理纹理？"
- "延迟渲染的实现方式？"

### 多文档支持

如果 `references/` 文件夹中有多个 Metal 相关的 Markdown 文件，skill 会：
- 自动搜索所有相关文档
- 根据问题选择最相关的文档
- 可以跨文档综合回答
- **列出所有相关文档的来源**

## 针对 Metal 技术的特殊处理

当处理 Metal 相关问题时：

- **API 识别**：自动识别 Metal API（如 MTLDevice、MTLCommandBuffer、MTLRenderPipelineDescriptor 等）
- **概念理解**：理解 Metal 核心概念（渲染管线、着色器、资源管理等）
- **代码示例**：优先查找和引用代码示例
- **章节定位**：能够定位到具体的章节（如 "Chapter 3: The Rendering Pipeline"）
- **跨文档搜索**：如果问题涉及多个主题，可以搜索多个文档
- **来源标注**：必须明确标注每个答案的来源文档和章节

## 触发关键词

Skill 会在以下情况下自动触发：

- Metal 相关技术问题
- 渲染管线、着色器、GPU 编程
- Metal API 使用问题
- 代码示例请求
- 章节内容查询
- 概念解释请求
- 性能优化问题

**注意**：即使没有明确提到文档名称，只要问题涉及 Metal 技术内容，skill 也会自动检查 `references/` 文件夹中的相关文档。

## 重要原则

### 必须遵守的规则

1. **明确标注来源**：每个答案都必须明确说明是否来自 `references/` 文件夹中的文档
2. **具体出处**：如果来自参考文档，必须说明：
   - 文档文件名（如 `references/Metal.by.Tutorials.4th.2023.12.md`）
   - 具体章节（如 "Chapter 3: The Rendering Pipeline"）
   - 代码位置（如果引用了代码）
3. **找不到时询问**：如果在 `references/` 文件夹中找不到相关信息，必须：
   - 明确告知用户未找到参考
   - 询问用户是否要使用网络搜索或大模型知识
   - **不要**直接使用网络或大模型知识而不说明
4. **诚实回答**：如果答案是基于大模型知识而非参考文档，必须明确说明

## 注意事项

- **文档位置**：所有 Metal 相关文档应该放在 `references/` 文件夹中
- **文档格式**：所有文档都应该是提炼好的 Markdown 格式（.md 文件）
- **文件命名**：建议文件名包含 "metal" 或相关关键词，便于自动识别
- **多文档支持**：支持处理多个 Markdown 文件，可以跨文件搜索
- **准确性**：始终基于文档的实际内容回答，不要猜测
- **版本信息**：注意区分不同版本或不同文档的内容差异
- **来源透明**：必须明确标注答案来源，提高可信度

## 参考资源

- 详细使用说明：参见 [.cursor/skills/metal-tutorials/references/usage.md](.cursor/skills/metal-tutorials/references/usage.md)
