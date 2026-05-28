---
name: fullstory-element-properties-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/HTML implementation guide for Fullstory's Element Properties API. Includes API reference, code examples, and framework patterns for web applications.
parent_skill: fullstory-element-properties
related_skills:
  - fullstory-element-properties
  - fullstory-page-properties
  - fullstory-analytics-events
---

# Fullstory Element Properties — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for property types, inheritance, and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### HTML Data Attributes

Element properties are defined using HTML data attributes:

| Attribute | Purpose | Required |
|-----------|---------|----------|
| `data-fs-properties-schema` | JSON object defining which attributes to capture and their types | Yes |
| `data-fs-element` | Names the element for use in Fullstory | No (recommended) |
| `data-{property-name}` | The actual property values | Yes |

### Schema Structure

```json
{
  "attribute-name": "type",
  "attribute-name-2": {
    "type": "type_value",
    "name": "override_property_name"
  }
}
```

**Schema formats:**
- **Simple**: `"data-price": "real"` — uses attribute name as property name
- **Expanded**: `"data-price": { "type": "real", "name": "price" }` — provides clean property name

---

## ✅ GOOD Implementation Examples

### Example 1: E-commerce Product Card

```html
<!-- GOOD: Comprehensive product card with proper typing and meaningful names -->
<div 
  class="product-card"
  data-product-id="SKU-12345"
  data-product-name="Premium Wireless Headphones"
  data-product-category="Electronics"
  data-product-price="199.99"
  data-product-stock="15"
  data-product-rating="4.5"
  data-on-sale="true"
  data-launch-date="2024-01-15"
  data-tags='["wireless", "bluetooth", "noise-canceling"]'
  data-fs-properties-schema='{
    "data-product-id": {
      "type": "str",
      "name": "productId"
    },
    "data-product-name": {
      "type": "str",
      "name": "productName"
    },
    "data-product-category": {
      "type": "str",
      "name": "category"
    },
    "data-product-price": {
      "type": "real",
      "name": "price"
    },
    "data-product-stock": {
      "type": "int",
      "name": "stockLevel"
    },
    "data-product-rating": {
      "type": "real",
      "name": "rating"
    },
    "data-on-sale": {
      "type": "bool",
      "name": "isOnSale"
    },
    "data-launch-date": {
      "type": "date",
      "name": "launchDate"
    },
    "data-tags": {
      "type": "strs",
      "name": "productTags"
    }
  }'
  data-fs-element="Product Card">
  
  <button 
    class="add-to-cart"
    data-fs-element="Add to Cart Button">
    Add to Cart
  </button>
</div>
```

**Why this is good:**
- ✅ Proper type mapping (real for price, int for stock, bool for sale status)
- ✅ Clean property names using the `name` override
- ✅ Captures both scalar and array values appropriately
- ✅ Named element for easy reference in Fullstory
- ✅ Child button inherits all parent properties
- ✅ Uses semantic attribute names that describe the data

### Example 2: Form with Hierarchy

```html
<!-- GOOD: Form-level properties inherited by all fields -->
<form 
  class="checkout-form"
  data-form-type="checkout"
  data-form-step="payment"
  data-user-tier="premium"
  data-fs-properties-schema='{
    "data-form-type": {
      "type": "str",
      "name": "formType"
    },
    "data-form-step": {
      "type": "str",
      "name": "checkoutStep"
    },
    "data-user-tier": {
      "type": "str",
      "name": "userTier"
    }
  }'
  data-fs-element="Checkout Form">
  
  <input 
    type="text"
    name="cardNumber"
    data-field-name="cardNumber"
    data-field-required="true"
    data-field-validation="credit-card"
    data-fs-properties-schema='{
      "data-field-name": {
        "type": "str",
        "name": "fieldName"
      },
      "data-field-required": {
        "type": "bool",
        "name": "isRequired"
      },
      "data-field-validation": {
        "type": "str",
        "name": "validationType"
      }
    }'
    data-fs-element="Card Number Field">
  
  <button 
    type="submit"
    data-button-type="primary"
    data-fs-properties-schema='{
      "data-button-type": "str"
    }'
    data-fs-element="Submit Payment Button">
    Complete Purchase
  </button>
</form>
```

**Why this is good:**
- ✅ Hierarchical property inheritance (form properties flow to all children)
- ✅ Each element has appropriate context-specific properties
- ✅ All interactions capture both element-specific and form-level context
- ✅ Clear separation of concerns (form context vs field specifics)

### Example 3: Form State Capture on Submit

