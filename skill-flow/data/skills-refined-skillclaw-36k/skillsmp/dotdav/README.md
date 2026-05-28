# Dotdav

一个基于 Python、Rclone 和 Systemd 的极简 Dotfiles 同步工具。

## 功能特性

- **多设备支持**：为不同设备（如 desktop, laptop）维护不同的配置版本。
- **WebDAV 同步**：通过 Rclone 支持 WebDAV 以及所有 Rclone 支持的网盘。
- **自动同步**：内置 Systemd 服务，支持文件变动自动推送 (Push) 和定时拉取 (Pull)。
- **Fish Shell 补全**：提供完整的命令行补全支持。

## 安装

### 前置要求

- Python 3.11+
- [Rclone](https://rclone.org/) (已安装并配置好 Remote)
- [uv](https://github.com/astral-sh/uv) (推荐)

### 安装步骤

1. 克隆本仓库：
   ```bash
   git clone https://github.com/yourusername/dotdav.git
   cd dotdav
   ```

2. 安装依赖并安装到本地环境：
   ```bash
   uv pip install -e .
   ```
   或者直接使用 `pip`：
   ```bash
   pip install -e .
   ```

## 快速开始

### 1. 初始化

首先初始化仓库，指定 Rclone 的 Remote 名称和路径：

```bash
dotdav init --remote mywebdav --path dotfiles
```

### 2. 添加配置文件

将现有的配置文件加入管理：

```bash
dotdav add ~/.bashrc
```

这会将 `~/.bashrc` 复制到 `repo/` 目录，并自动记录映射关系。

### 3. 多设备配置 (Profile)

如果你在另一台设备上（例如笔记本），希望使用不同的配置：

```bash
# 切换到 laptop 配置
dotdav profile laptop

# 添加特定于 laptop 的版本 (原有 .bashrc 会被保存为 bashrc_laptop)
dotdav add ~/.bashrc
```

### 3.5 移除文件

如果你想停止同步某个文件，并将其恢复为普通文件（删除软链接）：

```bash
dotdav remove ~/.bashrc
```

**注意**：请提供**本地文件的路径**（即当初 `add` 时使用的路径，例如 `~/.bashrc`），而不是仓库中的路径。

此操作会：
1. 从 `repo` 中删除对应文件。
2. 删除本地的软链接。
3. 将文件原本的内容从仓库复制回本地位置。

### 4. 部署

将仓库中的文件部署（软链接）到当前系统：

```bash
dotdav deploy
```

它会自动根据当前的 Profile 选择合适的文件版本。

### 5. 同步与自动同步

**手动同步：**

```bash
dotdav sync push  # 推送到网盘
dotdav sync pull  # 从网盘拉取
```

**开启自动同步守护进程：**

```bash
# 安装并启动 Systemd 用户服务
dotdav service install

# 查看状态
systemctl --user status dotdav.service
```

该服务会监听文件变动并实时上传，同时每 10 分钟自动拉取一次。

## Shell 补全

**Fish Shell:**

```fish
source completions.fish
```
可以将此行加入你的 `config.fish`。

## 目录结构

- `repo/`: 存放实际的配置文件。
- `config.yaml`: 本地配置（Remote 设置，当前 Profile）。
- `mappings.yaml`: 文件映射关系表。
