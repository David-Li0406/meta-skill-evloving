# Auto Skill 使用说明

## 概述

`auto-skill` 是一个智能 Skill 路由器，可以根据你的需求自动：
1. 在已安装的 skills 中查找匹配项
2. 如果没有找到，自动搜索 skills.sh
3. 呈现选项供你选择
4. 自动安装并执行

## 目录结构

```
auto-skill/
├── SKILL.md                    # Skill 入口文件
├── README.md                   # 本文件
├── phases/
│   ├── _orchestrator.md        # 编排器（状态管理）
│   └── actions/                # 独立动作
│       ├── 01-analyze-request.md
│       ├── 02-match-local-skills.md
│       ├── 03-search-skills.sh.md
│       ├── 04-present-options.md
│       ├── 05-execute-skill.md
│       └── 06-install-skill.md
├── specs/
│   ├── requirements.md         # 需求规范
│   └── action-catalog.md       # 动作目录
└── templates/
    └── action-base.md          # Action 模板
```

## 使用方式

直接向 Claude 描述你的需求，例如：

```
"帮我分析这个Excel文件"
"生成一份API文档"
"翻译这段文本"
```

auto-skill 会自动：
1. 分析你的需求
2. 匹配或搜索相关 skills
3. 呈现选项让你选择
4. 执行选定的 skill

## 工作流程

```
用户请求 → 分析需求 → 匹配本地skills
                    ↓ 无匹配
              搜索skills.sh
                    ↓
              呈现选项 → 安装 → 执行
```

## 配置

- **执行模式**: Autonomous（动态路由）
- **允许的工具**:
  - Task, AskUserQuestion, Read, Write, Bash, Glob, Grep
  - mcp__firecrawl__firecrawl_search
  - mcp__firecrawl__firecrawl_scrape
  - mcp__web_reader__webReader
  - mcp__web-search-prime__webSearchPrime

## 扩展

要添加新的 action，参考 `templates/action-base.md` 模板创建新文件，然后在 `_orchestrator.md` 中注册。

## 版本

v1.0.0 - 初始版本
