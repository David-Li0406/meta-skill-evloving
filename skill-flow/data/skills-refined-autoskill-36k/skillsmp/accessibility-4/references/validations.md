# Accessibility - Validations

## Image without alt attribute

### **Id**
missing-alt-text
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <img(?![^>]*alt=)[^>]*>
### **Message**
Image missing alt attribute - add alt text or alt="" for decorative
### **Fix Action**
Add alt="Description of image" or alt="" for decorative images
### **Applies To**
  - *.html
  - *.jsx
  - *.tsx
  - *.vue

## Link with no accessible name

### **Id**
empty-link
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <a[^>]*>(\s*|<img[^>]*>)\s*</a>
### **Message**
Link has no accessible name - add text or aria-label
### **Fix Action**
Add link text or aria-label="Description"
### **Applies To**
  - *.html
  - *.jsx
  - *.tsx

## Button with no accessible name

### **Id**
empty-button
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <button[^>]*>(\s*|<(svg|img|i)[^>]*>)\s*</button>
### **Message**
Button has no accessible name - add text or aria-label
### **Fix Action**
Add button text or aria-label="Action description"
### **Applies To**
  - *.html
  - *.jsx
  - *.tsx

## Click handler on non-interactive element

### **Id**
onclick-without-role
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <(div|span)[^>]*onclick=(?![^>]*role=)
### **Message**
Click handler on div/span without role - use button or add role="button"
### **Fix Action**
Use <button> or add role="button" tabindex="0" onKeyDown
### **Applies To**
  - *.html
  - *.jsx
  - *.tsx

## Positive tabindex value

### **Id**
positive-tabindex
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - tabindex="[1-9][0-9]*"
  - tabIndex=\{[1-9][0-9]*\}
### **Message**
Positive tabindex creates unpredictable focus order
### **Fix Action**
Use tabindex="0" or tabindex="-1", fix order in DOM
### **Applies To**
  - *.html
  - *.jsx
  - *.tsx

## Focus outline removed without replacement

### **Id**
no-focus-outline
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - :focus\s*\{[^}]*outline:\s*(none|0)[^}]*\}
  - outline:\s*(none|0)
### **Message**
Focus outline removed - provide visible focus indicator
### **Fix Action**
Use :focus-visible with custom outline or box-shadow
### **Applies To**
  - *.css
  - *.scss

## Auto-refresh or redirect

### **Id**
auto-refresh
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <meta[^>]*http-equiv="refresh"
  - window\.location[^;]*setTimeout
  - setTimeout[^}]*window\.location
### **Message**
Auto-refresh/redirect may disorient users
### **Fix Action**
Provide user control to pause, stop, or extend time limit
### **Applies To**
  - *.html
  - *.js
  - *.jsx

## Form input without label

### **Id**
missing-form-label
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <input(?![^>]*id="[^"]+")[^>]*>
  - <input[^>]*id="([^"]+)"(?!.*<label[^>]*for="\1")
### **Message**
Form input missing associated label
### **Fix Action**
Add <label for="inputId"> or wrap in <label>
### **Applies To**
  - *.html
  - *.jsx
  - *.tsx

## HTML element without lang attribute

### **Id**
missing-lang
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <html(?![^>]*lang=)
### **Message**
Page missing language declaration
### **Fix Action**
Add lang="en" (or appropriate code) to <html>
### **Applies To**
  - *.html

## Media with autoplay

### **Id**
autoplay-media
### **Severity**
info
### **Type**
regex
### **Pattern**
  - <(video|audio)[^>]*autoplay(?![^>]*muted)
### **Message**
Autoplay media can be disruptive - ensure muted or user-controlled
### **Fix Action**
Add muted attribute or provide play/pause controls
### **Applies To**
  - *.html
  - *.jsx
  - *.tsx

## ARIA role conflicts with implicit role

### **Id**
aria-role-conflict
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <button[^>]*role="link"
  - <a[^>]*role="button"
  - <input[^>]*role="
### **Message**
ARIA role conflicts with element's implicit role
### **Fix Action**
Use appropriate HTML element instead of overriding role
### **Applies To**
  - *.html
  - *.jsx
  - *.tsx

## Focusable element with aria-hidden

### **Id**
aria-hidden-focus
### **Severity**
error
### **Type**
regex
### **Pattern**
  - aria-hidden="true"[^>]*(?:tabindex="0"|<button|<a |<input)
  - <(button|a|input)[^>]*aria-hidden="true"
### **Message**
Focusable element has aria-hidden - creates confusing experience
### **Fix Action**
Remove aria-hidden or make element non-focusable
### **Applies To**
  - *.html
  - *.jsx
  - *.tsx