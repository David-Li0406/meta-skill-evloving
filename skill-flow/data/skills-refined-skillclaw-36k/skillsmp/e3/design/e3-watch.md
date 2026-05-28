# e3 watch: Live Development Command

This document specifies the `e3 watch` command for live package development.

## Overview

The `watch` command enables a live development workflow where changes to a TypeScript package definition file are automatically imported and deployed to a workspace when the file is saved.

## Command Syntax

```bash
e3 watch <repo> <workspace> <source.ts>
```

### Arguments

| Argument | Description |
|----------|-------------|
| `repo` | Path to e3 repository (`.` for current directory) |
| `workspace` | Target workspace name (created if it doesn't exist) |
| `source.ts` | Path to TypeScript file with default export of `PackageDef` |

### Options

| Option | Description |
|--------|-------------|
| `--start` | Also execute dataflow after each deploy |
| `--concurrency <n>` | Max concurrent tasks when using `--start` (default: 4) |
| `--abort-on-change` | Abort running execution when file changes (default: queue reload) |

## Source File Requirements

The watched TypeScript file must have a default export that is a `PackageDef`:

```ts
// my-package.ts
import e3 from '@elaraai/e3';
import { StringType } from '@elaraai/east';

const input_name = e3.input('name', StringType, 'World');

const say_hello = e3.task(
  'say_hello',
  [input_name],
  ($, name) => `Hello, ${name}!`
);

const pkg = e3.package('hello-world', '1.0.0', say_hello);

export default pkg;
```

## Behavior

### Initial Load

1. Resolve repository path
2. Create workspace if it doesn't exist
3. Import the TypeScript file using dynamic `import()`
4. Validate the default export is a `PackageDef`
5. Export the package to a temporary zip
6. Import the zip into the repository
7. Deploy the package to the workspace
8. If `--start` specified, execute the dataflow

### On File Change

1. Detect file modification via `fs.watch()`
2. Clear the module cache for the source file (and its dependencies)
3. Re-import the TypeScript file
4. Validate the default export
5. Compare package name/version with currently deployed
6. Export, import, and re-deploy
7. If `--start` specified, execute the dataflow

### Concurrent Save Handling

If a file is saved while a dataflow is executing:

1. **Queue the reload**: Mark that a reload is pending
2. **Wait for current execution**: Let the current dataflow complete (or abort on error)
3. **Process queued reload**: After completion, reload and redeploy
4. **Coalesce multiple saves**: If saved multiple times while executing, only reload once

```
[12:34:56] Starting dataflow...
  [START] slow_task
[12:34:58] File changed (queued, execution in progress)
[12:35:00] File changed (queued, execution in progress)
  [DONE] slow_task [5000ms]
[12:35:01] Processing queued reload...
[12:35:01] Loaded: hello-world@1.0.1
[12:35:01] Deployed to workspace: dev
[12:35:01] Starting dataflow...
```

With `--abort-on-change`, the running execution is cancelled immediately and a fresh reload starts.

### Error Handling

- **TypeScript compilation errors**: Display error, keep watching
- **Runtime errors in package definition**: Display error, keep watching
- **Invalid export**: Display error explaining expected format, keep watching
- **Import/deploy errors**: Display error, keep watching

The watch process should be resilient and continue watching after errors.

## Implementation Details

### Module Cache Invalidation

Node.js caches imported modules. To reload a changed file:

```ts
// For ESM modules, use a cache-busting query param
const module = await import(`${absolutePath}?update=${Date.now()}`);
```

### File Watching

Use `fs.watch()` with debouncing to handle rapid saves:

```ts
import { watch } from 'node:fs';

let debounceTimer: NodeJS.Timeout;
watch(sourcePath, () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => reload(), 100);
});
```

### TypeScript Execution

Use `typescript` to transpile and `vm` to execute, similar to `east-ui-extension`.

Automatically inherit the user's `tsconfig.json` using TypeScript's built-in APIs:

```ts
import ts from 'typescript';
import * as vm from 'vm';
import Module from 'module';
import * as path from 'path';
import * as fs from 'fs';

function loadCompilerOptions(filePath: string): ts.CompilerOptions {
  const searchPath = path.dirname(filePath);

  // Find tsconfig.json starting from the source file's directory
  const configPath = ts.findConfigFile(searchPath, ts.sys.fileExists, 'tsconfig.json');

  if (configPath) {
    // Read and parse tsconfig.json (handles "extends" automatically)
    const configFile = ts.readConfigFile(configPath, ts.sys.readFile);
    const parsed = ts.parseJsonConfigFileContent(
      configFile.config,
      ts.sys,
      path.dirname(configPath)
    );
    return {
      ...parsed.options,
      // Override module to CommonJS for vm execution
      module: ts.ModuleKind.CommonJS,
    };
  }

  // Fallback defaults if no tsconfig found
  return {
    module: ts.ModuleKind.CommonJS,
    target: ts.ScriptTarget.ES2022,
    esModuleInterop: true,
    strict: true,
  };
}

async function loadPackageFile(filePath: string): Promise<PackageDef> {
  const tsCode = fs.readFileSync(filePath, 'utf-8');
  const compilerOptions = loadCompilerOptions(filePath);

  // Transpile TypeScript to JavaScript
  const result = ts.transpileModule(tsCode, {
    compilerOptions,
    fileName: filePath,
  });

  // Create require that resolves from user's project directory
  const userRequire = Module.createRequire(filePath);

  // Execute in VM context
  const module = { exports: {} as Record<string, unknown> };
  const context = vm.createContext({
    module,
    exports: module.exports,
    require: userRequire,
    console,
    Buffer,
    process,
    __dirname: path.dirname(filePath),
    __filename: filePath,
  });

  vm.runInContext(result.outputText, context, { filename: filePath });

  // Get default export
  const defaultExport = module.exports.default ?? module.exports;

  // Validate it's a PackageDef
  if (!defaultExport || defaultExport.kind !== 'package') {
    throw new Error('Default export must be a PackageDef (created with e3.package())');
  }

  return defaultExport as PackageDef;
}
```

This approach:
- Uses `ts.findConfigFile()` to locate the user's `tsconfig.json`
- Uses `ts.parseJsonConfigFileContent()` to handle `extends` chains
- Uses `Module.createRequire(filePath)` so the user's `node_modules` are resolved
- Works with any TypeScript project that has `@elaraai/e3` installed
- No need for tsx or ts-node

### Temporary Files

Use OS temp directory for intermediate zip files:

```ts
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const tempZip = join(tmpdir(), `e3-watch-${Date.now()}.zip`);
```

Clean up temp files on exit.

## Example Usage

### Basic Watch

```bash
# Watch and deploy on save
e3 watch . dev ./src/my-package.ts
```

### Watch with Auto-Start

```bash
# Watch, deploy, and execute on save
e3 watch . dev ./src/my-package.ts --start
```

### With TypeScript Loader

```bash
# Using tsx for TypeScript support
node --import tsx $(which e3) watch . dev ./src/my-package.ts --start
```

## Output Format

```
Watching: ./src/my-package.ts
Target workspace: dev

[12:34:56] Initial load...
[12:34:56] Loaded: hello-world@1.0.0
[12:34:56] Exported to temp file
[12:34:56] Imported: 5 objects
[12:34:56] Deployed to workspace: dev
[12:34:56] Ready. Waiting for changes...

[12:35:10] File changed, reloading...
[12:35:10] Loaded: hello-world@1.0.0
[12:35:10] Deployed to workspace: dev
[12:35:10] Starting dataflow...
  [START] say_hello
  [DONE] say_hello [52ms]
[12:35:10] Done. Waiting for changes...

[12:36:00] File changed, reloading...
[12:36:00] Error: Cannot find module './utils'
[12:36:00] Waiting for changes...
```

## Signal Handling

- **SIGINT (Ctrl+C)**: Clean up temp files and exit gracefully
- **SIGTERM**: Same as SIGINT

## Future Considerations

### Dependency Watching

Currently only watches the main file. Could extend to watch imported dependencies:

```bash
e3 watch . dev ./src/my-package.ts --watch-deps
```

### Hot Reload Input Data

Could watch input data files and auto-set datasets:

```bash
e3 watch . dev ./src/my-package.ts --inputs ./data/
```

### Multiple Packages

Could watch a directory and deploy multiple packages:

```bash
e3 watch . dev ./src/packages/
```
