# Ux Design - Validations

## Missing Form Labels

### **Id**
missing-form-labels
### **Severity**
error
### **Type**
regex
### **Pattern**
<input(?![^>]*aria-label)(?![^>]*id=["'][^"']+["'][^>]*>.*<label[^>]+for=["'][^"']+["'])|<input[^>]+placeholder=["'][^"']+["'](?![^>]*<label)
### **Message**
Form input missing accessible label. Placeholder is not a replacement.
### **Fix Action**
Add proper <label> element or aria-label attribute
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Missing Form Error Messages

### **Id**
no-form-error-handling
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <form(?!.*error)(?!.*invalid)(?!.*aria-invalid)
### **Message**
Form missing error handling and validation feedback.
### **Fix Action**
Add error state UI, error messages, and aria-invalid attributes
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Loading State

### **Id**
no-loading-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
onClick.*fetch\((?!.*loading)(?!.*isLoading)|onSubmit.*axios\.(?!.*loading)
### **Message**
Async action missing loading state feedback.
### **Fix Action**
Add loading state with spinner/skeleton and disable button during load
### **Applies To**
  - *.tsx
  - *.jsx

## Generic Button Text

### **Id**
poor-button-microcopy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <button[^>]*>(Submit|Click Here|Click Me|Button|OK)</button>
### **Message**
Button text is generic. Use action-oriented microcopy.
### **Fix Action**
Use specific action words (e.g., 'Create Account', 'Download Report', 'Save Changes')
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Missing Empty State UI

### **Id**
missing-empty-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.length === 0.*<div>No data|\.length === 0.*<p>Empty
### **Message**
Empty state lacks helpful UI. Guide users on next action.
### **Fix Action**
Add illustration, helpful message, and CTA (e.g., 'Create your first item')
### **Applies To**
  - *.tsx
  - *.jsx

## Destructive Action Without Confirmation

### **Id**
destructive-action-no-confirm
### **Severity**
error
### **Type**
regex
### **Pattern**
onClick.*delete(?!.*confirm)(?!.*modal)|onClick.*remove(?!.*confirm)(?!.*dialog)
### **Message**
Destructive action (delete/remove) lacks confirmation dialog.
### **Fix Action**
Add confirmation modal/dialog before executing destructive actions
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Success Feedback

### **Id**
no-success-feedback
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - onSubmit.*(?!toast)(?!notification)(?!success)
### **Message**
Form submission missing success feedback.
### **Fix Action**
Show toast notification, success message, or redirect with confirmation
### **Applies To**
  - *.tsx
  - *.jsx

## Password Field UX Issues

### **Id**
poor-password-ux
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <input[^>]+type=["']password["'](?!.*toggle)(?!.*show)
### **Message**
Password field missing show/hide toggle.
### **Fix Action**
Add password visibility toggle button for better UX
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Input Helper Text

### **Id**
no-input-helper-text
### **Severity**
info
### **Type**
regex
### **Pattern**
<input[^>]+type=["']email["'](?!.*help)(?!.*hint)|<input[^>]+type=["']password["'](?!.*requirements)
### **Message**
Complex input field missing helper text or format examples.
### **Fix Action**
Add helper text explaining format or requirements (e.g., 'Enter your work email')
### **Applies To**
  - *.tsx
  - *.jsx

## Pagination Missing Current State

### **Id**
pagination-no-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pagination(?!.*active)(?!.*current)
### **Message**
Pagination component not showing current page clearly.
### **Fix Action**
Highlight current page and show total pages (e.g., 'Page 2 of 10')
### **Applies To**
  - *.tsx
  - *.jsx

## Modal Missing Close Button

### **Id**
modal-no-close-button
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <(dialog|Modal)(?!.*close)(?!.*onClose)
### **Message**
Modal/dialog missing clear close mechanism.
### **Fix Action**
Add close button (X icon) and ESC key handler
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Keyboard Navigation

### **Id**
no-keyboard-navigation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <div[^>]+onClick(?!.*onKeyDown)(?!.*onKeyPress)
### **Message**
Click handler on non-button element without keyboard support.
### **Fix Action**
Add onKeyDown handler or use semantic <button> element instead
### **Applies To**
  - *.tsx
  - *.jsx