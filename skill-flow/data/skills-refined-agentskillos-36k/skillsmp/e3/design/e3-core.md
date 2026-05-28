# e3-core: Core Operations

This document specifies the fundamental operations on an e3 repository. These operations form the API that the CLI and other interfaces use.

## Repository

### `init(path: String) → Result<(), Error>`

Create a new e3 repository at `path`.

Creates:
- `objects/`
- `packages/`
- `executions/`
- `workspaces/`

### `gc(repo: Repo) → Result<GcStats, Error>`

Remove unreferenced objects. Traces from roots (packages, workspaces, executions) and deletes unreachable objects.

Returns count of deleted objects and bytes reclaimed.

## Objects

All objects are content-addressed by SHA256 hash.

### `object_read(repo: Repo, hash: String) → Result<Bytes, Error>`

Read raw bytes of an object.

### `object_write(repo: Repo, data: Bytes) → String`

Write bytes to objects/, returns hash. Idempotent - same content always produces same hash.

### `object_exists(repo: Repo, hash: String) → Boolean`

Check if object exists.

### `object_path(repo: Repo, hash: String) → String`

Return filesystem path: `objects/<hash[0..2]>/<hash[2..]>`

## Packages

### `package_import(repo: Repo, zip_path: String) → Result<(String, String), Error>`

Import a package from a `.zip` file. Extracts objects to `objects/`, creates ref at `packages/<name>/<version>`.

Returns `(name, version)`.

### `package_export(repo: Repo, name: String, version: String, zip_path: String) → Result<(), Error>`

Export a package to a `.zip` file. Collects the package object and all transitively referenced objects.

### `package_remove(repo: Repo, name: String, version: String) → Result<(), Error>`

Remove package ref. Objects remain until `gc`.

### `package_list(repo: Repo) → Array<(String, String)>`

List installed packages as `(name, version)` pairs.

### `package_resolve(repo: Repo, name: String, version: String) → Result<String, Error>`

Resolve `packages/<name>/<version>` to PackageObject hash.

### `package_read(repo: Repo, name: String, version: String) → Result<PackageObject, Error>`

Read and parse a PackageObject.

## Workspaces

### `workspace_create(repo: Repo, name: String) → Result<(), Error>`

Create an empty workspace. Creates `workspaces/<name>/` directory.

### `workspace_remove(repo: Repo, name: String) → Result<(), Error>`

Remove a workspace. Objects remain until `gc`.

### `workspace_list(repo: Repo) → Array<String>`

List workspace names.

### `workspace_deploy(repo: Repo, ws: String, pkg_name: String, pkg_version: String) → Result<(), Error>`

Deploy a package to a workspace:
1. Write `workspaces/<ws>/package` ref to `<pkg_name>/<pkg_version>`
2. Copy package's `datasets.value` as workspace root
3. Write `workspaces/<ws>/root` ref

### `workspace_export(repo: Repo, ws: String, zip_path: String, name: Option<String>, version: Option<String>) → Result<(), Error>`

Export workspace as a package:
1. Read deployed package
2. Create new PackageObject with `datasets.value` set to current workspace root
3. Collect all referenced objects
4. Write to `.zip`

Default name: deployed package name. Default version: `<pkg_version>-<root_hash[0..8]>`.

### `workspace_get_package(repo: Repo, ws: String) → Result<(String, String), Error>`

Get deployed package `(name, version)`.

### `workspace_get_root(repo: Repo, ws: String) → Result<String, Error>`

Get root DataObject hash.

### `workspace_set_root(repo: Repo, ws: String, hash: String) → Result<(), Error>`

Atomically update root DataObject hash.

## Tree Objects

Tree objects form persistent trees with structural sharing. See e3.md "Data Tree Objects" for the type definitions.

### `tree_read(repo: Repo, hash: String) → Result<TreeObject, Error>`

Read and parse a tree object.

### `tree_write_struct(repo: Repo, fields: Dict<String, DataRef>) → String`

Write a struct tree (field name → DataRef). Returns hash.

### `tree_write_array(repo: Repo, elements: Array<DataRef>) → String`

Write an array tree (ordered DataRefs). Returns hash.

### `tree_write_dict(repo: Repo, entries: Array<(Bytes, DataRef)>) → String`

Write a dict tree (key bytes + DataRef pairs). Returns hash.

### `tree_write_variant(repo: Repo, case: String, value: DataRef) → String`

Write a variant tree (case name + DataRef). Returns hash.

## Dataset Access

High-level operations on workspace data trees using TreePaths.

