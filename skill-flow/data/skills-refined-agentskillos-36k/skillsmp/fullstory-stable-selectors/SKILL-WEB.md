---
name: fullstory-stable-selectors-web
version: v3
platform: web
sdk: fullstory-browser
description: Web implementation guide for stable selectors using HTML data-* attributes. Covers React, Angular, Vue, Svelte, Next.js, Astro, Solid.js, Web Components, and server-side templates. Includes TypeScript patterns and advanced scenarios.
parent_skill: fullstory-stable-selectors
related_skills:
  - fullstory-element-properties
  - fullstory-privacy-controls
  - fullstory-test-automation
---

# Fullstory Stable Selectors — Web Implementation

> **📚 Core Concepts**: See [SKILL.md](./SKILL.md) for naming conventions, taxonomy, and platform-agnostic principles.
> **📱 Mobile Implementation**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## Overview

This guide covers implementing stable selectors in **web applications** using HTML `data-*` attributes. These attributes provide stable, semantic identifiers that survive CSS-in-JS hash changes, build tool optimizations, and framework updates.

---

## Web-Specific Problem

Modern web build tools generate dynamic, unpredictable class names:

```html
<!-- What your code looks like -->
<button className={styles.primaryButton}>Add to Cart</button>

<!-- What renders in the browser -->
<button class="Button_primaryButton__x7Ks2">Add to Cart</button>
                                    ↑
                        This hash changes every build!
```

**Dynamic class names come from:**
- ❌ CSS Modules (hash suffixes)
- ❌ styled-components / Emotion (random class names)
- ❌ Tailwind CSS (class purging changes the set)
- ❌ Build optimizations (minification, renaming)
- ❌ Component libraries (internal naming conventions)
- ❌ Shadow DOM / Web Components (encapsulated styles)

---

## The Solution: data-* Attributes

Add stable `data-*` attributes that survive build changes:

```html
<!-- Before: Brittle selector -->
<button class="Button_primaryButton__x7Ks2">Add to Cart</button>

<!-- After: Stable selector -->
<button 
  class="Button_primaryButton__x7Ks2"
  data-component="ProductCard"
  data-element="add-to-cart-button"
>
  Add to Cart
</button>
```

**Benefits:**
- ✅ Survives all build changes
- ✅ Semantic and self-documenting
- ✅ Works in ANY web framework
- ✅ Enables reliable Fullstory CSS selector searches
- ✅ Powers defined elements and click maps
- ✅ No external plugins required

---

## Web Attribute Reference

### Primary Attributes

| Attribute | Purpose | Case | Example |
|-----------|---------|------|---------|
| `data-component` | Component boundary identifier | PascalCase | `ProductCard`, `CheckoutForm` |
| `data-element` | Element role within component | kebab-case | `add-to-cart`, `price-display` |

### Extended Attributes

| Attribute | Purpose | When to Use |
|-----------|---------|-------------|
| `data-action` | Describes what happens on interaction | Buttons, links, toggles |
| `data-state` | Current state of the element | Expandable, toggleable elements |
| `data-variant` | Visual or functional variant | A/B tests, feature flags |
| `data-testid` | Unified test/automation identifier | When aligning with E2E tests |

### Development Attributes (Strip in Production)

| Attribute | Purpose |
|-----------|---------|
| `data-source-file` | Source file reference for debugging |
| `data-source-line` | Line number for debugging |

---

## Framework Implementations

### React

```jsx
// ProductCard.jsx
function ProductCard({ product, onAddToCart }) {
  return (
    <div 
      data-component="ProductCard"
      data-element="card"
      className={styles.card}
    >
      <img 
        src={product.image} 
        alt={product.name}
        data-element="product-image"
      />
      
      <h3 data-element="product-name">{product.name}</h3>
      
      <span data-element="price">${product.price}</span>
      
      <button 
        data-element="add-to-cart"
        data-action="add-item"
        onClick={() => onAddToCart(product)}
      >
        Add to Cart
      </button>
    </div>
  );
}
```

#### React Helper Hook (Optional)

```jsx
// useStableSelector.js
export function useStableSelector(componentName) {
  return {
    root: {
      'data-component': componentName,
    },
    element: (name, action) => ({
      'data-element': name,
      ...(action && { 'data-action': action })
    }),
  };
}

// Usage
function ProductCard({ product }) {
  const sel = useStableSelector('ProductCard');
  
  return (
    <div {...sel.root} {...sel.element('card')}>
      <button {...sel.element('add-to-cart', 'add-item')}>
        Add to Cart
      </button>
    </div>
  );
}
```

