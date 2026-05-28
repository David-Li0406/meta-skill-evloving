---
name: skill-creator
description: |
  Create new Claude Code skills following V3 DX patterns with Beads/Serena integration. MUST BE USED when creating skills.
  Follows tech lead proven patterns from 300k LOC case study.
  Use when user wants to create a new skill, implement workflow automation, or enhance the skill system,
  or when user mentions "need a skill for X", "automate this workflow", "create new capability",
  repetitive manual processes, skill creation, meta-skill, or V3 patterns.
tags: [meta, skill-creation, automation, v3]
allowed-tools:
  - Read
  - Write
  - Edit
  - mcp__serena__*
  - Bash(git:*)
  - mcp__plugin_beads_beads__*
---

# Skill Creator

Create V3-compliant skills with automatic Beads/Serena integration (<5 minutes).

## Purpose

Automates skill creation following proven tech lead patterns:
- V3 philosophy compliance (minimal validation, trust environments)
- Progressive disclosure (<500 lines main, details in resources/)
- Beads MCP integration (Feature-Key tracking, issue linking)
- Serena tool integration (symbol-aware code operations)
- Auto-activation via skill-rules.json

**Philosophy:** Fast skill creation + Battle-tested patterns

## When to Use This Skill

**Trigger phrases:**
- "create skill"
- "new skill"
- "make a skill"
- "implement [X] skill"
- "need a skill for [X]"

**Use when:**
- Automating repetitive workflows
- Creating specialist capabilities
- Building meta-operations
- Enhancing the skill system itself

## Workflow

### 1. Classify Skill Type

Ask user which type:

**A. Workflow Skill** (most common)
- Automates multi-step processes
- Examples: sync-feature-branch, create-pull-request, fix-pr-feedback
- Duration: Hours to days of manual work → Seconds
- Pattern: Discovery → Action → Validation → Commit

**B. Platform Integration Skill** (NEW)
- Integrates with external platforms (Railway, GitHub, AWS, etc.)
- Examples: railway-integration, github-actions, terraform
- Duration: Configuration → Operations → Monitoring
- Pattern: Auth → Query → Mutate → Validate
- Uses platform's official skill patterns where available
- Follows agentskills.io format with GraphQL/API patterns

**C. Specialist Work (USE SUBAGENTS, NOT SKILLS)**
- Domain expertise for complex tasks - use Task tool with subagents
- Examples: Task(subagent_type="backend-engineer"), Task(subagent_type="frontend-engineer"), Task(subagent_type="security-engineer")
- Subagents available in `.claude/agents/` directory
- Duration: Minutes to hours of research/implementation
- Pattern: Launch subagent → Isolated context → Return results

**D. Meta Skill**
- Skills that create/manage other skills
- Examples: skill-creator (this skill!)
- Duration: Variable
- Pattern: Analysis → Generation → Integration

### 2. Gather Requirements

Ask user:

```
What does this skill do?
- Primary purpose (1 sentence)
- Main workflow steps (3-7 steps)
- Tools needed (Beads? Serena? Git? API?)
- Trigger phrases (natural language)
- Success criteria (what makes it "done"?)
```

### 3. Create Skill Structure

**Directory layout:**
```
.claude/skills/<skill-name>/
├── SKILL.md                 # Main file (<500 lines)
└── resources/               # Progressive disclosure
    ├── examples/
    ├── patterns/
    └── reference/
```

**Main SKILL.md structure:**
```yaml
---
name: skill-name
description: One-line purpose with MUST BE USED trigger. Use when [natural language patterns].
allowed-tools:
  - Tool category patterns (e.g., Bash(git:*), mcp__serena__*)
---

# Skill Name

One-line purpose with time metric.

## Purpose
What this skill does and why it exists

## When to Use This Skill
Natural language patterns and trigger phrases

## Workflow
Step-by-step execution (numbered list)

## Integration Points
How this integrates with Beads/Serena/Git/other skills

## Best Practices
Do's and don'ts

## What This Skill Does ✅
Specific capabilities

## What This Skill DOESN'T Do ❌
Out of scope

## Examples
Real usage scenarios
```

### 4. Generate Skill Content

**Read reference materials:**
- `resources/v3-philosophy.md` - Core V3 principles
- `resources/skill-types.md` - Patterns by skill type
- `resources/beads-integration-guide.md` - Beads MCP patterns
- `resources/serena-tool-reminders.md` - Serena usage
- `resources/examples/` - Real skill examples

