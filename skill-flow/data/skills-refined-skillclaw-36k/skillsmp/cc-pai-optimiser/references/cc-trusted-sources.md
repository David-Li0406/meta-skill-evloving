# Claude Code Trusted Sources (Updated 2026-01)

## Primary Sources (Official)

### Core Documentation

#### 1. Claude Code Documentation Hub
- **URL**: https://code.claude.com/docs/en/overview
- **Content**: Central documentation hub for all Claude Code features
- **Update Frequency**: Check weekly
- **Reliability**: Highest (Primary source of truth as of 2026)

#### 2. GitHub Repository
- **URL**: https://github.com/anthropics/claude-code
- **Key Files**:
    - `CHANGELOG.md` - Detailed version history
    - `releases` - Tagged releases with notes
- **Update Frequency**: Check weekly
- **Reliability**: Highest (Official source of truth)

#### 3. Anthropic Platform Documentation
- **URL**: https://docs.anthropic.com/en/docs/claude-code
- **Content**: API reference, core concepts
- **Update Frequency**: Check weekly
- **Reliability**: Highest

#### 4. Anthropic News/Blog
- **URL**: https://www.anthropic.com/news
- **Content**: Major feature announcements, model updates
- **Update Frequency**: Check monthly
- **Reliability**: Highest

#### 5. Anthropic Engineering Blog
- **URL**: https://www.anthropic.com/engineering/claude-code-best-practices
- **Content**: Best practices from Anthropic teams, multi-agent workflows
- **Key Resource**: "How Anthropic teams use Claude Code" (PDF)
- **Update Frequency**: Check quarterly
- **Reliability**: Highest

#### 6. NPM Package
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code
- **Content**: Package versions, dependency updates
- **Update Frequency**: Automatic via `claude --version`
- **Reliability**: Highest

### Feature-Specific Documentation

#### 7. MCP (Model Context Protocol)
- **URL**: https://code.claude.com/docs/en/mcp
- **Content**: MCP server integration, resource references, tool configuration
- **Key Features**: HTTP servers, stdio processes, resource @mentions
- **Update Frequency**: Check monthly
- **Reliability**: Highest

#### 8. Skills System
- **URL**: https://code.claude.com/docs/en/skills
- **Content**: Skill creation, frontmatter, lifecycle hooks
- **Key Features**: SKILL.md format, auto-activation, scoped hooks
- **Update Frequency**: Check monthly
- **Reliability**: Highest

#### 9. Hooks Reference
- **URL**: https://docs.claude.com/en/docs/claude-code/hooks
- **Content**: PreToolUse, PostToolUse, UserPromptSubmit hooks
- **Key Features**: Event-driven automation, tool interception
- **Update Frequency**: Check monthly
- **Reliability**: Highest

#### 10. Plugin Marketplaces
- **URL**: https://code.claude.com/docs/en/plugin-marketplaces
- **Content**: Plugin distribution, marketplace.json format
- **Key Features**: /plugin commands, versioning, auto-updates
- **Update Frequency**: Check monthly
- **Reliability**: Highest

#### 11. GitHub Actions Integration
- **URL**: https://code.claude.com/docs/en/github-actions
- **Content**: CI/CD automation, @claude mentions in PRs
- **Key Features**: Issue/PR integration, headless mode, progress tracking
- **Update Frequency**: Check monthly
- **Reliability**: Highest

#### 12. VS Code Extension
- **URL**: https://code.claude.com/docs/en/vs-code
- **Content**: VS Code integration, inline diffs, conversation history
- **Key Features**: Native IDE integration, sidebar panel, @mention files
- **Update Frequency**: Check weekly (beta as of 2026)
- **Reliability**: Highest

#### 13. Web Interface
- **URL**: https://code.claude.com/docs/en/claude-code-on-the-web
- **Content**: Web UI at claude.com/code, session teleport
- **Key Features**: Remote sessions, GitHub integration, /teleport
- **Update Frequency**: Check weekly
- **Reliability**: Highest

### Official Repositories

#### 14. Official Plugins Repository
- **URL**: https://github.com/anthropics/claude-plugins-official
- **Content**: Anthropic-managed plugin directory
- **Key Features**: Reference implementations, plugin standards
- **Update Frequency**: Check monthly
- **Reliability**: Highest

#### 15. GitHub Actions Repository
- **URL**: https://github.com/anthropics/claude-code-action
- **Content**: Official GitHub Actions integration
- **Key Features**: CI/CD workflows, automation patterns
- **Update Frequency**: Check monthly
- **Reliability**: Highest

---

## Secondary Sources (Community)

### Community Documentation

#### 16. marckrenn Claude Code Changelog
- **URL**: https://github.com/marckrenn/claude-code-changelog
- **Content**: Community-maintained system prompt history and changelog
- **Key File**: `cc-prompt.md` - Current system prompt
- **Update Frequency**: Near real-time
- **Reliability**: High (verified against official)

#### 17. ClaudeLog Changelog
- **URL**: https://claudelog.com/claude-code-changelog/
- **Content**: Community changelog aggregation
- **Update Frequency**: Near real-time
- **Reliability**: Medium-High

