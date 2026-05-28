---
name: fullstory-test-automation
version: v3
description: >
  AI assistant guide for generating test automation scripts from Fullstory-decorated codebases.
  This is the CORE skill that teaches discovery, analysis, and platform routing. For framework-
  specific patterns, see SKILL-WEB.md (Cypress, Playwright, Selenium) or SKILL-MOBILE.md
  (Detox, Espresso, XCUITest, Flutter, Appium, Maestro).
platforms: [web, ios, android, flutter, react-native]
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
related_skills:
  # Framework
  - fullstory-stable-selectors
  # Core
  - fullstory-element-properties
  - fullstory-page-properties
  - fullstory-user-properties
  - fullstory-identify-users
  - fullstory-analytics-events
  - fullstory-privacy-controls
  - fullstory-capture-control
  # Meta
  - mobile-instrumentation-orchestrator
  - universal-data-scoping-and-decoration
  # Industry
  - fullstory-ecommerce
---

# Fullstory Test Automation Framework Skill

## Overview

**This skill is designed for AI coding assistants** (Claude, GPT, Copilot, Cursor, etc.) to generate test automation scripts from codebases decorated with Fullstory patterns.

When a codebase is decorated following Fullstory's semantic decoration patterns (stable selectors, element properties, page properties), it becomes inherently **automation-ready**. This skill teaches AI assistants how to:

1. **Discover** what Fullstory decoration exists in a codebase
2. **Work with partial decoration** (not all codebases use all skills)
3. **Route to platform-specific skills** based on detected technology
4. **Leverage industry skills** (e-commerce, SaaS, etc.) for domain-specific testing

### Platform-Specific Files (Same Directory)

After using this core skill for discovery and analysis, read the appropriate platform file **in this same skill directory**:

| Platform | File | Frameworks Covered |
|----------|------|-------------------|
| **Web** | `./SKILL-WEB.md` | Cypress, Playwright, Selenium, WebdriverIO |
| **Mobile** | `./SKILL-MOBILE.md` | Detox, Espresso, XCUITest, Flutter, Appium, Maestro |

> **AI Note:** These files are in the same directory as this skill (`fullstory-test-automation/`). Read the appropriate one based on detected platform.

### The Problem This Solves

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRADITIONAL TEST AUTOMATION CHALLENGES                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ Brittle Selectors                                                       │
│     • Tests break on every CSS/build change                                 │
│     • Selectors like ".Button_primary__x7k2s" change per deploy             │
│     • Position-based selectors break on UI reorder                          │
│                                                                             │
│  ❌ No Semantic Understanding                                               │
│     • Test doesn't know "what" element does                                 │
│     • Can't verify correct element targeted                                 │
│     • Debugging requires UI inspection                                      │
│                                                                             │
│  ❌ Mobile Accessibility ID Chaos                                           │
│     • Inconsistent contentDescription/accessibilityIdentifier               │
│     • testID missing on critical elements                                   │
│     • No standard naming convention                                         │
│                                                                             │
│  ❌ Privacy-Masked Fields                                                   │
│     • Can't debug what test automation entered                              │
│     • Masked fields show as "████████" in session replay                   │
│     • No visibility into automation test data                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### The Solution: Semantic Decoration → Test Automation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  FULLSTORY-DECORATED CODEBASE = AUTOMATION-READY                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ✅ Stable Selectors (from fullstory-stable-selectors skill)                │
│     • data-component="ProductCard" → [data-component="ProductCard"]         │
│     • data-element="add-to-cart" → [data-element="add-to-cart"]            │
│     • data-action="submit-order" → [data-action="submit-order"]            │
│     • Survives all CSS/build changes                                        │
│                                                                             │
│  ✅ Semantic Element Names (from fullstory-element-properties skill)        │
│     • data-fs-element="Product Card" → Human-readable in tests              │
│     • Property schemas → Know element types (price=real, qty=int)           │
│                                                                             │
│  ✅ Navigation Context (from fullstory-page-properties skill)               │
│     • pageName: "Checkout" → Know which page/view we're on                  │
│     • Can assert navigation, generate Page Objects                          │
│                                                                             │
│  ✅ Test Data Capture (from fullstory-analytics-events skill)               │
│     • trackEvent for test input capture                                     │
│     • Debug automation even with privacy masking                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## AI ASSISTANT WORKFLOW

