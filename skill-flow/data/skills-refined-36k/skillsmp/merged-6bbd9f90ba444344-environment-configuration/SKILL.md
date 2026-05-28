---
name: environment-configuration
description: Use this skill when you need to query, stage, or apply configuration changes for Railway environments, including managing variables, build settings, and service connections.
---

# Environment Configuration

Query, stage, and apply configuration changes for Railway environments.

## Quick Actions

**When user asks "what's the config" or "show configuration":**

Run `railway status --json` to get the environment ID, then **always** query the full config:
```bash
bash <<'SCRIPT'
scripts/railway-api.sh \
  'query envConfig($envId: String!) {
    environment(id: $envId) { id config }
  }' \
  '{"envId": "ENV_ID_FROM_STATUS"}'
SCRIPT
```
Present: source (repo/image), build settings, deploy settings, variables per service.

**When user asks "what variables" or "show env vars":**
Use the same environment config query above - it includes variables per service and shared variables.

For **rendered** (resolved) variable values: `railway variables --json`

## Shell Escaping

**CRITICAL:** When running GraphQL queries via bash, you MUST wrap in heredoc to prevent shell escaping issues:

```bash
bash <<'SCRIPT'
scripts/railway-api.sh 'query ...' '{"var": "value"}'
SCRIPT
```

## When to Use

- User wants to create a new environment
- User wants to duplicate an environment (e.g., "copy production to staging")
- User wants to switch to a different environment
- User asks about current build/deploy settings, variables, replicas, health checks, domains
- User asks to change service source (Docker image, branch, commit, root directory)
- User wants to connect a service to a GitHub repo
- User wants to deploy from a GitHub repo (create empty service first via `new` skill, then use this)
- User asks to change build or start command
- User wants to add/update/delete environment variables
- User wants to change replica count or configure health checks
- User asks to delete a service, volume, or bucket
- User says "apply changes", "commit changes", "deploy changes"
- Auto-fixing build errors detected in logs

## Create Environment

Create a new environment in the linked project:

```bash
railway environment new <name>
```

Duplicate an existing environment:

```bash
railway environment new staging --duplicate production
```

With service-specific variables:

```bash
railway environment new staging --duplicate production --service-variable api PORT=3001
```

## Switch Environment

Link a different environment to the current directory:

```bash
railway environment <name>
```

Or by ID:

```bash
railway environment <environment-id>
```

## Get Context

**JSON output** - project/environment IDs:
```bash
railway status --json
```

Extract:
- `project.id` - for service lookup
- `environment.id` - for mutations

**Plain output** - linked service name:
```bash
railway status
```

### Resolve Service ID

If user specifies a service by name, query project services:

```graphql
query projectServices($projectId: String!) {
  project(id: $projectId) {
    services {
      edges {
        node {
          id
          name
        }
      }
    }
  }
}
```

## Query Configuration

Fetch current environment configuration and staged changes.

```graphql
query environmentConfig($environmentId: String!) {
  environment(id: $environmentId) {
    id
    config(decryptVariables: false)
    serviceInstances {
      edges {
        node {
          id
          serviceId
        }
      }
    }
  }
  environmentStagedChanges(environmentId: $environmentId) {
    id
    patch(decryptVariables: false)
  }
}
```

### Response Structure

The `config` field contains current configuration:

```json
{
  "services": {
    "<serviceId>": {
      "source": { "repo": "...", "branch": "main" },
      "build": { "buildCommand": "npm run build", "builder": "NIXPACKS" },
      "deploy": {
        "startCommand": "npm start",
        "multiRegionConfig": { "us-west2": { "numReplicas": 1 } }
      },
      "variables": { "NODE_ENV": { "value": "production" } },
      "networking": { "serviceDomains": {}, "customDomains": {} }
    }
  },
  "sharedVariables": { "DATABASE_URL": { "value": "..." } }
}
```

The `patch` field in `environmentStagedChanges` contains pending changes. The effective configuration is the base `config` merged with the staged `patch`.

## Get Rendered Variables

To see **rendered** (resolved) values as they appear at runtime:

```bash
# Current linked service
railway variables --json

# Specific service
railway variables --service <service-name> --json
```

## Stage Changes

Stage configuration changes via the `environmentStageChanges` mutation. Use `merge: true` to automatically merge with existing staged changes.

```graphql
mutation stageEnvironmentChanges(
  $environmentId: String!
  $input: EnvironmentConfig!
  $merge: Boolean
) {
  environmentStageChanges(
    environmentId: $environmentId
    input: $input
    merge: $merge
  ) {
    id
  }
}
```

### Delete Service

Use `isDeleted: true`:

```bash
bash <<'SCRIPT'
scripts/railway-api.sh \
  'mutation stageChanges($environmentId: String!, $input: EnvironmentConfig!, $merge: Boolean) {
    environmentStageChanges(environmentId: $environmentId, input: $input, merge: $merge) { id }
  }' \
  '{"environmentId": "ENV_ID", "input": {"services": {"SERVICE_ID": {"isDeleted": true}}}, "merge": true}'
SCRIPT
```

## Stage and Apply Immediately

For single changes that should deploy right away, use `environmentPatchCommit` to stage and apply in one call.

```graphql
mutation environmentPatchCommit(
  $environmentId: String!
  $patch: EnvironmentConfig
  $commitMessage: String
) {
  environmentPatchCommit(
    environmentId: $environmentId
    patch: $patch
    commitMessage: $commitMessage
  )
}
```

## Apply Staged Changes

Commit staged changes and trigger deployments.

### Apply Mutation

**Mutation name: `environmentPatchCommitStaged`**

```graphql
mutation environmentPatchCommitStaged(
  $environmentId: String!
  $message: String
  $skipDeploys: Boolean
) {
  environmentPatchCommitStaged(
    environmentId: $environmentId
    commitMessage: $message
    skipDeploys: $skipDeploys
  )
}
```

### Parameters

| Field           | Type    | Default | Description                                 |
| --------------- | ------- | ------- | ------------------------------------------- |
| `environmentId` | String! | -       | Environment ID from status                  |
| `message`       | String  | null    | Short description of changes                |
| `skipDeploys`   | Boolean | false   | Skip deploys (only if user explicitly asks) |

### Commit Message

Keep very short - one sentence max. Examples:

- "set build command to fix npm error"
- "add API_KEY variable"
- "increase replicas to 3"

### Default Behavior

**Always deploy** unless user explicitly asks to skip. Only set `skipDeploys: true` if user says "apply without deploying", "commit but don't deploy", or "skip deploys".

## Error Handling

### Service Not Found

```
Service "foo" not found in project. Available services: api, web, worker
```

### No Staged Changes

```
No patch to apply
```

### Invalid Configuration

Common issues:

- `buildCommand` and `startCommand` cannot be identical
- `buildCommand` only valid with NIXPACKS builder
- `dockerfilePath` only valid with DOCKERFILE builder

### No Permission

```
You don't have permission to modify this environment. Check your Railway role.
```

### No Linked Project

```
No project linked. Run `railway link` to link a project.
```

## Composability

- **Create service**: Use `service` skill
- **View logs**: Use `deployment` skill
- **Add domains**: Use `domain` skill
- **Deploy local code**: Use `deploy` skill