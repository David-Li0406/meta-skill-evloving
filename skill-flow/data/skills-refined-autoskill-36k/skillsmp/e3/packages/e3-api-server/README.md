# @elaraai/e3-api-server

HTTP server for e3 repositories.

## Installation

```bash
npm install @elaraai/e3-api-server
```

## Overview

REST API server exposing e3-core operations over HTTP. Uses BEAST2 binary serialization for efficient request/response encoding.

Supports two modes:
- **Single-repo mode**: Serve one repository, accessed via `/repos/default`
- **Multi-repo mode**: Serve multiple repositories from a directory, accessed via `/repos/:name`

## CLI Usage

```bash
# Single repository mode
e3-api-server --repo /path/to/repo
e3-api-server --repo /path/to/repo --port 8080 --cors

# Multi-repository mode (serves repos from subdirectories)
e3-api-server --repos /path/to/repos-dir

# With OIDC authentication
e3-api-server --repo /path/to/repo --oidc

# Custom port and host
e3-api-server --repo /path/to/repo --port 8080 --host 0.0.0.0
```

### CLI Options

| Option | Description |
|--------|-------------|
| `--repo <path>` | Single repository mode - serve one repo at `/repos/default` |
| `--repos <dir>` | Multi-repo mode - serve repos from subdirectories |
| `-p, --port <port>` | HTTP port (default: 3000) |
| `-H, --host <host>` | Bind address (default: localhost) |
| `--cors` | Enable CORS for cross-origin requests |
| `--oidc` | Enable built-in OIDC authentication provider |
| `--token-expiry <duration>` | Access token expiry, e.g., "5s", "15m", "1h" (default: 1h) |
| `--refresh-token-expiry <duration>` | Refresh token expiry, e.g., "7d", "90d" (default: 90d) |

## Programmatic Usage

### Single Repository (Embedded Server)

For embedding in applications like VS Code extensions:

```typescript
import { createServer } from '@elaraai/e3-api-server';

// createServer is async
const server = await createServer({
  singleRepoPath: '/path/to/repo',
  port: 3000,
  host: 'localhost',
  cors: true,  // Enable for webview/cross-origin access
});

await server.start();
console.log(`Server listening on http://localhost:${server.port}`);
console.log('Access repository via: /repos/default');

// Graceful shutdown
await server.stop();
```

### Multi-Repository Mode

For serving multiple repositories:

```typescript
import { createServer } from '@elaraai/e3-api-server';

const server = await createServer({
  reposDir: '/path/to/repos',  // Each subdirectory is a repo
  port: 3000,
  host: 'localhost',
});

await server.start();
// Repos accessible at /repos/repo1, /repos/repo2, etc.
```

### With Authentication

```typescript
import { createServer } from '@elaraai/e3-api-server';

const server = await createServer({
  singleRepoPath: '/path/to/repo',
  port: 3000,
  oidc: {
    baseUrl: 'http://localhost:3000',
    tokenExpiry: '1h',
    refreshTokenExpiry: '90d',
  },
});

await server.start();
// OIDC endpoints available at /.well-known/*, /oauth2/*, /device
```

### ServerConfig Options

```typescript
interface ServerConfig {
  // Repository mode (specify exactly one)
  singleRepoPath?: string;  // Single repo at /repos/default
  reposDir?: string;        // Multi-repo from subdirectories

  // Server options
  port?: number;            // Default: 3000
  host?: string;            // Default: 'localhost'
  cors?: boolean;           // Enable CORS (default: false)

  // Authentication (optional)
  auth?: AuthConfig;        // External JWT validation
  oidc?: OidcConfig;        // Built-in OIDC provider
}
```

## API Endpoints

All endpoints are prefixed with `/api/repos/:repo` where `:repo` is:
- `default` in single-repo mode
- The repository name in multi-repo mode

### Repository

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/repos` | List available repositories (multi-repo mode) |
| PUT | `/api/repos/:repo` | Create repository (multi-repo mode) |
| DELETE | `/api/repos/:repo` | Delete repository (multi-repo mode, async) |
| GET | `/api/repos/:repo/status` | Repository status (counts) |
| POST | `/api/repos/:repo/gc` | Start garbage collection (async) |
| GET | `/api/repos/:repo/gc/:id` | Get GC status |

### Packages

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/repos/:repo/packages` | List all packages |
| GET | `/api/repos/:repo/packages/:name/:version` | Get package details |
| POST | `/api/repos/:repo/packages` | Import package (zip body) |
| GET | `/api/repos/:repo/packages/:name/:version/export` | Export package as zip |
| DELETE | `/api/repos/:repo/packages/:name/:version` | Remove package |

### Workspaces

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/repos/:repo/workspaces` | List all workspaces |
| POST | `/api/repos/:repo/workspaces` | Create workspace |
| GET | `/api/repos/:repo/workspaces/:ws` | Get workspace info |
| GET | `/api/repos/:repo/workspaces/:ws/status` | Get workspace status (datasets, tasks, summary) |
| POST | `/api/repos/:repo/workspaces/:ws/deploy` | Deploy package to workspace |
| DELETE | `/api/repos/:repo/workspaces/:ws` | Remove workspace |
| GET | `/api/repos/:repo/workspaces/:ws/export` | Export workspace as package zip |

