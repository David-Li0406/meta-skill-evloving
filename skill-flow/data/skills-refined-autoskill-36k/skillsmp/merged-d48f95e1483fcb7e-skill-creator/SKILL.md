---
name: skill-creator
description: 使用此技能创建和优化 Claude Code Skills，遵循 Testany 公司的规范。
---

# Skill Creator

帮助创建符合 Testany 规范的 Claude Code Skills。

## 触发词

- "帮我创建一个 skill"
- "把这个变成 skill"
- "新建技能"
- "/create-skill"

## Skill 核心概念

Skill 是模块化的能力包，用于扩展 Claude 的能力：
- **专业工作流**：多步骤的领域流程
- **工具集成**：特定文件格式或 API 的使用方法
- **领域知识**：公司特定知识、schema、业务逻辑
- **打包资源**：脚本、参考文档、资产文件

## 目录结构

```
skill-name/
├── SKILL.md          # 必须 - 核心指令
└── 可选资源/
    ├── scripts/      # 可执行脚本（Python/Bash）
    ├── references/   # 参考文档（按需加载）
    └── assets/       # 输出资源（模板、图标）
```

## SKILL.md 格式

```yaml
---
name: skill-name
description: 触发词1、触发词2。功能描述，说明什么时候使用这个 skill。
---
```

### Body

- 使用中文撰写
- 简洁明了，< 500 行
- 包含使用示例
- 引用 references 时说明何时读取

## 创建流程

### 步骤 1：理解需求
- 这个 skill 要支持什么功能？
- 用户会怎么使用它？
- 什么话会触发这个 skill？

### 步骤 2：规划资源
- 需要脚本吗？放 `scripts/`
- 需要参考文档吗？放 `references/`
- 需要模板/资产吗？放 `assets/`

### 步骤 3：初始化 Skill

```bash
scripts/init_skill.py <skill-name>
```

脚本默认输出到 `skills/` 目录，会创建：
- SKILL.md 模板
- 示例目录结构（scripts/、references/、assets/）

### 步骤 4：编写 SKILL.md
- Frontmatter：清晰的 name + 全面的 description
- Body：使用 skill 和资源的指令

### 步骤 5：验证

```bash
scripts/quick_validate.py skills/<skill-name>
```

检查项：
- Frontmatter 格式
- 行数限制
- 触发词存在

### 步骤 6：人工审核
验证通过后，提交人工审核：
- 功能完整性
- 文档清晰度
- 示例有效性

## 示例：创建一个简单 skill

**用户**：帮我把"渲染公众号文章"变成 skill

**执行**：
1. 创建目录 `.claude/skills/render-article/`
2. 编写 SKILL.md
3. 测试触发词是否有效

## 常见问题

### Q: references 和 assets 的区别？
- **references/**：供 Claude 参考的文档，会加载到 context
- **assets/**：输出资源（图片、模板），不加载到 context

### Q: SKILL.md 太长怎么办？
拆分到 references/，在 SKILL.md 中引用并说明何时读取。

### Q: 如何测试 skill？
1. 运行 `quick_validate.py` 验证格式
2. 实际使用测试功能
3. 根据反馈迭代改进

*参考：[官方 Skill 仓库](https://github.com/anthropics/skills)*