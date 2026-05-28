---
name: browser-debugging
description: Use this skill for browser debugging and testing when explicitly requested by the user.
---

# Browser Debugging Skill (Chrome DevTools)

This skill is for browser debugging and testing, **only to be used when explicitly requested by the user**.

## ⚠️ Important

**Do not execute tests by default**. Follow the rule: do not test, compile, or run unless explicitly requested by the user.

## Usage Scenarios

Trigger this skill when the user says:
- "帮我测试一下" (Help me test)
- "运行测试" (Run the test)
- "检查浏览器" (Check the browser)
- "调试页面" (Debug the page)

## Calling Process

```javascript
// 1. Connect to the browser
chrome_devtools.connect()

// 2. Perform actions
chrome_devtools.navigate("http://localhost:3000")
chrome_devtools.click("#submit-btn")
chrome_devtools.type("#email", "test@example.com")

// 3. Screenshot/Check
chrome_devtools.screenshot()
chrome_devtools.evaluate("document.title")

// 4. Collect results and report
```

## Common Operations

### Navigation
```javascript
chrome_devtools.navigate("url")
chrome_devtools.reload()
chrome_devtools.back()
```

### Interaction
```javascript
chrome_devtools.click("selector")
chrome_devtools.type("selector", "text")
chrome_devtools.select("selector", "value")
```

### Inspection
```javascript
chrome_devtools.screenshot()
chrome_devtools.evaluate("js expression")
chrome_devtools.getHTML("selector")
```

### Network
```javascript
chrome_devtools.getNetworkRequests()
chrome_devtools.waitForRequest("url pattern")
```

## Test Result Reporting

After completing the test, report results using:

```javascript
寸止.feedback({
  summary: "测试完成",
  results: [
    "✅ 登录流程正常",
    "✅ 表单验证正确",
    "❌ 提交按钮样式异常"
  ],
  screenshots: ["login-page.png", "error-state.png"]
})
```

## Downgrade Plan

If chrome-devtools is unavailable, provide manual testing steps guidance.