# Code Analysis Strategies

Techniques for analyzing source code to verify design documentation accuracy.

## Overview

When syncing design docs with code, use these strategies to:

1. Verify referenced files exist
2. Check exports match documentation
3. Validate metrics have instrumentation
4. Track implementation of planned features
5. Identify architectural changes

## Strategy 1: File-based Verification

Verify files mentioned in docs exist and match documented structure.

### Find File References

Extract file paths from design doc:

```bash
# Extract TypeScript/JavaScript file paths
grep -o 'src/[^)]*\.[jt]sx\?' {doc} | sort -u

# Extract paths from all packages
grep -o 'pkgs/[^)]*\.[jt]sx\?' {doc} | sort -u
```

### Verify File Existence

Check each referenced file exists:

```bash
# For each extracted file path
for file in ${files[@]}; do
  if [ -f "{module-path}/${file}" ]; then
    echo "✅ ${file}"
  else
    echo "❌ ${file} - NOT FOUND"
  fi
done
```

### Strategy 1 Output Format

```text
File Verification Results:

✅ src/TypeRegistry.ts - Exists, 456 lines
✅ src/PackageFetcher.ts - Exists, 234 lines
❌ src/cache/DiskCache.ts - NOT FOUND
✅ src/observability/EventEmitter.ts - Exists, 234 lines
```

### Common Issues

**File deleted:**

```text
WARNING: Referenced file deleted
- Documented: src/cache/DiskCache.ts
- Reality: File does not exist
- Action: Check git history for deletion/move
```

**File moved:**

```text
UPDATE: File moved
- Documented: src/events.ts
- Reality: src/observability/EventEmitter.ts
- Action: Update path in documentation
```

## Strategy 2: Export Analysis

Compare documented exports with actual exports from entry point.

### Extract Documented Exports

Find what the doc claims is exported:

```bash
# Look for export lists in docs
grep -o 'exports:.*' {doc}
grep -o 'Main exports:.*' {doc}
```

### Get Actual Exports

Read actual exports from source code:

```bash
# Get all exports from index.ts
grep '^export' {module-path}/src/index.ts

# Get specific export names
grep -o 'export.*{.*}' {module-path}/src/index.ts
```

### Compare and Report

Generate comparison report:

```text
Export Verification:

Documented exports:
- TypeRegistry ✅
- PackageFetcher ✅

Actual exports:
- TypeRegistry (documented)
- PackageFetcher (documented)
- CacheStrategy (not documented ⚠️)
- EventEmitter (not documented ⚠️)

Missing from docs: CacheStrategy, EventEmitter
```

### Strategy 2 Update Suggestions

```text
UPDATE: Add new exports to documentation

**Current text:**
> Main exports: `TypeRegistry`, `PackageFetcher`

**Suggested update:**
> Main exports: `TypeRegistry`, `PackageFetcher`, `CacheStrategy`,
> `EventEmitter`

**Reason:** New exports added to src/index.ts
```

## Strategy 3: Metrics Verification

Verify documented metrics have actual instrumentation in code.

### Find Documented Metrics

Extract metric claims from docs:

```bash
# Look for metric patterns
grep -i 'cache hit rate' {doc}
grep -i 'performance' {doc}
grep -i 'latency' {doc}
grep -o '[0-9]+%' {doc}  # Find percentage claims
```

### Search for Instrumentation

Look for metric collection in code:

```bash
# Search for metrics collection
grep -r 'metrics\.' {module-path}/src
grep -r 'performance\.' {module-path}/src
grep -r 'counter\.' {module-path}/src
grep -r 'gauge\.' {module-path}/src
```

### Strategy 3 Verification Report

**Metric found:**

```text
✅ Metric verified: Cache hit rate
- Documented: "85% cache hit rate"
- Code: src/cache/metrics.ts:45 - cacheHitRate.record()
- Status: Instrumented
```

**Metric not found:**

```text
WARNING: Metric not verified
- Documented: "Cache hit rate: 85%"
- Code: No instrumentation found
- Action: Verify metric source or mark as outdated
```

## Strategy 4: API Signature Analysis

Verify function signatures match documentation.

### Find Documented Signatures

Extract function signatures from docs:

```text
Documented:
- fetchPackage(name: string)
- getTypes(packageName: string)
```

### Extract Actual Signatures

Use grep to find function declarations:

```bash
# Find function signatures
grep -n 'export.*function' {module-path}/src/{file}.ts
grep -n 'export.*async function' {module-path}/src/{file}.ts
```

### Compare Signatures

```text
UPDATE: Function signature changed

**Documented:**
```typescript
fetchPackage(name: string): Promise<Package>
```

**Actual:**

```typescript
fetchPackage(name: string, version?: string): Promise<Package>
```

**Action:** Update signature with new optional parameter

## Strategy 5: TODO Tracking

Match documented future work with TODOs in code.

### Find Code TODOs

Search for TODO comments:

```bash
# Find all TODOs with context
grep -rn 'TODO' {module-path}/src
grep -rn 'FIXME' {module-path}/src
grep -rn '@todo' {module-path}/src
```

### Match with Future Enhancements

Compare TODOs with documented future work:

```text
Future Enhancement Analysis:

Documented Future Work:
- Phase 2: Implement structured logging
- Phase 3: Add performance benchmarks

Code TODOs:
- src/Logger.ts:23 - TODO: Add structured logging ✅
- src/metrics.ts:45 - TODO: Benchmark cache performance ✅

