---
name: docs-browser
description: 使用 Chrome DevTools MCP 自动浏览官方文档并查找内容。当用户使用 /docs 命令、请求查询官方文档、需要在文档网站中搜索特定API/功能说明、或提到"查一下文档"、"看看官方文档"、"文档中怎么说"时触发。支持任意URL的官方文档查询。
---

# 文档浏览器 (Docs Browser)

通过 Chrome DevTools MCP 自动浏览官方文档，查找并提取用户需要的内容。

## 工作流程

### 1. 解析用户请求

从用户输入中提取：

- **文档URL**: 用户提供的官方文档地址
- **搜索关键词**: 用户想要查找的内容

示例输入：

- `/docs https://react.dev hooks` → URL: react.dev, 关键词: hooks
- `查一下Vue官方文档中的computed属性` → URL: vuejs.org, 关键词: computed
- `在 https://nodejs.org/docs 查找 fs.readFile` → URL: nodejs.org/docs, 关键词: fs.readFile

### 2. 打开文档页面

```
mcp__chrome-devtools__new_page(url: <文档URL>)
```

如果用户只提供了框架名称而非完整URL，使用常见官方文档地址：

- React: https://react.dev
- Vue: https://vuejs.org
- Angular: https://angular.dev
- Node.js: https://nodejs.org/docs
- TypeScript: https://www.typescriptlang.org/docs
- MDN: https://developer.mozilla.org

### 3. 获取页面快照

```
mcp__chrome-devtools__take_snapshot()
```

分析页面结构，识别：

- 搜索框元素
- 导航菜单
- 侧边栏目录
- 主要内容区域

### 4. 使用文档搜索功能

大多数官方文档都有搜索功能，优先使用：

```
# 定位搜索框
mcp__chrome-devtools__take_snapshot() # 获取元素uid
mcp__chrome-devtools__click(uid: <搜索按钮或搜索框uid>)
mcp__chrome-devtools__fill(uid: <搜索输入框uid>, value: <搜索关键词>)
mcp__chrome-devtools__press_key(key: "Enter")
```

### 5. 浏览搜索结果

```
mcp__chrome-devtools__take_snapshot() # 获取搜索结果
mcp__chrome-devtools__click(uid: <最相关结果的uid>) # 点击进入详情页
```

### 6. 提取内容

到达目标页面后：

```
mcp__chrome-devtools__take_snapshot() # 获取完整页面内容
```

如果内容较长，可以滚动查看：

```
mcp__chrome-devtools__press_key(key: "PageDown")
mcp__chrome-devtools__take_snapshot()
```

### 7. 整理并返回结果

将提取的内容整理为清晰的格式返回给用户，包括：

- 相关API/功能的说明
- 代码示例
- 重要注意事项
- 文档原始链接

## 常用操作参考

### 页面导航

```
mcp__chrome-devtools__navigate_page(type: "back")  # 返回上一页
mcp__chrome-devtools__navigate_page(type: "forward")  # 前进
mcp__chrome-devtools__navigate_page(type: "reload")  # 刷新
```

### 等待页面加载

```
mcp__chrome-devtools__wait_for(text: <期望出现的文本>)
```

### 截图保存

```
mcp__chrome-devtools__take_screenshot(filePath: "./docs-screenshot.png")
```

### 执行JavaScript提取内容

```
mcp__chrome-devtools__evaluate_script(function: "() => { return document.querySelector('article').innerText }")
```

## 处理常见情况

### 搜索框难以定位

很多网站使用快捷键打开搜索：

```
mcp__chrome-devtools__press_key(key: "Control+k")  # 或 "Meta+k" (Mac)
mcp__chrome-devtools__press_key(key: "/")  # 部分网站使用 / 键
```

### 内容在iframe中

使用 `mcp__chrome-devtools__list_pages()` 查看所有页面，必要时切换。

### 需要滚动加载

```
mcp__chrome-devtools__press_key(key: "End")  # 滚动到底部
mcp__chrome-devtools__press_key(key: "Home")  # 滚动到顶部
```

### 弹窗/对话框

```
mcp__chrome-devtools__handle_dialog(action: "dismiss")  # 关闭弹窗
```

## 示例：查询React Hooks文档

```
1. mcp__chrome-devtools__new_page(url: "https://react.dev")
2. mcp__chrome-devtools__take_snapshot()  # 找到搜索按钮
3. mcp__chrome-devtools__press_key(key: "Meta+k")  # 打开搜索
4. mcp__chrome-devtools__take_snapshot()  # 获取搜索框uid
5. mcp__chrome-devtools__fill(uid: "xxx", value: "useState")
6. mcp__chrome-devtools__press_key(key: "Enter")
7. mcp__chrome-devtools__take_snapshot()  # 查看搜索结果
8. mcp__chrome-devtools__click(uid: "yyy")  # 点击第一个结果
9. mcp__chrome-devtools__take_snapshot()  # 提取内容
```

## 注意事项

- 始终先用 `take_snapshot()` 了解页面结构再进行操作
- 等待页面加载完成后再进行下一步操作
- 如果操作失败，尝试刷新页面或使用替代方法
- 保持操作链路简短，避免不必要的页面跳转
