# Chrome拡張機能開発における型安全性

このドキュメントは、TypeScriptを使用したChrome拡張機能開発における型安全性の実践方法をまとめたものです。

## 目次

- [@types/chromeの活用](#typeschromeの活用)
- [chrome.storage API](#chromestorage-api)
- [chrome.runtime.sendMessage API](#chromeruntimesendmessage-api)
- [chrome.runtime.onMessage リスナー](#chromeruntimeonmessage-リスナー)
- [ランタイムデータ検証にはValibotを使う](#ランタイムデータ検証にはvalibotを使う)

---

## @types/chromeの活用

### 基本的な使い方

`@types/chrome`パッケージは、Chrome APIの型定義を提供します。

```bash
pnpm add -D @types/chrome
```

```typescript
// 型定義が利用可能
const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
// tab: chrome.tabs.Tab | undefined

if (tab?.id) {
  await chrome.tabs.sendMessage(tab.id, { type: 'hello' });
}
```

### chrome.runtime.lastError

Manifest V3ではPromiseを使うため、`chrome.runtime.lastError`を使う機会は減りますが、コールバックAPIを使う場合は注意が必要です。

```typescript
// Manifest V3: Promiseを使う（推奨）
try {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  console.log(tab);
} catch (error) {
  console.error('Error:', error);
}

// コールバックを使う場合（非推奨）
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  if (chrome.runtime.lastError) {
    console.error(chrome.runtime.lastError.message);
    return;
  }
  console.log(tabs[0]);
});
```

---

## chrome.storage API

### ジェネリクスで型指定

`chrome.storage.local.get()`と`chrome.storage.local.set()`はジェネリクスで型安全に使えます。

```typescript
// @types/chromeの型定義
get<T = { [key: string]: unknown }>(
  keys?: NoInferX<keyof T> | Array<NoInferX<keyof T>> | Partial<NoInferX<T>> | null,
): Promise<T>;

set<T = { [key: string]: any }>(items: Partial<T>): Promise<void>;
```

### 使用例

```typescript
type AppStorage = {
  userName: string;
  theme: 'light' | 'dark';
  count: number;
}

// 保存
await chrome.storage.local.set<AppStorage>({
  userName: 'Alice',
  theme: 'dark',
  count: 42,
});

// 取得
const result = await chrome.storage.local.get<AppStorage>(['userName', 'theme']);
// result: AppStorage（ただし各プロパティはundefinedの可能性あり）

// デフォルト値を使う
const userName = result.userName ?? 'Anonymous';
const theme = result.theme ?? 'light';
```

### 注意: ランタイム検証は別途必要

ジェネリクスで型を指定しても、実際のStorageデータが正しい型であることは保証されません。データが破損している可能性や、過去のバージョンとの互換性を考慮する必要があります。

**推奨: Valibotを使ったランタイム検証（後述）**

---

## chrome.runtime.sendMessage API

### ジェネリクスで型指定

`chrome.runtime.sendMessage()`はジェネリクス`<M, R>`でメッセージ型とレスポンス型を指定できます。

```typescript
// @types/chromeの型定義
export function sendMessage<M = any, R = any>(message: M, options?: MessageOptions): Promise<R>;
```

### 使用例

```typescript
type GetUserDataMessage = {
  type: 'getUserData';
  userId: number;
}

type GetUserDataResponse = {
  userName: string;
  age: number;
}

// 型安全なメッセージ送信
const response = await chrome.runtime.sendMessage<GetUserDataMessage, GetUserDataResponse>({
  type: 'getUserData',
  userId: 123,
});

console.log(response.userName); // 型安全
```

---

## chrome.runtime.onMessage リスナー

### メッセージリスナーの型定義

`chrome.runtime.onMessage`の型定義は以下の通りです。

```typescript
// @types/chromeの型定義
export const onMessage: events.Event<
  (message: any, sender: MessageSender, sendResponse: (response?: any) => void) => void
>;
```

メッセージは`any`型なので、受信側で型安全にするには工夫が必要です。

### 型安全なメッセージハンドリング（Valibot推奨）

ランタイムデータ検証にはValibotを使うことを推奨します（後述）。

```typescript
import * as v from 'valibot';

// メッセージスキーマ定義
const GetUserDataMessageSchema = v.object({
  type: v.literal('getUserData'),
  userId: v.number(),
});

const SetThemeMessageSchema = v.object({
  type: v.literal('setTheme'),
  theme: v.picklist(['light', 'dark']),
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // getUserDataメッセージ
  const getUserData = v.safeParse(GetUserDataMessageSchema, message);
  if (getUserData.success) {
    const { userId } = getUserData.output;
    sendResponse({ userName: 'Alice', age: 30 });
    return true;
  }

  // setThemeメッセージ
  const setTheme = v.safeParse(SetThemeMessageSchema, message);
  if (setTheme.success) {
    const { theme } = setTheme.output;
    chrome.storage.local.set({ theme });
    sendResponse({ success: true });
    return true;
  }

  // 未知のメッセージ
  sendResponse({ error: 'Unknown message type' });
  return true;
});
```

---

## ランタイムデータ検証にはValibotを使う

### なぜValibotが必要か

TypeScriptの型定義はコンパイル時のみ有効で、ランタイムでは検証されません。以下のような場合、ランタイム検証が必要です:

- `chrome.storage`から取得したデータ
- `chrome.runtime.onMessage`で受信したメッセージ
- 外部APIからのレスポンス
- Content Scriptからのメッセージ

**Valibotの利点:**
- 軽量（Zodと比べてバンドルサイズが小さい）
- モジュラー設計で必要な機能だけインポート可能
- 高速なバリデーション
- TypeScript型推論が優れている

### Valibotのインストール

```bash
pnpm add valibot
```

### 基本的な使い方

```typescript
import * as v from 'valibot';

// スキーマ定義
const UserSettingsSchema = v.object({
  theme: v.picklist(['light', 'dark']),
  language: v.string(),
  notifications: v.optional(v.boolean()),
});

// TypeScript型を自動生成
type UserSettings = v.InferOutput<typeof UserSettingsSchema>;

// ランタイム検証
async function getUserSettings(): Promise<UserSettings> {
  const result = await chrome.storage.local.get(['userSettings']);

  // パース（検証失敗時は例外をスロー）
  try {
    return v.parse(UserSettingsSchema, result.userSettings);
  } catch (error) {
    console.error('Invalid user settings:', error);
    // デフォルト値
    const defaultSettings: UserSettings = {
      theme: 'light',
      language: 'en',
    };
    await chrome.storage.local.set({ userSettings: defaultSettings });
    return defaultSettings;
  }
}

// または safeParse（例外をスローしない）
async function getUserSettingsSafe(): Promise<UserSettings> {
  const result = await chrome.storage.local.get(['userSettings']);
  const parsed = v.safeParse(UserSettingsSchema, result.userSettings);

  if (parsed.success) {
    return parsed.output;
  } else {
    console.error('Validation errors:', parsed.issues);
    const defaultSettings: UserSettings = {
      theme: 'light',
      language: 'en',
    };
    await chrome.storage.local.set({ userSettings: defaultSettings });
    return defaultSettings;
  }
}
```

### chrome.storageとValibotの組み合わせ

```typescript
import * as v from 'valibot';

// Storageスキーマ定義
const AppStorageSchema = v.object({
  userName: v.string(),
  theme: v.picklist(['light', 'dark']),
  lastSyncTime: v.number(),
});

type AppStorage = v.InferOutput<typeof AppStorageSchema>;

// 型安全な保存
async function saveSettings(settings: AppStorage): Promise<void> {
  await chrome.storage.local.set(settings);
}

// 型安全な取得（ランタイム検証付き）
async function loadSettings(): Promise<AppStorage | null> {
  const result = await chrome.storage.local.get(['userName', 'theme', 'lastSyncTime']);
  const parsed = v.safeParse(AppStorageSchema, result);

  if (parsed.success) {
    return parsed.output;
  } else {
    console.error('Invalid storage data:', parsed.issues);
    return null;
  }
}
```

### メッセージングとValibotの組み合わせ

```typescript
import * as v from 'valibot';

// メッセージスキーマ定義
const GetDataMessageSchema = v.object({
  type: v.literal('getData'),
  id: v.number(),
});

const GetDataResponseSchema = v.object({
  data: v.string(),
  timestamp: v.number(),
});

type GetDataMessage = v.InferOutput<typeof GetDataMessageSchema>;
type GetDataResponse = v.InferOutput<typeof GetDataResponseSchema>;

// Content Script: メッセージ送信
async function sendGetDataMessage(id: number): Promise<GetDataResponse> {
  const message: GetDataMessage = { type: 'getData', id };
  const response = await chrome.runtime.sendMessage(message);

  // レスポンスを検証
  return v.parse(GetDataResponseSchema, response);
}

// Background Script: メッセージ受信
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  const parsed = v.safeParse(GetDataMessageSchema, message);

  if (parsed.success) {
    const { id } = parsed.output;
    const response: GetDataResponse = {
      data: `Data for ${id}`,
      timestamp: Date.now(),
    };
    sendResponse(response);
    return true;
  }

  sendResponse({ error: 'Invalid message format' });
  return true;
});
```

---

## まとめ

Chrome拡張機能開発における型安全性のベストプラクティス:

1. **@types/chromeを活用**して、Chrome APIの型定義を利用する
2. **chrome.storage APIはジェネリクスで型指定**する
3. **chrome.runtime.sendMessageはジェネリクスで型指定**する
4. **ランタイムデータ検証にはValibotを使う**（型ガードの手書きは避ける）
5. **Manifest V3ではPromiseを使う**（コールバックAPIは避ける）

Valibotを使うことで、軽量かつ高速にランタイム検証を実装でき、型定義と検証ロジックを一箇所で管理できます。
