# Failure Modes and Recovery

Quick reference for error handling in Cartographer. For detailed command usage, see the relevant command files in `commands/`.

## Error Categories

| Category | Severity | User Impact | Action |
|----------|----------|-------------|--------|
| CRITICAL | Blocks operation | Cannot proceed | Must resolve before continuing |
| HIGH | Degrades output | Partial results | Proceed with warnings |
| MEDIUM | Quality impact | Suboptimal | Note in observations |
| LOW | Minor | Cosmetic | Log and continue |

## Pre-flight Failures

| Error | Detection | Severity | Recovery |
|-------|-----------|----------|----------|
| Not a git repo | `git rev-parse --git-dir` fails | MEDIUM | Warn user, continue without git features |
| Empty codebase | <10 source files | HIGH | Confirm correct directory with user |
| No project type | All scores <0.3 | HIGH | Prompt user to specify type |

## Analysis Failures

| Error | Detection | Severity | Recovery |
|-------|-----------|----------|----------|
| Directory inaccessible | Permission denied | MEDIUM | Skip directory, note in observations |
| Large codebase | >10k files or >5min | MEDIUM | Use sampling strategy, note approximations |
| Conflicting signals | Multiple types score within 0.1 | MEDIUM | Present options, ask user to choose |
| Few domains detected | <3 domains found | MEDIUM | Try deeper analysis, allow manual definition |

## File Operation Failures

| Error | Detection | Severity | Recovery |
|-------|-----------|----------|----------|
| Cannot create atlas dir | mkdir permission denied | CRITICAL | Suggest chmod or manual creation |
| Atlas already exists | `/cartographer:chart` with existing atlas | HIGH | Suggest `/cartographer:rechart` or confirm overwrite |
| Partial write failure | Some files fail to write | HIGH | Create partial atlas, list failed files |

## Validation Failures

| Error | Detection | Severity | Recovery |
|-------|-----------|----------|----------|
| Schema invalid | Required fields missing | HIGH | Apply defaults, add warning comments |
| Path drift | schema.yaml references missing paths | MEDIUM | Mark stale, recommend `/cartographer:rechart` |
| Broken links | SKILL.md references missing files | MEDIUM | Remove broken links, note in observations |

## Navigator Failures

| Error | Detection | Severity | Recovery |
|-------|-----------|----------|----------|
| Atlas not found | Navigator command without atlas | CRITICAL | Block command, suggest `/cartographer:chart` |
| Atlas too stale | Staleness >0.6 | HIGH | Warn user, offer proceed or rechart |
| Spec conflict | Plan would overwrite existing spec | MEDIUM | Offer view/archive/overwrite/rename options |

## Embed Failures

| Error | Detection | Severity | Recovery |
|-------|-----------|----------|----------|
| No CLAUDE.md | File doesn't exist | MEDIUM | Ask to create or output to stdout |
| Malformed markers | Multiple or broken section markers | MEDIUM | Report issue, ask for manual cleanup |

## General Guidelines

**Graceful degradation**: Log failure, continue with reduced functionality, note limitations.

**User communication**: Always provide: (1) what happened, (2) why it matters, (3) what to do.

**Retry policy**: Retry transient failures (network, file locks) up to 3 times with backoff. Never retry permission errors, missing files, or invalid config.
