# NATS

**Category**: cncf
**Description**: Cloud-native messaging system
**Homepage**: https://nats.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*NATS Go packages*

- `github.com/nats-io/nats.go` - Go client
- `github.com/nats-io/nats-server/v2` - NATS server
- `github.com/nats-io/nats-streaming-server` - Streaming server
- `github.com/nats-io/nkeys` - NKeys library
- `github.com/nats-io/jwt/v2` - JWT library

#### NPM
*NATS Node.js packages*

- `nats` - Node.js client
- `nats.ws` - WebSocket client

#### PYPI
*NATS Python packages*

- `nats-py` - Python client
- `asyncio-nats-client` - Async client

#### MAVEN
*NATS Java packages*

- `io.nats:jnats` - Java client

#### NUGET
*NATS .NET packages*

- `NATS.Client` - .NET client

#### CARGO
*NATS Rust packages*

- `nats` - Rust client
- `async-nats` - Async Rust client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate NATS usage*

- `nats.conf` - NATS configuration
- `nats-server.conf` - Server config
- `jetstream.conf` - JetStream config

### Code Patterns

**Pattern**: `nats\.io|nats-server`
- NATS references
- Example: `nats.io/nats-server`

**Pattern**: `nats://|nats-streaming://|nats-leaf://`
- NATS connection URLs
- Example: `nats://localhost:4222`

**Pattern**: `:4222|:8222|:6222`
- NATS default ports
- Example: `localhost:4222`

**Pattern**: `nats\.Connect|nats\.DefaultURL|nats-server`
- NATS code patterns
- Example: `nc, err := nats.Connect(nats.DefaultURL)`

**Pattern**: `jetstream|JetStream|JETSTREAM`
- JetStream persistence layer
- Example: `js, _ := nc.JetStream()`

**Pattern**: `Subject:|publish|subscribe|request`
- NATS messaging patterns
- Example: `nc.Subscribe("foo", func(m *nats.Msg))`

**Pattern**: `cluster\s*\{|routes\s*=|leafnodes\s*\{`
- NATS clustering config
- Example: `cluster {\n  routes = [`

**Pattern**: `authorization\s*\{|accounts\s*\{|users\s*\{`
- NATS auth config
- Example: `authorization {\n  users = [`

---

## Environment Variables

- `NATS_URL` - NATS server URL
- `NATS_CLUSTER_URL` - Cluster URL
- `NATS_USER` - Username
- `NATS_PASSWORD` - Password
- `NATS_CREDS` - Credentials file path
- `NATS_NKEY` - NKey seed

## Detection Notes

- Core NATS for pub/sub messaging
- JetStream for persistence
- NATS Streaming (deprecated, use JetStream)
- Supports clustering and leaf nodes
- NKeys for authentication

---

## Secrets Detection

### Credentials

#### NATS Password
**Pattern**: `NATS_PASSWORD\s*[=:]\s*['"]?([^\s'"]{8,})['"]?`
**Severity**: critical
**Description**: NATS user password in environment variable
**Example**: `NATS_PASSWORD=mysecretpass123`

#### NATS Token
**Pattern**: `NATS_TOKEN\s*[=:]\s*['"]?([^\s'"]{8,})['"]?`
**Severity**: critical
**Description**: NATS authentication token in environment variable
**Example**: `NATS_TOKEN=mytoken123456`

#### NKey Seed
**Pattern**: `SUAM[A-Z0-9]{56}`
**Severity**: critical
**Description**: NATS NKey seed (user)

---

## TIER 3: Configuration Extraction

### Port Extraction

**Pattern**: `port:\s*([0-9]+)`
- NATS listen port
- Extracts: `port`
- Example: `port: 4222`

### Cluster Name Extraction

**Pattern**: `name:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Cluster name
- Extracts: `cluster_name`
- Example: `name: "my-cluster"`

### JetStream Domain Extraction

**Pattern**: `domain:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- JetStream domain
- Extracts: `js_domain`
- Example: `domain: "hub"`
