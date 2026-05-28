---
name: skills-management
description: Use this skill when you want to search, discover, install, or manage Claude Code skills from the CCPM registry and Skillsmith system.
---

# Skills Management

This skill combines functionalities for discovering, installing, and managing Claude Code skills from both the Skillsmith and CCPM (Claude Code Plugin Manager) registries. It provides access to a wide range of community skills with trust verification, quality scoring, and security scanning.

## Quick Reference: Commands

| Command | Use When | Example |
|---------|----------|---------|
| `search` | Finding skills by keyword or category | "Find testing skills" |
| `install` | Installing a skill | "Install pdf-processor" |
| `uninstall` | Removing an installed skill | "Uninstall jest-helper" |
| `list` | Listing all installed skills | "What skills do I have installed?" |
| `info` | Getting details about a specific skill | "Show details for skill-creator" |
| `compare` | Comparing multiple skills | "Compare jest-helper and vitest-helper" |
| `recommend` | Getting contextual skill recommendations | "Recommend skills for my React project" |

## Searching for Skills

To search for skills, use the following command:

```bash
ccpm search <query>
```

### Examples:
```bash
ccpm search pdf              # Find PDF-related skills
ccpm search "code review"    # Find code review skills
```

## Installing Skills

To install a skill, use:

```bash
ccpm install <skill-name>
```

### Important:
After installing a skill, restart Claude Code for it to become available.

### Examples:
```bash
ccpm install pdf-processor                    # Install pdf-processor skill
ccpm install cloudflare-troubleshooting       # Install troubleshooting skill
```

## Uninstalling Skills

To remove an installed skill, use:

```bash
ccpm uninstall <skill-name>
```

### Example:
```bash
ccpm uninstall pdf-processor
```

## Trust Tiers

Skills are categorized by verification level:

| Tier | Badge | Meaning | When to Trust |
|------|-------|---------|---------------|
| **Official** | Green checkmark | Published by Anthropic, fully reviewed | Always safe |
| **Verified** | Blue checkmark | Verified publisher, 10+ stars, 30+ days old | Generally safe |
| **Community** | Yellow | Passed security scan, has required metadata | Review before install |
| **Unverified** | Red warning | No verification | Only if you trust the author |

## Security Model

Before any skill is installed, the system performs:

1. **SKILL.md validation** - Must have valid YAML frontmatter with name and description.
2. **Security scan** - Checks for vulnerabilities and suspicious content.
3. **Typosquatting detection** - Warns if skill name is similar to known skills.
4. **Blocklist check** - Rejects known-malicious skills.

**Recommendation**: Always review skill content before installation, especially for unverified skills.

## Common Tasks

### Check Installed Skills
```bash
ccpm list
```

### Get Recommendations
```bash
ccpm recommend <context>
```

## License

This skill uses **Elastic License 2.0**:
- You can self-host for internal use.
- You can modify for your own use.
- You cannot offer this skill as a managed service to others.

## Troubleshooting

### "ccpm: command not found"
Install CCPM globally:
```bash
npm install -g @daymade/ccpm
```

### Skill not available after install
Restart Claude Code - skills are loaded at startup.

### Permission errors
Check write permissions to `~/.claude/skills/`.

## Related Documentation

- [Security Deep-Dive](docs/SECURITY.md)
- [Trust Tiers](docs/TRUST_TIERS.md)
- [Quota System](docs/QUOTAS.md)

## Getting Help

- Docs: `npx @skillsmith/mcp-server --docs`
- Issues: https://github.com/smith-horn/skillsmith/issues
- Email: support@skillsmith.app