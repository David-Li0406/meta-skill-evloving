# Action: search-skills-sh

从 skills.sh 搜索相关的 skills。

## 输入

- `state.request_analysis`: 请求分析结果
- `state.user_request`: 用户原始请求

## 处理逻辑

```javascript
// 1. 构建搜索查询
const searchQuery = buildSearchQuery(state.request_analysis);

// 2. 多源搜索
const results = await Promise.all([
  // 方式1: Firecrawl 搜索
  searchWithFirecrawl(`site:skills.sh ${searchQuery}`),

  // 方式2: Web Reader 直接获取
  scrapeWithWebReader(`https://skills.sh/?q=${encodeURIComponent(searchQuery)}`),

  // 方式3: Web Search Prime
  searchWithPrime(`skills.sh ${searchQuery}`)
]);

// 3. 合并和去重
state.search_results = mergeAndDeduplicate(results);
state.execution_status = "searching";
```

## 搜索查询构建

```javascript
function buildSearchQuery(analysis) {
  // 组合关键词 + 意图
  const keywords = analysis.keywords.join(" ");
  const intentMap = {
    "document": "documentation generator",
    "analysis": "code analyzer",
    "management": "task manager",
    "processing": "data processor",
    "creation": "content writer"
  };
  return `${keywords} ${intentMap[analysis.intent] || ""}`.trim();
}
```

## 结果格式

```javascript
{
  name: "skill-name",
  description: "Skill描述",
  url: "https://skills.sh/...",
  source: "firecrawl|web-reader|prime",
  install_command: "npx @claudecode/skills install skill-name"
}
```

## 输出

- `state.search_results`: 搜索结果列表
- `state.execution_status = "searching"`

## 下一步

→ [present-options](04-present-options.md)
