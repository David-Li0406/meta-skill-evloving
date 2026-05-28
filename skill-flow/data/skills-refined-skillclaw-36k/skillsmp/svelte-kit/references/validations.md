# Svelte Kit - Validations

## Browser API used without environment check

### **Id**
browser-api-without-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?<!if\s*\(browser\)\s*)(?<!browser\s*&&\s*)localStorage\.
  - (?<!if\s*\(browser\)\s*)(?<!browser\s*&&\s*)sessionStorage\.
  - (?<!if\s*\(browser\)\s*)(?<!browser\s*&&\s*)window\.
### **Message**
Browser APIs will crash during SSR - check browser environment first
### **Fix Action**
Wrap in 'if (browser)' or use onMount
### **Applies To**
  - *.svelte
  - +page.ts
  - +layout.ts

## #each block without key for stateful items

### **Id**
each-without-key
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \{#each\s+\w+\s+as\s+\w+\s*\}(?!\s*\()
### **Message**
List without key may cause update bugs - add (item.id) key
### **Fix Action**
Add key: {#each items as item (item.id)}
### **Applies To**
  - *.svelte

## Manual store subscription without unsubscribe

### **Id**
store-subscribe-no-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.subscribe\s*\([^)]+\)(?![\s\S]*onDestroy)
### **Message**
Manual subscription needs cleanup to prevent memory leak
### **Fix Action**
Use $ auto-subscription or call unsubscribe in onDestroy
### **Applies To**
  - *.svelte

## Returning redirect instead of throwing

### **Id**
return-redirect
### **Severity**
error
### **Type**
regex
### **Pattern**
  - return\s+redirect\s*\(
### **Message**
Redirects must be thrown, not returned
### **Fix Action**
Change 'return redirect()' to 'throw redirect()'
### **Applies To**
  - +page.server.ts
  - +page.server.js

## Returning error instead of throwing

### **Id**
return-error
### **Severity**
error
### **Type**
regex
### **Pattern**
  - return\s+error\s*\(\s*\d
### **Message**
Errors must be thrown, not returned
### **Fix Action**
Change 'return error()' to 'throw error()'
### **Applies To**
  - +page.server.ts
  - +page.server.js

## Sensitive operations in universal load

### **Id**
sensitive-in-universal-load
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - prisma\.
  - db\.
  - process\.env\.
### **Message**
Sensitive operations should be in +page.server.ts, not +page.ts
### **Fix Action**
Move to +page.server.ts for server-only execution
### **Applies To**
  - +page.ts
  - +layout.ts

## Svelte 4 reactive declaration ($:)"

### **Id**
svelte4-reactive-declaration
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^\s*\$:\s+\w+\s*=
### **Message**
Consider migrating to Svelte 5 $derived rune
### **Fix Action**
Replace '$: x = y' with 'let x = $derived(y)'
### **Applies To**
  - *.svelte

## Svelte 4 reactive statement ($:)"

### **Id**
svelte4-reactive-statement
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^\s*\$:\s+[^=]
### **Message**
Consider migrating to Svelte 5 $effect rune
### **Fix Action**
Replace '$: statement' with '$effect(() => { statement })'
### **Applies To**
  - *.svelte

## #await block without error handling

### **Id**
await-without-catch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \{#await[\s\S]+?\{:then[\s\S]+?\{/await\}(?!\s*\{:catch)
### **Message**
#await should handle errors with {:catch} block
### **Fix Action**
Add {:catch error} block to handle failures
### **Applies To**
  - *.svelte

## @html used without sanitization mention

### **Id**
html-without-sanitize
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \{@html\s
### **Message**
@html can be an XSS vector - ensure content is trusted/sanitized
### **Fix Action**
Sanitize HTML content before rendering
### **Applies To**
  - *.svelte

## Console.log statements

### **Id**
console-log-in-production
### **Severity**
info
### **Type**
regex
### **Pattern**
  - console\.log\s*\(
### **Message**
Remove console.log before production
### **Fix Action**
Remove or use proper logging
### **Applies To**
  - *.svelte
  - *.ts
  - *.js