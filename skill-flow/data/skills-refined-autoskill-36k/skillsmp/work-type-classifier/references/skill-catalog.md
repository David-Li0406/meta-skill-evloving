# Complete Skill Catalog for Autonomous Development

This catalog lists all available skills that autonomous-dev can invoke during development, organized by category.

## Category A: Discipline Skills (Always Active)

These skills enforce development discipline and are invoked in EVERY autonomous development session.

### superpowers:brainstorming
- **Phase:** 2 (Requirement Understanding)
- **Purpose:** Turn vague ideas into fully-formed designs through Socratic dialogue
- **Key Features:**
  - Ask ONE clarifying question at a time
  - Apply YAGNI discipline ruthlessly
  - Explore alternatives before settling
  - Output: `docs/plans/YYYY-MM-DD-<topic>-design.md`
- **Trigger:** Always invoked before planning starts

### superpowers:writing-plans
- **Phase:** 3 (Planning)
- **Purpose:** Create detailed implementation plans with exact code snippets
- **Key Features:**
  - Bite-sized tasks (2-5 minutes each)
  - Exact file paths, commands, expected output
  - TDD built-in (test → fail → implement → pass → commit)
  - Output: `.claude/plans/auto-{timestamp}.md`
- **Trigger:** After task decomposition

### superpowers:test-driven-development
- **Phase:** 4 (Execution)
- **Purpose:** Enforce RED-GREEN-REFACTOR cycle for every task
- **Key Features:**
  - NO production code without failing test first
  - Write ONE minimal test that fails
  - Implement ONLY enough code to pass
  - Refactor while tests pass
- **Trigger:** During every task implementation
- **Iron Law:** "Tests-after = what does this do? Tests-first = what should this do?"

### superpowers:systematic-debugging
- **Phase:** 4 (Execution - when tests fail)
- **Purpose:** Find root cause before attempting any fix
- **Key Features:**
  - 4 phases: Investigation → Analysis → Hypothesis → Implementation
  - NO random fixes allowed
  - Max 3 fix attempts before escalating
- **Trigger:** When any test fails unexpectedly
- **Red Flag:** "Let me just try changing X" → STOP, return to Phase 1

### superpowers:verification-before-completion
- **Phase:** 6 (Review)
- **Purpose:** Evidence before claims, always
- **Key Features:**
  - Gate function: IDENTIFY → RUN → READ → VERIFY → CLAIM
  - Run ALL verification commands fresh
  - Show ACTUAL output, not assumptions
- **Trigger:** Before any completion claim
- **Red Flag:** Words like "should", "probably", "seems to" → STOP, run verification

### superpowers:requesting-code-review
- **Phase:** 6 (Review)
- **Purpose:** Dispatch code-reviewer subagent for structured review
- **Trigger:** After verification passes

### superpowers:receiving-code-review
- **Phase:** 6 (Review)
- **Purpose:** Process feedback with technical rigor
- **Key Features:**
  - Technical rigor over performative agreement
  - Verify suggestions before implementing
  - Never say "You're absolutely right!" without verification
- **Trigger:** When receiving code review feedback

---

## Category B: Domain-Specific Skills

### B1. Frontend/UI Development

#### frontend-design (Anthropic Official)
- **When:** Building UI components, web pages, React/Vue apps
- **Key Value:** "Avoid AI slop, make bold design choices"
- **Features:**
  - Production-grade interfaces
  - Modern design patterns
  - Responsive layouts
  - Tailwind CSS expertise

#### webapp-testing (Anthropic Official)
- **When:** Testing web applications, e2e tests
- **Key Value:** Playwright-based testing
- **Features:**
  - Browser automation
  - UI verification
  - Screenshot comparison
  - Accessibility testing

#### artifacts-builder (Anthropic Official)
- **When:** Complex React/Tailwind artifacts
- **Features:**
  - Multi-component artifacts
  - shadcn/ui integration
  - State management

#### ux-designer (Community)
- **When:** Accessibility, user experience focus
- **Features:**
  - WCAG compliance
  - User flow optimization
  - Interaction design

### B2. Backend/API Development

