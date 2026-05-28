---
name: claude-code-guide
description: Use this agent when the user asks questions ("Can Claude...", "Does Claude...", "How do I...") about Claude Code (the CLI tool) - features, hooks, slash commands, MCP servers, settings, IDE integrations, keyboard shortcuts, or the Claude API (formerly Anthropic API) - API usage, tool use, Anthropic SDK usage.
---

# Claude Code Guide

This skill provides quick reference to authoritative Claude Code resources. When questions arise about Claude Code capabilities, workflows, or best practices, consult these resources rather than guessing.

## Important Note on Currency

Claude Code and its models evolve rapidly. Advice predating Claude 4.5 Opus/Sonnet (late 2024/early 2025) is likely outdated. Always prefer official Anthropic documentation and recent 2026 resources.

## Local References (Downloaded for Offline Access)

These key documents have been downloaded and converted to markdown for faster access:

1. **[best-practices.md](references/best-practices.md)** - Comprehensive best practices guide from Anthropic
   - When to read: For optimizing workflows, learning about CLAUDE.md files, MCP integration, custom commands, multi-agent patterns
   - Key topics: CLAUDE.md files, tool allowlists, test-driven development, headless mode, git worktrees

2. **[common-workflows.md](references/common-workflows.md)** - Official workflow documentation
   - When to read: For specific how-to guides on common tasks
   - Key topics: Codebase exploration, bug fixing, refactoring, plan mode, subagents, testing, PR creation, image handling, custom slash commands

3. **[overview.md](references/overview.md)** - What Claude Code is and basic capabilities
   - When to read: For onboarding or explaining Claude Code to others
   - Key topics: Installation, core capabilities, philosophy, quick start

## Official Online Documentation

