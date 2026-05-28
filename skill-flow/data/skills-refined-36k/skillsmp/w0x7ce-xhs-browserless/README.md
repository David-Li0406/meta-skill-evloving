# 小红书发布 Skill - 详细说明

## 目录

- [架构原理](#架构原理)
- [会话保持机制](#会话保持机制)
- [使用指南](#使用指南)
- [配置说明](#配置说明)
- [故障排除](#故障排除)

---

## 架构原理

### 工作流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                          本地环境                                     │
│  ┌────────────────────┐                    ┌───────────────────────┐ │
│  │   xhs_login.py     │                    │    publish.ts         │ │
│  │                    │                    │                       │ │
│  │  1. 连接 Browserless│                    │  1. 连接 Browserless  │ │
│  │  2. 显示二维码      │                    │  2. 加载保存的 state  │ │
│  │  3. 扫码登录        │                    │  3. 使用登录会话      │ │
│  │  4. 保存 state     │                    │  4. 发布笔记          │ │
│  └────────┬───────────┘                    └───────────────────────┘ │
│           │                                                        │
│           │ 保存                                                    │ │
│           ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │         xhs_browser_state.json                              │  │
│  │                                                              │  │
│  │         {                                                    │  │
│  │           "cookies": [...],      ← 登录凭证                  │  │
│  │           "origins": [{          ← localStorage/SessionStorage  │
│  │             "localStorage": {...}                             │  │
│  │           }]                                                  │  │
│  │         }                                                    │  │
│  │                                                              │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ WebSocket (CDP)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    远程 Browserless 服务器                           │
│                    ws://hk2.w0x7ce.eu:10086                          │
│                                                                      │
│    ┌─────────────────────────────────────────────────────────────┐ │
│    │              Chrome 浏览器实例                               │ │
│    │                                                              │ │
│    │   ┌──────────────┐      ┌──────────────┐                   │ │
│    │   │  Context 1   │      │  Context 2   │                   │ │
│    │   │              │      │              │                   │ │
│    │   │  包含登录     │      │  从 state    │                   │ │
│    │   │  后的 cookies│      │  恢复的会话   │                   │ │
│    │   └──────────────┘      └──────────────┘                   │ │
│    └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 会话保持机制

### 核心原理

这个 skill 通过 **Browser State 持久化** 来确保使用同一个登录会话：

1. **登录时保存**：`xhs_login.py` 登录成功后，将浏览器的完整状态保存到 `xhs_browser_state.json`
2. **发布时加载**：`publish.ts` 连接到 Browserless 后，从 `xhs_browser_state.json` 恢复浏览器状态
3. **同一服务器**：两个脚本连接到同一个 Browserless 服务器

### State 文件内容

`xhs_browser_state.json` 包含：

```json
{
  "cookies": [
    {
      "name": "web_session",
      "value": "xxx",
      "domain": ".xiaohongshu.com",
      "path": "/",
      "expires": 1737723945.558455,
      "httpOnly": true,
      "secure": true,
      "sameSite": "Lax"
    }
  ],
  "origins": [
    {
      "origin": "https://www.xiaohongshu.com",
      "localStorage": [
        {
          "name": "user-token",
          "value": "xxx"
        }
      ]
    }
  ]
}
```

这些数据让浏览器"记住"登录状态。

---

## 使用指南

### Step 1: 登录（一次性）

```bash
cd /home/w0x7ce/Downloads/AOMG

python3 w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/xhs_login.py
```

**执行过程：**

```
============================================================
🚀 小红书登录工具 - 远程 Browserless 扫码登录
============================================================
🔗 Browserless: ws://hk2.w0x7ce.eu:10086?token=255=ff
💾 状态文件: xhs_browser_state.json
============================================================

🔗 连接到 Browserless...
🆕 创建浏览器上下文...
🌐 打开小红书首页...
⏳ 等待页面加载...

✅ 二维码已保存: screenshots_xhs/xhs_qr_20250123_142030.png

============================================================
📱 请用小红书 APP 扫描二维码登录
============================================================

步骤:
1. 打开小红书 APP
2. 点击「我」→「设置」→「扫一扫」
3. 扫描上方二维码图片
4. 在手机上确认登录

扫描完成后按 Enter 继续...
```

**手机扫码后按 Enter：**

```
⏳ 等待登录完成...
📄 当前页面: 小红书 - 你的生活兴趣社区
🔗 当前 URL: https://www.xiaohongshu.com/explore
📸 登录后截图: screenshots_xhs/xhs_logged_in_20250123_142030.png

💾 保存登录状态到: xhs_browser_state.json
✅ 状态文件已保存 (4523 bytes)
✅ 登录状态已保存！现在可以使用发布脚本了
```

### Step 2: 发布笔记

```bash
export XHS_WS_URL="ws://hk2.w0x7ce.eu:10086?token=255=ff"

# 发布文字笔记
npx -y bun w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/scripts/publish.ts \
  publish "今天天气真好" "分享一下今天的日常风景 #生活"

# 发布图片笔记
npx -y bun w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/scripts/publish.ts \
  publish "美食分享" "今天做了好吃的" \
  --images /path/to/food1.jpg /path/to/food2.jpg
```

**执行过程：**

```
🔗 连接到 Browserless: ws://hk2.w0x7ce.eu:10086?token=255=ff
📂 加载登录状态: xhs_browser_state.json

📝 开始发布笔记...
📌 标题: 美食分享
✍️  内容: 今天做了好吃的
📷 图片: 2 张
🌐 访问小红书首页...
🔍 查找发布按钮...
✅ 找到发布按钮
📷 上传图片...
✅ 上传: /path/to/food1.jpg
✅ 上传: /path/to/food2.jpg
📌 输入标题...
✅ 标题已输入
✍️  输入内容...
✅ 内容已输入
📸 截图: screenshots_xhs/before_publish_20250123_142105.png

==================================================
⚠️  请检查截图确认内容
💡 然后在浏览器中手动点击发布按钮
==================================================
```

---

## 配置说明

### 环境变量

| 变量 | 说明 | 默认值 | 必填 |
|------|------|--------|------|
| `XHS_WS_URL` | Browserless WebSocket 地址 | `ws://localhost:9222` | ✅ |
| `XHS_STATE_FILE` | 登录状态文件路径 | `xhs_browser_state.json` | ❌ |

### 确保使用同一环境的关键配置

**1. 相同的 Browserless 服务器**

两个脚本必须连接到同一个 Browserless：

```bash
# 方法 1: 使用环境变量
export XHS_WS_URL="ws://hk2.w0x7ce.eu:10086?token=255=ff"

# 方法 2: 在脚本中配置（默认值）
# xhs_login.py 第 13 行
WS_URL = "ws://hk2.w0x7ce.eu:10086?token=255=ff"

# publish.ts 第 16 行
const WS_URL = process.env.XHS_WS_URL || "ws://hk2.w0x7ce.eu:10086?token=255=ff";
```

**2. 相同的 State 文件路径**

默认使用 `xhs_browser_state.json`，确保两个脚本使用相同路径：

```bash
# 登录脚本保存到
STATE_FILE = "xhs_browser_state.json"

# 发布脚本读取自
const STATE_FILE = process.env.XHS_STATE_FILE || "xhs_browser_state.json";
```

**验证配置是否一致：**

```bash
# 检查登录脚本配置
grep WS_URL w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/xhs_login.py

# 检查发布脚本配置
grep WS_URL w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/scripts/publish.ts

# 确认 state 文件存在
ls -la xhs_browser_state.json
```

---

## 故障排除

### 问题 1: "未找到登录状态文件"

```
❌ 未找到登录状态文件!
请先运行: python3 xhs_login.py
```

**原因**：没有先运行登录脚本

**解决**：
```bash
python3 w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/xhs_login.py
```

---

### 问题 2: "未找到发布按钮"

```
❌ 未找到发布按钮，可能需要重新登录
```

**原因**：登录状态过期或无效

**解决**：
```bash
# 1. 删除旧的 state 文件
rm xhs_browser_state.json

# 2. 重新登录
python3 w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/xhs_login.py
```

---

### 问题 3: 连接失败

```
❌ CDP 连接超时
```

**原因**：Browserless 服务器不可达

**解决**：
1. 检查服务器是否运行：`curl http://your-server:port`
2. 检查防火墙设置
3. 确认 WebSocket URL 正确

---

### 问题 4: 发布后仍然要求登录

**原因**：state 文件与 Browserless 服务器不匹配

**检查**：
```bash
# 确认两个脚本使用相同的 WS URL
echo $XHS_WS_URL

# 查看 state 文件修改时间
ls -la xhs_browser_state.json

# 如果太久没登录，重新登录
rm xhs_browser_state.json
python3 w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/xhs_login.py
```

---

## 文件结构

```
w0x7ce-xiaohongshu-publisher/
├── README.md              ← 本文档
├── SKILL.md               ← Skill 简要说明
├── xhs_login.py           ← 登录脚本（根目录）
└── scripts/
    └── publish.ts         ← 发布脚本
```

---

## 安全建议

1. **保护 State 文件**
   ```bash
   # 添加到 .gitignore
   echo "xhs_browser_state.json" >> .gitignore
   ```

2. **使用加密连接**
   ```bash
   # 生产环境使用 wss:// 而不是 ws://
   export XHS_WS_URL="wss://your-server:port?token=xxx"
   ```

3. **定期更新登录**
   - 登录状态有时效性（通常几天到一周）
   - 定期重新登录保持会话有效

---

## 常见问题

**Q: 可以在多台机器上使用吗？**

A: 可以，但需要：
1. 每台机器都运行 `xhs_login.py` 登录
2. 或者复制 `xhs_browser_state.json` 到其他机器（不推荐，有安全风险）

**Q: 登录状态能保持多久？**

A: 通常 3-7 天，取决于小红书的 cookie 过期时间

**Q: 如何确认使用的是登录后的环境？**

A: 运行 `check` 命令：
```bash
npx -y bun w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/scripts/publish.ts check
```
如果显示 `✅ 已登录`，说明配置正确。

---

## 技术支持

如遇问题，请检查：
1. Browserless 服务器是否正常运行
2. `xhs_browser_state.json` 是否存在且有效
3. 网络连接是否正常
4. 截图文件 `screenshots_xhs/` 中的内容辅助排查
