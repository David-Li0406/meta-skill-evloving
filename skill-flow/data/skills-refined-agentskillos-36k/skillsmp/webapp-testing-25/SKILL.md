---
name: webapp-testing
description: Comprehensive UI/UX testing using Chrome DevTools MCP for visual inspection, interaction validation, and debugging. Includes Next.js DevTools integration for framework-specific diagnostics. Use when user requests to test, verify, check, validate, inspect, or debug the UI/UX, interface, app, or web application. Handles screenshots, snapshots, console errors, network requests, and performance analysis.
---

# Web Application Testing Skill

Automates UI/UX testing and verification using Chrome DevTools MCP with optional Next.js DevTools support for comprehensive web application quality assurance.

## When to Use This Skill

Use this skill when the user requests:

✅ **Primary Use Cases**

- "Test the UI/UX"
- "Check the interface"
- "Verify the app is working"
- "Inspect the web application"
- "Validate the user interface"
- "Debug the frontend"
- "Test the visual layout"
- "Check if the page loads correctly"

✅ **Secondary Use Cases**

- "Take a screenshot of the app"
- "Check console errors"
- "Verify network requests"
- "Test responsive design"
- "Inspect element behavior"
- "Validate accessibility"
- "Check page performance"
- "Test user interactions"

✅ **Framework-Specific**

- "Check Next.js hydration errors"
- "Inspect React components"
- "Verify server components"
- "Debug Next.js routing"

❌ **Do NOT use when**

- User asks only for unit tests or E2E test code (use testing framework skills)
- Backend API testing is needed (use API testing skills)
- Database verification is required (use database skills)
- User wants to write test code manually

## Prerequisites

### 1. Development Server Running & Port Management

The web application must be running on localhost before testing. This includes checking if the port is occupied and freeing it if necessary:

**Check if port 3000 is in use**:

```bash
# Check port status
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000

# Output: 200/301 = server running, 000 = port free, other = occupied by another app
```

**If port is occupied by another process**:

```bash
# Kill the process using the port
pnpm dlx kill-port 3000

# This will output: "Port 3000 has been released"
# Then start the dev server
pnpm dev
```

**If port is free**:

```bash
# For Next.js projects
pnpm dev

# Wait for: ✓ Ready in XXXms
```

**Port status resolution**:

- ✅ Port 3000 is free → Start dev server
- ✅ Port 3000 has our app running → Continue testing
- ❌ Port 3000 occupied by other app → Kill it with `pnpm dlx kill-port 3000`, then restart our app

### 2. Chrome DevTools MCP Activation

The Chrome DevTools tools are activated automatically when needed. You'll have access to:

- `mcp_chrome-devtoo_new_page` - Open URL in browser
- `mcp_chrome-devtoo_navigate_page` - Navigate or reload
- `mcp_chrome-devtoo_take_snapshot` - Text snapshot of page
- `mcp_chrome-devtoo_take_screenshot` - Visual screenshot
- `mcp_chrome-devtoo_click` - Click elements
- `mcp_chrome-devtoo_fill` - Fill form inputs
- `mcp_chrome-devtoo_list_console_messages` - Get console logs
- `mcp_chrome-devtoo_list_network_requests` - Network activity
- `mcp_chrome-devtoo_evaluate_script` - Run JavaScript

### 3. Optional: Next.js DevTools

For Next.js-specific debugging, tools are activated if needed:

- Build analysis
- Route inspection
- Hydration error detection
- Server component validation

---

## Step-by-Step Instructions

### Step 1: Check and Manage Application Port

Before opening the browser, verify the port status and manage any conflicts:

```bash
# Check if port 3000 is responding
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)

if [ "$HTTP_CODE" = "000" ]; then
  # Port is free, start dev server
  echo "Port 3000 is free - starting dev server"
  pnpm dev
elif [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ]; then
  # Port already has our app running
  echo "Port 3000 already has app running - continuing with tests"
else
  # Port occupied by another app
  echo "Port 3000 occupied by another app - releasing it"
  pnpm dlx kill-port 3000
  sleep 2
  echo "Starting dev server"
  pnpm dev
fi

# Wait for server to be ready
echo "Waiting for server to be ready..."
for i in {1..30}; do
  if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✓ Server is ready"
    break
  fi
  echo "Waiting... ($i/30)"
  sleep 1
done
```