**Apply patterns:**

**For Workflow Skills:**
```markdown
## Workflow

### 1. Check Prerequisites
- Verify context (branch, Beads issue, env)
- Fail fast if missing critical data

### 2. Gather Information
- Use Serena for code discovery
- Use Beads for issue context
- Use git/gh for repository state

### 3. Execute Core Action
- Make changes (code/git/API)
- Handle errors gracefully
- Provide progress updates

### 4. Validate Results
- Quick checks (<5s)
- Trust environments for full validation

### 5. Update State
- Commit changes (git)
- Update Beads (status, notes)
- Confirm to user

## Integration Points

### With Beads
- Check issue exists via show()
- Update status via update()
- Close on completion via close()
- Link discoveries via dep()

### With Serena
- Search: search_for_pattern()
- Navigate: find_symbol()
- Edit: replace_symbol_body()
- Insert: insert_after_symbol()

### With Git
- Status: git status, git branch
- Changes: git add, git commit
- Remote: git push, gh pr create
```

**For Specialist Skills:**
```markdown
## Workflow

### 1. Analyze Request
- Understand scope and constraints
- Identify required tools and knowledge
- Check for blockers

### 2. Research Context
- Read relevant code (Serena)
- Check related issues (Beads)
- Review documentation

### 3. Execute with Expertise
- Apply domain-specific patterns
- Use specialized tools
- Maintain quality standards

### 4. Verify and Document
- Test changes
- Update documentation
- Create follow-up issues if needed
```

### 5. Add Auto-Activation Rules

**Update `.claude/skills/skill-rules.json`:**

```json
{
  "skill-name": {
    "triggers": [
      "create X",
      "make X",
      "implement X",
      "need X"
    ],
    "intents": [
      "User wants to perform workflow X",
      "User asks for capability X"
    ],
    "examples": [
      "User: 'commit my work'",
      "User: 'create PR'",
      "User: 'fix the PR'"
    ]
  }
}
```

**Pattern matching:**
- Keywords: Exact phrases to match
- Intents: Semantic patterns
- Examples: Real usage for testing

### 6. Update Documentation

**Add to CLAUDE.md:**

```markdown
### Natural Language → Skills (Auto-Invoked)

- **"trigger phrase"** → skill-name skill
  - What it does (3-5 bullets)
  - **Total: <time>**
```

**Update skill list:**
```markdown
- **skill-name**: [Description] Use when [trigger patterns].
```

### 7. Test and Commit

**Testing workflow:**

1. **Test auto-activation:**
   ```
   User says trigger phrase
   → Verify hook detects it
   → Verify skill is invoked
   ```

2. **Test execution:**
   ```
   Follow skill workflow
   → Verify each step works
   → Verify integrations (Beads/Serena/Git)
   ```

3. **Test edge cases:**
   ```
   Missing prerequisites
   → Skill fails gracefully
   Error conditions
   → Clear error messages
   ```

**Commit:**
```bash
git add .claude/skills/<skill-name>/
git add .claude/skills/skill-rules.json
git add CLAUDE.md

git commit -m "feat: Add <skill-name> skill for <purpose>

Implements <workflow-type> skill following V3 patterns:
- Progressive disclosure (<500 lines main)
- Beads/Serena integration
- Auto-activation via skill-rules.json
- <X> second typical execution

Feature-Key: <CURRENT_FEATURE>
Agent: claude-code
Role: skill-creator"
```

## Progressive Disclosure Pattern

**Main SKILL.md stays <500 lines:**
- Core workflow only
- Reference resources/ for details
- Keep it scannable

**resources/ contains details:**
```
resources/
├── examples/
│   ├── simple-case.md
│   ├── complex-case.md
│   └── error-handling.md
├── patterns/
│   ├── beads-integration.md
│   ├── serena-usage.md
│   └── git-operations.md
└── reference/
    ├── tool-list.md
    ├── api-reference.md
    └── troubleshooting.md
```

**When to split:**
- Main file approaching 400 lines → Extract examples
- Complex patterns → Move to patterns/
- API details → Move to reference/

## Integration Points

### With Beads

**Create tracking issue:**
```typescript
issue = mcp__plugin_beads_beads__create({
  title: "SKILL_NAME",
  issue_type: "feature",
  priority: 2,
  design: "Skill creation following V3 patterns"
})
```

**Update on completion:**
```typescript
mcp__plugin_beads_beads__close(
  issue_id,
  reason="Skill created and tested"
)
```

### With Serena