Follow this workflow when generating test automation:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  AI ASSISTANT TEST GENERATION WORKFLOW                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. DISCOVER (this skill)                                                   │
│     └── Scan codebase for existing Fullstory decoration                    │
│     └── Identify which skills are implemented                              │
│     └── Detect platform: Web vs Mobile vs Both                             │
│                                                                             │
│  2. ANALYZE (this skill)                                                    │
│     └── Determine decoration maturity level (0-4)                          │
│     └── Identify gaps vs fully decorated elements                          │
│     └── Note privacy controls on sensitive fields                          │
│                                                                             │
│  3. ROUTE (to platform file in this directory)                              │
│     └── Web detected → Read ./SKILL-WEB.md                                 │
│     └── Mobile detected → Read ./SKILL-MOBILE.md                           │
│     └── Both → Read both as needed                                         │
│                                                                             │
│  4. GENERATE (platform skill)                                               │
│     └── Use best available selectors (fallback gracefully)                 │
│     └── Apply framework-specific patterns                                  │
│     └── Add test data tracking for masked fields                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Principle: Work With What Exists

Not every codebase will have all Fullstory skills implemented. The AI assistant should:

1. **Never assume** all decoration is present
2. **Discover first** what attributes exist in the codebase
3. **Gracefully degrade** to less specific selectors when needed
4. **Recommend improvements** where decoration gaps exist

---

## CODEBASE DISCOVERY

Before generating any test automation, discover what Fullstory decoration exists.

### Platform Detection

```bash
# Detect Web (React, Vue, Angular, etc.)
ls -la src/**/*.tsx src/**/*.jsx src/**/*.vue 2>/dev/null
grep -r "data-element=" --include="*.tsx" --include="*.jsx" --include="*.html"

# Detect React Native
grep -r "testID=" --include="*.tsx" --include="*.jsx"
ls -la ios/ android/ 2>/dev/null

# Detect Native Android
ls -la app/src/main/java/ app/src/main/kotlin/ 2>/dev/null
grep -r "contentDescription=" --include="*.xml"

# Detect Native iOS  
ls -la *.xcodeproj/ *.xcworkspace/ 2>/dev/null
grep -r "accessibilityIdentifier" --include="*.swift"

# Detect Flutter
ls -la lib/ pubspec.yaml 2>/dev/null
grep -r "Key\(" --include="*.dart"
```

### Decoration Discovery Queries

```bash
# Discover stable selectors (fullstory-stable-selectors)
grep -r "data-component=" --include="*.tsx" --include="*.jsx" --include="*.html"
grep -r "data-element=" --include="*.tsx" --include="*.jsx" --include="*.html"
grep -r "data-action=" --include="*.tsx" --include="*.jsx" --include="*.html"
grep -r "data-state=" --include="*.tsx" --include="*.jsx" --include="*.html"

# Discover element properties (fullstory-element-properties)
grep -r "data-fs-element=" --include="*.tsx" --include="*.jsx"
grep -r "data-fs-properties-schema=" --include="*.tsx" --include="*.jsx"
grep -r "data-product-id=" --include="*.tsx" --include="*.jsx"

# Discover page properties (fullstory-page-properties)
grep -r "pageName" --include="*.ts" --include="*.tsx" --include="*.js"

# Discover privacy controls (fullstory-privacy-controls)
grep -r "fs-exclude\|fs-mask\|fs-unmask" --include="*.tsx" --include="*.scss"

# Discover analytics events (fullstory-analytics-events)
grep -r "trackEvent\|FS\('trackEvent" --include="*.ts" --include="*.tsx"

# Discover user identification (fullstory-identify-users)
grep -r "setIdentity\|FS\('setIdentity" --include="*.ts" --include="*.tsx"
```

### Decoration Maturity Levels

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DECORATION MATURITY LEVELS                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Level 0: NONE                                                              │
│  └── No Fullstory decoration found                                         │
│  └── Must use CSS classes, IDs, text content (brittle)                     │
│  └── RECOMMEND: Implement fullstory-stable-selectors first                 │
│                                                                             │
│  Level 1: BASIC (stable selectors only)                                    │
│  └── data-element, data-component present                                  │
│  └── Can target elements reliably                                          │
│  └── Limited semantic context                                              │
│                                                                             │
│  Level 2: INTERMEDIATE (+ element/page properties)                         │
│  └── data-fs-element, property schemas present                             │
│  └── pageName set for navigation                                           │
│  └── Rich assertions possible                                              │
│                                                                             │
│  Level 3: ADVANCED (+ privacy + events)                                    │
│  └── Privacy classes applied (fs-exclude, fs-mask)                         │
│  └── trackEvent calls for business events                                  │
│  └── Can verify event tracking in tests                                    │
│                                                                             │
│  Level 4: COMPLETE (all skills)                                            │
│  └── User identification and properties                                    │
│  └── Capture control (shutdown/restart)                                    │
│  └── Full test automation capability                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Decoration Inventory

