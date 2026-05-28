---
name: email
description: メール送信、テンプレート、通知機能を実装する際に使用。
---

# Email

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] メール送信機能を実装する?
- [ ] メールテンプレートを作成する?
- [ ] 通知システムを構築する?
- [ ] SMTP設定を行う?

### 前提条件
- [ ] SMTP設定を環境変数で管理しているか?
- [ ] テスト環境と本番環境を分離しているか?
- [ ] メールテンプレートを用意したか?

### 禁止事項の確認
- [ ] SMTP認証情報をハードコードしようとしていないか?
- [ ] 本番環境でテストメールを送信しようとしていないか?
- [ ] ユーザーのメールアドレスをログに出力しようとしていないか?

---

## トリガー

- メール送信機能実装時
- メールテンプレート作成時
- 通知システム構築時
- SMTP設定時

---

## 🚨 鉄則

**本番で誤送信しない仕組みを作る。テスト環境は隔離。**

---

## 基本設定

```typescript
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: 587,
  secure: false,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,  // 🚫 ハードコード禁止
  }
});
```

---

## テスト環境の隔離

```typescript
// 開発環境ではMailtrap/Ethereal等を使用
const getTransporter = () => {
  if (process.env.NODE_ENV === 'development') {
    return createTestTransporter();
  }
  return createProductionTransporter();
};
```

---

## 🚫 禁止事項まとめ

- SMTP認証情報のハードコード
- 本番環境でのテストメール送信
- メールアドレスのログ出力
- テスト環境と本番環境の混同
