#!/usr/bin/env python3
"""
Prompt Extractor - 参考画像からビジュアル要素をYAML形式で抽出

Usage:
    python scripts/run.py prompt_extractor.py --image "/path/to/image.png"
    python scripts/run.py prompt_extractor.py --image "/path/to/image.png" --output analysis.yaml
"""

import sys
import json
import argparse
import time
import re
from pathlib import Path
from patchright.sync_api import sync_playwright

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    DATA_DIR,
    STATE_FILE,
    GEMINI_URL,
    DEFAULT_TIMEOUT
)
from browser_utils import BrowserFactory, StealthUtils


# YAML抽出用のプロンプトテンプレート
EXTRACTION_PROMPT = """この画像のビジュアル要素を分析し、以下のYAML形式で出力してください。
画像生成AIに指示するための詳細な分析をお願いします。

```yaml
visual_analysis:
  # 全体的なスタイル
  style:
    art_style: ""  # 写実的/イラスト/水彩/油絵/デジタルアート/アニメ/etc
    mood: ""  # 明るい/暗い/温かい/クール/ドラマチック/穏やか/etc
    texture: ""  # 滑らか/粗い/グランジ/etc

  # 色使い
  colors:
    primary: ""  # メインカラー
    secondary: ""  # サブカラー
    accent: ""  # アクセントカラー
    overall_tone: ""  # 暖色系/寒色系/モノクロ/パステル/ビビッド/etc

  # 構図
  composition:
    layout: ""  # 中央配置/三分割/対角線/etc
    perspective: ""  # 正面/俯瞰/アオリ/etc
    depth: ""  # 浅い/深い/etc

  # 被写体
  subjects:
    main: ""  # 主要な被写体の説明
    position: ""  # 左/中央/右/etc
    details: ""  # 被写体の詳細

  # 光
  lighting:
    type: ""  # 自然光/スタジオ/ネオン/etc
    direction: ""  # 正面/側面/逆光/上から/etc
    intensity: ""  # 強/中/弱
    quality: ""  # 柔らかい/硬い/拡散/etc

  # 背景
  background:
    type: ""  # 単色/グラデーション/風景/室内/etc
    description: ""  # 背景の詳細
    blur: ""  # ボケあり/シャープ/etc

  # 追加の特徴
  additional:
    effects: ""  # グロー/ビネット/フィルム粒子/etc
    notable_features: ""  # その他の特筆すべき特徴
```

上記のYAMLフォーマットに従って、この画像を分析してください。
値がない項目は空文字列のままにしてください。"""


def check_authenticated():
    """Check if user is authenticated."""
    if not STATE_FILE.exists():
        return False
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        if 'cookies' not in state or len(state['cookies']) == 0:
            return False
        google_auth_cookies = [c for c in state['cookies']
                               if c['name'] in ['SID', 'HSID', 'SSID', '__Secure-1PSID']]
        return len(google_auth_cookies) >= 2
    except Exception:
        return False


def extract_yaml_from_response(text: str) -> str:
    """
    Geminiの応答からYAML部分を抽出する

    Args:
        text: Geminiからの応答テキスト

    Returns:
        str: 抽出されたYAML文字列
    """
    # ```yaml ... ``` ブロックを探す
    yaml_pattern = r'```yaml\s*(.*?)\s*```'
    match = re.search(yaml_pattern, text, re.DOTALL)

    if match:
        return match.group(1).strip()

    # ``` ... ``` ブロックを探す（yaml指定なし）
    code_pattern = r'```\s*(.*?)\s*```'
    match = re.search(code_pattern, text, re.DOTALL)

    if match:
        content = match.group(1).strip()
        # YAMLっぽい内容かチェック
        if 'visual_analysis:' in content or 'style:' in content:
            return content

    # visual_analysis: で始まる部分を探す
    if 'visual_analysis:' in text:
        start = text.find('visual_analysis:')
        yaml_text = text[start:]

        # additional: セクションの終わりを見つける（YAMLの終わり）
        # 空行2つ以上、または日本語/英語の説明文の開始で終了
        lines = yaml_text.split('\n')
        yaml_lines = []
        indent_stack = []

        for line in lines:
            # 空行は保持
            if line.strip() == '':
                yaml_lines.append(line)
                continue

            # YAMLのインデント構造を確認
            stripped = line.lstrip()
            indent = len(line) - len(stripped)

            # YAMLとして有効な行かチェック
            # - インデントされた行
            # - キー: 値 の形式
            # - リスト項目 (- で始まる)
            # - コメント (# で始まる)
            if (stripped.startswith('#') or
                stripped.startswith('-') or
                ':' in stripped or
                indent > 0):
                yaml_lines.append(line)
            else:
                # YAML以外の説明文が始まったら終了
                # ただし、値として続いている場合は含める
                if indent == 0 and not stripped.startswith(('visual_analysis', 'style', 'colors', 'composition', 'subjects', 'lighting', 'background', 'additional')):
                    break
                yaml_lines.append(line)

        return '\n'.join(yaml_lines).strip()

    return text


