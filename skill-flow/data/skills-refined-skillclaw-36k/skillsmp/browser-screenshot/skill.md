---
name: browser-screenshot
description: 使用 Playwright 進行瀏覽器截圖管理，支援自動存檔、索引、查詢、比對和測試報告。當使用者要求截取網頁、分析截圖、執行視覺測試或產生測試報告時使用。
---

# 瀏覽器截圖管理

使用 Playwright 進行瀏覽器截圖，自動管理存檔位置、索引和測試報告。

## 檔案結構

```
{專案根目錄}/
├── screenshots/
│   ├── {domain}/
│   │   └── {編號}_{日期}_{描述}.png
│   └── index.json
├── test-reports/
│   ├── {編號}_{日期}_{測試名稱}.html
│   └── {編號}_{日期}_{測試名稱}.md
└── .gitignore
```

## 命名規則

- **編號**：當天自動遞增（001, 002, ...）
- **日期**：YYYY-MM-DD 格式
- **描述/測試名稱**：支援中文
- **完整格式**：`{編號}_{日期}_{描述}.png`
- **範例**：`001_2026-01-09_首頁.png`

## 基本截圖

當使用者要求截取網頁時，執行以下腳本：

```python
import os
import json
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
from datetime import datetime, timezone

# ===== 設定參數 =====
url = "https://example.com"  # 目標 URL
description = "首頁"  # 描述（支援中文）

# ===== 初始化 =====
project_root = os.getcwd()
screenshots_dir = os.path.join(project_root, 'screenshots')
reports_dir = os.path.join(project_root, 'test-reports')

# 建立資料夾
for dir_path in [screenshots_dir, reports_dir]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# 檢查並更新 .gitignore
gitignore_path = os.path.join(project_root, '.gitignore')
entries_to_add = ['screenshots/', 'test-reports/']

if os.path.exists(gitignore_path):
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()
else:
    content = ''

new_entries = [e for e in entries_to_add if e not in content]
if new_entries:
    with open(gitignore_path, 'a', encoding='utf-8') as f:
        f.write('\n# 截圖和測試報告（本地使用，不需版控）\n')
        for entry in new_entries:
            f.write(f'{entry}\n')

# ===== 取得當天編號 =====
today = datetime.now().strftime('%Y-%m-%d')
index_path = os.path.join(screenshots_dir, 'index.json')

if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
else:
    index = {'screenshots': [], 'daily_counter': {}}

# 取得/更新當天計數器
if today not in index.get('daily_counter', {}):
    index['daily_counter'] = index.get('daily_counter', {})
    index['daily_counter'][today] = 0

index['daily_counter'][today] += 1
seq_num = str(index['daily_counter'][today]).zfill(3)

# ===== 準備路徑 =====
parsed = urlparse(url)
domain = parsed.netloc.replace(':', '_')

domain_dir = os.path.join(screenshots_dir, domain)
if not os.path.exists(domain_dir):
    os.makedirs(domain_dir)

filename = f"{seq_num}_{today}_{description}.png"
filepath = os.path.join(domain_dir, filename)

# ===== 截圖 =====
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url, timeout=60000)
    page.wait_for_load_state('domcontentloaded')
    page.screenshot(path=filepath, full_page=True)
    browser.close()

print(f"截圖已儲存: {filepath}")

# ===== 更新索引 =====
relative_path = os.path.relpath(filepath, project_root).replace(chr(92), '/')
entry = {
    'id': f"{seq_num}_{today}_{description}",
    'path': relative_path,
    'url': url,
    'domain': domain,
    'seq_num': seq_num,
    'date': today,
    'description': description,
    'timestamp': datetime.now(timezone.utc).isoformat()
}
index['screenshots'].append(entry)

with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f"索引已更新: {index_path}")
```

## 測試截圖（混合模式）

用於 Playwright 測試，自動在關鍵節點和失敗時截圖：

