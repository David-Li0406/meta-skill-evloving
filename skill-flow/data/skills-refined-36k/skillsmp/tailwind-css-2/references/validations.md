# Tailwind Css - Validations

## Dynamic class name construction

### **Id**
dynamic-class-names
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - className=\{`[^`]*\$\{[^}]+\}[^`]*`\}
  - class=`[^`]*\$\{[^}]+\}[^`]*`
### **Message**
Dynamic class names may be purged in production
### **Fix Action**
Use object mapping with complete class names
### **Applies To**
  - *.tsx
  - *.jsx
  - *.vue

## Large arbitrary z-index value

### **Id**
arbitrary-z-index
### **Severity**
info
### **Type**
regex
### **Pattern**
  - z-\[\d{3,}\]
### **Message**
Large z-index values indicate stacking context issues
### **Fix Action**
Define z-index scale in tailwind.config.js
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html
  - *.vue

## Arbitrary color values

### **Id**
arbitrary-colors
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (bg|text|border)-\[#[0-9a-fA-F]+\]
### **Message**
Arbitrary colors break design consistency
### **Fix Action**
Add colors to tailwind.config.js theme.extend.colors
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Background without dark mode variant

### **Id**
missing-dark-variant
### **Severity**
info
### **Type**
regex
### **Pattern**
  - bg-white(?![^"]*dark:)
  - bg-gray-50(?![^"]*dark:)
### **Message**
Consider adding dark mode variant for backgrounds
### **Fix Action**
Add dark:bg-gray-900 or similar
### **Applies To**
  - *.tsx
  - *.jsx

## Text color without dark variant

### **Id**
text-without-dark
### **Severity**
info
### **Type**
regex
### **Pattern**
  - text-gray-900(?![^"]*dark:)
  - text-black(?![^"]*dark:)
### **Message**
Consider adding dark mode variant for text
### **Fix Action**
Add dark:text-white or dark:text-gray-100
### **Applies To**
  - *.tsx
  - *.jsx

## Inline styles alongside Tailwind

### **Id**
inline-style
### **Severity**
info
### **Type**
regex
### **Pattern**
  - style=\{[^}]+\}.*className=
  - className=.*style=\{[^}]+\}
### **Message**
Prefer Tailwind utilities over inline styles
### **Fix Action**
Use Tailwind classes or extend config
### **Applies To**
  - *.tsx
  - *.jsx

## Potentially conflicting utility classes

### **Id**
conflicting-classes
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - p-\d+\s+p-\d+
  - m-\d+\s+m-\d+
  - w-\d+\s+w-\d+
### **Message**
Conflicting classes - only one will apply
### **Fix Action**
Use tailwind-merge for class composition
### **Applies To**
  - *.tsx
  - *.jsx
  - *.html

## Excessive @apply usage

### **Id**
apply-overuse
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @apply\s+\w+[\s\w-]+\w+[\s\w-]+\w+[\s\w-]+\w+
### **Message**
@apply with many classes defeats Tailwind's purpose
### **Fix Action**
Create React component instead of CSS class
### **Applies To**
  - *.css

## Potential contrast issue

### **Id**
text-color-contrast
### **Severity**
info
### **Type**
regex
### **Pattern**
  - bg-white.*text-gray-[1-3]00
  - bg-gray-100.*text-gray-[1-4]00
### **Message**
Text color may have insufficient contrast
### **Fix Action**
Use text-gray-700 or darker for readability
### **Applies To**
  - *.tsx
  - *.jsx

## Missing responsive variants

### **Id**
mobile-only-classes
### **Severity**
info
### **Type**
regex
### **Pattern**
  - hidden(?!\s+sm:|\s+md:|\s+lg:)
### **Message**
Consider if element should be visible on different screen sizes
### **Fix Action**
Use md:block or similar for responsive visibility
### **Applies To**
  - *.tsx
  - *.jsx