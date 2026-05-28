---
name: Database Migration Workflow
description: Standard workflow for adding new database tables, updating types, and creating the API layer in Supabase + Next.js.
version: 1.0.0
---

# Skill: Database Migration Workflow

This skill orchestrates the end-to-end process of adding a new feature that requires database changes.
In Supabase projects, this involves specific steps to keep TypeScript types in sync.

## Execution Steps

### 1. Database Change (Supabase)
*Note: Since the agent cannot directly access the Supabase Dashboard, this step usually involves instructing the user or creating a SQL migration file if a local migration flow is set up.*

**Action**: Create a `.sql` file in `supabase/migrations/` (if enabled) OR provide the SQL to the user.
- Define Table: `CREATE TABLE [name] (...)`
- Enable RLS: `ALTER TABLE [name] ENABLE ROW LEVEL SECURITY;`
- Policies: `CREATE POLICY ...` (Standard: Select for Authenticated, Insert/Update for specific roles).

### 2. Update Types (`database.types.ts`)
**CRITICAL STEP**: The application relies on `lib/database.types.ts`.
- **Instruction**: "Please run `npx supabase gen types typescript --project-id [id] > lib/database.types.ts`"
- **Fallback**: If the user cannot run this, the agent must manually update the interface in `lib/database.types.ts` to reflect the new table structure so the code compiles.

### 3. Service Layer (`lib/`)
Create a helper function to interact with this table.
- File: `lib/[feature]-service.ts` or add to `lib/supabase.ts`.
- Use the typed client: `const supabase = createClient<Database>()`.

### 4. Server Action or API Route
Decide if the mutation (Create/Update/Delete) should be a **Server Action** or **API Route**.
- **Server Action** (`app/actions/[feature].ts`): Best for form submissions from the UI.
- **API Route** (`app/api/[feature]/route.ts`): Best for external webhooks or complex batch processing.

### 5. Frontend Integration
Create the UI component that calls the Action/Service.
- Use `useTransition` for Server Actions.
- Handle loading/error states.

## Agent Checklist
- [ ] SQL created and RLS policies defined?
- [ ] `database.types.ts` updated?
- [ ] Service function created with correct types?
- [ ] UI Component connected and error handling implemented?
