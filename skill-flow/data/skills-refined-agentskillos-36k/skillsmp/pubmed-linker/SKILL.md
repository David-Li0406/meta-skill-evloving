---
name: pubmed-linker
description: This skill should be used when the user asks to "update PubMed links", "check reference links", "find PubMed URLs", "download fulltext papers", or discusses PubMed/Medline literature search and reference management. Provides systematic approach for querying PubMed database and updating reference lists with accurate links.
version: 1.0.0
---

# PubMed 文献链接查询技能

这个技能提供了一套系统化的方法来使用 MCP PubMed 工具查询文献信息并更新参考文献列表的链接。

## 技能概述

当用户需要：
- 查询参考文献的 PubMed 链接
- 更新 `Reference_list.md` 中的文献链接
- 下载论文全文
- 检查文献的开放获取状态

使用此技能来准确调用 MCP PubMed 工具，避免幻觉。

## 可用的 MCP PubMed 工具

### 搜索工具
- `pubmed_search` - 高级搜索，支持布尔逻辑和 MeSH 术语
- `pubmed_quick_search` - 快速搜索，返回精简结果

### 查询工具
- `pubmed_get_details` - 获取完整文献信息（包括 PMID、DOI、全文链接）
- `pubmed_batch_query` - 批量查询多个 PMIDs
- `pubmed_extract_key_info` - 提取关键信息摘要

### 下载工具
- `pubmed_download_fulltext` - 下载指定文献的 PDF 全文
- `pubmed_batch_download` - 批量下载多个文献
- `pubmed_detect_fulltext` - 检测开放获取状态

### 其他工具
- `pubmed_cross_reference` - 查找相关文献（引用/被引用/相似文献）
- `pubmed_cache_info` - 缓存管理
- `pubmed_system_check` - 系统环境检查

## 文献引用格式解析

`Reference_list.md` 中的引用格式为：
```
[序号] 作者. 题目[J]. 期刊名, 年份, 卷(期): 页码.
```

提取关键信息用于 PubMed 搜索：
1. **作者姓氏** - 取第一作者姓氏
2. **关键词** - 从题目中选择 2-3 个核心关键词
3. **期刊名** - 可选，用于精确匹配
4. **发表年份** - 用于过滤结果

## 搜索策略

### 优先级搜索策略

**策略 1：作者 + 题目关键词**
```
作者姓氏 AND 题目关键词1 AND 题目关键词2
```
例如：`Langevin AND Relationship AND Acupuncture`

**策略 2：期刊 + 年份 + 题目关键词**
```
期刊名[ta] AND 年份[dp] AND 题目关键词
```
例如：`Anat Rec[ta] AND 2002[dp] AND acupuncture`

**策略 3：精确题目匹配**
使用完整题目（去除特殊字符）进行搜索

### 搜索结果验证

匹配成功需要满足：
- PMID 存在
- 作者姓名匹配
- 题目高度相似（>80%）
- 发表年份一致
- 期刊名匹配

## 链接格式

### PubMed 链接
```
https://pubmed.ncbi.nlm.nih.gov/{PMID}/
```

### DOI 链接（如果存在）
```
https://doi.org/{DOI}
```

### 全文下载链接
- 如果是开放获取，直接提供 PDF 链接
- 否则标注 "Subscription required"

## 更新文档格式

在原始引用后添加链接信息：

```markdown
[序号] 作者. 题目[J]. 期刊名, 年份, 卷(期): 页码.
- **PMID**: {PMID}
- **PubMed**: https://pubmed.ncbi.nlm.nih.gov/{PMID}/
- **DOI**: https://doi.org/{DOI} (如果存在)
- **Fulltext**: {下载链接或状态}
```

## 批量处理流程

当处理大量文献时：

1. **初始化检查** - 使用 `pubmed_system_check` 验证环境
2. **分组处理** - 每次处理 5-10 篇文献，避免超时
3. **使用批量查询** - 优先使用 `pubmed_batch_query` 提高效率
4. **缓存管理** - 定期使用 `pubmed_cache_info` 查看缓存状态
5. **进度记录** - 维护处理进度，支持断点续传

## 错误处理

### 未找到匹配文献
- 尝试不同的搜索策略
- 检查是否有拼写错误
- 考虑期刊名称缩写变化
- 在文档中标注 `⚠️ 未找到匹配`

### 多个匹配结果
- 选择作者、年份、期刊最匹配的结果
- 如果仍有歧义，标注 `⚠️ 多个匹配，需人工确认`

### 全文无法获取
- 使用 `pubmed_detect_fulltext` 检查开放获取状态
- 尝试查找预印本版本（如 bioRxiv）
- 标注 `🔒 订阅限制`

## 最佳实践

1. **精确性优先** - 使用多个搜索条件交叉验证
2. **保留原始格式** - 不修改原始引用内容
3. **标注不完整** - 对无法确认的信息明确标注
4. **批量操作** - 充分利用批量查询工具
5. **合理超时** - 设置适当的搜索超时时间

## 示例工作流程

```python
# 伪代码示例
for reference in reference_list:
    # 1. 解析引用信息
    info = parse_reference(reference)

    # 2. 执行搜索
    results = pubmed_search(
        query=f"{info.author} AND {info.keywords}",
        max_results=5
    )

    # 3. 验证匹配
    best_match = verify_match(info, results)

    # 4. 获取详细信息
    if best_match:
        details = pubmed_get_details(best_match.pmid)
        # 5. 更新文档
        update_reference(reference, details)
```

## 注意事项

- PubMed 数据库更新有延迟，最新文献可能未收录
- 期刊名称可能使用标准缩写（如 `J. Acupunct. Meridian Stud.`）
- 部分历史文献可能没有 PMID
- 非 PubMed 收录的文献需要手动处理
