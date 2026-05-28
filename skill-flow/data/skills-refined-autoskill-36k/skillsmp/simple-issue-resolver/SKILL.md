---
name: simple-issue-resolver
description: Automatically implement simple GitHub Issues by analyzing requirements, writing code, running tests, and creating Pull Requests. Best for single-file modifications (under 50 lines), bug fixes, and small feature additions. Supports Java/Spring Boot, Python, JavaScript/TypeScript projects with existing test coverage.
---

# Simple Issue Resolver

## 概述

这个 Skill 能够自动化处理简单的 GitHub Issue，从需求分析到代码实现再到提交 PR，全流程自动化。

**核心价值**:
- 🚀 **快速响应**: 简单 Issue 从提交到 PR 创建，全程自动化，节省 80% 时间
- ✅ **质量保障**: 自动运行测试、代码检查，确保代码质量
- 📋 **规范流程**: 遵循 Git 工作流最佳实践，PR 描述自动生成
- 🎯 **聚焦价值**: 只处理简单场景，复杂 Issue 交给人工处理

**适用场景**:
- ✅ Bug 修复（单文件，逻辑清晰）
- ✅ 小功能添加（<50 行代码）
- ✅ 配置修改
- ✅ 文档更新
- ❌ 架构重构（建议人工）
- ❌ 数据库迁移（建议人工）
- ❌ 多模块交互（建议人工）

---

## 快速开始

### 基本用法

```
解决 Issue #123
```

或者

```
implement issue https://github.com/owner/repo/issues/456
```

Skill 会自动：
1. 读取 Issue 详情
2. 分析复杂度（如果太复杂会提醒）
3. 创建工作分支
4. 实现代码修改
5. 运行测试验证
6. 创建 Pull Request

---

## 工作流程

```
📥 输入 Issue 号码
    ↓
🔍 步骤1: 读取并分析 Issue
    ↓
📊 步骤2: 复杂度评估
    ↓
🚦 步骤3: 决策点
    ├─→ 简单 → 自动实现
    ├─→ 中等 → 询问确认
    └─→ 复杂 → 建议人工
    ↓
🌿 步骤4: 创建分支
    ↓
💻 步骤5: 实现代码
    ↓
✅ 步骤6: 测试验证
    ↓
🔄 步骤7: 迭代修复（如需要）
    ↓
📤 步骤8: 创建 PR
```

---

## 步骤详解

### 步骤1: Issue 分析

**目标**: 理解 Issue 要求，提取关键信息。

**执行**: 使用 `gh issue view {number}` 获取详情

**分析维度**:
1. **需求类型**: Bug修复 / 新功能 / 重构 / 文档
2. **影响范围**: 单一模块 / 跨模块 / 架构级  
3. **明确程度**: 清晰 / 需澄清 / 模糊

---

### 步骤2: 复杂度评估

**评估标准**:

| 维度 | 简单 | 中等 | 复杂 |
|------|------|------|------|
| **代码行数** | <50 | 50-200 | >200 |
| **文件数量** | 1个 | 2-5个 | >5个 |
| **模块影响** | 单模块 | 2-3模块 | 跨架构 |
| **技术难度** | 逻辑修改 | 算法优化 | 架构设计 |

**决策规则**:
- **简单**: ✅ 自动执行
- **中等**: ⚠️ 显示计划，等待确认
- **复杂**: ❌ 建议人工处理

---

### 步骤3: 创建分支

**命名规范**: `{type}/issue-{number}-{description}`

类型:
- `fix/` → Bug 修复
- `feature/` → 新功能
- `docs/` → 文档更新

示例: `fix/issue-123-email-validation`

---

### 步骤4: 代码实现

**实施原则**:
1. **最小修改**: 只改必要代码
2. **保持风格**: 遵循项目规范
3. **向后兼容**: 不破坏现有功能
4. **添加注释**: 说明修改原因

