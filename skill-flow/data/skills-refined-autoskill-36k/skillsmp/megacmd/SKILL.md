---
name: megacmd
description: MEGA 云存储命令行工具，支持文件上传、下载、同步、备份和分享
---

# MEGAcmd

MEGA 云存储的命令行工具，提供完整的文件管理功能。

## 路径配置

```bash
# macOS 命令路径
/Applications/MEGAcmd.app/Contents/MacOS/

# 调用方式
bash -c 'PATH=/Applications/MEGAcmd.app/Contents/MacOS:$PATH mega-命令'
```

## 常用命令

### 账户管理
| 命令 | 说明 |
|------|------|
| `mega-login email password` | 登录账户 |
| `mega-logout` | 登出 |
| `mega-whoami` | 查看当前登录状态 |
| `mega-df` | 查看存储空间使用情况 |

### 浏览文件
| 命令 | 说明 |
|------|------|
| `mega-ls [路径]` | 列出文件/文件夹 |
| `mega-cd 路径` | 切换远程目录 |
| `mega-pwd` | 显示当前远程目录 |
| `mega-tree [路径]` | 树形显示目录结构 |
| `mega-find [路径] --pattern=模式` | 搜索文件 |
| `mega-du [-h] [路径]` | 查看文件/文件夹大小 |

### 文件操作
| 命令 | 说明 |
|------|------|
| `mega-get 远程路径 [本地路径]` | 下载文件/文件夹 |
| `mega-put 本地路径 [远程路径]` | 上传文件/文件夹 |
| `mega-mkdir 路径` | 创建远程目录 |
| `mega-cp 源路径 目标路径` | 复制文件 |
| `mega-mv 源路径 目标路径` | 移动/重命名文件 |
| `mega-rm [-r] 路径` | 删除文件（-r 递归删除目录）|

### 分享
| 命令 | 说明 |
|------|------|
| `mega-export -a 路径` | 创建分享链接 |
| `mega-export -d 路径` | 删除分享链接 |
| `mega-export` | 列出所有分享 |
| `mega-import 链接 [路径]` | 导入分享链接内容 |

### 同步与备份
| 命令 | 说明 |
|------|------|
| `mega-sync 本地路径 远程路径` | 设置双向同步 |
| `mega-sync` | 列出所有同步配置 |
| `mega-sync -d ID` | 删除同步配置 |
| `mega-backup 本地路径 远程路径 --period="cron表达式"` | 设置定时备份 |

### 传输管理
| 命令 | 说明 |
|------|------|
| `mega-transfers` | 查看传输列表 |
| `mega-transfers -c TAG` | 取消传输 |
| `mega-speedlimit [-u\|-d] 速度` | 设置上传/下载速度限制 |

## 使用示例

### 下载文件夹
```bash
bash -c 'PATH=/Applications/MEGAcmd.app/Contents/MacOS:$PATH mega-get /云端文件夹 /本地目录/'
```

### 上传文件
```bash
bash -c 'PATH=/Applications/MEGAcmd.app/Contents/MacOS:$PATH mega-put /本地文件.pdf /云端目录/'
```

### 创建分享链接（带过期时间）
```bash
bash -c 'PATH=/Applications/MEGAcmd.app/Contents/MacOS:$PATH mega-export -a /路径 --expire=7d'
```

### 设置同步
```bash
bash -c 'PATH=/Applications/MEGAcmd.app/Contents/MacOS:$PATH mega-sync ~/本地文件夹 /云端文件夹'
```

## 注意事项

1. 大文件下载可能超时，建议使用 `nohup` 后台运行
2. 首次使用需要先 `mega-login` 登录
3. 路径中有空格需要用引号包裹
4. 使用 `mega-logout --keep-session` 可以保留会话，下次自动登录

## 参考文档

- 官方文档: https://mega.nz/cmd
- GitHub: https://github.com/meganz/MEGAcmd
- 详细用户指南: https://raw.githubusercontent.com/meganz/MEGAcmd/master/UserGuide.md