4. **[Claude Code Docs](https://code.claude.com/docs/en/overview)** - Main documentation portal
   - When to read: For comprehensive, up-to-date official documentation
   - Covers: Setup, configuration, all features, troubleshooting

5. **[VS Code Integration](https://code.claude.com/docs/en/vs-code)** - VS Code extension guide
   - When to read: For IDE-specific features and keyboard shortcuts
   - Covers: Native graphical interface, IDE integration, extension features

6. **[Claude API/Platform Docs](https://docs.anthropic.com/en/release-notes/overview)** - Developer platform documentation
   - When to read: For API usage, model details, SDK information
   - Covers: API endpoints, authentication, rate limits, model capabilities

## Community Resources (2026)

7. **[Anthropic Engineering: Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)** - Official engineering blog post
   - When to read: Same as local best-practices.md (this is the source)
   - Why listed: Direct link to check for updates

8. **[How Anthropic Teams Use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)** - Internal workflows from Anthropic
   - When to read: For real-world examples from the creators
   - Covers: Production usage patterns, team workflows

9. **[GitHub: anthropics/claude-code](https://github.com/anthropics/claude-code)** - Official GitHub repository
   - When to read: For issue tracking, changelog, source code
   - Covers: Latest releases, known issues, feature requests

10. **[GitHub: awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)** - Community curated resources
    - When to read: For plugins, skills, hooks, and community tools
    - Covers: Extensions, integrations, third-party tools

11. **[Claude Code Creator's Workflow (VentureBeat)](https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are)** - Boris Cherny's workflow
    - When to read: For insights from the creator's actual usage patterns
    - Covers: Real-world workflows, 259 PRs in 30 days example

12. **[Shipyard Claude Code Cheatsheet](https://shipyard.build/blog/claude-code-cheat-sheet/)** - Quick reference guide
    - When to read: For quick command lookups and configuration reference
    - Covers: Commands, config files, prompts, best practices

## Practical Guide Articles (2026)

13. **[Builder.io: How I Use Claude Code](https://www.builder.io/blog/claude-code)** - Personal tips and workflow
    - When to read: For practical tips from experienced users
    - Key tip: Use /clear often, dedicate time to CLAUDE.md documentation

14. **[Blog: How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)** - Feature-by-feature guide
    - When to read: For comprehensive feature coverage with examples
    - Covers: Deep dive into each feature with use cases

15. **[Professional Guide for Senior Devs (2026)](https://wmedia.es/en/writing/claude-code-professional-guide-frontend-ai)** - Advanced usage
    - When to read: For advanced patterns and professional workflows
    - Covers: Frontend, AI integration, senior developer practices

16. **[20+ Most Important CLI Tricks (2026)](https://mlearning.substack.com/p/20-most-important-claude-code-tricks-2025-2026-cli-january-update)** - Tips and tricks compilation
    - When to read: For quick wins and productivity hacks
    - Covers: CLI shortcuts, hidden features, efficiency tips

17. **[F22 Labs: 10 Productivity Tips](https://www.f22labs.com/blogs/10-claude-code-productivity-tips-for-every-developer/)** - Productivity focused
    - When to read: For developer productivity optimization
    - Covers: Workflow optimization, time-saving techniques

18. **[GitHub: claude-code-tips](https://github.com/ykdojo/claude-code-tips)** - 40+ tips collection
    - When to read: For comprehensive tips including advanced topics
    - Covers: Basics to advanced, custom status line, Gemini CLI integration, container usage

## Creator Insights (Boris Cherny)

19. **[InfoQ: Inside the Development Workflow](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/)** - Creator workflow analysis
    - When to read: For understanding the creator's development process
    - Covers: Plan mode emphasis, verification loops, CLAUDE.md evolution

20. **[Medium: 22 Tips from Boris Cherny](https://medium.com/@joe.njenga/boris-cherny-claude-code-creator-shares-these-22-tips-youre-probably-using-it-wrong-1b570aedefbe)** - Direct tips from creator
    - When to read: For avoiding common mistakes
    - Covers: What not to do, optimization tips

21. **[Dev Genius: 13 Practical Moves](https://blog.devgenius.io/how-the-creator-of-claude-code-actually-uses-it-13-practical-moves-2bf02eec032a)** - Creator's practical techniques
    - When to read: For actionable techniques from Boris Cherny
    - Covers: Real usage patterns, practical moves

## Advanced Workflows

22. **[Medium: 17 Best Workflows](https://medium.com/@joe.njenga/17-best-claude-code-workflows-that-separate-amateurs-from-pros-instantly-level-up-5075680d4c49)** - Amateur vs Pro patterns
    - When to read: For leveling up your workflow game
    - Covers: Professional workflow patterns, advanced techniques

23. **[Medium: Two Simple Tricks (Julien Simon)](https://julsimon.medium.com/two-simple-tricks-that-will-dramatically-improve-your-productivity-with-claude-db90ce784931)** - High-impact productivity tips
    - When to read: For maximum ROI productivity improvements
    - Covers: Simple but powerful techniques

## Release Notes and Updates

24. **[Claude Code Changelog](https://docs.anthropic.com/en/release-notes/claude-code)** - Official release notes
    - When to read: For latest features, bug fixes, breaking changes
    - Covers: Version history, new features, deprecations

25. **[VentureBeat: Claude Code 2.1.0](https://venturebeat.com/orchestration/claude-code-2-1-0-arrives-with-smoother-workflows-and-smarter-agents)** - Major release coverage
    - When to read: For understanding major version updates
    - Covers: v2.1.0 features, agent lifecycle control, session portability

## Quick Reference Key Insights

### Essential Commands
- `/clear` - Reset context (use often!)
- `/permissions` - Manage tool allowlists
- `/agents` - Access specialized subagents
- `Escape` - Stop Claude (not Ctrl+C)
- `Shift+Tab` - Cycle permission modes (Normal → Auto-Accept → Plan)
- `Option/Alt+T` - Toggle thinking mode
- `Ctrl+O` - Toggle verbose mode

### Core Patterns
1. **CLAUDE.md files** - Document project conventions, checked into git
2. **Plan before code** - Use plan mode for complex features
3. **Verification loops** - Give Claude ways to verify work (tests, builds, visual checks)
4. **Custom slash commands** - Store in `.claude/commands/` or `~/.claude/commands/`
5. **MCP servers** - Extend Claude with custom tools
6. **Git worktrees** - Run parallel Claude sessions on different branches

### Performance Tips
- Keep CLAUDE.md concise and structured
- Use /clear between unrelated tasks
- Provide specific, actionable instructions
- Include visual references (screenshots, mockups)
- Set up feedback loops (tests, linters, builds)
- Use headless mode (`-p`) for automation

## When to Consult This Skill

Use this skill when questions arise about:
- "Can Claude Code do X?"
- "How do I configure Y?"
- "What's the best way to Z?"
- Keyboard shortcuts or CLI flags
- MCP servers, hooks, or settings
- IDE integration features
- API usage or SDK questions
- Troubleshooting Claude Code issues

Rather than guessing or providing outdated information, direct users to the appropriate resource above based on their specific question.
