# Components reference

All Agents UI components, their props, and usage examples.

## AgentSessionProvider

Required wrapper that provides session state to all child components. It wraps `SessionProvider` from `@livekit/components-react` and includes `RoomAudioRenderer` for audio playback.

You must create a session using `useSession` from `@livekit/components-react` and pass it to `AgentSessionProvider`:

```tsx
import { useRef, useEffect } from 'react';
import { useSession } from '@livekit/components-react';
import { TokenSource, TokenSourceConfigurable } from 'livekit-client';
import { AgentSessionProvider } from '@/components/agents-ui/agent-session-provider';

function MyApp() {
  // Use useRef to prevent recreating TokenSource on each render
  const tokenSource: TokenSourceConfigurable = useRef(
    TokenSource.endpoint('/api/token')
  ).current;

  // Create session using useSession hook (required)
  const session = useSession(tokenSource, { agentName: 'your-agent' });

  // Start session when component mounts
  useEffect(() => {
    session.start();
    return () => session.end();
  }, []);

  return (
    <AgentSessionProvider session={session}>
      {children}
    </AgentSessionProvider>
  );
}
```

| Prop | Type | Description |
|------|------|-------------|
| `session` | `UseSessionReturn` | Session object from `useSession` hook (required) |
| `volume` | `number` | Volume for the audio renderer |
| `muted` | `boolean` | Whether to mute the audio renderer |

## AgentControlBar

Combined control bar with track toggles and visualizer.

```tsx
import { AgentControlBar } from '@/components/agents-ui/agent-control-bar';

<AgentControlBar className="gap-4" />
```

| Prop | Type | Description |
|------|------|-------------|
| `className` | `string` | Additional CSS classes |

## AgentAudioVisualizerBar

Horizontal bar audio visualizer responding to agent speech.

```tsx
import { AgentAudioVisualizerBar } from '@/components/agents-ui/agent-audio-visualizer-bar';

<AgentAudioVisualizerBar 
  className="h-16 w-48"
  barCount={5}
  barWidth={4}
  barGap={2}
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | - | Additional CSS classes |
| `barCount` | `number` | `5` | Number of bars |
| `barWidth` | `number` | `4` | Width of each bar in pixels |
| `barGap` | `number` | `2` | Gap between bars in pixels |

## AgentAudioVisualizerGrid

Grid/dot matrix audio visualizer.

```tsx
import { AgentAudioVisualizerGrid } from '@/components/agents-ui/agent-audio-visualizer-grid';

<AgentAudioVisualizerGrid 
  className="w-32 h-32"
  rows={4}
  cols={4}
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | - | Additional CSS classes |
| `rows` | `number` | `4` | Number of rows |
| `cols` | `number` | `4` | Number of columns |

## AgentAudioVisualizerRadial

Circular/radial audio visualizer.

```tsx
import { AgentAudioVisualizerRadial } from '@/components/agents-ui/agent-audio-visualizer-radial';

<AgentAudioVisualizerRadial 
  className="w-48 h-48"
  barCount={32}
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | - | Additional CSS classes |
| `barCount` | `number` | `32` | Number of radial bars |

## AgentAudioVisualizerWave

Waveform-style audio visualizer.

```tsx
import { AgentAudioVisualizerWave } from '@/components/agents-ui/agent-audio-visualizer-wave';

<AgentAudioVisualizerWave 
  className="w-64 h-16"
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | - | Additional CSS classes |

## AgentAudioVisualizerAura

Ambient aura-style audio visualizer designed in partnership with Unicorn Studio. Creates a glowing visual effect that responds to agent audio.

```tsx
import { AgentAudioVisualizerAura } from '@/components/agents-ui/agent-audio-visualizer-aura';

<AgentAudioVisualizerAura 
  className="w-64 h-64"
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | - | Additional CSS classes |

## AgentTrackToggle

Toggle button for a specific track source.

```tsx
import { AgentTrackToggle } from '@/components/agents-ui/agent-track-toggle';

<AgentTrackToggle source="microphone" />
<AgentTrackToggle source="camera" />
<AgentTrackToggle source="screen_share" />
```

| Prop | Type | Description |
|------|------|-------------|
| `source` | `"microphone" \| "camera" \| "screen_share"` | Track source to control |
| `className` | `string` | Additional CSS classes |

## AgentTrackControl

Track control with label and toggle.

```tsx
import { AgentTrackControl } from '@/components/agents-ui/agent-track-control';

<AgentTrackControl source="microphone" />
```

| Prop | Type | Description |
|------|------|-------------|
| `source` | `"microphone" \| "camera" \| "screen_share"` | Track source to control |
| `className` | `string` | Additional CSS classes |

## AgentChatTranscript

Displays the conversation transcript between user and agent.

```tsx
import { AgentChatTranscript } from '@/components/agents-ui/agent-chat-transcript';

<AgentChatTranscript 
  className="h-96 overflow-y-auto"
  showTimestamps={true}
/>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | - | Additional CSS classes |
| `showTimestamps` | `boolean` | `false` | Show message timestamps |

## AgentChatIndicator

Shows when the agent is thinking or typing.

```tsx
import { AgentChatIndicator } from '@/components/agents-ui/agent-chat-indicator';

<AgentChatIndicator />
```

| Prop | Type | Description |
|------|------|-------------|
| `className` | `string` | Additional CSS classes |

## AgentDisconnectButton

Button to disconnect from the session.

```tsx
import { AgentDisconnectButton } from '@/components/agents-ui/agent-disconnect-button';

<AgentDisconnectButton className="bg-red-500 hover:bg-red-600" />
```

