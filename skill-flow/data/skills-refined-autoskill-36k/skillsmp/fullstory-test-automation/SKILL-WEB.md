---
name: fullstory-test-automation-web
version: v3
description: >
  WEB PLATFORM FILE — Part of fullstory-test-automation skill.
  Web test automation patterns for Fullstory-decorated codebases.
  Covers Cypress, Playwright, Selenium WebDriver, and WebdriverIO.
  Read SKILL.md first for discovery and analysis.
platform: web
parent_skill: fullstory-test-automation
related_skills:
  - fullstory-stable-selectors
  - fullstory-element-properties
  - fullstory-page-properties
  - fullstory-analytics-events
  - fullstory-privacy-controls
---

# Fullstory Test Automation - Web

**Prerequisites:** Read `SKILL.md` first for discovery, analysis, and decoration maturity assessment.

This skill covers web test automation frameworks:
- **Cypress** — Modern, developer-friendly
- **Playwright** — Microsoft's cross-browser solution
- **Selenium WebDriver** — Enterprise standard
- **WebdriverIO** — Node.js WebDriver bindings

---

## SELECTOR MAPPING (WEB)

### Stable Selectors

| Fullstory Attribute | Cypress | Playwright | Selenium |
|---------------------|---------|------------|----------|
| `data-element` | `cy.get('[data-element="X"]')` | `page.locator('[data-element="X"]')` | `By.cssSelector('[data-element="X"]')` |
| `data-component` | `cy.get('[data-component="X"]')` | `page.locator('[data-component="X"]')` | `By.cssSelector('[data-component="X"]')` |
| `data-testid` | `cy.get('[data-testid="X"]')` | `page.getByTestId('X')` | `By.cssSelector('[data-testid="X"]')` |
| `data-action` | `cy.get('[data-action="X"]')` | `page.locator('[data-action="X"]')` | `By.cssSelector('[data-action="X"]')` |
| `data-state` | `cy.get('[data-state="X"]')` | `page.locator('[data-state="X"]')` | `By.cssSelector('[data-state="X"]')` |

### Element Properties

| Fullstory Attribute | Cypress | Playwright | Selenium |
|---------------------|---------|------------|----------|
| `data-fs-element` | `cy.get('[data-fs-element="X"]')` | `page.locator('[data-fs-element="X"]')` | `By.cssSelector('[data-fs-element="X"]')` |
| `data-product-id` | `cy.get('[data-product-id="X"]')` | `page.locator('[data-product-id="X"]')` | `By.cssSelector('[data-product-id="X"]')` |
| `data-price` | `cy.get('[data-price="X"]')` | `page.locator('[data-price="X"]')` | `By.cssSelector('[data-price="X"]')` |
| Custom properties | `cy.get('[data-{prop}="X"]')` | `page.locator('[data-{prop}="X"]')` | `By.cssSelector('[data-{prop}="X"]')` |

### Privacy Classes

| Fullstory Class | Cypress | Playwright | Selenium |
|-----------------|---------|------------|----------|
| `.fs-exclude` | `cy.get('.fs-exclude')` | `page.locator('.fs-exclude')` | `By.className('fs-exclude')` |
| `.fs-mask` | `cy.get('.fs-mask')` | `page.locator('.fs-mask')` | `By.className('fs-mask')` |
| `.fs-unmask` | `cy.get('.fs-unmask')` | `page.locator('.fs-unmask')` | `By.className('fs-unmask')` |

---

## CYPRESS

### Configuration

```javascript
// cypress.config.js
module.exports = {
  e2e: {
    setupNodeEvents(on, config) {
      // ...
    },
  },
};

// cypress/support/e2e.js
Cypress.SelectorPlayground.defaults({
  selectorPriority: [
    'data-element',
    'data-component', 
    'data-testid',
    'data-action',
    'aria-label',
    'id',
    'class',
    'tag'
  ]
});
```

### Selector Helpers

