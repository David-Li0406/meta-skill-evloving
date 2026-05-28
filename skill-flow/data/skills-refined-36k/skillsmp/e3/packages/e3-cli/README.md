# @elaraai/e3-cli

Command-line interface for e3 (East Execution Engine).

## Installation

```bash
npm install -g @elaraai/e3-cli
```

## Commands

### Repository

```bash
e3 repo create <repo>             # Create a new repository
e3 repo status <repo>             # Show repository status
e3 repo remove <repo>             # Remove a repository
e3 repo gc <repo> [--dry-run]     # Remove unreferenced objects
```

### Packages

```bash
e3 package import <repo> <zip>        # Import package from .zip
e3 package export <repo> <pkg> <zip>  # Export package to .zip
e3 package list <repo>                # List installed packages
e3 package remove <repo> <pkg>        # Remove a package
```

### Workspaces

```bash
e3 workspace create <repo> <name>     # Create empty workspace
e3 workspace deploy <repo> <ws> <pkg> # Deploy package to workspace
e3 workspace export <repo> <ws> <zip> # Export workspace as package
e3 workspace list <repo>              # List workspaces
e3 workspace status <repo> <ws>       # Show workspace status
e3 workspace remove <repo> <ws>       # Remove workspace
```

### Data

```bash
e3 list <repo> [path]             # List workspaces or tree contents
e3 tree <repo> <path>             # Show full tree structure
e3 get <repo> <path> [-f format]  # Get dataset value (east/json/beast2)
e3 set <repo> <path> <file>       # Set dataset value from file
```

### Execution

```bash
e3 start <repo> <ws>              # Execute tasks in workspace
e3 run <repo> <task> [inputs...]  # Run task ad-hoc
e3 watch <repo> <ws> <source.ts>  # Watch and auto-deploy on changes
e3 logs <repo> <path> [--follow]  # View task logs
```

### Utilities

```bash
e3 convert [input] --to <format>  # Convert between .east/.json/.beast2
```

### Authentication (for remote servers)

```bash
e3 login <server>                 # Log in using OAuth2 Device Flow
e3 logout <server>                # Log out and clear credentials
e3 auth status                    # List all saved credentials
e3 auth token <server>            # Print access token (for curl/debugging)
e3 auth whoami [server]           # Show current identity
```

The `e3 auth token` command is useful for debugging API calls:

```bash
curl -H "Authorization: Bearer $(e3 auth token https://example.com)" \
  https://example.com/api/repos/my-repo/status
```

## Example

```bash
# Create repository and import a package
e3 repo create ./my-project
e3 package import ./my-project ./greeting-pkg-1.0.0.zip

# Create workspace and deploy package
e3 workspace create ./my-project dev
e3 workspace deploy ./my-project dev greeting-pkg@1.0.0

# Set input and run
e3 set ./my-project dev.inputs.name ./name.east
e3 start ./my-project dev

# Get results
e3 get ./my-project dev.tasks.shout.output
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
