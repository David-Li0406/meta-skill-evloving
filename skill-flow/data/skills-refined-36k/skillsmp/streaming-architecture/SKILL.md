---
name: streaming-architecture
description: LiteLLM-RS Streaming Architecture. Covers UnifiedSSEParser, SSETransformer trait, VecDeque buffering, provider-specific transformers, and real-time event handling.
---

# Streaming Architecture Guide

## Overview

LiteLLM-RS implements a unified streaming system that handles Server-Sent Events (SSE) from 66+ providers with provider-specific transformations while presenting a consistent OpenAI-compatible output format.

### Streaming Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Provider SSE Stream                          │
│  (OpenAI, Anthropic, Google, etc.)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    UnifiedSSEParser                             │
│  - Buffer management with VecDeque                              │
│  - Line-based SSE parsing                                       │
│  - Event type detection                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SSETransformer                               │
│  - Provider-specific data parsing                               │
│  - Format normalization to ChatChunk                            │
│  - Error handling                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OpenAI-Compatible Output                     │
│  ChatChunk (data: {...}\n\n or [DONE])                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### UnifiedSSEParser

```rust
use std::collections::VecDeque;

/// Unified SSE parser that handles various provider formats
pub struct UnifiedSSEParser {
    /// Buffer for incomplete lines
    buffer: VecDeque<u8>,
    /// Current event type being parsed
    current_event_type: Option<String>,
    /// Maximum buffer size to prevent memory issues
    max_buffer_size: usize,
}

impl UnifiedSSEParser {
    pub fn new() -> Self {
        Self {
            buffer: VecDeque::with_capacity(8192),
            current_event_type: None,
            max_buffer_size: 1024 * 1024, // 1MB max buffer
        }
    }

    /// Feed bytes into the parser and extract complete events
    pub fn feed(&mut self, bytes: &[u8]) -> Vec<SSEEvent> {
        // Add bytes to buffer
        for &byte in bytes {
            if self.buffer.len() < self.max_buffer_size {
                self.buffer.push_back(byte);
            }
        }

        self.extract_events()
    }

    /// Extract complete SSE events from the buffer
    fn extract_events(&mut self) -> Vec<SSEEvent> {
        let mut events = Vec::new();
        let mut current_data = String::new();

        // Convert buffer to string for processing
        let text: String = self.buffer.iter().map(|&b| b as char).collect();

        // Process line by line
        let mut processed_len = 0;
        for line in text.split('\n') {
            processed_len += line.len() + 1; // +1 for \n

            let line = line.trim_end_matches('\r');

            if line.is_empty() {
                // Empty line marks end of event
                if !current_data.is_empty() {
                    events.push(SSEEvent {
                        event_type: self.current_event_type.take(),
                        data: current_data.clone(),
                    });
                    current_data.clear();
                }
                continue;
            }

            if let Some(event_type) = line.strip_prefix("event: ") {
                self.current_event_type = Some(event_type.to_string());
            } else if let Some(data) = line.strip_prefix("data: ") {
                if !current_data.is_empty() {
                    current_data.push('\n');
                }
                current_data.push_str(data);
            } else if line.starts_with(':') {
                // Comment line, ignore
                continue;
            } else if let Some(id) = line.strip_prefix("id: ") {
                // Event ID, can be stored if needed
                let _ = id;
            } else if let Some(retry) = line.strip_prefix("retry: ") {
                // Retry interval, can be stored if needed
                let _ = retry;
            }
        }

        // Remove processed bytes from buffer
        // Keep any incomplete line
        let last_newline = text.rfind('\n').map(|i| i + 1).unwrap_or(0);
        for _ in 0..last_newline {
            self.buffer.pop_front();
        }

        events
    }

    /// Reset parser state
    pub fn reset(&mut self) {
        self.buffer.clear();
        self.current_event_type = None;
    }
}

#[derive(Debug, Clone)]
pub struct SSEEvent {
    pub event_type: Option<String>,
    pub data: String,
}
```

---

## SSETransformer Trait

