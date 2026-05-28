<workflow name="set-focus">
<required_reading>
**Read if unfamiliar with bd commands:**
1. references/beads-commands.md - bd CLI reference
</required_reading>

<objective>Set current focus (only one at a time).</objective>

<steps>
1. Check existing focus:
   ```bash
   bd list --label focus --json
   ```
2. If focus exists, remove label:
   ```bash
   bd update <old-id> --remove-label focus --json
   ```
3. Set new focus:
   - For existing bead:
     ```bash
     bd update <id> --add-label focus --json
     ```
   - For new item:
     ```bash
     bd create "<description>" -t task -p 2 -l focus,layton --json
     ```
</steps>

<constraint>
CRITICAL: Only ONE bead should have `focus` label at any time.
Always remove focus from previous item before setting new focus.
</constraint>

<success_criteria>

- Only ONE bead has `focus` label
- Previous focus label removed (if any)
</success_criteria>
</workflow>
