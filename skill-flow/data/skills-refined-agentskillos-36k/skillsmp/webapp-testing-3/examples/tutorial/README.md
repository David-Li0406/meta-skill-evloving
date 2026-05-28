# Web应用测试教程

使用 Playwright 进行 Web 应用自动化测试的完整实践教程。从基础HTML测试到复杂SPA应用，配套可运行示例，循序渐进掌握 Web 自动化测试技能。

## 目录

- [教程简介](#教程简介)
- [快速开始](#快速开始)
- [学习路径](#学习路径)
- [入门级示例](#入门级示例)
- [中级示例](#中级示例)
- [高级示例](#高级示例)
- [最佳实践](#最佳实践)
- [常见问题FAQ](#常见问题faq)
- [快速参考](#快速参考)
- [进阶资源](#进阶资源)

---

## 教程简介

### 这个教程适合谁？

- 🎯 想学习 Web 自动化测试的开发者
- 🎯 需要测试前端应用的QA工程师
- 🎯 想提高测试技能的全栈开发者
- 🎯 对 Playwright 感兴趣的技术人员

### 你将学到什么？

✅ **基础技能**
- 使用 Playwright 自动化浏览器操作
- 查找和操作页面元素
- 捕获截图进行视觉验证

✅ **中级技能**
- 自动化表单填写和提交
- 处理 JavaScript 渲染的动态内容
- 捕获和分析浏览器控制台日志

✅ **高级技能**
- 测试单页应用（SPA）的客户端路由
- 进行前后端集成测试
- 编写完整的端到端测试套件

### 教程特色

- 📚 **9个渐进式示例** - 从简单到复杂，循序渐进
- 🚀 **开箱即用** - 所有示例都可直接运行
- 💡 **实用导向** - 基于真实场景的测试案例
- 🎓 **配套练习** - 每个示例都有练习题巩固知识
- ⏱️ **时间规划** - 明确每个示例的学习时间

---

## 快速开始

### 环境准备

**1. 安装依赖**

```bash
# 安装 Playwright Python 库
pip install playwright

# 安装 Chromium 浏览器
playwright install chromium
```

**2. 验证安装**

```bash
# 进入教程目录
cd .codebuddy/skills/webapp-testing/examples/tutorial

# 查看可用命令
make help
```

### 运行第一个示例

```bash
# 方式1: 使用 make 命令 (推荐)
make 01

# 方式2: 直接运行 Python 脚本
cd beginner/01_static_html
python test_static.py
```

**预期输出：**
```
✓ Loaded: file:///path/to/sample.html
✓ Page title: Welcome to Web Testing
✓ Main heading: Hello, Playwright!
...
✓ Test completed successfully!
```

恭喜！🎉 你已经成功运行了第一个 Web 自动化测试！

---

## 学习路径

### 学习路线图

```
🟢 入门级 (1小时)           🟡 中级 (1.5小时)          🔴 高级 (2小时)
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  01 静态HTML      │ ───> │  04 表单自动化     │ ───> │  07 SPA测试       │
│  ⏱️ 15分钟        │      │  ⏱️ 25分钟        │      │  ⏱️ 30分钟        │
└──────────────────┘      └──────────────────┘      └──────────────────┘
         │                         │                         │
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  02 元素发现      │      │  05 动态内容⭐     │      │  08 服务器集成    │
│  ⏱️ 20分钟        │      │  ⏱️ 30分钟        │      │  ⏱️ 35分钟        │
└──────────────────┘      └──────────────────┘      └──────────────────┘
         │                         │                         │
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  03 截图测试      │      │  06 控制台调试     │      │  09 综合套件⭐     │
│  ⏱️ 15分钟        │      │  ⏱️ 20分钟        │      │  ⏱️ 45分钟        │
└──────────────────┘      └──────────────────┘      └──────────────────┘

⭐ = 重点示例
```

### 推荐学习顺序

**第1天：入门级** (完成示例 01-03)
- 掌握基础的浏览器自动化操作
- 学习页面元素的查找和检查
- 了解截图的使用方法

**第2天：中级** (完成示例 04-06)
- 掌握表单自动化填写
- **重点：学习处理动态内容的等待策略** ⭐
- 学习控制台日志的捕获和分析

**第3天：高级** (完成示例 07-09)
- 测试单页应用的路由和状态
- 进行前后端集成测试
- **重点：编写完整的测试套件** ⭐

---

## 入门级示例

### 示例01：静态HTML测试

**📝 学习目标**
- 加载本地 HTML 文件
- 使用 `file://` 协议
- 提取页面标题和内容
- 理解 Playwright 上下文管理器模式

**📋 前置知识**
- 基础 HTML 知识
- Python 基础语法

**⏱️ 预计时间：15分钟**

**🚀 运行命令**
```bash
make 01
# 或
make static-html
```

**🎯 练习题**

1. **基础练习**：修改测试脚本，提取页面中的第二个段落文本
2. **进阶练习**：统计页面中所有 `<li>` 元素的数量
3. **挑战练习**：创建一个新的 HTML 文件和对应的测试脚本

<details>
<summary>💡 查看提示</summary>

```python
# 练习1提示
second_paragraph = page.locator('p').nth(1).inner_text()

# 练习2提示
li_count = len(page.locator('li').all())

# 练习3提示
# 1. 创建 my_page.html
# 2. 复制 test_static.py 为 my_test.py
# 3. 修改文件路径指向你的 HTML 文件
```
</details>

---

### 示例02：元素发现

**📝 学习目标**
- 使用不同的选择器策略（标签、类、ID、文本、属性）
- 区分可见元素和隐藏元素
- 提取元素属性（href、name、placeholder等）
- 遍历多个匹配的元素

**📋 前置知识**
- CSS 选择器基础
- HTML 元素属性

**⏱️ 预计时间：20分钟**

**🚀 运行命令**
```bash
make 02
# 或
make discovery
```

**🎯 练习题**

1. **基础练习**：找出所有包含 "test" 文本的元素
2. **进阶练习**：提取所有表单输入框的 `name` 属性值
3. **挑战练习**：创建一个函数，自动发现页面上所有交互元素（按钮、链接、输入框）

<details>
<summary>💡 查看提示</summary>

```python
# 练习1提示
elements = page.locator('text=test').all()

# 练习2提示
inputs = page.locator('input').all()
names = [inp.get_attribute('name') for inp in inputs]

# 练习3提示
def discover_interactive_elements(page):
    return {
        'buttons': page.locator('button').all(),
        'links': page.locator('a').all(),
        'inputs': page.locator('input').all()
    }
```
</details>

---

### 示例03：截图测试

**📝 学习目标**
- 捕获全页面截图
- 捕获特定元素的截图
- 设置不同的视口尺寸（桌面、平板、手机）
- 组织截图输出文件

**📋 前置知识**
- 浏览器视口概念
- 响应式设计基础

**⏱️ 预计时间：15分钟**

**🚀 运行命令**
```bash
make 03
# 或
make screenshots
```

**💾 输出文件位置**
- `beginner/03_screenshots/screenshots/`

**🎯 练习题**

1. **基础练习**：添加一个 2560x1440 (4K) 视口的截图
2. **进阶练习**：创建一个循环，测试5种不同的视口尺寸
3. **挑战练习**：实现一个函数，自动截取页面中所有卡片元素的单独截图

<details>
<summary>💡 查看提示</summary>

```python
# 练习1提示
page.set_viewport_size({"width": 2560, "height": 1440})
page.screenshot(path='screenshots/4k.png', full_page=True)

# 练习2提示
viewports = [
    (1920, 1080),  # 桌面
    (1366, 768),   # 笔记本
    (768, 1024),   # 平板
    (414, 896),    # 手机
    (375, 667)     # 小屏手机
]
for width, height in viewports:
    page.set_viewport_size({"width": width, "height": height})
    page.screenshot(path=f'screenshots/{width}x{height}.png')

# 练习3提示
cards = page.locator('.card').all()
for i, card in enumerate(cards):
    card.screenshot(path=f'screenshots/card_{i+1}.png')
```
</details>

---

## 中级示例

### 示例04：表单自动化

**📝 学习目标**
- 填写文本输入框
- 选择下拉选项
- 勾选复选框和单选按钮
- 填写文本域
- 提交表单并验证结果

**📋 前置知识**
- HTML 表单元素（input、select、textarea、checkbox、radio）
- 表单提交流程

**⏱️ 预计时间：25分钟**

**🚀 运行命令**
```bash
make 04
# 或
make form
```

**💾 输出文件位置**
- `intermediate/04_form_automation/screenshots/`

**🎯 练习题**

1. **基础练习**：修改测试填写不同的表单数据（你的个人信息）
2. **进阶练习**：添加验证步骤，检查填写的数据是否正确显示
3. **挑战练习**：测试必填字段验证 - 尝试提交空表单，验证错误提示
4. **实战练习**：创建一个函数 `fill_form(data)` 接收字典参数自动填充表单

<details>
<summary>💡 查看提示</summary>

```python
# 练习4提示
def fill_form(page, data):
    """
    自动填充表单
    data = {
        'name': 'John',
        'email': 'john@example.com',
        'country': 'us',
        'message': 'Hello!',
        'newsletter': True
    }
    """
    page.fill('#name', data.get('name', ''))
    page.fill('#email', data.get('email', ''))
    page.select_option('#country', data.get('country', ''))
    page.fill('#message', data.get('message', ''))
    if data.get('newsletter'):
        page.check('#newsletter')
```
</details>

---

### 示例05：动态内容测试 ⭐

> **⚠️ 重要示例** - 这是整个教程中最关键的示例之一！

**📝 学习目标**
- 处理 JavaScript 渲染的内容
- 使用正确的等待策略（`networkidle`、`domcontentloaded`）
- 等待特定元素出现
- 测试异步数据加载

**📋 前置知识**
- JavaScript 异步编程基础
- AJAX/Fetch API 概念
- DOM 更新机制

**⏱️ 预计时间：30分钟**

**🚀 运行命令**
```bash
make 05
# 或
make dynamic
```

**🎓 核心知识点**

```python
# ❌ 错误做法 - 不等待直接操作
page.goto('http://localhost:3000')
page.click('#load-data')  # 可能失败！内容还没加载

# ✅ 正确做法1 - 等待网络空闲
page.goto('http://localhost:3000')
page.wait_for_load_state('networkidle')  # 关键！
page.click('#load-data')

# ✅ 正确做法2 - 等待特定元素
page.click('#load-data')
page.wait_for_selector('.data-loaded')  # 等待元素出现
```

**🎯 练习题**

1. **基础练习**：修改等待时间，观察使用 `wait_for_timeout()` 的不稳定性
2. **进阶练习**：测试快速连续点击按钮，验证是否能正确处理多次加载
3. **挑战练习**：实现一个通用的等待函数 `wait_for_content(selector, timeout=5000)`
4. **实战练习**：处理加载失败的情况 - 模拟网络错误并捕获

<details>
<summary>💡 查看提示</summary>

```python
# 练习3提示
def wait_for_content(page, selector, timeout=5000):
    """通用内容等待函数"""
    try:
        page.wait_for_selector(selector, timeout=timeout)
        return True
    except Exception as e:
        print(f"等待超时: {selector}")
        return False

# 使用示例
if wait_for_content(page, '.data-card'):
    print("内容已加载")
else:
    print("加载失败")
```
</details>

---

### 示例06：控制台调试

**📝 学习目标**
- 捕获浏览器控制台消息
- 按类型过滤消息（log、info、warning、error、debug）
- 调试 JavaScript 错误
- 将日志保存到文件

**📋 前置知识**
- 浏览器开发者工具 Console 面板
- JavaScript 控制台 API（console.log、console.error等）

**⏱️ 预计时间：20分钟**

**🚀 运行命令**
```bash
make 06
# 或
make console
```

**💾 输出文件位置**
- `intermediate/06_console_debugging/logs/`

**🎯 练习题**

1. **基础练习**：只捕获 error 类型的消息
2. **进阶练习**：实现消息计数器，统计各类型消息的数量
3. **挑战练习**：创建一个消息过滤器，只保存包含特定关键字的日志

<details>
<summary>💡 查看提示</summary>

```python
# 练习1提示
errors_only = []
page.on("console", lambda msg:
    errors_only.append(msg.text) if msg.type == 'error' else None
)

# 练习2提示
message_counts = {'log': 0, 'error': 0, 'warning': 0}
def count_messages(msg):
    if msg.type in message_counts:
        message_counts[msg.type] += 1

# 练习3提示
def filter_messages(msg, keywords=['API', 'Error', 'Failed']):
    if any(keyword in msg.text for keyword in keywords):
        print(f"[{msg.type}] {msg.text}")
```
</details>

---

## 高级示例

### 示例07：SPA测试

**📝 学习目标**
- 导航单页应用（SPA）
- 处理哈希路由（#/route）
- 验证 URL 变化而不刷新页面
- 测试浏览器前进/后退按钮
- 验证应用状态变化

**📋 前置知识**
- 单页应用（SPA）概念
- 客户端路由原理
- React Router、Vue Router 等框架的基础知识

**⏱️ 预计时间：30分钟**

**🚀 运行命令**
```bash
make 07
# 或
make spa
```

**🎓 核心知识点**

```python
# SPA 特点：URL 变化但页面不刷新
page.goto('http://localhost:3000')
page.wait_for_load_state('networkidle')  # 只需要一次

# 点击导航链接
page.click('a[href="#/about"]')
# ⚠️ 注意：没有页面重载！只需等待内容变化
page.wait_for_selector('.route-indicator')

# 验证 URL 改变
assert '#/about' in page.url
```

**🎯 练习题**

1. **基础练习**：测试所有导航链接是否正常工作
2. **进阶练习**：验证每个路由的页面标题是否正确
3. **挑战练习**：测试直接通过 URL 访问（深度链接）是否有效
4. **实战练习**：模拟用户快速切换路由，验证是否有竞态条件

<details>
<summary>💡 查看提示</summary>

```python
# 练习1提示
routes = ['/about', '/features', '/contact']
for route in routes:
    page.click(f'a[href="#{route}"]')
    page.wait_for_timeout(200)
    assert route in page.url, f"导航到 {route} 失败"

# 练习3提示
page.goto(f'{base_url}#/features')
page.wait_for_selector('.route-indicator')
heading = page.locator('h1').inner_text()
assert 'Features' in heading
```
</details>

---

### 示例08：服务器集成测试

**📝 学习目标**
- 使用 `with_server.py` 管理服务器生命周期
- 测试前后端集成
- 直接调用 API 端点
- 验证前端与后端的数据流

**📋 前置知识**
- HTTP 协议基础
- RESTful API 概念
- Flask 或其他 Web 框架基础

**⏱️ 预计时间：35分钟**

**🚀 运行命令**

```bash
# 方式1：使用 helper 脚本（推荐）
make 08

# 方式2：手动启动
# 终端1：
cd advanced/08_server_integration
python flask_app.py

# 终端2：
python test_with_server.py
```

**⚠️ 额外依赖**
```bash
pip install flask
```

**🎯 练习题**

1. **基础练习**：添加一个新的 API 端点 `/api/users` 并测试
2. **进阶练习**：测试 POST 请求 - 提交数据到服务器
3. **挑战练习**：测试错误处理 - 故意发送错误请求，验证服务器响应
4. **实战练习**：测试多个并发请求，验证服务器性能

<details>
<summary>💡 查看提示</summary>

```python
# 练习2提示 - POST请求
response = page.request.post(
    f'{base_url}/api/submit',
    data={'name': 'Test', 'email': 'test@example.com'}
)
assert response.status == 200

# 练习3提示 - 错误处理
response = page.request.get(f'{base_url}/api/nonexistent')
assert response.status == 404
```
</details>

---

### 示例09：综合测试套件 ⭐

> **⭐ 重点示例** - 综合运用所有学到的技术！

**📝 学习目标**
- 构建完整的端到端测试
- 编写可重用的辅助函数
- 组织大型测试代码
- 处理复杂的用户工作流
- 生成测试报告（截图 + 日志）

**📋 前置知识**
- 前面所有示例的内容
- 面向对象编程基础
- 测试最佳实践

**⏱️ 预计时间：45分钟**

**🚀 运行命令**
```bash
make 09
# 或
make ecommerce
```

**💾 输出文件位置**
- `advanced/09_comprehensive/screenshots/`

**🎯 练习题**

1. **基础练习**：添加一个新的测试 - 验证搜索功能对空查询的处理
2. **进阶练习**：实现数据驱动测试 - 用不同的产品数据运行相同的测试
3. **挑战练习**：添加断言失败时的自动截图功能
4. **实战练习**：将测试套件转换为 pytest 格式，使用 fixtures
5. **综合练习**：实现测试报告生成器 - 生成 HTML 格式的测试报告

<details>
<summary>💡 查看提示</summary>

```python
# 练习3提示 - 失败时截图
import traceback

def test_with_screenshot(page, test_func, screenshot_name):
    try:
        test_func()
    except Exception as e:
        page.screenshot(path=f'failures/{screenshot_name}.png')
        traceback.print_exc()
        raise

# 练习4提示 - pytest格式
import pytest

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

def test_add_to_cart(browser):
    page = browser.new_page()
    # ... 测试代码 ...
```
</details>

---

## 最佳实践

### 选择器策略（优先级从高到低）

1. **ARIA 角色**（最佳 - 可访问性优先）
   ```python
   page.locator('role=button[name="提交"]')
   ```

2. **文本内容**（可读性好）
   ```python
   page.locator('text=提交')
   ```

3. **测试ID**（如果有）
   ```python
   page.locator('[data-testid="submit-btn"]')
   ```

4. **ID 属性**
   ```python
   page.locator('#submit-btn')
   ```

5. **CSS 类**（最不稳定 - 容易变化）
   ```python
   page.locator('.btn-primary')  # 避免过度依赖
   ```

### 等待策略（优先级从高到低）

1. **等待网络空闲**（动态应用必备）
   ```python
   page.goto('http://localhost:3000')
   page.wait_for_load_state('networkidle')  # ✅ 最佳实践
   ```

2. **等待特定元素**（明确目标）
   ```python
   page.wait_for_selector('.result')  # ✅ 推荐
   ```

3. **固定延时**（最后手段）
   ```python
   page.wait_for_timeout(1000)  # ❌ 尽量避免
   ```

### 代码组织模式

#### 模式1：辅助函数

```python
class TestHelpers:
    @staticmethod
    def login(page, username, password):
        page.fill('#username', username)
        page.fill('#password', password)
        page.click('button:has-text("登录")')
        page.wait_for_selector('.dashboard')

# 使用
helpers = TestHelpers()
helpers.login(page, 'admin', 'password123')
```

#### 模式2：页面对象模式（POM）

```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator('#username')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('button:has-text("登录")')

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

# 使用
login_page = LoginPage(page)
login_page.login('admin', 'password123')
```

### 调试技巧

```python
# 1. 保存截图查看当前状态
page.screenshot(path='debug.png', full_page=True)

# 2. 打印页面内容
print(page.content())

# 3. 打印特定元素
print(page.locator('.element').inner_text())

# 4. 使用非 headless 模式观察
browser = p.chromium.launch(headless=False)
```

---

## 常见问题FAQ

### 安装和环境

**Q1: 如何安装 Playwright？**

```bash
pip install playwright
playwright install chromium
```

**Q2: 为什么提示找不到浏览器？**

A: 运行 `playwright install chromium` 安装浏览器。

**Q3: 可以使用其他浏览器吗？**

A: 可以！Playwright 支持 Chromium、Firefox 和 WebKit：
```python
browser = p.chromium.launch()  # Chrome/Edge
browser = p.firefox.launch()   # Firefox
browser = p.webkit.launch()    # Safari
```

### 元素查找

**Q4: 为什么找不到元素？**

常见原因：
1. ❌ 元素还没加载完成 → ✅ 使用 `wait_for_load_state('networkidle')`
2. ❌ 元素在 iframe 中 → ✅ 使用 `page.frame_locator()`
3. ❌ 选择器错误 → ✅ 截图查看页面实际内容
4. ❌ 元素被隐藏 → ✅ 使用 `.is_visible()` 检查

**Q5: `locator()` 和 `.all()` 有什么区别？**

```python
# locator 返回单个元素（第一个匹配）
button = page.locator('button')
button.click()  # 点击第一个按钮

# all() 返回所有匹配元素的列表
buttons = page.locator('button').all()
for btn in buttons:
    print(btn.inner_text())
```

**Q6: 如何选择第 N 个元素？**

```python
# 第一个
page.locator('button').first

# 最后一个
page.locator('button').last

# 第3个（0-indexed）
page.locator('button').nth(2)
```

### 等待和超时

**Q7: 什么时候用 `networkidle`？**

A: **动态 Web 应用必须使用！** 尤其是：
- React、Vue、Angular 等 SPA
- 有 AJAX 请求的页面
- JavaScript 渲染的内容

```python
# ✅ 正确
page.goto('http://localhost:3000')
page.wait_for_load_state('networkidle')  # 等待 JS 执行完毕
```

**Q8: 如何增加超时时间？**

```python
# 全局超时
page.set_default_timeout(60000)  # 60秒

# 单个操作超时
page.wait_for_selector('.element', timeout=10000)
```

**Q9: 为什么不应该用 `wait_for_timeout()`？**

A: 因为它**不稳定**：
- 网络慢时可能超时失败
- 网络快时浪费时间
- 应该等待特定条件，而不是固定时间

```python
# ❌ 不好 - 固定等待
page.wait_for_timeout(2000)

# ✅ 更好 - 等待特定条件
page.wait_for_selector('.data-loaded')
```

### 表单和交互

**Q10: 如何处理下拉菜单？**

```python
# 按 value 选择
page.select_option('select', value='option1')

# 按显示文本选择
page.select_option('select', label='选项一')

# 按索引选择
page.select_option('select', index=0)
```

**Q11: 复选框怎么操作？**

```python
# 勾选
page.check('#checkbox')

# 取消勾选
page.uncheck('#checkbox')

# 检查是否已勾选
is_checked = page.is_checked('#checkbox')
```

**Q12: 如何上传文件？**

```python
page.set_input_files('#file-input', 'path/to/file.pdf')

# 多个文件
page.set_input_files('#file-input', [
    'file1.pdf',
    'file2.jpg'
])
```

### 截图和调试

**Q13: 截图是空白的怎么办？**

常见原因：
1. 页面还没加载完 → 先等待 `networkidle`
2. 视口太小 → 使用 `full_page=True`
3. 元素不在视口内 → 先滚动到元素

**Q14: 如何只截取可见区域？**

```python
# 全页面
page.screenshot(path='full.png', full_page=True)

# 只截可见区域
page.screenshot(path='viewport.png', full_page=False)
```

### 动态内容

**Q15: SPA 应用测试有什么特殊之处？**

A: 关键区别：
- 路由变化**不会**刷新页面
- 使用 `wait_for_selector()` 而不是 `wait_for_load_state()`
- URL 通常包含 `#` 或使用 History API

```python
# 初次加载
page.goto('http://localhost:3000')
page.wait_for_load_state('networkidle')  # ✅ 只需一次

# 后续导航（SPA 内部）
page.click('a[href="#/about"]')
page.wait_for_selector('.about-content')  # ✅ 等待内容，不是页面加载
```

**Q16: 如何处理无限滚动？**

```python
def scroll_to_bottom(page):
    previous_height = 0
    while True:
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_timeout(1000)  # 等待加载

        new_height = page.evaluate('document.body.scrollHeight')
        if new_height == previous_height:
            break  # 没有更多内容
        previous_height = new_height
```

### 服务器集成

**Q17: `with_server.py` 是做什么的？**

A: 自动化服务器生命周期管理：
1. 启动服务器
2. 等待端口准备就绪
3. 运行你的测试
4. 自动关闭服务器

**Q18: 端口被占用怎么办？**

```bash
# macOS/Linux
lsof -ti:5000 | xargs kill

# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F
```

### 错误处理

**Q19: 如何捕获错误并继续测试？**

```python
try:
    page.click('.optional-button', timeout=2000)
except Exception:
    print("可选按钮不存在，继续...")

# 继续后续测试
page.click('.next-step')
```

**Q20: 测试失败时如何自动截图？**

```python
def test_with_failure_screenshot(page, test_name):
    try:
        # 你的测试代码
        yield
    except Exception as e:
        page.screenshot(path=f'failures/{test_name}.png')
        raise  # 重新抛出异常
```

---

## 快速参考

### 常用命令速查

```bash
# 查看所有命令
make help

# 运行特定示例
make 01        # 或 make static-html
make 05        # 或 make dynamic

# 运行所有示例
make all

# 清理生成文件
make clean
```

### 核心 API 速查

```python
# ===== 浏览器控制 =====
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('url')
    browser.close()

# ===== 导航和等待 =====
page.goto('http://localhost:3000')
page.wait_for_load_state('networkidle')
page.wait_for_selector('.element')
page.wait_for_timeout(1000)

# ===== 元素查找 =====
page.locator('button')              # 第一个匹配
page.locator('button').all()        # 所有匹配
page.locator('button').first        # 第一个
page.locator('button').last         # 最后一个
page.locator('button').nth(2)       # 第3个

# ===== 元素操作 =====
page.click('button')
page.fill('#input', '文本')
page.select_option('select', value='value')
page.check('#checkbox')
page.uncheck('#checkbox')

# ===== 内容提取 =====
element.inner_text()                # 可见文本
element.text_content()              # 所有文本（包括隐藏）
element.get_attribute('href')       # 属性值
element.is_visible()                # 是否可见
page.url()                          # 当前 URL
page.title()                        # 页面标题

# ===== 截图 =====
page.screenshot(path='file.png', full_page=True)
element.screenshot(path='element.png')

# ===== 控制台监控 =====
page.on("console", lambda msg: print(f"[{msg.type}] {msg.text}"))

# ===== 视口设置 =====
page.set_viewport_size({"width": 1920, "height": 1080})
```

### 常用选择器

```python
# 标签
page.locator('button')

# ID
page.locator('#submit-btn')

# 类
page.locator('.btn-primary')

# 属性
page.locator('[data-testid="submit"]')

# 文本
page.locator('text=提交')

# ARIA 角色
page.locator('role=button[name="提交"]')

# CSS 组合
page.locator('div.container > button.primary')

# XPath
page.locator('xpath=//button[@type="submit"]')
```

---

## 进阶资源

### 官方文档

- 📚 [Playwright Python 文档](https://playwright.dev/python/docs/intro)
- 📚 [CSS 选择器参考](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_Selectors)
- 📚 [ARIA 角色参考](https://developer.mozilla.org/zh-CN/docs/Web/Accessibility/ARIA/Roles)

### 推荐学习路径

完成本教程后，建议：

1. **实践项目** - 将所学应用到实际项目
2. **深入 Playwright** - 学习高级特性（网络拦截、模拟设备等）
3. **CI/CD 集成** - 将测试集成到持续集成流程
4. **性能测试** - 学习 Lighthouse 等性能测试工具
5. **视觉回归测试** - 学习截图对比工具

### 相关技术栈

- **pytest** - Python 测试框架，与 Playwright 完美集成
- **GitHub Actions** - CI/CD 中运行自动化测试
- **Docker** - 容器化测试环境
- **Allure** - 生成精美的测试报告

### 社区资源

- [Playwright Discord](https://aka.ms/playwright/discord) - 官方社区
- [Playwright GitHub](https://github.com/microsoft/playwright-python) - 源码和问题追踪
- [Stack Overflow](https://stackoverflow.com/questions/tagged/playwright) - 问题解答

---

## 总结

恭喜你完成了 Web 应用测试教程的学习！🎉

### 你现在掌握了：

✅ **基础技能**
- 浏览器自动化操作
- 元素查找和操作
- 截图和视觉验证

✅ **中级技能**
- 表单自动化
- 动态内容处理（关键！）
- 控制台日志分析

✅ **高级技能**
- SPA 应用测试
- 前后端集成测试
- 完整测试套件编写

### 下一步行动

1. ✍️ **完成所有练习题** - 巩固知识
2. 🚀 **应用到实际项目** - 实践是最好的学习
3. 📖 **阅读官方文档** - 深入了解高级特性
4. 🤝 **分享和交流** - 加入社区，帮助他人

### 需要帮助？

- 💬 查看 [常见问题FAQ](#常见问题faq)
- 📧 提交 Issue 到项目仓库
- 🌐 访问 Playwright 官方文档

---

**祝你测试愉快！Happy Testing! 🎭🧪**

---

<div align="center">

*本教程是 webapp-testing skill 的一部分*

[返回顶部](#web应用测试教程)

</div>
