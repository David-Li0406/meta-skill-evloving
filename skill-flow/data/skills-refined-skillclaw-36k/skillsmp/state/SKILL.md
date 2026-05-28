---
name: state
description: このワークスペースの state.md 管理、playbook 運用の専門知識。state.md の更新、done_criteria の判定、CRITIQUE の実行時に使用する。
---

# Workspace Management Skill

このワークスペース固有の管理知識を提供します。

## state.md の構造

```yaml
# 必須セクション
playbook:
  active: <playbook-path>   # 現在の playbook パス
  branch: <branch-name>     # playbook に紐づくブランチ
  review_pending: false     # true: レビュー未完了

goal:
  milestone: <milestone-id> # 現在のマイルストーン
  phase: <phase-id>         # 現在のフェーズ
  done_criteria:            # 達成条件（テストとして扱う）
    - criteria1
    - criteria2

session:
  last_start: <timestamp>   # セッション開始時刻
  last_clear: <timestamp>   # 最後の /clear 実行時刻

config:
  security: admin           # セキュリティレベル
  toolstack: A              # A: Claude Code only | B: +Codex | C: +Codex+CodeRabbit
```

## main ブランチ保護

main/master ブランチでは Edit/Write が常にブロックされる。
playbook 作成時に Claude が自動でブランチを切るため、ユーザーの手動操作は不要。

**例外（常に編集可能）**: state.md

## CRITIQUE の実行方法

done と判定する前に必ず実行:

```
[CRITIQUE]
done_criteria 達成の証拠:
  - {criteria}: {PASS|FAIL} - {具体的な証拠}
playbook 自体の妥当性: {問題なし|修正が必要}
成果物の動作確認: {確認済み|未確認}
判定: {PASS|FAIL}
```

## state.md 更新のルール

1. phase 完了時は state.md の goal.phase を次の phase に更新
2. playbook 完了時は playbook.active を null または次の playbook に更新
3. done_criteria を満たしたら証拠と共に記録

## playbook 必須ルール

```yaml
条件:
  playbook.active: null

対応:
  1. 作業開始禁止
  2. まず playbook を作成

手順:
  1. play/template/plan.json と play/template/progress.json を読む
  2. ユーザーにヒアリング:
     - 何を作るか（ゴール）
     - 完了条件は何か（done_criteria）
     - フェーズ分割
  3. play/<id>/plan.json と play/<id>/progress.json を作成
  4. state.md の playbook.active を更新
  5. 作業開始

なぜ必須か:
  - playbook なし = done_criteria なし = 完了判定不可能
  - 「計画なしで作業 → 自己報酬詐欺」の防止
```

## playbook 作成テンプレート（v2 JSON）

- `play/template/plan.json`
- `play/template/progress.json`
