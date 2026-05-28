# Best Practices

## For Better PR Descriptions

1. **Write Detailed Journal Entries**
   The AI uses journal entries to explain technical decisions, so capture the rationale as you work (the skill automatically pulls entries via `mcp__plugin_foundry_foundry-mcp__journal action="list"`).

2. **Use Clear Commit Messages**
   Commit messages help explain the development flow:
   ```bash
   git commit -m "task-1-1: Implement OAuth provider classes"
   ```

3. **Review Before Approving**
   Always review the draft and ask for revisions if needed:
   ```
   "Can you emphasize the security aspects more?"
   ```

4. **Keep Specs Updated**
   Ensure spec metadata is current before completion:
   - All tasks marked completed
   - Journal entries added
   - Objectives reflect actual work
