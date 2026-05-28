---
name: refactoring
description: 振る舞いを変えずにコード構造を改善する際に使用。
---

# Refactoring

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] コード品質を改善する?
- [ ] 重複コードを発見した?
- [ ] 可読性を向上させる?
- [ ] 技術的負債を解消する?

### 前提条件
- [ ] テストが存在し、通ることを確認したか?
- [ ] 変更の影響範囲を把握したか?
- [ ] 小さなステップで進める準備ができているか?

### 禁止事項の確認
- [ ] テストなしでリファクタリングしようとしていないか?
- [ ] 振る舞いを変えようとしていないか?
- [ ] 一度に大きな変更をしようとしていないか?
- [ ] 機能追加とリファクタリングを同時にしようとしていないか?

---

## トリガー

- コード品質改善時
- 重複コード発見時
- 可読性向上時
- 技術的負債解消時

---

## 🚨 鉄則

**テストがある状態で始める。振る舞いは変えない。**

---

## ⚠️ 進め方

```
1. テストが通ることを確認
2. 小さな変更
3. テスト実行
4. 繰り返し
```

---

## コードスメル

### 長いメソッド → 抽出

```typescript
// ❌ 長いメソッド
function processOrder(order) {
  // 100行のコード...
}

// ✅ 意味のある単位で抽出
function processOrder(order) {
  validateOrder(order);
  calculateTotal(order);
  applyDiscount(order);
  saveOrder(order);
}
```

### 重複コード → 共通化

```typescript
// ❌ 重複
function createUser() { /* validation logic */ }
function updateUser() { /* same validation logic */ }

// ✅ 共通化
function validateUserData(data) { /* validation logic */ }
function createUser() { validateUserData(data); }
function updateUser() { validateUserData(data); }
```

---

## 🚫 禁止事項まとめ

- テストなしでのリファクタリング
- 振る舞いの変更
- 一度に大きな変更
- 機能追加との同時実施
