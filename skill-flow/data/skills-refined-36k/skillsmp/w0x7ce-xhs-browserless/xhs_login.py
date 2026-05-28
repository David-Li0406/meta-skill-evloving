#!/usr/bin/env python3
"""
小红书登录脚本 - 支持两种登录方式

方式1: 扫码登录（推荐，安全）
方式2: 直接指定 Cookie（快速，无需扫码）

Cookie 获取方式：
1. 浏览器中登录小红书
2. F12 → Application → Cookies → xiaohongshu.com
3. 复制 web_session, webId 等关键 Cookie
"""

from playwright.sync_api import sync_playwright
import os
import sys
import random
import json
from datetime import datetime
from pathlib import Path

# 加载 .env 文件
ENV_FILE = Path(__file__).parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# ==================== 配置 ====================

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

WS_URL = os.environ.get("XHS_WS_URL", "ws://hk2.w0x7ce.eu:10086?token=255=ff")
STATE_FILE = os.environ.get("XHS_STATE_FILE", os.path.join(SCRIPT_DIR, "xhs_browser_state.json"))
COOKIE_FILE = os.environ.get("XHS_COOKIE_FILE", os.path.join(SCRIPT_DIR, "cookies.txt"))
SCREENSHOT_DIR = os.path.join(SCRIPT_DIR, "screenshots")
ENABLE_SCREENSHOTS = os.environ.get("XHS_SCREENSHOTS", "") == "1"

if ENABLE_SCREENSHOTS:
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

REAL_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
]

STEALTH_JS = """
() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en-US', 'en'] });
    Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
    window.chrome = { runtime: {}, loadTimes: function() {}, csi: function() {}, app: {} };
}
"""

# ==================== Cookie 登录 ====================

def load_cookies_from_file():
    """从文件加载 Cookie（支持 JSON 和浏览器导出的制表符格式）"""
    if not os.path.exists(COOKIE_FILE):
        return None

    try:
        with open(COOKIE_FILE, 'r') as f:
            content = f.read().strip()

        # 判断文件格式
        if content.startswith('{'):
            # JSON 格式
            data = json.loads(content)
            if "cookies" not in data:
                return None
            cookies = []
            for c in data["cookies"]:
                if not c.get("value") or str(c["value"]).startswith("在这里粘贴"):
                    continue
                cookies.append({
                    "name": c["name"],
                    "value": c["value"],
                    "domain": ".xiaohongshu.com",
                    "path": "/",
                })
            return cookies if cookies else None

        else:
            # 浏览器导出的制表符格式
            # 格式: name	value	domain	path	expiry	...
            cookies = []
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split('\t')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    value = parts[1].strip()
                    if name and value:
                        cookies.append({
                            "name": name,
                            "value": value,
                            "domain": ".xiaohongshu.com",
                            "path": "/",
                        })

            return cookies if cookies else None

    except Exception as e:
        print(f"⚠️  解析 Cookie 文件失败: {e}")
        return None

def save_cookies_to_file(cookies):
    """保存 Cookie 到文件（制表符格式，方便从浏览器复制粘贴）"""
    with open(COOKIE_FILE, 'w') as f:
        f.write(f"# 小红书登录 Cookie - 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# 直接从浏览器复制粘贴到这里\n")
        f.write("# 格式: name<TAB>value<TAB>domain<TAB>path...\n")
        f.write("\n")
        for c in cookies:
            f.write(f"{c['name']}\t{c['value']}\t.xiaohongshu.com\t/\n")
    print(f"💾 Cookie 已保存到: {COOKIE_FILE}")