**Find existing skills for reference:**
```typescript
mcp__serena__list_dir(
  relative_path=".claude/skills",
  recursive=true
)
```

**Read skill templates:**
```typescript
mcp__serena__get_symbols_overview(
  relative_path=".claude/skills/sync-feature-branch/SKILL.md"
)
```

### With V3 Philosophy

**Minimal validation:**
- Quick checks only (<5s)
- Trust environments for full validation
- Fail fast on critical errors

**Progressive disclosure:**
- Main file scannable in <2 minutes
- Details accessible on demand
- No overwhelming walls of text

**Trust patterns:**
- Don't reinvent wheel
- Use proven tech lead patterns
- Reference existing skills

## Skill Templates

### Workflow Skill Template

```markdown
---
name: skill-name
description: One-line purpose. MUST BE USED when [trigger]. Use when [patterns].
allowed-tools:
  - Tool patterns
---

# Skill Name

Purpose (<time> total).

## Purpose
What and why

## When to Use This Skill
Trigger patterns

## Workflow

### 1. Check Context
Prerequisites and validation

### 2. Execute Action
Main workflow steps

### 3. Update State
Commit and confirm

## Integration Points
Beads/Serena/Git integration

## Best Practices
Do's and don'ts

## Examples
Real scenarios
```

**Full template:** See `resources/examples/workflow-skill-template.md`

### Platform Integration Skill Template (NEW)

```markdown
---
name: platform-integration
description: |
  Platform integration for [Platform Name]. Use when [operations].
tags: [platform-integration, infrastructure]
allowed-tools:
  - Bash(platform:*)
  - Bash(curl:*)
  - Read
  - Write
  - Edit
---

# Platform Integration Skill

[Platform Name] deployment and configuration management.

## Purpose
Automate [Platform] operations using GraphQL/API + CLI patterns.

## When to Use This Skill
- Deploying to [Platform]
- Managing [Platform] resources
- Configuring environments

## Workflow

### 1. Check Prerequisites
- Platform CLI installed
- Platform authenticated
- Project linked

### 2. Execute Operation
- Use GraphQL API for config queries
- Use CLI for deployments
- Use GraphQL for mutations

### 3. Validate Results
- Check deployment status
- Verify configuration

## GraphQL Pattern

Cross-agent compatible pattern:
```bash
SKILLS_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.agent/skills}"
LIB_SCRIPT="$SKILLS_ROOT/lib/platform-api.sh"

bash <<'SCRIPT'
${LIB_SCRIPT} \
  'query { ... }' \
  '{"var": "value"}'
SCRIPT
```

## Common Operations
- Deploy code
- Manage environment variables
- Create services
- View deployment status

## Integration Points
- Pre-flight validation skills
- Environment management skills
- Multi-agent dispatch

## Agent Compatibility
Works across skills-native and MCP-dependent agents.
```

**Full template:** See `resources/examples/railway-integration-skill.md`

### Specialist Skill Template

```markdown
---
name: specialist-name
description: Domain expertise. MUST BE USED for [domain tasks].
allowed-tools:
  - Domain-specific tools
---

# Specialist Name

Domain expertise for [area].

## Purpose
Expertise domain and scope

## When to Use This Skill
Task patterns requiring expertise

## Workflow
Expert execution pattern

## Domain Knowledge
Key patterns and practices

## Integration Points
Standard integrations
```

**Full template:** See `resources/examples/specialist-skill-template.md`

### Meta Skill Template

```markdown
---
name: meta-skill-name
description: Operates on skill system itself. Use when [meta-operation].
allowed-tools:
  - File operations
  - System operations
---

# Meta Skill Name

Skill system operation.

## Purpose
What it changes about skills

## Workflow
Meta-operation steps

## Safety Guardrails
Protecting skill system integrity
```

**Full template:** See `resources/examples/meta-skill-template.md`

## Best Practices

### Do

✅ Keep main SKILL.md under 500 lines
✅ Use progressive disclosure for details
✅ Include real examples
✅ Test auto-activation before committing
✅ Follow V3 philosophy (fast, trust environments)
✅ Integrate with Beads for tracking
✅ Use Serena for code operations
✅ Document trigger phrases clearly
✅ Add to skill-rules.json
✅ Update CLAUDE.md

### Don't

❌ Create walls of text
❌ Duplicate existing skills
❌ Over-validate (trust environments)
❌ Forget allowed-tools restrictions
❌ Skip testing
❌ Ignore progressive disclosure
❌ Miss integration points
❌ Forget to update documentation

