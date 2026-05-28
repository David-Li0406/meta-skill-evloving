# @elaraai/e3-api-client

TypeScript client library for e3 API servers.

## Installation

```bash
npm install @elaraai/e3-api-client
```

## Overview

Stateless functions for interacting with an e3 API server. Uses BEAST2 binary serialization for efficient request/response encoding.

## API

### Repository

```typescript
import { repoStatus, repoGc } from '@elaraai/e3-api-client';

const status = await repoStatus('http://localhost:3000');
// { path: '/path/to/repo', objectCount: 42n, packageCount: 3n, workspaceCount: 2n }

const gcResult = await repoGc(url, { dryRun: true, minAge: variant('none', null) });
// { deletedObjects: 0n, retainedObjects: 42n, bytesFreed: 0n, ... }
```

### Packages

```typescript
import { packageList, packageImport, packageGet, packageExport, packageRemove } from '@elaraai/e3-api-client';

// List all packages
const packages = await packageList(url);
// [{ name: 'my-pkg', version: '1.0.0' }, ...]

// Import a package from zip bytes
const result = await packageImport(url, zipBytes);
// { name: 'my-pkg', version: '1.0.0', packageHash: 'abc123...', objectCount: 5n }

// Get package object
const pkg = await packageGet(url, 'my-pkg', '1.0.0');

// Export package as zip
const zip = await packageExport(url, 'my-pkg', '1.0.0');

// Remove package
await packageRemove(url, 'my-pkg', '1.0.0');
```

### Workspaces

```typescript
import { workspaceList, workspaceCreate, workspaceGet, workspaceStatus, workspaceDeploy, workspaceRemove } from '@elaraai/e3-api-client';

// Create workspace
const info = await workspaceCreate(url, 'production');
// { name: 'production', deployed: false, packageName: null, packageVersion: null }

// Deploy package to workspace
await workspaceDeploy(url, 'production', 'my-pkg@1.0.0');

// Get workspace status
const status = await workspaceStatus(url, 'production');
// { workspace: 'production', datasets: [...], tasks: [...], summary: { ... } }

// List workspaces
const workspaces = await workspaceList(url);
```

### Datasets

```typescript
import { datasetList, datasetListAt, datasetGet, datasetSet } from '@elaraai/e3-api-client';
import { encodeBeast2For, decodeBeast2For, StringType, variant } from '@elaraai/east';

// List root fields
const fields = await datasetList(url, 'production');
// ['inputs', 'tasks']

// List nested fields
const inputFields = await datasetListAt(url, 'production', [variant('field', 'inputs')]);
// ['config', 'data']

// Get dataset value (raw BEAST2 bytes)
const path = [variant('field', 'inputs'), variant('field', 'config')];
const bytes = await datasetGet(url, 'production', path);
const value = decodeBeast2For(StringType)(bytes);

// Set dataset value
const encoded = encodeBeast2For(StringType)('new value');
await datasetSet(url, 'production', path, encoded);
```

### Tasks

```typescript
import { taskList, taskGet } from '@elaraai/e3-api-client';

// List tasks
const tasks = await taskList(url, 'production');
// [{ name: 'compute', hash: 'abc123...' }, ...]

// Get task details
const task = await taskGet(url, 'production', 'compute');
// { name: 'compute', hash: '...', commandIr: '...', inputs: [...], output: [...] }
```

### Execution

```typescript
import { dataflowStart, dataflowExecute, dataflowGraph, taskLogs } from '@elaraai/e3-api-client';

// Start execution (non-blocking)
await dataflowStart(url, 'production', { force: true });

// Execute and wait for result (blocking)
const result = await dataflowExecute(url, 'production', { force: true });
// { success: true, executed: 1n, cached: 0n, failed: 0n, tasks: [...], duration: 1.234 }

// Get dependency graph
const graph = await dataflowGraph(url, 'production');
// { tasks: [{ name: 'compute', inputs: [...], output: '...', dependsOn: [...] }] }

// Read task logs
const logs = await taskLogs(url, 'production', 'compute', { stream: 'stdout' });
// { data: '...', offset: 0n, size: 1024n, totalSize: 2048n, complete: false }
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
