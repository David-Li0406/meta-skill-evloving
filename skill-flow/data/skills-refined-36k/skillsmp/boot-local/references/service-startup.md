# Service Startup

## Phase 3: Start Services

**CRITICAL**: All three services MUST be started in background mode so they run concurrently.

### Start All Three in Parallel

Use the Bash tool with `run_in_background: true` for ALL THREE commands:

```bash
# Start worker in background
cd C:/users/zac/eos-implementer-hub && npm run worker:dev
# Run with: run_in_background: true

# Start edge functions in background (with env file for API keys)
cd C:/users/zac/eos-implementer-hub && npx supabase functions serve --env-file supabase/.env.local
# Run with: run_in_background: true

# Start dev server on port 8080 in background
cd C:/users/zac/eos-implementer-hub && npm run dev -- --port 8080
# Run with: run_in_background: true
```

## Phase 4: Verify Startup

Use TaskOutput with `block: false` to check each background task's output.

### Expected Outputs

| Service | Success Indicator |
|---------|-------------------|
| Worker | `[AutomationWorker] Worker started successfully` |
| Edge Functions | `Serving functions on http://127.0.0.1:54321/functions/v1/` |
| Dev Server | `VITE ready` and `Local: http://localhost:8080/` |

**Note**: If port 8080 is in use, Vite will auto-increment. Note the actual port in the summary.

## Phase 5: Summary Report

Display final status:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Boot Local Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Service        | Status  | URL                                    |
|----------------|---------|----------------------------------------|
| Worker         | Running | http://localhost:3001/health           |
| Edge Functions | Running | http://127.0.0.1:54321/functions/v1/*  |
| Dev Server     | Running | http://localhost:8080                  |

Edge functions available:
- ai-chat
- ai-debrief
- impersonation-start
- impersonation-end
- process-past-due-invoices
- + more

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Start Commands Reference

```bash
# Start services
npm run worker:dev                                           # Worker with watch
npx supabase functions serve --env-file supabase/.env.local  # Edge functions
npm run dev -- --port 8080                                   # Vite on 8080

# Verify services
curl http://localhost:3001/health           # Worker health
curl http://127.0.0.1:54321/functions/v1/   # Edge functions
curl http://localhost:8080                   # Dev server
```
