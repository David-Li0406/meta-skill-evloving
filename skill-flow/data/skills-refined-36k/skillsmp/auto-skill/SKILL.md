---
name: auto-skill
description: |
  智能Skill路由器。根据用户需求自动选择已安装的skill，或从skills.sh搜索安装新skill。
  所有需要用户确认的操作都通过AskUserQuestion呈现。
allowed-tools:
  - Task
  - AskUserQuestion
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - mcp__firecrawl__firecrawl_search
  - mcp__firecrawl__firecrawl_scrape
  - mcp__web_reader__webReader
  - mcp__web-search-prime__webSearchPrime
---

# Auto Skill - 智能Skill路由器

根据用户需求自动选择并执行合适的 skill。

## 工作流程

```
用户请求 → 分析需求 → 匹配本地skill → 执行
                    ↓ 未匹配
              搜索skills.sh → 呈现选项 → 安装 → 执行
```

## 使用方式

直接描述你的需求，auto-skill 会自动：
1. 分析你的需求
2. 在已安装的 skills 中查找匹配项
3. 如果没有找到，搜索 skills.sh
4. 呈现选项供你选择
5. 自动安装并执行
