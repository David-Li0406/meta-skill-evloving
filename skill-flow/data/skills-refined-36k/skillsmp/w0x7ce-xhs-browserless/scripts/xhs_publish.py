#!/usr/bin/env python3
"""
小红书发布脚本 - Python 版本
支持自动发布图文笔记
"""

from playwright.sync_api import sync_playwright
import os
import sys
from pathlib import Path

# 加载 .env 文件
ENV_FILE = Path(__file__).parent.parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

WS_URL = os.environ.get("XHS_WS_URL", "ws://hk2.w0x7ce.eu:10086?token=255=ff")
STATE_FILE = os.environ.get("XHS_STATE_FILE", os.path.join(os.path.dirname(__file__), "..", "xhs_browser_state.json"))
# 截图目录（默认禁用，设置环境变量 XHS_SCREENSHOTS=1 启用）
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
ENABLE_SCREENSHOTS = os.environ.get("XHS_SCREENSHOTS", "") == "1"

# 创作者平台发布页面
PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=image"

# 多语言选择器
I18N_SELECTORS = {
    'titleInput': [
        'input[placeholder*="填写标题"]',
        'input[placeholder*="添加标题"]',
        'input[placeholder*="标题"]',
    ],
    'contentInput': [
        'div[contenteditable="true"][placeholder*="填写正文"]',
        'div[contenteditable="true"][placeholder*="添加正文"]',
        'div[contenteditable="true"]',
    ],
    'publishButton': [
        'button[type="submit"]',
        'button:has-text("发布")',
        'button:has-text("發布")',
    ],
}


def publish_note(title, content, image_path, submit=False):
    """发布笔记"""
    print(f"\n📝 开始发布笔记...")
    print(f"📌 标题: {title}")
    print(f"✍️  内容: {content[:100]}...")
    print(f"📷 图片: {image_path}")
    print(f"🚢 模式: {'发布' if submit else '预览'}")

    with sync_playwright() as p:
        print(f"🔗 连接到 Browserless: {WS_URL}")
        browser = p.chromium.connect_over_cdp(WS_URL)

        # 检查状态文件
        if not os.path.exists(STATE_FILE):
            print("❌ 未找到登录状态文件")
            print("请先运行: python3 xhs_login.py --file")
            browser.close()
            return False

        print(f"📂 加载登录状态: {STATE_FILE}")
        context = browser.new_context(
            storage_state=STATE_FILE,
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )

        page = context.new_page()

        try:
            # 访问发布页面
            print(f"🌐 打开发布页面...")
            page.goto(PUBLISH_URL, wait_until="networkidle")

            import time
            time.sleep(3)

            # 检查登录
            url = page.url
            if "login" in url.lower():
                print("❌ 未登录，请先运行: python3 xhs_login.py --file")
                return False

            # 截图（默认禁用，设置 XHS_SCREENSHOTS=1 启用）
            if ENABLE_SCREENSHOTS:
                os.makedirs(SCREENSHOT_DIR, exist_ok=True)
                page.screenshot(path=f"{SCREENSHOT_DIR}/publish_page.png", full_page=True)
                print(f"📸 截图: {SCREENSHOT_DIR}/publish_page.png")

            # 输入标题
            print("\n📌 输入标题...")
            for selector in I18N_SELECTORS['titleInput']:
                try:
                    el = page.query_selector(selector)
                    if el and el.is_visible():
                        el.click()
                        time.sleep(0.5)
                        # 逐字输入
                        for char in title:
                            page.keyboard.type(char)
                            time.sleep(0.03)
                        print("✅ 标题已输入")
                        break
                except:
                    continue

            # 上传图片
            print("\n📷 上传图片...")
            file_input = page.query_selector("input[type='file']")
            if file_input:
                file_input.set_input_files(image_path)
                time.sleep(3)
                print("✅ 图片已上传")
            else:
                print("⚠️  未找到上传控件")

            # 输入内容
            print("\n✍️  输入内容...")
            for selector in I18N_SELECTORS['contentInput']:
                try:
                    el = page.query_selector(selector)
                    if el and el.is_visible():
                        el.click()
                        time.sleep(0.5)
                        # 逐字输入
                        for char in content:
                            page.keyboard.type(char)
                            time.sleep(0.03)
                        print("✅ 内容已输入")
                        break
                except:
                    continue

            # 截图预览（默认禁用，设置 XHS_SCREENSHOTS=1 启用）
            if ENABLE_SCREENSHOTS:
                page.screenshot(path=f"{SCREENSHOT_DIR}/before_submit.png", full_page=True)
                print(f"📸 预览截图: {SCREENSHOT_DIR}/before_submit.png")

            # 发布
            if submit:
                print("\n🚀 开始发布...")
                for selector in I18N_SELECTORS['publishButton']:
                    try:
                        el = page.query_selector(selector)
                        if el and el.is_visible():
                            el.click()
                            print("✅ 发布按钮已点击")
                            time.sleep(5)

                            # 检查结果
                            final_url = page.url
                            print(f"📄 当前页面: {final_url}")

                            if "success" in final_url or "publish" not in final_url:
                                print("\n✅ 发布可能成功！")
                            else:
                                print("\n⚠️  请检查浏览器确认")
                            break
                    except:
                        continue
            else:
                print("\n👀 预览模式 - 请查看截图确认")

            # 保存状态 (可选)
            try:
                context.storage_state(path=STATE_FILE)
            except:
                pass  # 状态保存失败不影响发布结果

            return True

        except Exception as e:
            print(f"❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            browser.close()


if __name__ == "__main__":
    # 解析命令行参数
    title = None
    content = None
    image_path = None
    submit = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == "--content" and i + 1 < len(args):
            content = args[i + 1]
            i += 2
        elif args[i] == "--image" and i + 1 < len(args):
            image_path = args[i + 1]
            i += 2
        elif args[i] == "--submit":
            submit = True
            i += 1
        elif args[i] in ["--help", "-h"]:
            print("用法: python3 xhs_publish.py --title \"标题\" --content \"内容\" --image <图片路径> [--submit]")
            sys.exit(0)
        else:
            i += 1

    # 使用参数或默认值
    if not title:
        title = "aaa"
    if not content:
        content = "这是测试笔记内容"
    if not image_path:
        image_path = "/home/w0x7ce/Downloads/AOMG/vps_test.png"

    publish_note(
        title=title,
        content=content,
        image_path=image_path,
        submit=submit
    )
