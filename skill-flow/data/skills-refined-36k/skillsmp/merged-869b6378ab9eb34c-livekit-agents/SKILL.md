---
name: livekit-agents
description: Use this skill when building voice AI agents, voice assistants, or any realtime AI application using LiveKit's Agents SDKs in TypeScript or Python.
---

# LiveKit Agents SDK

Build voice AI agents with LiveKit's Agents SDKs for TypeScript and Python.

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
- ./references/tools.md -- Function tools, RunContext, and tool results
- ./references/models.md -- STT, LLM, TTS model strings and plugin configuration
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

## Quick start

### Basic agent with STT-LLM-TTS pipeline

**TypeScript Example:**

```typescript
import {
  type JobContext,
  type JobProcess,
  WorkerOptions,
  cli,
  defineAgent,
  voice,
} from '@livekit/agents';
import * as livekit from '@livekit/agents-plugin-livekit';
import * as silero from '@livekit/agents-plugin-silero';
import { BackgroundVoiceCancellation } from '@livekit/noise-cancellation-node';
import { fileURLToPath } from 'node:url';
import dotenv from 'dotenv';

dotenv.config({ path: '.env.local' });

export default defineAgent({
  prewarm: async (proc: JobProcess) => {
    proc.userData.vad = await silero.VAD.load();
  },
  entry: async (ctx: JobContext) => {
    const vad = ctx.proc.userData.vad! as silero.VAD;
    
    const assistant = new voice.Agent({
      instructions: `You are a helpful voice AI assistant.
        Keep responses concise, 1-3 sentences. No markdown or emojis.`,
    });

    const session = new voice.AgentSession({
      vad,
      stt: "assemblyai/universal-streaming:en",
      llm: "openai/gpt-4.1-mini",
      tts: "cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
      turnDetection: new livekit.turnDetector.MultilingualModel(),
    });

    await session.start({
      agent: assistant,
      room: ctx.room,
      inputOptions: {
        noiseCancellation: BackgroundVoiceCancellation(),
      },
    });

    await ctx.connect();

    const handle = session.generateReply({
      instructions: 'Greet the user and offer your assistance.',
    });
    await handle.waitForPlayout();
  },
});

cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));
```

**Python Example:**

```python
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import AgentSession, Agent, AgentServer, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(".env.local")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant.
            Keep responses concise, 1-3 sentences. No markdown or emojis.""",
        )

server = AgentServer()

@server.rtc_session()
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt="assemblyai/universal-streaming:en",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony()
                    if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )

if __name__ == "__main__":
    agents.cli.run_app(server)
```

### Basic agent with realtime model

**TypeScript Example:**

```typescript
import {
  type JobContext,
  WorkerOptions,
  cli,
  defineAgent,
  voice,
} from '@livekit/agents';
import * as openai from '@livekit/agents-plugin-openai';
import { BackgroundVoiceCancellation } from '@livekit/noise-cancellation-node';
import { fileURLToPath } from 'node:url';
import dotenv from 'dotenv';

dotenv.config({ path: '.env.local' });

export default defineAgent({
  entry: async (ctx: JobContext) => {
    const assistant = new voice.Agent({
      instructions: 'You are a helpful voice AI assistant.',
    });

    const session = new voice.AgentSession({
      llm: new openai.realtime.RealtimeModel({
        voice: 'coral',
      }),
    });

    await session.start({
      agent: assistant,
      room: ctx.room,
      inputOptions: {
        noiseCancellation: BackgroundVoiceCancellation(),
      },
    });

    await ctx.connect();

    const handle = session.generateReply({
      instructions: 'Greet the user and offer your assistance.',
    });
    await handle.waitForPlayout();
  },
});

cli.runApp(new WorkerOptions({ agent: fileURLToPath(import.meta.url) }));
```

**Python Example:**

