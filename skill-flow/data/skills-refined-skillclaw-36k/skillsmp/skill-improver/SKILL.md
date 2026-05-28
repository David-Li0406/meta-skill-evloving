---
name: skill-improver
description: Review feedback from skill retrospectives and update skill files to improve with use. Creates a continuous improvement loop where skills get better based on real-world usage.
---

# Skill Improver

Process user feedback from skill retrospectives and update skill files to improve them over time.

## When to Use

- User asks to "review skill feedback" or "improve skills based on usage"
- You notice feedback files in `.claude/feedback/`
- User mentions a skill didn't work well or missed something
- Periodic review (monthly) to incorporate learnings

## How It Works

### Step 1: Gather Feedback

Read all feedback files in `.claude/feedback/`:

```bash
ls -la .claude/feedback/retro-*.md
```

Look for patterns:
- Multiple users reporting same missing step → add to skill
- Benchmarks don't match user's context → add context-specific ranges
- Workflow confusing → restructure or add clarifications
- Skill incomplete → add missing sections

### Step 2: Identify High-Impact Changes

Prioritize updates based on:

**High Priority (do first):**
- Missing critical steps that users had to figure out themselves
- Incorrect benchmarks or numbers
- Confusing workflow that requires clarification
- Safety issues or errors

**Medium Priority:**
- Additional examples or templates
- Better explanations of existing steps
- Alternative approaches for different contexts

**Low Priority:**
- Nice-to-have additions
- Stylistic improvements
- Minor clarifications

### Step 3: Update Skill Files

For each skill needing updates:

#### 3a. Add a "Learnings" Section

If the skill doesn't have one, add at the end:

```markdown
## Learnings from Use

**[Date]**: [Brief description of what was learned]
- **Feedback**: [What users reported]
- **Update**: [What we changed]
- **Result**: [Expected improvement]
```

#### 3b. Update Main Content

If feedback suggests core changes:
- Add missing steps to checklists
- Update benchmarks with ranges (e.g., "20-30% for B2C, 50-70% for B2B")
- Restructure workflow if confusing
- Add "Common Pitfalls" section if users make same mistakes

#### 3c. Version the Change

At the top of the skill, track versions:

```markdown
---
name: skill-name
version: 1.2.0
last_updated: 2026-01-22
changelog:
  - v1.2.0 (2026-01-22): Added missing step for X based on user feedback
  - v1.1.0 (2026-01-15): Updated benchmarks for Y context
  - v1.0.0 (2026-01-01): Initial release
---
```

### Step 4: Archive Processed Feedback

Move processed feedback to archive:

```bash
mkdir -p .claude/feedback/archive
mv .claude/feedback/retro-2026-01-22-*.md .claude/feedback/archive/
```

Keep a summary of learnings in `.claude/feedback/SUMMARY.md`:

```markdown
# Feedback Summary

## [Skill Name]

**Total feedback sessions**: 12
**Last updated**: 2026-01-22

**Key learnings**:
- Added step for X (reported by 3 users)
- Updated benchmarks for B2B context (reported by 5 users)
- Clarified workflow around Y (reported by 2 users)

**Patterns**:
- Users in enterprise context need higher benchmarks
- Early-stage startups need more examples
- Non-technical users need clearer explanations of jargon
```

## Example Workflow

### Scenario: product-market-fit skill needs improvement

**Step 1: Review Feedback**

Read `.claude/feedback/retro-2026-01-22-143022.md`:

```markdown
## Feedback

**Missed important steps?** yes

**Improvements needed:**
The Sean Ellis test threshold of 40% seems high for B2B enterprise products.
We're at 32% "very disappointed" but our retention is 85% D30 which is excellent.
Should the skill mention that thresholds vary by product type?
```

**Step 2: Identify Pattern**

Check other feedback files → 3 more users report B2B context needs different benchmarks.

**Step 3: Update Skill**

Edit `.claude/skills/product-market-fit/SKILL.md`:

**Before:**
```markdown
## Sean Ellis Test (40% Rule)

"How would you feel if you could no longer use [product]?"
- ≥40% "Very disappointed" = Strong PMF
```

**After:**
```markdown
## Sean Ellis Test (Context-Dependent Thresholds)

"How would you feel if you could no longer use [product]?"

**Thresholds by product type:**
- **Consumer B2C**: ≥40% "Very disappointed" = Strong PMF
- **SMB B2B**: ≥35% "Very disappointed" = Strong PMF
- **Enterprise B2B**: ≥30% "Very disappointed" = Strong PMF (longer sales cycles, different buying psychology)

**Why the difference?**
- Enterprise buyers are more rational than emotional
- Switching costs are higher (contracts, integrations)
- Retention is a better PMF signal for B2B (see Step 2)
```

