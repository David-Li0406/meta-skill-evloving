---
name: shopify-app-bridge
description: Use this skill when you need to embed your app in the Shopify Admin and interact with the host interface, including showing toasts, modals, and handling navigation.
---

# Shopify App Bridge Skill

Shopify App Bridge is a library that allows you to embed your app directly inside the Shopify Admin. It provides a way to communicate with the host environment to trigger actions and navigation.

> [!NOTE]
> This skill focuses on **Shopify App Bridge v3 (NPM package)** and **App Bridge CDN (v4)** patterns. Always check which version the project is using, as many React apps still use `@shopify/app-bridge-react` (v3/v4 wrapper).

## Core Concepts

- **Host**: The Shopify Admin (web or mobile).
- **Client**: Your embedded app.
- **Actions**: Messages sent to the host to trigger UI elements (Toast, Modal) or navigation.

## Setup & Initialization

### Using CDN (App Bridge v4 - Recommended)

In modern Shopify apps, the preferred method is using the CDN script. This automatically exposes the `shopify` global variable, which is the primary entry point for all actions.

```html
<script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
<script>
  shopify.config = {
    apiKey: 'YOUR_API_KEY',
    host: new URLSearchParams(location.search).get("host"),
    forceRedirect: true,
  };
</script>
```

### Debugging & Exploration

Once initialized, the `shopify` global variable is available in your browser console.

> [!TIP]
> **Explore functionality**:
> 1. Open Chrome Developer Console in the Shopify Admin.
> 2. Switch the frame context to your app's iframe.
> 3. Type `shopify` to see all available methods and configurations.

### Using `@shopify/app-bridge-react` (Legacy/Specific Use Cases)

If you are strictly using React components or need the Provider context for deeply nested legacy components:

```jsx
import { Provider } from '@shopify/app-bridge-react';
// ... configuration setup
```

## Common Actions

### Toast

Display a temporary success or error message.

```javascript
shopify.toast.show('Product saved');
```

### Modal

Open a modal dialog.

```javascript
const modal = await shopify.modal.show({
  title: 'My Modal',
  message: 'Hello world',
  footer: {
    buttons: [
      { label: 'Ok', primary: true, id: 'ok-btn' }
    ]
  }
});
```