---
name: skill-installer
description: 为通用 AI 助手安装技能。当用户请求列出可用技能、从 Git 仓库（GitHub/GitLab/Gitea）或本地目录安装技能到特定 AI 助手（Codex、Roo、Claude、Copilot、Cursor 等）的指定作用域时使用此技能。
---

# 技能安装器

帮助用户从 Git 仓库或本地目录安装技能到各种 AI 助手的指定目录。

## 功能概述

1. **列出技能**: 显示指定位置（Git 仓库或本地目录）的可用技能
2. **安装技能**: 从源位置安装技能到目标 AI 助手的技能目录

## 支持的技能源

### Git 仓库
- **GitHub**: `https://github.com/owner/repo`
- **GitLab**: `https://gitlab.com/owner/repo` 或自托管 GitLab
- **Gitea**: 自托管 Gitea 实例

### 本地源
- 本地目录
- 本地 .skill 文件

### 远程文件
- 远程 .skill 文件 URL

## 支持的 AI 助手

详细的 AI 助手配置信息请参阅 [ai-assistants.md](ai-assistants.md)。

支持的助手包括：
- **Codex** (OpenAI)
- **Roo Code**
- **Claude Code**
- **KiloCode**
- **VS Code Copilot**
- **Cursor**

## 使用流程

### 步骤 1: 确定技能源

首先识别用户提供的技能源：
- Git 仓库 URL（GitHub/GitLab/Gitea）
- 本地目录路径

如果用户未明确指定，询问用户。

### 步骤 2: 列出可用技能

使用 [`list-skills.py`](scripts/list-skills.py) 脚本列出可用技能：

```bash
# 列出远程仓库的技能
python scripts/list-skills.py https://github.com/owner/repo/tree/main/skills

# 列出本地目录的技能
python scripts/list-skills.py /path/to/skills

# 指定分支
python scripts/list-skills.py https://github.com/owner/repo --ref develop

# 检查已安装（需要先确定目标目录）
python scripts/list-skills.py https://github.com/owner/repo --installed-dir ~/.roo/skills
```

**输出格式**:
- 默认文本格式：`1. skill-name (已安装)`
- JSON 格式：`--format json`

### 步骤 3: 确定安装目标

#### 如何确定目标路径

1. **用户已指定目标目录**: 直接使用该路径，跳过步骤 2

2. **用户指定了 AI 助手和作用域**: 
   - 阅读 [`ai-assistants.md`](ai-assistants.md) 查找对应的路径模板
   - 展开路径中的变量：
     - `~`: 用户主目录
     - `$CWD`: 当前工作目录
     - `$REPO_ROOT`: Git 仓库根目录（需要查找 .git 目录）
     - `{mode}`: 模式名称（用户提供）
   
   需要确定的信息：
   - **AI 助手**: 用户使用哪个 AI 助手（codex/roo/claude/copilot/cursor）
   - **作用域**: 安装到哪个作用域（global/project 等）
   - **模式**（可选）: 某些助手支持模式特定作用域（如 Roo 的 `global-mode`）

3. **信息不足**: 询问用户提供目标目录或 AI 助手及作用域信息

**示例对话**:
```
用户: "安装 skill-creator 技能到 Roo"
助手: "好的，我将安装 skill-creator。请问要安装到哪个作用域？
      - global: 全局可用（所有项目）
      - project: 仅当前项目
      选择或告诉我具体路径。"
```

### 步骤 4: 安装技能

使用 [`install-skill.py`](scripts/install-skill.py) 脚本安装技能：

```bash
# 从远程仓库安装
python scripts/install-skill.py \
  https://github.com/owner/repo \
  skill-name \
  --dest /path/to/skills

# 从本地目录安装
python scripts/install-skill.py \
  /local/path/to/skills \
  skill-name \
  --dest /path/to/target

# 安装多个技能
python scripts/install-skill.py \
  https://github.com/owner/repo \
  skill-1 skill-2 skill-3 \
  --dest /path/to/skills

# 指定分支或标签
python scripts/install-skill.py \
  https://github.com/owner/repo \
  skill-name \
  --dest /path/to/skills \
  --ref v1.0.0

# 强制覆盖已存在的技能
python scripts/install-skill.py \
  https://github.com/owner/repo \
  skill-name \
  --dest /path/to/skills \
  --force

# 指定安装方法
python scripts/install-skill.py \
  https://github.com/owner/repo \
  skill-name \
  --dest /path/to/skills \
  --method git  # auto/download/git

# 从本地 .skill 文件安装
python scripts/install-skill.py \
  /path/to/skill-name.skill \
  --dest /path/to/skills

# 从远程 .skill 文件安装
python scripts/install-skill.py \
  https://example.com/skills/skill-name.skill \
  --dest /path/to/skills
```