---

### Angular

```html
<!-- product-card.component.html -->
<article 
  data-component="ProductCard"
  data-element="card"
  class="product-card"
>
  <img 
    [src]="product.image" 
    [alt]="product.name"
    data-element="product-image"
  />
  
  <h3 data-element="product-name">{{ product.name }}</h3>
  
  <span data-element="price">{{ product.price | currency }}</span>
  
  <button 
    data-element="add-to-cart"
    data-action="add-item"
    (click)="addToCart()"
  >
    Add to Cart
  </button>
</article>
```

#### Angular Directive (Optional)

```typescript
// stable-selector.directive.ts
import { Directive, ElementRef, Input, OnInit } from '@angular/core';

@Directive({
  selector: '[fsComponent], [fsElement]'
})
export class StableSelectorDirective implements OnInit {
  @Input() fsComponent: string;
  @Input() fsElement: string;
  @Input() fsAction: string;
  
  constructor(private el: ElementRef) {}
  
  ngOnInit() {
    if (this.fsComponent) {
      this.el.nativeElement.setAttribute('data-component', this.fsComponent);
    }
    if (this.fsElement) {
      this.el.nativeElement.setAttribute('data-element', this.fsElement);
    }
    if (this.fsAction) {
      this.el.nativeElement.setAttribute('data-action', this.fsAction);
    }
  }
}

// Usage in template
<div fsComponent="ProductCard" fsElement="card">
  <button fsElement="add-to-cart" fsAction="add-item">Add to Cart</button>
</div>
```

---

### Vue

```vue
<!-- ProductCard.vue -->
<template>
  <article 
    data-component="ProductCard"
    data-element="card"
    class="product-card"
  >
    <img 
      :src="product.image" 
      :alt="product.name"
      data-element="product-image"
    />
    
    <h3 data-element="product-name">{{ product.name }}</h3>
    
    <span data-element="price">{{ formatPrice(product.price) }}</span>
    
    <button 
      data-element="add-to-cart"
      data-action="add-item"
      @click="$emit('add-to-cart', product)"
    >
      Add to Cart
    </button>
  </article>
</template>

<script setup>
defineProps(['product']);
defineEmits(['add-to-cart']);
</script>
```

#### Vue Directive (Optional)

```javascript
// main.js
app.directive('fs', {
  mounted(el, binding) {
    const { component, element, action } = binding.value;
    if (component) el.setAttribute('data-component', component);
    if (element) el.setAttribute('data-element', element);
    if (action) el.setAttribute('data-action', action);
  }
});

// Usage in template
<div v-fs="{ component: 'ProductCard', element: 'card' }">
  <button v-fs="{ element: 'add-to-cart', action: 'add-item' }">Add to Cart</button>
</div>
```

---

### Svelte

```svelte
<!-- ProductCard.svelte -->
<article 
  data-component="ProductCard"
  data-element="card"
  class="product-card"
>
  <img 
    src={product.image} 
    alt={product.name}
    data-element="product-image"
  />
  
  <h3 data-element="product-name">{product.name}</h3>
  
  <span data-element="price">${product.price}</span>
  
  <button 
    data-element="add-to-cart"
    data-action="add-item"
    on:click={() => dispatch('addToCart', product)}
  >
    Add to Cart
  </button>
</article>

<script>
  import { createEventDispatcher } from 'svelte';
  export let product;
  const dispatch = createEventDispatcher();
</script>
```

---

### Next.js (App Router / React Server Components)

Server components work identically—data attributes render to HTML:

```tsx
// app/products/[id]/page.tsx (Server Component)
export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);
  
  return (
    <main data-component="ProductPage" data-element="page">
      <ProductDetails product={product} />
      <AddToCartButton productId={product.id} />
    </main>
  );
}

// Client component with interactivity
'use client';
function AddToCartButton({ productId }: { productId: string }) {
  const [loading, setLoading] = useState(false);
  
  return (
    <button
      data-component="AddToCartButton"
      data-element="trigger"
      data-action="add-to-cart"
      data-state={loading ? 'loading' : 'idle'}
      onClick={handleClick}
    >
      {loading ? 'Adding...' : 'Add to Cart'}
    </button>
  );
}
```

---

### Astro (Islands Architecture)

