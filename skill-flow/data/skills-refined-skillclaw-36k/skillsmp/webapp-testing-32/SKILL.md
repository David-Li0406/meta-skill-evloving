---
name: webapp-testing
description: 'Toolkit cho testing và debugging local web applications sử dụng Playwright. Hỗ trợ verify frontend functionality, debug UI behavior, capture screenshots, view browser logs.'
---

# Web Application Testing Skill

Skill này enable comprehensive testing và debugging của web applications sử dụng Playwright automation.

## Khi Nào Sử Dụng

- Test frontend functionality trong real browser
- Verify UI behavior và interactions
- Debug web application issues
- Capture screenshots cho documentation/debugging
- Inspect browser console logs
- Validate form submissions và user flows
- Check responsive design across viewports

## Prerequisites

- Node.js installed
- Locally running web application (hoặc accessible URL)
- Playwright sẽ auto-install nếu chưa có

---

## Core Capabilities

### 1. Browser Automation

| Action | Description |
|--------|-------------|
| Navigate | Go to URLs |
| Click | Buttons, links |
| Fill | Form fields |
| Select | Dropdowns |
| Handle | Dialogs, alerts |

### 2. Verification

| Check | Description |
|-------|-------------|
| Element presence | Assert element exists |
| Text content | Verify text |
| Visibility | Check element visible |
| URLs | Validate navigation |
| Responsive | Test viewports |

### 3. Debugging

| Feature | Description |
|---------|-------------|
| Screenshots | Capture page state |
| Console logs | View browser console |
| Network | Inspect requests |
| Failed tests | Debug failures |

---

## Usage Examples

### Basic Navigation Test
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto('http://localhost:3000');
  await page.click('text=Login');
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'password123');
  await page.click('button[type="submit"]');
  
  // Verify login success
  await page.waitForSelector('.dashboard');
  
  await browser.close();
})();
```

### Screenshot Capture
```javascript
await page.screenshot({ path: 'screenshot.png', fullPage: true });
```

### Viewport Testing
```javascript
const viewports = [
  { width: 375, height: 667, name: 'mobile' },
  { width: 768, height: 1024, name: 'tablet' },
  { width: 1280, height: 720, name: 'desktop' },
];

for (const vp of viewports) {
  await page.setViewportSize({ width: vp.width, height: vp.height });
  await page.screenshot({ path: `${vp.name}.png` });
}
```

### Form Validation Test
```javascript
// Test empty form submission
await page.click('button[type="submit"]');
const errorMessage = await page.textContent('.error');
expect(errorMessage).toBe('Email is required');

// Test invalid email
await page.fill('#email', 'invalid-email');
await page.click('button[type="submit"]');
const emailError = await page.textContent('.email-error');
expect(emailError).toBe('Please enter a valid email');
```

---

## Testing Patterns

### Page Object Model
```javascript
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = '#email';
    this.passwordInput = '#password';
    this.submitButton = 'button[type="submit"]';
  }

  async login(email, password) {
    await this.page.fill(this.emailInput, email);
    await this.page.fill(this.passwordInput, password);
    await this.page.click(this.submitButton);
  }
}
```

### Wait Strategies
```javascript
// Wait for element
await page.waitForSelector('.element');

// Wait for navigation
await page.waitForNavigation();

// Wait for network idle
await page.waitForLoadState('networkidle');

// Custom timeout
await page.waitForSelector('.element', { timeout: 10000 });
```

---

## Guidelines

1. **Always verify app is running** - Check server accessible before tests
2. **Use explicit waits** - Wait for elements/navigation before interacting
3. **Capture screenshots on failure** - Help debug issues
4. **Clean up resources** - Always close browser when done
5. **Handle timeouts gracefully** - Set reasonable timeouts
6. **Test incrementally** - Start simple before complex flows
7. **Use selectors wisely** - Prefer data-testid hoặc role-based selectors

---

## Common Selectors

| Type | Example | Best For |
|------|---------|----------|
| Test ID | `[data-testid="login-btn"]` | Explicit test hooks |
| Role | `role=button[name="Submit"]` | Accessibility |
| Text | `text=Click me` | Visible text |
| CSS | `.class-name` | Styling hooks |
| ID | `#element-id` | Unique elements |

---

## Viewport Reference

| Name | Width | Device |
|------|-------|--------|
| Mobile | 375px | iPhone SE/12 mini |
| Tablet | 768px | iPad |
| Desktop | 1280px | Standard PC |
| Wide | 1920px | Large display |

---

## Limitations

- Requires running web application
- Cannot test native mobile apps
- Network-dependent for external resources
- Some interactions may need workarounds
