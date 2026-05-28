---
name: git-workflow
description: 使用此技能以确保团队遵循标准化的 Git 分支命名和提交规范，促进高效的版本控制和协作。
---

# Git Workflow Skill

> **版本控制是工程的基石**
> 清晰的提交历史 = 可追溯的项目演进

---

## 🌿 分支策略

### 标准分支

| 分支 | 用途 | 保护 |
|:---|:---|:---|
| `main` | 生产代码 | ✅ 保护 |
| `develop` | 开发主线 | ✅ 保护 |
| `feature/*` | 功能开发 | ❌ |
| `bugfix/*` | Bug修复 | ❌ |
| `hotfix/*` | 紧急修复 | ❌ |
| `release/*` | 发布准备 | ❌ |

### 分支命名

标准格式：
```
<type>/<developer-name>/<feature-description>
```

### 分支类型 (type)

- **feat**: 新功能开发
- **fix**: 错误修复
- **refactor**: 程序重构
- **docs**: 文档更新
- **style**: 样式调整
- **test**: 测试相关
- **chore**: 雜項任務

### 实际示例

```bash
# 功能分支
git checkout -b feature/user-authentication
# Bug修复
git checkout -b bugfix/login-redirect-issue
# 热修复
git checkout -b hotfix/critical-security-patch
```

---

## 📝 提交规范

### Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交类型

| Type | 用途 |
|:---|:---|
| `feat` | 新功能 |
| `fix` | Bug修复 |
| `docs` | 文档更新 |
| `style` | 格式调整（不影响代码） |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建/工具相关 |

### 提交检查清单

- [ ] 提交信息是否清晰？
- [ ] 是否只包含相关修改？
- [ ] 是否需要拆分成多个提交？
- [ ] 是否影响现有功能？

---

## 🔄 工作流程

### 1. 开始新功能

```bash
# 从 develop 创建分支
git checkout develop
git pull origin develop
git checkout -b <type>/<developer-name>/<feature-description>
```

### 2. 修复 Bug

```bash
# 从 develop 创建分支
git checkout -b bugfix/login-issue develop
```

### 3. 紧急修复

```bash
# 从 main 创建
git checkout -b hotfix/security-patch main
```

### 4. 提交变更

```bash
# 定期提交变更
git add .
git commit -m "<type>(<scope>): <description>"
```

### 5. 推送和创建 PR

```bash
git push -u origin <branch-name>
# 创建 Pull Request
```

---

## 🔙 回滚策略

### 回滚单个提交

```bash
git revert <commit-hash>
```

### 回滚到特定版本

```bash
git reset --soft <commit-hash>  # 软回滚
git reset --hard <commit-hash>  # 硬回滚
```

---

## 📋 PR 检查清单

创建 Pull Request 前：

- [ ] 代码已本地测试
- [ ] 提交历史清晰
- [ ] 无调试代码（console.log）
- [ ] 已更新文档（如需要）
- [ ] 已添加测试（如需要）
- [ ] 符合代码规范

---

## ⚠️ 禁止操作

```bash
# 禁止在 main 上直接修改
git checkout main
git commit ...  # 禁止！

# 禁止 force push 保护分支
git push -f origin main  # 禁止！
```

---

## 常见问题

### Q: 如何处理长时间开发的功能？

A: 建立 feature 分支，定期从 main rebase，完成后再合并。

### Q: 可以在分支名称中使用 issue 编号吗？

A: 可以，格式: `feat/lip/add-feature-#123`

---

## 参考资源

- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

**核心**: 小步提交、清晰历史、保护主干 | **规范**: Conventional Commits