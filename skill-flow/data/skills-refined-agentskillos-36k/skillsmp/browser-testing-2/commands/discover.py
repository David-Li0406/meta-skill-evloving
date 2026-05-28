#!/usr/bin/env python3
"""
探索頁面元素（按鈕、連結、輸入框）

Usage:
    python commands/discover.py <url> [--login]

Examples:
    python commands/discover.py http://localhost:3000
    python commands/discover.py http://localhost:3000/dashboard --login
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='探索頁面元素')
    parser.add_argument('url', help='目標 URL')
    parser.add_argument('--login', action='store_true', help='先登入再探索')

    args = parser.parse_args()

    script = generate_script(args.url, args.login)
    exec(script)

def generate_script(url: str, login: bool) -> str:
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
    print('✓ 登入成功\\n')
'''

    return f'''
from playwright.sync_api import sync_playwright
import os
import sys

print('🔍 探索頁面元素: {url}\\n')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_default_timeout(60000)
{login_code}
    # 導航到目標頁面
    page.goto('{url}', wait_until='domcontentloaded')
    page.wait_for_load_state('networkidle')

    # 探索按鈕
    buttons = page.locator('button').all()
    print(f'📍 按鈕 ({{len(buttons)}} 個):')
    for i, btn in enumerate(buttons[:10]):
        try:
            text = btn.inner_text().strip()[:50] if btn.is_visible() else '[hidden]'
            print(f'   [{{i}}] {{text}}')
        except:
            pass
    if len(buttons) > 10:
        print(f'   ... 還有 {{len(buttons) - 10}} 個')

    # 探索連結
    links = page.locator('a[href]').all()
    print(f'\\n🔗 連結 ({{len(links)}} 個):')
    for link in links[:10]:
        try:
            text = link.inner_text().strip()[:30]
            href = link.get_attribute('href')[:50]
            if text:
                print(f'   {{text}} -> {{href}}')
        except:
            pass
    if len(links) > 10:
        print(f'   ... 還有 {{len(links) - 10}} 個')

    # 探索輸入框
    inputs = page.locator('input, textarea, select').all()
    print(f'\\n📝 輸入框 ({{len(inputs)}} 個):')
    for inp in inputs[:10]:
        try:
            name = inp.get_attribute('name') or inp.get_attribute('id') or inp.get_attribute('placeholder') or '[unnamed]'
            inp_type = inp.get_attribute('type') or 'text'
            print(f'   {{name}} ({{inp_type}})')
        except:
            pass

    # 截圖
    os.makedirs('screenshots', exist_ok=True)
    page.screenshot(path='screenshots/discover.png', full_page=True)
    print(f'\\n📸 截圖已儲存: screenshots/discover.png')

    browser.close()
'''

if __name__ == '__main__':
    main()