**定位文件方法**:
- 方法1: Issue 中提到的文件路径
- 方法2: 关键词搜索 (`grep -r`)
- 方法3: 代码语义搜索

---

### 步骤5: 测试验证

**测试层次**（按优先级）:

1. ✅ **编译检查**（P0）
   ```bash
   mvn clean compile  # Java
   ```

2. ✅ **单元测试**（P0）
   ```bash
   mvn test  # Java
   pytest    # Python
   npm test  # Node.js
   ```

3. ⭐ **代码风格**（P1）
   ```bash
   mvn checkstyle:check
   ```

**失败处理**: 最多迭代3次修复，超过则请求人工介入

---

### 步骤6: 创建 PR

**PR 描述模板**:

```markdown
Fixes #{issue_number}

## 📋 变更说明
{核心需求描述}

## 🔧 实现细节
**修改文件**: 
- `{file}`: {说明}

**代码行数**: +{add} -{del}

## ✅ 测试
- [x] 编译检查通过
- [x] 单元测试通过
- [x] 代码风格通过

## 📝 相关 Issue
- Closes #{issue_number}

## 🤖 自动化说明
此 PR 由 simple-issue-resolver 自动生成
```

**执行命令**:
```bash
git add .
git commit -m "fix: {描述} (fixes #{number})"
git push origin {branch}
gh pr create --title "..." --body "..."
```

---

## 复杂度控制

### ✅ 自动处理（无需确认）
- 代码 <50 行
- 单文件修改
- 有测试覆盖
- Bug 修复/文档更新

### ⚠️ 需要确认
- 代码 50-200 行
- 2-5 个文件
- 修改公共 API
- 新增依赖

### ❌ 建议人工
- 代码 >200 行
- 架构重构
- 数据库 schema 变更
- 安全敏感代码

---

## 配置要求

### 必须的工具
- [x] **Git** ≥2.30
- [x] **GitHub CLI (gh)** 
  ```bash
  gh auth login
  ```
- [x] **构建工具**: Maven/Gradle/npm/pip

### 推荐配置
- GitHub Personal Access Token
- 本地测试环境
- CI/CD 集成

---

## 参考资源

### 详细文档（按需加载）

1. **references/implementation-guide.md**
   - 何时读取: 步骤4（代码实现）
   - 内容: 编码规范、常见模式

2. **references/testing-checklist.md**
   - 何时读取: 步骤5（测试验证）
   - 内容: 测试设计、失败处理

3. **references/pr-template.md**
   - 何时读取: 步骤6（创建 PR）
   - 内容: PR 描述模板库

### 辅助脚本

- **scripts/issue_fetcher.py**: 获取 Issue 详情
- **scripts/pr_creator.py**: 创建 PR

---

## 常见问题

**Q1: Issue 描述不清晰怎么办？**

A1: 会在 Issue 评论中询问关键信息，或建议转人工处理。

**Q2: 测试失败怎么办？**

A2: 自动修复最多3次，超过则通知用户人工介入。

**Q3: 可以跳过测试吗？**

A3: 不推荐，但支持 `--skip-tests` 参数。会在 PR 中标注。

**Q4: 生成的 PR 有问题如何修改？**

A4: 两种方式：
1. 在 PR 评论告知，AI 追加修复
2. 本地检出分支手动修改

---

## 限制与注意

### ❌ 不支持
- 架构重构
- 数据库迁移
- 复杂业务逻辑
- 性能优化

### ⚠️ 安全提示
- AI 代码需人工审查
- 关键代码需充分测试
- 先在开发分支验证

---

## 版本信息

**版本**: v1.0  
**日期**: 2026-01-03  
**支持**: Java/Spring Boot, Python, JavaScript/TypeScript

---

**使用提示**: 
1. 首次使用选择简单 Bug 修复验证
2. 确保已配置 `gh` CLI
3. AI 代码仍需人工审查
