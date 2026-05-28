# Architecture Diagram Patterns

ASCII diagrams for documenting feature architecture before implementation.

## Table of Contents

- [Layered Architecture](#layered-architecture)
- [Data Flow Diagrams](#data-flow-diagrams)
- [Sequence Diagrams](#sequence-diagrams)
- [Component Interaction Tables](#component-interaction-tables)

---

## Layered Architecture

### Three-Layer Pattern (ClaudeBar Standard)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FEATURE: [Feature Name]                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  EXTERNAL              INFRASTRUCTURE           DOMAIN               │
│  ┌─────────────┐       ┌─────────────────┐     ┌─────────────────┐  │
│  │  [Source]   │──────▶│  [Probe/Client] │────▶│  [Model]        │  │
│  │  (CLI/API)  │       │  (implements    │     │  (value types)  │  │
│  └─────────────┘       │   protocol)     │     └─────────────────┘  │
│                        └─────────────────┘             │             │
│                                                        ▼             │
│                                              ┌─────────────────┐     │
│                                              │  [Provider]     │     │
│                                              │  (AIProvider)   │     │
│                                              └─────────────────┘     │
│                                                       │              │
│                                                       ▼              │
│                        ┌───────────────────────────────────────┐    │
│                        │  APP LAYER                             │    │
│                        │  ┌─────────────────────────────────┐   │    │
│                        │  │  [Views/Registration]            │   │    │
│                        │  └─────────────────────────────────┘   │    │
│                        └───────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

### Full System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          ClaudeBar System                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                         Domain Layer                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │ │
│  │  │ UsageQuota   │  │ UsageSnapshot│  │ QuotaMonitor (actor)     │  │ │
│  │  │ QuotaStatus  │  │ AIProvider   │  │ QuotaAlerter             │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    ▲                                     │
│                                    │ implements                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      Infrastructure Layer                           │ │
│  │  ┌────────────────────────────────────────────────────────────┐    │ │
│  │  │                      CLI Probes                             │    │ │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │    │ │
│  │  │  │ Claude   │ │ Codex    │ │ Gemini   │ │ [NewProbe]   │   │    │ │
│  │  │  │ Probe    │ │ Probe    │ │ Probe    │ │              │   │    │ │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │    │ │
│  │  └────────────────────────────────────────────────────────────┘    │ │
│  │                                                                     │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │ │
│  │  │ CLIExecutor  │  │ NetworkClient│  │ NotificationAlerter      │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    ▲                                     │
│                                    │ uses                                │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                          App Layer                                  │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │ │
│  │  │ AppState     │  │ Views        │  │ ClaudeBarApp             │  │ │
│  │  │ (@Observable)│  │              │  │ (registration)           │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Probe Data Flow

```
┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
│  CLI/API  │────▶│  Probe    │────▶│  Parser   │────▶│ Snapshot  │
│  Output   │     │  Execute  │     │  Logic    │     │  Model    │
└───────────┘     └───────────┘     └───────────┘     └───────────┘
     Raw               Fetch            Parse            Domain
     Data              Data             Data             Model
```

### Refresh Cycle Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        REFRESH CYCLE                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Timer ──▶ QuotaMonitor ──▶ Provider.refresh() ──▶ Probe.probe()    │
│                │                                        │            │
│                │                                        ▼            │
│                │                              ┌─────────────────┐   │
│                │                              │ CLI/API Call    │   │
│                │                              └─────────────────┘   │
│                │                                        │            │
│                │                                        ▼            │
│                │                              ┌─────────────────┐   │
│                │                              │ Parse Response  │   │
│                │                              └─────────────────┘   │
│                │                                        │            │
│                ▼                                        ▼            │
│       ┌─────────────────┐                   ┌─────────────────┐     │
│       │ Notify Listener │◀──────────────────│ UsageSnapshot   │     │
│       │ (status change) │                   │ (returned)      │     │
│       └─────────────────┘                   └─────────────────┘     │
│                │                                                     │
│                ▼                                                     │
│       ┌─────────────────┐                                           │
│       │ Update UI/Alert │                                           │
│       └─────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────┘
```

### Error Handling Flow

```
┌─────────┐     ┌───────────┐     ┌─────────────┐     ┌──────────────┐
│  Probe  │────▶│ Try Fetch │────▶│   Success   │────▶│ Return Data  │
└─────────┘     └───────────┘     └─────────────┘     └──────────────┘
                      │
                      ▼ (failure)
               ┌─────────────┐     ┌─────────────────┐
               │ Catch Error │────▶│ Map to ProbeErr │
               └─────────────┘     └─────────────────┘
                                          │
                                          ▼
                                   ┌─────────────────┐
                                   │ Provider stores │
                                   │ lastError       │
                                   └─────────────────┘
```

---

## Sequence Diagrams

### User Clicks Refresh

```
User          AppState        QuotaMonitor        Provider          Probe
 │                │                 │                │                 │
 │──refresh()────▶│                 │                │                 │
 │                │──refreshAll()──▶│                │                 │
 │                │                 │──refresh()────▶│                 │
 │                │                 │                │──probe()───────▶│
 │                │                 │                │                 │
 │                │                 │                │◀──snapshot──────│
 │                │                 │◀──snapshot─────│                 │
 │                │                 │                │                 │
 │                │                 │──notify()─────▶│ (if changed)    │
 │◀───UI update───│                 │                │                 │
 │                │                 │                │                 │
```

### Status Change Notification

```
Probe           Provider        Monitor         Alerter           UI
  │                 │               │               │               │
  │──snapshot──────▶│               │               │               │
  │                 │──new status──▶│               │               │
  │                 │               │──compare()───▶│               │
  │                 │               │               │               │
  │                 │               │ (status degraded)             │
  │                 │               │──alert()─────▶│               │
  │                 │               │               │──notify user──│
  │                 │               │               │               │
  │                 │               │──update()────────────────────▶│
  │                 │               │               │               │
```

---

## Component Interaction Tables

### Standard Table Format

```
| Component        | Purpose                 | Inputs           | Outputs         | Dependencies      |
|------------------|-------------------------|------------------|-----------------|-------------------|
| NewUsageProbe    | Fetches usage from CLI  | CLI command      | UsageSnapshot   | CLIExecutor       |
| NewProvider      | Manages probe lifecycle | UsageProbe       | snapshot state  | UsageProbe        |
| ParsingLogic     | Converts raw to domain  | Raw CLI output   | UsageQuota[]    | None              |
```

### Extended Table (for complex features)

```
| Component        | Layer          | Protocol           | Creates/Modifies    | Test File                      |
|------------------|----------------|--------------------|---------------------|--------------------------------|
| NewUsageProbe    | Infrastructure | UsageProbe         | Creates             | NewUsageProbeTests.swift       |
| NewUsageProbe    | Infrastructure | -                  | Parsing (internal)  | NewUsageProbeParsingTests.swift|
| NewProvider      | Domain         | AIProvider         | Creates             | (integration only)             |
| ProviderRegistry | App            | -                  | Modifies            | -                              |
```

### Files to Create/Modify Table

```
| File Path                                    | Action   | Description                          |
|----------------------------------------------|----------|--------------------------------------|
| Sources/Infrastructure/CLI/NewProbe.swift    | Create   | Implements UsageProbe protocol       |
| Sources/Domain/Provider/NewProvider.swift    | Create   | Implements AIProvider protocol       |
| Tests/InfrastructureTests/NewProbeTests.swift| Create   | Probe behavior tests with mocks      |
| Sources/App/ClaudeBarApp.swift               | Modify   | Register new provider                |
```

---

## Approval Prompt Template

After presenting the architecture, ask for user approval:

```
## Architecture Review

I've designed the architecture for [Feature Name]:

[Diagram Here]

### Components Summary

| Component | Purpose |
|-----------|---------|
| [Name]    | [Desc]  |

### Files to Create/Modify

- `Sources/.../NewFile.swift` - [Description]
- `Tests/.../NewTests.swift` - [Description]

**Ready to proceed with TDD implementation?**
```

Use AskUserQuestion with:
- "Approve - proceed with implementation"
- "Modify - I have feedback on the design"