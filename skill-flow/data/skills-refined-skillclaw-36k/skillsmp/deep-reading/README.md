# Deep Reading Skill

基于 Mortimer Adler《如何阅读一本书》的系统性阅读助手。

## 功能

支持三种阅读层次：

| 层次 | 用途 | 时间 | 输出 |
|------|------|------|------|
| **检视阅读** | 快速了解结构，决定是否深入 | 5-15分钟 | 结构分析、关键点、摘要 |
| **分析阅读** | 深度理解，掌握内容 | 30-60分钟 | 完整分析、Q&A、评价 |
| **对比阅读** | 综合多个来源 | 45-90分钟 | 主题对比、综合分析 |

## 使用方法

### 基础用法

```
# 检视阅读（默认）
"请阅读这个链接：https://example.com/article.pdf"
"帮我快速了解这本书的内容"

# 分析阅读
"请分析这篇论文：./papers/ai-safety.pdf"
"深入阅读这篇文章并给我详细分析"

# 对比阅读
"对比这两篇文章的观点"
"比较这三个文档对同一问题的看法"
```

### 输入支持

- **URL**: 任何 HTTP/HTTPS 链接（包括 PDF）
- **YouTube 视频**: 自动下载字幕进行分析
- **本地 PDF**: 文件路径
- **已存笔记**: 继续之前的阅读分析

### YouTube 视频分析

```
"请分析这个 YouTube 视频：https://youtube.com/watch?v=xxx"
"帮我快速了解这个视频讲了什么"
```

**前置要求**:
```bash
# 安装 yt-dlp
brew install yt-dlp
```

技能会自动：
1. 下载视频字幕（支持手动和自动生成）
2. 清理格式（去除时间戳等）
3. 应用三种阅读层次进行分析
4. 保存转录文本到 `notes/transcripts/`

### 输出格式

每种阅读层次都会生成：
1. **Markdown 报告**: 结构化的分析文档
2. **Q&A 格式**: 关键问题与答案
3. **思考题**: 测试理解深度的问题

### 阅读笔记归档

所有阅读笔记自动保存到 `~/.claude/skills/deep-reading/notes/`

```bash
# 查看所有笔记
~/.claude/skills/deep-reading/reading-notes.sh list

# 搜索笔记
~/.claude/skills/deep-reading/reading-notes.sh search "关键词"

# 查看特定笔记
~/.claude/skills/deep-reading/reading-notes.sh show <doc-id>
```

### 渐进式深度阅读

技能支持在同一文档上逐步加深理解：

```
"继续深入分析这篇文章"  # 从检视阅读 → 分析阅读
"用之前的分析对比这篇新文章"  # 加入对比阅读
```

## 技能文件结构

```
~/.claude/skills/deep-reading/
├── SKILL.md                    # 主技能文档
├── README.md                   # 使用说明（本文件）
├── reading-notes.sh            # 笔记管理脚本
├── fetch-youtube-transcript.sh # YouTube 字幕下载脚本
└── notes/
    ├── index.md                # 主索引
    ├── transcripts/            # YouTube 字幕存档
    └── themes/                 # 对比阅读笔记
```

## 检视阅读输出示例

```markdown
# Inspectional Reading Report: Article Title

## Document Metadata
- **Source:** https://example.com/article.pdf
- **Date Read:** 2026-01-20
- **Document Type:** Academic Paper

## Structural Overview
- **Main Category:** Theoretical - Computer Science
- **Key Question:** How do LLMs handle multi-step reasoning?
- **Thesis Statement:** LLMs struggle with complex reasoning without external tools

## Quick Summary
This paper examines the limitations of current language models...
```

## 分析阅读输出示例

```markdown
# Analytical Reading Report: Book Title

## Classification
- **Genre/Category:** Philosophy of Science
- **Subject Domain:** Epistemology

## The Core Unity
**Main Question:** What constitutes scientific knowledge?

**Thesis Statement:** Scientific knowledge is provisional and falsifiable

## Propositions & Arguments
### Proposition 1: Scientific theories must be falsifiable
- **Argument:** Popper's criterion of demarcation
- **Evidence:** Historical cases of theory rejection
```

## 对比阅读输出示例

```markdown
# Comparative Reading Report: AI Safety

## Documents Analyzed
1. **Paper A** - Focus on alignment problem
2. **Paper B** - Focus on interpretability
3. **Paper C** - Focus on robustness

## Points of Agreement
- All agree current methods are insufficient for AGI
- All recommend interdisciplinary approaches

## Points of Disagreement
- **Priority:** Alignment vs Interpretability
- **Root:** Different assumptions about AGI timeline
```

## 技巧提示

1. **明确你的目标**: 想快速浏览还是深度理解？
2. **利用渐进阅读**: 先检视判断价值，再决定是否深入
3. **对比才有洞察**: 阅读多篇同一主题文章可获得更深入理解
4. **主动提问**: 告诉 AI 你特别关心哪些方面
