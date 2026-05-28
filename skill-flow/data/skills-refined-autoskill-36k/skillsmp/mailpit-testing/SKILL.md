---
name: mailpit-testing
description: Use Mailpit to test emails in local development. Understand email verification workflows and inspect outgoing emails without external services.
metadata:
  author: Bingify
  version: "1.0"
---

# Mailpit Local Email Testing

このスキルは、Bingifyプロジェクトでのメール機能のローカル開発・テストをカバーします。

## 概要

BingifyはMailpitを使用して、ローカル開発環境でメール送信のテストを行います。

## Mailpit WebUIへのアクセス

```
http://localhost:54324
```

Mailpit WebUIでは、送信されたすべてのメールを確認できます。

## メール送信関数

```typescript
import { sendEmail } from "@/lib/mail";

export async function sendWelcomeEmail(email: string) {
  const result = await sendEmail({
    to: email,
    subject: "Welcome to Bingify",
    html: "<h1>Welcome!</h1>",
  });

  return result;
}
```

## ServerActionsでのメール送信

```typescript
"use server";

import { sendEmail } from "@/lib/mail";

export async function submitContactForm(data: unknown) {
  const validData = contactFormSchema.parse(data);

  // お問い合わせ確認メール
  await sendEmail({
    to: validData.email,
    subject: "お問い合わせありがとうございます",
    html: `<p>メッセージを受け取りました。</p>`,
  });

  return { success: true };
}
```

## Mailpit REST API

メール情報の取得：

```bash
curl http://localhost:54324/api/v1/messages
```

## メールをクリア

```bash
curl -X DELETE http://localhost:54324/api/v1/messages
```

## 参考

- [Mailpit公式ドキュメント](https://mailpit.axllent.org/)
