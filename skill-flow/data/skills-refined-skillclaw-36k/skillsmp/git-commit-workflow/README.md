# Git Commit Workflow Skill

智能化的 Git 提交流程工具，支持中文团队规范，包含 PMS 单号和 GitHub Issue 追踪功能。

## 设计理念

采用"零脚本依赖"架构：
- **智能化解析**：AI 直接理解 PMS URL 和 GitHub Issue 格式，无需脚本处理
- **完全通用**：只有 Bash 命令调用，可在任何支持 Git 的 AI Agent 中使用
- **用户中心**：强制确认流程，用户完全掌控提交内容

## 架构概览

```
用户请求 → 主 Agent → git-commit-workflow Skill
                                  ↓
                            检查 Git 状态
                                  ↓
                            交互式文件选择
                                  ↓
                            AI 智能解析 PMS/Issue
                                  ↓
                            生成结构化提交信息
                                  ↓
                            用户确认
                                  ↓
                            执行提交
```

## 功能特性

- 📊 **智能状态检查** - 自动分析 Git 仓库状态，区分暂存和未暂存文件
- 🎯 **交互式暂存** - 让用户自主选择要提交的文件
- 📝 **结构化提交信息** - 生成符合规范的中英文双语提交信息
- 🔗 **PMS 单号智能解析** - AI 自动识别并解析 PMS URL 或直接输入的单号
- 🔐 **GitHub Issue 智能解析** - AI 自动识别并解析 Issue URL 或直接输入
- ✅ **强制确认流程** - 确保每次提交都经过用户明确确认
- 🚀 **零脚本依赖** - 完全通用，无需任何辅助脚本或编译
- 📏 **严格格式约束** - Body 行不超过 80 字符，中英文成对出现

## 使用方法

### 基本用法

在 OpenCode 中，直接输入：

```
帮我提交代码
```

或使用英文：

```
commit changes
```

或查看状态：

```
查看 git 状态
```

### 完整工作流程

1. **检查状态** - 运行 `git status --porcelain` 分析仓库状态
2. **选择文件** - 用户交互式选择要暂存的文件
3. **暂存文件** - 运行 `git add <files>` 暂存选定的文件
4. **查看差异** - 运行 `git diff --staged` 展示暂存变更
5. **生成草稿** - AI 根据变更自动生成结构化提交信息
6. **确认 PMS/Issue** - 询问用户，AI 智能解析 URL 或单号格式
7. **用户确认** - 展示完整提交草稿，等待用户确认或修改
8. **执行提交** - 运行 `git commit -m "<message>"` 完成提交

## 提交信息格式

提交信息遵循以下规范格式：

```
<type>[optional scope]: <English description>

[English body - optional, max 80 chars per line]

[Chinese body - optional, max 80 chars per line, must pair with English]

Log: <简洁的中文描述>
PMS: <BUG-number or TASK-number>
Issue: Fixes #<number> or owner/repo#<number>
Influence: <用中文说明影响范围>
```

### 类型（type）说明

- `feat` - 新功能
- `fix` - 修复 bug
- `docs` - 文档修改
- `style` - 代码格式调整（不影响功能）
- `refactor` - 重构（不是新功能也不是修复）
- `perf` - 性能优化
- `test` - 增加测试
- `chore` - 构建、工具、依赖等辅助修改

### 格式约束

- Title 行：`type: English description`
- Body 行：每行不超过 80 字符
- 中英文成对：如果提供英文 body，必须提供对应的中文 body
- Log：简洁的中文总结
- PMS：格式为 `BUG-XXXXX` 或 `TASK-XXXXX`
- Issue：格式为 `Fixes #XXX` 或 `Fixes owner/repo#XXX`

## 智能解析能力

### PMS 单号解析

AI 可以从以下格式中自动提取 PMS 单号：

1. **完整 URL**：
   ```
   https://pms.example.com/BUG-12345
   → 提取：BUG-12345
   ```

2. **单号直接输入**：
   ```
   BUG-12345
   TASK-67890
   → 直接使用
   ```

3. **不带前缀的数字**：
   ```
   12345
   → 智能推断：BUG-12345 或 TASK-12345（根据上下文）
   ```

### GitHub Issue 解析

AI 可以从以下格式中自动提取 Issue 信息：

1. **完整 URL**：
   ```
   https://github.com/owner/repo/issues/123
   → 提取：Fixes owner/repo#123
   ```

2. **简写格式**：
   ```
   owner/repo#123
   → 直接使用
   ```

3. **本地仓库 Issue**：
   ```
   #123
   → 通过 `git remote get-url origin` 推断仓库
   → 提取：Fixes #123
   ```

## 目录结构

```
git-commit-workflow/
├── SKILL.md                    # 主要工作流程指南（AI 完全按照此文件执行）
├── README.md                   # 本说明文档
└── templates/
    └── commit-examples.md      # 提交格式示例和类型参考
```

## 依赖要求