```html
<!-- GOOD: Capture form selections when submit is clicked -->
<form data-fs-element="checkout-form">
  
  <select data-selected-shipping
    data-fs-properties-schema='{"data-selected-shipping": "str"}'>
    <option value="standard">Standard</option>
    <option value="express" selected>Express</option>
  </select>
  
  <select data-selected-payment
    data-fs-properties-schema='{"data-selected-payment": "str"}'>
    <option value="credit_card" selected>Credit Card</option>
    <option value="paypal">PayPal</option>
  </select>
  
  <label>
    <input type="checkbox" checked data-gift-wrap="true"
      data-fs-properties-schema='{"data-gift-wrap": "bool"}'>
    Gift wrap
  </label>
  
  <!-- Submit button inherits ALL properties from above -->
  <button type="submit" data-fs-element="submit-order">
    Place Order
  </button>
  
</form>
```

**In Fullstory, when "submit-order" is clicked:**
- The click event captures: `selectedShipping`, `selectedPayment`, `giftWrap`
- You can now create metrics like:
  - "Submit clicks WHERE selectedPayment = 'paypal'"
  - "Group submit clicks BY selectedShipping"
  - "Funnel: visits → checkout-form viewed → submit-order clicked WHERE giftWrap = true"

---

## ❌ BAD Implementation Examples

### Example 1: Common Type Mistakes

```html
<!-- BAD: Multiple type and naming issues -->
<button 
  class="product-buy"
  data-price="$199.99"
  data-quantity="5 items"
  data-available="yes"
  data-fs-properties-schema='{
    "data-price": "str",
    "data-quantity": "int",
    "data-available": "bool"
  }'
  data-fs-element="Buy Button">
  Buy Now
</button>
```

**Why this is bad:**
- ❌ `data-price` contains "$" currency symbol but typed as string (should be real and clean: "199.99")
- ❌ `data-quantity` contains "items" text but typed as int (should be clean number: "5")
- ❌ `data-available` uses "yes" instead of boolean value (should be "true" or "1")
- ❌ Lost ability to do numeric filtering, comparisons, and aggregations

**CORRECTED:**

```html
<!-- GOOD: Proper types and clean values -->
<button 
  class="product-buy"
  data-price="199.99"
  data-quantity="5"
  data-available="true"
  data-currency="USD"
  data-fs-properties-schema='{
    "data-price": {
      "type": "real",
      "name": "price"
    },
    "data-quantity": {
      "type": "int",
      "name": "quantity"
    },
    "data-available": {
      "type": "bool",
      "name": "isAvailable"
    },
    "data-currency": {
      "type": "str",
      "name": "currency"
    }
  }'
  data-fs-element="Buy Button">
  Buy Now
</button>
```

### Example 2: Over-capturing Technical Data

```html
<!-- BAD: Capturing too many irrelevant properties -->
<div 
  data-component-name="ProductCard"
  data-component-version="1.2.3"
  data-react-key="product-123"
  data-render-timestamp="2024-10-20T14:30:00Z"
  data-css-class="product-card mb-4 shadow-lg"
  data-developer-name="John Doe"
  data-git-commit="abc123def456"
  data-build-number="4567"
  data-product-id="SKU-123"
  data-product-name="Widget"
  data-fs-properties-schema='{
    "data-component-name": "str",
    "data-component-version": "str",
    "data-react-key": "str",
    "data-render-timestamp": "date",
    "data-css-class": "str",
    "data-developer-name": "str",
    "data-git-commit": "str",
    "data-build-number": "int",
    "data-product-id": "str",
    "data-product-name": "str"
  }'>
```

**Why this is bad:**
- ❌ Captures technical/debug data not useful for analytics
- ❌ Captures implementation details (react-key, css-class)
- ❌ Wastes property quota (limit of 50 per interaction, 500 total)
- ❌ Creates high cardinality issues (timestamp, git commits)
- ❌ Makes actual business data harder to find

**CORRECTED:**

```html
<!-- GOOD: Only business-relevant properties -->
<div 
  data-product-id="SKU-123"
  data-product-name="Widget"
  data-product-category="Tools"
  data-product-price="29.99"
  data-fs-properties-schema='{
    "data-product-id": {
      "type": "str",
      "name": "productId"
    },
    "data-product-name": {
      "type": "str",
      "name": "productName"
    },
    "data-product-category": {
      "type": "str",
      "name": "category"
    },
    "data-product-price": {
      "type": "real",
      "name": "price"
    }
  }'
  data-fs-element="Product Card">
```

### Example 3: Invalid JSON Syntax

```html
<!-- BAD: Multiple JSON syntax errors -->
<button
  data-product-id="SKU-123"
  data-price="49.99"
  data-fs-properties-schema="{
    'data-product-id': 'str',
    "data-price": "real"
  }"
  data-fs-element="Add to Cart">
  Add to Cart
</button>
```

