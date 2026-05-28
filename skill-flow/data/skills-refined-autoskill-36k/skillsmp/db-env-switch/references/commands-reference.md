# Commands Reference

## Environment Detection

```bash
# Check current environment
grep "^VITE_SUPABASE_URL" .env.local
```

## Process Management (Windows)

```bash
# Find running processes
wmic process where "commandline like '%vite%' and name='node.exe'" get processid,commandline 2>nul
wmic process where "commandline like '%worker%' and name='node.exe'" get processid,commandline 2>nul

# Kill processes
taskkill //F //PID [pid]
```

## Local Supabase

```bash
# Check status
npx supabase status

# Start local Supabase
npx supabase start

# Stop local Supabase
npx supabase stop
```

## Restart Services

```bash
# Restart Vite dev server
npm run dev

# Restart with custom port
PORT=8080 npm run dev

# Restart worker
npm run worker:dev
```

## Verification

```bash
# In browser console (F12):
console.log(import.meta.env.VITE_SUPABASE_URL)

# Expected LOCAL: http://127.0.0.1:54321
# Expected PROD:  https://jbbdfbjihbpntjrmkcwf.supabase.co
```

## Environment Variables Modified

| Variable | LOCAL | PRODUCTION |
|----------|-------|------------|
| `VITE_SUPABASE_URL` | `http://127.0.0.1:54321` | `https://jbbdfbjihbpntjrmkcwf.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Demo anon key | Production anon key |
| `SUPABASE_SERVICE_ROLE_KEY` | Demo service role | Production service role |

All three MUST be switched together for consistent behavior.
