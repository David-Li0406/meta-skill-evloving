# Ui Design - Validations

## Inconsistent Spacing Scale

### **Id**
inconsistent-spacing-scale
### **Severity**
warning
### **Type**
regex
### **Pattern**
(margin|padding|gap):\s*(3px|5px|7px|9px|11px|13px|15px|17px|19px)|(margin|padding|gap):\s*["']?(3|5|7|9|11|13|15|17|19)px["']?
### **Message**
Using spacing values outside standard 4px/8px scale.
### **Fix Action**
Use consistent spacing scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64px
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
  - *.scss

## Missing Dark Mode Support

### **Id**
no-dark-mode-support
### **Severity**
warning
### **Type**
regex
### **Pattern**
bg-white|bg-black(?!.*dark:)|backgroundColor:\s*["']#(fff|000)["']
### **Message**
Hardcoded light/dark colors without dark mode variants.
### **Fix Action**
Use semantic color tokens that support dark mode (e.g., bg-background, dark:bg-gray-900)
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css

## Potential Color Contrast Issue

### **Id**
poor-color-contrast
### **Severity**
error
### **Type**
regex
### **Pattern**
text-gray-400 bg-white|text-yellow-300|color:\s*#ccc
### **Message**
Color combination may fail WCAG contrast requirements.
### **Fix Action**
Ensure text has 4.5:1 contrast ratio (3:1 for large text). Use contrast checker.
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css

## Missing Interactive Hover States

### **Id**
missing-hover-states
### **Severity**
warning
### **Type**
regex
### **Pattern**
<button(?!.*hover:)|<a[^>]+href(?!.*hover:)
### **Message**
Interactive element missing hover state styling.
### **Fix Action**
Add hover states to all clickable elements (e.g., hover:bg-gray-100)
### **Applies To**
  - *.tsx
  - *.jsx

## Touch Target Too Small

### **Id**
tiny-touch-targets
### **Severity**
error
### **Type**
regex
### **Pattern**
<button[^>]+className=["'][^"']*text-xs[^"']*p-1|<button[^>]+className=["'][^"']*w-6[^"']*h-6
### **Message**
Touch target smaller than 44x44px minimum (WCAG 2.5.5).
### **Fix Action**
Ensure interactive elements are at least 44x44px for mobile accessibility
### **Applies To**
  - *.tsx
  - *.jsx

## Inconsistent Button Sizing

### **Id**
inconsistent-button-height
### **Severity**
warning
### **Type**
regex
### **Pattern**
<button[^>]+style={{[^}]*height:|<button[^>]+className=["'][^"']*h-\[
### **Message**
Custom button heights detected. Use standardized button sizes.
### **Fix Action**
Use button size variants (sm, md, lg) from design system
### **Applies To**
  - *.tsx
  - *.jsx

## No Loading Skeleton

### **Id**
missing-loading-skeleton
### **Severity**
warning
### **Type**
regex
### **Pattern**
isLoading.*<div>Loading\.\.\.</div>|loading.*<p>Loading
### **Message**
Basic loading text instead of skeleton UI.
### **Fix Action**
Replace with skeleton components matching content layout
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Disabled State Styling

### **Id**
no-disabled-state-styling
### **Severity**
warning
### **Type**
regex
### **Pattern**
<button[^>]+disabled(?!.*disabled:)|<input[^>]+disabled(?!.*disabled:)
### **Message**
Disabled elements missing visual disabled state.
### **Fix Action**
Add disabled state styling (e.g., disabled:opacity-50 disabled:cursor-not-allowed)
### **Applies To**
  - *.tsx
  - *.jsx

## Inconsistent Icon Sizing

### **Id**
inconsistent-icon-sizes
### **Severity**
info
### **Type**
regex
### **Pattern**
<Icon[^>]+size={?(13|15|17|19|21|23|25)}|className=["'][^"']*w-\[15px\]
### **Message**
Icon sizes outside standard scale (16, 20, 24, 32, 40).
### **Fix Action**
Use consistent icon sizes from design system
### **Applies To**
  - *.tsx
  - *.jsx

## No Visual Hierarchy

### **Id**
poor-visual-hierarchy
### **Severity**
warning
### **Type**
regex
### **Pattern**
<h1[^>]*className=["'][^"']*text-base|<p[^>]*className=["'][^"']*text-4xl
### **Message**
Text sizing doesn't follow logical hierarchy.
### **Fix Action**
Use type scale: h1 (text-4xl), h2 (text-3xl), h3 (text-2xl), body (text-base)
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Keyboard Focus Indicators

### **Id**
missing-focus-visible
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <(button|a|input|select|textarea)(?!.*focus:)
### **Message**
Interactive element missing keyboard focus indicator.
### **Fix Action**
Add focus styles (e.g., focus:ring-2 focus:ring-offset-2 focus:outline-none)
### **Applies To**
  - *.tsx
  - *.jsx

## Text Selection Disabled

### **Id**
text-not-selectable
### **Severity**
warning
### **Type**
regex
### **Pattern**
user-select:\s*none|userSelect:\s*["']none["']
### **Message**
Text selection disabled unnecessarily.
### **Fix Action**
Only disable text selection on UI controls, not content text
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css