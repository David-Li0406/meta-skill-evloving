# Web Application Testing Examples

This directory contains practical examples of common testing scenarios using the webapp-testing skill.

## Available Examples

- [basic-page-test.md](./basic-page-test.md) - Simple homepage verification
- [form-interaction-test.md](./form-interaction-test.md) - Login form testing
- [responsive-design-test.md](./responsive-design-test.md) - Multi-viewport testing
- [error-investigation.md](./error-investigation.md) - Console error debugging

## Quick Reference

### Open and Test Page

```typescript
// 1. Open page
mcp_chrome - devtoo_new_page({ url: "http://localhost:3000" });

// 2. Snapshot
mcp_chrome - devtoo_take_snapshot();

// 3. Check errors
mcp_chrome - devtoo_list_console_messages({ types: ["error"] });
```

### Test Interaction

```typescript
// 1. Get snapshot for UIDs
mcp_chrome - devtoo_take_snapshot();

// 2. Click element
mcp_chrome - devtoo_click({ uid: "element_uid" });

// 3. Verify result
mcp_chrome - devtoo_take_snapshot();
```

### Responsive Testing

```typescript
const viewports = [
  { width: 375, height: 667, name: "mobile" },
  { width: 768, height: 1024, name: "tablet" },
  { width: 1920, height: 1080, name: "desktop" },
];

for (const vp of viewports) {
  mcp_chrome - devtoo_resize_page({ width: vp.width, height: vp.height });
  mcp_chrome -
    devtoo_take_screenshot({
      fullPage: true,
      filePath: `./${vp.name}-view.png`,
    });
}
```