```javascript
// cypress/support/selectors.js

/**
 * Fullstory-aligned selector helpers for Cypress
 */
export const Selectors = {
  // Select by element role
  element: (name) => cy.get(`[data-element="${name}"]`),
  
  // Select by component
  component: (name) => cy.get(`[data-component="${name}"]`),
  
  // Select element within component
  componentElement: (component, element) => 
    cy.get(`[data-component="${component}"] [data-element="${element}"]`),
  
  // Select by action
  action: (name) => cy.get(`[data-action="${name}"]`),
  
  // Select by testid (Playwright compatibility)
  testId: (id) => cy.get(`[data-testid="${id}"]`),
  
  // Select by Fullstory element name
  fsElement: (name) => cy.get(`[data-fs-element="${name}"]`),
  
  // Select by state
  elementWithState: (element, state) => 
    cy.get(`[data-element="${element}"][data-state="${state}"]`),
    
  // Select by property value
  withProperty: (prop, value) => cy.get(`[data-${prop}="${value}"]`),
};

// Usage
Selectors.element('add-to-cart').click();
Selectors.componentElement('ProductCard', 'price').should('contain', '$99.99');
Selectors.action('submit-order').should('be.visible');
Selectors.withProperty('product-id', 'SKU-123').click();
```

### Page Object Pattern

```javascript
// cypress/pages/CheckoutPage.js

/**
 * Checkout Page Object - Generated from Fullstory decoration
 */
class CheckoutPage {
  // Page identification
  static pageName = 'Checkout';
  
  // Component selectors (from data-component)
  static components = {
    form: '[data-component="CheckoutForm"]',
    summary: '[data-component="OrderSummary"]',
    payment: '[data-component="PaymentSection"]',
  };
  
  // Element selectors (from data-element)
  static elements = {
    // Shipping section
    shippingFirstName: '[data-element="shipping-first-name"]',
    shippingLastName: '[data-element="shipping-last-name"]',
    shippingAddress: '[data-element="shipping-address"]',
    shippingCity: '[data-element="shipping-city"]',
    shippingZip: '[data-element="shipping-zip"]',
    
    // Payment section (may be excluded/masked)
    cardNumber: '[data-element="card-number"]',
    cardExpiry: '[data-element="card-expiry"]',
    cardCvv: '[data-element="card-cvv"]',
    
    // Summary
    orderTotal: '[data-element="order-total"]',
    itemCount: '[data-element="item-count"]',
  };
  
  // Action selectors (from data-action)
  static actions = {
    submitOrder: '[data-action="submit-order"]',
    applyCoupon: '[data-action="apply-coupon"]',
  };
  
  // Page methods
  visit() {
    cy.visit('/checkout');
    cy.get(CheckoutPage.components.form).should('exist');
    return this;
  }
  
  fillShippingInfo(info) {
    cy.get(CheckoutPage.elements.shippingFirstName).type(info.firstName);
    cy.get(CheckoutPage.elements.shippingLastName).type(info.lastName);
    cy.get(CheckoutPage.elements.shippingAddress).type(info.address);
    cy.get(CheckoutPage.elements.shippingCity).type(info.city);
    cy.get(CheckoutPage.elements.shippingZip).type(info.zip);
    return this;
  }
  
  fillPaymentInfo(info) {
    cy.get(CheckoutPage.elements.cardNumber).type(info.cardNumber);
    cy.get(CheckoutPage.elements.cardExpiry).type(info.expiry);
    cy.get(CheckoutPage.elements.cardCvv).type(info.cvv);
    return this;
  }
  
  submitOrder() {
    cy.get(CheckoutPage.actions.submitOrder).click();
    return this;
  }
  
  verifyOrderTotal(expectedTotal) {
    cy.get(CheckoutPage.elements.orderTotal).should('contain', expectedTotal);
    return this;
  }
}

export default CheckoutPage;

// Usage in test
import CheckoutPage from '../pages/CheckoutPage';

describe('Checkout Flow', () => {
  it('completes a purchase', () => {
    const checkout = new CheckoutPage();
    
    checkout
      .visit()
      .fillShippingInfo({
        firstName: 'John',
        lastName: 'Test',
        address: '123 Test St',
        city: 'Testville',
        zip: '12345'
      })
      .fillPaymentInfo({
        cardNumber: '4111111111111111',
        expiry: '12/25',
        cvv: '123'
      })
      .verifyOrderTotal('$99.99')
      .submitOrder();
    
    cy.url().should('include', '/confirmation');
  });
});
```

