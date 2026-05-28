---
name: mcp-gateway
description: LiteLLM-RS MCP Gateway Architecture. Covers Model Context Protocol, JSON-RPC 2.0 implementation, multi-transport support (HTTP, SSE, WebSocket, Stdio), and permission system.
---

# MCP Gateway Architecture Guide

## Overview

The MCP (Model Context Protocol) Gateway enables LLMs to interact with external tools and services through a standardized protocol. LiteLLM-RS implements MCP with multiple transports and fine-grained permission control.

### MCP Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        LLM Provider                             │
│  (OpenAI, Anthropic, etc. with tool/function calling)          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ Tool calls
┌─────────────────────────────────────────────────────────────────┐
│                      MCP Gateway                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Tool Registry                           │   │
│  │  - Aggregates tools from all connected servers          │   │
│  │  - Handles routing and permission checks                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  MCP Server  │ │  MCP Server  │ │  MCP Server  │ │  MCP Server  │
│    (HTTP)    │ │    (SSE)     │ │ (WebSocket)  │ │   (Stdio)    │
│  Database    │ │  File System │ │    Slack     │ │   Local CLI  │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

---

## JSON-RPC 2.0 Protocol

### Request Format

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsonRpcRequest {
    pub jsonrpc: String,  // Always "2.0"
    pub id: JsonRpcId,
    pub method: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub params: Option<serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum JsonRpcId {
    Number(i64),
    String(String),
    Null,
}

impl JsonRpcRequest {
    pub fn new(method: impl Into<String>, params: Option<serde_json::Value>) -> Self {
        Self {
            jsonrpc: "2.0".to_string(),
            id: JsonRpcId::Number(rand::random()),
            method: method.into(),
            params,
        }
    }

    pub fn initialize(client_info: &ClientInfo) -> Self {
        Self::new("initialize", Some(serde_json::json!({
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "prompts": {},
                "resources": {}
            },
            "clientInfo": client_info
        })))
    }

    pub fn list_tools() -> Self {
        Self::new("tools/list", None)
    }

    pub fn call_tool(name: &str, arguments: serde_json::Value) -> Self {
        Self::new("tools/call", Some(serde_json::json!({
            "name": name,
            "arguments": arguments
        })))
    }
}
```

### Response Format

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsonRpcResponse {
    pub jsonrpc: String,
    pub id: JsonRpcId,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub result: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<JsonRpcError>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsonRpcError {
    pub code: i32,
    pub message: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub data: Option<serde_json::Value>,
}

// Standard error codes
impl JsonRpcError {
    pub const PARSE_ERROR: i32 = -32700;
    pub const INVALID_REQUEST: i32 = -32600;
    pub const METHOD_NOT_FOUND: i32 = -32601;
    pub const INVALID_PARAMS: i32 = -32602;
    pub const INTERNAL_ERROR: i32 = -32603;

    pub fn parse_error(message: impl Into<String>) -> Self {
        Self {
            code: Self::PARSE_ERROR,
            message: message.into(),
            data: None,
        }
    }

    pub fn method_not_found(method: &str) -> Self {
        Self {
            code: Self::METHOD_NOT_FOUND,
            message: format!("Method not found: {}", method),
            data: None,
        }
    }

    pub fn invalid_params(message: impl Into<String>) -> Self {
        Self {
            code: Self::INVALID_PARAMS,
            message: message.into(),
            data: None,
        }
    }

    pub fn internal_error(message: impl Into<String>) -> Self {
        Self {
            code: Self::INTERNAL_ERROR,
            message: message.into(),
            data: None,
        }
    }
}
```

---

## Transport Implementations

### Transport Trait

```rust
#[async_trait]
pub trait McpTransport: Send + Sync {
    /// Send a request and wait for response
    async fn send_request(&self, request: JsonRpcRequest) -> Result<JsonRpcResponse, McpError>;

    /// Send a notification (no response expected)
    async fn send_notification(&self, notification: JsonRpcRequest) -> Result<(), McpError>;

    /// Check if transport is connected
    fn is_connected(&self) -> bool;

    /// Close the transport
    async fn close(&self) -> Result<(), McpError>;
}
```

### HTTP Transport

