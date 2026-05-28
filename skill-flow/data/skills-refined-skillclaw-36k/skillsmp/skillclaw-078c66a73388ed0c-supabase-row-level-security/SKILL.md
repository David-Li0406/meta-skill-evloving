---
name: supabase-row-level-security
description: Use this skill when implementing Row Level Security (RLS) in Supabase applications to ensure data protection, user isolation, and secure access patterns.
---

# Skill body

## Overview

This skill provides a comprehensive guide to implementing Row Level Security (RLS) in Supabase applications, focusing on multi-tenant patterns, user isolation, and role-based access.

## Instructions

### 1. Applying RLS Policies

**Apply policies to tables:**
```bash
# Apply user isolation policies
bash scripts/apply-rls-policies.sh user-isolation conversations messages

# Apply multi-tenant policies
bash scripts/apply-rls-policies.sh multi-tenant organizations org_members documents

# Apply AI-specific policies
bash scripts/apply-rls-policies.sh ai-chat conversations messages message_embeddings
```

**Generate custom policy:**
```bash
# Generate policy from template
bash scripts/generate-policy.sh user-isolation my_table user_id

# Generate with custom column
bash scripts/generate-policy.sh multi-tenant projects organization_id
```

### 2. Testing RLS Enforcement

**Test policies work correctly:**
```bash
# Test all policies on a table
bash scripts/test-rls-policies.sh conversations

# Test specific user context
bash scripts/test-rls-policies.sh messages --user-id "user-uuid-here"

# Test multi-tenant isolation
bash scripts/test-rls-policies.sh documents --org-id "org-uuid-here"
```

### 3. Auditing Security

**Audit tables for missing RLS:**
```bash
# Audit all tables in public schema
bash scripts/audit-rls.sh

# Audit specific tables
bash scripts/audit-rls.sh conversations messages embeddings

# Generate audit report
bash scripts/audit-rls.sh --report audit-report.md
```

### 4. Policy Pattern Selection

**Choose the right pattern:**

- **user-isolation.sql**: User owns row directly (`user_id` column)
  - Use for: User profiles, settings, personal documents
  - Pattern: `auth.uid() = user_id`

- **multi-tenant.sql**: Organization/team-based isolation
  - Use for: SaaS apps, team workspaces, shared resources
  - Pattern: Check organization membership via join

- **role-based-access.sql**: Different permissions per role
  - Use for: Admin panels, hierarchical access, permission management

## Security Best Practices

- RLS is mandatory on every table to ensure data protection.
- The service role key should be treated as highly sensitive; it should only be used server-side.
- Always validate user inputs against established patterns and constraints to mitigate risks.

## Reference System Usage

For detailed guidance, consult the following reference files:
- **`references/patterns.md`**: For creation guidelines.
- **`references/sharp_edges.md`**: For diagnosing potential security failures.
- **`references/validations.md`**: For validating user inputs and ensuring compliance with security standards.