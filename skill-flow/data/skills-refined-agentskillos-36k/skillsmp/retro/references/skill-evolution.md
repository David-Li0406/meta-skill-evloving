# Skill Evolution

When and how to update skills based on session learnings.

## Update Triggers by Skill

### frontend-design Skill

**Add when:**
- New motion pattern used successfully 2+ times
- New accessibility pattern discovered and validated
- Test strategy proves reliable across multiple components
- Design token pattern emerges

**Specific triggers:**
| Discovery | Where to Add | Example |
|-----------|--------------|---------|
| Animation pattern | references/motion-mastery.md | New spring config that feels natural |
| State transition | references/state-choreography.md | Loading → Success timing |
| A11y pattern | references/accessibility-excellence.md | New ARIA pattern |
| Token structure | references/design-systems.md | New semantic layer |
| Test pattern | references/test-resilience.md | New mock strategy |

**Format:**
```markdown
### [Pattern Name]

**Context:** [When to use]
**Implementation:** [Code or description]
**Verification:** [How to test]
```

### mvp-prd Skill

**Add when:**
- New PRD section proves valuable repeatedly
- Scope management pattern emerges
- Sprint organization insight validated

**Specific triggers:**
| Discovery | Where to Add |
|-----------|--------------|
| New PRD section | SKILL.md output structure |
| Scope strategy | references/scope-management.md |
| Risk pattern | references/sprint-planning.md |

### prd-clarify Skill

**Add when:**
- Question revealed major scope change
- Question type should always be asked
- New category of ambiguity identified

**Specific triggers:**
| Discovery | Where to Add |
|-----------|--------------|
| New question | references/question-bank.md |
| Sequencing insight | references/sequencing-strategy.md |
| Expansion handling | references/scope-expansion.md |

**Format for new questions:**
```markdown
### [Category Name]
N. "[Question text]"
   - **Why ask:** [What it reveals]
   - **When to ask:** [Trigger conditions]
   - **Watch for:** [Red flags in answer]
```

### prd-ux Skill

**Add when:**
- New state pattern emerges
- New affordance rule discovered
- Z-index conflict resolved in novel way
- Pass technique improved

**Specific triggers:**
| Discovery | Where to Add |
|-----------|--------------|
| State pattern | references/state-choreography.md |
| Affordance rule | references/affordance-patterns.md |
| Error handling | references/failure-modes.md |
| Pass technique | references/pass-enhancements.md |

### ux-prompts Skill

**Add when:**
- New prompt structure proves effective
- Verification checklist improved
- Anti-pattern identified

**Specific triggers:**
| Discovery | Where to Add |
|-----------|--------------|
| Quality technique | references/quality-amplifiers.md |
| Verification | references/verification-templates.md |
| Mistake pattern | references/anti-patterns.md |

## CLAUDE.md Updates

**Update when:**
- New verification command discovered
- Additional paths worth documenting
- MCP tool usage pattern emerges
- Agent strategy refinement needed
- Context management insight gained

**Specific triggers:**
| Discovery | Section to Update |
|-----------|-------------------|
| Useful command | Commands |
| New directory | Paths |
| MCP integration | MCP Tools |
| Agent optimization | Agent Strategy |
| Error pattern | Error Protocol |

## Evolution Process

### Step 1: Identify Candidate

During session, note when:
- Pattern works exceptionally well
- Same solution applied 2+ times
- Would have saved time if documented earlier
- Surprised by non-obvious behavior

### Step 2: Validate Pattern

Before adding to skill:
- [ ] Pattern worked in at least 2 different contexts
- [ ] Pattern is project-agnostic (not specific to one codebase)
- [ ] Pattern provides clear value
- [ ] Pattern is not already documented elsewhere

### Step 3: Determine Location

| If the pattern is... | Add to... |
|---------------------|-----------|
| Core workflow | SKILL.md body |
| Detailed technique | Appropriate references/ file |
| Working code | examples/ |
| Utility script | scripts/ |

### Step 4: Document

Follow skill writing guidelines:
- Use imperative/infinitive form
- Be specific, not vague
- Include when to apply
- Include verification when applicable

### Step 5: Integrate

Ensure new content:
- Is referenced in SKILL.md (if in references/)
- Doesn't duplicate existing content
- Follows formatting conventions
- Is findable via reasonable search

## Evolution Anti-Patterns

### Don't Add

| Anti-Pattern | Problem | Alternative |
|--------------|---------|-------------|
| One-off solution | Not generalizable | Log in LEARNINGS.md only |
| Framework-specific | Too narrow | Make generic or skip |
| Version-dependent | Will become obsolete | Note in LEARNINGS.md |
| Obvious patterns | Low value | Skip entirely |
| Untested patterns | May not work | Wait until validated |

### Watch For

| Warning Sign | Indicates |
|--------------|-----------|
| Skill growing too large | Need to split to references/ |
| Similar patterns scattered | Need consolidation |
| Outdated patterns | Need pruning pass |
| Duplicate content | Need deduplication |

## Skill Maintenance

### Quarterly Review

Every 3 months:
1. Review all skill content for accuracy
2. Remove obsolete patterns
3. Consolidate similar content
4. Update examples if needed
5. Check references still exist and are relevant

### After Major Project

At project completion:
1. Capture project-specific insights → LEARNINGS.md
2. Generalize patterns for skills → skill updates
3. Remove project-specific content from skills
4. Validate skill triggers still accurate

### On Framework/Library Upgrade

When dependencies upgrade:
1. Review affected patterns
2. Update or remove outdated examples
3. Add new patterns if API changed
4. Update version references if any
