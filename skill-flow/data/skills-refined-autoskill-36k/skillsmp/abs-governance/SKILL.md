---
name: ABS Governance
description: Agent Behavior System governance layer for AI coding agents - enforce policies, audit decisions, and maintain safe autonomy
---

# ABS Governance Skill

This skill provides governance capabilities for AI coding agents through the ABS (Agent Behavior System) framework.

## Core Concepts

### Governance Header
Every ABS-governed response includes a structured header:

```json
{"abs":{"mode":"governed","verdict":"ALLOW","policy":"antigravity_integrity","risk_score":5,"trace_id":"abc123"}}
---
{response body}
```

### Verdicts
- `ALLOW` - Operation permitted
- `DENY` - Operation blocked by policy
- `ESCALATE` - Requires human review
- `SAFE_MODE` - All operations halted (kill switch)

## Available Tools

### WAL (Write-Ahead Log)
- `abs_wal_append` - Record action in immutable audit log
- `abs_wal_verify` - Verify log integrity (hash chain)

### Runtime Control
- `abs_runtime_heartbeat` - Check runtime health
- `abs_runtime_safe_mode` - Toggle kill switch
- `abs_state_materialize` - Consolidate WAL to STATE.md

## Invariants

| ID | Rule |
|----|------|
| I1 | No state mutation without WAL entry |
| I2 | No tool execution without ABS ALLOW |
| I3 | WAL entries follow hash-chain schema |
| I4 | Kill switch halts all operations immediately |
| I5 | Hash chain verified before any read |

## Usage

### Before making changes:
```
1. Call abs_wal_append with planned action
2. Receive WAL entry ID in response header
3. Execute action only if verdict is ALLOW
```

### When something goes wrong:
```
1. Call abs_runtime_safe_mode with enabled: true
2. All subsequent operations will be blocked
3. Investigate issue
4. Call abs_runtime_safe_mode with enabled: false to resume
```

## Integration with Other Skills

This skill works as a **governance layer** above other skills:
- Security skills → ABS enforces their recommendations
- Agent skills → ABS audits their decisions
- Development skills → ABS validates code changes

## Best Practices

1. **Always check the governance header** in tool responses
2. **Log all significant actions** to WAL before executing
3. **Use ESCALATE** for high-risk operations
4. **Enable safe mode** when debugging critical issues
5. **Verify WAL periodically** to detect tampering
