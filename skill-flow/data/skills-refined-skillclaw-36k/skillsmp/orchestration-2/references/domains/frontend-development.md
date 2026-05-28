# Frontend Development Domain

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Intelligent routing for UI/UX, design, and frontend.     │
│   Visual audits, accessibility, performance — all covered. │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **Load when**: UI/UX review, design audits, accessibility checks, performance optimization, responsive testing
> **Common patterns**: Screenshot-Analyze-Fix, Audit-Report-Remediate, Multi-Viewport-Compare

## Table of Contents

1. [Intent Detection](#intent-detection)
2. [Workflow Patterns](#workflow-patterns)
3. [Agent Selection](#agent-selection)
4. [Skill Stack](#skill-stack)
5. [Common Workflows](#common-workflows)

---

## Intent Detection

| User Request Pattern | Route To |
|---------------------|----------|
| "audit UI", "review design", "check visual" | playwright-automation -> frontend-aesthetic |
| "accessibility", "a11y", "screen reader", "WCAG" | playwright-automation -> accessibility-audit |
| "performance", "speed", "Core Web Vitals", "Lighthouse" | playwright-automation -> performance-audit |
| "responsive", "mobile", "breakpoints", "viewport" | playwright-automation (multi-viewport) -> frontend-aesthetic |
| "style", "CSS", "colors", "spacing", "typography" | frontend-aesthetic |
| "form", "input", "validation" | web-design-guidelines |
| "React", "Next.js", "component" | react-best-practices |
| "animation", "motion", "transition" | frontend-aesthetic |
| "dark mode", "theme", "design system" | frontend-aesthetic |

---

## Workflow Patterns

### Visual Audit

```
1. playwright_navigate to URL
2. playwright_screenshot full page
3. Analyze with frontend-aesthetic principles
4. Report issues with specific locations
```

### Accessibility Audit

```
1. playwright_navigate to URL
2. playwright_get_content (accessibility tree)
3. Run axe-core via playwright_evaluate
4. Cross-reference with web-design-guidelines
5. Prioritize by WCAG level (A, AA, AAA)
```

### Performance Audit

```
1. playwright_navigate with performance timing
2. Capture Core Web Vitals (LCP, FID, CLS)
3. playwright_screenshot above-fold content
4. Identify render-blocking resources
5. Recommend optimizations
```

### Responsive Testing

```
1. Define viewports: mobile (375), tablet (768), desktop (1280)
2. For each viewport:
   - playwright_screenshot
   - Check layout breaks
   - Verify touch targets (44x44 min on mobile)
3. Compare screenshots, report issues
```

---

## Agent Selection

| Task Type | Primary Agent | Tools |
|-----------|---------------|-------|
| Visual review | scout | Playwright MCP |
| Code changes | spark/kraken | Edit + Playwright validation |
| Full audit | kraken | Playwright + all skills |
| Quick fix | spark | Edit only |

---

## Skill Stack

Priority order for frontend tasks:

1. **playwright-automation** - Always first for browser context
2. **frontend-aesthetic** - Visual design validation
3. **web-design-guidelines** - Technical rules (a11y, forms)
4. **accessibility-audit** - Automated a11y scanning
5. **performance-audit** - Speed and Core Web Vitals
6. **react-best-practices** - React/Next.js specific

---

## Common Workflows

### "Make this page look better"

```
Phase 1: CAPTURE
└─ playwright_navigate + playwright_screenshot full page

Phase 2: ANALYZE
└─ Apply frontend-aesthetic principles:
   - Visual hierarchy (F-pattern, Z-pattern)
   - Spacing consistency (8px grid)
   - Color contrast ratios
   - Typography scale

Phase 3: FIX
└─ Specific CSS fixes with before/after comparison
```

### "Check if this is accessible"

```
Phase 1: AUTOMATED SCAN
├─ playwright_get_content (accessibility tree)
├─ Run axe-core via playwright_evaluate
└─ Collect violations

Phase 2: MANUAL CHECKS
├─ Keyboard navigation flow
├─ Focus indicator visibility
├─ ARIA label completeness
└─ Color-only information

Phase 3: REPORT
└─ WCAG compliance report prioritized by level (A, AA, AAA)
```

### "Why is this page slow?"

```
Phase 1: METRICS
├─ LCP (Largest Contentful Paint) < 2.5s
├─ FID (First Input Delay) < 100ms
├─ CLS (Cumulative Layout Shift) < 0.1
└─ TTFB (Time to First Byte) < 600ms

Phase 2: DIAGNOSE
├─ Identify render-blocking resources
├─ Check image optimization
├─ Analyze JavaScript bundle size
└─ Review third-party scripts

Phase 3: OPTIMIZE
└─ Prioritized recommendations with expected impact
```

### "Test on mobile"

```
Phase 1: VIEWPORT TESTING
├─ Mobile: 375x667 (iPhone SE)
├─ Tablet: 768x1024 (iPad)
├─ Desktop: 1280x800 (laptop)
└─ Wide: 1920x1080 (monitor)

Phase 2: INTERACTION CHECKS
├─ Touch targets >= 44x44px
├─ No horizontal scroll
├─ Text readable without zoom
└─ Forms usable on touch

Phase 3: COMPARE
└─ Side-by-side screenshot comparison
```

---

## Task Management Integration

For frontend tasks, create explicit tasks:

```python
# Visual audit decomposition
TaskCreate(subject="Capture screenshots", description="All viewports...")
TaskCreate(subject="Analyze design issues", description="Apply aesthetic principles...")
TaskCreate(subject="Check accessibility", description="axe-core + manual checks...")
TaskCreate(subject="Implement fixes", description="CSS/HTML changes...")
TaskCreate(subject="Validate fixes", description="Re-screenshot and compare...")

# Dependencies
TaskUpdate(taskId="2", addBlockedBy=["1"])  # Analyze after capture
TaskUpdate(taskId="4", addBlockedBy=["2", "3"])  # Fix after analysis
TaskUpdate(taskId="5", addBlockedBy=["4"])  # Validate after fix
```

---

```
─── Frontend Development ─────────────
```