def extract_visual_prompt(
    image_path: str,
    output_path: str = None,
    show_browser: bool = False,
    timeout: int = 120
) -> dict:
    """
    参考画像からビジュアル要素をYAML形式で抽出する

    Args:
        image_path: 参考画像のパス
        output_path: YAML出力先（オプション）
        show_browser: ブラウザを表示するか
        timeout: タイムアウト秒数

    Returns:
        dict: 抽出結果 {"success": bool, "yaml": str, "error": str}
    """
    image_file = Path(image_path)
    if not image_file.exists():
        return {"success": False, "yaml": "", "error": f"Image not found: {image_path}"}

    print(f"📷 Analyzing reference image: {image_path}")

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(
            playwright,
            headless=not show_browser
        )

        page = context.pages[0] if context.pages else context.new_page()

        # Geminiに移動
        print("   → Opening Gemini...")
        page.goto(GEMINI_URL, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)

        # 認証チェック
        if "accounts.google.com" in page.url:
            print("❌ Not authenticated. Run: python scripts/run.py auth_manager.py setup")
            context.close()
            playwright.stop()
            return {"success": False, "yaml": "", "error": "Not authenticated"}

        # Step 1: 画像アップロード
        print("   → Looking for upload mechanism...")

        # Gemini UIでは「+」ボタンまたは添付ボタンをクリックしてアップロード
        # まず添付/追加ボタンを探してクリック
        add_button_selectors = [
            'button[aria-label*="その他のオプション"]',
            'button[aria-label*="Add"]',
            'button[aria-label*="追加"]',
            'button[aria-label*="添付"]',
            'button[aria-label*="ファイル"]',
            'button[aria-label*="画像を追加"]',
            'button[aria-label*="Insert"]',
            '[class*="add-content"]',
            '[class*="upload"]',
            'button:has(mat-icon:has-text("add"))',
            'button:has(mat-icon:has-text("attach_file"))',
            'button:has(mat-icon:has-text("image"))',
        ]

        button_clicked = False
        for selector in add_button_selectors:
            try:
                btn = page.locator(selector).first
                if btn.is_visible():
                    print(f"   ✓ Found add button: {selector}")
                    btn.click()
                    page.wait_for_timeout(2000)
                    button_clicked = True
                    break
            except:
                continue

        # メニューから「ファイルをアップロード」等を選択
        if button_clicked:
            upload_menu_selectors = [
                'text="ファイルをアップロード"',
                'text="画像をアップロード"',
                'text="Upload file"',
                'text="Upload image"',
                '[role="menuitem"]:has-text("アップロード")',
                '[role="menuitem"]:has-text("Upload")',
                '[class*="menu"] *:has-text("アップロード")',
            ]

            for selector in upload_menu_selectors:
                try:
                    item = page.locator(selector).first
                    if item.is_visible():
                        print(f"   ✓ Found upload menu: {selector}")
                        item.click()
                        page.wait_for_timeout(1500)
                        break
                except:
                    continue

        # ファイル入力を探す（隠し要素の場合も対応）
        file_input = None

        # file inputのセレクタを複数試す
        file_input_selectors = [
            'input[type="file"]',
            'input[accept*="image"]',
            'input[accept*="*"]',
        ]

        # 最大3回試行
        for attempt in range(3):
            for selector in file_input_selectors:
                try:
                    locator = page.locator(selector)
                    count = locator.count()
                    if count > 0:
                        file_input = locator.first
                        print(f"   ✓ Found file input: {selector} (count: {count})")
                        break
                except:
                    continue
            if file_input:
                break
            page.wait_for_timeout(1000)

        if not file_input:
            print("❌ Could not find file upload mechanism")
            print("   Try using --show-browser to debug")
            context.close()
            playwright.stop()
            return {"success": False, "yaml": "", "error": "Upload button not found"}

        # Step 2: 画像をアップロード（file chooserイベント使用）
        print(f"   → Uploading image: {image_file.name}...")
        try:
            # file chooserイベントを待機しながらクリック
            with page.expect_file_chooser(timeout=10000) as fc_info:
                # 隠しinputの場合はdispatch_eventを使う
                file_input.dispatch_event('click')
            file_chooser = fc_info.value
            file_chooser.set_files(str(image_file.absolute()))
            print("   ✓ File uploaded via file chooser")
        except Exception as e:
            print(f"   → File chooser method failed: {e}")
            # 直接set_input_filesを試す
            try:
                file_input.set_input_files(str(image_file.absolute()))
                print("   ✓ File uploaded via set_input_files")
            except Exception as e2:
                print(f"❌ Upload failed: {e2}")
                context.close()
                playwright.stop()
                return {"success": False, "yaml": "", "error": f"Upload failed: {e2}"}

        page.wait_for_timeout(3000)

        # アップロード完了を確認
        print("   → Waiting for upload to complete...")
        page.wait_for_timeout(2000)

        # Step 3: 分析プロンプトを入力
        print("   → Entering analysis prompt...")
        input_selectors = [
            'div[contenteditable="true"]',
            'textarea',
            'rich-textarea textarea',
        ]

        input_element = None
        for selector in input_selectors:
            try:
                elem = page.locator(selector).first
                if elem.is_visible():
                    input_element = elem
                    break
            except:
                continue

        if not input_element:
            print("❌ Could not find input field")
            context.close()
            playwright.stop()
            return {"success": False, "yaml": "", "error": "Input field not found"}

        input_element.click()
        StealthUtils.random_delay(200, 400)
        input_element.fill(EXTRACTION_PROMPT)
        page.wait_for_timeout(500)

        # Step 4: 送信
        print("   → Sending request...")
        send_selectors = [
            'button[aria-label*="送信"]',
            'button[aria-label*="Send"]',
            'button.send-button',
        ]

        send_button = None
        for selector in send_selectors:
            try:
                btn = page.locator(selector).first
                if btn.is_visible():
                    send_button = btn
                    break
            except:
                continue

        if send_button:
            send_button.click()
        else:
            input_element.press("Enter")

        # Step 5: 応答を待つ
        print(f"   → Waiting for analysis (max {timeout}s)...")

        response_text = ""
        start_time = time.time()
        last_response_length = 0
        stable_count = 0

        while time.time() - start_time < timeout:
            elapsed = int(time.time() - start_time)

            # 応答要素を探す
            response_selectors = [
                'model-response',
                '[class*="response"]',
                '[class*="message-content"]',
            ]

            for selector in response_selectors:
                try:
                    elements = page.locator(selector).all()
                    if elements:
                        # 最後の応答を取得
                        last_elem = elements[-1]
                        response_text = last_elem.inner_text()
                        break
                except:
                    continue

            # YAMLが含まれているか確認
            if 'visual_analysis:' in response_text or '```yaml' in response_text:
                # 応答が安定したか確認（3秒間変化なし）
                if len(response_text) == last_response_length:
                    stable_count += 1
                    if stable_count >= 3:
                        print("   ✓ Analysis complete!")
                        break
                else:
                    stable_count = 0
                    last_response_length = len(response_text)

            if elapsed % 15 == 0 and elapsed > 0:
                print(f"      ... {elapsed}s elapsed")

            page.wait_for_timeout(1000)

        context.close()
        playwright.stop()

        if not response_text:
            return {"success": False, "yaml": "", "error": "No response received"}

        # YAMLを抽出
        yaml_content = extract_yaml_from_response(response_text)

        if not yaml_content:
            return {"success": False, "yaml": "", "error": "Could not extract YAML from response"}

        # 出力ファイルに保存
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(yaml_content, encoding='utf-8')
            print(f"   ✓ YAML saved to: {output_path}")

        print(f"\n✓ Visual analysis complete!")
        return {"success": True, "yaml": yaml_content, "error": ""}

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if context:
            context.close()
        if playwright:
            playwright.stop()
        return {"success": False, "yaml": "", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Extract visual elements from reference image")
    parser.add_argument(
        "--image",
        required=True,
        help="Path to reference image"
    )
    parser.add_argument(
        "--output",
        help="Output YAML file path"
    )
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Show browser window for debugging"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Maximum wait time in seconds (default: 120)"
    )

    args = parser.parse_args()

    # 認証チェック
    if not check_authenticated():
        print("❌ Not authenticated")
        print("   Run: python scripts/run.py auth_manager.py setup")
        return 1

    # 抽出実行
    result = extract_visual_prompt(
        image_path=args.image,
        output_path=args.output,
        show_browser=args.show_browser,
        timeout=args.timeout
    )

    if result["success"]:
        print("\n" + "="*50)
        print("Extracted YAML:")
        print("="*50)
        print(result["yaml"])
        return 0
    else:
        print(f"\n❌ Failed: {result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
