# East Execution Engine (e3)

e3 is an automated, durable execution engine for [East](https://github.com/elaraai/east) programs with cross-language runtime support.

## Packages

| Package | Description | npm | License |
|---------|-------------|-----|---------|
| [`@elaraai/e3`](packages/e3/) | SDK for authoring e3 packages | [![npm](https://img.shields.io/npm/v/@elaraai/e3)](https://www.npmjs.com/package/@elaraai/e3) | [![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](packages/e3/LICENSE.md) |
| [`@elaraai/e3-types`](packages/e3-types/) | Shared type definitions | [![npm](https://img.shields.io/npm/v/@elaraai/e3-types)](https://www.npmjs.com/package/@elaraai/e3-types) | [![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](packages/e3-types/LICENSE.md) |
| [`@elaraai/e3-core`](packages/e3-core/) | Core library (like libgit2 for git) | [![npm](https://img.shields.io/npm/v/@elaraai/e3-core)](https://www.npmjs.com/package/@elaraai/e3-core) | [![License](https://img.shields.io/badge/license-BSL--1.1-orange.svg)](packages/e3-core/LICENSE.md) |
| [`@elaraai/e3-cli`](packages/e3-cli/) | Command-line interface | [![npm](https://img.shields.io/npm/v/@elaraai/e3-cli)](https://www.npmjs.com/package/@elaraai/e3-cli) | [![License](https://img.shields.io/badge/license-BSL--1.1-orange.svg)](packages/e3-cli/LICENSE.md) |
| [`@elaraai/e3-api-client`](packages/e3-api-client/) | HTTP client for remote repositories | [![npm](https://img.shields.io/npm/v/@elaraai/e3-api-client)](https://www.npmjs.com/package/@elaraai/e3-api-client) | [![License](https://img.shields.io/badge/license-BSL--1.1-orange.svg)](packages/e3-api-client/LICENSE.md) |
| [`@elaraai/e3-api-server`](packages/e3-api-server/) | HTTP server for remote access | [![npm](https://img.shields.io/npm/v/@elaraai/e3-api-server)](https://www.npmjs.com/package/@elaraai/e3-api-server) | [![License](https://img.shields.io/badge/license-BSL--1.1-orange.svg)](packages/e3-api-server/LICENSE.md) |

## Features

- **Content-Addressable Storage** - Git-like object store with automatic deduplication
- **Automatic Memoization** - Cache results based on function IR and arguments
- **Durable Execution** - Tasks are queued and executed to completion
- **Real-time Monitoring** - Stream logs from running tasks
- **Type-Safe RPC** - Beast2 binary encoding for efficient data transfer
- **Local or Remote** - Same CLI commands work with local paths or HTTP URLs

## Quick Start

```bash
# Create repository
e3 repo create .

# Import a package and deploy to workspace
e3 package import . ./my-package.zip
e3 workspace create . dev
e3 workspace deploy . dev my-package@1.0.0

# Run tasks
e3 start . dev

# Watch logs in real-time
e3 logs . dev.my-task --follow

# Get result
e3 get . dev.tasks.my-task.output
```

## Repository Structure

```
my-repo/                      # e3 repository directory
├── objects/                  # Content-addressable storage
│   └── ab/cd1234...beast2    # IR, args, results, commits
├── packages/                 # Package references
├── workspaces/               # Workspace state
└── executions/               # Execution cache and logs
```

## License

This project uses multiple licenses:

| Package | License |
|---------|---------|
| `@elaraai/e3` | Dual AGPL-3.0 / Commercial |
| `@elaraai/e3-types` | Dual AGPL-3.0 / Commercial |
| `@elaraai/e3-core` | BSL 1.1 |
| `@elaraai/e3-cli` | BSL 1.1 |
| `@elaraai/e3-api-client` | BSL 1.1 |
| `@elaraai/e3-api-server` | BSL 1.1 |

**BSL 1.1 (Business Source License):**
- Non-production use (evaluation, testing, development) is free
- Production use by or on behalf of for-profit entities requires a commercial license
- Code becomes AGPL-3.0 four years after each release

See [LICENSE.md](LICENSE.md) for full details.

**Commercial licensing:** support@elara.ai

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Contributors must sign our [CLA](CLA.md) before we can accept pull requests.


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
  - [@elaraai/e3-cli](https://www.npmjs.com/package/@elaraai/e3-cli): `e3 repo`, `e3 workspace`, `e3 start`, `e3 logs` commands for managing repositories, workspaces, and tasks
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
