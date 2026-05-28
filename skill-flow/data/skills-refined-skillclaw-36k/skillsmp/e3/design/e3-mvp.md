# e3: MVP

A cut-down "version 1" plan for e3.


### Architecture

```
┌───────────────────────────────────────────────────────┐
│  . (your e3 repository directory)                     │
│  ├── objects/          # Content-addressed storage    │
│  ├── packages/         # Installed packages (refs)    │
│  ├── executions/       # Execution state and results  │
│  └── workspaces/       # Stateful dataset namespaces  │
└───────────────────────────────────────────────────────┘
```

The e3 repository contains and runs your workspaces, while also acting as a cache, execution log and package store.

Workspaces are where you work with data and follow the "template" defined in the package deployed to that workspace. You can type `e3 start <workspace>` to execute the tasks to produce results.

Packages can serve different purposes, from support libraries to client project code. When a package is deployed to a workspace, so are all of its dependencies (meaning each workspace is associated with a given "root" or "main" package). Packages are immutable, and if you run the same package in a different workspace or e3 repository (even on a different computer), the same outputs will be reproduced.

e3 is agnostic to how code and packages are authored. You might create packages in TypeScript using the fluent API, extract them from another repository, or eventually code them in a native East syntax. East tasks execute compiled modules (IR), installed via packages.

### Key Concepts

**Workspaces** are namespaces of interactive datasets that you can read and write. Each workspace is initialized by deploying a package to the workspace, and contains the datasets and tasks (transformations producing datasets).

**Packages** are an immutable bundle of e3 objects - task objects, data structure, and initial values.

**Runners** are programs that can execute e3 tasks (e.g. our Python interpreter `east-py` or Julia compiler). Each task object specifies its runner and the command template to execute it.

**Task objects** define a computation: a runner key plus paths to input and output datasets. For East tasks, the first input path points to the function IR (at `tasks.{name}.function_ir`), and the remaining inputs are the function arguments. Input/output types are inferred from the package's structure at those paths.

**Executions** are task executions with specific inputs. Execution identity is the hash of the runner plus all input hashes - same inputs always produce the same result, enabling memoization.

**Tasks** (user-facing) are transformations that read input datasets and produce output datasets. `e3 start` executes all tasks in dependency order (like `make`).

**Data tree structure:**
- `.inputs.{name}` - Input datasets (user-provided data)
- `.tasks.{name}.function_ir` - Task IR (compiled function, private)
- `.tasks.{name}.output` - Task output (result of running the task)

**Path syntax:**
- **CLI:** `workspace.path.to.dataset` (e.g., `production.inputs.sales`)
- **Internal/Keypath:** `#.path.to.dataset` (e.g., `#.inputs.sales`)

The CLI syntax uses the workspace name as the first segment for a natural feel.
Internally, e3 uses keypath syntax (`#.field[index]`) for serialization, glob patterns, and future East language integration.

### Example Workflow

```bash
# Initialize a repository for production data
$ cd ~/data/client-abc
$ e3 init .
Created e3 repository

# Install your team's package from a local .zip
$ e3 package import . ~/dev/acme-forecast/dist/acme-forecast-1.2.0.zip
Installing acme-forecast@1.2.0... done

# Run a task ad-hoc against data on your computer
$ e3 run . acme-forecast/train ./sales.beast2 -o ./model.beast2
Running acme-forecast/train... done (2.3s)

# Run again with same inputs - instant (cached)
$ e3 run . acme-forecast/train ./sales.beast2 -o ./model.beast2
Cached (0.01s)

# Create a workspace and deploy a package
$ e3 workspace create . production
Created production workspace

$ e3 workspace deploy . production acme-forecast@0.21.1
Deploying acme-forecast@0.21.1 to production... done

# Execute all tasks
$ e3 start . production
[1/3] preprocess... done (0.5s)
[2/3] train... done (38.1s)
[3/3] predict... done (1.2s)

# Get/set datasets
$ e3 get . production.tasks.predict.output
$ e3 set . production.inputs.sales ./new_sales.beast2

# Rerun - only affected tasks execute
$ e3 start . production
[1/3] preprocess... cached
[2/3] train... cached
[3/3] predict... done (1.1s)

# Export workspace as a package (includes deployed package + current data)
$ e3 workspace export . production ./handoff.zip
Exporting acme-forecast-0.21.1-a3f8b2c1 to handoff.zip... done

# Colleague imports it
$ e3 package import . ./handoff.zip
Installing acme-forecast@0.21.1-a3f8b2c1... done

$ e3 workspace deploy . analysis acme-forecast@0.21.1-a3f8b2c1
# Now they have your exact data state
```

