# AgentSession reference

The `voice.AgentSession` is the main orchestrator for your voice AI app.

## Constructor options

```typescript
import { voice } from '@livekit/agents';
import * as silero from '@livekit/agents-plugin-silero';
import * as livekit from '@livekit/agents-plugin-livekit';

const session = new voice.AgentSession({
  // Models (use inference strings or plugin instances)
  stt: "assemblyai/universal-streaming:en",
  llm: "openai/gpt-4.1-mini",
  tts: "cartesia/sonic-3:voice_id",
  
  // Voice activity detection
  vad: await silero.VAD.load(),
  
  // Turn detection
  turnDetection: new livekit.turnDetector.MultilingualModel(),
  
  // Voice options
  voiceOptions: {
    allowInterruptions: true,
    minInterruptionDuration: 500,
    minInterruptionWords: 0,
    minEndpointingDelay: 500,
    maxEndpointingDelay: 6000,
    preemptiveGeneration: false,
  },
  
  // User data
  userData: { key: 'value' },
});
```

## Starting the session

```typescript
import { 
  BackgroundVoiceCancellation, 
  TelephonyBackgroundVoiceCancellation 
} from '@livekit/noise-cancellation-node';

await session.start({
  agent: myAgent,
  room: ctx.room,
  inputOptions: {
    // Use BackgroundVoiceCancellation() for standard web/mobile participants
    // Use TelephonyBackgroundVoiceCancellation() for SIP/telephony applications
    noiseCancellation: BackgroundVoiceCancellation(),
  },
});

// Connect to room after starting session
await ctx.connect();

// Optionally wait for the greeting to complete
const handle = session.generateReply({
  instructions: 'Greet the user and offer your assistance.',
});
await handle.waitForPlayout();
```

For telephony applications (SIP calls), use the telephony-optimized noise cancellation:

```typescript
await session.start({
  agent: myAgent,
  room: ctx.room,
  inputOptions: {
    noiseCancellation: TelephonyBackgroundVoiceCancellation(),
  },
});
```

## Key methods

### Generate speech

```typescript
// Generate LLM response
const handle = session.generateReply({
  instructions: 'Greet the user warmly',
  userInput: 'Hello!', // Optional user message
  allowInterruptions: true,
});
await handle.waitForPlayout();

// Speak text directly
const handle = session.say('Hello! How can I help you today?', {
  allowInterruptions: true,
});
await handle.waitForPlayout();
```

### Interrupt and control

```typescript
// Stop current speech
session.interrupt();

// Commit user turn manually (when turnDetection="manual")
session.commitUserTurn();

// Clear user turn
session.clearUserTurn();
```

### Switch agents

```typescript
// Switch to a different agent
session.updateAgent(newAgent);
```

### Access state

```typescript
// Chat context
const chatCtx = session.chatCtx;

// Current agent state
const state = session.agentState; // "initializing", "listening", "thinking", "speaking"

// User data
const data = session.userData;

// Current agent
const agent = session.currentAgent;
```

## Events

```typescript
import { voice } from '@livekit/agents';

session.on(voice.AgentSessionEventTypes.UserStateChanged, (ev) => {
  // ev.newState: "speaking", "listening", "away"
  console.log(`User state: ${ev.newState}`);
});

session.on(voice.AgentSessionEventTypes.AgentStateChanged, (ev) => {
  // ev.newState: "initializing", "listening", "thinking", "speaking"
  console.log(`Agent state: ${ev.newState}`);
});

session.on(voice.AgentSessionEventTypes.ConversationItemAdded, (ev) => {
  console.log(`New message:`, ev.item);
});

session.on(voice.AgentSessionEventTypes.MetricsCollected, (ev) => {
  console.log(`Metrics:`, ev.metrics);
});

session.on(voice.AgentSessionEventTypes.UserInputTranscribed, (ev) => {
  console.log(`User said: ${ev.transcript}`);
});

session.on(voice.AgentSessionEventTypes.SpeechCreated, (ev) => {
  console.log(`Speech created:`, ev);
});

session.on(voice.AgentSessionEventTypes.Close, (ev) => {
  console.log(`Session closed:`, ev.reason);
});
```

## Turn detection modes

```typescript
import * as livekit from '@livekit/agents-plugin-livekit';
import * as silero from '@livekit/agents-plugin-silero';

// Recommended: Turn detector model
const session = new voice.AgentSession({
  turnDetection: new livekit.turnDetector.MultilingualModel(),
  vad: await silero.VAD.load(),
});

// English only (faster)
const session = new voice.AgentSession({
  turnDetection: new livekit.turnDetector.EnglishModel(),
  vad: await silero.VAD.load(),
});

// VAD only
const session = new voice.AgentSession({
  turnDetection: 'vad',
  vad: await silero.VAD.load(),
});

// STT endpointing
const session = new voice.AgentSession({
  turnDetection: 'stt',
  stt: "assemblyai/universal-streaming:en",
  vad: await silero.VAD.load(),
});

// Manual control
const session = new voice.AgentSession({
  turnDetection: 'manual',
});
```

## Voice options

| Option | Default | Description |
|--------|---------|-------------|
| `allowInterruptions` | `true` | Allow user to interrupt agent |
| `discardAudioIfUninterruptible` | `true` | Drop buffered audio when uninterruptible |
| `minInterruptionDuration` | `500` | Minimum speech duration (ms) before interruption |
| `minInterruptionWords` | `0` | Minimum words before interruption |
| `minEndpointingDelay` | `500` | Wait time (ms) before considering turn complete |
| `maxEndpointingDelay` | `6000` | Maximum wait time (ms) for turn completion |
| `maxToolSteps` | `3` | Maximum chained tool calls |
| `preemptiveGeneration` | `false` | Start LLM response while user still speaking |
| `userAwayTimeout` | `15.0` | Seconds before marking user as away |

## Closing the session

```typescript
// Graceful close
await session.close();

// Shutdown with options
session.shutdown({ drain: true, reason: 'user_initiated' });
```

## Input/Output control

```typescript
// Access input/output objects
const input = session.input;
const output = session.output;

// Enable/disable audio input
session.input.setAudioEnabled(false);
session.input.setAudioEnabled(true);
```
