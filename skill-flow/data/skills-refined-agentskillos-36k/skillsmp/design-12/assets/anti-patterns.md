# Design Anti-Patterns

## Overview

These patterns seem reasonable but consistently lead to poor user experiences. Avoid them.

---

## 1. Floating Labels

### What It Is

Labels that sit inside the input and "float" up when focused or filled.

```html
<!-- Floating label pattern -->
<div class="floating-label">
  <input type="text" placeholder=" ">
  <label>Email Address</label>
</div>
```

### Why It's Bad

- **Cognitive load:** Users must read and track moving elements
- **Accessibility:** Screen readers may miss the label
- **Small tap target:** Label competes with input space
- **No placeholder space:** Can't show format hints
- **Browser autofill:** Often breaks the float animation
- **Long labels:** Truncated when floated

### What To Do Instead

**Labels above inputs - always visible:**

```html
<div class="form-group">
  <label for="email">Email Address</label>
  <input type="email" id="email" placeholder="you@example.com">
</div>
```

```css
.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.form-group label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
}
```

---

## 2. Inline Validation (As You Type)

### What It Is

Validating and showing errors while the user is still typing.

```javascript
// Inline validation
input.addEventListener('input', () => {
  if (!isValidEmail(input.value)) {
    showError('Invalid email'); // Shows while typing!
  }
});
```

### Why It's Bad

- **Premature errors:** "Invalid email" shows before user finishes typing
- **Anxiety-inducing:** Red errors flash constantly
- **Interrupts flow:** User focuses on errors, not content
- **False positives:** Intermediate states are "invalid"

### What To Do Instead

**Validate on blur (leaving field) or submit:**

```javascript
// Validate on blur
input.addEventListener('blur', () => {
  if (input.value && !isValidEmail(input.value)) {
    showError('Please enter a valid email address');
  }
});

// Clear error when user starts fixing
input.addEventListener('focus', () => {
  clearError();
});
```

**Or validate on submit with summary:**

```javascript
form.addEventListener('submit', (e) => {
  const errors = validateForm(form);
  if (errors.length > 0) {
    e.preventDefault();
    showErrors(errors);
    focusFirstError();
  }
});
```

---

## 3. Generic Error Messages

### What It Is

Error messages that don't tell users what went wrong or how to fix it.

```html
<!-- Generic, unhelpful errors -->
<p class="error">Invalid input</p>
<p class="error">An error occurred</p>
<p class="error">Please try again</p>
<p class="error">Something went wrong</p>
```

### Why It's Bad

- **No guidance:** User doesn't know what to fix
- **Frustrating:** Creates trial-and-error guessing
- **Wastes time:** User may try the same wrong thing
- **Abandonment:** Users give up and leave

### What To Do Instead

**Specific, actionable error messages:**

```html
<!-- Specific, helpful errors -->
<p class="error">Password must be at least 8 characters</p>
<p class="error">Email format should be: name@example.com</p>
<p class="error">Phone number should include area code (e.g., 555-123-4567)</p>
<p class="error">That username is taken. Try "john_doe_42" instead?</p>
```

**Error message formula:**
1. What's wrong
2. Why it's wrong (if not obvious)
3. How to fix it

---

## 4. Tooltips for Critical Information

### What It Is

Hiding important information behind hover tooltips.

```html
<!-- Critical info in tooltip -->
<button>
  Delete Account
  <span class="tooltip">This permanently deletes all your data</span>
</button>
```

### Why It's Bad

- **Easy to miss:** Users may not hover before clicking
- **Touch devices:** Hover doesn't exist on mobile
- **Accessibility:** Screen readers may miss tooltips
- **Timing issues:** Tooltips have delay, users act fast

### What To Do Instead

**Show critical information directly:**

```html
<div class="dangerous-action">
  <button class="btn-danger">Delete Account</button>
  <p class="warning">
    <strong>Warning:</strong> This permanently deletes all your data
    and cannot be undone.
  </p>
</div>
```

**Or use a confirmation dialog:**

```html
<dialog class="confirm-dialog">
  <h2>Delete your account?</h2>
  <p>This will permanently delete:</p>
  <ul>
    <li>Your profile and settings</li>
    <li>All your saved data</li>
    <li>Your subscription</li>
  </ul>
  <p><strong>This cannot be undone.</strong></p>
  <div class="dialog-actions">
    <button class="btn-secondary">Cancel</button>
    <button class="btn-danger">Delete Account</button>
  </div>
</dialog>
```

---

## 5. Disabled Buttons Without Explanation

### What It Is

Buttons that are disabled with no indication of why or how to enable them.

```html
<!-- Unexplained disabled button -->
<button disabled>Submit</button>
```

### Why It's Bad

- **Confusing:** User doesn't know what's wrong
- **No path forward:** User can't fix the problem
- **Feels broken:** Looks like a bug, not a feature
- **Frustrating:** Creates dead ends

### What To Do Instead

**Option 1: Keep button enabled, validate on click:**

```javascript
submitButton.addEventListener('click', () => {
  const errors = validateForm();
  if (errors.length > 0) {
    showErrors(errors);
  } else {
    submitForm();
  }
});
```

**Option 2: Explain why disabled:**

```html
<button disabled aria-describedby="submit-help">Submit</button>
<p id="submit-help" class="help-text">
  Complete all required fields to submit
</p>
```

**Option 3: Progress indicator:**

```html
<div class="form-progress">
  <p>Complete 3 of 5 required fields</p>
  <progress value="3" max="5"></progress>
</div>
<button disabled>Submit</button>
```

