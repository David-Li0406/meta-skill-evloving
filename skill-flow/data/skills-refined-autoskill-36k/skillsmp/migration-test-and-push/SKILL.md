---
name: migration-test-and-push
description: Unified database migration skill. Use when user says "test migration", "push migration", "deploy migration", "reset local database", or "db push". Promotion pipeline local → staging → production with approval gates at each stage.
allowed-tools: Read, Edit, Bash, AskUserQuestion, Skill
version: 4.0.0
---

# Migration Test & Push

> Promotion pipeline for database migrations: Local → Staging → Production with gates at each stage.

<environments>

## Environments

| Environment | Project ID             | Host                                  | Purpose          |
| ----------- | ---------------------- | ------------------------------------- | ---------------- |
| Local       | -                      | `127.0.0.1:54321`                     | Development/test |
| Staging     | `vsrlvwhnchughfcbilqn` | `aws-0-us-west-2.pooler.supabase.com` | Vercel E2E tests |
| Production  | `jbbdfbjihbpntjrmkcwf` | `aws-0-us-west-1.pooler.supabase.com` | Live users       |

</environments>

<mode_selection>

## Step 0: Choose Mode (Always First)

Use AskUserQuestion to determine workflow:

```typescript
{
  questions: [
    {
      question: "What do you want to do with this migration?",
      header: "Mode",
      options: [
        {
          label: "Test locally only",
          description:
            "Reset local DB, run pgTAP, setup dev. No commit, no push.",
        },
        {
          label: "Push to staging only",
          description:
            "Test locally first, then push to staging for E2E testing.",
        },
        {
          label: "Full deployment",
          description:
            "Complete pipeline: local → staging → production with all safety gates.",
        },
      ],
      multiSelect: false,
    },
  ];
}
```

</mode_selection>

---

<local_workflow>

## LOCAL MODE (6 Steps)

Quick local testing - no commits, no remote changes.

| Step | Action                  | Details                                               |
| ---- | ----------------------- | ----------------------------------------------------- |
| 1    | Verify migration date   | Ask user to confirm timestamp                         |
| 2    | Reset local database    | `npx supabase db reset` (runs seed.sql automatically) |
| 3    | Run pgTAP tests         | `npm run test:sql`                                    |
| 4    | Check for missing tests | Ask if new tests needed                               |
| 5    | Restart worker          | Kill and restart worker process                       |
| 6    | Generate types locally  | `npx supabase gen types typescript --local`           |

**Result**: Ready for testing at localhost:8080. No commit, no push.

For detailed steps: [references/local-mode.md](references/local-mode.md)
</local_workflow>

---

<staging_workflow>

## STAGING MODE (8 Steps)

Push to staging for Vercel E2E testing. Includes local testing first.

| Step | Action                  | Gate | Details                                                |
| ---- | ----------------------- | ---- | ------------------------------------------------------ |
| 1    | Verify migration date   | Ask  | Confirm timestamp is correct                           |
| 2    | Reset local database    |      | `npx supabase db reset`                                |
| 3    | Run pgTAP tests         |      | `npm run test:sql`                                     |
| 4    | Check for missing tests | Ask  | Create tests for new tables?                           |
| 5    | Link to staging         |      | `npx supabase link --project-ref vsrlvwhnchughfcbilqn` |
| 6    | Dry-run staging         |      | `npx supabase db push --dry-run`                       |
| 7    | Push to staging         | Ask  | `npx supabase db push`                                 |
| 8    | Verify migration        |      | Check `schema_migrations` table                        |

**Result**: Staging database updated. Ready for Vercel E2E tests.

**Note**: No backup needed for staging (test data only). No types commit (staging types not used).

</staging_workflow>

---

<production_workflow>

## FULL DEPLOYMENT MODE (18 Steps)

Complete promotion pipeline: Local → Staging → Production.

| Step | Action                      | Gate | Phase      |
| ---- | --------------------------- | ---- | ---------- |
| 1    | Verify migration date       | Ask  | Pre-flight |
| 2    | Reset local database        |      | Local      |
| 3    | Run pgTAP tests             |      | Local      |
| 4    | Check for missing tests     | Ask  | Local      |
| 5    | Link to staging             |      | Staging    |
| 6    | Dry-run staging             |      | Staging    |
| 7    | Push to staging             | Ask  | Staging    |
| 8    | Verify staging migration    |      | Staging    |
| 9    | Commit migration to Git     |      | Pre-prod   |
| 10   | Analyze rollback strategy   |      | Pre-prod   |
| 11   | Check locking impact        |      | Pre-prod   |
| 12   | Link to production          |      | Production |
| 13   | Request db push permission  | Ask  | Production |
| 14   | Dry-run production          |      | Production |
| 15   | Get final approval          | Ask  | Production |
| 16   | Create production backup    |      | Production |
| 17   | Push to production          |      | Production |
| 18   | Verify production migration |      | Production |
| 19   | Revoke permission           | Auto | Production |
| 20   | Generate types from prod    |      | Post-prod  |
| 21   | Commit types                |      | Post-prod  |

