# Diagram Patterns

Mermaid diagram examples for common code investigation scenarios.

## Table of Contents
- [When to Use Each Diagram Type](#when-to-use-each-diagram-type)
- [Sequence Diagrams (Process Flow)](#sequence-diagrams-process-flow)
- [Flowcharts (Module Dependencies)](#flowcharts-module-dependencies)
- [State Diagrams (State Transitions)](#state-diagrams-state-transitions)
- [Class Diagrams (Rare Use)](#class-diagrams-rare-use)

## When to Use Each Diagram Type

| Scenario | Diagram Type | Reason |
|----------|--------------|--------|
| API request → response flow | `sequenceDiagram` | Shows temporal order and message passing |
| Data transformation pipeline | `sequenceDiagram` | Shows step-by-step processing |
| Module import/dependency structure | `flowchart LR` | Shows static relationships |
| Component composition | `flowchart TD` | Shows parent-child hierarchy |
| State machine (player, form, etc.) | `stateDiagram-v2` | Shows state transitions and triggers |
| Lifecycle (mount → update → unmount) | `stateDiagram-v2` | Shows state progression over time |

## Sequence Diagrams (Process Flow)

Use for: API calls, event handlers, data flow through functions/services

### Example 1: Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as routes/login.tsx::LoginForm
    participant API as routes/api.auth.callback.ts::action
    participant Auth as auth.ts::authenticator
    participant OAuth as GitHub OAuth
    
    User->>UI: Submit credentials
    UI->>API: POST with formData
    API->>Auth: authenticate('github', request)
    Auth->>OAuth: OAuth flow
    OAuth-->>Auth: user data
    Auth-->>API: user object
    API->>API: createUserSession()
    API-->>UI: redirect('/dashboard')
    UI-->>User: Show dashboard
```

**Key points:**
- Participants use `File::Symbol` format
- Use `-->>` for responses/returns
- Use `Note` for important details

### Example 2: Data Sync Flow

```mermaid
sequenceDiagram
    participant UI as components/PlaylistSync.tsx
    participant Hook as hooks/use-playlist-sync.ts
    participant API as routes/api.playlists.sync.ts
    participant Resolver as lib/conflict-resolver.ts
    participant DB as Database
    
    UI->>Hook: trigger sync
    Hook->>API: POST /api/playlists/sync
    API->>DB: load server data
    DB-->>API: serverPlaylists
    API->>Resolver: resolveConflicts(client, server)
    
    alt No conflicts
        Resolver-->>API: merged data
    else Conflicts found
        Resolver-->>API: conflict list
        API-->>UI: show conflict modal
        UI->>User: Choose resolution
        User-->>UI: selection
        UI->>API: POST with resolution
    end
    
    API->>DB: save merged data
    API-->>Hook: sync result
    Hook-->>UI: update state
```

**Key points:**
- Use `alt/else` for conditional logic
- Show error/conflict paths
- Keep happy path prominent

## Flowcharts (Module Dependencies)

Use for: Import relationships, data structure flow, component hierarchy

### Example 1: Module Dependency Chain

```mermaid
flowchart LR
    A[routes/_app.tsx] -->|imports| B[stores/player.ts]
    A -->|imports| C[hooks/use-youtube-player.ts]
    B -->|imports| D[lib/player/service.ts]
    C -->|imports| D
    D -->|imports| E[lib/player/youtube-api.ts]
    
    style A fill:#e1f5ff
    style E fill:#ffe1e1
```

**Key points:**
- Use `LR` (left-right) for dependency chains
- Use `TD` (top-down) for hierarchies
- Color entry points and external deps differently

### Example 2: Data Transformation Pipeline

```mermaid
flowchart TD
    A[Raw Form Data] -->|validate| B[lib/validator.ts]
    B -->|pass| C[lib/normalizer.ts]
    B -->|fail| D[Error Toast]
    C -->|transform| E[API Payload]
    E -->|POST| F[routes/api.submit.ts]
    F -->|success| G[Success Page]
    F -->|error| D
```

**Key points:**
- Label edges with action verbs
- Show both success and error paths
- Use `TD` for vertical flow

### Example 3: Component Composition

```mermaid
flowchart TD
    A[routes/_app.tsx] --> B[components/Header.tsx]
    A --> C[components/Player.tsx]
    A --> D[components/Playlist.tsx]
    
    C --> C1[components/ui/button.tsx]
    C --> C2[components/ui/slider.tsx]
    
    D --> D1[components/PlaylistItem.tsx]
    D1 --> D2[components/ui/card.tsx]
    
    style A fill:#e1f5ff
```

**Key points:**
- Shows parent-child component structure
- Helps understand render tree
- Useful for prop-drilling investigation

## State Diagrams (State Transitions)

Use for: State machines, lifecycle, status workflows

### Example 1: Player State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle
    
    Idle --> Loading: loadVideo()
    Loading --> Ready: onReady()
    Loading --> Error: onError()
    
    Ready --> Playing: play()
    Playing --> Paused: pause()
    Paused --> Playing: play()
    
    Playing --> Ended: onEnded()
    Ended --> Playing: replay()
    Ended --> Idle: stop()
    
    Error --> Idle: reset()
    
    note right of Playing
        Auto-save triggers
        every 5 seconds
    end note
```

**Key points:**
- Show all possible transitions
- Label transitions with trigger methods/events
- Use notes for side effects

### Example 2: Form Validation Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pristine
    
    Pristine --> Touched: user input
    Touched --> Validating: onBlur()
    
    Validating --> Valid: rules pass
    Validating --> Invalid: rules fail
    
    Valid --> Submitting: submit()
    Invalid --> Touched: user edit
    
    Submitting --> Success: API 200
    Submitting --> Failed: API error
    
    Success --> [*]
    Failed --> Touched: retry
```

**Key points:**
- Shows form lifecycle clearly
- Includes validation and submission states
- Shows retry paths

### Example 3: Data Sync Status

```mermaid
stateDiagram-v2
    [*] --> LocalOnly
    
    LocalOnly --> Syncing: trigger sync
    Syncing --> Synced: success
    Syncing --> Conflict: conflicts detected
    Syncing --> Failed: network error
    
    Conflict --> ConflictResolution: show modal
    ConflictResolution --> Syncing: user resolves
    ConflictResolution --> LocalOnly: user cancels
    
    Failed --> LocalOnly: dismiss
    Synced --> LocalOnly: edit locally
    
    note right of Conflict
        User must choose
        client or server version
    end note
```

## Class Diagrams (Rare Use)

⚠️ **Use sparingly** - Only for complex OOP class hierarchies. Most modern code uses functional patterns where class diagrams add little value.

### Example: When class diagram is useful

```mermaid
classDiagram
    class BasePlayer {
        +state: PlayerState
        +play()
        +pause()
        +stop()
    }
    
    class YouTubePlayer {
        +apiKey: string
        +loadVideo(id: string)
        +onReady()
    }
    
    class VimeoPlayer {
        +embedUrl: string
        +loadVideo(id: string)
        +onReady()
    }
    
    BasePlayer <|-- YouTubePlayer
    BasePlayer <|-- VimeoPlayer
    
    class PlayerFactory {
        +createPlayer(type: string): BasePlayer
    }
    
    PlayerFactory --> BasePlayer
```

**When to use:**
- Clear inheritance hierarchies
- Factory/strategy patterns
- Interface implementations

**When NOT to use:**
- Functional components (use flowchart instead)
- Simple object structures (describe in text)
- Module systems (use flowchart instead)

## Diagram Best Practices

### Keep It Minimal
❌ **Too detailed:**
```mermaid
sequenceDiagram
    participant A as File1.ts::funcA
    participant B as File1.ts::funcB
    participant C as File1.ts::funcC
    participant D as File2.ts::funcD
    participant E as File2.ts::funcE
    participant F as File3.ts::funcF
    A->>B: step1
    B->>C: step2
    C->>D: step3
    D->>E: step4
    E->>F: step5
```

✅ **Focused on key path:**
```mermaid
sequenceDiagram
    participant Entry as File1.ts::funcA
    participant Process as File2.ts::funcD
    participant Store as File3.ts::funcF
    
    Entry->>Process: process data
    Process->>Store: save result
```

### Use Descriptive Participant Names

❌ **Bad:**
```mermaid
sequenceDiagram
    participant A
    participant B
    participant C
```

✅ **Good:**
```mermaid
sequenceDiagram
    participant UI as routes/login.tsx::LoginForm
    participant API as routes/api.auth.ts::action
    participant DB as Database
```

### Show Error Paths When Relevant

```mermaid
sequenceDiagram
    participant UI
    participant API
    participant DB
    
    UI->>API: submit data
    API->>DB: save
    
    alt Success
        DB-->>API: saved
        API-->>UI: 200 OK
    else Database error
        DB-->>API: error
        API-->>UI: 500 Error
        UI->>UI: show error toast
    else Validation error
        API-->>UI: 400 Bad Request
        UI->>UI: highlight fields
    end
```

## Quick Reference: Diagram Type Selection

```mermaid
flowchart TD
    Start{What are you showing?}
    Start -->|Time-based flow| Time{Multiple participants?}
    Start -->|Static structure| Static{What kind?}
    Start -->|State changes| State[stateDiagram-v2]
    
    Time -->|Yes| Seq[sequenceDiagram]
    Time -->|No| Flow[flowchart TD]
    
    Static -->|Dependencies| Dep[flowchart LR]
    Static -->|Hierarchy| Hier[flowchart TD]
    Static -->|Classes| Class[classDiagram]
```
