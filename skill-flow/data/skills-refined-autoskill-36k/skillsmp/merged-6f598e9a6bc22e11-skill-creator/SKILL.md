---
name: skill-creator
description: 使用此技能创建和优化新的技能，以扩展Claude的能力，涵盖从需求收集到发布的完整工作流。
---

# Skill Creator

## 什么是技能？

技能是模块化、自包含的软件包，通过提供专业知识、工作流程和工具来扩展Claude的能力。它们可以视为特定领域或任务的“入职指南”，将Claude从通用智能体转变为配备过程性知识的专业智能体。

## 使用方式

```bash
/evolve --new-skill "<skill-name>"
```

## 五阶段流程

### 阶段 1: 引导式访谈

向用户提问，收集需求：

1. **问题定义**：这个技能要解决什么问题？
2. **目标用户**：新手 / 进阶 / 专家？
3. **前置需求**：需要什么MCP服务器或CLI工具？
4. **参考来源**：有没有类似的技能可以参考？

输出：内部需求文件

### 阶段 2: 分析 + 生成

**搜索顺序**：

1. **优先搜索官方技能库**：
   - [claude-domain-skills](https://github.com/miles990/claude-domain-skills) — 领域知识技能
   - [claude-software-skills](https://github.com/miles990/claude-software-skills) — 软件开发技能
2. 如无适合，搜索GitHub上其他技能
3. **如都无适合参考，使用4C方法自行研究**：
   - 加载`methodology/knowledge-acquisition-4c`技能
   - **Collect**：WebSearch / WebFetch收集官方文档、最佳实践
   - **Curate**：筛选高质量来源，去除噪音
   - **Contextualize**：分析领域核心概念和常见流程
   - **Codify**：整理成技能可用的知识结构

**生成流程**：

4. 选择适合的模板（basic / advanced）
5. 生成SKILL.md初稿
6. 建立目录结构（如需要scripts/templates）

输出：完整的技能目录

### 阶段 3: 验证

检查清单：
- [ ] SKILL.md前置元数据格式正确
- [ ] 必要字段存在（name, description, version）
- [ ] 模拟使用情境，确认指令清楚
- [ ] 如有scripts，确认可执行

输出：验证报告

### 阶段 3.5: Token优化

使用`skill-optimizer`优化新建立的技能：

1. **分析token效率**：
   - 检查总行数（目标<300行）
   - 计算核心内容占比（目标>70%）
   - 识别可外连的内容（大型示例、ASCII图表、模板）

2. **执行优化**：
   - 大型ASCII图表 → 简化为单行描述
   - 完整示例（>20行）→ 外连至`extended/examples.md`
   - 模板（>10行）→ 外连至`extended/templates.md`
   - 配置示例 → 外连至扩展文件

3. **建立分层结构（如需要）**：
   ```
   skill-name/
   ├── SKILL.md           # 核心层 (< 300 行)
   └── extended/          # 扩展层 (按需载入)
       ├── examples.md
       └── templates.md
   ```

4. **验证优化结果**：
   - 优化前后行数比较
   - 确认功能完整性未受影响

输出：优化报告（节省X% tokens）

### 阶段 4: 发布到GitHub

1. 询问：建立新repo或加入现有repo？
2. 生成README.md
3. git init + commit + push
4. 输出安装指令

输出：
```
✅ Skill已发布！

GitHub: https://github.com/<user>/<repo>
安装: /plugin install <user>/<repo>
```

## 技能结构规范

```
skill-name/
├── SKILL.md              # 必需：核心指令文件
│   ├── YAML前置元数据
│   │   ├── name: 技能名称（必需）
│   │   └── description: 描述+触发条件（必需）
│   └── Markdown指令正文
└── 可选资源/
    ├── scripts/          # 可执行脚本
    ├── references/       # 参考文档
    └── assets/           # 模板、图标等
```

## 核心设计原则

### 1. 简洁为王

上下文窗口是宝贵资源，只添加Claude确实不具备的信息。

### 2. 设定适当的自由度

| 自由度 | 形式 | 适用场景 |
|--------|------|----------|
| **高** | 文本指令 | 有多种有效方法 |
| **中** | 伪代码或带参数的脚本 | 有首选模式但允许变化 |
| **低** | 特定脚本、少量参数 | 操作脆弱、错误成本高 |

## 验证脚本

```bash
./scripts/validate-skill.sh <skill-directory>
```

## 发布脚本

```bash
./scripts/publish-skill.sh <skill-directory> [--new-repo]
```

## Plugin格式转换

将Skills仓库转换为Claude Code Plugin Marketplace格式：

```bash
./scripts/convert-to-plugin.sh <skills-repo-path> [--marketplace|--category]
```