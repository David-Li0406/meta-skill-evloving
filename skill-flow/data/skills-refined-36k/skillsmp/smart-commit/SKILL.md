---
name: smart-commit
description: 智能分组提交代码。按功能/模块划分未提交的代码，分批次有条理地 commit。当用户提到"提交"、"commit"、"分组提交"、"smart commit"时使用。
allowed-tools: Bash, Read, Glob, Grep, TodoWrite, AskUserQuestion
---

# 智能分组提交 - X-CLI 项目

按功能或模块划分当前未提交的代码，分批次创建有条理的 commit 记录。

## 核心约束

1. **禁止 AI 共同作者信息** - commit message 中不得包含任何 `Co-Authored-By` 或类似的 AI 生成标识
2. **使用 git config 作者** - 保持当前 git 配置的 user.name 和 user.email 作为提交作者
3. **代码安全优先** - 遇到 husky 预处理失败时，必须确保代码不丢失
4. **原子化提交** - 每个 commit 应该是一个独立的功能单元
5. **遵循 Conventional Commits** - 项目使用 `@commitlint/config-conventional` 规范

## 执行流程

### 第一步：收集信息

```bash
# 查看当前 git 用户配置
git config user.name
git config user.email

# 查看所有未提交的变更（不使用 -uall 避免大仓库内存问题）
git status

# 查看未暂存的变更
git diff --stat

# 查看已暂存的变更
git diff --cached --stat

# 查看最近的 commit 风格
git log --oneline -10
```

### 第二步：分析变更并分组

根据 X-CLI 项目结构对变更进行分组：

#### 1. 按目录/模块分组

| 目录                          | Scope          | 说明             |
| ----------------------------- | -------------- | ---------------- |
| `bin/`                        | `bin`          | CLI 入口文件     |
| `common/command/new/`         | `new`          | 项目创建命令     |
| `common/command/plugin/`      | `plugin`       | 插件管理命令     |
| `common/command/create/`      | `create`       | 组件创建命令     |
| `common/command/remove/`      | `remove`       | 组件删除命令     |
| `common/command/xi/`          | `xi`           | 安装命令         |
| `common/command/xu/`          | `xu`           | 卸载命令         |
| `common/command/xr/`          | `xr`           | 运行命令         |
| `common/constants/`           | `constants`    | 常量配置         |
| `common/utils/`               | `utils`        | 工具函数         |
| `common/utils/manager/`       | `manager`      | 包管理器         |
| `esbuild.config.js`           | `build`        | 构建配置         |
| `package.json`                | `deps`         | 依赖管理         |
| `readme.md`, `*.md`           | `docs`         | 文档             |
| `.commitlintrc`, `.czrc` 等   | `config`       | 项目配置         |
| `.husky/`, `.lintstagedrc`    | `hooks`        | Git hooks 配置   |

#### 2. 按功能类型分组

| Type       | 说明                              |
| ---------- | --------------------------------- |
| `feat`     | 新功能                            |
| `fix`      | Bug 修复                          |
| `refactor` | 代码重构（不改变功能）            |
| `style`    | 样式/格式调整（空格、分号等）     |
| `docs`     | 文档更新                          |
| `chore`    | 构建/工具/配置变更                |
| `test`     | 测试相关                          |
| `perf`     | 性能优化                          |
| `revert`   | 回滚提交                          |

#### 3. 常见分组场景

- **删除功能**: 多个相关文件被删除时，归为一个 `refactor` 或 `chore` 提交
- **新增插件**: 插件目录下的新增文件归为一个 `feat(plugin)` 提交
- **修复命令**: 特定命令的修改归为 `fix(<command>)` 提交
- **配置更新**: 配置文件变更归为 `chore(config)` 提交

### 第三步：与用户确认分组方案

使用 AskUserQuestion 工具向用户展示分组方案并确认：

```
建议将变更分为以下 N 个 commit:

1. refactor(create): 移除 create 命令相关代码
   - common/command/create/create.js (deleted)
   - common/command/create/templates/*.js (deleted)

2. feat(manager): 添加 bun 包管理器支持
   - common/utils/manager/bun.js (new)
   - common/utils/manager/manager.js (modified)

请确认或调整分组方案。
```

### 第四步：逐个提交

对每个分组执行：

```bash
# 1. 先重置暂存区（如果需要）
git reset HEAD

# 2. 添加该分组的文件
git add <file1> <file2> ...

# 3. 提交（使用 HEREDOC 确保格式正确，不带 Co-Authored-By）
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>
EOF
)"
```

## Commit Message 规范

### 格式

```
<type>(<scope>): <subject>

[可选的正文]
```

- `type`: 必填，见上方类型表
- `scope`: 可选，表示影响范围
- `subject`: 必填，简短描述（不超过 72 字符）

### 示例

```
feat(plugin): add eslint plugin auto-configuration

fix(manager): resolve pnpm detection on Windows

refactor(new): simplify project template generation

chore: update dependencies

docs: update CLI usage in readme
```

## 错误处理：Husky 预处理失败

本项目的 pre-commit hook 配置为始终通过（exit 0），但如果遇到 lint-staged 报错：

### 1. 保存当前状态

```bash
# 查看当前暂存的文件
git diff --cached --name-only

# 创建临时 stash 备份
git stash push -m "backup-before-fix-$(date +%Y%m%d-%H%M%S)"
```

### 2. 手动修复格式问题

```bash
# 运行 prettier 格式化
npx prettier --write <files>
```

### 3. 恢复并重新提交

```bash
# 恢复 stash
git stash pop

# 重新添加并提交
git add <files>
git commit -m "<message>"
```

## 安全措施

1. **提交前备份** - 复杂操作前创建 stash 备份
2. **分步执行** - 每个 commit 后验证 `git status`
3. **回滚方案**:
   ```bash
   # 撤销最后一次 commit（保留变更）
   git reset --soft HEAD~1

   # 撤销 add（保留变更）
   git reset HEAD <file>
   ```

## 禁止事项

- **禁止** 在 commit message 中添加 `Co-Authored-By` 或任何 AI 相关信息
- **禁止** 修改 git config 的 user 信息
- **禁止** 使用 `--amend` 修改已推送的 commit
- **禁止** 使用 `--force` 强制推送
- **禁止** 跳过 hooks（`--no-verify`）除非用户明确要求
- **禁止** 在没有备份的情况下执行可能丢失代码的操作

## 输出格式

每次提交后输出：

```
✓ Commit 1/N: <type>(<scope>): <description>
  - <file1>
  - <file2>
  SHA: <short-sha>

✓ Commit 2/N: <type>(<scope>): <description>
  ...

提交完成！共创建 N 个 commit。
```

## 特殊场景处理

### 大量文件删除

当存在大量文件删除时，按功能模块归类：

```bash
# 删除整个目录
git add common/command/create/
git commit -m "refactor: remove create command (moved to separate package)"
```

### 混合变更（新增+修改+删除）

优先按功能关联分组，而非按操作类型：

```bash
# 同一功能的增删改放在一起
git add common/utils/manager/bun.js common/utils/manager/manager.js common/constants/manager.const.js
git commit -m "feat(manager): add bun package manager support"
```

### 仅配置文件变更

配置类变更可以合并为一个 commit：

```bash
git add .commitlintrc .czrc .prettierrc
git commit -m "chore(config): update linting configuration"
```