```astro
---
// ProductCard.astro
const { product } = Astro.props;
---

<article 
  data-component="ProductCard"
  data-element="card"
  data-product-id={product.id}
>
  <img src={product.image} data-element="product-image" />
  <h3 data-element="product-name">{product.name}</h3>
  
  <!-- Interactive island -->
  <AddToCartButton client:visible productId={product.id} />
</article>
```

---

### Solid.js

```tsx
// ProductCard.tsx
function ProductCard(props: { product: Product }) {
  return (
    <article data-component="ProductCard" data-element="card">
      <img src={props.product.image} data-element="product-image" />
      <h3 data-element="product-name">{props.product.name}</h3>
      <button
        data-element="add-to-cart"
        data-action="add-item"
        onClick={() => addToCart(props.product)}
      >
        Add to Cart
      </button>
    </article>
  );
}
```

---

### TypeScript Type-Safe Selectors

Create compile-time safety for your selector values:

```typescript
// selectors.ts

// Define your component names as a union type
type ComponentName = 
  | 'ProductCard'
  | 'CheckoutForm'
  | 'NavigationHeader'
  | 'UserProfile'
  | 'CartDrawer';

// Define element names per component
type ElementName<C extends ComponentName> = 
  C extends 'ProductCard' ? 'card' | 'product-image' | 'product-name' | 'price' | 'add-to-cart' :
  C extends 'CheckoutForm' ? 'form' | 'shipping-section' | 'payment-section' | 'submit-button' :
  C extends 'CartDrawer' ? 'drawer' | 'item-list' | 'total' | 'checkout-button' :
  string;

// Type-safe selector builder
interface StableSelectors<C extends ComponentName> {
  'data-component': C;
  'data-element'?: ElementName<C>;
  'data-action'?: string;
  'data-state'?: string;
}

// Factory function
export function createSelectors<C extends ComponentName>(
  component: C
): {
  root: StableSelectors<C>;
  element: (name: ElementName<C>, action?: string) => Partial<StableSelectors<C>>;
} {
  return {
    root: { 'data-component': component },
    element: (name, action) => ({
      'data-element': name,
      ...(action && { 'data-action': action })
    })
  };
}

// Usage
function ProductCard({ product }: Props) {
  const sel = createSelectors('ProductCard');
  
  return (
    <div {...sel.root} {...sel.element('card')}>
      {/* TypeScript will error if you use 'invalid-element' */}
      <button {...sel.element('add-to-cart', 'add-item')}>
        Add to Cart
      </button>
    </div>
  );
}
```

---

### Vanilla JavaScript / Web Components

```javascript
// product-card.js
class ProductCard extends HTMLElement {
  connectedCallback() {
    const product = JSON.parse(this.getAttribute('product'));
    
    this.innerHTML = `
      <article data-component="ProductCard" data-element="card">
        <img 
          src="${product.image}" 
          alt="${product.name}"
          data-element="product-image"
        />
        <h3 data-element="product-name">${product.name}</h3>
        <span data-element="price">$${product.price}</span>
        <button data-element="add-to-cart" data-action="add-item">
          Add to Cart
        </button>
      </article>
    `;
    
    this.querySelector('[data-element="add-to-cart"]')
      .addEventListener('click', () => this.handleAddToCart(product));
  }
}

customElements.define('product-card', ProductCard);
```

---

### Server-Side Templates (PHP, Django, Rails)

```html
<!-- PHP/Blade -->
<article data-component="ProductCard" data-element="card">
  <img src="{{ $product->image }}" data-element="product-image" />
  <h3 data-element="product-name">{{ $product->name }}</h3>
  <button data-element="add-to-cart" data-action="add-item">Add to Cart</button>
</article>

<!-- Django -->
<article data-component="ProductCard" data-element="card">
  <img src="{{ product.image }}" data-element="product-image" />
  <h3 data-element="product-name">{{ product.name }}</h3>
  <button data-element="add-to-cart" data-action="add-item">Add to Cart</button>
</article>

<!-- Rails ERB -->
<article data-component="ProductCard" data-element="card">
  <img src="<%= product.image %>" data-element="product-image" />
  <h3 data-element="product-name"><%= product.name %></h3>
  <button data-element="add-to-cart" data-action="add-item">Add to Cart</button>
</article>
```

---

## Using Stable Selectors in Fullstory

### Searching by CSS Selector

```
# Find all ProductCard components
css selector: [data-component="ProductCard"]

# Find add-to-cart buttons
css selector: [data-element="add-to-cart"]

# Find add-to-cart within ProductCard
css selector: [data-component="ProductCard"] [data-element="add-to-cart"]

# Find buttons with specific action
css selector: [data-action="add-item"]
```

