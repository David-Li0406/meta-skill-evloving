# e3 User Guide

Usage guide for e3 (East Execution Engine) - a durable, content-addressable execution engine for East programs.

e3 provides git-like task management with cryptographic content addressing, allowing you to define dataflow pipelines that execute across multiple runtimes (Node.js, Python, Julia).

---

## Table of Contents

- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [SDK Reference](#sdk-reference)
- [CLI Reference](#cli-reference)
  - [Remote URLs](#remote-urls)
- [Project Setup](#project-setup)
- [Development Workflow](#development-workflow)
- [File Formats](#file-formats)

---

## Quick Start

### 1. Create a package

```typescript
// src/index.ts
import { East, IntegerType, StringType } from '@elaraai/east';
import e3 from '@elaraai/e3';

// Define an input
const name = e3.input('name', StringType, 'World');

// Define a task that uses the input
const greet = e3.task(
  'greet',
  [name],
  East.function([StringType], StringType, ($, n) =>
    East.str`Hello, ${n}!`
  )
);

// Bundle into a package
const pkg = e3.package('hello', '1.0.0', greet);

// Export for CLI import
await e3.export(pkg, '/tmp/hello.zip');
export default pkg;
```

### 2. Deploy and run

```bash
# Create a repository
e3 repo create .

# Import the package
e3 package import . /tmp/hello.zip

# Create a workspace and deploy
e3 workspace create . dev
e3 workspace deploy . dev hello@1.0.0

# Execute the dataflow
e3 start . dev

# Check the output
e3 get . dev.tasks.greet.output
# Output: "Hello, World!"

# Change the input and re-run
e3 set . dev.inputs.name name.east  # file containing: "Alice"
e3 start . dev
e3 get . dev.tasks.greet.output
# Output: "Hello, Alice!"
```

### 3. Watch mode (development)

```bash
# Auto-deploy and run on file changes
e3 watch . dev ./src/index.ts --start
```

---

## Core Concepts

### Package

An immutable collection of inputs, tasks, and their compiled East IR. Created with `e3.package()` and exported to a `.zip` file.

### Workspace

A mutable environment where a package is deployed. Workspaces hold:
- Input dataset values (can be modified)
- Task outputs (computed by running tasks)
- Execution state and cache

### Task

A computation that reads input datasets and produces an output dataset. Tasks are defined with `e3.task()` using an East function, or `e3.customTask()` for shell commands.

### Dataflow

The DAG of tasks and their dependencies. When you run `e3 start`, tasks execute in dependency order. Cached results are reused when inputs haven't changed.

### Content Addressing

All objects (IR, data, results) are stored by SHA256 hash. This enables:
- Automatic deduplication
- Cache invalidation when content changes
- Integrity verification

---

## SDK Reference

### `e3.input(name, type, defaultValue?)`

Defines an input dataset at `.inputs.${name}`.

```typescript
import { StringType, IntegerType, ArrayType } from '@elaraai/east';

// With default value
const name = e3.input('name', StringType, 'World');

// Without default (must be set before running)
const count = e3.input('count', IntegerType);

// Complex types
const items = e3.input('items', ArrayType(StringType), ['a', 'b', 'c']);
```

### `e3.task(name, inputs, fn, config?)`

Defines a task that runs an East function.

```typescript
import { East, IntegerType, StringType } from '@elaraai/east';

// Task with no inputs
const constant = e3.task(
  'constant',
  [],
  East.function([], IntegerType, ($) => {
    $.return(42n);
  })
);

// Task that depends on an input
const greet = e3.task(
  'greet',
  [name],  // input defined above
  East.function([StringType], StringType, ($, n) =>
    East.str`Hello, ${n}!`
  )
);

// Task that depends on another task's output
const shout = e3.task(
  'shout',
  [greet.output],
  East.function([StringType], StringType, ($, greeting) =>
    East.str`${greeting.toUpperCase()}!!!`
  )
);

// Task with custom runner
const pyTask = e3.task(
  'py_task',
  [someInput],
  East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n)),
  { runner: ['uv', 'run', 'east-py', 'run', '-p', 'east-py-std'] }
);
```

### `e3.customTask(name, inputs, outputType, command)`

Defines a task that runs a shell command instead of an East function.

```typescript
import { East, StringType, ArrayType } from '@elaraai/east';

const processData = e3.customTask(
  'process',
  [rawData],
  StringType,
  ($, input_paths, output_path) =>
    East.str`python process.py -i ${input_paths.get(0n)} -o ${output_path}`
);
```

### `e3.package(name, version, ...items)`

Bundles inputs and tasks into a package. Dependencies are collected automatically.

```typescript
// Only need to pass leaf tasks - dependencies are collected automatically
const pkg = e3.package('myapp', '1.0.0', finalTask);

// Or pass multiple items explicitly
const pkg = e3.package('myapp', '1.0.0',
  input1,
  input2,
  task1,
  task2
);
```

### `e3.export(pkg, zipPath)`

Exports a package to a `.zip` file for import into a repository.

```typescript
await e3.export(pkg, '/tmp/myapp.zip');
```

---

## CLI Reference

### Repository Commands

```bash
e3 repo create <repo>             # Create repository (local path or remote URL)
e3 repo remove <repo>             # Remove repository
e3 repo status <repo>             # Show repository status (packages, workspaces)
e3 repo gc <repo> [--dry-run]     # Remove unreferenced objects
```

### Package Commands

```bash
e3 package import <repo> <zipPath>       # Import package from .zip
e3 package export <repo> <pkg> <zipPath> # Export package to .zip
e3 package list <repo>                   # List installed packages
e3 package remove <repo> <pkg>           # Remove a package
```

### Workspace Commands

```bash
e3 workspace create <repo> <name>              # Create empty workspace
e3 workspace deploy <repo> <ws> <pkg[@ver]>    # Deploy package to workspace
e3 workspace export <repo> <ws> <zipPath>      # Export workspace as package
e3 workspace list <repo>                       # List workspaces
e3 workspace remove <repo> <ws>                # Remove workspace
e3 workspace status <repo> <ws>                # Show workspace status (tasks, datasets)
```

### Data Commands

```bash
e3 list <repo> [path]                          # List tree contents
e3 get <repo> <path> [-f east|json|beast2]     # Get dataset value
e3 set <repo> <path> <file> [--type <spec>]    # Set dataset from file
```

Path format: `workspace.path.to.dataset`

```bash
e3 get . dev.inputs.name           # Get input value
e3 get . dev.tasks.greet.output    # Get task output
e3 set . dev.inputs.name data.east # Set input from file
```

### Execution Commands

```bash
# Execute dataflow in workspace
e3 start <repo> <ws> [--filter <pattern>] [--concurrency <n>] [--force]

# Run a single task ad-hoc (outside workspace)
e3 run <repo> <pkg/task> [inputs...] -o <output>

# Watch and auto-deploy on changes
e3 watch <repo> <ws> <source.ts> [--start] [--abort-on-change]

# View task logs
e3 logs <repo> <path> [--follow]
```

### Utility Commands

```bash
# Convert between formats
e3 convert [input] [--from <fmt>] [--to <fmt>] [-o <output>] [--type <spec>]
```

### Authentication Commands

For remote servers that require authentication:

```bash
e3 login <server>                 # Log in using OAuth2 Device Flow
e3 logout <server>                # Log out and clear credentials
e3 auth status                    # List all saved credentials
e3 auth token <server>            # Print access token (for curl/debugging)
e3 auth whoami [server]           # Show current identity
```

The `e3 auth token` command is useful for debugging API calls with curl:

```bash
# Use token with curl
curl -H "Authorization: Bearer $(e3 auth token http://localhost:3000)" \
  http://localhost:3000/api/repos/my-repo/status
```

### Remote URLs

All commands that take a `<repo>` argument also accept HTTP URLs. Start a server with `e3-api-server`, then use the same CLI commands:

```bash
# Start a server (serves all repos under ./repos/)
e3-api-server --repos ./repos --port 3000

# All commands use the same URL format: http://server/repos/name
e3 repo create http://localhost:3000/repos/my-repo
e3 repo status http://localhost:3000/repos/my-repo
e3 repo remove http://localhost:3000/repos/my-repo

# Works the same for workspace and package commands
e3 workspace list http://localhost:3000/repos/my-repo
e3 workspace create http://localhost:3000/repos/my-repo dev
e3 package import http://localhost:3000/repos/my-repo ./pkg.zip
e3 workspace deploy http://localhost:3000/repos/my-repo dev myapp@1.0.0
```

**URL structure:**

```
User-facing URL:  http://localhost:3000/repos/my-repo
                  └──────────┬───────┘ └─────┬──────┘
                           origin      /repos/{name}

API endpoint:     http://localhost:3000/api/repos/my-repo/workspaces
                                        └─┬─┘
                                    inserted by CLI
```

The CLI automatically inserts `/api` when making requests. This keeps user-facing URLs clean (shareable, works in browser) while the server handles API routes under `/api/repos/...`.

---

## Project Setup

### TypeScript Project

```
my-e3-project/
├── package.json
├── tsconfig.json
├── pyproject.toml      # For Python runner (east-py)
├── src/
│   └── index.ts        # Package definition
└── repo/               # Repository (created by e3 repo create)
```

**package.json:**
```json
{
  "name": "my-e3-project",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "main": "node dist/index.js"
  },
  "dependencies": {
    "@elaraai/east": "^0.0.1-beta.11",
    "@elaraai/e3": "^0.0.2-beta.5"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src"]
}
```

**pyproject.toml** (for Python runner):
```toml
[project]
name = "my-e3-project"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "east-py>=0.0.1b11",
    "east-py-std>=0.0.1b11",
]

[tool.uv]
dev-dependencies = []
```

### Makefile (recommended)

```makefile
WORKSPACE ?= dev
PACKAGE_NAME ?= myapp
PACKAGE_VERSION ?= 1.0.0

build:
	npm run build

package: build
	npm run main

import: package
	e3 package import . /tmp/pkg.zip

deploy: import
	e3 workspace create . $(WORKSPACE) || true
	e3 workspace deploy . $(WORKSPACE) $(PACKAGE_NAME)@$(PACKAGE_VERSION)

start: deploy
	e3 start . $(WORKSPACE)

all: start

clean:
	rm -rf dist /tmp/pkg.zip
```

---

## Development Workflow

### Watch Mode

The fastest development workflow uses `e3 watch`:

```bash
e3 watch . dev ./src/index.ts --start
```

This:
1. Compiles your TypeScript on save
2. Exports and imports the package
3. Deploys to the workspace
4. Executes the dataflow
5. Repeats when files change

Use `--abort-on-change` to cancel running executions when you save:

```bash
e3 watch . dev ./src/index.ts --start --abort-on-change
```

### Manual Workflow

```bash
# Build and export
npm run build && npm run main

# Import and deploy
e3 package import . /tmp/pkg.zip
e3 workspace deploy . dev myapp@1.0.0

# Run
e3 start . dev

# Check results
e3 workspace status . dev
e3 get . dev.tasks.mytask.output
```

### Caching

Tasks are cached by content hash. A task only re-runs when:
- Its East function IR changes
- Any of its input values change

Changing one task doesn't invalidate unrelated tasks. Use `--force` to bypass cache:

```bash
e3 start . dev --force
```

---

## File Formats

e3 supports three formats for data:

### .east (Human-Readable)

```east
42                      # Integer
"hello"                 # String
[1, 2, 3]              # Array
(name="Alice", age=30) # Struct
```

### .json

```json
{"type": "Integer", "value": "42"}
```

### .beast2 (Binary)

Compact binary format with self-describing types. Use for efficiency.

### Converting

```bash
e3 convert data.beast2                    # → .east (default)
e3 convert data.east --to beast2 -o out.beast2
e3 convert data.json --to east
```

---

## Tips

1. **Use watch mode** for fast iteration during development
2. **Let dependencies flow** - only pass leaf tasks to `e3.package()`, dependencies are collected automatically
3. **Check status** with `e3 workspace status . <ws>` to see task states
4. **View logs** with `e3 logs . workspace.taskname` for debugging
5. **Use inputs** for values that change between runs, tasks for computations
