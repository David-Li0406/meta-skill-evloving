---
name: railway-deploy
description: Use this skill when you want to deploy code to Railway using the command "railway up" or similar phrases like "deploy", "ship", or "push".
---

# Railway Deploy

Deploy code from the current directory to Railway using `railway up`.

## When to Use

- User asks to "deploy", "ship", or "push code".
- User says "railway up" or "deploy to Railway".
- User wants to deploy local code changes.
- User says "deploy and fix any issues" (use --ci mode).

## Modes

### Detach Mode (default)
Starts deploy and returns immediately. Use for most deploys.

```bash
railway up --detach
```

### CI Mode
Streams build logs until complete. Use when user wants to watch the build or needs to debug issues.

```bash
railway up --ci
```

**When to use CI mode:**
- User says "deploy and watch" or "deploy and fix issues".
- User is debugging build failures.
- User wants to see build output.

## Deploy Specific Service

Default is linked service. To deploy to a different service:

```bash
railway up --detach --service <service-name>
```

## Deploy to Unlinked Project

Deploy to a project without linking first:

```bash
railway up --project <project-id> --environment production --detach
```

Requires both `--project` and `--environment` flags.

## CLI Options

| Flag | Description |
|------|-------------|
| `-d, --detach` | Don't attach to logs (default) |
| `-c, --ci` | Stream build logs, exit when done |
| `-s, --service <NAME>` | Target service (defaults to linked) |
| `-e, --environment <NAME>` | Target environment (defaults to linked) |
| `-p, --project <ID>` | Target project (requires --environment) |
| `[PATH]` | Path to deploy (defaults to current directory) |

## Directory Linking

Railway CLI walks up the directory tree to find a linked project. If you're in a subdirectory of a linked project, you don't need to relink.

For subdirectory deployments, prefer setting `rootDirectory` via the environment skill, then deploy normally with `railway up`.

## After Deploy

### Detach mode
```
Deploying to <service>...
```
Use the `railway-deployment` skill to check build status (with `--lines` flag).

### CI mode
Build logs stream inline. If the build fails, the error will be in the output.

**Do NOT run `railway logs --build` after CI mode** - the logs already streamed. If you need more context, use the `railway-deployment` skill with `--lines` flag (never stream).