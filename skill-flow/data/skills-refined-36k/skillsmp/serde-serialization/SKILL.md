---
name: Serde Serialization
description: Rust serialization/deserialization framework for JSON, YAML, TOML, and more.
metadata:
  labels: [rust, serde, serialization, json]
  triggers:
    files: ['**/*.rs']
    keywords: [Serialize, Deserialize, serde, serde_json]
---

# Serde Standards

## Basic Usage

```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    id: u64,
    name: String,
    email: String,
    #[serde(default)]
    active: bool,
}

// Serialize to JSON
let user = User { id: 1, name: "Alice".into(), email: "a@b.com".into(), active: true };
let json = serde_json::to_string(&user)?;

// Deserialize from JSON
let user: User = serde_json::from_str(&json)?;
```

## Field Attributes

```rust
#[derive(Serialize, Deserialize)]
struct Config {
    // Rename field in JSON
    #[serde(rename = "apiKey")]
    api_key: String,

    // Skip serializing if None
    #[serde(skip_serializing_if = "Option::is_none")]
    description: Option<String>,

    // Default value if missing
    #[serde(default = "default_timeout")]
    timeout_secs: u64,

    // Skip entirely
    #[serde(skip)]
    internal_state: bool,

    // Flatten nested struct
    #[serde(flatten)]
    metadata: Metadata,
}

fn default_timeout() -> u64 { 30 }
```

## Enums

```rust
#[derive(Serialize, Deserialize)]
#[serde(tag = "type")]  // Tagged union
enum Event {
    #[serde(rename = "user_created")]
    UserCreated { id: u64, email: String },

    #[serde(rename = "user_deleted")]
    UserDeleted { id: u64 },
}

// Serializes as: {"type": "user_created", "id": 1, "email": "..."}

// Untagged variant
#[derive(Serialize, Deserialize)]
#[serde(untagged)]
enum Value {
    Integer(i64),
    Float(f64),
    String(String),
}
```

## Custom Serialization

```rust
use serde::{Serializer, Deserializer};

#[derive(Serialize, Deserialize)]
struct Record {
    #[serde(serialize_with = "serialize_datetime")]
    #[serde(deserialize_with = "deserialize_datetime")]
    created_at: DateTime<Utc>,
}

fn serialize_datetime<S>(dt: &DateTime<Utc>, s: S) -> Result<S::Ok, S::Error>
where S: Serializer {
    s.serialize_str(&dt.to_rfc3339())
}

fn deserialize_datetime<'de, D>(d: D) -> Result<DateTime<Utc>, D::Error>
where D: Deserializer<'de> {
    let s = String::deserialize(d)?;
    DateTime::parse_from_rfc3339(&s)
        .map(|dt| dt.with_timezone(&Utc))
        .map_err(serde::de::Error::custom)
}
```

## Format Support

| Format | Crate | Use Case |
|--------|-------|----------|
| JSON | `serde_json` | APIs, config |
| YAML | `serde_yaml` | Config files |
| TOML | `toml` | Cargo.toml style |
| MessagePack | `rmp-serde` | Binary, compact |
| CBOR | `ciborium` | Binary, standards |

## Validation with Derive

```rust
use serde::Deserialize;
use validator::Validate;

#[derive(Deserialize, Validate)]
struct CreateUser {
    #[validate(length(min = 1, max = 100))]
    name: String,

    #[validate(email)]
    email: String,

    #[validate(range(min = 18, max = 120))]
    age: u8,
}
```

## Best Practices

1. **Deny unknown fields**: `#[serde(deny_unknown_fields)]` for strict parsing
2. **Rename all**: `#[serde(rename_all = "camelCase")]` for consistent naming
3. **Default trait**: Implement `Default` for optional defaults
4. **Error context**: Use `anyhow` or custom errors for better messages
5. **Performance**: Use `serde_json::from_slice` for bytes, avoid string conversion
