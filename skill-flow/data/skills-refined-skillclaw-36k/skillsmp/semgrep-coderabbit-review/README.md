# Semgrep + CodeRabbit Review Skill

An OpenCode skill for two-stage code review combining **fast pattern detection** (Semgrep) with **AI-powered semantic analysis** (CodeRabbit).

## Quick Start

### 1. Install Required Plugin

First, install the companion plugin that provides the tools:

```bash
npm install opencode-semgrep-coderabbit-plugin
# or
yarn add opencode-semgrep-coderabbit-plugin
# or
bun add opencode-semgrep-coderabbit-plugin
```

### 2. Load the Skill

In OpenCode, load this skill:

```
/skill semgrep-coderabbit-review
```

### 3. Run a Review

Choose a focus area:

```
/run review --stage both                    # Complete two-stage review
/run review --stage semgrep-only           # Fast pattern check only
/run coderabbitReview --focus security     # Security-focused AI review
/run coderabbitReview --focus api          # API layer review
/run coderabbitReview --focus database     # Database layer review
/run coderabbitReview --focus web          # Frontend review
```

## What This Skill Does

### Stage 1: Fast Pattern Detection (10-20 seconds)

Semgrep scans for:

- 🔐 **Security:** Hardcoded secrets, SQL injection, XSS, auth bypass
- 🏗️ **Architecture:** Repository Pattern violations, direct DB access, workspace imports
- 📋 **Code Quality:** console.log, weak crypto, any types, missing validation
- ✅ **Best Practices:** Missing error handling, insecure defaults, logging sensitive data

### Stage 2: AI-Powered Semantic Review (5-30 minutes)

CodeRabbit analyzes:

- ✅ Logic correctness and edge cases
- ✅ Test coverage and error handling
- ✅ API contracts and breaking changes
- ✅ Multi-tenant isolation and security
- ✅ Performance optimization opportunities
- ✅ Architecture and design patterns

## Focus Areas

| Focus      | What It Checks                                         |
| ---------- | ------------------------------------------------------ |
| `security` | Auth, secrets, data protection, encryption             |
| `api`      | Repository Pattern, auth guards, OpenAPI contracts     |
| `database` | Query safety, parameterization, multi-tenant isolation |
| `web`      | Svelte 5 runes, XSS, accessibility, performance        |
| `all`      | Everything (comprehensive review)                      |

## Review Workflow

```
┌─────────────────────────────────────┐
│  Stage 1: Run Semgrep (10-20s)     │
│  └─ Detects patterns, secrets       │
└────────────┬────────────────────────┘
             │
        Issues? ──YES──> Fix All
             │            │
             NO           └──> Re-run Semgrep
             │
┌────────────▼────────────────────────┐
│  Stage 2: Run CodeRabbit (5-30min)  │
│  └─ Analyzes logic, architecture    │
└────────────┬────────────────────────┘
             │
        Findings?
             │
        ┌────┴─────────────────┐
        │                      │
     CRITICAL/HIGH ───────> Fix
        │                      │
      MEDIUM/LOW              └──> Re-run Both
        │
        └─────────────────> Review & Iterate
```

## Common Issues & Fixes

### Security Issues

```
❌ const SECRET = "hardcoded-key"
✅ const SECRET = process.env.API_KEY

❌ SELECT * FROM users WHERE id = '${userId}'
✅ SELECT * FROM users WHERE id = ? (with parameterized binding)

❌ {@html userContent}
✅ {@html DOMPurify.sanitize(userContent)}

❌ fastify.get('/api/protected', (req, res) => {...})
✅ fastify.get('/api/protected', { preHandler: [fastify.authenticate] }, (req, res) => {...})
```

### Architecture Issues

```
❌ const users = await fastify.db.query('SELECT * FROM users')
✅ const users = await request.repos.users.findAll(ctx)

❌ export let prop
✅ let { prop } = $props()

❌ function process(data: any) { ... }
✅ function process(data: UserData) { ... }
```

### Code Quality Issues

```
❌ console.log('User ID:', userId)
✅ logger.info('User loaded', { userId })

❌ crypto.createHash('md5')
✅ crypto.createHash('sha256')

❌ await fetchData()  // No error handling
✅ try { await fetchData() } catch (error) { handle(error) }
```

## Layers Covered

### API Layer (Fastify Routes)

**Semgrep checks:**

