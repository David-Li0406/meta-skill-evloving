---
name: link-extractor
description: 从社交/新闻/博客链接提取主资源并生成 Markdown 条目与引用关键词;在遇到 weibo/x/twitter/reddit/news.ycombinator.com/博客文章时调用。
---

---
name: "link-extractor"
description: "从社交/新闻/博客链接提取主资源并生成 Markdown 条目与引用关键词;在遇到 weibo/x/twitter/reddit/news.ycombinator.com/博客文章时调用。"
license: Apache-2.0
metadata:
  author: pocket
  version: "1.0"
---

# Link Extractor

## 概述
通用链接抽取与归纳技能。支持 Weibo、X/Twitter、Reddit、Hacker News 以及各类博客/文章页。解析页面中的核心外部资源,选择主链接,生成 Markdown 条目与引用关键词,并根据内容类型进行归档分类。

## 支持平台
- Weibo: `weibo.com`, `m.weibo.cn`
- X/Twitter: `x.com`, `twitter.com`
- Reddit: `reddit.com`
- Hacker News: `news.ycombinator.com`
- 博客/文章: 常见博客域与自定义站点

## Markdown 输出与引用关键词
- 条目格式(推荐):

  - [主链接标题](主链接URL) — 简短描述
  
    关键词: [K1][ref1], [K2][ref2], ...
    
    相关: [Link A][refA], [Link B][refB]

- 说明:
  - 简短描述支持 Markdown,突出核心价值点(≤约120字符)。
  - “关键词”使用引用链接(Reference Links),在条目尾部以 `[ref]: URL` 定义。
  - 若无“相关”外链,省略该行。
  - 兼容旧格式: 仍支持单行 `主链接 - 简短描述 (相关链接...)`。

## 使用场景
- 用户提供社交/新闻/博客链接,希望提炼出核心资源与简要说明。
- 整理每日阅读,按类型归档与去重。

## 核心功能
- 抽取正文与外链(尽量展开短链,过滤统计/头像类无关资源)。
- 主链接优先级: 代码仓库 > 官方文档/项目主页 > 产品/工具页 > 明确标题的技术文章 > 文案强调链接。
- 生成 1 句客观描述;关键词以引用链接呈现;相关链接按出现顺序去重。

## 流程与决策
1. 识别来源域名 → 抽取正文+全部外链。
2. 依据优先级选择主链接(多仓库取正文中最靠前)。
3. 压缩生成简短描述(类型+核心价值),支持 Markdown。
4. 组装 Markdown 条目;引用链接在条目尾部定义。
5. 写入 Daily 归档并按类型分类;多条输入逐条输出独立行。

## Daily 归档(六大板块)
- 路径: `docs/daily-links/YYYY-MM-DD.md`
- 结构:
  - `# Daily Links YYYY-MM-DD`
  - `## 🪶 Remember This:` — 1–3 条精炼箴言/原则(斜体可选)
  - `## 🤓 Fav Finds` — 当日最值得收藏的链接(概念式两行或图标单行)
  - `## 📘 Read This` — 博客/长文/官方文章(概念式两行/要点式摘要/官方博客样式)
  - `## 🛠️ Tools` — 产品/服务/CLI(图标单行或概念式两行)
  - `## 🔧 Try This` — 可实践的教程/实验/方法(概念式两行或要点式)
  - `## 🎧 Listen To` — 播客/音频内容(概念式两行)
- 分类映射:
  - 文章/官方博客 → 📘 Read This
  - 工具/产品/代码仓库 → 🛠️ Tools
  - 方法论/思考贴 → 🤓 Fav Finds 或 🪶 Remember This(若为通用原则)
  - 教程/实验 → 🔧 Try This
  - 播客/音频 → 🎧 Listen To
- 写入策略:
  - 同一 URL 当日仅记录一次;重复出现时更新“来源/概要/要点”。
  - 样式选择以“清晰、简洁、可决策”为目标(两行概念/要点式/官方博客/图标单行)。

### 语言规则
- 分类标题可使用英文; 其余正文、概要与说明优先使用中文。
- 难以准确翻译的专业术语保留英文或中英混排(如 Agent harness、Plan 模式、grep)。

