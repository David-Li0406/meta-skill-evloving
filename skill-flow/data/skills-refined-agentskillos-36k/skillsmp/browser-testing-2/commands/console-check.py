#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
瀏覽器 Console 錯誤檢查工具

自動登入後檢查頁面的 console 錯誤、網路請求錯誤、和 DOM 狀態。
用於除錯 UI 問題，例如側邊欄空白、元件未載入等。

用法：
    python commands/console-check.py [url] [--login] [--wait N]

範例：
    # 檢查首頁（需要登入）
    python commands/console-check.py http://localhost:3000 --login

    # 檢查特定頁面，等待 10 秒
    python commands/console-check.py http://localhost:3000/inbox --login --wait 10

    # 檢查不需登入的頁面
    python commands/console-check.py http://localhost:3000/widget-demo
"""

import argparse
import io
import json
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# 修復 Windows 命令列中文輸出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description='檢查瀏覽器 console 錯誤')
    parser.add_argument('url', nargs='?', help='要檢查的 URL')
    parser.add_argument('--login', action='store_true', help='需要先登入')
    parser.add_argument('--wait', type=int, default=5, help='頁面載入後等待秒數 (預設: 5)')
    parser.add_argument('--output', '-o', help='輸出截圖路徑')
    args = parser.parse_args()

    # 載入測試設定
    if os.path.exists('.env.test'):
        load_dotenv('.env.test')

    base_url = os.getenv('TEST_BASE_URL', 'http://localhost:3000')
    url = args.url or base_url

    # 確保截圖目錄存在
    screenshots_dir = 'screenshots'
    os.makedirs(screenshots_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = args.output or f'{screenshots_dir}/console_check_{timestamp}.png'

    print(f'=== Console Check ===')
    print(f'URL: {url}')
    print(f'Login: {args.login}')
    print(f'Wait: {args.wait}s')
    print()

    # 收集資料
    console_logs = []
    error_responses = []
    all_responses = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(60000)

        # 監聽 console
        def on_console(msg):
            console_logs.append({
                'type': msg.type,
                'text': msg.text,
                'location': str(msg.location) if msg.location else None
            })
        page.on('console', on_console)

        # 監聽網路回應
        def on_response(response):
            entry = {
                'status': response.status,
                'method': response.request.method,
                'url': response.url
            }
            all_responses.append(entry)
            if response.status >= 400:
                error_responses.append(entry)
        page.on('response', on_response)

        # 如果需要登入
        if args.login:
            email = os.getenv('TEST_USER_EMAIL')
            password = os.getenv('TEST_USER_PASSWORD')

            if not email or not password:
                print('ERROR: 需要 .env.test 中的 TEST_USER_EMAIL 和 TEST_USER_PASSWORD')
                sys.exit(1)

            print(f'1. 登入中 ({email})...')
            login_url = f'{base_url}/login'
            page.goto(login_url, wait_until='domcontentloaded')
            page.wait_for_timeout(2000)

            page.fill('input[type="email"]', email)
            page.fill('input[type="password"]', password)
            page.click('button[type="submit"]')

            # 等待登入完成
            try:
                page.wait_for_url(lambda u: '/login' not in u, timeout=30000)
                print('   登入成功')
            except:
                print('   登入失敗，停留在登入頁')
                page.screenshot(path=screenshot_path, full_page=True)
                browser.close()
                sys.exit(1)

        # 導航到目標 URL
        if not args.login or url != base_url:
            print(f'2. 導航到 {url}...')
            page.goto(url, wait_until='domcontentloaded')

        # 等待頁面穩定
        print(f'3. 等待 {args.wait} 秒讓頁面載入...')
        page.wait_for_timeout(args.wait * 1000)

        # 收集頁面資訊
        print('4. 收集頁面資訊...')

        # 取得 session 狀態
        session_info = None
        try:
            session_info = page.evaluate('''async () => {
                try {
                    const response = await fetch('/api/auth/session');
                    return {
                        status: response.status,
                        data: await response.json()
                    };
                } catch (e) {
                    return { error: e.message };
                }
            }''')
        except:
            pass

        # 取得 DOM 資訊
        dom_info = page.evaluate('''() => {
            return {
                title: document.title,
                url: window.location.href,
                navLinks: document.querySelectorAll('nav a').length,
                navButtons: document.querySelectorAll('nav button').length,
                alerts: document.querySelectorAll('[role="alert"]').length,
                loadingText: document.body.innerText.includes('載入中'),
                errorText: document.body.innerText.includes('錯誤') || document.body.innerText.includes('Error')
            };
        }''')

        # 截圖
        page.screenshot(path=screenshot_path, full_page=True)
        print(f'5. 截圖已儲存: {screenshot_path}')

        browser.close()

    # 輸出報告
    print()
    print('=' * 50)
    print('檢查報告')
    print('=' * 50)

    # DOM 狀態
    print()
    print('【頁面狀態】')
    print(f'  標題: {dom_info["title"]}')
    print(f'  URL: {dom_info["url"]}')
    print(f'  導航連結數: {dom_info["navLinks"]}')
    print(f'  導航按鈕數: {dom_info["navButtons"]}')
    print(f'  Alert 元素: {dom_info["alerts"]}')
    print(f'  顯示「載入中」: {dom_info["loadingText"]}')
    print(f'  顯示錯誤文字: {dom_info["errorText"]}')

    # Session 狀態
    if session_info:
        print()
        print('【Session 狀態】')
        if 'error' in session_info:
            print(f'  錯誤: {session_info["error"]}')
        else:
            print(f'  HTTP 狀態: {session_info["status"]}')
            if session_info.get('data', {}).get('isValid'):
                user = session_info['data'].get('user', {})
                print(f'  使用者: {user.get("name")} ({user.get("email")})')
                print(f'  角色: {user.get("role")}')
            else:
                print('  Session 無效或已過期')

    # Console 錯誤
    errors = [log for log in console_logs if log['type'] == 'error']
    warnings = [log for log in console_logs if log['type'] == 'warning']

    if errors:
        print()
        print(f'【Console 錯誤】({len(errors)} 個)')
        for err in errors[:10]:  # 最多顯示 10 個
            print(f'  - {err["text"][:100]}')
        if len(errors) > 10:
            print(f'  ... 還有 {len(errors) - 10} 個錯誤')

    if warnings:
        print()
        print(f'【Console 警告】({len(warnings)} 個)')
        for warn in warnings[:5]:
            print(f'  - {warn["text"][:100]}')

    # HTTP 錯誤
    if error_responses:
        print()
        print(f'【HTTP 錯誤】({len(error_responses)} 個)')
        for resp in error_responses[:10]:
            print(f'  - {resp["status"]} {resp["method"]} {resp["url"][:80]}')
        if len(error_responses) > 10:
            print(f'  ... 還有 {len(error_responses) - 10} 個錯誤')

    # 總結
    print()
    print('=' * 50)
    issues = []
    if errors:
        issues.append(f'{len(errors)} console 錯誤')
    if error_responses:
        issues.append(f'{len(error_responses)} HTTP 錯誤')
    if dom_info['navLinks'] == 0:
        issues.append('導航欄空白')
    if dom_info['loadingText']:
        issues.append('頁面仍在載入')

    if issues:
        print(f'發現問題: {", ".join(issues)}')
        print(f'請查看截圖: {screenshot_path}')
    else:
        print('未發現明顯問題')

    print()

if __name__ == '__main__':
    main()
