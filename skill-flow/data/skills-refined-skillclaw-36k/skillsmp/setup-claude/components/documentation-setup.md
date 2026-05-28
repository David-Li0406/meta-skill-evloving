# Documentation Setup Component

This component guides configuring documentation access methods: Context7 MCP for framework docs, web search for errors/solutions, and project-specific documentation.

## Documentation Strategy

| Documentation Need | Method | When to Use |
|-------------------|--------|-------------|
| Framework/library docs | Context7 MCP | API reference, official guides |
| Errors/solutions | Web search | Stack Overflow, GitHub issues |
| Project-specific | Local files | Architecture, API docs |
| UI components | shadcn MCP | If using shadcn/ui |

## Setup Flow

### Step 1: Determine Documentation Needs

Based on tech stack:

| Tech Stack | Documentation Needs |
|------------|---------------------|
| Next.js | Next.js docs, React docs |
| Convex | Convex docs |
| Tailwind + shadcn | shadcn component docs |
| Any | Error resolution via web search |

### Step 2: Configure MCPs

**Context7 MCP** (for framework documentation):

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/context7-mcp"]
    }
  }
}
```

**shadcn MCP** (if using shadcn/ui):

```json
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/shadcn-mcp"]
    }
  }
}
```

### Step 3: Interview User

```
AskUserQuestion: "Documentation preferences?"

├── Context7 for framework docs (Recommended)
│   Provides live access to Next.js, React, etc.
│
├── shadcn MCP for UI components (if using shadcn/ui)
│   Provides component documentation
│
├── Web search for errors
│   Stack Overflow, GitHub issues
│
└── None - I'll look things up manually
```

### Step 4: Document in CLAUDE.md

Add Documentation Methods section:

```markdown
## Documentation Methods

### Framework/Library Docs
Use Context7 MCP:
- Next.js documentation
- React documentation
- Package documentation

### Errors and Solutions
Use web search for:
- Error messages
- Stack Overflow solutions
- GitHub issues

### Project-Specific Docs
- API docs: `/docs/api.md`
- Architecture: `/docs/architecture.md`

### External Resources
- Convex: https://docs.convex.dev
- Stripe: https://stripe.com/docs
```

## When to Use Each Method

### Context7 MCP

**Best for:**
- API reference lookups
- Official framework guides
- Understanding library interfaces
- Configuration options

**Examples:**
- "What's the signature for useRouter in Next.js?"
- "How do I configure middleware in Next.js 14?"
- "What options does the Image component accept?"

### Web Search

**Best for:**
- Error message resolution
- Community solutions
- GitHub issues
- Stack Overflow answers
- Recent changes/updates

**Examples:**
- "Error: hydration mismatch in React"
- "Convex deployment fails with error X"
- "Stripe webhook signature verification issue"

### Local Documentation

**Best for:**
- Project architecture
- API contracts
- Database schema
- Team conventions

**Examples:**
- Internal API documentation
- Database entity relationships
- Custom component library

## Context7 Usage Guide

### Supported Frameworks

Context7 provides documentation for:
- React
- Next.js
- Vue
- Angular
- Express
- Fastify
- And many more...

### Query Examples

```
Context7: "How to use useCallback in React"
Context7: "Next.js App Router data fetching"
Context7: "Express middleware error handling"
```

### Limitations

- May not have very recent updates
- Focused on official docs
- Doesn't cover Stack Overflow solutions

## Web Search Usage Guide

### When to Search

1. **Error messages**: Copy exact error text
2. **Specific issues**: Describe symptom
3. **Recent updates**: Include year/version

### Search Query Tips

```
Good: "Next.js 14 hydration error 'Text content did not match'"
Good: "Convex useQuery returns undefined 2024"
Good: "Stripe webhook signature verification Node.js"

Bad: "error in my code"
Bad: "thing not working"
```

### Trusted Sources

Prioritize results from:
- Official documentation
- GitHub issues (official repo)
- Stack Overflow (accepted/high-vote answers)
- Blog posts from known developers

## Project Documentation Setup

### Recommended Structure

```
docs/
├── README.md           # Documentation index
├── architecture.md     # System architecture
├── api.md              # API documentation
├── database.md         # Database schema
├── deployment.md       # Deployment guide
└── contributing.md     # Contribution guidelines
```

### Point to Docs in CLAUDE.md

```markdown
### Project Documentation
- Architecture: `/docs/architecture.md`
- API Reference: `/docs/api.md`
- Database Schema: `convex/schema.ts` (source of truth)
- Deployment: `/docs/deployment.md`
```

## Audit Checklist

When auditing documentation setup:

- [ ] Context7 MCP enabled (if using major frameworks)
- [ ] shadcn MCP enabled (if using shadcn/ui)
- [ ] CLAUDE.md has Documentation Methods section
- [ ] Local docs referenced in CLAUDE.md
- [ ] External resources listed
- [ ] Clear guidance on when to use each method

## Output Format

Present documentation configuration:

```
═══════════════════════════════════════════════════════════════════════════
Documentation Configuration
═══════════════════════════════════════════════════════════════════════════

MCPs Enabled:
├── context7 - Framework documentation
└── shadcn - UI component docs

Methods Available:
├── Context7: Next.js, React, Convex docs
├── Web Search: Errors, solutions, issues
└── Local Docs: /docs/api.md, /docs/architecture.md

Usage Guide:
├── API reference → Context7 MCP
├── Error messages → Web search
├── Project architecture → Local docs
└── UI components → shadcn MCP

Context Impact:
├── context7: ~5 tools
├── shadcn: ~3 tools
└── Total: ~8 tools ✓
```

## Troubleshooting

### MCP Not Returning Results

1. Check MCP is enabled in .mcp.json
2. Verify query is specific enough
3. Try rephrasing query
4. Fall back to web search

### Outdated Documentation

1. Check official docs website directly
2. Use web search with recent date filter
3. Check GitHub releases for recent changes

### Missing Project Docs

1. Create minimal docs structure
2. Add pointers in CLAUDE.md
3. Note source of truth files (schema, types)