### Test Data Capture (Cypress)

```javascript
// cypress/support/commands.js

// Track test input for masked fields
Cypress.Commands.add('typeTracked', { prevSubject: 'element' }, (subject, text, options = {}) => {
  const element = subject[0];
  const fieldName = element.getAttribute('data-element') || 
                    element.getAttribute('data-testid') ||
                    element.name;
  const component = element.closest('[data-component]')?.getAttribute('data-component');
  
  cy.window().then((win) => {
    if (win.FS && win.__TEST_AUTOMATION__) {
      win.FS('trackEvent', {
        name: 'Test Automation Input',
        properties: {
          field_name: fieldName,
          field_value: text,
          component: component,
          test_name: Cypress.currentTest.title,
        }
      });
    }
  });
  
  return cy.wrap(subject).type(text, options);
});

// Setup test automation session
Cypress.Commands.add('setupTestSession', () => {
  cy.window().then(win => {
    win.__TEST_AUTOMATION__ = true;
    
    if (win.FS) {
      win.FS('setProperties', {
        type: 'page',
        properties: {
          is_test_session: true,
          test_framework: 'cypress',
          test_name: Cypress.currentTest.title,
        }
      });
    }
  });
});

// Usage
beforeEach(() => {
  cy.setupTestSession();
});

cy.get('[data-element="card-number"]').typeTracked('4111111111111111');
```

### Event Verification (Cypress)

```javascript
// cypress/support/commands.js

Cypress.Commands.add('spyOnFullstoryEvents', () => {
  cy.window().then(win => {
    win.__FS_TRACKED_EVENTS__ = [];
    
    const originalFS = win.FS;
    win.FS = function(method, payload) {
      if (method === 'trackEvent') {
        win.__FS_TRACKED_EVENTS__.push(payload);
      }
      return originalFS?.apply(this, arguments);
    };
  });
});

Cypress.Commands.add('assertFullstoryEvent', (eventName, expectedProperties = {}) => {
  cy.window().then(win => {
    const events = win.__FS_TRACKED_EVENTS__ || [];
    const matchingEvent = events.find(e => e.name === eventName);
    
    expect(matchingEvent, `Event "${eventName}" should have been tracked`).to.exist;
    
    Object.entries(expectedProperties).forEach(([key, value]) => {
      expect(matchingEvent.properties[key]).to.equal(value);
    });
  });
});

// Usage
describe('Event Tracking', () => {
  beforeEach(() => {
    cy.spyOnFullstoryEvents();
  });
  
  it('should track Product Added event', () => {
    cy.get('[data-action="add-to-cart"]').click();
    cy.assertFullstoryEvent('Product Added', { product_id: 'SKU-123' });
  });
});
```

---

## PLAYWRIGHT

### Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    // Use data-element as primary test ID attribute
    testIdAttribute: 'data-element',
  },
});
```

### Selector Helpers

```typescript
// tests/helpers/selectors.ts

import { Page, Locator } from '@playwright/test';

/**
 * Fullstory-aligned selector helpers for Playwright
 */
export class Selectors {
  constructor(private page: Page) {}
  
  // Select by element (uses configured testIdAttribute)
  element(name: string): Locator {
    return this.page.getByTestId(name);
  }
  
  // Select by component
  component(name: string): Locator {
    return this.page.locator(`[data-component="${name}"]`);
  }
  
  // Select element within component
  componentElement(component: string, element: string): Locator {
    return this.page.locator(`[data-component="${component}"] [data-element="${element}"]`);
  }
  
  // Select by action
  action(name: string): Locator {
    return this.page.locator(`[data-action="${name}"]`);
  }
  
  // Select by Fullstory element name
  fsElement(name: string): Locator {
    return this.page.locator(`[data-fs-element="${name}"]`);
  }
  
  // Select by state
  elementWithState(element: string, state: string): Locator {
    return this.page.locator(`[data-element="${element}"][data-state="${state}"]`);
  }
  
  // Select by property value
  withProperty(prop: string, value: string): Locator {
    return this.page.locator(`[data-${prop}="${value}"]`);
  }
  
