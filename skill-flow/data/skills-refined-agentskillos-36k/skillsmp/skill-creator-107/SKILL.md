---
name: skill-creator
description: "Claude Code用のスキルを作成・設計するためのガイド。Anthropic公式skill-creatorをベースに最適化。スキル作成、skill作成、新しいスキル、SKILL.md、スキル設計、スキルの書き方の時に使用。"
user-invocable: true
argument-hint: "[skill-name] [--教育|--開発|--業務]"
---

# Skill Creator Guide

Claude Codeで使えるスキルを作成するためのガイド。
Anthropic公式のskill-creatorをベースに最適化。

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

**デフォルトの前提: Claudeは既に非常に賢い。** Claudeがまだ持っていない情報のみを追加する。

### 2. 500行ルール

SKILL.mdは**500行以下**に保つ。それ以上になる場合：
- 複数のスキルに分割
- 詳細は `references/` に移動
- 不要なセクションを削除

### 3. 明確なトリガー

`description` に必ず以下を含める：

```yaml
description: "何をするスキルか。トリガーキーワード1、キーワード2、キーワード3の時に使用。"
```

AIはこの記述を見て、スキルを起動するか判断する。

---

## スキルの構造

### Claude Codeのフォルダ構成

```
project/
├── .claude/
│   ├── skills/           # スキル定義
│   │   └── skill-name/
│   │       ├── SKILL.md     # メインの指示（必須）
│   │       ├── scripts/     # 実行可能コード
│   │       ├── references/  # 詳細ドキュメント
│   │       └── assets/      # 出力用ファイル
│   ├── rules/            # 常時適用ルール
│   └── commands/         # スラッシュコマンド
└── CLAUDE.md             # プロジェクト説明
```

### グローバル vs プロジェクト

| レベル | パス | 用途 |
|-------|------|------|
| グローバル | `~/.claude/skills/` | 全プロジェクト共通 |
| プロジェクト | `.claude/skills/` | プロジェクト固有 |

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
python scripts/init_skill.py <skill-name> --path <output-directory>
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

### Step 5: パッケージング

`scripts/package_skill.py` でバリデーション＆パッケージング：

```bash
python scripts/package_skill.py <path/to/skill-folder>
```

### Step 6: 反復改善

実際に使ってみて、うまくいかない部分を修正する。

---

## 良いスキルの特徴

### DO（やるべきこと）

- ✅ 明確なトリガーワードをdescriptionに含める
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
3. **Bundled resources** - Claudeが必要と判断した時（無制限）

**重要**: SKILL.mdからreferencesファイルを明確に参照し、いつ読むべきか説明する。

---

## Rules vs Skills の使い分け

| 項目 | Rules | Skills |
|------|-------|--------|
| 場所 | `.claude/rules/` | `.claude/skills/` |
| 適用 | 常に自動 | 必要な時だけ |
| 用途 | ポリシー、規約 | 手順、専門知識 |
| 例 | コーディング規約 | 指導案作成手順 |

**判断の目安**:
- 「毎回必ず守ってほしい」→ **Rules**
- 「特定のタスクでだけ使う」→ **Skills**

---

## 参考リンク

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
