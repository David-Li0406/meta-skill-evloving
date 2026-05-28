---
name: epistemic-beliefs
description: Guide for creating and managing epistemic beliefs in Patina. Use this skill when synthesizing project decisions into formal beliefs, when the user says "create a belief", "add belief", "capture this as a belief", or when distilling session learnings into the epistemic layer. Beliefs capture project decisions with evidence, confidence signals, and support/attack relationships. IMPORTANT - Proactively suggest belief capture when you notice design decisions, repeated patterns, strong principles, or statements like "we should always", "never do X", "the right way is". Do not wait for magic words.
---

# Epistemic Beliefs

Create formal beliefs that capture project decisions with evidence and reasoning.

## Proactive Belief Detection

**Do not wait for the user to say "create a belief".** Watch for:

| Pattern | Example | Action |
|---------|---------|--------|
| Design decision | "We should use sync, not async" | Suggest: "Capture as belief?" |
| Repeated principle | Said 3+ times in session | Suggest: "This keeps coming up..." |
| Strong preference | "Never do X", "Always Y" | Suggest: "This sounds like a core belief" |
| Contradiction found | Conflicts with existing belief | Ask: "This contradicts X - revise?" |
| Lesson learned | "That was a mistake because..." | Suggest: "Capture to avoid repeating?" |

When you notice these patterns, **ask the user**:
> "This sounds like a belief worth capturing: '{statement}'. Should I create it?"

If user confirms, proceed with belief creation. If user declines, move on.

## When to Create Beliefs

- User explicitly requests: "create a belief", "add this as a belief"
- **You notice a design decision or principle** (proactive)
- **A pattern is repeated multiple times** (proactive)
- Distilling session learnings into persistent knowledge
- Capturing architectural decisions with justification
- Recording design principles that guide future work

## Belief Creation Process

### Step 1: Gather Information

Before creating a belief, ensure you have:
- **Statement**: One clear sentence expressing the belief
- **Evidence**: At least one source (session, commit, document)
- **Persona**: Usually "architect" for project-level decisions
- **Confidence**: Your assessment (0.0-1.0)

### Step 2: Use the Creation Script

Execute the belief creation script with required fields:

```bash
.claude/skills/epistemic-beliefs/scripts/create-belief.sh \
  --id "belief-id-here" \
  --statement "One sentence belief statement" \
  --persona "architect" \
  --confidence "0.85" \
  --evidence "session-YYYYMMDD: description (weight: 0.9)" \
  --facets "domain1,domain2"
```

The script will:
1. Validate all required fields
2. Generate proper YAML frontmatter
3. Create the belief file in `layer/surface/epistemic/beliefs/`
4. Report success or validation errors

### Step 3: Add Optional Sections

After creation, you may edit the file to add:
- Additional evidence links
- Supports relationships (beliefs this supports)
- Attacks relationships (beliefs this defeats)
- Attacked-By relationships (known challenges)
- Applied-In examples (concrete applications)

## Belief Format Reference

See `references/belief-example.md` for the complete format.

Key fields:
- **id**: Lowercase, hyphenated identifier (e.g., `sync-first`)
- **persona**: Epistemic agent (usually `architect`)
- **facets**: Domain tags (e.g., `rust`, `architecture`)
- **confidence.score**: 0.0-1.0 overall confidence
- **entrenchment**: `low`, `medium`, `high`, or `very-high`
- **status**: `active`, `scoped`, `defeated`, or `archived`

## Confidence Signals

When assessing confidence, consider:
- **evidence**: Strength of supporting evidence (0.0-1.0)
- **source_reliability**: How reliable are the sources? (0.0-1.0)
- **recency**: How recent is the evidence? (0.0-1.0)
- **survival**: How long unchallenged? (0.0-1.0)
- **user_endorsement**: Has user explicitly validated? (0.0-1.0)

## Common Patterns

**High confidence belief** (0.85+):
- Multiple evidence sources
- Survived multiple sessions
- User endorsed or frequently applied

**Medium confidence belief** (0.65-0.85):
- Single strong evidence source
- Recently created, not yet proven
- No conflicting evidence

**Low confidence belief** (<0.65):
- Inferred from context
- Conflicting evidence exists
- Needs validation

## Validation Rules

The creation script enforces:
- ID must be lowercase with hyphens only
- Statement must be non-empty
- Confidence must be 0.0-1.0
- At least one evidence source required
- Persona must be specified