## 示例
- 概念(博客/文章):
  - [Remote Onboarding Program](https://medium.com/levelshealth/a-deep-dive-into-levels-month-long-onboarding-program-e0c4144d9c27) shared by [Kevin Galang](https://trends.vc)
  - How to build a deliberate remote first onboarding system

- 概念(工具/指南):
  - [Agent Best Practices](https://cursor.com/cn/blog/agent-best-practices) — 来自 Cursor 团队
  - Official guide for agent-based coding: long-run, multi-file refactors, test-driven iteration

- 概念(Weibo/方法论):
  - [MCP → SKILL 扩展机制](https://weibo.com/1648815335/Qn8iCfNyt) shared by [Weibo](https://weibo.com/1648815335/Qn8iCfNyt)
  - Split concerns: MCP standardizes connection, SKILL orchestrates workflow and externalizes state

## 归档样式扩展: 要点式摘要
- 适用: 文章/长文档,需快速判断是否值得深入阅读。
- 格式:
  - 第一行(加粗): **一句话主题/结论**
  - 随后 3–5 个要点条目,每条可含加粗的关键词。
- 示例:
  - [Increasing Your Luck Surface Area](https://www.codusoperandi.com/posts/increasing-your-luck-surface-area)
  
    **You can make your own luck** through a powerful principle of passion and communication.
  
    - **Pour energy into your passion**: when you're excited about something, you naturally pull others into your orbit
    - **Tell more people**: people will capture that value in ways you'd never predict — hiring you, partnering with you or investing in you
    - **Luck is ‘doing’ multiplied by ‘telling’**: the more you do and the more people you tell about it, the larger your Luck Surface Area becomes

## 归档样式扩展: 官方博客
- 适用: 官方团队发布的博客/公告,标题已能清晰传达主题。
- 规则:
  - 若标题足够清晰,仅保留“博客标题”一行;否则追加“明细说明”一句话概要。
- 格式:
  - [**博客标题**](原始URL) — 来自 [官方团队名]
  - 明细说明: 一句话概要(可选)
- 示例:
  - [**Agent Best Practices**](https://cursor.com/cn/blog/agent-best-practices) — 来自 Cursor 团队
  - 明细说明: 若标题不够清晰,补充简要说明;若已清晰,可省略。

### 官方团队名自动识别
- 判定“官方”: 主域与产品域一致,或存在 `blog.` 子域的官方站点;或已知官方域名映射。
- 提取优先级:
  1. JSON-LD `Organization.name`/`WebSite.name`
  2. `og:site_name`
  3. 页头品牌区域的可见名称或 logo 的 `alt`/链接文本
  4. `meta[name=author]`/`twitter:site` 的品牌标识
  5. 域名到品牌回退: 去掉 `www.`/`blog.`/TLD,对连字符/驼峰转为 TitleCase
- 特例映射:
  - `cursor.com` → Cursor team
  - `news.ycombinator.com` → Y Combinator
  - `*.github.io` → 取 `owner` 段并 TitleCase
  - `medium.com/<publication>` → 取 `<publication>` 并规范为 TitleCase(如 `levelshealth` → Levels Health)
- 输出格式: `from [团队名]` 将团队名作为可点击链接,目标为该域主页或品牌页。

## 归档样式扩展: GitHub Repo
- 适用: GitHub 代码仓库(库/框架/工具/示例)。
- 格式:
  - [仓库名称](仓库地址) — 仓库简要说明(可选)
  - 当“仓库名称”已足够表述功能时省略简要说明。
- 提取规则:
  - 仓库名称: 取 `owner/repo` 中的 `repo` 并保留大小写;或页面 H1/`og:title` 的可见仓库名。
  - 简要说明: 优先 `og:description`/页面描述段落;若无,生成 1 句中文概要,保留必要英文术语。
  - 语言: 简要说明用中文,库名/技术术语保留英文。
- 分类归属:
  - 默认归入 🛠️ Tools; 若为“值得收藏的库/生态入口”,也可置于 🤓 Fav Finds。
- 示例:
  - [swift-composable-architecture](https://github.com/pointfreeco/swift-composable-architecture) — Swift 应用架构库,强调组合与可测试性
  - [awesome-tca](https://github.com/antranapp/awesome-tca)

## 边界处理
- 不可访问/删除: 返回该链接 + “无法访问或已删除”。
- 无外链但有正文: 输出简要观点或结论并归入“知识点概念”。
- 多条输入: 每条链接独立处理并归档,不混淆主链接与相关链接。

## 验证清单
- name/description 更新为通用 link-extractor 并明确触发条件。
- Markdown 条目与引用链接格式清晰、一致。
- Daily 归档路径与分类规范可用,与旧 daily-weibo 兼容。

## 指令与脚本
- 指令调用:
  - 格式: `link <URL> [category] [style]`
  - category: Fav Finds | Read This | Tools | Try This | Listen To
  - style: 概念式 | 要点式 | 官方博客 | 图标单行 | GitHub Repo
  - 示例: `link https://cursor.com/cn/blog/agent-best-practices Read This 官方博客`
- 脚本: 生成 Daily Links 文件
  - 位置: `scripts/create-daily-links.sh`
  - 用法: `./scripts/create-daily-links.sh [YYYY-MM-DD]`
  - 作用: 在 `docs/daily-links/` 下创建当日文件,包含六大板块的空模板