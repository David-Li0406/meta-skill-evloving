#!/usr/bin/env python3
"""
快速截取網頁截圖

Usage:
    python commands/screenshot.py <url> [output.png] [--login]

Examples:
    # 截取公開頁面
    python commands/screenshot.py http://localhost:3000 homepage.png

    # 截取需要登入的頁面
    python commands/screenshot.py http://localhost:3000/dashboard dashboard.png --login

    # 使用預設檔名
    python commands/screenshot.py http://localhost:3000
"""

import sys
import os
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='快速截取網頁截圖')
    parser.add_argument('url', help='目標 URL')
    parser.add_argument('output', nargs='?', help='輸出檔名 (預設: screenshot_HHMMSS.png)')
    parser.add_argument('--login', action='store_true', help='先登入再截圖')
    parser.add_argument('--full', action='store_true', default=True, help='全頁截圖 (預設)')
    parser.add_argument('--visible', action='store_true', help='只截取可見區域')

    args = parser.parse_args()

    # 產生預設檔名
    if not args.output:
        timestamp = datetime.now().strftime('%H%M%S')
        args.output = f'screenshot_{timestamp}.png'

    # 確保 screenshots 目錄存在
    os.makedirs('screenshots', exist_ok=True)
    output_path = os.path.join('screenshots', args.output)

    # 動態產生測試腳本
    script = generate_script(args.url, output_path, args.login, not args.visible)

    # 執行
    print(f'📸 截取截圖: {args.url}')
    print(f'   輸出: {output_path}')
    if args.login:
        print('   模式: 登入後截圖')
    print()

    exec(script)

def generate_script(url: str, output: str, login: bool, full_page: bool) -> str:
    login_code = ''
    if login:
        login_code = '''
    # 讀取測試帳號
    from dotenv import load_dotenv
    if os.path.exists('.env.test'):
        load_dotenv('.env.test')
    else:
        print('❌ 需要 .env.test 才能登入')
        sys.exit(1)

    email = os.getenv('TEST_USER_EMAIL')
    password = os.getenv('TEST_USER_PASSWORD')
    base_url = os.getenv('TEST_BASE_URL', 'http://localhost:9002')

    # 登入
    page.goto(f'{base_url}/login', wait_until='domcontentloaded')
    page.wait_for_load_state('networkidle')
    page.fill('input[type="email"]', email)
    page.fill('input[type="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle')
    print('   ✓ 登入成功')
'''

    return f'''
from playwright.sync_api import sync_playwright
import os
import sys

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={{'width': 1920, 'height': 1080}})
    page.set_default_timeout(60000)
{login_code}
    # 導航到目標頁面
    page.goto('{url}', wait_until='domcontentloaded')
    page.wait_for_load_state('networkidle')

    # 截圖
    page.screenshot(path='{output}', full_page={full_page})
    print(f'   ✓ 截圖已儲存: {output}')

    browser.close()
'''

if __name__ == '__main__':
    main()
