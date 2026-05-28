---
name: Launch Planner
description: Transforms app ideas into shippable MVPs using Next.js + Supabase. Enforces ship-fast philosophy, prevents feature creep, generates PRDs and Claude Code starter prompts. Maximum 1-week builds focused on core user loop only.
---

# Launch Planner Skill

## Purpose

Turns app ideas into shippable MVPs by enforcing ruthless scoping, preventing over-engineering, and keeping you focused on shipping fast with real user validation.

**Philosophy**: Ship fast, validate with real users, iterate based on data, not assumptions.

## When to Use

Use this skill when:
- **Starting new project** - Scope MVP and generate PRD
- **Feeling stuck** - Refocus on core loop
- **Adding features** - Challenge if they're needed for launch
- **Over-engineering** - Simplify tech decisions
- **Planning build** - Create Claude Code starter prompts

## Product Philosophy

### Core Principles

**1. Ship Fast**
- 1 week maximum for MVP
- Launch with minimum viable features
- Imperfect but live beats perfect but unreleased

**2. Validate with Real Users**
- Real usage > theoretical assumptions
- Deploy early, get feedback fast
- Iterate based on actual user behavior

**3. No Feature Creep**
- Only features that serve core user loop
- Cut ruthlessly to hit 1-week deadline
- Add features AFTER validating core idea

### Anti-Patterns to Avoid

❌ **Building features nobody asked for**
- Don't assume what users want
- Don't build based on competitor features
- Don't add "nice to haves" pre-launch

❌ **Over-engineering**
- Don't optimize prematurely
- Don't build for scale you don't have
- Don't use complex tech for simple problems

❌ **Adding auth before validating idea**
- Don't require login for MVP unless essential
- Test core value prop first
- Add auth only when needed

## Preferred Tech Stack

### Default Stack (Fast & Reliable)

**Frontend**: Next.js (App Router)
- React framework with SSR
- File-based routing
- API routes built-in
- Fast deployment

**Backend**: Supabase
- PostgreSQL database
- Real-time subscriptions
- Row-level security (RLS)
- Auth when needed
- Storage for files

**Deployment**: Vercel
- Zero-config deployment
- Preview deployments
- Edge functions
- Analytics built-in

**Styling**: Tailwind CSS
- Utility-first CSS
- Fast development
- Design Guide compatible
- No custom CSS needed

### When to Deviate

**Stick with stack UNLESS**:
- You need specific functionality (e.g., mobile-first → React Native)
- You're already expert in different stack
- Constraint forces different choice (e.g., cost)

**Default answer**: Use Next.js + Supabase. Don't overthink it.

## MVP Scoping Rules

### The Core Loop Test

**Every feature must pass**:
1. Is this part of the core user loop?
2. Can users get value without this?
3. Can we fake/skip this for MVP?

**Core Loop Definition**: The minimum sequence of actions users take to get value.

**Example - Task Manager**:
```
Core Loop:
1. Add task → 2. View tasks → 3. Mark complete
(Everything else is optional)

✅ Must Have: Create, read, update task status
❌ Can Wait: Tags, filters, search, sharing, analytics
```

### 1-Week Maximum Rule

**If feature takes >1 week, it's not MVP**

**Options**:
1. Cut the feature entirely
2. Build simplified version (fake it)
3. Split into phases (MVP now, polish later)

**Time Budget**:
```
Day 1: Setup + Core data models
Day 2-3: Core user loop implementation
Day 4: Basic UI (functional, not perfect)
Day 5: Deploy + basic testing
Day 6-7: Buffer for issues
```

### Feature Triage

**Must Have (Core Loop)**:
- Features users can't get value without
- Minimum viable functionality
- Core CRUD operations

**Should Have (Post-Launch)**:
- Features that improve experience
- Polish and refinements
- Performance optimizations

**Could Have (Maybe Never)**:
- Nice-to-haves
- Advanced features
- Edge cases

**Won't Have (Never)**:
- Feature creep
- Premature optimization
- Vanity features

