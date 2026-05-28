# Agent Centric

Framework for agent-centric development with AGD (Agent-centric Governance Decision) tracking.

## What is AGD?

AGD (Agent-centric Governance Decision) is a decision record mechanism, similar to ADR or RFC. Each AGD has a unique number (e.g., AGD-001) that records important decisions, rationale, and impact.

Unlike traditional ADRs that focus solely on architecture, AGD covers **any important decision**:

- Design patterns and conventions
- Tool and library choices
- Process decisions
- API contracts
- Team agreements

Decisions can be **updated** (extended) or **obsoleted** (replaced) by later decisions, but original files are preserved, forming a complete decision history.

## Installation

```bash
# From the claude-skills directory
./scripts/install.sh skills agent-centric
```

## Quick Start

1. **Initialize** - The skill auto-initializes on first load, creating:
   - `.agents/decisions/` - Decision storage
   - `.agents/scripts/` - Skill scripts
   - `.agents/config.json` - Configuration file

2. **Define tags** - Add allowed tags to `.agents/config.json`:

   ```json
   {
     "tags": ["core", "auth", "api", "database"]
   }
   ```

3. **Create a decision** - Ask Agent or manually create AGD files:

   ```
   .agents/decisions/AGD-001_use-postgresql.md
   ```

4. **Automatic validation** - Hooks run automatically:
   - PreToolUse validates tags before creation
   - PostToolUse validates files and regenerates indexes

## Script Auto-Update

Scripts in `.agents/scripts/` are automatically synced from the skill directory on each load.

To disable auto-update for specific scripts:

```json
{
  "disableAutoUpdateScripts": ["validate-agds.py"]
}
```

To disable all script updates:

```json
{
  "disableAutoUpdateScripts": true
}
```

## Acknowledgments

Inspired by [caoer](https://github.com/caoer).
