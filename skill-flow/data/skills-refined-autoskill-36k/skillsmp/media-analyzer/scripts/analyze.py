#!/usr/bin/env python3
"""
Media Analyzer - Gemini API を使用した音楽・動画ファイル解析スクリプト
"""

import argparse
import base64
import mimetypes
import os
import sys
import tempfile
import urllib.request
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai パッケージが必要です")
    print("インストール: pip install google-genai")
    sys.exit(1)


# サポートするメディアタイプ
SUPPORTED_AUDIO = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'}
SUPPORTED_VIDEO = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.wmv', '.flv'}
SUPPORTED_IMAGE = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
SUPPORTED_MEDIA = SUPPORTED_AUDIO | SUPPORTED_VIDEO | SUPPORTED_IMAGE

# デフォルトプロンプト
DEFAULT_AUDIO_PROMPT = """
この音声/音楽ファイルを詳しく解析してください。以下の観点から分析をお願いします：

1. **ジャンル・スタイル**: どのような音楽ジャンルか
2. **テンポ・リズム**: BPM、リズムパターンの特徴
3. **楽器構成**: 使用されている楽器や音源
4. **雰囲気・ムード**: 曲が持つ感情的な印象
5. **構成**: イントロ、サビなどの構造
6. **特徴的な要素**: 特筆すべき音楽的特徴
7. **類似アーティスト/曲**: 似ている音楽があれば

分析結果を日本語で詳しく説明してください。
"""

DEFAULT_VIDEO_PROMPT = """
この動画ファイルを詳しく解析してください。以下の観点から分析をお願いします：

1. **内容概要**: 動画の主な内容
2. **映像特徴**: 画質、カメラワーク、編集スタイル
3. **音声要素**: BGM、効果音、ナレーションの有無と特徴
4. **雰囲気**: 動画全体の印象
5. **技術的特徴**: 特殊効果やアニメーションなど
6. **ターゲット**: 想定される視聴者層

分析結果を日本語で詳しく説明してください。
"""

DEFAULT_IMAGE_PROMPT = """
この画像を詳しく見て、自然な言葉で感想を述べてください。

堅苦しい箇条書きではなく、友達と画像を見ながら話すような感覚で：
- 画像に何が描かれている/写っているか
- 印象的な部分、目を引くポイント
- 雰囲気や感情的な印象
- イラストなら絵柄やキャラクターの特徴
- 写真なら構図や光の具合

ポイント：
- 機械的な分析ではなく、人間らしい感想として
- 「〜が描かれています」より「〜だね」「〜って感じ」のような親しみやすい口調で
- 相手が見せてくれた画像に興味を持って見ている感覚で
"""


def get_mime_type(file_path: str) -> str:
    """ファイルのMIMEタイプを取得"""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        ext = Path(file_path).suffix.lower()
        mime_map = {
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.aac': 'audio/aac',
            '.flac': 'audio/flac',
            '.ogg': 'audio/ogg',
            '.m4a': 'audio/mp4',
            '.wma': 'audio/x-ms-wma',
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.mkv': 'video/x-matroska',
            '.webm': 'video/webm',
            '.wmv': 'video/x-ms-wmv',
            '.flv': 'video/x-flv',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.bmp': 'image/bmp',
            '.tiff': 'image/tiff',
        }
        mime_type = mime_map.get(ext, 'application/octet-stream')
    return mime_type


def is_url(path: str) -> bool:
    """URLかどうかを判定"""
    return path.startswith(('http://', 'https://'))


def download_file(url: str, verbose: bool = False) -> str:
    """URLからファイルをダウンロード"""
    if verbose:
        print(f"ダウンロード中: {url}")

    # ファイル名を取得
    filename = url.split('/')[-1].split('?')[0]
    if not filename:
        filename = 'downloaded_media'

    # 拡張子を確認
    ext = Path(filename).suffix.lower()
    if not ext:
        ext = '.mp4'  # デフォルト
        filename += ext

    # 一時ファイルに保存
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, filename)

    try:
        # User-Agentを設定してDiscord CDNに対応
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MediaAnalyzer/1.0)',
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(temp_path, 'wb') as f:
                f.write(response.read())
        if verbose:
            print(f"ダウンロード完了: {temp_path}")
        return temp_path
    except Exception as e:
        raise Exception(f"ダウンロードエラー: {e}")


