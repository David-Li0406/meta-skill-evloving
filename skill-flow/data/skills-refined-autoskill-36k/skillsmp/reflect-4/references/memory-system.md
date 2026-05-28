# Memory System Guide

The memory system separates accumulated learnings from core skill files, following Anthropic's memory minimalism principle: "Signal gets lost in noise as files grow."

## Architecture

```
~/.claude/memories/
├── README.md                    # System overview
├── skill-patterns.md            # Cross-skill patterns (apply to multiple skills)
├── reflect-meta.md              # Reflect's self-learnings
├── frontend-design-prefs.md     # Skill-specific preferences
├── code-reviewer-prefs.md       # Skill-specific preferences
└── ...                          # Other skill preference files

~/.claude/memories-archive/      # Archived memories (>90 days old)
└── 2026-01/                     # Organized by month
    └── old-prefs.md
```

## When to Use Memories vs. SKILL.md

### Write to Memories

Use `~/.claude/memories/` for **accumulated learnings**:

- ✅ User preferences discovered through corrections
- ✅ Patterns observed across multiple sessions
- ✅ External feedback patterns (repeated test/lint errors)
- ✅ Edge cases and workarounds
- ✅ User-specific style choices
- ✅ Cross-skill patterns (accessibility, type safety, etc.)

**Example**: "User prefers Tailwind CSS over inline styles" → `frontend-design-prefs.md`

### Write to SKILL.md

Use `skills/[skill-name]/SKILL.md` for **core instructions**:

- ✅ Workflow steps and procedure
- ✅ Command syntax and usage
- ✅ Tool integrations
- ✅ Structural changes to the skill itself
- ✅ Bug fixes in skill logic

**Example**: "Add Step 2.5: Validate API schema" → `SKILL.md`

## Memory File Types

### 1. Cross-Skill Patterns (`skill-patterns.md`)

Patterns that apply to **multiple skills**.

**Structure**:
```markdown
## Pattern Name (Added: YYYY-MM-DD)

**Pattern**: Brief description

**Applies to**: skill1, skill2, skill3

**Evidence**:
- Specific examples or data
- Session IDs if relevant

**Implementation**:
- Concrete guidance
- Code examples if applicable
```

**Examples**:
- Accessibility requirements (applies to: frontend-design, code-reviewer)
- Type safety standards (applies to: python-pro, backend-architect)
- Testing requirements (applies to: all development skills)

### 2. Skill-Specific Preferences (`{skill-name}-prefs.md`)

Preferences for **one specific skill**.

**Structure**:
```markdown
# Skill Name Preferences

User preferences and learnings specific to the [skill-name] skill.

Last updated: YYYY-MM-DD

---

## Preference Topic (Added: YYYY-MM-DD)

**Preference**: Description

**Source**: [User correction/External feedback/Edge case/Success]

**Evidence**: What happened

**Implementation**:
- How to apply this preference
```

**Examples**:
- "Use Tailwind CSS for styling" → `frontend-design-prefs.md`
- "Flag functions >15 lines" → `code-reviewer-prefs.md`
- "Prefer pytest fixtures over setup/teardown" → `python-pro-prefs.md`

### 3. Reflect Meta-Learnings (`reflect-meta.md`)

Reflect's learnings **about itself**.

**Structure**:
```markdown
## Learning Topic (Added: YYYY-MM-DD)

**Learning**: What was learned

**Evidence**:
- Data or research supporting this
- Metrics or user feedback

**Application**:
- How this changes reflect's behavior
```

**Examples**:
- External feedback provides 10-30% accuracy gain
- Auto-pause after 3 rejections prevents false positives
- Memory minimalism keeps SKILL.md files focused

## Workflow Integration

### Step 1: Reading Memories (Before Analysis)

Reflect automatically reads memories before analyzing a session:

```bash
# Cross-skill patterns (always)
cat ~/.claude/memories/skill-patterns.md

# Skill-specific preferences (if exists)
cat ~/.claude/memories/${SKILL_NAME}-prefs.md

# Meta-learnings (for reflect skill only)
if [ "$SKILL_NAME" = "reflect" ]; then
    cat ~/.claude/memories/reflect-meta.md
fi
```

**Why**: Informs what patterns to look for in the conversation.

### Step 4: Writing Memories (After Approval)

When a proposal is approved, write to appropriate memory file:

**Decision tree**:
1. Does this apply to multiple skills? → `skill-patterns.md`
2. Does this apply to one skill? → `{skill-name}-prefs.md`
3. Is this about reflect itself? → `reflect-meta.md`

**Update timestamp**:
```bash
sed -i.bak "s/Last updated: .*/Last updated: $(date +%Y-%m-%d)/" "$MEMORY_FILE"
rm -f "$MEMORY_FILE.bak"
```

## Maintenance

### Automatic Cleanup (Recommended)

Run cleanup script periodically (e.g., monthly):

```bash
# Dry-run first (see what would be archived)
reflect-cleanup-memories.sh --dry-run

# Archive memories older than 90 days
reflect-cleanup-memories.sh

# Also clean old metrics and feedback
reflect-cleanup-memories.sh --clean-metrics --clean-feedback
```

**What it does**:
- Archives memory files not modified in 90 days
- Optionally cleans metrics older than 180 days
- Optionally cleans external feedback older than 30 days
- Creates timestamped archive directories

### Manual Review

Periodically review memories for relevance:

```bash
# View all memories
ls -lah ~/.claude/memories/

# View memory with modification dates
ls -lT ~/.claude/memories/*.md

# View a specific memory
cat ~/.claude/memories/frontend-design-prefs.md

# Search across all memories
grep -r "accessibility" ~/.claude/memories/
```

**Questions to ask**:
- Is this still relevant?
- Has this been superseded by a newer pattern?
- Should this be consolidated with another entry?

### Archive Structure

Old memories are archived by month:

```
~/.claude/memories-archive/
├── 2025-11/
│   ├── old-skill-prefs.md
│   └── obsolete-pattern.md
├── 2025-12/
│   └── deprecated-frontend-prefs.md
└── 2026-01/
    └── outdated-meta.md
```

**Restoration**:
```bash
# If you need to restore an archived memory
mv ~/.claude/memories-archive/2025-12/deprecated-frontend-prefs.md \
   ~/.claude/memories/frontend-design-prefs.md

# Update the timestamp
sed -i.bak "s/Last updated: .*/Last updated: $(date +%Y-%m-%d)/" \
   ~/.claude/memories/frontend-design-prefs.md
```

## Best Practices

### 1. Keep Memories Focused

**Good**:
```markdown
## Dark Mode Support (Added: 2026-01-17)

**Preference**: All new components must support dark mode

**Source**: Edge case discovered (Session: example-def)

**Evidence**: 2 components broke in dark mode

**Implementation**:
- Use `dark:` prefixes in Tailwind
- Test with `dark` class on `<html>`
- Avoid hard-coded colors
```

**Bad**:
```markdown
## Various UI Preferences

**Preference**: Use dark mode, also use Tailwind, also make components responsive, also add accessibility...

[Too many unrelated topics in one entry]
```

### 2. Add Clear Evidence

**Good**:
```markdown
**Evidence**:
- 5 ruff F401 errors across generated files
- Session ID: abc123
- External feedback: pytest failures
```

**Bad**:
```markdown
**Evidence**: Some errors happened
```

### 3. Provide Actionable Implementation

**Good**:
```markdown
**Implementation**:
```python
# Preferred
def process_user(user_id: int) -> User:
    ...

# Avoid
def process_user(user_id):
    ...
```
```

**Bad**:
```markdown
**Implementation**: Use types
```

### 4. Timestamp Everything

Always include `(Added: YYYY-MM-DD)` in section headers:
```markdown
## Pattern Name (Added: 2026-01-17)
```

Update file-level timestamp when modifying:
```markdown
Last updated: 2026-01-17
```

### 5. Attribute Sources

Always note where the learning came from:
- `User correction (Session: abc123)`
- `External feedback - 5 F401 errors`
- `Edge case discovered (Session: xyz789)`
- `User success feedback`

## Metrics Integration

Memory updates are tracked in metrics:

```jsonl
{
  "timestamp": "2026-01-17T10:30:00Z",
  "event": "proposal",
  "skill": "frontend-design",
  "decision": "approved",
  "memory_file": "frontend-design-prefs.md",
  "memory_type": "skill_preference"
}
```

**Memory types**:
- `cross_skill_pattern` - Added to `skill-patterns.md`
- `skill_preference` - Added to `{skill}-prefs.md`
- `meta_learning` - Added to `reflect-meta.md`

## Troubleshooting

### Memory file not found

**Problem**: Skill-specific preference file doesn't exist yet.

**Solution**: Create it with template:
```bash
cat > ~/.claude/memories/${SKILL_NAME}-prefs.md <<EOF
# ${SKILL_NAME^} Preferences

User preferences and learnings specific to the ${SKILL_NAME} skill.

Last updated: $(date +%Y-%m-%d)

---
EOF
```

### Duplicate entries

**Problem**: Same pattern added multiple times.

**Solution**: Consolidate into one entry, keep most recent timestamp:
```markdown
## Accessibility (Added: 2026-01-17, Updated: 2026-01-20)

**Pattern**: Consolidated from 3 separate entries
```

### Memory bloat

**Problem**: Memory file growing too large (>100KB).

**Solution**:
1. Split into more specific files
2. Archive old/obsolete entries
3. Consolidate similar patterns

### Archive restoration needed

**Problem**: Archived a memory too early, need it back.

**Solution**: See "Restoration" section above.

## Migration from SKILL.md

If you have existing learnings in SKILL.md files:

1. **Identify learnings** (not core instructions)
2. **Categorize** (cross-skill vs skill-specific)
3. **Extract** to appropriate memory file
4. **Remove** from SKILL.md (keep only workflow)
5. **Update** Step 1 to read from memories

**Example migration**:

Before (in `frontend-design/SKILL.md`):
```markdown
## Guidelines

- Never use gradients unless requested
- Use #000 for dark backgrounds, not #1a1a1a
- Prefer CSS Grid for card layouts
- Always add aria-labels to buttons
...
```

After (in `~/.claude/memories/frontend-design-prefs.md`):
```markdown
## Dark Backgrounds (Added: 2026-01-17)
**Preference**: Use #000 for dark backgrounds, not #1a1a1a
...

## Layout Preferences (Added: 2026-01-17)
**Preference**: Prefer CSS Grid for card layouts
...
```

And (in `~/.claude/memories/skill-patterns.md`):
```markdown
## Accessibility (Added: 2026-01-17)
**Pattern**: Always add aria-labels to buttons
**Applies to**: frontend-design, code-reviewer, ...
```

---

*Part of the reflect plugin Phase 3: Memory Migration*
*Last updated: 2026-01-17*
