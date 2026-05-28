<div align="center">

# Gemini Image Generator

**Google Gemini (Imagen 3) で画像を生成する Claude Code スキル**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](https://www.anthropic.com/news/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Google Gemini の Imagen 3 モデルを使用して、Claude Code から直接高品質なAI画像を生成。一度Googleにログインすれば、シンプルなプロンプトで画像生成が可能です。

[インストール](#インストール) • [クイックスタート](#クイックスタート) • [使い方](#使い方) • [仕組み](#仕組み)

</div>

---

## 機能

- **Imagen 3 画像生成** - Googleの最新画像生成モデルにアクセス
- **永続認証** - 一度ログインすれば、Cookieが期限切れになるまで有効（約7日間）
- **自動環境セットアップ** - 仮想環境と依存関係を自動管理
- **ブラウザ自動化** - 実績のある [NotebookLM スキル](https://github.com/PleasePrompto/notebooklm-skill) のパターンを採用
- **人間らしい操作** - 検出防止機能により安定した動作

---

## 重要：ローカル Claude Code のみ対応

**このスキルはローカルの [Claude Code](https://github.com/anthropics/claude-code) インストールでのみ動作します。Web UIでは使用できません。**

Web UIはスキルをサンドボックスで実行するため、このスキルに必要なネットワークアクセスが制限されます。

---

## インストール

### オプション1：ユーザースキルディレクトリにインストール（推奨）

```bash
# スキルディレクトリを作成
mkdir -p ~/.claude/skills

# このリポジトリをクローン
cd ~/.claude/skills
git clone https://github.com/RenTonoduka/NanobananaPro-skill.git gemini-image-generator
```

### オプション2：プロジェクトスキルディレクトリにインストール

```bash
# プロジェクトルートで実行
mkdir -p .claude/skills

# このリポジトリをクローン
cd .claude/skills
git clone https://github.com/RenTonoduka/NanobananaPro-skill.git gemini-image-generator
```

### インストール確認

Claude Code で以下を入力：
```
「使えるスキルを教えて」
```

Claude が Gemini Image Generator を含む利用可能なスキル一覧を表示します。

---

## クイックスタート

### 1. Googleで認証（初回のみ）

```
「Gemini の認証をセットアップして」
```

Chromeウィンドウが開く → Googleアカウントでログイン → 認証情報が保存されます。

### 2. 画像を生成

```
「山の上の夕日の画像を生成して」
```

出力先を指定する場合：
```
「未来的なロボットの画像を生成して robot.png に保存して」
```

---

## 使い方

### 認証状態の確認

```bash
python scripts/run.py auth_manager.py status
```

出力例：
```
✓ Authenticated
  Session age: 2.5 hours
  Total cookies: 51
  Google auth cookies: 27
```

### 認証（必要な場合）

```bash
python scripts/run.py auth_manager.py setup
```

### 画像生成

```bash
# 基本的な生成
python scripts/run.py image_generator.py --prompt "窓辺に座るかわいい猫"

# 出力パスを指定
python scripts/run.py image_generator.py --prompt "夜のサイバーパンク都市" --output images/city.png

# ブラウザを表示（デバッグ用）
python scripts/run.py image_generator.py --prompt "..." --show-browser

# タイムアウトを変更
python scripts/run.py image_generator.py --prompt "..." --timeout 300
```

### パラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|-----------|------|---------|-------------|
| `--prompt` | はい | - | 画像生成プロンプト |
| `--output` | いいえ | `output/generated_image.png` | 出力ファイルパス |
| `--show-browser` | いいえ | False | ブラウザウィンドウを表示 |
| `--timeout` | いいえ | 180 | 最大待機時間（秒） |

---

## 仕組み

### 認証フロー

1. `accounts.google.com` を開いてGoogleログイン
2. ログイン完了を待機（`myaccount.google.com` へのリダイレクト）
3. Gemini に移動して全Cookieを取得
4. 51個のCookie（うち27個がGoogle認証Cookie）を `state.json` に保存
5. 以降の実行ではCookieを自動で注入

### 画像生成フロー

1. Gemini (`gemini.google.com`) を開く
2. **「ツール」** ボタンをクリック
3. **「画像を作成」** オプションを選択
4. プロンプトを入力して送信
5. Imagen 3 が画像を生成するのを待機
6. 画像をダウンロードして保存

### アーキテクチャ

```
NanobananaPro-skill/
├── SKILL.md              # Claude Code 用の指示
├── README.md             # 英語版ドキュメント
├── README.ja.md          # 日本語版ドキュメント（このファイル）
├── LICENSE               # MIT ライセンス
├── requirements.txt      # Python 依存関係
├── scripts/
│   ├── run.py            # ラッパースクリプト（venv自動管理）
│   ├── config.py         # 設定の一元管理
│   ├── browser_utils.py  # ブラウザファクトリとステルス機能
│   ├── auth_manager.py   # Google認証管理
│   └── image_generator.py # 画像生成ロジック
├── data/                 # 認証データ（自動作成、gitignore対象）
└── output/               # 生成画像（gitignore対象）
```

---

## プロンプトのガイドライン

### 良いプロンプト例

```
「雪をかぶった山々の上の穏やかな夕日、暖かいオレンジ色の空」
「窓辺に座る猫の水彩画、柔らかな光」
「清潔な白いデスクの上のノートパソコンのプロ仕様の製品写真」
「ネオンライトと雨が降る夜のサイバーパンク都市」
```

### 避けるべきこと

- 曖昧なプロンプト：「何かいい感じのもの」
- 不適切なコンテンツ（Geminiが拒否します）
- 著作権キャラクターや商標コンテンツ

---

## トラブルシューティング

| 問題 | 解決方法 |
|---------|----------|
| 「Not authenticated」 | `auth_manager.py setup` を実行 |
| ModuleNotFoundError | 必ず `run.py` ラッパーを使用 |
| タイムアウト | `--timeout 300` で延長 |
| 「Could not find tool button」 | UIが変更された可能性、`--show-browser` で確認 |
| 生成が拒否された | プロンプトを修正（制限コンテンツを避ける） |

### クリアして再スタート

```bash
python scripts/run.py auth_manager.py clear
python scripts/run.py auth_manager.py setup
```

---

## 他のプロジェクトでの使用方法

### 方法1：シンボリックリンク（推奨）

```bash
# ユーザーディレクトリに一度インストール
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/RenTonoduka/NanobananaPro-skill.git gemini-image-generator

# 他のプロジェクトでシンボリックリンクを作成
cd /path/to/your/project
mkdir -p .claude/skills
ln -s ~/.claude/skills/gemini-image-generator .claude/skills/
```

### 方法2：Git サブモジュール

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git submodule add https://github.com/RenTonoduka/NanobananaPro-skill.git .claude/skills/gemini-image-generator
```

### 方法3：直接クローン

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git clone https://github.com/RenTonoduka/NanobananaPro-skill.git .claude/skills/gemini-image-generator
```

---

## 制限事項

- **生成時間：** 画像1枚あたり30〜180秒
- **ブラウザ自動化：** GeminiのUI変更で動作しなくなる可能性
- **認証：** 初回は手動でGoogleログインが必要
- **コンテンツポリシー：** Geminiが特定のプロンプトを拒否する場合あり
- **レート制限：** Googleアカウントの制限に従う
- **バッチ処理なし：** 1コマンドにつき1画像
- **ローカルのみ：** Claude Code Web UIでは動作しない

---

## セキュリティに関する注意

- 認証データは `data/` ディレクトリにローカル保存
- すべての機密ファイルは `.gitignore` で除外
- より信頼性の高い動作のため実際のChromeブラウザを使用
- `data/` ディレクトリの内容は絶対にコミットしないでください

---

## クレジット

[NotebookLM スキル](https://github.com/PleasePrompto/notebooklm-skill) の認証パターンを参考にしています。

---

## ライセンス

MIT ライセンス - 詳細は [LICENSE](LICENSE) を参照してください。

---

<div align="center">

**Claude Code から直接AIで画像を生成**

[問題を報告](https://github.com/RenTonoduka/NanobananaPro-skill/issues) • [機能をリクエスト](https://github.com/RenTonoduka/NanobananaPro-skill/issues)

</div>
