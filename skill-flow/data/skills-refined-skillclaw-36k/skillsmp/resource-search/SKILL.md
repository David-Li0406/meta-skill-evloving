---
name: resource-search
description: Search and collect the latest Skills resources including blog posts, GitHub repositories, video tutorials, case studies, and tools. Focus on Skills development, SKILL.md examples, and Skills best practices. Use when searching for new Skills resources, updating the resource library, or when the user asks to find Skills-related content.
---

# 资源搜索 Skill

## 描述

这个 Skill 帮助用户搜索和收集 Skills 相关的最新资料，包括博客文章、GitHub 仓库、视频教程等。

**重要：** 本项目专注于 Skills 本身，不是 Claude Code 的使用教程。搜索时应该专注于：

- Skills 开发教程
- SKILL.md 文件编写
- Skills 最佳实践
- Skills 示例和案例
- Agent Skills 相关内容

## 用途

定期更新和维护 Skills 资料库，搜索最新的社区资源并归档。

## 指令

当用户要求搜索最新资料时，请按照以下步骤操作：

### 搜索流程

1. **确定搜索关键词**
  - 根据用户需求确定搜索关键词
  - **重要：** 专注于 Skills 相关内容，避免搜索 Claude Code 使用教程
  - 常用关键词：
    - `Agent Skills`、`Claude Skills`、`Skills tutorial`
    - `SKILL.md`、`create Skills`、`build Skills`
    - `Skills examples`、`Skills best practices`
    - `Skills GitHub`、`Skills repository`
  - **避免的关键词：** `Claude Code tutorial`、`Claude Code install`、`Claude Code usage`（这些是 Claude Code 使用教程，不是 Skills 教程）
2. **使用动态搜索源**
  - **优先使用配置的搜索源**：读取 `community-resources/data/search-sources.json` 获取已配置的搜索源
  - **搜索源优先级**：按照配置的优先级顺序（官方博客 > 文档网站 > 社区网站 > GitHub 组织）
  - **生成搜索查询**：对每个搜索源，使用其搜索模式结合默认关键词生成完整搜索查询
  - **示例**：对于 "Cursor 官方博客" 搜索源，使用 `site:cursor.com/cn/blog Skills` 等模式
3. **执行搜索**
  - **优先搜索**：先使用配置的搜索源进行定向搜索
  - **全网搜索**：然后使用多个搜索关键词进行全网搜索
  - 搜索范围包括：
    - 配置的搜索源（官方博客、文档网站、社区网站等）
    - GitHub 仓库（搜索 Skills 示例项目）
    - 技术博客（Skills 开发教程）
    - 视频平台（YouTube、Bilibili）
    - 技术社区和论坛
4. **处理用户提供的新资源**
  - **提取来源信息**：当用户提供新资源时，从 URL 中提取基础域名和路径
  - **评估相关性**：检查是否与 Skills 相关，确认不是 Claude Code 使用教程
  - **建议添加到搜索源**：如果资源相关且来源有价值，建议将其添加到搜索源配置
  - **自动提取流程**：
    - 从 URL 提取基础 URL（如 `https://cursor.com/cn/blog`）
    - 识别来源类型（博客、文档、社区、GitHub 等）
    - 生成搜索模式（如 `site:cursor.com/cn/blog Skills`）
    - 更新 `community-resources/data/search-sources.json`
    - 更新 `community-resources/SEARCH-SOURCES.md`
5. **筛选和整理结果**
  - **重点筛选：** 只保留与 Skills 开发、SKILL.md 编写、Skills 示例相关的内容
  - **排除内容：** 
    - Claude Code 安装和配置教程
    - Claude Code 使用教程（除非专门讲 Skills）
    - 与 Skills 无关的 Claude Code 内容
  - 筛选相关度高的资源
  - 排除重复内容
  - 按分类整理（博客、视频、仓库、案例、工具）
