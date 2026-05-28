---
name: browser-testing
description: 使用 Playwright 測試網路應用程式的工具包。支援 UI 測試、截圖、登入驗證、伺服器管理和瀏覽器日誌擷取。整合 browser-screenshot skill 進行截圖管理和測試報告。
---

# 瀏覽器測試

使用 Playwright 與本地網路應用程式互動和測試。

## 檔案規則（必須遵守）

生成測試檔案時，**必須**遵守以下規則：

| 類型 | 位置 | 命名規則 | 範例 |
|------|------|----------|------|
| 子專案目錄 | `browser-tests/YYYY-MM-DD-NNN-<name>/` | 日期+編號+名稱 | `browser-tests/2026-01-09-001-login-test/` |
| 測試腳本 | `<子專案>/test_*.py` | test_ 前綴 | `<子專案>/test_login.py` |
| 截圖 | `<子專案>/screenshots/NN_*.png` | 編號+描述 | `<子專案>/screenshots/01_login.png` |
| 報告 | `<子專案>/result.html` | 固定名稱 | `<子專案>/result.html` |

**命名規則說明**：
- `YYYY-MM-DD`：建立日期
- `NNN`：三位數編號，同一天內遞增（001, 002, 003...）
- `<name>`：kebab-case 描述性名稱

**清理命令**：
```bash
# 清理所有測試子專案
rm -rf browser-tests/20*/

# 清理特定日期
rm -rf browser-tests/2026-01-09-*/

# 清理特定測試
rm -rf browser-tests/2026-01-09-001-login-test/
```

**gitignore 規則**（專案應包含）：
```gitignore
# 瀏覽器測試
browser-tests/20*/
```

---

## 快速命令

| 命令 | 說明 | 範例 |
|------|------|------|
| `console-check` | 檢查 console 錯誤 | `python commands/console-check.py <url> [--login] [--wait N]` |
| `screenshot` | 快速截圖 | `python commands/screenshot.py <url> [output.png] [--login]` |
| `discover` | 探索頁面元素 | `python commands/discover.py <url> [--login]` |
| `run-test` | 執行測試腳本 | `python commands/run-test.py <script.py> [--server "cmd" --port N]` |

### console-check - 檢查瀏覽器 Console 錯誤

**當使用者說「檢查瀏覽器 console」或遇到 UI 問題（如側邊欄空白、元件未載入）時，自動使用此命令。**

```bash
# 設定測試 port（根據實際情況調整）
# PORT=3000  # 或 3300, 9002 等

# 檢查首頁（需要登入）
python commands/console-check.py http://localhost:$PORT --login

# 檢查特定頁面，等待 10 秒讓頁面穩定
python commands/console-check.py http://localhost:$PORT/inbox --login --wait 10

# 檢查不需登入的頁面
python commands/console-check.py http://localhost:$PORT/widget-demo

# 搭配 run-test 使用（自動啟動伺服器，port 從 .env.test 讀取）
python commands/run-test.py "python commands/console-check.py http://localhost:$PORT --login" --auto-server
```

輸出報告包含：
- **頁面狀態**：導航連結數、是否顯示「載入中」
- **Session 狀態**：使用者資訊、角色
- **Console 錯誤**：JavaScript 錯誤訊息
- **HTTP 錯誤**：401、404、500 等請求錯誤
- **截圖**：自動儲存到 `screenshots/` 目錄

### screenshot - 快速截圖

```bash
# PORT 變數根據實際測試環境設定

# 截取公開頁面
python commands/screenshot.py http://localhost:$PORT homepage.png

# 截取需要登入的頁面
python commands/screenshot.py http://localhost:$PORT/dashboard dashboard.png --login

# 使用預設檔名（自動產生 screenshot_HHMMSS.png）
python commands/screenshot.py http://localhost:$PORT
```

### discover - 探索頁面元素

```bash
# PORT 變數根據實際測試環境設定

# 探索公開頁面
python commands/discover.py http://localhost:$PORT

# 探索需要登入的頁面
python commands/discover.py http://localhost:$PORT/dashboard --login
```

輸出：按鈕、連結、輸入框清單，並自動截圖到 `screenshots/discover.png`。

### run-test - 執行測試腳本