## Pre-Build Questions

### Ask These BEFORE Writing Any Code:

#### 1. Who is this for?

**Good Answers**:
- "Solo developers building side projects"
- "Small business owners tracking inventory"
- "Content creators managing social posts"

**Bad Answers**:
- "Everyone!"
- "Anyone who needs [vague thing]"
- "People like me"

**Why it matters**: Specific audience = clear decisions. Vague audience = endless feature debates.

#### 2. What's the ONE problem it solves?

**Good Answers**:
- "Managing tasks without complexity"
- "Finding apartments in [city] under $2000/mo"
- "Scheduling social posts across platforms"

**Bad Answers**:
- "Productivity and collaboration and analytics"
- "It's like [Product A] meets [Product B]"
- "Many things!"

**Why it matters**: One problem = focused MVP. Many problems = feature creep.

#### 3. How will I know if it works?

**Good Answers**:
- "Users create >3 tasks in first session"
- "Users return within 7 days"
- "Users upgrade to paid within 30 days"

**Bad Answers**:
- "People use it"
- "It gets popular"
- "Good reviews"

**Why it matters**: Measurable success = clear validation. Vague success = never know if it works.

## Common Mistakes & Solutions

### Mistake #1: Building Features Nobody Asked For

**Signs**:
- "Users might want..."
- "It would be cool if..."
- "Competitor has this..."

**Solution**:
- Launch without it
- If users ask, add it
- If nobody asks, you saved time

**Example**:
```
❌ Don't: Add dark mode, keyboard shortcuts, export to PDF
✅ Do: Launch with basic functionality, add based on requests
```

### Mistake #2: Over-Engineering

**Signs**:
- Microservices for MVP
- Complex caching strategies
- "Scalable to 1M users"
- Custom auth system

**Solution**:
- Use managed services (Supabase, Vercel)
- Build for 10 users, not 10M
- Optimize when you have real performance issues

**Example**:
```
❌ Don't: Build custom API, Redis caching, load balancing
✅ Do: Use Next.js API routes, Supabase, Vercel (scales automatically)
```

### Mistake #3: Adding Auth Before Validating Idea

**Signs**:
- Starting with login/signup flows
- Building user management first
- Worrying about OAuth providers

**Solution**:
- Test core idea without auth
- Use local storage for MVP
- Add Supabase Auth only when needed

**Example**:
```
❌ Don't: Build auth system before core features
✅ Do: Build core features, test locally, add auth for multi-device
```

### Mistake #4: Perfect UI Before Launch

**Signs**:
- Designing every screen in Figma
- Pixel-perfect mockups
- Custom animations
- Multiple design iterations

**Solution**:
- Use Design Guide defaults
- Ship functional, iterate on polish
- Tailwind + shadcn/ui = good enough

**Example**:
```
❌ Don't: Spend 3 days on perfect landing page
✅ Do: Use template, ship in 2 hours, improve based on feedback
```

### Mistake #5: Building for Edge Cases

**Signs**:
- "What if user has 10,000 items?"
- "What if they're offline?"
- "What about accessibility for color blind users?"

**Solution**:
- Build for common case (80%)
- Add edge cases when users report them
- Accessibility basics (semantic HTML, keyboard nav)

**Example**:
```
❌ Don't: Build offline mode, infinite scroll, complex error handling
✅ Do: Pagination, basic errors, online-only (for now)
```

## PRD Generation Template

### Minimal PRD Structure

