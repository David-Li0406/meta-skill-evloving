---
name: knowledge-base
description: 统一知识库。当用户说"查询知识"、"搜索经验"、"存储知识"、"有没有相关经验"、"之前遇到过"、"历史方案"、"最佳实践"、"技术栈知识"、"问题解决方案"时使用。支持知识存储、查询、触发加载，包含经验/技术栈/场景/问题/测试/范式/技能七大分类。
license: MIT
---

# 统一知识库 (Knowledge Base)

统一的知识存储、查询、触发和进化系统。

## 知识分类

| 分类 | 目录 | 说明 | 触发场景 |
|------|------|------|----------|
| **experience** | `experiences/` | 经验积累 | 优化、重构、最佳实践 |
| **tech-stack** | `tech-stacks/` | 技术栈知识 | 检测到项目使用某框架 |
| **scenario** | `scenarios/` | 场景知识 | 创建、实现、开发新功能 |
| **problem** | `problems/` | 问题解决 | 修复、调试、报错 |
| **testing** | `testing/` | 测试知识 | 测试、mock、验证 |
| **pattern** | `patterns/` | 编程范式 | 架构、设计模式 |
| **skill** | `skills/` | 编程技能 | 通用技巧 |

## 核心工具

### 1. 知识存储 (knowledge_store.py)

```bash
# 存储经验
python scripts/knowledge_store.py --category experience --name "Vite代理配置" \
  --content '{"description": "...", "solution": "..."}'

# 从 JSON 导入
echo '{"category": "problem", "name": "CORS跨域", ...}' | \
  python scripts/knowledge_store.py --from-json --source "session-123"
```

便捷方法：
- `store_experience()` - 存储经验
- `store_tech_stack()` - 存储技术栈知识
- `store_scenario()` - 存储场景知识
- `store_problem()` - 存储问题解决方案
- `store_testing()` - 存储测试知识
- `store_pattern()` - 存储编程范式
- `store_skill()` - 存储编程技能

### 2. 知识查询 (knowledge_query.py)

```bash
# 按触发关键字查询 (最常用)
python scripts/knowledge_query.py --trigger react,hooks,state

# 按分类查询
python scripts/knowledge_query.py --category problem

# 全文搜索
python scripts/knowledge_query.py --search "跨域"

# 获取单个条目
python scripts/knowledge_query.py --id problem-cors-abc123

# 查看统计
python scripts/knowledge_query.py --stats
```

### 3. 知识触发检测器 (knowledge_trigger.py)

**核心功能**：根据用户输入和项目上下文自动检测并加载相关知识。

```bash
# 根据用户输入触发
python scripts/knowledge_trigger.py --input "帮我修复这个 CORS 跨域问题"

# 根据项目检测触发
python scripts/knowledge_trigger.py --project /path/to/react-app

# 组合触发
python scripts/knowledge_trigger.py --input "如何优化 API 性能" --project .

# 输出为上下文格式 (适合嵌入 SKILL.md)
python scripts/knowledge_trigger.py --input "..." --format context
```

**触发机制**：
1. **项目检测**：解析 package.json, go.mod, pom.xml 等
2. **关键字匹配**：从用户输入提取关键字匹配触发词
3. **场景推断**：根据动词推断 (创建→scenario, 修复→problem, 测试→testing)
4. **问题症状**：识别常见问题关键字 (cors, memory, timeout)

### 4. 知识归纳总结器 (knowledge_summarizer.py)

**核心功能**：分析会话内容，自动提取、分类并存储知识。

```bash
# 分析会话内容
cat session.txt | python scripts/knowledge_summarizer.py

# 分析并自动存储
cat session.txt | python scripts/knowledge_summarizer.py --auto-store --session-id "session-123"

# 更新知识有效性 (正面反馈)
python scripts/knowledge_summarizer.py --feedback positive --entry-id "problem-cors-abc123"
```

**提取模式**：
- 问题-解决方案模式
- 最佳实践模式
- 注意事项/坑模式
- 用户反馈模式

## 知识条目 Schema

```json
{
  "id": "category-name-hash",
  "category": "experience|tech-stack|scenario|problem|testing|pattern|skill",
  "name": "知识名称",
  "triggers": ["触发关键字"],
  "content": { /* 分类特定内容 */ },
  "sources": ["来源URL或会话ID"],
  "tags": ["额外标签"],
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "usage_count": 0,
  "effectiveness": 0.5
}
```

## 工作流程

### 学习流程 (从 GitHub 学习)

```
github-to-skills 提取模式
        │
        ▼
knowledge_store.py 存储
        │
        ├── tech-stacks/<framework>.json
        ├── patterns/<pattern>.json
        └── practices → experiences/
```

### 进化流程 (从会话学习)

```
会话结束
    │
    ▼
skill-evolution-manager 检测触发
    │
    ▼
knowledge_summarizer.py 分析会话
    │
    ├── 提取知识
    ├── 推断分类
    ├── 生成触发关键字
    └── 存储到知识库
```

### 使用流程 (辅助编程)

```
用户输入
    │
    ▼
knowledge_trigger.py 检测触发
    │
    ├── 提取关键字
    ├── 检测项目技术栈
    └── 查询匹配知识
    │
    ▼
注入到 programming-assistant 上下文
```

