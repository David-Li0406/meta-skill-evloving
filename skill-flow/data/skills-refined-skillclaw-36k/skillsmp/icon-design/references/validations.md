# Icon Design - Validations

## Hardcoded Fill Color in SVG

### **Id**
hardcoded-svg-fill-color
### **Severity**
error
### **Type**
regex
### **Pattern**
fill="(#[0-9a-fA-F]{3,6}|rgb\(|rgba\(|black|white|gray|grey|red|blue|green)
### **Message**
Hardcoded fill color prevents theme/dark mode support.
### **Fix Action**
Use fill='currentColor' to inherit color from CSS, or use CSS custom properties.
### **Applies To**
  - *.svg
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - fill="#000000"
    - fill="#fff"
    - fill="rgb(0, 0, 0)"
    - fill="black"
    - fill="#333333"
  #### **Should Not Match**
    - fill="currentColor"
    - fill="none"
    - fill={color}
    - fill='var(--icon-color)'

## Hardcoded Stroke Color in SVG

### **Id**
hardcoded-svg-stroke-color
### **Severity**
error
### **Type**
regex
### **Pattern**
stroke="(#[0-9a-fA-F]{3,6}|rgb\(|rgba\(|black|white|gray|grey|red|blue|green)
### **Message**
Hardcoded stroke color prevents theme/dark mode support.
### **Fix Action**
Use stroke='currentColor' to inherit color from CSS.
### **Applies To**
  - *.svg
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - stroke="#000"
    - stroke="#1a1a1a"
    - stroke="rgb(51, 51, 51)"
    - stroke="black"
  #### **Should Not Match**
    - stroke="currentColor"
    - stroke="none"
    - stroke={strokeColor}

## SVG Missing viewBox Attribute

### **Id**
missing-viewbox
### **Severity**
error
### **Type**
regex
### **Pattern**
<svg(?![^>]*viewBox)[^>]*>
### **Message**
SVG missing viewBox attribute - required for proper scaling.
### **Fix Action**
Add viewBox attribute matching design dimensions (e.g., viewBox='0 0 24 24').
### **Applies To**
  - *.svg
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - <svg width="24" height="24">
    - <svg xmlns="http://www.w3.org/2000/svg">
    - <svg className="icon">
  #### **Should Not Match**
    - <svg viewBox="0 0 24 24">
    - <svg viewBox="0 0 16 16" fill="none">

## Non-Standard SVG viewBox Dimensions

### **Id**
non-standard-viewbox
### **Severity**
warning
### **Type**
regex
### **Pattern**
viewBox="0 0 (?!(16 16|20 20|24 24|32 32|48 48)")[0-9]+ [0-9]+"
### **Message**
Non-standard viewBox dimensions may cause inconsistent sizing.
### **Fix Action**
Use standard icon sizes: 16x16, 20x20, 24x24, 32x32, or 48x48.
### **Applies To**
  - *.svg
### **Test Cases**
  #### **Should Match**
    - viewBox="0 0 18 18"
    - viewBox="0 0 22 22"
    - viewBox="0 0 28 28"
  #### **Should Not Match**
    - viewBox="0 0 24 24"
    - viewBox="0 0 16 16"
    - viewBox="0 0 32 32"

## Hardcoded Width/Height on SVG

### **Id**
hardcoded-svg-dimensions
### **Severity**
warning
### **Type**
regex
### **Pattern**
<svg[^>]*(width="[0-9]+(px)?"|height="[0-9]+(px)?")[^>]*>
### **Message**
Hardcoded dimensions prevent flexible sizing via CSS.
### **Fix Action**
Remove width/height attributes; use viewBox only. Size via CSS.
### **Applies To**
  - *.svg
### **Test Cases**
  #### **Should Match**
    - <svg width="24" height="24" viewBox="0 0 24 24">
    - <svg height="16px" viewBox="0 0 16 16">
    - <svg width="32">
  #### **Should Not Match**
    - <svg viewBox="0 0 24 24">
    - <svg viewBox="0 0 24 24" fill="none">

## Unnecessary SVG Metadata

### **Id**
svg-metadata-bloat
### **Severity**
info
### **Type**
regex
### **Pattern**
<(metadata|defs>|desc>|title>(?!.*</title>)|sodipodi|inkscape)
### **Message**
SVG contains unnecessary metadata adding file size.
### **Fix Action**
Optimize SVG with SVGO or SVGOMG to remove metadata.
### **Applies To**
  - *.svg
### **Test Cases**
  #### **Should Match**
    - <metadata>Created with Illustrator</metadata>
    - <defs>
    - <sodipodi:namedview
    - <inkscape:version>
  #### **Should Not Match**
    - <path d="M0 0h24v24H0z"/>
    - <title id="icon-title">Settings</title>

## Excessive Path Coordinate Precision

### **Id**
excessive-path-precision
### **Severity**
info
### **Type**
regex
### **Pattern**
d="[^"]*\d+\.\d{4,}
### **Message**
Path coordinates have excessive decimal precision.
### **Fix Action**
Optimize with SVGO - 2 decimal places is sufficient for icons.
### **Applies To**
  - *.svg
