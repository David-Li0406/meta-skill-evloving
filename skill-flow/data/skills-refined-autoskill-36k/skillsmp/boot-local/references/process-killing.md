# Process Killing

## Phase 1: Kill Running Processes

**IMPORTANT**: First, use KillShell to terminate any background tasks from previous runs.

Then kill orphan processes holding the required ports by PID.

### Step 1: Find PID on Port 8080 (Dev Server)

```bash
netstat -ano | findstr :8080 | findstr LISTENING
```

Parse output to get PID (last column). Example:
```
  TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING       23048
```
PID is 23048.

### Step 2: Kill by PID

```bash
taskkill //F //PID <pid>
```

### Step 3: Repeat for Other Ports

- Port 3001 (worker health check)
- Port 54321 (edge functions - usually not needed)

## Phase 2: Wait for Termination

Verify processes are dead:

```bash
# Wait a moment for processes to fully terminate
timeout /t 2 /nobreak >nul

# Verify port 8080 is free
netstat -ano | findstr :8080 | findstr LISTENING
# Should return empty (no output)
```

If ports are still in use, wait additional time or force kill by PID.

## Commands Reference

```bash
# Kill commands (Windows)
taskkill //F //IM node.exe //FI "WINDOWTITLE eq *vite*"
taskkill //F //IM deno.exe
taskkill //F //PID <pid>

# Find processes by port
netstat -ano | findstr :<port> | findstr LISTENING
```
