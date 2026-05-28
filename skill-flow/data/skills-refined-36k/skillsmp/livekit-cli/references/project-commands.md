# Project management commands

The LiveKit CLI provides commands for managing projects and generating access tokens. A project consists of a URL, API key, and API secret that point to a LiveKit deployment.

## Cloud authentication

### Authenticate with LiveKit Cloud

Link your LiveKit Cloud account to the CLI:

```bash
lk cloud auth
```

This opens a browser-based flow to sign in and select a project. LiveKit Cloud generates API keys for your CLI instance and adds the project automatically.

**Options**:
- `--timeout SECONDS, -t SECONDS`: Seconds before giving up (default: 900)
- `--poll-interval SECONDS, -i SECONDS`: Seconds between poll requests (default: 4)

To link multiple projects, run `lk cloud auth` multiple times.

### Revoke authorization

Remove a project and revoke its API keys:

```bash
lk cloud auth --revoke
```

**Options**:
- `--project PROJECT_NAME`: Name of the project to revoke (default: current default project)

This revokes the API keys stored in your CLI instance. Any copies of these keys made with `lk app env` or `lk app create` are also revoked.

## Project commands

### List projects

Show all configured projects (default marked with `*`):

```bash
lk project list
```

Example output:
```
┌──────────────────────┬──────────────────────────────────────────────────┬───────────────┐
│ Name                 │ URL                                              │ API Key       │
├──────────────────────┼──────────────────────────────────────────────────┼───────────────┤
│   dev-local          │ http://localhost:7880                            │ APIxxxxxxxxxx │
│   staging            │ wss://staging-abc123.livekit.cloud               │ APIyyyyyyyyyy │
│ * production         │ wss://production-xyz789.livekit.cloud            │ APIzzzzzzzzzz │
└──────────────────────┴──────────────────────────────────────────────────┴───────────────┘
```

**Options**:
- `--json, -j`: Output as JSON, including API key and secret

### Add a project

Add a self-hosted or manual project:

```bash
lk project add PROJECT_NAME \
  --url LIVEKIT_URL \
  --api-key API_KEY \
  --api-secret API_SECRET \
  [--default]
```

**Options**:
- `PROJECT_NAME`: Unique name for the project in your CLI instance
- `--url URL`: WebSocket URL of the LiveKit server
- `--api-key KEY`: Project API key
- `--api-secret SECRET`: Project API secret
- `--default`: Set this project as the default

**Example** (self-hosted):
```bash
lk project add my-local \
  --url http://localhost:7880 \
  --api-key devkey \
  --api-secret secret \
  --default
```

### Set default project

Change the default project used by other commands:

```bash
lk project set-default PROJECT_NAME
```

### Remove a project

Remove a project from your local CLI configuration:

```bash
lk project remove PROJECT_NAME
```

This does not affect the project in LiveKit Cloud. For Cloud projects, use `lk cloud auth --revoke` to also revoke the API keys.

## Environment variables

### Load credentials to file

Write LiveKit credentials to a local environment file:

```bash
lk app env -w
```

This creates or updates `.env.local` with:
- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`

## Token generation

### Create an access token

Generate a token for joining rooms:

```bash
lk token create \
  --api-key <API_KEY> --api-secret <API_SECRET> \
  --join --room <ROOM_NAME> --identity <USER_IDENTITY> \
  --valid-for <DURATION>
```

**Options**:
- `--api-key KEY`: API key for signing the token
- `--api-secret SECRET`: API secret for signing the token
- `--join`: Grant permission to join rooms
- `--room ROOM`: Name of the room to join
- `--identity IDENTITY`: Unique identity for the participant
- `--valid-for DURATION`: Token validity period (e.g., `24h`, `1h30m`)

**Example for LiveKit Cloud**:
```bash
lk token create \
  --api-key <PROJECT_KEY> --api-secret <PROJECT_SECRET> \
  --join --room test_room --identity test_user \
  --valid-for 24h
```

**Example for local development** (dev mode):
```bash
lk token create \
  --api-key devkey --api-secret secret \
  --join --room test_room --identity test_user \
  --valid-for 24h
```

## App templates

### Create from template

Bootstrap a new application:

```bash
lk app create --template <TEMPLATE_NAME> <APP_NAME>
```

Run without `--template` to see available templates interactively:

```bash
lk app create
```

**Available templates**:

| Template | Language | Description |
|----------|----------|-------------|
| `agent-starter-python` | Python | Voice agent starter project |
| `agent-starter-react` | TypeScript/Next.js | Voice AI frontend |
| `agent-starter-android` | Kotlin | Android voice AI app |
| `agent-starter-swift` | Swift | iOS/macOS/visionOS voice AI app |
| `agent-starter-flutter` | Flutter | Cross-platform voice AI app |
| `agent-starter-react-native` | React Native/Expo | Mobile voice AI app |
| `agent-starter-embed` | TypeScript/Next.js | Embeddable voice AI widget |
| `token-server` | Node.js | Hosted token server |
| `meet` | TypeScript/Next.js | Video conferencing app |
| `multi-agent-python` | Python | Multi-agent workflow demo |
| `outbound-caller-python` | Python | Outbound calling agent |

## Room commands

### Join a room

Join a room as a simulated participant:

```bash
lk room join \
  --url <LIVEKIT_URL> \
  --api-key <API_KEY> --api-secret <API_SECRET> \
  --identity <IDENTITY> \
  <ROOM_NAME>
```

**Options**:
- `--publish-demo`: Publish a looped demo video to the room

**Example for LiveKit Cloud**:
```bash
lk room join \
  --url wss://my-project.livekit.cloud \
  --api-key <API_KEY> --api-secret <API_SECRET> \
  --publish-demo --identity bot_user \
  my_room
```

**Example for local development**:
```bash
lk room join \
  --url ws://localhost:7880 \
  --api-key devkey --api-secret secret \
  --publish-demo --identity bot_user \
  my_room
```

This is useful for testing multi-user sessions or simulating participants publishing media.
