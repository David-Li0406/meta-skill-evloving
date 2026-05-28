#!/usr/bin/env python3
"""
Code Review Generation Script

指定されたファイルを対象に、テンプレートベースのコードレビューを生成します。

使用方法:
    python3 generate_review.py <target_file_path> <output_file_path>

パラメータ:
    target_file_path: レビュー対象のファイルパス
    output_file_path: 出力するレビューファイルのパス
"""

import sys
import os


def load_template(template_path: str) -> str:
    """テンプレートファイルを読み込む"""
    if not os.path.exists(template_path):
        print(f"エラー: テンプレートファイルが見つかりません: {template_path}")
        sys.exit(1)
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except IOError as e:
        print(f"エラー: テンプレートファイルの読み込みに失敗しました: {e}")
        sys.exit(1)


def ensure_output_dir(output_file_path: str) -> None:
    """出力先ディレクトリを作成する"""
    output_dir = os.path.dirname(output_file_path)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except IOError as e:
            print(f"エラー: 出力ディレクトリの作成に失敗しました: {e}")
            sys.exit(1)


def write_output(output_file_path: str, content: str) -> None:
    """出力ファイルに内容を書き込む"""
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"レビューファイルを生成しました: {output_file_path}")
    except IOError as e:
        print(f"エラー: 出力ファイルの書き込みに失敗しました: {e}")
        sys.exit(1)


def main():
    """メイン処理"""
    if len(sys.argv) != 3:
        print("使用方法: python3 generate_review.py <target_file_path> <output_file_path>")
        sys.exit(1)

    target_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    template_path = ".claude/skills/readable-code-review/assets/review.md"
    template_content = load_template(template_path)
    output_content = template_content.replace("{対象ファイルパス}", target_file_path)

    ensure_output_dir(output_file_path)
    write_output(output_file_path, output_content)


if __name__ == "__main__":
    main()