```rust
use crate::core::types::responses::ChatChunk;

/// Trait for transforming provider-specific SSE data to ChatChunk
#[async_trait]
pub trait SSETransformer: Send + Sync {
    /// Transform raw SSE data to ChatChunk
    fn transform(&self, event: &SSEEvent) -> Result<Option<ChatChunk>, StreamError>;

    /// Check if the event indicates stream end
    fn is_done(&self, event: &SSEEvent) -> bool;

    /// Get provider name for error context
    fn provider_name(&self) -> &'static str;

    /// Handle provider-specific error events
    fn handle_error(&self, event: &SSEEvent) -> Option<StreamError>;
}

#[derive(Debug, thiserror::Error)]
pub enum StreamError {
    #[error("[{provider}] Parse error: {message}")]
    Parse {
        provider: &'static str,
        message: String,
    },

    #[error("[{provider}] Stream interrupted: {message}")]
    Interrupted {
        provider: &'static str,
        message: String,
    },

    #[error("[{provider}] Provider error: {message}")]
    ProviderError {
        provider: &'static str,
        message: String,
    },
}
```

---

## Provider-Specific Transformers

### OpenAI Transformer

```rust
pub struct OpenAITransformer;

impl SSETransformer for OpenAITransformer {
    fn transform(&self, event: &SSEEvent) -> Result<Option<ChatChunk>, StreamError> {
        // Handle [DONE] marker
        if event.data == "[DONE]" {
            return Ok(None);
        }

        // Parse OpenAI chunk format
        let chunk: ChatChunk = serde_json::from_str(&event.data)
            .map_err(|e| StreamError::Parse {
                provider: self.provider_name(),
                message: e.to_string(),
            })?;

        Ok(Some(chunk))
    }

    fn is_done(&self, event: &SSEEvent) -> bool {
        event.data == "[DONE]"
    }

    fn provider_name(&self) -> &'static str {
        "openai"
    }

    fn handle_error(&self, event: &SSEEvent) -> Option<StreamError> {
        if event.data.contains("\"error\"") {
            if let Ok(error) = serde_json::from_str::<serde_json::Value>(&event.data) {
                if let Some(msg) = error.get("error").and_then(|e| e.get("message")).and_then(|m| m.as_str()) {
                    return Some(StreamError::ProviderError {
                        provider: self.provider_name(),
                        message: msg.to_string(),
                    });
                }
            }
        }
        None
    }
}
```

### Anthropic Transformer