#### 18. DeepWiki Feature Evolution
- **URL**: https://deepwiki.com/anthropics/claude-code/
- **Content**: Detailed feature history and architecture docs
- **Update Frequency**: Weekly
- **Reliability**: Medium-High

#### 19. HumanLayer CLAUDE.md Guide
- **URL**: https://www.humanlayer.dev/blog/writing-a-good-claude-md
- **Content**: Authoritative guide on CLAUDE.md best practices
- **Key Topics**: Progressive disclosure, signal-to-noise ratio, instruction limits
- **Update Frequency**: Check quarterly
- **Reliability**: High

### Community Resources

#### 20. Awesome Claude Code
- **URL**: https://github.com/hesreallyhim/awesome-claude-code
- **Content**: Curated commands, workflows, tools, slash commands
- **Key Features**: 4,000+ stars, actively maintained
- **Update Frequency**: Check monthly
- **Reliability**: High

#### 21. Awesome Claude Skills
- **URL**: https://github.com/ComposioHQ/awesome-claude-skills
- **Content**: 4,167+ community skills (as of Jan 2026)
- **Key Features**: Multiple curated collections, skill pattern library
- **Update Frequency**: Check monthly
- **Reliability**: Medium-High

#### 22. Claude Code Showcase
- **URL**: https://github.com/ChrisWiles/claude-code-showcase
- **Content**: Comprehensive project configuration examples
- **Key Features**: Hooks, skills, agents, GitHub Actions workflows
- **Update Frequency**: Check monthly
- **Reliability**: High

#### 23. Claude Code Templates
- **URL**: https://www.aitmpl.com/plugins
- **Content**: Polished UI for browsing resources
- **Key Features**: Usage dashboard, analytics, categorized resources
- **Update Frequency**: Check monthly
- **Reliability**: Medium-High

### Community Platforms

#### 24. Claude Developers Discord
- **URL**: https://humanlayer.dev/discord
- **Content**: Community discussions, early feature previews
- **Update Frequency**: Real-time
- **Reliability**: Medium (Verify against official sources)

---

## Related Resources

### Architecture & Patterns

#### 25. 12-Factor Agents Repository
- **URL**: https://github.com/humanlayer/12-factor-agents
- **Content**: Agent architecture principles
- **Relevance**: Design patterns for PAI optimization
- **Reliability**: High

#### 26. Claude Agent SDK Documentation
- **URL**: https://docs.anthropic.com/en/docs/agent-sdk
- **Content**: SDK for building custom agents
- **Relevance**: Advanced PAI integration patterns
- **Reliability**: Highest

---

## Update Monitoring Strategy

### Automated Checks

```bash
#!/bin/bash
# Enhanced cc-update-check.sh - Add to cron

# Check current version
CURRENT=$(claude --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+')
echo "Current CC version: $CURRENT"

# Fetch latest from npm
LATEST=$(npm view @anthropic-ai/claude-code version 2>/dev/null)
echo "Latest CC version: $LATEST"

if [ "$CURRENT" != "$LATEST" ]; then
  echo "Update available: $CURRENT -> $LATEST"
  echo "Run: claude update"
fi

# Check for new plugin releases
echo "Checking official plugins..."
gh repo view anthropics/claude-plugins-official --json updatedAt --jq '.updatedAt' 2>/dev/null

# Check for new GitHub Actions
echo "Checking GitHub Actions..."
gh api repos/anthropics/claude-code-action/releases/latest --jq '.tag_name' 2>/dev/null

# Check VS Code extension
echo "Checking VS Code extension..."
code --list-extensions --show-versions 2>/dev/null | grep "anthropic.claude-code"
```

### Manual Review Cadence

| Source | Frequency | Action |
|--------|-----------|--------|
| code.claude.com docs | Weekly | Review new features |
| GitHub CHANGELOG | Weekly | Review version history |
| NPM Package | Each session | `claude --version` |
| Anthropic Blog | Monthly | Major announcements |
| Engineering Blog | Quarterly | Best practices |
| MCP Documentation | Monthly | New integrations |
| Plugin Marketplace | Monthly | New plugins |
| VS Code Extension | Weekly | Extension updates |
| GitHub Actions | Monthly | CI/CD patterns |
| Official Plugins Repo | Monthly | Reference implementations |
| Discord | As needed | Community insights |

---

## Feature Categories to Track

### Critical (Core Functionality)
- Model updates (Sonnet 4.5, Opus 4.5, Haiku)
- Context window changes
- Tool/permission system updates
- Subagent capabilities
- Hooks system changes
- **MCP server integrations** (NEW 2026)
- **Plugin system updates** (NEW 2026)
- **Web interface features** (NEW 2026)

### High Priority (Productivity)
- New slash commands
- Skill tool enhancements
- Task tool improvements
- Plan mode features
- **VS Code extension features** (NEW 2026)
- **GitHub Actions capabilities** (NEW 2026)
- **Teleport/session portability** (NEW 2026)

### Medium Priority (Enhancement)
- UI/UX improvements
- IDE integrations
- Terminal features
- **Plugin marketplace growth** (NEW 2026)
- **MCP server ecosystem** (NEW 2026)

