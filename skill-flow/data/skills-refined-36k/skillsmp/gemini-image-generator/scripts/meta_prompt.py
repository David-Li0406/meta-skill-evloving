#!/usr/bin/env python3
"""
Meta Prompt Generator - YAML分析結果から最適化された画像生成プロンプトを作成

Usage:
    python scripts/run.py meta_prompt.py --yaml analysis.yaml --request "犬を描いて"
    python scripts/run.py meta_prompt.py --yaml-text "style: watercolor..." --request "猫"
"""

import sys
import argparse
import yaml
from pathlib import Path
from typing import Optional


def load_yaml(yaml_path: str = None, yaml_text: str = None) -> dict:
    """
    YAMLファイルまたはテキストから分析結果を読み込む

    Args:
        yaml_path: YAMLファイルのパス
        yaml_text: YAML文字列

    Returns:
        dict: パースされたYAMLデータ
    """
    if yaml_text:
        return yaml.safe_load(yaml_text)
    elif yaml_path:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Either yaml_path or yaml_text must be provided")


def get_nested(data: dict, *keys, default: str = "") -> str:
    """
    ネストされた辞書から値を安全に取得

    Args:
        data: 辞書
        *keys: キーのパス
        default: デフォルト値

    Returns:
        str: 値またはデフォルト値
    """
    result = data
    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return default
    return result if result else default


def generate_meta_prompt(yaml_data: dict, user_request: str) -> str:
    """
    YAML分析結果とユーザーリクエストから最適化されたプロンプトを生成

    Args:
        yaml_data: YAML分析結果
        user_request: ユーザーが描きたいもの

    Returns:
        str: 最適化された画像生成プロンプト
    """
    # visual_analysisがある場合はその中身を使う
    analysis = yaml_data.get('visual_analysis', yaml_data)

    # 各要素を抽出
    style = analysis.get('style', {})
    colors = analysis.get('colors', {})
    composition = analysis.get('composition', {})
    lighting = analysis.get('lighting', {})
    background = analysis.get('background', {})
    additional = analysis.get('additional', {})

    # プロンプトパーツを構築
    parts = []

    # 1. ユーザーリクエスト（主題）
    parts.append(user_request)

    # 2. アートスタイル
    art_style = get_nested(style, 'art_style')
    if art_style:
        parts.append(f"{art_style} style")

    # 3. 雰囲気/ムード
    mood = get_nested(style, 'mood')
    if mood:
        parts.append(f"{mood} mood")

    # 4. 色調
    color_parts = []
    primary = get_nested(colors, 'primary')
    secondary = get_nested(colors, 'secondary')
    overall_tone = get_nested(colors, 'overall_tone')

    if primary:
        color_parts.append(primary)
    if secondary:
        color_parts.append(secondary)
    if overall_tone:
        color_parts.append(f"{overall_tone} tones")

    if color_parts:
        parts.append(", ".join(color_parts) + " color palette")

    # 5. ライティング
    light_type = get_nested(lighting, 'type')
    light_dir = get_nested(lighting, 'direction')
    light_quality = get_nested(lighting, 'quality')

    light_parts = []
    if light_type:
        light_parts.append(light_type)
    if light_dir:
        light_parts.append(f"from {light_dir}")
    if light_quality:
        light_parts.append(f"{light_quality} light")

    if light_parts:
        parts.append(" ".join(light_parts))

    # 6. 構図
    layout = get_nested(composition, 'layout')
    perspective = get_nested(composition, 'perspective')

    if layout:
        parts.append(f"{layout} composition")
    if perspective:
        parts.append(f"{perspective} perspective")

    # 7. 背景
    bg_type = get_nested(background, 'type')
    bg_desc = get_nested(background, 'description')

    if bg_desc:
        parts.append(f"{bg_desc} background")
    elif bg_type:
        parts.append(f"{bg_type} background")

    # 8. テクスチャ/質感
    texture = get_nested(style, 'texture')
    if texture:
        parts.append(f"{texture} texture")

    # 9. 追加エフェクト
    effects = get_nested(additional, 'effects')
    if effects:
        parts.append(effects)

    notable = get_nested(additional, 'notable_features')
    if notable:
        parts.append(notable)

    # 最終プロンプト
    prompt = ", ".join([p for p in parts if p.strip()])

    return prompt


