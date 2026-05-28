# AgentSession reference

The `AgentSession` is the main orchestrator for your voice AI app.

## Constructor options

```python
from livekit.agents import AgentSession
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

session = AgentSession(
    # Models (use inference strings or plugin instances)
    stt="assemblyai/universal-streaming:en",
    llm="openai/gpt-4.1-mini",
    tts="cartesia/sonic-3:voice_id",
    
    # Voice activity detection
    vad=silero.VAD.load(),
    
    # Turn detection
    turn_detection=MultilingualModel(),  # or "vad", "stt", "manual"
    
    # Voice options
    allow_interruptions=True,
    min_interruption_duration=0.5,
    min_interruption_words=0,
    min_endpointing_delay=0.5,
    max_endpointing_delay=3.0,
    
    # User data
    userdata={"key": "value"},
)
```

## Starting the session

```python
from livekit import rtc
from livekit.agents import room_io
from livekit.plugins import noise_cancellation

await session.start(
    room=ctx.room,
    agent=my_agent,
    room_options=room_io.RoomOptions(
        audio_input=room_io.AudioInputOptions(
            # Use adaptive noise cancellation based on participant type
            noise_cancellation=lambda params: noise_cancellation.BVCTelephony()
                if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                else noise_cancellation.BVC(),
        ),
    ),
)
```

## Key methods

### Generate speech

```python
# Generate LLM response
handle = session.generate_reply(
    instructions="Greet the user warmly",
    user_input="Hello!",  # Optional user message
    allow_interruptions=True,
)
await handle.wait_for_playout()

# Speak text directly
handle = session.say(
    "Hello! How can I help you today?",
    allow_interruptions=True,
)
await handle.wait_for_playout()
```

### Interrupt and control

```python
# Stop current speech
session.interrupt()

# Commit user turn manually (when turn_detection="manual")
session.commit_user_turn()

# Clear user turn
session.clear_user_turn()
```

### Switch agents

```python
# Switch to a different agent
session.update_agent(new_agent)
```

### Access state

```python
# Chat context
chat_ctx = session.chat_ctx

# Current agent state
state = session.agent_state  # "initializing", "listening", "thinking", "speaking"

# User data
data = session.userdata
```

## Events

```python
from livekit.agents import (
    UserStateChangedEvent,
    AgentStateChangedEvent,
    ConversationItemAddedEvent,
    MetricsCollectedEvent,
)

@session.on("user_state_changed")
def on_user_state_changed(ev: UserStateChangedEvent):
    # ev.new_state: "speaking", "listening", "away"
    print(f"User state: {ev.new_state}")

@session.on("agent_state_changed")
def on_agent_state_changed(ev: AgentStateChangedEvent):
    # ev.new_state: "initializing", "listening", "thinking", "speaking"
    print(f"Agent state: {ev.new_state}")

@session.on("conversation_item_added")
def on_conversation_item_added(ev: ConversationItemAddedEvent):
    print(f"New message: {ev.item}")

@session.on("metrics_collected")
def on_metrics_collected(ev: MetricsCollectedEvent):
    print(f"Metrics: {ev.metrics}")

@session.on("user_input_transcribed")
def on_user_input_transcribed(ev):
    print(f"User said: {ev.transcript}")
```

## Turn detection modes

```python
# Recommended: Turn detector model
from livekit.plugins.turn_detector.multilingual import MultilingualModel
session = AgentSession(
    turn_detection=MultilingualModel(),
    vad=silero.VAD.load(),
)

# VAD only
session = AgentSession(
    turn_detection="vad",
    vad=silero.VAD.load(),
)

# STT endpointing
session = AgentSession(
    turn_detection="stt",
    stt="assemblyai/universal-streaming:en",
    vad=silero.VAD.load(),
)

# Manual control
session = AgentSession(
    turn_detection="manual",
)
```

## Voice options

| Option | Default | Description |
|--------|---------|-------------|
| `allow_interruptions` | `True` | Allow user to interrupt agent |
| `min_interruption_duration` | `0.5` | Minimum speech duration before interruption |
| `min_interruption_words` | `0` | Minimum words before interruption |
| `min_endpointing_delay` | `0.5` | Wait time before considering turn complete |
| `max_endpointing_delay` | `3.0` | Maximum wait time for turn completion |
| `preemptive_generation` | `False` | Start LLM response while user still speaking |

## Closing the session

```python
# Graceful close
await session.close()

# Shutdown with options
session.shutdown(drain=True, reason="user_initiated")
```
