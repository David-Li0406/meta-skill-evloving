---
name: architecture-review
description: Use when generating or modifying code to ensure it follows project architecture and development guidelines. Enforces Result-based error handling, TypeScript conventions, and frontend architecture patterns.
---

# Architecture Skill

このスキルはプロジェクトのアーキテクチャと開発指針に基づいてコードを生成・修正する際に使用します。

## 必須読み込みファイル

作業開始前に以下のドキュメントを必ず参照してください:

1. **CLAUDE.md** - プロジェクト全体のガイドライン
2. **docs/architecture.md** - フロントエンドアーキテクチャ
3. **docs/css.md** - Tailwind CSS ガイドライン
4. **docs/error-handling.md** - エラーハンドリング規約
5. **docs/typescript.md** - TypeScript 規約
6. **docs/ui-specification.md** - UI 仕様

## コーディング規約

### エラーハンドリング
- `try-catch` は使用禁止
- `Result` 型を使用する
- ライブラリの非同期処理には `wrap` を使用
- インポート: `import { wrap, Ok, Err, AppError } from "@blog/errors"`

### TypeScript
- Zod スキーマを型定義の信頼源とする
- 明示的なインターフェースではなく、スキーマから型を推論する

### フロントエンドアーキテクチャ
- Feature-based アプローチ
- Container/Presentational パターン
- Next.js App Router と features/pages の 1:1 マッピング

### CSS & スタイリング
- Tailwind CSS v4 (CSS-first configuration)
- `@theme` ディレクティブでデザイントークンを定義
- コンポーネントバリアントには `cva` を使用
- 条件付きクラスには `cn()` を使用
- `@apply`、カスタム CSS クラス、新しい `@keyframes` は禁止
