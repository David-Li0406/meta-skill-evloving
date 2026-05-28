---
name: cga-programming
description: AIが自律的にTDDで実装する
allowed-tools: Task Read Glob Grep Edit Write Bash AskUserQuestion TodoWrite
disable-model-invocation: true
---

## いつ使うか

- 計画が確定し、実装を開始するとき
- バグ修正時にリグレッションテストを追加して修正するとき
- リファクタリング前にテストで保護してから変更するとき

## いつ使わないか

- 計画が未確定のとき（先に `/cga-explore-planning` で計画を策定する）
- 技術調査・ライブラリ選定フェーズ
- 設計レビューのみが必要なとき（`/cga-review` を使う）

## 何をするか

1. **TIDY?**: 構造の整理が必要か判断 → 必要なら `/cga-tf-refactoring` を実行
2. **RED**: 失敗するテストを書く
3. **GREEN**: 最小限の実装で通す
4. **REFACTOR**: コードを整理

## 中断条件

以下の場合は実装を中断し、開発者に状況を報告して `/cga-explore-planning` に戻る:

- **テスト5回連続失敗**: 同一テストが5回修正しても通らない場合
- **計画外の想定外事象**: 計画に記載のない前提条件の不整合や、計画では実現不可能と判断した場合

## 使用例

```text
/cga-programming doc/plans/cancel-order.md の計画に従って実装して
/cga-programming 在庫チェック機能を実装して
```

## ワークフロー位置

```
/cga-explore-planning → /cga-tf-refactoring → /cga-programming → /cga-review
        ↑                                          │
        └──────────── 中断（計画に戻る） ───────────┘
```

## 詳細

[guide.md](guide.md) を参照
