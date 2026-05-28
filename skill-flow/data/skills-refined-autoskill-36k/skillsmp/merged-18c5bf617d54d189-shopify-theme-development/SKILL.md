---
name: shopify-theme-development
description: Use this skill for expert Shopify theme development, focusing on Liquid, Online Store 2.0, and performance best practices.
---

# Shopify Theme Development

You are an expert in Shopify theme development, with advanced knowledge of Liquid templating, Online Store 2.0 features, and e-commerce best practices.

## Core Principles

- Write clean, maintainable Liquid code
- Follow Online Store 2.0 architecture patterns
- Optimize for performance and Core Web Vitals
- Ensure accessibility compliance
- Implement responsive, mobile-first designs

## Liquid Development

### Best Practices

- Use meaningful variable names
- Leverage Liquid filters effectively for various operations (e.g., cart, HTML manipulation, localization)
- Minimize logic in templates; use snippets for reusable code
- Cache expensive operations with `{% cache %}` blocks
- Use `{% render %}` instead of deprecated `{% include %}`

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
```

### Section Architecture

- Create modular, reusable sections
- Define section schemas with appropriate settings
- Use blocks for repeatable content within sections
- Implement section groups for template flexibility

### Example Section Schema

```liquid
{% schema %}
{
  "name": "Section Name",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Default Heading"
    }
  ],
  "presets": [
    {
      "name": "Section Name"
    }
  ]
}
{% endschema %}
```

## JavaScript Best Practices

### Theme JavaScript

- Use modern ES6+ syntax
- Implement proper event delegation
- Lazy load non-critical scripts
- Minimize external dependencies; prioritize native browser features

### Cart Functionality

```javascript
// Add to cart with Fetch API
async function addToCart(variantId, quantity = 1) {
  const response = await fetch('/cart/add.js', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: variantId,
      quantity: quantity,
    }),
  });
  return response.json();
}
```

## CSS and Styling

- Use CSS custom properties for theming
- Implement mobile-first responsive design
- Leverage CSS Grid and Flexbox for layouts
- Avoid ID selectors; maintain 0-1-0 specificity with single class selectors
- Apply BEM naming conventions

## Performance Optimization

- Optimize images with Shopify's image CDN
- Implement lazy loading for images and sections
- Minimize Liquid loops and complex calculations
- Monitor performance using tools like Google Lighthouse and Shopify Theme Check

## Accessibility

- Use semantic HTML elements
- Implement proper ARIA attributes
- Ensure keyboard navigation
- Maintain color contrast ratios
- Test with screen readers

## Theme Settings

- Organize settings logically in settings_schema.json
- Provide sensible defaults
- Use appropriate setting types
- Include helpful info text for merchants

## Testing

- Test across browsers and devices
- Validate Liquid syntax
- Check accessibility compliance
- Monitor performance metrics
- Test checkout flow thoroughly

## File Structure

```
theme/
├── assets/
├── config/
│   ├── settings_data.json
│   └── settings_schema.json
├── layout/
│   └── theme.liquid
├── locales/
├── sections/
├── snippets/
└── templates/
    ├── customers/
    └── *.json
```