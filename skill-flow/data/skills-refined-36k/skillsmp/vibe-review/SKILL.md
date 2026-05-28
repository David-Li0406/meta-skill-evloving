---
name: vibe-review
description: バイブコーディングCodexレビュー - design/plans/PRの観点別レビュー
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# /vibe-review - Codexレビュー依頼

design.md、plans.md、またはPRをCodexにレビュー依頼します。

## レビュー対象の自動判定

以下の優先順位で対象を判定：

1. PRが存在する場合 → PRレビュー
2. plans.md が存在する場合 → plans.mdレビュー
3. design.md が存在する場合 → design.mdレビュー

手動で指定する場合は引数を使用：
- `/vibe-review design` - design.mdをレビュー
- `/vibe-review plan` - plans.mdをレビュー
- `/vibe-review pr` - PRをレビュー

## レビュールール

### 共通ルール
- レビュー往復は基本1回まで
- Major issueがある場合のみ最大2回まで許容
- 完璧化ではなくリスク洗い出しに集中

### Major / Minor の判定基準

| 分類 | 内容 | 対応 |
|------|------|------|
| Major | 目的未達成、セキュリティリスク、設計矛盾、大規模手戻り | 修正必須 |
| Minor | 曖昧な表現、命名改善、説明不足、粒度調整 | 修正任意 |

## 実行手順

### 共通: tmux-manager.sh の設定

```bash
TMUX_MGR=~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh
```

### design.md レビュー

1. Codexペインを確保: `$TMUX_MGR ensure`
2. レビュー依頼を送信（stdinで複数行を送る）
3. 応答を待機してキャプチャ: `$TMUX_MGR wait_response 180 && $TMUX_MGR capture 300`

### PRレビュー

PRレビューは `/review-pr` を実行し、結果をバイブコーディング形式に変換します。

| review-pr | バイブコーディング | 対応 |
|-----------|-------------------|------|
| P0 (Blocking) | Major | 修正必須 |
| P1 (Urgent) | Major | 修正必須 |
| P2 (Normal) | Minor | 修正任意 |
| P3 (Low) | Minor | 修正任意 |

## レビュー結果の処理

### OK to proceed with minor fixes の場合
1. Minor指摘は任意で対応
2. 次のフェーズへ進む

### Not ready (Major issues present) の場合
1. Major指摘を修正
2. 再度 `/vibe-review` を実行（最大2回まで）
3. 2回目もMajorがある場合は人間に相談

## 人間の判断ポイント

1. design.md OK後: 方針確認 - この方向で進めてよいか
2. plans.md OK後: 計画承認 - この計画で実装を開始してよいか
3. PR OK後: マージ判断 - 本番に入れてよいか

CodexのOKは「リスク棚卸完了」を意味します。
「地雷がありそう」は教えてくれますが、「踏んでもいいか」は人間が決めます。
