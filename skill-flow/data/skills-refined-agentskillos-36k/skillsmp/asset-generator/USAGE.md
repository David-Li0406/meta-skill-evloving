# Asset Generator 詳細ガイド

## 目次

1. [セットアップ](#セットアップ)
2. [基本的な使い方](#基本的な使い方)
3. [プロンプト作成ガイド](#プロンプト作成ガイド)
4. [用途別プロンプト例](#用途別プロンプト例)
5. [トラブルシューティング](#トラブルシューティング)

---

## セットアップ

### 1. APIキーの取得

1. [Google AI Studio](https://aistudio.google.com/apikey) にアクセス
2. Googleアカウントでログイン
3. 「Create API Key」をクリック
4. 生成されたAPIキーをコピー

### 2. APIキーの設定

**方法1: 設定ファイル（推奨）**

```bash
mkdir -p ~/.gemini
echo '{"api_key": "YOUR_API_KEY_HERE"}' > ~/.gemini/config
chmod 600 ~/.gemini/config
```

**方法2: 環境変数**

```bash
export GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 3. 動作確認

```bash
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  --prompt "simple test icon" \
  --output /tmp/test.png
```

---

## 基本的な使い方

### コマンド構文

```bash
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- [オプション]
```

### 必須オプション

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--prompt` | `-p` | 画像生成プロンプト |
| `--output` | `-o` | 出力ファイルパス |

### オプション

| オプション | 短縮 | デフォルト | 説明 |
|-----------|------|-----------|------|
| `--aspect-ratio` | `-a` | `1:1` | アスペクト比 |
| `--model` | `-m` | `gemini-2.0-flash-preview-image-generation` | 使用モデル |

### アスペクト比

| 値 | 用途 |
|-----|------|
| `1:1` | アイコン、アバター、プロフィール画像 |
| `16:9` | バナー、OGP画像、YouTubeサムネイル |
| `9:16` | ストーリー、モバイル壁紙 |
| `4:3` | 標準サムネイル |
| `3:4` | ポートレート画像 |

---

## プロンプト作成ガイド

### 効果的なプロンプトの構造

```
[主題] + [スタイル] + [色] + [背景] + [追加詳細]
```

### スタイルキーワード

| カテゴリ | キーワード例 |
|---------|------------|
| デザインスタイル | flat design, minimalist, isometric, 3D render, pixel art |
| アートスタイル | watercolor, oil painting, digital art, vector art, sketch |
| 雰囲気 | modern, vintage, futuristic, playful, professional |

### 色指定

| 表現方法 | 例 |
|---------|---|
| 具体的な色 | blue, red, purple |
| グラデーション | blue to purple gradient |
| カラーパレット | pastel colors, vibrant colors, muted colors |
| ブランドカラー | tech blue, startup green |

### 背景指定

| キーワード | 効果 |
|-----------|------|
| white background | 白背景 |
| transparent background | 透明背景（対応している場合） |
| gradient background | グラデーション背景 |
| abstract background | 抽象的な背景 |

---

## 用途別プロンプト例

### アプリアイコン

```bash
# シンプルなアイコン
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "minimalist app icon, single geometric shape, blue gradient, white background, flat design" \
  -o ./app-icon.png

# 3Dスタイルアイコン
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "3D rendered app icon, glossy sphere with lightning bolt, purple and blue, soft shadow" \
  -o ./app-icon-3d.png
```

### Webサイトバナー

```bash
# ヒーローバナー
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "modern website hero banner, abstract tech shapes, flowing lines, dark blue to purple gradient" \
  -o ./hero-banner.png -a 16:9

# プロモーションバナー
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "sale promotion banner, bold typography space, vibrant orange and white, dynamic shapes" \
  -o ./promo-banner.png -a 16:9
```

### OGP/SNS画像

```bash
# ブログ記事OGP
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "blog article OGP image, clean layout with text space on left, abstract illustration on right, professional blue theme" \
  -o ./blog-ogp.png -a 16:9

# Twitter/X投稿画像
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "tech announcement graphic, futuristic design, glowing elements, dark background, space for headline" \
  -o ./twitter-card.png -a 16:9
```

### イラスト・装飾

```bash
# セクション区切り
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "decorative wave divider, flowing curves, gradient from blue to teal, minimal design" \
  -o ./divider.png -a 16:9

# 背景パターン
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "subtle geometric pattern, repeating triangles, light gray on white, minimal opacity" \
  -o ./pattern.png
```

### プロフィール・アバター

```bash
# キャラクターアバター
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "friendly cartoon avatar, developer character with headphones, simple illustration, warm colors" \
  -o ./avatar.png

# 抽象的なプロフィール
uv run --script ~/.claude/skills/asset-generator/scripts/generate_image.py -- \
  -p "abstract profile picture, geometric face made of polygons, colorful gradient, modern art style" \
  -o ./profile.png
```

---

## トラブルシューティング

### エラー: APIキーが見つかりません

**原因**: APIキーが設定されていない

**解決策**:
```bash
# 設定ファイルを確認
cat ~/.gemini/config

# 環境変数を確認
echo $GEMINI_API_KEY
```

### エラー: API制限に達しました

**原因**: Gemini APIのレート制限

**解決策**:
- 数分待ってから再試行
- 無料枠の場合、1日の制限をを確認

### エラー: 無効なリクエスト

**原因**: プロンプトがポリシーに違反、または形式が不正

**解決策**:
- プロンプトを見直す
- 著作権のあるキャラクター名を避ける
- センシティブなコンテンツを避ける

### エラー: 画像データが含まれていません

**原因**: モデルがテキストのみを返した

**解決策**:
- より具体的なプロンプトを試す
- 「generate an image of」などの明示的な指示を追加

### 画像の品質が低い

**解決策**:
- より詳細なプロンプトを使用
- スタイルを明示的に指定
- 「high quality」「detailed」などのキーワードを追加

---

## 参考リンク

- [Gemini API Image Generation Documentation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Google GenAI Python SDK](https://googleapis.github.io/python-genai/)
- [Google AI Studio](https://aistudio.google.com/)
