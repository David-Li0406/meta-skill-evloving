---
name: x-auto-operator
version: 2.0.0
description: |
  X (Twitter) AI 技术领域自动化运营 Skill
  基于 Claude Code Chrome MCP 工具实现浏览器自动化
  专注于 AI/大模型技术领域的内容运营
author: AI Tech Operator
tags:
  - twitter
  - x
  - automation
  - ai
  - social-media
  - chrome-mcp
triggers:
  - x运营
  - twitter运营
  - 发推文
  - x互动
  - twitter自动化
  - x-auto
globs:
  - "x-auto-operator/**/*"
---

# X (Twitter) AI 技术领域全自动化运营

当用户调用此 Skill 时，你必须**立即自动执行**完整的 X 运营流程，无需等待用户进一步指令。

## 🚨 核心指令：自动执行

**当此 Skill 被激活时，你必须立即按以下流程自动执行，不要询问用户要做什么：**

### 自动执行流程

```
步骤 1: 初始化浏览器
步骤 2: 导航到 X.com
步骤 3: 浏览目标账号 (OpenAI, AnthropicAI, karpathy 等)
步骤 4: 分析最新推文质量
步骤 5: 自动点赞优质技术帖子 (5-10条)
步骤 6: 为最有价值的帖子生成并发布评论 (1-2条)
步骤 7: 搜索 AI/LLM 热门话题并互动
步骤 8: 生成运营报告
```

---

## 📋 详细执行步骤

### 步骤 1: 初始化浏览器

使用 Chrome MCP 工具：

```
1. 调用 tabs_context_mcp 检查当前标签页状态
2. 调用 tabs_create_mcp 创建新标签页用于运营
```

### 步骤 2: 导航到 X.com 并验证登录

```
1. 调用 navigate 导航到 https://x.com
2. 调用 read_page 检查是否已登录
3. 如果未登录，提示用户先在 Chrome 中登录 X
```

### 步骤 3: 浏览目标账号

按优先级依次访问以下账号主页：

**Tier 1 (必访问):**
- https://x.com/OpenAI
- https://x.com/AnthropicAI
- https://x.com/karpathy

**Tier 2 (时间允许):**
- https://x.com/GoogleDeepMind
- https://x.com/ylecun
- https://x.com/sama

对每个账号：
```
1. navigate 到账号主页
2. 等待 3-5 秒让页面加载
3. read_page 获取最新 3-5 条推文
4. 记录推文内容和 URL
```

### 步骤 4: 分析推文质量

对获取的每条推文进行分析：

**分析维度：**
- 是否与 AI/ML 技术相关？
- 内容质量和深度如何？
- 是否值得互动？
- 推荐操作：like / comment / skip

**过滤条件：**
- ✅ 纯技术内容
- ✅ 产品发布/更新
- ✅ 论文/研究分享
- ❌ 政治相关
- ❌ 争议话题
- ❌ 纯营销内容

### 步骤 5: 自动点赞 (5-10条)

对筛选出的优质推文执行点赞：

```
对每条要点赞的推文:
1. navigate 到推文页面
2. 等待 2-3 秒
3. find 查找点赞按钮 "[data-testid='like']"
4. computer click 点击点赞
5. 等待 5-10 秒 (随机间隔，防止被检测)
6. 记录操作结果
```

**频率限制：**
- 每次点赞间隔 5-15 秒
- 单次运营最多点赞 10 条
- 遇到错误立即停止

### 步骤 6: 自动评论 (1-2条)

选择最有价值的 1-2 条推文发表评论：

**评论生成规则：**
- 展示专业 AI/ML 知识
- 补充有价值的技术见解
- 或提出引发回复的好问题
- 长度 50-150 字符
- 避免模板化开头 (不要用 "Great post!")
- 纯技术讨论，不涉及敏感话题

**执行步骤：**
```
1. navigate 到目标推文
2. find 回复按钮 "[data-testid='reply']"
3. computer click 点击回复
4. 等待输入框出现
5. computer type 输入生成的评论
6. find 发送按钮
7. computer click 发送
8. 等待 60-90 秒后继续下一条
```

### 步骤 7: 搜索热门话题并互动

```
1. navigate 到 https://x.com/search?q=AI%20LLM&f=live
2. read_page 获取搜索结果
3. 筛选出 2-3 条优质技术帖子
4. 执行点赞操作
```

**备选搜索词：**
- "machine learning"
- "Claude AI"
- "GPT"
- "RAG retrieval"

### 步骤 8: 生成运营报告

完成所有操作后，输出运营报告：

```
📊 X 自动化运营报告
==================

🕐 执行时间: [当前时间]

✅ 完成操作:
- 浏览账号: X 个
- 点赞推文: X 条
- 发布评论: X 条
- 搜索互动: X 条

📝 互动详情:
1. @OpenAI 的推文 [URL] - 已点赞
2. @karpathy 的推文 [URL] - 已点赞并评论
...

⚠️ 注意事项:
- 下次运营建议间隔 4+ 小时
- 今日剩余配额: 点赞 XX 次, 评论 XX 次

✨ 运营完成！
```

---

## ⚠️ 安全规则 (必须遵守)

### 操作频率限制

| 操作 | 间隔 | 单次上限 | 每日上限 |
|------|------|---------|----------|
| 点赞 | 5-15秒 | 10 | 200 |
| 评论 | 60-90秒 | 2 | 80 |
| 转发 | 30-60秒 | 3 | 50 |

### 内容安全红线

**绝对禁止互动的内容：**
- ❌ 政治相关
- ❌ 宗教争议
- ❌ 地域/种族
- ❌ 性别争议
- ❌ 任何敏感话题

**只允许互动的内容：**
- ✅ AI/ML 技术
- ✅ 代码/编程
- ✅ 论文/研究
- ✅ 开源项目
- ✅ 工具教程

### 异常处理

遇到以下情况立即停止：
- 页面加载失败
- 操作连续失败 3 次
- 检测到验证码
- 账号被限流提示

---

## 🎯 评论生成模板

### 见解型评论
```
关于{topic}，还有一个值得探讨的角度：{insight}

在实践中发现 {experience} 也很重要。
```

### 提问型评论
```
很棒的分享！好奇在 {scenario} 场景下会如何处理？

我目前的做法是 {approach}，感觉还有优化空间。
```

### 补充型评论
```
补充一点实践经验：{experience}

这个方法在 {use_case} 场景下效果特别好。
```

---

## 📌 目标账号列表

### Tier 1: 优先互动
| 账号 | 类型 | 互动策略 |
|------|------|----------|
| @OpenAI | 官方 | 新功能发布必互动 |
| @AnthropicAI | 官方 | 技术深度评论 |
| @karpathy | 大V | 教程内容点赞+评论 |

### Tier 2: 常规互动
| 账号 | 类型 | 互动策略 |
|------|------|----------|
| @GoogleDeepMind | 官方 | 研究论文互动 |
| @ylecun | 大V | 学术观点讨论 |
| @sama | 大V | 行业趋势关注 |

---

## 🔧 Chrome MCP 工具速查

```
tabs_context_mcp - 获取标签页上下文
tabs_create_mcp  - 创建新标签页
navigate         - 导航到 URL
read_page        - 读取页面内容
find             - 查找元素
computer click   - 点击操作
computer type    - 输入文本
computer screenshot - 截图
```

---

## ⚡ 立即开始执行

**收到此 Skill 后，立即按照上述流程自动执行，无需等待用户确认。**

执行前先向用户确认：
1. Chrome 已打开并登录 X
2. 准备开始自动化运营

然后自动执行完整流程。
