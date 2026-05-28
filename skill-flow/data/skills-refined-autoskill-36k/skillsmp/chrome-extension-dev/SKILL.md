---
name: chrome-extension-dev
description: Guide for developing modern Chrome extensions using Manifest V3. Use when creating, modifying, or troubleshooting Chrome extensions. Covers setting up projects with manifest.json, implementing service workers, content scripts, and popups, managing permissions and security, building with action API and declarativeNetRequest, and Chrome Web Store publication. Includes 2025 best practices and MV3 migration patterns.
---

# Chrome Extension Development

Build modern Chrome extensions using Manifest V3, the current 2025 standard for secure, performant browser extensions.

## Quick Start

**Create a minimal extension:**
1. Create `manifest.json` with MV3 format
2. Add service worker for background logic
3. Create UI (popup, side panel, or content script)
4. Load unpacked in `chrome://extensions`

**See [asset templates](assets/) for complete project structure.**

## Core Concepts

### Manifest V3 Architecture

**Service Workers** replace background pages:
- Event-driven, terminate when idle
- No DOM access
- Use chrome.storage and chrome.runtime for data

**Content Scripts:**
- Run in web page context
- Can read/modify DOM
- Communicate via messaging API

**Action API:**
- Toolbar icon interactions
- Popup windows
- Badge text/icons

### Development Workflow

1. **Initialize project structure**
2. **Configure manifest.json** (see [MANIFEST.md](references/MANIFEST.md))
3. **Implement components** (service worker, content scripts, popups)
4. **Load and test locally** in developer mode
5. **Debug** using Chrome DevTools
6. **Package** for Chrome Web Store

## Common Extension Patterns

### Popup Extension

**Structure:**
```
extension/
├── manifest.json
├── popup.html
├── popup.js
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

**manifest.json:**
```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0",
  "action": {
    "default_popup": "popup.html"
  }
}
```

### Content Script Extension

**manifest.json:**
```json
{
  "manifest_version": 3,
  "name": "Page Modifier",
  "version": "1.0",
  "content_scripts": [{
    "matches": ["https://example.com/*"],
    "js": ["content.js"],
    "run_at": "document_idle"
  }]
}
```

**Message passing to service worker:**
```javascript
// content.js
chrome.runtime.sendMessage({action: "getData"}, (response) => {
  console.log(response.data);
});

// background.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getData") {
    sendResponse({data: "example"});
  }
});
```

### Background Service Worker

**manifest.json:**
```json
{
  "manifest_version": 3,
  "name": "Background Task",
  "version": "1.0",
  "background": {
    "service_worker": "background.js"
  },
  "permissions": ["storage", "alarms"]
}
```

**background.js:**
```javascript
chrome.alarms.create("refresh", {periodInMinutes: 60});
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "refresh") {
    // Perform periodic task
  }
});
```

### Declarative Net Request

**manifest.json:**
```json
{
  "manifest_version": 3,
  "name": "Request Blocker",
  "version": "1.0",
  "permissions": ["declarativeNetRequest"],
  "declarative_net_request": {
    "rule_resources": [{
      "id": "ruleset",
      "enabled": true,
      "path": "rules.json"
    }]
  }
}
```

**rules.json:**
```json
[{
  "id": 1,
  "priority": 1,
  "action": {"type": "block"},
  "condition": {
    "domains": ["example.com"],
    "urlFilter": "||tracker.com/*"
  }
}]
```

## Permissions Best Practices

**Use minimum required permissions:**
- **Active permissions:** Declare in manifest.json
- **Optional permissions:** Request at runtime with `chrome.permissions.request()`

**Common permissions:**
- `storage` - chrome.storage API
- `activeTab` - current tab access (user gesture required)
- `scripting` - dynamic script injection
- `alarms` - scheduled tasks
- `tabs` - tab management

## Key APIs

### Storage API
```javascript
// Save data
chrome.storage.local.set({key: "value"});

// Retrieve data
chrome.storage.local.get(["key"], (result) => {
  console.log(result.key);
});
```

### Tabs API
```javascript
// Query tabs
chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
  const currentTab = tabs[0];
});

// Send message to content script
chrome.tabs.sendMessage(tabId, {action: "execute"});
```

### Scripting API
```javascript
// Inject content script dynamically
chrome.scripting.executeScript({
  target: {tabId: tabId},
  files: ["content.js"]
});
```

## Security Guidelines

**Critical MV3 requirements:**
- ✅ All code bundled with extension
- ❌ No remotely hosted JavaScript
- ❌ No eval() or inline scripts
- ✅ Content Security Policy required

**CSP example:**
```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'"
  }
}
```

## Testing & Debugging

**Load unpacked extension:**
1. Navigate to `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select extension directory

**Debug service worker:**
1. Go to `chrome://extensions`
2. Find extension, click "service worker" link
3. Opens DevTools for background script

**Debug content script:**
1. Open web page where script runs
2. Open DevTools (F12)
3. Content script appears in Sources panel

**Debug popup:**
1. Right-click extension icon
2. Select "Inspect popup"

## Migration from V2 to V3

**Key changes:**
1. Background pages → Service workers
2. `chrome.webRequest` → `declarativeNetRequest`
3. `chrome.extension.getBackgroundPage()` → Use messaging
4. Persistent state → chrome.storage

**See [MV3 Migration Guide](references/MIGRATION.md) for detailed steps.**

## Chrome Web Store Publication

**Requirements:**
- Single, clearly defined purpose
- Detailed store listing (screenshots, description)
- Privacy policy if collecting data
- Comply with [Developer Program Policies](https://developer.chrome.com/docs/webstore/program-policies)

**Package extension:**
1. Zip all extension files (not the folder itself)
2. Upload to Chrome Web Store Developer Dashboard
3. Complete store listing
4. Submit for review

## Resources

### Detailed Documentation
- **[Manifest Configuration](references/MANIFEST.md)** - Complete manifest.json reference
- **[MV3 Migration Guide](references/MIGRATION.md)** - V2 to V3 migration patterns
- **[API Reference](references/APIS.md)** - All Chrome extension APIs

### Asset Templates
- **[Basic extension](assets/basic-extension/)** - Minimal popup extension
- **[Content script](assets/content-script-extension/)** - Page modification example
- **[Service worker](assets/service-worker-extension/)** - Background processing example
- **[Declarative rules](assets/declarative-request-extension/)** - Network filtering example

### Tools
- **[Chrome Extensions Developer Hub](https://developer.chrome.com/docs/extensions)** - Official documentation
- **[Extension Playground](https://extension-workshop.com/)** - Tutorials and examples