```bash
# 伺服器已運行
python commands/run-test.py browser-tests/2026-01-09-001-login-test/test_login.py

# 自動啟動伺服器（從 .env.test 讀取 TEST_SERVER_CMD 和 TEST_SERVER_PORT）
python commands/run-test.py browser-tests/test_login.py --auto-server

# 自動啟動伺服器，指定超時時間（預設 60 秒）
python commands/run-test.py browser-tests/test_login.py --auto-server --timeout 90

# 手動指定伺服器（port 根據需求調整）
python commands/run-test.py browser-tests/test_login.py --server "npm run dev" --port $PORT
```

---

## TestManager API

提供截圖管理和測試報告生成的 API。

### 基本使用

```python
from browser_testing import TestManager
import os

# 從環境變數或 .env.test 取得 port
BASE_URL = os.getenv('TEST_BASE_URL', 'http://localhost:3000')

with TestManager() as tm:
    page = tm.page  # Playwright page 物件

    page.goto(f'{BASE_URL}/login')
    tm.capture('登入頁面')  # 截圖：screenshots/01_登入頁面.png

    page.fill('input[type="email"]', 'test@example.com')
    page.fill('input[type="password"]', 'password')
    tm.capture('填寫完成')

    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle')
    tm.capture('登入成功')

# with 區塊結束時自動：
# 1. 關閉瀏覽器
# 2. 產出報告到 test-reports/
```

### API 參考

| 方法/屬性 | 說明 |
|----------|------|
| `TestManager(headless=True)` | 建立測試管理器，headless=False 可看到瀏覽器 |
| `tm.page` | Playwright page 物件 |
| `tm.capture(名稱)` | 截圖並編號（01_名稱.png） |
| `tm.fail(訊息)` | 標記測試失敗 |

### 自動行為

- 自動偵測子專案目錄（從腳本位置推斷）
- 自動建立 `screenshots/` 和 `test-reports/` 目錄
- 自動擷取瀏覽器控制台日誌
- 測試結束自動產出 HTML 和 Markdown 報告
- 報告編號自動遞增（01, 02, 03...）

### 產出結構

```
browser-tests/2026-01-09-001-login-test/
├── test_login.py
├── screenshots/
│   ├── 01_登入頁面.png
│   ├── 02_填寫完成.png
│   └── 03_登入成功.png
└── test-reports/
    ├── 01_result.html      # 第一次執行
    ├── 01_result.md
    ├── 02_result.html      # 第二次執行
    └── 02_result.md
```

---

## 測試帳號管理

### 專案設定檔 `.env.test`

測試帳號設定存放在專案根目錄的 `.env.test`：

```bash
# 瀏覽器測試用帳密 - 自動產生
# 請勿提交到 git

TEST_USER_EMAIL=test@browser.local
TEST_USER_PASSWORD=Test@1234
TEST_BASE_URL=http://localhost:3000

# 伺服器設定（供 --auto-server 使用）
TEST_SERVER_CMD=npx next dev --turbopack -p 3000
TEST_SERVER_PORT=3000
```

**設定檔範本**：`.env.test.example`（可提交到 git）

---

## 決策樹：選擇你的方法

```
使用者任務 → 需要登入測試嗎？
    ├─ 是 → .env.test 存在嗎？
    │         ├─ 否 → 手動建立 .env.test（參考 .env.test.example）
    │         └─ 是 → 繼續測試
    │
    └─ 否 → 是靜態 HTML 嗎？
        ├─ 是 → 直接閱讀 HTML 檔案以識別選擇器
        └─ 否 → python commands/discover.py <url> 探索元素
```

---

## 登入測試範本（使用 TestManager）

```python
# 檔案：browser-tests/2026-01-09-001-login-test/test_login.py
from browser_testing import TestManager
from dotenv import load_dotenv
import os

# 讀取專案測試帳號設定
if os.path.exists('.env.test'):
    load_dotenv('.env.test')
else:
    raise FileNotFoundError('未找到 .env.test，請參考 .env.test.example 建立')

email = os.getenv('TEST_USER_EMAIL')
password = os.getenv('TEST_USER_PASSWORD')
base_url = os.getenv('TEST_BASE_URL', 'http://localhost:3000')

with TestManager() as tm:
    page = tm.page

    # 登入
    page.goto(f'{base_url}/login', wait_until='domcontentloaded')
    page.wait_for_load_state('networkidle')
    tm.capture('登入頁面')

    page.fill('input[type="email"]', email)
    page.fill('input[type="password"]', password)
    tm.capture('填寫完成')

    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle')

    # 驗證
    if '/dashboard' in page.url or '/home' in page.url:
        tm.capture('登入成功')
    else:
        tm.fail('登入失敗：未跳轉到預期頁面')
        tm.capture('登入失敗')
```

