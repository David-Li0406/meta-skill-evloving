#!/usr/bin/env python3
"""
X (Twitter) 浏览器控制 - Claude Code Chrome MCP 版本

本脚本设计为与 Claude Code 的 Chrome MCP 工具配合使用
不是独立运行的脚本，而是提供给 Claude Code 使用的工作流程指南

使用方式:
1. 启动 Claude Code with Chrome: claude --chrome
2. 让 Claude 按照本文件中的工作流程执行操作
"""

# ============================================================
# 这不是一个传统的 Python 脚本
# 这是一个工作流程指南，供 Claude Code 参考
# ============================================================

"""
## X (Twitter) 操作工作流程 - Claude Code Chrome MCP

### 前提条件

1. 确保已安装 Claude in Chrome 扩展 (v1.0.36+)
2. 在 Chrome 中已登录 X (Twitter) 账号
3. 使用 `claude --chrome` 启动 Claude Code

### 验证连接

使用 /chrome 命令验证 Chrome 连接状态

---

## 核心操作工作流程

### 1. 浏览 X 首页获取推文

工作流程:
```
1. 使用 mcp__Claude_in_Chrome__tabs_context_mcp 获取当前标签页
2. 使用 mcp__Claude_in_Chrome__tabs_create_mcp 创建新标签页
3. 使用 mcp__Claude_in_Chrome__navigate 导航到 https://x.com
4. 使用 mcp__Claude_in_Chrome__browser_snapshot 获取页面快照
5. 使用 mcp__Claude_in_Chrome__read_page 读取页面内容
```

### 2. 点赞推文

工作流程:
```
1. 导航到目标推文页面
2. 使用 read_page 找到点赞按钮 (data-testid="like")
3. 使用 computer 工具点击点赞按钮
4. 等待 2-5 秒
5. 验证点赞成功 (按钮变为 unlike)
```

### 3. 发布评论

工作流程:
```
1. 导航到目标推文页面
2. 找到回复按钮并点击
3. 在回复输入框中输入内容
4. 点击发送按钮
5. 等待发送完成
```

### 4. 发布推文

工作流程:
```
1. 导航到 https://x.com/compose/tweet 或点击发推按钮
2. 在输入框中输入推文内容
3. 如需添加图片，点击图片按钮并上传
4. 点击发布按钮
5. 等待发布完成
```

### 5. 搜索 AI 相关内容

工作流程:
```
1. 导航到 https://x.com/search?q=AI%20LLM&f=live
2. 读取搜索结果
3. 分析每条推文的质量
4. 选择值得互动的推文
```

---

## 安全限制

### 操作频率限制
- 点赞: 每次操作后等待 5-15 秒
- 评论: 每次操作后等待 60-120 秒
- 发帖: 每次操作后等待 30 分钟
- 每小时总操作不超过 30 次

### 内容安全
- 只发布/互动 AI/技术相关内容
- 不涉及政治、宗教、地域、性别等敏感话题
- 评论要有价值，不发模板化回复

---

## Chrome MCP 工具参考

### 页面导航
- navigate: 导航到 URL
- navigate_back: 后退

### 页面读取
- read_page: 获取页面元素树
- get_page_text: 获取页面文本
- browser_snapshot: 获取无障碍快照
- computer (screenshot): 截图

### 交互操作
- computer (click): 点击
- computer (type): 输入文本
- form_input: 填写表单
- find: 查找元素

### 标签页管理
- tabs_context_mcp: 获取标签页上下文
- tabs_create_mcp: 创建新标签页

---

## 示例: 完整的点赞工作流

用户请求: "帮我点赞 OpenAI 的最新推文"

Claude 执行步骤:
1. tabs_context_mcp - 检查当前标签页
2. tabs_create_mcp - 创建新标签页
3. navigate to "https://x.com/OpenAI" - 导航到 OpenAI 主页
4. read_page - 读取页面找到最新推文
5. find "like button" - 定位点赞按钮
6. computer click - 点击点赞
7. read_page - 验证点赞成功

---

## 示例: 智能评论工作流

用户请求: "分析 @AnthropicAI 的最新推文并发表有价值的评论"

Claude 执行步骤:
1. 导航到 https://x.com/AnthropicAI
2. 读取最新推文内容
3. 分析推文主题，生成有价值的技术评论
4. 进行内容安全检查
5. 点击回复按钮
6. 输入评论内容
7. 点击发送
8. 等待并验证发送成功
"""

