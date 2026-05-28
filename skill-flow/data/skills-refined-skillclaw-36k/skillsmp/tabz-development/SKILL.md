---
name: tabz-development
description: "Patterns for building and debugging TabzChrome itself. Use when working on Terminal.tsx, xterm.js integration, WebSocket I/O, resize handling, or any TabzChrome extension/backend code."
---

# TabzChrome Development

Reference patterns for building TabzChrome's terminal implementation.

## Core Architecture

```
extension/components/Terminal.tsx  →  WebSocket  →  backend/modules/pty-handler.js
         ↓                                                    ↓
    xterm.js render                                      tmux session
```

## Key Files

| File | Purpose |
|------|---------|
| `extension/components/Terminal.tsx` | xterm.js terminal + resize |
| `extension/hooks/useTerminalSessions.ts` | Session lifecycle |
| `extension/background/websocket.ts` | WebSocket management |
| `backend/modules/pty-handler.js` | PTY spawning, tmux |

## Quick Patterns

### Terminal Initialization
```typescript
const term = new Terminal({ /* options */ });
const fitAddon = new FitAddon();
term.loadAddon(fitAddon);
term.open(containerRef.current);
fitAddon.fit();
```

### Resize Handling
```typescript
// Debounce resize, sync xterm → PTY
fitAddon.fit();
ws.send(JSON.stringify({ type: 'resize', cols: term.cols, rows: term.rows }));
```

### WebSocket I/O
```typescript
// Terminal → Backend
term.onData(data => ws.send(JSON.stringify({ type: 'input', data })));
// Backend → Terminal
ws.onmessage = (e) => term.write(JSON.parse(e.data).data);
```

## References

See `references/` for detailed patterns:
- `xterm-patterns.md` - Terminal setup, addons, options
- `resize-handling.md` - Debouncing, PTY sync
- `websocket-io.md` - Message protocol, reconnection
- `testing-checklist.md` - Manual test scenarios
