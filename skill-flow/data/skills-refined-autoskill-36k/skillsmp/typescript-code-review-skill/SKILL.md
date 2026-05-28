---
name: typescript-code-review-skill
description: TypeScript/React向けコードレビュースキル。命名規則、テストコード品質のレビューを実施。TypeScriptコードのレビュー、PRレビューを依頼された際に使用。
---

# TypeScript Code Review Skill

TypeScript/Reactプロジェクト向けのコードレビューを実施する。

## レビュー観点

| 観点 | 説明 | 参照 |
|------|------|------|
| 命名規則 | TypeScript命名規則の準拠 | [naming-review.md](references/naming-review.md) |
| テストコード | FIRST原則、AAA、網羅性の確認 | [test-review.md](references/test-review.md) |

## 使用方法

1. レビュー対象のコードを受け取る
2. 該当する観点のreferenceを読み込む
3. 各referenceの出力形式に従ってレビュー結果を出力

## 重要度分類

- **Blocking**: 即修正必須
- **Should Fix**: 修正推奨
- **Nice to Have**: 改善提案
