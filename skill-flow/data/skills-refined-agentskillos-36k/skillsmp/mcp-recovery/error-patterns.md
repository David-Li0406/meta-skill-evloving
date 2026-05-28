# MCP Error Pattern Library

Known error patterns and their recovery actions.

## Error Pattern → Recovery Mapping

| Error Pattern | Recovery Level | Recovery Action | Command |
|---------------|---------------|-----------------|---------|
| `Port 9080 not listening` | Medium | Start Godot editor with MCP | `powershell -File .claude/skills/godot-mcp-dap-start/scripts/ensure_godot_mcp.ps1` |
| `Connection refused` | Medium | Check for duplicate Godot processes, restart | `tasklist \| findstr /i "Godot"` then kill duplicates |
| `Unknown command` | Light | Verify MCP CLI installation | `npx -y godot-mcp-cli@latest --version` |
| `Timeout on get_runtime_scene_structure` | Light | Start game (Godot running but game not) | `npx -y godot-mcp-cli@latest run_project --headed` |
| `Godot not in processes` | Heavy | Full restart - start Godot | `powershell -File .claude/skills/mcp-recovery/scripts/recover.ps1` |
| `Multiple Godot processes detected` | Medium | Kill all but one Godot instance | `Stop-Process -Name "Godot*" -Force` |
| `npx: command not found` | Light | Install Node.js and npm | Ask user to install Node.js |
| `EADDRINUSE: address already in use ::9080` | Medium | Duplicate MCP servers, kill Godot duplicates | `Stop-Process -Name "Godot*" -Force` |
| `WebSocket connection failed` | Medium | MCP addon not loaded, restart Godot | `powershell -File .claude/skills/mcp-recovery/scripts/recover.ps1` |
| `Failed to load script` in Godot console | Heavy | Script error blocking MCP, fix script first | Check Godot console for specific script error |
| `limboai DLL errors` | Medium | Addon conflict, disable limboai or fix DLL | Check addons/limboai/bin/ directory |

## Diagnostic Flowchart

```
                    MCP Command Fails?
                          |
                          v
                  Run Health Check
                          |
          +---------------+---------------+
          |                               |
    Port 9080 listening?            Godot running?
          |                               |
     NO / YES                        NO / YES
      |     |                         |     |
      v     v                         v     v
  Start   Check                   Start   Check
 Godot   dupes                   Godot   MCP CLI
          |                               |
          v                               v
    Kill dupes → Restart            Reinstall
          |                          Node.js
          v
    Verify MCP CLI
```

## Health Check Status Mapping

| Health Check Status | Meaning | Action |
|---------------------|---------|--------|
| `healthy` | All systems go | Proceed with work |
| `degraded` | Partial failure | Follow recommendations |
| `down` | Complete failure | Run recovery script |
| `unknown` | Health check failed | Escalate to user |

## Common Error Messages and Solutions

### "npx: command not found"
**Cause:** Node.js not installed or not in PATH
**Solution:** Ask user to install Node.js from nodejs.org

### "Port 9080 not listening" (Godot running)
**Cause:** MCP addon not enabled or failed to load
**Solution:**
1. Check Godot console for MCP errors
2. Enable MCP plugin in Project Settings > Plugins
3. Restart Godot

### "Multiple Godot processes detected"
**Cause:** Duplicate Godot instances from previous sessions
**Solution:**
```powershell
Stop-Process -Name "Godot*" -Force
Start-Sleep -Seconds 2
# Restart single instance
```

### "EADDRINUSE: address already in use ::9080"
**Cause:** Port conflict from previous Godot session
**Solution:** Same as multiple Godot processes

### "Timeout on get_project_info"
**Cause:** MCP server not responding
**Solution:**
1. Check if Godot is running
2. Check Godot console for MCP status
3. If MCP shows "started on port 9080", try CLI command again
4. If not, restart Godot

### "limboai DLL errors" (in Godot console)
**Cause:** limboai addon has missing or corrupted DLL files
**Solution:**
1. Disable limboai plugin temporarily
2. Or fix DLL files in `addons/limboai/bin/`
3. Restart Godot

## Escalation Criteria

**Ask user for help when:**
- Recovery script fails 3 times in a row
- Godot fails to start after heavy recovery
- MCP addon shows errors in Godot console
- Script errors prevent MCP from loading
- Health check returns `unknown` status
- You don't recognize the error pattern

## Prevention Tips

1. **Always close Godot properly** - Don't force-kill if possible
2. **Run health check before playtesting** - Catch issues early
3. **Use godot-mcp-dap-start skill** - Proper startup sequence
4. **Check Godot console** - MCP logs appear there
5. **One Godot instance only** - Multiple instances cause conflicts
