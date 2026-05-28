---
name: watch-and-verify
description: Use this skill to run `dotnet watch`, fix compile errors, and verify features in a browser. Activate when asked to "watch", "run and test", or "build and verify".
---

# Watch & Verify Skill

This skill runs `dotnet watch` to continuously build and run the MotoRent server, monitors for compile errors, fixes them, and guides the user through verification steps in a browser.

## When to activate

Trigger on requests like:
- "watch", "run watch", "start watching"
- "run and test in browser"
- "build and verify"
- "watch and fix errors"
- "run the app and check if it works"

## Workflow

### 1. Start dotnet watch in background

Run the following command in the background to allow continuous operation:

```bash
dotnet watch --project ./src/MotoRent.Server/MotoRent.Server.csproj
```

### 2. Monitor for compile errors

Check the output periodically for error patterns:
- Look for signatures such as `error CS`, `Unhandled exception`, `Build FAILED`, or `Hot reload of changes succeeded`.

### 3. Fix compile errors

When errors are found:
1. Parse the error message to identify the file and line number.
2. Read the problematic file.
3. Fix the error based on the error message.
4. Wait for `dotnet watch` to rebuild automatically.
5. Check the output again to verify the fix worked.

Common error patterns include:
- `error CS0103: The name 'X' does not exist` - missing using or variable.
- `error CS1061: 'X' does not contain a definition for 'Y'` - wrong property/method name.
- `error CS0246: The type or namespace name 'X' could not be found` - missing reference.

### 4. Coordinate verification

Once the build succeeds (look for `Now listening on https://localhost:<port>`):
1. Surface the URLs printed by `dotnet watch` for user navigation.
2. Provide step-by-step instructions on what to click, which tenant/user to impersonate, and expected results.
3. When possible, run CLI-based smoke checks against public endpoints to confirm the API responds.
4. Document the observed behavior before proceeding.

### 5. Fix-and-verify loop

If verification fails:
1. Identify what went wrong (missing element, wrong behavior, error displayed).
2. Go back to the code and fix the issue.
3. Wait for rebuild.
4. Re-run manual/CLI verification steps.
5. Repeat until the feature works correctly.

### 6. Stopping the watch

When done or when the user asks to stop:
1. Use the appropriate command to stop the background process.
2. Confirm that the process has ended before moving on.

## Impersonation

When the user asks to impersonate someone:
1. Instruct them to navigate to `https://localhost:<port>/account/impersonate?user=<user_name>&account=<tenant_account_no>`.
2. Continue guiding them through the requested scenario while `dotnet watch` keeps running.

### Example session

```
User: watch and verify the motorbike list page works

CLI: Starting dotnet watch...
Build succeeded! Server running on https://localhost:<port>

Verification plan for the user:
- Navigate to https://localhost:<port>/vehicles
- Confirm table renders 5 motorbikes with status badges and working Edit buttons
- Report any console errors

Feature verified successfully via manual walkthrough!
```

## Browser verification checklist

When verifying a page, check:
- [ ] Page loads without errors (no 500, no exceptions in console).
- [ ] Main content displays correctly.
- [ ] Interactive elements respond (buttons, links, forms).
- [ ] Data is displayed as expected.
- [ ] No visual issues or broken layouts.

## Constraints

- Always run `dotnet watch` in background mode.
- Check build output before attempting browser verification.
- Fix errors one at a time to avoid cascading issues.
- Provide clear instructions for manual verification.
- Report clear success/failure status to the user.