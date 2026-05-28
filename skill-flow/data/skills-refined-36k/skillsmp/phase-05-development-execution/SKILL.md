---
name: "phase_05_development_execution"
description: "Execute development in sprints with continuous quality. Sprint planning, code development, code reviews, security in development (shift left), unit testing, integration, and documentation."
phase: 5
phase_name: "Development Execution"
owner: "Technical Lead"
secondary_owner: "Project Manager (coordination)"
participants: ["Developers", "QA", "Product Owner", "Security Lead", "Tech Lead", "Scrum Master"]
entry_criteria: [
  "Work breakdown structure completed",
  "Resource plan approved",
  "Risk register created",
  "Quality and test plan approved",
  "Security and compliance plan approved",
  "CI/CD pipeline implemented",
  "Sprint 0 completed",
  "Development environment ready"
]
exit_criteria: [
  "All planned features implemented",
  "Unit tests passing (70-80% coverage)",
  "Code reviews completed for all changes",
  "Security reviews completed",
  "Integration tests passing",
  "Documentation updated",
  "Build artifacts ready",
  "Go/no-go decision to proceed to Phase 6"
]
estimated_duration: "8-16 weeks (multiple sprints)"
dependencies: ["phase_04_development_planning"]
outputs: [
  "Source code (version controlled)",
  "Unit tests (passing)",
  "Code review records",
  "Security review findings",
  "Integration test results",
  "Technical documentation",
  "Sprint deliverables"
]
next_phase: "phase_06_quality_security"
---

# Phase 5: Development Execution
### Where Plans Become Reality

Welcome to **Phase 5** - this is where the rubber meets the road! After all the careful planning in Phases 1-4, we finally get to build something real. Exciting, right?

Think of this phase as a series of 2-week sprints where your team transforms requirements into working, tested, secure code. You'll move fast, break things (in a safe way), fix them, and keep improving.

**The mindset here:** Ship small, ship often, learn continuously.

---

## What You'll Achieve

By the end of this phase, you'll have:

-  Working software that meets all requirements
-  Code that's tested, reviewed, and secure
-  A team rhythm that's sustainable and productive
-  Confidence that what you built actually works

**What happens next:** Phase 6 will put everything through rigorous testing to catch anything we missed.

---

## Who's Driving This Phase?

| Role | What They're Responsible For |
|------|-----------------------------|
| **Technical Lead** | Your development coach and quality gatekeeper |
| **Developers** | The builders - turning designs into reality |
| **Scrum Master** | Your rhythm keeper - keeping sprints flowing smoothly |
| **Security Lead** | Making sure security isn't an afterthought |
| **QA Lead** | Quality happens here, not later in Phase 6 |

---

## The Development Sprint Cycle

Picture a 2-week rhythm that looks like this:

```
Week 1: Plan → Build → Test → Review
Week 2: Refine → Complete → Demo → Reflect
Repeat until all features are done
```

Let's break down what actually happens during each sprint.

---

## Step 1: Sprint Planning (Start Strong)

**Time needed:** 2 hours per sprint
**Led by:** Tech Lead + Scrum Master

### What You're Doing

At the start of each sprint, the team gathers to decide what you'll build. This isn't about overcommitting - it's about choosing realistic goals and setting everyone up for success.

### The Agenda

1. **Review the sprint goal** - What's the one thing we must achieve?
2. **Select stories** - Pull from the prioritized backlog (from Phase 4)
3. **Estimate effort** - Be honest about capacity, not optimistic
4. **Identify dependencies** - What might block us?
5. **Commit as a team** - Everyone agrees this is achievable

<details>
<summary><strong>Deep Dive: Running Great Sprint Planning</strong></summary>

**Do This:**
- Start with the sprint goal, not the story list
- Let developers choose their own tasks (autonomy builds ownership)
- Break big stories into smaller ones (should fit in 1-3 days)
- Leave buffer for the unexpected (20% capacity is smart)
- End with confidence, not concern

