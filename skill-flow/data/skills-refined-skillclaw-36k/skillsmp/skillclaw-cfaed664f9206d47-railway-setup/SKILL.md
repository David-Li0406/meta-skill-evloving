---
name: railway-setup
description: Use this skill when you need to create or deploy Railway projects, services, or databases, especially when prompted with commands like "setup", "initialize", or "deploy from GitHub".
---

# New Project / Service / Database

Create Railway projects, services, and databases with proper configuration.

## When to Use

- User says "deploy to railway" (add service if linked, init if not)
- User says "create a railway project", "init", "new project" (explicit new project)
- User says "link to railway", "connect to railway"
- User says "create a service", "add a backend", "new api service"
- User says "create a vite app", "create a react website", "make a python api"
- User says "deploy from github.com/user/repo", "create service from this repo"
- User says "add postgres", "add a database", "add redis", "add mysql", "add mongo"
- User says "connect to postgres", "wire up the database", "connect my api to redis"
- User says "add postgres and connect to the server"
- Setting up code + Railway service together

## Prerequisites

Check if the Railway CLI is installed:

```bash
command -v railway
```

If not installed, run:

> Install Railway CLI:
>
> ```
> npm install -g @railway/cli
> ```
>
> or
>
> ```
> brew install railway
> ```

Check if authenticated:

```bash
railway whoami --json
```

If not authenticated, run:

> Run `railway login` to authenticate.

## Decision Flow

```
railway status --json (in current dir)
     │
┌────┴────┐
Linked    Not Linked
  │            │
  │       Check parent: cd .. && railway status --json
  │            │
  │       ┌────┴────┐
  │    Parent      Not linked
  │    Linked      anywhere
  │       │            │
  │   Add service   railway list
  │   Set rootDir      │
  │   Deploy       ┌───┴───┐
  │       │      Match?  No match
  │       │        │        │
  │       │      Link    Init new
  └───────┴────────┴────────┘
           │
    User wants service?
           │
     ┌─────┴─────┐
    Yes         No
     │           │
Scaffold code   Done
     │
railway add --service
     │
Configure if needed
     │
Ready to deploy
```

## Check Current State

```bash
railway status --json
```

- **If linked**: Add a service to the existing project (see above).
- **If not linked**: Check if a PARENT directory is linked (see above).