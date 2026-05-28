# redis-best-practices

Redis best practices for AI coding agents, following the [Agent Skills](https://agentskills.io) specification.

## Overview

This skill contains 43 rules across 8 categories, ordered by impact:

| Category | Impact | Description |
|----------|--------|-------------|
| Data Structures | CRITICAL | Choosing the right Redis data type for your use case |
| Key Design | CRITICAL | Key naming conventions, TTL strategies, and organization |
| Connection Management | HIGH | Connection pooling, pipelining, and resilience patterns |
| Commands & Patterns | HIGH | Transactions, Lua scripts, distributed locks, batch operations |
| Memory Management | MEDIUM-HIGH | maxmemory configuration, eviction policies, optimization |
| Persistence | MEDIUM | RDB snapshots, AOF logs, backup strategies |
| Clustering & HA | MEDIUM | Sentinel, Redis Cluster, replication patterns |
| Performance & Monitoring | LOW-MEDIUM | SLOWLOG, latency tracking, benchmarking |

## Installation

### Using add-skill (Recommended)

```bash
npx add-skill redis/redis-agent-kit
```

This installs the skill into your `.copilot/skills/` directory.

### Manual Installation

Clone this repository and copy the skill:

```bash
git clone https://github.com/redis/redis-agent-kit.git
cp -r redis-agent-kit/skills/redis-best-practices ~/.copilot/skills/
```

### Claude Code

```bash
cp -r skills/redis-best-practices ~/.claude/skills/
```

## File Structure

```
skills/redis-best-practices/
├── SKILL.md              # Skill definition (triggers agent activation)
├── AGENTS.md             # Compiled rules (what agents read)
├── metadata.json         # Version and metadata
├── README.md             # This file
└── rules/
    ├── _sections.md      # Section definitions
    ├── _template.md      # Template for new rules
    ├── ds-*.md           # Data structure rules (6)
    ├── key-*.md          # Key design rules (6)
    ├── conn-*.md         # Connection management rules (5)
    ├── cmd-*.md          # Commands & patterns rules (6)
    ├── memory-*.md       # Memory management rules (5)
    ├── persist-*.md      # Persistence rules (5)
    ├── cluster-*.md      # Clustering & HA rules (5)
    └── perf-*.md         # Performance & monitoring rules (5)
```

## How It Works

When you're working on Redis code, AI coding agents (Claude Code, GitHub Copilot, Gemini CLI, etc.) that support Agent Skills will automatically:

1. Detect the skill based on `SKILL.md` triggers
2. Load `AGENTS.md` rules into context
3. Apply best practices while generating or reviewing code

## Compiling Rules

To rebuild `AGENTS.md` from individual rules:

```bash
npm run build
# or
node scripts/compile.js
```

## Contributing

### Adding a New Rule

1. Copy `rules/_template.md` to a new file in the appropriate category
2. Fill in the frontmatter (title, impact, impactDescription, tags)
3. Add Incorrect and Correct code examples
4. Run `npm run build` to recompile AGENTS.md
5. Submit a pull request

### Rule Format

```markdown
---
title: Rule Title
impact: HIGH
impactDescription: Brief explanation of why this matters
tags: [relevant, tags, here]
---

**Incorrect (brief reason):**

\`\`\`python
# Anti-pattern code
\`\`\`

**Correct (brief reason):**

\`\`\`python
# Best practice code
\`\`\`
```

### Impact Levels

- **CRITICAL**: Prevents data loss, outages, or major performance issues
- **HIGH**: Significant performance or reliability impact
- **MEDIUM-HIGH**: Notable optimization opportunity
- **MEDIUM**: Recommended best practice
- **LOW-MEDIUM**: Nice to have
- **LOW**: Minor optimization

## Compatibility

This skill follows the [Agent Skills](https://agentskills.io) open standard and is compatible with:

- Claude Code
- VS Code (GitHub Copilot)
- GitHub.com
- Gemini CLI
- OpenCode
- Factory
- OpenAI Codex

## License

MIT

## Acknowledgments

- [Redis official documentation](https://redis.io/docs/)
- [Redis University](https://university.redis.io/) for learning resources
- The [Agent Skills](https://agentskills.io) specification from Anthropic
