# Metal 教程 Skill 使用指南

## 概述

这个 skill 专门用于处理 Metal 渲染相关的教程文档和参考资料。所有文档都是提炼好的 Markdown 格式，专注于 Metal 渲染管线相关技术。

**重要特性**：Skill 会明确标注每个答案的来源，如果在参考文档中找不到信息，会询问用户是否要使用网络搜索或大模型知识。

## 文档存放位置

**重要**：所有 Metal 相关的 Markdown 文档应该放在项目的 `references/` 文件夹中。

```
project-root/
├── references/                    # Metal 文档存放文件夹（推荐）
│   ├── Metal.by.Tutorials.4th.2023.12.md
│   ├── metal-rendering-guide.md
│   ├── metal-api-reference.md
│   ├── metal-best-practices.md
│   └── [其他 Metal 相关的 .md 文件]
└── ...
```

## 回答格式说明

### 当找到参考文档时

Skill 会明确标注来源：

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

Skill 会明确告知并询问：

```
❌ **未找到参考**

在 `references/` 文件夹中没有找到关于 [问题主题] 的相关信息。

❓ **请选择**：
1. 通过网络搜索查找相关信息
2. 基于大模型的通用知识来回答（可能不够准确）
3. 等待您提供更多信息或添加相关文档

请告诉我您希望使用哪种方式？
```

## 支持的文档

Skill 会自动识别和处理 `references/` 文件夹中的 Metal 相关 Markdown 文件，例如：

- `references/Metal.by.Tutorials.4th.2023.12.md` - Metal by Tutorials 完整教程
- `references/metal-rendering-guide.md` - Metal 渲染指南
- `references/metal-api-reference.md` - Metal API 参考
- `references/metal-best-practices.md` - Metal 最佳实践
- 其他 Metal 相关的 .md 文件

## 使用场景

### 1. 技术概念查询

**问题示例**：
- "Metal 的渲染管线是什么？"
- "Command Buffer 和 Command Queue 有什么区别？"
- "什么是延迟渲染？"

**处理方式**：
- 自动搜索 `references/` 文件夹中相关文档的概念解释
- 引用具体的章节和代码示例
- 提供准确的技术说明
- **明确标注来源文档和章节**

### 2. API 使用查询

**问题示例**：
- "如何创建 MTLDevice？"
- "MTLRenderPipelineDescriptor 怎么用？"
- "纹理加载的代码示例？"

**处理方式**：
- 在 `references/` 文件夹中查找 API 使用说明
- 提供完整的代码示例
- 说明参数和返回值
- **标注代码所在的文档和章节**

### 3. 章节内容查询

**问题示例**：
- "第 3 章的主要内容是什么？"
- "Chapter 14 讲的是什么？"
- "关于 G-buffer 的内容在哪里？"

**处理方式**：
- 在 `references/` 文件夹中定位到具体章节
- 总结章节要点
- 引用关键代码示例
- **明确说明来自哪个文档的哪个章节**

### 4. 代码示例查询

**问题示例**：
- "创建 pipeline descriptor 的完整代码？"
- "如何实现阴影渲染？"
- "粒子系统的实现代码？"

**处理方式**：
- 在 `references/` 文件夹中查找相关代码示例
- 提供完整的代码块
- 说明代码的上下文和用途
- **标注代码来源**

### 5. 跨文档综合查询

**问题示例**：
- "Metal 中处理纹理的几种方式？"
- "性能优化的最佳实践有哪些？"

**处理方式**：
- 搜索 `references/` 文件夹中的多个相关文档
- 综合不同文档的内容
- 提供全面的答案
- **列出所有相关文档的来源**

## 多文档支持

如果 `references/` 文件夹中有多个 Metal 相关的 Markdown 文件：

1. **自动识别**：Skill 会自动识别所有相关文档
2. **智能选择**：根据问题选择最相关的文档
3. **跨文档搜索**：可以在多个文档中搜索相关内容
4. **综合回答**：如果多个文档都有相关信息，可以综合引用
5. **来源标注**：列出所有相关文档的来源

## 最佳实践

### 文档组织建议

1. **统一位置**：所有 Metal 相关文档放在 `references/` 文件夹
   - ✅ `references/Metal.by.Tutorials.4th.2023.12.md`
   - ✅ `references/metal-rendering-guide.md`
   - ❌ `Metal.by.Tutorials.4th.2023.12.md`（根目录，不推荐）

2. **文件命名**：使用清晰的命名，包含 "metal" 或相关关键词
   - ✅ `metal-rendering-guide.md`
   - ✅ `metal-api-reference.md`
   - ❌ `doc1.md`（不推荐）

3. **文档结构**：保持清晰的章节结构
   - 使用 `# Chapter X` 等标题
   - 代码示例使用代码块标记
   - 重要概念使用清晰的标题

4. **内容提炼**：确保文档是提炼好的
   - 移除无关内容
   - 保留核心技术和代码示例
   - 保持结构清晰

### 提问建议

1. **直接提问**：不需要每次都提文件名或路径
   - ✅ "Metal 的渲染管线是什么？"
   - ✅ "如何创建 MTLDevice？"
   - ❌ "根据 references/Metal.by.Tutorials.4th.2023.12.md，Metal 的渲染管线是什么？"（不必要）

2. **具体问题**：问具体的技术问题
   - ✅ "Command Buffer 的提交方式有哪些？"
   - ✅ "延迟渲染中 G-buffer 的组成是什么？"

3. **章节查询**：可以直接问章节内容
   - ✅ "第 3 章的主要内容是什么？"
   - ✅ "Chapter 14 关于什么？"

## 来源标注的重要性

Skill 会明确标注每个答案的来源，这有助于：

1. **可信度**：知道答案来自哪里，是否可靠
2. **可追溯**：可以回到原始文档查看完整内容
3. **准确性**：区分来自参考文档的答案和来自大模型的答案
4. **学习**：了解哪些文档包含哪些内容

## 故障排除

### 问题：Skill 没有自动触发

**解决方案**：
- 确保问题涉及 Metal 相关技术
- 可以在问题中加入 "Metal" 关键词
- 检查 `references/` 文件夹中是否有 Metal 相关的 .md 文件

### 问题：找不到相关文档

**解决方案**：
- 确保文档在 `references/` 文件夹中
- 确保文档文件名包含 "metal" 或相关关键词
- 检查文件扩展名是否为 .md
- Skill 会询问是否要使用网络搜索或大模型知识

### 问题：答案不准确

**解决方案**：
- 确保文档内容是提炼好的，结构清晰
- 检查文档中是否真的包含相关信息
- 可以更具体地提问，帮助 skill 定位内容
- 检查答案的来源标注，确认是否来自参考文档

### 问题：答案没有标注来源

**解决方案**：
- 提醒 AI 需要标注来源
- 检查 skill 配置是否正确
- 如果答案来自大模型而非参考文档，应该明确说明

## 添加新文档

当你添加新的 Metal 相关 Markdown 文件时：
1. 放在 `references/` 文件夹中
2. 文件名包含 "metal" 或相关关键词
3. Skill 会自动识别和使用
4. 答案会明确标注来自哪个文档

## 下一步

1. 将你的 Metal 相关 Markdown 文件放到 `references/` 文件夹
2. 确保文件名包含相关关键词
3. 开始提问，skill 会自动识别和使用相关文档
4. 注意查看答案的来源标注，确认答案的可靠性
