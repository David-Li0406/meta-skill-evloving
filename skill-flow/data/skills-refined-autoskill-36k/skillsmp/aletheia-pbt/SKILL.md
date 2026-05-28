---
name: aletheia-pbt
description: Sub skill for pbt-workflow-guide. Apply Aletheia to generate and sync PBT templates/tests for any non-aletheia MoonBit repo.
---

# Aletheia PBT

## Overview

Apply Aletheia to a target MoonBit module or package to generate .pbt.md templates and sync them into per-package tests.

## Role in the Root Workflow

This is a sub skill of `pbt-workflow-guide`. Use it when the target repository is not `f4ah6o/aletheia.mbt`.

Use this skill to generate/sync templates. For property design details (generators, shrinking, state machines), use `pbt-workflow-guide`. For changes to Aletheia itself in this repo, use `aletheia-self-pbt`.

## Prerequisites & Installation

This skill assumes a working MoonBit toolchain. Aletheia is published on mooncakes.io, so you can install it directly:

```bash
moon add f4ah6o/aletheia
```

After installing, run the CLI from your target repo:

```bash
moon run f4ah6o/aletheia/aletheia -- analyze /path/to/target --explain
moon run f4ah6o/aletheia/aletheia -- generate /path/to/target
moon run f4ah6o/aletheia/aletheia -- sync /path/to/target
```

If you already have the aletheia.mbt repo locally, you can also run it from that repo with `moon run src/aletheia -- <subcommand> <path>`.

## Install & Run (Quickstart)

1. **Install**
   - From the target repo (where `moon.mod.json` lives), run `moon add f4ah6o/aletheia` to add the dependency.

2. **Run**
   - Execute from the target repo (`<path>` is a module root or package directory).

    ```bash
    moon run f4ah6o/aletheia/aletheia -- analyze <path> --explain
    moon run f4ah6o/aletheia/aletheia -- generate <path>
    moon run f4ah6o/aletheia/aletheia -- sync <path>
    ```

3. **Local run (using a dev checkout)**
   - In the aletheia.mbt repo, use `moon run src/aletheia -- <subcommand> <path>`.

## v0.4.0 Features

- **5 Pattern Types**: Round-Trip, Idempotent, Producer-Consumer, Invariant, and Oracle
- **State Machine Testing**: Support for stateful system testing with command generation
- **Enhanced Shrinking**: Advanced shrinking strategies for better counterexample analysis
- **Statistics Integration**: Built-in statistics for test insights
- **Size Parameter Control**: Configurable size parameters for recursive types

## Workflow

1. Choose a target path
   - Use a module root (contains moon.mod.json) or a package directory (contains moon.pkg.json).

2. Analyze patterns (optional)
   - `moon run src/aletheia -- analyze <path> --explain`
   - Shows detailed pattern detection with explanations

3. Generate templates
   - `moon run src/aletheia -- generate <path>`
   - CLI Options:
     - `--dry-run`: Preview without writing files
     - `--explain`: Output detection details
     - `--format <text|json>`: Output format (default: text)
   - Output path is `<module>.pbt.md` in the target root (derived from moon.mod.json).

4. Refine templates
   - Keep manual edits outside `<!-- aletheia:begin -->` / `<!-- aletheia:end -->`.
   - Leave code blocks as `mbt nocheck` until properties are validated; switch to `mbt check` afterward.
   - Use `@qc` (MoonBit QuickCheck) helpers for generators, shrinkers, and statistics.

5. Sync tests
   - `moon run src/aletheia -- sync [path]` (defaults to `<source>/<module>.pbt.md`).

Notes:
- If you still have `.pbt.mbt.md`, rename to `.pbt.md` to avoid MoonBit treating it as source.
- MoonBit-native `.mbt.md` is supported for sync when tests are in ` ```mbt test` / ` ```mbt check` blocks.

6. Verify
   - `moon info && moon fmt`
   - `moon test` (or `moon test --update` if snapshots change)

## Pattern Types

Aletheia automatically detects these patterns:

1. **Round-Trip**: encode/decode, serialize/deserialize
2. **Idempotent**: sort, normalize, trim
3. **Producer-Consumer**: Producer-consumer chains
4. **Invariant**: Collection invariants (Map, Filter, Sort)
5. **Oracle**: Implementation vs reference comparison
