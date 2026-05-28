---
name: shopify-extensions
description: Use this skill when you want to build and manage Shopify Extensions using the latest Shopify CLI and APIs.
---

# Shopify Extensions Guide

This skill provides a comprehensive guide to building Shopify Extensions. Extensions allow you to integrate your app's functionality directly into Shopify's user interfaces (Admin, Checkout, Online Store, POS) and backend logic.

## 📚 Official References (Latest)

*   **App Extensions Overview:** [Shopify.dev - App Extensions](https://shopify.dev/docs/apps/build/app-extensions)
*   **List of All Extensions:** [Shopify.dev - Extension List](https://shopify.dev/docs/apps/build/app-extensions/list)
*   **Checkout UI Extensions:** [Shopify.dev - Checkout UI Extensions](https://shopify.dev/docs/api/checkout-ui-extensions)
*   **Admin UI Extensions:** [Shopify.dev - Admin UI Extensions](https://shopify.dev/docs/api/admin-extensions)
*   **Theme App Extensions:** [Shopify.dev - Theme App Extensions](https://shopify.dev/docs/apps/online-store/theme-app-extensions)
*   **Shopify Functions:** [Shopify.dev - Shopify Functions](https://shopify.dev/docs/api/functions)

## 🛠️ Prerequisites

*   **Shopify CLI:** Ensure you are using the latest version of Shopify CLI.
    ```bash
    npm install -g @shopify/cli@latest
    ```
*   **Shopify App:** Extensions must be part of a Shopify App.

## 🚀 Common Extension Types

### 1. Admin UI Extensions
Embed your app into the Shopify Admin interface.

*   **Action Extensions:** Add transactional workflows (modals) to resource pages (Orders, Products, Customers).
    *   *Usage:* "More actions" menu.
*   **Block Extensions:** Embed contextual information as cards directly on resource pages.
    *   *Usage:* Inline cards on Product/Order details.
*   **Configuration:** Defined in `shopify.extension.toml`.
    ```toml
    [[extensions]]
    type = "ui_extension"
    name = "product-action"
    handle = "product-action"
    
    [[extensions.targeting]]
    target = "admin.product-details.action.render"
    module = "./src/ActionExtension.jsx"
    ```

### 2. Checkout UI Extensions
Customize the checkout flow (requires Shopify Plus for some features).

*   **Targets:** Information, Shipping, Payment, Order Summary, Thank You Page, Order Status Page.
*   **Capabilities:**
    *   Show banners/upsells.
    *   Collect additional data (attributes).
    *   Validate input.
*   **UI Components:** Use Shopify's restricted component library.