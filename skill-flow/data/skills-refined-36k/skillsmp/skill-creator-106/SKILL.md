---
name: skill-creator
description: |
  Gemini CLI用のスキルを作成・設計するためのガイド。
  Use when: スキル作成, skill作成, 新しいスキル, スキルを作りたい, SKILL.md, スキル設計, スキルの書き方
  Do not use when: 既存スキルの実行, スキルと関係ないタスク
---

# Skill Creator Guide

Gemini CLIで使えるスキルを作成するためのガイド。

## このスキルを使用する時

- 新しいスキルを作りたい
- スキルの構造を理解したい
- 効果的なスキルの書き方を知りたい
- 既存スキルを改善したい

## このスキルを使用しない時

- 既存のスキルを実行する
- スキルと関係ないタスク

---

## 核心原則

### 1. コンテキストは公共財

> "コンテキストウィンドウは公共財である"

スキルはAIが必要とする他の全てのものとコンテキストを共有する。
**必要最小限の情報のみ**を含め、各要素の必要性を吟味すること。

**デフォルトの前提: AIは既に非常に賢い。** AIがまだ持っていない情報のみを追加する。

### 2. 500行ルール

SKILL.mdは**500行以下**に保つ。それ以上になる場合：
- 複数のスキルに分割
- 詳細は `references/` に移動
- 不要なセクションを削除

### 3. 明確なトリガー

`description` に必ず以下を含める：

```yaml
description: |
  何をするスキルか。
  Use when: トリガーキーワード1, キーワード2, キーワード3
  Do not use when: 除外条件1, 除外条件2
```

AIはこの記述を見て、スキルを起動するか判断する。

---

## スキルの構造

### Gemini CLIのフォルダ構成

```
project/
├── .gemini/
│   ├── skills/           # スキル定義
│   │   └── skill-name/
│   │       ├── SKILL.md     # メインの指示（必須）
│   │       ├── scripts/     # 実行可能コード
│   │       ├── references/  # 詳細ドキュメント
│   │       └── assets/      # 出力用ファイル
│   └── rules/            # 常時適用ルール
└── GEMINI.md             # プロジェクト説明
```

### グローバル vs プロジェクト

| レベル | パス | 用途 |
|-------|------|------|
| グローバル | `~/.gemini/skills/` | 全プロジェクト共通 |
| プロジェクト | `.gemini/skills/` | プロジェクト固有 |

**注意**: Antigravity（Google AI IDE）とは異なります。
- Gemini CLI: `.gemini/` フォルダ
- Antigravity: `.agent/` フォルダ、`~/.gemini/antigravity/`

### Bundled Resources（オプション）

#### scripts/
実行可能コード（Python/Bashなど）。決定論的な信頼性が必要な場合や、同じコードが繰り返し書き直される場合に含める。

- **例**: `rotate_pdf.py`, `validate_data.py`
- **利点**: トークン効率的、決定論的、コンテキストに読み込まずに実行可能

#### references/
必要に応じてコンテキストに読み込むドキュメント。

- **例**: APIドキュメント、データベーススキーマ、詳細なワークフローガイド
- **利点**: SKILL.mdを軽量に保つ、必要な時だけ読み込む
- **ベストプラクティス**: 大きいファイル（10k語以上）にはgrep検索パターンを記載

#### assets/
出力で使用されるファイル（コンテキストには読み込まれない）。

- **例**: テンプレート、画像、フォント、ボイラープレートコード
- **利点**: 出力リソースをドキュメントから分離

---

## スキル作成プロセス

### Step 1: 具体例で理解する

スキルがどう使われるか、具体例を集める：
- 「どんな機能をサポートすべき？」
- 「使用例を教えて」
- 「どんな言葉でトリガーされる？」

### Step 2: リソースを計画する

各具体例を分析し、必要なリソースを特定：
- **scripts/**: 繰り返し書き直されるコード → スクリプト化
- **references/**: 毎回再発見する情報 → ドキュメント化
- **assets/**: 毎回使うボイラープレート → テンプレート化

### Step 3: スキルを初期化

新規作成の場合は `scripts/init_skill.py` を実行：

```bash
python scripts/init_skill.py <skill-name> --path .gemini/skills
```

### Step 4: スキルを編集

**出力パターン**: 詳細は `references/output-patterns.md` を参照
**ワークフローパターン**: 詳細は `references/workflows.md` を参照

#### SKILL.mdの書き方

```markdown
# スキル名

[1-2文で何をするか]

## このスキルを使用する時
- 条件1
- 条件2

## このスキルを使用しない時
- 除外1
- 除外2

## ワークフロー / 対応タスク
[具体的な手順やタスク一覧]

## ヒアリング項目
実装前に確認：
- 確認事項1
- 確認事項2

## 出力形式
[どのような形式で出力するか]
```

### Step 5: テスト＆検証

```bash
python scripts/quick_validate.py .gemini/skills/<skill-name>
```

### Step 6: 反復改善

実際に使ってみて、うまくいかない部分を修正する。

---

## 良いスキルの特徴

### DO（やるべきこと）

- ✅ 明確な `Use when:` と `Do not use when:` をdescriptionに
- ✅ 500行以下のSKILL.md
- ✅ 具体例を含む（説明より例）
- ✅ ヒアリング項目を用意
- ✅ 出力形式を明記
- ✅ 詳細はreferences/に分離

### DON'T（避けるべきこと）

- ❌ README.md, CHANGELOG.mdなど不要ファイル
- ❌ AIが既に知っている情報の重複
- ❌ 曖昧な説明（「良い感じに」「適切に」）
- ❌ 深くネストされた参照ファイル
- ❌ 複数の無関係なタスクを1つのスキルに

---

## Progressive Disclosure（段階的開示）

スキルは3レベルの読み込みシステムを使う：

1. **メタデータ（name + description）** - 常にコンテキストに（〜100語）
2. **SKILL.md本体** - スキルがトリガーされた時（<5k語）
3. **Bundled resources** - AIが必要と判断した時（無制限）

**重要**: SKILL.mdからreferencesファイルを明確に参照し、いつ読むべきか説明する。

---

## CLI別フォルダ比較

| ツール | スキルパス | ルールパス | グローバル |
|-------|-----------|-----------|-----------|
| Gemini CLI | `.gemini/skills/` | `.gemini/rules/` | `~/.gemini/skills/` |
| Antigravity | `.agent/skills/` | `.agent/rules/` | `~/.gemini/antigravity/skills/` |
| Claude Code | `.claude/skills/` | `.claude/rules/` | `~/.claude/skills/` |

---

## 参考リンク

- [Gemini CLI Documentation](https://ai.google.dev/gemini-api/docs/cli)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
