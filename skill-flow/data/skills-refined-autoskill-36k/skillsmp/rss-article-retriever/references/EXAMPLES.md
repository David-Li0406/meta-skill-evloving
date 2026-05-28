# Input/Output Examples

This document provides examples of user inputs and corresponding skill outputs.

## Operation Mode Examples

### Example 1: List Recent Articles

**User Input:**
```
获取最近3篇文章列表
```

**Skill Output:**
```json
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "list",
  "result": {
    "type": "summary",
    "total_count": 3,
    "articles": [
      {
        "id": "sgid_1234567890",
        "title": "民间借贷中，仅有转账凭证能认定借款关系吗？",
        "author": "法律小贴士",
        "published_at": "2026-01-20T08:30:00Z",
        "url": "https://mp.weixin.qq.com/s/sgid_1234567890",
        "summary": "在民间借贷纠纷中，出借人仅凭借转账凭证起诉要求借款人还款..."
      },
      {
        "id": "sgid_9876543210",
        "title": "劳动合同期满未续签，公司需要支付经济补偿吗？",
        "author": "职场法律指南",
        "published_at": "2026-01-19T14:15:00Z",
        "url": "https://mp.weixin.qq.com/s/sgid_9876543210",
        "summary": "劳动合同期满后，用人单位未与劳动者续签书面劳动合同..."
      },
      {
        "id": "sgid_1122334455",
        "title": "购买二手房需要注意的法律风险",
        "author": "房产法律顾问",
        "published_at": "2026-01-19T09:00:00Z",
        "url": "https://mp.weixin.qq.com/s/sgid_1122334455",
        "summary": "购买二手房是许多人的选择，但其中潜藏的法律风险不容忽视..."
      }
    ],
    "query": {
      "limit": 3,
      "page": 1,
      "title_include": null,
      "title_exclude": null
    }
  }
}
</skill-output>
```

---

### Example 2: Search by Keyword

**User Input:**
```
找一篇关于"离婚"的文章
```

**Skill Output:**
```json
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "search",
  "result": {
    "type": "summary",
    "total_count": 2,
    "articles": [
      {
        "id": "sgid_5566778899",
        "title": "离婚时，婚前购买的房产如何分割？",
        "author": "婚姻家庭法律",
        "published_at": "2026-01-18T16:45:00Z",
        "url": "https://mp.weixin.qq.com/s/sgid_5566778899",
        "summary": "离婚案件中，房产分割往往是争议的焦点。对于婚前购买的房产..."
      },
      {
        "id": "sgid_6677889900",
        "title": "离婚协议书怎么写？这份模板请收好",
        "author": "法律文书模板",
        "published_at": "2026-01-15T10:20:00Z",
        "url": "https://mp.weixin.qq.com/s/sgid_6677889900",
        "summary": "离婚协议书是夫妻双方自愿离婚的书面文件，需要包含以下内容..."
      }
    ],
    "query": {
      "limit": 10,
      "page": 1,
      "title_include": "离婚",
      "title_exclude": null
    }
  }
}
</skill-output>
```

---

### Example 3: Get Full Content (Legal Article)

**User Input:**
```
获取最新一篇文章的完整内容
```

**Skill Output:**
```json
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "get",
  "result": {
    "type": "full",
    "article": {
      "id": "sgid_1234567890",
      "title": "民间借贷中，仅有转账凭证能认定借款关系吗？",
      "author": "法律小贴士",
      "published_at": "2026-01-20T08:30:00Z",
      "url": "https://mp.weixin.qq.com/s/sgid_1234567890",
      "content": {
        "plain_text": "案情简介\n\n张某与李某系朋友关系。2022年3月，张某通过银行转账向李某支付人民币50万元。双方未签订书面借款合同，也未约定利息。\n\n2023年1月，张某要求李某还款，李某拒绝。张某遂诉至法院，要求李某偿还借款50万元及利息。\n\n李某辩称，该款项系张某支付的投资款，而非借款，并提供了一份微信群聊天记录作为证据。\n\n法院审理\n\n法院经审理认为，本案的争议焦点在于：张某向李某转账的50万元是借款还是投资款。\n\n根据《最高人民法院关于审理民间借贷案件适用法律若干问题的规定》第十六条规定，原告仅依据金融机构的转账凭证提起民间借贷诉讼，被告抗辩转账系偿还双方之前借款或者其他债务的，被告应当对其主张提供证据证明。\n\n本案中，张某提供了转账凭证，初步证明了款项交付的事实。李某主张该款项为投资款，应当提供相应证据。李某提供的微信群聊天记录仅显示双方曾讨论过投资项目，但并未明确约定该50万元为投资款，也未证明双方存在投资关系。\n\n法院判决\n\n判决被告李某于判决生效后十日内偿还原告张某借款本金50万元及利息（利息以50万元为基数，自2023年1月1日起至实际付清之日止，按照全国银行间同业拆借中心公布的一年期贷款市场报价利率计算）。\n\n法官说法\n\n在日常生活中，朋友之间借钱往往碍于情面，不签订书面借款合同，仅通过微信、支付宝、银行转账等方式进行。一旦发生纠纷，举证责任将直接影响案件的判决结果。\n\n对于出借人而言：借款时最好签订书面借款合同，明确约定借款金额、利息、还款期限等事项。如果不能签订书面合同，至少要保留好转账凭证，并通过微信、短信等方式确认借款事实。\n\n对于借款人而言：如果收到的款项不是借款，应当明确款项性质，并保留相关证据，以免产生不必要的纠纷。",
        "sections": [
          {
            "heading": "案情简介",
            "text": "张某与李某系朋友关系。2022年3月，张某通过银行转账向李某支付人民币50万元。双方未签订书面借款合同，也未约定利息。2023年1月，张某要求李某还款，李某拒绝。张某遂诉至法院，要求李某偿还借款50万元及利息。李某辩称，该款项系张某支付的投资款，而非借款，并提供了一份微信群聊天记录作为证据。"
          },
          {
            "heading": "法院审理",
            "text": "法院经审理认为，本案的争议焦点在于：张某向李某转账的50万元是借款还是投资款。根据《最高人民法院关于审理民间借贷案件适用法律若干问题的规定》第十六条规定，原告仅依据金融机构的转账凭证提起民间借贷诉讼，被告抗辩转账系偿还双方之前借款或者其他债务的，被告应当对其主张提供证据证明。本案中，张某提供了转账凭证，初步证明了款项交付的事实。李某主张该款项为投资款，应当提供相应证据。李某提供的微信群聊天记录仅显示双方曾讨论过投资项目，但并未明确约定该50万元为投资款，也未证明双方存在投资关系。"
          },
          {
            "heading": "法院判决",
            "text": "判决被告李某于判决生效后十日内偿还原告张某借款本金50万元及利息（利息以50万元为基数，自2023年1月1日起至实际付清之日止，按照全国银行间同业拆借中心公布的一年期贷款市场报价利率计算）。"
          },
          {
            "heading": "法官说法",
            "text": "在日常生活中，朋友之间借钱往往碍于情面，不签订书面借款合同，仅通过微信、支付宝、银行转账等方式进行。一旦发生纠纷，举证责任将直接影响案件的判决结果。对于出借人而言：借款时最好签订书面借款合同，明确约定借款金额、利息、还款期限等事项。如果不能签订书面合同，至少要保留好转账凭证，并通过微信、短信等方式确认借款事实。对于借款人而言：如果收到的款项不是借款，应当明确款项性质，并保留相关证据，以免产生不必要的纠纷。"
          }
        ],
        "source": "playwright"
      },
      "word_count": 1156,
      "cleaning_notes": [
        "Removed author profile",
        "Removed QR codes",
        "Removed subscription prompt",
        "Removed share buttons"
      ]
    }
  }
}
</skill-output>
```

