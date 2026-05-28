# Clerk Auth - Validations

## Clerk Secret Key in Client Code

### **Id**
secret-key-exposed
### **Severity**
error
### **Description**
CLERK_SECRET_KEY must only be used server-side
### **Pattern**
  (NEXT_PUBLIC|REACT_APP|VITE).*CLERK_SECRET
  
### **Message**
Clerk secret key exposed to client. Use CLERK_SECRET_KEY without NEXT_PUBLIC prefix.
### **Autofix**


## Protected Route Without Middleware

### **Id**
missing-middleware-protection
### **Severity**
error
### **Description**
API routes should have middleware protection
### **Pattern**
  app/api/(?!webhooks).*route\.ts
  
### **Anti Pattern**
  clerkMiddleware|auth\(\)
  
### **Message**
API route without auth check. Add middleware protection or auth() check.
### **Autofix**


## Hardcoded Clerk API Keys

### **Id**
hardcoded-clerk-keys
### **Severity**
error
### **Description**
Clerk keys should use environment variables
### **Pattern**
  (pk_test|pk_live|sk_test|sk_live)_[A-Za-z0-9]+
  
### **Message**
Hardcoded Clerk keys. Use environment variables.
### **Autofix**


## Missing Await on auth()

### **Id**
missing-await-auth
### **Severity**
error
### **Description**
auth() is async in App Router and must be awaited
### **Pattern**
  const.*=\s*auth\(\)(?!\s*await|\s*\.)
  
### **Message**
auth() not awaited. Use 'await auth()' in App Router.
### **Autofix**


## Multiple Middleware Files

### **Id**
multiple-middleware-files
### **Severity**
warning
### **Description**
Only one middleware.ts file should exist
### **Pattern**
  middleware.*\.ts.*middleware.*\.ts
  
### **Message**
Multiple middleware files detected. Use single middleware.ts.
### **Autofix**


## Webhook Route Not Excluded from Protection

### **Id**
webhook-not-public
### **Severity**
warning
### **Description**
Webhook routes should be public
### **Pattern**
  api/webhooks
  
### **Anti Pattern**
  isPublicRoute.*webhooks|webhooks.*isPublicRoute
  
### **Message**
Webhook route may be blocked by middleware. Add to public routes.
### **Autofix**


## Accessing Auth Without isLoaded Check

### **Id**
not-checking-isloaded
### **Severity**
warning
### **Description**
Check isLoaded before accessing user state in client components
### **Pattern**
  useUser\(\).*user\.(firstName|lastName|email)
  
### **Anti Pattern**
  isLoaded
  
### **Message**
Accessing user without isLoaded check. Check isLoaded first.
### **Autofix**


## Clerk Hooks in Server Component

### **Id**
hooks-in-server-component
### **Severity**
error
### **Description**
Clerk hooks only work in Client Components
### **Pattern**
  use(User|Auth|Session|Organization).*(?!['"]use client['"])
  
### **Message**
Clerk hooks in Server Component. Add 'use client' or use auth().
### **Autofix**


## Multi-Tenant Query Without orgId

### **Id**
missing-org-scope
### **Severity**
warning
### **Description**
Organization data should be scoped by orgId
### **Pattern**
  prisma\.(project|team|document)\.findMany
  
### **Anti Pattern**
  orgId|organizationId
  
### **Message**
Query without organization scope. Filter by orgId for multi-tenancy.
### **Autofix**


## Webhook Without Signature Verification

### **Id**
webhook-no-verification
### **Severity**
error
### **Description**
Clerk webhooks must verify svix signature
### **Pattern**
  webhooks/clerk.*POST
  
### **Anti Pattern**
  svix|Webhook.*verify
  
### **Message**
Webhook without signature verification. Use svix to verify.
### **Autofix**


## Webhook Using create Instead of upsert

### **Id**
webhook-race-condition
### **Severity**
warning
### **Description**
Webhooks can arrive out of order, use upsert
### **Pattern**
  user\.created.*prisma\..*\.create\(
  
### **Message**
Using create in webhook. Consider upsert for race conditions.
### **Autofix**
