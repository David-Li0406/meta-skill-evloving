---
name: observability
description: Best practices for structured logging, correlation IDs, performance metrics, and debugging in Bun applications using @sidequest/core/logging and LogTape. Use when implementing logging, setting up observability, debugging production issues, tracking performance metrics, adding correlation IDs, configuring subsystem loggers, or working with JSONL log analysis. Covers plugin logger factory, hierarchical categories, log levels, metrics collection, and operational debugging workflows.
allowed-tools: Read, Grep, Glob
---

# Observability

Production-grade logging, metrics, and debugging patterns using @sidequest/core/logging (LogTape + JSONL).

## Quick Navigation

- **[Core Concepts](#core-concepts)** - Correlation IDs, subsystem loggers, JSONL output
- **[Plugin Logger Setup](#plugin-logger-setup)** - Factory pattern, hierarchical categories
- **[Log Levels & Best Practices](#log-levels--best-practices)** - When to use DEBUG/INFO/WARN/ERROR
- **[Correlation ID Patterns](#correlation-id-patterns)** - Request tracing, operation tracking
- **[Performance Metrics](#performance-metrics)** - Automatic aggregation, session summaries
- **[Debugging Workflows](#debugging-workflows)** - grep patterns, jq queries, troubleshooting
- **[Testing](#testing)** - Log assertions, metrics validation
- **[Common Patterns](#common-patterns)** - Real-world examples
- **[Related Skills](#related-skills)** - Bun CLI, Bun Runtime

---

## Core Concepts

### Structured Logging with LogTape

**Why LogTape:** JSONL format enables programmatic analysis, grep filtering, and long-term storage.

**Log Location:** `~/.claude/logs/<plugin-name>.jsonl`

**Key Features:**
- JSONL (newline-delimited JSON) for machine parsing
- File rotation (1 MiB default, keeps 5 files)
- Hierarchical categories (plugin → subsystem)
- Tagged template literals for clean syntax
- Automatic timestamp, level, logger metadata

### Hierarchical Categories

```typescript
// Category hierarchy: [plugin, subsystem, ...submodule]
["para-obsidian"]                    // Root plugin logger
["para-obsidian", "inbox"]           // Inbox subsystem
["para-obsidian", "inbox", "pdf"]    // PDF submodule (if needed)

// Enables grep filtering:
// grep '"logger":"para-obsidian.inbox"' ~/.claude/logs/para-obsidian.jsonl
```

**Benefits:**
- Filter logs by subsystem
- Different log levels per category
- Trace operations across subsystems

### Correlation IDs

**Purpose:** Link related log entries across subsystems for request tracing.

```typescript
import { createCorrelationId } from "@sidequest/core/logging";

const cid = createCorrelationId(); // "a1b2c3d4" (8 chars)

// Pass cid through operation chain
inboxLogger.info`Scan started cid=${cid}`;
pdfLogger.debug`Extracting file cid=${cid}`;
llmLogger.info`Detection complete cid=${cid}`;
executeLogger.info`Note created cid=${cid}`;

// Later: grep cid=a1b2c3d4 to see full trace
```

---

## Plugin Logger Setup

### Factory Pattern

**ALWAYS use `createPluginLogger()` from `@sidequest/core/logging`:**

```typescript
// plugins/my-plugin/src/logger.ts
import {
  createCorrelationId,
  createPluginLogger,
} from "@sidequest/core/logging";

const {
  initLogger,
  rootLogger,
  getSubsystemLogger,
  subsystemLoggers,
  logFile,
} = createPluginLogger({
  name: "my-plugin",           // kebab-case (used for log file)
  subsystems: ["scraper", "auth", "api"],
  // Prefer vault-synced logs for user visibility:
  // logDir: `${process.env.PARA_VAULT}/.claude/logs` or a plugin-specific env override
});

// Export for use across plugin
export { createCorrelationId, initLogger, logFile, rootLogger };

// Named subsystem loggers
export const scraperLogger = subsystemLoggers.scraper;
export const authLogger = subsystemLoggers.auth;
export const apiLogger = subsystemLoggers.api;
```

**Parameters:**
| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `name` | ✅ | — | Plugin name (kebab-case), used for log file |
| `subsystems` | ❌ | `[]` | Subsystem names for hierarchical logging |
| `logDir` | ❌ | `~/.claude/logs` | Log directory path |
| `logFileName` | ❌ | `name` | Log file name (without extension) |
| `maxSize` | ❌ | 1 MiB | Max file size before rotation |
| `maxFiles` | ❌ | 5 | Number of rotated files to keep |
| `lowestLevel` | ❌ | `"debug"` | Minimum log level |

### Initialization

**ALWAYS call `initLogger()` before logging:**

```typescript
// In CLI entry point or MCP server startup
import { initLogger, scraperLogger } from "./logger";

async function main() {
  await initLogger(); // Creates log dir, configures LogTape

  scraperLogger.info`Application started`;
  // ... rest of app
}

main();
```

**Why:**
- Creates log directory if missing
- Configures LogTape sinks and formatters
- Logs initialization event (plugin, logDir, maxSize)
- Safe to call multiple times (only initializes once)
**Recommended:** Emit a one-time “logger initialized” INFO with `logFile`, `logDir`, and `lowestLevel` so users can confirm where JSONL is written (especially when overriding to a vault-synced path).

### Subsystem Logger Naming

**Convention:** Match subsystem name to functional area:

| Plugin | Subsystems | Use Cases |
|--------|------------|-----------|
| **cinema-bandit** | `scraper`, `pricing`, `auth`, `gmail` | Functional modules |
| **kit** | `ast`, `semantic`, `git` | Tool categories |

**Anti-pattern:** Don't use generic names like "utils", "helpers", "common"

---

## Log Levels & Best Practices

### Level Guidelines

```typescript
// DEBUG: Detailed diagnostic info (verbose, expensive operations)
pdfLogger.debug`Trying selector attempt=${attempt} selector="${sel}"`;
pdfLogger.debug`Hash calculated file=${filename} hash=${hash} duration=${ms}ms`;

// INFO: Normal operation events (milestones, counts, timing)
inboxLogger.info`Scan started vault=${vaultPath} cid=${cid}`;
scraperLogger.info`Scrape complete movies=${count} duration=${ms}ms`;

// WARN: Degraded operation (fallbacks, edge cases, soft failures)
inboxLogger.warn`Skipping already processed: ${filename}`;
llmLogger.warn`LLM detection failed, using fallback confidence`;

// ERROR: Operation failures (exceptions, validation errors)
executeLogger.error`Failed to create note: ${error.message} cid=${cid}`;
authLogger.error`OAuth token refresh failed: ${error}`;
```

### Logging Patterns

#### Pattern 1: Operation Tracing (Start → Complete)

```typescript
const cid = createCorrelationId();
const startTime = Date.now();

scraperLogger.info`Scrape started url=${url} cid=${cid}`;

try {
  const result = await scrape(url);
  const duration = Date.now() - startTime;

  scraperLogger.info`Scrape complete movies=${result.length} duration=${duration}ms cid=${cid}`;

  return result;
} catch (error) {
  const duration = Date.now() - startTime;

  scraperLogger.error`Scrape failed error=${error.message} duration=${duration}ms cid=${cid}`;

  throw error;
}
```

**Benefits:**
- Trace operation lifecycle
- Measure performance (duration)
- Link failure to operation start (cid)

#### Pattern 2: Conditional Debug Logging

```typescript
// Expensive operations - log at DEBUG level
for (const selector of selectors) {
  pdfLogger.debug`Trying selector="${selector}"`;

  const element = await page.locator(selector).first();

  if (await element.isVisible()) {
    pdfLogger.debug`Selector matched="${selector}"`;
    return element;
  }
}

pdfLogger.warn`No selectors matched - using fallback`;
```

**Why:** DEBUG logs can be voluminous; use INFO for successes.

#### Pattern 3: Structured Logging (Recommended)

**Use structured logs with properties object instead of template literals:**

```typescript
// ✅ GOOD: Structured format with properties object
inboxLogger.info("Bookmark enrichment started", {
  event: "enrichment_started",
  sessionCid,
  cid,
  parentCid,
  file: file.filename,
  url,
  timestamp: new Date().toISOString(),
});

// ❌ BAD: Template literal (harder to query)
inboxLogger.info`Bookmark enrichment started file=${file.filename} url=${url}`;
```

**Benefits:**
- Easier jq queries: `jq 'select(.properties.event == "enrichment_started")'`
- Consistent field structure across logs
- Type safety with TypeScript
- Better for automated analysis

**Queryable later:**
```bash
# Find all enrichment operations
jq 'select(.properties.event == "enrichment_started")' ~/.claude/logs/para-obsidian.jsonl

# Find operations by template type
jq 'select(.properties.template == "invoice")' ~/.claude/logs/para-obsidian.jsonl

# Find slow operations
jq 'select(.properties.durationMs > 1000)' ~/.claude/logs/para-obsidian.jsonl
```

**Event naming convention:**
```typescript
// Use snake_case for event names
"scan_started", "scan_complete"       // Operation lifecycle
"file_processing_started"              // File operations
"enrichment_started", "enrichment_ended"  // Sub-operations
"pdf_extraction_complete"              // Specific tasks
```

**PII safety:** When logs sync to cloud storage, mask or omit sensitive extracted fields (names, amounts, IDs) before logging. Prefer short summaries or hashed values over raw content.

### Log Level Convention Table

| Level | Volume | Use Case | Example |
|-------|--------|----------|---------|
| **DEBUG** | High | Detailed diagnostics, loops, retries | Selector attempts, hash calculations |
| **INFO** | Medium | Milestones, summaries, timing | Scan started/complete, item counts |
| **WARN** | Low | Degraded operation, edge cases | Skipped files, fallback logic |
| **ERROR** | Very Low | Operation failures, exceptions | Create failed, validation error |

---

## Correlation ID Patterns

### OpenTelemetry-Compatible Three-Tier Hierarchy

**Based on W3C Trace Context specification, used in production at para-obsidian:**

```typescript
// Three-tier ID hierarchy for distributed tracing:
// 1. sessionCid (trace_id): Session-level identifier - present in ALL logs
// 2. cid (span_id): Unique operation identifier for each logical unit of work
// 3. parentCid (parent_span_id): Links child operations to their parent
```

**Example hierarchy:**
```
acdfe223 (Session: para scan, 3.2s)
├─ e400fff2: inbox:scan (parent: acdfe223)
│  ├─ df2b9fd7: inbox:processPdf (parent: e400fff2, session: acdfe223)
│  ├─ eae519bd: enrich:bookmark (parent: e400fff2, session: acdfe223)
│  └─ 45c84df0: inbox:skipFastPath (parent: e400fff2, session: acdfe223)
```

### Pattern 1: Session-Level Tracking (Recommended)

**Use when:** You have a top-level operation (CLI command, MCP request) that spawns multiple sub-operations.

```typescript
// Interface for context passing
interface ProcessFileContext {
  /** Session-level correlation ID for linking scan → execute operations */
  sessionCid: string;
  /** Parent correlation ID (scan's CID) for trace hierarchy */
  parentCid: string;
  file: InboxFile;
  // ... other fields
}

async function scan(options?: ScanOptions) {
  // Create session-level CID once at top level
  const sessionCid = createCorrelationId();
  const cid = createCorrelationId(); // This operation's CID

  inboxLogger.info("Scan started", {
    event: "scan_started",
    sessionCid,
    cid,
    vault: vaultPath,
    timestamp: new Date().toISOString(),
  });

  // Pass BOTH sessionCid and parentCid to all sub-operations
  for (const file of files) {
    await processSingleFile({
      sessionCid,      // ✅ Same for entire session
      parentCid: cid,  // ✅ This scan's CID becomes parent
      file,
      // ... other context
    });
  }

  inboxLogger.info("Scan complete", {
    event: "scan_complete",
    sessionCid,
    cid,
    processed: files.length,
    durationMs: Date.now() - startTime,
    timestamp: new Date().toISOString(),
  });
}

async function processSingleFile(ctx: ProcessFileContext) {
  const { sessionCid, parentCid, file } = ctx;
  const cid = createCorrelationId(); // New CID for this file

  // Include ALL three IDs in structured logs
  pdfLogger.info("File processing started", {
    event: "file_processing_started",
    sessionCid,    // ✅ Links back to session
    cid,           // ✅ This operation's ID
    parentCid,     // ✅ Links to parent scan
    file: file.name,
  });

  // Pass to enrichment pipeline
  await enrichmentPipeline.processFile(file, {
    sessionCid,
    cid,
    parentCid,  // ✅ Current operation becomes parent for enrichment
  });
}
```

**Benefits:**
- ✅ End-to-end traceability across async operations
- ✅ Can trace all operations for a session: `grep sessionCid=acdfe223`
- ✅ Can see parent-child relationships: `grep parentCid=e400fff2`
- ✅ Compatible with OpenTelemetry for future integration

### Pattern 2: Per-Item Tracking (Legacy, Not Recommended)

**Use when:** Simple scripts without session concept.

```typescript
for (const file of files) {
  const itemCid = createCorrelationId(); // Unique cid per item

  try {
    pdfLogger.info`Processing file=${file} cid=${itemCid}`;

    const text = await extractPdf(file, itemCid);
    const type = await detectType(text, itemCid);

    pdfLogger.info`Processed file=${file} type=${type} cid=${itemCid}`;
  } catch (error) {
    pdfLogger.error`Failed file=${file} error=${error.message} cid=${itemCid}`;
  }
}
```

**Limitation:** Cannot trace operations back to originating session.

### Grep Debugging Workflow (Three-Tier IDs)

```bash
# Find all operations for a session
grep 'sessionCid=acdfe223' ~/.claude/logs/para-obsidian.jsonl

# Find all children of a specific operation
grep 'parentCid=e400fff2' ~/.claude/logs/para-obsidian.jsonl

# Find a specific operation and its children
grep -E '(cid=e400fff2|parentCid=e400fff2)' ~/.claude/logs/para-obsidian.jsonl

# Timeline view with full trace context
grep 'sessionCid=acdfe223' ~/.claude/logs/para-obsidian.jsonl | \
  jq -r '."@timestamp" + " | " + (.properties.cid // "N/A") + " | " + (.properties.parentCid // "N/A") + " | " + .message'

# Build hierarchy tree (requires jq post-processing)
grep 'sessionCid=acdfe223' ~/.claude/logs/para-obsidian.jsonl | \
  jq -s 'group_by(.properties.parentCid) |
         map({parent: .[0].properties.parentCid, children: map(.properties.cid)})'
```

**Legacy single-CID workflow:**
```bash
# Find all logs for a specific operation (old pattern)
grep 'cid=a1b2c3d4' ~/.claude/logs/my-plugin.jsonl

# Pretty-print as JSON
grep 'cid=a1b2c3d4' ~/.claude/logs/my-plugin.jsonl | jq .

# Extract only messages
grep 'cid=a1b2c3d4' ~/.claude/logs/my-plugin.jsonl | jq -r '.message'

# Timeline view (timestamp + message)
grep 'cid=a1b2c3d4' ~/.claude/logs/my-plugin.jsonl | \
  jq -r '."@timestamp" + " | " + .level + " | " + .message'
```

---

## Performance Metrics

### Automatic Metrics Collection

**`MetricsCollector`** aggregates durationMs from logs automatically:

```typescript
import { MetricsCollector } from "@sidequest/core/logging";

// In Stop hook or session end
const collector = new MetricsCollector();
await collector.collect(); // Parses ~/.claude/logs/*.jsonl

const summary = collector.getSummary();

console.log(summary.toMarkdown());
```

**Include summaries in CLI/JSON output:** After a run, return or print `{ metrics: summary, logFile }` so users and automation can locate performance data and the corresponding JSONL file.

**Output:**
```
═══════════════════════════════════════════════════════════════
📊 MCP Performance Metrics - Session Summary
═══════════════════════════════════════════════════════════════

Total Operations: 150
Successful: 145 (96.7%)
Failed: 5 (3.3%)
Total Duration: 45.2s

───────────────────────────────────────────────────────────────
Tool Name                   Calls  Avg Time   Min    Max  Errors
───────────────────────────────────────────────────────────────
kit_index_find                 25    12ms      8ms   45ms     0
bun_runTests                   10  1250ms   980ms 1.5s      2
biome_lintCheck                 8   180ms   120ms  250ms     0
───────────────────────────────────────────────────────────────

Slowest Operations:
1. bun_runTests (1.5s)
2. semantic_search (980ms)
...
```

### Manual Metrics Logging

**For custom metrics, log `durationMs` property:**

```typescript
const startTime = Date.now();

try {
  const result = await operation();
  const durationMs = Date.now() - startTime;

  scraperLogger.info`Operation complete`, {
    tool: "scraper_fetch",
    durationMs,
    success: true,
    cid,
  };

  return result;
} catch (error) {
  const durationMs = Date.now() - startTime;

  scraperLogger.error`Operation failed`, {
    tool: "scraper_fetch",
    durationMs,
    success: false,
    cid,
  };

  throw error;
}
```

**MetricsCollector** automatically aggregates:
- Call counts
- Min/max/avg latency
- Error rates
- Success rates

### Querying Metrics Manually

```bash
# Average duration for a specific tool
jq 'select(.properties.tool == "kit_index_find") | .properties.durationMs' \
  ~/.claude/logs/kit.jsonl | \
  awk '{sum+=$1; count++} END {print sum/count " ms"}'

# Count errors vs successes
jq 'select(.properties.tool == "bun_runTests") | .properties.success' \
  ~/.claude/logs/bun-runner.jsonl | \
  sort | uniq -c

# Find slow operations (>1s)
jq 'select(.properties.durationMs > 1000)' ~/.claude/logs/*.jsonl
```

---

## Debugging Workflows

### Common Grep Patterns

```bash
# All errors in last session
grep '"level":"error"' ~/.claude/logs/my-plugin.jsonl | tail -20

# Trace specific file processing
grep 'file=invoice-123.pdf' ~/.claude/logs/para-obsidian.jsonl

# Find all WARNING + ERROR messages
grep -E '"level":"(warn|error)"' ~/.claude/logs/my-plugin.jsonl

# Operations taking >1s
jq 'select(.properties.durationMs > 1000)' ~/.claude/logs/*.jsonl
```

### JQ Analysis Patterns

```bash
# Group errors by type
jq -s 'group_by(.properties.error) |
       map({error: .[0].properties.error, count: length})' \
  ~/.claude/logs/my-plugin.jsonl

# Summarize by log level
jq -s 'group_by(.level) |
       map({level: .[0].level, count: length})' \
  ~/.claude/logs/my-plugin.jsonl

# Timeline view with correlation IDs
jq -r '."@timestamp" + " | " + .properties.cid + " | " + .message' \
  ~/.claude/logs/my-plugin.jsonl
```

**Discipline:** Ensure every log in the flow carries `cid` (including skips, hash failures, LLM errors, and execute failures) so traces stay contiguous.

### Production Debugging Checklist

When debugging production issues:

- [ ] Identify error time range (timestamps)
- [ ] Extract correlation ID from error log
- [ ] Grep all logs for that correlation ID
- [ ] Trace operation from start → error
- [ ] Check for WARNings before ERROR (degraded state)
- [ ] Measure duration (did it timeout?)
- [ ] Check subsystem logs (pdf, llm, execute)
- [ ] Look for patterns (multiple similar errors)
- [ ] Extract error properties (file, type, etc.)
- [ ] Check metrics for performance degradation

---

## Testing

### Log Assertions in Tests

```typescript
import { describe, expect, test, beforeEach, afterEach } from "bun:test";
import { initLogger, scraperLogger } from "./logger";

describe("Scraper", () => {
  beforeEach(async () => {
    await initLogger();
  });

  test("logs scrape started", async () => {
    // Note: LogTape logs are async - test functional behavior, not logs
    // Direct log assertions are fragile; test observable effects instead

    const result = await scrape(url);

    // Test result, not logs
    expect(result).toBeDefined();
    expect(result.length).toBeGreaterThan(0);
  });
});
```

**Recommendation:** Test functional behavior, not log output. Logs are for observability, not assertions.

### Metrics Validation

```typescript
test("MetricsCollector aggregates correctly", () => {
  const collector = new MetricsCollector();

  collector.recordOperation("tool_a", 100, true);
  collector.recordOperation("tool_a", 200, true);
  collector.recordOperation("tool_b", 50, false);

  const summary = collector.getSummary();

  expect(summary.totalOperations).toBe(3);
  expect(summary.successfulOperations).toBe(2);
  expect(summary.failedOperations).toBe(1);

  const toolA = summary.toolMetrics.find(m => m.tool === "tool_a");
  expect(toolA?.avgDurationMs).toBe(150);
  expect(toolA?.successRate).toBe(100);
});
```

---

## Common Patterns

### Pattern 1: Subsystem Logger Per Module

```typescript
// plugins/my-plugin/src/scraper.ts
import { scraperLogger, createCorrelationId } from "./logger";

export async function scrapeMovies(url: string) {
  const cid = createCorrelationId();

  scraperLogger.info`Scrape started url=${url} cid=${cid}`;

  // ... scraping logic

  scraperLogger.info`Scrape complete count=${movies.length} cid=${cid}`;

  return movies;
}
```

### Pattern 2: Fallback Chains with Logging

```typescript
async function trySelectors(page, selectors) {
  for (const selector of selectors) {
    pdfLogger.debug`Trying selector="${selector}"`;

    const element = await page.locator(selector).first();

    if (await element.isVisible()) {
      pdfLogger.debug`Selector matched="${selector}"`;
      return element;
    }
  }

  pdfLogger.warn`All selectors failed - using default`;
  return defaultElement;
}
```

### Pattern 3: Registry Updates with Logging

```typescript
async function updateRegistry(hash: string, notePath: string, cid: string) {
  executeLogger.debug`Updating registry hash=${hash} cid=${cid}`;

  try {
    await registry.markProcessed({
      sourceHash: hash,
      processedAt: new Date().toISOString(),
      createdNote: notePath,
    });

    await registry.save();

    executeLogger.debug`Registry saved hash=${hash} cid=${cid}`;
  } catch (error) {
    executeLogger.error`Registry update failed hash=${hash} error=${error.message} cid=${cid}`;
    throw error;
  }
}
```

### Pattern 4: Performance Tracking

```typescript
async function processItems(items: Item[], cid: string) {
  const overallStart = Date.now();
  let successCount = 0;
  let failureCount = 0;

  for (const item of items) {
    const itemStart = Date.now();

    try {
      await processItem(item, cid);
      successCount++;

      const duration = Date.now() - itemStart;
      executeLogger.debug`Item processed file=${item.name} duration=${duration}ms cid=${cid}`;
    } catch (error) {
      failureCount++;

      const duration = Date.now() - itemStart;
      executeLogger.error`Item failed file=${item.name} duration=${duration}ms cid=${cid}`;
    }
  }

  const totalDuration = Date.now() - overallStart;

  executeLogger.info`Batch complete success=${successCount} failed=${failureCount} duration=${totalDuration}ms cid=${cid}`;
}
```

---

## Quick Reference

### File Structure

```
plugins/my-plugin/
├── src/
│   ├── logger.ts         # createPluginLogger setup + exports
│   ├── scraper.ts        # Uses scraperLogger
│   ├── auth.ts           # Uses authLogger
│   └── cli.ts            # Calls initLogger()
└── mcp/
    └── index.ts          # Calls initLogger() in startup
```

### Key Imports

```typescript
// Always import from @sidequest/core/logging
import {
  createCorrelationId,
  createPluginLogger,
  MetricsCollector,
} from "@sidequest/core/logging";
```

### Checklist: Adding Logging to a Plugin

- [ ] Create `src/logger.ts` with `createPluginLogger()`
- [ ] Define subsystems (match functional areas)
- [ ] Export subsystem loggers + `initLogger` + `createCorrelationId`
- [ ] Call `await initLogger()` in CLI/MCP entry point
- [ ] Use correlation IDs for operation tracing
- [ ] Log at appropriate levels (DEBUG/INFO/WARN/ERROR)
- [ ] Include `durationMs` for performance metrics
- [ ] Test logs manually with grep/jq
- [ ] Document log location in plugin CLAUDE.md
- [ ] Add metrics collection to Stop hook (optional)

---

## Related Skills

### Bun CLI Development

**Reference:** [Bun CLI skill](../bun-cli/SKILL.md)

Use for:
- CLI entry point patterns (where to call `initLogger()`)
- Error handling with exit codes
- Output formatting (markdown + JSON)

**Example integration:**
```typescript
// src/cli.ts
import { initLogger, scraperLogger } from "./logger";

async function main() {
  await initLogger(); // Before any logging

  const { command, flags } = parseArgs(process.argv.slice(2));

  scraperLogger.info`CLI started command=${command}`;

  // ... rest of CLI
}

main();
```

### Bun Runtime Workflows

**Reference:** [Bun Runtime skill](../bun-runtime/SKILL.md)

Use for:
- Testing patterns (beforeEach/afterEach for initLogger)
- Async/await best practices (initLogger is async)
- Performance optimization (log levels impact throughput)

---

## FAQ

### When should I create a new subsystem logger?

**Create a new subsystem when:**
- Functional area is distinct (scraping, auth, storage)
- You want independent log filtering (`grep '"logger":"my-plugin.scraper"'`)
- Module has significant enough volume to justify separation

**Don't create subsystems for:**
- Utils/helpers (use root logger)
- One-off operations (use root logger)
- Overly granular divisions (too many subsystems = hard to filter)

### Should I log in tests?

**Generally no.** Tests should assert functional behavior, not log output.

**Exception:** When testing logging infrastructure itself (logger.ts, metrics.ts).

### How do I rotate logs manually?

Logs auto-rotate at 1 MiB (default). To force rotation:

```bash
# Rename current log
mv ~/.claude/logs/my-plugin.jsonl ~/.claude/logs/my-plugin.jsonl.1

# LogTape will create new file on next log
```

### What's the difference between correlation ID and request ID?

**Correlation ID:** 8-character UUID for tracing a single operation across subsystems.

**Request ID:** Typically longer, used for distributed tracing across services.

For local plugins, correlation IDs are sufficient.

### How do I debug "no logs appearing"?

1. **Verify `initLogger()` called:** Logs won't appear until initialization
2. **Check log level:** DEBUG logs hidden if lowestLevel > "debug"
3. **Inspect log file directly:** `tail -f ~/.claude/logs/my-plugin.jsonl`
4. **Check LogTape errors:** Look for "logtape.meta" ERROR logs
5. **Verify file permissions:** Log directory must be writable

---

## Production Reference Implementation

### para-obsidian Plugin

**Location:** `plugins/para-obsidian/`

**Observability Maturity:** 4/5 (Adaptive)

**Key Features:**
- ✅ OpenTelemetry-compatible three-tier CID hierarchy (sessionCid, cid, parentCid)
- ✅ Structured logging with properties objects across all subsystems
- ✅ End-to-end traceability across async operations (scan → classify → enrich → execute)
- ✅ Full trace correlation with parent-child relationships
- ✅ Subsystem loggers: inbox, pdf, llm, execute, git, enrich, search, templates, frontmatter, fs, lock, tx, cli, classify

**Files to Study:**
- `src/shared/logger.ts` - Plugin logger setup with 14 subsystems
- `src/inbox/core/engine.ts` - Session-level CID threading through file processing
- `src/inbox/enrich/strategies/bookmark-strategy.ts` - Structured logging in enrichment
- `OBSERVABILITY_IMPROVEMENTS.md` - Complete implementation details and rationale

**Example Trace:**
```json
{
  "@timestamp": "2025-12-20T21:37:26.567Z",
  "level": "info",
  "logger": "para-obsidian.enrich",
  "message": "Bookmark enrichment started",
  "properties": {
    "event": "enrichment_started",
    "sessionCid": "acdfe223",
    "cid": "eae519bd",
    "parentCid": "e400fff2",
    "file": "bookmark-example.md",
    "url": "https://example.com"
  }
}
```

**Grep Workflow:**
```bash
# Trace entire session
grep 'sessionCid=acdfe223' ~/.claude/logs/para-obsidian.jsonl

# Timeline view with hierarchy
grep 'sessionCid=acdfe223' ~/.claude/logs/para-obsidian.jsonl | \
  jq -r '."@timestamp" + " | " + .properties.cid + " | " + .message'
```

**References:**
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- OpenTelemetry Traces: https://opentelemetry.io/docs/concepts/signals/traces/
- Observability Review: Agent a1a07a7 (can be resumed for follow-up work)

---

**Last Updated:** 2025-12-20
**Status:** Production Reference Implementation
**Related:** [Bun CLI](../bun-cli/SKILL.md), [Bun Runtime](../bun-runtime/SKILL.md), [Inbox Processing Expert](../inbox-processing-expert/SKILL.md)