# 操作配置
OPERATION_CONFIG = {
    "rate_limits": {
        "like": {
            "min_delay": 5,    # 秒
            "max_delay": 15,
            "hourly_limit": 30,
            "daily_limit": 200
        },
        "comment": {
            "min_delay": 60,
            "max_delay": 120,
            "hourly_limit": 15,
            "daily_limit": 80
        },
        "post": {
            "min_delay": 1800,  # 30分钟
            "max_delay": 3600,
            "hourly_limit": 3,
            "daily_limit": 15
        },
        "retweet": {
            "min_delay": 30,
            "max_delay": 60,
            "hourly_limit": 10,
            "daily_limit": 50
        }
    },
    "x_selectors": {
        "tweet_article": "article",
        "like_button": "[data-testid='like']",
        "unlike_button": "[data-testid='unlike']",
        "retweet_button": "[data-testid='retweet']",
        "reply_button": "[data-testid='reply']",
        "tweet_input": "[data-testid='tweetTextarea_0']",
        "tweet_button": "[data-testid='tweetButton']",
        "search_input": "[data-testid='SearchBox_Search_Input']"
    },
    "target_accounts": [
        {"handle": "OpenAI", "priority": 1},
        {"handle": "AnthropicAI", "priority": 1},
        {"handle": "GoogleDeepMind", "priority": 1},
        {"handle": "karpathy", "priority": 2},
        {"handle": "ylecun", "priority": 2},
        {"handle": "sama", "priority": 2}
    ],
    "search_queries": [
        "AI LLM",
        "machine learning",
        "Claude AI",
        "GPT",
        "RAG retrieval",
        "fine-tuning LLM"
    ]
}

# 敏感词列表 (用于内容检查)
SENSITIVE_KEYWORDS = {
    "politics": ["election", "president", "政治", "选举", "政党"],
    "religion": ["religion", "religious", "宗教", "信仰"],
    "region": ["地域", "歧视", "外地人"],
    "gender": ["性别", "女权", "男权"]
}

def check_content_safety(text: str) -> dict:
    """
    检查内容安全性 (供 Claude 参考的逻辑)

    Returns:
        {"safe": bool, "warnings": list}
    """
    text_lower = text.lower()
    warnings = []

    for category, keywords in SENSITIVE_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                warnings.append(f"检测到 {category} 相关词汇: {keyword}")

    return {
        "safe": len(warnings) == 0,
        "warnings": warnings
    }


# 推文质量分析提示词
TWEET_ANALYSIS_PROMPT = """
分析这条推文是否值得作为 AI 技术博主进行互动:

推文内容: {tweet_content}

请评估:
1. 是否与 AI/ML 技术相关？
2. 内容质量如何？
3. 是否值得评论/点赞？
4. 建议的互动方式？

返回格式:
- 值得互动: 是/否
- 推荐操作: like/comment/retweet/skip
- 评论建议: (如果推荐评论)
"""

# 评论生成提示词
COMMENT_GENERATION_PROMPT = """
为以下推文生成一条高质量的技术评论:

原帖作者: @{author}
原帖内容: {tweet_content}

要求:
1. 展示专业 AI/ML 知识
2. 补充有价值的见解或提出好问题
3. 长度 50-150 字符
4. 语气专业但友好
5. 避免模板化开头如 "Great post!"
6. 不涉及任何敏感话题

直接输出评论内容。
"""

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     X (Twitter) 自动化运营 - Claude Code Chrome MCP 版       ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║  本脚本不是独立运行的程序                                      ║
    ║  而是供 Claude Code 参考的工作流程和配置                       ║
    ║                                                              ║
    ║  使用方式:                                                    ║
    ║  1. 启动: claude --chrome                                    ║
    ║  2. 验证: /chrome                                            ║
    ║  3. 告诉 Claude 你想执行的 X 运营任务                         ║
    ║                                                              ║
    ║  示例命令:                                                    ║
    ║  - "帮我浏览 OpenAI 主页并点赞最新推文"                        ║
    ║  - "搜索 AI LLM 相关帖子并分析质量"                           ║
    ║  - "为 @AnthropicAI 的推文生成评论"                           ║
    ║  - "发布一条关于 RAG 的技术推文"                              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