**Success indicators**:

- ✅ "Port 3000 is free - starting dev server"
- ✅ "Port 3000 already has app running - continuing with tests"
- ✅ "Port 3000 has been released" (from kill-port command)
- ✅ "Server is ready"

### Step 2: Activate Browser Tools

```typescript
// Tools are activated automatically when this skill is loaded
// Check available tools in the context
activate_browser_navigation_tools();
activate_snapshot_and_screenshot_tools();
activate_console_logging_tools();
```

### Step 3: Open or Navigate to Page

**For new testing session**:

```typescript
mcp_chrome -
  devtoo_new_page({
    url: "http://localhost:3000",
    timeout: 30000, // 30 seconds
  });
```

**For existing page**:

```typescript
mcp_chrome -
  devtoo_navigate_page({
    type: "url",
    url: "http://localhost:3000/page-to-test",
  });
```

**For reload**:

```typescript
mcp_chrome -
  devtoo_navigate_page({
    type: "reload",
    ignoreCache: true,
  });
```

### Step 4: Take Initial Snapshot

Capture text-based accessibility tree snapshot:

```typescript
mcp_chrome -
  devtoo_take_snapshot({
    verbose: false, // Set true for detailed a11y tree
  });
```

**What to check**:

- Page structure is correct
- All expected elements are present
- Text content is accurate
- Interactive elements are accessible
- No unexpected elements

### Step 5: Capture Visual Screenshot

```typescript
mcp_chrome -
  devtoo_take_screenshot({
    fullPage: true, // Capture entire page
    format: "png",
    quality: 90,
  });
```

**What to inspect**:

- Layout appears correct
- Colors and styling are proper
- Images load correctly
- No visual glitches
- Responsive design works

**⚠️ Avoiding Context Overflow (413 Error)**

Screenshots can generate large base64-encoded images that exceed Copilot's request size limits. To prevent **413 Request Entity Too Large** errors:

**Prevention Strategies**:

1. **Avoid full-page screenshots when possible**:
   ```typescript
   // Instead of fullPage: true, use element screenshots
   mcp_chrome-devtoo_take_screenshot({
     fullPage: false,  // Viewport only
     quality: 80,      // Reduce quality slightly
   });
   ```

2. **Use snapshots instead of screenshots for structure validation**:
   ```typescript
   // Prefer text-based snapshots (Step 4) for most checks
   mcp_chrome-devtoo_take_snapshot({ verbose: false });
   ```

3. **Describe findings in text when screenshots fail**:
   - If a screenshot causes 413 error, rely on console messages, network logs, and snapshots
   - Describe visual issues verbally instead of capturing them

4. **Reduce image quality for large pages**:
   ```typescript
   mcp_chrome-devtoo_take_screenshot({
     fullPage: true,
     quality: 60,  // Lower quality = smaller file
     format: "jpeg" // JPEG smaller than PNG for photos
   });
   ```

**When 413 occurs**:
- ✅ Use `take_snapshot` for structural validation
- ✅ Rely on console errors and network requests
- ✅ Describe UI issues in text
- ✅ Take viewport-only screenshots instead of full-page
- ❌ Don't retry the same full-page screenshot

### Step 6: Check Console for Errors

```typescript
mcp_chrome -
  devtoo_list_console_messages({
    types: ["error", "warn", "issue"],
    pageSize: 50,
  });
```

**Critical errors to watch**:

- React hydration errors
- Network failures
- JavaScript exceptions
- Resource loading errors
- CORS issues
- Deprecation warnings

### Step 6: Validate Network Requests

```typescript
mcp_chrome -
  devtoo_list_network_requests({
    resourceTypes: ["document", "xhr", "fetch"],
    pageSize: 30,
  });
```

**What to verify**:

- API calls succeed (200-299 status)
- No 404s for resources
- No failed CORS requests
- Reasonable load times
- Correct request/response data

### Step 7: Test User Interactions

**Click buttons/links**:

