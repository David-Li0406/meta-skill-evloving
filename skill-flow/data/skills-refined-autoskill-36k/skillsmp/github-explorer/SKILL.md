---
name: github-explorer
description: Explore and summarize popular GitHub projects. Use when the user wants to discover trending GitHub repositories, analyze project details, or get summaries of popular projects.
allowed-tools:
  - WebFetch
  - WebSearch
  - Read
  - Write
  - Grep
  - Task
user-invocable: true
argument-hint: <query>
---

# GitHub 项目探索和总结

## Instructions

当用户想要探索和总结 GitHub 上的热门项目时，按照以下步骤执行：

### 1. 确定搜索目标

- 如果用户提供了具体的项目名称或技术栈，直接搜索相关项目
- 如果用户没有明确目标，搜索当前热门或趋势项目
- 使用 WebSearch 工具查找相关 GitHub 仓库

### 2. 收集项目信息

使用以下方法收集项目信息：

- **WebSearch**: 搜索 "trending GitHub repositories" 或 "popular GitHub projects <tech-stack>"
- **WebFetch**: 获取 GitHub 项目页面信息
- **GitHub API**: 如果需要，可以访问 GitHub API 获取项目详细信息

### 3. 分析项目内容

对每个项目进行以下分析：

- **项目名称和描述**: 获取项目的基本信息
- **Star 数量**: 评估项目的受欢迎程度
- **主要技术栈**: 识别项目使用的主要技术
- **最近更新**: 检查项目活跃度
- **贡献者数量**: 评估社区活跃度
- **项目特点**: 识别项目的独特功能或优势
- **文档质量**: 评估项目的文档完整性

### 4. 生成项目总结

为每个项目生成以下信息：

- **项目名称**: 项目完整名称
- **描述**: 项目的主要功能和目标
- **GitHub 链接**: 项目地址
- **Stars**: Star 数量
- **技术栈**: 使用的主要技术
- **最后更新**: 最近更新时间
- **项目亮点**: 项目的独特功能或优势
- **适用场景**: 适合的应用场景

### 5. 提供综合分析

- 按受欢迎程度排序项目列表
- 提供整体趋势分析
- 推荐最适合用户需求的项目
- 指出项目之间的差异和特点

## Output Format

以结构化格式输出项目信息：

```
## 项目名称
- **描述**: 项目功能描述
- **GitHub**: [链接地址](https://github.com/...)
- **Stars**: 数量
- **技术栈**: 技术列表
- **最后更新**: 日期
- **亮点**: 项目特色
- **适用场景**: 使用场景
```

## Examples

### 示例 1: 探索前端框架
用户: "帮我找一些流行的前端框架项目"
- 搜索 "popular frontend frameworks GitHub"
- 分析 React, Vue, Angular 等项目
- 提供详细的技术栈和特点对比

### 示例 2: 探索 AI 相关项目
用户: "找一些热门的 AI 开源项目"
- 搜索 "trending AI open source projects"
- 分析项目的技术栈和应用场景
- 提供项目亮点和适用场景

### 示例 3: 探索特定技术
用户: "找一些用 TypeScript 写的优秀项目"
- 搜索 "best TypeScript projects GitHub"
- 分析项目质量和技术特点
- 提供综合评价和推荐