## Repository Structure

An e3 repository is a directory containing content-addressed storage and refs. Most files outside `objects/` are **refs** - small text files containing a SHA256 hash pointing to an object.

### Example Repository

```
~/data/client-abc/                    # Your e3 repository
├── objects/                          # Content-addressed storage (all data lives here)
│   ├── 3a/
│   │   └── 8f2b...                   # A package object
│   ├── 7c/
│   │   └── 91d4...                   # A module IR blob
│   ├── a1/
│   │   └── bc56...                   # A dataset value
│   └── f2/
│       └── e847...                   # An execution result
│
├── packages/                         # Installed packages (refs)
│   └── acme-forecast/
│       ├── 0.20.0                    # Contains: 7d3e1a... → objects/7d/3e1a...
│       └── 0.21.1                    # Contains: 9b4c2f... → objects/9b/4c2f...
│
├── executions/                       # Execution history for tasks
│   └── c4f9a2.../                    # Input hash (hash of all input values)
│       ├── stdout.txt                # Captured stdout (streamed during run)
│       ├── stderr.txt                # Captured stderr (streamed during run)
│       └── output                    # Contains: f2e847... → objects/f2/e847...
│
└── workspaces/                       # Stateful dataset namespaces
    └── production.beast2             # Workspace state (deployment + data root)
```

### Directory Reference

#### `objects/`

Content-addressed storage for all immutable data. Objects are stored by SHA256 hash, split into subdirectories by first two hex characters (like git). Everything ends up here: module IR, task definitions, dataset values, execution results, packages.

#### `packages/`

Installed packages. Each `<name>/<version>` file is a ref pointing to a package object in `objects/`. Package objects contain refs to their tasks, data structure, and initial values.

When you `e3 package add . acme-forecast`:
1. Package object and all referenced objects stored in `objects/`
2. Ref created at `packages/acme-forecast/0.21.1`

#### `executions`

Task execution logs and (memoized) outputs. Organized by execution hash (the SHA256 of the task object plus inputs).

- `stdout.txt`, `stderr.txt` - Captured output (streamed live during execution)
- `output` - Ref to the result object

Execution identity = hash(task_hash, input_hashes...). Same inputs → same execution directory → cache hit.

#### `workspaces/`

Stateful namespaces where you work with data. Each workspace is stored as a single `.beast2` file (`workspaces/<name>.beast2`) containing the workspace state:

```ts
type WorkspaceState = {
  packageName: string;      // Name of deployed package
  packageVersion: string;   // Version of deployed package
  packageHash: string;      // Hash of package object at deploy time (immutable)
  deployedAt: Date;         // UTC datetime of deployment
  rootHash: string;         // Current root data tree hash
  rootUpdatedAt: Date;      // UTC datetime of last root update
};
```

An empty file indicates an undeployed workspace (created but no package deployed yet).

Workspaces follow the "template" defined by their package: the tasks determine what computations run and how datasets connect. But the actual data values can differ between workspaces.