```rust
pub struct AnthropicTransformer {
    /// Accumulated content for multi-part responses
    accumulated_content: std::cell::RefCell<String>,
}

impl AnthropicTransformer {
    pub fn new() -> Self {
        Self {
            accumulated_content: std::cell::RefCell::new(String::new()),
        }
    }
}

impl SSETransformer for AnthropicTransformer {
    fn transform(&self, event: &SSEEvent) -> Result<Option<ChatChunk>, StreamError> {
        // Anthropic uses event types
        let event_type = event.event_type.as_deref().unwrap_or("");

        match event_type {
            "message_start" => {
                // Initialize message, extract ID
                let data: serde_json::Value = serde_json::from_str(&event.data)
                    .map_err(|e| StreamError::Parse {
                        provider: self.provider_name(),
                        message: e.to_string(),
                    })?;

                let id = data.get("message")
                    .and_then(|m| m.get("id"))
                    .and_then(|i| i.as_str())
                    .unwrap_or("msg_anthropic")
                    .to_string();

                Ok(Some(ChatChunk {
                    id,
                    object: "chat.completion.chunk".to_string(),
                    created: chrono::Utc::now().timestamp(),
                    model: data.get("message")
                        .and_then(|m| m.get("model"))
                        .and_then(|m| m.as_str())
                        .unwrap_or("claude")
                        .to_string(),
                    choices: vec![],
                    usage: None,
                    system_fingerprint: None,
                }))
            }

            "content_block_delta" => {
                let data: serde_json::Value = serde_json::from_str(&event.data)
                    .map_err(|e| StreamError::Parse {
                        provider: self.provider_name(),
                        message: e.to_string(),
                    })?;

                let delta_text = data.get("delta")
                    .and_then(|d| d.get("text"))
                    .and_then(|t| t.as_str())
                    .unwrap_or("");

                // Convert to OpenAI chunk format
                Ok(Some(ChatChunk {
                    id: "".to_string(),
                    object: "chat.completion.chunk".to_string(),
                    created: chrono::Utc::now().timestamp(),
                    model: "".to_string(),
                    choices: vec![crate::core::types::responses::ChunkChoice {
                        index: 0,
                        delta: crate::core::types::responses::ChunkDelta {
                            role: None,
                            content: Some(delta_text.to_string()),
                            tool_calls: None,
                            function_call: None,
                        },
                        finish_reason: None,
                        logprobs: None,
                    }],
                    usage: None,
                    system_fingerprint: None,
                }))
            }

            "message_stop" => {
                Ok(None)
            }

            "message_delta" => {
                // Final message with usage info
                let data: serde_json::Value = serde_json::from_str(&event.data)
                    .map_err(|e| StreamError::Parse {
                        provider: self.provider_name(),
                        message: e.to_string(),
                    })?;

                let finish_reason = data.get("delta")
                    .and_then(|d| d.get("stop_reason"))
                    .and_then(|r| r.as_str())
                    .map(|r| match r {
                        "end_turn" => crate::core::types::responses::FinishReason::Stop,
                        "max_tokens" => crate::core::types::responses::FinishReason::Length,
                        "tool_use" => crate::core::types::responses::FinishReason::ToolCalls,
                        _ => crate::core::types::responses::FinishReason::Stop,
                    });

                Ok(Some(ChatChunk {
                    id: "".to_string(),
                    object: "chat.completion.chunk".to_string(),
                    created: chrono::Utc::now().timestamp(),
                    model: "".to_string(),
                    choices: vec![crate::core::types::responses::ChunkChoice {
                        index: 0,
                        delta: crate::core::types::responses::ChunkDelta {
                            role: None,
                            content: None,
                            tool_calls: None,
                            function_call: None,
                        },
                        finish_reason,
                        logprobs: None,
                    }],
                    usage: data.get("usage").and_then(|u| {
                        Some(crate::core::types::responses::Usage {
                            prompt_tokens: u.get("input_tokens").and_then(|t| t.as_u64()).unwrap_or(0) as u32,
                            completion_tokens: u.get("output_tokens").and_then(|t| t.as_u64()).unwrap_or(0) as u32,
                            total_tokens: 0,
                            prompt_tokens_details: None,
                            completion_tokens_details: None,
                            thinking_usage: None,
                        })
                    }),
                    system_fingerprint: None,
                }))
            }

            "error" => {
                Err(StreamError::ProviderError {
                    provider: self.provider_name(),
                    message: event.data.clone(),
                })
            }

            _ => Ok(None),
        }
    }

    fn is_done(&self, event: &SSEEvent) -> bool {
        event.event_type.as_deref() == Some("message_stop")
    }

    fn provider_name(&self) -> &'static str {
        "anthropic"
    }

    fn handle_error(&self, event: &SSEEvent) -> Option<StreamError> {
        if event.event_type.as_deref() == Some("error") {
            return Some(StreamError::ProviderError {
                provider: self.provider_name(),
                message: event.data.clone(),
            });
        }
        None
    }
}
```

### Google Gemini Transformer

