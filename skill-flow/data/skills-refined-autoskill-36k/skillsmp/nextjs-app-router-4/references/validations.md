# Nextjs App Router - Validations

## Async Client Component

### **Id**
nextjs-async-client
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ["']use client["'][\s\S]{0,500}export\s+(?:default\s+)?async\s+function
  - ["']use client["'][\s\S]{0,500}async\s+function\s+\w+\s*\(
### **Message**
Client Components cannot be async. Move data fetching to a Server Component or use useEffect.
### **Fix Action**
Remove async from the component, fetch data in a parent Server Component
### **Applies To**
  - *.tsx
  - *.jsx

## Server Import in Client

### **Id**
nextjs-server-import-client
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ["']use client["'][\s\S]*?import[^;]*from\s*["'](?:fs|path|crypto|child_process)["']
  - ["']use client["'][\s\S]*?import[^;]*from\s*["']next/headers["']
  - ["']use client["'][\s\S]*?import[^;]*from\s*["']server-only["']
### **Message**
Server-only module imported in Client Component. This will fail at build/runtime.
### **Fix Action**
Move server imports to a Server Component or Server Action
### **Applies To**
  - *.tsx
  - *.jsx
  - *.ts
  - *.js

## Cookies in Client Component

### **Id**
nextjs-cookies-client
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ["']use client["'][\s\S]*?(?:cookies|headers)\s*\(\s*\)
### **Message**
cookies()/headers() can only be used in Server Components.
### **Fix Action**
Read cookies in a Server Component and pass as props, or use document.cookie
### **Applies To**
  - *.tsx
  - *.jsx

## Window Access Without Guard

### **Id**
nextjs-window-ssr
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?<!typeof\s)window\.\w+
  - (?<!typeof\s)document\.\w+
### **Message**
Browser API used without guard. May cause hydration mismatch.
### **Fix Action**
Wrap in useEffect or check typeof window !== 'undefined'
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Loading State

### **Id**
nextjs-missing-loading
### **Severity**
warning
### **Type**
file
### **Pattern**
loading.tsx
### **Message**
Consider adding loading.tsx for better UX during data fetching.
### **Fix Action**
Create loading.tsx with a skeleton or spinner
### **Applies To**
  - app/**/page.tsx

## Missing Error Boundary

### **Id**
nextjs-missing-error
### **Severity**
warning
### **Type**
file
### **Pattern**
error.tsx
### **Message**
Consider adding error.tsx to handle errors gracefully.
### **Fix Action**
Create error.tsx with 'use client' and error UI
### **Applies To**
  - app/**/page.tsx

## Excessive use client

### **Id**
nextjs-use-client-overuse
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ["']use client["'][\s\S]*?export\s+default\s+function\s+\w*Page
### **Message**
Page component marked as Client Component. Consider if Server Component would work.
### **Fix Action**
Extract only the interactive parts into Client Components
### **Applies To**
  - app/**/page.tsx

## Fetch Without Cache Config

### **Id**
nextjs-fetch-no-cache
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fetch\s*\([^)]+\)(?![^)]*(?:cache|revalidate|next))
### **Message**
fetch() without cache configuration. Consider adding cache or revalidate options.
### **Fix Action**
Add { cache: 'force-cache' } or { next: { revalidate: 60 } }
### **Applies To**
  - *.ts
  - *.tsx