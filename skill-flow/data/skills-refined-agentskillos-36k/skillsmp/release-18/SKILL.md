---
name: release
description: cloudflare-operator 新版本发布。处理版本升级、变更日志、Git 标签和 GitHub 发布。适用于发布新版本、创建标签或发布发行版。
allowed-tools: Read, Edit, Bash, Grep
user-invocable: true
---

# 发布流程

## 概述

此技能指导 cloudflare-operator 的发布流程，包括版本升级、Git 标签创建和 GitHub 发布。

## 发布前检查清单

```bash
# 1. 确保所有测试通过
make fmt vet test lint build

# 2. 检查当前版本
grep "VERSION ?=" Makefile

# 3. 获取最新标签
git tag --sort=-v:refname | head -5

# 4. 检查未提交的变更
git status
```

## 发布步骤

### 步骤 1：确定版本号

遵循语义化版本：
- **MAJOR** (x.0.0)：破坏性 API 变更
- **MINOR** (0.x.0)：新功能，向后兼容
- **PATCH** (0.0.x)：Bug 修复，向后兼容

当前版本格式：`v0.17.X`

### 步骤 2：更新 Makefile 中的版本

```bash
# 编辑 Makefile
sed -i '' 's/VERSION ?= .*/VERSION ?= 0.17.新版本/' Makefile
```

或手动编辑：
```makefile
VERSION ?= 0.17.新版本
```

### 步骤 3：提交版本升级

```bash
git add Makefile
git commit -m "chore: bump version to 0.17.新版本

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### 步骤 4：创建注释标签

```bash
git tag -a v0.17.新版本 -m "v0.17.新版本: 简要描述

## 变更

### 功能
- 功能描述

### Bug 修复
- 修复描述

### 文档
- 文档变更

## 破坏性变更
无（或列出破坏性变更）"
```

### 步骤 5：推送到 GitHub

```bash
git push origin main
git push origin v0.17.新版本
```

### 步骤 6：验证发布

```bash
# 检查工作流状态
gh run list --limit 5

# 检查已创建的发布
gh release list --limit 3

# 查看发布详情
gh release view v0.17.新版本
```

## 发布工作流

CI 自动执行：
1. 构建 Docker 镜像（amd64, arm64）
2. 推送到 `ghcr.io/stringke/cloudflare-operator:VERSION`
3. 生成安装器清单
4. 创建 GitHub Release，包含资产：
   - `cloudflare-operator.yaml`
   - `cloudflare-operator.crds.yaml`

## 回滚

如果发布失败：

```bash
# 删除本地标签
git tag -d v0.17.新版本

# 删除远程标签（如果已推送）
git push origin :refs/tags/v0.17.新版本

# 回退版本提交
git revert HEAD
```

## 发布说明模板

```markdown
## v0.17.X

### 功能
- feat(组件): 描述 (#PR)

### Bug 修复
- fix(组件): 描述 (#PR)

### 文档
- docs: 描述

### 破坏性变更
- **破坏性**: 破坏性变更描述

### 迁移指南
从上一版本迁移的步骤（如适用）

### 完整变更日志
https://github.com/StringKe/cloudflare-operator/compare/v0.17.上一版本...v0.17.X
```

## 热修复发布

紧急修复：

```bash
# 1. 创建热修复分支（可选）
git checkout -b hotfix/v0.17.X

# 2. 应用修复
# ... 进行变更 ...

# 3. 快速发布
make fmt vet test
git add -A
git commit -m "fix(组件): 紧急修复描述"
git checkout main
git merge hotfix/v0.17.X

# 4. 立即发布
# 按照标准发布步骤
```

## 版本历史

查看最近版本：
```bash
git tag --sort=-v:refname | head -20
```

查看版本间变更：
```bash
git log v0.17.上一版本..v0.17.新版本 --oneline
```
