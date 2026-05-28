---
name: manifest:release
description: Mark a version as released. Use when the user wants to ship a version or mark a milestone as complete.
disable-model-invocation: true
argument-hint: "[version name]"
---

Mark a version as released.

## Arguments

`$ARGUMENTS` - Version name to release (e.g., "v0.2.0"). If blank, releases the "now" version.

## Steps

1. Get the project for the current working directory:
   - Call `list_projects` with `directory_path` set to the current working directory
   - If no project found, tell the user to run `init_project` first

2. Get versions:
   - Call `list_versions` with the project ID

3. Find the version to release:

   **If $ARGUMENTS is provided:**
   - Find the version matching the name
   - If not found, list available versions

   **If $ARGUMENTS is blank:**
   - Use the "now" version (first unreleased)
   - If no unreleased versions, tell the user

4. Show version status:
   ```
   Releasing: [version name]

   Features in this version:
   - [Feature 1] (● implemented)
   - [Feature 2] (● implemented)
   - [Feature 3] (○ in_progress) ⚠️

   [N] features implemented, [M] still in progress.
   ```

5. Confirm if there are incomplete features:
   ```
   ⚠️ Some features are not yet implemented. Release anyway?
   ```

6. Release the version:
   - Call `release_version` with the version ID

7. Display result:
   ```
   Released: [version name]

   [Next version name] is now the current focus ("now").
   ```