---

## 偵錯技巧

### 以非無頭模式執行（可見瀏覽器）
```python
browser = p.chromium.launch(headless=False)
```

### 擷取主控台日誌
```python
page.on('console', lambda msg: print(f'Console: {msg.text}'))
```

### 等待網路請求完成
```python
page.wait_for_load_state('networkidle')
```

---

## 常見問題與解法

### 登入後側邊欄空白

**症狀**：登入成功但側邊欄沒有導航項目

**診斷**：使用 `console-check` 檢查
```bash
# $PORT 為實際測試 port
python commands/console-check.py http://localhost:$PORT --login --wait 10
```

**常見原因**：
1. **Session API 401 錯誤** - 登入後 cookie 尚未設好，前端 hook 讀取 session 失敗
2. **權限 hook 無重試機制** - 第一次失敗後沒有重試

**解法**：在前端 hook 加入重試機制
```typescript
// usePermission.tsx
useEffect(() => {
  let retryCount = 0;
  const maxRetries = 3;
  const retryDelay = 500;

  const loadUser = async (): Promise<boolean> => {
    const response = await fetch('/api/auth/session');
    const data = await response.json();
    if (data.isValid && data.user) {
      setCurrentUser(data.user);
      return true;
    }
    return false;
  };

  const attemptLoad = async () => {
    const success = await loadUser();
    if (!success && retryCount < maxRetries) {
      retryCount++;
      setTimeout(attemptLoad, retryDelay * retryCount);
    }
  };

  attemptLoad();
}, []);
```

### 登入按鈕卡在「登入中...」

**症狀**：點擊登入後按鈕一直顯示 loading

**原因**：伺服器剛啟動，API 回應慢或 Firestore 連線未建立

**解法**：使用 `wait_for_url` 而非固定等待時間
```python
# 等待 URL 變化，最多 30 秒
try:
    page.wait_for_url(lambda url: '/login' not in url, timeout=30000)
except:
    print('登入超時')
```

### networkidle 超時

**症狀**：`page.wait_for_load_state('networkidle')` 超時

**原因**：頁面有 WebSocket、輪詢或持續的網路請求

**解法**：改用固定等待或等待特定元素
```python
# 方案 1：固定等待
page.wait_for_timeout(5000)

# 方案 2：等待特定元素出現
page.wait_for_selector('nav a', timeout=10000)
```

### Next.js 首次編譯時間長

**症狀**：首次載入頁面超時（60 秒），但伺服器已啟動

**原因**：Next.js（尤其是 Turbopack）首次編譯頁面可能需要 15-30 秒

**解法**：
```python
# 設定較長的預設超時（90 秒）
page.set_default_timeout(90000)

# 或針對特定導航設定超時
page.goto(f'{base_url}/ai-studio', wait_until='domcontentloaded', timeout=120000)

# 登入後等待 URL 變化，給予足夠時間
page.wait_for_url(lambda url: '/login' not in url, timeout=90000)
```

**建議**：測試前先手動訪問一次目標頁面「暖機」，或在測試腳本中加入重試機制。

---

## 遇到問題時的處理流程

**當快速命令失敗時，按此順序嘗試解決：**

### 1. 診斷問題類型

| 錯誤類型 | 症狀 | 解決方案 |
|----------|------|----------|
| Port 衝突 | `EADDRINUSE` | 使用 `--auto-server` 或換 port |
| 編碼錯誤 | `UnicodeEncodeError` | 使用 TestManager API 撰寫 Python 腳本 |
| 伺服器未啟動 | `Connection refused` | 使用 `--auto-server` 自動管理 |
| 登入失敗 | 401/403 | 確認 `.env.test` 設定正確 |
| 超時 | `TimeoutError` | 增加 `--timeout` 或用 `--wait` |

