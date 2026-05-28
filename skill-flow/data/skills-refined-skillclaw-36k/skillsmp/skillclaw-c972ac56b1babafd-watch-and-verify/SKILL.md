---
name: watch-and-verify
description: Use this skill when you need to run `dotnet watch`, fix compile errors, and verify features in a browser.
---

# Skill body

This skill runs `dotnet watch` to continuously build and run the MotoRent server, monitors for compile errors, fixes them, and guides the user through verification steps.

## When to activate

Trigger on requests like:
- "watch", "run watch", "start watching"
- "run and test in browser"
- "build and verify"
- "watch and fix errors"
- "run the app and check if it works"

## Workflow

### 1. Start dotnet watch in background

Use the `run_shell_command` tool to start the process:

```bash
dotnet watch --project ./src/MotoRent.Server/MotoRent.Server.csproj
```

### 2. Monitor for compile errors

Check the output:
- Watch for signatures such as `error CS`, `Unhandled exception`, `Build FAILED`, or `Hot reload of changes succeeded`

### 3. Fix compile errors

When errors are found:
1. Parse the error message to identify file and line number.
2. Read the problematic file.
3. Fix the error based on the error message.
4. Wait for `dotnet watch` to rebuild automatically.
5. Check output again to verify the fix worked.

Common error patterns:
- `error CS0103: The name 'X' does not exist` - missing using or variable.
- `error CS1061: 'X' does not contain a definition for 'Y'` - wrong property/method name.
- `error CS0246: The type or namespace name 'X' could not be found` - missing reference.

### 4. Coordinate verification

Once `dotnet watch` reports success (look for `Now listening on https://localhost:<port>`):
1. Surface the URLs printed by `dotnet watch` so the user knows where to browse.
2. Provide step-by-step instructions describing what to click, which tenant/user to impersonate, and what results to expect.
3. When possible, run CLI-based smoke checks (e.g., `curl`) against public endpoints to confirm the API responds.
4. Document the observed behavior (from CLI output or user feedback) before proceeding.

### 5. Fix-and-verify loop

If verification fails:
1. Identify what went wrong (missing element, wrong behavior, error displayed).
2. Go back to the code and fix the issue.
3. Wait for rebuild.
4. Re-run manual/CLI verification steps.
5. Repeat until the feature works correctly.

### 6. Handle hot reload issues

If the server output indicates "Unable to apply hot reload because of a rude edit" or changes don't seem to be applying correctly, press "Ctrl + R" to restart the watch.