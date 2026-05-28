---
name: db-env-switch
description: Switch between local and production database environments by updating .env.local, killing running processes, and providing restart instructions. Use when user says "switch to local database", "switch to production database", or "change database environment".
allowed-tools: Read, Write, Bash, AskUserQuestion
version: 2.1.0
---

# Database Environment Switch

> Safely switch between local and production database configurations with process restart.

<when_to_use>

## When to Use

Invoke when user says:

- "switch to local database"
- "switch to production database"
- "use local Supabase"
- "connect to production"
- "change database environment"
  </when_to_use>

<workflow>
## Workflow Overview

| Phase | Action                                      | Reference                  |
| ----- | ------------------------------------------- | -------------------------- |
| 1     | Detect current environment                  | Read .env.local            |
| 2     | Safety check (production requires approval) | AskUserQuestion            |
| 3     | Update .env.local                           | Comment/uncomment sections |
| 4     | Kill running processes                      | Vite + Worker PIDs         |
| 5     | Verify + provide restart instructions       | Summary report             |

For detailed steps: [references/workflow-phases.md](references/workflow-phases.md)
</workflow>

<safety_rules>

## Critical Safety Rules

1. **ALWAYS confirm production switch** - Use AskUserQuestion before switching TO production
2. **Verify local Supabase is running** - Check `npx supabase status` before switching TO local
3. **Kill ALL processes** - Dev server and worker cache env vars; updating .env.local alone is NOT enough
   </safety_rules>

<environments>
## Environments

| Environment | URL                                        | Safe to Experiment       |
| ----------- | ------------------------------------------ | ------------------------ |
| LOCAL       | `http://127.0.0.1:54321`                   | Yes                      |
| PRODUCTION  | `https://jbbdfbjihbpntjrmkcwf.supabase.co` | **NO - Real user data!** |

</environments>

<approval_gates>

## Approval Gates

| Gate               | Phase                            | Question                                                   |
| ------------------ | -------------------------------- | ---------------------------------------------------------- |
| Production Confirm | Switching TO production          | "Switch to PRODUCTION? All queries affect REAL USER DATA." |
| Local Supabase     | Switching TO local (not running) | "Start local Supabase now?"                                |

</approval_gates>

<quick_reference>

## Quick Reference

```bash
# Check current environment
grep "^VITE_SUPABASE_URL" .env.local

# Find processes (Windows)
wmic process where "commandline like '%vite%'" get processid 2>nul

# Kill by PID
taskkill //F //PID [pid]

# Restart services after switch
npm run dev
npm run worker:dev
```

For detailed commands: [references/commands-reference.md](references/commands-reference.md)
For error recovery: [references/error-recovery.md](references/error-recovery.md)
For safety reminders: [references/safety-reminders.md](references/safety-reminders.md)
</quick_reference>

<references>
## References

- [references/workflow-phases.md](references/workflow-phases.md) - Detailed 5-phase workflow
- [references/commands-reference.md](references/commands-reference.md) - Process and Supabase commands
- [references/error-recovery.md](references/error-recovery.md) - Troubleshooting failures
- [references/safety-reminders.md](references/safety-reminders.md) - Production warnings and checklists
  </references>

<version_history>

## Version History

- **v2.1.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title

- **v2.0.0** (2025-12-28): Refactored to follow skill-authoring-patterns
  - Added XML tags for structure
  - Created references/ for detailed content
  - Reduced from 916 to ~120 lines

- **v1.0.0** (2025-11-03): Initial release
  </version_history>