### 2. 嘗試 skill 內的替代方案

**不要自行撰寫替代腳本**，優先使用 skill 提供的方法：

```bash
# Port 衝突 → 使用 --auto-server（從 .env.test 讀取設定）
python commands/run-test.py <script.py> --auto-server

# 編碼問題 → 改用 TestManager API 撰寫測試
# 見下方 TestManager API 範例

# 伺服器管理 → 使用 run-test.py（port 從 .env.test 讀取）
python commands/run-test.py "python commands/console-check.py http://localhost:$PORT" --auto-server
```

**TestManager API 範例（解決編碼問題）**：
```python
from browser_testing import TestManager
import os

BASE_URL = os.getenv('TEST_BASE_URL', 'http://localhost:3000')

with TestManager() as tm:
    page = tm.page
    page.goto(f'{BASE_URL}/widget-demo')
    tm.capture('widget_demo')  # 使用 ASCII 名稱避免編碼問題

    # 檢查元素
    button = page.locator('.minimized-button')
    if button.is_visible():
        tm.capture('button_visible')
    else:
        tm.fail('Button not found')
```

### 3. 記錄和回報

如果所有 skill 方法都失敗：

1. **記錄錯誤訊息**：完整錯誤輸出
2. **記錄嘗試過的方法**：列出已嘗試的 skill 命令
3. **詢問使用者**：說明問題並請求指引

**禁止行為**：
- ❌ 不經嘗試就跳過 skill 命令
- ❌ 自行撰寫替代腳本繞過 skill
- ❌ 假設 skill 方法不適用而不驗證

---

## iframe 內嵌 Widget 測試

測試嵌入在 iframe 中的 Widget（如聊天機器人）需要特殊處理。

### 基本結構

```python
from playwright.sync_api import sync_playwright
import os

# Port 設定 - 使用 get_test_port() 或環境變數
TEST_PORT = int(os.environ.get('TEST_PORT', 3300))  # 從環境變數讀取，預設 3300

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    # 收集 console 日誌
    console_logs = []
    page.on('console', lambda msg: console_logs.append(f'[{msg.type}] {msg.text}'))

    page.goto(f'http://localhost:{TEST_PORT}/widget-demo')
    page.wait_for_timeout(3000)

    # 取得 iframe 內的元素
    iframe = page.frame_locator('#dafon-chat-frame')

    # 取得父頁面的元素
    frame_container = page.locator('#dafon-chat-frame-container')
    minimized_btn = page.locator('#dafon-line-minimized')

    browser.close()
```

### 常用選擇器

| 目標 | 選擇器 | 說明 |
|------|--------|------|
| 關閉按鈕 | `button:has(svg.lucide-minus)` | Lucide 圖標按鈕 |
| 輸入框 | `input[placeholder*="輸入訊息"]` | 用 placeholder 定位 |
| 發送按鈕 | `button[type="submit"]` | 表單提交按鈕 |
| CSS class 檢查 | `el.classList.contains("line-chat")` | JavaScript evaluate |
| Tab 標籤 | `[role="tab"]:has-text("標籤名")` | shadcn/ui Tabs 元件 |
| Switch 開關 | `button[role="switch"]` | shadcn/ui Switch 元件 |
| Radio 選項 | `[role="radio"]:has-text("選項")` | shadcn/ui RadioGroup |
| Slider 滑桿 | `input[type="range"]` 或 `[role="slider"]` | 滑桿元件 |

**Tab 選擇器注意事項**：
- 不要使用 `button[value="xxx"]`，shadcn/ui Tabs 不一定有 value 屬性
- 優先使用 `[role="tab"]:has-text("顯示文字")` 或 `[role="tab"]` + nth() 索引

### iframe 內操作範例

```python
# 點擊 iframe 內的按鈕
iframe = page.frame_locator('#dafon-chat-frame')
close_btn = iframe.locator('button:has(svg.lucide-minus)').first
close_btn.click(timeout=5000)

# 填寫 iframe 內的輸入框
input_field = iframe.locator('input[placeholder*="輸入訊息"]').first
input_field.click(timeout=5000)
input_field.fill('你好')
input_field.press('Enter')

# 檢查父頁面元素的 CSS class
frame_container = page.locator('#dafon-chat-frame-container')
has_class = frame_container.evaluate('el => el.classList.contains("line-chat")')
```