For each component you want to test, build an inventory:

```typescript
interface ComponentDecorationInventory {
  componentName: string;
  filePath: string;
  platform: 'web' | 'react-native' | 'android' | 'ios' | 'flutter';
  
  // From fullstory-stable-selectors
  stableSelectors: {
    dataComponent?: string;
    dataElements: string[];
    dataActions: string[];
    dataStates: string[];
  };
  
  // From fullstory-element-properties
  elementProperties: {
    fsElementNames: string[];
    businessProperties: string[]; // data-product-id, data-price, etc.
  };
  
  // From fullstory-privacy-controls
  privacyControls: {
    excludedFields: string[];
    maskedFields: string[];
  };
  
  // Assessment
  maturityLevel: 0 | 1 | 2 | 3 | 4;
  gaps: string[];
}
```

---

## WORKING WITH PARTIAL DECORATION

### Graceful Degradation Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SELECTOR FALLBACK CHAIN (Best → Worst)                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. data-element="X"         ← Best: Stable, semantic                       │
│  2. data-testid="X"          ← Good: Test-specific                          │
│  3. data-component + context ← Good: Scoped                                 │
│  4. data-action="X"          ← OK: Behavioral                               │
│  5. aria-label="X"           ← OK: Accessibility-based                      │
│  6. [role="X"]               ← Fallback: Semantic HTML                      │
│  7. button, input[type]      ← Fallback: Element type                       │
│  8. .class-name              ← Last resort: CSS class (warn user)           │
│                                                                             │
│  ALWAYS AVOID:                                                              │
│  ✗ Dynamic classes (.Button_x7k2s)                                         │
│  ✗ Position-based (:nth-child)                                             │
│  ✗ Auto-generated IDs (#react-select-123)                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Level-Specific Behavior

**Level 0 (No Decoration):**
```
⚠️ WARNING: No Fullstory decoration found.
Tests will be BRITTLE. Recommend implementing fullstory-stable-selectors first.
Proceeding with accessibility-based and semantic HTML selectors as fallback.
```

**Level 1 (Basic):**
- Use `data-element` and `data-component` for targeting
- Limited assertions (visibility, text content)
- No rich property assertions

**Level 2+ (Intermediate+):**
- Full selector capability
- Rich property assertions (`data-price`, `data-in-stock`)
- Page navigation verification

### Generating Improvement Recommendations

When gaps are found, recommend specific improvements:

```typescript
function generateRecommendations(inventory: ComponentDecorationInventory): string[] {
  const recs: string[] = [];
  
  if (inventory.stableSelectors.dataElements.length === 0) {
    recs.push('🔴 CRITICAL: Add data-element to interactive elements');
  }
  
  if (!inventory.stableSelectors.dataComponent) {
    recs.push('🟡 RECOMMENDED: Add data-component to component root');
  }
  
  if (inventory.elementProperties.fsElementNames.length === 0) {
    recs.push('🟢 OPTIONAL: Add data-fs-element for human-readable names');
  }
  
  return recs;
}
```

---

## INDUSTRY SKILL INTEGRATION

Industry-specific skills provide domain schemas that enhance test targeting.

### E-Commerce (fullstory-ecommerce)

```typescript
// E-commerce properties enable targeted testing
interface EcommerceProductProperties {
  'data-product-id': string;
  'data-price': string;
  'data-category': string;
  'data-in-stock': 'true' | 'false';
}

// Test patterns
await page.locator('[data-component="ProductCard"][data-category="Electronics"]').click();
await expect(productCard).toHaveAttribute('data-in-stock', 'true');
```

### SaaS/B2B

```typescript
// Role-based testing
interface SaaSUserProperties {
  'data-user-role': 'admin' | 'editor' | 'viewer';
  'data-plan-tier': 'free' | 'pro' | 'enterprise';
}

// Test patterns
await setupTestUser(page, { role: 'admin', plan: 'enterprise' });
await expect(page.locator('[data-element="admin-panel"]')).toBeVisible();
```

### Financial Services

```typescript
// Account-based testing with privacy awareness
interface FinancialAccountProperties {
  'data-account-type': 'checking' | 'savings';
  'data-account-status': 'active' | 'locked';
  // Actual amounts in fs-exclude regions
}
```

---

## CORE CONCEPTS

### Selector Priority

Always use selectors in this order:

1. `data-element` / `data-testid` — Most stable
2. `data-component` + `data-element` — Scoped
3. `data-action` — Behavioral
4. Element properties: `[data-product-id="X"]` — Data-driven
5. `aria-label` / accessibility
6. Semantic HTML
7. Text content — Last resort

### Core Skills → Test Capabilities

| Core Skill | Test Automation Capability |
|------------|---------------------------|
| `fullstory-stable-selectors` | Reliable element targeting |
| `fullstory-element-properties` | Rich assertions, data-driven targeting |
| `fullstory-page-properties` | Navigation verification, Page Object mapping |
| `fullstory-user-properties` | Test user setup, role-based scenarios |
| `fullstory-identify-users` | Test session identification |
| `fullstory-analytics-events` | Event verification, test data capture |
| `fullstory-privacy-controls` | Privacy-aware test patterns |
| `fullstory-capture-control` | Test session isolation |

---

## BEST PRACTICES

### ✅ DO

- Use `data-element` as primary selector
- Scope selectors with `data-component` when needed
- Use `data-action` for behavioral targeting
- Fall back to `aria-label` for accessibility-first selection
- Track test inputs via `trackEvent` for debugging masked fields
- Generate Page Objects from Fullstory decoration

### ❌ DON'T

- Use dynamic CSS classes (`.Button_x7k2s`)
- Use positional selectors (`:nth-child(3)`)
- Use auto-generated IDs (`#react-select-123`)
- Use text content for non-semantic selection
- Hard-code waits (`sleep(5000)`)
- Ignore privacy in test sessions

---

## KEY TAKEAWAYS FOR AGENT

### Workflow Summary

1. **Discover** → Scan for decoration, detect platform
2. **Analyze** → Determine maturity level (0-4)
3. **Route** → Web (`SKILL-WEB.md`) or Mobile (`SKILL-MOBILE.md`)
4. **Generate** → Use platform-specific patterns

### Questions to Ask

1. "Is your codebase following Fullstory stable selector patterns?"
2. "Which platform: Web, React Native, Native Mobile, or Flutter?"
3. "Which test framework are you using or considering?"
4. "Do you have privacy-masked fields that need test data capture?"

### Framework Selection Guide

| Scenario | Recommended Framework | Skill |
|----------|----------------------|-------|
| Modern web app | Playwright | SKILL-WEB.md |
| Legacy web | Cypress | SKILL-WEB.md |
| Enterprise web | Selenium | SKILL-WEB.md |
| React Native | Detox | SKILL-MOBILE.md |
| Flutter | integration_test | SKILL-MOBILE.md |
| Native Android | Espresso | SKILL-MOBILE.md |
| Native iOS | XCUITest | SKILL-MOBILE.md |
| Cross-platform mobile | Maestro/Appium | SKILL-MOBILE.md |

---

## REFERENCE LINKS

### Platform-Specific Files (This Directory)
- **Web Test Automation**: `./SKILL-WEB.md` — Cypress, Playwright, Selenium, WebdriverIO
- **Mobile Test Automation**: `./SKILL-MOBILE.md` — Detox, Espresso, XCUITest, Flutter, Appium, Maestro

### Fullstory Core Skills
- **Stable Selectors**: ../fullstory-stable-selectors/SKILL.md
- **Element Properties**: ../../core/fullstory-element-properties/SKILL.md
- **Page Properties**: ../../core/fullstory-page-properties/SKILL.md
- **Privacy Controls**: ../../core/fullstory-privacy-controls/SKILL.md
- **Analytics Events**: ../../core/fullstory-analytics-events/SKILL.md

### Industry Skills
- **E-Commerce**: ../../industry/fullstory-ecommerce/SKILL.md

---

*This is the CORE test automation skill. For framework-specific patterns, read `./SKILL-WEB.md` or `./SKILL-MOBILE.md` in this same directory.*
