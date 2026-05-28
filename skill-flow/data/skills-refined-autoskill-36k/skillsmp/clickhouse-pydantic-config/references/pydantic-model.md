**Skill**: [ClickHouse Pydantic Config](../SKILL.md)

# Pydantic Model Reference

<!-- ADR: 2025-12-09-clickhouse-pydantic-config-skill -->

Complete documentation for the `ClickHouseConnection` Pydantic v2 model.

## Model Overview

The `ClickHouseConnection` model serves as the Single Source of Truth (SSoT) for ClickHouse connection configuration. It provides:

- Type-safe configuration with validation
- Computed fields for derived values
- Mode-aware defaults (local vs cloud)
- Environment variable loading

## Fields

| Field             | Type                                              | Default              | Description                     |
| ----------------- | ------------------------------------------------- | -------------------- | ------------------------------- |
| `name`            | `str`                                             | `"clickhouse-local"` | Connection display name         |
| `mode`            | `ConnectionMode`                                  | `LOCAL`              | `local` or `cloud`              |
| `host`            | `str`                                             | `"localhost"`        | ClickHouse hostname             |
| `port`            | `int`                                             | `8123`               | HTTP port                       |
| `database`        | `str`                                             | `"default"`          | Default database                |
| `ssl_enabled`     | `bool`                                            | `False`              | Enable SSL/TLS                  |
| `ssl_mode`        | `Literal["disable", "require", "verify-ca", ...]` | `"disable"`          | SSL verification mode           |
| `connection_type` | `Literal["dev", "test", "prod"]`                  | `"dev"`              | Environment type for DBeaver UI |

## Computed Fields

### `jdbc_url`

Generates the JDBC connection URL:

```python
@computed_field
@property
def jdbc_url(self) -> str:
    protocol = "https" if self.ssl_enabled else "http"
    return f"jdbc:clickhouse:{protocol}://{self.host}:{self.port}/{self.database}"
```

**Examples**:

- Local: `jdbc:clickhouse:http://localhost:8123/default`
- Cloud: `jdbc:clickhouse:https://xyz.clickhouse.cloud:8443/default`

### `connection_id`

Generates unique DBeaver connection ID:

```python
@computed_field
@property
def connection_id(self) -> str:
    return f"clickhouse-jdbc-{secrets.token_hex(8)}"
```

**Example**: `clickhouse-jdbc-a1b2c3d4e5f67890`

## Model Validator

The `validate_mode_settings` validator automatically applies cloud defaults:

```python
@model_validator(mode='after')
def validate_mode_settings(self) -> 'ClickHouseConnection':
    if self.mode == ConnectionMode.CLOUD:
        self.port = 8443
        self.ssl_enabled = True
        self.ssl_mode = "require"
    return self
```

## Factory Methods

### `from_env()`

Creates a connection from environment variables:

```python
@classmethod
def from_env(cls, prefix: str = "CLICKHOUSE_") -> 'ClickHouseConnection':
    return cls(
        name=os.environ.get(f"{prefix}NAME", "clickhouse-local"),
        mode=ConnectionMode(os.environ.get(f"{prefix}MODE", "local")),
        host=os.environ.get(f"{prefix}HOST", "localhost"),
        port=int(os.environ.get(f"{prefix}PORT", "8123")),
        database=os.environ.get(f"{prefix}DATABASE", "default"),
        connection_type=os.environ.get(f"{prefix}TYPE", "dev")
    )
```

**Environment Variables**:

| Variable              | Default            |
| --------------------- | ------------------ |
| `CLICKHOUSE_NAME`     | `clickhouse-local` |
| `CLICKHOUSE_MODE`     | `local`            |
| `CLICKHOUSE_HOST`     | `localhost`        |
| `CLICKHOUSE_PORT`     | `8123`             |
| `CLICKHOUSE_DATABASE` | `default`          |
| `CLICKHOUSE_TYPE`     | `dev`              |

## Instance Methods

### `to_dbeaver_config()`

Generates DBeaver connection entry with mode-aware credential handling:

```python
def to_dbeaver_config(self) -> dict:
    config = {
        "provider": "clickhouse",
        "driver": "com_clickhouse",
        "name": self.name,
        "configuration": {
            "host": self.host,
            "port": str(self.port),
            "database": self.database,
            "url": self.jdbc_url,
            "type": self.connection_type,
            "auth-model": "native"
        }
    }

    # Credential handling by mode
    if self.mode == ConnectionMode.LOCAL:
        config["configuration"]["user"] = "default"
        config["configuration"]["password"] = ""
    elif self.mode == ConnectionMode.CLOUD:
        config["configuration"]["user"] = os.environ.get("CLICKHOUSE_USER_READONLY", "default")
        config["configuration"]["password"] = os.environ.get("CLICKHOUSE_PASSWORD_READONLY", "")

    return config
```

## Usage Examples

### Basic Local Connection

```python
conn = ClickHouseConnection()
print(conn.jdbc_url)  # jdbc:clickhouse:http://localhost:8123/default
```

### Cloud Connection

```python
conn = ClickHouseConnection(
    mode=ConnectionMode.CLOUD,
    host="xyz.clickhouse.cloud"
)
# Automatically sets port=8443, ssl_enabled=True, ssl_mode="require"
print(conn.jdbc_url)  # jdbc:clickhouse:https://xyz.clickhouse.cloud:8443/default
```

### From Environment

```python
# With mise [env] or exported variables
conn = ClickHouseConnection.from_env()
config = conn.to_dbeaver_config()
```

## ConnectionMode Enum

```python
class ConnectionMode(str, Enum):
    LOCAL = "local"
    CLOUD = "cloud"
```

## Related

- [DBeaver Format Reference](./dbeaver-format.md)
- [Parent Skill](../SKILL.md)
