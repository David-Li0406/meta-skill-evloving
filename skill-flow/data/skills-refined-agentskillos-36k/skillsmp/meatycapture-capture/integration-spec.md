# MeatyCapture Integration Spec

Design specification for integrating the meatycapture-capture skill into project workflows. Use this spec during skill deployment to configure target projects.

---

## Entry Points (Token Efficiency)

MeatyCapture provides two entry points optimized for different use cases:

| Entry Point | Use Case | Tokens | When to Use |
|-------------|----------|-------:|-------------|
| `/mc` command | list, view, search, capture, note add, update | ~150 | Simple operations (95% of use cases) |
| `meatycapture-capture` skill | batch capture, complex workflows | ~400 | Batch operations, validation, templates |

**Default to `/mc`** for all simple operations. Only invoke the full skill when you need:
- Batch capture of multiple items
- Access to workflow documentation
- Item validation via scripts
- Template-based capture

### File Structure

```
.claude/skills/meatycapture-capture/
├── SKILL.md                      # 30 lines - command router
├── skill-config.yaml             # Project defaults
├── workflows/                    # Load only when needed
│   ├── capturing.md              # Batch capture, validation
│   ├── viewing.md                # Advanced filters, output formats
│   ├── updating.md               # Status transitions
│   └── managing.md               # Project configuration
├── references/
│   ├── field-options.md          # Valid field values
│   ├── json-schemas.md           # JSON input schemas
│   └── troubleshooting.md        # Error handling
├── templates/
│   ├── quick-capture.json        # Single item template
│   └── batch-capture.json        # Multi-item template
└── scripts/
    └── validate-items.ts         # Execute-vs-load validation
```

---

## Integration Points

| Trigger | Action | Command |
|---------|--------|---------|
| Bug discovered | Capture as type:bug | `/mc capture {...}` |
| Enhancement identified | Capture as type:enhancement | `/mc capture {...}` |
| Technical debt noted | Capture as type:task | `/mc capture {...}` |
| Work started | Update status to in-progress | `meatycapture log item update DOC ITEM --status in-progress` |
| Work completed | Update status to done | `meatycapture log item update DOC ITEM --status done` |
| Item won't be fixed | Update + add note | `meatycapture log item update DOC ITEM --status wontfix` + `log note add` |
| Progress update | Add note to item | `meatycapture log note add DOC ITEM -c "..."` |

---

## CLAUDE.md Integration

Add to project's root CLAUDE.md under appropriate section:

```markdown
## Development Tracking

Use `/mc` command for quick request-log operations (token-efficient):

| Operation | Command | Example |
|-----------|---------|---------|
| List logs | `/mc list PROJECT` | `/mc list meatycapture` |
| View log | `/mc view PATH` | `/mc view ~/.meatycapture/meatycapture/REQ-20251231.md` |
| Search | `/mc search "query" PROJECT` | `/mc search "auth bug" meatycapture` |
| Quick capture | `/mc capture {...}` | `/mc capture {"title": "Fix auth", "type": "bug"}` |
| Add note | `/mc note DOC ITEM -c "text"` | `/mc note doc.md ITEM-01 -c "Fixed in PR #123"` |
| Update item | `/mc update DOC ITEM [opts]` | `/mc update doc.md ITEM-01 --status done` |

For batch capture or complex workflows, use `/meatycapture-capture` skill instead.

| When | Action |
|------|--------|
| Bug found | `/mc capture {"title": "...", "type": "bug", "domain": "..."}` |
| Enhancement idea | `/mc capture {"title": "...", "type": "enhancement"}` |
| TODO needed | Capture instead of code comment (searchable, trackable) |
| Starting logged work | `/mc update DOC ITEM --status in-progress` |
| Work complete | `/mc update DOC ITEM --status done` |
| Add context | `/mc note DOC ITEM -c "progress update..."` |

Search existing logs before creating duplicates: `/mc search "keyword" PROJECT`
```

---

## Command Integration Patterns

### Fix Commands (e.g., `/fix:fix-gh-issue`, `/fix:bugfix-commit`)

**After successful fix**, capture for future reference:

```markdown
## Follow-up (after fix merged)

If the bug warrants tracking for patterns/recurrence:
- Use `/mc capture {"title": "...", "type": "bug", "status": "done"}`
- Include: root cause, solution approach, affected files
```

### Development Commands (e.g., `/dev:implement-story`, `/dev:new-feature`)

**Before implementation**, check for related logs:

```markdown
## Context Gathering

Search request-logs for related items:
- `/mc search "feature-keyword" PROJECT`

Reference existing items when relevant to current work.
```