```rust
pub struct HttpTransport {
    client: reqwest::Client,
    base_url: String,
    auth: Option<AuthConfig>,
}

impl HttpTransport {
    pub fn new(base_url: &str, auth: Option<AuthConfig>) -> Self {
        let mut client_builder = reqwest::Client::builder()
            .timeout(Duration::from_secs(30));

        Self {
            client: client_builder.build().unwrap(),
            base_url: base_url.to_string(),
            auth,
        }
    }
}

#[async_trait]
impl McpTransport for HttpTransport {
    async fn send_request(&self, request: JsonRpcRequest) -> Result<JsonRpcResponse, McpError> {
        let mut req = self.client
            .post(&self.base_url)
            .header("Content-Type", "application/json");

        // Add authentication
        if let Some(auth) = &self.auth {
            req = match auth {
                AuthConfig::Bearer { token } => {
                    req.header("Authorization", format!("Bearer {}", token))
                }
                AuthConfig::ApiKey { header, key } => {
                    req.header(header, key)
                }
                AuthConfig::Basic { username, password } => {
                    req.basic_auth(username, Some(password))
                }
            };
        }

        let response = req
            .json(&request)
            .send()
            .await
            .map_err(|e| McpError::Transport(e.to_string()))?;

        if !response.status().is_success() {
            return Err(McpError::Transport(format!(
                "HTTP error: {}",
                response.status()
            )));
        }

        response
            .json()
            .await
            .map_err(|e| McpError::Transport(e.to_string()))
    }

    async fn send_notification(&self, notification: JsonRpcRequest) -> Result<(), McpError> {
        let _ = self.send_request(notification).await?;
        Ok(())
    }

    fn is_connected(&self) -> bool {
        true  // HTTP is stateless
    }

    async fn close(&self) -> Result<(), McpError> {
        Ok(())  // Nothing to close for HTTP
    }
}
```

### SSE Transport

```rust
use futures::StreamExt;
use tokio::sync::mpsc;

pub struct SseTransport {
    base_url: String,
    event_sender: mpsc::Sender<JsonRpcRequest>,
    response_receiver: mpsc::Receiver<JsonRpcResponse>,
    connected: Arc<AtomicBool>,
}

impl SseTransport {
    pub async fn connect(base_url: &str, auth: Option<AuthConfig>) -> Result<Self, McpError> {
        let (event_tx, event_rx) = mpsc::channel(100);
        let (response_tx, response_rx) = mpsc::channel(100);
        let connected = Arc::new(AtomicBool::new(false));
        let connected_clone = connected.clone();

        // Start SSE listener
        let url = format!("{}/events", base_url);
        tokio::spawn(async move {
            let client = reqwest::Client::new();
            let response = client.get(&url).send().await;

            if let Ok(response) = response {
                connected_clone.store(true, Ordering::SeqCst);

                let mut stream = response.bytes_stream();
                let mut buffer = String::new();

                while let Some(chunk) = stream.next().await {
                    if let Ok(bytes) = chunk {
                        buffer.push_str(&String::from_utf8_lossy(&bytes));

                        // Parse SSE events
                        while let Some(event_end) = buffer.find("\n\n") {
                            let event_data = buffer[..event_end].to_string();
                            buffer = buffer[event_end + 2..].to_string();

                            if let Some(data) = event_data.strip_prefix("data: ") {
                                if let Ok(response) = serde_json::from_str::<JsonRpcResponse>(data) {
                                    let _ = response_tx.send(response).await;
                                }
                            }
                        }
                    }
                }

                connected_clone.store(false, Ordering::SeqCst);
            }
        });

        Ok(Self {
            base_url: base_url.to_string(),
            event_sender: event_tx,
            response_receiver: response_rx,
            connected,
        })
    }
}

#[async_trait]
impl McpTransport for SseTransport {
    async fn send_request(&self, request: JsonRpcRequest) -> Result<JsonRpcResponse, McpError> {
        // Send request via POST
        let client = reqwest::Client::new();
        client
            .post(&format!("{}/message", self.base_url))
            .json(&request)
            .send()
            .await
            .map_err(|e| McpError::Transport(e.to_string()))?;

        // Wait for response via SSE
        tokio::time::timeout(
            Duration::from_secs(30),
            self.response_receiver.recv()
        )
        .await
        .map_err(|_| McpError::Timeout)?
        .ok_or(McpError::Transport("Channel closed".to_string()))
    }

    fn is_connected(&self) -> bool {
        self.connected.load(Ordering::SeqCst)
    }

    async fn close(&self) -> Result<(), McpError> {
        self.connected.store(false, Ordering::SeqCst);
        Ok(())
    }
}
```