```python
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import AgentSession, Agent, AgentServer, room_io
from livekit.plugins import openai, noise_cancellation

load_dotenv(".env.local")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful voice AI assistant."
        )

server = AgentServer()

@server.rtc_session()
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(voice="coral")
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony()
                    if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )

if __name__ == "__main__":
    agents.cli.run_app(server)
```

## Core concepts

### Agent class

Define agent behavior by subclassing `Agent`:

**TypeScript:**

```typescript
import { defineAgent, type JobContext, type JobProcess } from '@livekit/agents';

export default defineAgent({
  prewarm: async (proc: JobProcess) => {
    proc.userData.vad = await silero.VAD.load();
  },
  
  entry: async (ctx: JobContext) => {
    // Your agent logic here
  },
});
```

**Python:**

```python
from livekit.agents import Agent, function_tool

class MyAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="Your system prompt here",
        )

    async def on_enter(self) -> None:
        await self.session.generate_reply(
            instructions="Greet the user"
        )

    async def on_exit(self) -> None:
        pass

    @function_tool()
    async def my_tool(self, param: str) -> str:
        return f"Result: {param}"
```

### AgentSession

The session orchestrates the voice pipeline:

**TypeScript:**

```typescript
const session = new voice.AgentSession({
  stt: "assemblyai/universal-streaming:en",
  llm: "openai/gpt-4.1-mini",
  tts: "cartesia/sonic-3:voice_id",
  vad: await silero.VAD.load(),
  turnDetection: new livekit.turnDetector.MultilingualModel(),
});
```

**Python:**

```python
session = AgentSession(
    stt="assemblyai/universal-streaming:en",
    llm="openai/gpt-4.1-mini",
    tts="cartesia/sonic-3:voice_id",
    vad=silero.VAD.load(),
    turn_detection=MultilingualModel(),
)
```

Key methods:
- `session.start(room, agent)` - Start the session
- `session.say(text)` - Speak text directly
- `session.generate_reply(instructions)` - Generate LLM response
- `session.interrupt()` - Stop current speech
- `session.update_agent(new_agent)` - Switch to different agent

## Running the agent

For TypeScript:

```bash
# Development mode with auto-reload
pnpm dev

# Production mode
pnpm build && pnpm start

# Download required model files
pnpm download-files
```

For Python:

```bash
# Development mode with auto-reload
uv run agent.py dev

# Console mode (local testing)
uv run agent.py console

# Production mode
uv run agent.py start

# Download required model files
uv run agent.py download-files
```

## LiveKit Inference model strings

Use model strings for simple configuration without API keys:

**STT (Speech-to-Text)**:
- `"assemblyai/universal-streaming:en"` - AssemblyAI streaming
- `"deepgram/nova-3:en"` - Deepgram Nova
- `"cartesia/ink"` - Cartesia STT

**LLM (Large Language Model)**:
- `"openai/gpt-4.1-mini"` - GPT-4.1 mini (recommended)
- `"openai/gpt-4.1"` - GPT-4.1
- `"openai/gpt-5"` - GPT-5
- `"gemini/gemini-3-flash"` - Gemini 3 Flash

**TTS (Text-to-Speech)**:
- `"cartesia/sonic-3:{voice_id}"` - Cartesia Sonic 3
- `"elevenlabs/eleven_turbo_v2_5:{voice_id}"` - ElevenLabs
- `"deepgram/aura:{voice}"` - Deepgram Aura

## Best practices

1. **Always use LiveKit Inference model strings** as the default for STT, LLM, and TTS. This eliminates the need to manage individual provider API keys. Only use plugins when you specifically need custom models, voice cloning, or self-hosted models.
2. **Use adaptive noise cancellation** with a lambda to detect SIP participants and apply appropriate noise cancellation.
3. **Use MultilingualModel turn detection** for natural conversation flow.
4. **Structure prompts** with Identity, Output rules, Tools, Goals, and Guardrails sections.
5. **Test with console mode** before deploying to LiveKit Cloud.
6. **Use `lk app env -w`** to load LiveKit Cloud credentials into your environment.