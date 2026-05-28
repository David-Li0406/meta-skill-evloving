---
name: fullstory-privacy-controls-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/CSS implementation guide for Fullstory's Privacy Controls. Includes CSS classes (fs-exclude, fs-mask, fs-unmask), selector rules, framework patterns, and comprehensive examples.
parent_skill: fullstory-privacy-controls
related_skills:
  - fullstory-privacy-controls
  - fullstory-privacy-strategy
  - fullstory-user-consent
---

# Fullstory Privacy Controls — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for privacy modes, compliance guidance, and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### CSS Classes

```html
<!-- Exclude: Nothing captured, events ignored -->
<div class="fs-exclude">...</div>

<!-- Mask: Structure captured, text replaced with wireframe -->
<div class="fs-mask">...</div>

<!-- Unmask: Everything captured (override in masked context) -->
<div class="fs-unmask">...</div>
```

### Legacy Classes (Still Supported)

```html
<!-- Legacy: Use fs-exclude instead -->
<div class="fs-block">...</div>
```

### ⚠️ BUILD TOOL WARNING

Modern CSS build tools may remove "unused" classes, breaking privacy controls:

```javascript
// DANGER: CSS purge tools might remove fs-* classes!
// In tailwind.config.js, postcss.config.js, etc., safelist these classes:
module.exports = {
  safelist: [
    'fs-exclude',
    'fs-mask', 
    'fs-unmask',
    'fs-block'  // legacy
  ]
}
```

**Always verify** privacy classes survive your build process by:
1. Inspecting production HTML for `fs-*` classes
2. Testing in Fullstory to confirm masking/exclusion works
3. Using CSS selector rules in Settings as backup

---

## ✅ GOOD Implementation Examples

### Example 1: Login Form with Proper Protection

```html
<!-- GOOD: Password field excluded, email masked -->
<div class="login-form">
  <label for="email">Email</label>
  <input 
    type="email" 
    id="email" 
    name="email" 
    class="fs-mask"
  />
  
  <label for="password">Password</label>
  <input 
    type="password" 
    id="password" 
    name="password" 
    class="fs-exclude"
  />
  
  <button type="submit" class="fs-unmask">Login</button>
</div>
```

**Why this is good:**
- ✅ Explicit exclusion for password
- ✅ Email masked (PII protected, structure visible)
- ✅ Login button visible for funnel analysis

### Example 2: User Profile with Layered Privacy

```html
<!-- GOOD: User profile with appropriate masking -->
<div class="user-profile">
  <!-- Mask PII but allow click tracking -->
  <div class="profile-header fs-mask">
    <img src="avatar.jpg" alt="User avatar" />
    <h2>John Smith</h2>  <!-- Masked: appears as "████ █████" -->
    <p>john.smith@company.com</p>  <!-- Masked -->
  </div>
  
  <!-- Public content - unmask -->
  <div class="profile-actions fs-unmask">
    <button>Edit Profile</button>
    <button>Settings</button>
  </div>
  
  <!-- Sensitive financial data - exclude entirely -->
  <div class="payment-methods fs-exclude">
    <h3>Saved Payment Methods</h3>
    <div class="card">**** **** **** 4242</div>
  </div>
</div>
```

**Why this is good:**
- ✅ Name and email masked (visible structure, no text)
- ✅ Action buttons fully visible for UX analysis
- ✅ Payment info completely excluded (not even structure)
- ✅ Avatar images still visible for context

### Example 3: Healthcare Form (HIPAA-Compliant)

```html
<!-- GOOD: Healthcare form with HIPAA-appropriate privacy -->
<form class="patient-intake-form">
  <!-- PHI must be excluded, not just masked -->
  <fieldset class="fs-exclude">
    <legend>Medical History</legend>
    <label>Current Medications</label>
    <textarea name="medications"></textarea>
    
    <label>Medical Conditions</label>
    <div class="condition-checkboxes">
      <label><input type="checkbox" name="diabetes" /> Diabetes</label>
      <label><input type="checkbox" name="heart" /> Heart Disease</label>
      <!-- Even checkbox interactions are excluded -->
    </div>
  </fieldset>
  
  <!-- Appointment preferences can be masked -->
  <fieldset class="fs-mask">
    <legend>Appointment Preferences</legend>
    <label>Preferred Date</label>
    <input type="date" name="preferred_date" />
    
    <label>Preferred Time</label>
    <select name="preferred_time">
      <option>Morning</option>
      <option>Afternoon</option>
    </select>
  </fieldset>
  
  <!-- Navigation elements unmasked -->
  <div class="form-navigation fs-unmask">
    <button type="button">Previous</button>
    <button type="submit">Submit</button>
  </div>
</form>
```

