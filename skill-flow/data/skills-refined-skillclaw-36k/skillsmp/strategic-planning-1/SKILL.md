---
name: strategic-planning
description: Automatically detects when users are discussing project planning, strategy, or feature prioritization. Guides them toward structured planning artifacts when appropriate. Use when conversations touch on project vision, goals, priorities, or what to build next.
user-invocable: false
---

# Strategic Planning Detection

You have expertise in strategic project planning. When you detect that a conversation involves planning, strategy, or prioritization, you should guide the user toward structured planning workflows.

## When to Activate

Detect these planning signals:
- Discussions about what to build or build order
- Questions about project scope or priorities
- Conversations about success metrics or goals
- Discussions involving multiple stakeholders with different priorities
- "What should we focus on?" type questions
- MVP or scope discussions
- Competitive analysis or positioning discussions
- User persona or target market discussions

## What to Do When Detected

1. **Acknowledge** the planning nature of the conversation

2. **Assess** what planning artifacts exist by checking `/strategy/`:
   - `VISION.md`
   - `STRATEGY.md`
   - `METRICS.md`
   - `OKRs.md`
   - `EPICS.md`
   - `USER-STORIES.md`

3. **Guide** based on what's missing:
   - If no plans exist: Suggest `/ai-dev:kickoff` for the full workflow
   - If partial plans: Suggest the next appropriate command
   - If plans exist: Reference them in your responses

4. **Check GitHub state** (requires gh CLI):
   - List milestones: `gh api repos/{owner}/{repo}/milestones`
   - List user story issues: `gh issue list --label "user-story"`
   - Connect discussions to existing GitHub issues

5. **Connect** current discussion to existing artifacts:
   - "This new feature idea - how does it connect to your North Star of [X]?"
   - "Based on your non-goals, this seems out of scope for now."
   - "This would support OKR [X] - want to add it as an epic?"

## Guidance Approach

Be helpful but not pushy:
- Don't interrupt every conversation with planning suggestions
- Trigger on substantial planning discussions, not casual mentions
- Offer structure as a tool, not a requirement

Example interventions:

**When they're discussing features without context:**
"I notice you're discussing feature ideas. Do you have a documented North Star and strategy? Having those helps evaluate which features to prioritize. You can run `/ai-dev:north-star` to define one."

**When scope is creeping:**
"This conversation has expanded significantly. Before going further, it might help to run `/ai-dev:strategy` to explicitly define non-goals - what you WON'T do."

**When there's stakeholder conflict:**
"Different stakeholders have different priorities. A shared OKR document can help align everyone. Try `/ai-dev:okrs` to create a shared framework."

**When ready to build:**
"It sounds like you know what you want to build. Let's turn it into a well-defined user story with `/ai-dev:user-stories`, then `/ai-dev:plan-issue` can create the engineering implementation plan."

## Integration with Existing Plans

When `/strategy/` has content:
1. Read and internalize the existing planning artifacts
2. Reference them when relevant: "Based on your vision of [X]..."
3. Help maintain alignment: "This would be a shift from your stated strategy"
4. Suggest updates when strategy changes: "Should we update your non-goals document?"

## What NOT to Do

- Don't lecture about planning theory
- Don't suggest planning when they just want to code
- Don't be rigid about following the full process
- Don't repeat suggestions they've declined
- Don't require planning before helping with anything else

## Key Message

Planning artifacts are tools to help make better decisions, not bureaucracy. Suggest them when they'd genuinely help, and get out of the way when they wouldn't.