## What This Skill Does

✅ Classifies skill type (workflow/specialist/meta)
✅ Gathers requirements from user
✅ Creates skill directory structure
✅ Generates SKILL.md following V3 patterns
✅ Adds auto-activation rules
✅ Updates CLAUDE.md documentation
✅ Tests auto-activation
✅ Commits with proper Feature-Key

## What This Skill DOESN'T Do

❌ Create skills without user input
❌ Modify existing skills (use Edit directly)
❌ Generate skills for unclear requirements
❌ Skip testing phase
❌ Create skills that duplicate existing ones

## Examples

### Example 1: Simple Workflow Skill

```
User: "create a skill that runs linting"

AI asks: "What type of skill? (workflow/specialist/meta)"
User: "workflow"

AI asks requirements:
- Purpose: Run quick linting checks before commit
- Steps: 1) Check files changed, 2) Run linters, 3) Report results
- Tools: Bash (linters), Git (status)
- Triggers: "lint my code", "check formatting"
- Success: Linters pass or report errors

AI creates:
.claude/skills/lint-check/
├── SKILL.md (250 lines)
└── resources/
    └── linter-configs.md

AI updates:
- skill-rules.json (add triggers)
- CLAUDE.md (add to skills list)

AI tests:
User says: "lint my code"
→ Skill auto-activates ✓
→ Linters run ✓
→ Results reported ✓

AI commits:
"feat: Add lint-check skill for pre-commit linting"
```

### Example 2: Specialist Skill

```
User: "create a database migration skill"

AI asks: "What type?"
User: "specialist"

AI gathers requirements:
- Expertise: Database schema migrations
- Tools: Supabase CLI, SQL, migration scripts
- Domain: Schema design, data integrity, rollback safety

AI creates:
.claude/skills/database-migration/
├── SKILL.md (380 lines)
└── resources/
    ├── migration-patterns.md
    ├── rollback-strategies.md
    └── examples/
        ├── add-column.md
        └── add-table.md

AI integrates:
- Beads: Track migrations as tasks
- Serena: Read existing schema
- Railway: Verify in protected shell

AI commits and tests.
```

### Example 3: Meta Skill (skill-creator itself!)

```
User: "create a skill that creates skills"

AI: "That's a meta skill - operates on the skill system itself"

AI creates skill-creator following this exact pattern:
- Main SKILL.md <500 lines
- Progressive disclosure in resources/
- Templates for each skill type
- Auto-activation on "create skill"
- Self-referential documentation

Result: The skill you're reading right now!
```

## Troubleshooting

### Skill doesn't auto-activate

**Check:**
1. skill-rules.json has correct triggers
2. User phrase matches trigger pattern
3. UserPromptSubmit hook is working
4. No typos in skill name

**Fix:**
```bash
# Test hook manually
cat .claude/hooks/userpromptsubmit_skill_activation.sh | bash
# Should output skill reminders
```

### Skill file too large

**Pattern:**
- Extract examples to resources/examples/
- Move detailed patterns to resources/patterns/
- Move API docs to resources/reference/
- Keep main workflow in SKILL.md

### Unclear integration

**Add to Integration Points section:**
```markdown
### With [System]
- What it does
- How it connects
- Example code
```

## Related Skills

- **sync-feature-branch**: Commit workflow (reference for git patterns)
- **create-pull-request**: PR workflow (reference for gh CLI)
- **fix-pr-feedback**: Iterative refinement (reference for discovery pattern)
- **beads-workflow**: Issue tracking (reference for Beads MCP)

## Resources

**Read before creating:**
- `resources/v3-philosophy.md` - V3 core principles
- `resources/skill-types.md` - Patterns by type
- `resources/beads-integration-guide.md` - Beads MCP guide
- `resources/serena-tool-reminders.md` - Serena usage guide
- `resources/examples/` - Real skill examples

**Reference during creation:**
- `resources/examples/workflow-skill-template.md`
- `resources/examples/specialist-skill-template.md`
- `resources/examples/meta-skill-template.md`

---

**Last Updated:** 2025-01-12
**Skill Type:** Meta
**Average Duration:** <5 minutes
**Related Docs:**
- docs/DX_PARITY_V3/SKILL_ACTIVATION_SYSTEM_SPEC.md
- docs/DX_PARITY_V3/TECH_LEAD_300K_LOC_CASE_STUDY.md
- CLAUDE.md (V3 DX Workflow)