### WebSocket Transport

```rust
use tokio_tungstenite::{connect_async, tungstenite::Message};

pub struct WebSocketTransport {
    sender: mpsc::Sender<Message>,
    response_receiver: mpsc::Receiver<JsonRpcResponse>,
    connected: Arc<AtomicBool>,
}

impl WebSocketTransport {
    pub async fn connect(url: &str) -> Result<Self, McpError> {
        let (ws_stream, _) = connect_async(url)
            .await
            .map_err(|e| McpError::Transport(e.to_string()))?;

        let (write, read) = ws_stream.split();
        let (tx, rx) = mpsc::channel(100);
        let (response_tx, response_rx) = mpsc::channel(100);
        let connected = Arc::new(AtomicBool::new(true));

        // Writer task
        let connected_writer = connected.clone();
        tokio::spawn(async move {
            let mut rx = rx;
            let mut write = write;
            while let Some(msg) = rx.recv().await {
                if write.send(msg).await.is_err() {
                    connected_writer.store(false, Ordering::SeqCst);
                    break;
                }
            }
        });

        // Reader task
        let connected_reader = connected.clone();
        tokio::spawn(async move {
            let mut read = read;
            while let Some(Ok(msg)) = read.next().await {
                if let Message::Text(text) = msg {
                    if let Ok(response) = serde_json::from_str::<JsonRpcResponse>(&text) {
                        let _ = response_tx.send(response).await;
                    }
                }
            }
            connected_reader.store(false, Ordering::SeqCst);
        });

        Ok(Self {
            sender: tx,
            response_receiver: response_rx,
            connected,
        })
    }
}

#[async_trait]
impl McpTransport for WebSocketTransport {
    async fn send_request(&self, request: JsonRpcRequest) -> Result<JsonRpcResponse, McpError> {
        let json = serde_json::to_string(&request)
            .map_err(|e| McpError::Serialization(e.to_string()))?;

        self.sender
            .send(Message::Text(json))
            .await
            .map_err(|e| McpError::Transport(e.to_string()))?;

        tokio::time::timeout(
            Duration::from_secs(30),
            self.response_receiver.recv()
        )
        .await
        .map_err(|_| McpError::Timeout)?
        .ok_or(McpError::Transport("Channel closed".to_string()))
    }

    fn is_connected(&self) -> bool {
        self.connected.load(Ordering::SeqCst)
    }

    async fn close(&self) -> Result<(), McpError> {
        self.connected.store(false, Ordering::SeqCst);
        Ok(())
    }
}
```

### Stdio Transport

```rust
use tokio::process::{Child, Command};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};

pub struct StdioTransport {
    child: Child,
    stdin: tokio::process::ChildStdin,
    response_receiver: mpsc::Receiver<JsonRpcResponse>,
}

impl StdioTransport {
    pub async fn spawn(command: &str, args: &[&str]) -> Result<Self, McpError> {
        let mut child = Command::new(command)
            .args(args)
            .stdin(std::process::Stdio::piped())
            .stdout(std::process::Stdio::piped())
            .stderr(std::process::Stdio::piped())
            .spawn()
            .map_err(|e| McpError::Transport(format!("Failed to spawn process: {}", e)))?;

        let stdin = child.stdin.take().unwrap();
        let stdout = child.stdout.take().unwrap();

        let (response_tx, response_rx) = mpsc::channel(100);

        // Reader task
        tokio::spawn(async move {
            let reader = BufReader::new(stdout);
            let mut lines = reader.lines();

            while let Ok(Some(line)) = lines.next_line().await {
                if let Ok(response) = serde_json::from_str::<JsonRpcResponse>(&line) {
                    let _ = response_tx.send(response).await;
                }
            }
        });

        Ok(Self {
            child,
            stdin,
            response_receiver: response_rx,
        })
    }
}

#[async_trait]
impl McpTransport for StdioTransport {
    async fn send_request(&self, request: JsonRpcRequest) -> Result<JsonRpcResponse, McpError> {
        let json = serde_json::to_string(&request)
            .map_err(|e| McpError::Serialization(e.to_string()))?;

        self.stdin
            .write_all(format!("{}\n", json).as_bytes())
            .await
            .map_err(|e| McpError::Transport(e.to_string()))?;

        self.stdin
            .flush()
            .await
            .map_err(|e| McpError::Transport(e.to_string()))?;

        tokio::time::timeout(
            Duration::from_secs(30),
            self.response_receiver.recv()
        )
        .await
        .map_err(|_| McpError::Timeout)?
        .ok_or(McpError::Transport("Channel closed".to_string()))
    }

    fn is_connected(&self) -> bool {
        // Check if process is still running
        true  // Would need to track process state
    }

    async fn close(&self) -> Result<(), McpError> {
        self.child.kill().await.ok();
        Ok(())
    }
}
```