```typescript
mcp_chrome -
  devtoo_click({
    uid: "button_uid_from_snapshot",
    dblClick: false,
  });
```

**Fill forms**:

```typescript
mcp_chrome -
  devtoo_fill({
    uid: "input_uid_from_snapshot",
    value: "test value",
  });
```

**Fill multiple fields**:

```typescript
mcp_chrome -
  devtoo_fill_form({
    elements: [
      { uid: "email_uid", value: "test@example.com" },
      { uid: "password_uid", value: "testpass123" },
    ],
  });
```

### Step 8: Execute Custom JavaScript

For advanced validation:

```typescript
mcp_chrome -
  devtoo_evaluate_script({
    function: `() => {
    return {
      bodyClasses: document.body.className,
      metaTags: Array.from(document.querySelectorAll('meta')).length,
      hasErrors: window.__NEXT_DATA__?.err !== null
    }
  }`,
    args: [],
  });
```

### Step 9: Test Responsive Design

```typescript
// Mobile view
mcp_chrome -
  devtoo_resize_page({
    width: 375,
    height: 667,
  });

// Take snapshot
mcp_chrome - devtoo_take_snapshot();

// Desktop view
mcp_chrome -
  devtoo_resize_page({
    width: 1920,
    height: 1080,
  });
```

### Step 10: Report Findings

Summarize test results:

**Format**:

```markdown
## Testing Results for [Page Name]

### ✅ Passed Checks

- Page loads successfully
- All elements render correctly
- No console errors
- Network requests succeed

### ⚠️ Warnings

- Missing image alt texts (accessibility concern)
- Slow API response time (performance)

### ❌ Issues Found

- Button does not respond to click
- Form validation error not displayed
- Console error: [specific error message]

### 📸 Evidence

[Screenshot or snapshot showing the issue]

### 🔧 Recommendations

1. Fix [specific issue]
2. Improve [specific area]
3. Test [specific scenario]
```

---

## Advanced Usage

### Performance Testing with Core Web Vitals

Comprehensive performance analysis targeting Google's Core Web Vitals metrics.

```typescript
// Start performance trace
mcp_chrome -
  devtoo_performance_start_trace({
    reload: true,
    autoStop: true,
  });

// After page loads, analyze insights
mcp_chrome -
  devtoo_performance_analyze_insight({
    insightSetId: "id_from_trace",
    insightName: "LCPBreakdown",
  });
```

#### Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

#### Detailed Performance Analysis

```typescript
// Get comprehensive performance metrics
mcp_chrome -
  devtoo_evaluate_script({
    function: `() => {
    const nav = performance.getEntriesByType('navigation')[0];
    const paint = performance.getEntriesByType('paint');
    const lcp = performance.getEntriesByType('largest-contentful-paint');
    const cls = performance.getEntriesByType('layout-shift');
    
    // Calculate CLS
    let clsScore = 0;
    cls.forEach(entry => {
      if (!entry.hadRecentInput) {
        clsScore += entry.value;
      }
    });
    
    return {
      // Navigation Timing
      timing: {
        dns: nav.domainLookupEnd - nav.domainLookupStart,
        tcp: nav.connectEnd - nav.connectStart,
        ssl: nav.secureConnectionStart ? nav.connectEnd - nav.secureConnectionStart : 0,
        ttfb: nav.responseStart - nav.requestStart,
        download: nav.responseEnd - nav.responseStart,
        domParse: nav.domInteractive - nav.responseEnd,
        domReady: nav.domContentLoadedEventEnd - nav.domContentLoadedEventStart,
        load: nav.loadEventEnd - nav.loadEventStart,
        total: nav.loadEventEnd - nav.fetchStart,
      },
      
      // Core Web Vitals
      vitals: {
        fcp: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 'N/A',
        lcp: lcp.length ? lcp[lcp.length - 1].startTime : 'N/A',
        cls: clsScore.toFixed(4),
        lcpElement: lcp.length ? lcp[lcp.length - 1].element?.tagName : 'N/A',
      },
      
      // Resources
      resources: {
        total: performance.getEntriesByType('resource').length,
        scripts: performance.getEntriesByType('resource').filter(r => r.initiatorType === 'script').length,
        styles: performance.getEntriesByType('resource').filter(r => r.initiatorType === 'link' || r.initiatorType === 'css').length,
        images: performance.getEntriesByType('resource').filter(r => r.initiatorType === 'img').length,
        fonts: performance.getEntriesByType('resource').filter(r => r.initiatorType === 'css' && r.name.includes('font')).length,
      },
      
      // Memory (if available)
      memory: performance.memory ? {
        usedJSHeap: (performance.memory.usedJSHeapSize / 1048576).toFixed(2) + ' MB',
        totalJSHeap: (performance.memory.totalJSHeapSize / 1048576).toFixed(2) + ' MB',
      } : 'N/A'
    };
  }`,
  });
```

