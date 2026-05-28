# Onboarding Difficulty Assessment

Guide for assessing and reducing the time required for new developers to become productive.

## Onboarding Phases

### Phase 1: Environment Setup (Day 1)
- Clone repository
- Install dependencies
- Run tests
- Start development server

**Target**: < 2 hours

### Phase 2: Understanding Architecture (Days 2-5)
- Read documentation
- Understand module boundaries
- Learn domain concepts
- Identify key abstractions

**Target**: < 1 week for basic understanding

### Phase 3: First Contribution (Week 2)
- Find good first issue
- Make small change
- Get PR approved
- Merge to production

**Target**: < 2 weeks for first merge

### Phase 4: Independent Work (Weeks 3-4)
- Take on feature work
- Make design decisions
- Review others' code
- Productive team member

**Target**: < 4 weeks for full productivity

## Difficulty Assessment Rubric

### Score: 1-2 (Very Easy)

**Characteristics**:
- Self-contained modules
- Clear naming and documentation
- Minimal domain knowledge required
- Few dependencies between modules
- Consistent patterns throughout

**Example**: Well-architected Phoenix API with comprehensive docs

**Time to productivity**: 3-5 days

### Score: 3-4 (Easy)

**Characteristics**:
- Mostly self-contained
- Good documentation
- Some domain knowledge needed
- Moderate dependencies
- Mostly consistent patterns

**Example**: Standard CRUD application with some business logic

**Time to productivity**: 1-2 weeks

### Score: 5-6 (Moderate)

**Characteristics**:
- Some tightly coupled modules
- Partial documentation
- Significant domain knowledge required
- Complex dependencies
- Some pattern inconsistencies

**Example**: E-commerce platform with multiple integrations

**Time to productivity**: 2-4 weeks

### Score: 7-8 (Hard)

**Characteristics**:
- Many coupled modules
- Minimal documentation
- Deep domain knowledge required
- Hidden dependencies
- Pattern inconsistencies

**Example**: Legacy system with accumulated complexity

**Time to productivity**: 4-8 weeks

### Score: 9-10 (Very Hard)

**Characteristics**:
- Tightly coupled throughout
- Sparse or outdated documentation
- Tribal knowledge required
- Implicit dependencies everywhere
- No consistent patterns

**Example**: 10-year-old system with many authors, no refactoring

**Time to productivity**: 2-6 months

## Assessment Checklist

### Documentation Quality (0-10 points)

- [ ] README with quick start (2 points)
- [ ] Architecture documentation (2 points)
- [ ] API documentation (1 point)
- [ ] Domain glossary (2 points)
- [ ] ADRs for major decisions (2 points)
- [ ] Onboarding guide (1 point)

**Score**: Sum of checked items

### Code Clarity (0-10 points)

- [ ] Consistent naming conventions (2 points)
- [ ] Self-documenting code (2 points)
- [ ] Appropriate comments (why, not what) (2 points)
- [ ] Clear module boundaries (2 points)
- [ ] Minimal surprises (2 points)

**Score**: Sum of checked items

### System Knowledge Required (0-10 points, lower is better)

- [ ] Must understand <3 core modules (0 points)
- [ ] Must understand 3-5 core modules (3 points)
- [ ] Must understand 6-10 core modules (6 points)
- [ ] Must understand >10 core modules (10 points)

**Score**: Select applicable item

### Domain Complexity (0-10 points, lower is better)

- [ ] Domain concepts clear from code (0 points)
- [ ] Domain documented (2 points)
- [ ] Domain requires expert consultation (5 points)
- [ ] Domain requires tribal knowledge (8 points)
- [ ] Domain undocumented and complex (10 points)

**Score**: Select highest applicable item

### Total Onboarding Score

```
Score = (
  (10 - Documentation Quality) +
  (10 - Code Clarity) +
  System Knowledge Required +
  Domain Complexity
) / 4
```

## Reducing Onboarding Difficulty

### Quick Wins (1-2 days effort)

1. **Create comprehensive README**
```markdown
# Project Name

## Quick Start
```bash
git clone ...
mise install
mix deps.get
mix ecto.setup
mix phx.server
```

Visit http://localhost:4000

## Architecture
[High-level overview with diagrams]

## Key Concepts
[Domain glossary]

## Common Tasks
- Run tests: `mix test`
- Check quality: `mix precommit`
- etc.
```