```python
import os
import json
from playwright.sync_api import sync_playwright, Page
from urllib.parse import urlparse
from datetime import datetime, timezone
import traceback

class TestScreenshotManager:
    def __init__(self, test_name: str, project_root: str = None):
        self.test_name = test_name
        self.project_root = project_root or os.getcwd()
        self.screenshots_dir = os.path.join(self.project_root, 'screenshots')
        self.reports_dir = os.path.join(self.project_root, 'test-reports')
        self.steps = []
        self.console_logs = []
        self.start_time = None
        self.end_time = None
        self.status = 'pending'
        self.error = None

        # 初始化
        self._init_dirs()
        self._init_gitignore()
        self._load_index()

    def _init_dirs(self):
        for dir_path in [self.screenshots_dir, self.reports_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def _init_gitignore(self):
        gitignore_path = os.path.join(self.project_root, '.gitignore')
        entries = ['screenshots/', 'test-reports/']

        content = ''
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                content = f.read()

        new_entries = [e for e in entries if e not in content]
        if new_entries:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write('\n# 截圖和測試報告\n')
                for entry in new_entries:
                    f.write(f'{entry}\n')

    def _load_index(self):
        self.index_path = os.path.join(self.screenshots_dir, 'index.json')
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index = {'screenshots': [], 'daily_counter': {}}

        # 取得當天編號
        self.today = datetime.now().strftime('%Y-%m-%d')
        if self.today not in self.index.get('daily_counter', {}):
            self.index['daily_counter'] = self.index.get('daily_counter', {})
            self.index['daily_counter'][self.today] = 0

        self.index['daily_counter'][self.today] += 1
        self.seq_num = str(self.index['daily_counter'][self.today]).zfill(3)

    def _save_index(self):
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

    def capture(self, page: Page, step_name: str, is_failure: bool = False):
        """截圖並記錄步驟"""
        url = page.url
        parsed = urlparse(url)
        domain = parsed.netloc.replace(':', '_') or 'local'

        domain_dir = os.path.join(self.screenshots_dir, domain)
        if not os.path.exists(domain_dir):
            os.makedirs(domain_dir)

        step_num = len(self.steps) + 1
        filename = f"{self.seq_num}_{self.today}_{self.test_name}_{step_num:02d}_{step_name}.png"
        filepath = os.path.join(domain_dir, filename)

        page.screenshot(path=filepath, full_page=True)

        relative_path = os.path.relpath(filepath, self.project_root).replace(chr(92), '/')

        step_entry = {
            'step_num': step_num,
            'name': step_name,
            'screenshot': relative_path,
            'url': url,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'is_failure': is_failure
        }
        self.steps.append(step_entry)

        # 更新索引
        index_entry = {
            'id': f"{self.seq_num}_{self.today}_{self.test_name}_{step_num:02d}_{step_name}",
            'path': relative_path,
            'url': url,
            'domain': domain,
            'seq_num': self.seq_num,
            'date': self.today,
            'description': f"{self.test_name} - {step_name}",
            'test_name': self.test_name,
            'step_num': step_num,
            'is_failure': is_failure,
            'timestamp': step_entry['timestamp']
        }
        self.index['screenshots'].append(index_entry)

        return filepath

    def capture_on_load(self, page: Page):
        """頁面載入完成時截圖"""
        return self.capture(page, '頁面載入')

    def capture_before_submit(self, page: Page):
        """表單提交前截圖"""
        return self.capture(page, '提交前')

    def capture_after_submit(self, page: Page):
        """表單提交後截圖"""
        return self.capture(page, '提交後')

    def capture_on_failure(self, page: Page, error: Exception):
        """測試失敗時截圖"""
        self.error = str(error)
        return self.capture(page, '失敗', is_failure=True)

    def capture_final(self, page: Page):
        """測試結束時截圖"""
        return self.capture(page, '測試結束')

    def add_console_log(self, msg):
        """記錄控制台日誌"""
        self.console_logs.append({
            'type': msg.type,
            'text': msg.text,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })

    def start(self):
        """開始測試"""
        self.start_time = datetime.now(timezone.utc)
        self.status = 'running'

    def finish(self, success: bool = True):
        """結束測試"""
        self.end_time = datetime.now(timezone.utc)
        self.status = 'passed' if success else 'failed'
        self._save_index()

    def generate_report(self):
        """產生 HTML 和 Markdown 報告"""
        report_base = f"{self.seq_num}_{self.today}_{self.test_name}"

        # 計算執行時間
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0

        # HTML 報告
        html_path = os.path.join(self.reports_dir, f"{report_base}.html")
        html_content = self._generate_html_report(duration)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Markdown 報告
        md_path = os.path.join(self.reports_dir, f"{report_base}.md")
        md_content = self._generate_md_report(duration)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        return html_path, md_path

    def _generate_html_report(self, duration):
        status_color = '#4caf50' if self.status == 'passed' else '#f44336'
        status_text = '通過' if self.status == 'passed' else '失敗'

        steps_html = ''
        for step in self.steps:
            step_class = 'failure' if step['is_failure'] else 'success'
            steps_html += f'''
            <div class="step {step_class}">
                <h3>步驟 {step['step_num']}: {step['name']}</h3>
                <p>URL: {step['url']}</p>
                <p>時間: {step['timestamp']}</p>
                <img src="../{step['screenshot']}" alt="{step['name']}" onclick="this.classList.toggle('expanded')">
            </div>
            '''

        console_html = ''
        for log in self.console_logs:
            log_class = 'error' if log['type'] == 'error' else 'log'
            console_html += f'<div class="console-{log_class}">[{log["type"]}] {log["text"]}</div>'

        error_html = ''
        if self.error:
            error_html = f'<div class="error-stack"><h3>錯誤訊息</h3><pre>{self.error}</pre></div>'

        return f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>測試報告 - {self.test_name}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .header {{ background: {status_color}; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .header .meta {{ opacity: 0.9; }}
        .step {{ background: white; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .step.failure {{ border-left: 4px solid #f44336; }}
        .step.success {{ border-left: 4px solid #4caf50; }}
        .step h3 {{ margin-top: 0; }}
        .step img {{ max-width: 100%; cursor: pointer; border: 1px solid #ddd; border-radius: 4px; transition: all 0.3s; }}
        .step img.expanded {{ max-width: none; width: 100%; }}
        .console {{ background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px; margin-top: 20px; font-family: monospace; max-height: 300px; overflow-y: auto; }}
        .console-error {{ color: #f44336; }}
        .console-log {{ color: #d4d4d4; }}
        .error-stack {{ background: #ffebee; border: 1px solid #f44336; padding: 15px; border-radius: 8px; margin-top: 20px; }}
        .error-stack pre {{ white-space: pre-wrap; word-wrap: break-word; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .summary-card {{ background: white; padding: 15px; border-radius: 8px; text-align: center; }}
        .summary-card .value {{ font-size: 24px; font-weight: bold; color: #333; }}
        .summary-card .label {{ color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{self.test_name}</h1>
        <div class="meta">
            <span>狀態: {status_text}</span> |
            <span>日期: {self.today}</span> |
            <span>編號: {self.seq_num}</span>
        </div>
    </div>

    <div class="summary">
        <div class="summary-card">
            <div class="value">{len(self.steps)}</div>
            <div class="label">總步驟數</div>
        </div>
        <div class="summary-card">
            <div class="value">{duration:.2f}s</div>
            <div class="label">執行時間</div>
        </div>
        <div class="summary-card">
            <div class="value">{len([s for s in self.steps if s['is_failure']])}</div>
            <div class="label">失敗步驟</div>
        </div>
        <div class="summary-card">
            <div class="value">{len(self.console_logs)}</div>
            <div class="label">控制台日誌</div>
        </div>
    </div>

    <h2>測試步驟</h2>
    {steps_html}

    {error_html}

    <h2>控制台日誌</h2>
    <div class="console">
        {console_html if console_html else '<div>無日誌</div>'}
    </div>
</body>
</html>'''

    def _generate_md_report(self, duration):
        status_text = '✅ 通過' if self.status == 'passed' else '❌ 失敗'

        steps_md = ''
        for step in self.steps:
            status_icon = '❌' if step['is_failure'] else '✅'
            steps_md += f'''
### {status_icon} 步驟 {step['step_num']}: {step['name']}

- **URL**: {step['url']}
- **時間**: {step['timestamp']}
- **截圖**: ![{step['name']}](../{step['screenshot']})

'''

        console_md = ''
        for log in self.console_logs:
            console_md += f'- [{log["type"]}] {log["text"]}\n'

        error_md = ''
        if self.error:
            error_md = f'''
## 錯誤訊息

```
{self.error}
```
'''

        return f'''# 測試報告 - {self.test_name}

| 項目 | 值 |
|------|-----|
| 狀態 | {status_text} |
| 日期 | {self.today} |
| 編號 | {self.seq_num} |
| 執行時間 | {duration:.2f}s |
| 總步驟數 | {len(self.steps)} |
| 失敗步驟 | {len([s for s in self.steps if s['is_failure']])} |

## 測試步驟

{steps_md}

{error_md}

## 控制台日誌

{console_md if console_md else '無日誌'}
'''


# ===== 使用範例 =====
def run_test_example():
    """測試範例"""
    manager = TestScreenshotManager('登入測試')
    manager.start()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            # 監聽控制台
            page.on('console', manager.add_console_log)

            # 測試流程
            page.goto('https://example.com', timeout=60000)
            page.wait_for_load_state('domcontentloaded')
            manager.capture_on_load(page)

            # ... 執行測試動作 ...

            manager.capture_final(page)
            browser.close()

        manager.finish(success=True)
    except Exception as e:
        manager.capture_on_failure(page, e)
        manager.finish(success=False)
        raise
    finally:
        html_path, md_path = manager.generate_report()
        print(f"HTML 報告: {html_path}")
        print(f"Markdown 報告: {md_path}")
```

