# @elaraai/e3-api-tests

Compliance test suite for e3 API servers, used for integration tests in the e3 monorepo. Intended to verify the reference server (`@elaraai/e3-api-server`), and ensure any alternative e3 server implementations conform to the same API contract.

## Installation

```bash
npm install @elaraai/e3-api-tests
```

## Usage

```typescript
import { describe, before, after } from 'node:test';
import { createServer } from '@elaraai/e3-api-server';
import { allApiTests, createTestContext, type TestContext } from '@elaraai/e3-api-tests';

describe('API compliance', () => {
  let server: Server;
  let context: TestContext;

  before(async () => {
    server = await createServer({ reposDir: tempDir, port: 0 });
    await server.start();
    context = await createTestContext({
      baseUrl: `http://localhost:${server.port}`,
      getToken: async () => '',  // No auth for local server
    });
  });

  after(async () => {
    await context.cleanup();
    await server.stop();
  });

  // Registers all API test suites
  allApiTests(() => context);
});
```

## Exports

| Export | Description |
|--------|-------------|
| `createTestContext` | Create test context with helpers for setup/teardown |
| `allApiTests` | Register all API test suites (repository, packages, workspaces, datasets, dataflow) |
| `allTests` | Register all tests including CLI tests (requires credentials env) |
| `repositoryTests` | Repository CRUD tests |
| `packageTests` | Package import/export tests |
| `workspaceTests` | Workspace management tests |
| `datasetTests` | Dataset read/write tests |
| `dataflowTests` | Dataflow execution tests |
| `platformTests` | Platform capability tests |
| `cliTests` | CLI integration tests |
| `createPackageZip` | Create a test package zip file |
| `runE3Command` | Run an e3 CLI command |

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
