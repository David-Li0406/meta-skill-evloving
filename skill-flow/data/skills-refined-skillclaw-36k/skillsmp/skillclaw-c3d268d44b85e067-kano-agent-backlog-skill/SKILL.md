---
name: kano-agent-backlog-skill
description: Use this skill for local-first, multi-product backlog management with agent collaboration discipline.
---

# Skill body

## 🎯 Quick Start

This skill provides **local-first, multi-product backlog management** with agent collaboration discipline.

## Essential Reading

### 1. **Overview and Core Concepts**
   - Read: [Purpose](../../../skills/kano-agent-backlog-skill/SKILL.md#purpose)
   - Read: [Core Concepts](../../../skills/kano-agent-backlog-skill/SKILL.md#core-concepts)

### 2. **CLI Commands**
   - Reference: [CLI Reference](../../../skills/kano-agent-backlog-skill/SKILL.md#cli-reference)
   - Bootstrap: 
     ```bash
     kano-backlog admin init --product <name> --agent <id>
     ```
   - Create item: 
     ```bash
     kano-backlog workitem create --type Task --title "..." --agent <id>
     ```
   - Update state: 
     ```bash
     kano-backlog workitem update-state <ID> --state Done --agent <id>
     ```
   - Refresh views: 
     ```bash
     kano-backlog view refresh --agent <id>
     ```

### 3. **Workflows and Discipline**
   - Read: [Agent Workflows](../../../skills/kano-agent-backlog-skill/SKILL.md#agent-workflows)
   - Read: [Backlog Discipline](../../../skills/kano-agent-backlog-skill/SKILL.md#backlog-discipline)

## Common Tasks

### Create a New Work Item
```bash
python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem create \
  --type Task \
  --title "Implement feature X" \
  --product kano-agent-backlog-skill \
  --agent <agent_id>
```

### Update Item State
```bash
python skills/kano-agent-backlog-skill/scripts/kano-backlog workitem update-state <ID> \
  --state InProgress \
  --agent <agent_id>
```

## Installation
```bash
cd skills/kano-agent-backlog-skill
pip install -e .
```

## References

| Topic | Link |
|-------|------|
| **Full Documentation** | [`SKILL.md`](../../../skills/kano-agent-backlog-skill/SKILL.md) |
| **CLI Reference** | [`SKILL.md#cli-reference`](../../../skills/kano-agent-backlog-skill/SKILL.md#cli-reference) |
| **Architecture ADRs** | [`decisions/`](../../../_kano/backlog/products/kano-agent-backlog-skill/decisions/) |