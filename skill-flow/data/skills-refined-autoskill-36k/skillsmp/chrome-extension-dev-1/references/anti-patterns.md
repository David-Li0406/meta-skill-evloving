# Chrome拡張機能開発のアンチパターン

このドキュメントは、Chrome拡張機能開発において避けるべきアンチパターンと、その改善方法をまとめたものです。

## 目次

- [状態管理の問題](#状態管理の問題)
- [メッセージパッシングの問題](#メッセージパッシングの問題)
- [セキュリティ上の問題](#セキュリティ上の問題)
- [非同期処理の問題](#非同期処理の問題)
- [パーミッション管理の問題](#パーミッション管理の問題)
- [TypeScript使用時の問題](#typescript使用時の問題)

---

## 状態管理の問題

### ❌ グローバル変数に状態を保存

Service Workerは一時的なもので、いつでも停止される可能性があります。グローバル変数に状態を保存すると、データが失われます。

```typescript
// ❌ 悪い例
let userSettings = {
  theme: 'dark',
  language: 'ja'
};

chrome.runtime.onMessage.addListener(({ type, settings }) => {
  if (type === 'update-settings') {
    userSettings = settings; // Service Workerが停止すると失われる
  }
});
```

**問題点:**
- Service Workerが停止すると、`userSettings`の値が失われる
- 拡張機能の再起動時に状態が初期化される

**✅ 改善方法:**

```typescript
// ✅ 良い例
chrome.runtime.onMessage.addListener(async ({ type, settings }) => {
  if (type === 'update-settings') {
    await chrome.storage.local.set({ userSettings: settings });
  }
});

// データの取得
async function getUserSettings() {
  const { userSettings } = await chrome.storage.local.get(['userSettings']);
  return userSettings || { theme: 'light', language: 'en' }; // デフォルト値
}
```

---

### ❌ onSuspendだけに頼った状態保存

`runtime.onSuspend`は必ずしも実行されるとは限りません（クラッシュ時など）。

```typescript
// ❌ 悪い例
let importantData = [];

chrome.runtime.onSuspend.addListener(() => {
  // クラッシュ時には実行されない可能性がある
  chrome.storage.local.set({ importantData });
});
```

**✅ 改善方法:**

```typescript
// ✅ 良い例: データ変更時に即座に保存
async function addData(newItem: unknown) {
  const { importantData = [] } = await chrome.storage.local.get(['importantData']);
  importantData.push(newItem);
  await chrome.storage.local.set({ importantData }); // 即座に保存
}
```

---

## メッセージパッシングの問題

### ❌ ポートを適切にクローズしない

メッセージポートをクローズしないと、Service Workerがアンロードされません。

```typescript
// ❌ 悪い例
const port = chrome.runtime.connect({ name: "persistent-connection" });

port.onMessage.addListener((msg) => {
  console.log(msg);
  // ポートをクローズしない → メモリリーク
});
```

**✅ 改善方法:**

```typescript
// ✅ 良い例
const port = chrome.runtime.connect({ name: "persistent-connection" });

port.onMessage.addListener((msg) => {
  console.log(msg);

  if (msg.type === 'close') {
    port.disconnect();
  }
});

// 切断の監視
port.onDisconnect.addListener(() => {
  console.log("Port disconnected");
});
```

---

### ❌ sendResponseを同期的に使用

非同期処理でsendResponseを使用する場合、`true`を返さないとレスポンスが送信されません。

```typescript
// ❌ 悪い例
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => {
      sendResponse(data); // 動作しない
    });
  // trueを返していない
});
```

**✅ 改善方法:**

```typescript
// ✅ 良い例
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => {
      sendResponse(data);
    })
    .catch(error => {
      sendResponse({ error: error.message });
    });

  return true; // 非同期レスポンスを示す
});
```

**✅ より良い例（async/await）:**

```typescript
// ✅ より良い例
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  (async () => {
    try {
      const response = await fetch('https://api.example.com/data');
      const data = await response.json();
      sendResponse(data);
    } catch (error) {
      sendResponse({ error: (error as Error).message });
    }
  })();

  return true;
});
```

---

## セキュリティ上の問題

### ❌ innerHTMLで外部データを表示

外部から取得したデータを`innerHTML`で表示すると、XSSの脆弱性があります。

```typescript
// ❌ 悪い例
const response = await fetch("https://api.example.com/data.json");
const jsonData = await response.json();
document.getElementById("resp")!.innerHTML = jsonData; // XSS脆弱性
```

**問題点:**
- 攻撃者が悪意のあるスクリプトを注入できる
- CSPで保護されていない場合、スクリプトが実行される

**✅ 改善方法:**

```typescript
// ✅ 良い例1: textContentを使用
const response = await fetch("https://api.example.com/data.json");
const jsonData = await response.json();
document.getElementById("resp")!.textContent = jsonData;

// ✅ 良い例2: JSON.parseを使用
const response = await fetch("https://api.example.com/data.json");
const jsonData = await response.json();
const resp = JSON.parse(jsonData);
// respを安全に使用

// ✅ 良い例3: DOMメソッドを使用
const element = document.createElement('div');
element.textContent = jsonData;
document.getElementById("resp")!.appendChild(element);
```

---

### ❌ CSPを緩和しすぎる

CSPを緩和しすぎると、セキュリティリスクが高まります。

```json
// ❌ 悪い例
{
  "content_security_policy": {
    "extension_pages": "script-src 'self' 'unsafe-eval' https:; object-src *;"
  }
}
```

**問題点:**
- `'unsafe-eval'`は`eval()`を許可し、XSSのリスクを高める
- `https:`はすべてのHTTPSドメインからのスクリプト読み込みを許可
- `object-src *`はすべてのオブジェクトソースを許可

**✅ 改善方法:**

```json
// ✅ 良い例: 最小限のCSP
{
  "content_security_policy": {
    "extension_pages": "script-src 'self' 'wasm-unsafe-eval'; object-src 'self';"
  }
}
```

---


## 非同期処理の問題

### ❌ lastErrorのチェック漏れ

コールバックベースのAPIでは、`chrome.runtime.lastError`をチェックしないとエラーが見逃されます。

```typescript
// ❌ 悪い例
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  // lastErrorをチェックしていない
  chrome.tabs.sendMessage(tabs[0].id, { type: 'hello' });
});
```

**✅ 改善方法:**

```typescript
// ✅ 良い例
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  if (chrome.runtime.lastError) {
    console.error(chrome.runtime.lastError.message);
    return;
  }

  if (tabs[0]?.id) {
    chrome.tabs.sendMessage(tabs[0].id, { type: 'hello' });
  }
});
```

**✅ より良い例（Promise使用）:**

```typescript
// ✅ より良い例
async function sendMessageToActiveTab() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab?.id) {
      await chrome.tabs.sendMessage(tab.id, { type: 'hello' });
    }
  } catch (error) {
    console.error('Error:', error);
  }
}
```

---

### ❌ Promiseとコールバックの混在

PromiseとコールバックAPIを混在させると、コードが読みにくくなります。

```typescript
// ❌ 悪い例
async function getData() {
  const { name } = await chrome.storage.local.get(['name']);

  chrome.tabs.query({ active: true }, (tabs) => {
    // Promiseとコールバックが混在
    chrome.tabs.sendMessage(tabs[0].id, { name });
  });
}
```

**✅ 改善方法:**

```typescript
// ✅ 良い例: すべてPromiseで統一
async function getData() {
  const { name } = await chrome.storage.local.get(['name']);
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (tab?.id) {
    await chrome.tabs.sendMessage(tab.id, { name });
  }
}
```

---

## パーミッション管理の問題

### ❌ 過剰なパーミッション要求

必要以上のパーミッションを要求すると、ユーザーの信頼を失います。

```json
// ❌ 悪い例
{
  "permissions": [
    "tabs",
    "bookmarks",
    "history",
    "cookies",
    "<all_urls>",
    "webRequest",
    "webRequestBlocking"
  ]
}
```

**問題点:**
- 必要のない権限を要求している
- `<all_urls>`はすべてのサイトへのアクセスを許可
- ユーザーに警告が表示される

**✅ 改善方法:**

```json
// ✅ 良い例: 必要最小限のパーミッション
{
  "permissions": [
    "storage",
    "activeTab"
  ],
  "optional_permissions": [
    "bookmarks"  // ユーザーが機能を有効にした時のみ要求
  ],
  "host_permissions": [
    "https://api.example.com/*"  // 特定のドメインのみ
  ]
}
```

---

### ❌ オプショナルパーミッションの誤用

オプショナルパーミッションをインストール時に要求すると、意味がありません。

```typescript
// ❌ 悪い例
chrome.runtime.onInstalled.addListener(async () => {
  // インストール直後にオプショナルパーミッションを要求
  await chrome.permissions.request({
    permissions: ['tabs']
  });
});
```

**✅ 改善方法:**

```typescript
// ✅ 良い例: ユーザーが機能を使う時に要求
async function enableAdvancedFeature() {
  const granted = await chrome.permissions.request({
    permissions: ['tabs']
  });

  if (granted) {
    // 機能を有効化
    console.log("Advanced feature enabled");
  } else {
    console.log("Permission denied");
  }
}

// ユーザーのボタンクリックなどで呼び出す
document.getElementById('enable-btn')?.addEventListener('click', enableAdvancedFeature);
```

## まとめ

Chrome拡張機能開発における主なアンチパターン:

### 状態管理
- グローバル変数に状態を保存しない
- onSuspendだけに頼らない

### メッセージパッシング
- ポートを適切にクローズする
- 非同期レスポンスでは`true`を返す

### セキュリティ
- innerHTMLで外部データを表示しない
- CSPを緩和しすぎない

### 非同期処理
- lastErrorをチェックする
- PromiseとコールバックAPIを混在させない

### パーミッション
- 過剰なパーミッションを要求しない
- オプショナルパーミッションは適切なタイミングで要求する

これらのアンチパターンを避けることで、より安全で保守性の高いChrome拡張機能を開発できます。