**Why this is good:**
- ✅ PHI (medications, conditions) completely excluded
- ✅ HIPAA compliance — no health data leaves device
- ✅ Non-PHI preferences masked (structure visible)
- ✅ Navigation buttons visible for funnel analysis

### Example 4: E-commerce Checkout

```html
<!-- GOOD: Checkout with appropriate privacy levels -->
<div class="checkout-page">
  <!-- Order summary - can show product names -->
  <section class="order-summary fs-unmask">
    <h2>Your Order</h2>
    <div class="item">
      <span class="name">Premium Widget</span>
      <span class="qty">x 2</span>
      <span class="price">$99.98</span>
    </div>
    <div class="total">Total: $109.98</div>
  </section>
  
  <!-- Shipping address - mask the details -->
  <section class="shipping-address fs-mask">
    <h2>Shipping To</h2>
    <p class="name">John Smith</p>
    <p class="street">123 Main Street</p>
    <p class="city-state">San Francisco, CA 94102</p>
  </section>
  
  <!-- Payment - exclude entirely -->
  <section class="payment-info fs-exclude">
    <h2>Payment Method</h2>
    <input type="text" name="card_number" placeholder="Card Number" />
    <input type="text" name="expiry" placeholder="MM/YY" />
    <input type="text" name="cvv" placeholder="CVV" />
  </section>
  
  <!-- Action buttons visible -->
  <div class="actions fs-unmask">
    <button>Edit Cart</button>
    <button type="submit">Place Order</button>
  </div>
</div>
```

**Why this is good:**
- ✅ Order details visible (useful for conversion analysis)
- ✅ Shipping PII masked but structure shows flow
- ✅ Payment card data completely excluded (PCI compliance)
- ✅ Actions visible for funnel analysis

### Example 5: Search Results with Selective Masking

```html
<!-- GOOD: Search results with selective privacy -->
<div class="search-results">
  <!-- Search term can be visible for analytics -->
  <div class="search-header fs-unmask">
    <span>Results for: "wireless headphones"</span>
    <span>50 results</span>
  </div>
  
  <!-- Product grid - unmask for analysis -->
  <div class="product-grid fs-unmask">
    <div class="product-card">
      <img src="product.jpg" alt="Wireless Headphones" />
      <h3>Premium Wireless Headphones</h3>
      <span class="price">$199.99</span>
      <button>Add to Cart</button>
    </div>
  </div>
  
  <!-- Customer reviews might contain names -->
  <div class="reviews fs-mask">
    <div class="review">
      <span class="author">Sarah J.</span>  <!-- Masked -->
      <span class="text">Great product!</span>  <!-- Masked -->
      <span class="rating fs-unmask">★★★★★</span>  <!-- Unmasked -->
    </div>
  </div>
</div>
```

**Why this is good:**
- ✅ Search terms visible for search analytics
- ✅ Product info visible for conversion analysis
- ✅ Reviewer names/content masked (privacy)
- ✅ Ratings still visible (useful for UX)

### Example 6: Private by Default Unmasking Strategy

```html
<!-- Private by Default: Must explicitly unmask safe content -->
<body>  <!-- Everything masked by default -->
  
  <!-- Unmask navigation (no PII) -->
  <nav class="fs-unmask">
    <a href="/products">Products</a>
    <a href="/pricing">Pricing</a>
    <a href="/about">About</a>
  </nav>
  
  <!-- Unmask product info (no PII) -->
  <div class="product-card fs-unmask">
    <h2>Product Name</h2>
    <p class="price">$99.99</p>
    <button>Add to Cart</button>
  </div>
  
  <!-- Customer info stays masked (default) -->
  <div class="customer-details">
    <p>Name: John Smith</p>  <!-- Masked by default ✓ -->
    <p>Email: john@example.com</p>  <!-- Masked by default ✓ -->
  </div>
  
  <!-- Payment still excluded (always) -->
  <div class="payment-form fs-exclude">
    <input type="text" name="cardNumber" />
  </div>
</body>
```