## 查詢截圖

```python
import json

with open('screenshots/index.json', 'r', encoding='utf-8') as f:
    index = json.load(f)

# 依日期查詢
results = [s for s in index['screenshots'] if s['date'] == '2026-01-09']

# 依測試名稱查詢
results = [s for s in index['screenshots'] if s.get('test_name') == '登入測試']

# 依網站查詢
results = [s for s in index['screenshots'] if s['domain'] == 'www.google.com']

# 只看失敗的截圖
results = [s for s in index['screenshots'] if s.get('is_failure')]
```

## 比對截圖

```python
from PIL import Image, ImageChops

img1 = Image.open("screenshots/domain/001_2026-01-09_before.png")
img2 = Image.open("screenshots/domain/002_2026-01-09_after.png")

diff = ImageChops.difference(img1, img2)

if diff.getbbox():
    diff.save("screenshots/domain/diff.png")
    print("發現差異")
else:
    print("完全相同")
```

## 注意事項

1. **編號系統**：每天從 001 開始自動遞增
2. **自動截圖時機**：頁面載入、表單提交前後、測試結束、失敗時
3. **報告格式**：HTML（互動式）+ Markdown（版控友好）
4. **截圖引用**：報告引用 `screenshots/` 的圖，不重複儲存
5. **Git 忽略**：自動將 `screenshots/` 和 `test-reports/` 加入 `.gitignore`
