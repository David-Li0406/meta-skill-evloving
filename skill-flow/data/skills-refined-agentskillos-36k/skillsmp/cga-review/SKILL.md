---
name: cga-review
description: サブエージェントを使って並列でコードレビューを実施。人間がマージ判断。
allowed-tools: Task Read Glob Grep Bash
---

## いつ使うか

- プルリクエストのレビュー時
- 特定ファイル・ディレクトリのレビュー時
- リファクタリング前の品質チェック時

## 何をするか

4タスクを同時に並列起動し、全完了後に結果をマージする:

1. **Task(Bash)**: 自動チェック（`npm run review:json`）
2. **Task(Explore)**: ビジネスロジックの正しさレビュー
3. **Task(Explore)**: 設計・命名レビュー
4. **Task(Explore)**: セキュリティレビュー

結果をマージして問題点と改善提案をまとめる。

## 使用例

```text
/cga-review src/ordering/usecases/
/cga-review src/ordering/usecases/create-order.ts
```

## ワークフロー位置

```
/cga-explore-planning → /cga-tf-refactoring → /cga-programming → /cga-review
```

## 詳細

[guide.md](guide.md) を参照