---

### Example 4: Error Response (RSS Connection Failed)

**User Input:**
```
获取最近5篇文章
```

**Skill Output:**
```json
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "list",
  "error": {
    "code": "RSS_CONNECTION_ERROR",
    "message": "Cannot connect to RSS service at localhost:4000",
    "suggestion": "Ensure WeWe-RSS service is running on http://localhost:4000"
  }
}
</skill-output>
```

---

### Example 5: Fallback to RSS Summary (Playwright Timeout)

**User Input:**
```
获取完整内容
```

**Skill Output:**
```json
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "get",
  "result": {
    "type": "full",
    "article": {
      "id": "sgid_1234567890",
      "title": "民间借贷中，仅有转账凭证能认定借款关系吗？",
      "author": "法律小贴士",
      "published_at": "2026-01-20T08:30:00Z",
      "url": "https://mp.weixin.qq.com/s/sgid_1234567890",
      "content": {
        "plain_text": "在民间借贷纠纷中，出借人仅凭借转账凭证起诉要求借款人还款，借款人主张该款项系其他债务时，应当由借款人承担举证责任...",
        "sections": [],
        "source": "rss_fallback"
      },
      "word_count": 85,
      "cleaning_notes": [
        "Playwright timeout - using RSS summary as fallback"
      ]
    }
  }
}
</skill-output>
```

---

## Integration Example: Chain with video-script-generator

**User Input:**
```
请用最新一篇关于"民间借贷"的文章来制作视频脚本
```

**Step 1 - rss-article-retriever Output:**
```json
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "search",
  "result": {
    "type": "summary",
    "total_count": 1,
    "articles": [
      {
        "id": "sgid_1234567890",
        "title": "民间借贷中，仅有转账凭证能认定借款关系吗？",
        "url": "https://mp.weixin.qq.com/s/sgid_1234567890",
        "summary": "..."
      }
    ]
  }
}
</skill-output>
```

**Step 2 - rss-article-retriever Full Content:**
```json
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "get",
  "result": {
    "type": "full",
    "article": {
      "content": {
        "plain_text": "案情简介\n\n张某与李某系朋友关系..."
      }
    }
  }
}
</skill-output>
```

**Step 3 - video-script-generator Output:**
```json
<skill-output type="video-script" schema-version="1.0.0">
{
  "style_profile": {...},
  "system_instruction": "...",
  "templates": {...}
}
</skill-output>
```

---

## Test API Calls

### Raw RSS API Test
```bash
# Test basic connectivity
curl "http://localhost:4000/feeds/all.atom?limit=1"

# Test search functionality
curl "http://localhost:4000/feeds/all.atom?title_include=民间借贷&limit=5"

# Test pagination
curl "http://localhost:4000/feeds/all.atom?limit=10&page=2"
```

### Expected XML Response Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>WeWe-RSS</title>
  <entry>
    <id>sgid_1234567890</id>
    <title>文章标题</title>
    <author>
      <name>公众号名称</name>
    </author>
    <published>2026-01-20T08:30:00Z</published>
    <link href="https://mp.weixin.qq.com/s/sgid_1234567890"/>
    <summary>文章摘要...</summary>
  </entry>
</feed>
```
