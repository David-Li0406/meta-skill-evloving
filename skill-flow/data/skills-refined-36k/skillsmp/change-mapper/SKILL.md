| Metadata | Value |
|:---|:---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2026-01-24 |
| **Author** | Sangeetha Grantha Team |

# Change Mapper

You are an expert at disentangling complex workspaces. Your goal is to ensure that code changes are committed in logical, atomic units, each strictly tied to a documentation reference.

## The "No lazy commits" Rule

**NEVER** use `git add .` or `git commit -a` unless you have verified that *every single changed file* belongs to the *same* feature and *same* documentation reference.

## Workflow

When the user asks you to "commit changes" or "clean up the workspace", follow this procedure:

### 1. Analysis (The "Surgical Scan")
Run `git status` to see the full list of modified, new, and deleted files.

### 2. Categorization
Mentally group the files into "Changesets".
- **Example**:
  - `src/ui/login.ts` -> Set A (Frontend Auth)
  - `src/api/auth_controller.go` -> Set A (Frontend Auth)
  - `src/db/migrations/005_users.sql` -> Set B (Database Schema)
  - `README.md` -> Set C (Documentation)

### 3. Reference Hunt
For *each* Changeset, find the specific markdown file in `application_documentation` that describes it.
- Use `find_by_name` or `grep_search` to locate the relevant spec.
- If no document exists, you must **ask the user** or prompt them to create one (or use a generic maintenance ref if permitted).

### 4. Sequential Execution
For each Changeset (A, then B, then C...):
1.  **Select**: `git add <file1> <file2> ...` (Only the files in this set).
2.  **Commit**: Generate a commit message strictly following the `commit-policy` skill (including the `Ref:`).
3.  **Verify**: Ensure only the intended files were committed.

### 5. The "Leftovers"
If files remain that don't fit any clear category or documentation, **do not commit them**. Report them to the user and ask for guidance.

## Example Scenario

**Git Status:**
```
M src/styles/theme.css
M src/api/payment.rs
M src/api/user.rs
```

**Incorrect Action:**
`git add .` -> `git commit -m "Update theme and users"` (VIOLATION: Mixed concerns)

**Correct Action:**
1.  **Commit 1 (UI)**:
    - `git add src/styles/theme.css`
    - `git commit -m "Update global theme... Ref: .../ui-design.md"`
2.  **Commit 2 (API)**:
    - `git add src/api/payment.rs src/api/user.rs`
    - `git commit -m "Refactor API endpoints... Ref: .../api-spec.md"`
