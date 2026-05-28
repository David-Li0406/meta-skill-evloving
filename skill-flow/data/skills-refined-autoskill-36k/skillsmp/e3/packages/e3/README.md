# @elaraai/e3

SDK for authoring e3 packages.

## Installation

```bash
npm install @elaraai/e3
```

## Example

```typescript
import e3 from '@elaraai/e3';
import { StringType, East } from '@elaraai/east';

// Define input datasets with default values
const input_name = e3.input('name', StringType, 'World');
const input_prefix = e3.input('prefix', StringType, 'Hello');

// Define a task that combines inputs
const greet = e3.task(
  'greet',
  [input_prefix, input_name],
  East.function(
    [StringType, StringType],
    StringType,
    ($, prefix, name) => East.str`${prefix}, ${name}!`
  )
);

// Chain tasks - output of one feeds into the next
const shout = e3.task(
  'shout',
  [greet.output],  // reads from previous task's output
  East.function(
    [StringType],
    StringType,
    ($, greeting) => greeting.upperCase()
  )
);

// Create and export the package
const pkg = e3.package('greeting-pkg', '1.0.0', shout);
await e3.export(pkg, 'dist/greeting-pkg-1.0.0.zip');
```

This creates a package with:
- `.inputs.name` - String input (default: "World")
- `.inputs.prefix` - String input (default: "Hello")
- `.tasks.greet` - Combines inputs into greeting
- `.tasks.shout` - Transforms greeting to uppercase

## API

- `e3.input(name, type, default)` - Define an input dataset
- `e3.task(name, inputs, fn)` - Define a task with East function
- `e3.package(name, version, task)` - Create a package (dependencies collected automatically)
- `e3.export(pkg, path)` - Export package to zip file


## License

Dual AGPL-3.0 / Commercial. See [LICENSE.md](./LICENSE.md).

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