def read_file_as_base64(file_path: str) -> str:
    """ファイルをBase64エンコード"""
    with open(file_path, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8')


def analyze_media(
    file_path: str,
    prompt: str = None,
    verbose: bool = False,
    model: str = "gemini-3-flash-preview"
) -> str:
    """
    メディアファイルを解析

    Args:
        file_path: ファイルパスまたはURL
        prompt: カスタムプロンプト（Noneの場合はデフォルト使用）
        verbose: 詳細出力モード
        model: 使用するGeminiモデル

    Returns:
        解析結果テキスト
    """
    # API キー確認
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 環境変数を設定してください")

    # URLの場合はダウンロード
    temp_file = None
    if is_url(file_path):
        temp_file = download_file(file_path, verbose)
        file_path = temp_file

    # ファイル存在確認
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    # ファイルタイプ確認
    ext = Path(file_path).suffix.lower()
    if ext not in SUPPORTED_MEDIA:
        raise ValueError(f"サポートされていないファイル形式: {ext}")

    is_audio = ext in SUPPORTED_AUDIO
    is_image = ext in SUPPORTED_IMAGE
    mime_type = get_mime_type(file_path)

    if verbose:
        file_size = os.path.getsize(file_path)
        print(f"ファイル: {file_path}")
        print(f"タイプ: {mime_type}")
        print(f"サイズ: {file_size / 1024 / 1024:.2f} MB")

    # デフォルトプロンプト設定
    if prompt is None:
        if is_audio:
            prompt = DEFAULT_AUDIO_PROMPT
        elif is_image:
            prompt = DEFAULT_IMAGE_PROMPT
        else:
            prompt = DEFAULT_VIDEO_PROMPT

    # Gemini クライアント初期化
    client = genai.Client(api_key=api_key)

    # ファイルをBase64エンコード
    if verbose:
        print("ファイルをエンコード中...")

    file_data = read_file_as_base64(file_path)

    # コンテンツ作成
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    data=base64.standard_b64decode(file_data),
                    mime_type=mime_type
                ),
                types.Part.from_text(text=prompt),
            ],
        ),
    ]

    # 生成設定（Google検索は無効 - メディア解析には不要でAPIコールが増える）
    generate_content_config = types.GenerateContentConfig(
        # thinking_levelはデフォルト（MEDIUM）を使用
    )

    if verbose:
        print("Gemini API に送信中...")
        print("-" * 50)

    # ストリーミングで結果を取得
    result_text = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                if verbose:
                    print(chunk.text, end="", flush=True)
                result_text += chunk.text
    except Exception as e:
        raise Exception(f"API エラー: {e}")
    finally:
        # 一時ファイルの削除
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)

    if verbose:
        print("\n" + "-" * 50)

    return result_text


def main():
    parser = argparse.ArgumentParser(
        description="Gemini API を使用してメディアファイルを解析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s audio.mp3                      # ローカルファイルを解析
  %(prog)s https://example.com/video.mp4  # URLから解析
  %(prog)s file.mp3 --prompt "曲の雰囲気を教えて"  # カスタムプロンプト
  %(prog)s file.mp4 --verbose             # 詳細モード
        """
    )

    parser.add_argument(
        'file',
        help='解析するファイルパスまたはURL'
    )
    parser.add_argument(
        '--prompt', '-p',
        help='カスタム解析プロンプト'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='詳細出力モード'
    )
    parser.add_argument(
        '--model', '-m',
        default='gemini-3-flash-preview',
        help='使用するGeminiモデル (デフォルト: gemini-3-flash-preview)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='JSON形式で出力'
    )

    args = parser.parse_args()

    try:
        # ヘッダー出力
        if not args.json:
            print("=" * 50)
            print("メディア解析 (Gemini API)")
            print("=" * 50)
            print()

        # 解析実行
        result = analyze_media(
            file_path=args.file,
            prompt=args.prompt,
            verbose=args.verbose,
            model=args.model
        )

        # 結果出力
        if args.json:
            import json
            output = {
                "file": args.file,
                "result": result,
                "model": args.model
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            if not args.verbose:
                print(result)
            print()
            print("=" * 50)
            print("解析完了")
            print("=" * 50)

    except FileNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
