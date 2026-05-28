# Chrome拡張機能開発のベストプラクティス

このドキュメントは、Google公式ドキュメントと@types/chromeライブラリに基づいた、Chrome拡張機能開発におけるベストプラクティスをまとめたものです。

## 目次

- [Manifest V3の採用](#manifest-v3の採用)
- [状態管理とデータ永続化](#状態管理とデータ永続化)
- [メッセージパッシング](#メッセージパッシング)
- [セキュリティ対策](#セキュリティ対策)
- [非同期処理とPromise](#非同期処理とpromise)
- [パーミッション管理](#パーミッション管理)

---

## Manifest V3の採用

### 推奨事項

Manifest V3を使用することで、セキュリティ、プライバシー、パフォーマンスが向上します。

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0"
}
```

### Service Workerの理解

Manifest V3では、バックグラウンドページの代わりにService Workerを使用します。Service Workerは一時的なもので、イベント駆動型で動作します。

```json
{
  "background": {
    "service_worker": "background.js"
  }
}
```

**重要な特徴:**
- Service Workerは必要に応じて起動・停止される一時的な存在
- グローバル変数は信頼できない（リセットされる可能性がある）
- 状態は`chrome.storage` APIを使用して永続化する必要がある

---

## 状態管理とデータ永続化

### ✅ 推奨: Storage APIを使用

Service Workerはいつでも停止される可能性があるため、グローバル変数ではなく`chrome.storage` APIを使用して状態を管理します。

```typescript
// ❌ 非推奨: グローバル変数（Manifest V2スタイル）
let savedName: string | undefined = undefined;

chrome.runtime.onMessage.addListener(({ type, name }) => {
  if (type === "set-name") {
    savedName = name;
  }
});

chrome.action.onClicked.addListener((tab) => {
  chrome.tabs.sendMessage(tab.id, { name: savedName });
});
```

```typescript
// ✅ 推奨: Storage API（Manifest V3スタイル）
chrome.runtime.onMessage.addListener(({ type, name }) => {
  if (type === "set-name") {
    chrome.storage.local.set({ name });
  }
});

chrome.action.onClicked.addListener(async (tab) => {
  const { name } = await chrome.storage.local.get(["name"]);
  chrome.tabs.sendMessage(tab.id, { name });
});
```

### データ永続化のタイミング

重要なデータは定期的に保存し、拡張機能がクラッシュした場合でもデータが失われないようにします。

```typescript
// 定期的にデータを保存
chrome.storage.local.set({ variable: variableInformation });
```

### onSuspendイベントの活用

Service Workerがアンロードされる前に最終クリーンアップが必要な場合は、`runtime.onSuspend`イベントを使用します。ただし、データの永続化には`chrome.storage` APIを使用することが推奨されます。

```typescript
chrome.runtime.onSuspend.addListener(() => {
  console.log("Unloading.");
  chrome.action.setBadgeText({ text: "" });
});
```

---

## メッセージパッシング

### 一時的なメッセージ送信

一時的なメッセージには`chrome.runtime.sendMessage()`を使用します。

```typescript
// Content Script
chrome.runtime.sendMessage('get-user-data', (response) => {
  console.log('received user data', response);
  initializeUI(response);
});

// Service Worker
type User = {
  username: string;
}

const user: User = {
  username: 'demo-user'
};

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message === 'get-user-data') {
    sendResponse(user);
  }
});
```

### 長期的な接続

長期的なメッセージングには`chrome.runtime.connect()`を使用します。

```typescript
// Content Script
const port = chrome.runtime.connect({ name: "myPort" });
port.postMessage({ greeting: "hello" });

port.onMessage.addListener((response) => {
  console.log("Received response:", response);
});

// Service Worker
chrome.runtime.onConnect.addListener((port) => {
  if (port.name === "myPort") {
    port.onMessage.addListener((msg) => {
      console.log("Received message:", msg);
      port.postMessage({ response: "hi there!" });
    });
  }
});
```

### ポートの適切なクローズ

メッセージポートを使用する場合は、すべてのポートが適切にクローズされていることを確認します。Service Workerは、すべてのポートがクローズされるまでアンロードされません。

```typescript
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message === 'goodbye') {
    port.disconnect();
  }
});

// ポートの切断を監視
chrome.runtime.Port.onDisconnect.addListener((port) => {
  console.log("Port disconnected:", port.name);
});
```

---

## セキュリティ対策

### Content Security Policy (CSP)

拡張機能のセキュリティを確保するため、適切なContent Security Policyを設定します。

**基本的なCSP:**

```json
{
  "content_security_policy": {
    "extension_pages": "default-src 'self'"
  }
}
```

**最小限のCSP（Manifest V3）:**

```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self' 'wasm-unsafe-eval'; object-src 'self';"
  }
}
```

**開発時（unpackedのみ）のlocalhost許可:**

```text
script-src 'self' 'wasm-unsafe-eval' 'inline-speculation-rules' http://localhost:* http://127.0.0.1:*; object-src 'self';
```

## 非同期処理とPromise

### Chrome 95以降: Promiseサポート

Chrome 95以降、Manifest V3版の`chrome.storage` APIはPromiseを返すようになりました。

```typescript
// ✅ 推奨: async/awaitを使用
async function getUserData() {
  const { name } = await chrome.storage.local.get(["name"]);
  return name;
}
```

## パーミッション管理

### 最小権限の原則

必要最小限のパーミッションのみをリクエストします。

```json
{
  "permissions": [
    "storage",
    "activeTab"
  ]
}
```

### オプショナルパーミッション

ユーザーが必要な機能を有効にするまで、パーミッションをリクエストしないようにします。

```json
{
  "optional_permissions": [
    "tabs",
    "bookmarks"
  ]
}
```

```typescript
// ランタイムでパーミッションをリクエスト
async function requestPermission() {
  const granted = await chrome.permissions.request({
    permissions: ['tabs']
  });

  if (granted) {
    console.log("Permission granted");
  } else {
    console.log("Permission denied");
  }
}
```

### activeTabパーミッション

`activeTab`パーミッションは、ユーザーの操作に応じて一時的なホストパーミッションを付与します。警告なしで使用できます。

```json
{
  "permissions": ["activeTab"],
  "action": {
    "default_title": "Click to activate"
  }
}
```

---
## まとめ

Chrome拡張機能開発では、以下のポイントに注意することで、安全で保守性の高いコードを書くことができます。

1. **Manifest V3**を採用し、Service Workerの特性を理解する
2. **Storage API**を使用して状態を永続化する
3. **適切なメッセージパッシング**パターンを選択する
4. **CSP**と**XSS対策**を実装する
5. **Promise**と**async/await**を活用する
6. **最小権限の原則**に従ってパーミッションを管理する

これらのベストプラクティスに従うことで、セキュアで信頼性の高いChrome拡張機能を開発できます。

型安全性については、[type-safety.md](./type-safety.md)を参照してください。
