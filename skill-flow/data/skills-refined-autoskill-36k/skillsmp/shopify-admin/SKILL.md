---
name: shopify-admin
description: Fetch data from Shopify Admin API. Use when querying products, orders, customers, files, images, videos, or uploading content to Shopify.
---

# Shopify Admin API

Fetch data from your Shopify store using the Admin GraphQL API.

## Requirements

Set these environment variables:

- `STORE` - Your Shopify store name (e.g., `my-store` for `my-store.myshopify.com`)
- `ADMIN_API_TOKEN` - Your Admin API access token

## Fetch Products

```bash
bash .claude/skills/shopify-admin/scripts/fetch-products.sh
```

Options:

- `--limit N` - Number of products (default: 10)
- `--query "search term"` - Filter products by title

Examples:

```bash
# Fetch 10 products
bash .claude/skills/shopify-admin/scripts/fetch-products.sh

# Fetch 25 products
bash .claude/skills/shopify-admin/scripts/fetch-products.sh --limit 25

# Search for specific products
bash .claude/skills/shopify-admin/scripts/fetch-products.sh --query "coffee"
```

## Fetch Files (Images/Videos)

```bash
bash .claude/skills/shopify-admin/scripts/fetch-files.sh
```

Options:

- `--limit N` - Number of files (default: 20)
- `--type TYPE` - Filter by type: `IMAGE`, `VIDEO`, `DOCUMENT`, or `ALL` (default)

Examples:

```bash
# Fetch all files
bash .claude/skills/shopify-admin/scripts/fetch-files.sh

# Fetch only images
bash .claude/skills/shopify-admin/scripts/fetch-files.sh --type IMAGE

# Fetch 50 videos
bash .claude/skills/shopify-admin/scripts/fetch-files.sh --type VIDEO --limit 50
```

## Upload Files

```bash
bash .claude/skills/shopify-admin/scripts/upload-file.sh <file-path> [alt-text]
```

Supported formats: jpg, png, gif, webp, svg, mp4, mov, webm, pdf

Examples:

```bash
# Upload an image
bash .claude/skills/shopify-admin/scripts/upload-file.sh ./hero.jpg "Hero banner image"

# Upload a video
bash .claude/skills/shopify-admin/scripts/upload-file.sh ./promo.mp4 "Product promo video"
```

## Custom Queries

For custom GraphQL queries, use the base script:

```bash
bash .claude/skills/shopify-admin/scripts/query.sh 'YOUR_GRAPHQL_QUERY'
```
