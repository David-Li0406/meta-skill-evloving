# Serde Serialization Patterns

## Basic Derive

```rust
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    id: u64,
    name: String,
    email: String,
    #[serde(default)]
    active: bool,
}

// Usage
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let user = User {
        id: 1,
        name: "John".into(),
        email: "john@example.com".into(),
        active: true,
    };

    // To JSON
    let json = serde_json::to_string(&user)?;
    let json_pretty = serde_json::to_string_pretty(&user)?;

    // From JSON
    let parsed: User = serde_json::from_str(&json)?;

    Ok(())
}
```

## Field Attributes

```rust
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct User {
    user_id: u64,  // Serializes as "userId"
    
    #[serde(rename = "userName")]
    name: String,
    
    #[serde(skip_serializing_if = "Option::is_none")]
    bio: Option<String>,
    
    #[serde(skip)]
    internal_state: String,
    
    #[serde(default = "default_role")]
    role: String,
    
    #[serde(flatten)]
    metadata: Metadata,
    
    #[serde(with = "chrono::serde::ts_seconds")]
    created_at: DateTime<Utc>,
}

fn default_role() -> String {
    "user".into()
}

#[derive(Serialize, Deserialize)]
struct Metadata {
    source: String,
    version: u32,
}
```

## Enum Representations

```rust
// Default: externally tagged
#[derive(Serialize, Deserialize)]
enum Message {
    Text(String),           // {"Text": "hello"}
    Image { url: String },  // {"Image": {"url": "..."}}
    Ping,                   // "Ping"
}

// Internally tagged
#[derive(Serialize, Deserialize)]
#[serde(tag = "type")]
enum Event {
    Click { x: i32, y: i32 },  // {"type": "Click", "x": 10, "y": 20}
    KeyPress { key: String },
}

// Adjacently tagged
#[derive(Serialize, Deserialize)]
#[serde(tag = "type", content = "data")]
enum Response {
    Success(Data),  // {"type": "Success", "data": {...}}
    Error(String),
}

// Untagged
#[derive(Serialize, Deserialize)]
#[serde(untagged)]
enum Value {
    Integer(i64),
    Float(f64),
    Text(String),
}
```

## Custom Serializers

```rust
use serde::{Serializer, Deserializer};

#[derive(Serialize, Deserialize)]
struct Config {
    #[serde(serialize_with = "serialize_duration")]
    #[serde(deserialize_with = "deserialize_duration")]
    timeout: Duration,
}

fn serialize_duration<S>(duration: &Duration, s: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
{
    s.serialize_u64(duration.as_secs())
}

fn deserialize_duration<'de, D>(d: D) -> Result<Duration, D::Error>
where
    D: Deserializer<'de>,
{
    let secs = u64::deserialize(d)?;
    Ok(Duration::from_secs(secs))
}

// Or use a module
mod duration_secs {
    use super::*;
    
    pub fn serialize<S>(duration: &Duration, s: S) -> Result<S::Ok, S::Error>
    where S: Serializer {
        s.serialize_u64(duration.as_secs())
    }
    
    pub fn deserialize<'de, D>(d: D) -> Result<Duration, D::Error>
    where D: Deserializer<'de> {
        let secs = u64::deserialize(d)?;
        Ok(Duration::from_secs(secs))
    }
}

#[derive(Serialize, Deserialize)]
struct Config {
    #[serde(with = "duration_secs")]
    timeout: Duration,
}
```

## Generic Types

```rust
#[derive(Serialize, Deserialize)]
struct Response<T> {
    success: bool,
    data: Option<T>,
    error: Option<String>,
}

#[derive(Serialize, Deserialize)]
#[serde(bound = "T: Serialize + DeserializeOwned")]
struct Paginated<T> {
    items: Vec<T>,
    page: u32,
    total: u32,
}
```

## Different Formats

```rust
// JSON
let json = serde_json::to_string(&data)?;
let data: Data = serde_json::from_str(&json)?;

// YAML
let yaml = serde_yaml::to_string(&data)?;
let data: Data = serde_yaml::from_str(&yaml)?;

// TOML
let toml = toml::to_string(&data)?;
let data: Data = toml::from_str(&toml)?;

// Bincode (binary)
let bytes = bincode::serialize(&data)?;
let data: Data = bincode::deserialize(&bytes)?;
```
