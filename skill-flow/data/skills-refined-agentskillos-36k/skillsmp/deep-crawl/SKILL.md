---
name: deep-crawl
description: 大规模文档爬取与处理，用于 API 文档、W3C 规范、大型代码库（>5万行）。
当抓取网站、提取文档、处理大规模文档时使用。
Use when crawling websites, extracting docs, or processing massive documentation.
allowed-tools: "Bash,Grep,Read,Write,mcp__tavily__tavily-crawl,mcp__tavily__tavily-extract,mcp__web_reader__webReader"
---

# Deep Crawl - 深度文档爬取

大规模文档爬取与处理，用于 API 文档、W3C 规范和大型代码库（5万+行）。

## 使用场景

- API 文档提取
- W3C 规范处理
- 大型代码库分析（>5万行）
- 网站结构映射
- 批量文档下载

## 处理方法

### 第一步：提取结构

使用 `sed`/`grep` 提取目录结构，生成 `map.txt`：

```bash
# 提取目录或网站结构
grep -E "^(#{1,3} |<h[1-3])" docs/*.md > structure.txt
```

### 第二步：精准提取

使用 Python 脚本配合 `requests` + `html2text` 精准提取内容。

❌ **避免**：全页 `markdownify`（太慢、太杂）
✅ **使用**：定向内容提取

### 第三步：输出格式

仅展示汇总表格，包含：
- 路径
- 行数 / 文件大小
- 处理耗时

示例：
```
| 路径                | 行数   | 大小  | 耗时  |
|---------------------|--------|-------|-------|
| docs/api/rest.md    | 1,234  | 45KB  | 0.3s  |
| docs/api/graphql.md | 2,567  | 89KB  | 0.5s  |
```

## URL 验证规则

### 严格：严禁未经验证直接给出 URL

1. 使用 `mcp__tavily__tavily-search` 搜索官方文档地址，并验证
2. 仅写入已验证的 URL

### 工具优先级

```
tavily > 直接 URL 访问
```

## PDF 处理规范

```bash
# 优先使用 pdftotext -layout 保留格式
pdftotext -layout document.pdf -

# 文本 >50 字 → 直接分析
# 文本 <=50 字 → 视为扫描件，需要 OCR
```

## 命令参考

```bash
# Tavily 爬取（用于发现）
mcp__tavily__tavily-crawl --url="https://docs.example.com" --max-depth=2

# Tavily 提取
mcp__tavily__tavily-extract --urls=["https://docs.example.com/page1"]

```

## 常见触发场景

使用此技能时，你会听到：
- "抓取这个 API 文档"
- "爬取整个网站"
- "提取文档结构"
- "处理大文档"
- "Crawl this site"
- "Extract documentation"