```markdown
# [Product Name] MVP

## Overview
[2-3 sentence description of what this is and why it exists]

## Target User
**Who**: [Specific user persona]
**Problem**: [One specific problem they have]
**Current Solution**: [How they solve it today]
**Why this is better**: [Your advantage]

## Success Metrics
**Primary**: [Main metric to track]
**Secondary**: [Supporting metrics]
**Goal**: [Specific target for launch validation]

## Core User Loop
1. [Step 1]
2. [Step 2]
3. [Step 3]

*Users get value at step [X]*

## MVP Features (Must Have)

### Feature 1: [Name]
**User Story**: As a [user], I want [action] so that [benefit]
**Acceptance Criteria**:
- [ ] Criteria 1
- [ ] Criteria 2

**Technical Notes**:
- Supabase table: [table name]
- Key fields: [fields]

### Feature 2: [Name]
[Same structure]

### Feature 3: [Name]
[Same structure]

## Deferred Features (Post-Launch)
- [Feature]: Why deferred
- [Feature]: Why deferred

## Tech Stack
- **Frontend**: Next.js 14 (App Router), Tailwind CSS
- **Backend**: Supabase (PostgreSQL + Auth)
- **Deployment**: Vercel
- **Key Libraries**: [Any specific libraries needed]

## Data Model

```sql
-- Core tables only
create table [table_name] (
  id uuid primary key default uuid_generate_v4(),
  created_at timestamp default now(),
  -- fields
);
```

## MVP Scope
**Timeline**: 1 week (5-7 days)
**Launch Date**: [Target date]

## What We're NOT Building
- [Feature 1]: Why
- [Feature 2]: Why
- [Feature 3]: Why

## Validation Plan
**How to test**: [Specific actions]
**Success looks like**: [Measurable outcome]
**Failure looks like**: [When to pivot]
```

## Claude Code Starter Prompt Template

### Template for Starting Development

```markdown
I'm building [product name] - [one sentence description].

**Target**: [Specific user persona]
**Core Problem**: [One problem it solves]
**Success Metric**: [How we measure success]

**Tech Stack**:
- Next.js 14 (App Router)
- Supabase (PostgreSQL + Auth)
- Tailwind CSS
- Vercel deployment

**Core User Loop**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**MVP Features** (1-week build):

1. **[Feature 1]**: [Brief description]
   - [Acceptance criteria 1]
   - [Acceptance criteria 2]

2. **[Feature 2]**: [Brief description]
   - [Acceptance criteria 1]
   - [Acceptance criteria 2]

3. **[Feature 3]**: [Brief description]
   - [Acceptance criteria 1]
   - [Acceptance criteria 2]

**NOT building yet**: [Deferred features]

**Data Model**:
```sql
[Paste Supabase schema here]
```

**Next Steps**:
1. Set up Next.js + Supabase project
2. Create database schema
3. Build [Feature 1]
4. Build [Feature 2]
5. Build [Feature 3]
6. Deploy to Vercel

Let's start with project setup. Create Next.js app with Supabase integration.
```

## Examples

### Example 1: Task Manager MVP

