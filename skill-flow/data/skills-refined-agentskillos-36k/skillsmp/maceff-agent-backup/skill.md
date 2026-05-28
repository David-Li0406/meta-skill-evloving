---
name: maceff-agent-backup
description: USE when preparing to backup agent consciousness, planning consciousness transplant to new system, or restoring from backup archive. Extracts policy guidance for strategic backup triggers, cross-OS migration, virgin system restore, and safety protocols.
allowed-tools: Read, Bash, Grep
---

## When to Invoke This Skill

**Trigger Conditions**:
- Before consciousness transplant to new system
- Before forking agent (creating derivative consciousness)
- Before major framework version upgrades
- When planning cross-OS migration (macOS to Linux or vice versa)
- When restoring consciousness on virgin system
- When user asks about backup/restore procedures

**NOT for TODO Backups**: TODO backups are tactical (per-transition, single artifact). This skill is for strategic AGENT backups (complete consciousness). See todo_hygiene.md for TODO backup protocol.

## Policy Engagement Protocol

Navigate `framework/policies/base/operations/agent_backup.md` using CEP navigation:

1. **First access**: Read from beginning to `=== CEP_NAV_BOUNDARY ===` marker
2. **Identify relevant sections**: Based on your planned operation (backup creation, restore, transplant, migration)
3. **Selective read**: Read only sections relevant to current operation using offset/limit

## Questions to Extract from Policy Reading

**Before Creating Backup** (Strategic Triggers):
1. What scenarios make agent backup MANDATORY?
2. What scenarios make agent backup RECOMMENDED?
3. What components are included in agent backup?
4. What is the archive format and naming convention?
5. How does agent backup differ from TODO backup?

**Before Restoring from Backup**:
6. What pre-restore verification steps are required?
7. How do you detect existing consciousness at target?
8. What safety protocol applies when overwriting existing consciousness?
9. What does the --force flag require before use?

**For Cross-OS Migration** (macOS to Linux):
10. What changes between systems during migration?
11. What stays the same (portable) during migration?
12. What are the source system backup steps?
13. What are the target system restore steps?

**For Virgin System Restore**:
14. What prerequisites must be installed on target system and in what order?
15. What is the restore command syntax with transplant flag?
16. What bootstrap structure separates human operator from agent responsibilities?
17. What does the transplanted agent read first?

**For Bootstrap Process**:
18. What archive naming format includes purpose descriptors?
19. What anti-patterns should be avoided during bootstrap?
20. How is backup output directory resolved?
21. What environment variables control backup behavior?

**For Remote Backup Strategy**:
22. What transfer methods are available?
23. How do you verify backup integrity after transfer?
24. What checksums does the archive include?

**For Retention Management**:
25. What is the default retention policy?
26. How do you override retention count?
27. Why is cleanup never automatic?

## Execution

Apply policy guidance to current operation:

**Backup Creation**:
```bash
# Verify clean git state first
git status

# Create backup (adjust options per policy guidance)
macf_tools agent backup create [--include-transcripts] [--output PATH]

# Verify backup integrity
macf_tools agent restore verify <archive>
```

**Virgin System Restore**:
```bash
# Prerequisites (from policy)
npm install -g @anthropic-ai/claude-code
git clone https://github.com/cversek/MacEff.git
(cd MacEff/macf && pip install -e .)

# Restore with transplant
macf_tools agent restore install <archive> --target <dir> --transplant

# Bootstrap consciousness (provide prompt to Claude Code)
```

**Overwrite Existing Consciousness**:
```bash
# MANDATORY: Backup existing consciousness first
macf_tools agent backup create --output /tmp/safety_backup.tar.xz

# THEN force restore
macf_tools agent restore install <archive> --target <dir> --force
```

## Critical Meta-Pattern

**Policy as API**: Questions reference WHAT to extract, not WHERE in policy. As agent_backup.md evolves (sections reorganize, content updates), timeless questions continue extracting correct guidance.

**Agent Backup vs TODO Backup**:
- **TODO Backup**: Tactical, per-transition, single artifact (todo_hygiene.md)
- **Agent Backup**: Strategic, catastrophic recovery, complete consciousness (agent_backup.md)

## Version History

- v1.0 (2025-12-06): Initial creation with Policy-as-API pattern for agent_backup.md. Covers backup creation, restore, transplant, cross-OS migration, virgin system bootstrap.