- ✅ 系统安装了 `git` 命令（唯一要求）
- ✅ 支持任何 AI Agent（Gemini、Claude、GPT 等）
- ❌ 无需任何脚本
- ❌ 无需编译
- ❌ 无需特定编程语言支持

## 工作原理

### AI 职责

AI Agent 按照 `SKILL.md` 中的指导执行：

- ✅ 直接运行 bash 命令（`git status`, `git add`, `git diff`, `git commit`）
- ✅ 智能解析 PMS URL 和 Issue URL（无需脚本，AI 自己理解格式规则）
- ✅ 生成结构化提交信息（遵循中英文双语规范）
- ✅ 获取用户确认（绝不自动提交）
- ✅ 处理边界情况（初始提交、空暂存区等）

### 无脚本的原因

- **PMS 解析**：AI 理解 URL 格式规则（正则模式），提取数字并添加前缀
- **Issue 解析**：AI 通过 `git remote get-url origin` 检查仓库上下文，推断完整的 Issue 标识
- **纯文本指导**：所有逻辑直接嵌入在 `SKILL.md` 的指导中，AI 自然语言理解

## 测试

在任何 Git 仓库中测试：

```bash
# 查看技能是否激活（在 AI 对话中）
"请帮我检查 git 状态"

# 完整提交流程测试
"帮我修改一个文件并提交"
```

测试场景：

1. **正常提交**：修改文件 → 暂存 → 生成提交信息 → 确认 → 提交
2. **PMS 解析测试**：输入 PMS URL 或单号，验证 AI 正确提取
3. **Issue 解析测试**：输入 GitHub Issue URL，验证 AI 正确格式化
4. **边界情况**：初始提交、空暂存区、无变更

## 常见问题

### Q: 为什么需要中英文双语？

A: 符合国际化团队的协作规范，英文便于国际开发者理解，中文便于本地团队交流。中英文成对出现确保信息完整性。

### Q: Body 行的 80 字符限制？

A: 遵循 Git 提交信息的最佳实践，确保在各种 Git 客户端（命令行、GitHub、GitLab 等）中都能良好显示。

### Q: 如何确保 PMS 单号正确？

A: 采用多重验证机制：
  1. 用户输入后展示解析结果
  2. 展示完整提交草稿前二次确认
  3. 用户可以修改解析结果

### Q: 支持哪些 Git 仓库？

A: 任何 Git 仓库都支持：
- GitHub
- GitLab
- Gitee
- 自建 Git 服务器
- 本地仓库

### Q: 能否跳过 PMS/Issue 字段？

A: 可以。如果项目中不使用 PMS 或 GitHub Issue，可以选择不填写这两个字段。

### Q: 提交失败会怎么办？

A:
  1. AI 会捕获错误信息
  2. 分析失败原因（暂存区为空、冲突等）
  3. 提供修正建议
  4. 等待用户决策

## 注意事项

- ⚠️ **永远不会自动提交** - 总是等待用户明确确认后才执行 `git commit`
- 📢 **提供反馈机会** - 用户可以修改提交信息草稿的任何部分
- 🔧 **处理特殊情况** - 支持初始提交、空暂存区、无变更等边界情况
- 📏 **遵守约束** - Body 行不超过 80 字符，中英文成对出现
- 🌐 **完全通用** - 任何支持 Bash 工具的 AI Agent 都可以使用

## 与其他工具的对比

| 特性 | Git Commit Workflow | 传统 git commit | Git Commitizen |
|------|---------------------|-----------------|----------------|
| **自动化程度** | 半自动（AI 辅助） | 手动 | 全自动 |
| **PMS 集成** | ✅ 智能解析 | ❌ | ❌ |
| **Issue 追踪** | ✅ 智能解析 | ❌ | 部分 |
| **中英文双语** | ✅ 支持 | ❌ | ❌ |
| **格式约束** | ✅ 自动检查 | ❌ | ✅ |
| **交互确认** | ✅ 强制确认 | N/A | 可选 |
| **零依赖** | ✅ 仅 git | ✅ 仅 git | ❌ 需要 Node.js |
| **学习成本** | 低 | 中 | 低 |

## 进阶使用

### 自定义提交类型

可以在 `templates/commit-examples.md` 中查看更多提交类型示例，根据项目需求添加自定义类型。

### 批量提交

AI 支持处理多个文件的批量提交：
1. 选择要提交的所有文件
2. 生成统一的提交信息
3. 用户确认后一次性提交

### 撤销提交

如果提交有误，可以在 AI 对话中请求撤销：

```
撤销最后一次提交
```

AI 会执行：
- `git reset --soft HEAD~1`（保留更改）
- 或 `git reset --hard HEAD~1`（丢弃更改）

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关资源

- **Git 提交信息规范**：https://www.conventionalcommits.org/
- **Commitizen 文档**：https://commitizen-tools.github.io/commitizen/
- **Git 最佳实践**：https://github.com/agis/git-style-guide
