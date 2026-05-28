---
name: error-handling
description: エラーハンドリングを実装する際に使用。回復戦略と復元パターンをカバー。
---

# Error Handling

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] 例外処理を実装する?
- [ ] try-catchを設計する?
- [ ] リトライロジックを実装する?
- [ ] エラーレスポンスを設計する?

### 前提条件
- [ ] エラーの種類を分類したか?(回復可能/不可能)
- [ ] ユーザーへのエラーメッセージを検討したか?
- [ ] ログに記録すべき情報を整理したか?

### 禁止事項の確認
- [ ] エラーを握りつぶそうとしていないか?(空のcatch)
- [ ] スタックトレースをユーザーに露出しようとしていないか?
- [ ] 全てのエラーを同じように扱おうとしていないか?

---

## トリガー

- 例外処理実装時
- try-catch設計時
- リトライロジック実装時
- エラーレスポンス設計時

---

## 🚨 鉄則

**回復可能かどうかで処理を分ける。**

---

## エラー分類

```typescript
// 回復可能(リトライ対象)
class TransientError extends Error { retryable = true; }

// 回復不可能
class PermanentError extends Error { retryable = false; }
```

---

## リトライパターン

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  delay = 1000
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (!error.retryable || i === maxRetries - 1) throw error;
      await sleep(delay * Math.pow(2, i)); // 指数バックオフ
    }
  }
}
```

---

## ユーザー向けエラー

```typescript
// 🚫 内部詳細を露出しない
res.status(500).json({
  error: 'Internal server error'
  // stacktrace: ... ❌
});

// ログには詳細を記録
logger.error('DB connection failed', { error, requestId });
```

---

## 🚫 禁止事項まとめ

- 空のcatchブロック(エラー握りつぶし)
- スタックトレースのユーザー露出
- 全エラーの同一扱い
- リトライなしの一時的エラー
