# MyAgentive Architecture Reference

## Project Structure

```
MyAgentive/
├── server/                      # Backend (Bun runtime)
│   ├── index.ts                 # Entry point, bootstraps application
│   ├── config.ts                # Configuration loading, path resolution
│   ├── server.ts                # Express server + WebSocket upgrade
│   ├── setup-wizard.ts          # First-run interactive setup
│   ├── version.ts               # Version information
│   │
│   ├── core/
│   │   ├── ai-client.ts         # Claude Agent SDK integration
│   │   └── session-manager.ts   # Session orchestration
│   │
│   ├── db/
│   │   ├── database.ts          # SQLite with bun:sqlite, WAL mode
│   │   ├── migrations/          # Schema migrations (001-initial, etc.)
│   │   └── repositories/
│   │       ├── session-repo.ts  # Session CRUD operations
│   │       └── message-repo.ts  # Message CRUD operations
│   │
│   ├── telegram/
│   │   ├── bot.ts               # Grammy bot initialisation
│   │   ├── monitoring.ts        # Activity notifications to group
│   │   ├── subscription-manager.ts # Message streaming to Telegram
│   │   └── handlers/
│   │       ├── command-handler.ts  # /start, /help, /session, etc.
│   │       ├── message-handler.ts  # Text message processing
│   │       └── media-handler.ts    # Voice, audio, document, video, photo
│   │
│   ├── auth/
│   │   ├── middleware.ts        # Web authentication (password, token, API key)
│   │   └── telegram-auth.ts     # Telegram user ID verification
│   │
│   └── utils/
│       └── media-detector.ts    # Media file detection in messages
│
├── client/                      # React + Tailwind frontend
│   ├── src/
│   │   ├── App.tsx              # Main React component
│   │   ├── components/          # UI components
│   │   └── hooks/               # Custom React hooks
│   └── index.html               # Entry HTML
│
├── .claude/skills/              # Claude Code skills for development
├── package.json                 # Bun dependencies
└── tsconfig.json                # TypeScript configuration
```

## Core Components

### Entry Point: server/index.ts

Bootstraps the application:
1. Checks if `~/.myagentive/config` exists
2. Runs setup wizard if missing
3. Loads configuration into `process.env`
4. Changes cwd to config directory
5. Initialises database (runs migrations)
6. Starts Express server and Telegram bot
7. Handles graceful shutdown (SIGTERM, SIGINT)

### Configuration: server/config.ts

Loads and resolves configuration:
- Reads from `~/.myagentive/config`
- Resolves relative paths to absolute (relative to MYAGENTIVE_HOME)
- Exports `config` object with typed properties

Key config properties:
```typescript
{
  port: number;              // Server port (default 3847)
  webPassword: string;       // Web interface password
  apiKey: string;            // REST API key
  databasePath: string;      // SQLite database path
  mediaPath: string;         // Media storage path
  telegram: {
    botToken: string;
    userId: number;
    monitoringGroupId?: number;
    allowedGroups?: number[];
    responseTimeoutMinutes: number;
  }
}
```

### AI Client: server/core/ai-client.ts

Wraps Claude Agent SDK:
- **SYSTEM_PROMPT** (lines 31-64): Agent identity and capabilities
- **MessageQueue**: Async queue for multi-turn conversations
- **AgentSession**: Manages Claude SDK query() calls

Key exports:
```typescript
class AgentSession {
  constructor(options: AgentSessionOptions)
  sendMessage(content: string): void
  switchModel(model: 'opus' | 'sonnet' | 'haiku'): void
  stop(): Promise<void>
}
```

Query options passed to Claude SDK:
```typescript
{
  prompt: message,
  options: {
    maxTurns: 50,
    cwd: PROJECT_ROOT,           // For skill discovery
    allowedTools: ['Read', 'Write', 'Edit', ...],
  }
}
```

### Session Manager: server/core/session-manager.ts

Orchestrates all chat sessions:
- **ManagedSession**: Wrapper around AgentSession
- **SessionManager**: Singleton managing all sessions

Key functionality:
- Creates/retrieves sessions by name
- Manages WebSocket client subscriptions
- Routes messages between clients and AI
- Emits activity events for monitoring
- Persists messages to database

## Data Flow

