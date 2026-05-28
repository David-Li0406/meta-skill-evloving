# Vue Nuxt - Validations

## Destructuring reactive without toRefs

### **Id**
reactive-destructure
### **Severity**
error
### **Type**
regex
### **Pattern**
  - const\s*\{[^}]+\}\s*=\s*reactive\(
  - const\s*\{[^}]+\}\s*=\s*use\w+Store\(\)(?!\s*\.)
### **Message**
Destructuring reactive loses reactivity - use toRefs() or storeToRefs()
### **Fix Action**
Wrap with toRefs(): const { foo } = toRefs(reactive({...}))
### **Applies To**
  - *.vue
  - *.ts

## Direct prop mutation

### **Id**
mutating-props
### **Severity**
error
### **Type**
regex
### **Pattern**
  - props\.\w+\s*=
  - props\.\w+\.push\(
  - props\.\w+\.splice\(
### **Message**
Props are read-only - emit an event for the parent to handle
### **Fix Action**
Use emit('update:propName', newValue) for v-model or custom events
### **Applies To**
  - *.vue

## Options API in Vue 3 project

### **Id**
options-api-in-vue3
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - export\s+default\s*\{[^}]*data\s*\(\s*\)
  - export\s+default\s*\{[^}]*methods\s*:
### **Message**
Options API detected - prefer Composition API with <script setup>
### **Fix Action**
Migrate to <script setup> with ref(), computed(), etc.
### **Applies To**
  - *.vue

## Watch on route param without immediate

### **Id**
watch-without-immediate
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - watch\s*\(\s*\(\)\s*=>\s*route\.(params|query)\.\w+[^{]*\{[^}]*\}\s*\)
### **Message**
Route param watch should have immediate: true for initial load
### **Fix Action**
Add { immediate: true } as third argument
### **Applies To**
  - *.vue

## v-if used with v-for on same element

### **Id**
v-if-with-v-for
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - v-for="[^"]*"\s+v-if=
  - v-if="[^"]*"\s+v-for=
### **Message**
v-if with v-for has implicit precedence - use computed or wrapper
### **Fix Action**
Filter in computed property or wrap with <template v-for>
### **Applies To**
  - *.vue

## v-for without :key

### **Id**
missing-key-in-v-for
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - v-for="[^"]*"(?!\s+:key=)
### **Message**
v-for without :key can cause rendering issues
### **Fix Action**
Add :key with unique identifier: v-for="item in items" :key="item.id"
### **Applies To**
  - *.vue

## Ref compared without .value

### **Id**
ref-value-comparison
### **Severity**
error
### **Type**
regex
### **Pattern**
  - if\s*\(\s*\w+\s*===?\s*(true|false|null|undefined|[0-9]+|"[^"]*"|'[^']*')\s*\)
### **Message**
Possible ref comparison without .value - refs need .value in script
### **Fix Action**
Use .value: if (myRef.value === true)
### **Applies To**
  - *.vue
  - *.ts

## Data fetching in onMounted instead of useFetch

### **Id**
nuxt-fetch-in-mounted
### **Severity**
info
### **Type**
regex
### **Pattern**
  - onMounted\s*\(\s*async\s*\(\s*\)\s*=>\s*\{[^}]*fetch\(
  - onMounted\s*\(\s*async\s*\(\s*\)\s*=>\s*\{[^}]*axios
### **Message**
Use useFetch() or useAsyncData() for SSR-compatible data fetching
### **Fix Action**
Replace with useFetch('/api/...') for automatic SSR handling
### **Applies To**
  - *.vue

## Direct window/document access

### **Id**
window-access-without-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?<!if\s*\()[^?]window\.
  - (?<!if\s*\()[^?]document\.
### **Message**
Direct browser API access fails on server - use ClientOnly or onMounted
### **Fix Action**
Wrap in onMounted() or <ClientOnly> component
### **Applies To**
  - *.vue

## Store accessed at module level

### **Id**
store-outside-setup
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^const\s+\w+\s*=\s*use\w+Store\(\)
  - ^let\s+\w+\s*=\s*use\w+Store\(\)
### **Message**
Store must be accessed inside setup() or Nuxt plugin context
### **Fix Action**
Move useStore() inside component setup or a function
### **Applies To**
  - *.ts

## Side effects in computed

### **Id**
computed-with-side-effects
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - computed\s*\(\s*\(\s*\)\s*=>\s*\{[^}]*(console\.|fetch\(|emit\()
### **Message**
Computed should be pure - no side effects
### **Fix Action**
Move side effects to watch() or methods
### **Applies To**
  - *.vue

## useFetch without await

### **Id**
unused-await-usefetch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?<!await\s+)useFetch\s*\(
  - (?<!await\s+)useAsyncData\s*\(
### **Message**
useFetch/useAsyncData should be awaited to prevent hydration issues
### **Fix Action**
Add await: const { data } = await useFetch(...)
### **Applies To**
  - *.vue