| Prop | Type | Description |
|------|------|-------------|
| `className` | `string` | Additional CSS classes |
| `onClick` | `() => void` | Optional click handler |

## StartAudioButton

Button to start audio playback (required by some browsers).

```tsx
import { StartAudioButton } from '@/components/agents-ui/start-audio-button';

<StartAudioButton label="Click to enable audio" />
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | - | Additional CSS classes |
| `label` | `string` | `"Start Audio"` | Button label |

## Local hooks (from Agents UI)

These hooks are installed with the Agents UI components via the shadcn CLI. They are copied to your project at `@/components/agents-ui/hooks/` and can be customized directly.

**These are NOT from the `@livekit/components-react` npm package.** For hooks from that package (like `useSession`, `useAgent`, `useVoiceAssistant`, `useTrackToggle`, `useChat`), see the **livekit-react-hooks** skill. Note that `useSession` from `@livekit/components-react` is required to use `AgentSessionProvider`.

### useAgentState

Get the current agent state.

```tsx
// Local hook from Agents UI (copied to your project)
import { useAgentState } from '@/components/agents-ui/hooks/use-agent-state';

function MyComponent() {
  const state = useAgentState();
  // state: "initializing" | "listening" | "thinking" | "speaking"
  
  return <div>Agent is {state}</div>;
}
```

### useAgentControlBar

Hook for building custom control bars.

```tsx
// Local hook from Agents UI (copied to your project)
import { useAgentControlBar } from '@/components/agents-ui/hooks/use-agent-control-bar';

function CustomControlBar() {
  const { isMuted, toggleMute, isConnected, disconnect } = useAgentControlBar();
  
  return (
    <div>
      <button onClick={toggleMute}>
        {isMuted ? 'Unmute' : 'Mute'}
      </button>
      <button onClick={disconnect}>
        Disconnect
      </button>
    </div>
  );
}
```

### useAgentAudioVisualizerBar

Hook for building custom audio visualizers.

```tsx
// Local hook from Agents UI (copied to your project)
import { useAgentAudioVisualizerBar } from '@/components/agents-ui/hooks/use-agent-audio-visualizer-bar';

function CustomVisualizer() {
  const { volumes, state } = useAgentAudioVisualizerBar({ barCount: 5 });
  
  return (
    <div className="flex gap-1">
      {volumes.map((volume, i) => (
        <div 
          key={i}
          className="w-2 bg-blue-500 transition-all"
          style={{ height: `${volume * 100}%` }}
        />
      ))}
    </div>
  );
}
```

## Complete example

```tsx
'use client';

import { useRef, useEffect } from 'react';
import { useSession } from '@livekit/components-react';
import { TokenSource, TokenSourceConfigurable } from 'livekit-client';
import { AgentSessionProvider } from '@/components/agents-ui/agent-session-provider';
import { AgentControlBar } from '@/components/agents-ui/agent-control-bar';
import { AgentAudioVisualizerRadial } from '@/components/agents-ui/agent-audio-visualizer-radial';
import { AgentChatTranscript } from '@/components/agents-ui/agent-chat-transcript';
import { AgentDisconnectButton } from '@/components/agents-ui/agent-disconnect-button';
import { StartAudioButton } from '@/components/agents-ui/start-audio-button';

export function VoiceAssistant() {
  // Use useRef to prevent recreating TokenSource on each render
  const tokenSource: TokenSourceConfigurable = useRef(
    TokenSource.endpoint('/api/token')
  ).current;

  // Create session using useSession hook (required)
  const session = useSession(tokenSource, {
    roomName: 'my-room',
    participantIdentity: 'user-123',
    agentName: 'my-agent',
  });

  // Start session when component mounts
  useEffect(() => {
    session.start();
    return () => session.end();
  }, []);

  return (
    <AgentSessionProvider session={session}>
      <div className="flex flex-col h-screen bg-slate-950 text-white">
        {/* Header */}
        <header className="flex justify-between items-center p-4 border-b border-slate-800">
          <h1 className="text-xl font-semibold">Voice Assistant</h1>
          <AgentDisconnectButton className="text-red-400 hover:text-red-300" />
        </header>
        
        {/* Main content */}
        <main className="flex-1 flex flex-col items-center justify-center gap-8 p-8">
          <AgentAudioVisualizerRadial className="w-48 h-48" />
          <AgentControlBar className="gap-4" />
          <StartAudioButton className="text-sm text-slate-400" />
        </main>
        
        {/* Chat transcript */}
        <aside className="h-64 border-t border-slate-800 p-4 overflow-y-auto">
          <AgentChatTranscript showTimestamps />
        </aside>
      </div>
    </AgentSessionProvider>
  );
}
```

## Installation reference

```bash
# All components
npx shadcn@latest add @agents-ui/agent-session-provider
npx shadcn@latest add @agents-ui/agent-control-bar
npx shadcn@latest add @agents-ui/agent-track-toggle
npx shadcn@latest add @agents-ui/agent-track-control
npx shadcn@latest add @agents-ui/agent-audio-visualizer-bar
npx shadcn@latest add @agents-ui/agent-audio-visualizer-grid
npx shadcn@latest add @agents-ui/agent-audio-visualizer-radial
npx shadcn@latest add @agents-ui/agent-audio-visualizer-wave
npx shadcn@latest add @agents-ui/agent-audio-visualizer-aura
npx shadcn@latest add @agents-ui/agent-chat-transcript
npx shadcn@latest add @agents-ui/agent-chat-indicator
npx shadcn@latest add @agents-ui/agent-disconnect-button
npx shadcn@latest add @agents-ui/start-audio-button
```