### Creating Defined Elements

When creating defined elements in Fullstory, use stable selectors:

| Element Name | Selector |
|--------------|----------|
| Add to Cart Button | `[data-element="add-to-cart"]` |
| Product Card | `[data-component="ProductCard"]` |
| Search Input | `[data-element="search-input"]` |
| Checkout Submit | `[data-component="CheckoutForm"] [data-element="submit-button"]` |

### Combining with Element Properties

Stable selectors and Element Properties work together:

```html
<div 
  data-component="ProductCard"
  data-element="card"
  data-fs-element="Product Card"
  data-fs-properties-schema='{"product_id":"string","price":"real"}'
  data-product-id="SKU-123"
  data-price="99.99"
>
  <!-- content -->
</div>
```

| Attribute | Purpose |
|-----------|---------|
| `data-component` | Stable selector for searching |
| `data-element` | Stable selector for specific element |
| `data-fs-element` | Fullstory defined element name |
| `data-fs-properties-schema` | Fullstory element properties schema |

### Aligning with Testing Tools

Many teams use `data-testid` for Cypress/Playwright. You can unify:

```html
<!-- Option 1: Use both (redundant but safe) -->
<button 
  data-element="add-to-cart"
  data-testid="add-to-cart-button"
>Add</button>

<!-- Option 2: Configure test tools to use data-element -->
```

```javascript
// cypress.config.js
Cypress.SelectorPlayground.defaults({
  selectorPriority: ['data-element', 'data-component', 'data-testid', 'id']
});

// playwright.config.js
use: {
  testIdAttribute: 'data-element'
}
```

---

## ✅ GOOD Implementation Examples

### Example 1: E-commerce Product Grid

```html
<section data-component="ProductGrid" data-element="grid">
  <h2 data-element="section-title">Featured Products</h2>
  
  <div data-element="product-list">
    <article data-component="ProductCard" data-element="card">
      <img src="..." data-element="product-image" />
      <h3 data-element="product-name">Wireless Headphones</h3>
      <div data-element="pricing">
        <span data-element="current-price">$149.99</span>
        <span data-element="original-price">$199.99</span>
      </div>
      <div data-element="actions">
        <button data-element="add-to-cart" data-action="add-item">Add to Cart</button>
        <button data-element="wishlist" data-action="save-item">♡</button>
      </div>
    </article>
  </div>
  
  <nav data-element="pagination">
    <button data-element="prev-page" data-action="navigate-prev">Previous</button>
    <button data-element="next-page" data-action="navigate-next">Next</button>
  </nav>
</section>
```

### Example 2: Multi-Step Form

```html
<form data-component="CheckoutForm" data-element="form">
  <nav data-element="step-indicator">
    <span data-element="step" data-step="shipping" data-state="active">Shipping</span>
    <span data-element="step" data-step="payment">Payment</span>
    <span data-element="step" data-step="review">Review</span>
  </nav>
  
  <fieldset data-element="shipping-step">
    <div data-element="name-field">
      <label>Full Name</label>
      <input type="text" data-element="name-input" />
    </div>
    <div data-element="address-field">
      <label>Address</label>
      <input type="text" data-element="address-input" />
    </div>
  </fieldset>
  
  <!-- Payment step (with privacy) -->
  <fieldset data-element="payment-step" class="fs-exclude">
    <div data-element="card-field">
      <label>Card Number</label>
      <input type="text" data-element="card-input" />
    </div>
  </fieldset>
  
  <div data-element="form-actions">
    <button type="button" data-element="back-button" data-action="go-back">Back</button>
    <button type="submit" data-element="submit-button" data-action="submit-form">Continue</button>
  </div>
</form>
```

### Example 3: Navigation with Dropdowns

```html
<header data-component="SiteHeader" data-element="header">
  <a href="/" data-element="logo">
    <img src="logo.svg" alt="Company" />
  </a>
  
  <nav data-component="MainNav" data-element="navigation">
    <ul data-element="nav-list">
      <li data-element="nav-item">
        <a href="/products" data-element="nav-link">Products</a>
        <ul data-element="dropdown-menu" data-state="collapsed">
          <li><a href="/products/shoes" data-element="dropdown-item">Shoes</a></li>
          <li><a href="/products/bags" data-element="dropdown-item">Bags</a></li>
        </ul>
      </li>
    </ul>
  </nav>
  
  <div data-element="header-actions">
    <button data-element="search-toggle" data-action="toggle-search">🔍</button>
    <a href="/cart" data-element="cart-link">
      Cart (<span data-element="cart-count">3</span>)
    </a>
  </div>
</header>
```

