---
name: commit-conventions
description: Git 提交信息规范和最佳实践。用于编写清晰、规范的提交信息，遵循 Conventional Commits 标准。
allowed-tools: Bash, Read
---

# Git 提交规范

## Conventional Commits 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 基本格式
```
type(scope): subject
```

**示例**：
```
feat(auth): add login with OAuth
fix(api): handle null response in user endpoint
docs(readme): update installation instructions
```

## Type 类型

### 主要类型
- **feat**: 新功能
- **fix**: 修复 bug
- **docs**: 文档变更
- **style**: 代码格式（不影响代码运行）
- **refactor**: 重构（既不是新功能也不是修复）
- **perf**: 性能优化
- **test**: 添加或修改测试
- **chore**: 构建过程或辅助工具的变动

### 其他类型
- **build**: 构建系统或外部依赖变更
- **ci**: CI 配置文件和脚本变更
- **revert**: 回滚之前的提交

## Scope 范围

指明改动的范围，可选但推荐使用。

**示例**：
- `feat(auth)`: 认证模块
- `fix(api)`: API 层
- `docs(readme)`: README 文件
- `style(button)`: Button 组件
- `refactor(utils)`: 工具函数

**常见 scope**：
- 组件名：`button`, `modal`, `navbar`
- 模块名：`auth`, `api`, `database`
- 文件名：`readme`, `config`, `package`
- 功能名：`login`, `checkout`, `search`

## Subject 主题

### 规则
- 使用祈使句，现在时："add" 而不是 "added" 或 "adds"
- 首字母小写
- 结尾不加句号
- 简洁明了，一般不超过 50 字符

### 示例
```
✅ 好的 subject
feat(auth): add OAuth login support
fix(api): handle empty response
docs(readme): update setup instructions

❌ 不好的 subject
feat(auth): Added OAuth login support.
fix(api): Fixed a bug
docs: updated readme
```

## Body 正文

详细描述改动的内容、原因和影响。

### 规则
- 与 subject 之间空一行
- 使用祈使句，现在时
- 解释"为什么"而不只是"做了什么"
- 可以分多段

### 示例
```
feat(auth): add OAuth login support

Implement OAuth 2.0 authentication flow to allow users to login
with their Google or GitHub accounts.

This change improves user experience by reducing friction in the
signup process and eliminates the need to remember another password.

Changes include:
- Add OAuth provider configuration
- Implement callback handler
- Update user model to support OAuth tokens
- Add UI for OAuth login buttons
```

## Footer 页脚

用于关联 issue、标记破坏性变更等。

### Breaking Changes
```
feat(api): change response format

BREAKING CHANGE: API response format changed from array to object.
Clients need to update their code to handle the new format.

Before: GET /users returns [{ id: 1, name: 'John' }]
After: GET /users returns { data: [{ id: 1, name: 'John' }] }
```

### 关联 Issue
```
fix(auth): prevent duplicate login requests

Fixes #123
Closes #456
Related to #789
```

## 完整示例

### 示例 1：新功能
```
feat(checkout): add promo code support

Allow users to apply promo codes during checkout to receive
discounts on their orders.

Implementation includes:
- Add promo code input field
- Validate promo codes against database
- Calculate and display discount
- Update order total

Closes #234
```

### 示例 2：Bug 修复
```
fix(cart): prevent negative quantities

Add validation to ensure cart item quantities cannot be negative.
This fixes an issue where users could exploit the quantity input
to create negative totals.

Fixes #567
```

### 示例 3：重构
```
refactor(api): extract validation logic

Move validation logic from controllers to separate validator
functions to improve code reusability and testability.

No functional changes.
```

### 示例 4：破坏性变更
```
feat(api): migrate to REST API v2

BREAKING CHANGE: API endpoints have been updated to v2.

Changes:
- All endpoints now use /api/v2 prefix
- Response format changed to include metadata
- Authentication now requires Bearer token

Migration guide: docs/migration-v2.md

Closes #890
```

## 提交最佳实践

### 1. 原子提交
每个提交应该是一个独立的、完整的改动。

```
✅ 好 - 每个提交一个功能
feat(auth): add login form
feat(auth): add password validation
feat(auth): add remember me option

❌ 不好 - 一个提交多个不相关的改动
feat(auth): add login, fix navbar, update readme
```

### 2. 提交频率
- 经常提交，保持提交小而专注
- 每个逻辑改动一个提交
- 不要等到一天结束才提交

### 3. 提交前检查
```bash
# 查看改动
git diff

# 查看暂存的改动
git diff --cached

# 查看状态
git status
```

### 4. 修改最后一次提交
```bash
# 修改提交信息
git commit --amend -m "new message"

# 添加遗漏的文件
git add forgotten-file.js
git commit --amend --no-edit
```

### 5. 交互式暂存
```bash
# 选择性暂存改动
git add -p

# 暂存部分文件
git add file1.js file2.js
```

## 团队规范

### 提交信息模板
创建 `.gitmessage` 文件：
```
# <type>(<scope>): <subject>
# |<----  最多 50 字符  ---->|

# 解释为什么做这个改动
# |<----   每行最多 72 字符   ---->|

# 关联的 issue
# Fixes #
# Closes #
# Related to #

# --- COMMIT END ---
# Type 可以是:
#   feat     : 新功能
#   fix      : 修复 bug
#   docs     : 文档变更
#   style    : 代码格式
#   refactor : 重构
#   perf     : 性能优化
#   test     : 测试
#   chore    : 构建/工具变更
```

配置模板：
```bash
git config --global commit.template ~/.gitmessage
```

### 提交钩子
使用 `husky` 和 `commitlint` 强制规范：

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky
```

`commitlint.config.js`:
```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'chore',
        'revert'
      ]
    ],
    'subject-case': [2, 'never', ['upper-case']],
    'subject-max-length': [2, 'always', 50]
  }
};
```

## 常见错误

### ❌ 错误 1：提交信息太模糊
```
fix: bug fix
update: changes
```

### ✅ 正确
```
fix(auth): prevent session timeout on page refresh
refactor(api): extract user validation logic
```

### ❌ 错误 2：一个提交包含多个不相关改动
```
feat: add login page, fix navbar bug, update readme
```

### ✅ 正确
```
feat(auth): add login page
fix(navbar): correct mobile menu alignment
docs(readme): update installation steps
```

### ❌ 错误 3：提交信息使用过去时
```
feat(auth): added login feature
fixed bug in api
```

### ✅ 正确
```
feat(auth): add login feature
fix(api): handle null response
```

## 工具推荐

### Commitizen
交互式提交工具：
```bash
npm install -g commitizen
commitizen init cz-conventional-changelog --save-dev --save-exact

# 使用
git cz
```

### Commitlint
提交信息校验：
```bash
npm install --save-dev @commitlint/{cli,config-conventional}
```

### Husky
Git hooks 管理：
```bash
npm install --save-dev husky
npx husky install
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'
```

## 查看提交历史

```bash
# 查看提交历史
git log --oneline

# 按类型过滤
git log --oneline --grep="^feat"

# 查看某个文件的历史
git log --oneline -- path/to/file

# 美化输出
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'
```

## 生成 CHANGELOG

使用 `standard-version` 自动生成：
```bash
npm install --save-dev standard-version

# 生成 changelog 并打 tag
npm run release
```

## 总结

好的提交信息应该：
1. 遵循统一的格式
2. 清晰描述改动内容
3. 解释改动原因
4. 保持简洁明了
5. 便于追踪和回滚
