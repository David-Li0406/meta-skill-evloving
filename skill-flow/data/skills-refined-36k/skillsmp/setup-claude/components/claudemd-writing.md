# CLAUDE.md Writing Component

This component provides best practices and templates for creating comprehensive CLAUDE.md files with all 10 required sections.

## What is CLAUDE.md?

CLAUDE.md is a markdown file in your project root that provides context to Claude Code. It's automatically read when Claude starts a session, giving Claude important information about your project.

## Why CLAUDE.md Matters

Without CLAUDE.md, Claude:
- Doesn't know your project's purpose
- Has to discover commands by reading package.json
- Might suggest patterns that don't fit your codebase
- Won't know about your coding conventions
- Could miss important warnings or gotchas
- Doesn't know what skills/MCPs/subagents are available

With a good CLAUDE.md, Claude:
- Understands project context immediately
- Uses correct commands from the start
- Follows your established patterns
- Avoids common pitfalls you've documented
- Knows what tools and workflows are available

---

## The 10 Required Sections

A comprehensive CLAUDE.md includes all of these sections:

| # | Section | Purpose |
|---|---------|---------|
| 1 | Project Description | What is this project? |
| 2 | Development Workflow | How does development flow? |
| 3 | Things NOT to Do | Critical warnings |
| 4 | Common Code Practices | Coding conventions |
| 5 | Commands | dev, test, build, lint |
| 6 | Available Skills | User-invokable skills with triggers |
| 7 | MCP Servers | Enabled MCPs and when to use |
| 8 | Documentation Methods | How to look up docs |
| 9 | Subagents | When to delegate to specialized agents |
| 10 | General Guidelines | Miscellaneous guidance |

---

## Section Details

### 1. Project Description (Required)

Brief description of what the project does. Help Claude understand the domain.

```markdown
# Project Name

E-commerce platform for handmade goods. Built with Next.js 14, uses Stripe for payments,
and Convex for the database. Currently in production serving ~10k users.

**Target users**: Small business owners selling handmade products
**Key features**: Product listings, shopping cart, checkout, order management
```

**Tips:**
- Keep it brief (2-4 sentences)
- Mention key technologies
- Note production status if relevant
- Include target users and key features

### 2. Development Workflow (Required)

How does development typically flow in this project?

```markdown
## Development Workflow

1. **Create feature branch** from `main`
2. **Implement with tests** (TDD encouraged)
3. **Run checks**: `npm run lint && npm run typecheck && npm test`
4. **Create PR** with description
5. **Get review** and address feedback
6. **Merge to main** (squash merge)
7. **Auto-deploy** to production

### Local Development
1. Clone repo
2. Copy `.env.example` to `.env.local`
3. Run `npm install`
4. Run `npm run dev`
5. Open http://localhost:3000
```

**Tips:**
- Document the full flow from branch to deploy
- Include local setup steps
- Note any required tools or services

### 3. Things NOT to Do (Required)

Critical warnings and anti-patterns. Use strong language.

```markdown
## Things NOT to Do

- **NEVER** commit `.env` files (contains Stripe keys)
- **NEVER** modify files in `/legacy` (deprecated, will be removed)
- **NEVER** use `any` type - use `unknown` with type guards
- **NEVER** push directly to `main` branch
- **DON'T** skip the PR review process, even for small changes
- **DON'T** use deprecated API v1 endpoints (use v2)
- **DON'T** add console.log to production code (use logger)
```