2. **Add module documentation**
```elixir
defmodule MyApp.Accounts do
  @moduledoc """
  The Accounts context manages users and authentication.

  ## Responsibilities
  - User registration and management
  - Authentication (email/password, OAuth)
  - Session management
  - Password reset workflows

  ## Key Concepts
  - **User**: Person with account in system
  - **Session**: Active authentication period
  - **Token**: Temporary access credential

  ## Examples

      iex> Accounts.register_user(%{email: "...", password: "..."})
      {:ok, %User{}}

      iex> Accounts.authenticate("email", "password")
      {:ok, %User{}}
  """
end
```

3. **Create domain glossary**
```markdown
# Domain Glossary

## User
A person with an account in the system.
- States: unverified, active, suspended, deleted
- Transitions: (diagram)

## Order
A purchase request from a user.
- States: cart, pending, paid, shipped, delivered, cancelled
- Lifecycle: (flowchart)

## Product
An item available for purchase.
- Types: physical, digital, service
- Inventory: tracked for physical only
```

### Medium Effort (3-5 days)

4. **Document architecture decisions**

Create ADRs (Architecture Decision Records):

```markdown
# ADR 001: Use Phoenix Contexts for DDD

## Status
Accepted

## Context
As codebase grew, needed clear module boundaries and prevented tightly coupled code.

## Decision
Organize code using Phoenix Contexts following Domain-Driven Design.

## Consequences
**Positive**:
- Clear ownership of functionality
- Easier to find code
- Prevents cross-context coupling

**Negative**:
- Learning curve for developers new to DDD
- More files/directories

## References
- Phoenix Contexts Guide: https://hexdocs.pm/phoenix/contexts.html
```

5. **Create onboarding guide**

```markdown
# Onboarding Guide

## Week 1: Getting Started

### Day 1: Environment Setup
1. Complete README quick start
2. Run test suite: `mix test`
3. Browse codebase structure
4. Read this guide

### Day 2-3: Core Concepts
1. Read architecture documentation
2. Study domain glossary
3. Understand key contexts:
   - Accounts (user management)
   - Orders (purchase flow)
   - Products (catalog)

### Day 4-5: First Contribution
1. Find "good first issue" in GitHub
2. Read relevant modules
3. Make small change
4. Submit PR

## Week 2: Feature Work

### Learning Resources
- Context pattern: lib/my_app/accounts.ex (good example)
- LiveView patterns: lib/my_app_web/live/user_live.ex
- Testing approach: test/my_app/accounts_test.exs

### Common Questions

**Q**: Where does validation happen?
**A**: In Ecto changesets (e.g., User.changeset/2)

**Q**: How do I add a new API endpoint?
**A**: See Router docs, add to appropriate scope

[More Q&A]

## Week 3-4: Independent Work

By now you should be able to:
- Take features from issue to production
- Review PRs from other developers
- Make architectural suggestions

### Advanced Topics
- Performance optimization
- Distributed systems patterns
- Production debugging

## Resources
- [Link to architecture docs]
- [Link to API docs]
- [Link to deployment guide]
- [Team Slack channels]
```

6. **Add learning tests**

Tests that demonstrate how system works:

```elixir
defmodule OnboardingTest do
  use MyApp.DataCase

  @moduledoc """
  Learning tests demonstrating how the system works.
  Read these to understand key behaviors.
  """

  describe "user registration flow" do
    test "complete registration workflow" do
      # Step 1: User submits registration
      attrs = %{
        name: "Alice",
        email: "alice@example.com",
        password: "Secret123"
      }

      assert {:ok, user} = Accounts.register_user(attrs)

      # Step 2: User receives verification email
      assert_email_sent(to: "alice@example.com", subject: "Verify your email")

      # Step 3: User clicks verification link
      assert {:ok, verified_user} = Accounts.verify_email(user.verification_token)

      # Step 4: User can now log in
      assert {:ok, authenticated_user} = Accounts.authenticate("alice@example.com", "Secret123")

      # Demonstrates complete flow with all steps
    end
  end

  describe "order lifecycle" do
    test "complete order flow from cart to delivery" do
      # Shows how orders move through states
      # ...
    end
  end
end
```

