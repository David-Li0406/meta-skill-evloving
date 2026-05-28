# Artifact Prune Checklist

Monthly (or per release) checklist for pruning stale Copilot artifacts to maintain discoverability and reduce tool overload.

## When to Run

- Monthly artifact review
- Before major releases
- When artifact count becomes unwieldy
- When prompts/skills show low usage

## Prune Checklist

### Prompts (`.github/prompts/`)

- [ ] **Identify unused prompts**: Check if prompt has been used in past 30 days
- [ ] **Mark for deprecation**: Add `[DEPRECATED]` to description
- [ ] **Update references**: Update any agents/skills that referenced the prompt
- [ ] **Remove after grace period**: Delete after 1-2 releases if still unused

### Skills (`.github/skills/`)

- [ ] **Identify outdated skills**: Check if skill matches current patterns
- [ ] **Verify references valid**: Ensure SSOT links still point to correct files
- [ ] **Update or deprecate**: Fix or mark as deprecated
- [ ] **Remove stale skills**: Delete skills that no longer match workflow

### Agents (`.github/agents/`)

- [ ] **Review tool lists**: Reduce tool lists that have grown too large
- [ ] **Check handoff targets**: Verify handoff agents still exist
- [ ] **Update role descriptions**: Ensure descriptions match current responsibilities
- [ ] **Consolidate duplicates**: Merge agents with overlapping responsibilities

### Instructions (`.github/instructions/`)

- [ ] **Check for drift**: Verify instructions match codebase reality
- [ ] **Remove duplicates**: Ensure no rules are scattered across multiple files
- [ ] **Update SSOT links**: Fix broken references in skills/prompts

## Deprecation Protocol

### Step 1: Mark as Deprecated

Add to artifact's description:

```yaml
description: "[DEPRECATED - use X instead] Original description..."
```

### Step 2: Update References

Search for usages:

```bash
# Find references to a prompt
grep -r "prompt-name" .github/

# Find references to a skill
grep -r "skill-name" .github/

# Find handoff references to an agent
grep -r "agent-name" .github/agents/
```

### Step 3: Grace Period

- Keep artifact functional for 1-2 releases
- Monitor if anyone still uses it
- Communicate deprecation to team

### Step 4: Remove

- Delete the artifact file(s)
- Update manifest.json (if OS artifact)
- Run validation to ensure nothing breaks

## Tool List Reduction

When agent tool lists grow too large:

1. **Audit current tools**: List all tools in agent
2. **Identify lane defaults**: Check lane-playbooks for recommended tools
3. **Apply least-privilege**: Remove tools not essential for role
4. **Test functionality**: Verify agent still works with reduced tools

### Recommended Tool Limits

| Agent Type | Max Tools | Focus |
|------------|-----------|-------|
| Orchestrator | 4 | read, search, todo, edit (plans only) |
| Leads | 5 | read, search, edit (specs), execute optional |
| Implementers | 5 | read, search, edit, execute, tests |
| QA | 5 | read, search, edit, execute, tests |
| Security Reviewer | 2 | read, search (read-only) |

## Prune Report Template

```
ARTIFACT PRUNE REPORT

Date:
Release:

Prompts reviewed: X
- Deprecated: [list]
- Removed: [list]

Skills reviewed: X
- Updated: [list]
- Deprecated: [list]
- Removed: [list]

Agents reviewed: X
- Tool lists reduced: [list]
- Handoffs updated: [list]

Instructions reviewed: X
- Drift tickets created: [list]
- Updated: [list]

Actions for next cycle:
-
```

## Validation After Prune

```bash
# Validate OS artifacts (if applicable)
make agent.os.check

# Check for broken references
grep -r "DEPRECATED" .github/
```

## SSOT Reference

- Prune protocol: [KYORA_AGENT_OS.md#L1066-L1079](../../../KYORA_AGENT_OS.md#L1066-L1079)
