# Portal Testing Workflow

## Purpose

Test the Nikita web portal (Next.js on Vercel) using Chrome DevTools MCP.

---

## Prerequisites

- Chrome DevTools MCP server running
- Portal deployed to Vercel
- Test user with valid session

---

## Portal URLs

| Environment | URL |
|-------------|-----|
| Production | `https://nikita-portal.vercel.app` (example) |
| Preview | Check Vercel dashboard for preview URLs |

---

## Phase 1: Initial Load Test

### 1.1 Navigate to Portal

```
mcp__chrome-devtools__new_page

mcp__chrome-devtools__navigate_page
  url="https://nikita-portal.vercel.app"
```

### 1.2 Take Screenshot

```
mcp__chrome-devtools__take_screenshot
```

**Verify:**
- [ ] Page loaded without errors
- [ ] No blank screen
- [ ] Expected UI elements visible

### 1.3 Check Console Errors

```
mcp__chrome-devtools__list_console_messages
```

**Verify:**
- [ ] No JavaScript errors
- [ ] No failed network requests
- [ ] No hydration mismatches

---

## Phase 2: Authentication Flow

### 2.1 Check Login Form

```
mcp__chrome-devtools__evaluate_script
  script="document.querySelector('form[action*=login]')?.innerHTML || document.querySelector('input[type=email]')?.outerHTML"
```

**Expected:** Login form present with email input

### 2.2 Fill Login Form

```
mcp__chrome-devtools__fill
  selector="input[type='email']"
  value="test@example.com"

mcp__chrome-devtools__click
  selector="button[type='submit']"
```

### 2.3 Wait for OTP Email

```
# Wait 30 seconds for email delivery
# Then use Gmail MCP to retrieve OTP

mcp__gmail__search_emails
  query="from:noreply subject:Nikita code"
  max_results=1
```

### 2.4 Complete Login

```
# Extract OTP from email and enter

mcp__chrome-devtools__fill
  selector="input[name='otp']"
  value="<OTP_CODE>"

mcp__chrome-devtools__click
  selector="button[type='submit']"
```

---

## Phase 3: Dashboard Verification

### 3.1 Navigate to Dashboard

After successful login:

```
mcp__chrome-devtools__navigate_page
  url="https://nikita-portal.vercel.app/dashboard"

mcp__chrome-devtools__take_screenshot
```

### 3.2 Verify Dashboard Components

```
mcp__chrome-devtools__evaluate_script
  script=`
    ({
      scoreCard: !!document.querySelector('[data-testid="score-card"]'),
      chapterCard: !!document.querySelector('[data-testid="chapter-card"]'),
      metricsGrid: !!document.querySelector('[data-testid="metrics-grid"]'),
      engagementCard: !!document.querySelector('[data-testid="engagement-card"]'),
    })
  `
```

**Expected:** All components present (true)

### 3.3 Check API Connections

```
mcp__chrome-devtools__list_network_requests
```

**Verify:**
- [ ] API calls to backend successful (200 status)
- [ ] No CORS errors
- [ ] Data loading correctly

---

## Phase 4: Interactive Testing

### 4.1 Navigation

Test all navigation links:

```
mcp__chrome-devtools__click
  selector="a[href='/history']"

mcp__chrome-devtools__take_screenshot
```

**Verify:**
- [ ] History page loads
- [ ] Score history graph renders
- [ ] Conversation list populates

### 4.2 Settings Page

```
mcp__chrome-devtools__click
  selector="a[href='/settings']"

mcp__chrome-devtools__take_screenshot
```

**Verify:**
- [ ] Settings form loads
- [ ] User data pre-populated
- [ ] Save button functional

---

## Phase 5: Responsive Testing

### 5.1 Mobile Viewport

```
mcp__chrome-devtools__resize_page
  width=375
  height=812

mcp__chrome-devtools__take_screenshot
```

**Verify:**
- [ ] Mobile layout renders correctly
- [ ] No horizontal scroll
- [ ] Touch targets adequate size

### 5.2 Tablet Viewport

```
mcp__chrome-devtools__resize_page
  width=768
  height=1024

mcp__chrome-devtools__take_screenshot
```

### 5.3 Desktop Viewport

```
mcp__chrome-devtools__resize_page
  width=1920
  height=1080

mcp__chrome-devtools__take_screenshot
```

---

## Phase 6: Performance Check

### 6.1 Start Performance Trace

```
mcp__chrome-devtools__performance_start_trace
```

### 6.2 Navigate and Interact

```
mcp__chrome-devtools__navigate_page
  url="https://nikita-portal.vercel.app/dashboard"

# Wait for load
```

### 6.3 Stop and Analyze

```
mcp__chrome-devtools__performance_stop_trace

mcp__chrome-devtools__performance_analyze_insight
```

**Metrics to check:**
- First Contentful Paint < 1.5s
- Largest Contentful Paint < 2.5s
- Total Blocking Time < 200ms

---

## Phase 7: Cleanup

```
mcp__chrome-devtools__close_page
```

---

## Common Failures

| Symptom | Likely Cause | Recovery |
|---------|--------------|----------|
| Blank page | Build error | Check Vercel build logs |
| CORS error | API misconfiguration | Check CORS headers |
| 401 on API | Session expired | Re-authenticate |
| Console errors | JavaScript bug | Check error details |
| Slow load | Large bundle | Check performance trace |

---

## Report Template

```markdown
## Portal E2E Test Results

**URL**: [portal URL]
**Date**: [timestamp]

### Page Load
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| FCP | Xs | <1.5s | PASS/FAIL |
| LCP | Xs | <2.5s | PASS/FAIL |
| TBT | Xms | <200ms | PASS/FAIL |

### Components
| Component | Present | Functional |
|-----------|---------|------------|
| Score Card | ✅/❌ | ✅/❌ |
| Chapter Card | ✅/❌ | ✅/❌ |
| Metrics Grid | ✅/❌ | ✅/❌ |

### Issues Found
- [List any issues]

### Screenshots
- [Attach screenshots]
```

---

## Checklist

- [ ] Portal loads without errors
- [ ] Authentication flow works
- [ ] Dashboard components render
- [ ] API connections successful
- [ ] Navigation works
- [ ] Responsive layouts correct
- [ ] Performance metrics acceptable
