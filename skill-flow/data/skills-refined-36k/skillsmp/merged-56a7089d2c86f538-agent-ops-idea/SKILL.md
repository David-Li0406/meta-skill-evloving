---
name: agent-ops-idea
description: Capture loosely structured ideas, enrich them with research, and create backlog issues. Use this skill when a user has a raw concept that needs fleshing out.
---

# Agent Idea Workflow

## Purpose

Transform loosely structured ideas into well-researched IDEA issues in the backlog. This skill bridges the gap between "I have a vague idea" and "I have a trackable, researched issue ready for triage."

## When to Use

- User says "I have an idea for..." or "/agent-idea"
- User describes a concept without clear requirements
- User wants to explore feasibility before committing to work
- Brainstorming sessions that should be captured

## MCP Integration (Optional Enhancement)

When MCP tools are available, use them to enhance research quality.

### Check MCP Availability

At skill start, check if MCP is configured:
1. Look for `.agent/mcp.yaml` or project's `mcp.yaml`
2. If present, MCP tools may be available for enhanced research

### Available MCP Tools

| Tool | Provider | Use Case |
|------|----------|----------|
| `brave_web_search` | brave-search | Search web for existing solutions, similar projects |
| `get_library_docs` | context7 | Get library documentation for relevant packages |
| `search_repositories` | github | Find similar open source implementations |
| `get_readme` | github | Fetch README from relevant repositories |

### Research Source Tags

When reporting research findings, tag sources with emojis:
- 🌐 = Web search (MCP: brave-search)
- 📚 = Library docs (MCP: context7)
- 🔍 = GitHub search (MCP: github)
- 💭 = Agent analysis (training data/reasoning)

### Graceful Fallback

If MCP tools fail or are unavailable:
1. **Log but don't block**: Note tool unavailability, continue with agent knowledge
2. **Tag appropriately**: Use 💭 tag for agent-sourced research
3. **Be transparent**: Mention in research notes that external tools were unavailable

Example fallback note:
```
⚠️ MCP tools unavailable — research based on agent knowledge.
For deeper research, enable MCP: `pip install agent-ops-cli[mcp]`
```

## Procedure

### Phase 1: Capture Raw Idea

1. **Accept idea text** from user (can be informal, incomplete, or vague)
2. **Echo back understanding**: "I understand you want to: {paraphrase}"
3. **Ask clarifying question** (optional, only if truly unclear):
   - "What problem does this solve?" OR
   - "Who would use this?" OR
   - "Can you give an example use case?"

**Keep friction low** — don't over-interview. One clarifying question max.

### Phase 2: Research Guidance

**Step 1: Check MCP availability**
- If MCP available: Use tools for enhanced research
- If MCP unavailable: Use agent knowledge with transparency

**Step 2: Research using available sources**

Present research prompts to enrich the idea. The agent should investigate these areas:

| Research Area | MCP Tool (if available) | Fallback |
|---------------|------------------------|----------|
| **Existing solutions** | `brave_web_search` | Agent knowledge 💭 |
| **Relevant libraries** | `get_library_docs` | Agent knowledge 💭 |
| **Similar implementations** | `search_repositories` | Agent knowledge 💭 |
| **Best practices** | Agent analysis 💭 | Agent analysis 💭 |
| **Potential challenges** | Agent analysis 💭 | Agent analysis 💭 |

**Research output format:**
```markdown
### Research Findings

#### Existing Solutions [source tag]
- {solution 1}: {brief description, link if applicable}
- {solution 2}: {brief description}

#### Relevant Libraries/Tools [source tag]
- {library}: {what it provides}

#### Similar Implementations [source tag]
- {project/example}: {how it's relevant}

#### Potential Challenges [💭 Agent Analysis]
- {challenge 1}
- {challenge 2}
```

**Note**: Research depth should match idea scope. Simple ideas need less research.

### Phase 3: Create IDEA Issue

Generate issue using this template:

```markdown
## IDEA-{NUMBER}@{HASH} — {Title}

**Status:** `idea`
**Type:** IDEA
**Created:** {YYYY-MM-DD}
**Epic:** {if applicable}
**Research Sources:** {MCP tools used, or "Agent knowledge"}

### Original Idea

{User's raw idea text, preserved verbatim}

### Problem Statement

{What problem does this solve? Why is it valuable?}

### Research Findings

#### Existing Solutions [source tag]
{List existing tools/solutions that address similar needs}

#### Relevant Libraries/Tools [source tag]
{Packages, frameworks, or tools that could help implementation}

#### Similar Implementations [source tag]
{Examples from other projects, open source references}

#### Potential Challenges [💭 Agent Analysis]
{Technical or UX obstacles to consider}

### Suggested Approach

{High-level approach based on research}

### Next Steps

- [ ] Triage to determine priority
- [ ] Refine into concrete requirements
- [ ] Break into implementation tasks (if approved)

### External References

- {link 1}
- {link 2}
```

### Phase 4: Save and Confirm

1. **Generate ID**: Read `.counter`, increment, generate hash
2. **Append to backlog.md**: Add issue at end of file
3. **Update focus.md**: Note "Created IDEA-{ID} from user idea"
4. **Present confirmation**:

```
✅ Created IDEA-{ID}: {Title}

Research summary:
- Found {N} existing solutions
- Identified {N} relevant libraries
- Noted {N} potential challenges

The idea has been added to backlog.md with status `idea`.

What's next?
1. Triage this idea (assign priority)
2. Research more deeply
3. Create another idea
4. Done for now
```

## Minimal Mode

For quick capture without research (user says "just capture it"):

1. Accept raw idea text
2. Create minimal IDEA issue:
   ```markdown
   ## IDEA-{NUMBER}@{HASH} — {Title}

   **Status:** `idea`
   **Type:** IDEA
   **Created:** {YYYY-MM-DD}

   ### Original Idea

   {User's raw idea text}

   ### Notes

   (No research conducted — quick capture mode)
   ```
3. Save and confirm

## Research Quality Guidelines

### Good Research Output

- ✅ Specific tool/library names with brief descriptions
- ✅ Links to relevant documentation or examples
- ✅ Honest assessment of challenges
- ✅ Actionable suggested approach

### Poor Research Output (avoid)

- ❌ Generic statements ("there are many solutions")
- ❌ Speculation without evidence
- ❌ Overwhelming detail for simple ideas
- ❌ Missing the user's actual intent

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `agent-ops-tasks` | Uses issue creation procedure, ID generation |
| `agent-ops-interview` | Used for clarifying questions (sparingly) |
| `agent-ops-focus-scan` | IDEA issues appear in backlog for triage |
| `agent-ops-planning` | Triaged ideas become planning inputs |

## Completion Criteria

- [ ] Raw idea captured in issue
- [ ] Research conducted (unless minimal mode)
- [ ] Research sources clearly attributed (MCP vs agent knowledge)
- [ ] Issue saved to backlog.md with valid ID
- [ ] Counter file updated
- [ ] User presented with next step options

## Anti-patterns (avoid)

- ❌ Over-interviewing — keep friction low
- ❌ Skipping research entirely (unless user requests minimal mode)
- ❌ Creating detailed implementation plans (that's planning skill's job)
- ❌ Auto-triaging — let user decide priority
- ❌ Blocking on perfect research — good enough is fine
- ❌ Failing silently when MCP tools error — log and fallback gracefully
- ❌ Presenting agent knowledge as verified external facts

## Examples

### Example 1: Full Workflow with MCP

**User**: "I have an idea — what if we could sync issues to Notion?"

**Agent Response** (with MCP available):
```
I understand you want to: Sync AgentOps issues bidirectionally with Notion.

Let me research this using available tools...

### Research Findings

#### Existing Solutions [🌐 MCP: brave-search]
- notion-py: Unofficial Python client for Notion API
- Notion API (official): REST API with database support
- notion-database-py: Database-focused wrapper

#### Relevant Libraries/Tools [📚 MCP: context7]
- notion-client (official Python SDK): Full API coverage, async support
- notion-database: Simplified database operations

#### Similar Implementations [🔍 MCP: github]
- todoist-notion-sync: Bidirectional Todoist ↔ Notion sync
- obsidian-notion-bridge: Document sync implementation

#### Potential Challenges [💭 Agent Analysis]
- Notion API rate limits (3 requests/second)
- Bidirectional sync conflict resolution
- Mapping issue schema to Notion database schema

#### Suggested Approach
Create a `notion-sync` command in aoc that:
1. Maps issue fields to Notion database columns
2. Uses official Notion SDK for API calls
3. Tracks sync state to handle conflicts

---

✅ Created IDEA-0134@f2e3d4: Notion Integration for Issue Sync

Research sources: brave-search, context7, github
Added to backlog.md. What's next?
```

### Example 2: Full Workflow without MCP

**User**: "I have an idea — what if we could sync issues to Notion?"

**Agent Response** (MCP unavailable):
```
I understand you want to: Sync AgentOps issues bidirectionally with Notion.

⚠️ MCP tools not configured — using agent knowledge for research.

### Research Findings

#### Existing Solutions [💭 Agent Analysis]
- Notion API: Official REST API with database support
- notion-py: Community Python client

#### Relevant Libraries/Tools [💭 Agent Analysis]
- notion-client: Official Python SDK from Notion

#### Similar Implementations [💭 Agent Analysis]
- Various sync scripts exist on GitHub for Todoist, Obsidian

#### Potential Challenges [💭 Agent Analysis]
- Notion API rate limits
- Bidirectional sync conflict resolution
- Schema mapping between systems

---

✅ Created IDEA-0134@f2e3d4: Notion Integration for Issue Sync

Research sources: Agent knowledge only
For enhanced research, enable MCP: `pip install agent-ops-cli[mcp]`

Added to backlog.md. What's next?
```

### Example 3: Minimal Mode

**User**: "/agent-idea Add voice control for TUI — just capture it, no research needed"

**Agent Response**:
```
✅ Created IDEA-0135@a1b2c3: Voice Control for TUI

Captured in backlog.md (minimal mode, no research).

What's next?
```