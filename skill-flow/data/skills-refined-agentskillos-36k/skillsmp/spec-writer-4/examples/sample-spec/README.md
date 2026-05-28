# Sample Specification Example

This directory contains a complete example of the spec-writer discovery process for a hypothetical feature: "Cross-Service Dependency Tracker for Microservices".

## Example Scenario

**Problem**: Engineering teams working on features that span multiple microservices lose visibility into cross-service dependencies, leading to integration issues discovered late in development.

**Solution Discovery**: Through structured discovery, user stories emerged organically from problem understanding rather than being predefined.

## File Overview

### SPEC.md
The progressive deliverable containing graduated user stories. This example shows:
- 3 fully graduated stories (P1, P2 priorities)
- 1 in-progress story
- Complete acceptance scenarios with Given/When/Then format
- Extracted requirements and success criteria
- Edge cases identified and handled
- Cross-references to decisions and research

### STATE.md
Working memory showing current discovery state. Demonstrates:
- Problem understanding evolution
- Story landscape with status tracking
- In-progress story detail with confidence levels
- Proto-stories still emerging
- Watching list for potential revisions
- Current phase and next actions

### OPEN_QUESTIONS.md
Active questions organized by category. Shows:
- Blocking questions preventing story graduation
- Clarifying questions for completeness
- Watching questions that may affect graduated stories
- Context explaining why each question matters

### archive/DECISIONS.md
Decision history with traceability. Includes:
- Context explaining why decision was needed
- Options considered with tradeoffs
- Rationale for chosen approach
- Implications for stories and requirements
- Cross-references to questions and stories

### archive/RESEARCH.md
Research log documenting investigation. Contains:
- Industry pattern research
- Technical approach exploration
- Findings and implications
- Cross-references to informed stories

## How This Example Was Created

This specification represents the state after approximately 3 iterations:

1. **Iteration 1** (Phase 1: Problem Exploration)
   - Understood core problem through open-ended questions
   - Identified 2 primary personas
   - Mapped current vs. desired state
   - 3 proto-stories emerged

2. **Iteration 2** (Phase 2: Story Crystallization)
   - Transformed proto-stories into 5 concrete stories
   - Prioritized (2 P1, 2 P2, 1 P3)
   - Identified dependencies
   - User confirmed backlog

3. **Iteration 3** (Phase 3: Story Development)
   - Developed Story 1 to graduation
   - Developed Story 2 to graduation
   - Developed Story 3 to graduation
   - Story 4 currently in progress at 85% confidence
   - Story 5 queued, dependent on Story 4

## Key Patterns Demonstrated

### Stories Emerged from Understanding

The stories were not predefined. They crystallized through:
- Understanding who experiences the problem
- Mapping current pain points
- Exploring what success looks like
- Identifying themes that became stories

### Progressive Detail

Compare early vs. late STATE.md problem statements:

**Early**: "Teams struggle to track work across services"

**Late**: "Engineering teams working on features spanning 3+ services lose visibility into cross-service dependencies because each service team uses different tracking tools, resulting in integration issues discovered late in the development cycle"

### Quantified Everything

Vague terms replaced with specifics:
- "Fast" → "Under 200ms for graphs with < 20 services"
- "Many services" → "Up to 50 service dependencies per feature"
- "Reliable" → "99.9% uptime for dependency tracking"

### Revision Awareness

STATE.md watching list shows potential graduated story revisions:
- Q45 may affect Story 1
- Story 4 scope may overlap with Story 2

This proactive flagging enables clean revision management.

### Complete Traceability

Every story links to:
- Decisions that shaped it (D1, D2, etc.)
- Research that informed it (R1, R2, etc.)
- Questions that were resolved (Q1, Q3, etc.)

Can reconstruct why any requirement exists.

## Using This Example

### As a Template

Copy this structure for your own discoveries:
```bash
cp -r examples/sample-spec/ my-feature-discovery/
# Edit files to match your feature
```

### As a Reference

When writing your own specification:
- Compare your SPEC.md story format to this example
- Check your STATE.md structure matches this pattern
- Verify your questions are categorized like this example
- Ensure your decisions have similar level of detail

### For Learning

Study how:
- Problem statement evolved through iterations
- Proto-stories transformed into concrete stories
- Acceptance scenarios became progressively more specific
- Edge cases were systematically identified
- Requirements were extracted from scenarios
- Success criteria were quantified

## What Good Looks Like

This example demonstrates production-ready specification quality:

**Story Quality**:
- ✅ Every story independently testable
- ✅ Every scenario specific and unambiguous
- ✅ Every edge case has defined handling
- ✅ Every requirement measurable

**Process Quality**:
- ✅ Stories emerged from understanding, weren't imposed
- ✅ All decisions documented with rationale
- ✅ All research logged with implications
- ✅ All questions tracked until resolved

**Artifact Quality**:
- ✅ SPEC.md is the deliverable (graduated stories)
- ✅ STATE.md is working memory (in-flight work)
- ✅ Archive files provide traceability
- ✅ Cross-references maintained throughout

## Anti-Patterns to Avoid

This example intentionally avoids common mistakes:

**❌ Starting with predetermined stories**
✅ Started with problem understanding, let stories emerge

**❌ Vague acceptance criteria**
✅ Specific Given/When/Then scenarios

**❌ Unmeasured success criteria**
✅ Quantified with numbers and thresholds

**❌ Missing traceability**
✅ Every decision and research finding logged

**❌ Graduating stories too early**
✅ Stories graduated only at 100% confidence

**❌ Ignoring graduated story revisions**
✅ Watching list tracks potential revision needs

## Next Steps

After studying this example:

1. Start your own discovery with `/spec-writer`
2. Reference these files when structuring yours
3. Compare your artifacts to this example for quality
4. Use the templates in `references/file-templates.md`
5. Follow the guidance in `references/phase-guide.md`

Remember: Your discovery will be unique. This is one example path—your feature will have its own story to tell.
