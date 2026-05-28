# Prisma Migration 詳細ガイド

## マイグレーションコマンド

### 開発環境

```bash
# マイグレーション生成と適用
npx prisma migrate dev --name {migration_name}

# クライアント再生成
npx prisma generate

# スキーマをDBにプッシュ（マイグレーションなし）
npx prisma db push

# DBの状態をリセット
npx prisma migrate reset
```

### 本番環境

```bash
# マイグレーション適用のみ
npx prisma migrate deploy
```

## マイグレーション命名規則

| パターン | 例 |
| --- | --- |
| テーブル追加 | `add_payments` |
| カラム追加 | `add_cancelled_at_to_orders` |
| カラム削除 | `remove_legacy_field_from_users` |
| インデックス追加 | `create_user_id_index` |
| リレーション追加 | `add_order_items_relation` |

## 破壊的変更の対処

### カラム名変更（3ステップ）

1. 新カラムをnullableで追加
2. データ移行スクリプト実行
3. 旧カラム削除

### 型変更（3ステップ）

1. 新しい型のカラムをnullableで追加
2. データ移行
3. 入れ替え

## インデックス設計

- 検索条件に使うカラムにインデックスを作成
- 複合インデックスはカーディナリティの高い順に
- ユニーク制約は`@@unique`で定義

## 注意事項

- 本番環境では `migrate deploy` を使用
- 破壊的変更は段階的に実行
- バックアップを取ってから実行
