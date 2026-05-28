---
name: code-review
description: コード修正後にプロジェクトルールへの準拠をチェック。コードを書いた後、修正した後、実装が完了した時に使用。
allowed-tools: Read, Grep, Glob
---

# Code Review - ルール準拠チェック

修正したコードがプロジェクトルールに準拠しているかをチェックします。

## ルールファイル

以下のファイルを参照してチェックを実施:

- `.claude/rules/01-architecture.md` - アーキテクチャ、ディレクトリ構成
- `.claude/rules/02-supabase.md` - Supabaseキー、認証、データベース
- `.claude/rules/03-coding-rules.md` - API、型、ログ、テスト、ワークフロー

## チェック手順

1. 修正されたファイルを特定
2. 上記ルールファイルを読み込み
3. 各ルールに違反していないか確認
4. 違反があれば具体的な行番号と修正案を提示
5. 最後に `npm run format && npm run lint:fix && npm run test && npm run build` を実行

## 出力フォーマット

```markdown
## ルール準拠チェック結果

### 違反なし
- ✅ アーキテクチャ (01-architecture.md)
- ✅ Supabase (02-supabase.md)

### 違反あり
- ❌ コーディングルール (03-coding-rules.md)
  - `src/app/api/xxx/route.ts:25` - `as any`を使用
  - 修正案: 適切な型定義を作成

### 要確認
- ⚠️ コーディングルール (03-coding-rules.md)
  - 新規UseCaseにテストがありません
```
