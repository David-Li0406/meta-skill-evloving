#!/usr/bin/env python3
"""
TestManager 示範腳本

執行方式：
    cd ~/.claude/skills/browser-testing
    python commands/run-test.py examples/test_manager_demo.py
"""

from browser_testing import TestManager

with TestManager(headless=True) as tm:
    page = tm.page

    # 步驟 1：訪問 example.com
    page.goto('https://example.com')
    page.wait_for_load_state('domcontentloaded')
    tm.capture('Example.com 首頁')

    # 步驟 2：檢查標題
    title = page.title()
    if 'Example' in title:
        tm.capture('標題驗證成功')
    else:
        tm.fail(f'標題不正確: {title}')
        tm.capture('標題驗證失敗')

    # 步驟 3：檢查內容
    content = page.text_content('h1')
    tm.capture('內容檢查完成')

print('\n示範完成！請查看 examples/screenshots/ 和 examples/test-reports/')
