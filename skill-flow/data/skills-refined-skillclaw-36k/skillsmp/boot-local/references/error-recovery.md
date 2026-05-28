# Error Recovery

## Port 8080 Still In Use After Kill

If port 8080 is still occupied:

1. Find the process:
   ```bash
   netstat -ano | findstr :8080
   ```

2. Kill by PID:
   ```bash
   taskkill //F //PID <pid>
   ```

3. If still fails, inform user to manually close the application

## Edge Functions Fail to Start

If `npx supabase functions serve` fails:

1. Check if local Supabase is running:
   ```bash
   npx supabase status
   ```

2. If not running, start it:
   ```bash
   npx supabase start
   ```

3. Then retry edge functions:
   ```bash
   npx supabase functions serve --env-file supabase/.env.local
   ```

## Worker Fails to Start

If worker fails:

1. Check for build errors in output

2. Try rebuilding:
   ```bash
   npm run worker:build
   ```

3. Check if port 3001 is in use:
   ```bash
   netstat -ano | findstr :3001
   ```

## Dev Server Auto-Increments Port

If Vite shows a different port than 8080:

- This means port 8080 was still in use
- Note the actual port in the summary
- Inform user of the actual URL

## All Services Fail to Start

Full reset procedure:

1. Kill all Node processes:
   ```bash
   taskkill //F //IM node.exe
   ```

2. Kill all Deno processes:
   ```bash
   taskkill //F //IM deno.exe
   ```

3. Wait for processes to terminate:
   ```bash
   timeout /t 5 /nobreak
   ```

4. Restart Supabase:
   ```bash
   npx supabase stop
   npx supabase start
   ```

5. Retry boot-local skill
