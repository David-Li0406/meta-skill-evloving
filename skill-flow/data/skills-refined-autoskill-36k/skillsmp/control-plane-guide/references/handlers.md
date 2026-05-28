# Writing Handlers

Handlers are scripts that process capability requests, executed by `fort-provider` (the FastCGI server).

## Handler Contract

| Input | Source |
|-------|--------|
| Request JSON | stdin |
| Caller identity | `$FORT_ORIGIN` env var |
| Capability name | `$FORT_CAPABILITY` env var |

| Output | Destination |
|--------|-------------|
| Response JSON | stdout |
| Exit code 0 | Success (200) |
| Exit code non-zero | Failure (500) |

## Simple Handler

```bash
#!/usr/bin/env bash
set -euo pipefail

# Read request (optional - ignore if no input needed)
request=$(cat)

# Do work
result=$(some-command)

# Return JSON response
jq -n --arg result "$result" '{"status": "ok", "data": $result}'
```

## Handler with Input Parsing

```bash
#!/usr/bin/env bash
set -euo pipefail

# Parse request JSON
request=$(cat)
service=$(echo "$request" | jq -r '.service // empty')

if [[ -z "$service" ]]; then
  echo '{"error": "missing service field"}' >&2
  exit 1
fi

# Process request
client_id=$(register-oidc-client "$service")

# Return response
jq -n --arg id "$client_id" '{"client_id": $id}'
```

## Handler Permissions

Handlers run as root by default (via systemd). If your handler needs:

- **Secrets**: Read from `/run/agenix/` or `/var/lib/<app>/`
- **Network**: Make HTTP calls to local services
- **State**: Write to `/var/lib/fort/` or app-specific directories

## Idempotency

Handlers SHOULD be idempotent when possible:

```bash
# Good: Check before creating
if ! client-exists "$service"; then
  create-client "$service"
fi
get-client-info "$service"

# Bad: Always create (will fail on retry)
create-client "$service"
```

## Working Example: Status Handler

The simplest handler - just returns a file:

```bash
#!/usr/bin/env bash
cat /var/lib/fort/status/status.json
```

## Working Example: OIDC Register Handler

From `apps/pocket-id/handlers/oidc-register`:

```bash
#!/usr/bin/env bash
set -euo pipefail

request=$(cat)
service=$(echo "$request" | jq -r '.service')
callback=$(echo "$request" | jq -r '.callback // empty')

# Check if client exists
existing=$(pocket-id-admin list-clients | jq -r --arg s "$service" '.[] | select(.name == $s)')

if [[ -n "$existing" ]]; then
  echo "$existing"
  exit 0
fi

# Create new client
pocket-id-admin create-client \
  --name "$service" \
  --callback "${callback:-https://${service}.fort.example.com/callback}" \
  --json
```

## Debugging Handlers

Test locally by piping JSON:

```bash
echo '{"service": "test"}' | /etc/fort/handlers/my-capability
```

Check logs on the host:

```bash
journalctl -u fort-provider -n 50
```

## Handler Location at Runtime

Handlers are installed to `/etc/fort/handlers/<capability-name>` during NixOS activation.
