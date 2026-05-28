---
name: evolving-agent
description: 协调器。当用户说"学习这个仓库"、"从 GitHub 学习"、"提取代码规范"、"检查所有 skill 状态"、"系统健康检查"、"协调 skill"时使用。负责编排 github-to-skills、skill-manager、skill-evolution-manager、programming-assistant 四个核心组件。
user-invocable: false
license: MIT
---

# Evolving Agent - 协调器

这是整个 Evolving Programming Agent 系统的**协调层**，负责编排和管理四个核心 skill 组件。

## 核心职责

1.  **学习触发器**：检测用户输入中的 GitHub URL，触发学习流程
2.  **进化触发器**：在编程任务结束后，自动触发进化流程
3.  **健康检查器**：定期扫描并检测过期或无效的 skill
4.  **会话管理器**：追踪会话状态，持久化上下文信息

## 触发条件

### 学习流程触发

**触发模式**：
- 用户发送 GitHub 仓库 URL
- "学习这个仓库"
- "提取这个项目的代码规范"
- "从这个项目中学习最佳实践"

**检测关键词**：
- `https://github.com/...`
- `http://github.com/...`
- `github.com/...`
- `learn`, `学习`, `提取`, `extract`

### 管理流程触发

**触发命令**：
- `/skill-manager check`
- `/skill-manager list`
- `/skill-manager enable <name>`
- `/skill-manager disable <name>`
- `/skill-manager health`
- "检查 skill 更新"
- "列出所有 skill"
- "启用/禁用 skill"

### 进化流程触发

**触发条件**（在 programming-assistant 会话结束时）：
1. 修复了复杂 Bug（连续尝试 > 1 次）
2. 用户给出明确反馈（"记住"、"保存"、"重要"等）
3. 发现了新的最佳实践
4. 使用了非标准解决方案

**自动触发**：
- 在 programming-assistant 中配置 `auto_evolve: true`
- 达到触发阈值后自动调用 `/evolve`

## 协调工作流程

```
用户输入
    │
    ▼
输入分析器
    │
    ├── GitHub URL? ───▶ 学习流程 (github-to-skills)
    ├── 编程任务? ───▶ 执行流程 (programming-assistant) ───▶ 进化流程 (skill-evolution-manager)
    └── 管理命令? ───▶ 管理流程 (skill-manager)
```

### 学习流程（Learning Workflow）

```
用户: 学习这个仓库 https://github.com/example/react-app
    │
    ▼
1. 触发 github-to-skills (学习模式)
    │
    ├── fetch_github_info.py - 获取仓库信息
    ├── extract_patterns.py --store - 提取并存储
    │   ├── 分析项目架构 → knowledge-base/patterns/
    │   ├── 检测技术栈 → knowledge-base/tech-stacks/
    │   └── 提取最佳实践 → knowledge-base/skills/
    │
    └── 更新 knowledge-base/index.json (触发词索引)
    │
    ▼
2. 下次编程时自动加载
    │
    └── programming-assistant 通过 knowledge_trigger.py 按需查询
```

### 进化流程（Evolution Workflow）

```
用户: 帮我修复这个 bug
助手: [分析并修复...]
    │
    ▼
1. programming-assistant 执行编程任务
    │
    ├── 修复 bug
    ├── 验证结果
    └── 更新 progress.txt
    │
    ▼
2. 会话结束检查
    │
    ├── 是否满足进化触发条件?
    │   ├── 是 → 调用 skill-evolution-manager
    │   │   ├── trigger_detector.py - 检测是否需要进化
    │   │   ├── knowledge_summarizer.py - 分析会话内容
    │   │   └── 存储到 knowledge-base/
    │   │       ├── problems/ - 问题解决方案
    │   │       ├── experiences/ - 经验教训
    │   │       └── 更新 index.json
    │   └── 自动进化完成
    │
    └── 否 → 正常结束会话
```

### 管理流程（Management Workflow）

```
用户: /skill-manager health
    │
    ▼
1. 触发 skill-manager
    │
    ├── health_check.py - 扫描所有 skill
    │   ├── 检查 SKILL.md 存在性
    │   ├── 检查 GitHub hash 过期
    │   └── 生成健康报告
    │
    ├── 报告状态
    │   ├── ✅ 健康的 skill
    │   ├── ⚠️  过期的 skill
    │   └── ❌ 无效的 skill
    │
    └── 提供建议操作
        ├── 更新过期 skill
        ├── 修复无效 skill
        └── 启用/禁用 skill
```

## 依赖关系

| 组件 | 用途 | 依赖 | 数据流向 |
|--------|------|------|----------|
| **knowledge-base** | 统一知识存储 | 无 | 被所有组件读写 |
| **github-to-skills** | 学习新技能 | knowledge-base | 写入知识库 |
| **skill-manager** | 管理 skill 库 | 无 | 独立运行 |
| **skill-evolution-manager** | 进化优化 | knowledge-base | 写入知识库 |
| **programming-assistant** | 执行编程任务 | knowledge-base | 读取知识库 |
| **evolving-agent** | 协调所有组件 | 以上全部 | 编排调度 |

## 全局配置

