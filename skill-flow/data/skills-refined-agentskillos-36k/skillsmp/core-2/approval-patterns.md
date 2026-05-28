# Human Approval Patterns for PAI

**Factor 7 Compliance:** Contact Humans with Tool Calls

This document defines when and how PAI agents should request human approval for high-stakes operations.

---

## When to Request Approval

### HIGH-STAKES (ALWAYS require blocking approval)

These operations are irreversible or have significant consequences:

| Operation | Pattern | Risk |
|-----------|---------|------|
| Force push | `git push.*--force` | Rewrites history |
| Delete recursively | `rm -rf` on directories | Data loss |
| Production deployment | `deploy prod`, `kubectl apply -n production` | Service impact |
| Database destructive | `DROP`, `TRUNCATE`, `DELETE FROM.*WHERE 1` | Data loss |
| Credential rotation | API key, secret changes | Access disruption |
| Public repository ops | Push to public repos from private | Data exposure |
| System config changes | `chmod 777`, `/etc/` modifications | Security |

### MEDIUM-STAKES (Request input, proceed cautiously)

These operations benefit from human review but aren't strictly blocking:

| Operation | Pattern | Risk |
|-----------|---------|------|
| Major version upgrades | `npm install pkg@major` | Breaking changes |
| Architecture decisions | New patterns, refactoring | Technical debt |
| External API calls with cost | Paid APIs, cloud resources | Cost |
| Branch operations | `git branch -D`, forced checkout | Work loss |

### LOW-STAKES (Log but don't block)

These operations are safe but should be audited:

- File modifications within project
- Local git operations (commit, branch, merge)
- Read-only API calls
- Test execution

---

## Implementation Patterns

### Pattern 1: AskUserQuestion for Blocking Approval

Use Claude Code's native AskUserQuestion tool for synchronous approval:

```typescript
// Before destructive operation
const approval = await AskUserQuestion({
  questions: [{
    question: "This operation will permanently delete the database. Proceed?",
    header: "Approval",
    options: [
      { label: "Approve", description: "Execute DROP DATABASE command" },
      { label: "Deny", description: "Cancel operation and explain concerns" }
    ],
    multiSelect: false
  }]
});

// Check response and proceed or abort
```

### Pattern 2: PreToolUse Hook Detection

Add patterns to `.claude/hooks/pre-tool-use-security.ts` to detect dangerous operations:

```typescript
const DANGEROUS_PATTERNS = [
  { pattern: /rm\s+-rf\s+[\/~]/, risk: "recursive delete from root/home" },
  { pattern: /git\s+push.*--force/, risk: "force push" },
  { pattern: /DROP\s+(DATABASE|TABLE)/i, risk: "database destruction" },
  { pattern: /chmod\s+777/, risk: "world-writable permissions" },
  { pattern: /curl.*\|\s*(ba)?sh/, risk: "remote code execution" },
];

// Return "REQUIRE_APPROVAL" to trigger human review
```

### Pattern 3: Explicit Confirmation in Commands

Add explicit approval steps in command workflows:

```markdown
## Before Deployment

IMPORTANT: This command will deploy to production. Before proceeding:

1. Verify all tests pass
2. Review the changes being deployed
3. Confirm with the user using AskUserQuestion:
   - "Ready to deploy these changes to production?"
   - Options: "Deploy", "Review changes first", "Cancel"
```

---

## Approval Workflow Architecture

```
Agent Action
    ↓
PreToolUse Hook
    ↓ (pattern match?)
    ├─ No  → Execute normally
    └─ Yes → Dangerous pattern detected
              ↓
        AskUserQuestion
              ↓
        ┌─────┴─────┐
        ↓           ↓
    Approved     Denied
        ↓           ↓
    Execute     Abort + Log
```

---

## Integration with PAI Hooks

### settings.json Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "${PAI_DIR}/hooks/pre-tool-use-security.ts"
        }]
      }
    ]
  }
}
```

### Hook Response Protocol

The security hook should output one of:
- `APPROVED` - Proceed with operation
- `REQUIRE_APPROVAL` - Block and request human approval
- `BLOCKED` - Deny outright (e.g., matches deny list)

---

## Audit Trail

All approval decisions should be logged to `thoughts/memory/approvals.jsonl`:

```json
{
  "timestamp": "2026-01-10T12:00:00Z",
  "session_id": "abc123",
  "operation": "git push --force origin main",
  "pattern_matched": "force push",
  "decision": "approved",
  "decided_by": "user",
  "context": "Fixing corrupted history after rebase"
}
```

---

## Examples

### Example 1: Force Push Prevention

```
Agent: I need to force push to fix the branch.

[PreToolUse hook detects "git push --force"]

Agent: This operation will force push to the remote branch, which could
overwrite others' work.

[AskUserQuestion]
Question: "Approve force push to origin/feature-branch?"
Options:
  - "Approve" - I understand the risks
  - "Deny" - Find another approach

User: [Selects Approve]

Agent: [Executes force push, logs approval]
```

### Example 2: Database Deletion

```
Agent: Cleaning up the test database.

[PreToolUse hook detects "DROP DATABASE"]

Agent: [BLOCKED - Production database patterns always require approval]

[AskUserQuestion]
Question: "This will permanently delete the database. Proceed?"
Options:
  - "Approve" - Yes, delete the database
  - "Deny" - Cancel this operation

User: [Selects Deny with reason: "Wrong database, should be test_db"]

Agent: Operation cancelled. Which database should I target instead?
```

---

## Best Practices

1. **Fail Safe**: When in doubt, ask for approval
2. **Clear Context**: Always explain what the operation will do
3. **Audit Everything**: Log all approval decisions
4. **Respect Denials**: Never retry a denied operation without new context
5. **Batch Carefully**: For bulk operations, consider requesting approval once with a summary

---

## Related Documents

- `security-protocols.md` - Repository safety and key handling
- `checkpoint-protocol.md` - Rollback capabilities
- `hooks-guide.md` - Hook system documentation
