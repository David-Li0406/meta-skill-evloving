# Solo Developer Workflows

Specific workflows and practices for solo developers applying Linear Method principles.

## Your First Day Setup

### 1. Workspace Configuration (15 min)

```
✓ Create workspace
✓ Create single team (even solo, structure helps)
✓ Configure 2-week cycles
✓ Enable auto-archiving:
  - Auto-archive completed issues after 3 months
  - Auto-archive completed cycles after 2 months
✓ Set up labels:
  - Priority: p0 (critical), p1 (high), p2 (normal)
  - Type: feature, bug, chore, design
  - Size: small (< 1 day), medium (1-2 days), large (3 days)
```

### 2. Define Initial Direction (20 min)

```
Create 2-3 Initiatives:
- "Build MVP Core Features" (8 weeks)
- "Launch to First 10 Users" (10 weeks)  
- "Set Up Infrastructure" (ongoing)

Set Your First Goal:
- Measurable and achievable
- Example: "Get 5 people using product weekly by Dec 1"
```

### 3. Create First Project (20 min)

```
Pick most important feature needed for MVP

Write brief spec:
- Why it matters (2 sentences)
- What you're building (3 sentences)
- How you'll approach it (bullet points)

Break into 5-10 issues:
- Each completable in 1-3 days
- Start with foundation/setup issues
- End with polish/testing issues
```

### 4. Start First Cycle (5 min)

```
From your project, pull 6-8 issues into current cycle
Don't overload - these should feel achievable
Pick first issue and start building
```

## Daily Workflow

### Morning Routine (5 min)

```
1. Look at active cycle view
2. Pick 1-2 issues to complete today
3. Move to "In Progress"
4. Optional: Check if any blockers/dependencies
```

### During Work

```
Working on an issue:
- Keep it focused on that one task
- If you discover new work needed → Create new issue
- If issue is bigger than expected → Break it down
- Don't let perfect be enemy of done

When you complete an issue:
- Mark it "Done" (feels great!)
- Commit your code
- Move to next issue or take a break

Discovered a bug while working:
- Create issue immediately
- Add to current cycle if critical
- Otherwise let it queue for next cycle
```

### End of Day (2 min)

```
Quick glance at what you completed
Note any blockers for tomorrow
Close laptop and actually stop working
```

## Weekly Workflow

### Start of Week (Monday, 10 min)

```
Review Current Cycle:
- What's completed?
- What's in progress?
- What's blocked?
- Anything to remove/defer?

Plan the Week:
- Which issues are priority?
- Any time-sensitive work?
- Realistic to finish current cycle on time?
```

### Mid-Week Check (Wednesday, 5 min)

```
Quick health check:
- On track for cycle goals?
- Any issues taking longer than expected?
- Need to adjust scope or defer anything?
```

### End of Cycle (Every 2 weeks, 30 min)

```
1. Review Completed Work (5 min)
   - List everything shipped
   - Celebrate wins (even small ones!)

2. Write Changelog Entry (10 min)
   - What shipped this cycle
   - Any major improvements
   - Keep it brief and user-focused

3. Move Incomplete Work (2 min)
   - Let Linear auto-move to next cycle
   - No guilt about unfinished items

4. Plan Next Cycle (10 min)
   - What's most important now?
   - Pull issues from planned projects
   - 6-8 issues that feel achievable

5. Start New Cycle (3 min)
   - Mark cycle as complete
   - Begin new cycle
   - Pick first issue to work on Monday
```

## Project Planning Workflow

### When to Create a Project

**Create a project when:**
- Building a new feature that needs multiple issues
- Working on something that takes > 1 week
- Need to organize related work
- Want to communicate progress to others

**Don't create a project for:**
- Single issues (just make an issue)
- Very quick fixes or tweaks
- Exploration that might lead nowhere

### Project Planning Steps

