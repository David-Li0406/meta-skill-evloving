# Unity MCP Troubleshooting

Common issues and solutions when working with Unity MCP tools.

## Connection Issues

### MCP Server Not Connected

**Symptom:** `/mcp` shows red X for `ai-game-developer`

**Causes & Solutions:**

1. **Server not running**

   - Run `start-mcp-server.bat` in project root
   - Keep terminal window open

2. **Unity not connected**

   - Unity must be opened AFTER server starts
   - Check Unity console for connection messages

3. **Port conflict**
   - Default port: 56688
   - Check if another process uses the port
   - Restart server and Unity

### Tools Return "Not Found"

**Symptom:** MCP tool calls return error about tool not existing

**Cause:** Tool is disabled in config

**Solution:**

1. Check tool status: `/unity-mcp-status`
2. Enable required group: `/unity-mcp-enable [group]`
3. Or enable all: `/unity-mcp-enable-all`

## Tool Enablement Issues

### "Tool is disabled" Error

**Symptom:** Tool call fails with disabled message

**Solution:**

```text
1. Identify which group contains the tool
2. Run /unity-mcp-enable [group]
3. Retry the operation
```

**Group Quick Reference:**

| Tool Prefix       | Enable Group              |
| ----------------- | ------------------------- |
| `scene-*`         | scene-read or scene-write |
| `gameobject-*`    | gameobject                |
| `*-component-*`   | component                 |
| `script-*`        | script                    |
| `assets-prefab-*` | prefab                    |
| `assets-*`        | assets                    |
| `tests-*`         | testing                   |
| `editor-*`        | editor                    |
| `package-*`       | packages                  |
| `reflection-*`    | reflection                |

### Config File Not Found

**Symptom:** Enable command fails to find config

**Solution:**

1. Verify file exists: `Assets/Resources/AI-Game-Developer-Config.json`
2. If missing, create from template or restart Unity MCP plugin

## Scene Operation Issues

### "Scene not found"

**Symptom:** Scene tools can't find specified scene

**Causes:**

1. Scene name is incorrect
2. Scene not loaded in editor

**Solution:**

1. Use `/unity-mcp-scene-info` to check loaded scenes
2. Use full scene name without path: `GameplayScene` not `Assets/Scenes/GameplayScene.unity`

### "GameObject not found"

**Symptom:** `gameobject-find` returns null

**Causes:**

1. Path is incorrect
2. Object doesn't exist
3. Object is inactive

**Solution:**

1. Use MCP Resource to inspect hierarchy first
2. Check exact path including parent names
3. Path format: `Parent/Child/GrandChild`

## Component Issues

### "Component type not found"

**Symptom:** `gameobject-component-add` fails

**Cause:** Incorrect component type name

**Solution:** Use full namespace:

- Wrong: `SpriteRenderer`
- Correct: `UnityEngine.SpriteRenderer`

Custom scripts:

- Wrong: `TileView`
- Correct: `ZeroDayAttack.View.TileView`

### Component Values Not Updating

**Symptom:** `gameobject-component-modify` succeeds but values unchanged

**Causes:**

1. Property is read-only
2. Scene not saved

**Solution:**

1. Check if property is settable
2. Call `scene-save` after modifications
3. Verify with `gameobject-component-get`

## Script Issues

### Compilation Errors

**Symptom:** `script-update-or-create` reports errors

**Solution:**

1. Read the compilation feedback carefully
2. Check for:
   - Missing using statements
   - Syntax errors
   - Missing dependencies
3. Fix issues and retry

### Script Not Appearing in Unity

**Symptom:** Script created but not visible in Unity

**Solution:**

1. Call `assets-refresh` to force reimport
2. Check file was created in correct location
3. Verify file has `.cs` extension

## Test Issues

### Tests Not Running

**Symptom:** `tests-run` returns no results

**Causes:**

1. Testing group not enabled
2. No tests match filter
3. Editor is in play mode

**Solution:**

1. Enable testing: `/unity-mcp-enable testing`
2. Check test filter matches actual test names
3. Exit play mode before running tests

### Tests Fail Unexpectedly

**Symptom:** Tests that should pass are failing

**Causes:**

1. Scene state is dirty
2. Previous test left state
3. Missing test setup

**Solution:**

1. Save scene before testing
2. Check test isolation
3. Review test setup/teardown

## Performance Issues

### MCP Calls Are Slow

**Causes:**

1. Too many tools enabled (context overhead)
2. Large scene hierarchy
3. Server connection issues

**Solutions:**

1. Enable only needed groups, reset after
2. Use specific paths instead of querying entire hierarchy
3. Check server connection stability

### Context Window Filling Up

**Symptom:** Claude running out of context

**Cause:** Too many MCP tools enabled

**Solution:**

1. Run `/unity-mcp-reset` after MCP work
2. Enable only required tool groups
3. Use MCP Resource for read-only inspection (no enablement needed)

## Quick Fixes Checklist

When MCP isn't working:

1. [ ] Is MCP server running? (`start-mcp-server.bat`)
2. [ ] Is Unity open and connected?
3. [ ] Run `/mcp` - is `ai-game-developer` green?
4. [ ] Are required tools enabled? (`/unity-mcp-status`)
5. [ ] Is Editor in Edit mode (not Play mode)?
6. [ ] Are paths/names correct?
7. [ ] Are component types fully qualified?

## Getting Help

If issues persist:

1. Check Unity console for error messages
2. Check MCP server terminal for connection logs
3. Try `/unity-mcp-reset` then re-enable specific groups
4. Restart MCP server and Unity if needed

For complex issues, spawn the `mcp-coordinator` agent for expert diagnosis.