  // Semantic selectors
  button(text: string): Locator {
    return this.page.getByRole('button', { name: text });
  }
  
  link(text: string): Locator {
    return this.page.getByRole('link', { name: text });
  }
  
  input(label: string): Locator {
    return this.page.getByLabel(label);
  }
}

// Usage
const sel = new Selectors(page);
await sel.element('add-to-cart').click();
await sel.componentElement('ProductCard', 'price').toContainText('$99.99');
await sel.withProperty('product-id', 'SKU-123').click();
```

### Page Object Pattern

```typescript
// tests/pages/CheckoutPage.ts

import { Page, Locator, expect } from '@playwright/test';

/**
 * Checkout Page Object - Generated from Fullstory decoration
 */
export class CheckoutPage {
  readonly page: Page;
  
  // Components
  readonly checkoutForm: Locator;
  readonly orderSummary: Locator;
  readonly paymentSection: Locator;
  
  // Elements - Shipping
  readonly shippingFirstName: Locator;
  readonly shippingLastName: Locator;
  readonly shippingAddress: Locator;
  readonly shippingCity: Locator;
  readonly shippingZip: Locator;
  
  // Elements - Payment
  readonly cardNumber: Locator;
  readonly cardExpiry: Locator;
  readonly cardCvv: Locator;
  
  // Actions
  readonly submitOrderButton: Locator;
  readonly applyCouponButton: Locator;
  
  // Summary
  readonly orderTotal: Locator;
  
  constructor(page: Page) {
    this.page = page;
    
    // Components
    this.checkoutForm = page.locator('[data-component="CheckoutForm"]');
    this.orderSummary = page.locator('[data-component="OrderSummary"]');
    this.paymentSection = page.locator('[data-component="PaymentSection"]');
    
    // Shipping elements
    this.shippingFirstName = page.getByTestId('shipping-first-name');
    this.shippingLastName = page.getByTestId('shipping-last-name');
    this.shippingAddress = page.getByTestId('shipping-address');
    this.shippingCity = page.getByTestId('shipping-city');
    this.shippingZip = page.getByTestId('shipping-zip');
    
    // Payment elements
    this.cardNumber = page.getByTestId('card-number');
    this.cardExpiry = page.getByTestId('card-expiry');
    this.cardCvv = page.getByTestId('card-cvv');
    
    // Action elements
    this.submitOrderButton = page.locator('[data-action="submit-order"]');
    this.applyCouponButton = page.locator('[data-action="apply-coupon"]');
    
    // Summary elements
    this.orderTotal = page.getByTestId('order-total');
  }
  
  async goto() {
    await this.page.goto('/checkout');
    await expect(this.checkoutForm).toBeVisible();
  }
  
  async fillShippingInfo(info: {
    firstName: string;
    lastName: string;
    address: string;
    city: string;
    zip: string;
  }) {
    await this.shippingFirstName.fill(info.firstName);
    await this.shippingLastName.fill(info.lastName);
    await this.shippingAddress.fill(info.address);
    await this.shippingCity.fill(info.city);
    await this.shippingZip.fill(info.zip);
  }
  
  async fillPaymentInfo(info: {
    cardNumber: string;
    expiry: string;
    cvv: string;
  }) {
    await this.cardNumber.fill(info.cardNumber);
    await this.cardExpiry.fill(info.expiry);
    await this.cardCvv.fill(info.cvv);
  }
  
  async submitOrder() {
    await this.submitOrderButton.click();
  }
  
  async verifyOrderTotal(expectedTotal: string) {
    await expect(this.orderTotal).toContainText(expectedTotal);
  }
}

// Usage in test
import { test, expect } from '@playwright/test';
import { CheckoutPage } from './pages/CheckoutPage';

test('completes a purchase', async ({ page }) => {
  const checkout = new CheckoutPage(page);
  
  await checkout.goto();
  
  await checkout.fillShippingInfo({
    firstName: 'John',
    lastName: 'Test',
    address: '123 Test St',
    city: 'Testville',
    zip: '12345'
  });
  
  await checkout.fillPaymentInfo({
    cardNumber: '4111111111111111',
    expiry: '12/25',
    cvv: '123'
  });
  
  await checkout.verifyOrderTotal('$99.99');
  await checkout.submitOrder();
  
  await expect(page).toHaveURL(/\/confirmation/);
});
```

### Test Data Capture (Playwright)

```typescript
// tests/helpers/testDataCapture.ts

