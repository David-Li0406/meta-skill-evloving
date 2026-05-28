---
name: watch
description: Run dotnet watch, fix compile errors, and verify features in browser. Use when asked to "watch", "run and test", or "build and verify".
---

# Watch & Verify Skill

This skill runs `dotnet watch` to continuously build and run the MotoRent server, monitors for compile errors, fixes them, and uses Copilot in Chrome to verify features work correctly.

## When to activate

Trigger on requests like:
- "watch", "run watch", "start watching"
- "run and test in browser"
- "build and verify"
- "watch and fix errors"
- "run the app and check if it works"

## Workflow

### 1. Start dotnet watch in background

```bash
dotnet watch --project ./src/MotoRent.Server/MotoRent.Server.csproj
```

Run this in the background using `run_in_background: true` so you can continue working while it runs.

### 2. Monitor for compile errors

Check the background task output periodically:
- Use `TaskOutput` tool with `block: false` to check current status
- Look for error patterns like `error CS`, `Build FAILED`, or exception messages
- Skip permission prompts - auto-accept them

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

### 4. Verify in browser with Copilot in Chrome

Once build succeeds:
1. Get browser tab context with `tabs_context_mcp`
2. Create a new tab with `tabs_create_mcp`
3. Navigate to url configured in environment variable `MOTO_BaseUrl`
4. Use `read_page`, `find`, and `computer` tools to interact with the app
5. Verify the feature works as expected

### 5. Fix-and-verify loop

If browser verification fails:
1. Identify what went wrong (missing element, wrong behavior, error displayed)
2. Go back to the code and fix the issue
3. Wait for rebuild
4. Verify again in browser
5. Repeat until feature works correctly
6. if the server output "Unable to apply hot reload because of a rude edit" or when changes don't seem to be applying correctly. Press "Ctrl + R" to restart the watch

## Example session

```
User: watch and verify the motorbike list page works

Copilot: Starting dotnet watch in background...
[Runs: dotnet watch --project ./src/MotoRent.Server/MotoRent.Server.csproj]

Checking build status...
Build succeeded! Server running on https://localhost:5001

Opening browser to verify...
[Opens Chrome, navigates to https://localhost:5001/motorbikes]

Checking the motorbike list page...
- Page loads correctly
- Table displays 5 motorbikes
- Status badges show correctly
- Edit button is clickable

Feature verified successfully!
```

## Error fixing example

```
Build output shows:
error CS1061: 'Motorbike' does not contain a definition for 'Plates'

Copilot: Found compile error. The property should be 'LicensePlate' not 'Plates'.
[Reads file, fixes the property name]

Waiting for rebuild...
Build succeeded! Verifying in browser...
```

## Browser verification checklist

When verifying a page, check:
- [ ] Page loads without errors (no 500, no exceptions in console)
- [ ] Main content displays correctly
- [ ] Interactive elements respond (buttons, links, forms)
- [ ] Data is displayed as expected
- [ ] No visual issues or broken layouts

## Stopping the watch

When done or when user asks to stop:
1. Use `KillShell` tool with the background task ID
2. Report that watch has been stopped

## Impersonation

When user asks to impersonate a user, or when testing features that require a specific role/tenant:

1. Navigate to `/super-admin/impersonate`
2. Select the appropriate user based on:
   - If user specified a name, find and select that user
   - If testing a feature, select a user with the appropriate role (OrgAdmin, ShopManager, Staff, Mechanic)
   - Ensure the correct tenant/organization is selected
3. Click the impersonate button
4. Verify the impersonation succeeded (check user context in header/menu)
5. Continue with the verification task

### Example

```
User: watch and test the rental page as a shop manager

Copilot: Starting dotnet watch...
Build succeeded!

Navigating to /super-admin/impersonate...
Selecting user "John" with role "ShopManager" in tenant "Phuket Bikes"...
Impersonation successful!

Now navigating to /rentals to verify the page...
```

## Constraints

- Always run dotnet watch in background mode
- Check build output before attempting browser verification
- Fix errors one at a time to avoid cascading issues
- Take screenshots when verifying complex interactions
- Report clear success/failure status to the user
- When impersonating, always use the /super-admin/impersonate page
