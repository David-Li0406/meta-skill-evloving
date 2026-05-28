---
name: security-review
description: 認証、ユーザー入力、機密データを扱う際に使用。OWASP Top 10をカバー。
---

# Security Review

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] 認証・認可コードを実装する?
- [ ] ユーザー入力を処理する?
- [ ] 機密データを取り扱う?
- [ ] セキュリティレビューを実施する?

### 前提条件
- [ ] OWASP Top 10を把握しているか?
- [ ] 入力検証を実装したか?
- [ ] 認可チェックを実装したか?

### 禁止事項の確認
- [ ] ユーザー入力を信用しようとしていないか?
- [ ] 認可チェックを省略しようとしていないか?
- [ ] 機密データを平文で保存しようとしていないか?
- [ ] SQLインジェクション脆弱性を作ろうとしていないか?

---

## トリガー

- 認証・認可コード実装時
- ユーザー入力処理時
- 機密データ取り扱い時
- セキュリティレビュー実施時

---

## 🚨 鉄則

**入力は信用しない。権限は常に確認。機密は暗号化。**

---

## OWASP Top 10 要点

### A01: アクセス制御

```typescript
// ⚠️ 必須チェック
if (req.user.id !== resourceOwnerId && !req.user.isAdmin) {
  return res.status(403).json({ error: 'Forbidden' });
}
```

### A02: 暗号化

```typescript
// パスワードはbcrypt
const hash = await bcrypt.hash(password, 12);

// 機密データは暗号化
const encrypted = crypto.createCipheriv(...);
```

### A03: インジェクション

```typescript
// ❌ 文字列連結
db.query(`SELECT * FROM users WHERE id = '${id}'`);

// ✅ パラメータ化
db.query('SELECT * FROM users WHERE id = ?', [id]);
```

### A07: XSS

```typescript
// ❌ そのまま出力
element.innerHTML = userInput;

// ✅ サニタイズ
element.textContent = userInput;
```

---

## 🚫 禁止事項まとめ

- ユーザー入力の信用
- 認可チェックの省略
- 機密データの平文保存
- SQLインジェクション脆弱性
- XSS脆弱性
