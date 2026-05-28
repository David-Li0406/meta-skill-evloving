---
name: api-design
description: REST APIを設計する際に使用。RESTful原則とエラーハンドリングをカバー。
---

# API Design

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] REST APIを設計する?
- [ ] エンドポイントを新規作成する?
- [ ] エラーレスポンス形式を検討する?
- [ ] APIバージョニングを検討する?

### 前提条件
- [ ] 対象リソースを明確に定義したか?
- [ ] クライアントの利用シナリオを理解しているか?
- [ ] 認証・認可の要件を把握しているか?
- [ ] 既存APIとの一貫性を確認したか?

### 禁止事項の確認
- [ ] 動詞をエンドポイントに含めようとしていないか?(/getUsers → /users)
- [ ] 500エラーで内部詳細を露出しようとしていないか?
- [ ] 破壊的変更をバージョンアップなしで行おうとしていないか?
- [ ] 一貫性のないレスポンス形式を使おうとしていないか?

---

## トリガー

- REST API設計時
- エンドポイント新規作成時
- エラーレスポンス形式検討時
- APIバージョニング検討時

---

## 🚨 鉄則

**APIは契約。公開後の変更は困難。**

---

## RESTful設計

```
GET    /users          # 一覧
GET    /users/123      # 取得
POST   /users          # 作成
PUT    /users/123      # 全更新
PATCH  /users/123      # 部分更新
DELETE /users/123      # 削除
```

---

## ステータスコード

```
200 OK           - 成功
201 Created      - 作成成功
400 Bad Request  - ⚠️ バリデーションエラー
401 Unauthorized - 認証必要
403 Forbidden    - 権限なし
404 Not Found    - リソースなし
500 Internal     - 🚫 詳細を隠す
```

---

## エラーレスポンス

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      { "field": "email", "message": "Invalid format" }
    ]
  }
}
```

---

## ⚠️ バージョニング

```
/v1/users
/v2/users
```

破壊的変更はメジャーバージョンアップ。

---

## レート制限

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95

429 Too Many Requests
Retry-After: 60
```

---

## 🚫 禁止事項まとめ

- 動詞をエンドポイントに含める(/getUsers, /createUser)
- 500エラーで内部スタックトレースを露出
- バージョンアップなしの破壊的変更
- 一貫性のないレスポンス形式