### Datasets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/repos/:repo/workspaces/:ws/datasets` | List root datasets |
| GET | `/api/repos/:repo/workspaces/:ws/datasets/*path` | Get dataset value (BEAST2) |
| PUT | `/api/repos/:repo/workspaces/:ws/datasets/*path` | Set dataset value (BEAST2) |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/repos/:repo/workspaces/:ws/tasks` | List tasks |
| GET | `/api/repos/:repo/workspaces/:ws/tasks/:task` | Get task details |

### Execution

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/repos/:repo/workspaces/:ws/dataflow/start` | Start dataflow (async, returns immediately) |
| POST | `/api/repos/:repo/workspaces/:ws/dataflow/execute` | Execute dataflow (blocking, returns result) |
| GET | `/api/repos/:repo/workspaces/:ws/dataflow/graph` | Get dependency graph |
| GET | `/api/repos/:repo/workspaces/:ws/dataflow/logs/:task` | Read task logs |
| GET | `/api/repos/:repo/workspaces/:ws/dataflow/state` | Get current execution state |

## Request/Response Format

All requests and responses use BEAST2 binary encoding with `Content-Type: application/beast2`.

Response bodies are wrapped in a variant type:
- `{ type: 'success', value: <result> }` - Operation succeeded
- `{ type: 'error', value: <error> }` - Operation failed

Error variants include:
- `workspace_not_found` - Workspace doesn't exist
- `workspace_not_deployed` - No package deployed to workspace
- `workspace_locked` - Workspace is locked by another process
- `package_not_found` - Package doesn't exist
- `package_exists` - Package already exists
- `dataset_not_found` - Dataset path doesn't exist
- `task_not_found` - Task doesn't exist
- `internal` - Internal server error

## Using with e3-api-client

```typescript
import { workspaceList, workspaceStatus, datasetGet } from '@elaraai/e3-api-client';

const baseUrl = 'http://localhost:3000';
const repo = 'default';  // In single-repo mode
const options = { token: '' };  // Empty token if no auth configured

// List workspaces
const workspaces = await workspaceList(baseUrl, repo, options);

// Get workspace status
const status = await workspaceStatus(baseUrl, repo, 'my-workspace', options);

// Get dataset value
const path = [{ value: 'inputs' }, { value: 'data' }];
const data = await datasetGet(baseUrl, repo, 'my-workspace', path, options);
```

## License

BSL 1.1. See [LICENSE.md](./LICENSE.md).

### Ecosystem

- **[East Node](https://github.com/elaraai/east-node)**: Node.js platform functions for I/O, databases, and system operations. Connect East programs to filesystems, SQL/NoSQL databases, cloud storage, and network services.
  - [@elaraai/east-node-std](https://www.npmjs.com/package/@elaraai/east-node-std): Filesystem, console, HTTP fetch, crypto, random distributions, timestamps
  - [@elaraai/east-node-io](https://www.npmjs.com/package/@elaraai/east-node-io): SQLite, PostgreSQL, MySQL, MongoDB, S3, FTP, SFTP
  - [@elaraai/east-node-cli](https://www.npmjs.com/package/@elaraai/east-node-cli): CLI for running East IR programs in Node.js

- **[East Python](https://github.com/elaraai/east-py)**: Python runtime and platform functions for data science and machine learning. Execute East programs with access to optimization solvers, gradient boosting, neural networks, and model explainability.
  - [@elaraai/east-py-datascience](https://www.npmjs.com/package/@elaraai/east-py-datascience): TypeScript types for optimization, gradient boosting, neural networks, explainability

- **[East UI](https://github.com/elaraai/east-ui)**: East types and expressions for building dashboards and interactive layouts. Define UIs as data structures that render consistently across React, web, and other environments.
  - [@elaraai/east-ui](https://www.npmjs.com/package/@elaraai/east-ui): 50+ typed UI components for layouts, forms, charts, tables, dialogs
  - [@elaraai/east-ui-components](https://www.npmjs.com/package/@elaraai/east-ui-components): React renderer with Chakra UI styling

- **[e3 - East Execution Engine](https://github.com/elaraai/e3)**: Durable execution engine for running East pipelines at scale. Features Git-like content-addressable storage, automatic memoization, task queuing, and real-time monitoring.
  - [@elaraai/e3](https://www.npmjs.com/package/@elaraai/e3): SDK for authoring e3 packages with typed tasks and pipelines
  - [@elaraai/e3-core](https://www.npmjs.com/package/@elaraai/e3-core): Git-like object store, task queue, result caching
  - [@elaraai/e3-types](https://www.npmjs.com/package/@elaraai/e3-types): Shared type definitions for e3 packages
  - [@elaraai/e3-cli](https://www.npmjs.com/package/@elaraai/e3-cli): `e3 init`, `e3 run`, `e3 logs` commands for managing and monitoring tasks
  - [@elaraai/e3-api-client](https://www.npmjs.com/package/@elaraai/e3-api-client): HTTP client for remote e3 servers
  - [@elaraai/e3-api-server](https://www.npmjs.com/package/@elaraai/e3-api-server): REST API server for e3 repositories

## Links

- [East Language](https://github.com/elaraai/east)
- [East Python Runtime](https://github.com/elaraai/east-py)
- [Elara AI](https://elaraai.com/)
- [Issues](https://github.com/elaraai/e3/issues)
- support@elara.ai

## About Elara

East is developed by [Elara AI Pty Ltd](https://elaraai.com/), an AI-powered platform that creates economic digital twins of businesses that optimize performance. Elara combines business objectives, decisions and data to help organizations make data-driven decisions across operations, purchasing, sales and customer engagement, and project and investment planning. East powers the computational layer of Elara solutions, enabling the expression of complex business logic and data in a simple, type-safe and portable language.

---

*Developed by [Elara AI Pty Ltd](https://elaraai.com/)*
