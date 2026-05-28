# Claude Code プロンプト規約

## CLAUDE.md

### 目的と配置

CLAUDE.mdはClaudeがセッション開始時に自動読み込みするコンテキストファイル。

**配置優先順位**（上から順に読み込み）:
1. `~/.claude/CLAUDE.md` - 全プロジェクト共通
2. リポジトリルート `CLAUDE.md` - プロジェクト固有（git管理推奨）
3. サブディレクトリ `CLAUDE.md` - 必要に応じて読み込み
4. `CLAUDE.local.md` - 個人設定（.gitignore推奨）

### 推奨構成

```markdown
# プロジェクト名

## コマンド
- `npm run build`: ビルド
- `npm run test`: テスト実行
- `npm run lint`: リント

## コードスタイル
- ES Modules使用（CommonJS禁止）
- インポートは分割代入で（`import { foo } from 'bar'`）

## ワークフロー
- 変更後は必ずtypecheck実行
- テストは単体で実行（全体実行は遅い）

## 注意事項
- `legacy/`配下は触らない
- APIキーは環境変数から取得
```

### 記述ルール

**DO**
- 簡潔に（各項目1-2行）
- 具体的なコマンド・ファイル名を記載
- Claudeが知らない固有情報を優先
- 頻出するワークフローを明記

**DON'T**
- 一般的な知識の説明
- 長文の背景説明
- 曖昧な指示（「適切に」「うまく」）

### 効果的な強調

```markdown
# 弱い
テストを書いてください

# 強い
IMPORTANT: 変更には必ずテストを追加。mockは使用禁止。

# 最強
⚠️ MUST: PRマージ前にCI通過必須。例外なし。
```

## カスタムスラッシュコマンド

### 配置と命名

```
.claude/commands/
├── fix-issue.md      → /project:fix-issue
├── review-pr.md      → /project:review-pr
└── deploy.md         → /project:deploy

~/.claude/commands/
└── daily-standup.md  → /user:daily-standup
```

### 基本構造

```markdown
$ARGUMENTSで指定されたGitHub Issueを修正する。

手順:
1. `gh issue view $ARGUMENTS`でIssue内容を確認
2. 関連ファイルを特定
3. 修正を実装
4. テストを追加・実行
5. コミット＆PR作成

制約:
- 既存のコードスタイルに従う
- 破壊的変更は避ける
- PRの説明にIssue番号を含める
```

### $ARGUMENTS の使用

`$ARGUMENTS`はコマンド実行時の引数を展開する特殊キーワード。

```markdown
# /project:fix-issue 123 と実行すると
# $ARGUMENTS → "123" に展開

Issue #$ARGUMENTS を分析して修正する。

1. `gh issue view $ARGUMENTS` で詳細確認
2. 修正実装
3. `gh pr create --body "Fixes #$ARGUMENTS"`
```

### 効果的なコマンド例

**シンプルなタスク**
```markdown
# review-changes.md
ステージされた変更をレビューして問題点を指摘する。

`git diff --staged`を実行し、以下を確認:
- バグの可能性
- セキュリティリスク
- パフォーマンス問題
- コードスタイル違反

問題がなければ「LGTM」と返答。
```

**複雑なワークフロー**
```markdown
# refactor-component.md
$ARGUMENTSで指定されたコンポーネントをリファクタリングする。

<phase_1>
現状分析:
- コンポーネントの責務を特定
- 依存関係をマッピング
- テストカバレッジを確認
</phase_1>

<phase_2>
リファクタリング計画:
- 変更箇所をリストアップ
- 破壊的変更の有無を確認
- ユーザーに計画を提示して承認を得る
</phase_2>

<phase_3>
実装:
- 計画に従って変更
- 各ステップでテスト実行
- 完了後にPR作成
</phase_3>
```

## SKILL.md

### frontmatter（必須）

```yaml
---
name: skill-name
description: 何をするスキルか、いつ使うか。具体的なトリガーワード・ファイル形式・シナリオを含める。
---
```

**description例**
```yaml
# Bad
description: ドキュメントを処理するスキル

# Good
description: Word文書（.docx）の作成・編集・分析。追跡変更、コメント追加、書式保持に対応。「Wordファイルを作成」「文書を編集」「変更を追跡」で発動。
```

### body構造

```markdown
# スキル名

[1-2文の概要]

## クイックスタート

[最もよく使うパターンの簡潔な例]

## ワークフロー

### パターン1: [ユースケース名]
[手順・コード例]

### パターン2: [ユースケース名]
[手順・コード例]

## 詳細リファレンス

複雑な操作は別ファイルを参照:
- [操作A詳細](references/operation-a.md)
- [操作B詳細](references/operation-b.md)
```

### スキル内の参照ファイル

**references/**: 必要時に読み込むドキュメント
```
references/
├── api-spec.md      # API仕様
├── examples.md      # 詳細な例
└── troubleshoot.md  # トラブルシューティング
```

**scripts/**: 実行可能なコード
```
scripts/
├── process.py       # 処理スクリプト
└── validate.sh      # 検証スクリプト
```

**assets/**: 出力に使用するファイル
```
assets/
├── template.docx    # テンプレート
└── logo.png         # ロゴ
```
