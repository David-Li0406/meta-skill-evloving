---
name: screenshot
description: "Capture screenshots of aiandi.dev for visual verification. Puppeteer-based, outputs to /tmp. Foundation for the design-loop skill."
---

# Screenshot Skill

**Purpose:** Capture screenshots of the blog for visual verification, documentation, or as part of the design-loop refinement process.

---

## When to Use

- **Standalone**: Quick visual verification before commit
- **With design-loop**: Iterative design refinement (see design-loop skill)
- **Documentation**: Capturing UI states for discussion
- **Debugging**: Layout or styling issues

---

## Quick Start

```bash
# 1. Ensure dev server is running
bun run dev --host 0.0.0.0 &
sleep 5

# 2. Capture screenshot
cat << 'EOF' | bun run -
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 800 });

// Note: Check server output for actual port (4321 or 4322)
await page.goto('http://localhost:4321/', { waitUntil: 'networkidle0' });

const path = `/tmp/aiandi-${Date.now()}.png`;
await page.screenshot({ path, fullPage: false });

await browser.close();
console.log(path);
EOF

# 3. IMMEDIATELY read the image with Read tool (don't wait for human)
# The Read tool can display images - call it right after capturing
# Read /tmp/aiandi-TIMESTAMP.png
```

---

## Configuration

### Viewport Sizes

| Device | Width | Height | Use Case |
|--------|-------|--------|----------|
| Monitor | 1920 | 1080 | Realistic desktop (recommended) |
| Desktop | 1280 | 800 | Smaller screens |
| Tablet | 768 | 1024 | Responsive testing |
| Mobile | 375 | 667 | Mobile-first verification |

**Important:** Use 1920x1080 to verify centering and layout on realistic monitors. Smaller viewports may hide centering issues.

### Screenshot Options

```javascript
// Full page (scrolls entire content)
await page.screenshot({ path, fullPage: true });

// Specific element
const element = await page.$('.hero');
await element.screenshot({ path });

// With transparency
await page.screenshot({ path, omitBackground: true });

// After hover state
await page.hover('.button');
await page.screenshot({ path });

// After waiting for animation
await page.waitForTimeout(300);
await page.screenshot({ path });
```

### Common Pages

| Page | Path |
|------|------|
| Home | `/` |
| Blog index | `/blog` |
| About | `/about` |
| Blog post | `/blog/[slug]` |

---

## Multiple Screenshots

```javascript
const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

const page = await browser.newPage();
const ts = Date.now();

const routes = [
  { path: '/', name: 'home' },
  { path: '/blog', name: 'blog' },
  { path: '/about', name: 'about' }
];

for (const { path, name } of routes) {
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto(`http://localhost:4321${path}`, { waitUntil: 'networkidle0' });
  await page.screenshot({ path: `/tmp/aiandi-${name}-${ts}.png` });
  console.log(`Captured: ${name}`);
}

await browser.close();
```

---

## Cleanup

Screenshots in `/tmp` auto-clean on system restart. For immediate cleanup:

```bash
rm /tmp/aiandi-*.png
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | Check server output for actual port (4321 or 4322) |
| Blank screenshot | Increase sleep time or use `waitUntil: 'networkidle0'` |
| Browser launch fails | Ensure `--no-sandbox` flag is included |
| Element not found | Use `await page.waitForSelector('.element')` |
| Stale content | Add `await page.reload()` before capture |

---

## Important Notes

- **Always use `/tmp`** - Never save screenshots in the repo
- **Never commit screenshots** - They're for verification only
- **Check the port** - Server may use 4321 or 4322
- **Kill server when done** - `pkill -f "astro dev"` if needed
- **Read immediately** - After capturing, call `Read /tmp/path.png` in the same response to avoid human gate
- **Use 1920x1080** - Realistic monitor size catches centering/layout issues

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| **design-loop** | Uses screenshot as part of iterative refinement |
| **web-design** | Provides the design system for what you're capturing |

---

*Visual verification catches what code review misses.*
