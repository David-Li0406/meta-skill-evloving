---
name: livekit
description: LiveKit real-time communication platform for building voice and text AI agents, video conferencing, and telephony applications
---

# LiveKit Skill

Comprehensive assistance with LiveKit development for voice AI agents, text chat agents, video applications, and telephony integrations.

## When to Use This Skill

This skill should be triggered when:
- Building voice AI agents with speech-to-text and text-to-speech
- Creating text/chat-based AI agents
- Implementing real-time communication (WebRTC)
- Integrating telephony (SIP, phone calls)
- Working with LiveKit SDKs (Python, Node.js, React, etc.)
- Configuring LLM, STT, and TTS providers

## Quick Reference

### Voice Agent - Minimal Setup (Python)

```python
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.agents.llm import function_tool
from livekit.plugins import openai, silero

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=Agent(instructions="You are a helpful assistant."),
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
```

### Voice Agent - With Tools

```python
from livekit.agents import AgentSession, Agent
from livekit.agents.llm import function_tool
from livekit.plugins import openai, silero

class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful assistant that can look up weather."
        )

    @function_tool()
    async def get_weather(self, location: str) -> str:
        """Get the current weather for a location."""
        # Your weather API call here
        return f"The weather in {location} is sunny, 72°F"

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o"),
        tts=openai.TTS(),
        vad=silero.VAD.load(),
    )

    await session.start(room=ctx.room, agent=MyAgent())
```

### Text-Only Agent (No Voice)

```python
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    # Text-only: no STT, TTS, or VAD needed
    session = AgentSession(
        llm=openai.LLM(model="gpt-4o"),
    )

    await session.start(
        room=ctx.room,
        agent=Agent(instructions="You are a helpful text assistant."),
        room_input_options=RoomInputOptions(text_enabled=True),
    )
```

### Generate Reply Programmatically

```python
# Trigger agent to speak without user input
await session.generate_reply(
    instructions="Greet the user and offer your assistance."
)

# Or with specific user message
await session.generate_reply(
    user_input="Tell me about the weather"
)
```

### Access Token Generation (Server-Side)

```python
from livekit import api
import os

token = api.AccessToken(
    os.getenv('LIVEKIT_API_KEY'),
    os.getenv('LIVEKIT_API_SECRET')
).with_identity("user-123") \
 .with_name("John Doe") \
 .with_grants(api.VideoGrants(
    room_join=True,
    room="my-room",
))

jwt_token = token.to_jwt()
```

### React Frontend Component

```tsx
import { LiveKitRoom, VideoConference } from '@livekit/components-react';
import '@livekit/components-styles';

export function MyRoom({ token, serverUrl }) {
  return (
    <LiveKitRoom
      token={token}
      serverUrl={serverUrl}
      connect={true}
    >
      <VideoConference />
    </LiveKitRoom>
  );
}
```

### Telephony Agent (SIP Integration)

```python
from livekit.agents import AgentServer, JobContext
import livekit.agents as agents

server = AgentServer()

@server.rtc_session(agent_name="my-telephony-agent")
async def my_agent(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=deepgram.STT(),
        llm=openai.LLM(),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=Agent(instructions="You are a phone support agent."),
    )

if __name__ == "__main__":
    agents.cli.run_app(server)
```

### Multi-Turn Workflow with Tasks

```python
from livekit.agents import AgentTask, function_tool, RunContext
from livekit.agents.beta.workflows import TaskGroup
from dataclasses import dataclass

@dataclass
class IntroResults:
    name: str
    intro: str

class IntroTask(AgentTask[IntroResults]):
    def __init__(self):
        super().__init__(
            instructions="Welcome the user and collect their name."
        )

    async def on_enter(self):
        await self.session.generate_reply(
            instructions="Greet the user and ask for their name."
        )

    @function_tool()
    async def record_name(self, context: RunContext, name: str) -> None:
        """Record the user's name"""
        results = IntroResults(name=name, intro="")
        self.complete(results)

# Use in workflow
task_group = TaskGroup()
task_group.add_task(IntroTask())
```