---

## 6. Custom Scrollbars

### What It Is

Overriding the browser's native scrollbar with custom styling.

```css
/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
}
```

### Why It's Bad

- **Inconsistent:** Only works in some browsers
- **Accessibility:** May remove keyboard scrolling cues
- **Performance:** Can cause janky scrolling
- **Familiarity:** Users expect native behavior
- **Small targets:** Custom scrollbars often too thin

### What To Do Instead

**Leave scrollbars alone. Trust the browser.**

If you must customize (rarely):
- Keep width at least 16px
- Maintain high contrast
- Don't hide scrollbars that should be visible
- Test on all browsers and devices

```css
/* If you must - minimal customization */
@supports (scrollbar-color: auto) {
  * {
    scrollbar-color: var(--color-neutral-400) var(--color-neutral-100);
    scrollbar-width: auto; /* thin, auto, or none - prefer auto */
  }
}
```

---

## 7. Hamburger Menu on Desktop

### What It Is

Hiding main navigation behind a hamburger menu even on large screens.

```html
<!-- Hamburger on desktop -->
<nav class="desktop-hamburger">
  <button class="hamburger-btn">☰</button>
  <ul class="hidden-menu">
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

### Why It's Bad

- **Extra clicks:** Users must click to see options
- **Discoverability:** Users don't know what's available
- **Wastes space:** Desktop has room for full navigation
- **Slower task completion:** More steps to navigate

### What To Do Instead

**Show full navigation on desktop:**

```html
<nav class="main-nav">
  <ul class="nav-list">
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
  <button class="hamburger-btn mobile-only">☰</button>
</nav>
```

```css
.nav-list {
  display: none;
}

.hamburger-btn {
  display: block;
}

@media (min-width: 1024px) {
  .nav-list {
    display: flex;
    gap: var(--space-lg);
  }

  .hamburger-btn {
    display: none;
  }
}
```

---

## 8. Infinite Scroll Without Alternative

### What It Is

Loading content automatically as user scrolls, with no way to reach the footer or navigate to specific content.

### Why It's Bad

- **Can't reach footer:** Contact, legal links inaccessible
- **No sense of progress:** User doesn't know how much content exists
- **Bookmark impossible:** Can't link to specific items
- **Browser back breaks:** Returns to top, losing position
- **Accessibility:** Screen readers struggle with dynamic content

### What To Do Instead

**Pagination or "Load More" button:**

```html
<div class="content-list">
  <!-- Items 1-20 -->
</div>

<div class="pagination">
  <button class="btn-secondary">Load More</button>
  <p>Showing 20 of 156 items</p>
</div>

<footer>
  <!-- Footer is always accessible -->
</footer>
```

**Or hybrid approach:**

```html
<div class="content-list">
  <!-- Items -->
</div>

<nav class="pagination">
  <a href="?page=1">1</a>
  <a href="?page=2">2</a>
  <a href="?page=3" aria-current="page">3</a>
  <a href="?page=4">4</a>
  <span>...</span>
  <a href="?page=12">12</a>
</nav>
```

---

## 9. Carousels / Auto-Rotating Content

### What It Is

Content that automatically changes without user control.

### Why It's Bad

- **Users miss content:** Rotates before they finish reading
- **No control:** User can't pause or go back
- **Accessibility nightmare:** Screen readers get confused
- **Banner blindness:** Users learn to ignore carousels
- **Performance:** Multiple images loaded

### What To Do Instead

**Static hero with clear CTAs:**

```html
<section class="hero">
  <h1>Your Main Message</h1>
  <p>Supporting text that users can read at their own pace.</p>
  <a href="/action" class="btn-primary">Take Action</a>
</section>
```

**Or user-controlled tabs:**

```html
<div class="feature-tabs">
  <div class="tab-controls">
    <button class="tab active">Feature 1</button>
    <button class="tab">Feature 2</button>
    <button class="tab">Feature 3</button>
  </div>
  <div class="tab-content">
    <!-- User-controlled content switching -->
  </div>
</div>
```

---

## 10. Modal Overuse

### What It Is

Using modal dialogs for everything - confirmations, forms, information, errors.

### Why It's Bad

- **Disruptive:** Interrupts user's flow
- **Mobile issues:** Modals often break on small screens
- **Stacking:** Multiple modals create confusion
- **Escape routes:** Users feel trapped
- **Context loss:** Can't reference page content

### What To Do Instead

**Inline alternatives:**

```html
<!-- Instead of delete confirmation modal -->
<button class="btn-danger" data-confirm>Delete Item</button>
<div class="inline-confirm hidden">
  <p>Delete this item?</p>
  <button class="btn-secondary">Cancel</button>
  <button class="btn-danger">Delete</button>
</div>
```

**When modals ARE appropriate:**
- Complex multi-step forms
- Media preview (lightbox)
- Critical warnings requiring decision
- Login/signup flows

---

## Quick Reference: Do vs Don't

| Don't | Do |
|-------|-----|
| Floating labels | Labels above inputs |
| Validate while typing | Validate on blur/submit |
| "Error occurred" | "Password must be 8+ characters" |
| Tooltip for warnings | Show warnings inline |
| Disabled without reason | Explain why disabled |
| Custom scrollbars | Native scrollbars |
| Hamburger on desktop | Full nav on desktop |
| Infinite scroll only | Pagination or load more |
| Auto-rotating carousels | Static or user-controlled |
| Modals for everything | Inline interactions |
