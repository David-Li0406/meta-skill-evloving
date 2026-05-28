# Sections

## 1. Security / RLS (rls)

**Impact:** CRITICAL
**Description:** Row Level Security policies, auth.uid() patterns. RLS is the foundation of Supabase security - incorrectly configured policies expose data.

## 2. Database Design (schema)

**Impact:** CRITICAL
**Description:** Foreign keys, constraints, migrations. Good schema design ensures data integrity and query performance.

## 3. Authentication (auth)

**Impact:** HIGH
**Description:** OAuth providers, MFA, session management. Secure authentication protects user accounts and data.

## 4. Real-time (realtime)

**Impact:** HIGH
**Description:** Subscriptions, presence, broadcast. Real-time features require careful management of connections and state.

## 5. Edge Functions (edge)

**Impact:** MEDIUM-HIGH
**Description:** Deno deploy, secrets, error handling. Edge Functions provide serverless compute for custom logic.

## 6. Storage (storage)

**Impact:** MEDIUM
**Description:** Bucket policies, transformations, signed URLs. Secure file storage requires proper access controls.

## 7. Performance (perf)

**Impact:** MEDIUM
**Description:** Connection pooling, indexes, query optimization. Performance tuning for Supabase applications.

## 8. Client Libraries (client)

**Impact:** LOW-MEDIUM
**Description:** Type generation, hooks, error handling. Best practices for using Supabase client libraries.
