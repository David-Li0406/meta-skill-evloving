# Orchestrating Swarms Skill - Status and Access Guide

## Overview

This skill documents **TeammateTool**, a complete multi-agent orchestration system embedded in Claude Code v2.1.19. The skill provides comprehensive documentation for team-based coordination, parallel execution, and inter-agent messaging.

## Current Status: Feature-Gated

### ⚠️ Important: TeammateTool is NOT Available in Standard Claude Code

TeammateTool exists as **production-quality code** in Claude Code v2.1.19 but is **feature-gated** behind two disabled flags:

```javascript
isEnabled() {
  return I9() && qFB()  // Both return false in public v2.1.19
}
```

This means:

- ✅ The code is complete, tested, and ready
- ✅ All 13 operations are implemented
- ✅ File structures, schemas, and protocols are defined
- ❌ The feature flags prevent activation
- ❌ No official Anthropic documentation exists
- ❌ No official release date announced

## What TeammateTool Provides

When enabled, TeammateTool will provide:

### Core Capabilities

| Capability                | Description                                                      |
| ------------------------- | ---------------------------------------------------------------- |
| **Team Management**       | Create teams with leaders and members                            |
| **Agent Spawning**        | Spawn persistent teammates with Task tool + `team_name` + `name` |
| **Inter-Agent Messaging** | Direct messages (`write`) and broadcast to all                   |
| **Shared Task Lists**     | Task queue with dependencies and auto-unblocking                 |
| **Graceful Shutdown**     | Request/approve shutdown protocol                                |
| **Plan Approval**         | Leader approves/rejects teammate plans                           |
| **Multiple Backends**     | in-process, tmux, iTerm2 execution modes                         |

### 13 Operations

| Operation         | Purpose                   | Who Can Use   |
| ----------------- | ------------------------- | ------------- |
| `spawnTeam`       | Create a new team         | Any agent     |
| `discoverTeams`   | List available teams      | Any agent     |
| `requestJoin`     | Request team membership   | Any agent     |
| `approveJoin`     | Accept join request       | Leader only   |
| `rejectJoin`      | Decline join request      | Leader only   |
| `write`           | Message specific teammate | Team members  |
| `broadcast`       | Message all teammates     | Team members  |
| `requestShutdown` | Ask teammate to exit      | Leader only   |
| `approveShutdown` | Accept shutdown and exit  | Teammate only |
| `rejectShutdown`  | Decline shutdown          | Teammate only |
| `approvePlan`     | Approve proposed plan     | Leader only   |
| `rejectPlan`      | Reject plan with feedback | Leader only   |
| `cleanup`         | Remove team resources     | Leader only   |

### File Structure

When enabled, TeammateTool uses:

```
~/.claude/
├── teams/{team-name}/
│   ├── config.json              # Team metadata, member list
│   └── inboxes/
│       ├── team-lead.json       # Leader's inbox
│       ├── worker-1.json        # Worker 1's inbox
│       └── worker-2.json        # Worker 2's inbox

~/.claude/tasks/{team-name}/
├── 1.json                       # Task with owner, status, dependencies
├── 2.json                       # Task #2
└── 3.json                       # Task #3 (can be blocked by #2)
```

## How to Verify TeammateTool Exists in Your Binary

Even though it's gated, you can confirm it exists in your Claude Code installation:

```bash
# Check if TeammateTool operations are in the binary
strings ~/.local/share/claude/versions/2.1.19 | grep "TeammateTool" | wc -l
# Should output: 13+ (one per operation)

# Extract specific operations
strings ~/.local/share/claude/versions/2.1.19 | grep -E "spawnTeam|discoverTeams|write|broadcast" | sort -u

# Find environment variable references
strings ~/.local/share/claude/versions/2.1.19 | grep "CLAUDE_CODE_TEAM"

# Verify your Claude Code version
claude --version
# Should output: 2.1.19 (Claude Code)
```

## How to Access TeammateTool Today

### Option 1: Unofficial Unlocked Build (Recommended for Testing)

The `claude-sneakpeek` package provides an unlocked version with feature flags enabled:

```bash
# Install unlocked version
npx @realmikekelly/claude-sneakpeek quick --name claudesp

# Verify TeammateTool is available
claudesp --version  # Should show 2.1.19 with sneakpeek

# Run with full TeammateTool access
claudesp
```

**Important Notes:**

- Uses separate config directory: `~/.claude-sneakpeek/`
- Does not affect your standard Claude Code installation
- For research and testing purposes only
- Not officially supported by Anthropic

### Option 2: Wait for Official Release

Anthropic will eventually enable the feature flags and provide official documentation. No release date has been announced.

## Discovery Timeline

| Date             | Event                                                            |
| ---------------- | ---------------------------------------------------------------- |
| **Jan 23, 2026** | Kieran Klaassen performs binary analysis, discovers TeammateTool |
| **Jan 25, 2026** | Analysis published on GitHub Gist and Paddo.dev blog             |
| **Jan 26, 2026** | Story reaches Hacker News, TLDR.tech, LinkedIn tech circles      |
| **Jan 26, 2026** | This skill added to repository with community documentation      |

## Why This Matters

### For Multi-Agent Workflows

TeammateTool provides native infrastructure for:

- **Parallel specialists**: Multiple reviewers (security, performance, architecture) working simultaneously
- **Pipeline workflows**: Sequential stages with automatic dependency unblocking
- **Swarm patterns**: Self-organizing workers claiming tasks from a shared pool
- **Research → Plan → Implement**: Multi-stage workflows with inter-agent handoffs

### For Stateless Agent Methodology

TeammateTool aligns with the [Stateless Agent Methodology](../../methodology_development/stateless-agent-methodology.md):