#### LCP Analysis

```typescript
// Identify LCP element and optimization opportunities
mcp_chrome -
  devtoo_performance_analyze_insight({
    insightSetId: "current_trace",
    insightName: "LCPBreakdown",
  });
```

**LCP Optimization Checklist**:
- [ ] Preload critical images (`<link rel="preload">`)
- [ ] Use responsive images (`srcset`, `sizes`)
- [ ] Optimize image formats (WebP, AVIF)
- [ ] Eliminate render-blocking resources
- [ ] Use `fetchpriority="high"` on LCP image

#### CLS Debugging

```typescript
// Monitor layout shifts in real-time
mcp_chrome -
  devtoo_evaluate_script({
    function: `() => {
    const shifts = [];
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          shifts.push({
            value: entry.value,
            time: entry.startTime,
            sources: entry.sources?.map(s => ({
              element: s.node?.tagName,
              previousRect: s.previousRect,
              currentRect: s.currentRect,
            }))
          });
        }
      }
    });
    observer.observe({ type: 'layout-shift', buffered: true });
    
    return {
      existingShifts: performance.getEntriesByType('layout-shift')
        .filter(e => !e.hadRecentInput)
        .map(e => ({ value: e.value, time: e.startTime })),
      message: 'Observer active - interact with page to detect more shifts'
    };
  }`,
  });
```

**CLS Optimization Checklist**:
- [ ] Set explicit dimensions on images/videos
- [ ] Reserve space for dynamic content
- [ ] Use `transform` instead of changing layout properties
- [ ] Avoid inserting content above existing content
- [ ] Use `content-visibility: auto` for off-screen content

---

### Mobile Device Emulation

Test responsive design across various device profiles.

#### Preset Device Profiles

```typescript
// iPhone SE
mcp_chrome -
  devtoo_resize_page({ width: 375, height: 667 });

// iPhone 12/13/14 Pro
mcp_chrome -
  devtoo_resize_page({ width: 390, height: 844 });

// iPhone 14 Pro Max
mcp_chrome -
  devtoo_resize_page({ width: 430, height: 932 });

// Samsung Galaxy S21
mcp_chrome -
  devtoo_resize_page({ width: 360, height: 800 });

// iPad Mini
mcp_chrome -
  devtoo_resize_page({ width: 768, height: 1024 });

// iPad Pro 12.9"
mcp_chrome -
  devtoo_resize_page({ width: 1024, height: 1366 });

// Desktop HD
mcp_chrome -
  devtoo_resize_page({ width: 1920, height: 1080 });

// Desktop 4K
mcp_chrome -
  devtoo_resize_page({ width: 3840, height: 2160 });
```

#### Complete Responsive Testing Suite