**参数说明**:
- `source`: 技能源（URL 或本地路径）
- `skills`: 一个或多个技能名称（相对于源的路径）
- `--dest`: 目标安装目录（必需）
- `--ref`: Git 分支或标签（默认: main）
- `--force`: 强制覆盖已存在的技能
- `--method`: 安装方法
  - `auto`（默认）: 优先使用下载，失败时回退到 git
  - `download`: 仅使用下载方式
  - `git`: 使用 git 稀疏检出

### 步骤 5: 确认安装

安装完成后，告知用户：
1. 已安装的技能名称和位置
2. 某些 AI 助手可能需要重启才能识别新技能

## 常见场景示例

### 场景 1: 从 GitHub 安装到 Roo 全局

```
用户: "从 anthropics/skills 安装 skill-creator 到 Roo 全局"

助手操作:
1. 阅读 ai-assistants.md 确定 Roo 全局路径: ~/.roo/skills
2. 运行安装命令:
   python scripts/install-skill.py \
     https://github.com/anthropics/skills \
     skills/skill-creator \
     --dest ~/.roo/skills
```

### 场景 2: 列出并选择安装

```
用户: "列出 openai/skills 中 .experimental 目录的技能"

助手操作:
1. 运行列表命令:
   python scripts/list-skills.py \
     https://github.com/openai/skills/tree/main/skills/.experimental

2. 展示技能列表，询问用户要安装哪些
3. 根据用户选择执行安装
```

### 场景 3: 从本地目录安装

```
用户: "把 /Users/me/my-skills/custom-skill 安装到 Claude 项目"

助手操作:
1. 阅读 ai-assistants.md 确定 Claude 项目路径: .claude/skills
2. 运行安装命令:
   python scripts/install-skill.py \
     /Users/me/my-skills \
     custom-skill \
     --dest .claude/skills
```

### 场景 4: 用户指定安装目录

```
用户: "安装到 /custom/path/skills"

助手操作:
直接使用用户指定的路径，无需查阅 ai-assistants.md:
python scripts/install-skill.py \
  https://github.com/owner/repo \
  skill-name \
  --dest /custom/path/skills
```

### 场景 5: 安装到特定模式

```
用户: "安装到 Roo 的 code 模式全局作用域"

助手操作:
1. 阅读 ai-assistants.md 查找 Roo 的 global-mode 配置
2. 路径模板: ~/.roo/skills-{mode}
3. 展开为: ~/.roo/skills-code
4. 执行安装到该目录
```

### 场景 6: 从 .skill 文件安装

```
用户: "安装这个 skill-creator.skill 文件到 Claude 全局"

助手操作:
1. 阅读 ai-assistants.md 确定 Claude 全局路径: ~/.claude/skills
2. 运行安装命令:
   python scripts/install-skill.py \
     skill-creator.skill \
     --dest ~/.claude/skills
```

### 场景 7: 从远程 .skill 文件安装

```
用户: "从 https://example.com/skills/my-skill.skill 安装"

助手操作:
直接下载并安装:
python scripts/install-skill.py \
  https://example.com/skills/my-skill.skill \
  --dest /path/to/skills
```

## 故障排除

### 下载失败

如果从 Git 平台下载失败：
- 检查网络连接
- 对于私有仓库，确保设置了相应的环境变量：
  - GitHub: `GITHUB_TOKEN` 或 `GH_TOKEN`
  - GitLab: `GITLAB_TOKEN`
  - Gitea: `GITEA_TOKEN`
- 尝试使用 `--method git` 回退到 Git 克隆

### 技能已存在

如果技能已存在，脚本会报错。使用 `--force` 参数强制覆盖。

### 路径不存在

脚本会自动创建目标目录。如果父目录不存在可能会失败，先确保父目录存在。

## 重要注意事项

1. **用户指定路径优先**: 如果用户明确提供了安装目录，直接使用，无需查阅配置
2. **查阅配置文件**: 当需要根据 AI 助手和作用域确定路径时，必须读取 ai-assistants.md
3. **验证技能结构**: 确保源目录包含有效的 SKILL.md 文件
4. **处理路径变量**: 正确展开 `~`, `$CWD`, `$REPO_ROOT` 等变量
5. **询问不明确的信息**: 当无法确定安装目标时，主动询问用户
6. **提供清晰反馈**: 安装完成后明确告知用户安装位置

## 脚本参考

- [`git_utils.py`](scripts/git_utils.py): Git 平台操作工具函数
- [`list-skills.py`](scripts/list-skills.py): 列出可用技能
- [`install-skill.py`](scripts/install-skill.py): 安装技能
- [`ai-assistants.md`](ai-assistants.md): AI 助手目录配置参考
