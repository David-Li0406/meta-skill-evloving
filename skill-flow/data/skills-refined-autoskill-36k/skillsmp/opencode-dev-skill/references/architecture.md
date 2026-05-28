# OpenCode Architecture

## Project Structure

```
opencode/
├── packages/
│   ├── opencode/          # Core package - main business logic
│   │   ├── src/
│   │   │   ├── cli/       # CLI commands
│   │   │   │   └── cmd/tui/  # Terminal UI (SolidJS + opentui)
│   │   │   ├── server/    # HTTP server implementation
│   │   │   ├── session/   # Session management, messages, LLM
│   │   │   ├── tool/      # Built-in tools (bash, edit, read, etc.)
│   │   │   ├── provider/  # LLM provider integrations
│   │   │   ├── config/    # Configuration handling
│   │   │   ├── file/      # File operations, ripgrep
│   │   │   ├── skill/     # Agent skills system
│   │   │   ├── permission/# Permission management
│   │   │   └── ...
│   │   └── script/        # Build scripts
│   │
│   ├── sdk/js/            # JavaScript/TypeScript SDK
│   │   ├── src/
│   │   │   ├── index.ts   # Main exports
│   │   │   ├── client.ts  # Client creation
│   │   │   ├── server.ts  # Server spawning
│   │   │   └── gen/       # Auto-generated types & SDK
│   │   └── example/       # Usage examples
│   │
│   ├── app/               # Shared web UI components (SolidJS)
│   ├── desktop/           # Native desktop app (Tauri)
│   ├── web/               # Documentation website
│   ├── plugin/            # @opencode-ai/plugin package
│   └── ...
│
├── sdks/                  # SDKs for other languages
│   └── python/
│
└── script/                # Monorepo scripts
```

## Key Source Files

### Server (`packages/opencode/src/server/`)
- `server.ts` - Main HTTP server, route definitions
- `tui.ts` - TUI control endpoints
- `project.ts` - Project management
- `error.ts` - Error handling

### Session (`packages/opencode/src/session/`)
- `index.ts` - Session management
- `message.ts` - Message types and schemas (Zod)
- `prompt.ts` - Prompt processing
- `llm.ts` - LLM interaction
- `status.ts` - Session status tracking
- `todo.ts` - Todo list management

### Tools (`packages/opencode/src/tool/`)
Built-in tools available to the agent:
- `bash.ts` - Shell command execution
- `read.ts` - File reading
- `write.ts` - File writing
- `edit.ts` - File editing
- `glob.ts` - File pattern matching
- `grep.ts` - Content search
- `task.ts` - Subagent spawning
- `webfetch.ts` - URL fetching
- `todo.ts` - Todo management

### SDK (`packages/sdk/js/src/`)
- `index.ts` - Main entry, `createOpencode()`
- `client.ts` - `createOpencodeClient()`
- `server.ts` - `createOpencodeServer()`, `createOpencodeTui()`
- `gen/types.gen.ts` - All TypeScript types
- `gen/sdk.gen.ts` - Generated API client

## Development Setup

```bash
# Requirements: Bun 1.3+
bun install
bun dev              # Start dev server
bun dev <directory>  # Run against specific directory
bun dev .            # Run against repo root
```

### Building Standalone Binary
```bash
./packages/opencode/script/build.ts --single
./packages/opencode/dist/opencode-<platform>/bin/opencode
```

### Running Web UI
```bash
bun run --cwd packages/app dev
# Opens http://localhost:5173
```

### Regenerating SDK
After modifying `packages/opencode/src/server/server.ts`:
```bash
./script/generate.ts
```

## Style Guide

- **Functions**: Keep logic in single functions unless reuse benefits
- **Control flow**: Avoid `else` statements
- **Error handling**: Prefer `.catch(...)` over try/catch
- **Types**: Precise types, avoid `any`
- **Variables**: Immutable patterns, avoid `let`
- **Naming**: Concise single-word identifiers
- **Runtime**: Use Bun helpers like `Bun.file()`

## Client/Server Architecture

```
┌─────────────┐     HTTP/SSE      ┌─────────────┐
│   Client    │◄──────────────────│   Server    │
│  (TUI/Web)  │                   │  (opencode) │
└─────────────┘                   └─────────────┘
                                        │
                                        ▼
                                  ┌─────────────┐
                                  │ LLM Provider│
                                  │  (Claude)   │
                                  └─────────────┘
```

The TUI/Web clients connect to the server via HTTP. The server:
1. Exposes REST API for session/message management
2. Streams events via SSE (`/event` endpoint)
3. Communicates with LLM providers
4. Executes tools in the local environment
