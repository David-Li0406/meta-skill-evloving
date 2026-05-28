---
name: cga-prisma-migration
description: Prismaを使用したDBスキーマ変更とマイグレーション管理。
allowed-tools: Read Glob Grep Edit Write Bash AskUserQuestion
disable-model-invocation: true
---

## いつ使うか

- テーブル追加・変更するとき
- カラム追加・削除するとき
- インデックス作成するとき

## いつ使わないか

- `schema.prisma` の変更を伴わない型定義の変更
- テーブル設計が未確定のとき（先に `/cga-explore-planning` で設計を決める）

## 何をするか

1. `prisma/schema.prisma` を編集
2. `npx prisma migrate dev --name {name}` でマイグレーション生成
3. `npx prisma generate` でクライアント生成
4. `src/models/` に型定義作成

## 命名規則

- `add_{table}` - テーブル追加
- `add_{column}_to_{table}` - カラム追加
- `remove_{column}_from_{table}` - カラム削除
- `create_{index}_index` - インデックス追加

## 中断条件

以下の場合はマイグレーションを中断し、開発者に確認を求める:

- **破壊的変更**: 既存データの削除・型変更を伴うマイグレーションが生成された場合
- **複数テーブル影響**: 予期しない複数テーブルへの影響が検出された場合

## 注意事項

- 本番環境では `migrate deploy` を使用
- 破壊的変更は段階的に実行
- バックアップを取ってから実行

## 使用例

```text
/cga-prisma-migration OrderテーブルにcancelledAtカラムを追加して
/cga-prisma-migration 新しいPaymentテーブルを作成して
```

## 詳細

[guide.md](guide.md) を参照
