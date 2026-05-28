# Low Determinism Example: Creative Content Generation Skill

This example demonstrates minimal resiliency for a creative content generation skill with low determinism requirements.

## Determinism Assessment

**Scores:**
- Output Precision: 2 (creative output, subjective quality)
- Process Rigidity: 1 (many valid approaches)
- Failure Consequence: 1 (easily regenerated)
- Recovery Difficulty: 1 (just try again)

**Total: 5/40 - Low Determinism → Minimal Resiliency**

## Skill Structure

```
content-generation-skill/
├── SKILL.md
└── references/
    ├── style-guide.md
    └── examples.md
```

**Note:** No scripts/ or complex validation needed. Simple structure reflects low determinism.

## SKILL.md (Excerpt)

```markdown
---
name: creative-content-generation
description: This skill should be used when the user asks to "write blog post", "generate marketing copy", "create content", "draft article", or discusses creative writing tasks. Provides guidance for generating engaging content with minimal constraints.
version: 1.0.0
---

# Creative Content Generation

## Overview

This skill guides the creation of creative content (blog posts, marketing copy, articles) with flexible approaches and subjective quality assessment.

**Use for:** Blog posts, marketing copy, social media content, articles, creative writing

## Approach

Content generation is inherently creative with multiple valid outputs. Focus on:
- Understanding the goal and audience
- Following brand guidelines (if provided)
- Iterating based on feedback
- Exploring different angles and styles

## Process

### Step 1: Understand the Goal

Clarify intent with the user:
- What's the purpose of this content?
- Who's the target audience?
- What tone/style is desired?
- Are there any key messages or points to include?
- Any constraints (length, format, keywords)?

**No rigid requirements—gather what's helpful.**

### Step 2: Gather Context (Optional)

If relevant, gather:
- Brand voice guidelines
- Previous content examples
- Competitor content
- Audience research
- SEO keywords

**Skip if not needed. Context helps but isn't mandatory.**

### Step 3: Generate Content

Create content based on understanding:

**Multiple Approaches (all valid):**
- Start with outline, then expand
- Write freely, then edit
- Draft multiple versions, choose best
- Collaborative iteration with user

**No prescribed method—use what works.**

### Step 4: Review and Iterate

Share draft with user for feedback:
- Does it match the goal?
- Is the tone appropriate?
- Does it resonate with the target audience?
- Any specific changes needed?

**Iterate based on feedback. Multiple rounds are normal.**

## Quality Guidelines

Since output is subjective, focus on:

**Clarity:**
- Is the message clear?
- Is it easy to read?
- Does it flow well?

**Relevance:**
- Does it address the goal?
- Is it appropriate for the audience?
- Does it include key points?

**Engagement:**
- Is it interesting?
- Does it capture attention?
- Does it encourage action (if intended)?

**Brand Alignment (if applicable):**
- Does it match brand voice?
- Does it follow style guidelines?
- Is terminology consistent?

**No pass/fail validation—assess with user.**

## Anti-Patterns to Avoid

While creativity is encouraged, avoid:

**Plagiarism:**
- Always create original content
- Don't copy from sources
- Properly attribute quotes or references

**Inappropriate Content:**
- Avoid offensive language
- Stay professional
- Respect audience sensibilities

**Off-Target Content:**
- Don't ignore the goal
- Stay relevant to the topic
- Address user's stated purpose

**Over-Optimization:**
- Don't sacrifice readability for SEO
- Natural language trumps keyword stuffing
- Human audience before algorithms

## Iteration Examples

Content generation often requires multiple iterations:

**Example 1: Tone Adjustment**

*Draft 1:* "Our product is the best solution for enterprise data management."
*Feedback:* "Too corporate, we want a friendlier tone"
*Draft 2:* "Managing enterprise data doesn't have to be painful. We've built a solution that actually makes sense."

**Example 2: Audience Shift**

*Draft 1:* "Leverage our cutting-edge API infrastructure for seamless integration..."
*Feedback:* "Our audience isn't technical, simplify the language"
*Draft 2:* "Connect your tools together easily, no coding required..."

**Example 3: Message Focus**

*Draft 1:* [500 words covering many features]
*Feedback:* "Focus on the speed benefit, that's our key differentiator"
*Draft 2:* [300 words focused on speed, with brief mentions of other features]

**Iteration is expected and valuable. No iteration is "failure"—it's the creative process.**

## Style Variations

Multiple valid style approaches:

**Formal:**
- Professional terminology
- Complete sentences
- Structured paragraphs
- Objective tone

**Conversational:**
- Friendly language
- Short sentences
- Direct address ("you")
- Subjective opinions welcome

**Storytelling:**
- Narrative arc
- Characters/examples
- Emotional connection
- Descriptive language

**Listicle:**
- Numbered/bulleted points
- Scannable format
- Brief explanations
- Easy to digest

**Choose based on audience and goal. No single "correct" style.**

## Working with Feedback

User feedback guides iteration:

**Specific Feedback (Easy):**
- "Change X to Y"
- "Remove this section"
- "Add more about Z"

**Vague Feedback (Probe Further):**
- "It doesn't feel right" → Ask: what specifically feels off?
- "Make it better" → Ask: what would "better" look like?
- "Not quite" → Ask: what's missing or what should change?

**Conflicting Feedback (Discuss Priorities):**
- "Make it shorter" + "Add more details" → Ask: which is more important?
- "More professional" + "More casual" → Ask: what's the primary audience?

**No Fixed Formula:** Adapt to user's feedback style and needs.

## When to Finish

Content is "complete" when:
- User is satisfied with the output
- It meets the stated goal
- No more iterations requested

**Subjective completion criteria. User decides when it's done.**

## Handling Dissatisfaction

If user is consistently unsatisfied:

**Check Understanding:**
- Re-clarify the goal
- Confirm audience and tone
- Review any constraints or guidelines

**Explore Examples:**
- Ask for examples of content they like
- Discuss what makes those examples work
- Identify specific attributes to emulate

**Try Different Approaches:**
- If outline-first didn't work, try free-form
- If serious tone isn't landing, try playful
- If long-form isn't working, try concise

**No "failure" state—just exploring until the right approach emerges.**

## Optional Enhancements

For users who want more structure:

**Content Brief (Optional Template):**
```markdown
# Content Brief

