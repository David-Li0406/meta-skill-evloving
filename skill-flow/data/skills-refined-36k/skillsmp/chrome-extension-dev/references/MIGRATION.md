# Manifest V2 to V3 Migration Guide

Step-by-step guide for migrating Chrome extensions from Manifest V2 to V3.

## Core Architectural Changes

### 1. Background Pages → Service Workers

**V2 - Background Page:**
```json
{
  "background": {
    "scripts": ["background.js"],
    "persistent": true
  }
}
```

**V3 - Service Worker:**
```json
{
  "background": {
    "service_worker": "background.js"
  }
}
```

**Key differences:**
- Service workers are event-driven (terminate when idle)
- No DOM access
- Cannot use `window`, `document`, `localStorage`
- Use `chrome.storage` instead of `localStorage`
- Use `chrome.runtime.getURL()` for file paths

**Code changes:**
```javascript
// V2 - persistent background
let variable = "value";

// V3 - service worker (use storage)
chrome.storage.local.set({variable: "value"});
chrome.storage.local.get(["variable"], (result) => {
  console.log(result.variable);
});
```

### 2. Web Request → Declarative Net Request

**V2 - webRequest API:**
```json
{
  "permissions": ["webRequest", "webRequestBlocking", "<all_urls>"]
}
```

```javascript
// V2
chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    return {cancel: true};
  },
  {urls: ["<all_urls>"]},
  ["blocking"]
);
```

**V3 - declarativeNetRequest:**
```json
{
  "permissions": ["declarativeNetRequest"],
  "declarative_net_request": {
    "rule_resources": [{
      "id": "ruleset_1",
      "enabled": true,
      "path": "rules.json"
    }]
  }
}
```

```json
// rules.json
[{
  "id": 1,
  "priority": 1,
  "action": {"type": "block"},
  "condition": {
    "urlFilter": "||example.com/*",
    "resourceTypes": ["main_frame", "sub_frame"]
  }
}]
```

**For dynamic modifications** (not possible with declarative rules), use `declarativeNetRequestWithHostAccess` and `declarativeNetRequestFeedback` permissions.

### 3. Remote Code Prohibition

**V2 - Allowed remote code:**
```javascript
// This is NO LONGER ALLOWED in V3
fetch('https://example.com/script.js')
  .then(response => response.text())
  .then(script => eval(script));
```

**V3 - All code must be bundled:**
```javascript
// Bundle all JavaScript in extension package
importScripts('helper.js'); // OK
importScripts('https://example.com/helper.js'); // NOT OK
```

**No inline scripts:**
```html
<!-- V2 - inline script (NOT ALLOWED in V3) -->
<script>console.log('inline');</script>

<!-- V3 - external script required -->
<script src="popup.js"></script>
```

### 4. Content Security Policy

**V2:**
```json
{
  "content_security_policy": "script-src 'self' https://example.com; object-src 'self'"
}
```

**V3:**
```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'",
    "sandbox": "sandbox allow-scripts allow-forms; script-src 'self' 'unsafe-inline' 'unsafe-eval'"
  }
}
```

### 5. Host Permissions

**V2:**
```json
{
  "permissions": ["<all_urls>", "tabs", "storage"]
}
```

**V3:**
```json
{
  "permissions": ["tabs", "storage"],
  "host_permissions": ["<all_urls>"]
}
```

**Use specific URLs when possible:**
```json
{
  "host_permissions": [
    "https://api.example.com/*",
    "https://*.github.com/*"
  ]
}
```

### 6. Browser Action → Action API

**V2:**
```json
{
  "browser_action": {
    "default_popup": "popup.html",
    "default_title": "Extension Name"
  }
}
```

**V3:**
```json
{
  "action": {
    "default_popup": "popup.html",
    "default_title": "Extension Name"
  }
}
```

**Code changes:**
```javascript
// V2
chrome.browserAction.onClicked.addListener(...);
chrome.browserAction.setTitle({title: "Text"});

// V3
chrome.action.onClicked.addListener(...);
chrome.action.setTitle({title: "Text"});
```

### 7. Tab API Changes

```javascript
// V2 - callback-based
chrome.tabs.query({active: true}, (tabs) => {
  console.log(tabs[0].url);
});

// V3 - promise-based (recommended)
chrome.tabs.query({active: true}).then((tabs) => {
  console.log(tabs[0].url);
});
```

### 8. Messaging API Changes

```javascript
// V2
chrome.runtime.sendMessage(message, (response) => {
  console.log(response);
});

// V3 - promise-based
chrome.runtime.sendMessage(message).then((response) => {
  console.log(response);
});
```

## Migration Checklist

- [ ] Update `manifest_version` to `3`
- [ ] Replace `background.scripts` with `background.service_worker`
- [ ] Remove `persistent: true` from background
- [ ] Replace `localStorage` with `chrome.storage`
- [ ] Replace `chrome.browser_action` with `chrome.action`
- [ ] Move URL permissions from `permissions` to `host_permissions`
- [ ] Replace `webRequest` with `declarativeNetRequest` if blocking
- [ ] Remove all remote code loading
- [ ] Update CSP to V3 format
- [ ] Replace callbacks with promises where possible
- [ ] Test extension thoroughly after migration

## Common Migration Patterns

### Storing State Across Sessions

**V2:**
```javascript
// In background page (persistent)
let state = {};
chrome.runtime.onMessage.addListener((message) => {
  state[message.key] = message.value;
});
```

**V3:**
```javascript
// In service worker (non-persistent)
chrome.runtime.onMessage.addListener((message) => {
  chrome.storage.local.set({[message.key]: message.value});
});

// Retrieve on startup
self.addEventListener('activate', () => {
  chrome.storage.local.get(null, (state) => {
    // Restore state
  });
});
```

### Opening Extension Pages

**V2:**
```javascript
const bgPage = chrome.extension.getBackgroundPage();
bgPage.document.getElementById('element').textContent = 'text';
```

**V3:**
```javascript
// Use messaging to communicate with service worker
chrome.runtime.sendMessage({action: 'updateElement', text: 'text'});

// Or open new extension page
chrome.tabs.create({url: 'page.html'});
```

## Testing After Migration

1. **Load unpacked extension** in developer mode
2. **Test all core functionality**
3. **Check console for errors** (service worker, content scripts, popups)
4. **Verify permissions** are correctly requested
5. **Test across browser restarts** (service worker lifecycle)
6. **Monitor memory usage** (service workers should terminate)

## Resources

- [Official Migration Guide](https://developer.chrome.com/docs/extensions/develop/migrate)
- [Manifest V3 Overview](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3)
- [Declarative Net Request Guide](https://developer.chrome.com/docs/extensions/reference/declarativeNetRequest)
