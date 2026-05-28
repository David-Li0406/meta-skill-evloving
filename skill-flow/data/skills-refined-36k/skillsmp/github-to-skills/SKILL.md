---
name: github-to-skills
description: GitHub 仓库学习器。当用户说"学习这个仓库"、"从 GitHub 学习"、"提取这个项目的最佳实践"、"把这个仓库的经验存起来"、"分析这个开源项目"时使用。提取的知识存储到 knowledge-base 作为知识条目，不创建独立 skill。
license: MIT
---

# GitHub to Skills - 仓库学习器

从 GitHub 仓库提取编程知识，转化为可复用的技能条目，存储到统一知识库。

## 核心定位

**不是**创建独立的 skill 文件夹，**而是**：
1. 分析 GitHub 仓库的代码结构、README、最佳实践
2. 提取编程知识（技术栈、模式、经验、问题解决方案）
3. 按知识库 schema 格式化，存入 `knowledge-base/skills/` 分类
4. 供协调器（evolving-agent）按需调度加载

## 使用场景

| 触发词 | 说明 |
|--------|------|
| "学习这个仓库" | 全面分析仓库，提取所有类型知识 |
| "从 GitHub 学习 <url>" | 指定仓库 URL 学习 |
| "提取这个项目的最佳实践" | 聚焦提取最佳实践 |
| "分析这个开源项目的架构" | 聚焦架构模式 |
| "把这个仓库的经验存起来" | 存储到知识库 |

## 工作流程

```
GitHub URL → 获取仓库信息 → 分析提取 → 格式化为知识条目 → 存储到知识库 → 更新索引
```

### 1. 获取仓库信息

```bash
python scripts/fetch_github_info.py <github_url>
```

输出：
- 仓库描述、README 内容
- 目录结构、主要文件
- 最新提交哈希、版本标签
- package.json / go.mod / pom.xml 等配置文件

### 2. 分析提取知识

```bash
python scripts/extract_knowledge.py --input <repo_info.json>
```

提取内容：
- **技术栈知识**：框架、库、版本、配置方式
- **架构模式**：目录结构、分层设计、模块划分
- **最佳实践**：代码规范、命名约定、注释风格
- **常见问题**：README 中的 FAQ、已知问题

### 3. 存储到知识库

```bash
python scripts/store_to_knowledge.py --category skill --input <extracted.json>
```

存储格式遵循 `knowledge-base/schema.json` 的 SkillContent：

```json
{
  "id": "skill-<repo-name>-<hash>",
  "category": "skill",
  "name": "<仓库名> 编程技能",
  "triggers": ["<框架名>", "<关键技术>", ...],
  "content": {
    "skill_name": "<技能名称>",
    "level": "intermediate",
    "description": "<技能描述>",
    "key_concepts": ["概念1", "概念2"],
    "practical_tips": ["技巧1", "技巧2"],
    "common_mistakes": ["错误1", "错误2"]
  },
  "sources": ["<github_url>"],
  "tags": ["<标签>"],
  "created_at": "<ISO-8601>"
}
```

### 4. 跨分类存储

根据提取内容，可能同时存储到多个分类：

| 提取内容 | 存储分类 | 示例 |
|----------|----------|------|
| 框架使用方法 | `tech-stack` | React Hooks 使用规范 |
| 架构设计 | `pattern` | Feature-Based 架构 |
| 问题解决方案 | `problem` | CORS 跨域处理 |
| 测试方法 | `testing` | Jest + RTL 测试模式 |
| 通用技能 | `skill` | 代码组织技巧 |

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `scripts/fetch_github_info.py` | 获取 GitHub 仓库元数据 |
| `scripts/extract_knowledge.py` | 从仓库信息提取结构化知识 |
| `scripts/store_to_knowledge.py` | 存储到知识库对应分类 |

## 与其他组件的关系

```
github-to-skills
      │
      ▼ 存储知识
knowledge-base/skills/
      │
      ▼ 索引更新
knowledge-base/index.json (trigger_index)
      │
      ▼ 协调器调度
evolving-agent
      │
      ▼ 按需加载
programming-assistant (执行编程任务时自动获取相关知识)
```

## 使用示例

### 学习 React 项目

```
用户：学习这个仓库 https://github.com/facebook/react

AI 执行：
1. fetch_github_info.py https://github.com/facebook/react
2. extract_knowledge.py --input repo_info.json
3. store_to_knowledge.py --input extracted.json

结果：
- 存储 React 技术栈知识到 tech-stacks/react.json
- 存储 Fiber 架构模式到 patterns/fiber-architecture.json
- 存储 Hooks 编程技能到 skills/react-hooks.json
- 更新 index.json 触发索引
```

### 后续使用

```
用户：帮我实现一个 React 组件

AI（协调器）：
1. 检测到 "React" 关键词
2. 查询 knowledge-base: python knowledge_query.py --trigger react
3. 加载相关知识到上下文
4. 调用 programming-assistant 执行任务
```

## 渐进式加载

遵循项目的渐进式设计原则：
- **存储时**：完整存储所有提取的知识
- **加载时**：仅根据触发词加载相关条目
- **执行时**：按需展开详细内容

## 约束

- 不创建独立的 skill 文件夹（如 `~/.claude/skills/xxx/`）
- 所有知识存储到 `knowledge-base/` 统一管理
- 遵循 `schema.json` 定义的格式
- 通过触发词索引实现按需加载
