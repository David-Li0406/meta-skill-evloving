---
name: internationalization
description: Implement i18n using next-intl. Manage multilingual content in en.json and ja.json. Apply translation patterns for UI and dynamic content.
metadata:
  author: Bingify
  version: "1.0"
---

# Internationalization (i18n)

このスキルは、Bingifyの多言語対応とメッセージ管理をカバーします。

## 概要

Bingifyはnext-intlを使用して、英語 (en) と日本語 (ja) をサポートしています。

## ロケール別ルート

```text
/                   # 英語版ホーム
/dashboard          # 英語版ダッシュボード
/ja/                # 日本語版ホーム
/ja/dashboard       # 日本語版ダッシュボード
```

## メッセージファイル

### messages/ja.JSON

```json
{
  "common": {
    "app_name": "Bingify",
    "sign_in": "ログイン",
    "home": "ホーム"
  }
}
```

## クライアントコンポーネント

```tsx
"use client";

import { useTranslations } from "next-intl";

export function Dashboard() {
  const t = useTranslations("dashboard");
  return <h1>{t("title")}</h1>;
}
```

## サーバーコンポーネント

```tsx
import { getTranslations } from "next-intl/server";

export async function Page() {
  const t = await getTranslations("dashboard");
  return <h1>{t("title")}</h1>;
}
```

## 言語選択

```tsx
"use client";

import { useLocale } from "next-intl";
import { useRouter } from "next-intl/navigation";

export function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();

  return (
    <button onClick={() => router.push("/", { locale: "ja" })}>日本語</button>
  );
}
```

## 参考

- [next-intl公式ドキュメント](https://next-intl.dev/)
- [STYLE_GUIDE.md](../../../docs/STYLE_GUIDE.md)
- [GLOSSARY.md](../../../docs/GLOSSARY.md)
