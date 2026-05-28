---
name: logging-observability
description: ロギングやモニタリングを実装する際に使用。
---

# Logging and Observability

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] ロギングを実装する?
- [ ] 監視・メトリクスを設計する?
- [ ] デバッグ用ログを追加する?
- [ ] 本番環境の可観測性を改善する?

### 前提条件
- [ ] ログレベルを決定したか?
- [ ] 構造化ログを使用しているか?
- [ ] requestIdを全ログに含めているか?

### 禁止事項の確認
- [ ] 機密情報(パスワード、トークン)をログに出力しようとしていないか?
- [ ] console.logを本番コードに残そうとしていないか?
- [ ] ログレベルを適切に使い分けているか?

---

## トリガー

- ロギング実装時
- 監視・メトリクス設計時
- デバッグ用ログ追加時
- 本番環境の可観測性改善時

---

## 🚨 鉄則

**本番で何が起きているかを把握できる状態を作る。**

---

## 構造化ログ

```typescript
// ❌
console.log(`User ${id} logged in`);

// ✅
logger.info('User logged in', {
  userId: id,
  ip,
  requestId,  // ⚠️ 全ログに含める
  timestamp: new Date().toISOString()
});
```

---

## ログレベル

```typescript
logger.debug('詳細なデバッグ情報');  // 開発時のみ
logger.info('正常な操作');           // 監査・追跡
logger.warn('問題の予兆');           // 注意が必要
logger.error('エラー発生');          // 即座に対応
```

---

## 機密情報の除外

```typescript
// ❌
logger.info('User data', { user }); // パスワード含む可能性

// ✅
logger.info('User data', {
  userId: user.id,
  email: user.email
  // password は含めない
});
```

---

## 🚫 禁止事項まとめ

- 機密情報のログ出力
- 本番でのconsole.log
- ログレベルの誤用
- requestIdなしのログ
