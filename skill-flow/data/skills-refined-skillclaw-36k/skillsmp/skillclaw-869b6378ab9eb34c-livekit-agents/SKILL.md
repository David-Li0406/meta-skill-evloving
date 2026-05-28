---
name: livekit-agents
description: Use this skill when building voice AI agents, voice assistants, or any realtime AI application using LiveKit's Agents SDK in either TypeScript or Python.
---

# LiveKit Agents SDK

Build voice AI agents with LiveKit's Agents SDK, available in both TypeScript and Python.

## LiveKit MCP server tools

This skill works alongside the LiveKit MCP server, which provides direct access to the latest LiveKit documentation, code examples, and changelogs. Use these tools when you need up-to-date information that may have changed since this skill was created.

**Available MCP tools:**
- `docs_search` - Search the LiveKit docs site
- `get_pages` - Fetch specific documentation pages by path
- `get_changelog` - Get recent releases and updates for LiveKit packages
- `code_search` - Search LiveKit repositories for code examples
- `get_python_agent_example` - Browse 100+ Python agent examples

**When to use MCP tools:**
- You need the latest API documentation or feature updates
- You're looking for recent examples or code patterns
- You want to check if a feature has been added in recent releases
- The local references don't cover a specific topic

**When to use local references:**
- You need quick access to core concepts covered in this skill
- You're working offline or want faster access to common patterns
- The information in the references is sufficient for your needs

Use MCP tools and local references together for the best experience.

## References

Consult these resources as needed:

- ./references/livekit-overview.md -- LiveKit ecosystem overview and how these skills work together
- ./references/agent-session.md -- AgentSession lifecycle, events, and configuration
- ./references/tools.md -- Function tools with zod schemas and RunContext
- ./references/models.md -- STT, LLM, TTS models and plugin configuration
- ./references/workflows.md -- Multi-agent handoffs, Tasks, TaskGroups, and pipeline nodes

## Installation

For TypeScript:

```bash
pnpm add @livekit/agents@1.x \
    @livekit/agents-plugin-silero@1.x \
    @livekit/agents-plugin-livekit@1.x \
    @livekit/noise-cancellation-node@0.x \
    dotenv
```

For Python:

```bash
uv add "livekit-agents[silero,turn-detector]~=1.3" \
  "livekit-plugins-noise-cancellation~=0.2" \
  "python-dotenv"
```

## Environment variables

Use the LiveKit CLI to load your credentials into a `.env.local` file:

```bash
lk app env -w
```

Or manually create a `.env.local` file:

```bash
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_URL=wss://your-project.livekit.cloud
```