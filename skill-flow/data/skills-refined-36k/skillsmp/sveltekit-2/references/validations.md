# Sveltekit - Validations

## No secrets in +page.ts

### **Id**
no-secrets-in-page-ts
### **Severity**
critical
### **Description**
API keys and secrets must not be in +page.ts files (exposed to client)
### **Pattern**
  #### **File Glob**
**/+page.ts
  #### **Match**
(API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE)\s*=
  #### **Exclude**
\$env/static/public
### **Message**
Secrets detected in +page.ts - this file is bundled and sent to client. Move to +page.server.ts
### **Autofix**


## Private env only in server files

### **Id**
private-env-in-server-only
### **Severity**
critical
### **Description**
$env/static/private must only be used in server-side files
### **Pattern**
  #### **File Glob**
**/*.{ts,js,svelte}
  #### **Match**
\$env/(static|dynamic)/private
  #### **Exclude**
(\+page\.server|\+layout\.server|\+server|hooks\.server)
### **Message**
Private environment variables used in client-accessible file
### **Autofix**


## Forms should use enhance

### **Id**
form-has-enhance
### **Severity**
high
### **Description**
Form actions without use:enhance cause full page reloads
### **Pattern**
  #### **File Glob**
**/*.svelte
  #### **Match**
method="POST"(?!.*use:enhance)
  #### **Context Lines**

### **Message**
Form with POST method should use use:enhance for SPA behavior
### **Autofix**
  #### **Find**
(<form[^>]*method="POST"[^>]*)>
  #### **Replace**
$1 use:enhance>
  #### **Import Needed**
import { enhance } from '$app/forms';

## No fetch in onMount

### **Id**
no-fetch-in-component
### **Severity**
high
### **Description**
Data fetching should happen in load functions, not components
### **Pattern**
  #### **File Glob**
**/*.svelte
  #### **Match**
onMount\s*\(\s*async.*fetch\(
  #### **Context Lines**

### **Message**
Move fetch to +page.ts or +page.server.ts load function for SSR support
### **Autofix**


## Prefer runes over stores in Svelte 5

### **Id**
use-runes-not-stores
### **Severity**
medium
### **Description**
Svelte 5 runes ($state, $derived) should be used instead of stores
### **Pattern**
  #### **File Glob**
**/*.svelte
  #### **Match**
import.*\{.*writable.*\}.*from.*'svelte/store'
### **Message**
Consider using $state rune instead of writable store in Svelte 5
### **Autofix**


## Use redirect() in load functions

### **Id**
redirect-not-goto-in-load
### **Severity**
high
### **Description**
goto() doesn't work properly in load functions, use redirect()
### **Pattern**
  #### **File Glob**
**/+page.{ts,server.ts}
  #### **Match**
goto\s*\(
### **Message**
Use 'throw redirect(303, '/path')' instead of goto() in load functions
### **Autofix**


## Use $props() in Svelte 5

### **Id**
svelte5-props-syntax
### **Severity**
medium
### **Description**
Svelte 5 uses $props() instead of export let for component props
### **Pattern**
  #### **File Glob**
**/*.svelte
  #### **Match**
export\s+let\s+\w+\s*[=;]
### **Message**
Use 'let { prop } = $props()' instead of 'export let prop' in Svelte 5
### **Autofix**


## Parallelize independent fetches

### **Id**
parallel-load-fetches
### **Severity**
medium
### **Description**
Sequential awaits in load functions should be parallelized
### **Pattern**
  #### **File Glob**
**/+page.{ts,server.ts}
  #### **Match**
await\s+fetch.*\n.*await\s+fetch
  #### **Context Lines**

### **Message**
Use Promise.all() for independent fetches to avoid waterfalls
### **Autofix**


## Check browser before using client APIs

### **Id**
browser-check-for-client-apis
### **Severity**
high
### **Description**
Client-only APIs (localStorage, window) cause SSR hydration mismatches
### **Pattern**
  #### **File Glob**
**/*.svelte
  #### **Match**
(localStorage|sessionStorage|window\.|document\.)(?!.*browser)
  #### **Exclude**
\$effect|onMount
### **Message**
Wrap browser-only APIs with 'if (browser)' check or use in onMount/$effect
### **Autofix**


## Adapter must be configured

### **Id**
adapter-configured
### **Severity**
high
### **Description**
SvelteKit requires an adapter for production builds
### **Pattern**
  #### **File Glob**
svelte.config.js
  #### **Match**
adapter-auto
### **Message**
Configure a specific adapter (adapter-node, adapter-vercel, etc.) for production
### **Autofix**


## Runes require .svelte or .svelte.ts files

### **Id**
runes-in-svelte-files
### **Severity**
high
### **Description**
$state, $derived, $effect only work in .svelte files or .svelte.ts files
### **Pattern**
  #### **File Glob**
**/*.ts
  #### **Match**
\$(state|derived|effect|props)\s*\(
  #### **Exclude**
\.svelte\.ts$
### **Message**
Runes only work in .svelte or .svelte.ts files. Rename to .svelte.ts or use different patterns
### **Autofix**


## Use depends() for invalidation

### **Id**
load-has-depends
### **Severity**
low
### **Description**
Load functions using invalidate() should declare dependencies
### **Pattern**
  #### **File Glob**
**/+page.{ts,server.ts}
  #### **Match**
invalidate\s*\(['"]
  #### **Exclude**
depends\s*\(
### **Message**
Add depends('key') to load function when using invalidate('key')
### **Autofix**
