---
name: sage-core-guidelines
description: Use this skill when working with the core components of the Sage framework, including session management, sandbox security, and configuration systems.
---

# Sage Core Guidelines

## Overview

The Sage framework consists of several core modules that provide essential functionalities such as session management, sandbox security, and configuration systems. This guide outlines the key components and their usage.

### 1. Session Management

The session management module provides features for session persistence, recovery, and branching. It includes the following components:

- **Session Structure**: Defines the core attributes of a session, including ID, name, timestamps, working directory, associated Git branch, messages, token usage, and state.

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Session {
    pub id: SessionId,
    pub name: Option<String>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub working_directory: PathBuf,
    pub git_branch: Option<String>,
    pub messages: Vec<ConversationMessage>,
    pub token_usage: TokenUsage,
    pub state: SessionState,
    pub error: Option<String>,
}
```

### 2. Sandbox Security

The sandbox security module is crucial for ensuring command safety and access control. It implements a multi-layer security model that includes:

- **OS-Level Isolation**: Utilizes macOS sandbox-exec or Linux seccomp for strong isolation.
- **Resource Limits**: Enforces limits on CPU, memory, and output.
- **Policy-Based Controls**: Implements command filtering and path access control.

### 3. Configuration System

The configuration system is responsible for loading, managing, and validating configurations and credentials. Key components include:

- **Main Configuration Structure**: Defines the primary configuration attributes, such as default provider, execution limits, and model parameters.

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(default)]
pub struct Config {
    pub default_provider: String,
    pub max_steps: Option<u32>,
    pub total_token_budget: Option<u64>,
    pub model_providers: HashMap<String, ModelParameters>,
    pub enable_lakeview: bool,
}
```

## When to Use

Use this skill when you need to manage sessions, ensure security in command execution, or handle configuration settings within the Sage framework. This guide provides a comprehensive overview of the core components and their interactions.