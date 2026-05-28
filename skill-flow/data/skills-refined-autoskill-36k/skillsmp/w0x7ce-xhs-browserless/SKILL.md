---
name: w0x7ce-xhs-browserless
description: Publish to Xiaohongshu (Little Red Book) via remote Browserless CDP. Cookie-based login, auto-publish, supports multi-image posts. No local browser needed.
---

# XHS Browserless - 小红书远程浏览器发布工具

基于 Browserless 远程浏览器自动化发布小红书笔记，无需本地浏览器。

## 特点

- **Browserless 远程控制** - 通过 CDP 连接远程浏览器，无需本地 Chrome
- **Cookie 登录** - 从浏览器复制粘贴，无需扫码
- **自动发布** - 填写标题、内容、上传图片、点击发布
- **会话保持** - 登录状态自动保存

## 快速开始

### 1. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填写你的 Browserless 服务器地址
# vim .env 或 nano .env
```

### 2. 获取 Cookie

```bash
# 1. 浏览器登录 https://www.xiaohongshu.com
# 2. F12 → Application → Cookies → xiaohongshu.com
# 3. 全选 → 复制
# 4. 粘贴到 cookies.txt (参考 cookies.txt.example)
```

### 3. 登录

```bash
python3 ${SKILL_DIR}/xhs_login.py --file
```

### 4. 发布笔记

```bash
python3 ${SKILL_DIR}/scripts/xhs_publish.py \
  --title "标题" \
  --content "内容" \
  --image /path/to/image.png \
  --submit
```

---

## 命令

### 登录

```bash
python3 ${SKILL_DIR}/xhs_login.py --file    # 使用 cookies.txt 登录
```

### 发布

```bash
python3 ${SKILL_DIR}/scripts/xhs_publish.py --title "标题" --content "内容" --image 图片.png --submit
```

| 参数 | 说明 |
|------|------|
| `--title <text>` | 标题（必需） |
| `--content <text>` | 内容（必需） |
| `--image <path>` | 图片文件路径（必需） |
| `--submit` | 实际发布（默认预览） |

---

## 完整示例

### 发布单图笔记

```bash
python3 ${SKILL_DIR}/scripts/xhs_publish.py \
  --title "今日穿搭分享 👗" \
  --content "今天分享一套超级好看的春日穿搭！\n\n#OOTD #春日穿搭 #时尚分享" \
  --image ./outfit.png \
  --submit
```

---

## 配置

### 环境变量 (.env)

| 变量 | 说明 | 必需 |
|------|------|------|
| `XHS_WS_URL` | Browserless WebSocket URL | ✅ 是 |
| `XHS_STATE_FILE` | 登录状态文件路径 | 否 |
| `XHS_COOKIE_FILE` | Cookie 文件路径 | 否 |
| `XHS_SCREENSHOTS` | 启用截图调试 (设为 1) | 否 |

示例 `.env` 文件：

```bash
# Browserless 服务器地址 (必需)
XHS_WS_URL=ws://your-browserless-server:10086?token=your-token

# 状态文件路径 (可选)
# XHS_STATE_FILE=/path/to/xhs_browser_state.json

# Cookie 文件路径 (可选)
# XHS_COOKIE_FILE=/path/to/cookies.txt

# 启用截图调试 (可选)
# XHS_SCREENSHOTS=1
```

### Cookie 文件

- **文件位置**: `cookies.txt` (参考 `cookies.txt.example`)
- **格式**: 浏览器导出的制表符格式
- **获取方式**:
  1. 浏览器登录 https://www.xiaohongshu.com
  2. F12 → Application → Cookies → xiaohongshu.com
  3. 全选 → 复制
  4. 粘贴到 `cookies.txt`

---

## 工作流程

```
┌─────────────────────────────────────────────────────┐
│ 1. 复制 .env.example 为 .env 并配置服务器地址       │
│ 2. 浏览器复制 Cookie → cookies.txt                   │
│ 3. python3 xhs_login.py --file (保存登录状态)      │
│ 4. python3 xhs_publish.py --title "xxx" --content   │
│    "xxx" --image photo.png --submit (远程发布)       │
└─────────────────────────────────────────────────────┘
```

---

## 会话管理

### Cookie 过期更新

```bash
# 1. 浏览器复制新 Cookie
# 2. 粘贴到 cookies.txt
# 3. 重新登录
python3 ${SKILL_DIR}/xhs_login.py --file
```

### Cookie 有效期

- 通常 **7-30 天**
- 过期后需要重新获取

---

## 图片要求

| 项目 | 要求 |
|------|------|
| 格式 | JPG, PNG, WebP |
| 数量 | 1-9 张 |
| 尺寸 | 小于 10MB/张 |
| 比例 | 推荐 3:4 (竖图) |

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| **未登录** | 运行 `python3 xhs_login.py --file` |
| **Cookie 过期** | 浏览器重新获取 Cookie 更新 cookies.txt |
| **连接失败** | 检查 .env 中的 Browserless 服务器地址 |
| **发布失败** | 设置 `XHS_SCREENSHOTS=1` 查看截图 |

---

## 文件结构

```
w0x7ce-xhs-browserless/
├── .env.example           # 环境变量模板
├── .gitignore             # Git 忽略文件
├── xhs_login.py           # 登录脚本
├── cookies.txt.example    # Cookie 模板
├── scripts/
│   ├── xhs_publish.py     # 发布脚本 (Python)
│   └── publish.ts         # 发布脚本 (TypeScript)
├── SKILL.md               # 本文件
└── README.md              # 详细文档
```

---

## 安全建议

1. **保护 .env** - 包含服务器地址，不要分享
2. **保护 Cookie** - cookies.txt 包含登录凭证，不要分享
3. **定期更新** - Cookie 过期后及时更新
4. **使用加密** - 生产环境使用 WSS 而不是 WS
