---
name: hooks
description: iterate Hooks 机制设计方案。确定性的脚本执行点，用于上下文注入、日志记录、自动化任务。
---

# iterate Hooks 机制设计

## 概述

Hooks 是**确定性的脚本执行点**，在 iterate 生命周期的特定时机自动执行，不依赖 AI 决策。

## Hook 事件类型

### 1. PreRun (会话开始前)

**触发时机**：对话开始时，AI 生成第一条消息前

**用途**：
- 检查 `.cunzhi-knowledge/` 更新 (`git fetch + status`)
- 读取 `skills/INDEX.md` 注入触发词表
- 启动 iterate 服务端口
- 注入项目上下文

**实现方式**：
```bash
# ~/.cunzhi/hooks/pre-run.sh
#!/bin/bash

# 1. 检查知识库更新
cd .cunzhi-knowledge && git fetch --quiet
if [ $(git rev-list HEAD...origin/main --count) -gt 0 ]; then
  echo "⚠️ 知识库有更新，请运行 git pull"
fi

# 2. 输出触发词表（注入上下文）
cat .cunzhi-knowledge/prompts/skills/INDEX.md

# 3. 检查端口
if ! lsof -i :8080 > /dev/null 2>&1; then
  echo "⚠️ iterate 服务未启动"
fi
```

### 2. PostRun (会话结束后)

**触发时机**：`KeepGoing=false` 返回后

**用途**：
- 记录对话到 `conversations/YYYY-MM-DD.md`
- 自动 git commit + push 知识库
- 清理临时文件

**实现方式**：
```bash
# ~/.cunzhi/hooks/post-run.sh
#!/bin/bash

# 1. 记录对话摘要
DATE=$(date +%Y-%m-%d)
echo "## $(date +%H:%M) - $PROJECT_PATH" >> .cunzhi-knowledge/conversations/$DATE.md
cat ~/.cunzhi/$PORT/output.md >> .cunzhi-knowledge/conversations/$DATE.md
echo "" >> .cunzhi-knowledge/conversations/$DATE.md

# 2. 同步知识库
cd .cunzhi-knowledge
git add .
git commit -m "auto: conversation $(date +%Y-%m-%d_%H:%M)" --quiet
git push --quiet
```

### 3. UserSubmit (用户提交时)

**触发时机**：用户在 iterate GUI 中点击"发送"后，消息发送给 AI 前

**用途**：
- 匹配触发词，注入对应 SKILL.md 内容
- 追加条件性上下文（已有功能）
- 验证输入格式

**实现方式**：
```python
# ~/.cunzhi/hooks/user-submit.py
import sys
import re

user_input = sys.argv[1]
skills_index = open('.cunzhi-knowledge/prompts/skills/INDEX.md').read()

# 解析触发词表
triggers = {}
for line in skills_index.split('\n'):
    if '|' in line and 'SKILL.md' in line:
        parts = line.split('|')
        if len(parts) >= 3:
            skill_path = re.search(r'\[.*?\]\((.*?)\)', parts[1])
            keywords = parts[2].strip()
            if skill_path:
                triggers[skill_path.group(1)] = keywords.split('、')

# 匹配触发词
for path, keywords in triggers.items():
    for kw in keywords:
        if kw in user_input:
            skill_content = open(f'.cunzhi-knowledge/prompts/skills/{path}').read()
            print(f"\n---\n## 自动加载 Skill: {path}\n{skill_content}\n---\n")
            break
```

## 配置文件

### ~/.cunzhi/hooks.json

```json
{
  "hooks": {
    "PreRun": {
      "enabled": true,
      "command": "~/.cunzhi/hooks/pre-run.sh",
      "inject_stdout": true
    },
    "PostRun": {
      "enabled": true,
      "command": "~/.cunzhi/hooks/post-run.sh",
      "inject_stdout": false
    },
    "UserSubmit": {
      "enabled": true,
      "command": "python3 ~/.cunzhi/hooks/user-submit.py",
      "inject_stdout": true
    }
  }
}
```

## 与现有机制的整合

| 现有机制 | 对应 Hook | 整合方式 |
|----------|-----------|----------|
| `trigger: always_on` 规则 | PreRun | 规则内容通过 PreRun 注入 |
| `zhi` 强制调用 | PostRun | 对话结束后自动记录 |
| 上下文追加开关 | UserSubmit | 作为 UserSubmit 的一部分 |
| Skills INDEX.md | PreRun + UserSubmit | PreRun 加载表，UserSubmit 匹配 |

## 实现优先级

1. **Phase 1**：UserSubmit Hook（触发词匹配）
2. **Phase 2**：PostRun Hook（对话记录）
3. **Phase 3**：PreRun Hook（知识库检查）

## 技术实现

需要修改的文件：
1. `cunzhi.py` - 添加 Hook 执行逻辑
2. `cunzhi-server.py` - 服务端 Hook 支持
3. 创建 `~/.cunzhi/hooks/` 目录和脚本
