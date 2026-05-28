---
name: sage-system-management
description: Use this skill when managing sessions, security, and configuration in the Sage system, including session persistence, sandbox security, and configuration loading.
---

# Sage System Management Development Guide

## Module Overview

The Sage system management module encompasses session management, sandbox security, and configuration management, providing a comprehensive framework for managing the Sage environment.

### 1. Session Management

#### 1.1 Overview

The session management module provides session persistence and recovery features, including session creation, restoration, and branching management.

```rust
// Example of session structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Session {
    pub id: SessionId,
    pub name: Option<String>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub working_directory: PathBuf,
    pub messages: Vec<ConversationMessage>,
    pub state: SessionState,
}
```

#### 1.2 SessionManager

The `SessionManager` handles the creation, restoration, and management of sessions.

```rust
impl SessionManager {
    pub async fn create(&self, config: SessionConfig) -> SageResult<SessionId>;
    pub async fn resume(&self, id: &SessionId) -> SageResult<Session>;
    pub async fn save(&self, session: &Session) -> SageResult<()>;
}
```

### 2. Sandbox Security

#### 2.1 Overview

The sandbox security module provides multi-layer security protections, including command validation, path policies, and OS-level isolation.

```rust
#[async_trait]
pub trait Sandbox: Send + Sync {
    fn check_path(&self, path: &PathBuf, write: bool) -> SandboxResult<()>;
    fn check_command(&self, command: &str) -> SandboxResult<()>;
}
```

#### 2.2 Command Validation

The command validation system checks for potential security issues in commands before execution.

```rust
pub fn validate_command(command: &str, context: &ValidationContext) -> ValidationResult;
```

### 3. Configuration Management

#### 3.1 Overview

The configuration management module handles multi-source loading, credential management, and runtime persistence.

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub default_provider: String,
    pub max_steps: Option<u32>,
    pub model_providers: HashMap<String, ModelParameters>,
}
```

#### 3.2 ConfigLoader

The `ConfigLoader` facilitates loading configurations from various sources, including files, environment variables, and command-line arguments.

```rust
pub struct ConfigLoader {
    sources: Vec<ConfigSource>,
}

impl ConfigLoader {
    pub fn load(self) -> SageResult<Config>;
}
```

### 4. Usage Examples

#### 4.1 Basic Session Management

```rust
let manager = SessionManager::in_memory();
let session_id = manager.create(config).await?;
manager.add_message(&session_id, ConversationMessage::user("Hello!")).await?;
```

#### 4.2 Sandbox Security Check

```rust
let sandbox = DefaultSandbox::new(config);
sandbox.check_command("rm -rf /").await?;
```

#### 4.3 Configuration Loading

```rust
let config = ConfigLoader::new()
    .with_file("~/.sage/config.json")
    .with_env()
    .load()?;
```

### 5. Development Guidelines

#### 5.1 Adding New Session Features

1. Extend the `Session` struct with new fields.
2. Update the `SessionManager` methods to handle new session features.

#### 5.2 Enhancing Sandbox Security

1. Implement new validation checks in the `validation` module.
2. Update the `Sandbox` trait to include new security checks.

#### 5.3 Extending Configuration Management

1. Add new configuration fields in the `Config` struct.
2. Implement validation rules for new fields in the `validation` module.

---

*Last updated: 2026-01-10*