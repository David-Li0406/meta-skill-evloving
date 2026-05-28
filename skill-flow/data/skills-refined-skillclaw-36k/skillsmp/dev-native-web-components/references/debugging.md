````markdown
# Debugging Reference

> Debug native web components with Playwright MCP Server and browser DevTools.

---

## Primary: Playwright MCP Server

Use the [Playwright MCP Server](https://github.com/microsoft/playwright-mcp) for automated browser debugging from your IDE.

### Setup

```bash
# Install Playwright MCP Server
npm install -g @anthropic/playwright-mcp

# Or use npx
npx @anthropic/playwright-mcp
```

### MCP Server Configuration

Add to your MCP settings (`.claude/mcp.json` or VS Code settings):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@anthropic/playwright-mcp"]
    }
  }
}
```

### Available Tools

| Tool | Description |
|------|-------------|
| `playwright_navigate` | Navigate to URL |
| `playwright_screenshot` | Capture viewport screenshot |
| `playwright_click` | Click element by selector |
| `playwright_fill` | Fill input field |
| `playwright_evaluate` | Execute JS in browser |
| `playwright_select` | Select option from dropdown |
| `playwright_hover` | Hover over element |
| `playwright_console` | Get browser console logs |
| `playwright_network` | Inspect network requests |

### Debugging Web Components with MCP

```typescript
// Example: Inspect Shadow DOM via MCP
// Use playwright_evaluate to query Shadow DOM

await playwright_evaluate({
  expression: `
    const component = document.querySelector('my-card');
    const shadow = component.shadowRoot;
    return {
      styles: shadow.querySelector('style')?.textContent,
      slots: [...shadow.querySelectorAll('slot')].map(s => s.name || 'default'),
      assignedElements: shadow.querySelector('slot')?.assignedElements().length
    };
  `
});
```

### Screenshot Debugging

```typescript
// Capture component state
await playwright_screenshot({ 
  selector: 'my-card',
  fullPage: false 
});
```

---

## Related Skill: playwright-testing

For comprehensive E2E testing of web components, use the `playwright-testing` skill.

**Key references from playwright-testing:**
- `references/best-practices.md` — Testing patterns
- `references/debugging.md` — Detailed debugging guide
- `assets/examples/` — Test examples including accessibility and visual tests

### Integration Pattern

```typescript
// src/e2e/components/my-card.spec.ts
import { test, expect } from '@playwright/test';

test.describe('my-card component', () => {
  test('renders with DSD', async ({ page }) => {
    await page.goto('/components/my-card');
    
    // Query shadow DOM
    const card = page.locator('my-card');
    const shadowContent = card.locator('internal:shadow=.content');
    
    await expect(shadowContent).toBeVisible();
  });
  
  test('slots content correctly', async ({ page }) => {
    await page.goto('/components/my-card');
    
    const card = page.locator('my-card');
    const slottedTitle = card.locator('h2[slot="title"]');
    
    await expect(slottedTitle).toHaveText('Card Title');
  });
});
```

---

## Secondary: Browser DevTools

When MCP tools are not available, use native browser DevTools.

### Chrome DevTools

#### Inspect Shadow DOM

1. Open DevTools (F12)
2. Elements panel → expand component
3. `#shadow-root (open)` shows shadow content
4. Click elements inside to inspect

#### Shadow DOM Settings

**DevTools → Settings → Preferences:**
- ✅ Show user agent shadow DOM
- ✅ Show CSS custom properties

#### Console Queries

```typescript
// Get shadow root
const card = document.querySelector('my-card') as HTMLElement;
const shadow = card.shadowRoot!;

// Query inside shadow
shadow.querySelector('.content');
shadow.querySelectorAll('slot');

// Get slotted elements
const slot = shadow.querySelector('slot') as HTMLSlotElement;
slot.assignedElements();
slot.assignedNodes();

// Check computed styles
getComputedStyle(shadow.querySelector('.content')!);
```

#### Styles Panel

1. Select element in shadow DOM
2. Styles panel shows scoped styles
3. `:host` rules visible when selecting host element
4. `::slotted()` rules visible when selecting slotted content

---

### Firefox DevTools