### 等待非同步回覆（如 AI 回覆）

```python
# 方法 1：輪詢檢查按鈕文字變化
print('Waiting for AI reply...')
for i in range(15):  # 每 2 秒檢查，最多 30 秒
    page.wait_for_timeout(2000)
    btn_text = minimized_btn.locator('span').text_content()
    print(f'  Button text: "{btn_text}"')
    if '新訊息' in btn_text:
        print('  PASS: Button updated!')
        break
else:
    print('  INFO: No reply within 30 seconds')

# 方法 2：監聽 postMessage 事件（進階）
# 透過 console.log 追蹤 [Dafon Widget] 日誌
```

### 清除 localStorage

```python
def clear_local_storage(page):
    """清除特定前綴的 localStorage"""
    page.evaluate('''() => {
        const keys = Object.keys(localStorage).filter(k => k.startsWith('dafon-'));
        keys.forEach(k => localStorage.removeItem(k));
    }''')
    print('[clear] localStorage cleared')

# 使用
clear_local_storage(page)
page.reload()
page.wait_for_timeout(3000)
```

### 驗證 localStorage 狀態

```python
# 檢查特定 key
last_read_id = page.evaluate('() => localStorage.getItem("dafon-last-read-msg-id")')
if last_read_id:
    print(f'  PASS: localStorage has value: {last_read_id}')
else:
    print('  INFO: localStorage is empty')
```

### 頁面滾動與元素定位

當目標元素在可視區域外時，需要滾動才能看到或操作：

```python
# 方法 1：滾動到特定元素
element = page.locator('text=Widget 自動開啟').first
element.scroll_into_view_if_needed()
page.wait_for_timeout(500)  # 等待滾動動畫完成

# 方法 2：滾動到頁面底部
page.evaluate('window.scrollTo(0, document.body.scrollHeight)')

# 方法 3：分段滾動截圖（長頁面）
for scroll_pos in [0, 500, 1000, 1500]:
    page.evaluate(f'window.scrollTo(0, {scroll_pos})')
    page.wait_for_timeout(300)
    page.screenshot(path=f'screenshots/scroll_{scroll_pos}.png')

# 方法 4：滾動到頂部
page.evaluate('window.scrollTo(0, 0)')
```

**注意事項**：
- 某些元素即使 `is_visible()` 返回 True，也可能被其他元素遮擋
- 使用 `scroll_into_view_if_needed()` 前，元素必須存在於 DOM 中
- 滾動後建議等待 300-500ms 讓頁面穩定

### 完整 Widget 測試範例

```python
import os
from playwright.sync_api import sync_playwright

# 測試未讀訊息計數功能
# Port 設定 - 使用環境變數或 get_test_port()
TEST_PORT = int(os.environ.get('TEST_PORT', 3300))

def test_unread_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        console_logs = []
        page.on('console', lambda msg: console_logs.append(msg.text))

        page.goto(f'http://localhost:{TEST_PORT}/widget-demo')
        page.wait_for_timeout(3000)

        iframe = page.frame_locator('#dafon-chat-frame')
        minimized_btn = page.locator('#dafon-line-minimized')

        # 1. 開啟聊天
        iframe.locator('body').click()
        page.wait_for_timeout(2000)

        # 2. 發送訊息
        input_field = iframe.locator('input[placeholder*="輸入訊息"]').first
        input_field.fill('你好')
        input_field.press('Enter')

        # 3. 關閉 Widget
        close_btn = iframe.locator('button:has(svg.lucide-minus)').first
        close_btn.click()
        page.wait_for_timeout(1000)

        # 4. 等待 AI 回覆，檢查按鈕更新
        for i in range(15):
            page.wait_for_timeout(2000)
            btn_text = minimized_btn.locator('span').text_content()
            if '新訊息' in btn_text:
                print('PASS: Unread count updated!')
                break

        # 5. 檢查 console 日誌
        for log in console_logs:
            if 'Unread count' in log:
                print(f'  {log}')

        browser.close()
```

---

## 伺服器 Port 管理

### 檢查 Port 佔用