**Goal:** [What should this content achieve?]
**Audience:** [Who will read this?]
**Tone:** [Formal/conversational/playful/authoritative?]
**Key Points:** [Must include...]
**Length:** [Approximate word count or duration]
**Format:** [Blog post/email/social post/etc.]
**SEO Keywords:** [If relevant]
**Call to Action:** [What should reader do after?]
```

**Use if helpful, skip if not.**

**Style Reference (Optional):**

See `references/style-guide.md` for examples of different content styles and when to use them.

**Examples Library (Optional):**

See `references/examples.md` for sample content across formats and styles.

## What Resiliency Means Here

For low-determinism creative tasks, "resiliency" looks different:

**Not about:**
- Validation checkpoints
- Error detection
- Rollback procedures
- Automated recovery

**Instead about:**
- Flexibility to explore
- Easy iteration
- User feedback integration
- Multiple valid outcomes

**Resiliency = ability to adapt and iterate until user is satisfied.**

## Success Criteria

Content generation succeeds when:
- User is satisfied with output
- Content achieves stated goal
- Iterative process felt productive

**All subjective, all valid. No automated validation possible or needed.**

## Additional Resources

- **`references/style-guide.md`** - Examples of different content styles
- **`references/examples.md`** - Sample content across formats

---

**Note:** This skill intentionally lacks:
- Validation scripts
- Checkpoint procedures
- Error handling
- Recovery mechanisms
- Automated testing

**Why?** Because creative content generation is low-determinism. Adding complex resiliency would be over-engineering that creates friction without benefit.

## Anti-Examples (What NOT to Do)

### ❌ Over-Engineering: Content Validation

**Don't do this:**
```bash
# scripts/validate-content.sh
echo "Validating content..."

# Check word count
WC=$(wc -w < draft.md)
if [ $WC -lt 300 ] || [ $WC -gt 800 ]; then
    echo "❌ Word count must be between 300-800"
    exit 1
fi

# Check reading level
READING_LEVEL=$(textstat flesch_reading_ease draft.md)
if [ $READING_LEVEL -lt 60 ]; then
    echo "❌ Reading level too complex"
    exit 1
fi

# Check keyword density
KEYWORD_DENSITY=$(grep -o "enterprise" draft.md | wc -l)
if [ $KEYWORD_DENSITY -lt 3 ]; then
    echo "❌ Keyword 'enterprise' must appear at least 3 times"
    exit 1
fi

echo "✅ Content validation passed"
```

**Why not?**
- Creative content shouldn't be constrained by arbitrary metrics
- Reading level depends on audience (technical audiences may prefer complex)
- Keyword requirements sacrifice natural language
- User satisfaction matters, not automated checks

### ❌ Over-Engineering: Rollback Procedures

**Don't do this:**
```markdown
## Rollback Procedure

If user is unsatisfied with Draft 3:

1. Identify which draft was preferred:
   - Draft 1 (initial)
   - Draft 2 (first iteration)

2. Run rollback script:
   ```bash
   scripts/rollback-draft.sh --to draft1
   ```

3. This will:
   - Restore previous draft
   - Reset iteration count
   - Clear feedback history
```

**Why not?**
- Just show the user previous drafts—no script needed
- Chat history contains all versions
- "Rollback" is just copying text, not a procedure

### ❌ Over-Engineering: Checkpoint Validation

**Don't do this:**
```markdown
## Checkpoint 1: Outline Validation

Before proceeding to full draft, validate outline:

**Requirements:**
- [ ] 3-5 main sections defined
- [ ] Each section has 2-3 key points
- [ ] Logical flow between sections
- [ ] Introduction and conclusion present
- [ ] Estimated word count within range

Run: `scripts/validate-outline.sh`

Proceed only after validation passes.
```

**Why not?**
- Outline structure is subjective
- User might prefer different organization
- Rigid requirements constrain creativity
- User can simply say "this outline works" or "let's adjust it"

## The Right Amount of Resiliency

**For low-determinism creative tasks:**

**Do provide:**
- Guidelines and principles
- Examples of good approaches
- Anti-patterns to avoid
- Iteration framework

**Don't provide:**
- Automated validation
- Rigid checkpoints
- Error detection
- Recovery procedures
- Comprehensive testing

**Guideline:** If you can't objectively evaluate it, don't try to validate it.

## Comparing Resiliency Levels

|  | Low Determinism (This Skill) | High Determinism (Deployment) |
|---|---|---|
| **Validation** | None (subjective) | Comprehensive (automated) |
| **Checkpoints** | None | Every phase |
| **Error Handling** | Iterate on feedback | Automatic rollback |
| **Recovery** | Just try again | Complex procedures |
| **Testing** | User satisfaction | Automated test suites |
| **Documentation** | Guidelines | Runbooks |
| **Scripts** | None needed | Extensive automation |

**The difference is massive, and appropriately so.**

---

**Key Takeaway:** Low determinism → minimal resiliency. Provide guidance and flexibility, not validation and constraints. Over-engineering creates friction that inhibits the creative process.
