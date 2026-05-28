# Frontend - Validations

## Hydration Mismatch Risk

### **Id**
frontend-hydration-hazard
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - return[^;]*Date\.now\(\)
  - return[^;]*Math\.random\(\)
  - (?<!typeof\s)window\.\w+(?![^}]*useEffect)
  - (?<!typeof\s)localStorage\.\w+(?![^}]*useEffect)
### **Message**
Using Date.now(), Math.random(), window, or localStorage in render causes hydration mismatch.
### **Fix Action**
Move to useEffect or guard with typeof window !== 'undefined'
### **Applies To**
  - *.tsx
  - *.jsx

## Data Fetching in useEffect

### **Id**
frontend-useeffect-fetch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - useEffect\s*\([^)]*\{[^}]*fetch\s*\(
  - useEffect\s*\([^)]*\{[^}]*axios\s*\.
### **Message**
Fetching data in useEffect can cause waterfalls, race conditions, and memory leaks.
### **Fix Action**
Use React Query, SWR, or framework data loaders instead
### **Applies To**
  - *.tsx
  - *.jsx

## Effect Without Cleanup

### **Id**
frontend-missing-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - useEffect\s*\([^)]*addEventListener[^)]*\)(?![^}]*removeEventListener)
  - useEffect\s*\([^)]*setInterval[^)]*\)(?![^}]*clearInterval)
  - useEffect\s*\([^)]*setTimeout[^)]*\)(?![^}]*clearTimeout)
### **Message**
Event listener, interval, or timeout without cleanup will cause memory leaks.
### **Fix Action**
Return a cleanup function: return () => removeEventListener/clearInterval/clearTimeout
### **Applies To**
  - *.tsx
  - *.jsx

## Non-semantic Interactive Element

### **Id**
frontend-div-onclick
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <div[^>]*onClick
  - <span[^>]*onClick
  - <div[^>]*onKeyDown
### **Message**
Using div/span with click handler is not accessible. Screen readers and keyboards won't work.
### **Fix Action**
Use <button> for clickable elements, or add role='button' tabIndex={0} and keyboard handlers
### **Applies To**
  - *.tsx
  - *.jsx

## Image Without Alt Text

### **Id**
frontend-img-no-alt
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <img[^>]*(?!alt)[^>]*/?>
### **Message**
Image without alt attribute is not accessible. Screen readers can't describe it.
### **Fix Action**
Add alt='description' for meaningful images, or alt='' role='presentation' for decorative
### **Applies To**
  - *.tsx
  - *.jsx

## Input Without Label

### **Id**
frontend-input-no-label
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <input[^>]*(?!id=|aria-label)[^>]*/?>
### **Message**
Input without associated label is not accessible.
### **Fix Action**
Wrap in <label> or add aria-label/aria-labelledby
### **Applies To**
  - *.tsx
  - *.jsx

## Barrel Import of Large Library

### **Id**
frontend-barrel-import
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - import\s+\w+\s+from\s+['"]lodash['"]
  - import\s+\{[^}]+\}\s+from\s+['"]lodash['"]
  - import\s+\w+\s+from\s+['"]moment['"]
  - import\s+\{[^}]+\}\s+from\s+['"]antd['"]
### **Message**
Importing from barrel file ships entire library. Use specific imports.
### **Fix Action**
Import from lodash/debounce instead of lodash. Use tree-shakeable alternatives.
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - *.jsx

## CSS !important Usage

### **Id**
frontend-important-css
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - !important
### **Message**
Using !important indicates specificity problems. Will be hard to override later.
### **Fix Action**
Fix the specificity issue at the source. Use CSS Modules, Tailwind, or flatten selectors.
### **Applies To**
  - *.css
  - *.scss

## Inline Style Object in JSX

### **Id**
frontend-inline-style-object
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - style=\{\s*\{[^}]+\}\s*\}
### **Message**
Inline style objects create new references every render, breaking memo optimization.
### **Fix Action**
Move style object outside component or use useMemo
### **Applies To**
  - *.tsx
  - *.jsx

## Array Index as React Key

### **Id**
frontend-index-as-key
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.map\s*\([^)]*,\s*\w*\s*\)[^}]*key=\{\s*\w+\s*\}
  - key=\{index\}
  - key=\{i\}
### **Message**
Using array index as key can cause bugs when items are reordered or filtered.
### **Fix Action**
Use unique, stable IDs from your data as keys
### **Applies To**
  - *.tsx
  - *.jsx

## Multiple Boolean States for Single Concept

### **Id**
frontend-boolean-state-soup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - useState\s*<\s*boolean\s*>\s*\([^)]*\)[^;]*useState\s*<\s*boolean\s*>\s*\([^)]*\)[^;]*useState
  - isLoading.*isError.*isSuccess
### **Message**
Multiple boolean flags for mutually exclusive states. Can have invalid combinations.
### **Fix Action**
Use discriminated union: type State = { status: 'idle' } | { status: 'loading' } | ...
### **Applies To**
  - *.tsx
  - *.ts

## Image Without Dimensions

### **Id**
frontend-img-no-dimensions
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <img[^>]*src=[^>]*(?!width|height|aspectRatio)[^>]*/>
### **Message**
Image without dimensions causes layout shift (CLS) when it loads.
### **Fix Action**
Add width and height attributes, or use aspectRatio style
### **Applies To**
  - *.tsx
  - *.jsx

## Using 100vh on Mobile

### **Id**
frontend-100vh
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - height:\s*100vh
  - min-height:\s*100vh
### **Message**
100vh includes mobile address bar, causing content to be cut off on iOS Safari.
### **Fix Action**
Use 100dvh (dynamic viewport height) or min-height: 100svh
### **Applies To**
  - *.css
  - *.scss
  - *.tsx
  - *.jsx