```markdown
# QuickTask MVP

## Overview
Dead-simple task manager for solo developers who hate complexity. Add tasks, mark them done, that's it. No teams, no projects, no BS.

## Target User
**Who**: Solo developers and indie hackers
**Problem**: Existing task managers are bloated with features they don't need
**Current Solution**: Text files, Notes app, pen and paper
**Why this is better**: Faster than text files, simpler than Todoist

## Success Metrics
**Primary**: Tasks created per user
**Secondary**: 7-day retention
**Goal**: Users create average 5+ tasks in first week

## Core User Loop
1. Add task (quick input)
2. View all tasks (simple list)
3. Mark task complete (one click)

*Users get value at step 1 (task is saved)*

## MVP Features (Must Have)

### Feature 1: Quick Task Input
**User Story**: As a developer, I want to quickly add tasks without friction
**Acceptance Criteria**:
- [ ] Text input always visible
- [ ] Enter key adds task
- [ ] Task appears in list immediately

**Technical Notes**:
- Supabase table: `tasks`
- Key fields: `id`, `text`, `completed`, `created_at`

### Feature 2: Task List
**User Story**: As a user, I want to see all my tasks in one place
**Acceptance Criteria**:
- [ ] Shows all tasks newest first
- [ ] Completed tasks visually distinct
- [ ] Empty state with helpful message

### Feature 3: Complete Task
**User Story**: As a user, I want to mark tasks done with one click
**Acceptance Criteria**:
- [ ] Checkbox toggles completion
- [ ] Completed tasks stay visible
- [ ] No confirmation needed

## Deferred Features (Post-Launch)
- **Delete tasks**: Can just mark complete for now
- **Edit tasks**: Can delete and recreate for now
- **Due dates**: Not needed for MVP
- **Tags/categories**: Over-engineering
- **Search**: Not needed until >50 tasks

## Tech Stack
- **Frontend**: Next.js 14 (App Router), Tailwind CSS
- **Backend**: Supabase (PostgreSQL)
- **Deployment**: Vercel
- **Key Libraries**: None needed

## Data Model

```sql
create table tasks (
  id uuid primary key default uuid_generate_v4(),
  text text not null,
  completed boolean default false,
  created_at timestamp default now()
);
```

## MVP Scope
**Timeline**: 1 week
**Launch Date**: [This Friday]

## What We're NOT Building
- **Authentication**: Use localStorage for now
- **Multiple lists**: Single list is enough
- **Collaboration**: Solo users only
- **Mobile app**: Responsive web is fine
- **Keyboard shortcuts**: Nice to have, not essential

## Validation Plan
**How to test**: Use it myself for 1 week, share with 10 dev friends
**Success looks like**: I prefer this over my text file, friends create >5 tasks
**Failure looks like**: Nobody uses it after day 2
```

### Claude Code Starter Prompt

```markdown
I'm building QuickTask - a dead-simple task manager for developers who hate bloated apps.

**Target**: Solo developers and indie hackers
**Core Problem**: Existing task managers are too complex
**Success Metric**: Users create 5+ tasks in first week

**Tech Stack**:
- Next.js 14 (App Router)
- Supabase (PostgreSQL)
- Tailwind CSS
- Vercel deployment

**Core User Loop**:
1. Add task (quick input)
2. View tasks (simple list)
3. Mark complete (one click)

**MVP Features** (1-week build):

1. **Quick Task Input**: Always-visible text input, Enter to add
   - Text input component with auto-focus
   - Creates task on Enter keypress
   - Clears input after adding

2. **Task List**: All tasks in single list, newest first
   - Display all tasks from Supabase
   - Show completed tasks with strikethrough
   - Empty state: "No tasks yet. Add one above!"

3. **Complete Task**: One-click checkbox to mark done
   - Checkbox toggles `completed` boolean
   - Visual feedback (strikethrough + gray)
   - No delete needed for MVP

**NOT building yet**: Delete, edit, due dates, tags, search, auth

**Data Model**:
```sql
create table tasks (
  id uuid primary key default uuid_generate_v4(),
  text text not null,
  completed boolean default false,
  created_at timestamp default now()
);
```

**Next Steps**:
1. Create Next.js app: `npx create-next-app@latest quicktask`
2. Set up Supabase project and get credentials
3. Create tasks table in Supabase
4. Build task input component
5. Build task list component
6. Connect to Supabase and deploy

Let's start! Create the Next.js project with App Router, Tailwind, and TypeScript.
```

## Decision Framework

### When Stuck on Product Decision

**Question Format**: "Should I [build feature X]?"

**Decision Tree**:
```
Is it part of core user loop?
├─ No → Don't build
└─ Yes
   ↓
   Can users get value without it?
   ├─ Yes → Don't build (optional)
   └─ No
      ↓
      Can I fake it for MVP?
      ├─ Yes → Fake it (manual process)
      └─ No
         ↓
         Does it take >1 week?
         ├─ Yes → Simplify or cut
         └─ No → Build it
```

### Example Decisions

**Q**: Should I add user authentication?
```
Core loop? Maybe (depends on product)
Value without? Usually yes (use localStorage)
Fake it? Yes (single-user mode)
>1 week? No (Supabase Auth is fast)
Decision: ⏸️ Defer - Test core idea first, add auth later
```

