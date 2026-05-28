---
name: unity-editor-control
description: Use when you need to interact with Unity Editor - run builds, get debug output, manipulate scenes, or check for compile errors.
---

# Unity Editor Control

## Overview

This skill triggers the **mcp-unity** MCP server for direct Unity Editor manipulation.

## When to Use

- "Run the game" / "Play the scene"
- "Build the project"
- "Check for compile errors"
- "Get Unity console output"
- "Create a new scene"
- "Add a GameObject to the scene"

## Available Operations

### Build & Run
```
- Run project in Play mode
- Build standalone player
- Stop running game
```

### Debug Information
```
- Get console output (errors, warnings, logs)
- Check compile status
- Get project settings
```

### Scene Operations
```
- Create new scenes
- Load existing scenes
- Add GameObjects
- Modify scene hierarchy
```

## Usage Pattern

1. **Before coding**: Check if Unity compiles with current code
2. **After coding**: Verify no compile errors introduced
3. **Testing**: Run the game to test changes
4. **Debugging**: Get console output to diagnose issues

## MCP Server

**Server**: mcp-unity
**Package**: @anthropic/mcp-server-unity
**Requires**: Unity Editor running with MCP bridge enabled

## Integration Notes

- Unity must be open with the VeilBreakers3D project loaded
- MCP bridge must be installed in Unity (via Package Manager)
- Commands execute in the context of the active scene

## Workflow Example

```
1. Make code changes using Serena
2. USE THIS SKILL to check compile status
3. If errors: Use unity-debugger agent to investigate
4. If clean: USE THIS SKILL to run and test
5. Check console output for runtime errors
```
