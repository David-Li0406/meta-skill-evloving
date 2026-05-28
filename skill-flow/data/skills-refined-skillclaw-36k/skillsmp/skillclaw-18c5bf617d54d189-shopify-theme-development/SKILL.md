---
name: shopify-theme-development
description: Use this skill when you need to develop or optimize Shopify themes using Liquid, Online Store 2.0, and best practices for performance and user experience.
---

# Shopify Theme Development

You are an expert in Shopify theme development, with advanced knowledge of Liquid templating, Online Store 2.0 features, and e-commerce best practices.

## Core Principles

- Write clean, maintainable Liquid code.
- Follow Online Store 2.0 architecture patterns.
- Optimize for performance and Core Web Vitals.
- Ensure accessibility compliance.
- Implement responsive, mobile-first designs.

## Liquid Templating

### Best Practices

- Use meaningful variable names.
- Leverage Liquid filters effectively for operations like cart handling, string transformations, and formatting.
- Minimize logic in templates; use snippets for reusable code.
- Cache expensive operations with `{% cache %}` blocks.
- Use `{% render %}` instead of deprecated `{% include %}`.

### Common Patterns

```liquid
{% comment %} Product card snippet {% endcomment %}
{% render 'product-card', product: product, show_vendor: true %}

{% comment %} Conditional rendering {% endcomment %}
{% if product.available %}
  <button type="submit">Add to Cart</button>
{% else %}
  <button disabled>Sold Out</button>
{% endif %}

{% comment %} Loop with forloop object {% endcomment %}
{% for product in collection.products limit: 12 %}
  {% render 'product-card', product: product %}
{% endfor %}
```

## Online Store 2.0

### Section Architecture

- Create modular, reusable sections.
- Define section schemas with appropriate settings.
- Use blocks for repeatable content within sections.
- Implement section groups for template flexibility.

### Section Schema Example

```liquid
{% schema %}
{
  "name": "Featured Collection",
  "settings": [
    {
      "type": "collection",
      "id": "collection",
      "label": "Collection"
    },
    {
      "type": "range",
      "id": "products_to_show",
      "min": 2,
      "max": 12,
      "step": 2,
      "default": 4,
      "label": "Products to show"
    }
  ],
  "presets": [
    {
      "name": "Featured Collection"
    }
  ]
}
{% endschema %}
```

### JSON Templates

- Use JSON templates for flexible page layouts.
- Define template sections in JSON format.
- Allow merchants to customize through the theme editor.

## JavaScript Best Practices

### Theme JavaScript

- Use modern ES6+ syntax.
- Implement proper event delegation.
- Lazy load non-critical scripts.
- Use Shopify's Section Rendering API for dynamic updates.

### Cart Functionality Example

```javascript
// Add to cart with Fetch API
async function addToCart(variantId, quantity) {
  // Implementation here
}
```

## UX Principles

- Keep all text translated using locale files with sensible keys.
- Settings should be simple, clear, and non-repetitive.
- Group related settings under headings.
- Use conditional settings judiciously (max 2 levels deep).

## CSS Guidelines

- Avoid ID selectors; maintain 0-1-0 specificity with single class selectors.
- Use CSS variables for redundancy reduction.
- Apply BEM naming conventions.
- Use mobile-first media queries with `screen` descriptor.

## HTML Standards

- Use semantic HTML with modern features.
- Ensure interactive elements remain focusable.
- Use `tabindex="0"` sparingly.

## Conclusion

By following these guidelines, you can create high-quality, performant Shopify themes that enhance user experience and meet e-commerce best practices.