---

## Tool Registry

### Tool Definition

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolDefinition {
    pub name: String,
    pub description: String,
    #[serde(rename = "inputSchema")]
    pub input_schema: serde_json::Value,
}

#[derive(Debug, Clone)]
pub struct RegisteredTool {
    pub definition: ToolDefinition,
    pub server_name: String,
    pub transport: Arc<dyn McpTransport>,
}
```

### Tool Registry Implementation

```rust
use dashmap::DashMap;

pub struct ToolRegistry {
    tools: DashMap<String, RegisteredTool>,
    permissions: Arc<PermissionManager>,
}

impl ToolRegistry {
    pub fn new(permissions: Arc<PermissionManager>) -> Self {
        Self {
            tools: DashMap::new(),
            permissions,
        }
    }

    pub fn register_tool(&self, tool: RegisteredTool) {
        self.tools.insert(tool.definition.name.clone(), tool);
    }

    pub fn unregister_tools(&self, server_name: &str) {
        self.tools.retain(|_, tool| tool.server_name != server_name);
    }

    pub fn get_tool(&self, name: &str) -> Option<RegisteredTool> {
        self.tools.get(name).map(|t| t.clone())
    }

    pub fn list_tools(&self, user_id: &str) -> Vec<ToolDefinition> {
        self.tools
            .iter()
            .filter(|entry| {
                self.permissions.can_use_tool(user_id, &entry.definition.name)
            })
            .map(|entry| entry.definition.clone())
            .collect()
    }

    pub async fn call_tool(
        &self,
        user_id: &str,
        name: &str,
        arguments: serde_json::Value,
    ) -> Result<serde_json::Value, McpError> {
        // Check permissions
        if !self.permissions.can_use_tool(user_id, name) {
            return Err(McpError::PermissionDenied(format!(
                "User {} cannot use tool {}",
                user_id, name
            )));
        }

        // Get tool
        let tool = self.tools.get(name)
            .ok_or_else(|| McpError::ToolNotFound(name.to_string()))?;

        // Call via transport
        let request = JsonRpcRequest::call_tool(name, arguments);
        let response = tool.transport.send_request(request).await?;

        if let Some(error) = response.error {
            return Err(McpError::ToolError(error.message));
        }

        response.result.ok_or(McpError::EmptyResponse)
    }
}
```

---

## Permission System

### Permission Configuration

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PermissionConfig {
    pub default_policy: Policy,
    pub rules: Vec<PermissionRule>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Policy {
    Allow,
    Deny,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PermissionRule {
    pub users: Vec<String>,      // User patterns (supports *)
    pub tools: Vec<String>,      // Tool patterns (supports *)
    pub servers: Vec<String>,    // Server patterns (supports *)
    pub policy: Policy,
}
```

### Permission Manager

```rust
pub struct PermissionManager {
    config: PermissionConfig,
}

impl PermissionManager {
    pub fn new(config: PermissionConfig) -> Self {
        Self { config }
    }

    pub fn can_use_tool(&self, user_id: &str, tool_name: &str) -> bool {
        // Check rules in order (first match wins)
        for rule in &self.config.rules {
            if self.matches_pattern(&rule.users, user_id)
                && self.matches_pattern(&rule.tools, tool_name)
            {
                return matches!(rule.policy, Policy::Allow);
            }
        }

        // Fall back to default policy
        matches!(self.config.default_policy, Policy::Allow)
    }

    pub fn can_use_server(&self, user_id: &str, server_name: &str) -> bool {
        for rule in &self.config.rules {
            if self.matches_pattern(&rule.users, user_id)
                && self.matches_pattern(&rule.servers, server_name)
            {
                return matches!(rule.policy, Policy::Allow);
            }
        }

        matches!(self.config.default_policy, Policy::Allow)
    }

    fn matches_pattern(&self, patterns: &[String], value: &str) -> bool {
        patterns.iter().any(|pattern| {
            if pattern == "*" {
                true
            } else if pattern.ends_with('*') {
                value.starts_with(&pattern[..pattern.len() - 1])
            } else if pattern.starts_with('*') {
                value.ends_with(&pattern[1..])
            } else {
                pattern == value
            }
        })
    }
}
```

