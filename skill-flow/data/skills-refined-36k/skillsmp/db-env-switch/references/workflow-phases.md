# Detailed Workflow Phases

## Phase 1: Detect Current State

### Step 1: Read Current Environment

```bash
Read C:\users\zac\eos-implementer-hub\.env.local
```

**Logic to determine current environment**:
- Look for uncommented `VITE_SUPABASE_URL=` line
- If contains `https://jbbdfbjihbpntjrmkcwf.supabase.co` → **PRODUCTION**
- If contains `http://127.0.0.1:54321` → **LOCAL**

### Step 2: Determine Target Environment

Parse user request:
- "switch to local" / "use local" → TARGET = LOCAL
- "switch to production" / "connect to prod" → TARGET = PRODUCTION

If ambiguous, use AskUserQuestion to clarify.

### Step 3: Check If Switch Needed

If current == target:
```
✅ Already on [TARGET] environment
No changes needed.
```
**STOP execution**.

### Step 4: Find Running Processes

```bash
# Find Vite dev server
wmic process where "commandline like '%vite%' and name='node.exe'" get processid,commandline 2>nul

# Find worker
wmic process where "commandline like '%worker%' and name='node.exe'" get processid,commandline 2>nul
```

Extract PIDs from output for later termination.

---

## Phase 2: Safety Checks

### If Switching TO Production

**MUST use AskUserQuestion**:
```
⚠️ Switch to PRODUCTION database? All queries will affect REAL USER DATA.
- Yes, switch to production
- No, stay on local
```

If "No": **STOP execution**.

### If Switching TO Local

Check if local Supabase is running:
```bash
npx supabase status
```

If not running, offer options:
1. Start local Supabase now
2. Continue switch anyway
3. Cancel switch

---

## Phase 3: Update .env.local

### Switching TO LOCAL:

1. **Comment out production section**:
   ```
   # VITE_SUPABASE_URL=https://jbbdfbjihbpntjrmkcwf.supabase.co
   # VITE_SUPABASE_ANON_KEY=...
   # SUPABASE_SERVICE_ROLE_KEY=...
   ```

2. **Uncomment local section**:
   ```
   VITE_SUPABASE_URL=http://127.0.0.1:54321
   VITE_SUPABASE_ANON_KEY=eyJhbGci...demo...
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGci...demo...
   ```

### Switching TO PRODUCTION:

1. **Uncomment production section**
2. **Comment out local section**

### Verify Changes

Read back the file and confirm correct URL is active.

---

## Phase 4: Terminate Running Processes

**Why we kill processes**:
- Vite caches `import.meta.env` at startup
- Worker loads `.env.local` via dotenv at startup
- Simply updating .env.local is NOT sufficient

### Kill Vite Dev Server

```bash
taskkill //F //PID [vite_pid]
```

### Kill Worker

```bash
taskkill //F //PID [worker_pid]
```

---

## Phase 5: Verification & Next Steps

Display summary:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Database Environment Switch Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FROM: [SOURCE] database
TO:   [TARGET] database

Next Steps:
1. npm run dev          (restart Vite)
2. npm run worker:dev   (restart worker)
3. Verify in browser console
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If switched to PRODUCTION: Show critical warnings about live data.
If switched to LOCAL: Show safe-to-experiment message.