```ts
type TreePath = Array<PathComponent>;
type PathComponent =
    | { field: String }     // .field "name"
    | { glob: null };       // .glob
```

### `dataset_get(repo: Repo, ws: String, path: TreePath) → Result<Bytes, Error>`

Read a blob at a specific path (no globs). Traverses the tree, returns blob bytes.

Example: `dataset_get(repo, "production", [.field "inputs", .field "sales"])`

### `dataset_set(repo: Repo, ws: String, path: TreePath, value: Bytes) → Result<(), Error>`

Update a blob at a specific path (no globs). Creates new tree objects along the path (structural sharing), updates workspace root atomically.

### `dataset_list(repo: Repo, ws: String, path: TreePath) → Result<Array<Key>, Error>`

List keys at a tree node (array indices or dict keys). The path should point to an array or dict tree.

### `dataset_traverse(repo: Repo, ws: String, path: TreePath) → Result<Array<(TreePath, String)>, Error>`

Expand globs in path, return all matching (concrete_path, blob_hash) pairs.

Example: `dataset_traverse(repo, "production", [.field "inputs", .field "sales", .glob])`
→ `[([.field "inputs", .field "sales", .index 0], "abc..."), ...]`

## Tasks

### `task_resolve(repo: Repo, pkg_name: String, pkg_version: String, task_name: String) → Result<String, Error>`

Resolve a task to its TaskObject hash.

### `task_read(repo: Repo, hash: String) → Result<TaskObject, Error>`

Read and parse a TaskObject.

### `task_materialize(repo: Repo, task_hash: String) → Result<(), Error>`

Ensure task's `bin/` directory is ready:
1. If `tasks/<hash>/bin/` exists, done
2. Create `tasks/<hash>/bin/`
3. Materialize `init_tree` files
4. Run `init` command (if present)

### `task_run(repo: Repo, task_hash: String, inputs: Array<String>, output_path: String) → Result<String, Error>`

Execute a task:
1. Compute input_hash from input content hashes
2. Check cache: `tasks/<task_hash>/executions/<input_hash>/output`
3. If cached, return cached result hash
4. Materialize task (if needed)
5. Run task command, capture stdout/stderr
6. Store result, write output ref
7. Return result hash

## Dataflow Execution

Dataflows connect dataset paths to tasks. Two variants: `task` (runs computation) and `shuffle` (reorganizes data).

### `dataflow_start(repo: Repo, ws: String, filter: Option<String>) → Result<(), Error>`

Execute dataflows in a workspace:

1. Read package's dataflows from PackageObject
2. Build dependency graph from input/output paths
3. Topologically sort dataflows
4. For each dataflow (respecting `filter`):

**Task dataflow execution:**
1. Expand globs in input paths via `dataset_traverse`
2. Group by glob indices to determine task instances
3. For each task instance:
   - Read input blobs from dataset
   - Run task (cache key = task_hash + input content hashes)
   - Write output blobs to dataset paths

**Shuffle dataflow execution:**
1. Traverse input path (with globs)
2. Reorganize entries according to output path structure
3. Write reorganized tree to output path

### `dataflow_expand(repo: Repo, ws: String, dataflow: DataflowDef) → Result<Array<TaskInstance>, Error>`

Expand a task dataflow into concrete task instances by resolving globs.

```ts
type TaskInstance = {
    task: String,
    inputs: Array<{ path: TreePath, hash: String }>,
    output: TreePath,
};
```

Example: If input path is `[.field "inputs", .field "regions", .glob]` and the dataset has regions `["us", "eu", "asia"]`, this produces three TaskInstances.

### `dataflow_start_watch(repo: Repo, ws: String, filter: Option<String>) → Result<(), Error>`

Like `dataflow_start`, but watches for input changes (via inotify) and re-runs affected dataflows. Only re-executes task instances whose inputs have changed.

## Registry

### `registry_add(repo: Repo, url: String) → Result<(), Error>`

Add a registry URL to `e3.east`.

### `registry_remove(repo: Repo, url: String) → Result<(), Error>`

Remove a registry URL.

### `registry_list(repo: Repo) → Array<String>`

List configured registries.

### `registry_fetch(repo: Repo, name: String, version: Option<String>) → Result<String, Error>`

Fetch a package from registries. Downloads `.zip` to temp, returns path.

### `registry_publish(repo: Repo, pkg_name: String, pkg_version: String) → Result<(), Error>`

Publish a package to the default registry.

### `registry_search(repo: Repo, query: String) → Result<Array<(String, String)>, Error>`

Search registries for packages matching query.