def login_with_cookies(use_file=False):
    """使用 Cookie 登录"""
    print("\n" + "="*60)
    print("🍪 Cookie 登录方式")
    print("="*60)

    cookies = None

    # 尝试从文件读取
    if use_file or os.path.exists(COOKIE_FILE):
        cookies = load_cookies_from_file()
        if cookies:
            print(f"\n✅ 从文件读取到 {len(cookies)} 个 Cookie")
            for c in cookies:
                print(f"   - {c['name']}")
        else:
            print(f"\n⚠️  Cookie 文件不存在或格式错误")
            use_file = False

    # 手动输入
    if not cookies:
        print("\n📖 获取 Cookie 步骤:")
        print("1. 在浏览器中登录小红书 https://www.xiaohongshu.com")
        print("2. 按 F12 打开开发者工具")
        print("3. 切换到 Application → Cookies → xiaohongshu.com")
        print("4. 选择所有 Cookie，复制")
        print("5. 直接粘贴到 cookies.txt 文件中")
        print("   或者粘贴到下面（按 Ctrl+D 结束输入）:")
        print("\n" + "="*60)

        # 支持多行输入（制表符格式）
        print("\n📝 请粘贴 Cookie（按 Ctrl+D 或输入 END 结束）:")
        cookie_lines = []
        try:
            while True:
                line = input()
                if line.strip() == "END":
                    break
                cookie_lines.append(line)
        except EOFError:
            pass

        cookie_str = '\n'.join(cookie_lines).strip()

        if not cookie_str:
            print("❌ Cookie 不能为空")
            return False

        # 解析制表符格式
        cookies = []
        for line in cookie_str.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split('\t')
            if len(parts) >= 2:
                name = parts[0].strip()
                value = parts[1].strip()
                if name and value:
                    cookies.append({
                        "name": name,
                        "value": value,
                        "domain": ".xiaohongshu.com",
                        "path": "/",
                    })

        print(f"\n✅ 解析到 {len(cookies)} 个 Cookie")
        for c in cookies:
            print(f"   - {c['name']}")

        # 保存到文件
        save_choice = input("\n💾 是否保存到文件 cookies.txt 以便下次使用? (y/n): ").strip().lower()
        if save_choice == 'y':
            # 保存到 txt 文件（制表符格式）
            txt_file = "cookies.txt"
            with open(txt_file, 'w') as f:
                f.write(f"# 小红书登录 Cookie - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for line in cookie_str.split('\n'):
                    f.write(line + '\n')
            print(f"💾 Cookie 已保存到: {txt_file}")
            # 同时更新 JSON 格式供脚本使用
            COOKIE_FILE_TMP = "cookies.txt"
            with open(COOKIE_FILE_TMP, 'w') as f:
                for line in cookie_str.split('\n'):
                    f.write(line + '\n')
            print(f"💾 同时更新了 {COOKIE_FILE_TMP}")

    # 连接并设置 Cookie
    with sync_playwright() as p:
        print("\n🔗 连接到 Browserless...")
        try:
            browser = p.chromium.connect_over_cdp(WS_URL)
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            print("💡 请检查 Browserless 服务器是否运行")
            return False

        context = browser.new_context(
            user_agent=random.choice(REAL_USER_AGENTS),
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )

        # 添加 Cookie
        context.add_cookies(cookies)
        print("✅ Cookie 已添加到浏览器")

        page = context.new_page()

        # 访问小红书验证
        print("\n🌐 访问小红书验证登录...")
        page.goto("https://www.xiaohongshu.com", wait_until="networkidle")

        import time
        time.sleep(3)

        # 截图（默认禁用，设置 XHS_SCREENSHOTS=1 启用）
        if ENABLE_SCREENSHOTS:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=f"{SCREENSHOT_DIR}/cookie_login_{timestamp}.png", full_page=True)

        url = page.url
        title = page.title()

        print(f"\n📄 页面标题: {title}")
        print(f"🔗 当前 URL: {url}")

        # 检查是否登录成功
        is_logged_in = "login" not in url.lower() and "captcha" not in url.lower()

        if is_logged_in:
            print("✅ 登录成功！")

            # 保存状态
            context.storage_state(path=STATE_FILE)
            print(f"💾 状态已保存: {STATE_FILE}")

            if os.path.exists(STATE_FILE):
                size = os.path.getsize(STATE_FILE)
                print(f"✅ 状态文件大小: {size} bytes")

            print("\n" + "="*60)
            print("✅ 现在可以使用发布脚本了！")
            print("="*60)
            print("\n发布命令:")
            print("npx -y bun w0x7ce_skills/skills/w0x7ce-xiaohongshu-publisher/scripts/publish.ts \\")
            print('  publish "标题" "内容"')
            print("="*60)
            return True
        else:
            print("❌ Cookie 可能无效或已过期")
            print("💡 请重新获取 Cookie")
            return False

# ==================== 扫码登录 ====================

