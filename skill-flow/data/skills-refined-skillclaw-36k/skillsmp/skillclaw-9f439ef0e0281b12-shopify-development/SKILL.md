---
name: shopify-development
description: Use this skill when building Shopify applications, extensions, and themes, or when integrating with Shopify APIs and services.
---

# Skill body

## Overview

This skill provides guidance on building Shopify apps, extensions, and themes using the Shopify CLI, GraphQL/REST APIs, Polaris UI components, and Liquid templating.

## When to Use

Use this skill when you need to:
- Build Shopify apps or extensions
- Customize checkout, admin, or POS interfaces
- Develop themes using Liquid
- Integrate with Shopify APIs for product, order, and customer management
- Implement webhooks or billing features

## Development Workflow

### Prerequisites

Install the Shopify CLI:

```bash
npm install -g @shopify/cli@latest
```

### Creating a New App

1. Initialize a new app:

   ```bash
   shopify app init
   ```

2. Start the development server:

   ```bash
   shopify app dev
   ```

3. Deploy the app:

   ```bash
   shopify app deploy
   ```

### Generating Extensions

To create different types of extensions, use the following commands:

```bash
shopify app generate extension --type checkout_ui_extension
shopify app generate extension --type admin_action
shopify app generate extension --type pos_ui_extension
```

### Theme Development

1. Initialize a new theme:

   ```bash
   shopify theme init
   ```

2. Start local preview:

   ```bash
   shopify theme dev
   ```

3. Pull the live theme:

   ```bash
   shopify theme pull --live
   ```

4. Push to the development theme:

   ```bash
   shopify theme push --development
   ```

## Access Scopes

Configure access scopes in `shopify.app.toml`:

```toml
[access_scopes]
scopes = "read_products,write_products,read_orders,write_orders,read_customers"
```

### Common Scopes

- `read_products`, `write_products`: Access to product catalog
- `read_orders`, `write_orders`: Order management capabilities
- `read_customers`, `write_customers`: Access to customer data