#!/usr/bin/env python3
"""
AI顧問サービス ファーストビュー画像生成スクリプト

LP用のヒーロー画像をGeminiで生成します。

Usage:
    cd /Users/tonodukaren/Programming/AI/02_Workspace/05_Client/03_Sun/ALA28/.claude/skills/gemini-image-generator
    python scripts/run.py ../generate_ala48_first_view.py
"""

import sys
from pathlib import Path

# Add scripts to path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from image_generator import generate_image, check_authenticated

def main():
    # 認証チェック
    if not check_authenticated():
        print("❌ 認証されていません")
        print("   実行: python scripts/run.py auth_manager.py setup")
        return 1

    # ファーストビュー用プロンプト（日本語）
    prompt = """以下の画像を生成してください:

日本のビジネスランディングページ用の高品質なヒーロー画像

【シーン設定】
- 40代の自信に満ちた日本人男性経営者
- スマートカジュアルな白いシャツを着用
- モダンでクリーンなオフィス環境（背景はぼかし）
- AIやテクノロジーを象徴する要素（青い光、デジタルグラフィック）

【構図】
- 正面やや斜めから
- 上半身のショット
- 視線はカメラに向ける
- 明るく前向きな表情

【カラーパレット】
- 主要色: 信頼感のある青（#3B82F6系）
- 背景: 白・ライトグレーのグラデーション
- アクセント: テクノロジーを表す青い光

【イメージスタイル】
- プロフェッショナルで信頼感がある
- 現代的でテクノロジー先進的
- 親しみやすさと専門性のバランス
- ランディングページの右側に配置する想定

テキストは入れないでください。人物メインの画像にしてください。"""

    output_path = "/Users/tonodukaren/Programming/AI/02_Workspace/05_Client/03_Sun/ALA28/test/ai_komon_service/images/first_view_hero.png"

    print("=" * 60)
    print("AI顧問サービス ファーストビュー画像生成")
    print("=" * 60)

    success = generate_image(
        prompt=prompt,
        output_path=output_path,
        show_browser=False,
        timeout=300
    )

    if success:
        print(f"\n✅ ファーストビュー画像を生成しました")
        print(f"   出力: {output_path}")
        return 0
    else:
        print(f"\n❌ 画像生成に失敗しました")
        return 1

if __name__ == "__main__":
    sys.exit(main())
