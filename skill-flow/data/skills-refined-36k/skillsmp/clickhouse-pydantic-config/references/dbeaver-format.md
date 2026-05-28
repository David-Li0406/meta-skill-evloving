**Skill**: [ClickHouse Pydantic Config](../SKILL.md)

# DBeaver Format Reference

<!-- ADR: 2025-12-09-clickhouse-pydantic-config-skill -->

Complete specification of the DBeaver `data-sources.json` format for ClickHouse connections.

## File Location

DBeaver stores connection configurations in:

```
.dbeaver/data-sources.json
```

This file should be **gitignored** as it may contain credentials.

## JSON Structure

```json
{
  "folders": {},
  "connections": {
    "clickhouse-jdbc-{random-hex}": {
      "provider": "clickhouse",
      "driver": "com_clickhouse",
      "name": "Connection Display Name",
      "configuration": {
        "host": "localhost",
        "port": "8123",
        "database": "default",
        "url": "jdbc:clickhouse:http://localhost:8123/default",
        "type": "dev",
        "auth-model": "native",
        "user": "default",
        "password": ""
      }
    }
  }
}
```

## Field Reference

### Root Level

| Field         | Type   | Description                    |
| ------------- | ------ | ------------------------------ |
| `folders`     | object | Connection folder organization |
| `connections` | object | Map of connection ID to config |

### Connection Entry

| Field           | Type   | Required | Description                |
| --------------- | ------ | -------- | -------------------------- |
| `provider`      | string | Yes      | Always `"clickhouse"`      |
| `driver`        | string | Yes      | Always `"com_clickhouse"`  |
| `name`          | string | Yes      | Display name in DBeaver UI |
| `configuration` | object | Yes      | Connection parameters      |

### Configuration Block

| Field         | Type   | Required | Description                      |
| ------------- | ------ | -------- | -------------------------------- |
| `host`        | string | Yes      | ClickHouse hostname              |
| `port`        | string | Yes      | HTTP port (as string)            |
| `database`    | string | Yes      | Default database                 |
| `url`         | string | Yes      | Full JDBC URL                    |
| `type`        | string | Yes      | `"dev"`, `"test"`, or `"prod"`   |
| `auth-model`  | string | Yes      | Always `"native"` for ClickHouse |
| `user`        | string | No       | Username (omit for prompt)       |
| `password`    | string | No       | Password (omit for prompt)       |
| `handler-ssl` | string | No       | `"openssl"` when SSL enabled     |
| `ssl-mode`    | string | No       | SSL verification mode            |

## Connection ID Format

Connection IDs must be unique and follow this pattern:

```
clickhouse-jdbc-{16-char-hex}
```

**Example**: `clickhouse-jdbc-a1b2c3d4e5f67890`

Generated using `secrets.token_hex(8)` in Python.

## JDBC URL Format

### Local (HTTP)

```
jdbc:clickhouse:http://{host}:{port}/{database}
```

**Example**: `jdbc:clickhouse:http://localhost:8123/default`

### Cloud (HTTPS)

```
jdbc:clickhouse:https://{host}:{port}/{database}
```

**Example**: `jdbc:clickhouse:https://xyz.clickhouse.cloud:8443/default`

## SSL Configuration

For cloud connections, add these fields to `configuration`:

```json
{
  "handler-ssl": "openssl",
  "ssl-mode": "require"
}
```

**SSL Modes**:

| Mode          | Description                             |
| ------------- | --------------------------------------- |
| `disable`     | No SSL                                  |
| `require`     | SSL required, no certificate validation |
| `verify-ca`   | Verify server certificate               |
| `verify-full` | Verify certificate and hostname         |

## Important Limitations

### No Variable Substitution

DBeaver does **NOT** support environment variable substitution in `data-sources.json`:

```json
// WRONG - will not work
{
  "host": "${CLICKHOUSE_HOST}",
  "password": "${CLICKHOUSE_PASSWORD}"
}

// CORRECT - pre-populate values at generation time
{
  "host": "localhost",
  "password": ""
}
```

### Port as String

The `port` field must be a **string**, not an integer:

```json
// WRONG
{ "port": 8123 }

// CORRECT
{ "port": "8123" }
```

## Complete Examples

### Local Development

```json
{
  "folders": {},
  "connections": {
    "clickhouse-jdbc-abc123def456": {
      "provider": "clickhouse",
      "driver": "com_clickhouse",
      "name": "ClickHouse Local",
      "configuration": {
        "host": "localhost",
        "port": "8123",
        "database": "default",
        "url": "jdbc:clickhouse:http://localhost:8123/default",
        "type": "dev",
        "auth-model": "native",
        "user": "default",
        "password": ""
      }
    }
  }
}
```

### ClickHouse Cloud

```json
{
  "folders": {},
  "connections": {
    "clickhouse-jdbc-789xyz012abc": {
      "provider": "clickhouse",
      "driver": "com_clickhouse",
      "name": "ClickHouse Cloud",
      "configuration": {
        "host": "xyz.clickhouse.cloud",
        "port": "8443",
        "database": "default",
        "url": "jdbc:clickhouse:https://xyz.clickhouse.cloud:8443/default",
        "type": "prod",
        "auth-model": "native",
        "handler-ssl": "openssl",
        "ssl-mode": "require",
        "user": "readonly_user",
        "password": "secret-password"
      }
    }
  }
}
```

## macOS Notes

### DBeaver Binary Path

Use the full binary path, NOT `open -a`:

```bash
# CORRECT
/Applications/DBeaver.app/Contents/MacOS/dbeaver -data .dbeaver-workspace &

# WRONG - does not support -data flag
open -a DBeaver
```

### Workspace Separation

Use `-data` flag to keep project-specific workspace:

```bash
dbeaver -data .dbeaver-workspace &
```

This prevents mixing connections across projects.

## Related

- [Pydantic Model Reference](./pydantic-model.md)
- [Parent Skill](../SKILL.md)