**After implementation**, update any related items:

```markdown
## Post-Implementation

Update status of any request-log items addressed by this work:
- `/mc update DOC ITEM --status done`
- Add resolution note: `/mc note DOC ITEM -c "Fixed in PR #XXX"`
- For workflow docs, see `./workflows/updating.md`
```

### Planning Commands (e.g., `/plan:plan-feature`, `/plan:spike`)

**During planning**, check existing logs for related items:

```markdown
## Discovery Phase

Query existing request-logs for related bugs/enhancements:
- `/mc search "type:bug" PROJECT`
- `/mc search "domain:web" PROJECT`

Incorporate relevant items into implementation plan.
```

---

## Skill Cross-References

### artifact-tracking Integration

When using `/artifact-tracking` for phase progress:

```markdown
## Task Sources

Reference request-log items in task definitions:
```yaml
tasks:
  - id: "TASK-1.1"
    source: "REQ-20251229-project-03"  # Link to request-log item
    status: "pending"
```
```

### planning Integration

When using `/planning` skill:

```markdown
## Input Sources

Include request-log search in planning discovery (use /mc for token efficiency):
- Bugs: `/mc search "type:bug status:backlog" PROJECT`
- Enhancements: `/mc search "type:enhancement" PROJECT`
```

---

## Generic Integration Patterns

For projects without specific commands, add to CLAUDE.md:

```markdown
## Request Log Workflow

### Quick Operations (use /mc - token efficient)

| Operation | Command |
|-----------|---------|
| List logs | `/mc list PROJECT` |
| View log | `/mc view PATH` |
| Search | `/mc search "keyword" PROJECT` |
| Quick capture | `/mc capture {"title": "...", "type": "bug"}` |

### Batch Operations (use skill when needed)

For batch capture of multiple items, invoke the full skill:
- Use `/meatycapture-capture` for access to templates and validation
- See `./workflows/capturing.md` for batch capture patterns

### Update (during/after work)

Update item status as work progresses:
- `/mc update DOC ITEM --status in-progress` (when starting)
- `/mc update DOC ITEM --status done` (when complete)
- `/mc note DOC ITEM -c "progress update"` (add context)
```

---

## Init Workflow

When deploying this skill to a new project:

### 1. Copy /mc Command

Copy the `/mc` command to the target project:

```bash
cp .claude/commands/mc.md TARGET_PROJECT/.claude/commands/mc.md
```

### 2. Configure skill-config.yaml

```bash
# Set project default
cat > .claude/skills/meatycapture-capture/skill-config.yaml << 'EOF'
default_project: "project-slug"
auto_detect: true
auto_create_project: true
default_path_pattern: "~/.meatycapture/{project}"
EOF
```

### 3. Add CLAUDE.md Section

Insert the "Development Tracking" section from above into the project's CLAUDE.md. Key points:
- Reference `/mc` for quick operations (token-efficient)
- Reference `/meatycapture-capture` skill for batch/complex operations
- Include example commands with project name

### 4. Identify Integration Points

Scan for existing commands/skills that should integrate:

| Pattern | Integration | Entry Point |
|---------|-------------|-------------|
| `fix/*` commands | Post-fix capture guidance | `/mc capture` |
| `dev/*` commands | Context search + status update | `/mc search` |
| `plan/*` commands | Discovery search | `/mc search` |
| `review/*` commands | Bug capture for findings | `/mc capture` |

### 5. Update Relevant Commands

For each identified command, add appropriate integration snippet from patterns above. Always prefer `/mc` for simple operations.

---

## Anti-Patterns

| Don't | Instead |
|-------|---------|
| Create TODO comments | Capture to request-log (searchable, trackable) |
| Log every minor fix | Only log patterns worth tracking |
| Duplicate existing items | Search before capture |
| Leave items in triage forever | Review and transition regularly |

---

## Validation

After init, verify integration:

```bash
# Test /mc command works (token-efficient)
/mc list PROJECT
/mc search "test" PROJECT

# Test capture works
/mc capture {"project": "test", "title": "Test", "type": "task"}

# Test project is configured
cat .claude/skills/meatycapture-capture/skill-config.yaml
```

### Token Efficiency Verification

| Entry Point | Expected Tokens | Test |
|-------------|----------------:|------|
| `/mc list` | <200 | Run command, check no skill files loaded |
| `/mc search` | <200 | Run command, check no skill files loaded |
| Skill invocation | <500 | Invoke skill, check only SKILL.md loaded |
| Full workflow | <1,500 | Load workflow file when needed |