```rust
pub struct GeminiTransformer;

impl SSETransformer for GeminiTransformer {
    fn transform(&self, event: &SSEEvent) -> Result<Option<ChatChunk>, StreamError> {
        // Gemini uses a different format
        let data: serde_json::Value = serde_json::from_str(&event.data)
            .map_err(|e| StreamError::Parse {
                provider: self.provider_name(),
                message: e.to_string(),
            })?;

        // Extract text from candidates[0].content.parts[0].text
        let text = data.get("candidates")
            .and_then(|c| c.as_array())
            .and_then(|c| c.first())
            .and_then(|c| c.get("content"))
            .and_then(|c| c.get("parts"))
            .and_then(|p| p.as_array())
            .and_then(|p| p.first())
            .and_then(|p| p.get("text"))
            .and_then(|t| t.as_str());

        let finish_reason = data.get("candidates")
            .and_then(|c| c.as_array())
            .and_then(|c| c.first())
            .and_then(|c| c.get("finishReason"))
            .and_then(|r| r.as_str())
            .map(|r| match r {
                "STOP" => crate::core::types::responses::FinishReason::Stop,
                "MAX_TOKENS" => crate::core::types::responses::FinishReason::Length,
                "SAFETY" => crate::core::types::responses::FinishReason::ContentFilter,
                _ => crate::core::types::responses::FinishReason::Stop,
            });

        Ok(Some(ChatChunk {
            id: "".to_string(),
            object: "chat.completion.chunk".to_string(),
            created: chrono::Utc::now().timestamp(),
            model: "gemini".to_string(),
            choices: vec![crate::core::types::responses::ChunkChoice {
                index: 0,
                delta: crate::core::types::responses::ChunkDelta {
                    role: None,
                    content: text.map(|t| t.to_string()),
                    tool_calls: None,
                    function_call: None,
                },
                finish_reason,
                logprobs: None,
            }],
            usage: None,
            system_fingerprint: None,
        }))
    }

    fn is_done(&self, event: &SSEEvent) -> bool {
        serde_json::from_str::<serde_json::Value>(&event.data)
            .ok()
            .and_then(|d| d.get("candidates"))
            .and_then(|c| c.as_array())
            .and_then(|c| c.first())
            .and_then(|c| c.get("finishReason"))
            .is_some()
    }

    fn provider_name(&self) -> &'static str {
        "google"
    }

    fn handle_error(&self, event: &SSEEvent) -> Option<StreamError> {
        if let Ok(data) = serde_json::from_str::<serde_json::Value>(&event.data) {
            if let Some(error) = data.get("error") {
                return Some(StreamError::ProviderError {
                    provider: self.provider_name(),
                    message: error.to_string(),
                });
            }
        }
        None
    }
}
```

---

## Stream Processing Pipeline

```rust
use futures::{Stream, StreamExt};
use std::pin::Pin;

pub struct StreamProcessor<T: SSETransformer> {
    parser: UnifiedSSEParser,
    transformer: T,
}

impl<T: SSETransformer> StreamProcessor<T> {
    pub fn new(transformer: T) -> Self {
        Self {
            parser: UnifiedSSEParser::new(),
            transformer,
        }
    }

    /// Process a byte stream and produce ChatChunks
    pub fn process_stream(
        mut self,
        input: impl Stream<Item = Result<bytes::Bytes, reqwest::Error>> + Send + 'static,
    ) -> Pin<Box<dyn Stream<Item = Result<ChatChunk, StreamError>> + Send>> {
        let stream = input.flat_map(move |result| {
            match result {
                Ok(bytes) => {
                    let events = self.parser.feed(&bytes);
                    let chunks: Vec<Result<ChatChunk, StreamError>> = events
                        .into_iter()
                        .filter_map(|event| {
                            // Check for errors first
                            if let Some(error) = self.transformer.handle_error(&event) {
                                return Some(Err(error));
                            }

                            // Check if done
                            if self.transformer.is_done(&event) {
                                return None;
                            }

                            // Transform event
                            match self.transformer.transform(&event) {
                                Ok(Some(chunk)) => Some(Ok(chunk)),
                                Ok(None) => None,
                                Err(e) => Some(Err(e)),
                            }
                        })
                        .collect();

                    futures::stream::iter(chunks)
                }
                Err(e) => {
                    futures::stream::iter(vec![Err(StreamError::Interrupted {
                        provider: self.transformer.provider_name(),
                        message: e.to_string(),
                    })])
                }
            }
        });

        Box::pin(stream)
    }
}
```

---

## HTTP Response Streaming

