---
name: error-handling
description: LiteLLM-RS Error Handling Architecture. Covers two-tier error hierarchy, ProviderError factory methods, HTTP status mapping, retry logic, and error context preservation.
---

# Error Handling Architecture Guide

## Two-Tier Error Hierarchy

LiteLLM-RS uses a two-tier error architecture optimized for 66+ providers:

```
┌────────────────────────────────────────────────────────┐
│                    Gateway Layer                        │
│  LiteLLMError (core/types/errors/litellm.rs)          │
│  - 15 variants for gateway-level errors                │
│  - Routing, configuration, authentication errors       │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│                   Provider Layer                        │
│  ProviderError (core/providers/unified_provider.rs)   │
│  - 24 variants for provider-specific errors            │
│  - Each variant includes provider: &'static str        │
│  - Rich factory methods for error creation             │
└────────────────────────────────────────────────────────┘
```

---

## ProviderError (24 Variants)

```rust
// src/core/providers/unified_provider.rs

#[derive(Debug, Clone, thiserror::Error)]
pub enum ProviderError {
    // Authentication & Authorization
    #[error("[{provider}] Authentication failed: {message}")]
    Authentication {
        provider: &'static str,
        message: String,
    },

    // Rate Limiting & Quotas
    #[error("[{provider}] Rate limit exceeded: {message}")]
    RateLimit {
        provider: &'static str,
        message: String,
        retry_after: Option<u64>,
        rpm_limit: Option<u32>,
        tpm_limit: Option<u32>,
        current_usage: Option<u32>,
    },

    #[error("[{provider}] Quota exceeded: {message}")]
    QuotaExceeded {
        provider: &'static str,
        message: String,
    },

    // Model & Request Errors
    #[error("[{provider}] Model not found: {model}")]
    ModelNotFound {
        provider: &'static str,
        model: String,
    },

    #[error("[{provider}] Invalid request: {message}")]
    InvalidRequest {
        provider: &'static str,
        message: String,
    },

    // Network & Availability
    #[error("[{provider}] Network error: {message}")]
    Network {
        provider: &'static str,
        message: String,
    },

    #[error("[{provider}] Request timeout: {message}")]
    Timeout {
        provider: &'static str,
        message: String,
    },

    #[error("[{provider}] Provider unavailable: {message}")]
    ProviderUnavailable {
        provider: &'static str,
        message: String,
    },

    // Feature Support
    #[error("[{provider}] Feature not supported: {feature}")]
    NotSupported {
        provider: &'static str,
        feature: String,
    },

    #[error("[{provider}] Not implemented: {feature}")]
    NotImplemented {
        provider: &'static str,
        feature: String,
    },

    #[error("[{provider}] Feature disabled: {feature}")]
    FeatureDisabled {
        provider: &'static str,
        feature: String,
    },

    // Content & Token Limits
    #[error("[{provider}] Context length exceeded: max={max}, actual={actual}")]
    ContextLengthExceeded {
        provider: &'static str,
        max: u32,
        actual: u32,
    },

    #[error("[{provider}] Token limit exceeded: {message}")]
    TokenLimitExceeded {
        provider: &'static str,
        message: String,
    },

    #[error("[{provider}] Content filtered: {reason}")]
    ContentFiltered {
        provider: &'static str,
        reason: String,
        policy_violations: Option<Vec<String>>,
        potentially_retryable: Option<bool>,
    },

    // Configuration & Serialization
    #[error("[{provider}] Configuration error: {message}")]
    Configuration {
        provider: &'static str,
        message: String,
    },

    #[error("[{provider}] Serialization error: {message}")]
    Serialization {
        provider: &'static str,
        message: String,
    },

    // Advanced Errors
    #[error("[{provider}] API error (status={status}): {message}")]
    ApiError {
        provider: &'static str,
        status: u16,
        message: String,
    },

    #[error("[{provider}] Deployment error ({deployment}): {message}")]
    DeploymentError {
        provider: &'static str,
        deployment: String,
        message: String,
    },

    #[error("[{provider}] Response parsing error: {message}")]
    ResponseParsing {
        provider: &'static str,
        message: String,
    },

    #[error("[{provider}] Routing error: {message}")]
    RoutingError {
        provider: &'static str,
        attempted_providers: Vec<String>,
        message: String,
    },

    #[error("[{provider}] Transformation error ({from_format} -> {to_format}): {message}")]
    TransformationError {
        provider: &'static str,
        from_format: String,
        to_format: String,
        message: String,
    },

    #[error("[{provider}] Streaming error ({stream_type}): {message}")]
    Streaming {
        provider: &'static str,
        stream_type: String,
        position: Option<u64>,
        last_chunk: Option<String>,
        message: String,
    },

    #[error("[{provider}] Operation cancelled ({operation_type}): {cancellation_reason}")]
    Cancelled {
        provider: &'static str,
        operation_type: String,
        cancellation_reason: String,
    },

    #[error("[{provider}] Error: {message}")]
    Other {
        provider: &'static str,
        message: String,
    },
}
```

