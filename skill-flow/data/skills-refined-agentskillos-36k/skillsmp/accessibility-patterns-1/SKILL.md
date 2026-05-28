---
name: "Accessibility Patterns"
description: "WCAG 2.2 Level AA compliance for Rails/ViewComponent/Hotwire. Use when: (1) Building interactive widgets, (2) Handling form validation errors, (3) Adding dynamic content with Turbo Streams, (4) Auditing existing components. Trigger keywords: accessibility, a11y, WCAG, ARIA, screen reader, keyboard, focus, contrast"
version: 1.1.0
---

# Accessibility Patterns

WCAG 2.2 Level AA compliance for Rails applications.

## Accessibility Decision Tree

```
What are you building?
│
├─ Interactive widget (modal, dropdown, tabs)
│   └─ Go to: Widget ARIA Patterns
│
├─ Form with validation
│   └─ Go to: Form Accessibility
│
├─ Dynamic content (Turbo Stream)
│   └─ Go to: Live Regions
│
├─ Icon-only button
│   └─ Add: aria-label="Action name" + aria-hidden="true" on icon
│
└─ Custom keyboard navigation
    └─ Go to: Keyboard Patterns
```

---

## WCAG AA Quick Reference

| Criterion | Requirement | Check |
|-----------|-------------|-------|
| 1.4.3 Contrast | 4.5:1 text, 3:1 large text | webaim.org/resources/contrastchecker |
| 2.1.1 Keyboard | All functionality via keyboard | Tab through everything |
| 2.4.7 Focus Visible | Clear focus indicator | `focus:ring-2 focus:ring-primary` |
| 3.3.1 Error ID | Identify errors clearly | `aria-invalid` + `role="alert"` |
| 4.1.3 Status | Announce without focus | `aria-live="polite"` |

---

## NEVER Do This

**NEVER** use positive tabindex:
```erb
<%# WRONG: Breaks natural focus order %>
<input tabindex="1">
<input tabindex="2">

<%# RIGHT: Let DOM order determine focus %>
<input>
<input>
```

**NEVER** rely on color alone for meaning:
```erb
<%# WRONG: Only color indicates status %>
<span class="text-success">Approved</span>

<%# RIGHT: Icon + text + color %>
<span class="text-success flex items-center gap-2">
  <svg aria-hidden="true">...</svg>
  Approved
</span>
```

**NEVER** use ARIA when native HTML works:
```erb
<%# WRONG: Redundant ARIA %>
<button role="button">Click</button>

<%# RIGHT: Native element %>
<button>Click</button>
```

**NEVER** hide content from screen readers without reason:
```erb
<%# WRONG: Hiding meaningful content %>
<p aria-hidden="true">Important information</p>

<%# RIGHT: Only hide decorative content %>
<img src="decoration.svg" alt="" aria-hidden="true">
```

**NEVER** trap keyboard focus without escape:
- Modals MUST close on Escape key
- Focus MUST return to trigger element after modal closes

---

## Widget ARIA Patterns

### Modal Dialog
```erb
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Title</h2>
  <button aria-label="Close">×</button>
</div>
```
**Requirements**: Focus trap, Escape closes, return focus to trigger.

### Tabs
```erb
<div role="tablist" aria-label="Section tabs">
  <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">Content</div>
```
**Requirements**: Arrow keys navigate, roving tabindex pattern.

### Dropdown Menu
```erb
<button aria-haspopup="menu" aria-expanded="false" aria-controls="menu">
  Options
</button>
<ul role="menu" id="menu" hidden>
  <li role="menuitem"><a href="#">Edit</a></li>
</ul>
```
**Requirements**: Escape closes, arrow keys navigate.

### Expandable Section
```erb
<button aria-expanded="false" aria-controls="details">Show Details</button>
<div id="details" hidden>Content...</div>
```

---

## Form Accessibility

### Required Pattern
```erb
<label for="email">Email <span aria-hidden="true">*</span></label>
<input id="email" type="email" aria-required="true">
```

### Error Pattern
```erb
<input id="email"
       type="email"
       aria-invalid="true"
       aria-describedby="email-error"
       aria-errormessage="email-error">
<div id="email-error" role="alert">Please enter valid email</div>
```

### Hint Pattern
```erb
<input id="password" type="password" aria-describedby="password-hint">
<div id="password-hint">Minimum 8 characters</div>
```

### Error Summary (Top of Form)
```erb
<div role="alert" aria-live="assertive">
  <h2>Please fix the following:</h2>
  <ul>
    <li><a href="#email">Email is invalid</a></li>
  </ul>
</div>
```

---

## Live Regions (Turbo Streams)

### Polite Announcements (Non-urgent)
```erb
<div aria-live="polite" aria-atomic="true">
  <%= flash[:notice] %>
</div>
```

### Assertive Announcements (Urgent)
```erb
<div role="alert" aria-live="assertive">
  <%= flash[:alert] %>
</div>
```

### Status Updates
```erb
<div role="status" aria-live="polite">
  Showing <%= @items.count %> items
</div>
```

### Loading State
```erb
<div aria-busy="true">
  <span class="sr-only">Loading...</span>
</div>
```

---

## Keyboard Patterns

### Standard Keys
| Component | Keys | Action |
|-----------|------|--------|
| Button | Enter, Space | Activate |
| Tabs | Arrow keys | Switch |
| Menu | Arrow keys, Enter | Navigate, select |
| Modal | Escape | Close |

### Focus Management After Actions
```javascript
// After delete: focus next item or container
item.remove()
nextItem?.focus() || container.focus()

// After modal close: return focus to trigger
modal.hidden = true
triggerElement.focus()
```

### Skip Link (Required)
```erb
<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-primary focus:text-white focus:px-4 focus:py-2">
  Skip to main content
</a>
<main id="main" tabindex="-1">...</main>
```

---

## Testing Checklist

**Before shipping any UI:**

```
Keyboard:
[ ] Tab reaches all interactive elements
[ ] Focus indicator visible (3:1 contrast)
[ ] Escape closes modals/dropdowns
[ ] No keyboard traps

Screen Reader:
[ ] Images have alt text (or alt="" if decorative)
[ ] Form inputs have labels
[ ] Errors announced with role="alert"
[ ] Dynamic updates use aria-live

Visual:
[ ] Text contrast 4.5:1 minimum
[ ] UI component contrast 3:1
[ ] Works at 200% zoom
[ ] Meaning not conveyed by color alone
```

**Automated Testing:**
```ruby
# spec/system/accessibility_spec.rb
require "axe-rspec"

it "is accessible" do
  visit dashboard_path
  expect(page).to be_axe_clean.according_to(:wcag2aa)
end
```

---

## TailAdmin Focus Classes

```erb
<%# Standard focus ring %>
<button class="focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:outline-none">

<%# Keyboard-only focus %>
<a class="focus-visible:ring-2 focus-visible:ring-primary focus-visible:outline-none">

<%# Dark background %>
<button class="focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-boxdark">
```

---

## References

Detailed implementation examples in `references/`:
- `stimulus-controllers.md` - Focus trap, roving tabindex, modal controllers
- `viewcomponent-examples.md` - Accessible form, modal, tabs components
- `wcag-criteria.md` - Complete WCAG 2.2 Level AA criteria with TailAdmin colors
