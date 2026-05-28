---
name: wechat-article-fetcher
description: WeChat official account article fetcher with intelligent ranking based on research interests (AI Agent, System Design, GitHub Open Source). Supports fetching from specific accounts or all followed accounts with date filtering and Obsidian integration.
dependencies: []
---

# WeChat Article Fetcher Skill

## 概述
这是一个强大的微信公众号文章获取和分析工具，支持**智能排序**、**研究兴趣匹配**、**日期过滤**以及**Obsidian 集成**。可以根据你的研究兴趣（AI Agent、System Design、GitHub 开源项目）对文章进行智能排序和筛选，自动生成结构化报告并保存到 Obsidian vault。

## 核心功能
- 🎯 **智能排序**: 基于研究兴趣自动评分排序（AI Agent、System、GitHub 开源项目）
- 📱 **多账号获取**: 支持获取指定公众号或所有关注公众号的文章
- 📅 **日期过滤**: 支持获取昨天、特定日期范围的文章
- 🏷️ **智能标签**: 自动添加相关标签（#ai-agent、#system、#github、#paper 等）
- 📊 **结构化输出**: 生成 Obsidian 格式的 Markdown 报告，包含 frontmatter、内部链接
- 💾 **自动保存**: 直接保存到 Obsidian vault 的 `wechat-official-aacount/` 文件夹
- 🔍 **质量过滤**: 自动过滤营销文章、低质量内容、重复文章
- 📈 **统计分析**: 提供文章分类统计、研究洞察、行动建议

## 何时使用

### 日常信息获取
- **每日晨读**: 获取昨天的最新文章，早上 7:45 自动推送
- **研究追踪**: 追踪 AI Agent、System Design 领域的最新进展
- **开源发现**: 发现 GitHub 上有趣的开源项目和工具

### 特定需求
- **公众号调研**: 查看某个特定公众号的历史文章
- **专题研究**: 获取某个时间范围内的相关文章
- **论文发现**: 找到值得阅读的论文和开源代码

## 研究兴趣优先级

### Tier 1 (优先级 10): 核心研究
- AI Agent for System
- Multi-Agent Systems
- Autonomous Agents
- LLM Agent

### Tier 2 (优先级 8-9): 系统设计
- System Design
- Distributed Systems
- Operating Systems
- Computer Architecture

### Tier 3 (优先级 8): GitHub 开源项目
- GitHub Open Source Projects
- Interesting Open Source Tools
- Framework Libraries
- Practical Implementations

### Tier 4 (优先级 7-8): AI/ML 核心
- Machine Learning
- Deep Learning
- Reinforcement Learning
- Transformers, LLMs

### Tier 5 (优先级 6-7): 学术研究
- SOTA methods
- Benchmarks
- Paper Reviews
- Top conferences (NeurIPS, ICML, OSDI, SOSP, ICSE)

### Tier 6 (优先级 4-5): 实践指南
- Tutorials
- Best Practices

## 使用方法

### 场景 1: 获取昨天的所有文章（最常用）
```
请使用 WeChat Article Fetcher 获取昨天所有关注公众号的文章
```

### 场景 2: 获取指定公众号的文章
```
使用 WeChat Article Fetcher 获取"量子位"和"PaperAgent"最近的文章
```

### 场景 3: 按日期范围获取
```
使用 WeChat Article Fetcher 获取 2025-01-15 到 2025-01-20 期间的所有文章
```

### 场景 4: 生成特定主题报告
```
使用 WeChat Article Fetcher 生成一份关于 AI Agent 的最新文章报告
```

### 场景 5: 发现 GitHub 开源项目
```
使用 WeChat Article Fetcher 找出最近介绍的 GitHub 开源项目
```

## 输出格式

生成的报告会保存到 Obsidian vault，格式如下：

### Frontmatter
```yaml
---
title: "YYYY-MM-DD 微信公众号文章汇总"
date: YYYY-MM-DD
tags: [wechat, daily-summary, ai-agent, system, github]
created: YYYY-MM-DDTHH:MM:SSZ
research_focus: [AI Agent, Agent for System, Multi-Agent System]
statistics:
  total_articles: N
  must_read: N
  high_priority: N
  interesting: N
---
```

### 文章分类
- 🔥 **Must Read (9-10分)**: 直接相关核心研究，必读
- 📚 **High Priority (7-8分)**: 高相关度，值得阅读
- 💡 **Interesting (5-6分)**: 有一定参考价值
- ⚠️ **Skipped**: 不相关或低质量

### 每篇文章包含
- **来源**: 公众号名称
- **评分**: 相关性评分 (0-100)
- **核心内容**: 2-3句话总结
- **研究关联**: 与你研究的关联
- **行动项**: Checkbox 任务列表
- **相关链接**: 原文链接、论文链接、代码仓库

## CLI Usage

See `references/cli-usage.md` for complete command reference:
- All parameters and options
- Output formats (Markdown, JSON)
- Integration with automation tools
- Troubleshooting guide

## Ranking System

See `references/ranking-system.md` for:
- 6-tier priority system details
- Score calculation algorithm
- Keyword matching logic
- Custom configuration options

## Examples

See `examples/usage-scenarios.md` for:
- Daily morning routine
- Topic-specific fetching
- GitHub project discovery
- Preview before saving
- Research digest generation
- Custom date range queries
