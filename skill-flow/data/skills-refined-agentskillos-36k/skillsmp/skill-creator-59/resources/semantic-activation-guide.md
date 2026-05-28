# Semantic Activation Guide

Quick reference for creating skills that activate naturally via Claude's semantic understanding.

## Core Principle

Skills are **model-invoked** - Claude autonomously decides which skills to load based on description metadata and conversational context, NOT explicit pattern matching.

## Gold Standard Pattern

```yaml
description: |
  [What it does]. Use when [natural situations]. Invoke when [context clues]. Keywords: [semantic terms]
tags: [categories]
```

## Real Example

From sync-feature-branch skill:

```yaml
description: |
  Commit current work to feature branch with Beads metadata tracking and git integration.
  MUST BE USED for all commit operations. Use when user wants to save progress, commit
  changes, prepare work for review, sync local changes, or finalize current work. Invoke
  when seeing "uncommitted changes", "git status shows changes", "Feature-Key missing",
  or discussing commit operations, saving work, or git workflows. Keywords: commit, git,
  save work, Feature-Key, beads sync, git add, git commit, sync, save progress
tags: [workflow, git, beads, commit]
```

## What Triggers Activation

1. **Natural language phrases** users would actually say
   - "commit my work", "I'm done", "fix the PR"
   - Not: "execute commit operation", "perform git add"

2. **Error patterns and context clues**
   - "uncommitted changes", "CI failures", "missing Feature-Key"
   - What would I see that indicates this skill is needed?

3. **Semantic keywords** related to the domain
   - Domain terms: commit, git, save, beads
   - Related concepts: feature key, sync, progress
   - CLI commands: git add, git commit, bd sync

4. **Conversational context**
   - Discussing commits → sync-feature-branch becomes relevant
   - Not explicitly triggered, but contextually appropriate

## Anti-Patterns to Avoid

❌ **Regex pattern matching in hooks**
```typescript
// DON'T DO THIS
if (/\b(proceed|continue)\s+with/i.test(prompt)) {
  suggestSkill("issue-first");
}
```

❌ **Overly technical trigger language**
```yaml
# BAD
description: Execute feature branch synchronization protocol with metadata persistence
```

❌ **Forcing activation via explicit checks**
```yaml
# BAD - Don't try to match every possible phrase
Use when user says "commit", "save", "push", "sync", "commit my work",
"commit changes", "save my work", "save changes", "push my code"...
```

✅ **Trust Claude's contextual understanding**
```yaml
# GOOD - Natural language, semantic keywords
Use when user wants to save progress, commit changes, or prepare work for review.
Keywords: commit, git, save work, Feature-Key
```

## Testing Your Skill Description

### Ask yourself:

1. **Would a human understand when to use this?**
   - If yes: Probably semantic enough
   - If no: Add more natural language

2. **Does it include what users would actually say?**
   - "commit my work" ✓
   - "initiate commit sequence" ✗

3. **Does it include error patterns/context clues?**
   - "uncommitted changes" ✓
   - Just "git operations" ✗

4. **Are keywords domain-relevant?**
   - Actual terms from the domain
   - Not just synonyms for the skill name

### Test in practice:

1. Say the natural language phrase to Claude
2. Does the skill activate?
3. If not: Add that phrase or related keywords to description
4. Iterate based on real usage

## Structure Breakdown

### "Use when" clause
Natural situations where skill is needed:
- User goals: "wants to save progress"
- User actions: "preparing work for review"
- Workflow states: "finishing current work"

### "Invoke when" clause
Observable signals that skill is relevant:
- Error patterns: "uncommitted changes", "CI failures"
- Status indicators: "git status shows changes"
- Missing elements: "Feature-Key missing"
- Discussion topics: "discussing commit operations"

### "Keywords" clause
Semantic terms for matching:
- Domain terms: commit, git, beads
- CLI commands: git add, git commit, bd sync
- Related concepts: Feature-Key, save work, sync
- Natural phrases: save progress, commit changes

### "Tags" clause
Categorization for discovery:
- Type: workflow, meta, context
- Domain: git, beads, github, pr
- Operation: commit, merge, deploy

## Coverage Analysis

**Current state:** 24/26 skills (92%) follow this pattern

**Audit:** See docs/SKILL_SEMANTIC_AUDIT_bd-7fl.md for full analysis

## Reference

- **Anthropic blog:** [Equipping Agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Full deep dive:** See context-dx-meta skill
- **Templates:** resources/examples/ in this skill directory

---

**Last Updated:** 2025-01-18
**Related:** skill-creator/resources/examples/workflow-skill-template.md
