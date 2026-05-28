---
name: code-review
description: Use when performing code reviews. Provides a checklist to verify error handling, TypeScript, CSS, and architecture patterns.
---

# Code Review Skill

コードレビューを行う際のチェックリストです。

## レビュー前の確認事項

以下のドキュメントを参照してレビューを行ってください:

- **CLAUDE.md** - プロジェクトガイドライン
- **docs/error-handling.md** - エラーハンドリング規約
- **docs/typescript.md** - TypeScript 規約
- **docs/css.md** - CSS ガイドライン

## チェックリスト

### エラーハンドリング
- [ ] `try-catch` が使用されていないか
- [ ] `Result` 型が適切に使用されているか
- [ ] ライブラリ呼び出しに `wrap` が使用されているか

### TypeScript
- [ ] Zod スキーマから型が推論されているか
- [ ] 不要な明示的インターフェースがないか

### CSS
- [ ] `@apply` が使用されていないか
- [ ] カスタム CSS クラスが追加されていないか
- [ ] `cva` と `cn()` が適切に使用されているか

### アーキテクチャ
- [ ] Container/Presentational パターンに従っているか
- [ ] 適切なディレクトリ構造か

## レビュー後

問題がなければ以下を実行:

```bash
pnpm biome
pnpm build
pnpm type-check
```
