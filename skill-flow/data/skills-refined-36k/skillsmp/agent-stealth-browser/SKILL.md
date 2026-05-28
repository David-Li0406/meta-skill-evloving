---
name: agent-stealth-browser
description: Stealth 模式的浏览器自动化 MCP 工具，能够绕过反爬检测（如 Cloudflare、reCAPTCHA 等）。完全兼容 agent-browser API。当需要操作有反爬保护的网站时使用此工具，包括：(1) 访问受保护页面 (2) 自动登录需要验证的网站 (3) 表单填写和提交 (4) 截图和数据提取 (5) 持久化登录状态
---

# Agent Stealth Browser

与 agent-browser 兼容的 Stealth 模式浏览器 MCP 工具。

## MCP 配置

```json
{
  "mcpServers": {
    "stealth-browser": {
      "command": "uvx",
      "args": ["agent-stealth-browser"]
    }
  }
}
```

## 核心工作流

1. 导航: `browser_navigate {"url": "<url>"}`
2. 快照: `browser_snapshot {}` (返回带 @ref 的元素列表)
3. 交互: 使用快照中的 @ref 进行操作
4. 页面变化后重新获取快照

## 工具列表

### 导航
```
browser_navigate {"url": "<url>"}           # 导航到 URL
browser_close {}                            # 关闭浏览器
```

### 快照 (页面分析)
```
browser_snapshot {}                         # 获取可交互元素
browser_snapshot {"interactive_only": true} # 仅交互元素（默认）
```

### 交互 (使用快照中的 @ref)
```
browser_click {"target": "@e1"}                          # 点击
browser_fill {"target": "@e2", "text": "内容"}           # 清空并填写
browser_type {"target": "@e2", "text": "内容"}           # 逐字输入
browser_press {"key": "Enter"}                           # 按键
browser_hover {"target": "@e1"}                          # 悬停
browser_select {"target": "@e1", "value": "选项值"}      # 下拉选择
browser_scroll {"direction": "down", "amount": 500}      # 滚动
```

### 获取信息
```
browser_get {"what": "text", "target": "@e1"}  # 获取文本
browser_get {"what": "html", "target": "@e1"}  # 获取 HTML
browser_get {"what": "value", "target": "@e1"} # 获取输入值
browser_get {"what": "title"}                  # 获取标题
browser_get {"what": "url"}                    # 获取 URL
```

### 截图
```
browser_screenshot {}                          # 当前视口截图
browser_screenshot {"full_page": true}         # 全页面截图
browser_screenshot {"selector": "@e1"}         # 指定元素截图
```

### 等待
```
browser_wait {"ms": 2000}                      # 等待毫秒
browser_wait {"selector": ".success"}          # 等待元素出现
```

### Cookie 持久化
```
browser_cookies_save {"domain": "example"}     # 保存登录状态
browser_cookies_load {"domain": "example"}     # 加载登录状态
```

### JavaScript
```
browser_eval {"script": "document.title"}      # 执行 JS
```

## 示例: 表单提交

```
browser_navigate {"url": "https://example.com/form"}
browser_snapshot {}
# 输出: @e1 textbox "Email", @e2 textbox "Password", @e3 button "Submit"

browser_fill {"target": "@e1", "text": "user@example.com"}
browser_fill {"target": "@e2", "text": "password123"}
browser_click {"target": "@e3"}
browser_wait {"ms": 2000}
browser_snapshot {}  # 检查结果
```

## 示例: 保存登录状态

```
# 登录成功后保存
browser_cookies_save {"domain": "mysite"}

# 下次使用时加载
browser_navigate {"url": "https://mysite.com"}
browser_cookies_load {"domain": "mysite"}
browser_navigate {"url": "https://mysite.com"}  # 刷新应用 cookies
```

## 与 agent-browser 的区别

| 特性 | agent-browser | agent-stealth-browser |
|------|---------------|----------------------|
| Stealth 模式 | ❌ | ✅ |
| 反爬绕过 | ❌ | ✅ |
| Cookie 持久化 | ❌ | ✅ |
| API 兼容性 | - | 100% |

## 调试技巧

- 元素找不到: 先滚动 `browser_scroll {"direction": "down"}` 再重新快照
- 需要等待: 使用 `browser_wait {"ms": 2000}` 或 `browser_wait {"selector": ".element"}`
- 检查状态: 使用 `browser_screenshot {}` 查看当前页面