## 异步子会话调用 (Subsession)

> **核心原则**: 知识检索和归纳使用子会话异步执行，不阻塞主编程任务。

### 子代理定义

| 代理 | 文件 | 用途 |
|------|------|------|
| `knowledge-retrieval` | `agents/retrieval-agent.md` | 异步检索知识 |
| `knowledge-summarize` | `agents/summarize-agent.md` | 异步归纳知识 |

### 平台适配

#### Claude Code / OpenCode

使用 `Task` tool 启动子会话：

```python
# 知识检索 (任务开始时)
Task(
    subagent_type="general",
    description="Knowledge retrieval",
    prompt="""
    使用 knowledge-retrieval-agent 检索知识:
    - user_input: "{用户输入}"
    - project_dir: "{项目目录}"
    - output_file: ".knowledge-context.md"
    
    执行: python knowledge-base/scripts/knowledge_trigger.py --input "..." --project "." --format context > .knowledge-context.md
    """
)

# 知识归纳 (任务结束时)
Task(
    subagent_type="general", 
    description="Knowledge summarization",
    prompt="""
    使用 knowledge-summarize-agent 归纳知识:
    - session_id: "{session_id}"
    
    分析以下会话内容并提取知识:
    {session_content}
    
    执行: echo "{content}" | python knowledge-base/scripts/knowledge_summarizer.py --auto-store --session-id "{id}"
    """
)
```

#### Cursor

在 Composer 中使用 Agent 模式：

```
@knowledge-retrieval 检索关于 {topic} 的知识
@knowledge-summarize 归纳本次会话的知识
```

或直接在终端运行脚本（不阻塞 Composer）。

### 异步工作流

```
┌─────────────────────────────────────────────────────────────────┐
│                         主任务流程                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  用户输入                                                        │
│      │                                                          │
│      ├──────► [异步] Task: knowledge-retrieval                  │
│      │              └─► 写入 .knowledge-context.md              │
│      │                                                          │
│      ▼                                                          │
│  执行编程任务 (不等待)                                            │
│      │                                                          │
│      │  ◄──── [可选] 读取 .knowledge-context.md 获取知识上下文   │
│      │                                                          │
│      ▼                                                          │
│  任务完成                                                        │
│      │                                                          │
│      └──────► [异步] Task: knowledge-summarize                  │
│                    └─► 分析会话 → 存储知识库                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 文件通信

子会话通过文件与主任务通信：

| 文件 | 用途 | 生命周期 |
|------|------|----------|
| `.knowledge-context.md` | 检索到的知识上下文 | 任务开始时创建，任务结束时可删除 |
| `.knowledge-summary.md` | 归纳报告 | 任务结束时创建 |

### 触发时机

**知识检索** (retrieval):
- 任务开始时立即异步触发
- 不等待结果，主任务继续执行
- 主任务可在需要时读取 `.knowledge-context.md`

**知识归纳** (summarize):
- 任务结束时异步触发
- 检测到以下条件时触发:
  - 解决了复杂问题 (多次尝试)
  - 用户明确反馈 ("记住"、"保存")
  - 使用了非标准解决方案

## 与其他组件集成

### programming-assistant

在任务开始时异步触发知识检索：

```markdown
## 知识辅助 (异步)

任务开始时，启动子会话检索知识：

Task(subagent_type="general", description="Knowledge retrieval", prompt="...")

主任务继续执行，不等待检索完成。
如需参考知识，可读取 .knowledge-context.md。
```

### skill-evolution-manager

在会话结束时异步触发知识归纳：

```markdown
## 知识归纳 (异步)

检测到进化触发条件时，启动子会话：

Task(subagent_type="general", description="Knowledge summarization", prompt="...")

不阻塞用户，后台完成知识存储。
```

### github-to-skills

学习新框架后存储到统一知识库：

```bash
python scripts/extract_patterns.py --json | \
  python knowledge-base/scripts/knowledge_store.py --from-json --source "{github_url}"
```

## 目录结构

```
knowledge-base/
├── SKILL.md              # 本文档
├── schema.json           # 知识条目 schema 定义
├── index.json            # 全局索引 + 触发关键字映射
├── agents/               # 子代理定义
│   ├── retrieval-agent.md    # 知识检索代理
│   └── summarize-agent.md    # 知识归纳代理
├── scripts/
│   ├── knowledge_store.py      # 存储工具
│   ├── knowledge_query.py      # 查询工具
│   ├── knowledge_trigger.py    # 触发检测器
│   └── knowledge_summarizer.py # 归纳总结器
├── experiences/          # 经验积累
├── tech-stacks/          # 技术栈知识
├── scenarios/            # 场景知识
├── problems/             # 问题解决
├── testing/              # 测试知识
├── patterns/             # 编程范式
└── skills/               # 编程技能
```

## 最佳实践

1. **触发关键字设计**：每个知识条目应有 3-10 个触发关键字
2. **知识粒度**：一个条目解决一个问题/描述一个模式
3. **来源追踪**：始终记录知识来源 (GitHub URL, 会话 ID)
4. **有效性反馈**：使用正面/负面反馈持续优化知识质量
5. **定期清理**：低有效性的知识应被清理或更新
