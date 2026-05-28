---
name: nuke-build-system
description: Comprehensive task execution through a C# DSL build system - NUKE. Use when restoring dependencies, building projects, publishing artifacts, building OCI images, cleaning-up artifacts or doing other project related tasks.
license: MIT
compatibility: opencode, claude code, copilot
metadata:
    author: Vasil Kotsev
    audience: contributors
    version: "1.0.0"
---

# NUKE Build System

Use the `NUKE` build system for carrying out various build related tasks,
such as restoring dependencies, building projects, cleaning-up artifacts,
evaluating automation test suites and others.

## Checks

Detect if the `NUKE` build system is setup by checking if the following files &
directories exist:

- `../../../build.sh`
- `../../../build.ps1`
- `../../../build/`
- `../../../.nuke/`

If the build system is setup, proceed forward. If not - ignore this skill and revert
to the `dotnet CLI`.

## When to Apply

Leverage the `NUKE` build system whenever you assess that an applicable target
should be invoked (e.g, `clean`, `restore`, `build`). Consider it as the go-to-build
toolchain for this repository.

**Evaluate** `NUKE` targets when:

- Code changes have been made across multiple `C#` assemblies
- You need to evaluate all `unit` or `integration` tests
- All build artifacts should be cleaned-up
- A Docker image needs to be built locally
- You need to ensure that all projects are built successfully, without
  compilation errors
- ORM migrations need to be `created`, `removed` or `applied`

**Revert** to standard `dotnet CLI` operations when:

- You need to verify that a single assembly compiles successfully
- A single `unit` / `integration` test scenario needs to be evaluated
- Code changes impact only a single `C#` assembly

## How to Use

In order to evaluate targets from the `NUKE` build system you must either use
the global `nuke.globaltool` `dotnet CLI` tool or one of the following bootstrap
scripts:

```sh
# Bootstrap script for Unix environments.
../../../build.sh --help

```

```powershell
# Bootstrap script for WinNT environments.
..\..\..\build.ps1 --help
```

Prefer to use the `nuke` global dotnet CLI tool, if it's installed, via:

```sh
nuke --help
```

If it's not - prompt the user to install it:

```sh
dotnet tool install -g nuke.globaltool
```

## Examples

For usage examples, see [examples.md](./examples.md);

## Target Implementations

If you wish to reference the actual target implementations, you can review
the docs in `../../../build/Components/`. The default target an be found
in `../../../build/Build.cs`.
