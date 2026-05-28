---
name: shopify-polaris-design
description: Use this skill when designing and implementing Shopify Admin interfaces with the Polaris Design System to ensure a native, accessible, and professional look and feel for Shopify Merchants.
---

# Core Principles

1. **Merchant-Focused**: Design for efficiency and clarity, as merchants use these tools to run their business.
2. **Native Feel**: Ensure the app feels like a natural extension of the Shopify Admin, avoiding foreign design patterns unless absolutely necessary.
3. **Accessibility**: Maintain accessibility by using semantic components (e.g., `Button`, `Link`, `TextField`) instead of custom `div` implementations.
4. **Predictability**: Follow standard Shopify patterns, such as placing save buttons in the Contextual Save Bar and centering primary content.

## Technical Implementation

### Dependencies
- `@shopify/polaris`
- `@shopify/polaris-icons`
- `@shopify/app-bridge-react` (for navigation, title bar, toasts, save bar)

### Fundamental Components

- **AppProvider**: Wrap all Polaris apps in `<AppProvider i18n={enTranslations}>`.
- **Page**: Use as the top-level container for a route, always setting `title` and `primaryAction` (if applicable).
  ```jsx
  <Page title="Products" primaryAction={{content: 'Add product', onAction: handleAdd}}>
  ```
- **Layout**: Structure content using `Layout` and `Layout.Section`.
    - `Layout.AnnotatedSection`: For settings pages (Title/Description on left, Card on right).
    - `Layout.Section`: Use standard Full (default), 1/2 (`variant="oneHalf"`), or 1/3 (`variant="oneThird"`) width columns.
- **Card**: The primary container for content pieces. Group related information in a Card.
    - Use `BlockStack` (vertical) or `InlineStack` (horizontal) for internal layout within a Card.
    - Avoid using `Card.Section` as it is deprecated; use `BlockStack` with `gap`.

### Data Display

- **IndexTable**: For lists of objects (Products, Orders) with bulk actions and filtering, replacing the older `ResourceList` for complex table cases.
- **LegacyCard** + **ResourceList**: Still valid for simple lists where table headers aren't needed.
- **DataTable**: For displaying tabular data with advanced features.