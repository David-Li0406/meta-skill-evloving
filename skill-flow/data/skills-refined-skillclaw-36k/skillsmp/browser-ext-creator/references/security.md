# セキュリティガイド

## 目次

1. [XSS 防止](#xss-防止)
2. [最小権限の原則](#最小権限の原則)
3. [Content Security Policy](#content-security-policy)
4. [外部通信のセキュリティ](#外部通信のセキュリティ)
5. [ストレージセキュリティ](#ストレージセキュリティ)

## XSS 防止

### 安全なDOM操作

```javascript
// NG: innerHTML は XSS の原因
element.innerHTML = userInput;

// OK: textContent を使用
element.textContent = userInput;

// OK: DOM API で要素作成
const span = document.createElement('span');
span.textContent = userInput;
container.appendChild(span);
```

### DOMPurify によるサニタイズ

HTML を挿入する必要がある場合は DOMPurify を使用：

```javascript
// DOMPurify をバンドルして使用
import DOMPurify from 'dompurify';

const cleanHTML = DOMPurify.sanitize(untrustedHTML);
element.innerHTML = cleanHTML;
```

### 禁止事項

Manifest V3 では以下が禁止：

```javascript
// NG: eval
eval('console.log("hello")');

// NG: new Function
const fn = new Function('return 1 + 1');

// NG: innerHTML + スクリプト
element.innerHTML = '<script>alert("xss")</script>';
```

## 最小権限の原則

### 必要な権限のみ要求

```json
// NG: 過剰な権限
{
  "permissions": ["tabs", "history", "bookmarks", "downloads"],
  "host_permissions": ["<all_urls>"]
}

// OK: 必要最小限
{
  "permissions": ["storage"],
  "host_permissions": ["https://specific-site.com/*"]
}
```

### activeTab の活用

ユーザーアクションに応じた一時的な権限：

```json
{
  "permissions": ["activeTab", "scripting"]
}
```

クリック時のみアクティブタブにアクセス可能。

## Content Security Policy

### Manifest V3 のデフォルト CSP

```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'"
  }
}
```

### サンドボックスページ

外部コンテンツを表示する場合：

```json
{
  "sandbox": {
    "pages": ["sandbox.html"]
  }
}
```

## 外部通信のセキュリティ

### HTTPS のみ使用

```javascript
// NG: HTTP
fetch('http://api.example.com/data');

// OK: HTTPS
fetch('https://api.example.com/data');
```

### API キーの保護

```javascript
// NG: コードにハードコード
const API_KEY = 'sk-1234567890';

// OK: storage から取得
const { apiKey } = await chrome.storage.sync.get(['apiKey']);
```

### レスポンスの検証

```javascript
const response = await fetch(url);

// ステータスコードを確認
if (!response.ok) {
  throw new Error(`HTTP error: ${response.status}`);
}

// Content-Type を確認
const contentType = response.headers.get('content-type');
if (!contentType?.includes('application/json')) {
  throw new Error('Invalid content type');
}

const data = await response.json();
```

## ストレージセキュリティ

### 機密データの取り扱い

```javascript
// API キーは sync で同期（Chrome アカウント認証済み環境）
await chrome.storage.sync.set({ apiKey: userApiKey });

// 大量データや一時データは local
await chrome.storage.local.set({ cache: largeData });
```

### ストレージの暗号化

本当に機密性の高いデータは Web Crypto API で暗号化：

```javascript
const encryptData = async (data, key) => {
  const encoder = new TextEncoder();
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    encoder.encode(data)
  );
  return { iv, encrypted };
};
```

### 入力バリデーション

```javascript
const validateApiKey = (key) => {
  if (typeof key !== 'string') return false;
  if (key.length < 10 || key.length > 100) return false;
  if (!/^[a-zA-Z0-9_-]+$/.test(key)) return false;
  return true;
};

const saveApiKey = async (key) => {
  if (!validateApiKey(key)) {
    throw new Error('Invalid API key format');
  }
  await chrome.storage.sync.set({ apiKey: key });
};
```