Firefox has excellent Shadow DOM support:

1. **Inspector** → Expand component
2. **#shadow-root** node visible
3. **Style Editor** → Shows all stylesheets including shadow

#### Firefox-Specific Features

- **Accessibility Inspector**: Great for checking ARIA in shadow DOM
- **Flexbox/Grid Inspector**: Works inside shadow DOM
- **Font Inspector**: Shows inherited fonts

---

### Safari Web Inspector

1. **Develop menu** → Show Web Inspector
2. **Elements tab** → Expand custom elements
3. **Shadow Root** content visible

---

## Debugging Common Issues

### Issue: Styles Not Applying

```typescript
// Check if styles are in shadow DOM
const shadow = (document.querySelector('my-card') as HTMLElement).shadowRoot!;
const style = shadow.querySelector('style');
console.log(style?.textContent);

// Check computed value
const host = document.querySelector('my-card') as HTMLElement;
console.log(getComputedStyle(host).display); // Should be 'block' from :host
```

### Issue: Slots Not Receiving Content

```typescript
// Check slot assignment
const slot = shadow.querySelector('slot[name="header"]') as HTMLSlotElement;
console.log('Assigned elements:', slot.assignedElements());

// Check if content has correct slot attribute
const content = document.querySelector('[slot="header"]');
console.log('Content:', content, 'Parent:', content?.parentElement);
```

### Issue: Events Not Bubbling

```typescript
// Check event listeners
const component = document.querySelector('my-card') as HTMLElement;
component.addEventListener('click', (e: Event) => {
  console.log('Event target:', e.target);
  console.log('Composed path:', e.composedPath());
});

// Events from shadow DOM
// Use { bubbles: true, composed: true } for events to cross shadow boundary
```

### Issue: Container Queries Not Working

```typescript
// Check container-type
const container = shadow.querySelector('.wrapper') as HTMLElement;
console.log(getComputedStyle(container).containerType);

// Verify container size
console.log(container.clientWidth);
```

---

## DevTools Extensions

### Web Components DevTools

- **Chrome**: No official extension; use built-in Shadow DOM inspection
- **Firefox**: Native support excellent

### Lighthouse

Run Lighthouse audits for web component pages:

```bash
# CLI
npx lighthouse http://localhost:3000 --view

# Or use Chrome DevTools → Lighthouse tab
```

### Accessibility Inspection

```typescript
// Check accessibility tree
// Chrome DevTools → Elements → Accessibility pane

// Or programmatically with axe-core
import type { AxeResults } from 'axe-core';
const axe = await import('axe-core');
const results: AxeResults = await axe.default.run();
console.log(results.violations);
```

---

## Debug Workflow

### 1. Visual Issue

```
1. Screenshot (MCP: playwright_screenshot or manual)
2. DevTools Elements panel → Inspect shadow DOM
3. Check computed styles
4. Verify CSS custom properties inherited correctly
```

### 2. Slot Issue

```
1. Elements panel → Check slot assignments
2. Console: slot.assignedElements()
3. Verify slot="name" matches slot[name="name"]
4. Check for fallback content visibility
```

### 3. Event Issue

```
1. Console: addEventListener with composedPath() logging
2. Check if event has composed: true
3. Verify bubbles: true for custom events
4. Check stopPropagation() calls
```

### 4. Layout Issue

```
1. DevTools → Grid/Flexbox inspector
2. Check container-type on parent
3. Verify container query breakpoints
4. Check for overflow issues
```

---

## Checklist

- [ ] Set up Playwright MCP Server for automated debugging
- [ ] Use `playwright_evaluate` for shadow DOM inspection
- [ ] Fall back to browser DevTools when needed
- [ ] Check shadow DOM in Elements panel
- [ ] Use console to query shadow roots
- [ ] Test slot assignments with `assignedElements()`
- [ ] Verify events with `composedPath()`
- [ ] Run Lighthouse for performance/accessibility

---

_References:_
- [Playwright MCP Server](https://github.com/microsoft/playwright-mcp)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [Firefox DevTools](https://firefox-source-docs.mozilla.org/devtools-user/)
- Related skill: `playwright-testing`
````
