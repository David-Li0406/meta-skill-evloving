---
id: accessibility-evaluation
name: "Accessibility Evaluation"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Accessibility Evaluation

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #accessibility #wcag #a11y
- **Agent:** faion-usability-agent

---

## Problem

Products exclude users with disabilities. Legal requirements (ADA, Section 508, AODA) are not met. Accessibility is treated as an afterthought. Testing only happens at the end, when fixes are expensive. Teams do not know what to test or how.

Without accessibility evaluation:
- Users with disabilities excluded
- Legal compliance risk
- Expensive late-stage fixes
- Poor experience for many users

---

## Framework

### What is Accessibility Evaluation?

Accessibility evaluation assesses whether a digital product can be used by people with disabilities, including those who are blind, deaf, have motor impairments, or have cognitive disabilities.

### WCAG Principles (POUR)

| Principle | Meaning | Examples |
|-----------|---------|----------|
| **Perceivable** | Can users perceive content? | Alt text, captions, contrast |
| **Operable** | Can users operate controls? | Keyboard access, timing |
| **Understandable** | Can users understand content? | Clear language, predictable |
| **Robust** | Does it work with assistive tech? | Valid code, ARIA |

### WCAG Conformance Levels

| Level | Description | Requirement |
|-------|-------------|-------------|
| **A** | Minimum accessibility | Must have |
| **AA** | Standard for most | Legal requirement in most places |
| **AAA** | Enhanced accessibility | Ideal but not always achievable |

### Evaluation Types

| Type | What it is | When to use |
|------|------------|-------------|
| **Automated testing** | Tools scan for issues | Continuous, catches ~30% |
| **Manual testing** | Human checks with tools | Development, catches ~50% |
| **Assistive tech testing** | Test with screen readers, etc. | Pre-release, real experience |
| **User testing** | People with disabilities test | Validation, catches remaining |

---

## Process

### Step 1: Automated Scanning

Run automated tools first:

```
Tools:
- axe DevTools (browser extension)
- WAVE (browser extension)
- Lighthouse (Chrome DevTools)
- Pa11y (CI integration)
```

**What automated tools find:**
- Missing alt text
- Color contrast issues
- Missing form labels
- Incorrect heading structure
- Missing language attribute

**What they miss:**
- Alt text quality
- Keyboard usability
- Meaningful reading order
- Context and understanding

### Step 2: Manual Testing

#### Keyboard Testing

Test without mouse:

| Check | How to Test | Pass |
|-------|-------------|------|
| Tab navigation | Tab through page | All interactive elements reachable |
| Focus visible | Watch for focus indicator | Always visible where you are |
| Logical order | Tab and note sequence | Order matches visual flow |
| Skip links | Tab from top | Skip to main content available |
| Traps | Tab everywhere | Can always Tab out |
| Keyboard shortcuts | Test documented shortcuts | Work and don't conflict |

#### Color and Contrast

| Check | Requirement | Tool |
|-------|-------------|------|
| Text contrast | 4.5:1 (normal), 3:1 (large) | Colour Contrast Analyser |
| UI contrast | 3:1 for interactive elements | Same |
| Not color alone | Color not only indicator | Manual check |

#### Content Structure

| Check | What to verify |
|-------|----------------|
| Headings | Logical hierarchy (H1 → H2 → H3) |
| Landmarks | Main, nav, header, footer marked |
| Lists | Proper list markup where appropriate |
| Tables | Headers marked, scope defined |
| Links | Descriptive text (not "click here") |

### Step 3: Screen Reader Testing

Test with actual screen readers:

| Screen Reader | Platform | Users |
|---------------|----------|-------|
| **NVDA** | Windows | Free, common |
| **JAWS** | Windows | Enterprise, expensive |
| **VoiceOver** | Mac/iOS | Built-in |
| **TalkBack** | Android | Built-in |

**Basic screen reader checks:**
- Can you navigate by headings?
- Are images described?
- Do forms announce labels?
- Are state changes announced?
- Can you complete key tasks?

### Step 4: Cognitive Accessibility

Check for cognitive accessibility:

| Check | What to verify |
|-------|----------------|
| Clear language | Plain language, no jargon |
| Consistent navigation | Same location throughout |
| Error prevention | Confirmation before destructive actions |
| Error recovery | Clear error messages with solutions |
| Timeouts | Warnings before timeout, option to extend |
| Animation | Can be paused, no excessive motion |

### Step 5: Document and Fix

Prioritize issues:

| Priority | Description | Fix Timeline |
|----------|-------------|--------------|
| **Critical** | Blocks access completely | Immediately |
| **High** | Major barrier, workaround difficult | This sprint |
| **Medium** | Creates difficulty | Next sprint |
| **Low** | Enhancement, not blocking | Backlog |

---

## Templates

### Accessibility Audit Template

