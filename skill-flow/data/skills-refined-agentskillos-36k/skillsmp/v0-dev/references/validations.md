# V0 Dev - Validations

## Hardcoded UI Strings

### **Id**
hardcoded-strings
### **Severity**
low
### **Type**
regex
### **Pattern**
>\s*[A-Z][a-z]+\s+(Plan|Package|Tier|Feature)
### **Message**
Hardcoded strings should be converted to props for reusability.
### **Fix Action**
Extract to component props or constants
### **Applies To**
  - *.tsx
  - *.jsx

## Input Without Label

### **Id**
missing-input-labels
### **Severity**
high
### **Type**
regex
### **Pattern**
<Input[^>]*placeholder=[^>]*/>
### **Negative Pattern**
htmlFor|Label|aria-label
### **Message**
Input fields should have associated labels for accessibility.
### **Fix Action**
Add Label component with htmlFor matching input id
### **Applies To**
  - *.tsx
  - *.jsx

## Icon Button Without aria-label

### **Id**
icon-button-no-label
### **Severity**
high
### **Type**
regex
### **Pattern**
<Button[^>]*>\s*<\w+Icon
### **Negative Pattern**
aria-label
### **Message**
Icon-only buttons need aria-label for screen readers.
### **Fix Action**
Add aria-label describing the button action
### **Applies To**
  - *.tsx
  - *.jsx

## Hardcoded Color Values

### **Id**
hardcoded-colors
### **Severity**
medium
### **Type**
regex
### **Pattern**
bg-(white|black|gray-\d00)\s
### **Negative Pattern**
dark:
### **Message**
Hardcoded colors break dark mode. Use CSS variable colors.
### **Fix Action**
Replace with bg-background, bg-foreground, etc.
### **Applies To**
  - *.tsx
  - *.jsx

## Component Without TypeScript Props

### **Id**
no-typescript-props
### **Severity**
medium
### **Type**
regex
### **Pattern**
function \w+\(\)\s*\{
### **Message**
Component should accept typed props for reusability.
### **Fix Action**
Add interface and props parameter
### **Applies To**
  - *.tsx

## List Without Key Prop

### **Id**
missing-key-prop
### **Severity**
high
### **Type**
regex
### **Pattern**
\.map\([^)]*\)\s*=>\s*\([^k]*<
### **Negative Pattern**
key=
### **Message**
List items must have unique key prop.
### **Fix Action**
Add key={item.id} or key={index} to mapped elements
### **Applies To**
  - *.tsx
  - *.jsx

## Clickable Div Without Semantics

### **Id**
clickable-div
### **Severity**
medium
### **Type**
regex
### **Pattern**
<div[^>]*onClick
### **Negative Pattern**
role=|tabIndex|onKeyDown
### **Message**
Clickable divs need button role and keyboard handlers.
### **Fix Action**
Use <button> or add role='button', tabIndex, onKeyDown
### **Applies To**
  - *.tsx
  - *.jsx

## Image Without Alt Text

### **Id**
image-no-alt
### **Severity**
high
### **Type**
regex
### **Pattern**
<img[^>]*src=
### **Negative Pattern**
alt=
### **Message**
Images must have alt text for accessibility.
### **Fix Action**
Add descriptive alt text or alt='' for decorative images
### **Applies To**
  - *.tsx
  - *.jsx