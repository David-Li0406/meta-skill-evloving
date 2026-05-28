# X (Twitter) AI 技术领域自动化运营 Skill

基于 **Claude Code Chrome MCP** 的智能运营 Skill，专注于 AI/大模型技术领域的 X (Twitter) 账号运营。

## 特性

- **基于 X 开源算法优化** - 深度分析 [twitter/the-algorithm](https://github.com/twitter/the-algorithm)，策略有据可依
- **Claude Code Chrome MCP 集成** - 无需额外安装 Playwright/Selenium，直接使用已登录的 Chrome
- **智能内容生成** - AI 辅助生成高质量技术推文和评论
- **安全防护** - 内置敏感词检测、操作频率限制、内容安全检查

## 算法洞察

基于 X 开源代码的 Heavy Ranker 权重分析：

| 互动类型 | 权重 | 策略 |
|----------|------|------|
| 作者回复你的评论 | **+75** | 最高价值，发布引发回复的深度评论 |
| 直接回复 | +13.5 | 高质量技术见解 |
| 外链降权 | -30~50% | **链接放评论区** |
| Blue Verified | 2-4× | 强烈推荐认证 |
| 原生视频 | 2-4× | 优先发布视频内容 |

## 快速开始

### 前提条件

1. **Claude in Chrome 扩展** (v1.0.36+)
2. **Chrome 中已登录 X (Twitter)**
3. **Claude Code CLI** (v2.0.73+)

### 安装

```bash
# 克隆到 Claude Code skills 目录
git clone https://github.com/yordyi/skillforx.git ~/.claude/skills/x-auto-operator
```

### 使用

```bash
# 启动 Claude Code with Chrome
claude --chrome

# 验证连接
/chrome

# 开始运营
帮我执行 X 早间互动任务
```

## 功能模块

### 1. 智能互动

```
帮我浏览 @OpenAI 主页并点赞最新推文

为 @AnthropicAI 的推文生成一条有价值的技术评论

搜索 "LLM fine-tuning" 相关帖子，分析值得互动的内容
```

### 2. 内容发布

```
帮我发布一条关于 RAG 最佳实践的推文

生成并发布一个关于 LLM 微调技巧的 Thread (7条)
```

### 3. 数据分析

```
分析我最近的推文表现

总结今天的互动数据
```

## 文件结构

```
x-auto-operator/
├── x-auto-operator.skill      # 主 Skill 文件
├── references/
│   ├── x-algorithm-analysis.md  # X 算法深度分析
│   ├── engagement-strategy.md   # 互动策略指南
│   ├── content-templates.md     # 内容模板库
│   └── safety-rules.md          # 安全规则
├── scripts/
│   ├── browser_controller.py    # Chrome MCP 工作流程
│   └── content_generator.py     # AI 内容生成器
├── assets/
│   ├── config_template.json     # 配置模板
│   └── target_accounts.json     # 目标账号列表
└── requirements.txt
```

## 安全规则

### 操作频率限制

| 操作 | 间隔 | 每小时上限 | 每日上限 |
|------|------|-----------|----------|
| 点赞 | 5-15秒 | 30 | 200 |
| 评论 | 60-120秒 | 15 | 80 |
| 转发 | 30-60秒 | 10 | 50 |
| 发帖 | 30分钟 | 3 | 15 |

### 内容红线

**绝对禁止**: 政治、宗教、地域、性别等敏感话题

**只允许**: AI/技术讨论、代码、论文、开源项目、工具教程

## 目标账号

### Tier 1: AI 公司
- @OpenAI, @AnthropicAI, @GoogleDeepMind, @MetaAI, @xAI

### Tier 2: AI 大V
- @karpathy, @ylecun, @sama, @drfeifei

## 参考资源

- [X 算法仓库](https://github.com/twitter/the-algorithm)
- [Claude Code Chrome 文档](https://code.claude.com/docs/en/chrome)

## 免责声明

本 Skill 仅用于合法的社交媒体运营。使用者需遵守 X 服务条款，对账号安全负责。

## License

MIT