def login_with_qrcode():
    """使用二维码登录"""
    print("\n" + "="*60)
    print("📱 扫码登录方式")
    print("="*60)

    with sync_playwright() as p:
        print("\n🔗 连接到 Browserless...")
        try:
            browser = p.chromium.connect_over_cdp(WS_URL)
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False

        context = browser.new_context(
            user_agent=random.choice(REAL_USER_AGENTS),
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )

        page = context.new_page()
        page.add_init_script(STEALTH_JS)

        print("\n🌐 打开小红书首页...")
        page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded")

        import time
        time.sleep(5)

        # 截图显示二维码（默认禁用，设置 XHS_SCREENSHOTS=1 启用）
        if ENABLE_SCREENSHOTS:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            qr_path = f"{SCREENSHOT_DIR}/xhs_qr_{timestamp}.png"
            page.screenshot(path=qr_path, full_page=True)
            print(f"\n✅ 二维码已保存: {qr_path}")
        else:
            print("\n📱 请查看浏览器中的二维码")
        print("\n" + "="*60)
        print("📱 请用小红书 APP 扫描二维码登录")
        print("="*60)
        print("\n步骤:")
        print("1. 打开小红书 APP")
        print("2. 点击「我」→「设置」→「扫一扫」")
        print("3. 扫描二维码图片")
        print("4. 在手机上确认登录")
        print("\n扫描完成后按 Enter 继续...")

        input()

        print("\n⏳ 等待登录完成...")
        print("💡 正在等待页面跳转，请稍候...")

        # 等待页面变化，最多等待 30 秒
        max_wait = 30
        for i in range(max_wait):
            time.sleep(1)
            try:
                current_url = page.url
                if "login" not in current_url.lower() and "captcha" not in current_url.lower():
                    print(f"\n✅ 检测到登录成功！(等待 {i+1} 秒)")
                    break
            except Exception as e:
                print(f"⚠️  连接中断: {e}")
                print("💡 尝试重新连接...")

                # 尝试重新连接并获取状态
                try:
                    browser = p.chromium.connect_over_cdp(WS_URL)
                    contexts = browser.contexts
                    if contexts:
                        context = contexts[0]
                    else:
                        print("❌ 无法恢复连接")
                        return False
                except:
                    print("❌ 重新连接失败")
                    return False

        # 再等待一下确保完全加载
        time.sleep(3)

        # 检查登录状态
        try:
            url = page.url
            print(f"\n🔗 当前 URL: {url}")
        except:
            print("⚠️  无法获取 URL，但尝试保存状态...")

        try:
            title = page.title()
            print(f"📄 当前页面: {title}")
        except:
            print("⚠️  无法获取标题")

        # 登录后截图（默认禁用，设置 XHS_SCREENSHOTS=1 启用）
        if ENABLE_SCREENSHOTS:
            try:
                after_path = f"{SCREENSHOT_DIR}/xhs_logged_in_{timestamp}.png"
                page.screenshot(path=after_path, full_page=True)
                print(f"📸 登录后截图: {after_path}")
            except Exception as e:
                print(f"⚠️  截图失败: {e}")

        # 保存登录状态（重要！即使连接断开也尝试保存）
        print(f"\n💾 保存登录状态到: {STATE_FILE}")
        try:
            context.storage_state(path=STATE_FILE)
        except Exception as e:
            print(f"⚠️  保存状态失败: {e}")
            # 尝试使用浏览器级别的状态保存
            try:
                if browser.contexts:
                    browser.contexts[0].storage_state(path=STATE_FILE)
                    print("✅ 使用备用方式保存成功")
            except:
                print("❌ 状态保存失败")

        # 验证状态文件
        if os.path.exists(STATE_FILE):
            size = os.path.getsize(STATE_FILE)
            print(f"✅ 状态文件已保存 ({size} bytes)")

            if "login" not in url.lower():
                print("\n✅ 登录成功！现在可以使用发布脚本了")
                success = True
            else:
                print("\n⚠️  登录可能未成功，请检查")
                success = False
        else:
            print("❌ 状态文件保存失败")
            success = False

        browser.close()
        return success

# ==================== 主函数 ====================

def main():
    print("="*60)
    print("🚀 小红书登录工具")
    print("="*60)
    print(f"🔗 Browserless: {WS_URL}")
    print(f"💾 状态文件: {STATE_FILE}")
    print("="*60)

    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--cookie" or sys.argv[1] == "-c":
            success = login_with_cookies()
        elif sys.argv[1] == "--file" or sys.argv[1] == "-f":
            success = login_with_cookies(use_file=True)
        elif sys.argv[1] == "--qrcode" or sys.argv[1] == "-q":
            success = login_with_qrcode()
        else:
            print(f"\n❌ 未知参数: {sys.argv[1]}")
            print("\n用法:")
            print("  python xhs_login.py              # 交互式选择")
            print("  python xhs_login.py --cookie     # 手动输入 Cookie")
            print("  python xhs_login.py --file       # 从 cookies.json 读取")
            print("  python xhs_login.py --qrcode     # 扫码登录")
            return
    else:
        # 交互式选择
        print("\n请选择登录方式:")
        print("  1. 扫码登录（推荐，安全）")
        print("  2. Cookie 登录（快速，需要从浏览器复制）")

        choice = input("\n请输入选择 (1 或 2，直接回车默认扫码): ").strip()

        if choice == "2":
            success = login_with_cookies()
        else:
            success = login_with_qrcode()

    if success:
        print("\n✅ 登录流程完成！")
    else:
        print("\n❌ 登录失败，请重试")

if __name__ == "__main__":
    main()
