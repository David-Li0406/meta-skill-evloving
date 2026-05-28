---
name: agent-execution
description: >
  Agent execution patterns including LLM calls and token handling.
  Use when implementing agent execution or multipart forms.
  Triggers: agent.Agent, VisionForm, ParseVisionForm, Token injection,
  constructAgent, ChatStream, VisionStream, multipart/form-data, base64,
  Provider.Options["token"], go-agents, ExecuteRequest, SetSecret, GetSecret.
  File patterns: internal/agents/*.go
---

# Agent Execution Patterns

## When This Skill Applies

- Implementing agent endpoints (chat, vision, embed)
- Handling multipart form uploads
- Injecting runtime tokens
- Streaming agent responses
- Working with go-agents library

## Principles

### 1. VisionForm Pattern

Centralized multipart form parsing for vision endpoints with validation and base64 conversion:

```go
type VisionForm struct {
    Prompt  string
    Images  []string  // base64 data URIs
    Options map[string]any
    Token   string
}

func ParseVisionForm(r *http.Request, maxMemory int64) (*VisionForm, error) {
    if err := r.ParseMultipartForm(maxMemory); err != nil {
        return nil, fmt.Errorf("failed to parse multipart form: %w", err)
    }

    form := &VisionForm{
        Prompt: r.FormValue("prompt"),
        Token:  r.FormValue("token"),
    }

    // Validate required fields
    if form.Prompt == "" {
        return nil, fmt.Errorf("prompt is required")
    }

    // Parse optional JSON options
    if optStr := r.FormValue("options"); optStr != "" {
        if err := json.Unmarshal([]byte(optStr), &form.Options); err != nil {
            return nil, fmt.Errorf("invalid options JSON: %w", err)
        }
    }

    // Convert uploaded images to base64 data URIs
    files := r.MultipartForm.File["images"]
    if len(files) == 0 {
        return nil, fmt.Errorf("at least one image is required")
    }

    images, err := prepareImages(files)
    if err != nil {
        return nil, err
    }
    form.Images = images

    return form, nil
}
```

**Usage**:
```go
func (h *Handler) Vision(w http.ResponseWriter, r *http.Request) {
    form, err := ParseVisionForm(r, 32<<20)  // 32 MB memory limit
    if err != nil {
        handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
        return
    }

    agt, err := h.constructAgent(r.Context(), id, form.Token)
    // ... execute vision with form.Prompt, form.Images, form.Options
}
```

### 2. Token Injection Pattern

Runtime token injection for providers requiring authentication (e.g., Azure):

```go
func (h *Handler) constructAgent(ctx context.Context, id uuid.UUID, token string) (agent.Agent, error) {
    record, err := h.sys.GetByID(ctx, id)
    if err != nil {
        return nil, err
    }

    var cfg agtconfig.AgentConfig
    if err := json.Unmarshal(record.Config, &cfg); err != nil {
        return nil, fmt.Errorf("%w: %v", ErrInvalidConfig, err)
    }

    // Inject token at request time
    if token != "" {
        if cfg.Provider.Options == nil {
            cfg.Provider.Options = make(map[string]any)
        }
        cfg.Provider.Options["token"] = token
    }

    agt, err := agent.New(&cfg)
    if err != nil {
        return nil, fmt.Errorf("%w: %v", ErrInvalidConfig, err)
    }

    return agt, nil
}
```

**Key Points**:
- Token passed at request time, not stored in database
- Stored config uses placeholder value (e.g., `"token": "token"`) for validation
- Real token injected into `Provider.Options["token"]` before agent construction

### 3. Secure Workflow Token Pattern

For workflow execution, tokens must be available during execution but never persisted. Uses the Secrets feature from go-agents-orchestration:

```go
type ExecuteRequest struct {
    Params map[string]any `json:"params,omitempty"`
    Token  string         `json:"token,omitempty"`  // Not persisted
}
```

**Executor Implementation**:
```go
func (e *executor) Execute(ctx context.Context, name string, params map[string]any, token string) (*Run, error) {
    // params persisted to workflow_runs.params
    run, err := e.repo.CreateRun(ctx, name, params)

    // token stored as secret, NOT persisted to checkpoint
    if token != "" {
        initialState = initialState.SetSecret("token", token)
    }

    // Workflow nodes access via s.GetSecret("token")
}
```

**Security Guarantees**:
- Secrets NOT stored in checkpoint data
- Secrets NOT returned in API responses when querying run history
- Secrets available in workflow state during execution only
- Supports expiring JWT tokens (e.g., Azure AD/Entra ID)

**Usage in Workflows**:
```go
// In workflow node
token, _ := s.GetSecret("token")
agentID, err := workflows.ExtractAgentID(s, stage)
// Use token for agent construction
```

### 4. SSE Streaming Pattern

Server-Sent Events for streaming agent responses:

```go
func (h *Handler) writeSSEStream(w http.ResponseWriter, r *http.Request, stream <-chan *response.StreamingChunk) {
    w.Header().Set("Content-Type", "text/event-stream")
    w.Header().Set("Cache-Control", "no-cache")
    w.Header().Set("Connection", "keep-alive")
    w.WriteHeader(http.StatusOK)

    if f, ok := w.(http.Flusher); ok {
        f.Flush()
    }

    for chunk := range stream {
        if chunk.Error != nil {
            data, _ := json.Marshal(map[string]string{"error": chunk.Error.Error()})
            fmt.Fprintf(w, "data: %s\n\n", data)
            if f, ok := w.(http.Flusher); ok {
                f.Flush()
            }
            return
        }

        select {
        case <-r.Context().Done():
            return
        default:
        }

        data, _ := json.Marshal(chunk)
        fmt.Fprintf(w, "data: %s\n\n", data)
        if f, ok := w.(http.Flusher); ok {
            f.Flush()
        }
    }

    fmt.Fprintf(w, "data: [DONE]\n\n")
    if f, ok := w.(http.Flusher); ok {
        f.Flush()
    }
}
```

**Key Points**:
- `text/event-stream` content type
- Each chunk prefixed with `data: ` and followed by `\n\n`
- Flush after each chunk for real-time delivery
- Check context cancellation for client disconnect
- Final `[DONE]` marker signals stream completion

## Patterns

### Agent Endpoint Handler

```go
func (h *Handler) Chat(w http.ResponseWriter, r *http.Request) {
    idStr := r.PathValue("id")
    id, err := uuid.Parse(idStr)
    if err != nil {
        handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
        return
    }

    var req ChatRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        handlers.RespondError(w, h.logger, http.StatusBadRequest, err)
        return
    }

    agt, err := h.constructAgent(r.Context(), id, req.Token)
    if err != nil {
        handlers.RespondError(w, h.logger, MapHTTPStatus(err), err)
        return
    }

    stream := agt.ChatStream(r.Context(), req.Prompt, req.Options)
    h.writeSSEStream(w, r, stream)
}
```

### Base64 Image Conversion

```go
func prepareImages(files []*multipart.FileHeader) ([]string, error) {
    images := make([]string, 0, len(files))
    for _, fh := range files {
        file, err := fh.Open()
        if err != nil {
            return nil, fmt.Errorf("open image %s: %w", fh.Filename, err)
        }
        defer file.Close()

        data, err := io.ReadAll(file)
        if err != nil {
            return nil, fmt.Errorf("read image %s: %w", fh.Filename, err)
        }

        mimeType := http.DetectContentType(data)
        b64 := base64.StdEncoding.EncodeToString(data)
        dataURI := fmt.Sprintf("data:%s;base64,%s", mimeType, b64)
        images = append(images, dataURI)
    }
    return images, nil
}
```

## Anti-Patterns

### Persisting Tokens

```go
// Bad: Token stored in regular state (gets checkpointed)
initialState = initialState.Set("token", token)

// Good: Token stored as secret (never checkpointed)
initialState = initialState.SetSecret("token", token)
```

### Token in Params

```go
// Bad: Token in params (persisted to database)
run, _ := e.repo.CreateRun(ctx, name, map[string]any{
    "agent_id": agentID,
    "token":    token,
})

// Good: Token separate from params
run, _ := e.repo.CreateRun(ctx, name, map[string]any{
    "agent_id": agentID,
})
initialState = initialState.SetSecret("token", token)
```