```
User Message Flow:
─────────────────
1. User sends message via Telegram or Web
2. Handler receives message
3. SessionManager routes to ManagedSession
4. ManagedSession queues message to AgentSession
5. AgentSession calls Claude SDK query()
6. Response streams back through subscribers
7. Message persisted to SQLite

Response Streaming:
──────────────────
AgentSession → ManagedSession → SubscriptionManager → Clients
                                ├── TelegramSubscription → Telegram Chat
                                └── WebSocketSubscription → Browser
```

## Database Schema

### sessions
```sql
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  title TEXT,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  archived INTEGER DEFAULT 0
);
```

### messages
```sql
CREATE TABLE messages (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL,          -- 'user' | 'assistant'
  content TEXT NOT NULL,
  timestamp INTEGER NOT NULL,
  source TEXT,                 -- 'telegram' | 'web'
  metadata TEXT,               -- JSON
  FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

### auth_tokens
```sql
CREATE TABLE auth_tokens (
  id TEXT PRIMARY KEY,
  user_type TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL,
  last_used_at INTEGER
);
```

### media_files
```sql
CREATE TABLE media_files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  telegram_file_id TEXT,
  file_type TEXT NOT NULL,     -- 'voice' | 'audio' | 'document' | 'video' | 'photo'
  stored_path TEXT NOT NULL,
  original_filename TEXT,
  mime_type TEXT,
  file_size INTEGER,
  created_at INTEGER NOT NULL
);
```

### activity_log
```sql
CREATE TABLE activity_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT,
  activity_type TEXT NOT NULL,
  summary TEXT,
  details TEXT,
  created_at INTEGER NOT NULL
);
```

## Telegram Integration

### Bot Initialisation: server/telegram/bot.ts

Uses Grammy framework:
```typescript
const bot = new Bot(config.telegram.botToken);

// Middleware
bot.use(authMiddleware);     // Restrict to configured user

// Handlers
bot.command('start', ...);
bot.command('help', ...);
bot.on('message:text', messageHandler);
bot.on('message:voice', mediaHandler);
// etc.
```

### Media Handling: server/telegram/handlers/media-handler.ts

Processes uploaded media:
1. Downloads file from Telegram servers
2. Stores in `~/.myagentive/media/{type}/`
3. Records in `media_files` table
4. Sends system message to agent with file path
5. Agent can then process (e.g., transcribe voice)

### Activity Monitoring: server/telegram/monitoring.ts

Sends notifications to monitoring group:
- Session created/switched
- Messages sent/received
- Errors and warnings

## Web Interface

### Server: server/server.ts

Express routes:
- `GET /` - Serves React app
- `GET /api/health` - Health check
- `GET /api/sessions` - List sessions
- `POST /api/sessions` - Create session
- `GET /api/sessions/:id/messages` - Get messages
- `POST /api/auth/login` - Password login
- `GET /api/media/*` - Serve media files

WebSocket upgrade at `/ws`:
- Handles real-time chat
- Subscribes clients to sessions
- Streams AI responses

### Client: client/

React + Tailwind CSS:
- Session list sidebar
- Chat interface
- Message streaming display
- Authentication flow

## Path Resolution

The `resolvePath()` function in config.ts:

```typescript
function resolvePath(path: string): string {
  if (path.startsWith('/')) {
    return path;  // Absolute - use as-is
  }
  // Relative - resolve to MYAGENTIVE_HOME
  return join(MYAGENTIVE_HOME, path.replace(/^\.\//, ''));
}
```

Examples:
- `./data/db.sqlite` → `/Users/x/.myagentive/data/db.sqlite`
- `media` → `/Users/x/.myagentive/media`
- `/custom/path` → `/custom/path`

## Key Source File Locations

| Purpose | File |
|---------|------|
| System prompt | `server/core/ai-client.ts:31-64` |
| Config loading | `server/config.ts` |
| Setup wizard | `server/setup-wizard.ts` |
| Telegram commands | `server/telegram/handlers/command-handler.ts` |
| Message handling | `server/telegram/handlers/message-handler.ts` |
| Media download | `server/telegram/handlers/media-handler.ts` |
| Database init | `server/db/database.ts` |
| Web auth | `server/auth/middleware.ts` |
| Media detection | `server/utils/media-detector.ts` |
