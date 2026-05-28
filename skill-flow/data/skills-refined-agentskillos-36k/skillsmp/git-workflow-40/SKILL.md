---
name: git-workflow
description: Git 工作流，包含 commit 信息生成和 PR 审查。
当需要写 commit message、创建/审查 Pull Request 时使用。
Use when writing commit messages, creating PRs, or reviewing pull requests.
allowed-tools: "Bash,Read,Write,Grep"
---

# Git Workflow - Git 工作流

Git commit 信息生成和 Pull Request 审查。

## 🎯 适用范围

**使用此技能**：
- ✅ 生成规范的 commit message
- ✅ 创建 Pull Request
- ✅ 审查代码变更
- ✅ 代码审查清单

---

## 📝 Commit Message 规范

### Conventional Commits 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): add OAuth login` |
| `fix` | 修复 bug | `fix(api): handle null response` |
| `docs` | 文档变更 | `docs(readme): update install guide` |
| `style` | 格式调整 | `style: fix indentation` |
| `refactor` | 重构 | `refactor(user): simplify validation` |
| `perf` | 性能优化 | `perf(query): add caching` |
| `test` | 测试相关 | `test(auth): add login tests` |
| `chore` | 构建/工具 | `chore: update deps` |

### Subject 主体

```bash
# ❌ 错误
"fixed bug"
"update"
"add stuff"

# ✅ 正确
"fix(auth): resolve token expiration issue"
"feat(api): add pagination to user list"
"docs: clarify API rate limits"
```

**规则**：
- 使用动词原形
- 小写
- 不超过 50 字符
- 不以句号结尾

### Body 正文

```
# 详细描述变更内容

- Closes #123
- Refs #456
- Breaking change: API endpoint renamed from /user to /users
```

---

## Commit Message 生成流程

### 步骤 1：分析变更

```bash
# 查看暂存的变更
git diff --staged

# 或查看当前变更
git diff
```

### 步骤 2：识别变更类型

| 变更内容 | Type |
|----------|------|
| 新增功能 | `feat` |
| 修复 bug | `fix` |
| 文档更新 | `docs` |
| 格式调整 | `style` |
| 重构代码 | `refactor` |
| 性能优化 | `perf` |
| 测试相关 | `test` |
| 构建/配置 | `chore` |

### 步骤 3：生成 message

```bash
# 示例输入
"修改了用户登录的验证逻辑，修复了 token 过期的问题"

# 输出
fix(auth): resolve token expiration issue

- Check token expiration before validation
- Add refresh token mechanism
- Update error handling for expired tokens

Closes #42
```

---

## Pull Request 审查

### PR 审查清单

#### 1. 功能正确性

- [ ] 实现符合需求/spec
- [ ] 边界条件已处理
- [ ] 错误处理完善
- [ ] 无明显 bug

#### 2. 代码质量

- [ ] 命名清晰
- [ ] 逻辑易懂
- [ ] 无重复代码
- [ ] 遵循项目风格

#### 3. 测试覆盖

- [ ] 新功能有测试
- [ ] 修改不影响现有测试
- [ ] 测试覆盖率维持/提升

#### 4. 性能与安全

- [ ] 无明显性能退化
- [ ] 无安全漏洞
- [ ] 敏感数据处理正确

#### 5. 文档

- [ ] API 文档更新
- [ ] README 更新（如需要）
- [ ] 变更日志更新

### PR 审查流程

```bash
# 1. 获取 PR 信息
gh pr view 123

# 2. 查看变更
gh pr diff 123

# 3. 检查 CI 状态
gh pr checks 123

# 4. 添加评论
gh pr comment 123 --body "Review comments..."

# 5. 批准/请求修改
gh pr review 123 --approve
# 或
gh pr review 123 --request-changes
```

---

## PR 审查意见模板

### 通过模板

```markdown
## ✅ LGTM

变更符合要求，代码质量良好。

### 小建议
- （可选）非阻塞改进建议

### 下一步
可以合并。
```

### 需要修改模板

```markdown
## 🔄 Request Changes

总体方向正确，但需要解决以下问题：

### 必须修复
- [ ] **问题 1**: 具体描述...
  - 位置: `file.ts:42`
  - 建议: 如何修复

### 建议改进
- [ ] **改进 1**: 非阻塞建议...

### 修改后
请提交新 commits 或 squash 当前 commits。
```

---

## 命令参考

```bash
# Commit 相关
git add .
git commit -m "feat(scope): description"

# 修改最后一次 commit
git commit --amend

# 修改 commit message
git commit --amend -m "new message"

# PR 相关
gh pr create --title "feat: add feature" --body "Description..."
gh pr list
gh pr view 123
gh pr diff 123
gh pr review 123 --approve
gh pr merge 123 --squash

# Git 工作树（并行开发）
git worktree add ../feature-branch feature-branch
git worktree list
git worktree remove ../feature-branch
```

---

## 常见触发场景

使用此技能时，你会听到：
- "生成 commit message"
- "写个 commit"
- "审查这个 PR"
- "Review PR"
- "Code review"
- "Create pull request"