---

## ❌ BAD Implementation Examples

### Example 1: Over-Excluding (Losing Analytics Value)

```html
<!-- BAD: Entire page excluded -->
<div class="checkout-page fs-exclude">
  <!-- EVERYTHING is excluded - no analytics at all! -->
  <h1>Checkout</h1>
  <div class="items">...</div>
  <div class="payment">...</div>
  <button>Place Order</button>  <!-- Can't see conversions! -->
</div>
```

**Why this is bad:**
- ❌ No visibility into checkout flow
- ❌ Can't analyze conversion funnel
- ❌ Button clicks not captured
- ❌ Overkill — only payment needs exclusion

**CORRECTED:**

```html
<!-- GOOD: Granular privacy -->
<div class="checkout-page">
  <h1>Checkout</h1>
  <div class="items fs-unmask">...</div>
  <div class="payment fs-exclude">...</div>
  <button class="fs-unmask">Place Order</button>
</div>
```

### Example 2: Relying Only on Auto-Detection

```html
<!-- BAD: Assuming Fullstory will auto-detect all sensitive fields -->
<form>
  <!-- Not excluded! No password type or autocomplete -->
  <input name="social_security_number" placeholder="SSN" />
  
  <!-- Not excluded! Custom credit card field -->
  <input name="credit_card" placeholder="Card Number" />
  
  <!-- Not excluded! No standard pattern -->
  <input name="secret_pin" placeholder="PIN" />
</form>
```

**Why this is bad:**
- ❌ SSN field not auto-detected
- ❌ Credit card not auto-detected
- ❌ PIN code sent in clear text
- ❌ Relying on convention without verification

**CORRECTED:**

```html
<!-- GOOD: Explicit exclusion for all sensitive fields -->
<form>
  <input 
    name="social_security_number" 
    placeholder="SSN" 
    class="fs-exclude"
  />
  <input 
    name="credit_card" 
    placeholder="Card Number" 
    class="fs-exclude"
    autocomplete="cc-number"
  />
  <input 
    name="secret_pin" 
    placeholder="PIN" 
    type="password"
    class="fs-exclude"
  />
</form>
```

### Example 3: Masking When Should Exclude

```html
<!-- BAD: Using mask for highly sensitive data -->
<div class="account-info fs-mask">
  <p>SSN: 123-45-6789</p>  <!-- BAD: Should be excluded! -->
  <p>Bank Account: 12345678</p>  <!-- BAD: Should be excluded! -->
  <p>Routing: 021000021</p>  <!-- BAD: Should be excluded! -->
</div>
```

**Why this is bad:**
- ❌ Mask only hides text, structure is still sent
- ❌ Financial data should be excluded entirely
- ❌ Even wireframe could reveal sensitive info format
- ❌ Regulatory risk (PCI, etc.)

**CORRECTED:**

```html
<!-- GOOD: Exclude highly sensitive financial data -->
<div class="account-info fs-exclude">
  <p>SSN: 123-45-6789</p>
  <p>Bank Account: 12345678</p>
  <p>Routing: 021000021</p>
</div>
```

### Example 4: Forgetting Child Elements Need Exclusion

```html
<!-- BAD: Parent masked but sensitive child needs exclusion -->
<div class="user-card fs-mask">
  <h3>Account Details</h3>
  <p>Name: John Smith</p>  <!-- Masked - OK -->
  <p>Email: john@example.com</p>  <!-- Masked - OK -->
  
  <!-- BAD: Credit card inherits mask, but needs exclude! -->
  <div class="saved-payment">
    <p>Card: **** **** **** 4242</p>
    <p>Expiry: 12/25</p>
  </div>
</div>
```

**CORRECTED:**

