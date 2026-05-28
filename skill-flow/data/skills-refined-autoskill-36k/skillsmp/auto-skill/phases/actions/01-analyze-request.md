# Action: analyze-request

分析用户请求，提取关键词和意图。

## 输入

- `state.user_request`: 用户原始请求文本

## 处理逻辑

```javascript
// 1. 提取关键词
const keywords = extractKeywords(state.user_request);

// 2. 意图分类
const intent = classifyIntent(state.user_request);
// - "document": 文档生成、编辑
// - "analysis": 代码分析、数据分析
// - "management": 任务、issue管理
// - "processing": 数据处理、转换
// - "creation": 内容创作、翻译
// - "general": 通用需求

// 3. 更新状态
state.request_analysis = {
  keywords: keywords,
  intent: intent,
  confidence: 0.8
};
state.execution_status = "analyzing";
```

## 关键词提取示例

| 用户输入 | 提取的关键词 | 意图 |
|---------|-------------|-----|
| "帮我分析这个Excel" | [excel, 分析, 数据] | analysis |
| "生成一份API文档" | [api, 文档, 生成] | document |
| "翻译这段文本" | [翻译, 文本] | creation |

## 输出

- 更新 `state.request_analysis`
- `state.execution_status = "analyzing"`

## 下一步

→ [match-local-skills](02-match-local-skills.md)
