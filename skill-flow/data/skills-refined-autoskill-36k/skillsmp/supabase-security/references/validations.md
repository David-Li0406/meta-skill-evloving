# Supabase Security - Validations

## Service role key in client code

### **Id**
service-role-exposed
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - NEXT_PUBLIC.*SERVICE.*ROLE
  - NEXT_PUBLIC.*service.*role
  - process\.env\.NEXT_PUBLIC.*SERVICE
### **Message**
Service role key must never be exposed to client
### **Fix Action**
Remove NEXT_PUBLIC_ prefix, use only in server code
### **Applies To**
  - *.ts
  - *.tsx
  - *.js
  - .env*

## RLS explicitly disabled

### **Id**
rls-disabled
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - disable row level security
  - ALTER TABLE.*DISABLE.*RLS
### **Message**
RLS should never be disabled on production tables
### **Fix Action**
Enable RLS and create appropriate policies
### **Applies To**
  - *.sql

## Overly permissive RLS policy

### **Id**
permissive-policy
### **Severity**
high
### **Type**
regex
### **Pattern**
  - using\s*\(\s*true\s*\)
  - with check\s*\(\s*true\s*\)
### **Message**
Policies with (true) allow all access
### **Fix Action**
Add proper auth.uid() checks
### **Applies To**
  - *.sql

## Policy without auth.uid() check

### **Id**
missing-auth-uid
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - create policy(?!.*auth\.uid).*using
### **Message**
Consider adding auth.uid() check to policy
### **Fix Action**
Verify policy properly restricts access
### **Applies To**
  - *.sql

## Public storage bucket

### **Id**
public-bucket
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - public.*=.*true
  - public:\s*true
### **Message**
Public buckets expose all files
### **Fix Action**
Use private bucket with RLS policies
### **Applies To**
  - *.sql

## Hardcoded Supabase keys

### **Id**
anon-key-hardcoded
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - eyJ[A-Za-z0-9_-]{50,}
### **Message**
Do not hardcode Supabase keys
### **Fix Action**
Use environment variables
### **Applies To**
  - *.ts
  - *.tsx
  - *.js