```html
<!-- GOOD: Override to exclude payment section -->
<div class="user-card fs-mask">
  <h3>Account Details</h3>
  <p>Name: John Smith</p>
  <p>Email: john@example.com</p>
  
  <!-- Explicitly exclude payment section -->
  <div class="saved-payment fs-exclude">
    <p>Card: **** **** **** 4242</p>
    <p>Expiry: 12/25</p>
  </div>
</div>
```

### Example 5: Dynamic Content Without Privacy Classes

```javascript
// BAD: Dynamically added content without privacy consideration
function showUserDetails(user) {
  const html = `
    <div class="user-popup">
      <p>Name: ${user.name}</p>
      <p>Email: ${user.email}</p>
      <p>Phone: ${user.phone}</p>
      <p>SSN: ${user.ssn}</p>
    </div>
  `;
  // No privacy classes! All content visible
  document.body.insertAdjacentHTML('beforeend', html);
}
```

**CORRECTED:**

```javascript
// GOOD: Apply privacy classes to dynamic content
function showUserDetails(user) {
  const html = `
    <div class="user-popup fs-mask">
      <p>Name: ${user.name}</p>
      <p>Email: ${user.email}</p>
      <p>Phone: ${user.phone}</p>
      <p class="fs-exclude">SSN: ${user.ssn}</p>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', html);
}
```

### Example 6: Console Logging Sensitive Data

```javascript
// BAD: Logging sensitive data to console (captured by FS)
function processPayment(cardNumber, cvv) {
  console.log('Processing payment:', cardNumber, cvv);  // BAD!
  console.log('User SSN:', user.ssn);  // BAD!
}
```

**Why this is bad:**
- ❌ Console logs are captured by Fullstory
- ❌ Card number and CVV in console
- ❌ Privacy classes don't affect console

**CORRECTED:**

```javascript
// GOOD: Never log sensitive data, or disable console capture
function processPayment(cardNumber, cvv) {
  console.log('Processing payment for card ending:', cardNumber.slice(-4));
  // Or use FS.log which you control:
  FS('log', { level: 'info', msg: 'Payment processing initiated' });
}

// Or disable console capture in Fullstory settings
```

---

## Framework Integration

### React Component Library with Built-in Privacy

```jsx
// GOOD: React component library with privacy classes built-in
import React from 'react';

// Text Input - automatically masked
export function TextInput({ label, sensitive = false, ...props }) {
  const privacyClass = sensitive ? 'fs-exclude' : 'fs-mask';
  
  return (
    <div className={`form-field ${privacyClass}`}>
      <label>{label}</label>
      <input type="text" {...props} />
    </div>
  );
}

// Password Input - always excluded
export function PasswordInput({ label, ...props }) {
  return (
    <div className="form-field fs-exclude">
      <label>{label}</label>
      <input type="password" {...props} />
    </div>
  );
}

// Credit Card Input - always excluded
export function CreditCardInput({ label, ...props }) {
  return (
    <div className="form-field fs-exclude">
      <label>{label}</label>
      <input 
        type="text" 
        inputMode="numeric"
        autoComplete="cc-number"
        {...props} 
      />
    </div>
  );
}

// Public content - explicitly unmasked
export function PublicContent({ children }) {
  return (
    <div className="fs-unmask">
      {children}
    </div>
  );
}

// Usage
function CheckoutForm() {
  return (
    <form>
      <TextInput label="Full Name" name="name" />  {/* Masked */}
      <TextInput label="Email" name="email" />     {/* Masked */}
      <TextInput 
        label="SSN" 
        name="ssn" 
        sensitive={true}  // Excluded
      />
      <PasswordInput label="Password" />  {/* Excluded */}
      <CreditCardInput label="Card Number" />  {/* Excluded */}
      
      <PublicContent>
        <button type="submit">Submit</button>  {/* Visible */}
      </PublicContent>
    </form>
  );
}
```

### Vue Component with Privacy Props

```vue
<template>
  <div :class="privacyClass">
    <label>{{ label }}</label>
    <input :type="inputType" v-bind="$attrs" />
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  label: String,
  privacy: {
    type: String,
    default: 'mask',
    validator: (v) => ['exclude', 'mask', 'unmask'].includes(v)
  },
  inputType: {
    type: String,
    default: 'text'
  }
});

const privacyClass = computed(() => `fs-${props.privacy}`);
</script>