**Q**: Should I add dark mode?
```
Core loop? No
Value without? Yes
Decision: ❌ Don't build - Add post-launch if requested
```

**Q**: Should I add task creation?
```
Core loop? Yes (fundamental feature)
Value without? No (can't use app without it)
Fake it? No (need it to function)
>1 week? No (simple CRUD)
Decision: ✅ Build - Essential for MVP
```

## Launch Checklist

### Pre-Launch (Day 6-7)

**Technical**:
- [ ] Core features work end-to-end
- [ ] Deployed to production URL
- [ ] Basic error handling (no crashes)
- [ ] Mobile responsive (Design Guide rules)
- [ ] Page loads in <3 seconds

**Product**:
- [ ] Core user loop is clear
- [ ] Success metric defined
- [ ] Landing page explains what it does
- [ ] Call-to-action is obvious

**What NOT to worry about**:
- [ ] ~~Perfect UI~~ (functional is enough)
- [ ] ~~Edge cases~~ (fix when reported)
- [ ] ~~Analytics setup~~ (manual tracking is fine)
- [ ] ~~SEO optimization~~ (not needed yet)
- [ ] ~~Email marketing~~ (too early)

### Launch Day

**Share**:
1. Twitter/X with demo GIF
2. Indie Hackers with story
3. Reddit (relevant subreddit)
4. Show HN (if ready)
5. Personal network (ask for feedback)

**Track**:
- Visitors (Vercel Analytics)
- Sign-ups / usage (Supabase dashboard)
- Feedback (Twitter replies, DMs)

**Don't**:
- Obsess over metrics first day
- Make changes based on 1 person's feedback
- Panic if nobody uses it immediately

### Week 1 Post-Launch

**Collect**:
- User feedback (what they love/hate)
- Feature requests (what they ask for)
- Usage patterns (what they actually do)

**Decide**:
- Keep building? (if validation metrics hit)
- Pivot core feature? (if users use it differently)
- Shut down? (if nobody cares after 1 week)

**Iterate**:
- Fix critical bugs
- Add most-requested feature
- Improve core loop based on usage

## Integration with Other Skills

### Full Product Workflow

1. **Idea Validator** → Is this idea worth building?
   - Market analysis
   - Demand validation
   - Competitor research

2. **Launch Planner** → Turn idea into shippable MVP
   - Scope MVP features
   - Generate PRD
   - Create starter prompts

3. **Design Guide** → Build with modern UI
   - Apply design principles
   - Use Design Guide components

4. **Confidence Check** → Verify before coding
   - Technical validation
   - Architecture review

5. **Roadmap Builder** → Plan post-launch features
   - Prioritize user requests
   - Decide what to build next

## Quick Reference

### MVP Scoping Questions
- Who is this for? (specific user)
- What ONE problem does it solve? (single focus)
- How will I know if it works? (measurable metric)

### Core Loop Test
- Is this part of core user loop? (essential)
- Can users get value without this? (optional if yes)
- Can we fake/skip this for MVP? (defer if yes)

### 1-Week Rule
- If feature takes >1 week → cut, simplify, or fake it
- Day 1-3: Core features
- Day 4-5: Deploy + test
- Day 6-7: Buffer

### Common Mistakes
- ❌ Building features nobody asked for
- ❌ Over-engineering
- ❌ Adding auth before validating
- ❌ Perfect UI before launch
- ❌ Building for edge cases

### Default Tech Stack
- Frontend: Next.js + Tailwind
- Backend: Supabase
- Deploy: Vercel
- Don't overthink it

### Launch Checklist
- ✅ Core features work
- ✅ Deployed to production
- ✅ Mobile responsive
- ✅ Success metric defined
- ❌ NOT perfect UI
- ❌ NOT edge cases

## Remember

**Your goal**: Ship working MVP in 1 week, validate with real users, iterate based on data.

**Not your goal**: Build perfect product, anticipate every need, optimize prematurely.

**Mantra**: Ship fast, learn fast, iterate fast. Done is better than perfect.
