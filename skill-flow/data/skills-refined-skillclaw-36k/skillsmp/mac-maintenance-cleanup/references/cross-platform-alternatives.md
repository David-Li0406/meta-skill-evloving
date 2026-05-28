# 跨平台清理替代方案

本文档提供在不同操作系统上执行系统清理的替代方案和工具。

## 目录

- [Windows 替代方案](#windows-替代方案)
- [Linux 替代方案](#linux-替代方案)
- [跨平台工具](#跨平台工具)
- [命令对照表](#命令对照表)

---

## Windows 替代方案

### 系统缓存清理

#### 内置工具

**1. 磁盘清理工具**

```powershell
# 打开磁盘清理
cleanmgr

# 通过命令行运行
cleanmgr /d C: /lowdisk
```

**功能**：
- 临时文件清理
- 系统缓存清理
- 回收站清理
- 缩略图缓存

**2. Storage Sense（存储感知）**

Windows 10/11 内置的自动清理功能。

设置路径：设置 > 系统 > 存储 > 存储感知

**3. PowerShell 命令**

```powershell
# 清理临时文件
Remove-Item -Path $env:TEMP\* -Recurse -Force
Remove-Item -Path C:\Windows\Temp\* -Recurse -Force

# 清理 Windows Update 缓存
Stop-Service -Name wuauserv
Remove-Item -Path C:\Windows\SoftwareDistribution\Download\* -Recurse -Force
Start-Service -Name wuauserv

# 清理回收站
Clear-RecycleBin -Force
```

#### 第三方工具

**1. BleachBit**

开源的磁盘清理工具，类似 CCleaner。

下载：https://www.bleachbit.org/

**功能**：
- 缓存清理
- 临时文件清理
- 浏览器历史清理
- 隐私保护

**使用方法**：
```powershell
# 下载并安装 BleachBit
# 运行图形界面或命令行
bleachbit.exe --clean
```

**2. WizTree**

快速的磁盘空间分析工具。

下载：https://www.diskanalyzer.com/

**功能**：
- 磁盘空间分析
- 大文件查找
- 文件类型统计

---

### 应用卸载

#### 内置工具

**1. 控制面板**

```powershell
# 打开程序和功能
appwiz.cpl
```

**2. PowerShell**

```powershell
# 列出已安装程序
Get-WmiObject -Class Win32_Product | Select-Object Name, Version

# 卸载程序（需要程序的具体 GUID）
msiexec /x {GUID} /qn
```

#### 第三方工具

**1. Revo Uninstaller**

强大的卸载工具，可以彻底卸载应用及其残留文件。

下载：https://www.revouninstaller.com/

**功能**：
- 彻底卸载
- 残留文件清理
- 注册表清理
- 强制卸载

**2. Geek Uninstaller**

轻量级的卸载工具。

下载：http://www.geekuninstaller.com/

---

### 磁盘空间分析

#### 内置工具

**1. Storage Usage**

设置 > 系统 > 存储

**2. PowerShell**

```powershell
# 查看磁盘使用情况
Get-PSDrive -PSProvider FileSystem

# 查找大文件
Get-ChildItem -Path C:\ -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt 1GB } |
    Select-Object FullName, @{Name='Size(GB)';Expression={[math]::Round($_.Length/1GB,2)}} |
    Sort-Object 'Size(GB)' -Descending
```

#### 第三方工具

**1. WinDirStat**

磁盘空间可视化工具。

下载：https://windirstat.net/

**2. SpaceSniffer**

磁盘空间分析工具。

下载：http://www.uderzo.it/main_products/space_sniffer/

---

### 项目构建清理

**Node.js 项目**

```powershell
# 删除 node_modules
Get-ChildItem -Include node_modules -Recurse | Remove-Item -Recurse -Force

# 删除 npm 缓存
npm cache clean --force
```

**Python 项目**

```powershell
# 删除虚拟环境
Get-ChildItem -Include venv,.venv -Recurse -Directory | Remove-Item -Recurse -Force

# 删除 __pycache__
Get-ChildItem -Include __pycache__ -Recurse | Remove-Item -Recurse -Force
```

---

## Linux 替代方案

### 系统缓存清理

#### 包管理器清理

**Debian/Ubuntu (apt)**

```bash
# 清理不再需要的包
sudo apt autoremove

# 清理 apt 缓存
sudo apt clean
sudo apt autoclean

# 删除孤立的包
sudo deborphan | xargs sudo apt-get -y remove --purge
```

**Fedora/RHEL (dnf)**

```bash
# 清理不再需要的包
sudo dnf autoremove

# 清理 dnf 缓存
sudo dnf clean all

# 删除重复的包
sudo dnf repoquery --duplicates
```

**Arch Linux (pacman)**

```bash
# 清理缓存
sudo pacman -Sc

# 删除不再需要的包
sudo pacman -Qtdq | sudo pacman -Rns -

# 清理未安装包的缓存
sudo paccache -ruk0
```

#### 系统清理工具

**1. BleachBit**

```bash
# 安装
sudo apt install bleachbit  # Debian/Ubuntu
sudo dnf install bleachbit  # Fedora

# 运行
bleachbit
```

**2. Stacer**

Linux 系统优化和清理工具。

```bash
# 安装
sudo apt install stacer  # Debian/Ubuntu

# 运行
stacer
```

---

### 应用卸载

**Debian/Ubuntu**

```bash
# 卸载但保留配置
sudo apt remove package-name

# 完全卸载（包括配置）
sudo apt purge package-name

# 清理残留配置
sudo apt autoremove
```

**Fedora/RHEL**

```bash
# 卸载
sudo dnf remove package-name

# 删除不再需要的依赖
sudo dnf autoremove
```

**Arch Linux**

```bash
# 卸载
sudo pacman -R package-name

# 完全卸载（包括配置和依赖）
sudo pacman -Rns package-name
```

---

### 磁盘空间分析

**1. ncdu**

基于 ncurses 的磁盘使用分析工具。

```bash
# 安装
sudo apt install ncdu  # Debian/Ubuntu
sudo dnf install ncdu  # Fedora

# 运行
ncdu /
ncdu ~/
```

**2. du + human-readable**

```bash
# 查看目录大小
du -sh ~/* | sort -hr

# 查看最大的 10 个目录
du -h --max-depth=1 ~/ | sort -hr | head -n 10

# 查找大于 100MB 的文件
find ~ -type f -size +100M -exec du -sh {} \; | sort -hr
```

**3. df**

```bash
# 查看磁盘使用情况
df -h
```

---

### 项目构建清理

**Node.js**

```bash
# 删除 node_modules
find ~ -type d -name "node_modules" -prune -exec rm -rf {} \;

# 清理 npm 缓存
npm cache clean --force

# 清理 yarn 缓存
yarn cache clean
```

**Python**

```bash
# 删除虚拟环境
find ~ -type d -name "venv" -prune -exec rm -rf {} \;
find ~ -type d -name ".venv" -prune -exec rm -rf {} \;

# 删除 __pycache__
find ~ -type d -name "__pycache__" -prune -exec rm -rf {} \;
find ~ -type f -name "*.pyc" -delete
```

**Rust**

```bash
# 删除 target 目录
find ~ -type d -name "target" -prune -exec rm -rf {} \;

# 清理 Cargo 缓存
cargo clean
```

**Java/Maven**

```bash
# 删除 .m2 目录
find ~ -type d -name ".m2" -prune -exec rm -rf {} \;
```

**Go**

```bash
# 清理 Go 模块缓存
go clean -modcache
```

---

## 跨平台工具

### 1. BleachBit

支持 Windows、Linux 的跨平台清理工具。

网站：https://www.bleachbit.org/

**功能**：
- 系统缓存清理
- 浏览器数据清理
- 临时文件清理
- 隐私保护

### 2. ncdu

终端磁盘使用分析工具，支持 Linux、macOS。

```bash
# 安装
sudo apt install ncdu  # Debian/Ubuntu
brew install ncdu      # macOS
```

### 3. du 和 df

所有 Unix-like 系统（Linux、macOS）都内置的工具。

```bash
# 查看目录大小
du -sh directory

# 查看磁盘使用
df -h
```

### 4. Fossil

跨平台的磁盘清理工具。

网站：https://github.com/maxkluster/fossil

---

## 命令对照表

### 系统状态查看

| 操作 | macOS (Mole) | Windows | Linux |
|------|-------------|---------|-------|
| 系统状态 | `mo status` | 任务管理器 | `htop` |
| 磁盘使用 | `mo analyze` | `Storage Usage` | `ncdu` |
| 磁盘空间 | `df -h` | `Get-PSDrive` | `df -h` |

### 缓存清理

| 操作 | macOS (Mole) | Windows | Linux |
|------|-------------|---------|-------|
| 系统缓存 | `mo clean` | `cleanmgr` | `bleachbit` |
| 临时文件 | 自动 | `Remove-Item $env:TEMP\*` | `rm -rf /tmp/*` |
| 浏览器缓存 | `mo clean` | BleachBit | BleachBit |

### 应用卸载

| 操作 | macOS (Mole) | Windows | Linux |
|------|-------------|---------|-------|
| 卸载应用 | `mo uninstall` | Revo Uninstaller | `apt remove` |
| 残留清理 | 自动 | Revo Uninstaller | `apt purge` |

### 项目清理

| 操作 | macOS (Mole) | Windows | Linux |
|------|-------------|---------|-------|
| Node.js | `mo purge` | 手动删除 | 手动删除 |
| Python | `mo purge` | 手动删除 | 手动删除 |
| Rust | `mo purge` | 手动删除 | `cargo clean` |

---

## 平台检测脚本

在跨平台脚本中，可以这样检测平台：

```bash
#!/bin/bash

# 检测操作系统
OS="$(uname -s)"
case "${OS}" in
  Linux*)     machine=Linux;;
  Darwin*)    machine=Mac;;
  MINGW*MSYS*)machine=Windows;;
  *)          machine="UNKNOWN:${OS}"
esac

echo "检测到平台: ${machine}"

# 根据平台执行不同命令
if [ "${machine}" = "Mac" ]; then
  # macOS 命令
  mo clean --dry-run
elif [ "${machine}" = "Linux" ]; then
  # Linux 命令
  sudo apt clean
elif [ "${machine}" = "Windows" ]; then
  # Windows 命令
  cleanmgr
fi
```

PowerShell 版本：

```powershell
# 检测平台
if ($IsMacOS) {
    # macOS 命令
    mo clean --dry-run
} elseif ($IsLinux) {
    # Linux 命令
    sudo apt clean
} elseif ($IsWindows) {
    # Windows 命令
    cleanmgr
}
```

---

## 建议

1. **macOS 用户**
   - 使用 Mole（主要工具）
   - 参考 `mole-commands.md`

2. **Windows 用户**
   - 使用 BleachBit 和 Revo Uninstaller
   - 定期运行磁盘清理工具
   - 考虑使用 Storage Sense 自动清理

3. **Linux 用户**
   - 使用包管理器清理
   - BleachBit 和 Stacer
   - ncdu 进行磁盘分析

4. **跨平台项目**
   - 使用平台检测脚本
   - 为每个平台提供等效命令
   - 测试所有平台的功能

---

## 注意事项

1. Windows 和 Linux 的清理工具功能可能不如 Mole 全面
2. 某些功能可能需要组合多个工具才能实现
3. 建议在清理前备份重要数据
4. Linux 不同发行版的包管理器命令可能不同
5. Windows 工具通常需要管理员权限

---

## 参考资源

- **BleachBit**: https://www.bleachbit.org/
- **Revo Uninstaller**: https://www.revouninstaller.com/
- **Stacer**: https://oguzhaninan.github.io/Stacer-Web/
- **ncdu**: https://dev.yorhel.nl/ncdu