**Avoid This:**
- Story point poker games (they're not as useful as talking)
- Committing to 120% capacity (that's how sprints fail)
- Ignoring technical debt (it will slow you down)
- Skipping the "definition of done" discussion

**Red Flag:** If anyone says "we'll figure it out later," stop and figure it out now.

</details>

### What You'll Have

**Expected Output:**
- Sprint backlog with clear task assignments
- Sprint goal statement
- Confidence that the team can deliver

**Who Approves:**
- Tech Lead confirms the work is technically sound
- Product Owner confirms the work delivers value

---

## Step 2: Daily Development (The Heart of Agile)

**Time needed:** Every day
**Owned by:** Each developer

### The Daily Rhythm

Every day, your team syncs for 15 minutes (the "standup"). Keep it focused:

1. **What did I complete yesterday?**
2. **What will I work on today?**
3. **What's blocking me?**

**Pro tip:** This isn't a status report for management. It's a team coordination meeting to unblock each other.

### Writing Code That Lasts

While coding, follow these habits:

<details>
<summary><strong>Code Quality Checklist (Use This Daily)</strong></summary>

- [ ] Code follows team standards (agreed in Phase 3)
- [ ] Variable names explain themselves (no cryptic abbreviations)
- [ ] Functions do one thing well (keep them small)
- [ ] Error handling is thoughtful (not just catch-all exceptions)
- [ ] Security is built in (no hardcoded secrets, validate inputs)
- [ ] Tests are written alongside code (TDD is encouraged)
- [ ] Comments explain *why*, not *what* (code should be self-documenting)
- [ ] Documentation is updated as you go (not as an afterthought)

**Remember:** Future you will thank present you for clean code.

</details>

### What You'll Have

**Expected Output:**
- Working features in the development branch
- Unit tests that pass (aim for 70-80% coverage)
- Self-reviewed code ready for peer review

**Who Approves:**
- You (self-review is the first gate)
- CI/CD pipeline (must pass all automated checks)

---

## Step 3: Code Reviews (Where Learning Happens)

**Time needed:** Within 24-48 hours of submission
**Led by:** Tech Lead + Senior Developers

### Why Reviews Matter

Code reviews aren't about criticism - they're about:
- Catching bugs before they reach production
- Sharing knowledge across the team
- Maintaining code quality standards
- Building collective code ownership

Think of it as pair programming, just not at the same time.

### The Review Process

1. **Developer submits** with a clear description of what changed and why
2. **Reviewer examines** within 24 hours (respect everyone's time)
3. **Feedback is given** constructively (ask questions, don't just point fingers)
4. **Developer responds** to each comment (explain or fix)
5. **Approval happens** when code is ready to merge

<details>
<summary><strong>Review Checklist: What to Look For</strong></summary>

**Correctness:**
- Does the code do what it's supposed to do?
- Are edge cases handled?
- Is error handling appropriate?

**Security:**
- Are inputs validated?
- Are secrets properly managed?
- Are there obvious vulnerabilities?

**Performance:**
- Will this scale?
- Are there unnecessary database queries?
- Is caching used appropriately?

**Maintainability:**
- Is the code readable?
- Is it overly complex?
- Would a new team member understand this?

**Testing:**
- Are there tests for the happy path?
- Are there tests for edge cases?
- Do tests actually test the right things?

**Pro tip:** If a review takes more than 30 minutes, the PR is probably too big. Keep changes small and focused.

</details>

### What You'll Have

**Expected Output:**
- Code review comments and resolutions
- Approved pull requests
- Code quality metrics tracked over time

**Who Approves:**
- At least one reviewer (usually a senior developer)
- Tech Lead gives final merge approval
- Security Lead reviews for sensitive changes

---

## Step 4: Security (Built In, Not Bolted On)

**Time needed:** Continuous throughout development
**Led by:** Security Lead

### Shift Left Means Start Now

"Shift left" is fancy talk for addressing security early, not as a final step. Here's what that looks like in practice:

### Daily Security Habits

- **Scan dependencies** automatically (SAST tools in your CI/CD)
- **Check credentials** never make it into code (use secret scanning)
- **Validate inputs** on every API endpoint
- **Follow secure coding** guidelines (OWASP Top 10 awareness)
- **Ask questions** when something feels "off"

<details>
<summary><strong>Common Security Pitfalls to Avoid</strong></summary>

**Don't Do This:**
- Hardcode API keys or passwords (use environment variables)
- Trust client-side input (always validate server-side)
- Use outdated libraries (keep dependencies updated)
- Log sensitive data (PII, tokens, passwords)
- Roll your own crypto (use established libraries)
- Ignore security warnings (fix them immediately)

**Do This Instead:**
- Use secret management tools (HashiCorp Vault, AWS Secrets Manager)
- Validate and sanitize all inputs
- Run SAST/SCA scans on every PR
- Follow the principle of least privilege
- Encrypt data at rest and in transit
- Participate in threat modeling sessions

**Remember:** Security is everyone's job, not just the security lead's.

</details>

### What You'll Have

**Expected Output:**
- Security scan results (SAST, SCA)
- Security review records for sensitive changes
- Vulnerability remediation tracker
- Threat model updates (if new risks emerge)

**Who Approves:**
- Security Lead validates security posture
- Tech Lead confirms fixes are feasible

---

## Step 5: Unit Testing (Your Safety Net)

**Time needed:** Continuous, alongside development
**Owned by:** Developers

### Why Unit Tests Matter

Unit tests are your first line of defense against bugs. They:
- Catch regressions early (when you change something, you know if you broke something else)
- Document how code is supposed to work
- Make refactoring safer (you can change with confidence)
- Reduce debugging time (fail fast, fix early)

### The Testing Mindset

Think about testing like this: For every piece of code, ask yourself:
- What should this do when everything works?
- What could go wrong?
- What are the edge cases?

Then write tests for all of it.

<details>
<summary><strong>Testing Best Practices</strong></summary>

**What Makes a Good Unit Test:**
- Tests one thing only (avoid giant test methods)
- Is fast (unit tests should run in seconds, not minutes)
- Is deterministic (same result every time)
- Is readable (test names should describe what they test)
- Is independent (tests shouldn't depend on each other)

**Test Coverage Goals:**
- Aim for 70-80% coverage (don't obsess over 100%)
- Prioritize critical paths and complex logic
- Don't test getters/setters (that's not valuable)
- Do test error handling and edge cases

**TDD (Test-Driven Development):**
- Write the test first (it will fail - that's expected)
- Write the minimum code to make it pass
- Refactor to clean up
- Repeat

TDD isn't mandatory, but teams that use it tend to have fewer bugs.

</details>

### What You'll Have

**Expected Output:**
- Passing unit test suite
- Coverage reports (70-80% target)
- Test data fixtures and mocks
- CI/CD pipeline running tests on every change

**Who Approves:**
- CI/CD pipeline (tests must pass to merge)
- QA Lead validates coverage is meaningful (not just empty tests)

---

## Step 6: Continuous Integration (Stay in Sync)

**Time needed:** Continuous, on every commit
**Led by:** Tech Lead + DevOps

### What CI Actually Does

Every time someone pushes code, the CI/CD pipeline:
1. Runs all tests (unit, integration)
2. Scans for security issues
3. Checks code quality metrics
4. Builds the artifact
5. Deploys to staging (or tells you what broke)

This means you catch issues immediately, not days later when you try to release.

### The Git Workflow

Here's the rhythm:

```
1. Create feature branch from main
2. Write code + tests (TDD if you're brave)
3. Commit frequently (small, focused changes)
4. Push to remote
5. Open pull request with clear description
6. Wait for CI to pass (automated checks)
7. Request code review
8. Address feedback
9. Merge when approved
10. Delete feature branch (keep main clean)
```

<details>
<summary><strong>Dealing With Merge Conflicts</strong></summary>

Merge conflicts happen. They're not a failure, they're part of the process.

**When Conflicts Happen:**
1. Don't panic (this is normal)
2. Pull latest changes from main
3. Identify what conflicts (git will show you)
4. Talk to the other developer (don't guess)
5. Resolve together (both "yours" and "theirs" might be right)
6. Run tests (make sure nothing broke)
7. Commit the resolution
8. Push and continue

**Pro tip:** Small, frequent commits mean smaller conflicts. Large, infrequent commits mean nightmare conflicts.

</details>

### What You'll Have

**Expected Output:**
- CI/CD pipeline running successfully
- Integration tests passing
- Build artifacts generated
- Clean git history

**Who Approves:**
- CI/CD pipeline (automated gate)
- Tech Lead (manual merge approval)

---

## Step 7: Documentation (Write as You Go)

**Time needed:** Continuous, with each feature
**Owned by:** Tech Lead + Developers

### Documentation That Actually Gets Used

Nobody loves writing documentation, but everyone hates missing documentation. The trick is to write it as you go, not at the end.

### What to Document

- **APIs** - Use OpenAPI/Swagger for REST endpoints
- **Architecture decisions** - ADRs (Architecture Decision Records) explain *why* you chose something
- **Runbooks** - How to operate and troubleshoot the system
- **Known issues** - Be honest about what's not perfect
- **Getting started** - New team members should be productive in their first day

<details>
<summary><strong>Documentation Anti-Patterns (Avoid These)</strong></summary>

**Don't Do This:**
- Write everything at the end (it will be rushed and incomplete)
- Document the obvious (code should be self-explanatory)
- Let documentation get stale (update it when code changes)
- Use screenshots (they break, use code examples instead)
- Create a 100-page document nobody reads (keep it focused)

**Do This Instead:**
- Document as you code (it's fresher in your mind)
- Focus on the "why," not just the "what"
- Use examples over explanations (show, don't just tell)
- Keep it close to the code (README in each module)
- Update docs in the same PR as the code change

**Remember:** The best documentation is the kind that actually gets read.

</details>

### What You'll Have

**Expected Output:**
- Updated technical documentation
- API documentation (if applicable)
- Architecture Decision Records (ADRs)
- Runbooks for operations
- Known issues document

**Who Approves:**
- Tech Lead validates technical accuracy
- Product Owner validates user-facing docs make sense

---

## Sprint Demo and Retro (Learn and Improve)

**Time needed:** 1 hour each, end of sprint
**Led by:** Scrum Master

### The Sprint Demo (Show Your Work)

At the end of each sprint, show what you built. This isn't about perfection - it's about progress and feedback.

**Demo Tips:**
- Keep it to 30 minutes max (respect everyone's time)
- Focus on working software, not slides
- Be honest about what didn't work (transparency builds trust)
- Collect feedback immediately (product owner might have new insights)

### The Sprint Retrospective (Improve Your Process)

After the demo, the team reflects on how they worked together. This is your continuous improvement engine.

**Three Questions:**
1. What went well? (keep doing this)
2. What didn't go well? (change this)
3. What will we improve next sprint? (actionable commitment)

**Pro tip:** Pick one or two improvements per sprint. Trying to fix everything at once fixes nothing.

---

## Quality Gates: Are We Ready for Phase 6?

Before you can move to Phase 6 (Quality & Security Validation), confirm:

- [ ] **All planned features are implemented** - Nothing left to code
- [ ] **Unit tests are passing** - With 70-80% coverage
- [ ] **All code has been reviewed** - No unreviewed code in main
- [ ] **Security reviews are complete** - No critical vulnerabilities
- [ ] **Integration tests are passing** - Components work together
- [ ] **Documentation is updated** - Docs match the code
- [ ] **Build artifacts are ready** - Deployable package exists
- [ ] **Go/no-go decision made** - Team agrees to proceed

**If anything is missing:** Don't panic. Just identify what's needed and create a plan to complete it. Quality gates exist to protect you, not to block you.

---

## Metrics That Matter

Track these to understand how you're doing:

| Metric | What It Tells You | Target |
|--------|------------------|--------|
| **Sprint Velocity** | How much work you complete per sprint | Establish baseline, then improve |
| **Code Coverage** | How much code is tested | 70-80% |
| **Code Review Turnaround** | How fast reviews happen | <24 hours |
| **Build Success Rate** | How often CI/CD passes | >95% |
| **Defect Escape Rate** | How many bugs reach later phases | <5% |
| **Security Vulnerabilities** | Security posture | Zero critical |

**Remember:** Metrics are for learning, not blame. Use them to identify patterns and improve, not to punish individuals.

---

## Common Pitfalls (And How to Avoid Them)

<details>
<summary><strong>Pitfall 1: Overcommitting to Sprints</strong></summary>

**The Problem:** Teams often commit to too much work, thinking they'll go faster.

**The Fix:**
- Leave 20% buffer for the unexpected
- Track velocity over several sprints (it takes 3-5 sprints to stabilize)
- Say no to scope creep during the sprint

</details>

<details>
<summary><strong>Pitfall 2: Skipping Code Reviews</strong></summary>

**The Problem:** "We're behind, let's skip reviews to catch up."

**The Fix:**
- Never skip reviews (they save time by catching bugs early)
- If you're behind, reduce scope, not quality
- Automate what you can (linters, formatters)

</details>

<details>
<summary><strong>Pitfall 3: Treating Tests as Optional</strong></summary>

**The Problem:** Tests are written "when there's time" (which is never).

**The Fix:**
- Make tests part of the definition of done
- Block PRs that don't include tests
- Celebrate high coverage (make it a team metric)

</details>

<details>
<summary><strong>Pitfall 4: Documentation Debt</strong></summary>

**The Problem:** "We'll write docs at the end" (which never happens).

**The Fix:**
- Require docs to be updated in the same PR as code changes
- Assign docs in sprint backlog (make them visible)
- Keep docs close to code (README files in each module)

</details>

---

## Words of Encouragement

Phase 5 is intense. You're in the thick of it, balancing speed with quality, features with security, and immediate needs with long-term maintainability.

**Remember:**
- You don't have to be perfect, you have to be progressing
- Bugs happen (that's why we have testing and reviews)
- Communication is your superpower (ask for help early)
- Celebrate small wins (every merged PR is progress)

**You've got this.** The plans from Phases 1-4 were good, but what you're building now is real. That's worth celebrating.

---

## What's Next

Once all quality gates are met and the team agrees, you'll move to **Phase 6: Quality & Security Validation**. There, everything you've built will be put through comprehensive testing to catch anything you might have missed.

Think of Phase 5 as building the car, and Phase 6 as the safety inspections before it goes on the road. Both are essential.

**Next up:** Validation, testing, and confidence that what you built is ready for the real world.

---

**Previous Phase:** [Phase 4: Development Planning](../phase_04_development_planning/SKILL.md)
**Next Phase:** [Phase 6: Quality & Security Validation](../phase_06_quality_security/SKILL.md)

---

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
