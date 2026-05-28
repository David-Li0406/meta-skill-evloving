---
name: database-design
description: スキーマ設計やマイグレーション作成時に使用。
---

# Database Design

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] テーブルを設計する?
- [ ] マイグレーションを作成する?
- [ ] インデックスを設計する?
- [ ] クエリを最適化する?

### 前提条件
- [ ] データの関係性を理解しているか?
- [ ] 想定されるクエリパターンを把握しているか?
- [ ] データ量の見積もりがあるか?

### 禁止事項の確認
- [ ] created_at/updated_atを忘れていないか?
- [ ] 適切なインデックスを設計したか?
- [ ] 外部キー制約を検討したか?
- [ ] ロールバック不可能なマイグレーションを書こうとしていないか?

---

## トリガー

- テーブル設計時
- マイグレーション作成時
- インデックス設計時
- クエリ最適化時

---

## 🚨 鉄則

**データモデルは変更コストが高い。慎重に設計。**

---

## 必須カラム

```sql
CREATE TABLE posts (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  -- ...
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## マイグレーション原則

```
□ UP/DOWNが対になっている
□ データ破壊がない(DROP前にバックアップ)
□ 本番で実行可能な速度
□ ロールバック可能
```

---

## インデックス

```sql
-- WHERE句で頻繁に使うカラム
CREATE INDEX idx_users_email ON users(email);

-- 複合インデックス(順序が重要)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
```

---

## 🚫 禁止事項まとめ

- created_at/updated_at忘れ
- インデックスなしの検索カラム
- ロールバック不可能なマイグレーション
- データ破壊を伴う変更(確認なし)
