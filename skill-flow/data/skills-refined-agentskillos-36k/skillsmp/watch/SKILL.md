---
name: watch
description: Run dotnet watch, fix compile errors, and verify features in browser. Use when asked to "watch", "run and test", or "build and verify".
---

# Watch & Verify Skill

This skill uses Gemini CLI to run `dotnet watch`, monitor compiler output, fix errors, and guide the user through verification steps. Because the CLI cannot drive a GUI browser, provide clear manual verification instructions (or scripted HTTP checks) once the server is running.

## When to activate

Trigger on requests like:
- "watch", "run watch", "start watching"
- "run and test in browser"
- "build and verify"
- "watch and fix errors"
- "run the app and check if it works"

## Workflow

### 1. Start dotnet watch in background

Use the `run_shell_command` tool to start the process.

```bash
dotnet watch --project ./src/MotoRent.Server/MotoRent.Server.csproj
```

### 2. Monitor for compile errors

Check the output:
- Watch for signatures such as `error CS`, `Unhandled exception`, `Build FAILED`, or `Hot reload of changes succeeded`

### 3. Fix compile errors

When errors are found:
1. Parse the error message to identify file and line number
2. Read the problematic file
3. Fix the error based on the error message
4. Wait for dotnet watch to rebuild automatically
5. Check output again to verify the fix worked

Common error patterns:
- `error CS0103: The name 'X' does not exist` - missing using or variable
- `error CS1061: 'X' does not contain a definition for 'Y'` - wrong property/method name
- `error CS0246: The type or namespace name 'X' could not be found` - missing reference

### 4. Coordinate verification

Once watch reports success (look for `Now listening on https://localhost:<port>`): port number is the value of environment variable `MOTO_BaseUrl`
1. Surface the URLs printed by `dotnet watch` so the user knows where to browse.
2. Provide step-by-step instructions describing what to click, which tenant/user to impersonate, and what results to expect.
3. When possible, run CLI-based smoke checks (e.g., `powershell` > `Invoke-WebRequest` or `curl`) against public endpoints to confirm the API responds.
4. Document the observed behavior (from CLI output or user feedback) before proceeding.

### 5. Fix-and-verify loop

If verification fails:
1. Identify what went wrong (missing element, wrong behavior, error displayed)
2. Go back to the code and fix the issue
3. Wait for rebuild
4. Re-run manual/CLI verification steps
5. Repeat until feature works correctly

## Example session

```
User: watch and verify the motorbike list page works

Gemini CLI: Starting dotnet watch...
[Runs: dotnet watch --project ./src/MotoRent.Server/MotoRent.Server.csproj]

Checking build status...
Build succeeded! Server running on https://localhost:<port>

Verification plan for the user:
- Navigate to https://localhost:<port>/vehicles
- Confirm table renders 5 motorbikes with status badges and working Edit buttons
- Report any console errors

Feature verified successfully via manual walkthrough!
```

## Error fixing example

```
Build output shows:
error CS1061: 'Motorbike' does not contain a definition for 'Plates'

Gemini CLI: Found compile error. The property should be 'LicensePlate' not 'Plates'.
[Reads file, fixes the property name]

Waiting for rebuild...
Build succeeded! Verifying in browser...
```

## Browser verification checklist

Use this checklist when describing manual test steps or validating with CLI tools:
- [ ] Page loads without errors (no 500, no exceptions in console)
- [ ] Main content displays correctly
- [ ] Interactive elements respond (buttons, links, forms)
- [ ] Data is displayed as expected
- [ ] No visual issues or broken layouts

## Impersonation

When the user asks to impersonate someone, describe the UI steps they should follow once the app is running (since Gemini CLI cannot operate the browser directly):

1. Instruct them to open `https://localhost:<port>/account/impersonate?user=<user_name>&account=<tenant_account_no>`
4. Continue guiding them through the requested scenario while watch keeps running

### Example

```
User: watch and test the rental page as a shop manager

Gemini CLI: Starting dotnet watch...
Build succeeded!

Ask the user to:
1. Browse to  `https://localhost:<port>/account/impersonate?user=<user_name>&account=<tenant_account_no>`
3. Confirm the header shows the impersonated user, then open /rentals and verify the page
```

## Constraints

- Check build output before attempting browser verification
- Fix errors one at a time to avoid cascading issues
- Provide clear instructions for manual verification (screenshots are optional and handled by the user)
- Report clear success/failure status to the user
- When impersonating, always use the ``https://localhost:<port>/account/impersonate?user=<user_name>&account=<tenant_account_no>`` page