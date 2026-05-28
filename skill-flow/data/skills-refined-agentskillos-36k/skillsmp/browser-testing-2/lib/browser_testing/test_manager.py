#!/usr/bin/env python3
"""
TestManager - 瀏覽器測試管理器

提供截圖、控制台日誌擷取、測試報告生成功能。

Usage:
    from browser_testing import TestManager

    with TestManager() as tm:
        page = tm.page
        page.goto('http://localhost:3000')
        tm.capture('首頁')
"""

import os
import re
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright, Page


class TestManager:
    """瀏覽器測試管理器，支援截圖和報告生成"""

    def __init__(self, headless: bool = True, viewport_width: int = 1920, viewport_height: int = 1080):
        """
        初始化測試管理器

        Args:
            headless: 是否使用無頭模式（預設 True）
            viewport_width: 視窗寬度（預設 1920）
            viewport_height: 視窗高度（預設 1080）
        """
        self.headless = headless
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        # 狀態
        self._playwright = None
        self._browser = None
        self._page = None
        self._test_dir = None
        self._screenshots_dir = None
        self._reports_dir = None

        # 測試資料
        self._steps = []
        self._console_logs = []
        self._start_time = None
        self._end_time = None
        self._status = 'pending'
        self._error_message = None
        self._step_counter = 0

    @property
    def page(self) -> Page:
        """取得 Playwright page 物件"""
        return self._page

    def __enter__(self):
        """進入 context manager"""
        self._start_time = datetime.now(timezone.utc)
        self._status = 'running'

        # 偵測測試目錄（從呼叫者的檔案位置推斷）
        import inspect
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_file = caller_frame.f_globals.get('__file__', os.getcwd())
        self._test_dir = os.path.dirname(os.path.abspath(caller_file))

        # 建立目錄
        self._screenshots_dir = os.path.join(self._test_dir, 'screenshots')
        self._reports_dir = os.path.join(self._test_dir, 'test-reports')
        os.makedirs(self._screenshots_dir, exist_ok=True)
        os.makedirs(self._reports_dir, exist_ok=True)

        # 啟動 Playwright
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._page = self._browser.new_page(
            viewport={'width': self.viewport_width, 'height': self.viewport_height}
        )
        self._page.set_default_timeout(60000)

        # 監聽控制台日誌
        self._page.on('console', self._on_console)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """離開 context manager"""
        self._end_time = datetime.now(timezone.utc)

        # 處理例外
        if exc_type is not None:
            self._status = 'failed'
            self._error_message = str(exc_val)
            # 嘗試截圖
            try:
                self.capture('錯誤', is_failure=True)
            except:
                pass
        elif self._status == 'running':
            self._status = 'passed'

        # 關閉瀏覽器
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

        # 產出報告
        self._generate_reports()

        # 不抑制例外
        return False

    def _on_console(self, msg):
        """處理控制台日誌"""
        self._console_logs.append({
            'type': msg.type,
            'text': msg.text,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })

    def capture(self, name: str, is_failure: bool = False) -> str:
        """
        截圖並記錄步驟

        Args:
            name: 步驟名稱
            is_failure: 是否為失敗截圖

        Returns:
            截圖檔案路徑
        """
        self._step_counter += 1
        filename = f"{self._step_counter:02d}_{name}.png"
        filepath = os.path.join(self._screenshots_dir, filename)

        self._page.screenshot(path=filepath, full_page=True)

        step = {
            'num': self._step_counter,
            'name': name,
            'filename': filename,
            'url': self._page.url,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'is_failure': is_failure
        }
        self._steps.append(step)

        print(f"[CAPTURE] screenshots/{filename}")
        return filepath

    def fail(self, message: str):
        """
        標記測試失敗

        Args:
            message: 失敗訊息
        """
        self._status = 'failed'
        self._error_message = message
        print(f"[FAIL] {message}")

    def _get_next_report_number(self) -> int:
        """取得下一個報告編號"""
        existing = []
        if os.path.exists(self._reports_dir):
            for f in os.listdir(self._reports_dir):
                match = re.match(r'^(\d+)_result\.(html|md)$', f)
                if match:
                    existing.append(int(match.group(1)))
        return max(existing, default=0) + 1

    def _generate_reports(self):
        """產出 HTML 和 Markdown 報告"""
        report_num = self._get_next_report_number()

        # 計算執行時間
        duration = 0
        if self._start_time and self._end_time:
            duration = (self._end_time - self._start_time).total_seconds()

        # 取得測試名稱（從目錄名稱）
        test_name = os.path.basename(self._test_dir)

        # 產出 HTML
        html_path = os.path.join(self._reports_dir, f"{report_num:02d}_result.html")
        html_content = self._generate_html(test_name, duration, report_num)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[REPORT] test-reports/{report_num:02d}_result.html")

        # 產出 Markdown
        md_path = os.path.join(self._reports_dir, f"{report_num:02d}_result.md")
        md_content = self._generate_markdown(test_name, duration, report_num)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"[REPORT] test-reports/{report_num:02d}_result.md")

        # 最終狀態（console 使用 ASCII 避免 Windows 編碼問題）
        status_text = 'passed' if self._status == 'passed' else 'failed'
        print("[" + status_text.upper() + "] Test " + status_text)

    def _generate_html(self, test_name: str, duration: float, report_num: int) -> str:
        """產出 HTML 報告"""
        status_color = '#4caf50' if self._status == 'passed' else '#f44336'
        status_text = '通過' if self._status == 'passed' else '失敗'
        status_icon = '✅' if self._status == 'passed' else '❌'

        # 步驟 HTML
        steps_html = ''
        for step in self._steps:
            step_icon = '❌' if step['is_failure'] else '✅'
            step_class = 'failure' if step['is_failure'] else 'success'
            steps_html += f'''
            <div class="step {step_class}">
                <h3>{step_icon} 步驟 {step['num']}：{step['name']}</h3>
                <p><strong>URL:</strong> {step['url']}</p>
                <p><strong>時間:</strong> {step['timestamp']}</p>
                <img src="../screenshots/{step['filename']}" alt="{step['name']}" onclick="this.classList.toggle('expanded')">
            </div>
            '''

        # 控制台日誌 HTML
        console_html = ''
        for log in self._console_logs:
            log_class = 'error' if log['type'] == 'error' else 'log'
            console_html += f'<div class="console-{log_class}">[{log["type"]}] {log["text"]}</div>\n'

        # 錯誤訊息 HTML
        error_html = ''
        if self._error_message:
            error_html = f'''
            <div class="error-section">
                <h2>錯誤訊息</h2>
                <pre>{self._error_message}</pre>
            </div>
            '''

        # 執行時間格式化
        exec_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>測試報告 - {test_name}</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }}
        .header {{
            background: {status_color};
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 24px;
        }}
        .header .meta {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .summary-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card .value {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
        }}
        .summary-card .label {{
            color: #666;
            margin-top: 5px;
            font-size: 14px;
        }}
        .step {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .step.success {{ border-left: 4px solid #4caf50; }}
        .step.failure {{ border-left: 4px solid #f44336; }}
        .step h3 {{
            margin: 0 0 10px 0;
            font-size: 18px;
        }}
        .step p {{
            margin: 5px 0;
            color: #666;
            font-size: 14px;
        }}
        .step img {{
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-top: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .step img.expanded {{
            max-width: none;
            width: 100%;
        }}
        .console {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            max-height: 300px;
            overflow-y: auto;
        }}
        .console-error {{ color: #f44336; }}
        .console-log {{ color: #d4d4d4; }}
        .console-warn {{ color: #ff9800; }}
        .error-section {{
            background: #ffebee;
            border: 1px solid #f44336;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .error-section h2 {{
            margin: 0 0 10px 0;
            color: #c62828;
        }}
        .error-section pre {{
            background: #fff;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 0;
        }}
        h2 {{
            color: #333;
            margin: 30px 0 15px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{status_icon} 測試報告：{test_name}</h1>
        <div class="meta">
            執行時間：{exec_time} | 耗時：{duration:.2f}s | 執行次數：#{report_num}
        </div>
    </div>

    <div class="summary">
        <div class="summary-card">
            <div class="value">{len(self._steps)}</div>
            <div class="label">總步驟</div>
        </div>
        <div class="summary-card">
            <div class="value">{len([s for s in self._steps if not s['is_failure']])}</div>
            <div class="label">成功</div>
        </div>
        <div class="summary-card">
            <div class="value">{len([s for s in self._steps if s['is_failure']])}</div>
            <div class="label">失敗</div>
        </div>
        <div class="summary-card">
            <div class="value">{duration:.1f}s</div>
            <div class="label">耗時</div>
        </div>
    </div>

    {error_html}

    <h2>測試步驟</h2>
    {steps_html if steps_html else '<p>無步驟記錄</p>'}

    <h2>控制台日誌</h2>
    <div class="console">
        {console_html if console_html else '<div>無日誌</div>'}
    </div>
</body>
</html>'''

    def _generate_markdown(self, test_name: str, duration: float, report_num: int) -> str:
        """產出 Markdown 報告"""
        status_text = '✅ 通過' if self._status == 'passed' else '❌ 失敗'
        exec_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 步驟 Markdown
        steps_md = ''
        for step in self._steps:
            step_icon = '❌' if step['is_failure'] else '✅'
            steps_md += f'''
### {step_icon} 步驟 {step['num']}：{step['name']}

- **URL:** {step['url']}
- **時間:** {step['timestamp']}

![{step['name']}](../screenshots/{step['filename']})

'''

        # 控制台日誌 Markdown
        console_md = ''
        for log in self._console_logs:
            console_md += f'- [{log["type"]}] {log["text"]}\n'

        # 錯誤訊息 Markdown
        error_md = ''
        if self._error_message:
            error_md = f'''
## 錯誤訊息

```
{self._error_message}
```

'''

        return f'''# 測試報告：{test_name}

| 項目 | 值 |
|------|-----|
| 狀態 | {status_text} |
| 執行時間 | {exec_time} |
| 耗時 | {duration:.2f}s |
| 執行次數 | #{report_num} |
| 總步驟 | {len(self._steps)} |
| 失敗步驟 | {len([s for s in self._steps if s['is_failure']])} |

{error_md}

## 測試步驟

{steps_md if steps_md else '無步驟記錄'}

## 控制台日誌

{console_md if console_md else '無日誌'}
'''