**Why this is bad:**
- ❌ Mixed single and double quotes in JSON (invalid JSON)
- ❌ JSON will fail to parse
- ❌ Properties won't be captured at all
- ❌ Silent failure — no console errors

**CORRECTED:**

```html
<!-- GOOD: Valid JSON with consistent quoting -->
<button
  data-product-id="SKU-123"
  data-price="49.99"
  data-fs-properties-schema='{
    "data-product-id": {
      "type": "str",
      "name": "productId"
    },
    "data-price": {
      "type": "real",
      "name": "price"
    }
  }'
  data-fs-element="Add to Cart">
  Add to Cart
</button>
```

### Example 4: Schema References Missing Attributes

```html
<!-- BAD: Schema references attributes that don't exist -->
<button
  data-product-id="SKU-123"
  data-fs-properties-schema='{
    "data-product-id": "str",
    "data-product-name": "str",
    "data-price": "real",
    "data-category": "str"
  }'
  data-fs-element="Product Button">
  View Product
</button>
```

**Why this is bad:**
- ❌ Schema references `data-product-name`, `data-price`, `data-category` but these attributes don't exist
- ❌ Only `data-product-id` will be captured
- ❌ Incomplete data reduces analytics value

**CORRECTED:**

```html
<!-- GOOD: All referenced attributes exist -->
<button
  data-product-id="SKU-123"
  data-product-name="Premium Widget"
  data-price="49.99"
  data-category="Electronics"
  data-fs-properties-schema='{
    "data-product-id": {
      "type": "str",
      "name": "productId"
    },
    "data-product-name": {
      "type": "str",
      "name": "productName"
    },
    "data-price": {
      "type": "real",
      "name": "price"
    },
    "data-category": {
      "type": "str",
      "name": "category"
    }
  }'
  data-fs-element="Product Button">
  View Product
</button>
```

---

## Framework Integration

### React

```jsx
// GOOD: Dynamically setting properties in a React component
function ProductCard({ product }) {
  const schemaRef = useRef(null);
  
  useEffect(() => {
    if (schemaRef.current) {
      // Set the schema as a data attribute
      schemaRef.current.setAttribute('data-fs-properties-schema', JSON.stringify({
        'data-product-id': { type: 'str', name: 'productId' },
        'data-product-name': { type: 'str', name: 'productName' },
        'data-price': { type: 'real', name: 'price' },
        'data-in-stock': { type: 'bool', name: 'inStock' },
        'data-variant-count': { type: 'int', name: 'variantCount' }
      }));
      
      // Set the actual attribute values
      schemaRef.current.setAttribute('data-product-id', product.id);
      schemaRef.current.setAttribute('data-product-name', product.name);
      schemaRef.current.setAttribute('data-price', product.price.toString());
      schemaRef.current.setAttribute('data-in-stock', product.inStock.toString());
      schemaRef.current.setAttribute('data-variant-count', product.variants.length.toString());
      schemaRef.current.setAttribute('data-fs-element', 'Product Card');
    }
  }, [product]);
  
  return (
    <div ref={schemaRef} className="product-card">
      {/* Component content */}
    </div>
  );
}
```

**Alternative: Inline JSX approach:**

```jsx
// GOOD: Inline data attributes in JSX
function ProductCard({ product }) {
  const schema = JSON.stringify({
    'data-product-id': { type: 'str', name: 'productId' },
    'data-price': { type: 'real', name: 'price' },
    'data-in-stock': { type: 'bool', name: 'inStock' }
  });
  
  return (
    <div 
      className="product-card"
      data-product-id={product.id}
      data-price={product.price}
      data-in-stock={product.inStock}
      data-fs-properties-schema={schema}
      data-fs-element="Product Card"
    >
      <button data-fs-element="Add to Cart Button">
        Add to Cart
      </button>
    </div>
  );
}
```

### Vue

```vue
<template>
  <div 
    class="product-card"
    :data-product-id="product.id"
    :data-product-name="product.name"
    :data-price="product.price"
    :data-in-stock="product.inStock"
    :data-fs-properties-schema="schema"
    data-fs-element="Product Card"
  >
    <button data-fs-element="Add to Cart Button">
      Add to Cart
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps(['product']);

const schema = computed(() => JSON.stringify({
  'data-product-id': { type: 'str', name: 'productId' },
  'data-product-name': { type: 'str', name: 'productName' },
  'data-price': { type: 'real', name: 'price' },
  'data-in-stock': { type: 'bool', name: 'inStock' }
}));
</script>
```

### Angular

