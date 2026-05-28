# ASCII Pattern Library

## Box Diagrams

### Single Component

```
┌─────────────────┐
│  Component A    │
│  (description)  │
└─────────────────┘
```

### Vertical Flow

```
┌─────────────────┐
│  Component A    │
│  (description)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Component B    │
└─────────────────┘
```

### Horizontal Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Input  │────▶│ Process │────▶│ Output  │
└─────────┘     └─────────┘     └─────────┘
```

### Bidirectional

```
┌─────────┐           ┌─────────┐
│ Client  │◀─────────▶│ Server  │
└─────────┘           └─────────┘
```

## File Trees

```
project/
├── src/
│   ├── components/
│   │   ├── Button.tsx
│   │   └── Input.tsx
│   ├── utils/
│   │   └── helpers.ts
│   └── index.ts
├── tests/
│   └── unit/
└── package.json
```

Tree characters: `├──`, `└──`, `│`

## Decision Flows

### Simple Branch

```
     ┌──────────────┐
     │   Request    │
     └──────┬───────┘
            │
     ┌──────▼───────┐
     │ Authorized?  │
     └──────┬───────┘
       yes / \ no
          /   \
┌────────▼┐   ┌▼────────┐
│ Process │   │  Error  │
└─────────┘   └─────────┘
```

### Multi-Branch

```
          ┌─────────┐
          │  Input  │
          └────┬────┘
               │
        ┌──────▼──────┐
        │    Type?    │
        └──────┬──────┘
     ┌─────────┼─────────┐
     │         │         │
┌────▼───┐ ┌───▼───┐ ┌───▼────┐
│  Text  │ │ Number│ │  Date  │
└────────┘ └───────┘ └────────┘
```

## Sequence Diagrams

### Vertical Timeline

```
Client          API            Database
  │               │                │
  │──── GET ─────▶│                │
  │               │──── SELECT ───▶│
  │               │◀─── rows ──────│
  │◀─── JSON ─────│                │
  │               │                │
```

### With Notes

```
Client              Server
  │                    │
  │── authenticate ───▶│
  │                    │ validate
  │◀──── token ────────│
  │                    │
  │── request + token ▶│
  │                    │ process
  │◀──── response ─────│
  │                    │
```

## Comparison Tables

### Side-by-Side

```
┌────────────────────────────────────────┐
│  Option A          │  Option B         │
├────────────────────┼───────────────────┤
│  Fast startup      │  Slow startup     │
│  Limited features  │  Full features    │
│  Low memory        │  High memory      │
└────────────────────┴───────────────────┘
```

### With Metrics

```
┌──────────────────────────────────────┐
│  Metric      │  Before  │  After    │
├──────────────┼──────────┼───────────┤
│  Build time  │  8.5s    │  4.2s     │
│  Bundle size │  2.1MB   │  890KB    │
│  Test count  │  45      │  127      │
└──────────────┴──────────┴───────────┘
```

## Layered Architecture

### Horizontal Layers

```
┌─────────────────────────────────────────┐
│              Presentation               │
├─────────────────────────────────────────┤
│              Application                │
├─────────────────────────────────────────┤
│                Domain                   │
├─────────────────────────────────────────┤
│             Infrastructure              │
└─────────────────────────────────────────┘
```

### With Components

```
┌─────────────────────────────────────────┐
│  UI Layer                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │  React   │ │  Redux   │ │  Router  │ │
│  └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────┤
│  API Layer                              │
│  ┌──────────┐ ┌──────────┐              │
│  │   tRPC   │ │   REST   │              │
│  └──────────┘ └──────────┘              │
├─────────────────────────────────────────┤
│  Data Layer                             │
│  ┌──────────┐ ┌──────────┐              │
│  │  Prisma  │ │  Redis   │              │
│  └──────────┘ └──────────┘              │
└─────────────────────────────────────────┘
```

## State Machines

```
         ┌───────────────────────────────────────┐
         │                                       │
         ▼                                       │
┌─────────────┐    submit    ┌─────────────┐    │
│    Draft    │─────────────▶│   Review    │    │
└─────────────┘              └──────┬──────┘    │
                                    │           │
                          approve / │ \ reject  │
                                 /  │  \        │
                    ┌───────────▼┐  │  └────────┘
                    │  Approved  │  │
                    └──────┬─────┘  │
                           │        │
                    publish│        │
                           ▼        │
                    ┌───────────┐   │
                    │ Published │   │
                    └───────────┘   │
```

## Box-Drawing Characters

### Lines and Corners

```
Single line:  ┌─┬─┐  │  ├─┼─┤  └─┴─┘
Double line:  ╔═╦═╗  ║  ╠═╬═╣  ╚═╩═╝
Rounded:      ╭───╮  │  ╰───╯
```

### Arrows

```
Vertical:     ▲  ▼
Horizontal:   ◀  ▶

With lines:   ─▶  ◀─  ───▶  ◀───
              │
              ▼

Corners:      └─▶  ┌─▶  ──┐  ──┘
                        │     │
                        ▼     ▼
```

### T-Junctions

```
├──   ──┤   ┬   ┴
         │   │
```

## Tips

* Use single-line box characters (`┌─┐`) for most diagrams
* Reserve double-line (`╔═╗`) for emphasis or outer boundaries
* Keep consistent spacing inside boxes (2 spaces padding)
* Align vertical lines across the diagram
* Use `▶` for directional arrows, `─` for connections