| SAM Stage               | TeammateTool Support                                 |
| ----------------------- | ---------------------------------------------------- |
| **Discovery**           | Research agents with shared findings                 |
| **Planning**            | Plan approval workflow (`approvePlan`/`rejectPlan`)  |
| **Context Integration** | Multiple agents exploring codebase in parallel       |
| **Task Decomposition**  | Native task list with dependencies                   |
| **Execution**           | Worker agents claiming and completing tasks          |
| **Forensic Review**     | Independent verification agent with separate process |
| **Orchestration**       | Leader coordinates via inbox messages                |
| **Final Verification**  | Aggregator synthesizes all worker results            |

## Community Resources

### Primary Sources (Binary Analysis)

1. **Kieran Klaassen - TeammateTool Source Code Analysis**

   - <https://gist.github.com/kieranklaassen/d2b35569be2c7f1412c64861a219d51f>
   - Direct extraction from compiled binary

2. **Kieran Klaassen - Claude Code Swarm Orchestration Skill**
   - <https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea>
   - Complete operation documentation

### Analysis & Commentary

3. **Paddo.dev - Claude Code's Hidden Multi-Agent System**

   - <https://paddo.dev/blog/claude-code-hidden-swarm/>
   - Why it's gated, comparison to community patterns

4. **ruvnet - Claude Flow vs Claude Code Architectural Comparison**
   - <https://gist.github.com/ruvnet/18dc8d060194017b989d1f8993919ee4>
   - 92% architectural overlap analysis

### Related Projects

5. **ruvnet/claude-flow** - Community multi-agent framework

   - <https://github.com/ruvnet/claude-flow>
   - Validates TeammateTool's architectural patterns

6. **mikekelly/claude-sneakpeek** - Unlocked build
   - <https://github.com/mikekelly/claude-sneakpeek>
   - npm: `@realmikekelly/claude-sneakpeek`

## Official Documentation Status

As of January 26, 2026:

- ❌ Not in official Claude Code documentation (<https://code.claude.com/docs/>)
- ❌ Not in Anthropic documentation (<https://docs.anthropic.com/>)
- ❌ Not in release notes or changelogs
- ❌ No official announcement from Anthropic
- ❌ No official GitHub repository

**The absence is deliberate** - this is feature gating for product release timing, not incomplete development.

## Using This Skill

### Now (Feature-Gated)

The skill serves as:

- **Documentation** of the coming feature
- **API reference** for when flags are enabled
- **Design patterns** for multi-agent coordination
- **Preparation guide** for future workflows

The examples in `SKILL.md` are accurate but **not executable** in standard Claude Code v2.1.19.

### When Enabled (Future)

Once Anthropic enables the feature flags:

1. Load the skill: `Skill(command: "orchestrating-swarms")`
2. Claude will have access to all TeammateTool patterns
3. Examples become directly executable
4. No installation or configuration needed

## Comparison to Standard Sub-Agents

| Feature         | Task (Sub-Agent)     | Task + team_name (Teammate)    |
| --------------- | -------------------- | ------------------------------ |
| Lifespan        | Until task complete  | Until shutdown requested       |
| Communication   | Return value         | Inbox messages                 |
| Task access     | None                 | Shared task list               |
| Team membership | No                   | Yes                            |
| Coordination    | One-off              | Ongoing                        |
| Context         | Fresh per invocation | Persistent within team session |

## Architectural Alignment

TeammateTool has **92% architectural overlap** with Claude Flow V3:

| Concept       | Claude Flow V3   | TeammateTool             |
| ------------- | ---------------- | ------------------------ |
| Group Unit    | Swarm            | Team                     |
| Member        | Agent            | Teammate                 |
| Coordinator   | Queen            | Leader                   |
| Messaging     | MessageBus       | Inbox files              |
| Plan Approval | ConsensusVote    | approvePlan/rejectPlan   |
| Spawn Backend | tmux, in-process | tmux, in-process, iTerm2 |
| Task Sharing  | taskQueue        | ~/.claude/tasks/{team}/  |

Anthropic is **productizing community patterns** - similar to how Steve Yegge's "Beads" architecture became the official Task tool.

## FAQ

### Q: Why isn't this documented officially?

**A:** Feature-gated for product reasons. Likely concerns:

- Cost management (multi-agent = N× API calls)
- Safety and governance (multiple autonomous agents with file system access)
- Support readiness (multi-agent bugs are complex)
- Market positioning and timing

### Q: Is this experimental or unstable?

**A:** No. Binary analysis shows production-quality code with:

- Complete error handling
- Defined schemas
- Graceful degradation
- Environment variable support
- Multiple execution backends

This is finished code waiting for release approval.

### Q: Will this be released?

**A:** Unknown. Anthropic has not announced plans. The complete implementation suggests they intend to release it eventually.

### Q: Should I use claude-sneakpeek in production?

**A:** No. It's an unofficial build for research and testing only. Wait for official Anthropic release for production use.

### Q: Does this work with MCP servers?

**A:** Unknown - not documented in community analysis. Likely yes, as sub-agents inherit MCP tool access from the parent.

### Q: Can teammates spawn other teammates?

**A:** Unknown - binary analysis doesn't confirm or deny. Standard sub-agents cannot spawn other sub-agents, so teammates likely cannot either (prevents infinite nesting).

## Next Steps

1. **Monitor for official release**: Watch Anthropic documentation and release notes
2. **Study the patterns**: The orchestration patterns in SKILL.md are valuable regardless
3. **Design for compatibility**: Build artifact schemas and coordination protocols that map to TeammateTool's message format
4. **Test with sneakpeek** (optional): Experiment with the unlocked build to understand behavior

---

**Last Updated**: January 26, 2026
**Claude Code Version**: 2.1.19
**Status**: Feature-gated (complete but disabled)
**Official Documentation**: None (not yet released)