import { Page } from '@playwright/test';

export async function setupTestSession(page: Page, testName: string) {
  await page.evaluate((testName) => {
    window.__TEST_AUTOMATION__ = true;
    
    if (window.FS) {
      window.FS('setProperties', {
        type: 'page',
        properties: {
          is_test_session: true,
          test_framework: 'playwright',
          test_name: testName,
        }
      });
    }
  }, testName);
}

export async function trackTestInput(page: Page, field: string, value: string) {
  await page.evaluate(({ field, value }) => {
    if (window.FS && window.__TEST_AUTOMATION__) {
      window.FS('trackEvent', {
        name: 'Test Automation Input',
        properties: {
          field_name: field,
          field_value: value,
        }
      });
    }
  }, { field, value });
}

// Usage
test.beforeEach(async ({ page }) => {
  await setupTestSession(page, test.info().title);
});

// For masked fields
await page.locator('[data-element="card-number"]').fill('4111111111111111');
await trackTestInput(page, 'card-number', '4111111111111111');
```

### Event Verification (Playwright)

```typescript
// tests/helpers/eventVerification.ts

import { Page, expect } from '@playwright/test';

export async function spyOnFullstoryEvents(page: Page) {
  await page.evaluate(() => {
    window.__FS_TRACKED_EVENTS__ = [];
    
    const originalFS = window.FS;
    window.FS = function(method: string, payload: any) {
      if (method === 'trackEvent') {
        window.__FS_TRACKED_EVENTS__.push(payload);
      }
      return originalFS?.apply(this, arguments);
    };
  });
}

export async function assertFullstoryEvent(
  page: Page, 
  eventName: string, 
  expectedProperties?: Record<string, any>
) {
  const events = await page.evaluate(() => window.__FS_TRACKED_EVENTS__ || []);
  const matchingEvent = events.find((e: any) => e.name === eventName);
  
  expect(matchingEvent, `Event "${eventName}" should have been tracked`).toBeDefined();
  
  if (expectedProperties) {
    for (const [key, value] of Object.entries(expectedProperties)) {
      expect(matchingEvent.properties[key]).toBe(value);
    }
  }
}

// Usage
test('should track checkout completion', async ({ page }) => {
  await spyOnFullstoryEvents(page);
  
  // ... perform checkout
  
  await assertFullstoryEvent(page, 'Order Completed', {
    order_id: expect.stringMatching(/^ORD-/),
  });
});
```

### Property Assertions (Playwright)

```typescript
// Rich assertions using element properties

test('verify product properties', async ({ page }) => {
  const productCard = page.locator('[data-component="ProductCard"]').first();
  
  // Assert element properties
  await expect(productCard).toHaveAttribute('data-product-id', /^SKU-/);
  await expect(productCard).toHaveAttribute('data-in-stock', 'true');
  await expect(productCard).toHaveAttribute('data-category', 'Electronics');
  
  // Extract and verify price
  const price = await productCard.getAttribute('data-price');
  expect(parseFloat(price!)).toBeGreaterThan(0);
  
  // Verify Fullstory element name
  await expect(productCard).toHaveAttribute('data-fs-element', 'Product Card');
});

// Data-driven targeting
test('add in-stock product to cart', async ({ page }) => {
  // Find first in-stock product
  const inStockProduct = page.locator('[data-component="ProductCard"][data-in-stock="true"]').first();
  await inStockProduct.locator('[data-action="add-to-cart"]').click();
});
```

---

## SELENIUM WEBDRIVER

### Selector Helpers (Java)

```java
// selenium/src/main/java/selectors/FullstorySelectors.java

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

/**
 * Fullstory-aligned selector helpers for Selenium
 */
public class FullstorySelectors {
    
    private final WebDriver driver;
    
    public FullstorySelectors(WebDriver driver) {
        this.driver = driver;
    }
    