```bash
# Windows（將 PORT 替換為實際 port 號碼）
netstat -ano | findstr ":PORT" | findstr "LISTENING"

# 查看程序名稱
powershell "Get-Process -Id <PID> | Select-Object ProcessName, Id"
```

### 處理 Port 衝突

```python
import os

# 方法 1：使用環境變數指定 port
TEST_PORT = int(os.environ.get('TEST_PORT', 3300))
BASE_URL = f'http://localhost:{TEST_PORT}'

# 方法 2：使用 get_test_port() 自動尋找可用 port（見下方最佳實踐）

# 方法 3：終止佔用程序（Windows）
import subprocess
subprocess.run(['powershell', 'Stop-Process -Id <PID> -Force'])
```

### 僵死 Node 進程

**症狀**：Port 顯示 LISTENING 但 curl/瀏覽器連線超時

**原因**：Node 進程僵死，仍佔用 port 但無法處理請求

**診斷**：
```bash
# 檢查 port 是否被佔用
netstat -ano | findstr ":3300" | findstr "LISTENING"

# 測試伺服器是否有回應（應該在 5 秒內返回）
curl -s -o /dev/null -w "%{http_code}" http://localhost:3300/ --connect-timeout 5 --max-time 10
```

**解法**：
```bash
# 找出 PID 後終止進程
powershell "Stop-Process -Id <PID> -Force"

# 或一次終止所有 Node 進程（謹慎使用）
powershell "Get-Process -Name node -ErrorAction SilentlyContinue | Stop-Process -Force"

# 然後重新啟動伺服器
npx next dev --turbopack -p 3300
```

### Port 設定最佳實踐

測試腳本應使用變數管理 port，支援多種設定方式：

```python
import os
import socket

# 優先順序：環境變數 > 參數 > 自動偵測
def get_test_port(default=3300):
    """取得測試用 port"""
    # 1. 從環境變數讀取
    env_port = os.environ.get('TEST_PORT')
    if env_port:
        return int(env_port)

    # 2. 檢查預設 port 是否可用
    if is_port_available(default):
        return default

    # 3. 自動尋找可用 port
    return find_free_port(start=default)

def is_port_available(port):
    """檢查 port 是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def find_free_port(start=3300, end=3400):
    """在範圍內尋找可用 port"""
    for port in range(start, end):
        if is_port_available(port):
            return port
    raise RuntimeError('No free port found in range')

# 使用方式
TEST_PORT = get_test_port()
BASE_URL = f'http://localhost:{TEST_PORT}'
print(f'Using port: {TEST_PORT}')
```

**使用範例**：
```bash
# 使用環境變數指定 port
TEST_PORT=3305 python test_widget.py

# 或讓腳本自動選擇可用 port
python test_widget.py
```

---

## 常見陷阱

- **不要**在動態應用程式上等待 `networkidle` 之前檢查 DOM
- **要**在檢查前等待 `page.wait_for_load_state('networkidle')`
- **不要**使用固定短時間等待（如 3 秒），伺服器冷啟動可能需要更長時間
- **要**使用 `wait_for_url` 或 `wait_for_selector` 等待具體條件

## 最佳實踐

- 每個測試案例建立獨立子專案目錄
- 截圖使用有序編號：`01_step.png`, `02_step.png`
- 對於同步腳本使用 `sync_playwright()`
- 完成後始終關閉瀏覽器
- 使用描述性選擇器：`text=`、`role=`、CSS 選擇器或 ID
- **永遠不要將 .env.test 提交到 git**

## 目錄結構

**專案內**：
```
project/
├── .env.test                              # 測試帳密（不提交）
├── .env.test.example                      # 範本（可提交）
└── browser-tests/
    ├── 2026-01-09-001-crm-autofill/
    │   ├── test_crm_autofill.py           # 測試腳本
    │   ├── result.html                     # 測試報告
    │   └── screenshots/                    # 截圖
    │       ├── 01_login.png
    │       └── 02_result.png
    └── 2026-01-09-002-phone-extraction/
        ├── test_phone_extraction.py
        ├── result.html
        └── screenshots/
```

**Skill 內**：
```
~/.claude/skills/browser-testing/
├── SKILL.md
├── commands/
│   ├── screenshot.py
│   ├── discover.py
│   └── run-test.py
├── scripts/
│   └── with_server.py
└── examples/
    └── ...
```