**Tips:**
- Lead with action verbs (NEVER, DON'T, AVOID)
- Explain consequences if not obvious
- Be specific about what and why
- Include common mistakes

### 4. Common Code Practices (Recommended)

Your project's coding conventions and patterns.

```markdown
## Common Code Practices

### Component Structure
- Use functional components with hooks
- Props interface above component
- Hooks at the top, then handlers, then render

### Naming Conventions
- Components: PascalCase (`UserProfile.tsx`)
- Utilities: camelCase (`formatDate.ts`)
- Constants: SCREAMING_SNAKE_CASE

### Patterns
- Prefer `async/await` over `.then()`
- Use early returns to reduce nesting
- Extract complex logic to custom hooks
- Use Convex for all data operations

### File Organization
- Tests live next to source files (`*.test.ts`)
- Shared types in `src/types/`
- API routes in `src/app/api/`
```

**Tips:**
- Be specific and actionable
- Focus on project-specific conventions
- Note what's different from common patterns
- Include examples where helpful

### 5. Commands (Required)

Commands Claude will use frequently.

```markdown
## Commands

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server (http://localhost:3000) |
| `npm test` | Run unit tests |
| `npm run test:e2e` | Run E2E tests (Playwright) |
| `npm run build` | Build for production |
| `npm run lint` | Run ESLint |
| `npm run typecheck` | TypeScript type checking |
| `npx convex dev` | Start Convex dev server |

### Combined Commands
- **Before commit**: `npm run lint && npm run typecheck && npm test`
- **Full build check**: `npm run build && npm run test:e2e`
```

**Tips:**
- List all frequently-used commands
- Use exact commands (don't abbreviate)
- Include combined commands for common workflows
- Note any required environment setup

### 6. Available Skills (Required)

User-invokable skills with their triggers.

```markdown
## Available Skills

Skills are specialized workflows triggered by slash commands.

| Skill | Trigger | Purpose |
|-------|---------|---------|
| prd | `/prd` | Create product requirements documents |
| agent-browser | `/agent-browser` | Browser automation and E2E testing |
| react-best-practices | `/react-best-practices` | React performance optimization |
| convex-patterns | `/convex-patterns` | Convex database patterns |
| git-workflow | `/git-workflow` | Git conventions |

### When to Use Each
- **prd**: Before implementing any significant feature
- **agent-browser**: For E2E testing or browser automation tasks
- **react-best-practices**: When optimizing React components
- **convex-patterns**: When writing Convex queries/mutations
- **git-workflow**: When unsure about git conventions
```

**Tips:**
- List all installed skills with triggers
- Explain when to use each
- Skills are not preloaded (invoked on demand)

### 7. MCP Servers (Required)

What MCPs are enabled and when to use them.

```markdown
## MCP Servers

MCPs (Model Context Protocol) provide additional capabilities.

| MCP | Purpose | When to Use |
|-----|---------|-------------|
| context7 | Framework documentation | Looking up Next.js, React docs |
| shadcn | UI component docs | Adding shadcn/ui components |

### MCP vs CLI
Prefer CLIs over MCPs when available (more token-efficient):
- Use `vercel` CLI, not Vercel MCP
- Use `gh` CLI, not GitHub MCP
- Use `stripe` CLI, not Stripe MCP

### Context Window Note
Currently: 2 MCPs enabled (~15 tools)
Keep MCPs minimal to preserve context window.
```

**Tips:**
- List only enabled MCPs
- Explain when to use each
- Note CLI alternatives
- Include context window status

### 8. Documentation Methods (Required)

How to look up documentation.

```markdown
## Documentation Methods

### For Framework/Library Docs
Use Context7 MCP:
- Next.js documentation
- React documentation
- Package documentation

### For Errors and Solutions
Use web search for:
- Error messages
- Stack Overflow solutions
- GitHub issues

### Project-Specific Docs
- API docs: `/docs/api.md`
- Architecture: `/docs/architecture.md`
- Database schema: `convex/schema.ts` (source of truth)

### External Resources
- Convex docs: https://docs.convex.dev
- Stripe docs: https://stripe.com/docs
- Vercel docs: https://vercel.com/docs
```

**Tips:**
- Clarify when to use MCP vs web search
- Point to internal documentation
- List important external resources

### 9. Subagents (Recommended)

When to delegate to specialized agents.

```markdown
## Subagents

Subagents are specialized Claude instances with limited tools.

| Subagent | Tools | When to Use |
|----------|-------|-------------|
| planner | Read, Glob, Grep | Before implementing features |
| code-reviewer | Read, Glob, Grep | After completing features |
| tdd-guide | Read, Write, Edit, Bash | Test-driven development |
| refactor-cleaner | Read, Edit, Grep | Removing dead code |

### When to Delegate
- **planner**: Use before any significant implementation
- **code-reviewer**: Use before creating PR
- **tdd-guide**: Use when tests are required
- **refactor-cleaner**: Use for cleanup tasks

### How to Invoke
```
Task with subagent_type="planner"
```
```

**Tips:**
- List available subagents and their tools
- Explain when each is appropriate
- Show how to invoke

### 10. General Guidelines (Recommended)

Miscellaneous guidance that doesn't fit elsewhere.

```markdown
## General Guidelines

### Performance
- Lazy load heavy components
- Use React.memo for expensive renders
- Optimize images with next/image

### Security
- Validate all user input
- Use parameterized queries (Convex handles this)
- Never expose API keys in client code

### Testing Priority
1. Business logic (highest priority)
2. API endpoints
3. Complex UI interactions
4. Simple components (lowest priority)

### Getting Help
- Check existing code for patterns
- Search codebase with Grep before creating new utilities
- Ask if unsure about conventions
```

**Tips:**
- Catch-all for important guidance
- Include priorities and tradeoffs
- Note where to find help

---

## CLAUDE.md Generation Flow

### Step 1: Gather Information

**From existing files:**
- README.md → Project description
- package.json → Commands (scripts section)
- Directory structure → Project structure
- .claude/skills/ → Available skills
- .mcp.json → MCP configuration
- .claude/agents/ → Subagents

**From user interview:**

```
AskUserQuestion: "Describe this project in 2-3 sentences"
(Free text)
```

```
AskUserQuestion: "What are the key development commands?"
├── Dev: [input]
├── Test: [input]
├── Build: [input]
└── Lint: [input]
```

```
AskUserQuestion: "Any critical warnings or things NOT to do?"
(Free text)
```

```
AskUserQuestion: "Key coding conventions?"
├── Use functional components
├── Prefer async/await
├── Tests next to source
└── Custom: [input]
```

### Step 2: Generate Draft

Combine gathered information into CLAUDE.md with all 10 sections.

### Step 3: Review with User

Present draft and ask for feedback:

```
Here's the CLAUDE.md I've created (10 sections):

[Show content]

AskUserQuestion: "Review and approve?"
├── Accept as-is
├── Edit before saving
└── Add more details
```

### Step 4: Write File

Write to project root as `CLAUDE.md`.

---

## Audit Checklist

When auditing an existing CLAUDE.md, check for:

### Required Sections
- [ ] 1. Project Description
- [ ] 2. Development Workflow
- [ ] 3. Things NOT to Do
- [ ] 4. Common Code Practices
- [ ] 5. Commands
- [ ] 6. Available Skills
- [ ] 7. MCP Servers
- [ ] 8. Documentation Methods
- [ ] 9. Subagents
- [ ] 10. General Guidelines

### Quality Checks
- [ ] Information is current (not stale)
- [ ] Commands are correct (test them)
- [ ] Skills match what's installed
- [ ] MCPs match .mcp.json
- [ ] Subagents match .claude/agents/
- [ ] No sensitive information included

### Missing Section Recovery

For each missing section, add during audit:

| Missing | Recovery Strategy |
|---------|-------------------|
| Skills | Read .claude/skills/ directory |
| MCPs | Read .mcp.json |
| Subagents | Read .claude/agents/ directory |
| Commands | Read package.json scripts |
| Workflow | Interview user |
| Warnings | Interview user |
