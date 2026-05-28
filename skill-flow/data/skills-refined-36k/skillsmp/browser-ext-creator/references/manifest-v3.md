# Manifest V3 リファレンス

## 目次

1. [Chrome と Firefox の違い](#chrome-と-firefox-の違い)
2. [permissions 一覧](#permissions-一覧)
3. [Content Scripts](#content-scripts)
4. [Background Scripts](#background-scripts)
5. [メッセージング](#メッセージング)

## Chrome と Firefox の違い

### manifest.json 比較

```json
// Chrome Manifest V3
{
  "manifest_version": 3,
  "name": "Extension",
  "version": "1.0.0",
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html"
  }
}
```

```json
// Firefox Manifest V3
{
  "manifest_version": 3,
  "name": "Extension",
  "version": "1.0.0",
  "browser_specific_settings": {
    "gecko": {
      "id": "extension@example.com",
      "strict_min_version": "109.0"
    }
  },
  "background": {
    "scripts": ["background.js"]
  },
  "action": {
    "default_popup": "popup.html"
  }
}
```

### 主な差異

| 項目 | Chrome | Firefox |
| ---- | ------ | ------- |
| Background | `service_worker` | `scripts` (配列) |
| 固有設定 | 不要 | `browser_specific_settings` 必須 |
| API namespace | `chrome.*` | `browser.*` (Promise対応) |

## permissions 一覧

### よく使う permissions

| Permission | 説明 |
| ---------- | ---- |
| `storage` | `chrome.storage` API の使用 |
| `tabs` | タブ情報へのアクセス |
| `activeTab` | クリック時にアクティブタブへの一時的アクセス |
| `scripting` | `chrome.scripting` API（動的スクリプト注入） |
| `alarms` | `chrome.alarms` API（タイマー機能） |
| `notifications` | 通知の表示 |
| `contextMenus` | 右クリックメニューの追加 |
| `clipboardRead` | クリップボード読み取り |
| `clipboardWrite` | クリップボード書き込み |

### host_permissions

特定ドメインへのアクセス権限：

```json
{
  "host_permissions": [
    "https://example.com/*",
    "https://*.example.org/*"
  ]
}
```

## Content Scripts

### 宣言的注入（manifest.json）

```json
{
  "content_scripts": [
    {
      "matches": ["https://example.com/*"],
      "js": ["content-script.js"],
      "css": ["content.css"],
      "run_at": "document_idle"
    }
  ]
}
```

### `run_at` オプション

| 値 | タイミング |
| -- | ---------- |
| `document_start` | DOM構築前 |
| `document_end` | DOM構築後、リソース読み込み前 |
| `document_idle` | DOM + リソース読み込み後（デフォルト） |

### 動的注入（chrome.scripting）

```javascript
// background.js
chrome.scripting.executeScript({
  target: { tabId: tabId },
  files: ['content-script.js']
});
```

## Background Scripts

### Service Worker の制約（Chrome）

- 永続的な状態を持てない（アイドル後に停止）
- DOM アクセス不可
- `setTimeout` / `setInterval` 非推奨（`chrome.alarms` を使用）

### 状態の永続化

```javascript
// 状態を storage に保存
chrome.storage.local.set({ state: currentState });

// Service Worker 起動時に復元
chrome.storage.local.get(['state'], (result) => {
  if (result.state) {
    currentState = result.state;
  }
});
```

## メッセージング

### Content Script ↔ Background

```javascript
// Content Script から送信
chrome.runtime.sendMessage({ action: 'getData', id: 123 }, (response) => {
  console.log(response);
});

// Background で受信
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getData') {
    fetchData(request.id).then(sendResponse);
    return true; // 非同期レスポンスを有効化
  }
});
```

### Tab へのメッセージ送信

```javascript
// Background から特定タブに送信
chrome.tabs.sendMessage(tabId, { action: 'update' }, (response) => {
  console.log(response);
});

// Content Script で受信
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'update') {
    updateUI();
    sendResponse({ success: true });
  }
});
```