The workspace root is a tree structure (like a git commit's root tree) enabling:
- **Atomic updates**: Swap one ref to update entire workspace
- **Structural sharing**: Unchanged subtrees keep the same hash
- **Fast cloning**: Duplicate a workspace by copying the state file

### Refs Pattern

Most files outside `objects/` are refs - text files containing a SHA256 hash:

```bash
$ cat packages/acme-forecast/0.21.1
3a8f2b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a

$ cat executions/c4f9a2.../output
d4e5f6789abc0123456789abcdef0123456789abcdef0123456789abcdef0123
```

This indirection enables:
- **Deduplication**: Same data referenced from multiple places
- **Atomic updates**: Write new object, then update ref
- **Easy diffing**: Compare ref values to detect changes

The exceptions are:
- `executions/<hash>/*.txt` - Log files streamed during execution
- `workspaces/<name>.beast2` - Binary state file (not a simple ref)

### Object Types

All data in `objects/` is one of these types:

| Object | Description | Defined in |
|--------|-------------|------------|
| **Package** | Bundle of tasks, data structure, initial values | Packages section |
| **Module** | East IR + imports | Packages section |
| **Task** | How to run a computation (runner + input/output paths) | Tasks & Execution section |
| **Data** | East values as trees or blobs | Data Objects section |

Objects reference each other by hash. A package contains hashes pointing to its tasks. A task contains paths to datasets (where input data and function IR are read, and where outputs are written).

### Data Tree Objects

Data tree objects store East values as persistent trees with structural sharing (like git trees). Each tree object is a `.beast2` file containing an East variant:

```ts
type DataRefType = VariantType<{
    unassigned: NullType, // leaf for unassigned value (e.g. result of a pending task)
    null: NullType,       // leaf for inline null value (optimization for NullType)
    value: StringType,   // leaf for value in object store (hash of .beast2 object)
    tree: StringType,     // tree of data refs (hash of .beast2 object)
}>

type TreeObjectType<T extends EastType> =
  T extends StructType<infer Fields> ? StructType<{ [K in keyof Fields]: DataRefType }> :
//   T extends ArrayType<infer U> ? ArrayType<DataRefType> :
//   T extends DictType<infer K, infer V> ? Dict<K, DataRefType> :
//   T extends VariantType<infer Cases> ? StructType<{ case: StringType /* keyof Cases */, value: DataRefType }> :
  never
```

The MVP will only contain "struct" trees - the names of datasets are static.
The more dynamic types will allow for data partitioning and dataflow patterns like scatter-gather later.

**Example: Workspace root (struct)**

```east
(
    inputs = .tree "a1bc56...",
    tasks = .tree "d4e5f6...",
)
```

**Example: inputs struct**

```east
(
    sales = .value "7c91d4...",
    features = .value "8d2e7f...",
)
```

**Example: tasks struct**

```east
(
    train = .tree "b2c3d4...",
    predict = .tree "e5f6a7...",
)
```

**Example: task subtree (tasks/train)**

```east
(
    function_ir = .value "1a2b3c...",   // The compiled IR (private)
    output = .unassigned,                // Task output (initially unassigned)
)
```

**Type inference:** Data references don't include East types. The type can be inferred by traversing the package's dataset schema in parallel with the object tree. The variant tag (value/tree) tells the decoder how to interpret the object's structure; the schema tells it what the values mean. Note each .beast2 object has a self-describing header - this means the tree object do include struct field names inside the referred object.

**Structural sharing:** When updating a single field, only the path from root to that field needs new objects. Unchanged subtrees keep their hashes, enabling fast atomic updates and cheap workspace cloning.

### Garbage Collection

`e3 gc` removes unreferenced objects. The object graph is traced from roots:

**Roots:**
- `packages/<name>/<version>` → PackageObject hash
- `workspaces/<ws>.beast2` → Contains packageHash and rootHash
- `executions/<hash>/output` → DataObject hash

**Object references:**

| Object | References |
|--------|------------|
| PackageObject | `tasks` → TaskObject hashes |
| | `data.value` → TreeObject hash (root of data tree) |
| TaskObject | None (contains paths, not hashes) |
| TreeObject | `.value` refs → DataObject hashes (blobs) |
| | `.tree` refs → TreeObject hashes (subtrees) |
| | `.null` / `.unassigned` → None (terminal) |

### Bundled vs Installed

**Bundled** (`.zip` for distribution):
```
acme-forecast-0.21.1.zip
├── packages/
│   └── acme-forecast/
│       └── 0.21.1              # Ref to package object hash
└── objects/
    ├── 3a/8f2b...
    ├── 7c/91d4...
    └── ...
```
- All objects inline in a zip file
- Package identity via path structure (no separate manifest)
- Self-contained, can be copied anywhere
- Produced by TypeScript build, `e3 package export`, or `e3 workspace export`
- Streaming I/O via `yauzl`/`yazl` (no need to load into RAM)

**Installed** (in repository):
- Objects extracted to `objects/`
- Ref created at `packages/<name>/<version>`
- Deduped with other packages
- Ready to deploy to workspaces

## Packages

A **package** bundles everything needed to run computations: task objects, data structure, and initial values. Packages are:
- **Defined in TypeScript** using the e3 SDK
- **Distributed as `.zip`** files (bundled form)
- **Installed as refs** to objects in the repository

### Package Object

A package object is stored in `objects/` and contains refs (hashes) to other objects:

```ts
type PackageObject = StructType<{
    // Task objects: name → task object hash
    tasks: DictType<StringType, StringType>,

    // Data structure and initial values
    data: StructType<{
        structure: Structure,    // Defines tree shape (what's a tree vs dataset)
        value: StringType,       // Hash of root TreeObject
    }>,

    // Future package dependencies:
    // dependencies: DictType<StringType, StringType>,  // pkg name → version
}>;

// Structure defines the workspace tree shape (what's a tree vs dataset)
type Structure = VariantType<{
    value: EastTypeValue,                         // Dataset: holds a typed value
    struct: DictType<StringType, Structure>,      // Tree: has named children
    // Future variants: array, dict, variant trees
}>;

// TreePath identifies a location in the data tree
type TreePath = ArrayType<PathSegment>;

type PathSegment = VariantType<{
    field: StringType,  // Struct field access
    // Future variants:
    //  - index: array element access
    //  - key: dict key lookup
    //  - glob: iterate over array/dict entries
}>;

// Task object: runner + input/output paths (types inferred from structure)
type TaskObject = StructType<{
    runner: StringType,           // Runner key (e.g., "east-node")
    inputs: ArrayType<TreePath>,  // Paths to input datasets
    output: TreePath,             // Path to output dataset
}>;
```

**Example package object:**

```east
(
    tasks = {
        "train": "5e7a3b...",      // hash of TaskObject
        "predict": "c4d5e6...",    // hash of TaskObject
    },

    data = (
        structure = .struct {
            "inputs": .struct {
                "sales": .value SalesRecordType,
                "features": .value FeaturesType,
            },
            "tasks": .struct {
                "train": .struct {
                    "function_ir": .value FunctionIRType,
                    "output": .value ModelType,
                },
                "predict": .struct {
                    "function_ir": .value FunctionIRType,
                    "output": .value PredictionType,
                },
            },
        },
        value = "f4a7c2...",  // Hash of root TreeObject (initial values)
    ),
)
```

**Example task object (for "train"):**

```east
(
    runner = "east-node",
    inputs = [
        [.field "tasks", .field "train", .field "function_ir"],
        [.field "inputs", .field "sales"],
        [.field "inputs", .field "features"],
    ],
    output = [.field "tasks", .field "train", .field "output"],
)
```

### Bundled vs Installed

**Bundled** (`.zip` for distribution):
- All content inline in a zip file
- Self-contained, can be copied anywhere
- Produced by TypeScript build or `e3 workspace export`

**Installed** (in repository):
- Content stored in `objects/`
- Ref at `packages/<name>/<version>` points to package object
- Dependencies resolved to specific versions

```bash
# Import from local .zip
$ e3 package import . ~/dev/acme-forecast/dist/acme-forecast-0.21.0.zip

# Add from registry (fetches + imports)
$ e3 package add . acme-forecast@0.21.0

# Export an installed package to .zip
$ e3 package export . acme-forecast@0.21.0 ./acme-forecast-0.21.0.zip
```

### Package Namespacing

Package names provide namespaces for their contents:

```bash
# Run a task from a package
$ e3 run . acme-forecast/train inputs/sales.east -o model.beast2

# Reference a module from another package (in East code)
const ml = $.import("east-python/ml");
```

### Creating Packages

Packages are defined in TypeScript using the e3 SDK:

```typescript
import { ArrayType } from '@elaraai/east';
import e3 from '@elaraai/e3';

// Input dataset at .inputs.sales
const sales = e3.input("sales", ArrayType(...), /* default value goes here */);

// Define a task - creates .tasks.train.function_ir and .tasks.train.output
const train = e3.task("train", [sales], ($, salesData) => {
    // ... East function body
    return model;
});

// Chain tasks - train.output is at .tasks.train.output
const predict = e3.task("predict", [train.output, sales], ($, model, salesData) => {
    // ... East function body
    return predictions;
});

// Construct the package - dependencies collected automatically
const pkg = e3.package("acme-forecast", "0.21.0", predict);

// Export to zip
await e3.export(pkg, "./acme-forecast-0.21.0.zip");
```

There is a lot of freedom to import and bundle "pure" East modules defined in other npm packages, dynamically link with e3 packages, define logic inline, or more.

Simply run the script to produce the `acme-forecast-0.21.0.zip` bundle.

## Tasks & Execution

A **task object** defines how to run a computation: a runner key plus paths to input and output datasets. Tasks are stored in `objects/` and referenced by packages.

### Task Object

```ts
type TaskObject = StructType<{
    runner: StringType,           // Runner key (e.g., "east-node")
    inputs: ArrayType<TreePath>,  // Paths to input datasets
    output: TreePath,             // Path to output dataset
}>;
```

Input/output types are inferred from the package's structure at those paths - the task just references locations, not types.

### Example: Node.js Task

```east
(
    runner = "east-node",
    inputs = [
        [.field "tasks", .field "train", .field "function_ir"],
        [.field "inputs", .field "sales"],
    ],
    output = [.field "tasks", .field "train", .field "output"],
)
```

### Runner command configuration

Each task object includes a `command` field that specifies how to execute the runner. The command is a template with placeholders for input and output paths.

```ts
type CommandPart = VariantType<{
    literal: StringType,     // Literal string: "east-py", "run"
    input_path: NullType,    // Path to "next" input (e.g. first)
    inputs: ArrayType<VariantType<{ // For each remaining input
        literal: StringType, // Literal string: "--input"
        input_path: NullType // Path to inputs
    }>>,
    output_path: NullType, // Path where output should be written
}>;
```

This allows each task to define exactly how its runner should be invoked, without needing a central repository configuration file.

### The East CLI

The `east-node` CLI (from `@elaraai/east-node`) runs East IR:

```bash
east-node run \
  --runtime @elaraai/east-node-fs \
  acme-forecast/train \
  --input ./inputs/sales.beast2 \
  --output ./outputs/model.beast2
```

- `--runtime <pkg>` - npm packages providing runtime modules (self-register their module names)
- `<name>` - the IR to execute
- `--input <path>` - input data files
- `--output <path>` - where to write result

Runtime module packages export a record keyed by module name:

```typescript
// @elaraai/east-node-fs
export default {
    "east-node/fs": { 
        readFile: (path: EastString) => /* ... */,
        writeFile: (path: EastString, data: EastBytes) => /* ... */,
    },
};
```

### Execution

An **execution** is a task invoked with specific inputs. Execution identity:

```
input_hash = hash(runner, ...input_hashes)
```

Same runner + same inputs (fixed or otherwise) = same execution directory = cache hit.

### Running Tasks

```bash
# Ad-hoc run (specify I/O explicitly)
$ e3 run . acme-forecast/train inputs/sales.east -o outputs/model.beast2
Running acme-forecast/train... done (2.3s)

# Run again - cache hit
$ e3 run . acme-forecast/train inputs/sales.east -o outputs/model.beast2
Cached (0.01s)

# Run from a different package
$ e3 run . other-pkg/preprocess inputs/raw.json -o inputs/clean.east
```

### Execution Process

Each task execution runs as a **separate process**:

1. e3 looks up the task object from `objects/`
2. Run the runner's command, substituting:
   - `.input_path` → path to "next" input (starting with first)
   - `.inputs` → repeat a pattern for all remaining inputs
   - `.output` → output path
4. Store result in `objects/`, write ref to `executions/<hash>/output`
5. Stdout/stderr streamed to `executions/<hash>/*.txt`

### Memoization

Executions are cached by their ID (hash of task + inputs). When you run a task:

1. Compute input hash from input content hashes
2. Check if `tasks/<task_hash>/executions/<input_hash>/output` exists
3. If cached: return result immediately (read ref, fetch from objects/)
4. If not: execute, store result, write ref
5. If dir exists but without output, it is either a failed or concurrent execution (prompt user to check logs and use `--force` to rerun if necessary)

This means:
- Changing inputs → new execution (cache miss)
- Changing module code → new task hash → new execution
- Re-running unchanged computation → instant cache hit
- User can handle failures manually

Note e3 MVP has no capability for the user to concurrently launch multiple tasks (use `e3 start` to get it to handle this in a single process).
Possibly we should use a repository-wide lock file to handle this.

## Running Tasks

```bash
# Run all tasks in a workspace (like `make`)
$ e3 start . production
[1/3] preprocess... done (0.5s)
[2/3] train... cached
[3/3] predict... done (1.2s)

# Watch for changes and re-run affected tasks
$ e3 start . production --watch
Watching for changes... (Ctrl+C to stop)
```

The task DAG is implicit - all tasks in the package, connected by their input/output paths.

`e3 start` topologically sorts tasks by their input/output dependencies and executes them in order. Cached results are used when inputs haven't changed.
With the `--watch` flag it will use inotify to watch for changed values (when an external process changes the workspace data) and propagate them.

### Selective Execution

```bash
# Run a specific task
$ e3 start . production train
```

### Project structure

This git repository is an npm workspace with the following packages:

 - **e3-types** - TypeScript types for e3 object and ref content (shared)
 - **e3-core** - Programmatic TypeScript API for interacting with e3 repositories (NodeJS)
 - **e3-cli** - CLI tool wrapping the above 
 - **integration-tests** - runs end-to-end tests using the CLI tool in a temp dir
