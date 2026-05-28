---
name: scholar-workflow
description: 学术论文搜索与验证工作流，使用 OpenAlex、DBLP、CrossRef、arXiv。
当搜索论文、验证 DOI、查询 DBLP、检查发表场所时使用。
Use when searching papers, verifying DOIs, checking publication venues, or validating academic sources.
allowed-tools: "mcp__tavily__tavily-search,Read,Write,Bash"
---

# Scholar Workflow - 学术搜索工作流

学术论文搜索、验证与多源校验，使用 OpenAlex API、DBLP、CrossRef 和 arXiv。

## 核心原则

- **多源验证**：不要只信任单一数据库
- **DOI 校验**：必须验证年份、卷期、页码、作者顺序
- **严格标准**：标题匹配不算验证通过

## 检索链

```
OpenAlex (API) -> DBLP -> CrossRef -> arXiv -> 作者主页
```

## 校验规则

### 已发表论文

必须**同时满足**：
- DBLP 记录存在
- OpenAlex DOI 匹配

### 预印本/在审论文

检索 `github.io` 路径模式：
```
/assets/pubs/
/publications/
/paper/
```

## DOI 深度解析

必须校验：
- 年份
- 卷期
- 页码
- 作者排序

### 文件命名模式识别

```
hivetee-tifs26.pdf → 投稿 TIFS 2026
ccai-micro25.pdf   → 投稿 MICRO 2025
```

## 硬性要求

- ❌ **严禁**仅根据单一数据库判定论文"不存在"
- ❌ **严禁**标题对上就认为验证通过
- ✅ **必须**验证 DOI/卷期/作者
- ✅ **必须**交叉检查多个来源

## API 使用示例

### DBLP 安全解析

```python
# ❌ 错误：空结果时 KeyError
hits = d['result']['hits']['hit']

# ✅ 正确：先检查 @total
total = d['result']['hits'].get('@total', '0')
hits = d['result']['hits'].get('hit', []) if total != '0' else []
```

### OpenAlex 精确搜索

```bash
# ❌ 太宽泛：38289 条不相关结果
curl "api.openalex.org/works?search=ccAI"

# ✅ filter 参数精确匹配
curl "api.openalex.org/works?filter=title.search:Compatible%20and%20Confidential"
```

## 常见触发场景

使用此技能时，你会听到：
- "搜索这篇论文"
- "验证这个 DOI"
- "查一下这篇论文发表在哪里"
- "这篇论文是真的吗？"
- "Check DBLP for..."
- "verify publication venue"