---

## Factory Methods

### Basic Factory Methods

```rust
impl ProviderError {
    pub fn authentication(provider: &'static str, message: impl Into<String>) -> Self {
        Self::Authentication {
            provider,
            message: message.into(),
        }
    }

    pub fn rate_limit(provider: &'static str, retry_after: Option<u64>) -> Self {
        Self::RateLimit {
            provider,
            message: "Rate limit exceeded".to_string(),
            retry_after,
            rpm_limit: None,
            tpm_limit: None,
            current_usage: None,
        }
    }

    pub fn model_not_found(provider: &'static str, model: impl Into<String>) -> Self {
        Self::ModelNotFound {
            provider,
            model: model.into(),
        }
    }

    pub fn invalid_request(provider: &'static str, message: impl Into<String>) -> Self {
        Self::InvalidRequest {
            provider,
            message: message.into(),
        }
    }

    pub fn network(provider: &'static str, message: impl Into<String>) -> Self {
        Self::Network {
            provider,
            message: message.into(),
        }
    }

    pub fn timeout(provider: &'static str, message: impl Into<String>) -> Self {
        Self::Timeout {
            provider,
            message: message.into(),
        }
    }

    pub fn provider_unavailable(provider: &'static str, message: impl Into<String>) -> Self {
        Self::ProviderUnavailable {
            provider,
            message: message.into(),
        }
    }

    pub fn not_supported(provider: &'static str, feature: impl Into<String>) -> Self {
        Self::NotSupported {
            provider,
            feature: feature.into(),
        }
    }

    pub fn configuration(provider: &'static str, message: impl Into<String>) -> Self {
        Self::Configuration {
            provider,
            message: message.into(),
        }
    }

    pub fn serialization(provider: &'static str, message: impl Into<String>) -> Self {
        Self::Serialization {
            provider,
            message: message.into(),
        }
    }

    pub fn api_error(provider: &'static str, status: u16, message: impl Into<String>) -> Self {
        Self::ApiError {
            provider,
            status,
            message: message.into(),
        }
    }

    pub fn response_parsing(provider: &'static str, message: impl Into<String>) -> Self {
        Self::ResponseParsing {
            provider,
            message: message.into(),
        }
    }
}
```

### Enhanced Factory Methods

```rust
impl ProviderError {
    pub fn rate_limit_with_limits(
        provider: &'static str,
        retry_after: Option<u64>,
        rpm_limit: Option<u32>,
        tpm_limit: Option<u32>,
        current_usage: Option<u32>,
    ) -> Self {
        Self::RateLimit {
            provider,
            message: format!(
                "Rate limit exceeded. RPM: {:?}, TPM: {:?}, Current: {:?}",
                rpm_limit, tpm_limit, current_usage
            ),
            retry_after,
            rpm_limit,
            tpm_limit,
            current_usage,
        }
    }

    pub fn context_length_exceeded(
        provider: &'static str,
        max: u32,
        actual: u32,
    ) -> Self {
        Self::ContextLengthExceeded {
            provider,
            max,
            actual,
        }
    }

    pub fn content_filtered(
        provider: &'static str,
        reason: impl Into<String>,
        policy_violations: Option<Vec<String>>,
        potentially_retryable: Option<bool>,
    ) -> Self {
        Self::ContentFiltered {
            provider,
            reason: reason.into(),
            policy_violations,
            potentially_retryable,
        }
    }

    pub fn streaming_error(
        provider: &'static str,
        stream_type: impl Into<String>,
        position: Option<u64>,
        last_chunk: Option<String>,
        message: impl Into<String>,
    ) -> Self {
        Self::Streaming {
            provider,
            stream_type: stream_type.into(),
            position,
            last_chunk,
            message: message.into(),
        }
    }

    pub fn routing_error(
        provider: &'static str,
        attempted_providers: Vec<String>,
        message: impl Into<String>,
    ) -> Self {
        Self::RoutingError {
            provider,
            attempted_providers,
            message: message.into(),
        }
    }
}
```

---

## HTTP Status Mapping

### Standard Mapping Pattern

