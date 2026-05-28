# Vercel Deployment - Validations

## Secret in NEXT_PUBLIC Variable

### **Id**
vercel-secret-public
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - NEXT_PUBLIC_.*SECRET
  - NEXT_PUBLIC_.*PRIVATE
  - NEXT_PUBLIC_.*SERVICE_ROLE
  - NEXT_PUBLIC_.*DATABASE_URL
  - NEXT_PUBLIC_.*PASSWORD
### **Message**
Secret exposed via NEXT_PUBLIC_ prefix. This will be visible in browser.
### **Fix Action**
Remove NEXT_PUBLIC_ prefix and access only in server-side code
### **Applies To**
  - .env*
  - *.ts
  - *.tsx

## Hardcoded Vercel URL

### **Id**
vercel-hardcoded-url
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - https://[a-z0-9-]+\.vercel\.app
  - https://[a-z0-9-]+-[a-z0-9]+\.vercel\.app
### **Message**
Hardcoded Vercel URL. Use VERCEL_URL environment variable instead.
### **Fix Action**
Use process.env.VERCEL_URL or NEXT_PUBLIC_VERCEL_URL
### **Applies To**
  - *.ts
  - *.tsx
  - *.js

## Node.js API in Edge Runtime

### **Id**
vercel-node-in-edge
### **Severity**
error
### **Type**
regex
### **Pattern**
  - runtime.*['"]edge['"][\s\S]*?import.*from\s*['"]fs['"]
  - runtime.*['"]edge['"][\s\S]*?import.*from\s*['"]path['"]
  - runtime.*['"]edge['"][\s\S]*?require\(['"]fs['"]\)
### **Message**
Node.js module used in Edge runtime. fs/path not available in Edge.
### **Fix Action**
Use runtime = 'nodejs' or remove Node.js dependencies
### **Applies To**
  - app/api/**/*.ts
  - middleware.ts

## API Route Without CORS Headers

### **Id**
vercel-missing-cors
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - export async function (GET|POST|PUT|DELETE)(?![\s\S]*Access-Control-Allow)
### **Message**
API route without CORS headers may fail cross-origin requests.
### **Fix Action**
Add Access-Control-Allow-Origin header if API is called from other domains
### **Applies To**
  - app/api/**/*.ts
  - pages/api/**/*.ts

## API Route Without Error Handling

### **Id**
vercel-no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - export async function (GET|POST)(?![\s\S]*try[\s\S]*catch)
### **Message**
API route without try/catch. Unhandled errors return 500 without details.
### **Fix Action**
Wrap in try/catch and return appropriate error responses
### **Applies To**
  - app/api/**/*.ts

## Secret Read in Static Context

### **Id**
vercel-static-secret-read
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - generateStaticParams[\s\S]*process\.env\.(?!NEXT_PUBLIC)
  - generateMetadata[\s\S]*process\.env\.(?!NEXT_PUBLIC)
### **Message**
Server secret accessed in static generation. Value baked into build.
### **Fix Action**
Move secret access to runtime code or use NEXT_PUBLIC_ for public values
### **Applies To**
  - app/**/page.tsx
  - app/**/layout.tsx

## Large Package Import

### **Id**
vercel-large-import
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - import.*from\s*['"]lodash['"]
  - import.*from\s*['"]moment['"]
  - import.*from\s*['"]aws-sdk['"]
### **Message**
Large package imported. May cause slow cold starts. Consider alternatives.
### **Fix Action**
Use lodash-es with tree shaking, date-fns instead of moment, @aws-sdk/client-* instead of aws-sdk
### **Applies To**
  - *.ts
  - *.tsx

## Dynamic Page Without Revalidation Config

### **Id**
vercel-missing-revalidate
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - export const dynamic\s*=\s*['"]force-dynamic['"](?![\s\S]*revalidate)
### **Message**
Dynamic page without revalidation config. Consider setting revalidation strategy.
### **Fix Action**
Add export const revalidate = 60 for ISR, or 0 for no cache
### **Applies To**
  - app/**/page.tsx