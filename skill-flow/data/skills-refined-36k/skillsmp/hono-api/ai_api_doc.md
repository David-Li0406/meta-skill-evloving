## 知网、维普降重和降AI率，第三方接口接入文档

###  请求域名

从环境变量 `c.env.REDUCEAI_API_URL` 和 `c.env.CHEEYUAN_API_URL` 获取，`c.env.REDUCEAI_API_URL` 为维普降AI率和（知网、维普）降重的请求域名，`c.env.CHEEYUAN_API_URL` 为知网降AI率的请求域名。

### 访问TOKEN获取方式的代码示例

```ts
testRpc.post('/kv-token', async (c) => {
  return c.json(createSuccessResponse({
    cheeyuanToken: (c.var as Variables).cheeyuanToken,
    reduceAiToken: (c.var as Variables).reduceAiToken,
  }, '获取第三方Token成功'))
})
```

### REDUCEAI接入指南

> 用于维普、知网降重，维普降AI率

#### REDUCEAI 提交降重或降AI率的任务接口

baseUrl: `c.env.REDUCEAI_API_URL`
POST /ai/reduce
header:
"authorization"：Bearer {reduceAiToken}，其中{reduceAiToken}从环境变量 `c.var.reduceAiToken` 获取。
ContentType: application/json

入参：
"text": "测试测试测试测试测试测试”（待处理文本，单次处理最多 3000 字）
"toolName": "onlyjc"（模型传的是不同的值，用【仅降AI(全平台版)】传"onlyai"，用【仅降重(全平台版)】传"onlyjc"）

出参：
{
  "taskId": "onlyjc_98631379_1758017276712",
  "newBalance": 462
}

#### REDUCEAI 任务结果获取接口

baseUrl: `c.env.REDUCEAI_API_URL`
POST: /result/:taskId
header:
"authorization"：Bearer {reduceAiToken}，其中{reduceAiToken}从环境变量 `c.var.reduceAiToken` 获取。
ContentType: application/json

出参：
{
    "userId": 98625456,
    "toolName": "onlyai",
    "status": "completed",
    "progress": 39,
    "totalSentences": 1,
    "processedSentences": 0,
    "result": "12231",
    "queuePosition": 0,
    "cost": 5
}
OR
{"result":"测试验证检测试验考察检验"}

### CHEEYUAN接入指南

> 用于知网降AI率

#### CHEEYUAN 提交降AI率的任务接口

baseUrl: `c.env.CHEEYUAN_API_URL`
POST /tools/freechangeword/async
header:
"authorization"：Bearer {reduceAiToken}，其中{reduceAiToken}从环境变量 `c.var.reduceAiToken` 获取。
ContentType: application/json

入参：
"content": "需要改写的原始文本内容", 待处理文本，单次处理最多 3000 字）。
"product_type": 78 （78代表知网降AI率，固定值）

出参：
{
    "code": 1,
    "message": "正在生成中,切勿重复提交，后续生成在使用明细，请耐心等待",
    "data": 123456 这个是返回的任务id
}

#### CHEEYUAN 查询改写结果接口

baseUrl: `c.env.CHEEYUAN_API_URL`
POST /tools/common/status
header:
"authorization"：Bearer {reduceAiToken}，其中{reduceAiToken}从环境变量 `c.var.reduceAiToken` 获取。
ContentType: application/json

入参：
"id": 123456 （提交任务接口返回的任务ID）

出参：
{
    "code": 1,
    "message": "success",
    "data": {
        "id": 1550425,
        "api_type": 1,
        "user_id": 28,
        "size": 24,
        "desc": "Vue3 \u662f\u4e00\u4e2a\u524d\u7aef\u6846\u67b6\uff0c\u7528\u6765\u5f00\u53d1web",
        "origintxt": "Vue3 \u662f\u4e00\u4e2a\u524d\u7aef\u6846\u67b6\uff0c\u7528\u6765\u5f00\u53d1web \u5e94\u7528\u3002",
        "txt": "Vue 3\u662f\u4e00\u6b3e\u9886\u5148\u7684\u524d\u7aef\u5f00\u53d1\u6846\u67b6\uff0c\u4e3b\u8981\u5e94\u7528\u4e8eWeb\u5e94\u7528\u5e73\u53f0\u7684\u5f00\u53d1\u4e0e\u5b9e\u65bd\u3002",
        "deleted_at": null,
        "created_at": "2025-11-03 14:04:04",
        "updated_at": "2025-11-03 14:04:16",
        "pay_status": 1,
        "deal_status": 1,
        "money": "0.048",
        "standard": "2.000\u5143\/\u5343\u5b57",
        "product_type": 1,
        "resulttext": "Vue 3\u662f\u4e00\u6b3e\u9886\u5148\u7684\u524d\u7aef\u5f00\u53d1\u6846\u67b6\uff0c\u4e3b\u8981\u5e94\u7528\u4e8eWeb\u5e94\u7528\u5e73\u53f0\u7684\u5f00\u53d1\u4e0e\u5b9e\u65bd\u3002",
        "lock_content": "",
        "log_txt": null,
        "wenxian": null,
        "result_type": "text",
        "result_key": "",
        "product_type_text": "\u964d\u91cd\u590d\u7387"
    }
}

说明：resulttext没有数据表明接口正在处理，有数据则为处理完成，可以获取改写后的文本内容，前端可以 3 秒轮询查询。
改写后的文本内容在data.resulttext字段中。