### Lower Priority (Nice-to-have)
- Theme/styling options
- Documentation updates
- Community tools integration

---

## CC 2.1.x Key Features

| Feature | Version | Description |
|---------|---------|-------------|
| Model routing | 2.1.0+ | Per-task model selection (haiku/sonnet/opus) |
| Skill invocation | 2.1.0+ | Skill tool for user-defined skills |
| Background tasks | 2.1.0+ | run_in_background for async agents |
| Task resume | 2.1.0+ | Resume agents via agent ID |
| Status line | 2.1.0+ | Custom status line in settings.json |
| Enhanced hooks | 2.1.0+ | Hooks in settings.json (replaces hooks.json) |
| WebSearch | 2.1.0+ | Built-in web search tool |
| AskUserQuestion | 2.1.0+ | Interactive questions with options |
| MCP integration | 2.1.0+ | Connect to external tools via Model Context Protocol |
| Plugin system | 2.1.0+ | Install/manage plugins from marketplaces |
| Teleport feature | 2.1.0+ | Move sessions between web and terminal |
| Web interface | 2.1.0+ | claude.com/code for Pro/Max users |
| VS Code extension | 2.1.0+ | Native IDE integration (beta) |
| Thinking mode | 2.1.0+ | think/ultrathink for planning |
| Vim bindings | 2.1.0+ | Vim mode for text input |
| Hot reload skills | 2.1.0+ | Skills update without restart |
| GitHub Actions | 2.1.0+ | @claude mentions in PRs/issues |
| Merged skills/commands | 2.1.3+ | Unified slash commands and skills |
| Custom commands (new) | 2.1.3+ | .claude/commands/ markdown files |
| Plugin marketplaces | 2.1.3+ | Distributed plugin catalogs |
| Release channel toggle | 2.1.3+ | stable/latest selection in /config |
| Enhanced /doctor | 2.1.3+ | Detects unreachable permission rules |
| Extended hook timeout | 2.1.3+ | Hook execution timeout: 10 minutes |
| Disable background tasks | 2.1.4+ | CLAUDE_CODE_DISABLE_BACKGROUND_TASKS env var |

---

## Source Quality Guidelines

### High Reliability Indicators
- Official Anthropic domains (anthropic.com, code.claude.com)
- Anthropic GitHub repositories (anthropics/*)
- Last updated within 1 month
- Active maintenance (commits, issues, releases)

### Medium Reliability Indicators
- Community GitHub repos with 1000+ stars
- Community blogs from known contributors
- Last updated within 3 months
- Referenced by official docs or Anthropic team

### Use with Caution
- Sources last updated 6+ months ago
- Unverified community claims
- Sources not cross-referenced elsewhere
- Anonymous or single-contributor sources

---

## Validation Checklist

Use this checklist when updating the trusted sources document:

- [ ] All official Anthropic sources verified and current
- [ ] All documentation URLs tested and accessible
- [ ] All GitHub repositories checked for recent activity
- [ ] All community resources verified as maintained (updated within 3 months)
- [ ] All feature tables updated with latest CC version
- [ ] Monitoring scripts tested and functional
- [ ] Review cadence table reflects current best practices
- [ ] No duplicate or conflicting information
- [ ] All sources categorized correctly
- [ ] All new major features (2.1.0+) documented

---

## Changes from Previous Version (2025-01)

### Added Primary Sources
- Claude Code Documentation Hub (code.claude.com)
- Anthropic Engineering Blog (Best Practices)
- MCP (Model Context Protocol) Documentation
- Skills System Documentation
- Hooks Reference Documentation
- Plugin Marketplaces Documentation
- GitHub Actions Integration Documentation
- VS Code Extension Documentation
- Web Interface Documentation
- Official Plugins Repository
- GitHub Actions Repository

### Added Community Sources
- HumanLayer CLAUDE.md Guide
- Awesome Claude Code Repository
- Awesome Claude Skills Collections
- Claude Code Showcase
- Claude Code Templates Platform

### Updated Sections
- Enhanced Automated Checks script
- Expanded Manual Review Cadence
- Updated Feature Categories (added 2026 features)
- Expanded CC 2.1.x Key Features table
- Added Source Quality Guidelines
- Added Validation Checklist

### Total Sources
- Previous: 10 sources
- Current: 26 sources
- Net gain: 16 sources (+160%)

---

## Future Research Recommendations

Consider researching these areas for future updates:

1. **Claude Code Performance Benchmarks** - Latency, token usage, cost optimization
2. **Enterprise Features** - Team management, audit logs, compliance
3. **Security Best Practices** - Permissions, secrets, sandboxing
4. **Multi-Language Support** - Language-specific patterns and tools
5. **Migration Guides** - Upgrading from older CC versions
6. **Troubleshooting Resources** - Common issues and solutions
7. **Video Tutorials** - Official and community video content
8. **Case Studies** - Real-world implementation examples

---

## Version History

- **2026-01**: Major update with 16 new sources, expanded feature tracking, enhanced monitoring
- **2025-01**: Initial version with 10 core sources
