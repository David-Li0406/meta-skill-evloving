---
name: shopify-remix-template
description: Use this skill when you want to develop Shopify apps using the official Shopify Remix Template, covering app structure, authentication, API usage, and deployment.
---

# Shopify Remix Template Guide

This skill provides a guide for building Shopify apps using the official **Shopify Remix App Template**. This template is the recommended starting point for most new Shopify embedded apps (though React Router is the future direction, Remix is still widely used and supported).

## 🚀 Getting Started

To create a new app using the Remix template, run:

```bash
git clone https://github.com/Shopify/shopify-app-template-remix.git
```

## 📂 Project Structure

A typical Remix app structure:

*   `app/`
    *   `routes/`: File-system based routing.
        *   `app._index.tsx`: The main dashboard page.
        *   `app.tsx`: The root layout for the authenticated app.
        *   `webhooks.tsx`: Webhook handler.
    *   `shopify.server.ts`: **Critical**. Initializes the Shopify API client, authentication, and session storage (Redis).
    *   `db.server.ts`: Database connection (Mongoose).
    *   `models/`: Mongoose models (e.g., `Session.ts`, `Shop.ts`).
    *   `root.tsx`: The root component for the entire application.
*   `shopify.app.toml`: Main app configuration file.

## 🔐 Authentication & Sessions

The template uses `@shopify/shopify-app-remix` to handle authentication automatically.

### `shopify.server.ts`
This file exports an `authenticate` object used in loaders and actions. It is configured to use **Redis** for session storage.

```typescript
import { shopifyApp } from "@shopify/shopify-app-remix/server";
import { RedisSessionStorage } from "@shopify/shopify-app-session-storage-redis";

const sessionDb = new RedisSessionStorage(
  new URL(process.env.REDIS_URL!)
);

const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY,
  apiSecretKey: process.env.SHOPIFY_API_SECRET,
  appUrl: process.env.SHOPIFY_APP_URL,
  scopes: process.env.SCOPES?.split(","),
  apiVersion: "2025-10",
  sessionStorage: sessionDb,
  isEmbeddedApp: true,
});

export const authenticate = shopify.authenticate;
export const apiVersion = "2025-10";
export const addDocumentResponseHeaders = shopify.addDocumentResponseHeaders;
```

### Usage in Loaders (Data Fetching)
Protect routes and get the session context:

```typescript
import { json } from "@remix-run/node";
import { authenticate } from "../shopify.server";

export const loader = async ({ request }) => {
  // Your loader logic here
};
```