---

## ❌ BAD Implementation Examples

### Example 1: Generic Names

```html
<!-- ❌ BAD: Names are too generic -->
<div data-component="Component">
  <img data-element="image" />
  <span data-element="text" />
  <button data-element="button">Click</button>
</div>
```

**Why it's bad:** Every component has "image", "text", "button" - searches return everything.

**✅ CORRECTED:**
```html
<div data-component="ProductCard">
  <img data-element="product-image" />
  <span data-element="product-name" />
  <button data-element="add-to-cart">Click</button>
</div>
```

### Example 2: Position-Based Names

```html
<!-- ❌ BAD: Position-based naming -->
<div data-component="ProductList">
  <div data-element="item-0">First product</div>
  <div data-element="item-1">Second product</div>
  <div data-element="item-2">Third product</div>
</div>
```

**Why it's bad:** If sort order changes, "item-0" is now a different product.

**✅ CORRECTED:**
```html
<div data-component="ProductList">
  <div data-element="product-item" data-product-id="SKU-A">First product</div>
  <div data-element="product-item" data-product-id="SKU-B">Second product</div>
  <div data-element="product-item" data-product-id="SKU-C">Third product</div>
</div>
```

### Example 3: Appearance-Based Names

```html
<!-- ❌ BAD: Named by appearance -->
<button data-element="blue-button">Primary Action</button>
<button data-element="gray-button">Secondary Action</button>
<div data-element="left-sidebar">Navigation</div>
```

**Why it's bad:** If design changes (blue → green, sidebar moves right), names become wrong.

**✅ CORRECTED:**
```html
<button data-element="primary-action">Primary Action</button>
<button data-element="secondary-action">Secondary Action</button>
<div data-element="side-navigation">Navigation</div>
```

---

## Advanced Patterns

### Virtualized Lists / Infinite Scroll

For virtualized content where DOM elements are recycled:

```tsx
// React with react-window
function VirtualizedProductList({ products }) {
  return (
    <div data-component="ProductList" data-element="virtual-container">
      <FixedSizeList height={600} itemCount={products.length} itemSize={120}>
        {({ index, style }) => (
          <div
            style={style}
            data-element="product-row"
            data-product-id={products[index].id}  // Stable ID, not position!
          >
            <ProductCard product={products[index]} />
          </div>
        )}
      </FixedSizeList>
    </div>
  );
}
```

**Key Principle**: Use stable business identifiers (`data-product-id`), not positional indices.

---

### Shadow DOM / Web Components

Shadow DOM encapsulates styles but data attributes still work:

```javascript
class ProductCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  
  connectedCallback() {
    // Set attributes on the host element (light DOM)
    this.setAttribute('data-component', 'ProductCard');
    this.setAttribute('data-element', 'card');
    
    // Shadow DOM content also gets attributes
    this.shadowRoot.innerHTML = `
      <style>/* encapsulated styles */</style>
      <article>
        <slot name="image"></slot>
        <button data-element="add-to-cart" data-action="add-item">
          <slot name="button-text">Add to Cart</slot>
        </button>
      </article>
    `;
  }
}
```

**Fullstory Note**: Contact Fullstory support about Shadow DOM capture configuration for your account.

---

### Micro-Frontends

When multiple teams own different parts of the UI, namespace your selectors:

```html
<!-- Team Checkout owns this -->
<div 
  data-component="Checkout.PaymentForm"
  data-team="checkout"
  data-element="form"
>
  <button data-element="submit-payment">Pay</button>
</div>

<!-- Team Catalog owns this -->
<div 
  data-component="Catalog.ProductCard"
  data-team="catalog"
  data-element="card"
>
  <button data-element="add-to-cart">Add</button>
</div>
```

**Namespace Convention**: `{Team}.{Component}` prevents collisions.

---

### A/B Tests and Feature Flags

Track variants for analysis:

```html
<!-- Variant A: Original -->
<button
  data-component="CTAButton"
  data-element="hero-cta"
  data-variant="control"
  data-experiment="homepage-cta-2024"
>
  Get Started
</button>

<!-- Variant B: Test -->
<button
  data-component="CTAButton"
  data-element="hero-cta"
  data-variant="treatment-green"
  data-experiment="homepage-cta-2024"
>
  Start Free Trial
</button>
```