Status:
- Phase 2 appears implemented (Logger.ts exists)
- Phase 3 in progress (metrics.ts has TODO)
```

### Strategy 5 Update Suggestion

```text
UPDATE: Mark completed phase

**Current text:**
> **Phase 2:** Implement structured logging

**Suggested update:**
Move to "Completed" section:
> **Phase 2 (Completed 2026-01-10):** Structured logging via Logger.ts

**Reason:** src/observability/Logger.ts exists and exports StructuredLogger
```

## Strategy 6: Architecture Verification

Verify documented architecture matches actual file structure.

### Find Documented Components

Extract component structure from docs:

```text
Documented Architecture:
- Type Registry (core)
- Package Fetcher (external)
- Cache Layer (optimization)
- Observability (monitoring)
```

### Analyze Actual Structure

Use directory structure and imports:

```bash
# Get directory structure
find {module-path}/src -type d

# Get main components (top-level files)
ls {module-path}/src/*.ts

# Check for undocumented directories
```

### Strategy 6 Comparison Report

```text
Architecture Verification:

Documented Components:
✅ Type Registry (src/TypeRegistry.ts)
✅ Package Fetcher (src/PackageFetcher.ts)
✅ Observability (src/observability/)
⚠️  Cache Layer - not found as documented

Actual Components:
✅ TypeRegistry (documented)
✅ PackageFetcher (documented)
✅ Observability (documented)
⚠️  CacheStrategy - exists but not documented

Missing from docs: CacheStrategy abstraction
```

## Strategy 7: Dependency Analysis

Verify package.json dependencies match documentation.

### Extract Documented Dependencies

Find dependency mentions in docs:

```bash
# Look for dependency mentions
grep -i 'dependencies:' {doc}
grep -i 'requires:' {doc}
grep -i 'peer.*dependency' {doc}
```

### Read Actual Dependencies

Parse package.json:

```bash
# Get dependencies
jq '.dependencies' {module-path}/package.json

# Get peer dependencies
jq '.peerDependencies' {module-path}/package.json
```

### Strategy 7 Update Suggestion

```text
UPDATE: Add new dependency

**Current text:**
> Dependencies: none (pure Effect-TS)

**Suggested update:**
> Dependencies:
> - Effect-TS (runtime)
> - pino (logging, optional peer dependency)

**Reason:** package.json shows pino as peerDependency
```

## Strategy 8: Line Count Estimation

Update documented line counts with actual counts.

### Get Line Counts

```bash
# Count lines in specific files
wc -l {module-path}/src/{file}.ts

# Count lines in directories
find {module-path}/src/observability -name '*.ts' -exec wc -l {} + | tail -1
```

### Strategy 8 Update Format

```text
UPDATE: Update line count

**Current text:**
> The observability system is ~500 lines of code

**Suggested update:**
> The observability system is ~687 lines of code

**Reason:** Current file sizes:
- EventEmitter.ts: 234 lines
- Logger.ts: 189 lines
- Metrics.ts: 264 lines
```

## Combining Strategies

Use multiple strategies together for comprehensive sync:

### Analysis Workflow

1. **File verification** - Ensure all referenced files exist
2. **Export analysis** - Check for new/removed exports
3. **API signatures** - Verify function signatures
4. **Metrics verification** - Validate performance claims
5. **TODO tracking** - Match future work with code
6. **Architecture check** - Verify component structure
7. **Dependencies** - Check package.json changes
8. **Line counts** - Update size estimates

### Comprehensive Report

```markdown
## Verification Details

### Files Verified (8)

1. ✅ src/TypeRegistry.ts - Exists, 456 lines
2. ✅ src/PackageFetcher.ts - Exists, 234 lines
3. ❌ src/cache/DiskCache.ts - Not found
4. ✅ src/observability/EventEmitter.ts - Exists, 234 lines

### Exports Verified

**From src/index.ts:**

- TypeRegistry (documented ✅)
- PackageFetcher (documented ✅)
- CacheStrategy (not documented ⚠️)

### Architecture Match

- ✅ Type Registry system
- ✅ Package Fetcher
- ✅ Observability system
- ⚠️  Cache Strategy abstraction (not documented)

### Dependencies

- ✅ Effect-TS (documented)
- ⚠️  pino (not documented, added as peerDependency)
```

## Error Prevention

### False Positives

**Old file paths in examples:**

Don't flag code examples or historical references as errors.

```text
Context check:
- Line mentions file in "Historical context" section
- Skip: Not a current reference
```

**Alternative implementations:**

Files may have different names but same functionality.

```text
Context check:
- Documented: src/cache/DiskCache.ts
- Git history shows: Renamed to src/cache/Cache.ts
- Action: Update path, not deletion
```

### Git History Integration

Use git to understand changes:

```bash
# Find when file was deleted/moved
git log --all --full-history -- "**/DiskCache.ts"

# Find file renames
git log --follow --all -- {file}

# Check recent changes
git log --since="30 days ago" -- {module-path}/src
```

## Success Criteria

A thorough analysis:

- ✅ All file references checked
- ✅ Exports verified against source
- ✅ Metrics validated with instrumentation
- ✅ API signatures compared
- ✅ Architecture structure verified
- ✅ Dependencies matched with package.json
- ✅ Clear discrepancy report generated
- ✅ Git history consulted for context
