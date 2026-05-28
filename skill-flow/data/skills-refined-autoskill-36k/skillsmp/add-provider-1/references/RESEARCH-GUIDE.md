# Provider Research Guide

**Before writing ANY code, complete this research phase.**

This guide helps you gather the information needed to correctly implement a provider, avoiding the most common mistakes.

## Phase 0: Pre-Implementation Checklist

- [ ] Provider documentation is publicly available
- [ ] You have access to test the provider (free tier or trial)
- [ ] You've identified the official config file locations
- [ ] You've audited support for all 11 primitives
- [ ] You've documented your findings (see template below)

## Step 1: Official Documentation Audit

**Visit the provider's official documentation:**
- Main site (e.g., cursor.com, claude.ai)
- Developer docs (e.g., developers.openai.com)
- GitHub repository (if open source)
- Official examples and tutorials

**Create a list of config file locations:**

```
Provider: [Name]

Project-level config:
- [ ] What files/folders exist at project root? (e.g., AGENTS.md, .cursor/config.toml)
- [ ] Where do instructions/rules go?
- [ ] Where do skills/workflows go?
- [ ] Where do custom agents go?

Global/User-level config:
- [ ] What files/folders in home directory? (e.g., ~/.cursor/settings.json)
- [ ] Where do global settings go?
- [ ] Where do global instructions go?
- [ ] Where do global commands go?

Configuration format:
- [ ] TOML? JSON? YAML? Plain text?
- [ ] Official schema or example provided?
- [ ] Links to official examples
```

## Step 2: Primitive Support Audit

**For each of the 11 primitives, research:**

```markdown
### Primitive Name: [e.g., Agent Mode]

**Support Level:** [ ] full [ ] partial [ ] diy [ ] none

**Evidence:**
- Official docs link: [e.g., https://cursor.com/docs/agent/modes]
- Feature name in provider: [e.g., "Agent mode" / "Agent Mode" / different name?]
- Native support: yes/no
- Requires plugin/extension: yes/no
- Requires workaround: yes/no
- Available in: [e.g., "Stable" / "Nightly only" / "Beta"]

**Configuration location:**
- File path: [e.g., ~/.cursor/settings.json]
- Property/section: [e.g., agent.enabled = true]
- Example config: [paste snippet from official docs]

**Limitations/Notes:**
[Any caveats, gotchas, or important context]

**Support level decision:**
- **full** if: Natively supported, documented, core feature
- **partial** if: Works with limitations or workarounds
- **diy** if: Possible but requires custom setup
- **none** if: Not possible (rare)
```

## Step 3: Create Capability Audit Summary

Create a table showing your research results:

| Primitive | Supported | Level | Config Location | Evidence |
|-----------|-----------|-------|-----------------|----------|
| Agent Mode | ✓ | full | ~/.provider/config.toml | [link] |
| Skills/Workflows | ✓ | partial | AGENTS.md | [link] |
| Tool Integrations | ✓ | full | ~/.provider/config.toml | [link] |
| ... | ... | ... | ... | ... |

**Use this table to verify:**
- All 11 primitives have a decision
- Each decision has evidence (link to official docs)
- Config locations are consistent and accurate
- Support levels match your evidence

## Step 4: Verify Against Real Provider

If possible, test your findings:

```bash
# Try creating the config files yourself
mkdir -p ~/.newprovider
touch ~/.newprovider/config.toml

# Follow official tutorial/quickstart
# Verify the file paths match official docs
# Test that the configuration actually works
```

## Step 5: Document Your Research

Before implementing, save your research in a comment at the top of your PR or in commit messages:

```
Provider: OpenAI Codex
Research completed: 2025-01-17

Audit results:
- All 11 primitives researched
- Config locations verified against official docs
- Support levels: 7 full, 4 partial, 0 diy, 0 none
- 100% coverage with official documentation references

Key findings:
- Project instructions via AGENTS.md (open standard)
- Global config: ~/.codex/config.toml
- MCP servers: Fully supported via config
- CLI: Natively supports multi-step execution (Agent Mode)

References:
- https://developers.openai.com/codex/
- https://github.com/openai/codex
- https://developers.openai.com/codex/guides/agents-sdk/
```