**In Fullstory**: Search by `[data-experiment="homepage-cta-2024"][data-variant="treatment-green"]` to analyze specific variants.

---

### Dynamic/Lazy-Loaded Content

Ensure selectors are present when content loads:

```tsx
// React with Suspense
function ProductDetails({ productId }) {
  return (
    <Suspense 
      fallback={
        <div 
          data-component="ProductDetails" 
          data-element="skeleton" 
          data-state="loading"
        >
          Loading...
        </div>
      }
    >
      <ProductDetailsContent productId={productId} />
    </Suspense>
  );
}

function ProductDetailsContent({ productId }) {
  const product = use(fetchProduct(productId));
  
  return (
    <div 
      data-component="ProductDetails" 
      data-element="content"
      data-state="loaded"
    >
      {/* content */}
    </div>
  );
}
```

**Note**: The `data-state` attribute helps distinguish loading vs loaded states in Fullstory searches.

---

### Iframes (Cross-Origin Limitations)

For same-origin iframes, selectors work normally. For cross-origin:

```html
<!-- Parent page -->
<iframe 
  src="https://checkout.example.com/embed"
  data-component="CheckoutEmbed"
  data-element="iframe"
  title="Checkout"
></iframe>
```

**Limitation**: Fullstory cannot directly capture cross-origin iframe content. The iframe must have its own Fullstory snippet installed.

---

## Troubleshooting

### Selectors Not Working in Fullstory

**Check in browser DevTools:**
1. Inspect the element
2. Verify `data-component` and `data-element` attributes exist
3. Check for typos in attribute names

**Common issues:**
- Framework stripping data attributes in production
- SSR/hydration mismatch
- Conditional rendering removing the element

### Too Many Search Results

**Problem:** Searching `[data-element="button"]` returns hundreds of results

**Solution:** Be more specific:
```
[data-component="ProductCard"] [data-element="add-to-cart"]
```

### Attributes Stripped in Production

Check your build tool configuration:

```javascript
// webpack.config.js - DON'T strip data-* attributes
optimization: {
  minimizer: [
    new HtmlWebpackPlugin({
      minify: {
        // Keep data-* attributes
        removeDataAttributes: false
      }
    })
  ]
}
```

---

## KEY TAKEAWAYS FOR AGENT

When helping web developers implement stable selectors:

### Web-Specific Guidance

1. **Use `data-*` attributes** — HTML standard, works everywhere
2. **Primary: `data-component` + `data-element`** — Component boundary + element role
3. **Extended: `data-action`, `data-state`, `data-variant`** — CUA/AI readiness
4. **Combine with Element Properties** — `data-fs-element` for Fullstory analytics
5. **Combine with ARIA** — `aria-label` for accessibility + AI understanding

### Framework-Specific Notes

| Framework | Notes |
|-----------|-------|
| React/Next.js | Works in Server Components; use hooks for DRY code |
| Angular | Use directives for consistency |
| Vue | Use directives or simple attributes |
| Svelte | Direct attributes; simple approach |
| Astro | Works in both static and hydrated islands |

### Implementation Checklist (Web)

```markdown
□ Add data-component to component roots
□ Add data-element to interactive elements
□ Add data-action for buttons/links
□ Add data-state for stateful elements
□ Verify attributes in production build
□ Configure E2E tools to use data-element
□ Create Fullstory defined elements with CSS selectors
```

---

## REFERENCE LINKS

### Fullstory Documentation
- **CSS Selectors in Search**: https://help.fullstory.com/hc/en-us/articles/360020623294
- **Defined Elements**: https://help.fullstory.com/hc/en-us/articles/360020828113
- **Element Properties**: ../core/fullstory-element-properties/SKILL.md

### Testing Tool Integration
- **Cypress Best Practices**: https://docs.cypress.io/guides/references/best-practices#Selecting-Elements
- **Playwright Locators**: https://playwright.dev/docs/locators
- **Testing Library Queries**: https://testing-library.com/docs/queries/about

### Web Standards
- **MDN: Using Data Attributes**: https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes
- **WAI-ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/

### Historical Context
These skills consolidate and extend patterns from:
- `fullstorydev/eslint-plugin-annotate-react` (React-specific)
- `fullstorydev/fullstory-babel-plugin-annotate-react` (Build-time injection)

The manual approach in this skill is more flexible and works across all frameworks.

---

*This skill provides web-specific implementation guidance for stable selectors. See SKILL.md for core concepts and SKILL-MOBILE.md for mobile implementation.*
