---
name: input-validation
description: ユーザー入力、フォームデータ、APIリクエストを検証する際に使用。
---

# Input Validation

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] ユーザー入力を処理する?
- [ ] フォームデータを検証する?
- [ ] APIリクエストを検証する?
- [ ] 外部データを受け取る?

### 前提条件
- [ ] 入力の期待値を定義したか?
- [ ] エラーメッセージを用意したか?
- [ ] サーバー側での検証を実装したか?

### 禁止事項の確認
- [ ] クライアント側の検証だけで済ませようとしていないか?
- [ ] 入力をサニタイズせずにDB/HTMLに出力しようとしていないか?
- [ ] 型チェックを省略しようとしていないか?

---

## トリガー

- ユーザー入力処理時
- フォームデータ検証時
- APIリクエスト検証時
- 外部データ受け取り時

---

## 🚨 鉄則

**クライアントは信用しない。サーバーで必ず検証。**

---

## バリデーション層

```
クライアント: UX向上(即座のフィードバック)
     ↓
サーバー: ⚠️ 必須(セキュリティ)
     ↓
データベース: 最終防衛(制約)
```

---

## Zodによる検証

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  age: z.number().int().positive().optional()
});

// 使用
const result = UserSchema.safeParse(input);
if (!result.success) {
  return res.status(400).json({ errors: result.error.issues });
}
```

---

## SQLインジェクション防止

```typescript
// ❌ 文字列連結
const query = `SELECT * FROM users WHERE id = '${id}'`;

// ✅ パラメータ化クエリ
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [id]);
```

---

## 🚫 禁止事項まとめ

- クライアント側検証のみ
- サニタイズなしの出力
- 型チェックの省略
- 文字列連結でのSQL構築
