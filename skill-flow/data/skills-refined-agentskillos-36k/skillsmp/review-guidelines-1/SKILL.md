---
name: review-guidelines
description: Apply comprehensive review standards for Vive. Use when reviewing PRs or performing self-review.
---

# Review Guidelines (Vive)

## 1. 仕様とコードの整合性

- 仕様/概念: `docs/spec.md`, `docs/concept.md`
- アーキテクチャ: `docs/architecture.md`
- README の利用者向け説明と齟齬がないか

## 2. アーキテクチャの一貫性

- `Discovery / Monitor / TUI / Orchestrator` の責務分離が守られているか
- `config.toml` のプレースホルダー処理やコマンド実行が仕様通りか
- `tmux` / `git worktree` 操作の安全性（削除や誤操作の防止）

## 3. 実装品質

- 例外/エラー処理が適切か（`Result` の伝播とログ）
- 不要な `unwrap()` の多用がないか
- 長時間ループや監視の負荷に配慮しているか

## 4. テスト・検証

- `tests/` の追加や更新が必要な変更か
- ローカル再現手順が明記されているか（`cargo test` / `cargo run`）

## 5. ドキュメント更新

- `docs/` の更新が必要な変更が反映されているか
- README の操作例や設定例が最新か
