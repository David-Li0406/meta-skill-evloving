# Manifest V3 Configuration Reference

Complete reference for `manifest.json` in Chrome Extensions with Manifest V3.

## Required Fields

```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "1.0.0"
}
```

**manifest_version**: Always `3` for current extensions

**name**: Short, descriptive identifier (max 45 chars)

**version**: Version string (1-4 dot-separated numbers)

## Recommended Fields

```json
{
  "description": "Brief description of the extension",
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

## Background Service Worker

```json
{
  "background": {
    "service_worker": "background.js",
    "type": "module"
  }
}
```

**service_worker**: Path to background script

**type**: Optional - "module" for ES modules, defaults to classic script

## Content Scripts

```json
{
  "content_scripts": [
    {
      "matches": ["https://*.example.com/*"],
      "js": ["content.js"],
      "css": ["styles.css"],
      "run_at": "document_idle"
    }
  ]
}
```

**matches**: URL patterns (required)
- `*://*/*` - All protocols and domains
- `https://*.example.com/*` - Specific domain
- `file://*/*` - Local files

**js**: Array of JavaScript files (in injection order)

**css**: Array of CSS files

**run_at**: When to inject
- `document_start` - Before CSS
- `document_end` - After DOM ready
- `document_idle` (default) - Browser choice

## Action API

```json
{
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png"
    },
    "default_title": "Tooltip text"
  }
}
```

## Permissions

```json
{
  "permissions": ["storage", "activeTab", "alarms"],
  "host_permissions": ["https://api.example.com/*"]
}
```

**Common permissions:**
- `activeTab` - Current tab on user action
- `storage` - chrome.storage API
- `alarms` - Scheduled tasks
- `tabs` - Tab metadata
- `scripting` - Dynamic script injection
- `declarativeNetRequest` - Network filtering
- `declarativeNetRequestWithHostAccess` - Filtering with host access

**host_permissions**: URL patterns for API access

## Declarative Net Request

```json
{
  "permissions": ["declarativeNetRequest"],
  "declarative_net_request": {
    "rule_resources": [
      {
        "id": "ruleset_1",
        "enabled": true,
        "path": "rules.json"
      }
    ]
  }
}
```

## Options Page

```json
{
  "options_page": "options.html",
  "options_ui": {
    "page": "options.html",
    "open_in_tab": false
  }
}
```

## Side Panel

```json
{
  "side_panel": {
    "default_path": "sidepanel.html"
  }
}
```

## Web Accessible Resources

```json
{
  "web_accessible_resources": [
    {
      "resources": ["images/*.png"],
      "matches": ["https://*.example.com/*"]
    }
  ]
}
```

## Content Security Policy

```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'",
    "sandbox": "sandbox allow-scripts; script-src 'self' 'unsafe-eval'"
  }
}
```

**extension_pages**: For extension pages

**sandbox**: For sandboxed pages

## Minimum Chrome Version

```json
{
  "minimum_chrome_version": "88"
}
```

## Developer Information

```json
{
  "author": "Developer Name",
  "homepage_url": "https://example.com"
}
```

## Example: Complete Manifest

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "description": "Does something useful",
  "version": "1.0.0",
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "action": {
    "default_popup": "popup.html",
    "default_title": "My Extension"
  },
  "background": {
    "service_worker": "background.js"
  },
  "permissions": ["storage", "activeTab"],
  "host_permissions": ["https://api.example.com/*"],
  "content_scripts": [
    {
      "matches": ["https://*.example.com/*"],
      "js": ["content.js"]
    }
  ],
  "options_page": "options.html"
}
```
