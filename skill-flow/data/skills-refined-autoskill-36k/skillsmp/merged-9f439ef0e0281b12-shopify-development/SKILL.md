---
name: shopify-development
description: Use this skill when building Shopify applications, extensions, and themes using GraphQL/REST APIs, Shopify CLI, Polaris UI components, and Liquid templating.
---

# Shopify Development Skill

This skill provides guidance for building on the Shopify platform, including apps, extensions, themes, and API integrations.

## Core Components

- **Shopify CLI**: Development workflow tool.
- **GraphQL Admin API**: Primary API for data operations (recommended).
- **REST Admin API**: Legacy API (maintenance mode).
- **Polaris UI**: Design system for consistent interfaces.
- **Liquid**: Template language for themes.

## When to Build What

### Build an App When:
- Integrating external services.
- Adding functionality across multiple stores.
- Building merchant-facing admin tools.
- Managing store data programmatically.
- Implementing complex business logic.
- Charging for functionality.

### Build an Extension When:
- Customizing checkout flow.
- Adding fields/features to admin pages.
- Creating POS actions for retail.
- Implementing discount/payment/shipping rules.
- Extending customer account pages.

### Build a Theme When:
- Creating custom storefront design.
- Building unique shopping experiences.
- Customizing product/collection pages.
- Implementing brand-specific layouts.
- Modifying homepage/content pages.

### Combination Approach:
**App + Theme Extension**: Use when backend logic and storefront UI are needed together.

## Quick Start

### Prerequisites

Install Shopify CLI:
```bash
npm install -g @shopify/cli@latest
```

### Create New App

```bash
shopify app init          # Initialize app
shopify app dev           # Start development server
shopify app deploy        # Deploy app to Shopify
```

### Generate Extension

```bash
shopify app generate extension --type checkout_ui_extension
```

### Theme Development

```bash
shopify theme init        # Initialize theme
shopify theme dev         # Start local preview
shopify theme pull --live # Pull live theme
shopify theme push --development  # Push to development theme
```

## Access Scopes

Configure in `shopify.app.toml`:
```toml
[access_scopes]
scopes = "read_products,write_products,read_orders,write_orders,read_customers"
```

## GraphQL Patterns

### Query Products
```graphql
query GetProducts($first: Int!, $query: String) {
  products(first: $first, query: $query) {
    edges {
      node {
        id
        title
        handle
        variants(first: 5) {
          edges {
            node {
              id
              price
              inventoryQuantity
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Set Metafields
```graphql
mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
    }
    userErrors {
      field
      message
    }
  }
}
```

## Checkout Extension Example
```tsx
import {
  reactExtension,
  BlockStack,
  TextField,
  Checkbox,
  useApplyAttributeChange,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.checkout.block.render", () => (
  <GiftMessage />
));

function GiftMessage() {
  const [isGift, setIsGift] = useState(false);
  const [message, setMessage] = useState("");
  const applyAttributeChange = useApplyAttributeChange();

  useEffect(() => {
    if (isGift && message) {
      applyAttributeChange({
        type: "updateAttribute",
        key: "gift_message",
        value: message,
      });
    }
  }, [isGift, message]);

  return (
    <BlockStack spacing="loose">
      <Checkbox checked={isGift} onChange={setIsGift}>
        This is a gift
      </Checkbox>
      {isGift && (
        <TextField
          label="Gift Message"
          value={message}
          onChange={setMessage}
          multiline={3}
        />
      )}
    </BlockStack>
  );
}
```

## Best Practices

### API Usage
- Prefer GraphQL over REST for new development.
- Request only needed fields to reduce costs.
- Implement pagination for large datasets.
- Respect rate limits.

### Security
- Store API credentials in environment variables.
- Verify webhook signatures.
- Use OAuth for public apps.

### Performance
- Cache API responses when appropriate.
- Optimize images in themes.

## Troubleshooting

**Rate Limit Errors**: Monitor `X-Shopify-Shop-Api-Call-Limit` header and implement exponential backoff.

**Authentication Failures**: Verify access token validity and required scopes.

**Extension Not Appearing**: Check extension target and ensure app is installed.

## Resources

- [Shopify Developer Docs](https://shopify.dev/docs)
- [GraphQL Admin API Reference](https://shopify.dev/docs/api/admin-graphql)
- [Shopify CLI Reference](https://shopify.dev/docs/api/shopify-cli)
- [Polaris Design System](https://polaris.shopify.com)

**Note**: This skill covers Shopify platform as of January 2025. Refer to official documentation for the latest updates.