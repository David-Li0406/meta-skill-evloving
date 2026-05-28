---
name: design-review
description: Use when reviewing UI/UX design. Provides a checklist for colors, typography, accessibility, design patterns, design tokens, and writing guidelines.
---

# Design Review Skill

デザインガイドラインに基づいてUI/UXをレビューする際のチェックリストです。

## レビュー前の確認事項

以下のドキュメントを参照してレビューを行ってください:

- **docs/design/colors.md** - カラーガイドライン
- **docs/design/typography.md** - タイポグラフィ
- **docs/design/accessibility.md** - アクセシビリティ
- **docs/design/design-principles.md** - デザイン原則
- **docs/design/design-patterns.md** - デザインパターン
- **docs/design/design-tokens.md** - デザイントークン
- **docs/design/writing.md** - ライティング
- **docs/design/content-guidelines.md** - コンテンツガイドライン

## チェックリスト

### カラー
- [ ] ブランドカラーパレットに準拠しているか
- [ ] コントラスト比が4.5:1以上を満たしているか
- [ ] 色だけで情報を伝えていないか（形状やテキストも併用）

### タイポグラフィ
- [ ] フォントサイズがデザイントークンに準拠しているか
- [ ] 行間が適切か（1.4以上）
- [ ] 10px未満のフォントサイズを使用していないか

### アクセシビリティ
- [ ] 画像に適切なalt属性があるか（装飾画像は `alt=""`）
- [ ] キーボード操作が可能か
- [ ] フォーカス状態が視認できるか
- [ ] 見出し構造が正しいか（h1→h2→h3の順序、スキップなし）
- [ ] フォームにラベルとアクセシブルネームがあるか

### デザインパターン
- [ ] 視線誘導が考慮されているか（F型/Z型）
- [ ] 視覚的グルーピングが適切か（余白/矩形/罫線）
- [ ] モバイルレイアウトが考慮されているか（シングルカラム推奨）
- [ ] フィードバックが操作要素の近くに表示されるか
- [ ] 危険な操作（削除等）にワンクッション（確認ダイアログ）があるか
- [ ] モーダルの完了ボタンを無効化していないか（エラーはフィードバックで表示）

### デザイントークン
- [ ] ハードコードされたカラー値がないか
- [ ] セマンティックトークンを使用しているか（`--color-text-primary` 等）
- [ ] 余白がTailwindスケールに準拠しているか（arbitrary value を避ける）
- [ ] 角丸がトークンに準拠しているか（`--radius-*`）

### ライティング
- [ ] エラーメッセージが3要素（事象・原因・対処）を含むか
- [ ] ボタンラベルが動詞で終わっているか（「保存する」「削除する」）
- [ ] 一文が50文字程度に収まっているか
- [ ] 表記が統一されているか（同じ機能に同じ言葉）
- [ ] 二重否定を使用していないか

## レビュー後

問題がなければ以下を実行:

```bash
pnpm biome
pnpm type-check
```