### **Test Cases**
  #### **Should Match**
    - d="M12.345678 0L24.12345678 12"
    - d="M3.14159265359 12"
  #### **Should Not Match**
    - d="M12.35 0L24.12 12"
    - d="M3 12h18"
    - d="M12 3L22 12L12 21"

## Non-Standard Stroke Width

### **Id**
inconsistent-stroke-width
### **Severity**
warning
### **Type**
regex
### **Pattern**
stroke-width="(?!1|1\.5|2|2\.5|3")[0-9.]+"
### **Message**
Stroke width outside standard scale (1, 1.5, 2, 2.5, 3).
### **Fix Action**
Use standard stroke widths for consistency across icon set.
### **Applies To**
  - *.svg
### **Test Cases**
  #### **Should Match**
    - stroke-width="1.2"
    - stroke-width="1.75"
    - stroke-width="0.5"
  #### **Should Not Match**
    - stroke-width="1"
    - stroke-width="1.5"
    - stroke-width="2"

## Decorative Icon Missing aria-hidden

### **Id**
icon-missing-aria-hidden
### **Severity**
warning
### **Type**
regex
### **Pattern**
<svg[^>]*className="[^"]*icon[^"]*"[^>]*>(?![^<]*aria-hidden)
### **Message**
Icon may need aria-hidden='true' if decorative.
### **Fix Action**
Add aria-hidden='true' for decorative icons, or aria-label for meaningful icons.
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - <svg className="icon">
    - <svg className="w-4 h-4 icon-sm">
  #### **Should Not Match**
    - <svg className="icon" aria-hidden="true">
    - <svg aria-hidden="true" className="icon">

## Icon Button Missing Accessible Label

### **Id**
icon-button-missing-label
### **Severity**
error
### **Type**
regex
### **Pattern**
<button[^>]*>[\s\n]*<(svg|Icon|[A-Z][a-z]+Icon)[^>]*/?>
### **Message**
Icon-only button missing accessible name.
### **Fix Action**
Add aria-label to button or include visually hidden text.
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - <button><svg viewBox="0 0 24 24"></svg>
    - <button className="btn">\n<TrashIcon />
    - <button><Icon name="close" /></button>
  #### **Should Not Match**
    - <button aria-label="Close"><XIcon /></button>
    - <button><SaveIcon /><span>Save</span></button>

## Icon Touch Target Too Small

### **Id**
tiny-icon-touch-target
### **Severity**
error
### **Type**
regex
### **Pattern**
<button[^>]*className="[^"]*\b(p-0|p-1|w-4|w-5|w-6|h-4|h-5|h-6)\b[^"]*"[^>]*>[\s\n]*<(svg|Icon|[A-Z][a-z]+Icon)
### **Message**
Icon button touch target smaller than 44x44px minimum.
### **Fix Action**
Ensure button is at least 44x44px for accessibility (p-2.5 with 24px icon).
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - <button className="p-1"><TrashIcon /></button>
    - <button className="w-6 h-6"><XIcon />
  #### **Should Not Match**
    - <button className="p-3"><TrashIcon /></button>
    - <button className="w-11 h-11"><XIcon />

## Icon Animation Without Reduced Motion Support

### **Id**
animation-missing-reduced-motion
### **Severity**
error
### **Type**
regex
### **Pattern**
(animate-spin|animate-bounce|animate-pulse)(?![^}]*prefers-reduced-motion)
### **Message**
Animated icon class without reduced motion consideration.
### **Fix Action**
Add @media (prefers-reduced-motion: reduce) override or use motion-safe: prefix.
### **Applies To**
  - *.tsx
  - *.jsx
  - *.css
### **Test Cases**
  #### **Should Match**
    - className="animate-spin"
    - animate-bounce
    - class="animate-pulse"
  #### **Should Not Match**
    - className="motion-safe:animate-spin"
    - motion-reduce:animate-none

## Inline Style on SVG Elements

### **Id**
inline-svg-style
### **Severity**
warning
### **Type**
regex
### **Pattern**
<(svg|path|circle|rect|line|polygon)[^>]*style="[^"]*"
### **Message**
Inline styles on SVG elements - prefer classes or attributes.
### **Fix Action**
Move styles to CSS classes or use SVG attributes directly.
### **Applies To**
  - *.svg
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - <path style="fill: red">
    - <svg style="width: 24px">
    - <circle style="stroke-width: 2px">
  #### **Should Not Match**
    - <path fill="currentColor">
    - <svg className="icon">

## Mixed Filled and Outline Icons in Same Context

### **Id**
mixed-icon-styles
### **Severity**
info
### **Type**
regex
### **Pattern**
(Outline|Solid|Filled|Fill)[A-Z][a-z]+Icon[^}]*\s+(Outline|Solid|Filled|Fill)[A-Z][a-z]+Icon
### **Message**
Mixing icon styles (outline/filled) in same component.
### **Fix Action**
Use consistent icon style within a component or icon group.
### **Applies To**
  - *.tsx
  - *.jsx
### **Test Cases**
  #### **Should Match**
    - OutlineHomeIcon /> <SolidUserIcon />
    - <FilledIcon />\n<OutlineIcon />
  #### **Should Not Match**
    - OutlineHomeIcon /> <OutlineUserIcon />
    - <SolidTrashIcon /> <SolidEditIcon />