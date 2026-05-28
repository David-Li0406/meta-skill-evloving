# Session Persistence Pattern

> **Pattern**: Memory persistence using SessionStart/PreCompact/Stop hooks
> **State File**: `${CLAUDE_PROJECT_DIR}/.claude/TOOLKIT_STATE.md`
> **Use Case**: Plugin development workflow - persist decisions across sessions

## Pattern Overview

**Problem**: Claude Code sessions are saved locally but don't provide "persistent memory" for plugin development decisions like manifest choices, naming conventions, and open validation issues.

**Solution**: Use hooks to save/load session state to a canonical file that persists across sessions.

**Implementation**:
- **SessionStart**: Load existing state and inject as `additionalContext`
- **Stop**: Incremental state save after each response
- **PreCompact**: Critical save before context compaction

---

## State Schema

### TOOLKIT_STATE.md Structure

```markdown
# Plugin Development Session State

> **Auto-generated** by meta-plugin-manager memory persistence hooks
> **Last updated**: [ISO 8601 timestamp]

## Session Metadata
- **Session ID**: `abc123...`
- **Project Path**: `/path/to/plugin`
- **Working Plugin**: `plugin-name` (if set)

---

## Manifest Decisions

### Plugin Configuration
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "type": "toolkit",
  "description": "..."
}
```

**Decision Rationale**: Brief explanation of choices made

---

## Naming Decisions

### Skills
| Component | Name | Status | Notes |
|-----------|------|--------|-------|
| Skill 1 | `data-validator` | ✅ Created | Progressive disclosure with 2 references |
| Skill 2 | `api-integrator` | 🚧 Pending | Depends on MCP architecture |

### Commands
| Component | Name | Status | Notes |
|-----------|------|--------|-------|
| (none) | - | - | - |

**Naming Convention Applied**: `kebab-case`, gerund form for skills

---

## Open Validation Issues

### High Priority
- [ ] **plugin.json**: Missing `repository` field
- [ ] **skill-name/SKILL.md**: URL validation section missing

### Medium Priority
- [ ] **Architecture**: Consider MCP for external API calls
- [ ] **Progressive Disclosure**: SKILL.md exceeds 500 lines, consider references/

### Low Priority
- [ ] **Documentation**: Add examples/ directory with usage samples

---

## Architecture Decisions

### Chosen Patterns
- **Skills-First**: ✅ Primary interface
- **Hub-and-Spoke**: ✅ toolkit-architect routes to domain experts
- **Context Fork**: ✅ toolkit-worker for noisy analysis

### Rejected Alternatives
- **Command Wrapper Pattern**: Rejected - causes metadata bloat
- **Global Hooks**: Rejected - prefer component-scoped hooks

---

## Quality Metrics

### Current Quality Score: 7.5/10
- Structural (30%): 8/10
- Components (50%): 7/10
- Standards (20%): 8/10

### Target: ≥ 8/10
```

---

## Hook Implementation

### SessionStart Hook

**Purpose**: Load existing state and inject as context

**Configuration**:
```json
{
  "SessionStart": [{
    "matcher": "startup|resume|clear|compact",
    "hooks": [{
      "type": "command",
      "command": "\"${CLAUDE_PLUGIN_ROOT}\"/hooks/scripts/session-start.sh",
      "timeout": 10
    }]
  }]
}
```

**Script Output** (JSON):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "[STATE_FILE_CONTENT or 'No previous state found']"
  }
}
```

**Matcher Options**:
- `startup` - Initial session start
- `resume` - Session resumed with `--resume` or `--continue`
- `clear` - After `/clear` command
- `compact` - After auto or manual compact

### Stop Hook

**Purpose**: Incremental state save after each response

**Configuration**:
```json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "\"${CLAUDE_PLUGIN_ROOT}\"/hooks/scripts/stop-save.sh",
      "timeout": 10
    }]
  }]
}
```

**Behavior**:
- Runs when Claude finishes responding
- Does NOT run if stoppage was due to user interrupt
- Calls `update-state.py` to extract and save state

### PreCompact Hook

**Purpose**: Critical save before context compaction

**Configuration**:
```json
{
  "PreCompact": [{
    "matcher": "manual|auto",
    "hooks": [{
      "type": "command",
      "command": "\"${CLAUDE_PLUGIN_ROOT}\"/hooks/scripts/precompact-save.sh",
      "timeout": 10
    }]
  }]
}
```

**Matcher Options**:
- `manual` - Invoked from `/compact`
- `auto` - Automatic compaction due to full context window

**Behavior**:
- Runs BEFORE compaction occurs
- Ensures state is saved before context loss
- Same state extraction as Stop hook

---

## State Extraction Logic

### update-state.py

**Purpose**: Parse transcript and update TOOLKIT_STATE.md

**Input**: JSON via stdin with session metadata

**Output**: None (silent success)

**Extraction Patterns**:

1. **Manifest Decisions**: Extract from `plugin.json` edits
   - Parse Edit/Write tool calls targeting `plugin.json`
   - Capture decision rationale from conversation context

2. **Naming Decisions**: Extract from component creation
   - Parse skill creation outputs (`## Skill Created: {name}`)
   - Parse subagent creation outputs
   - Track naming conventions applied

3. **Validation Issues**: Extract from audit outputs
   - Parse audit result patterns
   - Track priority levels (High/Medium/Low)
   - Extract issue descriptions and file locations

4. **Architecture Decisions**: Extract from conversation
   - Parse chosen patterns (skills-first, hub-and-spoke, context fork)
   - Track rejected alternatives with rationale
   - Extract from toolkit-architect decisions

5. **Quality Metrics**: Extract from audit scores
   - Parse overall quality score
   - Extract structural/component/standards breakdown
   - Track improvement over time

