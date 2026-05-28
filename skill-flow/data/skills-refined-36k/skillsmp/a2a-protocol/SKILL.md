---
name: a2a-protocol
description: LiteLLM-RS A2A Protocol Architecture. Covers Agent-to-Agent communication, JSON-RPC 2.0 messaging, multi-provider orchestration, agent registry, and task state management.
---

# A2A Protocol Architecture Guide

## Overview

The A2A (Agent-to-Agent) Protocol enables autonomous agents to communicate and collaborate through a standardized interface. LiteLLM-RS implements A2A with support for multiple agent providers (LangGraph, Vertex AI Agent Builder, Azure AI Agent Service, Amazon Bedrock Agents, Pydantic AI).

### A2A Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Client Application                        │
│  (User, Orchestrator, or Another Agent)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ JSON-RPC 2.0
┌─────────────────────────────────────────────────────────────────┐
│                       A2A Gateway                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Agent Registry                          │   │
│  │  - Agent discovery and registration                      │   │
│  │  - Health monitoring and load balancing                  │   │
│  │  - Capability matching                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   LangGraph  │ │  Vertex AI   │ │   Azure AI   │ │   Bedrock    │
│    Agent     │ │    Agent     │ │    Agent     │ │    Agent     │
│  (Python)    │ │   Builder    │ │   Service    │ │   Agents     │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

---

## JSON-RPC 2.0 Message Format