    // Select by element role
    public WebElement element(String name) {
        return driver.findElement(By.cssSelector(
            String.format("[data-element=\"%s\"]", name)
        ));
    }
    
    // Select by component
    public WebElement component(String name) {
        return driver.findElement(By.cssSelector(
            String.format("[data-component=\"%s\"]", name)
        ));
    }
    
    // Select element within component
    public WebElement componentElement(String component, String element) {
        return driver.findElement(By.cssSelector(
            String.format("[data-component=\"%s\"] [data-element=\"%s\"]", component, element)
        ));
    }
    
    // Select by action
    public WebElement action(String name) {
        return driver.findElement(By.cssSelector(
            String.format("[data-action=\"%s\"]", name)
        ));
    }
    
    // Select by property value
    public WebElement withProperty(String prop, String value) {
        return driver.findElement(By.cssSelector(
            String.format("[data-%s=\"%s\"]", prop, value)
        ));
    }
    
    // By selectors for explicit waits
    public static By byElement(String name) {
        return By.cssSelector(String.format("[data-element=\"%s\"]", name));
    }
    
    public static By byComponent(String name) {
        return By.cssSelector(String.format("[data-component=\"%s\"]", name));
    }
    
    public static By byAction(String name) {
        return By.cssSelector(String.format("[data-action=\"%s\"]", name));
    }
}

// Usage
FullstorySelectors sel = new FullstorySelectors(driver);
sel.element("add-to-cart").click();
sel.componentElement("ProductCard", "price").getText();
sel.withProperty("product-id", "SKU-123").click();
```

---

## WEBDRIVERIO

### Custom Commands

```javascript
// wdio/support/commands.js

browser.addCommand('$element', function(name) {
  return this.$(`[data-element="${name}"]`);
});

browser.addCommand('$component', function(name) {
  return this.$(`[data-component="${name}"]`);
});

browser.addCommand('$componentElement', function(component, element) {
  return this.$(`[data-component="${component}"] [data-element="${element}"]`);
});

browser.addCommand('$action', function(name) {
  return this.$(`[data-action="${name}"]`);
});

browser.addCommand('$withProperty', function(prop, value) {
  return this.$(`[data-${prop}="${value}"]`);
});

// Usage
await browser.$element('add-to-cart').click();
await browser.$componentElement('ProductCard', 'price').getText();
await browser.$withProperty('product-id', 'SKU-123').click();
```

---

## PAGE OBJECT GENERATION

### Auto-Generate from Decorated HTML

```javascript
// tools/generatePageObjects.js

const { JSDOM } = require('jsdom');

/**
 * Generate Page Objects from HTML decorated with Fullstory attributes
 */
