# Fullstack Example

This example demonstrates a typical fullstack application with frontend, backend, and shared code.

## Structure

```
fullstack-app/
├── client/                   # React frontend
│   └── .claude/
│       ├── config.json
│       └── context.md
├── server/                   # Express backend
│   └── .claude/
│       ├── config.json
│       └── context.md
├── shared/                   # Shared utilities and types
│   └── .claude/
│       ├── config.json
│       └── context.md
├── .workspace/
│   └── config.json
└── docker-compose.yml
```

## Workspace Configuration

See `.workspace/config.json` for the complete workspace setup.

## Usage with Claude

```
@workspace init fullstack-app
# Claude will detect client, server, and shared

@workspace analyze
# Shows tech stack and dependencies

@workspace task "Add user authentication"
# Claude coordinates changes across client, server, and shared
```

## Key Features

- **Type safety**: Shared TypeScript types between frontend and backend
- **API contract**: Shared validation schemas
- **Code reuse**: Utility functions used by both client and server
- **Consistent tooling**: Same linting and formatting rules

## Tech Stack

### Client
- React 18
- TypeScript
- Vite
- TailwindCSS
- React Query

### Server
- Node.js
- Express
- TypeScript
- PostgreSQL
- Prisma ORM

### Shared
- TypeScript
- Zod (validation)
- Utility functions

## Dependencies

```
client → shared, server (API calls)
server → shared
shared → (no internal deps)
```

## Development

```bash
# Install dependencies
npm install

# Start development servers
npm run dev
# Runs both client (port 3000) and server (port 3001)

# Run tests
npm test

# Build for production
npm run build
```

## API Communication

- Client calls server via REST API at `http://localhost:3001/api`
- Shared types ensure type safety across the boundary
- Shared validation schemas used on both sides