```typescript
// Test all major breakpoints
const viewports = [
  { name: 'iPhone SE', width: 375, height: 667, type: 'mobile' },
  { name: 'iPhone 14 Pro', width: 390, height: 844, type: 'mobile' },
  { name: 'Android', width: 360, height: 800, type: 'mobile' },
  { name: 'iPad Mini', width: 768, height: 1024, type: 'tablet' },
  { name: 'iPad Pro', width: 1024, height: 1366, type: 'tablet' },
  { name: 'Laptop', width: 1366, height: 768, type: 'desktop' },
  { name: 'Desktop HD', width: 1920, height: 1080, type: 'desktop' },
];

for (const viewport of viewports) {
  // 1. Resize to viewport
  mcp_chrome - devtoo_resize_page({ width: viewport.width, height: viewport.height });
  
  // 2. Wait for resize and reflow
  await new Promise(r => setTimeout(r, 500));
  
  // 3. Take snapshot for structure
  mcp_chrome - devtoo_take_snapshot();
  
  // 4. Take screenshot for visual
  mcp_chrome - devtoo_take_screenshot({ 
    fullPage: true, 
    filePath: `./${viewport.name.replace(/\s/g, '-').toLowerCase()}.png` 
  });
  
  // 5. Check for horizontal overflow
  mcp_chrome - devtoo_evaluate_script({
    function: `() => ({
      hasHorizontalScroll: document.body.scrollWidth > window.innerWidth,
      bodyWidth: document.body.scrollWidth,
      viewportWidth: window.innerWidth,
      overflowElements: Array.from(document.querySelectorAll('*')).filter(el => 
        el.scrollWidth > el.clientWidth
      ).map(el => el.tagName + '.' + el.className).slice(0, 5)
    })`
  });
}
```

#### Touch-Specific Testing

```typescript
// Verify touch targets are at least 44x44px (Apple HIG) / 48x48px (Material)
mcp_chrome -
  devtoo_evaluate_script({
    function: `() => {
    const touchTargets = document.querySelectorAll('button, a, input, select, textarea, [role="button"], [onclick]');
    const smallTargets = [];
    
    touchTargets.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.width < 44 || rect.height < 44) {
        smallTargets.push({
          element: el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''),
          width: rect.width.toFixed(0),
          height: rect.height.toFixed(0),
          issue: rect.width < 44 ? 'too narrow' : 'too short'
        });
      }
    });
    
    return {
      totalTouchTargets: touchTargets.length,
      smallTargets: smallTargets.slice(0, 10),
      passRate: ((1 - smallTargets.length / touchTargets.length) * 100).toFixed(1) + '%'
    };
  }`,
  });
```

### Accessibility Audit (WCAG AAA Compliance)

This section covers comprehensive accessibility testing targeting **WCAG 2.2 AAA** standards.

```typescript
// Take verbose snapshot for full a11y tree
mcp_chrome -
  devtoo_take_snapshot({
    verbose: true,
  });
```

#### WCAG 2.2 AAA Checklist

**Perceivable (Level AAA)**:
| Criterion | Check | How to Verify |
|-----------|-------|---------------|
| 1.4.6 Contrast Enhanced | 7:1 for normal text, 4.5:1 for large text | Use browser DevTools color picker |
| 1.4.7 Low Background Audio | Audio can be paused/stopped | Manual audio controls check |
| 1.4.8 Visual Presentation | Line spacing ≥1.5, paragraph spacing ≥2x | Inspect CSS line-height |
| 1.4.9 Images of Text (No Exception) | No images of text | Snapshot analysis |

**Operable (Level AAA)**:
| Criterion | Check | How to Verify |
|-----------|-------|---------------|
| 2.1.3 Keyboard (No Exception) | All functions keyboard accessible | Tab through entire page |
| 2.2.3 No Timing | No time limits | Review any timers in code |
| 2.2.6 Timeouts | Warn users of data loss | Check for session timeout handling |
| 2.3.2 Three Flashes | No content flashes more than 3x/sec | Visual inspection of animations |
| 2.4.8 Location | Breadcrumbs or site map provided | Check navigation elements |
| 2.4.9 Link Purpose (Link Only) | Links make sense out of context | Review link text |
| 2.4.10 Section Headings | Content organized with headings | Check heading hierarchy |

**Understandable (Level AAA)**:
| Criterion | Check | How to Verify |
|-----------|-------|---------------|
| 3.1.3 Unusual Words | Glossary for jargon | Check for definitions |
| 3.1.4 Abbreviations | Expanded forms available | Hover/focus on abbreviations |
| 3.2.5 Change on Request | No automatic context changes | Verify no auto-redirects |
| 3.3.5 Help | Context-sensitive help available | Check help buttons/tooltips |
| 3.3.6 Error Prevention (All) | Review before submit | Check form confirmation |

