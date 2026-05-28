---
name: logging
description: Guide for implementing structured logging in SideQuest plugins using @sidequest/core. Use when adding logging to new plugins, debugging existing plugins, or setting up log analysis.
---

# Plugin Logging Guide

Implement structured, JSONL logging in SideQuest plugins using the `@sidequest/core/logging` factory.

## When to Use This Skill

- Adding logging to a new plugin
- Migrating a plugin to structured logging
- Debugging plugin behavior via logs
- Setting up log rotation or analysis
- Questions about logging best practices

## Quick Start

### 1. Add Dependency

```json
// package.json
{
  "dependencies": {
    "@sidequest/core": "workspace:*"
  }
}
```

### 2. Create Logger Module

```typescript
// src/logger.ts
import { createPluginLogger } from "@sidequest/core/logging";

export const {
  initLogger,
  createCorrelationId,
  getSubsystemLogger,
  logDir,
  logFile,
} = createPluginLogger({
  name: "my-plugin",
  subsystems: ["scraper", "api", "cache"],
});

// Export typed subsystem loggers
export const scraperLogger = getSubsystemLogger("scraper");
export const apiLogger = getSubsystemLogger("api");
export const cacheLogger = getSubsystemLogger("cache");
```

### 3. Initialize at Entry Points

```typescript
// src/index.ts (CLI entry point)
import { initLogger, createCorrelationId, scraperLogger } from "./logger";

await initLogger();

const cid = createCorrelationId();
scraperLogger.info`Starting scrape operation ${cid}`;
```

### 4. Use Correlation IDs

```typescript
// Pass cid through function calls
async function scrape(url: string, cid: string) {
  scraperLogger.debug`Fetching ${url} ${cid}`;
  try {
    const result = await fetch(url);
    scraperLogger.info`Fetched ${url} status=${result.status} ${cid}`;
    return result;
  } catch (error) {
    scraperLogger.error`Failed to fetch ${url}: ${error} ${cid}`;
    throw error;
  }
}
```

## Log Levels

| Level | When to Use |
|-------|-------------|
| `debug` | Detailed diagnostic info: selector attempts, parsing steps, cache hits |
| `info` | Normal operations: start/complete, item counts, timing |
| `warning` | Degraded operation: fallbacks, edge cases, retries |
| `error` | Failures: exceptions, validation errors, unrecoverable states |

## Checklist: Adding Logging to a Plugin

### Setup Phase
- [ ] Add `@sidequest/core: workspace:*` to dependencies
- [ ] Create `src/logger.ts` with plugin name and subsystems
- [ ] Export subsystem-specific loggers

### Entry Points
- [ ] Call `initLogger()` at the start of CLI tools
- [ ] Call `initLogger()` in MCP server startup
- [ ] Generate correlation ID for each operation

### Logging Calls
- [ ] Use template literal syntax: `logger.info\`message\``
- [ ] Include correlation ID in all logs: `${cid}`
- [ ] Use appropriate log level for each message
- [ ] Log operation start/end with timing

### Error Handling
- [ ] Log errors with full context before re-throwing
- [ ] Include correlation ID in error logs
- [ ] Log stack traces for unexpected errors

### Testing
- [ ] Verify logs are created in `~/.<plugin-name>/logs/`
- [ ] Check JSONL format is valid
- [ ] Verify rotation works (file size > 1MB)

## File Locations

| Item | Path |
|------|------|
| Log directory | `~/.<plugin-name>/logs/` |
| Log file | `<plugin-name>.jsonl` |
| Rotated files | `<plugin-name>.1.jsonl`, `<plugin-name>.2.jsonl`, etc. |

## Configuration Defaults

```typescript
{
  maxSize: 1048576,    // 1 MiB before rotation
  maxFiles: 5,         // Keep 5 rotated files
  level: "debug",      // Capture all levels
  extension: ".jsonl"  // JSON Lines format
}
```

Override in `createPluginLogger()`:

```typescript
createPluginLogger({
  name: "my-plugin",
  subsystems: ["api"],
  maxSize: 5 * 1024 * 1024,  // 5 MiB
  maxFiles: 10,
  lowestLevel: "info",  // Production: skip debug logs
});
```

## Log Entry Format

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "info",
  "category": ["my-plugin", "scraper"],
  "message": ["Starting scrape operation", "abc123"]
}
```

## Viewing Logs

### Tail Recent Logs
```bash
tail -f ~/.my-plugin/logs/my-plugin.jsonl | jq .
```

### Filter by Correlation ID
```bash
grep "abc123" ~/.my-plugin/logs/my-plugin.jsonl | jq .
```

### Filter by Level
```bash
jq 'select(.level == "error")' ~/.my-plugin/logs/my-plugin.jsonl
```

### Filter by Subsystem
```bash
jq 'select(.category[1] == "scraper")' ~/.my-plugin/logs/my-plugin.jsonl
```

## Common Patterns

### Timing Operations

```typescript
const start = Date.now();
// ... operation ...
const durationMs = Date.now() - start;
logger.info`Operation completed in ${durationMs}ms ${cid}`;
```

### Structured Context

```typescript
// Include key-value pairs in message
logger.info`Processed url=${url} count=${items.length} ${cid}`;
```

### Error Context

```typescript
try {
  await riskyOperation();
} catch (error) {
  logger.error`Failed operation=${opName} error=${error.message} ${cid}`;
  throw error;
}
```

### Request Tracing

```typescript
// MCP tool handler
async function handleTool(args: ToolArgs) {
  const cid = createCorrelationId();
  logger.info`Tool invoked tool=${args.name} ${cid}`;

  try {
    const result = await process(args, cid);
    logger.info`Tool completed tool=${args.name} ${cid}`;
    return result;
  } catch (error) {
    logger.error`Tool failed tool=${args.name} ${error} ${cid}`;
    throw error;
  }
}
```

## Example: Full Plugin Setup

```typescript
// src/logger.ts
import { createPluginLogger } from "@sidequest/core/logging";

export const {
  initLogger,
  createCorrelationId,
  getSubsystemLogger,
} = createPluginLogger({
  name: "cinema-bandit",
  subsystems: ["scraper", "pricing", "gmail"],
});

export const scraperLogger = getSubsystemLogger("scraper");
export const pricingLogger = getSubsystemLogger("pricing");
export const gmailLogger = getSubsystemLogger("gmail");

// src/scraper.ts
import { scraperLogger, createCorrelationId } from "./logger";

export async function scrapeShowtimes(cinema: string) {
  const cid = createCorrelationId();
  const start = Date.now();

  scraperLogger.info`Starting scrape cinema=${cinema} ${cid}`;

  try {
    const page = await fetchPage(cinema, cid);
    const shows = await parseShowtimes(page, cid);

    const durationMs = Date.now() - start;
    scraperLogger.info`Scrape complete shows=${shows.length} durationMs=${durationMs} ${cid}`;

    return shows;
  } catch (error) {
    scraperLogger.error`Scrape failed cinema=${cinema} ${error} ${cid}`;
    throw error;
  }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not created | Check `initLogger()` called before logging |
| Empty logs | Verify `await` on async operations |
| Missing correlation ID | Pass `cid` through all function calls |
| Logs too verbose | Set `level: "info"` in production |
| Disk space issues | Reduce `maxFiles` or `maxSize` |

## Related Resources

- `/kit:logs` - View kit plugin logs
- `@logtape/logtape` - Underlying logging framework
- `CLAUDE.md` - Plugin-specific logging configuration