### Long-term Investment (1-2 weeks)

7. **Refactor for clarity**

Apply cognitive complexity patterns:
- Deep modules
- Eliminate temporal coupling
- Clear naming
- Consistent abstractions

8. **Video walkthroughs**

Record videos:
- Architecture overview (15 min)
- Adding a feature (30 min)
- Debugging common issues (20 min)

9. **Pair programming sessions**

Schedule with new developers:
- Week 1: Walkthrough session
- Week 2: Feature implementation
- Week 3: Code review session
- Week 4: Architecture discussion

## Measuring Improvement

### Before Refactoring

Track metrics:
- Time to first commit: X days
- Time to independent work: Y weeks
- Questions asked: Z per week
- Onboarding score: N/10

### After Refactoring

Measure same metrics:
- Time to first commit: should decrease
- Time to independent work: should decrease
- Questions asked: should decrease
- Onboarding score: should improve

**Target improvements**:
- 30-50% reduction in time to productivity
- Onboarding score improvement of 2-3 points

## Red Flags

Signs of high onboarding difficulty:

1. **"Just ask [person]"**
   - Tribal knowledge instead of documentation
   - **Fix**: Document what [person] knows

2. **"It's complicated"**
   - Unclear architecture or business logic
   - **Fix**: Create architectural overview

3. **"Look at similar feature"**
   - No clear patterns documented
   - **Fix**: Document patterns in project-learnings.md

4. **"Be careful with [module]"**
   - High-risk areas not well understood
   - **Fix**: Refactor for clarity, add tests, document gotchas

5. **"We don't touch that code"**
   - Legacy complexity preventing change
   - **Fix**: Create learning tests, refactor incrementally

## Onboarding Guide Template

```markdown
# [Project] Onboarding Guide

## Before You Start

- [ ] Environment setup complete
- [ ] Test suite passes
- [ ] Development server running
- [ ] GitHub access configured

## Week 1: Learning Phase

### Day 1
**Goal**: Understand project structure

**Tasks**:
1. Read README and architecture docs
2. Explore codebase structure
3. Run test suite, understand test organization
4. Set up development tools (editor, linter, formatter)

**Resources**:
- Architecture: docs/architecture.md
- Domain glossary: docs/domain.md

### Day 2-3
**Goal**: Understand core concepts

**Tasks**:
1. Study [Context A] (most important)
   - Read: lib/my_app/[context_a].ex
   - Tests: test/my_app/[context_a]_test.exs
   - Purpose: [what it does]

2. Study [Context B]
   - Read: lib/my_app/[context_b].ex
   - Tests: test/my_app/[context_b]_test.exs
   - Purpose: [what it does]

**Resources**:
- Example: [link to good example module]

### Day 4-5
**Goal**: First contribution

**Tasks**:
1. Find "good first issue" labeled issue
2. Read relevant code
3. Make change following patterns
4. Submit PR

**Tips**:
- Ask questions early and often
- Follow existing patterns
- Write tests first

## Week 2: Guided Feature Work

### Goals
- Complete first feature independently
- Understand PR review process
- Learn deployment workflow

### Resources
- Pattern examples: [list]
- Test examples: [list]
- Mentors: [@person1, @person2]

## Week 3-4: Independent Contribution

### Goals
- Take issues from start to finish
- Review others' PRs
- Participate in architecture discussions

### Common Patterns
[Document key patterns here]

## FAQ

**Q**: [Common question]
**A**: [Clear answer with examples]

[More Q&A pairs]

## Getting Help

- Questions about code: #engineering Slack
- Questions about domain: #product Slack
- Blockers: Tag @mentor
- Architecture: Schedule with @tech-lead

## Success Criteria

By end of Week 4, you should:
- [ ] Complete 3+ features independently
- [ ] Review 5+ PRs
- [ ] Understand core architecture
- [ ] Be productive team member
```

## Continuous Improvement

1. **Collect feedback** from new hires
2. **Update documentation** based on common questions
3. **Refactor** high-complexity areas identified during onboarding
4. **Measure** onboarding metrics over time
5. **Celebrate** successful onboarding milestones
