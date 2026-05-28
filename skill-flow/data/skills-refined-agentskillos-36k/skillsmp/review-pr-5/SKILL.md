---
name: review-pr
description: PRを体系的にレビューして実行可能なフィードバックを提供
user-invocable: true
allowed-tools:
  - Bash(gh:*)
  - Bash(git:*)
  - Read
  - Glob
  - Grep
---

# /review-pr - 体系的なPRレビュー

このPRを体系的にレビューし、実行可能なフィードバックを提供してください。

> バイブコーディング用: `/vibe-review pr`

## 実行手順

### 1. PR情報の取得

```bash
gh pr view --comments
gh pr diff
gh pr checks
```

### 2. Codex分析の実施

tmux内の場合:
```bash
TMUX_MGR=~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh
$TMUX_MGR ensure
$TMUX_MGR send "gh pr diffをレビューしてください。P0-P3の優先度で問題を分類し、各指摘は [PX] file:line - 問題の要約 の形式で報告してください。"
$TMUX_MGR wait_response 180
$TMUX_MGR capture 300
```

tmux外の場合:
```bash
codex exec "gh pr diffをレビューしてください。P0-P3の優先度で問題を分類し、各指摘は [PX] file:line - 問題の要約 の形式で報告してください。"
```

### 3. 統合レビューの作成

Codex分析とあなた自身の評価を統合し、以下のフォーマットで出力。

## 出力フォーマット

```markdown
## レビュー結果

変更内容: X files (+XXX/-XXX lines) | CI: Pass/Fail
総合評価: X/10点

### 概要
PRの目的と変更内容を1-2文で要約。

### レビューステータス
- [ ] 変更要求（P0項目の修正後に再レビュー）
- [ ] 承認保留（質問への回答待ち）
- [ ] 承認（LGTM - マージ可能）

---

## P0: マージ前に必須
### [file:line] 問題の要約
問題: 何が問題か
修正案: 具体的な修正方法

## P1: 次のサイクルで対応
### [file:line] 問題の要約
問題: 何が問題か
修正案: 改善方法

## P2: いずれ修正
- [file:line] 簡潔な提案

## P3: 余裕があれば
- [file:line] 簡潔な提案

---

## 良かった点（任意）
- [file:line] 良い実装の理由

## 注意事項（任意）
- Breaking Changes: なし/あり
- ロールバック: 容易/注意が必要
```

## 優先度の判断基準

| 優先度 | 内容 | 例 |
|--------|------|-----|
| P0 | マージ前に必須 | セキュリティ脆弱性、データ損失、重大なバグ |
| P1 | 次のサイクルで対応 | パフォーマンス問題、エラーハンドリング不足 |
| P2 | いずれ修正 | 設計改善、保守性向上、ドキュメント |
| P3 | 余裕があれば | 命名改善、軽微なリファクタリング |

## 重要な原則

- Codex指摘を鵜呑みにせず妥当性を検証
- False Positive（AI誤検知）は除外
- プロジェクト固有の文脈・制約を考慮
- 最終的なレビュー内容はあなたが責任を持って決定