def generate_detailed_prompt(yaml_data: dict, user_request: str) -> str:
    """
    より詳細な説明形式のプロンプトを生成

    Args:
        yaml_data: YAML分析結果
        user_request: ユーザーが描きたいもの

    Returns:
        str: 詳細な画像生成プロンプト
    """
    analysis = yaml_data.get('visual_analysis', yaml_data)

    style = analysis.get('style', {})
    colors = analysis.get('colors', {})
    lighting = analysis.get('lighting', {})
    background = analysis.get('background', {})

    # 構造化された説明を構築
    prompt_parts = []

    # 主題
    prompt_parts.append(f"Create an image of {user_request}")

    # スタイル説明
    art_style = get_nested(style, 'art_style')
    mood = get_nested(style, 'mood')
    if art_style or mood:
        style_desc = f"in {art_style} style" if art_style else ""
        mood_desc = f"with {mood} atmosphere" if mood else ""
        prompt_parts.append(f"{style_desc} {mood_desc}".strip())

    # 色の説明
    primary = get_nested(colors, 'primary')
    overall_tone = get_nested(colors, 'overall_tone')
    if primary or overall_tone:
        color_desc = f"featuring {overall_tone} color palette" if overall_tone else ""
        if primary:
            color_desc += f" with {primary} as the dominant color"
        prompt_parts.append(color_desc.strip())

    # ライティング
    light_type = get_nested(lighting, 'type')
    light_quality = get_nested(lighting, 'quality')
    light_dir = get_nested(lighting, 'direction')
    if light_type or light_quality:
        light_desc = f"{light_quality} {light_type} lighting" if light_quality else f"{light_type} lighting"
        if light_dir:
            light_desc += f" coming from {light_dir}"
        prompt_parts.append(light_desc)

    # 背景
    bg_desc = get_nested(background, 'description')
    if bg_desc:
        prompt_parts.append(f"set against {bg_desc}")

    return ". ".join([p for p in prompt_parts if p.strip()]) + "."


def main():
    parser = argparse.ArgumentParser(
        description="Generate optimized image prompt from YAML analysis"
    )
    parser.add_argument(
        "--yaml",
        help="Path to YAML analysis file"
    )
    parser.add_argument(
        "--yaml-text",
        help="YAML analysis as text string"
    )
    parser.add_argument(
        "--request",
        required=True,
        help="What you want to create (e.g., '犬を描いて', 'a cat')"
    )
    parser.add_argument(
        "--format",
        choices=["simple", "detailed"],
        default="simple",
        help="Prompt format: simple (comma-separated) or detailed (sentences)"
    )
    parser.add_argument(
        "--output",
        help="Output file path for the generated prompt"
    )

    args = parser.parse_args()

    if not args.yaml and not args.yaml_text:
        print("❌ Either --yaml or --yaml-text is required")
        return 1

    try:
        # YAML読み込み
        yaml_data = load_yaml(yaml_path=args.yaml, yaml_text=args.yaml_text)

        # プロンプト生成
        if args.format == "detailed":
            prompt = generate_detailed_prompt(yaml_data, args.request)
        else:
            prompt = generate_meta_prompt(yaml_data, args.request)

        # 出力
        print("\n" + "="*50)
        print("Generated Prompt:")
        print("="*50)
        print(prompt)
        print("="*50 + "\n")

        # ファイルに保存
        if args.output:
            output_file = Path(args.output)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(prompt, encoding='utf-8')
            print(f"✓ Prompt saved to: {args.output}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