```
1. Write Brief Spec (30 min)
   - Why (problem/opportunity)
   - What (solution)
   - How (approach)
   - Out of scope
   
2. Break Into Issues (20 min)
   - List all tasks needed
   - Each 1-3 days max
   - Order by dependency
   
3. Estimate Timeline (5 min)
   - Count issues × average time
   - Add 20% buffer
   - Set target date
   
4. Add to Initiative (2 min)
   - Link to relevant initiative
   - Shows how this fits bigger picture
   
5. Start Building (Go!)
   - Pull first few issues into current cycle
   - Begin work
```

## Prioritization Workflow for Solo Devs

### When You Have Too Many Ideas

```
Step 1: Dump everything into issues
- Don't worry about quality yet
- Just capture the ideas
- Takes 10 minutes

Step 2: Tag each issue
- Is it a blocker or enabler?
- Is it needed now or later?
- How much effort? (S/M/L)

Step 3: Sort by Now + High Impact + Low Effort
- These are your quick wins
- Prioritize these first

Step 4: Create projects for multi-issue features
- Group related issues
- Add proper specs
- Set timelines

Step 5: Defer the rest
- Remove from active cycle
- Add to backlog/icebox
- Review monthly
```

### Daily Prioritization

```
When starting your day, pick issues based on:

1. Blockers first (critical bugs, things preventing launch)
2. Then enablers (features that unlock next steps)
3. Then improvements (polish, optimization)
4. Then nice-to-haves (can wait)

Ask for each issue:
- "Does this move me toward my current goal?"
- "Is this needed for MVP?"
- "Can this wait until after launch?"
```

## Launch Workflow

### Pre-Launch Checklist Project

```
Create a "Launch Prep" project with issues like:

- [ ] Test full user journey end-to-end
- [ ] Fix critical bugs (P0 only)
- [ ] Set up error monitoring (Sentry)
- [ ] Set up basic analytics
- [ ] Write launch announcement
- [ ] Prepare product hunt post
- [ ] Set up support email/chat
- [ ] Create simple documentation
- [ ] Test on mobile devices
- [ ] Test on different browsers
- [ ] Deploy to production
- [ ] Post launch announcement

Each issue = 1 day or less
Total: 1-2 week sprint to launch
```

### Launch Day

```
Morning:
- Final production checks
- Post announcement (Twitter, Reddit, Product Hunt)
- Share with friends/network

During Day:
- Monitor for critical bugs
- Respond to early feedback
- Fix show-stopper issues immediately
- Create issues for non-critical feedback

Evening:
- Collect all feedback into issues
- Prioritize fixes for tomorrow
- Celebrate shipping! 🎉
```

### Post-Launch (First Week)

```
Each Day:
- Triage new feedback → Create issues
- Fix critical bugs immediately
- Ship updates daily if needed
- Respond to all user messages

End of Week:
- Write changelog of all fixes/improvements
- Thank early users publicly
- Plan next cycle based on feedback
```

## Dealing with Context Switching

### When Building Multiple Features

**Don't**: Try to work on 5 features simultaneously

**Do**: Work on 1-2 features at a time
```
Active:
- Feature A (80% done - finishing up)
- Feature B (just started)

Queued:
- Feature C (next up)
- Feature D (after C)
- Feature E (low priority)
```

### When Bugs Interrupt Flow

```
Critical Bug (Blocks Users):
- Stop current work
- Fix immediately
- Deploy hotfix
- Document what happened
- Create issue to prevent recurrence

Non-Critical Bug:
- Create issue with details
- Tag as "bug"
- Add to current cycle if time permits
- Otherwise queues for next cycle
- Return to current work

Pro tip: Set aside Friday afternoons for bug fixes
```

## Managing Energy and Burnout

### Sustainable Solo Dev Practices

