# Supabase Backend - Validations

## Service Role in Client Code

### **Id**
supabase-service-role-client
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - SUPABASE_SERVICE_ROLE
  - service_role_key
  - serviceRoleKey
### **Message**
Service role key detected. This MUST NOT be used in client-side code.
### **Fix Action**
Move to Server Action or API route, use anon key for client
### **Applies To**
  - *.tsx
  - *.jsx
  - *.ts
  - *.js
### **Exclude**
  - app/actions*.ts
  - app/api/**
  - lib/supabase-admin.ts

## Table Without RLS

### **Id**
supabase-missing-rls
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - create table[^;]+;(?![\\s\\S]{0,200}?enable row level security)
### **Message**
Table created without enabling RLS. All data is exposed.
### **Fix Action**
Add 'alter table X enable row level security;' immediately after
### **Applies To**
  - *.sql
  - migrations/*.sql

## Hardcoded Supabase Key

### **Id**
supabase-anon-key-hardcoded
### **Severity**
error
### **Type**
regex
### **Pattern**
  - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\\.[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+
  - sb-[a-z]+-[a-z]+\\.supabase\\.co
### **Message**
Hardcoded Supabase credentials. Use environment variables.
### **Fix Action**
Move to .env and use process.env.NEXT_PUBLIC_SUPABASE_*
### **Applies To**
  - *.tsx
  - *.jsx
  - *.ts
  - *.js

## Query Without Select

### **Id**
supabase-from-without-select
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\.from\\([^)]+\\)(?!\\.select)
### **Message**
Supabase query without .select(). Returns all columns unnecessarily.
### **Fix Action**
Add .select('column1, column2') to fetch only needed columns
### **Applies To**
  - *.tsx
  - *.ts

## Supabase Call Without Error Check

### **Id**
supabase-no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await supabase\\.[^}]+(?!error)
  - const\\s*{\\s*data\\s*}\\s*=\\s*await\\s*supabase
### **Message**
Supabase call without error handling. Always destructure { data, error }.
### **Fix Action**
Use const { data, error } = await supabase... and handle error
### **Applies To**
  - *.tsx
  - *.ts

## Realtime Subscription Without Cleanup

### **Id**
supabase-realtime-no-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\.subscribe\\(\\)(?![\\s\\S]{0,500}?removeChannel|unsubscribe)
### **Message**
Realtime subscription without cleanup. Memory leak risk.
### **Fix Action**
Add cleanup in useEffect return: supabase.removeChannel(channel)
### **Applies To**
  - *.tsx
  - *.jsx

## Public Bucket for User Data

### **Id**
supabase-public-bucket-sensitive
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - buckets.*?public.*?true.*?(?:user|avatar|document|private|upload)
  - createBucket.*?public.*?true
### **Message**
Consider if this bucket should be public. User data should be private.
### **Fix Action**
Set public: false and use RLS policies for access control
### **Applies To**
  - *.sql
  - *.ts

## Foreign Key Without Cascade

### **Id**
supabase-delete-no-cascade
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - references\\s+\\w+\\([^)]+\\)(?!\\s+on\\s+delete)
### **Message**
Foreign key without ON DELETE clause. Consider cascade behavior.
### **Fix Action**
Add 'on delete cascade' or 'on delete set null' as appropriate
### **Applies To**
  - *.sql
  - migrations/*.sql