#### architecture-patterns (Community)
- **When:** System design, Clean Architecture, DDD
- **Key Value:** Production-grade backend patterns
- **Features:**
  - Clean Architecture implementation
  - Domain-Driven Design
  - Microservices patterns
  - SOLID principles

#### api-design-principles (Community)
- **When:** REST or GraphQL API design
- **Features:**
  - RESTful conventions
  - GraphQL schema design
  - Versioning strategies
  - Error handling patterns

#### senior-architect (Community)
- **When:** Complex system design
- **Features:**
  - Multi-service architecture
  - Database schema design
  - Performance optimization
  - Diagram generation

#### mcp-builder (Anthropic Official)
- **When:** External API integrations, MCP servers
- **Features:**
  - MCP server creation
  - Tool definition
  - Authentication handling
  - Error management

### B3. Documentation & Content

#### doc-coauthoring (Anthropic Official)
- **When:** Technical docs, proposals, specs
- **Features:**
  - Structured workflow
  - Iterative refinement
  - Reader verification

#### internal-comms (Anthropic Official)
- **When:** Status reports, newsletters, FAQs
- **Features:**
  - Company format templates
  - Professional tone
  - Structured updates

### B4. Document Generation

#### pdf (Anthropic Official)
- **When:** PDF creation, manipulation, forms
- **Features:**
  - Text/table extraction
  - PDF creation
  - Merge/split
  - Form handling

#### docx (Anthropic Official)
- **When:** Word documents
- **Features:**
  - Tracked changes
  - Comments
  - Formatting preservation

#### xlsx (Anthropic Official)
- **When:** Spreadsheets, data analysis
- **Features:**
  - Formulas
  - Formatting
  - Charts
  - Data visualization

#### pptx (Anthropic Official)
- **When:** Presentations
- **Features:**
  - Slide creation
  - Layouts
  - Charts
  - Speaker notes

### B5. Creative & Visual

#### canvas-design (Anthropic Official)
- **When:** Visual art, posters, PNG/PDF design
- **Features:**
  - Design philosophy
  - Visual composition
  - Original artwork

#### algorithmic-art (Anthropic Official)
- **When:** Generative art, p5.js
- **Features:**
  - Seeded randomness
  - Flow fields
  - Particle systems
  - Interactive parameters

#### slack-gif-creator (Anthropic Official)
- **When:** Animated GIFs for Slack
- **Features:**
  - Size optimization
  - Animation concepts
  - Constraint validation

#### brand-guidelines (Anthropic Official)
- **When:** Branding, style guides
- **Features:**
  - Color schemes
  - Typography
  - Visual consistency

---

## Category C: Advanced Patterns

### superpowers:using-git-worktrees
- **When:** Parallel development branches
- **Features:**
  - Smart directory selection
  - Safety verification
  - Isolated workspaces

### superpowers:finishing-a-development-branch
- **When:** Development complete, deciding integration
- **Features:**
  - Options: Merge locally, Create PR, Keep, Discard
  - Verification before action
  - Cleanup automation

### superpowers:dispatching-parallel-agents
- **When:** Multiple independent tasks
- **Features:**
  - Concurrent subagent workflows
  - Domain-based grouping
  - Result integration

### superpowers:subagent-driven-development
- **When:** Complex feature implementation
- **Features:**
  - Fresh subagent per task
  - Two-stage review (spec + quality)
  - Context isolation

---

## Skill Invocation Reference

### How to Invoke Skills

In autonomous-dev phases, invoke skills using the Skill tool:

```
Use the Skill tool with skill: "superpowers:brainstorming"
```

### Phase-Skill Mapping Quick Reference

| Phase | Always Invoke | Conditional |
|-------|---------------|-------------|
| 1 | work-type-classifier | - |
| 2 | brainstorming | frontend-design (if FRONTEND) |
| 3 | writing-plans | - |
| 4 | test-driven-development | systematic-debugging (if failure) |
| 5 | finishing-a-development-branch | - |
| 6 | verification-before-completion, requesting-code-review | webapp-testing (if FRONTEND) |

---

## Sources

- [Superpowers Plugin](https://github.com/obra/superpowers)
- [Anthropic Agent Skills](https://code.claude.com/docs/en/skills)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
