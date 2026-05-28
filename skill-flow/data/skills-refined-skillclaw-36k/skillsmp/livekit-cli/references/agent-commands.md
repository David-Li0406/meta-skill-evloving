# Agent deployment commands

The LiveKit CLI provides commands for deploying and managing agents on LiveKit Cloud. All agent commands are prefixed with `lk agent`.

## Prerequisites

- Latest version of the LiveKit CLI
- A LiveKit Cloud project linked via `lk cloud auth`
- A working agent project

## Create and deploy an agent

Register and deploy a new agent:

```bash
cd your-agent-project
lk agent create
```

This command:
1. Registers your agent with LiveKit Cloud and assigns a unique ID
2. Creates a `livekit.toml` configuration file
3. Creates a `Dockerfile` if one doesn't exist
4. Uploads your code to the build service
5. Builds a container image
6. Deploys to your LiveKit Cloud project

### Options for create

- `--region REGION`: Region code for the agent deployment
- `--secrets KEY=VALUE`: Secrets injected as environment variables (can use multiple times)
- `--secrets-file FILE`: File containing secret KEY=VALUE pairs, one per line
- `--secret-mount FILE`: Path to a file to mount as a secret in the container
- `--config FILE`: Name of the configuration file (default: `livekit.toml`)
- `--silent`: Do not prompt for interactive confirmation

## Deploy new versions

Deploy an updated version of your agent:

```bash
lk agent deploy
```

LiveKit Cloud uses rolling deployments:
1. Builds a new container image from your code
2. Deploys new instances alongside existing ones
3. Routes new sessions to new instances
4. Gives old instances up to 1 hour to complete active sessions
5. Autoscales based on demand

### Options for deploy

- `--secrets KEY=VALUE`: Update secrets during deployment
- `--secrets-file FILE`: File containing secrets to update
- `--secret-mount FILE`: File to mount as a secret

You can also deploy from a specific directory:

```bash
lk agent deploy /path/to/agent
```

## Monitor status

Check the status of your deployed agent:

```bash
lk agent status
```

This shows:
- Current deployment status
- Number of replicas running
- Health information

## View logs

Stream runtime logs from your agent:

```bash
lk agent logs
```

This shows a live tail of logs from the newest agent server instance, including recent log history.

View build logs from the current deployment:

```bash
lk agent logs --log-type=build
```

## Rollback

Revert to a previous version without rebuilding:

```bash
lk agent rollback
```

Rollback uses the same rolling deployment strategy as regular deployments. This feature requires a paid LiveKit Cloud plan.

## Configuration file

The `livekit.toml` file contains your agent's deployment configuration:

```toml
[project]
  subdomain = "<my-project-subdomain>"

[agent]
  id = "<agent-id>"
```

Generate a new configuration file:

```bash
lk agent config
```

## Secrets management

### List secrets

View all secrets for your agent (values are hidden):

```bash
lk agent secrets
```

### Update secrets

Add or update secrets:

```bash
# From individual values
lk agent update-secrets --secrets "API_KEY=value" --secrets "OTHER_KEY=value"

# From a file
lk agent update-secrets --secrets-file=.env.production

# Replace all secrets (delete existing, add new)
lk agent update-secrets --secrets-file=new-secrets.env --overwrite
```

### File-mounted secrets

Mount a file as a secret (available at `/etc/secret/<filename>`):

```bash
lk agent update-secrets --secret-mount ./google-application-credentials.json
```

### Automatic secrets

LiveKit Cloud automatically provides these environment variables:
- `LIVEKIT_URL` - Your LiveKit Cloud server URL
- `LIVEKIT_API_KEY` - API key for your project
- `LIVEKIT_API_SECRET` - API secret for your project

These cannot be set or modified manually.

## Secret naming rules

- Only letters, numbers, and underscores allowed
- Maximum 70 characters
- Case sensitive
- Recommended: uppercase letters and underscores (e.g., `MY_API_KEY`)

## Log forwarding

Forward logs to external services by adding their credentials as secrets:

**Datadog**:
```bash
lk agent update-secrets --secrets "DATADOG_TOKEN=your-client-token"
lk agent update-secrets --secrets "DATADOG_REGION=us1"  # Optional, default: us1
```

**CloudWatch**:
```bash
lk agent update-secrets \
  --secrets "AWS_ACCESS_KEY_ID=your-key-id" \
  --secrets "AWS_SECRET_ACCESS_KEY=your-secret-key" \
  --secrets "AWS_REGION=us-west-2"  # Optional, default: us-west-2
```

**Sentry**:
```bash
lk agent update-secrets --secrets "SENTRY_DSN=your-sentry-dsn"
```

**New Relic**:
```bash
lk agent update-secrets --secrets "NEW_RELIC_LICENSE_KEY=your-license-key"
```

## Build requirements

The build process has a 10-minute timeout. To optimize builds:

1. Use a proper `.dockerignore` to exclude unnecessary files
2. Download ML models during build, not at runtime (use `download-files` command)
3. Never include `.env` files or secrets in your image
4. Use lockfiles for reproducible builds

## Dockerfile tips

The CLI generates a Dockerfile automatically, but if you customize it:

- Use glibc-based images (Debian/Ubuntu), not Alpine
- Don't run as root
- Set an explicit `WORKDIR`
- Use the `start` command in your `CMD`/`ENTRYPOINT`
