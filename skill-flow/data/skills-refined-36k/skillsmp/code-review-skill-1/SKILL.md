---
name: code-review-skill
description: 言語共通のコードレビュースキル。コメント最適化、マジックナンバー検出、構造改善のレビューを実施。コードレビュー、PRレビュー、コード品質チェックを依頼された際に使用。
---

# Code Review Skill

言語共通のコードレビューを実施する。

## レビュー観点

| 観点 | 説明 | 参照 |
|------|------|------|
| コメント最適化 | Why/Docコメント以外を削除・置換 | [comment-review.md](references/comment-review.md) |
| マジックナンバー | 意味不明な数値・文字列リテラルの検出 | [magic-number-review.md](references/magic-number-review.md) |
| 構造改善 | Guard Clauses、Dead Code等の検出 | [structure-review.md](references/structure-review.md) |

## 使用方法

1. レビュー対象のコードを受け取る
2. 該当する観点のreferenceを読み込む
3. 各referenceの出力形式に従ってレビュー結果を出力

## 重要度分類

- **Blocking**: 即修正必須
- **Should Fix**: 修正推奨
- **Nice to Have**: 改善提案