<!-- Usage -->
<FormInput label="Name" />  <!-- Masked by default -->
<FormInput label="SSN" privacy="exclude" />  <!-- Excluded -->
<FormInput label="Search" privacy="unmask" />  <!-- Visible -->
```

### Angular Directive

```typescript
// privacy.directive.ts
import { Directive, Input, ElementRef, OnInit } from '@angular/core';

@Directive({
  selector: '[fsPrivacy]'
})
export class PrivacyDirective implements OnInit {
  @Input() fsPrivacy: 'exclude' | 'mask' | 'unmask' = 'mask';
  
  constructor(private el: ElementRef) {}
  
  ngOnInit() {
    this.el.nativeElement.classList.add(`fs-${this.fsPrivacy}`);
  }
}

// Usage in template
<div fsPrivacy="exclude">Sensitive content</div>
<div fsPrivacy="mask">PII content</div>
<div fsPrivacy="unmask">Public content</div>
```

---

## CSS Selector Rules (Settings UI)

In addition to CSS classes, you can define rules via Settings > Data Capture and Privacy > Privacy.

### Supported Selectors

```css
/* Tag name */
input

/* Class */
.sensitive-field

/* ID */
#credit-card-input

/* Attribute */
[data-sensitive="true"]
[autocomplete^="cc-"]

/* Descendant */
.checkout-form input

/* Child */
.payment > input

/* Multiple classes */
.form-field.sensitive
```

### Unsupported Selectors

```css
/* NOT supported in Fullstory privacy rules */
:hover
:focus
:nth-child()
::before
::after
:not()
```

### Example Rules in Settings

| Selector | Rule Type | Purpose |
|----------|-----------|---------|
| `input[type=password]` | Exclude | All password fields |
| `.pii-field` | Mask | Custom PII class |
| `.payment-section input` | Exclude | All payment inputs |
| `[data-fs-privacy="exclude"]` | Exclude | Attribute-based |
| `.public-content` | Unmask | Public areas |

### Bulk Unmasking for Private by Default

```css
/* Unmask all navigation links */
nav a

/* Unmask all product titles */
.product-card h2, .product-card h3

/* Unmask all prices */
.price, [data-price], .product-price

/* Unmask all buttons */
button, .btn, [role="button"]

/* Unmask error messages */
.error-message, .alert, [role="alert"]
```

---

## Form Privacy Feature

Fullstory's Form Privacy feature (accounts created after Nov 10, 2021) provides additional automatic protection:

### Automatically Protected

- Input fields without explicit unmask
- Textarea content
- Select/dropdown selected values
- Content editable elements

### Form Privacy Modes

| Mode | Behavior |
|------|----------|
| Strict | All form inputs masked by default |
| Standard | Common sensitive fields masked |
| Off | Rely on manual privacy classes |

---

## Troubleshooting

### Content Still Visible After Excluding

**Symptom**: Added `.fs-exclude` but content still appears

**Common Causes**:
1. CSS specificity issue
2. Class added after page load
3. Conflicting unmask rule in Settings
4. Build tool removed the class

**Solutions**:
- Check browser DevTools for class presence
- Add class before Fullstory initializes
- Check Settings for conflicting rules
- Safelist `fs-*` classes in build config

### Clicks Not Captured on Masked Elements

**Symptom**: Masking works but clicks missing

**Common Causes**:
1. Used `.fs-exclude` instead of `.fs-mask`
2. Parent is excluded

**Solutions**:
- Use `.fs-mask` to keep click tracking
- Only use `.fs-exclude` when events shouldn't be tracked

### Dynamic Content Not Protected

**Symptom**: AJAX-loaded content visible in replay

**Common Causes**:
1. No privacy class on dynamic content
2. Content rendered before class applied

**Solutions**:
- Include privacy classes in template
- Use CSS selector rules as backup
- Apply classes in component library

---

## Reference Links

- **Privacy Protection**: https://help.fullstory.com/hc/en-us/articles/360020623574
- **Privacy Settings**: https://help.fullstory.com/hc/en-us/articles/360020622814
- **Private by Default**: https://help.fullstory.com/hc/en-us/articles/360044349073
- **Form Privacy**: https://help.fullstory.com/hc/en-us/articles/4411898245271