```rust
use actix_web::{HttpResponse, web};
use futures::StreamExt;

pub async fn stream_chat_completion(
    request: ChatRequest,
    provider: Arc<dyn LLMProvider>,
) -> HttpResponse {
    // Get streaming response from provider
    let stream = match provider.chat_completion_stream(request, context).await {
        Ok(s) => s,
        Err(e) => {
            return HttpResponse::InternalServerError()
                .json(json!({"error": e.to_string()}));
        }
    };

    // Transform to SSE format
    let sse_stream = stream.map(|result| {
        match result {
            Ok(chunk) => {
                let json = serde_json::to_string(&chunk).unwrap_or_default();
                Ok::<_, std::io::Error>(bytes::Bytes::from(format!("data: {}\n\n", json)))
            }
            Err(e) => {
                let error_json = json!({"error": e.to_string()});
                Ok(bytes::Bytes::from(format!("data: {}\n\n", error_json)))
            }
        }
    });

    // Add [DONE] marker at the end
    let final_stream = sse_stream.chain(futures::stream::once(async {
        Ok::<_, std::io::Error>(bytes::Bytes::from("data: [DONE]\n\n"))
    }));

    HttpResponse::Ok()
        .content_type("text/event-stream")
        .insert_header(("Cache-Control", "no-cache"))
        .insert_header(("Connection", "keep-alive"))
        .streaming(final_stream)
}
```

---

## Buffer Management

### VecDeque Advantages

```rust
/// VecDeque is used for efficient buffer management:
/// - O(1) push/pop at both ends
/// - Contiguous memory for cache efficiency
/// - No reallocation when cycling through buffer

impl UnifiedSSEParser {
    /// Efficient buffer trimming
    fn trim_processed(&mut self, bytes_processed: usize) {
        // VecDeque allows efficient removal from front
        for _ in 0..bytes_processed {
            self.buffer.pop_front();
        }
    }

    /// Prevent buffer overflow
    fn check_buffer_limit(&mut self) {
        while self.buffer.len() > self.max_buffer_size {
            // Drop oldest data if buffer exceeds limit
            self.buffer.pop_front();
        }
    }
}
```

---

## Configuration

```yaml
streaming:
  enabled: true

  buffer:
    initial_size: 8192      # Initial buffer size in bytes
    max_size: 1048576       # 1MB max buffer
    chunk_size: 4096        # Read chunk size

  timeouts:
    first_byte: 30000       # 30s timeout for first byte
    between_events: 60000   # 60s timeout between events
    total: 300000           # 5 minute total timeout

  retry:
    enabled: true
    max_attempts: 3
    backoff_ms: 1000
```

---

## Best Practices

### 1. Handle Incomplete Events

```rust
// Good - buffer incomplete data
pub fn feed(&mut self, bytes: &[u8]) -> Vec<SSEEvent> {
    self.buffer.extend(bytes);
    self.extract_complete_events() // Only return complete events
}

// Bad - assume complete data
pub fn feed(&mut self, bytes: &[u8]) -> Vec<SSEEvent> {
    let text = String::from_utf8_lossy(bytes);
    self.parse_all(&text) // May split events incorrectly
}
```

### 2. Preserve Stream Order

```rust
// Good - maintain ordering
let stream = input.map(|chunk| {
    self.process_chunk(chunk) // Process in order
});

// Bad - parallel processing breaks order
let stream = input
    .map(|chunk| async move { self.process_chunk(chunk).await })
    .buffer_unordered(10); // Order not guaranteed!
```

### 3. Clean Resource Handling

```rust
// Good - cleanup on drop
impl Drop for StreamProcessor {
    fn drop(&mut self) {
        self.parser.reset();
        // Signal stream end if needed
    }
}
```

### 4. Backpressure Handling

```rust
// Good - respect backpressure
let stream = input
    .map(|chunk| self.process(chunk))
    .buffer_unordered(1); // Limit concurrent processing

// Bad - unbounded buffering
let stream = input
    .map(|chunk| self.process(chunk))
    .buffer_unordered(1000); // May exhaust memory
```
