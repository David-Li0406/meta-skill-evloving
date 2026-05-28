---
name: boot-local
description: Kill all running local development processes (worker, edge functions, dev server), wait for termination, then restart them. Dev server runs on port 8080. Use when user says "boot local", "restart local", "reboot dev", or needs to refresh local services.
allowed-tools: Bash, TaskOutput
version: 2.1.0
---

# Boot Local

> Kill and restart all local development services when the dev environment needs a fresh start.

<when_to_use>

## When to Use

Invoke when user says:

- "boot local"
- "restart local"
- "reboot dev"
- "restart all services"
- "kill and restart"
  </when_to_use>

<workflow>
## Workflow

| Phase | Action                                    | Reference                                           |
| ----- | ----------------------------------------- | --------------------------------------------------- |
| 1     | Kill running processes (ports 8080, 3001) | [process-killing.md](references/process-killing.md) |
| 2     | Wait for termination, verify ports free   | [process-killing.md](references/process-killing.md) |
| 3     | Start all 3 services in background        | [service-startup.md](references/service-startup.md) |
| 4     | Verify startup (check logs)               | [service-startup.md](references/service-startup.md) |
| 5     | Display status report                     | Final output                                        |

**Note**: Use `run_in_background: true` for all three start commands to avoid blocking.
</workflow>

<services>
## Services

| Service        | Command                                                       | Port  | URL                                  |
| -------------- | ------------------------------------------------------------- | ----- | ------------------------------------ |
| Worker         | `npm run worker:dev`                                          | 3001  | http://localhost:3001/health         |
| Edge Functions | `npx supabase functions serve --env-file supabase/.env.local` | 54321 | http://127.0.0.1:54321/functions/v1/ |
| Dev Server     | `npm run dev -- --port 8080`                                  | 8080  | http://localhost:8080                |

</services>

<approval_gates>

## Approval Gates

| Gate | Phase | Question                                             |
| ---- | ----- | ---------------------------------------------------- |
| None | -     | No destructive operations; all local process cleanup |

</approval_gates>

<quick_reference>

## Quick Reference

```bash
# Find process on port
netstat -ano | findstr :8080 | findstr LISTENING

# Kill by PID
taskkill //F //PID <pid>

# Start services (use run_in_background: true)
npm run worker:dev
npx supabase functions serve --env-file supabase/.env.local
npm run dev -- --port 8080
```

For detailed steps: [references/process-killing.md](references/process-killing.md)
For error recovery: [references/error-recovery.md](references/error-recovery.md)
</quick_reference>

<references>
## References

- [references/process-killing.md](references/process-killing.md) - Finding and killing processes
- [references/service-startup.md](references/service-startup.md) - Starting dev services
- [references/error-recovery.md](references/error-recovery.md) - Troubleshooting failures
  </references>

<version_history>

## Version History

- **v2.1.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title
  - Soften directive language per Opus 4.5 guidance

- **v2.0.0** (2025-12-28): Refactored to follow skill-authoring-patterns
  - Added XML tags for structure
  - Created references/ for detailed content
  - Reduced from 197 to ~90 lines

- **v1.0.1** (2025-12-21): Fix edge functions env file
  - Added `--env-file supabase/.env.local`

- **v1.0.0** (2025-12-21): Initial release
  </version_history>