6. **格式化输出**
  - 按照资源模板格式输出
  - 包含：标题、链接、描述、作者、标签、日期等信息

### 搜索分类

- **博客文章**：搜索技术博客、教程文章
- **GitHub 仓库**：搜索相关代码仓库和项目
- **视频教程**：搜索 YouTube、Bilibili 等平台的视频
- **案例研究**：搜索实际应用案例
- **工具插件**：搜索开发工具和插件

### 输出格式

每个资源按以下格式输出：

```markdown
- **{标题}**
  - 链接：{URL}
  - 描述：{描述}
  - 作者：{作者}
  - 发布日期：{日期}
  - 标签：{标签}
  - 添加日期：{当前日期}
```

## 示例

**用户输入：** "搜索最新的 Skills 教程"

**处理流程：**

1. 使用关键词 "Agent Skills tutorial"、"create Skills"、"SKILL.md tutorial" 进行搜索
2. 筛选与 Skills 开发相关的教程文章和视频
3. 排除 Claude Code 使用教程（除非专门讲 Skills）
4. 按分类整理结果
5. 输出格式化的资源列表

**用户输入：** "搜索 Skills 的 GitHub 仓库"

**处理流程：**

1. 使用关键词 "Skills GitHub"、"Agent Skills examples"、"SKILL.md examples" 进行搜索
2. 筛选包含 Skills 示例的 GitHub 仓库
3. 整理仓库信息（名称、描述、Stars、作者）
4. 输出格式化的仓库列表

## 动态搜索源管理

### 搜索源配置文件

搜索源配置位于 `community-resources/data/search-sources.json`，包含：

- **官方博客**：Cursor、Claude 等官方技术博客
- **文档网站**：官方文档站点
- **社区网站**：Skills 相关社区
- **GitHub 组织**：包含 Skills 示例的 GitHub 组织

### 添加新搜索源

当用户提供新资源时，应该：

1. **提取来源**：从 URL 提取基础 URL（如 `https://example.com/blog`）
2. **识别类型**：判断是博客、文档、社区还是 GitHub
3. **生成搜索模式**：创建 `site:` 搜索模式
4. **更新配置**：
  - 编辑 `community-resources/data/search-sources.json`
  - 在相应分类下添加新条目
  - 更新 `community-resources/SEARCH-SOURCES.md`
  - 记录添加原因和日期

### 示例：添加 Cursor 官方博客

**用户提供资源：** `https://cursor.com/cn/blog/dynamic-context-discovery`

**处理步骤：**

1. 提取基础 URL：`https://cursor.com/cn/blog`
2. 识别类型：官方博客
3. 生成搜索模式：
  - `site:cursor.com/cn/blog Skills`
  - `site:cursor.com/cn/blog Agent Skills`
  - `site:cursor.com/cn/blog SKILL.md`
4. 添加到 `search_sources.official_blogs` 分类

## 注意事项

- **核心原则：** 本项目专注于 Skills，不是 Claude Code 使用教程
- **动态扩展：** 根据用户提供的资源自动扩展搜索源
- 确保搜索结果的时效性（优先最新内容）
- 验证链接的有效性
- 避免重复添加已有资源
- 保持资源描述的准确性
- **严格筛选：** 只添加与 Skills 开发、SKILL.md 编写、Skills 示例相关的内容
- **排除标准：** 如果资源主要是 Claude Code 使用教程，而不是 Skills 相关内容，应该排除

## GitHub Pages 同步（必读）

本仓库启用了 GitHub Pages，用于统一展示 `community-resources/` 资源库：

- 更新资源文件（如 `community-resources/*.md`、`community-resources/data/resources.json`、`community-resources/reports/*.md`）后，**commit + push** 即会触发 GitHub Actions 自动同步并发布到 Pages
- 本地预览/生成可运行：`python3 scripts/generate_github_pages.py`（会把 `community-resources/` 同步到 `docs/community-resources/` 供 MkDocs 构建）

