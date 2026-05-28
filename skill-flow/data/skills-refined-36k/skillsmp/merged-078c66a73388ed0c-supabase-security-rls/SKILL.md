---
name: supabase-security-rls
description: Use this skill when securing Supabase applications with Row Level Security (RLS) policies, ensuring user isolation, and implementing multi-tenant patterns.
---

# Supabase Security with RLS

This skill provides comprehensive guidance on implementing Row Level Security (RLS) in Supabase applications, focusing on user isolation, multi-tenant patterns, and security best practices.

## Instructions

### 1. Applying RLS Policies

**Apply policies to tables:**
```bash
# Apply user isolation policies
bash scripts/apply-rls-policies.sh user-isolation <table_name>

# Apply multi-tenant policies
bash scripts/apply-rls-policies.sh multi-tenant <table_name>

# Apply AI-specific policies
bash scripts/apply-rls-policies.sh ai-chat <table_name>
```

**Generate custom policy:**
```bash
# Generate policy from template
bash scripts/generate-policy.sh user-isolation <table_name> <user_column>

# Generate with custom column
bash scripts/generate-policy.sh multi-tenant <table_name> <organization_column>
```

### 2. Testing RLS Enforcement

**Test policies work correctly:**
```bash
# Test all policies on a table
bash scripts/test-rls-policies.sh <table_name>

# Test specific user context
bash scripts/test-rls-policies.sh <table_name> --user-id "<user-id>"

# Test multi-tenant isolation
bash scripts/test-rls-policies.sh <table_name> --org-id "<org-id>"
```

### 3. Auditing Security

**Audit tables for missing RLS:**
```bash
# Audit all tables in public schema
bash scripts/audit-rls.sh

# Audit specific tables
bash scripts/audit-rls.sh <table_name_1> <table_name_2>

# Generate audit report
bash scripts/audit-rls.sh --report <report_file>
```

### 4. Policy Pattern Selection

**Choose the right pattern:**

- **user-isolation.sql**: User owns row directly (`user_id` column)
  - Use for: User profiles, settings, personal documents

- **multi-tenant.sql**: Organization/team-based isolation
  - Use for: SaaS apps, team workspaces, shared resources

- **role-based-access.sql**: Different permissions per role
  - Use for: Admin panels, hierarchical access, permission levels

- **ai-chat-policies.sql**: Chat/conversation data
  - Use for: AI chat apps, message history, conversation threads

- **embeddings-policies.sql**: Vector/embedding data
  - Use for: RAG systems, semantic search, vector databases

## Requirements

### Prerequisites
- Supabase project with database access
- PostgreSQL client (`psql`) installed
- Environment variables set:
  - `SUPABASE_DB_URL`: PostgreSQL connection string
  - `SUPABASE_ANON_KEY`: For testing anon access
  - `SUPABASE_SERVICE_KEY`: For admin operations

### Security Checklist
- [ ] RLS enabled on all tables in public schema
- [ ] Policies test both authenticated and anonymous access
- [ ] Indexes created on columns used in policies (user_id, org_id, etc.)
- [ ] Service key never exposed to client applications
- [ ] Policies use `(SELECT auth.uid())` for performance
- [ ] WITH CHECK clause included on INSERT/UPDATE policies
- [ ] Testing validates isolation between users/tenants

### Performance Optimization
- Create indexes: `CREATE INDEX idx_table_user_id ON <table>(user_id);`
- Wrap auth functions: `(SELECT auth.uid())` instead of `auth.uid()`
- Always filter queries: `.eq('user_id', <userId>)` in client code
- Use security definer functions for complex authorization logic
- Specify roles in policies: `TO authenticated` to skip anon checks

---

**Best Practices:**
1. Enable RLS before adding any data.
2. Test with multiple user contexts.
3. Use audit script regularly in CI/CD.
4. Document policy decisions in migration files.
5. Monitor query performance after adding policies.

## Reference System Usage

Always consult the provided reference files for best practices and guidelines:
- **For Creation:** Consult **`references/patterns.md`** for building patterns.
- **For Diagnosis:** Refer to **`references/sharp_edges.md`** for critical failures.
- **For Review:** Use **`references/validations.md`** for validating inputs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.