**Robust (Level AAA)**:
| Criterion | Check | How to Verify |
|-----------|-------|---------------|
| 4.1.3 Status Messages | Screen reader announces changes | Test with narrator/NVDA |

#### Accessibility Testing Script

```typescript
// Comprehensive a11y evaluation
mcp_chrome -
  devtoo_evaluate_script({
    function: `() => {
    const issues = [];
    
    // Check for missing alt text
    document.querySelectorAll('img:not([alt])').forEach(img => {
      issues.push({ type: 'error', rule: '1.1.1', message: 'Image missing alt text', element: img.outerHTML.slice(0, 100) });
    });
    
    // Check heading hierarchy
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
    let lastLevel = 0;
    headings.forEach(h => {
      const level = parseInt(h.tagName[1]);
      if (level > lastLevel + 1) {
        issues.push({ type: 'warning', rule: '2.4.10', message: 'Skipped heading level', element: h.outerHTML.slice(0, 100) });
      }
      lastLevel = level;
    });
    
    // Check for keyboard focusable elements without visible focus
    const focusable = document.querySelectorAll('a, button, input, select, textarea, [tabindex]');
    
    // Check form labels
    document.querySelectorAll('input:not([type="hidden"]):not([type="submit"]):not([type="button"])').forEach(input => {
      if (!input.labels?.length && !input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')) {
        issues.push({ type: 'error', rule: '1.3.1', message: 'Form input missing label', element: input.outerHTML.slice(0, 100) });
      }
    });
    
    // Check for empty buttons/links
    document.querySelectorAll('a, button').forEach(el => {
      if (!el.textContent?.trim() && !el.getAttribute('aria-label') && !el.querySelector('img[alt]')) {
        issues.push({ type: 'error', rule: '2.4.4', message: 'Empty link/button', element: el.outerHTML.slice(0, 100) });
      }
    });
    
    // Check language attribute
    if (!document.documentElement.lang) {
      issues.push({ type: 'error', rule: '3.1.1', message: 'Missing lang attribute on html' });
    }
    
    return {
      totalIssues: issues.length,
      errors: issues.filter(i => i.type === 'error'),
      warnings: issues.filter(i => i.type === 'warning'),
      wcagLevel: issues.filter(i => i.type === 'error').length === 0 ? 'Potentially AAA' : 'Needs fixes'
    };
  }`,
  });
```

#### Color Contrast Verification