```
Weekly Cadence:
- Mon-Thu: Feature building (focused work)
- Friday: Bugs, admin, planning, learning
- Weekend: Actually off (no guilt!)

Daily Rhythm:
- Morning: Deep work on complex issues
- Afternoon: Smaller tasks, reviews, planning
- Evening: Stop working (seriously)

Momentum ≠ Burnout:
- Ship daily, but work reasonable hours
- Skip standup meetings (you're solo!)
- No need for process theatre
- Focus on actual building
```

### When You Feel Stuck

```
Issue taking too long?
- Break it into smaller issues
- Ship partial solution first
- Ask for help (forums, Discord)
- Take a walk and come back fresh

Lost motivation?
- Look at what you've shipped (changelog helps!)
- Ship something small today for quick win
- Talk to a user to remember why this matters
- Take a day off to recharge

Overwhelmed by backlog?
- Archive old, irrelevant issues
- Delete duplicate/outdated issues
- Focus only on current cycle
- Backlog is not a todo list
```

## Feedback Collection Workflow

### Collecting Feedback

```
Set up channels:
- In-app feedback button
- Support email
- Twitter mentions monitoring
- Simple contact form

When feedback comes in:
1. Thank the person
2. Create issue immediately
3. Quote their feedback directly in issue
4. Link to conversation
5. Tag with "user-feedback"

Weekly:
- Review all "user-feedback" issues
- Spot trends (multiple people asking for same thing?)
- Prioritize based on frequency + impact
```

### User Feedback → Project Planning

```
Monthly exercise:
1. List top 5 most requested features
2. For each, understand the underlying problem
3. Decide: 
   - Is this for our target user?
   - Does it align with our vision?
   - Is now the right time?
4. Create projects for the yes's
5. Respond to users with timeline
```

## Solo Dev Anti-Patterns to Avoid

### ❌ Over-Planning

**Bad**: Spending weeks planning perfect architecture
**Good**: Plan 1-2 weeks ahead max, iterate as you learn

### ❌ Perfectionism

**Bad**: Polishing every detail before shipping
**Good**: Ship working version, polish based on real usage

### ❌ Feature Hopping

**Bad**: Starting 10 features, finishing none
**Good**: Complete 2-3 issues daily, see steady progress

### ❌ No User Contact

**Bad**: Building in isolation for months
**Good**: Show work-in-progress, get feedback early

### ❌ Ignoring Your Calendar

**Bad**: Overcommitting every cycle, burning out
**Good**: Realistic cycles with buffer time

## Quick Decision Framework

**When deciding what to work on today:**

```
1. Any critical bugs blocking users?
   → Fix immediately
   
2. Any issues that unblock other work?
   → Do these next
   
3. Any quick wins (< 2 hours, high impact)?
   → Knock these out
   
4. What moves you toward current goal?
   → Focus here
   
5. Everything else?
   → Queue for later
```

**When deciding whether to build a feature:**

```
Questions to ask:
- Does this solve a real problem users have?
- Is this needed for MVP or nice-to-have?
- Will this move me toward my current goal?
- Can I ship a simple version quickly?
- What's the smallest version that adds value?

If yes to most: Build it
If no to most: Defer it
If unsure: Talk to users
```

## Sample Weekly Schedule

### Monday
```
9am: Review cycle, plan week (10 min)
9:10am: Pick first issue, start building
12pm: Lunch break
1pm: Continue building
5pm: Mark completed issues done, commit code
```

### Tuesday-Thursday
```
9am: Pick issue, start building
12pm: Lunch
1pm: Continue building
4pm: Review progress, create new issues if needed
5pm: Mark completed issues done, commit code
```

### Friday
```
9am: Bug fixes and quick improvements
11am: Admin work (emails, feedback)
12pm: Lunch
1pm: Plan next week / cycle
2pm: Learning / exploration
4pm: Review week's accomplishments
5pm: Weekend! 🎉
```

### Every Other Friday (Cycle End)
```
Add 30min for:
- Write changelog
- Complete current cycle
- Plan next cycle
```

This schedule is flexible - adjust to your energy and preferences. The key is consistency and actually shipping.
