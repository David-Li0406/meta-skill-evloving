---
name: media-analyzer
description: |
  Gemini APIを使用して画像・音楽・動画ファイルを解析するスキル。
  ローカルファイルパスまたはURLを受け取り、AI解析を実行。
  使用トリガー: メディア解析、画像分析、音楽分析、動画分析、Gemini解析
---

# Media Analyzer (Gemini API)

Gemini APIを使用して画像・音楽ファイル・動画ファイルを解析するスキル。

## 必要条件

```bash
# 依存パッケージのインストール
pip install google-genai

# 環境変数設定
export GEMINI_API_KEY="your_api_key"
```

## 使用方法

### ローカルファイルの解析
```bash
python .claude/skills/media-analyzer/scripts/analyze.py /path/to/audio.mp3
python .claude/skills/media-analyzer/scripts/analyze.py /path/to/video.mp4
```

### URLからの解析
```bash
python .claude/skills/media-analyzer/scripts/analyze.py "https://example.com/audio.mp3"
```

### カスタムプロンプトでの解析
```bash
python .claude/skills/media-analyzer/scripts/analyze.py /path/to/file.mp3 --prompt "この曲のジャンルと雰囲気を分析して"
```

### 詳細モード
```bash
python .claude/skills/media-analyzer/scripts/analyze.py /path/to/file.mp4 --verbose
```

## サポートフォーマット

### 画像
- JPG, JPEG, PNG, GIF, WebP, BMP, TIFF

### 音声
- MP3, WAV, AAC, FLAC, OGG, M4A

### 動画
- MP4, AVI, MOV, MKV, WebM

## 出力例

```
=== メディア解析結果 ===
ファイル: example.mp3
タイプ: audio/mpeg

[解析内容]
この曲はテンポの速いエレクトロニックミュージックで...
```

## 環境変数

| 変数名 | 説明 | 必須 |
|--------|------|------|
| GEMINI_API_KEY | Gemini API キー | Yes |

## トラブルシューティング

### API キーエラー
```
export GEMINI_API_KEY="your_key_here"
```

### ファイルサイズ制限
大きなファイルは自動的にチャンク処理されます。
