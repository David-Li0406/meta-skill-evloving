# Onboarding New Team Members

Guide for getting new developers up to speed with Claude Code and team workflows.

## Onboarding Checklist

### Day 1: Environment Setup

- [ ] Install Claude Code CLI
- [ ] Clone project repository
- [ ] Run `bun install`
- [ ] Verify `bun dev` starts successfully
- [ ] Verify `bun test` passes

### Day 1: Claude Code Setup

- [ ] Create personal config `~/.claude/CLAUDE.md`
- [ ] Review project CLAUDE.md
- [ ] Review `.claude/rules/*.md`
- [ ] Test Claude understands project context

### Week 1: Learn Conventions

- [ ] Read code style standards
- [ ] Complete small starter task
- [ ] Get first PR reviewed
- [ ] Attend code review session

### Month 1: Full Integration

- [ ] Complete larger feature
- [ ] Review others' PRs
- [ ] Suggest improvements to standards
- [ ] Help next new team member

## Personal Configuration

New team members should create `~/.claude/CLAUDE.md`:

```markdown
# Personal Claude Config

## About Me
- Name: [Your Name]
- Role: [Frontend/Backend/Full Stack]
- Experience: [Junior/Mid/Senior]

## Personal Preferences
- Editor: VS Code / WebStorm / etc.
- Prefer detailed explanations: Yes/No
- Working hours: [timezone]

## Learning Focus
- Currently learning: [frameworks, patterns]
- Ask me to explain: [when uncertain about these areas]

## Communication Style
- I prefer: step-by-step guidance / quick answers
- Code comments: verbose / minimal
```

## First Day Script

New team member should run:

```bash
# 1. Clone and setup
git clone [repo-url]
cd [project]
bun install

# 2. Verify project works
bun dev    # Should start without errors
bun test   # Should pass

# 3. Check Claude Code setup
claude --version  # Should show latest version

# 4. Verify Claude understands project
# Ask Claude: "Summarize this project's tech stack and conventions"
# Claude should reference CLAUDE.md content
```

## Project Orientation

Include in CLAUDE.md for new team members:

```markdown
## New Team Member Guide

### Quick Start
```bash
bun install          # Install dependencies
bun dev              # Start dev server (localhost:3000)
bun test             # Run tests
```

### Key Files to Read First
1. `CLAUDE.md` - This file, project overview
2. `.claude/rules/code-style.md` - Coding conventions
3. `docs/ARCHITECTURE.md` - System design
4. `src/README.md` - Source code organization

### Who to Ask
- API questions: @backend-team
- UI questions: @frontend-team
- DevOps: @infra-team
- General: #dev-questions channel

### First Tasks
Look for issues labeled `good-first-issue` in the tracker.
```

## Starter Tasks

Create a set of graduated starter tasks:

### Level 1: Minimal (Day 1-2)

```markdown
## Starter Task: Fix Typo in Error Message

**Goal:** Get familiar with the codebase and workflow.

### Steps
1. Find the typo in `src/components/ErrorBanner.tsx`
2. Fix it
3. Run `bun test` to verify no breakage
4. Create PR following team conventions

### Success Criteria
- PR created with correct title format
- Tests pass
- Review approved
```

### Level 2: Small Feature (Week 1)

```markdown
## Starter Task: Add Loading State

**Goal:** Add loading indicator to UserList component.

### Steps
1. Find `src/components/UserList.tsx`
2. Add loading state using existing Spinner component
3. Write test for loading state
4. Create PR

### Hints
- Look at `ProductList.tsx` for similar pattern
- Use `isLoading` from React Query hook
```

### Level 3: Full Feature (Week 2-3)

```markdown
## Starter Task: User Profile Page

**Goal:** Create new user profile page.

### Requirements
- Route: `/users/:id`
- Display user info from API
- Handle loading and error states
- Write tests

### This will teach you
- Routing patterns
- API integration
- Component structure
- Testing approach
```

## Onboarding Skill

Create `.claude/skills/onboarding/SKILL.md`:

```yaml
---
name: onboarding
description: Guide for onboarding new team members to this project.
---

# Onboarding Guide

Welcome to [Project Name]!

## Day 1 Setup

1. **Clone and Install**
   ```bash
   git clone [repo-url]
   cd [project]
   bun install
   ```

2. **Verify Setup**
   ```bash
   bun dev    # Start dev server
   bun test   # Run tests
   ```

3. **Personal Config**
   Create `~/.claude/CLAUDE.md` with your preferences.

## Key Resources

| Resource | Location |
|----------|----------|
| Project docs | `docs/` |
| API reference | `docs/api.md` |
| Architecture | `docs/ARCHITECTURE.md` |
| Conventions | `.claude/rules/` |

## Common Commands

```bash
bun dev              # Start development
bun test             # Run tests
bun test:watch       # Tests in watch mode
bun lint             # Check code style
bun build            # Production build
```

## Getting Help

- Check existing code for patterns
- Search issues/PRs for context
- Ask in #dev-questions
- Schedule pairing session

## Your First PR

1. Pick a `good-first-issue`
2. Create feature branch
3. Implement with tests
4. Submit PR with description
5. Address review comments
```

## Mentorship Pattern

Pair new members with experienced ones:

```markdown
## Mentorship Program

### Mentor Responsibilities
- Answer questions (DM or channel)
- Review first 3 PRs
- Weekly 30-min check-in
- Help navigate codebase

### Mentee Expectations
- Ask questions (no "stupid" questions)
- Share blockers early
- Take notes
- Help improve docs when confused

### Pairing Sessions
- First week: Daily 30-min pairing
- Second week: 2-3 sessions
- After: As needed
```

## Common New Member Questions

Add an FAQ section:

```markdown
## FAQ

### Q: How do I run a single test file?
```bash
bun test src/services/user.test.ts
```

### Q: How do I reset my local database?
```bash
bun db:reset  # Drops and recreates
```

### Q: Where do I put new components?
Components go in `src/components/[feature]/`. See existing examples.

### Q: How do I add a new API endpoint?
1. Create handler in `src/routes/`
2. Add schema in `src/schemas/`
3. Write tests
4. Document in `docs/api.md`

### Q: Who reviews my PR?
Use CODEOWNERS file. GitHub assigns automatically.

### Q: How long should PRs be open?
Target 24-48 hours for initial review.
```

## Onboarding Feedback

Collect feedback to improve:

```markdown
## Onboarding Feedback (After Week 1)

Please share your experience:

1. **Setup Experience**
   - Any blockers during setup?
   - Missing documentation?
   - Unclear instructions?

2. **Documentation Quality**
   - CLAUDE.md helpful?
   - Rules files clear?
   - Missing information?

3. **Team Support**
   - Response time to questions?
   - Pairing session helpful?
   - Suggestions for improvement?

4. **Starter Tasks**
   - Appropriate difficulty?
   - Good learning experience?
   - Better task ideas?

Submit feedback to: [channel/form/doc]
```

## Continuous Improvement

### Track Onboarding Metrics

- Time to first PR merged
- Number of questions in first week
- Blockers encountered
- Documentation gaps found

### Regular Updates

After each onboarding:
1. Review feedback
2. Update CLAUDE.md with clarifications
3. Add FAQs for common questions
4. Improve starter task descriptions
5. Update this onboarding guide

### Onboarding Champions

Rotate onboarding responsibilities:
- One person owns onboarding process
- Update docs after each new hire
- Collect and implement feedback
- Train other mentors