```markdown
# Accessibility Audit Report

**Product:** [Name]
**Version:** [Version]
**Date:** [Date]
**Auditor:** [Name]
**Standard:** WCAG 2.1 Level AA

## Executive Summary

**Overall status:** [Pass/Fail/Partial]
**Critical issues:** [Count]
**Total issues:** [Count]

**Summary:**
[Brief overview of accessibility status]

## Methodology

| Method | Coverage |
|--------|----------|
| Automated scan (axe) | 100% of pages |
| Manual keyboard testing | All interactive elements |
| Screen reader (VoiceOver) | Key user flows |
| Color contrast check | All text and UI |

## Findings by Principle

### Perceivable

| Issue | WCAG | Count | Priority |
|-------|------|-------|----------|
| Missing alt text | 1.1.1 | 5 | High |
| Low contrast | 1.4.3 | 12 | High |
| | | | |

### Operable

| Issue | WCAG | Count | Priority |
|-------|------|-------|----------|
| | | | |

### Understandable

| Issue | WCAG | Count | Priority |
|-------|------|-------|----------|
| | | | |

### Robust

| Issue | WCAG | Count | Priority |
|-------|------|-------|----------|
| | | | |

## Detailed Findings

### Issue 1: [Title]

**WCAG:** [Criterion number and name]
**Priority:** [Critical/High/Medium/Low]
**Location:** [Page/component]

**Problem:**
[Description of the issue]

**Impact:**
[Who is affected and how]

**Recommendation:**
[How to fix]

**Code example:**
```html
<!-- Current -->
<img src="photo.jpg">

<!-- Fixed -->
<img src="photo.jpg" alt="Description of image">
```

### Issue 2: [Title]
[Same structure]

## Testing Checklist

- [x] Automated scan completed
- [x] Keyboard navigation tested
- [x] Screen reader tested
- [x] Color contrast verified
- [ ] User testing with disabled users

## Recommendations

1. **Immediate:** [Critical fixes]
2. **Short-term:** [High priority fixes]
3. **Ongoing:** [Process improvements]
```

### Issue Template

```markdown
## Issue: [Brief title]

**WCAG Criterion:** [e.g., 1.4.3 Contrast (Minimum)]
**Level:** A / AA / AAA
**Priority:** Critical / High / Medium / Low
**Component:** [Where issue occurs]

**Description:**
[What the issue is]

**User Impact:**
[Who is affected, how it affects them]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What currently happens]

**Recommendation:**
[How to fix]

**Resources:**
- [Link to WCAG understanding doc]
- [Link to technique]
```

---

## Examples

### Example 1: Form Accessibility

**Issue:** Form inputs have no visible labels

**Before:**
```html
<input type="text" placeholder="Email">
```

**Problem:**
- Screen readers may not announce the field purpose
- Placeholder disappears when typing
- Low contrast placeholder text

**After:**
```html
<label for="email">Email address</label>
<input type="text" id="email" name="email"
       aria-describedby="email-hint">
<span id="email-hint">We'll never share your email.</span>
```

### Example 2: Image Accessibility

**Issue:** Decorative image has no alt attribute

**Decorative image (should be hidden):**
```html
<img src="decorative-line.png" alt="" role="presentation">
```

**Informative image (needs description):**
```html
<img src="chart.png" alt="Sales increased 25% in Q3 compared to Q2">
```

**Complex image (needs long description):**
```html
<figure>
  <img src="complex-diagram.png"
       alt="System architecture diagram"
       aria-describedby="diagram-desc">
  <figcaption id="diagram-desc">
    The system consists of three layers: presentation,
    business logic, and data. [Full description...]
  </figcaption>
</figure>
```

---

## Tools

### Automated Testing

| Tool | Type | Use For |
|------|------|---------|
| axe DevTools | Browser extension | Quick page scan |
| WAVE | Browser extension | Visual feedback |
| Lighthouse | Chrome DevTools | Performance + a11y |
| Pa11y | CLI/CI | Automated pipeline |
| SiteImprove | Service | Enterprise scanning |

### Manual Testing

| Tool | Purpose |
|------|---------|
| Colour Contrast Analyser | Check contrast ratios |
| HeadingsMap | Check heading structure |
| Web Developer Toolbar | Inspect page structure |
| ANDI | Section 508 testing |

### Screen Readers

| Tool | Platform | Free |
|------|----------|------|
| NVDA | Windows | Yes |
| VoiceOver | Mac/iOS | Built-in |
| TalkBack | Android | Built-in |
| JAWS | Windows | No ($$$) |

---

## Common Mistakes

1. **Relying only on automated tools** - They catch only 30% of issues
2. **Testing only with mouse** - Keyboard users have different experience
3. **Ignoring cognitive accessibility** - Not just visual impairments
4. **Adding ARIA incorrectly** - Bad ARIA worse than no ARIA
5. **Testing at the end** - Should be continuous

---

## Quick Checks

### Five-Minute Test

```
1. Tab through the page
   - Can you reach everything?
   - Can you see where you are?

2. Zoom to 200%
   - Is everything still usable?
   - Does content reflow?

3. Check one image
   - Does alt text make sense?

4. Check one form
   - Are labels visible and connected?

5. Run axe DevTools
   - Any critical issues?
```

### Pre-Commit Checks

Before code review:
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color contrast passes (4.5:1)
- [ ] Interactive elements keyboard accessible
- [ ] Heading hierarchy is correct

---

## Checklist

- [ ] Automated scan run
- [ ] All critical issues fixed
- [ ] Keyboard navigation works
- [ ] Tab order is logical
- [ ] Focus is always visible
- [ ] Screen reader testing done
- [ ] Alt text is meaningful
- [ ] Color contrast passes
- [ ] Form labels present
- [ ] Error messages clear
- [ ] Headings are hierarchical
- [ ] Links are descriptive
- [ ] No keyboard traps
- [ ] Skip links present
- [ ] ARIA used correctly

---

## References

- WCAG 2.1 Guidelines: w3.org/WAI/WCAG21/quickref/
- WebAIM: webaim.org
- A11y Project: a11yproject.com
- Deque University: dequeuniversity.com