function generatePageObject(htmlContent, options = {}) {
  const { framework = 'playwright', className = 'GeneratedPage' } = options;
  const dom = new JSDOM(htmlContent);
  const document = dom.window.document;
  
  // Extract decoration
  const components = [...document.querySelectorAll('[data-component]')].map(el => ({
    name: el.getAttribute('data-component'),
    selector: `[data-component="${el.getAttribute('data-component')}"]`,
  }));
  
  const elements = [...document.querySelectorAll('[data-element]')].map(el => ({
    name: el.getAttribute('data-element'),
    selector: `[data-element="${el.getAttribute('data-element')}"]`,
    isInput: ['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName),
  }));
  
  const actions = [...document.querySelectorAll('[data-action]')].map(el => ({
    name: el.getAttribute('data-action'),
    selector: `[data-action="${el.getAttribute('data-action')}"]`,
  }));
  
  // Generate code
  if (framework === 'playwright') {
    return generatePlaywrightClass({ components, elements, actions, className });
  } else if (framework === 'cypress') {
    return generateCypressClass({ components, elements, actions, className });
  }
}

function generatePlaywrightClass({ components, elements, actions, className }) {
  const camelCase = (s) => s.replace(/-([a-z])/g, (g) => g[1].toUpperCase());
  
  return `
import { Page, Locator, expect } from '@playwright/test';

export class ${className} {
  readonly page: Page;
  
  // Components
${components.map(c => `  readonly ${camelCase(c.name)}: Locator;`).join('\n')}
  
  // Elements
${elements.map(e => `  readonly ${camelCase(e.name)}: Locator;`).join('\n')}
  
  constructor(page: Page) {
    this.page = page;
    
${components.map(c => `    this.${camelCase(c.name)} = page.locator('${c.selector}');`).join('\n')}
${elements.map(e => `    this.${camelCase(e.name)} = page.locator('${e.selector}');`).join('\n')}
  }
  
  // Generated fill methods for inputs
${elements.filter(e => e.isInput).map(e => `
  async fill${camelCase(e.name).charAt(0).toUpperCase() + camelCase(e.name).slice(1)}(value: string) {
    await this.${camelCase(e.name)}.fill(value);
  }`).join('\n')}
  
  // Generated action methods
${actions.map(a => `
  async ${camelCase(a.name)}() {
    await this.page.locator('${a.selector}').click();
  }`).join('\n')}
}
`;
}

module.exports = { generatePageObject };
```

---

## COMPLETE EXAMPLE

### E-Commerce Checkout Test (Playwright)

```typescript
import { test, expect, Page } from '@playwright/test';
import { CheckoutPage } from './pages/CheckoutPage';
import { setupTestSession, trackTestInput } from './helpers/testDataCapture';
import { spyOnFullstoryEvents, assertFullstoryEvent } from './helpers/eventVerification';

test.describe('E-Commerce Checkout', () => {
  test.beforeEach(async ({ page }) => {
    await setupTestSession(page, test.info().title);
    await spyOnFullstoryEvents(page);
  });
  
  test('complete checkout with event verification', async ({ page }) => {
    // Navigate to product
    await page.goto('/products');
    
    // Select in-stock product using property
    const product = page.locator('[data-component="ProductCard"][data-in-stock="true"]').first();
    await product.click();
    
    // Verify product detail page
    await expect(page.locator('[data-component="ProductDetail"]')).toBeVisible();
    
    // Add to cart
    await page.locator('[data-action="add-to-cart"]').click();
    
    // Verify event tracked
    await assertFullstoryEvent(page, 'Product Added');
    
    // Go to checkout
    await page.locator('[data-action="checkout"]').click();
    
    const checkout = new CheckoutPage(page);
    await expect(checkout.checkoutForm).toBeVisible();
    
    // Fill shipping
    await checkout.fillShippingInfo({
      firstName: 'John',
      lastName: 'Test',
      address: '123 Test St',
      city: 'Testville',
      zip: '12345'
    });
    
    // Fill payment (masked fields - track for debugging)
    await checkout.cardNumber.fill('4111111111111111');
    await trackTestInput(page, 'card-number', '4111111111111111');
    
    await checkout.cardExpiry.fill('12/25');
    await checkout.cardCvv.fill('123');
    await trackTestInput(page, 'card-cvv', '123');
    
    // Submit
    await checkout.submitOrder();
    
    // Verify completion
    await assertFullstoryEvent(page, 'Order Completed');
    await expect(page.locator('[data-component="OrderConfirmation"]')).toBeVisible();
  });
});
```

---

## REFERENCE LINKS

### This Skill's Files
- **Core (Discovery & Routing)**: `./SKILL.md`
- **Mobile Platform**: `./SKILL-MOBILE.md`

### Fullstory Skills
- **Stable Selectors**: ../fullstory-stable-selectors/SKILL.md
- **Element Properties**: ../../core/fullstory-element-properties/SKILL.md
- **Page Properties**: ../../core/fullstory-page-properties/SKILL.md
- **Privacy Controls**: ../../core/fullstory-privacy-controls/SKILL.md
- **Analytics Events**: ../../core/fullstory-analytics-events/SKILL.md

### Framework Documentation
- **Cypress Best Practices**: https://docs.cypress.io/guides/references/best-practices
- **Playwright Locators**: https://playwright.dev/docs/locators
- **Selenium WebDriver**: https://www.selenium.dev/documentation/webdriver/
- **WebdriverIO**: https://webdriver.io/docs/selectors

---

*This file covers web test automation. For mobile, see `./SKILL-MOBILE.md`. For discovery and analysis, see `./SKILL.md`.*
