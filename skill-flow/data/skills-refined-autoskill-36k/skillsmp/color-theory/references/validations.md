# Color Theory - Validations

## Hardcoded Hex Colors

### **Id**
hardcoded-hex-colors
### **Severity**
warning
### **Type**
regex
### **Pattern**
(?:color|background|border-color|fill|stroke):\s*#[0-9a-fA-F]{3,8}(?!.*var\()
### **Message**
Hardcoded hex color detected. Use color tokens for maintainability.
### **Fix Action**
Replace with CSS variable (e.g., var(--color-primary)) or Tailwind class
### **Applies To**
  - *.css
  - *.scss
  - *.less
### **Test Cases**
  #### **Should Match**
    - color: #FF0000;
    - background: #fff;
    - border-color: #2563EB;
  #### **Should Not Match**
    - color: var(--text-primary);
    - /* #FF0000 is the brand color */

## Hardcoded RGB Colors

### **Id**
hardcoded-rgb-colors
### **Severity**
warning
### **Type**
regex
### **Pattern**
(?:color|background|border-color):\s*rgba?\([^)]+\)(?!.*var\()
### **Message**
Hardcoded RGB/RGBA color detected. Use color tokens.
### **Fix Action**
Replace with CSS variable that contains the color value
### **Applies To**
  - *.css
  - *.scss
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - color: rgb(255, 0, 0);
    - background: rgba(0, 0, 0, 0.5);
  #### **Should Not Match**
    - background: var(--overlay-bg);

## Inline Style Color Values

### **Id**
inline-style-colors
### **Severity**
warning
### **Type**
regex
### **Pattern**
style=\{?\{[^}]*(?:color|background|backgroundColor|borderColor):\s*["']#[0-9a-fA-F]+
### **Message**
Inline style with hardcoded color. Use className with tokens.
### **Fix Action**
Move color to CSS class or use Tailwind utility with design token
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - style={{ color: '#FF0000' }}
    - style={{ backgroundColor: '#2563EB' }}
  #### **Should Not Match**
    - style={{ color: 'var(--primary)' }}
    - className="text-primary"

## Potential Low Contrast Gray Text

### **Id**
low-contrast-gray-text
### **Severity**
error
### **Type**
regex
### **Pattern**
text-gray-[345]00(?:\s|"|$)|color:\s*#[9-b][9-b][9-b]
### **Message**
Light gray text may fail WCAG contrast requirements on white backgrounds.
### **Fix Action**
Use text-gray-600 or darker (5.0:1+ contrast on white)
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
### **Test Cases**
  #### **Should Match**
    - className="text-gray-400"
    - text-gray-300 bg-white
    - color: #999999;
  #### **Should Not Match**
    - text-gray-600
    - text-gray-700
    - color: #374151;

## Missing Dark Mode Color Variant

### **Id**
missing-dark-mode-variant
### **Severity**
warning
### **Type**
regex
### **Pattern**
(?:bg-white|bg-black|bg-gray-[0-9]{2,3})(?![^"]*dark:)
### **Message**
Background color without dark mode variant.
### **Fix Action**
Add dark: variant (e.g., bg-white dark:bg-gray-900)
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - className="bg-white"
    - className="bg-gray-100"
  #### **Should Not Match**
    - className="bg-white dark:bg-gray-900"
    - className="bg-gray-100 dark:bg-gray-800"

## Color-Only Error Indicator

### **Id**
color-only-error-state
### **Severity**
error
### **Type**
regex
### **Pattern**
(?:border|ring)-red-[0-9]+(?![^"]*(?:icon|Icon|error|Error|message|Message|text-))
### **Message**
Error indicated by color only. Add icon or text for accessibility.
### **Fix Action**
Pair red border with error icon and/or error message text
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - className="border-red-500"
    - ring-red-400
  #### **Should Not Match**
    - border-red-500 flex"><ErrorIcon
    - border-red-500"><span className="text-red

## OKLCH Without Fallback

### **Id**
oklch-without-fallback
### **Severity**
warning
### **Type**
regex
### **Pattern**
^\s*(?:color|background|border-color):\s*oklch\([^)]+\);?\s*$
### **Message**
OKLCH color without fallback for older browsers.
### **Fix Action**
Add hex or rgb fallback before OKLCH declaration
### **Applies To**
  - *.css
  - *.scss
### **Test Cases**
  #### **Should Match**
    - color: oklch(50% 0.2 240);
    - background: oklch(95% 0.05 150);
  #### **Should Not Match**
    -       color: #2563EB;
      color: oklch(55% 0.25 240);
      

## Removed Focus Outline

### **Id**
removed-focus-outline
### **Severity**
critical
### **Type**
regex
### **Pattern**
outline:\s*(?:none|0)(?![^}]*outline:\s*[^none0])|outline-width:\s*0
### **Message**
Focus outline removed. Keyboard users cannot see focus.
### **Fix Action**
Add focus-visible styles with visible indicator (2px+ solid color)
### **Applies To**
  - *.css
  - *.scss
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - outline: none;
    - outline: 0;
    - outline-width: 0;
  #### **Should Not Match**
    -       outline: none;
      outline: 2px solid blue;
      

## Pure Black or White Colors

### **Id**
pure-black-white-colors
### **Severity**
info
### **Type**
regex
### **Pattern**
(?:bg|text|border)-(?:black|white)(?!\s*dark:)|#(?:000000|FFFFFF|fff|000)(?:\s|;|"|$)
### **Message**
Pure black/white creates harsh contrast (21:1). Consider softer alternatives.
### **Fix Action**
Use near-black (#1A1A1A) or off-white (#FAFAFA) for gentler contrast
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
### **Test Cases**
  #### **Should Match**
    - bg-black
    - text-white
    - color: #000000;
    - background: #FFFFFF;
  #### **Should Not Match**
    - bg-gray-900
    - text-gray-50
    - bg-black dark:bg-white

## High Saturation in Dark Mode

### **Id**
saturated-dark-mode-colors
### **Severity**
warning
### **Type**
regex
### **Pattern**
dark:(?:bg|text|border)-(?:red|green|blue|yellow|purple|pink|orange)-[5-9]00
### **Message**
Highly saturated color in dark mode may cause eye strain.
### **Fix Action**
Use lighter, less saturated variant for dark mode (e.g., dark:text-blue-400)
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - dark:bg-blue-600
    - dark:text-red-500
    - dark:border-green-700
  #### **Should Not Match**
    - dark:bg-blue-400
    - dark:text-red-300

## Red/Green Color Combination

### **Id**
red-green-combination
### **Severity**
warning
### **Type**
regex
### **Pattern**
(?:bg|text|border)-red-[0-9]+[^"]*(?:bg|text|border)-green-|(?:bg|text|border)-green-[0-9]+[^"]*(?:bg|text|border)-red-
### **Message**
Red and green combination problematic for color blind users (8% of men).
### **Fix Action**
Use blue/orange or add non-color indicators (icons, patterns)
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - className="bg-red-500 text-green-500"
    - border-green-400 bg-red-100
  #### **Should Not Match**
    - bg-red-500 text-white
    - bg-green-500

## Magic Color Values

### **Id**
magic-color-numbers
### **Severity**
warning
### **Type**
regex
### **Pattern**
bg-\[[^\]]*(?:#|rgb|hsl|oklch)[^\]]+\]|text-\[[^\]]*(?:#|rgb)[^\]]+\]
### **Message**
Arbitrary color value. Define as design token for consistency.
### **Fix Action**
Add to Tailwind config as named color or use CSS variable
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - bg-[#FF5733]
    - text-[rgb(255,87,51)]
  #### **Should Not Match**
    - bg-primary
    - bg-blue-500

## Opacity Color Hack

### **Id**
opacity-color-hack
### **Severity**
info
### **Type**
regex
### **Pattern**
(?:bg|text|border)-[a-z]+-[0-9]+/[0-9]+
### **Message**
Using opacity modifier. Ensure adequate contrast is maintained.
### **Fix Action**
Verify contrast ratio of resulting color combination
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - bg-blue-500/50
    - text-gray-900/75
  #### **Should Not Match**
    - bg-blue-500
    - opacity-50

## Missing Semantic Color Usage

### **Id**
missing-semantic-color
### **Severity**
info
### **Type**
regex
### **Pattern**
(?:success|error|warning|danger|info).*(?:bg|text|border)-(?:green|red|yellow|blue)-[0-9]+
### **Message**
Consider using semantic color token instead of direct color.
### **Fix Action**
Use semantic tokens: color-success, color-danger, color-warning, color-info
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - isError && "text-red-500"
    - success ? "bg-green-100"
  #### **Should Not Match**
    - text-success
    - bg-danger