---

## Integration Patterns

### During Plugin Creation

When `toolkit-architect` creates a plugin:

1. **Initialize State**: Create TOOLKIT_STATE.md with template
2. **Record Manifest**: Capture plugin.json decisions as made
3. **Track Naming**: Record component names and conventions
4. **Document Architecture**: Note chosen patterns and rejections

### During Plugin Audit

When `toolkit-architect` audits a plugin:

1. **Load State**: Read existing TOOLKIT_STATE.md (if exists)
2. **Append Issues**: Add validation issues found during audit
3. **Update Metrics**: Refresh quality scores
4. **Generate Report**: Output includes state context

### During Plugin Refinement

When `toolkit-architect` refines a plugin:

1. **Load State**: Read existing TOOLKIT_STATE.md
2. **Update Decisions**: Modify architecture decisions section
3. **Mark Resolved**: Remove fixed validation issues
4. **Update Metrics**: Refresh quality scores after improvements

---

## Anti-Patterns

### DON'T: Create Separate State Management Skill

**Why**: Creates unnecessary fragmentation

**Correct**: Embed state protocol knowledge in `hooks-knowledge/references/session-persistence.md`

### DON'T: Use SessionEnd for State Save

**Why**: SessionEnd runs on termination; may miss last saves if session crashes

**Correct**: Use Stop (after each response) + PreCompact (before compaction)

### DON'T: Store State in Plugin Root

**Why**: Clutters plugin directory with session-specific files

**Correct**: Use `.claude/TOOLKIT_STATE.md` (project-local, git-ignored)

### DON'T: Parse Entire Transcript Every Time

**Why**: Expensive for long sessions

**Correct**: Parse incrementally - only new entries since last save

---

## Best Practices

### State File Management

- ✅ Create state file on first session
- ✅ Update incrementally (don't rewrite entire file)
- ✅ Add to `.gitignore` (session-specific, not project code)
- ✅ Use markdown format (human-readable)
- ✅ Include timestamps for each update

### Hook Performance

- ✅ Keep hooks fast (<10 seconds)
- ✅ Use command hooks (deterministic, fast)
- ✅ Set appropriate timeouts
- ✅ Return JSON output for SessionStart
- ✅ Silent exit (0) for Stop/PreCompact

### State Format

- ✅ Use markdown (human-readable)
- ✅ Include timestamps
- ✅ Structure with clear sections
- ✅ Use tables for structured data
- ✅ Include rationale for decisions

---

## Example Integration

### toolkit-architect create action

```
1. Initialize TOOLKIT_STATE.md with template
2. Prompt: "What type of plugin are you creating?"
3. User: "A toolkit for API testing"
4. Record: Manifest decision - type: "toolkit"
5. Prompt: "What should we name the main skill?"
6. User: "http-validator"
7. Record: Naming decision - skill: "http-validator", gerund form
8. Continue with creation...
9. Stop hook fires: Save state with all decisions
```

### toolkit-architect audit action

```
1. Load: TOOLKIT_STATE.md (contains previous decisions)
2. Run audit workflow
3. Found issue: Missing URL validation section
4. Record: High priority - http-validator/SKILL.md missing URL section
5. Found issue: No progressive disclosure
6. Record: Medium priority - merge SKILL.md or add references/
7. Stop hook fires: Save state with new issues
```

---

## Troubleshooting

### State Not Loading

**Symptoms**: Session starts without previous state

**Solutions**:
1. Verify hooks.json is registered (`/hooks` command)
2. Check script permissions (`chmod +x hooks/scripts/*.sh`)
3. Test session-start.sh manually with stdin input
4. Check .claude/ directory exists and is writable

### State Not Saving

**Symptoms**: Changes not persisting between sessions

**Solutions**:
1. Verify .claude/ directory exists and is writable
2. Check update-state.py is executable
3. Test stop-save.sh manually with JSON input
4. Verify transcript_path is passed correctly

### State Corrupted

**Symptoms**: Parse errors, malformed state

**Solutions**:
1. Delete TOOLKIT_STATE.md
2. Restart session (will recreate from template)
3. Implement backup/rotation in future

### Hook Not Triggering

**Symptoms**: Hooks not firing at expected times

**Solutions**:
1. Run `/hooks` to verify registration
2. Check plugin.json has `"hooks": "hooks/hooks.json"`
3. Verify event names match exactly (case-sensitive)
4. Test with simple hook first (echo command)

---

## Related Documentation

- **Hooks Guide**: https://code.claude.com/docs/en/hooks
- **Plugin Architecture**: https://code.claude.com/docs/en/plugins
- **Session Lifecycle**: hooks-knowledge SKILL.md (Session Management section)
- **Progressive Disclosure**: skills-knowledge SKILL.md

---

## Implementation Checklist

- [ ] Create hooks/hooks.json with SessionStart/Stop/PreCompact configuration
- [ ] Implement hooks/scripts/session-start.sh (load + inject)
- [ ] Implement hooks/scripts/stop-save.sh (incremental save)
- [ ] Implement hooks/scripts/precompact-save.sh (pre-compaction save)
- [ ] Implement hooks/scripts/update-state.py (transcript parsing)
- [ ] Add hooks reference to plugin.json
- [ ] Update hooks-knowledge/SKILL.md with session persistence section
- [ ] Update hooks-architect/SKILL.md with routing to session-persistence.md
- [ ] Update toolkit-architect/SKILL.md with state management in actions
- [ ] Test SessionStart loads state correctly
- [ ] Test Stop saves after responses
- [ ] Test PreCompact saves before compaction
- [ ] Add .claude/TOOLKIT_STATE.md to .gitignore