## Common Research Mistakes

### ❌ "I assumed this was supported"
- Don't assume. Verify against official docs.
- Unsupported features waste implementation time.

### ❌ "The documentation is outdated"
- If docs seem outdated, verify with recent GitHub issues or discussion
- Add a comment noting the inconsistency
- Consider using "partial" support level if unsure

### ❌ "I can't find the config file location"
- Search official documentation thoroughly
- Check README in official GitHub repo
- Look at example projects/templates
- If still missing, contact maintainers or file an issue

### ❌ "All providers do the same thing, right?"
- No! Each provider implements primitives differently
- Example: Agent Mode looks different in Cursor vs Claude vs Copilot
- Research each provider individually

### ❌ "I forgot to check both project and global config"
- Every primitive needs TWO location entries
- One for project-level (.cursor/instructions.md)
- One for global/user-level (~/.cursor/config.toml)
- Look for both in provider docs

## Support Level Decision Tree

Use this flowchart to decide support levels:

```
Does the provider officially document this feature?
├─ YES
│  ├─ Is it part of the core product?
│  │  ├─ YES → "full"
│  │  └─ NO
│  │     ├─ Requires paid tier? → "partial"
│  │     ├─ Requires plugin? → "partial"
│  │     ├─ Requires workaround? → "partial"
│  │     └─ Everything works smoothly? → "full"
│  └─ Does the documentation show limitations?
│     ├─ YES → "partial"
│     └─ NO → "full"
└─ NO
   ├─ Is there a community workaround?
   │  ├─ YES → "diy"
   │  └─ NO → "none"
   └─ Could this be implemented externally?
      ├─ YES → "diy"
      └─ NO → "none"
```

## Example: OpenAI Codex Research

Here's what the actual research looked like for Codex:

**Agent Mode**: full support
- Official docs: developers.openai.com/codex/guides/agents-sdk/
- Config: AGENTS.md (project) + CLI execution
- Native support: ✓ documented

**Tool Integrations (MCP)**: full support
- Official docs: developers.openai.com/codex/guides/mcp-integration/
- Config: ~/.codex/config.toml
- Native support: ✓ documented

**Path-Scoped Rules**: no support
- Official docs: searched thoroughly, no mention
- Workaround: Not applicable
- Support level: "diy" (could potentially create custom solution)

**Skills/Workflows**: partial support
- Official docs: mentions AGENTS.md for workflows
- Limitation: Uses standard format, not Codex-specific
- Support level: "partial" (works but through shared standard)

## Validation Checklist

Before moving to Stream 1, verify:

- [ ] All 11 primitives have a support level decision
- [ ] Each support level has evidence (official docs link)
- [ ] Config file locations are from official sources
- [ ] You've tested config files where possible
- [ ] Support levels match the decision tree criteria
- [ ] Your research summary is documented
- [ ] You're confident in your findings

If anything is uncertain, use "partial" support level and add a TODO comment.

## Questions to Ask Yourself

1. **Is this documented in the provider's official docs?**
   - If no → can't use "full", consider "partial" or "diy"

2. **Have I tested this configuration myself?**
   - If possible, test before deciding support level

3. **Is this a core feature or an add-on?**
   - Core features are usually "full"
   - Add-ons might be "partial"

4. **Are there limitations or workarounds needed?**
   - With workarounds → "partial"
   - Without workarounds → "full"

5. **Would a typical user expect this to work?**
   - If yes and it does → "full"
   - If yes but with caveats → "partial"
   - If no and it doesn't work → "none"

## Next Steps

Once you've completed research and verified your findings:

1. Save your research summary (comment/gist/document)
2. Proceed to Stream 1: Type System
3. Use your audit data when filling in primitives.ts
4. Reference your research if support levels seem wrong later

**Remember**: Good research = faster implementation + higher quality data.