```typescript
// Check contrast ratios for text elements
mcp_chrome -
  devtoo_evaluate_script({
    function: `() => {
    function getLuminance(r, g, b) {
      const [rs, gs, bs] = [r, g, b].map(c => {
        c = c / 255;
        return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
    }
    
    function getContrastRatio(l1, l2) {
      const lighter = Math.max(l1, l2);
      const darker = Math.min(l1, l2);
      return (lighter + 0.05) / (darker + 0.05);
    }
    
    const textElements = document.querySelectorAll('p, span, a, h1, h2, h3, h4, h5, h6, li, td, th, label');
    const lowContrast = [];
    
    textElements.forEach(el => {
      const style = window.getComputedStyle(el);
      const color = style.color;
      const bgColor = style.backgroundColor;
      // Simplified check - real implementation would need to trace up for transparent bgs
      if (bgColor !== 'rgba(0, 0, 0, 0)') {
        // Would calculate contrast here
      }
    });
    
    return { message: 'Use DevTools Lighthouse for detailed contrast audit' };
  }`,
  });
```

### Next.js Specific Testing

When testing Next.js apps, also check:

1. **Hydration Errors**: Look for "Hydration failed" in console
2. **Server vs Client**: Verify server components render correctly
3. **Route Navigation**: Test Link components and route transitions
4. **Metadata**: Verify SEO meta tags are generated

```typescript
// Check Next.js specific errors
mcp_chrome -
  devtoo_evaluate_script({
    function: `() => {
    return {
      nextData: window.__NEXT_DATA__,
      buildId: window.__NEXT_DATA__?.buildId,
      pageProps: window.__NEXT_DATA__?.props?.pageProps
    }
  }`,
  });
```

### Multi-Page Testing Flow

```typescript
// Test multiple pages in sequence
const pages = ["/", "/about", "/contact"];

for (const page of pages) {
  // Navigate
  (await mcp_chrome) -
    devtoo_navigate_page({ type: "url", url: `http://localhost:3000${page}` });

  // Test
  (await mcp_chrome) - devtoo_take_snapshot();
  (await mcp_chrome) - devtoo_list_console_messages({ types: ["error"] });

  // Report
  console.log(`✅ Page ${page} tested`);
}
```

---

## Examples

### Example 1: Basic Page Verification

**User request**: "Test the homepage UI"

**Actions**:

```typescript
// 1. Open page
mcp_chrome - devtoo_new_page({ url: "http://localhost:3000" });

// 2. Take snapshot
mcp_chrome - devtoo_take_snapshot();

// 3. Check console
mcp_chrome - devtoo_list_console_messages({ types: ["error", "warn"] });

// 4. Take screenshot
mcp_chrome - devtoo_take_screenshot({ fullPage: true });
```

**Expected result**:

- Page structure matches requirements
- No console errors
- Visual screenshot confirms design
- All interactive elements present

### Example 2: Form Interaction Test

**User request**: "Verify the login form works"

**Actions**:

```typescript
// 1. Navigate to login
mcp_chrome -
  devtoo_navigate_page({
    type: "url",
    url: "http://localhost:3000/login",
  });

// 2. Get page snapshot to find UIDs
mcp_chrome - devtoo_take_snapshot();

// 3. Fill form
mcp_chrome -
  devtoo_fill_form({
    elements: [
      { uid: "email_input_uid", value: "test@example.com" },
      { uid: "password_input_uid", value: "password123" },
    ],
  });

// 4. Click submit
mcp_chrome - devtoo_click({ uid: "submit_button_uid" });

// 5. Wait and verify redirect
mcp_chrome - devtoo_wait_for({ text: "Dashboard", timeout: 5000 });

// 6. Check for errors
mcp_chrome - devtoo_list_console_messages({ types: ["error"] });
```

**Expected result**: Form submits, user redirects to dashboard, no errors.

### Example 3: Console Error Investigation

**User request**: "Check if there are any errors in the app"

**Actions**:

```typescript
// 1. List all console messages
const messages =
  (await mcp_chrome) -
  devtoo_list_console_messages({
    types: ["error", "warn", "issue"],
    includePreservedMessages: true,
  });

// 2. Get detailed error info
for (const msg of messages) {
  (await mcp_chrome) - devtoo_get_console_message({ msgid: msg.id });
}

// 3. Analyze and categorize
// - Critical: JavaScript errors, network failures
// - Warning: Deprecations, performance issues
// - Info: Development warnings, suggestions
```

**Expected result**: Comprehensive error report with severity levels and fix suggestions.

### Example 4: Responsive Design Check

**User request**: "Test the UI on mobile and desktop"

**Actions**:

```typescript
// Mobile test
mcp_chrome - devtoo_resize_page({ width: 375, height: 667 });
mcp_chrome -
  devtoo_take_screenshot({ fullPage: true, filePath: "./mobile-view.png" });
mcp_chrome - devtoo_take_snapshot();

// Tablet test
mcp_chrome - devtoo_resize_page({ width: 768, height: 1024 });
mcp_chrome -
  devtoo_take_screenshot({ fullPage: true, filePath: "./tablet-view.png" });

// Desktop test
mcp_chrome - devtoo_resize_page({ width: 1920, height: 1080 });
mcp_chrome -
  devtoo_take_screenshot({ fullPage: true, filePath: "./desktop-view.png" });

// Compare layouts and report differences
```

**Expected result**: Layout adapts correctly to all viewport sizes, no broken elements.

---

## Error Handling

### Common Errors

| Error                                | Cause                       | Solution                                                             |
| ------------------------------------ | --------------------------- | -------------------------------------------------------------------- |
| "Connection refused"                 | Dev server not running      | Use Step 1 to check/start server                                     |
| "Port 3000 already in use"           | Another process using port  | Run `pnpm dlx kill-port 3000` then `pnpm dev`                        |
| "Cannot kill port"                   | Permission issues           | Identify process: `lsof -i :3000` or `netstat -ano \| findstr :3000` |
| "Page load timeout"                  | Slow server response        | Increase timeout or optimize app                                     |
| "Element not found (stale snapshot)" | Page changed after snapshot | Take fresh snapshot before interaction                               |
| "CORS blocked"                       | Cross-origin request issue  | Check CORS headers or proxy config                                   |
| "Hydration error"                    | Server/client HTML mismatch | Fix React hydration issues in code                                   |

### Debugging Tips

```typescript
// Enable verbose logging
mcp_chrome - devtoo_take_snapshot({ verbose: true });

// Check network issues
mcp_chrome -
  devtoo_list_network_requests({
    resourceTypes: ["all"],
    includePreservedRequests: true,
  });

// Inspect specific request
mcp_chrome - devtoo_get_network_request({ reqid: request_id });

// Evaluate diagnostic script
mcp_chrome -
  devtoo_evaluate_script({
    function: `() => {
    return {
      errors: window.__errors || [],
      warnings: window.__warnings || [],
      performance: performance.getEntriesByType('navigation')[0]
    }
  }`,
  });
```

---

## Best Practices

1. **Verify port before testing**: Always run Step 1 to ensure server is ready and port conflicts are resolved
2. **Use pnpm dlx kill-port when needed**: Safely release occupied ports instead of manually hunting processes
3. **Always take snapshot before interactions**: UIDs become stale after page changes
4. **Check console after every navigation**: Catch errors immediately
5. **Use appropriate viewport sizes**: Test responsive breakpoints
6. **Wait for dynamic content**: Use `wait_for` for async-loaded elements
7. **Save screenshots for evidence**: Document visual issues
8. **Test critical user flows**: Focus on most important interactions
9. **Clear cache when needed**: Use `ignoreCache: true` for fresh loads
10. **Test both success and error states**: Validate error handling
11. **Avoid context overflow**: Use `take_snapshot` over `take_screenshot` when possible; reduce screenshot quality if needed to prevent 413 errors

---

## Related Skills

- [github-pull-request](./../github-pull-request/SKILL.md) - Create PR after fixing UI issues
- Database skills - Verify data integrity affects UI
- API testing skills - Test backend integration with UI

---

## Resources

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Next.js Debugging](https://nextjs.org/docs/app/building-your-application/debugging)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
- [Core Web Vitals](https://web.dev/vitals/)

---

## Notes

- **Performance**: Full page screenshots can be slow for large pages and may exceed context limits (413 error)
- **Screenshots vs Snapshots**: Prefer snapshots (text) for faster testing and to avoid context overflow; use screenshots only for visual validation
- **413 Error Prevention**: Reduce screenshot quality (60-80), use viewport-only captures, or rely on snapshots and console logs instead
- **Browser State**: Each test should be independent; consider reloading between tests
- **Authentication**: Handle login flows at the start of testing sessions
- **Dynamic Content**: Wait for loading states to complete before assertions
- **Network Emulation**: Use `emulate` tool to test slow connections or offline scenarios

---

## Testing Checklist

Use this checklist for comprehensive testing:

### Visual Testing

- [ ] Page loads without visual glitches
- [ ] Layout is correct on mobile (375px)
- [ ] Layout is correct on tablet (768px)
- [ ] Layout is correct on desktop (1920px)
- [ ] All images load correctly
- [ ] Typography is readable
- [ ] Colors match design system

### Functional Testing

- [ ] All links navigate correctly
- [ ] Buttons respond to clicks
- [ ] Forms accept input
- [ ] Form validation works
- [ ] Error states display properly
- [ ] Loading states appear

### Technical Testing

- [ ] No console errors
- [ ] No console warnings (or documented)
- [ ] Network requests succeed
- [ ] No 404s or failed requests
- [ ] Page loads in < 3 seconds
- [ ] No hydration errors (Next.js)

### Accessibility Testing

- [ ] Semantic HTML structure
- [ ] ARIA labels where needed
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] Alt text on images
- [ ] Color contrast adequate

### Performance Testing

- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] No layout shifts
- [ ] Optimized images
- [ ] Minimal render blocking
