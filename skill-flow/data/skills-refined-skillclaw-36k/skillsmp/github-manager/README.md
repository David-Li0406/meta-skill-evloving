# 🐙 GitHub Manager - GitHub 仓库管理工具

完整的 GitHub 仓库管理工具，通过自然对话轻松管理 GitHub 仓库。

这是一个 Claude Code Skill，通过对话即可完成所有 GitHub 操作。

---

## 🚀 快速开始

### 第一次使用前准备

#### 1. 检查 Git 是否已安装

```
检查我的 Git 版本
```

如果没有安装 Git，请先安装：
- **macOS**: `brew install git`
- **Ubuntu**: `sudo apt-get install git`
- **Windows**: 下载 [Git for Windows](https://git-scm.com/download/win)

#### 2. 获取 GitHub Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置 Token 名称（如：GitHub Manager）
4. 勾选权限：
   - ✅ `repo` - 完整仓库访问权限
   - ✅ `user` - 用户信息
   - ✅ `delete_repo` - 删除仓库
5. 点击 "Generate token"
6. **重要**：复制并保存 Token（只显示一次）

#### 3. 配置 Token

```
配置 GitHub Token 为 ghp_xxxxx
```

---

## 📚 常用操作

### 1. 上传本地项目到 GitHub

最简单的使用方式，一键上传本地文件夹：

```
把 /path/to/project 这个项目上传到 GitHub，仓库名叫 my-repo
```

**自动完成**：
- ✅ 在 GitHub 创建仓库
- ✅ 初始化 Git
- ✅ 创建 .gitignore
- ✅ 添加所有文件
- ✅ 提交并推送

**示例对话**：
```
你：上传 ~/my-project 到 GitHub，仓库名 awesome-project

Claude：✅ 上传成功！仓库地址：https://github.com/username/awesome-project
```

```
你：把当前项目上传为私有仓库

Claude：✅ 已创建私有仓库并推送成功
```

### 2. 克隆 GitHub 仓库

```
克隆 username/repo-name 这个仓库
克隆到指定目录 /path/to/dest
```

### 3. 创建新仓库

```
在 GitHub 创建一个新仓库叫 my-repo，描述为"我的项目"
创建一个私有仓库叫 private-repo
```

### 4. 查看和管理仓库

```
列出我所有的 GitHub 仓库
只显示公开仓库
查看 username/repo-name 的详细信息
删除 username/repo-name 仓库
```

### 5. Git 常用操作

```
查看当前 Git 状态
提交更改，提交信息为"修复bug"
推送到远程仓库
拉取最新更新
查看提交历史
```

### 6. 分支管理

```
列出所有分支
创建新分支 feature-login
切换到 main 分支
创建并切换到新分支 feature-payment
合并 feature-login 分支到当前分支
删除 feature-login 分支
```

---

## 💡 工作流示例

### 场景1：上传新项目

```
你：帮我把 ~/my-project 上传到 GitHub

Claude：好的，我来帮你上传。仓库名用什么？

你：就叫 my-project 吧

Claude：✅ 上传成功！
   仓库地址：https://github.com/username/my-project
   描述：我的项目
   可见性：公开
```

### 场景2：日常开发流程

```
你：克隆 username/project 这个项目

Claude：✅ 克隆成功...

你：创建一个新分支 feature-new-api

Claude：✅ 已创建并切换到 feature-new-api 分支

你：帮我提交代码，提交信息为"添加新API"

Claude：✅ 提交成功...

你：推送到远程

Claude：✅ 推送成功...

你：切换回 main 分支，然后合并 feature-new-api

Claude：✅ 已切换并合并成功...
```

### 场景3：团队协作

```
你：拉取最新代码

Claude：✅ 已拉取最新更改...

你：查看当前状态

Claude：📊 当前状态：
   - 修改文件：3个
   - 新文件：1个

你：提交并推送，信息为"更新代码"

Claude：✅ 提交并推送成功...
```

---

## 📋 完整命令参考

### 仓库管理

```
创建仓库 <仓库名> [描述]
列出仓库 [类型：public/private]
克隆仓库 <仓库地址> [目标目录]
删除仓库 <仓库地址>
查看仓库信息 <仓库地址>
```

### 上传项目

```
上传 <本地路径> 到 GitHub，仓库名 <名称>
上传当前目录为私有仓库
```

### Git 操作

```
查看 Git 状态
提交 <提交信息>
推送
拉取
查看日志
创建 .gitignore
```

### 分支管理

```
列出分支
创建分支 <名称>
切换分支 <名称>
新建并切换 <名称>
合并分支 <名称>
删除分支 <名称>
```

### Token 管理

```
配置 GitHub Token <token>
查看当前 Token
```

---

## ⚠️ 注意事项

### Token 安全

- Token 存储在本地加密文件中
- 不要分享给他人
- 定期更新 Token
- 如果 Token 泄露，立即在 GitHub 撤销并重新生成

### 删除仓库

- 删除操作**不可恢复**
- 删除前会要求确认
- 请谨慎操作

### Git 冲突

- 拉取或合并时可能出现冲突
- 需要手动解决冲突后再次提交

---

## 🔧 常见问题

### Token 无效

```
❌ API 请求失败 (401): Bad credentials
```

**解决方法**：
```
重新配置 GitHub Token 为 <new-token>
```

### Git 未安装

```
❌ Git 未安装
```

**解决方法**：
- macOS: `brew install git`
- Ubuntu: `sudo apt-get install git`

### 权限不足

```
❌ 推送失败: permission denied
```

**解决方法**：
1. 检查 Token 权限是否包含 `repo`
2. 检查仓库是否为你所有
3. 重新生成包含正确权限的 Token

### 分支冲突

```
❌ 合并失败: conflict
```

**解决方法**：
```
帮我解决合并冲突
```

---

## 💪 最佳实践

1. **明确描述** - 上传项目时明确说明仓库名和描述
2. **分支管理** - 开发新功能时使用独立分支
3. **定期提交** - 完成小功能后及时提交
4. **推送前检查** - 推送前先查看状态确认更改
5. **Token 安全** - 定期更新 Token，不要泄露

---

**开始管理你的 GitHub 仓库吧！** 🐙