- Missing authentication guards
- Direct database access
- SQL injection patterns
- Hardcoded secrets

**CodeRabbit checks:**

- OpenAPI schema correctness
- HTTP status codes
- Error response formats
- Rate limiting
- Breaking changes

### Database Layer (Repository Pattern)

**Semgrep checks:**

- Raw SQL queries
- Direct database access
- Missing error handling

**CodeRabbit checks:**

- Query parameterization
- User context scoping
- Multi-tenant isolation
- Error recovery logic

### Frontend Layer (Svelte 5, TypeScript)

**Semgrep checks:**

- Legacy Svelte 4 syntax
- Unsafe `{@html}` usage
- `any` types
- console.log statements

**CodeRabbit checks:**

- Svelte 5 runes compliance
- Component logic correctness
- Performance issues
- Accessibility compliance

### Shared Types & Contracts

**Semgrep checks:**

- `any` types in type definitions
- Hardcoded values

**CodeRabbit checks:**

- Zod schema completeness
- Type correctness
- Breaking change documentation

## Installation & Setup

### Prerequisites

- Node.js >= 18
- OpenCode CLI
- Semgrep: `brew install semgrep`
- CodeRabbit CLI: `brew install coderabbit`

### Step-by-Step

1. **Install the plugin** (provides the tools):

   ```bash
   npm install opencode-semgrep-coderabbit-plugin
   ```

2. **Configure OpenCode** (`opencode.json`):

   ```json
   {
     "plugins": ["opencode-semgrep-coderabbit-plugin"]
   }
   ```

3. **Load this skill** in OpenCode:

   ```
   /skill semgrep-coderabbit-review
   ```

4. **Run your first review**:
   ```
   /run review --stage both
   ```

## Performance Metrics

| Stage           | Duration | Use Case            |
| --------------- | -------- | ------------------- |
| Semgrep only    | 10-20s   | Quick feedback loop |
| CodeRabbit only | 5-30min  | Semantic review     |
| Both stages     | 5-30min  | Complete review     |

**Tips for faster reviews:**

- Start with Semgrep only (10-20s)
- Fix violations immediately
- Run CodeRabbit while working on fixes
- Batch similar fixes together
- Break large PRs into smaller ones

## Troubleshooting

### Plugin Not Loading

```bash
# Verify installation
npm list opencode-semgrep-coderabbit-plugin

# Restart OpenCode
opencode

# Check logs
opencode --logs
```

### Semgrep Command Not Found

```bash
# Install Semgrep
brew install semgrep

# Verify installation
semgrep --version
```

### CodeRabbit Command Not Found

```bash
# Install CodeRabbit CLI
brew install coderabbit

# Verify installation
coderabbit --version
```

### Too Many False Positives

- Reduce scope (focus on specific layers)
- Review rule definitions in `.semgrep.yaml`
- Check if patterns are context-specific
- Mark issues as "intended" if safe

### Reviews Taking Too Long

- Break changes into smaller PRs
- Use Semgrep only for quick feedback
- Focus on security/API layers first
- Run CodeRabbit in parallel while fixing

## Priority Levels

| Priority | Level    | Examples                                          | Action            |
| -------- | -------- | ------------------------------------------------- | ----------------- |
| 🚫       | CRITICAL | Secrets, auth bypass, SQL injection, XSS, leakage | Fix before merge  |
| 🚫       | HIGH     | Missing guards, schema mismatch, breaking changes | Fix before merge  |
| ⚠️       | MEDIUM   | Weak crypto, poor error handling, duplication     | Fix if reasonable |
| 💡       | LOW      | Suggestions, optimization, style                  | Consider optional |

## Related Resources

- **Plugin Repository:** https://github.com/acedergren/opencode-semgrep-coderabbit-plugin
- **OpenCode Docs:** https://opencode.ai/docs
- **Semgrep Docs:** https://semgrep.dev/docs
- **CodeRabbit Docs:** https://coderabbit.ai

## Contributing

Found an issue or have suggestions?

1. Check the [plugin issues](https://github.com/acedergren/opencode-semgrep-coderabbit-plugin/issues)
2. Review existing skill documentation
3. Try the troubleshooting guide above
4. Open an issue with details and reproduction steps

## License

MIT - See LICENSE file

---

**Version:** 1.0  
**Last Updated:** Jan 22, 2026  
**Status:** Production Ready  
**Requires:** opencode-semgrep-coderabbit-plugin >= 1.0.0