配置文件位于 `config.yaml`：

```yaml
evolution:
  auto_evolve: true           # 启用自动进化
  threshold: medium             # 触发阈值: low/medium/high
  silent_mode: true            # 静默模式，不打断用户流程

skill_manager:
  auto_check_interval: 7d     # 每 7 天检查一次更新
  auto_update: false            # 是否自动更新过期 skill

learning:
  default_mode: tool            # 默认模式: tool/learn
  save_addons_to: ~/.config/opencode/skill/knowledge-addons/

logging:
  level: info                 # 日志级别: debug/info/warn/error
  file: ~/.config/evolving-agent.log
```

## 使用示例

### 示例 1: 学习新框架

```
用户: 学习这个 React 项目的最佳实践
      https://github.com/alan2207/bulletproof-react

智能体:
1. 检测到 GitHub URL，触发学习流程
2. 运行 fetch_github_info.py 获取仓库信息
3. 运行 extract_patterns.py 分析代码结构
4. 生成 bulletproof-react-knowledge addon
5. 自动附加到 programming-assistant

输出: "已学习 bulletproof-react 的最佳实践，包括:
      - Feature-Based 架构
      - React Query 状态管理
      - Zod 类型校验
      下次创建 React 项目时将自动应用这些范式。"
```

### 示例 2: 自动进化

```
用户: 帮我修复这个 API 报错

智能体:
1. 分析问题，定位到跨域配置错误
2. 修复代码，验证通过
3. 检测到这是一个值得保存的经验
4. 自动触发进化流程
5. 将 "Vite 开发服务器需要配置 proxy 解决跨域" 写入 evolution.json

用户下次遇到类似问题时，智能体会主动提示这个解决方案。
```

### 示例 3: 插件管理

```
用户: /skill-manager health

智能体:
1. 运行 health_check.py 扫描所有 skill
2. 生成健康检查报告

输出:
┌─────────────────────────────────────────────────────────┐
│               Skill 健康检查报告                         │
├─────────────────────────────────────────────────────────┤
│ 总计: 5 个 skill                                        │
│ ✅ 健康: 3                                              │
│ ⚠️  过期: 1 (yt-dlp-tool)                               │
│ ❌ 损坏: 1 (deprecated-helper)                          │
├─────────────────────────────────────────────────────────┤
│ 建议操作:                                               │
│ 1. 运行 `/skill-manager update yt-dlp-tool` 更新       │
│ 2. 运行 `/skill-manager delete deprecated-helper` 清理 │
└─────────────────────────────────────────────────────────┘
```

## 最佳实践

1. **非侵入式**：协调器不直接修改用户代码，只触发相应的 skill
2. **可观测性**：所有操作都记录日志，便于调试
3. **容错性**：单个组件失败不影响其他组件
4. **用户控制**：所有自动化功能都可以通过配置关闭或调整

## 统一知识库 (Unified Knowledge Base)

所有知识统一存储到 `knowledge-base/` 目录，协调器通过触发词索引按需加载：

### 知识来源

| 来源 | 存储位置 | 说明 |
|------|----------|------|
| github-to-skills | `knowledge-base/skills/`, `knowledge-base/tech-stacks/`, `knowledge-base/patterns/` | 从 GitHub 仓库学习 |
| skill-evolution-manager | `knowledge-base/experiences/`, `knowledge-base/problems/` | 从编程会话中进化 |
| 手动存储 | 各分类目录 | 用户主动添加 |

### 查询方式

```bash
# 根据项目自动检测并加载相关知识
python knowledge-base/scripts/knowledge_trigger.py \
  --input "用户输入" \
  --project "." \
  --format context > .knowledge-context.md

# 按触发关键字查询
python knowledge-base/scripts/knowledge_query.py --trigger react,hooks

# 按分类查询
python knowledge-base/scripts/knowledge_query.py --category problem
```

### 数据流向

```
┌─────────────────────────────────────────────────────────────────┐
│                    统一知识库 (knowledge-base/)                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐  │
│  │experience│tech-stack│scenario│ problem │ pattern │  skill  │  │
│  └────▲────┴────▲────┴────▲────┴────▲────┴────▲────┴────▲────┘  │
│       │         │         │         │         │         │       │
│       │         │         │         │         │         │       │
│  ┌────┴────┐    │    ┌────┴────┐    │    ┌────┴─────────┴────┐  │
│  │evolution│    │    │  编程   │    │    │  github-to-skills │  │
│  │ manager │    │    │assistant│    │    │    (学习仓库)      │  │
│  └─────────┘    │    └─────────┘    │    └───────────────────┘  │
│                 │                   │                           │
│            ┌────┴───────────────────┴────┐                      │
│            │      index.json             │                      │
│            │   (trigger_index 索引)      │                      │
│            └─────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

## 注意事项

- evolving-agent 主要作为**逻辑协调器**，实际工作由各个 skill 组件完成
- 在非自动化场景下，用户可以直接调用各个 skill 的命令
- 自动进化功能需要在 programming-assistant 中配置 `auto_evolve: true`
- 统一知识查询会合并 GitHub 学习和用户经验，提供完整的知识上下文