---

## MCP Gateway

### Gateway Implementation

```rust
pub struct McpGateway {
    servers: DashMap<String, Arc<McpServer>>,
    tool_registry: Arc<ToolRegistry>,
    config: McpGatewayConfig,
}

impl McpGateway {
    pub fn new(config: McpGatewayConfig) -> Self {
        let permissions = Arc::new(PermissionManager::new(config.permissions.clone()));
        let tool_registry = Arc::new(ToolRegistry::new(permissions));

        Self {
            servers: DashMap::new(),
            tool_registry,
            config,
        }
    }

    pub async fn connect_server(&self, server_config: &McpServerConfig) -> Result<(), McpError> {
        let transport: Arc<dyn McpTransport> = match &server_config.transport {
            TransportConfig::Http { url, auth } => {
                Arc::new(HttpTransport::new(url, auth.clone()))
            }
            TransportConfig::Sse { url, auth } => {
                Arc::new(SseTransport::connect(url, auth.clone()).await?)
            }
            TransportConfig::WebSocket { url } => {
                Arc::new(WebSocketTransport::connect(url).await?)
            }
            TransportConfig::Stdio { command, args } => {
                Arc::new(StdioTransport::spawn(command, args).await?)
            }
        };

        // Initialize connection
        let init_request = JsonRpcRequest::initialize(&ClientInfo {
            name: "litellm-gateway".to_string(),
            version: env!("CARGO_PKG_VERSION").to_string(),
        });
        transport.send_request(init_request).await?;

        // List tools
        let tools_request = JsonRpcRequest::list_tools();
        let tools_response = transport.send_request(tools_request).await?;

        let tools: Vec<ToolDefinition> = serde_json::from_value(
            tools_response.result.unwrap_or(serde_json::json!({ "tools": [] }))
        ).unwrap_or_default();

        // Register tools
        for tool in tools {
            self.tool_registry.register_tool(RegisteredTool {
                definition: tool,
                server_name: server_config.name.clone(),
                transport: transport.clone(),
            });
        }

        let server = McpServer {
            name: server_config.name.clone(),
            transport,
        };

        self.servers.insert(server_config.name.clone(), Arc::new(server));

        Ok(())
    }

    pub fn list_tools(&self, user_id: &str) -> Vec<ToolDefinition> {
        self.tool_registry.list_tools(user_id)
    }

    pub async fn call_tool(
        &self,
        user_id: &str,
        name: &str,
        arguments: serde_json::Value,
    ) -> Result<serde_json::Value, McpError> {
        self.tool_registry.call_tool(user_id, name, arguments).await
    }
}
```

---

## Configuration

```yaml
mcp:
  enabled: true

  servers:
    - name: "database"
      transport:
        type: "http"
        url: "http://localhost:3001/mcp"
        auth:
          type: "bearer"
          token: ${MCP_DATABASE_TOKEN}

    - name: "filesystem"
      transport:
        type: "stdio"
        command: "npx"
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/data"]

    - name: "slack"
      transport:
        type: "sse"
        url: "http://localhost:3002/events"
        auth:
          type: "api_key"
          header: "X-API-Key"
          key: ${SLACK_MCP_KEY}

  permissions:
    default_policy: "deny"
    rules:
      - users: ["admin*"]
        tools: ["*"]
        servers: ["*"]
        policy: "allow"

      - users: ["*"]
        tools: ["query_*", "read_*"]
        servers: ["database", "filesystem"]
        policy: "allow"

      - users: ["*"]
        tools: ["write_*", "delete_*"]
        servers: ["*"]
        policy: "deny"
```

---

## Error Types

```rust
#[derive(Debug, thiserror::Error)]
pub enum McpError {
    #[error("Transport error: {0}")]
    Transport(String),

    #[error("Serialization error: {0}")]
    Serialization(String),

    #[error("Tool not found: {0}")]
    ToolNotFound(String),

    #[error("Tool error: {0}")]
    ToolError(String),

    #[error("Permission denied: {0}")]
    PermissionDenied(String),

    #[error("Server not found: {0}")]
    ServerNotFound(String),

    #[error("Request timeout")]
    Timeout,

    #[error("Empty response")]
    EmptyResponse,

    #[error("JSON-RPC error: {0}")]
    JsonRpc(String),
}
```