```typescript
// product-card.component.ts
@Component({
  selector: 'app-product-card',
  template: `
    <div 
      class="product-card"
      [attr.data-product-id]="product.id"
      [attr.data-product-name]="product.name"
      [attr.data-price]="product.price"
      [attr.data-in-stock]="product.inStock"
      [attr.data-fs-properties-schema]="schema"
      data-fs-element="Product Card"
    >
      <button data-fs-element="Add to Cart Button">
        Add to Cart
      </button>
    </div>
  `
})
export class ProductCardComponent {
  @Input() product: Product;
  
  get schema(): string {
    return JSON.stringify({
      'data-product-id': { type: 'str', name: 'productId' },
      'data-product-name': { type: 'str', name: 'productName' },
      'data-price': { type: 'real', name: 'price' },
      'data-in-stock': { type: 'bool', name: 'inStock' }
    });
  }
}
```

---

## Common Patterns

### Pattern 1: Dynamic List Items

```javascript
// Rendering product list with element properties
function renderProductList(products) {
  const container = document.getElementById('product-list');
  
  products.forEach((product, index) => {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    // Set attribute values
    card.setAttribute('data-product-id', product.id);
    card.setAttribute('data-product-name', product.name);
    card.setAttribute('data-price', product.price.toString());
    card.setAttribute('data-position', index.toString());
    
    // Set schema
    card.setAttribute('data-fs-properties-schema', JSON.stringify({
      'data-product-id': { type: 'str', name: 'productId' },
      'data-product-name': { type: 'str', name: 'productName' },
      'data-price': { type: 'real', name: 'price' },
      'data-position': { type: 'int', name: 'listPosition' }
    }));
    
    // Name the element
    card.setAttribute('data-fs-element', 'Product Card');
    
    container.appendChild(card);
  });
}
```

### Pattern 2: Reusable Schema Builder

```javascript
// Helper to build schemas consistently
function buildElementProperties(element, properties, elementName) {
  const schema = {};
  
  Object.entries(properties).forEach(([key, config]) => {
    const attrName = `data-${key}`;
    
    // Set the attribute value
    element.setAttribute(attrName, String(config.value));
    
    // Build schema entry
    schema[attrName] = {
      type: config.type,
      name: config.name || key
    };
  });
  
  // Set schema and element name
  element.setAttribute('data-fs-properties-schema', JSON.stringify(schema));
  element.setAttribute('data-fs-element', elementName);
}

// Usage
buildElementProperties(productCard, {
  productId: { value: 'SKU-123', type: 'str' },
  price: { value: 49.99, type: 'real' },
  inStock: { value: true, type: 'bool' }
}, 'Product Card');
```

### Pattern 3: TypeScript Type Definitions

```typescript
// Type-safe element properties
interface ElementPropertySchema {
  type: 'str' | 'strs' | 'int' | 'ints' | 'real' | 'reals' | 'bool' | 'bools' | 'date' | 'dates';
  name?: string;
}

interface ProductCardProperties {
  'data-product-id': ElementPropertySchema;
  'data-product-name': ElementPropertySchema;
  'data-price': ElementPropertySchema;
  'data-in-stock': ElementPropertySchema;
}

function setProductCardProperties(
  element: HTMLElement, 
  product: Product
): void {
  const schema: ProductCardProperties = {
    'data-product-id': { type: 'str', name: 'productId' },
    'data-product-name': { type: 'str', name: 'productName' },
    'data-price': { type: 'real', name: 'price' },
    'data-in-stock': { type: 'bool', name: 'inStock' }
  };
  
  element.setAttribute('data-product-id', product.id);
  element.setAttribute('data-product-name', product.name);
  element.setAttribute('data-price', String(product.price));
  element.setAttribute('data-in-stock', String(product.inStock));
  element.setAttribute('data-fs-properties-schema', JSON.stringify(schema));
  element.setAttribute('data-fs-element', 'Product Card');
}
```

---

## Validation and Testing

### Pre-Deployment Checklist

1. **Open browser DevTools** and inspect the element
2. **Verify all `data-` attributes** are present with correct values
3. **Parse the schema JSON** to ensure it's valid:
   ```javascript
   JSON.parse(element.getAttribute('data-fs-properties-schema'))
   ```
4. **Check attribute existence** — every key in schema should have a corresponding data attribute

### Validation in Fullstory

1. **Trigger an interaction** on the decorated element
2. **Find the session** in Fullstory
3. **Click on the element** in the replay
4. **Check the Inspector** for element properties
5. **Verify all properties appear** with correct names and values
6. **Test filtering** using the captured properties

---

## Reference Links

- **Browser API**: https://developer.fullstory.com/browser/fullcapture/set-element-properties/
- **Help Center**: https://help.fullstory.com/hc/en-us/articles/24236341468311-Extracted-Element-Properties
