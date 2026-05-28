---
name: environment-configuration
description: 環境変数やシークレットを管理する際に使用。
---

# Environment Configuration

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] 環境変数を設定する?
- [ ] .envファイルを作成する?
- [ ] シークレットを管理する?
- [ ] 環境別設定を分離する?

### 前提条件
- [ ] .env.exampleを用意したか?
- [ ] .gitignoreに.envを追加したか?
- [ ] 必須の環境変数を明確にしたか?

### 禁止事項の確認
- [ ] 機密情報をコードにハードコードしようとしていないか?
- [ ] .envファイルをコミットしようとしていないか?
- [ ] デフォルト値に本番の値を設定しようとしていないか?

---

## トリガー

- 環境変数設定時
- .env ファイル作成時
- シークレット管理時
- 環境別設定分離時

---

## 🚨 鉄則

**設定はコードから分離。機密情報はコードに書かない。**

---

## .env

```bash
# .env.example (✅ コミットする)
DATABASE_URL=postgres://user:pass@localhost/db

# .env (🚫 コミットしない)
DATABASE_URL=postgres://real:pass@prod/db
```

---

## バリデーション

```typescript
// 起動時に必須変数をチェック
const required = ['DATABASE_URL', 'JWT_SECRET', 'API_KEY'];

for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing required env: ${key}`);
  }
}
```

---

## 環境別設定

```
.env.development
.env.test
.env.production
```

---

## 🚫 禁止事項まとめ

- 機密情報のハードコード
- .envファイルのコミット
- 本番値のデフォルト設定
- 環境変数バリデーションの省略
