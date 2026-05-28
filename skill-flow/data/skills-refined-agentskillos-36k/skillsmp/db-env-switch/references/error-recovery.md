# Error Recovery

## Scenario 1: .env.local File Not Found

**Problem**: Cannot locate .env.local

**Recovery**:
```
❌ .env.local file not found!

Expected location: C:\users\zac\eos-implementer-hub\.env.local

The file must be created manually. Template:

# LOCAL DATABASE (default)
VITE_SUPABASE_URL=http://127.0.0.1:54321
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...demo...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...demo...

# PRODUCTION DATABASE (uncomment to switch)
# VITE_SUPABASE_URL=https://jbbdfbjihbpntjrmkcwf.supabase.co
# VITE_SUPABASE_ANON_KEY=<production anon key>
# SUPABASE_SERVICE_ROLE_KEY=<production service role key>
```

**STOP execution**.

---

## Scenario 2: Cannot Determine Current Environment

**Problem**: No uncommented `VITE_SUPABASE_URL` found

**Recovery**: Use AskUserQuestion to ask which environment user is on:
- Local (127.0.0.1)
- Production (jbbdfbjihbpntjrmkcwf)
- Unknown/Other

If "Unknown": Show file contents, ask user to fix manually. **STOP**.

---

## Scenario 3: Local Supabase Not Running

**Problem**: Switching to LOCAL but Supabase not running

**Recovery**:
```
⚠️ Local Supabase is not running

Options:
1. Start local Supabase now (npx supabase start)
2. Continue switch anyway (manual start later)
3. Cancel switch
```

---

## Scenario 4: Processes Won't Terminate

**Problem**: taskkill fails (permission denied, etc.)

**Recovery**:
```
⚠️ Could not kill process automatically

Manual cleanup:
  taskkill //F //PID [pid]
  OR close the terminal window running the process

After killing manually:
  npm run dev          (for Vite)
  npm run worker:dev   (for worker)
```

**Continue** with switch even if kill fails.

---

## Scenario 5: Already on Target Environment

**Problem**: User requests switch but already on target

**Recovery**:
```
✅ Already on [TARGET] environment

Current configuration:
  VITE_SUPABASE_URL=[current URL]

No changes needed.
```

**STOP execution**.

---

## Scenario 6: User Cancels During Safety Check

**Problem**: User selects "No" or "Cancel"

**Recovery**:
```
❌ Switch cancelled by user

No changes made.
Current environment remains: [SOURCE]
```

**STOP execution** cleanly.