### Request Structure

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct A2ARequest {
    pub jsonrpc: String,  // Always "2.0"
    pub id: A2ARequestId,
    pub method: A2AMethod,
    pub params: Option<serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum A2ARequestId {
    Number(i64),
    String(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum A2AMethod {
    /// Send a task to an agent
    TaskSend,
    /// Get task status
    TaskGet,
    /// Cancel a running task
    TaskCancel,
    /// Subscribe to task updates (SSE)
    TaskSendSubscribe,
    /// Get agent capabilities
    AgentCapabilities,
    /// Ping for health check
    Ping,
}

impl A2ARequest {
    pub fn task_send(task: &Task) -> Self {
        Self {
            jsonrpc: "2.0".to_string(),
            id: A2ARequestId::String(uuid::Uuid::new_v4().to_string()),
            method: A2AMethod::TaskSend,
            params: Some(serde_json::to_value(task).unwrap()),
        }
    }

    pub fn task_get(task_id: &str) -> Self {
        Self {
            jsonrpc: "2.0".to_string(),
            id: A2ARequestId::String(uuid::Uuid::new_v4().to_string()),
            method: A2AMethod::TaskGet,
            params: Some(serde_json::json!({ "task_id": task_id })),
        }
    }

    pub fn task_cancel(task_id: &str) -> Self {
        Self {
            jsonrpc: "2.0".to_string(),
            id: A2ARequestId::String(uuid::Uuid::new_v4().to_string()),
            method: A2AMethod::TaskCancel,
            params: Some(serde_json::json!({ "task_id": task_id })),
        }
    }
}
```

### Response Structure

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct A2AResponse {
    pub jsonrpc: String,
    pub id: A2ARequestId,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub result: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<A2AError>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct A2AError {
    pub code: i32,
    pub message: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub data: Option<serde_json::Value>,
}

// Standard A2A Error Codes
impl A2AError {
    pub const PARSE_ERROR: i32 = -32700;
    pub const INVALID_REQUEST: i32 = -32600;
    pub const METHOD_NOT_FOUND: i32 = -32601;
    pub const INVALID_PARAMS: i32 = -32602;
    pub const INTERNAL_ERROR: i32 = -32603;

    // A2A-specific error codes
    pub const TASK_NOT_FOUND: i32 = -32001;
    pub const AGENT_NOT_FOUND: i32 = -32002;
    pub const AGENT_BUSY: i32 = -32003;
    pub const TASK_CANCELLED: i32 = -32004;
    pub const CAPABILITY_MISMATCH: i32 = -32005;
    pub const RATE_LIMITED: i32 = -32006;

    pub fn task_not_found(task_id: &str) -> Self {
        Self {
            code: Self::TASK_NOT_FOUND,
            message: format!("Task not found: {}", task_id),
            data: None,
        }
    }

    pub fn agent_not_found(agent_id: &str) -> Self {
        Self {
            code: Self::AGENT_NOT_FOUND,
            message: format!("Agent not found: {}", agent_id),
            data: None,
        }
    }

    pub fn agent_busy(agent_id: &str) -> Self {
        Self {
            code: Self::AGENT_BUSY,
            message: format!("Agent is busy: {}", agent_id),
            data: Some(serde_json::json!({ "retry_after": 5 })),
        }
    }
}
```

---

## Task State Machine

### Task States

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum TaskState {
    /// Task received, waiting to be processed
    Pending,
    /// Task is currently being executed
    Running,
    /// Task completed successfully
    Completed,
    /// Task failed with error
    Failed,
    /// Task was cancelled
    Cancelled,
    /// Task requires user input
    InputRequired,
}

impl TaskState {
    pub fn is_terminal(&self) -> bool {
        matches!(self, Self::Completed | Self::Failed | Self::Cancelled)
    }

    pub fn can_transition_to(&self, next: TaskState) -> bool {
        match (self, next) {
            // From Pending
            (Self::Pending, Self::Running) => true,
            (Self::Pending, Self::Cancelled) => true,

            // From Running
            (Self::Running, Self::Completed) => true,
            (Self::Running, Self::Failed) => true,
            (Self::Running, Self::Cancelled) => true,
            (Self::Running, Self::InputRequired) => true,

            // From InputRequired
            (Self::InputRequired, Self::Running) => true,
            (Self::InputRequired, Self::Cancelled) => true,

            // Terminal states cannot transition
            _ => false,
        }
    }
}
```

### Task Definition

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub state: TaskState,
    pub input: TaskInput,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub output: Option<TaskOutput>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<TaskError>,
    pub metadata: TaskMetadata,
    pub created_at: i64,
    pub updated_at: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskInput {
    /// Natural language instruction for the agent
    pub instruction: String,
    /// Context data for the task
    #[serde(default)]
    pub context: serde_json::Value,
    /// Files or artifacts to process
    #[serde(default)]
    pub artifacts: Vec<Artifact>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskOutput {
    /// Agent's response
    pub response: String,
    /// Structured data output
    #[serde(skip_serializing_if = "Option::is_none")]
    pub data: Option<serde_json::Value>,
    /// Generated artifacts
    #[serde(default)]
    pub artifacts: Vec<Artifact>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Artifact {
    pub id: String,
    pub name: String,
    pub mime_type: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub content: Option<String>,  // Base64 encoded for binary
    #[serde(skip_serializing_if = "Option::is_none")]
    pub url: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskMetadata {
    pub agent_id: String,
    pub provider: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub parent_task_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub session_id: Option<String>,
    #[serde(default)]
    pub tags: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskError {
    pub code: String,
    pub message: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub details: Option<serde_json::Value>,
    pub retryable: bool,
}

impl Task {
    pub fn new(agent_id: &str, provider: &str, instruction: &str) -> Self {
        let now = chrono::Utc::now().timestamp();
        Self {
            id: uuid::Uuid::new_v4().to_string(),
            state: TaskState::Pending,
            input: TaskInput {
                instruction: instruction.to_string(),
                context: serde_json::Value::Null,
                artifacts: vec![],
            },
            output: None,
            error: None,
            metadata: TaskMetadata {
                agent_id: agent_id.to_string(),
                provider: provider.to_string(),
                parent_task_id: None,
                session_id: None,
                tags: vec![],
            },
            created_at: now,
            updated_at: now,
        }
    }

    pub fn transition(&mut self, new_state: TaskState) -> Result<(), A2AError> {
        if !self.state.can_transition_to(new_state) {
            return Err(A2AError {
                code: A2AError::INVALID_PARAMS,
                message: format!(
                    "Invalid state transition from {:?} to {:?}",
                    self.state, new_state
                ),
                data: None,
            });
        }
        self.state = new_state;
        self.updated_at = chrono::Utc::now().timestamp();
        Ok(())
    }
}
```

---

## Agent Registry

### Agent Definition

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentCard {
    pub id: String,
    pub name: String,
    pub description: String,
    pub provider: AgentProvider,
    pub capabilities: Vec<Capability>,
    pub endpoint: AgentEndpoint,
    pub status: AgentStatus,
    pub metadata: AgentMetadata,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum AgentProvider {
    LangGraph,
    VertexAI,
    AzureAI,
    Bedrock,
    PydanticAI,
    Custom,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Capability {
    pub name: String,
    pub description: String,
    #[serde(default)]
    pub input_schema: Option<serde_json::Value>,
    #[serde(default)]
    pub output_schema: Option<serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentEndpoint {
    pub url: String,
    pub auth: Option<EndpointAuth>,
    pub timeout_seconds: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum EndpointAuth {
    Bearer { token: String },
    ApiKey { header: String, key: String },
    OAuth2 { client_id: String, client_secret: String, token_url: String },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum AgentStatus {
    Online,
    Offline,
    Degraded,
    Maintenance,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentMetadata {
    pub version: String,
    pub created_at: i64,
    pub last_seen_at: i64,
    #[serde(default)]
    pub tags: Vec<String>,
    #[serde(default)]
    pub extra: HashMap<String, serde_json::Value>,
}
```

### Registry Implementation

```rust
use dashmap::DashMap;
use std::sync::Arc;

pub struct AgentRegistry {
    agents: DashMap<String, Arc<AgentCard>>,
    health_checker: Arc<HealthChecker>,
}

impl AgentRegistry {
    pub fn new(health_check_interval: Duration) -> Self {
        let registry = Self {
            agents: DashMap::new(),
            health_checker: Arc::new(HealthChecker::new()),
        };

        // Start background health checker
        registry.start_health_monitoring(health_check_interval);

        registry
    }

    pub fn register(&self, agent: AgentCard) -> Result<(), A2AError> {
        // Validate agent configuration
        self.validate_agent(&agent)?;

        let id = agent.id.clone();
        self.agents.insert(id.clone(), Arc::new(agent));

        tracing::info!(agent_id = %id, "Agent registered");
        Ok(())
    }

    pub fn unregister(&self, agent_id: &str) -> Option<Arc<AgentCard>> {
        let removed = self.agents.remove(agent_id).map(|(_, v)| v);
        if removed.is_some() {
            tracing::info!(agent_id = %agent_id, "Agent unregistered");
        }
        removed
    }

    pub fn get(&self, agent_id: &str) -> Option<Arc<AgentCard>> {
        self.agents.get(agent_id).map(|entry| entry.clone())
    }

    pub fn list(&self) -> Vec<Arc<AgentCard>> {
        self.agents.iter().map(|entry| entry.value().clone()).collect()
    }

    pub fn list_online(&self) -> Vec<Arc<AgentCard>> {
        self.agents
            .iter()
            .filter(|entry| entry.value().status == AgentStatus::Online)
            .map(|entry| entry.value().clone())
            .collect()
    }

    pub fn find_by_capability(&self, capability_name: &str) -> Vec<Arc<AgentCard>> {
        self.agents
            .iter()
            .filter(|entry| {
                entry.value().status == AgentStatus::Online &&
                entry.value().capabilities.iter().any(|c| c.name == capability_name)
            })
            .map(|entry| entry.value().clone())
            .collect()
    }

    pub fn update_status(&self, agent_id: &str, status: AgentStatus) {
        if let Some(mut entry) = self.agents.get_mut(agent_id) {
            let agent = Arc::make_mut(&mut entry);
            agent.status = status;
            agent.metadata.last_seen_at = chrono::Utc::now().timestamp();
        }
    }

    fn validate_agent(&self, agent: &AgentCard) -> Result<(), A2AError> {
        if agent.id.is_empty() {
            return Err(A2AError {
                code: A2AError::INVALID_PARAMS,
                message: "Agent ID cannot be empty".to_string(),
                data: None,
            });
        }

        if agent.capabilities.is_empty() {
            return Err(A2AError {
                code: A2AError::INVALID_PARAMS,
                message: "Agent must have at least one capability".to_string(),
                data: None,
            });
        }

        Ok(())
    }

    fn start_health_monitoring(&self, interval: Duration) {
        let agents = self.agents.clone();
        let health_checker = self.health_checker.clone();

        tokio::spawn(async move {
            let mut ticker = tokio::time::interval(interval);
            loop {
                ticker.tick().await;

                for entry in agents.iter() {
                    let agent = entry.value().clone();
                    let agents_ref = agents.clone();
                    let checker = health_checker.clone();

                    tokio::spawn(async move {
                        let status = checker.check(&agent).await;
                        if let Some(mut entry) = agents_ref.get_mut(&agent.id) {
                            let agent = Arc::make_mut(&mut entry);
                            agent.status = status;
                            agent.metadata.last_seen_at = chrono::Utc::now().timestamp();
                        }
                    });
                }
            }
        });
    }
}
```

---

## Provider Adapters

### Provider Trait

```rust
#[async_trait]
pub trait A2AProvider: Send + Sync {
    /// Provider identifier
    fn provider_type(&self) -> AgentProvider;

    /// Send a task to the agent
    async fn send_task(&self, agent: &AgentCard, task: &Task) -> Result<Task, A2AError>;

    /// Get task status
    async fn get_task(&self, agent: &AgentCard, task_id: &str) -> Result<Task, A2AError>;

    /// Cancel a running task
    async fn cancel_task(&self, agent: &AgentCard, task_id: &str) -> Result<(), A2AError>;

    /// Stream task updates
    async fn stream_task(
        &self,
        agent: &AgentCard,
        task: &Task,
    ) -> Result<Pin<Box<dyn Stream<Item = Result<TaskUpdate, A2AError>> + Send>>, A2AError>;

    /// Check agent health
    async fn health_check(&self, agent: &AgentCard) -> AgentStatus;
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskUpdate {
    pub task_id: String,
    pub state: TaskState,
    pub progress: Option<f32>,  // 0.0 to 1.0
    pub message: Option<String>,
    pub partial_output: Option<TaskOutput>,
}
```

### LangGraph Adapter

```rust
pub struct LangGraphProvider {
    client: reqwest::Client,
}

impl LangGraphProvider {
    pub fn new() -> Self {
        Self {
            client: reqwest::Client::builder()
                .timeout(Duration::from_secs(300))
                .build()
                .unwrap(),
        }
    }
}

#[async_trait]
impl A2AProvider for LangGraphProvider {
    fn provider_type(&self) -> AgentProvider {
        AgentProvider::LangGraph
    }

    async fn send_task(&self, agent: &AgentCard, task: &Task) -> Result<Task, A2AError> {
        let url = format!("{}/runs", agent.endpoint.url);

        let body = serde_json::json!({
            "input": {
                "messages": [
                    { "role": "user", "content": task.input.instruction }
                ],
                "context": task.input.context
            },
            "config": {
                "tags": task.metadata.tags
            }
        });

        let mut request = self.client.post(&url).json(&body);

        // Add authentication
        if let Some(auth) = &agent.endpoint.auth {
            request = match auth {
                EndpointAuth::Bearer { token } => {
                    request.header("Authorization", format!("Bearer {}", token))
                }
                EndpointAuth::ApiKey { header, key } => {
                    request.header(header, key)
                }
                _ => request,
            };
        }

        let response = request
            .send()
            .await
            .map_err(|e| A2AError {
                code: A2AError::INTERNAL_ERROR,
                message: format!("LangGraph request failed: {}", e),
                data: None,
            })?;

        if !response.status().is_success() {
            let error_body = response.text().await.unwrap_or_default();
            return Err(A2AError {
                code: A2AError::INTERNAL_ERROR,
                message: format!("LangGraph error: {}", error_body),
                data: None,
            });
        }

        let result: serde_json::Value = response.json().await.map_err(|e| A2AError {
            code: A2AError::INTERNAL_ERROR,
            message: format!("Failed to parse LangGraph response: {}", e),
            data: None,
        })?;

        // Transform LangGraph response to Task
        let mut updated_task = task.clone();
        updated_task.state = TaskState::Completed;
        updated_task.output = Some(TaskOutput {
            response: result["output"]["messages"]
                .as_array()
                .and_then(|msgs| msgs.last())
                .and_then(|msg| msg["content"].as_str())
                .unwrap_or("")
                .to_string(),
            data: Some(result["output"].clone()),
            artifacts: vec![],
        });

        Ok(updated_task)
    }

    async fn get_task(&self, agent: &AgentCard, task_id: &str) -> Result<Task, A2AError> {
        let url = format!("{}/runs/{}", agent.endpoint.url, task_id);

        let mut request = self.client.get(&url);

        if let Some(EndpointAuth::Bearer { token }) = &agent.endpoint.auth {
            request = request.header("Authorization", format!("Bearer {}", token));
        }

        let response = request.send().await.map_err(|e| A2AError {
            code: A2AError::INTERNAL_ERROR,
            message: format!("Failed to get task: {}", e),
            data: None,
        })?;

        if response.status() == reqwest::StatusCode::NOT_FOUND {
            return Err(A2AError::task_not_found(task_id));
        }

        let result: serde_json::Value = response.json().await.map_err(|e| A2AError {
            code: A2AError::INTERNAL_ERROR,
            message: format!("Failed to parse response: {}", e),
            data: None,
        })?;

        // Transform to Task...
        Ok(Task::new(&agent.id, "langgraph", ""))
    }

    async fn cancel_task(&self, agent: &AgentCard, task_id: &str) -> Result<(), A2AError> {
        let url = format!("{}/runs/{}/cancel", agent.endpoint.url, task_id);

        let mut request = self.client.post(&url);

        if let Some(EndpointAuth::Bearer { token }) = &agent.endpoint.auth {
            request = request.header("Authorization", format!("Bearer {}", token));
        }

        let response = request.send().await.map_err(|e| A2AError {
            code: A2AError::INTERNAL_ERROR,
            message: format!("Failed to cancel task: {}", e),
            data: None,
        })?;

        if !response.status().is_success() {
            return Err(A2AError {
                code: A2AError::INTERNAL_ERROR,
                message: "Failed to cancel task".to_string(),
                data: None,
            });
        }

        Ok(())
    }

    async fn stream_task(
        &self,
        agent: &AgentCard,
        task: &Task,
    ) -> Result<Pin<Box<dyn Stream<Item = Result<TaskUpdate, A2AError>> + Send>>, A2AError> {
        let url = format!("{}/runs/stream", agent.endpoint.url);

        let body = serde_json::json!({
            "input": {
                "messages": [
                    { "role": "user", "content": task.input.instruction }
                ]
            },
            "stream_mode": "updates"
        });

        let mut request = self.client.post(&url).json(&body);

        if let Some(EndpointAuth::Bearer { token }) = &agent.endpoint.auth {
            request = request.header("Authorization", format!("Bearer {}", token));
        }

        let response = request.send().await.map_err(|e| A2AError {
            code: A2AError::INTERNAL_ERROR,
            message: format!("Failed to start stream: {}", e),
            data: None,
        })?;

        let task_id = task.id.clone();
        let stream = response.bytes_stream().map(move |result| {
            match result {
                Ok(bytes) => {
                    // Parse SSE event
                    let text = String::from_utf8_lossy(&bytes);
                    if let Some(data) = text.strip_prefix("data: ") {
                        if let Ok(update) = serde_json::from_str::<serde_json::Value>(data) {
                            return Ok(TaskUpdate {
                                task_id: task_id.clone(),
                                state: TaskState::Running,
                                progress: None,
                                message: update["message"].as_str().map(|s| s.to_string()),
                                partial_output: None,
                            });
                        }
                    }
                    Ok(TaskUpdate {
                        task_id: task_id.clone(),
                        state: TaskState::Running,
                        progress: None,
                        message: None,
                        partial_output: None,
                    })
                }
                Err(e) => Err(A2AError {
                    code: A2AError::INTERNAL_ERROR,
                    message: format!("Stream error: {}", e),
                    data: None,
                }),
            }
        });

        Ok(Box::pin(stream))
    }

    async fn health_check(&self, agent: &AgentCard) -> AgentStatus {
        let url = format!("{}/health", agent.endpoint.url);

        match self.client.get(&url).timeout(Duration::from_secs(5)).send().await {
            Ok(response) if response.status().is_success() => AgentStatus::Online,
            Ok(_) => AgentStatus::Degraded,
            Err(_) => AgentStatus::Offline,
        }
    }
}
```

### Vertex AI Agent Builder Adapter

```rust
pub struct VertexAIProvider {
    client: reqwest::Client,
    project_id: String,
    location: String,
}

#[async_trait]
impl A2AProvider for VertexAIProvider {
    fn provider_type(&self) -> AgentProvider {
        AgentProvider::VertexAI
    }

    async fn send_task(&self, agent: &AgentCard, task: &Task) -> Result<Task, A2AError> {
        let url = format!(
            "https://{}-aiplatform.googleapis.com/v1/projects/{}/locations/{}/agents/{}:run",
            self.location, self.project_id, self.location, agent.id
        );

        let body = serde_json::json!({
            "userInput": {
                "text": task.input.instruction
            },
            "context": task.input.context
        });

        let response = self.client
            .post(&url)
            .json(&body)
            .send()
            .await
            .map_err(|e| A2AError {
                code: A2AError::INTERNAL_ERROR,
                message: format!("Vertex AI request failed: {}", e),
                data: None,
            })?;

        // Process Vertex AI response...
        let mut updated_task = task.clone();
        updated_task.state = TaskState::Completed;

        Ok(updated_task)
    }

    // Other method implementations...
}
```

---

## A2A Gateway

### Gateway Implementation

```rust
pub struct A2AGateway {
    registry: Arc<AgentRegistry>,
    providers: HashMap<AgentProvider, Arc<dyn A2AProvider>>,
    task_store: Arc<TaskStore>,
    config: A2AConfig,
}

impl A2AGateway {
    pub fn new(config: A2AConfig) -> Self {
        let registry = Arc::new(AgentRegistry::new(
            Duration::from_secs(config.health_check_interval_seconds),
        ));

        let mut providers: HashMap<AgentProvider, Arc<dyn A2AProvider>> = HashMap::new();
        providers.insert(AgentProvider::LangGraph, Arc::new(LangGraphProvider::new()));
        // Add other providers...

        Self {
            registry,
            providers,
            task_store: Arc::new(TaskStore::new()),
            config,
        }
    }

    pub fn register_agent(&self, agent: AgentCard) -> Result<(), A2AError> {
        self.registry.register(agent)
    }

    pub fn unregister_agent(&self, agent_id: &str) -> Option<Arc<AgentCard>> {
        self.registry.unregister(agent_id)
    }

    pub fn list_agents(&self) -> Vec<Arc<AgentCard>> {
        self.registry.list_online()
    }

    pub fn find_agents_by_capability(&self, capability: &str) -> Vec<Arc<AgentCard>> {
        self.registry.find_by_capability(capability)
    }

    pub async fn send_task(&self, agent_id: &str, task: Task) -> Result<Task, A2AError> {
        let agent = self.registry.get(agent_id)
            .ok_or_else(|| A2AError::agent_not_found(agent_id))?;

        if agent.status != AgentStatus::Online {
            return Err(A2AError {
                code: A2AError::AGENT_BUSY,
                message: format!("Agent {} is not online", agent_id),
                data: None,
            });
        }

        let provider = self.providers.get(&agent.provider)
            .ok_or_else(|| A2AError {
                code: A2AError::INTERNAL_ERROR,
                message: format!("No provider for {:?}", agent.provider),
                data: None,
            })?;

        // Store task
        self.task_store.store(task.clone()).await?;

        // Send to provider
        let result = provider.send_task(&agent, &task).await;

        // Update task state
        if let Ok(ref updated_task) = result {
            self.task_store.update(updated_task.clone()).await?;
        }

        result
    }

    pub async fn get_task(&self, task_id: &str) -> Result<Task, A2AError> {
        self.task_store.get(task_id).await
    }

    pub async fn cancel_task(&self, task_id: &str) -> Result<(), A2AError> {
        let task = self.task_store.get(task_id).await?;

        if task.state.is_terminal() {
            return Err(A2AError {
                code: A2AError::INVALID_PARAMS,
                message: "Cannot cancel a completed task".to_string(),
                data: None,
            });
        }

        let agent = self.registry.get(&task.metadata.agent_id)
            .ok_or_else(|| A2AError::agent_not_found(&task.metadata.agent_id))?;

        let provider = self.providers.get(&agent.provider)
            .ok_or_else(|| A2AError {
                code: A2AError::INTERNAL_ERROR,
                message: format!("No provider for {:?}", agent.provider),
                data: None,
            })?;

        provider.cancel_task(&agent, task_id).await?;

        // Update task state
        let mut updated_task = task;
        updated_task.transition(TaskState::Cancelled)?;
        self.task_store.update(updated_task).await?;

        Ok(())
    }

    pub async fn stream_task(
        &self,
        agent_id: &str,
        task: Task,
    ) -> Result<Pin<Box<dyn Stream<Item = Result<TaskUpdate, A2AError>> + Send>>, A2AError> {
        let agent = self.registry.get(agent_id)
            .ok_or_else(|| A2AError::agent_not_found(agent_id))?;

        let provider = self.providers.get(&agent.provider)
            .ok_or_else(|| A2AError {
                code: A2AError::INTERNAL_ERROR,
                message: format!("No provider for {:?}", agent.provider),
                data: None,
            })?;

        provider.stream_task(&agent, &task).await
    }
}
```

---

## Task Storage

```rust
use dashmap::DashMap;

pub struct TaskStore {
    tasks: DashMap<String, Task>,
}

impl TaskStore {
    pub fn new() -> Self {
        Self {
            tasks: DashMap::new(),
        }
    }

    pub async fn store(&self, task: Task) -> Result<(), A2AError> {
        self.tasks.insert(task.id.clone(), task);
        Ok(())
    }

    pub async fn get(&self, task_id: &str) -> Result<Task, A2AError> {
        self.tasks
            .get(task_id)
            .map(|entry| entry.clone())
            .ok_or_else(|| A2AError::task_not_found(task_id))
    }

    pub async fn update(&self, task: Task) -> Result<(), A2AError> {
        if self.tasks.contains_key(&task.id) {
            self.tasks.insert(task.id.clone(), task);
            Ok(())
        } else {
            Err(A2AError::task_not_found(&task.id))
        }
    }

    pub async fn delete(&self, task_id: &str) -> Result<(), A2AError> {
        self.tasks.remove(task_id);
        Ok(())
    }

    pub async fn list_by_agent(&self, agent_id: &str) -> Vec<Task> {
        self.tasks
            .iter()
            .filter(|entry| entry.value().metadata.agent_id == agent_id)
            .map(|entry| entry.value().clone())
            .collect()
    }

    pub async fn list_by_state(&self, state: TaskState) -> Vec<Task> {
        self.tasks
            .iter()
            .filter(|entry| entry.value().state == state)
            .map(|entry| entry.value().clone())
            .collect()
    }
}
```

---

## Configuration

```yaml
a2a:
  enabled: true

  gateway:
    health_check_interval_seconds: 30
    task_timeout_seconds: 300
    max_concurrent_tasks: 100

  agents:
    - id: "research-agent"
      name: "Research Agent"
      description: "Performs web research and summarization"
      provider: "langgraph"
      endpoint:
        url: "http://localhost:8100"
        auth:
          type: "bearer"
          token: ${LANGGRAPH_API_KEY}
        timeout_seconds: 120
      capabilities:
        - name: "web_search"
          description: "Search the web for information"
        - name: "summarize"
          description: "Summarize documents and content"

    - id: "code-agent"
      name: "Code Agent"
      description: "Writes and reviews code"
      provider: "vertex_ai"
      endpoint:
        url: "https://us-central1-aiplatform.googleapis.com"
        auth:
          type: "oauth2"
          client_id: ${GOOGLE_CLIENT_ID}
          client_secret: ${GOOGLE_CLIENT_SECRET}
          token_url: "https://oauth2.googleapis.com/token"
        timeout_seconds: 180
      capabilities:
        - name: "code_generation"
          description: "Generate code from requirements"
        - name: "code_review"
          description: "Review and improve code"

    - id: "data-agent"
      name: "Data Analysis Agent"
      description: "Analyzes data and creates visualizations"
      provider: "bedrock"
      endpoint:
        url: "https://bedrock-runtime.us-east-1.amazonaws.com"
        timeout_seconds: 240
      capabilities:
        - name: "data_analysis"
          description: "Analyze datasets"
        - name: "visualization"
          description: "Create charts and graphs"
```

---

## Error Types

```rust
#[derive(Debug, thiserror::Error)]
pub enum A2AProtocolError {
    #[error("Agent not found: {0}")]
    AgentNotFound(String),

    #[error("Task not found: {0}")]
    TaskNotFound(String),

    #[error("Provider error: {provider} - {message}")]
    ProviderError {
        provider: AgentProvider,
        message: String,
    },

    #[error("Invalid state transition: {from:?} -> {to:?}")]
    InvalidTransition {
        from: TaskState,
        to: TaskState,
    },

    #[error("Task timeout: {0}")]
    Timeout(String),

    #[error("Rate limited: retry after {retry_after} seconds")]
    RateLimited { retry_after: u64 },

    #[error("Capability not found: {0}")]
    CapabilityNotFound(String),

    #[error("Configuration error: {0}")]
    Configuration(String),

    #[error("Network error: {0}")]
    Network(String),
}
```

---

## Best Practices

### 1. Agent Registration

```rust
// Good - validate capabilities and endpoint
fn register_agent(&self, agent: AgentCard) -> Result<(), A2AError> {
    // Validate agent has capabilities
    if agent.capabilities.is_empty() {
        return Err(A2AError::invalid_params("Agent must have capabilities"));
    }

    // Validate endpoint is reachable
    self.health_check(&agent).await?;

    self.registry.insert(agent);
    Ok(())
}

// Bad - no validation
fn register_agent(&self, agent: AgentCard) {
    self.registry.insert(agent);
}
```

### 2. Task State Management

```rust
// Good - enforce state transitions
impl Task {
    pub fn transition(&mut self, new_state: TaskState) -> Result<(), A2AError> {
        if !self.state.can_transition_to(new_state) {
            return Err(A2AError::invalid_transition(self.state, new_state));
        }
        self.state = new_state;
        self.updated_at = chrono::Utc::now().timestamp();
        Ok(())
    }
}

// Bad - allow arbitrary state changes
impl Task {
    pub fn set_state(&mut self, state: TaskState) {
        self.state = state;
    }
}
```

### 3. Error Handling

```rust
// Good - provide context and retryability
fn handle_provider_error(err: reqwest::Error, provider: AgentProvider) -> A2AError {
    if err.is_timeout() {
        return A2AError {
            code: A2AError::INTERNAL_ERROR,
            message: format!("Provider {} timed out", provider),
            data: Some(serde_json::json!({ "retryable": true })),
        };
    }

    if err.is_connect() {
        return A2AError {
            code: A2AError::INTERNAL_ERROR,
            message: format!("Cannot connect to provider {}", provider),
            data: Some(serde_json::json!({ "retryable": true })),
        };
    }

    A2AError {
        code: A2AError::INTERNAL_ERROR,
        message: err.to_string(),
        data: None,
    }
}
```

### 4. Capability Matching

```rust
// Good - match by capability semantics
pub fn find_agent_for_task(&self, instruction: &str) -> Option<Arc<AgentCard>> {
    // Extract required capabilities from instruction
    let required_caps = self.extract_capabilities(instruction);

    // Find agent with best match
    self.registry
        .list_online()
        .into_iter()
        .filter(|agent| {
            required_caps.iter().all(|cap| {
                agent.capabilities.iter().any(|c| c.name == *cap)
            })
        })
        .min_by_key(|agent| self.get_agent_load(agent))
}
```