```rust
impl MyProvider {
    fn map_http_error(&self, status: u16, body: &str) -> ProviderError {
        match status {
            // Authentication errors
            401 => ProviderError::authentication(PROVIDER_NAME, "Invalid API key"),
            403 => ProviderError::authentication(PROVIDER_NAME, "Access forbidden"),

            // Not found errors
            404 => ProviderError::model_not_found(PROVIDER_NAME, body),

            // Client errors
            400 => ProviderError::invalid_request(PROVIDER_NAME, body),
            422 => ProviderError::invalid_request(PROVIDER_NAME, "Unprocessable entity"),

            // Rate limiting
            429 => ProviderError::rate_limit(PROVIDER_NAME, self.parse_retry_after(body)),

            // Server errors
            500 => ProviderError::provider_unavailable(PROVIDER_NAME, "Internal server error"),
            502 => ProviderError::provider_unavailable(PROVIDER_NAME, "Bad gateway"),
            503 => ProviderError::provider_unavailable(PROVIDER_NAME, "Service unavailable"),
            504 => ProviderError::timeout(PROVIDER_NAME, "Gateway timeout"),

            // Default
            _ => ProviderError::api_error(PROVIDER_NAME, status, body),
        }
    }

    fn parse_retry_after(&self, body: &str) -> Option<u64> {
        // Parse retry-after from response headers or body
        serde_json::from_str::<serde_json::Value>(body)
            .ok()
            .and_then(|v| v.get("retry_after"))
            .and_then(|v| v.as_u64())
    }
}
```

### ErrorMapper Trait

```rust
// src/core/traits/error_mapper/trait_def.rs

pub trait ErrorMapper: Send + Sync {
    type Error;

    fn map_http_error(&self, status: u16, body: &str) -> Self::Error;
    fn map_network_error(&self, error: reqwest::Error) -> Self::Error;
    fn map_parse_error(&self, error: serde_json::Error) -> Self::Error;
}

// Generic implementation for ProviderError
pub struct GenericErrorMapper;

impl ErrorMapper for GenericErrorMapper {
    type Error = ProviderError;

    fn map_http_error(&self, status: u16, body: &str) -> Self::Error {
        match status {
            401 | 403 => ProviderError::authentication("generic", body),
            404 => ProviderError::model_not_found("generic", body),
            429 => ProviderError::rate_limit("generic", None),
            400 | 422 => ProviderError::invalid_request("generic", body),
            500..=599 => ProviderError::provider_unavailable("generic", body),
            _ => ProviderError::api_error("generic", status, body),
        }
    }

    fn map_network_error(&self, error: reqwest::Error) -> Self::Error {
        if error.is_timeout() {
            ProviderError::timeout("generic", error.to_string())
        } else if error.is_connect() {
            ProviderError::network("generic", error.to_string())
        } else {
            ProviderError::network("generic", error.to_string())
        }
    }

    fn map_parse_error(&self, error: serde_json::Error) -> Self::Error {
        ProviderError::response_parsing("generic", error.to_string())
    }
}
```

---

## Retry Logic

### Retryable Error Detection

```rust
impl ProviderError {
    pub fn is_retryable(&self) -> bool {
        matches!(
            self,
            Self::RateLimit { .. }
                | Self::Timeout { .. }
                | Self::Network { .. }
                | Self::ProviderUnavailable { .. }
        )
    }

    pub fn retry_after(&self) -> Option<Duration> {
        match self {
            Self::RateLimit { retry_after, .. } => {
                retry_after.map(Duration::from_secs)
            }
            Self::Timeout { .. } => Some(Duration::from_secs(1)),
            Self::Network { .. } => Some(Duration::from_millis(500)),
            Self::ProviderUnavailable { .. } => Some(Duration::from_secs(5)),
            _ => None,
        }
    }

    pub fn should_fallback(&self) -> bool {
        matches!(
            self,
            Self::ProviderUnavailable { .. }
                | Self::RateLimit { .. }
                | Self::QuotaExceeded { .. }
                | Self::ModelNotFound { .. }
        )
    }
}
```

### Retry Implementation

```rust
pub async fn execute_with_retry<F, T, E>(
    operation: F,
    max_retries: u32,
    base_delay: Duration,
) -> Result<T, E>
where
    F: Fn() -> Pin<Box<dyn Future<Output = Result<T, E>> + Send>>,
    E: std::fmt::Debug,
{
    let mut attempts = 0;
    let mut last_error;

    loop {
        match operation().await {
            Ok(result) => return Ok(result),
            Err(e) => {
                attempts += 1;
                last_error = e;

                if attempts >= max_retries {
                    break;
                }

                // Exponential backoff
                let delay = base_delay * 2u32.pow(attempts - 1);
                tokio::time::sleep(delay).await;
            }
        }
    }

    Err(last_error)
}
```

