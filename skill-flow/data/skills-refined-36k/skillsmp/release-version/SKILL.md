---
name: release-version
description: Automatically release a new version. Detects current version, analyzes recent changes, suggests version bump (patch/minor/major), and executes release. Trigger when user says "请发版本", "release", "发版", "bump version".
---

# Release Version

自动化版本发布流程，根据变更内容智能推荐版本号增幅级别。

## 触发词

- "请发版本"
- "发版"
- "release"
- "bump version"
- "发布新版本"

## 执行流程

### 1. 获取当前版本信息

```bash
# 获取最新 tag
git tag --sort=-v:refname | head -1

# 查看当前 package.json 中的版本
cat prd-desktop/package.json | grep '"version"'
```

### 2. 分析自上次发版以来的变更

```bash
# 获取上次 tag 以来的所有提交
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# 查看变更的文件统计
git diff --stat $(git describe --tags --abbrev=0)..HEAD

# 查看变更的文件列表
git diff --name-only $(git describe --tags --abbrev=0)..HEAD
```

### 3. 判断版本增幅级别

根据变更内容判断应该增加哪个级别的版本号：

#### Patch (x.y.Z) - 默认选择
适用于：
- Bug 修复
- 小型 UI 调整（样式、文案）
- 代码重构（不影响功能）
- 依赖更新（非破坏性）
- 文档更新

**关键词**: fix, refactor, style, chore, docs, update, enhance, tweak

#### Minor (x.Y.0) - 需要提醒用户确认
适用于：
- 新功能添加
- 功能增强（非破坏性）
- 新增 API 端点
- 新增页面或组件
- 较大的 UI 改版

**关键词**: feat, add, implement, new, feature, 新增, 添加, 实现

**触发条件**:
- 新增超过 3 个文件
- 变更超过 500 行代码
- 提交信息包含 `feat:` 或 `add` 开头

#### Major (X.0.0) - 必须提醒用户确认
适用于：
- 破坏性变更（Breaking Changes）
- 不兼容的 API 修改
- 架构重大调整
- 依赖大版本升级
- 功能移除

**关键词**: breaking, remove, deprecate, migrate, 重构, 迁移

**触发条件**:
- 提交信息包含 `BREAKING CHANGE` 或 `!:`
- 删除超过 10 个文件
- 重命名核心模块

### 4. 询问用户确认

根据分析结果，向用户展示：

```
## 版本发布分析

**当前版本**: v1.5.2
**建议新版本**: v1.5.3 (Patch)

### 自上次发版的变更 (共 X 个提交)

- abc1234 Fix: 修复某某问题
- def5678 Refactor: 重构某某模块
- ...

### 变更统计
- 新增文件: X
- 修改文件: Y
- 删除文件: Z
- 代码变更: +XXX / -YYY 行

### 判断依据
本次变更主要是 Bug 修复和小型调整，建议 Patch 版本。

是否继续发布 v1.5.3？
```

如果检测到可能需要 Minor 或 Major：

```
⚠️ 检测到以下重大变更，建议考虑升级版本级别：

- 新增了 3 个新功能模块
- 代码变更量超过 800 行
- 包含 "feat: 实现新功能" 提交

建议选择：
1. v1.5.3 (Patch) - 仅小版本修复
2. v1.6.0 (Minor) - 包含新功能 [推荐]
3. v2.0.0 (Major) - 重大版本升级

请选择版本号：
```

### 5. 执行发版

用户确认后执行：

```bash
# 使用项目的发版脚本
./quick.sh release <version>
```

此命令会自动：
1. 同步版本号到所有配置文件
2. 创建 git commit
3. 创建 git tag
4. 推送到远程仓库
5. 触发 GitHub Actions 构建发布

### 6. 发版后确认

```
✅ 版本 v1.5.3 发布成功！

- Git tag: v1.5.3
- Commit: chore(release): bump version to 1.5.3

GitHub Actions 正在构建发布包...
查看进度: https://github.com/inernoro/prd_agent/actions
```

## 版本号计算示例

| 当前版本 | Patch | Minor | Major |
|---------|-------|-------|-------|
| 1.5.2   | 1.5.3 | 1.6.0 | 2.0.0 |
| 2.0.0   | 2.0.1 | 2.1.0 | 3.0.0 |
| 0.9.9   | 0.9.10| 0.10.0| 1.0.0 |

## 特殊情况处理

### 工作区有未提交的更改
```
⚠️ 检测到未提交的更改，请先提交或暂存：
[显示 git status]

是否要先提交这些更改？
```

### 没有新的提交
```
ℹ️ 自上次发版 (v1.5.2) 以来没有新的提交。

是否仍要发布新版本？这通常用于：
- 修复发布配置问题
- 重新触发 CI/CD
```

### Tag 已存在
```
❌ Tag v1.5.3 已存在！

可选操作：
1. 使用下一个版本 v1.5.4
2. 删除现有 tag 并重新发布（谨慎）
```

## 相关命令

```bash
# 仅同步版本号（不创建 commit/tag）
./quick.sh version <version>

# 完整发版流程
./quick.sh release <version>

# 查看最近的 tags
git tag --sort=-v:refname | head -10

# 查看某个 tag 的详情
git show v1.5.2
```
