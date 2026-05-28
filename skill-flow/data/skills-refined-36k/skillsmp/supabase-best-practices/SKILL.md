---
name: supabase-best-practices
description: Supabase development standards. Triggers when working with Supabase projects, Row Level Security, real-time subscriptions, or Edge Functions.
trigger_patterns:
  - supabase
  - row level security
  - rls
  - auth.uid
  - edge function
  - realtime
  - supabase-js
auto_load_with: []
---

# Supabase Best Practices

Comprehensive coding standards for Supabase development, optimized for AI agents and LLMs.

## Overview

This skill provides 22 rules organized across 8 categories:

1. **Security (RLS) (rls-)** - Row Level Security policies, auth patterns [CRITICAL]
2. **Database Design (schema-)** - Foreign keys, constraints, migrations [CRITICAL]
3. **Authentication (auth-)** - OAuth, MFA, session management [HIGH]
4. **Real-time (realtime-)** - Subscriptions, presence, broadcast [HIGH]
5. **Edge Functions (edge-)** - Deno deploy, secrets, logging [MEDIUM-HIGH]
6. **Storage (storage-)** - Bucket policies, transformations [MEDIUM]
7. **Performance (perf-)** - Connection pooling, indexes [MEDIUM]
8. **Client Libraries (client-)** - Type generation, hooks [LOW-MEDIUM]

## Usage

Reference this skill when:
- Designing Supabase database schemas
- Implementing Row Level Security
- Building real-time features
- Creating Edge Functions
- Configuring authentication

## Build

```bash
pnpm build    # Compile rules to AGENTS.md
pnpm validate # Validate rule files
```