---

## LiteLLMError (Gateway Level)

```rust
// src/core/types/errors/litellm.rs

#[derive(Debug, thiserror::Error)]
pub enum LiteLLMError {
    #[error("Provider error: {0}")]
    Provider(#[from] ProviderError),

    #[error("Routing error: {0}")]
    Routing(String),

    #[error("Configuration error: {0}")]
    Configuration(String),

    #[error("Authentication error: {0}")]
    Authentication(String),

    #[error("Authorization error: {0}")]
    Authorization(String),

    #[error("Validation error: {0}")]
    Validation(String),

    #[error("Timeout error: {0}")]
    Timeout(String),

    #[error("Rate limit error: {0}")]
    RateLimit(String),

    #[error("Internal error: {0}")]
    Internal(String),

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Conflict: {0}")]
    Conflict(String),

    #[error("Service unavailable: {0}")]
    ServiceUnavailable(String),

    #[error("Bad gateway: {0}")]
    BadGateway(String),

    #[error("Cancelled: {0}")]
    Cancelled(String),

    #[error("Unknown error: {0}")]
    Unknown(String),
}
```

---

## Error Context Preservation

### Adding Context to Errors

```rust
// Using the anyhow pattern for context
use anyhow::Context;

async fn process_request(request: ChatRequest) -> Result<ChatResponse, LiteLLMError> {
    let provider = select_provider(&request.model)
        .context("Failed to select provider")?;

    let response = provider
        .chat_completion(request, context)
        .await
        .context("Chat completion failed")?;

    Ok(response)
}
```

### Error Chain Display

```rust
impl ProviderError {
    pub fn display_chain(&self) -> String {
        let mut chain = vec![self.to_string()];

        // Add any source errors
        if let Some(source) = std::error::Error::source(self) {
            chain.push(format!("Caused by: {}", source));
        }

        chain.join("\n")
    }
}
```

---

## Best Practices

### 1. Always Use Factory Methods

```rust
// Good
ProviderError::authentication(PROVIDER_NAME, "Invalid API key")

// Bad - verbose and error-prone
ProviderError::Authentication {
    provider: PROVIDER_NAME,
    message: "Invalid API key".to_string(),
}
```

### 2. Include Provider Name

```rust
// Good - error clearly identifies source
ProviderError::network("openai", "Connection refused")

// Bad - unclear which provider failed
ProviderError::network("unknown", "Connection refused")
```

### 3. Preserve Error Context

```rust
// Good - preserves original error
self.pool_manager.execute_request(&url, method, headers, body)
    .await
    .map_err(|e| ProviderError::network(PROVIDER_NAME, e.to_string()))?

// Bad - loses original error
self.pool_manager.execute_request(&url, method, headers, body)
    .await
    .map_err(|_| ProviderError::network(PROVIDER_NAME, "Request failed"))?
```

### 4. Use Specific Error Types

```rust
// Good - specific error type
if response.status() == 429 {
    return Err(ProviderError::rate_limit(PROVIDER_NAME, retry_after));
}

// Bad - generic error loses information
if !response.status().is_success() {
    return Err(ProviderError::api_error(PROVIDER_NAME, status, "Failed"));
}
```

### 5. Handle All Error Variants in Match

```rust
// Good - exhaustive handling
match error {
    ProviderError::RateLimit { retry_after, .. } => {
        if let Some(delay) = retry_after {
            tokio::time::sleep(Duration::from_secs(delay)).await;
        }
        // Retry...
    }
    ProviderError::Authentication { .. } => {
        // Don't retry, return immediately
        return Err(error);
    }
    e if e.is_retryable() => {
        // Retry with backoff
    }
    _ => return Err(error),
}
```

---

## HTTP to ProviderError Mapping Reference

| HTTP Status | ProviderError Variant | Retryable |
|-------------|----------------------|-----------|
| 400 | `InvalidRequest` | No |
| 401 | `Authentication` | No |
| 403 | `Authentication` | No |
| 404 | `ModelNotFound` | No |
| 408 | `Timeout` | Yes |
| 422 | `InvalidRequest` | No |
| 429 | `RateLimit` | Yes |
| 500 | `ProviderUnavailable` | Yes |
| 502 | `ProviderUnavailable` | Yes |
| 503 | `ProviderUnavailable` | Yes |
| 504 | `Timeout` | Yes |