**Critical**: Each stage must pass before proceeding to the next.

For detailed steps: [references/production-mode.md](references/production-mode.md)
</production_workflow>

---

<approval_gates>

## Approval Gates

| Gate            | Phase | Question                                    |
| --------------- | ----- | ------------------------------------------- |
| Mode            | 0     | "Local, staging, or full deployment?"       |
| Date            | 1     | "Migration dated YYYY-MM-DD correct?"       |
| Tests           | 4     | "Create pgTAP tests for new tables?"        |
| Staging Push    | 7     | "Push to staging?"                          |
| Permission      | 13    | "Enable db push temporarily?"               |
| Production Push | 15    | "Push to production? (shows rollback plan)" |

All gates use AskUserQuestion tool. Stop execution if user declines.
</approval_gates>

---

<safety_rules>

## Safety Rules

### Rule 1: Sequential Promotion

```
Local → Staging → Production
```

Never skip environments. Each must pass before proceeding.

### Rule 2: Never Push Without Approval

Use AskUserQuestion before any `npx supabase db push` - required for safety.

### Rule 3: Follow Exact Workflow Order

Never skip or reorder steps within a phase.

### Rule 4: Stop on Any Error

- Local test fails → STOP, fix migration
- Staging push fails → STOP, investigate
- User denies → STOP, cancel deployment
- Production push fails → STOP, show rollback guidance

### Rule 5: Permission is Temporary

Add pattern to `bash_validator.py` before production push, remove immediately after.

### Rule 6: Backup Before Production Only

Staging uses test data - no backup needed. Production requires backup.
</safety_rules>

---

<quick_reference>

## Quick Reference

### Local Testing

```bash
npx supabase db reset
npm run test:sql
npx supabase gen types typescript --local > src/integrations/supabase/types.ts
```

### Staging Push

```bash
npx supabase link --project-ref vsrlvwhnchughfcbilqn
npx supabase db push --dry-run
npx supabase db push
```

### Production Push

```bash
npx supabase link --project-ref jbbdfbjihbpntjrmkcwf
npx supabase db push --dry-run
npx supabase db push
npx supabase gen types typescript --project-id jbbdfbjihbpntjrmkcwf > src/integrations/supabase/types.ts
```

### Verification (both staging and production)

```sql
SELECT version FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 1;
```

### Production Backup

```bash
PGPASSWORD="<password>" pg_dump -h aws-0-us-west-1.pooler.supabase.com -p 6543 \
  -U postgres.jbbdfbjihbpntjrmkcwf -d postgres --schema=public -Fc \
  > supabase/backups/pre_migration_$(date +%Y%m%d_%H%M%S).dump
```

</quick_reference>

---

<when_to_use>

## When to Use

**Triggers for this skill:**

- "test migration"
- "push migration"
- "deploy migration"
- "reset local database"
- "apply migration"
- "db push"
- "test and push"
- "push to staging"
- "push to production"

**Ambiguous requests** → Ask which mode first
</when_to_use>

---

<references>

## Reference Files

Detailed documentation:

- [Local Mode Steps](references/local-mode.md)
- [Production Mode Steps](references/production-mode.md)
- [Rollback Patterns](references/rollback-patterns.md)
- [Error Recovery](references/error-recovery.md)
- [Command Reference](references/commands.md)

</references>

---

<version_history>

## Version History

- **v4.0.0** (2026-01-19): Add staging environment to promotion pipeline
  - New 3-tier workflow: Local → Staging → Production
  - Added staging project ID (`vsrlvwhnchughfcbilqn`)
  - New "Push to staging only" mode for E2E test prep
  - Full deployment now includes staging verification before production
  - Updated approval gates for staging push

- **v3.1.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title
  - Soften directive language (NON-NEGOTIABLE → required for production safety)

- **v3.0.0** (2025-12-28): Rewrite following Anthropic best practices
  - Progressive disclosure: Core in SKILL.md, details in references/
  - XML tags for structure
  - Imperative form throughout
  - Reduced from 1,071 lines to ~200 lines
- **v2.0.0** (2025-12-28): Merged with migration-test-local skill
  - Mode selection (local test vs production push)
  - Local mode: 7 steps, no commits
  - Production mode: 16 steps, full safety
- **v1.2.0** (2025-12-28): Industry best practices update
  - Test BEFORE commit workflow order
  - Added rollback analysis, locking check, backup, verification
- **v1.0.0** (2025-10-26): Initial release

</version_history>
