---
name: github-manager
description: "GitHub 仓库管理工具。克隆仓库、创建项目、上传文件夹、Git 操作、分支管理等完整功能。"
---

# 🐙 GitHub Manager - GitHub 仓库管理工具

完整的 GitHub 仓库管理工具，帮助你：
- ✅ 克隆和管理 GitHub 仓库
- ✅ 创建新的 GitHub 仓库
- ✅ 上传本地文件夹到 GitHub
- ✅ Git 常用操作（提交、推送、拉取等）
- ✅ 分支管理
- ✅ 查看仓库状态和历史

**适用场景**：GitHub 项目管理、代码同步、版本控制

---

## 🚀 快速开始

### 第一步：配置 GitHub Token

```bash
# 设置 GitHub Personal Access Token
python3 ~/.config/claude/skills/github-manager/scripts/token_manager.py 设置 <your-token>
```

**获取 Token**：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选权限：`repo`、`user`、`delete_repo`
4. 生成并复制 Token

### 第二步：克隆仓库

```bash
# 克隆你的仓库
python3 ~/.config/claude/skills/github-manager/scripts/repo_manager.py 克隆 username/repo-name

# 克隆到指定目录
python3 ~/.config/claude/skills/github-manager/scripts/repo_manager.py 克隆 username/repo-name /path/to/destination
```

### 第三步：上传本地项目

```bash
# 上传文件夹到 GitHub（会自动创建仓库）
python3 ~/.config/claude/skills/github-manager/scripts/upload_folder.py /path/to/folder repo-name "初始提交"
```

**完成！** 你已经成功上传了第一个项目。

---

## 🔥 常用命令速查

```bash
# 仓库管理
python3 ~/.config/claude/skills/github-manager/scripts/repo_manager.py 克隆 username/repo-name
python3 ~/.config/claude/skills/github-manager/scripts/repo_manager.py 创建 repo-name "仓库描述"
python3 ~/.config/claude/skills/github-manager/scripts/repo_manager.py 列出
python3 ~/.config/claude/skills/github-manager/scripts/repo_manager.py 删除 username/repo-name

# 上传和提交
python3 ~/.config/claude/skills/github-manager/scripts/upload_folder.py /path/to/folder repo-name "提交信息"
python3 ~/.config/claude/skills/github-manager/scripts/git_operations.py 提交 "修复bug"
python3 ~/.config/claude/skills/github-manager/scripts/git_operations.py 推送

# Git 操作
python3 ~/.config/claude/skills/github-manager/scripts/git_operations.py 状态
python3 ~/.config/claude/skills/github-manager/scripts/git_operations.py 日志
python3 ~/.config/claude/skills/github-manager/scripts/git_operations.py 拉取

# 分支管理
python3 ~/.config/claude/skills/github-manager/scripts/branch_manager.py 创建 feature-branch
python3 ~/.config/claude/skills/github-manager/scripts/branch_manager.py 切换 main
python3 ~/.config/claude/skills/github-manager/scripts/branch_manager.py 列出

# Token 管理
python3 ~/.config/claude/skills/github-manager/scripts/token_manager.py 设置 <token>
python3 ~/.config/claude/skills/github-manager/scripts/token_manager.py 查看
```

---

## 💡 使用场景

### 场景1：上传本地项目到 GitHub

```bash
# 1. 上传文件夹（自动创建仓库）
python3 ~/.config/claude/skills/github-manager/scripts/upload_folder.py ~/my-project my-awesome-project "初始版本"

# 自动完成：
# ✅ 在 GitHub 创建仓库
# ✅ 初始化 git
# ✅ 添加所有文件
# ✅ 提交并推送
```

### 场景2：克隆并修改项目

```bash
# 1. 克隆仓库
python3 ~/.config/claude/skills/github-manager/scripts/repo_manager.py 克隆 username/repo-name

# 2. 进入目录修改代码
cd repo-name

# 3. 提交更改
python3 ~/.config/claude/skills/github-manager/scripts/git_operations.py 提交 "添加新功能"

# 4. 推送到远程
python3 ~/.config/claude/skills/github-manager/scripts/git_operations.py 推送
```

### 场景3：创建新仓库

```bash
# 创建公开仓库
python3 ~/.config/claude/skills/github-manager/scripts/repo_manager.py 创建 my-new-repo "我的新项目"

# 创建私有仓库
python3 ~/.config/claude/skills/github-manager/scripts/repo_manager.py 创建 my-new-repo "私有项目" --private
```

### 场景4：分支管理

```bash
# 创建新分支
python3 ~/.config/claude/skills/github-manager/scripts/branch_manager.py 创建 feature-login

# 切换分支
python3 ~/.config/claude/skills/github-manager/scripts/branch_manager.py 切换 feature-login

# 合并分支
python3 ~/.config/claude/skills/github-manager/scripts/branch_manager.py 合并 feature-login
```

---

## 📚 功能模块

| 模块 | 脚本 | 说明 |
|------|------|------|
| 仓库管理 | `repo_manager.py` | 克隆、创建、列出、删除仓库 |
| 文件上传 | `upload_folder.py` | 上传文件夹到 GitHub |
| Git 操作 | `git_operations.py` | 提交、推送、拉取、状态等 |
| 分支管理 | `branch_manager.py` | 创建、切换、合并分支 |
| Token 管理 | `token_manager.py` | 存储和管理 GitHub Token |
| API 调用 | `github_api.py` | GitHub API 封装 |
| 工具函数 | `utils.py` | 通用工具函数 |

---

## 📖 详细文档

- `README.md` - 基本用法和示例
- `docs/GITHUB_API_GUIDE.md` - GitHub API 使用指南
- `docs/TROUBLESHOOTING.md` - 常见问题解决

---

## 🔧 依赖

```bash
pip3 install requests
```

**系统要求**：
- Git 命令行工具
- Python 3.6+
- GitHub 账户和 Personal Access Token

---

## ⚠️ 注意事项

1. **Token 安全**
   - Token 存储在本地加密文件中
   - 不要分享给他人
   - 定期更新 Token

2. **第一次使用**
   - 需要先配置 GitHub Token
   - 需要配置 Git 用户信息

3. **数据安全**
   - 推送前确认提交内容
   - 重要数据先备份
   - 删除仓库不可恢复

---

**现在开始管理你的 GitHub 仓库吧！** 🐙