Add to Learnings section:

```markdown
## Learnings from Use

**2026-01-22**: Refined Sean Ellis thresholds by product type
- **Feedback**: 4 users reported 40% threshold too high for B2B enterprise
- **Update**: Added context-specific thresholds (B2C 40%, SMB 35%, Enterprise 30%)
- **Result**: More accurate PMF diagnosis for different product types
```

**Step 4: Archive & Track**

```bash
mv .claude/feedback/retro-2026-01-22-*.md .claude/feedback/archive/
```

Update `.claude/feedback/SUMMARY.md`:

```markdown
## product-market-fit

**Total feedback sessions**: 4
**Last updated**: 2026-01-22

**Key learnings**:
- Added context-specific Sean Ellis thresholds (reported by 4 users)
- B2B needs different benchmarks than B2C

**Next improvements to consider**:
- Add industry-specific retention benchmarks
- Include examples from different verticals
```

## Quality Checklist

Before updating any skill, ensure:

- [ ] Feedback is from multiple users (pattern, not outlier)
- [ ] Change makes skill more accurate, not just more complex
- [ ] Benchmarks are sourced or validated (not anecdotal)
- [ ] Update is backward compatible (doesn't break existing workflows)
- [ ] Learnings section documents why we made the change
- [ ] Version number incremented appropriately (semver)
- [ ] Processed feedback archived, not deleted

## Feedback Categories

Track feedback by type to identify systemic issues:

### Category 1: Missing Steps
**Example**: "Skill forgot to mention we need to segment cohorts by acquisition channel"
**Action**: Add step to checklist

### Category 2: Incorrect Benchmarks
**Example**: "40% D30 retention is not 'strong' for our B2B SaaS, it's average"
**Action**: Update benchmarks with context (B2C vs B2B vs Enterprise)

### Category 3: Confusing Workflow
**Example**: "I didn't know whether to do cohort analysis before or after Sean Ellis test"
**Action**: Number steps clearly, add workflow diagram

### Category 4: Missing Context
**Example**: "Skill assumes I have 1000+ users, what if I only have 50?"
**Action**: Add "Early Stage Adaptation" section

### Category 5: Tool-Specific Issues
**Example**: "How do I calculate D30 retention in Google Analytics?"
**Action**: Add "Implementation in Common Tools" section

## Best Practices

### Do:
✅ Look for patterns across multiple feedback sessions
✅ Update skills incrementally (small, tested changes)
✅ Document why changes were made (Learnings section)
✅ Preserve feedback history (archive, don't delete)
✅ Version skills so users know what changed

### Don't:
❌ Update based on single piece of feedback (might be outlier)
❌ Make skills overly complex trying to cover every edge case
❌ Remove content without understanding why it was there
❌ Ignore feedback for more than 30 days (patterns emerge)
❌ Update without testing the new version

## Automation Ideas

### Weekly Digest (optional)
Create a script to summarize new feedback:

```bash
#!/bin/bash
# .claude/hooks/learning/weekly-feedback-digest.sh

echo "📊 Feedback Digest (Last 7 Days)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

find .claude/feedback -name "retro-*.md" -mtime -7 | while read -r file; do
    echo ""
    echo "File: $(basename $file)"
    grep "Skills Used" -A 5 "$file"
    grep "Improvements needed:" -A 3 "$file"
done
```

### Auto-Tag for Review
When feedback mentions specific issues, auto-tag:

- "missing step" → tag for immediate review
- "wrong number" → tag for fact-check
- "confusing" → tag for clarity rewrite

## Success Metrics

Track improvement over time:

- **Feedback frequency**: Decreasing = skills getting better
- **Repeated issues**: Should approach zero over time
- **User satisfaction**: Track "Did this skill help?" responses
- **Skill usage**: Updated skills should see increased usage

---

## Meta: This Skill Improves Itself

This skill should follow its own advice:

**Learnings from Use:**

*[To be filled as this skill gets used and improved]*

**Version History:**

- v1.0.0 (2026-01-22): Initial release - framework for skill improvement

---

**Next Steps:**

1. Review feedback in `.claude/feedback/`
2. Identify patterns and prioritize updates
3. Update skill files with improvements
4. Document learnings
5. Archive processed feedback
6. Commit changes with clear message

The more you use this system, the better your skills become. It's a continuous improvement loop.
