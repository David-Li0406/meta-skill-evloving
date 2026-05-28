# Taste And Craft - Validations

## Inconsistent Naming Convention

### **Id**
tc-inconsistent-naming
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - get[A-Z]\w+.*fetch[A-Z]\w+
  - is[A-Z]\w+.*has[A-Z]\w+
  - handle[A-Z]\w+.*on[A-Z]\w+
### **Message**
Inconsistent naming patterns. Craft means consistency. Pick conventions and stick to them.
### **Fix Action**
Standardize: all fetchers use fetch*, all boolean getters use is*, all handlers use handle*
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx

## Magic Values Without Context

### **Id**
tc-magic-values
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?<!const\s\w+\s=\s)(?:0\.5|0\.8|1\.5|2\.0|10|100|500|1000)(?!\d)
  - margin:\s*\d+px|padding:\s*\d+px|gap:\s*\d+px
### **Message**
Magic numbers in code. Craft means intentional, documented choices.
### **Fix Action**
Extract to named constants or design tokens: 16 → SPACING_MD or --spacing-md
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx
  - *.css

## Duplicate Code Blocks

### **Id**
tc-copy-paste-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (\n\s*\w+\([^)]*\)\s*\{[^}]{50,}\}).*\1
### **Message**
Repeated code pattern detected. Craft means DRY. Duplication is a design smell.
### **Fix Action**
Extract to shared function or component. One source of truth.
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx

## Generic Error Messages

### **Id**
tc-generic-error
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - something.?went.?wrong|error.?occurred|an.?error|oops|failed
### **Message**
Generic error message. Craft means helpful errors that guide users to resolution.
### **Fix Action**
Specific error: 'Something went wrong' → 'Could not save. Check your connection and try again.'
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx
  - *.json

## Arbitrary Z-Index Values

### **Id**
tc-z-index-chaos
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - z-index:\s*(?:9999|99999|100000|\d{4,})
  - zIndex:\s*(?:9999|99999|100000|\d{4,})
### **Message**
Z-index arms race detected. Arbitrary high values indicate missing stacking strategy.
### **Fix Action**
Create z-index scale: base(0), dropdown(10), modal(20), toast(30). Use system, not random numbers.
### **Applies To**
  - *.css
  - *.scss
  - *.ts
  - *.tsx

## Text Truncation Without Tooltip

### **Id**
tc-truncation-no-tooltip
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - text-overflow:\s*ellipsis
  - truncate
  - line-clamp
### **Message**
Text truncation without showing full content. User cannot access hidden information.
### **Fix Action**
Add title attribute or tooltip to reveal full content on hover
### **Applies To**
  - *.css
  - *.scss
  - *.tsx
  - *.jsx

## Loading State Without Skeleton

### **Id**
tc-loading-no-skeleton
### **Severity**
info
### **Type**
regex
### **Pattern**
  - loading|isLoading|pending
### **Message**
Loading state detected. Spinners feel slower than skeletons. Show shape of incoming content.
### **Fix Action**
Replace spinner with skeleton that matches content shape. Perceived performance matters.
### **Applies To**
  - *.tsx
  - *.jsx

## Hardcoded Color Values

### **Id**
tc-hardcoded-color
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - #[0-9A-Fa-f]{3,8}(?![^{]*var\()
  - rgb\([^)]+\)(?![^{]*var\()
  - hsl\([^)]+\)(?![^{]*var\()
### **Message**
Hardcoded colors detected. Craft means systematic design tokens, not ad-hoc values.
### **Fix Action**
Use design tokens: #3B82F6 → var(--color-primary) or theme.colors.primary
### **Applies To**
  - *.css
  - *.scss
  - *.tsx
  - *.jsx

## Animation Without Reduced Motion Check

### **Id**
tc-animation-no-reduced-motion
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - animation:|transition:
  - @keyframes
### **Message**
Animation without reduced motion consideration. Some users get motion sick.
### **Fix Action**
Add @media (prefers-reduced-motion: reduce) check to disable or simplify animations
### **Applies To**
  - *.css
  - *.scss

## Button Without Disabled State

### **Id**
tc-button-no-disabled-style
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <button(?!.*disabled)
  - Button(?!.*disabled)
### **Message**
Button without disabled state handling. Users need feedback when actions are unavailable.
### **Fix Action**
Add disabled prop with visual indication: lower opacity, no hover effect, cursor: not-allowed
### **Applies To**
  - *.tsx
  - *.jsx

## Form Without Validation Feedback

### **Id**
tc-form-no-validation-feedback
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <form|<input|<textarea
### **Message**
Form elements detected. Craft means clear validation feedback before, during, and after submit.
### **Fix Action**
Add inline validation, clear error messages, and success confirmation
### **Applies To**
  - *.tsx
  - *.jsx

## Inconsistent Spacing Values

### **Id**
tc-inconsistent-spacing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - margin:\s*(?:3|5|7|9|11|13|15|17|19|21|23)px
  - padding:\s*(?:3|5|7|9|11|13|15|17|19|21|23)px
### **Message**
Non-standard spacing values. Craft means systematic spacing scale (4, 8, 12, 16, 24, 32...).
### **Fix Action**
Use spacing scale: 5px → 4px or 8px. Consistency creates visual harmony.
### **Applies To**
  - *.css
  - *.scss
  - *.tsx
  - *.jsx