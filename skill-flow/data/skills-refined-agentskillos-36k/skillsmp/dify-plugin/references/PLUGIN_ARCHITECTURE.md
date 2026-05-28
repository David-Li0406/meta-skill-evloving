# Dify Plugin Architecture Deep Dive

This document provides detailed information about the Dify Plugin Daemon's plugin system internals, including lifecycle, hooks, and configuration conventions.

## Table of Contents

1. [Plugin Types Overview](#1-plugin-types-overview)
2. [Runtime Types](#2-runtime-types)
3. [Plugin Lifecycle](#3-plugin-lifecycle)
4. [Hooks and Callback Mechanisms](#4-hooks-and-callback-mechanisms)
5. [Variables and Configuration](#5-variables-and-configuration)
6. [Plugin Type Reference](#6-plugin-type-reference)
7. [Plugin Directory Structure](#7-plugin-directory-structure)

---

## 1. Plugin Types Overview

Dify supports six main plugin types, defined in `pkg/entities/plugin_entities/plugin_declaration.go`:

```go
type PluginCategory string

const (
    PLUGIN_CATEGORY_TOOL           PluginCategory = "tool"           // Tool plugin
    PLUGIN_CATEGORY_MODEL          PluginCategory = "model"          // Model plugin
    PLUGIN_CATEGORY_EXTENSION      PluginCategory = "extension"      // Extension plugin
    PLUGIN_CATEGORY_AGENT_STRATEGY PluginCategory = "agent-strategy" // Agent Strategy plugin
    PLUGIN_CATEGORY_DATASOURCE     PluginCategory = "datasource"     // Datasource plugin
    PLUGIN_CATEGORY_TRIGGER        PluginCategory = "trigger"        // Trigger plugin
)
```

### 1.1 Plugin Type Mutual Exclusion Rules

| Plugin Type | Can Combine with Others | Description |
|-------------|------------------------|-------------|
| Tool | Yes (can combine with Endpoint) | Reusable tool functions |
| Model | No | Exclusive, provides AI model capabilities |
| Agent Strategy | No | Exclusive, provides Agent reasoning strategies |
| Datasource | No | Exclusive, provides data source connections |
| Trigger | No | Exclusive, provides event triggering capabilities |
| Endpoint | Yes (can combine with Tool) | HTTP endpoint extension |

---

## 2. Runtime Types

Defined in `pkg/entities/plugin_entities/runtime.go`:

```go
type PluginRuntimeType string

const (
    PLUGIN_RUNTIME_TYPE_LOCAL      PluginRuntimeType = "local"      // Local process
    PLUGIN_RUNTIME_TYPE_REMOTE     PluginRuntimeType = "remote"     // Remote debugging
    PLUGIN_RUNTIME_TYPE_SERVERLESS PluginRuntimeType = "serverless" // Serverless
)
```

### 2.1 Runtime Comparison

| Feature | Local | Remote/Debug | Serverless |
|---------|-------|--------------|------------|
| Process Model | Subprocess | TCP Connection | HTTP Request |
| Communication Protocol | STDIN/STDOUT (JSON) | TCP Binary + Newline | HTTP SSE |
| Concurrency Mode | Multiple Instances (Replicas) | Single Connection | Per Request |
| Lifecycle | Long-running Process | Persistent Connection | Stateless |
| Heartbeat Timeout | 120 seconds | 60 seconds | Per Request Timeout |
| Load Balancing | Round-robin | N/A | N/A |
| Use Case | Production Deployment | Development/Debugging | Cloud Deployment |

### 2.2 Runtime Status

```go
const (
    PLUGIN_RUNTIME_STATUS_ACTIVE     = "active"     // Running
    PLUGIN_RUNTIME_STATUS_LAUNCHING  = "launching"  // Starting
    PLUGIN_RUNTIME_STATUS_STOPPED    = "stopped"    // Stopped
    PLUGIN_RUNTIME_STATUS_RESTARTING = "restarting" // Restarting
    PLUGIN_RUNTIME_STATUS_PENDING    = "pending"    // Pending
)
```

---

## 3. Plugin Lifecycle

### 3.1 Complete Lifecycle Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                       Installation Phase                          │
├─────────────────────────────────────────────────────────────────┤
│  1. InstallMultiplePluginsToTenant()                            │
│     ↓                                                           │
│  2. DisableAutoLaunch() - Prevent WatchDog from starting early  │
│     ↓                                                           │
│  3. InstallToLocal() - Copy package to install directory        │
│     ↓                                                           │
│  4. LaunchLocalPlugin() - Start runtime                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Initialization Phase                         │
├─────────────────────────────────────────────────────────────────┤
│  5. AcquireLock + Semaphore - Acquire lock and semaphore        │
│     ↓                                                           │
│  6. BuildRuntime() - Build runtime instance                     │
│     ↓                                                           │
│  7. AcquireDistributedLock (Redis) - Distributed lock in cluster│
│     ↓                                                           │
│  8. InitEnvironment()                                           │
│     ├── ExtractPlugin - Extract plugin                          │
│     └── InitPythonEnv                                           │
│         ├── CreateVenv - Create virtual environment             │
│         ├── InstallDeps (UV) - Install dependencies             │
│         └── PreCompile - Pre-compile                            │
│     ↓                                                           │
│  9. MountNotifiers() - Mount lifecycle notifiers                │
│     ↓                                                           │
│  10. Schedule() - Start scheduling loop                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        Running Phase                              │
├─────────────────────────────────────────────────────────────────┤
│  11. startNewInstance() - Start subprocess                      │
│      ↓                                                          │
│  12. Wait for Heartbeat (max 120 seconds)                       │
│      ↓                                                          │
│  13. OnInstanceReady() - Instance ready notification            │
│      ↓                                                          │
│  14. Enter normal service state                                 │
│      ├── Listen() - Register session listener                   │
│      ├── Write() - Send request to plugin                       │
│      └── Heartbeat Monitor (every 30 seconds)                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       Shutdown Phase                              │
├─────────────────────────────────────────────────────────────────┤
│  15. GracefulStop() / Stop()                                    │
│      ↓                                                          │
│  16. Stop schedule loop                                         │
│      ↓                                                          │
│  17. For each instance:                                         │
│      ├── Wait for listeners (graceful)                          │
│      ├── Close stdin/stdout/stderr                              │
│      └── Kill subprocess + Reap                                 │
│      ↓                                                          │
│  18. OnRuntimeClose() - Runtime close notification              │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Key File Locations

| Component | File Path |
|-----------|-----------|
| Install Entry | `internal/service/install_plugin.go` |
| Installer | `internal/core/plugin_manager/installer.go` |
| Launcher | `internal/core/control_panel/launcher_local.go` |
| Runtime Constructor | `internal/core/local_runtime/constructor.go` |
| Environment Init | `internal/core/local_runtime/environment.go` |
| Python Environment | `internal/core/local_runtime/environment_python.go` |
| Subprocess Management | `internal/core/local_runtime/subprocess.go` |
| Instance Management | `internal/core/local_runtime/instance.go` |
| Schedule Control | `internal/core/local_runtime/control.go` |
| Session Management | `internal/core/session_manager/session.go` |

### 3.3 Session Structure

```go
type Session struct {
    ID                     string
    TenantID               string
    UserID                 string
    PluginUniqueIdentifier plugin_entities.PluginUniqueIdentifier
    ClusterID              string

    InvokeFrom             access_types.PluginAccessType   // Invocation source type
    Action                 access_types.PluginAccessAction // Specific action
    Declaration            *plugin_entities.PluginDeclaration

    // Context information
    ConversationID *string
    MessageID      *string
    AppID          *string
    EndpointID     *string
    Context        map[string]any

    // Runtime reference
    runtime             plugin_entities.PluginRuntimeSessionIOInterface
    backwardsInvocation dify_invocation.BackwardsInvocation
}
```

---

## 4. Hooks and Callback Mechanisms

This section categorizes hooks and callback mechanisms by runtime type.

### 4.1 Local Runtime Hooks

Local runtime manages plugins through subprocesses and has the most complete lifecycle hook system.

#### 4.1.1 Instance-Level Hooks (PluginInstanceNotifier)

Defined in `internal/core/local_runtime/signals_instance.go`:

```go
type PluginInstanceNotifier interface {
    OnInstanceStarting()                              // Instance starting
    OnInstanceReady(*PluginInstance)                  // Instance ready
    OnInstanceLaunchFailed(*PluginInstance, error)    // Launch failed
    OnInstanceShutdown(*PluginInstance)               // Instance shutdown
    OnInstanceHeartbeat(*PluginInstance)              // Heartbeat received
    OnInstanceLog(*PluginInstance, PluginLogEvent)    // Plugin log
    OnInstanceErrorLog(*PluginInstance, error)        // Error log
    OnInstanceWarningLog(*PluginInstance, string)     // Warning log
    OnInstanceStdout(*PluginInstance, []byte)         // Standard output
    OnInstanceStderr(*PluginInstance, []byte)         // Standard error
}
```

**Trigger Timing**:

| Hook | Trigger Timing | Purpose |
|------|----------------|---------|
| `OnInstanceStarting` | Before subprocess starts | Logging, status update |
| `OnInstanceReady` | After first heartbeat received | Mark instance available, release semaphore |
| `OnInstanceLaunchFailed` | Launch timeout or process exit | Error handling, retry logic |
| `OnInstanceShutdown` | When instance stops | Resource cleanup, status update |
| `OnInstanceHeartbeat` | Each heartbeat received | Update activity timestamp |
| `OnInstanceLog` | Plugin outputs log event | Log collection |
| `OnInstanceErrorLog` | Plugin outputs error | Error monitoring |
| `OnInstanceWarningLog` | Heartbeat timeout warning | Health check |
| `OnInstanceStdout` | stdout has data | Data processing, activity detection |
| `OnInstanceStderr` | stderr has data | Error collection |

#### 4.1.2 Runtime-Level Hooks (PluginRuntimeNotifier)

Defined in `internal/core/local_runtime/signals_runtime.go`:

```go
type PluginRuntimeNotifier interface {
    OnInstanceStarting()                        // Instance starting
    OnInstanceReady(*PluginInstance)            // Instance ready
    OnInstanceLaunchFailed(*PluginInstance, error)
    OnInstanceShutdown(*PluginInstance)
    OnInstanceLog(*PluginInstance, PluginLogEvent)
    OnInstanceScaleUp(int32)                    // Scale up notification
    OnInstanceScaleDown(int32)                  // Scale down notification
    OnInstanceScaleDownFailed(error)            // Scale down failed
    OnRuntimeStopSchedule()                     // Schedule loop stopped
    OnRuntimeClose()                            // Runtime fully closed
}
```

**Scaling Hooks**:
- `OnInstanceScaleUp(count)`: Triggered when instance count increases, parameter is new total instance count
- `OnInstanceScaleDown(count)`: Triggered when instance count decreases, parameter is new total instance count
- `OnInstanceScaleDownFailed(err)`: Triggered when scale down fails

#### 4.1.3 Control Panel Hooks (ControlPanelNotifier)

Defined in `internal/core/control_panel/signals.go`:

```go
type ControlPanelNotifier interface {
    // Local runtime hooks
    OnLocalRuntimeStarting(identifier PluginUniqueIdentifier)
    OnLocalRuntimeReady(runtime *LocalPluginRuntime)
    OnLocalRuntimeStartFailed(identifier PluginUniqueIdentifier, err error)
    OnLocalRuntimeStop(runtime *LocalPluginRuntime)
    OnLocalRuntimeStopped(identifier PluginUniqueIdentifier)
    OnLocalRuntimeScaleUp(runtime *LocalPluginRuntime, newCount int32)
    OnLocalRuntimeScaleDown(runtime *LocalPluginRuntime, newCount int32)

    // Debug runtime hooks
    OnDebuggingRuntimeConnected(runtime *RemotePluginRuntime)
    OnDebuggingRuntimeDisconnected(runtime *RemotePluginRuntime)
}
```

#### 4.1.4 Local Lifecycle Flow Diagram

```
LaunchLocalPlugin()
    │
    ├─► OnLocalRuntimeStarting()
    │
    ▼
BuildRuntime() → InitEnvironment()
    │
    ▼
Schedule() → startNewInstance()
    │
    ├─► OnInstanceStarting()
    │
    ▼
Wait for Heartbeat (max 120s)
    │
    ├─[Success]─► OnInstanceReady() → OnLocalRuntimeReady()
    │
    └─[Failure]─► OnInstanceLaunchFailed() → OnLocalRuntimeStartFailed()

Running:
    │
    ├─► OnInstanceHeartbeat() (each heartbeat)
    ├─► OnInstanceLog() (log events)
    ├─► OnInstanceStdout/Stderr() (IO events)
    │
    ▼
GracefulStop() / Stop()
    │
    ├─► OnLocalRuntimeStop()
    ├─► OnRuntimeStopSchedule()
    │
    ▼
For each instance: OnInstanceShutdown()
    │
    ▼
OnRuntimeClose() → OnLocalRuntimeStopped()
```

---

### 4.2 Remote/Debug Runtime Hooks

Remote runtime manages plugins through TCP connections, primarily used for development and debugging.

#### 4.2.1 Server-Level Hooks (PluginRuntimeNotifier)

Defined in `internal/core/debugging_runtime/server_signals.go`:

```go
type PluginRuntimeNotifier interface {
    OnRuntimeConnected(*RemotePluginRuntime) error  // Plugin connected successfully
    OnRuntimeDisconnected(*RemotePluginRuntime)     // Plugin disconnected
    OnServerShutdown(reason ServerShutdownReason)   // Server shutdown
}
```

**Server Shutdown Reasons**:
```go
type ServerShutdownReason string

const (
    SERVER_SHUTDOWN_REASON_EXIT  = "exit"   // Normal exit
    SERVER_SHUTDOWN_REASON_ERROR = "error"  // Error exit
)
```

#### 4.2.2 gnet Event Hooks

Defined in `internal/core/debugging_runtime/hooks.go`:

| gnet Hook | Trigger Timing | Internal Handling |
|-----------|----------------|-------------------|
| `OnBoot` | TCP server starts | Initialization |
| `OnOpen` | New TCP connection established | Create `RemotePluginRuntime`, set 10s handshake timeout |
| `OnClose` | TCP connection closed | Call `cleanupResources()`, trigger `OnRuntimeDisconnected` |
| `OnTraffic` | Data received | Decode message, route to `onMessage()` |
| `OnShutdown` | Server shutdown | Trigger `OnServerShutdown(SERVER_SHUTDOWN_REASON_EXIT)` |

#### 4.2.3 Handshake Phase Registration Events

Defined in `internal/core/debugging_runtime/type.go`:

```go
type RegisterEventType string

const (
    REGISTER_EVENT_TYPE_HAND_SHAKE                = "hand_shake"
    REGISTER_EVENT_TYPE_ASSET_CHUNK               = "asset_chunk"
    REGISTER_EVENT_TYPE_MANIFEST_DECLARATION      = "manifest_declaration"
    REGISTER_EVENT_TYPE_TOOL_DECLARATION          = "tool_declaration"
    REGISTER_EVENT_TYPE_MODEL_DECLARATION         = "model_declaration"
    REGISTER_EVENT_TYPE_ENDPOINT_DECLARATION      = "endpoint_declaration"
    REGISTER_EVENT_TYPE_AGENT_STRATEGY_DECLARATION = "agent_strategy_declaration"
    REGISTER_EVENT_TYPE_DATASOURCE_DECLARATION    = "datasource_declaration"
    REGISTER_EVENT_TYPE_TRIGGER_DECLARATION       = "trigger_declaration"
    REGISTER_EVENT_TYPE_END                       = "end"
)
```

#### 4.2.4 Remote Lifecycle Flow Diagram

```
TCP Client Connect
    │
    ▼
OnOpen() → Create RemotePluginRuntime
    │
    ├─► 10 second handshake timeout timer
    │
    ▼
OnTraffic() → onMessage()
    │
    ├─► REGISTER_EVENT_TYPE_HAND_SHAKE
    │       └─► handleHandleShake()
    │
    ├─► REGISTER_EVENT_TYPE_ASSET_CHUNK
    │       └─► handleAssetChunk()
    │
    ├─► REGISTER_EVENT_TYPE_*_DECLARATION
    │       └─► handleDeclarationRegister()
    │
    └─► REGISTER_EVENT_TYPE_END
            │
            ├─► Mark initialized = true
            ├─► OnRuntimeConnected()
            └─► SpawnCore() start message processing loop

Running:
    │
    ├─► OnTraffic() → Parse event → Route to session callback
    │
    ▼
TCP Disconnect / Heartbeat timeout (60s)
    │
    ▼
OnClose()
    │
    ├─► cleanupResources()
    ├─► Close all session listeners
    └─► OnRuntimeDisconnected()
```

#### 4.2.5 Heartbeat Monitoring

Defined in `internal/core/debugging_runtime/lifetime.go`:

```go
func (r *RemotePluginRuntime) HeartbeatMonitor() {
    // Check every 60 seconds
    // If no activity for more than 60 seconds, close connection
}
```

---

### 4.3 Serverless Runtime Hooks

Serverless runtime is a stateless HTTP call mode and **does not implement the traditional Notifier pattern**.

#### 4.3.1 Characteristics

- **No persistent connection**: Each call is an independent HTTP request
- **No instance management**: Does not maintain long-running processes
- **No scaling hooks**: Managed automatically by cloud platform
- **No backwards invocation support**: `SESSION_MESSAGE_TYPE_INVOKE` is rejected

#### 4.3.2 Session Event Callbacks

Serverless uses callback functions instead of interface pattern to handle events.

Defined in `internal/core/serverless_runtime/io.go`:

```go
// Listen creates a session listener
func (r *ServerlessPluginRuntime) Listen(sessionId string) (
    *entities.Broadcast[plugin_entities.SessionMessage],
    error,
)

// Write sends request and handles response
func (r *ServerlessPluginRuntime) Write(
    sessionId string,
    action access_types.PluginAccessAction,
    data []byte,
) error
```

**Write method internal callbacks** (lines 97-125):

```go
plugin_entities.ParsePluginUniversalEvent(
    eventBytes,
    statusText,
    // 1. Session message callback
    func(sessionId string, data []byte) {
        // Parse and send to listener
        l.Send(sessionMessage)
    },
    // 2. Heartbeat callback (empty implementation)
    func() {},
    // 3. Error callback
    func(err string) {
        l.Send(plugin_entities.SessionMessage{
            Type: plugin_entities.SESSION_MESSAGE_TYPE_ERROR,
            Data: []byte(err),
        })
    },
    // 4. Log callback (empty implementation)
    func(logEvent plugin_entities.PluginLogEvent) {},
)
```

#### 4.3.3 Serverless Transaction Handler

Defined in `internal/core/io_tunnel/backwards_invocation/transaction/serverless_handler.go`:

```go
type ServerlessTransactionHandler struct {
    maxTimeout time.Duration
}

// Handle processes Serverless request
func (h *ServerlessTransactionHandler) Handle(ctx *gin.Context, sessionId string)
```

**Transaction Writer** (defined in `serverless_writer.go`):

```go
type ServerlessTransactionWriter struct {
    session          *session_manager.Session
    writeFlushCloser WriteFlushCloser
}

// Write writes event and flushes
func (w *ServerlessTransactionWriter) Write(
    event session_manager.PLUGIN_IN_STREAM_EVENT,
    data any,
) error

// Done closes the writer
func (w *ServerlessTransactionWriter) Done()
```

#### 4.3.4 Serverless Lifecycle Flow Diagram

```
HTTP POST /invoke?action=xxx
    │
    ▼
ServerlessPluginRuntime.Listen(sessionId)
    │
    └─► Create Broadcast[SessionMessage]

ServerlessPluginRuntime.Write(sessionId, action, data)
    │
    ├─► Async submit request task
    │       │
    │       ▼
    │   HTTP POST → Lambda Function
    │       │
    │       ▼
    │   bufio.Scanner reads SSE response
    │       │
    │       ├─► ParsePluginUniversalEvent()
    │       │       │
    │       │       ├─► sessionHandler → l.Send(message)
    │       │       ├─► errorHandler → l.Send(error)
    │       │       └─► heartbeat/log (ignored)
    │       │
    │       └─► Response ends
    │               │
    │               ├─► l.Send(SESSION_MESSAGE_TYPE_END)
    │               ├─► l.Close()
    │               └─► listeners.Delete(sessionId)
    │
    └─► Return nil (async processing)

Listener reads:
    │
    ▼
Broadcast.Listen(callback)
    │
    └─► callback(SessionMessage) is called
```

#### 4.3.5 Serverless Limitations

| Feature | Support | Description |
|---------|---------|-------------|
| Tool invocation | ✅ | Via HTTP request |
| Model invocation | ✅ | Via HTTP request |
| Backwards invocation | ❌ | Explicitly rejected, returns `serverless_event_not_supported` |
| Heartbeat monitoring | ❌ | Stateless, no heartbeat needed |
| Instance scaling | ❌ | Managed by cloud platform |
| Log collection | ❌ | Log callback is empty implementation |

**Backwards invocation rejection logic** (defined in `internal/core/io_tunnel/generic.go`):

```go
case plugin_entities.SESSION_MESSAGE_TYPE_INVOKE:
    if session.Runtime().Type() == plugin_entities.PLUGIN_RUNTIME_TYPE_SERVERLESS {
        response.Write(InvokePluginResponse[T]{
            Event:   "serverless_event_not_supported",
            Message: "serverless event is not supported by full duplex",
        })
        return
    }
    // ... handle backwards invocation
```

---

### 4.4 Runtime Hooks Comparison

| Hook Category | Local | Remote/Debug | Serverless |
|---------------|-------|--------------|------------|
| **Instance Starting** | `OnInstanceStarting` | `OnOpen` | N/A |
| **Instance Ready** | `OnInstanceReady` | `OnRuntimeConnected` | N/A |
| **Instance Failed** | `OnInstanceLaunchFailed` | Handshake timeout closes | HTTP error |
| **Instance Shutdown** | `OnInstanceShutdown` | `OnClose` | Request ends |
| **Heartbeat Monitoring** | `OnInstanceHeartbeat` | `HeartbeatMonitor` | N/A |
| **Log Events** | `OnInstanceLog` | Event parsing | Ignored |
| **Error Events** | `OnInstanceErrorLog` | Event parsing | Callback handling |
| **Scaling** | `OnInstanceScaleUp/Down` | N/A | Cloud platform managed |
| **Runtime Close** | `OnRuntimeClose` | `OnServerShutdown` | N/A |
| **Backwards Invocation** | ✅ Supported | ✅ Supported | ❌ Not supported |

---

### 4.5 Backwards Invocation

Plugins can access Dify API services through the backwards invocation mechanism.

**Note**: Serverless runtime does not support backwards invocation; only Local and Remote/Debug runtimes support it.

#### 4.5.1 Supported Invocation Types

Defined in `internal/core/dify_invocation/types.go`:

| Invocation Type | Description | Required Permission |
|-----------------|-------------|---------------------|
| `llm` | LLM model invocation | `AllowInvokeLLM()` |
| `llm_structured_output` | Structured output | `AllowInvokeLLM()` |
| `text_embedding` | Text embedding | `AllowInvokeTextEmbedding()` |
| `multimodal_embedding` | Multimodal embedding | `AllowInvokeTextEmbedding()` |
| `rerank` | Reranking | `AllowInvokeRerank()` |
| `multimodal_rerank` | Multimodal reranking | `AllowInvokeRerank()` |
| `tts` | Text-to-speech | `AllowInvokeTTS()` |
| `speech2text` | Speech-to-text | `AllowInvokeSpeech2Text()` |
| `moderation` | Content moderation | `AllowInvokeModeration()` |
| `tool` | Tool invocation | `AllowInvokeTool()` |
| `app` | App invocation | `AllowInvokeApp()` |
| `node_parameter_extractor` | Parameter extraction | `AllowInvokeNode()` |
| `node_question_classifier` | Question classification | `AllowInvokeNode()` |
| `storage` | Storage operations | `AllowInvokeStorage()` |
| `upload_file` | File upload | Always allowed |
| `fetch_app` | Fetch app info | `AllowInvokeApp()` |

#### 4.5.2 Backwards Invocation Flow

```
Plugin Process
    │
    ▼ (Send SESSION_MESSAGE_TYPE_INVOKE)
Plugin Runtime
    │
    ▼
Session Manager
    │
    ▼ (Route to) BackwardsInvocation.InvokeDify()
    │
    ├─► Permission Check (check manifest permissions)
    │       │
    │       └─► Denied? WriteError() → Return to plugin
    │
    ├─► Async Task Dispatch
    │       │
    │       ▼
    │   Specific executor (e.g., executeDifyInvocationLLMTask)
    │       │
    │       ▼
    │   HTTP Client → Dify API Server
    │       │
    │       ▼ (Streaming/Structured response)
    │   handle.WriteResponse()
    │       │
    │       ▼
    │   Transaction Writer → Return to plugin
```

#### 4.5.3 BackwardsInvocation Interface

```go
type BackwardsInvocation interface {
    InvokeLLM(payload *InvokeLLMRequest) (*stream.Stream[LLMResultChunk], error)
    InvokeLLMWithStructuredOutput(...) (*stream.Stream[...], error)
    InvokeTextEmbedding(payload *InvokeTextEmbeddingRequest) (*TextEmbeddingResult, error)
    InvokeMultimodalEmbedding(...) (*MultimodalEmbeddingResult, error)
    InvokeRerank(payload *InvokeRerankRequest) (*RerankResult, error)
    InvokeMultimodalRerank(...) (*MultimodalRerankResult, error)
    InvokeTTS(payload *InvokeTTSRequest) (*stream.Stream[TTSResult], error)
    InvokeSpeech2Text(payload *InvokeSpeech2TextRequest) (*Speech2TextResult, error)
    InvokeModeration(payload *InvokeModerationRequest) (*ModerationResult, error)
    InvokeTool(payload *InvokeToolRequest) (*stream.Stream[ToolResponseChunk], error)
    InvokeApp(payload *InvokeAppRequest) (*stream.Stream[map[string]any], error)
    InvokeParameterExtractor(...) (*InvokeNodeResponse, error)
    InvokeQuestionClassifier(...) (*InvokeNodeResponse, error)
    InvokeEncrypt(payload *InvokeEncryptRequest) (map[string]any, error)
    InvokeSummary(payload *InvokeSummaryRequest) (*InvokeSummaryResponse, error)
    UploadFile(payload *UploadFileRequest) (*UploadFileResponse, error)
    FetchApp(payload *FetchAppRequest) (map[string]any, error)
}
```

### 4.6 Plugin Event Types

Defined in `pkg/entities/plugin_entities/event.go`:

```go
// Plugin output events
const (
    PLUGIN_EVENT_LOG       = "log"       // Log event
    PLUGIN_EVENT_SESSION   = "session"   // Session message
    PLUGIN_EVENT_ERROR     = "error"     // Error event
    PLUGIN_EVENT_HEARTBEAT = "heartbeat" // Heartbeat event
)

// Session message types
const (
    SESSION_MESSAGE_TYPE_STREAM = "stream" // Streaming response
    SESSION_MESSAGE_TYPE_END    = "end"    // End marker
    SESSION_MESSAGE_TYPE_ERROR  = "error"  // Error message
    SESSION_MESSAGE_TYPE_INVOKE = "invoke" // Backwards invocation
)
```

---

## 5. Variables and Configuration

### 5.1 Environment Variables

For complete configuration reference, see `.env.example`. Main categories:

#### Server Configuration
```bash
SERVER_HOST=0.0.0.0
SERVER_PORT=5002
SERVER_KEY=<security-key>
GIN_MODE=release
```

#### Dify Internal API
```bash
DIFY_INNER_API_KEY="<api-key>"
DIFY_INNER_API_URL=http://127.0.0.1:5001
DIFY_INVOCATION_CONNECTION_IDLE_TIMEOUT=120
DIFY_BACKWARDS_INVOCATION_WRITE_TIMEOUT=5000
DIFY_BACKWARDS_INVOCATION_READ_TIMEOUT=240000
```

#### Plugin Remote Installation
```bash
PLUGIN_REMOTE_INSTALLING_ENABLED=true
PLUGIN_REMOTE_INSTALLING_HOST=127.0.0.1
PLUGIN_REMOTE_INSTALLING_PORT=5003
```

#### Storage Configuration
```bash
PLUGIN_STORAGE_TYPE=local           # local / s3 / tencent-cos / aliyun-oss / azure / gcs / huawei-obs / volcengine-tos
PLUGIN_STORAGE_LOCAL_ROOT=./storage
PLUGIN_INSTALLED_PATH=plugin
PLUGIN_WORKING_PATH=cwd
```

#### Redis Configuration
```bash
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=difyai123456
REDIS_DB=0
REDIS_USE_SSL=false
```

#### Database Configuration
```bash
DB_TYPE=postgresql
DB_USERNAME=postgres
DB_PASSWORD=difyai123456
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=dify_plugin
```

#### Plugin Runtime
```bash
PYTHON_INTERPRETER_PATH=/usr/bin/python3
UV_PATH=
PYTHON_ENV_INIT_TIMEOUT=120
PLUGIN_RUNTIME_BUFFER_SIZE=1024
PLUGIN_RUNTIME_MAX_BUFFER_SIZE=5242880
```

#### Security Configuration
```bash
FORCE_VERIFYING_SIGNATURE=true
ENFORCE_LANGGENIUS_PLUGIN_SIGNATURES=true
MAX_PLUGIN_PACKAGE_SIZE=52428800
```

### 5.2 Plugin Unique Identifier Format

```
Format: author/plugin_id:version@checksum

Examples:
- langgenius/my_tool:1.0.0@abc123def456...
- partner-name/api_plugin:2.1.3-beta@xyz789...

Rules:
- Author: 1-64 characters, alphanumeric/underscore/hyphen
- Plugin ID: 1-255 characters, alphanumeric/underscore/hyphen
- Version: Semantic versioning (e.g., 1.0.0, 2.1.3-beta)
- Checksum: 32-64 hexadecimal characters (SHA256)
```

### 5.3 HTTP Request Header Constants

```go
const (
    X_PLUGIN_ID     = "X-Plugin-ID"      // Plugin ID
    X_API_KEY       = "X-Api-Key"        // API key
    X_ADMIN_API_KEY = "X-Admin-Api-Key"  // Admin API key
)
```

---

## 6. Plugin Type Reference

For development guides, directory structures, YAML configuration, and Python implementation for each plugin type, refer to the corresponding documentation:

| Plugin Type | Purpose | Development Guide | Declaration Definition |
|-------------|---------|-------------------|------------------------|
| Tool | Tool functions for Agent/workflow invocation | [tool-plugin.md](tool-plugin.md) | `tool_declaration.go` |
| Model | AI model providers (LLM, Embedding, etc.) | [model-plugin.md](model-plugin.md) | `model_declaration.go` |
| Agent Strategy | Agent reasoning strategies | [agent-strategy-plugin.md](agent-strategy-plugin.md) | `agent_declaration.go` |
| Datasource | Data source connections (cloud drive, documents, etc.) | [datasource-plugin.md](datasource-plugin.md) | `datasource_declaration.go` |
| Trigger | Webhook event triggers | [trigger-plugin.md](trigger-plugin.md) | `trigger_declaration.go` |
| Extension | HTTP endpoint extensions | [extension-plugin.md](extension-plugin.md) | `endpoint_declaration.go` |

Declaration definition files are located in the `pkg/entities/plugin_entities/` directory.

### 6.1 Directory Structure Comparison

| Plugin Type | Provider Directory | Core Function Directory | manifest plugins Field |
|-------------|-------------------|------------------------|----------------------|
| Tool | `provider/` | `tools/` | `tools` |
| Model | `provider/` | `models/{type}/` | `models` |
| Extension | `group/` | `endpoints/` | `endpoints` |
| Agent Strategy | `provider/` | `strategies/` | `agent_strategies` |
| Datasource | `provider/` | `datasources/` | `datasources` |
| Trigger | `provider/` | `events/` | `triggers` |

### 6.2 Common Files Description

| File | Purpose |
|------|---------|
| `manifest.yaml` | Plugin metadata, version, permission declarations |
| `pyproject.toml` | Python dependencies (uv managed) |
| `main.py` | Plugin entry point |
| `README.md` | Plugin documentation |
| `_assets/icon.svg` | Plugin icon (SVG format) |
| `*.yaml` | Declaration files (parameters, schema, i18n) |
| `*.py` | Implementation files (business logic) |

---

## Appendix

### A. Plugin Manifest Complete Structure

```go
type PluginDeclaration struct {
    // Basic information
    Version     string     // Version number (semantic versioning)
    Type        string     // Type: "plugin"
    Author      string     // Author (1-64 characters)
    Name        string     // Name (1-128 characters)
    Label       I18nObject // Multilingual label (required)
    Description I18nObject // Multilingual description (required)
    Icon        string     // Icon path (required, max 128 characters)
    IconDark    string     // Dark theme icon (optional)

    // Resource requirements
    Resource PluginResourceRequirement

    // Plugin component declarations
    Plugins PluginExtensions

    // Runtime meta information
    Meta PluginMeta

    // Category tags
    Tags []PluginTag

    // Timestamp
    CreatedAt time.Time

    // Optional information
    Privacy *string // Privacy policy
    Repo    *string // Code repository

    // Provider declarations (select based on type)
    Verified      bool
    Endpoint      *EndpointProviderDeclaration
    Model         *ModelProviderDeclaration
    Tool          *ToolProviderDeclaration
    AgentStrategy *AgentStrategyProviderDeclaration
    Datasource    *DatasourceProviderDeclaration
    Trigger       *TriggerProviderDeclaration
}

// Resource requirements
type PluginResourceRequirement struct {
    Memory     int64                        // Memory (bytes)
    Permission *PluginPermissionRequirement // Permission requirements
}

// Permission requirements
type PluginPermissionRequirement struct {
    Tool     *PluginPermissionToolRequirement     // Tool invocation permission
    Model    *PluginPermissionModelRequirement    // Model invocation permission
    Node     *PluginPermissionNodeRequirement     // Node invocation permission
    Endpoint *PluginPermissionEndpointRequirement // Endpoint registration permission
    App      *PluginPermissionAppRequirement      // App invocation permission
    Storage  *PluginPermissionStorageRequirement  // Storage permission
}

// Runtime meta information
type PluginMeta struct {
    Version            string   // Meta version
    Arch               []Arch   // Supported architectures: amd64, arm64
    Runner             PluginRunner
    MinimumDifyVersion *string  // Minimum Dify version
}

type PluginRunner struct {
    Language   string // Language: python
    Version    string // Version: 3.11
    Entrypoint string // Entry point
}
```

### B. Multilingual Object Structure

```go
type I18nObject struct {
    EnUS   string `json:"en_US"`            // English (required)
    JaJp   string `json:"ja_JP,omitempty"`  // Japanese
    ZhHans string `json:"zh_Hans,omitempty"` // Simplified Chinese
    PtBr   string `json:"pt_BR,omitempty"`  // Portuguese
}
```

### C. Supported Tags

```go
// Available tags
search, image, videos, weather, finance, design, travel, social,
news, medical, productivity, education, business, entertainment,
utilities, agent, rag, other, trigger
```

### D. Configuration Types

```go
const (
    CONFIG_TYPE_SECRET_INPUT   = "secret-input"   // Sensitive input
    CONFIG_TYPE_TEXT_INPUT     = "text-input"     // Text input
    CONFIG_TYPE_SELECT         = "select"         // Dropdown selection
    CONFIG_TYPE_BOOLEAN        = "boolean"        // Boolean value
    CONFIG_TYPE_MODEL_SELECTOR = "model-selector" // Model selector
    CONFIG_TYPE_APP_SELECTOR   = "app-selector"   // App selector
    CONFIG_TYPE_TOOLS_SELECTOR = "array[tools]"   // Tools selector
    CONFIG_TYPE_ANY            = "any"            // Any type
)
```