## Provider Configuration

### LLM Providers

```python
# OpenAI
from livekit.plugins import openai
llm = openai.LLM(model="gpt-4o")

# Anthropic Claude
from livekit.plugins import anthropic
llm = anthropic.LLM(model="claude-3-5-sonnet-20241022")

# Google Gemini
from livekit.plugins import google
llm = google.LLM(model="gemini-2.0-flash-exp")

# Groq (fast inference)
from livekit.plugins import groq
llm = groq.LLM(model="llama-3.1-70b-versatile")

# Ollama (local)
from livekit.plugins import ollama
llm = ollama.LLM(model="llama3.2")
```

### STT Providers

```python
# OpenAI Whisper
from livekit.plugins import openai
stt = openai.STT()

# Deepgram
from livekit.plugins import deepgram
stt = deepgram.STT()

# AssemblyAI
from livekit.plugins import assemblyai
stt = assemblyai.STT()

# Azure
from livekit.plugins import azure
stt = azure.STT()
```

### TTS Providers

```python
# OpenAI
from livekit.plugins import openai
tts = openai.TTS(voice="alloy")

# ElevenLabs
from livekit.plugins import elevenlabs
tts = elevenlabs.TTS(voice_id="your-voice-id")

# Cartesia
from livekit.plugins import cartesia
tts = cartesia.TTS()

# Deepgram
from livekit.plugins import deepgram
tts = deepgram.TTS()
```

## Environment Variables

```bash
# LiveKit Server
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# AI Providers (use whichever you need)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEEPGRAM_API_KEY=...
ELEVENLABS_API_KEY=...
CARTESIA_API_KEY=...
```

## CLI Commands

```bash
# Run agent in development mode
uv run agent.py dev

# Run agent in production
uv run agent.py start

# Create a new agent project
lk app create

# List projects
lk cloud projects list

# Create SIP dispatch rule
lk sip dispatch create dispatch-rule.json
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **llms-full.md** - Complete LiveKit documentation (50,000+ lines)
- **llms.md** - Condensed documentation overview
- **voice.md** - Voice agent examples and patterns
- **agents.md** - Agent framework documentation
- **getting_started.md** - Quick start guides

Use `view` to read specific reference files when detailed information is needed.

## Key Concepts

### Agent Session
The `AgentSession` orchestrates STT → LLM → TTS pipeline for voice agents.

### Function Tools
Decorate methods with `@function_tool()` to let the LLM call your functions.

### VAD (Voice Activity Detection)
Silero VAD detects when users start/stop speaking for natural turn-taking.

### Rooms, Participants, Tracks
- **Room**: A virtual space for communication
- **Participant**: A user or agent in a room
- **Track**: Audio/video stream from a participant

### Agent Dispatch
Control how agents are assigned to rooms - automatic or explicit.

## Common Patterns

### Handle User Join
```python
@ctx.room.on("participant_connected")
def on_participant_connected(participant):
    print(f"User joined: {participant.identity}")
```

### Send Data Messages
```python
await ctx.room.local_participant.publish_data(
    payload=b"Hello from agent",
    topic="chat"
)
```

### Interrupt Handling
```python
session = AgentSession(
    # ... other config
    interrupt_min_words=3,  # Minimum words before allowing interrupt
)
```

## Resources

- **LiveKit Cloud**: https://cloud.livekit.io
- **Python SDK**: https://github.com/livekit/agents
- **Node.js SDK**: https://github.com/livekit/agents-js
- **React Components**: https://github.com/livekit/components-js
- **Documentation**: https://docs.livekit.io

## Notes

- This skill was automatically generated from LiveKit's llms.txt documentation
- Reference files contain the complete official documentation
- Code examples are extracted from official docs with language annotations
- For telephony, you need a SIP provider (Twilio, Telnyx, etc.)
