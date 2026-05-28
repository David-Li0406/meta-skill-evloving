# md2html2pptx

Markdown → HTML → PowerPoint 変換ツール

## インストール

このスキルをAIコーディングアシスタントで使用するには、以下の場所に配置してください:

| ツール | 配置先 |
|--------|--------|
| **Claude Code** | `~/.claude/skills/md2html2pptx/`（グローバル） |
| **GitHub Copilot** |  |
| **Codex CLI** |  |
| **Cursor** |  |

```bash
# Claude Code (グローバル)
mkdir -p ~/.claude/skills
cp -r md2html2pptx ~/.claude/skills/
```

## クイックスタート

### 1. セットアップ

```
/md2html2pptx setup
```

これで以下が自動的に行われます:
- フォルダ作成 (`1_mds/`, `2_htmls/`, `3_pptxs/`)
- `package.json` 生成
- 依存パッケージのインストール

### 2. Markdownを書く

`1_mds/` フォルダにMarkdownファイルを作成:

```markdown
## PART 1: プレゼンテーション入門
- 副題: サブタイトル

## 1.1: 概要
- リスト:
  - ポイント1
  - ポイント2
  - ポイント3

## 1.2: 3つの機能
- カード1: 機能A
  - 説明1
  - 説明2
- カード2: 機能B
  - 説明1
  - 説明2
- カード3: 機能C
  - 説明1
  - 説明2
```

### 3. HTMLスライドを生成

```
/md2html2pptx to_html 1_mds/example.md
```

内部で以下のコマンドが実行されます:
```bash
npm run to_html -- 1_mds/example.md
```

### 4. プレビュー

```
/md2html2pptx preview
```

内部で以下のコマンドが実行されます:
```bash
npm run preview
```

ブラウザでスライドを確認。矢印キーでページ送り。

### 5. PowerPointを生成

```
/md2html2pptx to_pptx
```

`3_pptxs/presentation.pptx` が生成されます。

## コマンド一覧

| コマンド | 説明 |
|----------|------|
| `/md2html2pptx setup` | 初期セットアップ |
| `/md2html2pptx to_html <file>` | MarkdownからHTMLスライドを生成 |
| `/md2html2pptx preview` | ブラウザでプレビュー |
| `/md2html2pptx to_pptx [filter]` | HTMLからPowerPointを生成 |

## Markdown記法

### 基本記法

| 記法 | 説明 |
|------|------|
| `## セクション: タイトル` | スライド定義（例: `## 1.1: 概要`） |
| `## PART N: タイトル` | タイトルスライド（ダーク背景） |
| `- 副題: テキスト` | タイトルスライドの副題 |

### コンテンツ記法

| 記法 | 説明 |
|------|------|
| `- リスト:` + 子項目 | 箇条書きリスト（ネスト対応） |
| `- カードN: 名前` + 子項目 | カードレイアウト（1〜4枚） |
| `- ステップN: ラベル` + 子項目 | ステップ形式（番号付き） |
| `- テーブル:` + マークダウン表 | 比較表 |
| `- フロー:` + 子項目 | 横並びフロー図 |
| `- Good: ラベル` + 子項目 | 推奨カード（緑） |
| `- Bad: ラベル` + 子項目 | 非推奨カード（赤） |

### コードとダイアグラム

| 記法 | 説明 |
|------|------|
| `- コード:` + コードブロック | シンタックスハイライト付きコード |
| `- Mermaid:` + mermaidコードブロック | Mermaidダイアグラム |
| ` ```言語 ` + コード + ` ``` ` | 直接コードブロック |

### 複合レイアウト

| 記法 | 説明 |
|------|------|
| `- 複合: 1:2` | 左1列、右2列のグリッドレイアウト |
| `- 複合: 2:1` | 左2列、右1列のグリッドレイアウト |
| `- 複合: 2:2` | 2x2グリッドレイアウト |
| `- layout: vertical` | 縦並びレイアウト（ステップ用） |

## スライドタイプ

| タイプ | トリガー | 説明 |
|-------|---------|------|
| `title` | `## PART N: タイトル` | ダーク背景のタイトルスライド |
| `bulletList` | `- リスト:` | 箇条書きリスト（3階層まで対応） |
| `cards` | `- カードN:` | カードレイアウト（自動幅計算） |
| `goodBad` | `- Good:` / `- Bad:` | 比較カード（推奨/非推奨） |
| `steps` | `- ステップN:` | ステップ形式（番号付き） |
| `table` | `- テーブル:` + マークダウン表 | 比較表 |
| `flow` | `- フロー:` | 横並びフロー図 |
| `code` | `- コード:` + コードブロック | シンタックスハイライト付きコード |
| `mermaid` | `- Mermaid:` + mermaidブロック | Mermaidダイアグラム（PNG変換） |
| `composite` | `- 複合: N:M` | グリッドレイアウト |

## 使用例

### 箇条書きリスト（ネスト対応）

```markdown
## 1.1: 概要
- リスト:
  - 第1階層
    - 第2階層
      - 第3階層
  - 別の項目
```

### カードレイアウト

```markdown
## 1.2: 3つの機能
- カード1: 機能A
  - 説明1
  - 説明2
- カード2: 機能B
  - 説明1
- カード3: 機能C
  - 説明1
```

### Good/Bad 比較

```markdown
## 1.3: コーディング規約
- Good: 推奨
  - 明確な変数名
  - 一貫したスタイル
- Bad: 非推奨
  - 略語の多用
  - 混在したスタイル
```

### コードブロック

```markdown
## 1.4: TypeScriptの例

` ``typescript
interface User {
  id: number;
  name: string;
}
` ``
```

### Mermaidダイアグラム

```markdown
## 1.5: システム構成
- Mermaid:

` ``mermaid
flowchart TD
    A[フロントエンド] --> B[バックエンド]
    B --> C[(データベース)]
` ``
```

### 複合レイアウト

```markdown
## 1.6: 比較と図
- 複合: 1:2
  - Good: 推奨
    - 明確な設計
  - Bad: 非推奨
    - 曖昧な設計
  - Mermaid:

` ``mermaid
flowchart LR
    A --> B --> C
` ``
```

## フォルダ構成

```
project/
├── 1_mds/    # Markdownソース
├── 2_htmls/  # 生成されたHTMLスライド
└── 3_pptxs/  # 生成されたPowerPoint
```

## Tips

- Markdown記法に従えば決定論的にHTMLが生成される
- HTMLは960x540px（16:9）で設計されている
- 複数パートに分けて生成可能: `/md2html2pptx to_pptx part1`
- 生成後のHTMLは手動編集も可能
- Mermaidダイアグラムは自動的にPNG画像に変換されPPTXに埋め込まれる
- コードブロックはHighlight.jsによるシンタックスハイライトが適用される

## ライセンス

MIT
