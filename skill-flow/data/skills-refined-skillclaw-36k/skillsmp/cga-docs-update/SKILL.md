---
name: cga-docs-update
description: git diff ..mainを参考に、doc/domain・doc/decisionsを更新した方がいいことを提案する。
allowed-tools: Bash Read Glob Grep Edit AskUserQuestion
---

## いつ使うか

- フィーチャーブランチの作業が一段落したとき
- PRを作成する前
- mainへマージする前のドキュメント整合性チェック

## 何をするか

1. `git diff main..HEAD` でコード変更を分析
2. 影響を受けるドキュメントを特定し、更新を提案
3. ユーザー確認後、更新を実行

## 対象ドキュメント

### doc/domain/（ユーザーストーリー・語彙）

| 観点 | 説明 |
|------|------|
| 進捗状況 | 実装済み機能の進捗率を更新 |
| 受け入れ条件 | 完了したタスクにチェックを入れる |
| 技術タスク | 追加・変更されたファイルを反映 |
| エラー型定義 | 新しいエラー型が追加されていないか |

### doc/decisions/（意思決定記録）

| 観点 | 説明 |
|------|------|
| 新規ADR/DDR | 重要な意思決定が記録されているか |
| 既存DR更新 | 実装で判明した追加情報があるか |

## 使用例

```text
/cga-docs-update
```

## 詳細

[guide.md](guide.md) を参照
