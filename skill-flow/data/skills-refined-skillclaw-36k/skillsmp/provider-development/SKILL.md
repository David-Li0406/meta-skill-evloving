---
name: provider-development
description: LiteLLM-RS Provider 开发与架构指南。用于添加新 provider、迁移错误处理、维护 66+ provider 的一致性。包含架构对比分析和最佳实践。
---

# LiteLLM-RS Provider 开发指南

## 架构概述

本项目采用**统一错误 + Trait Object**架构，这是经过对比分析后的最佳选择。

### 当前架构层次

```
┌────────────────────────────────────────────────────────┐
│                    网关层 (Gateway)                     │
│  LiteLLMError (core/types/errors/litellm.rs)          │
│  - 顶层错误类型，15 个变体                              │
│  - 处理路由、配置、认证等网关级错误                      │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│                   Provider 层                          │
│  ProviderError (core/providers/unified_provider.rs)   │
│  - 统一 provider 错误，24 个变体                        │
│  - 每个变体包含 provider: &'static str 字段            │
│  - 丰富的工厂方法和上下文信息                           │
└────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────┐
│              各 Provider 实现 (66+)                     │
│  - 已迁移: type Error = ProviderError                  │
│  - 待迁移: type Error = XxxError (独立错误枚举)         │
└────────────────────────────────────────────────────────┘
```

---

## 架构方案对比

### 方案一：Enum Dispatch（编译时多态）

```rust
#[enum_dispatch]
pub enum Provider {
    OpenAI(OpenAIProvider),
    Anthropic(AnthropicProvider),
    // ... 66+ 变体
}
```

| 指标 | 评估 |
|------|------|
| 方法调用延迟 | ~480ns（最快） |
| 二进制体积 | 大（~50MB，66个变体单态化） |
| 编译时间 | 慢（~10分钟） |
| 运行时扩展 | 不支持 |
| 适用场景 | 封闭类型集、高频调用 |

**结论**：不适合 66+ provider 场景，二进制膨胀严重

### 方案二：Trait Object + 统一错误（动态派发）✅ 当前采用

```rust
pub trait LLMProvider: Send + Sync {
    type Error = ProviderError;  // 统一错误类型
    async fn chat_completion(&self, ...) -> Result<ChatResponse, ProviderError>;
}
```

| 指标 | 评估 |
|------|------|
| 方法调用延迟 | ~5,900ns |
| 二进制体积 | 小（~10MB） |
| 编译时间 | 快（~2分钟） |
| 运行时扩展 | 支持 |
| 适用场景 | 多后端系统、API 网关 |

**结论**：最适合本项目，5μs 延迟在 10ms+ 网络延迟中可忽略（0.05%）

### 方案三：混合模式（分层派发）

```rust
// 热路径：前 10 个 provider 用 enum dispatch
enum FastProvider { OpenAI, Anthropic, Azure, ... }
// 冷路径：其余 56 个用 trait object
type ExtendedProvider = Box<dyn LLMProvider>;
```

| 指标 | 评估 |
|------|------|
| 加权延迟 | ~1,500ns（80/20 分布） |
| 复杂度 | 高（两条代码路径） |
| 适用场景 | 极致性能要求 |

**结论**：备选方案，增加复杂度但性能更好

### 方案四：完全单态化

```rust
pub async fn completion<P: LLMProvider>(provider: &P, ...) { ... }
```

| 指标 | 评估 |
|------|------|
| 方法调用延迟 | ~0ns（内联） |
| 二进制体积 | 巨大（泛型代码 66x 拷贝） |
| 编译时间 | 非常慢 |

**结论**：不实用，66+ provider 会导致二进制爆炸

### 方案五：SNAFU 堆栈错误（GreptimeDB 模式）

```rust
#[derive(Debug, Snafu)]
pub enum ProviderError {
    #[snafu(display("Auth failed: {source}"))]
    Authentication { source: Box<dyn Error>, backtrace: Backtrace },
}
```

| 指标 | 评估 |
|------|------|
| 错误上下文 | 丰富（堆栈、回溯） |
| 性能开销 | 堆分配 + 回溯收集 |
| 适用场景 | 复杂系统调试 |

**结论**：可选增强，但当前 `ProviderError` 已足够

---

## 性能对比总结

| 方案 | 调用延迟 | 二进制体积 | 编译时间 | 扩展性 | 推荐度 |
|------|----------|------------|----------|--------|--------|
| Enum Dispatch | ~480ns | 大 | 慢 | 无 | ⭐⭐ |
| **Trait Object** | ~5,900ns | **小** | **快** | **有** | ⭐⭐⭐⭐⭐ |
| 混合模式 | ~1,500ns | 中 | 中 | 有 | ⭐⭐⭐⭐ |
| 完全单态化 | ~0ns | 巨大 | 极慢 | 编译时 | ⭐ |
| SNAFU | ~5,900ns | 小 | 快 | 有 | ⭐⭐⭐⭐ |

### 为什么 5μs 差异不重要

```
典型 LLM API 请求延迟分解：
├── 网络往返：         50-200ms
├── Provider API 处理： 500-5000ms
├── 序列化/反序列化：   0.1-1ms
├── 路由决策：          0.01-0.1ms
└── 派发开销：          0.005ms (5μs)  ← 占比 0.001%-0.01%
```

---

## 统一错误类型详解

### ProviderError 变体

```rust
pub enum ProviderError {
    // 认证与授权
    Authentication { provider, message },

    // 限流与配额
    RateLimit { provider, message, retry_after, rpm_limit, tpm_limit, current_usage },
    QuotaExceeded { provider, message },

    // 模型与请求
    ModelNotFound { provider, model },
    InvalidRequest { provider, message },

    // 网络与可用性
    Network { provider, message },
    Timeout { provider, message },
    ProviderUnavailable { provider, message },

    // 功能支持
    NotSupported { provider, feature },
    NotImplemented { provider, feature },
    FeatureDisabled { provider, feature },

    // 内容与长度
    ContextLengthExceeded { provider, max, actual },
    TokenLimitExceeded { provider, message },
    ContentFiltered { provider, reason, policy_violations, potentially_retryable },

    // 配置与序列化
    Configuration { provider, message },
    Serialization { provider, message },

    // 高级错误
    ApiError { provider, status, message },
    DeploymentError { provider, deployment, message },
    ResponseParsing { provider, message },
    RoutingError { provider, attempted_providers, message },
    TransformationError { provider, from_format, to_format, message },
    Streaming { provider, stream_type, position, last_chunk, message },
    Cancelled { provider, operation_type, cancellation_reason },

    Other { provider, message },
}
```

### 工厂方法使用

```rust
// 基础工厂方法
ProviderError::authentication("openai", "Invalid API key")
ProviderError::rate_limit("anthropic", Some(60))
ProviderError::model_not_found("groq", "llama-invalid")
ProviderError::network("azure", "Connection timeout")

// 增强工厂方法
ProviderError::rate_limit_with_limits("openai", Some(60), Some(100), Some(40000), None)
ProviderError::context_length_exceeded("claude", 100000, 150000)
ProviderError::content_filtered("openai", "Violence detected", Some(vec!["violence"]), Some(false))
ProviderError::streaming_error("fireworks", "chat", Some(42), None, "Connection reset")
```

---

## 添加新 Provider

### 目录结构

```
src/core/providers/my_provider/
├── mod.rs           # 模块导出
├── config.rs        # ProviderConfig 实现
├── provider.rs      # LLMProvider 实现
├── model_info.rs    # 模型定义和能力
└── streaming.rs     # SSE 流解析（可选）
```

### 配置实现

```rust
// config.rs
use crate::core::providers::base::BaseProviderConfig;
use crate::core::traits::config::ProviderConfig;

#[derive(Debug, Clone)]
pub struct MyProviderConfig {
    pub base: BaseProviderConfig,
    pub custom_option: Option<String>,
}

impl Default for MyProviderConfig {
    fn default() -> Self {
        Self {
            base: BaseProviderConfig {
                api_key: std::env::var("MY_PROVIDER_API_KEY").ok(),
                api_base: Some("https://api.myprovider.com/v1".to_string()),
                ..Default::default()
            },
            custom_option: None,
        }
    }
}

impl ProviderConfig for MyProviderConfig {
    fn validate(&self) -> Result<(), String> {
        if self.base.api_key.is_none() {
            return Err("MY_PROVIDER_API_KEY is required".to_string());
        }
        Ok(())
    }

    fn get_api_key(&self) -> Option<String> {
        self.base.api_key.clone()
    }

    fn get_api_base(&self) -> String {
        self.base.api_base.clone()
            .unwrap_or_else(|| "https://api.myprovider.com/v1".to_string())
    }
}
```

### Provider 实现（使用统一错误）

```rust
// provider.rs
use crate::core::providers::unified_provider::ProviderError;
use crate::core::traits::provider::llm_provider::trait_definition::LLMProvider;

const PROVIDER_NAME: &str = "my_provider";

#[derive(Debug, Clone)]
pub struct MyProvider {
    config: MyProviderConfig,
    pool_manager: Arc<GlobalPoolManager>,
    models: Vec<ModelInfo>,
}

impl MyProvider {
    pub fn new(config: MyProviderConfig) -> Result<Self, ProviderError> {
        config.validate()
            .map_err(|e| ProviderError::configuration(PROVIDER_NAME, e))?;

        let pool_manager = Arc::new(
            GlobalPoolManager::new()
                .map_err(|e| ProviderError::configuration(PROVIDER_NAME, e.to_string()))?
        );

        Ok(Self { config, pool_manager, models: get_models() })
    }

    pub fn from_env() -> Result<Self, ProviderError> {
        Self::new(MyProviderConfig::default())
    }
}

#[async_trait]
impl LLMProvider for MyProvider {
    type Config = MyProviderConfig;
    type Error = ProviderError;  // ← 使用统一错误
    type ErrorMapper = crate::core::providers::base::GenericErrorMapper;

    fn name(&self) -> &'static str {
        PROVIDER_NAME
    }

    async fn chat_completion(
        &self,
        request: ChatRequest,
        context: RequestContext,
    ) -> Result<ChatResponse, Self::Error> {
        let api_key = self.config.get_api_key()
            .ok_or_else(|| ProviderError::authentication(PROVIDER_NAME, "API key required"))?;

        let response = self.pool_manager
            .execute_request(&url, HttpMethod::POST, headers, Some(body))
            .await
            .map_err(|e| ProviderError::network(PROVIDER_NAME, e.to_string()))?;

        if !response.status().is_success() {
            return Err(self.map_http_error(response.status().as_u16(), &body));
        }

        // ...
    }
}

impl MyProvider {
    fn map_http_error(&self, status: u16, body: &str) -> ProviderError {
        match status {
            401 => ProviderError::authentication(PROVIDER_NAME, "Invalid API key"),
            404 => ProviderError::model_not_found(PROVIDER_NAME, body),
            429 => ProviderError::rate_limit(PROVIDER_NAME, self.parse_retry_after(body)),
            400 => ProviderError::invalid_request(PROVIDER_NAME, body),
            500..=599 => ProviderError::provider_unavailable(PROVIDER_NAME, body),
            _ => ProviderError::api_error(PROVIDER_NAME, status, body),
        }
    }
}
```

### 模型信息

```rust
// model_info.rs
use crate::core::types::common::{ModelInfo, ProviderCapability};

pub fn get_models() -> Vec<ModelInfo> {
    vec![
        ModelInfo {
            id: "my-model-large".to_string(),
            name: "My Model Large".to_string(),
            provider: "my_provider".to_string(),
            max_context_length: 128000,
            max_output_length: Some(4096),
            supports_streaming: true,
            supports_tools: true,
            supports_multimodal: false,
            input_cost_per_1k_tokens: Some(0.01),
            output_cost_per_1k_tokens: Some(0.03),
            currency: "USD".to_string(),
            capabilities: vec![
                ProviderCapability::ChatCompletion,
                ProviderCapability::ChatCompletionStream,
                ProviderCapability::ToolCalling,
            ],
            ..Default::default()
        },
    ]
}
```

### 注册 Provider

```rust
// src/core/providers/my_provider/mod.rs
mod config;
mod model_info;
mod provider;

pub use config::MyProviderConfig;
pub use provider::MyProvider;
pub use model_info::get_models;

// src/core/providers/mod.rs
pub mod my_provider;
pub use my_provider::{MyProvider, MyProviderConfig};
```

---

## 迁移现有 Provider

### 迁移步骤

1. **删除 error.rs 文件**
2. **修改 provider.rs**：

```rust
// 修改前
use super::error::FireworksError;

impl LLMProvider for FireworksProvider {
    type Error = FireworksError;
    // ...
}

// 创建错误
Err(FireworksError::AuthenticationError("Invalid key".into()))
Err(FireworksError::NetworkError(e.to_string()))
```

```rust
// 修改后
use crate::core::providers::unified_provider::ProviderError;

impl LLMProvider for FireworksProvider {
    type Error = ProviderError;
    // ...
}

// 创建错误
Err(ProviderError::authentication("fireworks", "Invalid key"))
Err(ProviderError::network("fireworks", e.to_string()))
```

### 错误映射对照表

| 旧模式 | 新模式 |
|--------|--------|
| `XxxError::AuthenticationError(msg)` | `ProviderError::authentication("xxx", msg)` |
| `XxxError::RateLimitError { retry_after }` | `ProviderError::rate_limit("xxx", retry_after)` |
| `XxxError::ModelNotFoundError(model)` | `ProviderError::model_not_found("xxx", model)` |
| `XxxError::InvalidRequestError(msg)` | `ProviderError::invalid_request("xxx", msg)` |
| `XxxError::NetworkError(msg)` | `ProviderError::network("xxx", msg)` |
| `XxxError::TimeoutError(msg)` | `ProviderError::timeout("xxx", msg)` |
| `XxxError::ApiError(status, msg)` | `ProviderError::api_error("xxx", status, msg)` |
| `XxxError::NotSupported(feature)` | `ProviderError::not_supported("xxx", feature)` |

### 迁移影响

| 指标 | 迁移前 | 迁移后 | 节省 |
|------|--------|--------|------|
| 错误文件数 | 50 | 1 | **49 文件** |
| 错误代码行数 | ~10,000 | ~740 | **~9,260 行** |
| ProviderErrorTrait 实现 | 50 | 0 | **50 实现** |
| From<XxxError> 实现 | 50 | 0 | **50 实现** |
| 编译时间 | ~5 分钟 | ~2 分钟 | **~60%** |

---

## 检查清单

### 新 Provider 检查清单

```markdown
## 配置
- [ ] 实现 ProviderConfig trait
- [ ] 包含 validate() 方法
- [ ] 支持环境变量
- [ ] 有合理的默认值

## Provider 实现
- [ ] 使用 ProviderError（不是自定义错误类型）
- [ ] 实现所有必需的 LLMProvider 方法
- [ ] HTTP 错误正确映射
- [ ] 支持流式传输（如适用）

## 模型信息
- [ ] 定义支持的模型
- [ ] 包含定价信息
- [ ] 正确指定能力

## 质量
- [ ] 无 unwrap() 调用
- [ ] 错误消息清晰
- [ ] 所有错误包含 provider 名称
- [ ] 单元测试覆盖错误映射

## 注册
- [ ] 添加到 providers/mod.rs
- [ ] 添加到 provider registry
```

### 迁移检查清单

```markdown
## 错误迁移
- [ ] 删除 error.rs 文件
- [ ] 更新 type Error = ProviderError
- [ ] 替换所有 XxxError::Variant 为 ProviderError::factory()
- [ ] 删除 ProviderErrorTrait impl
- [ ] 删除 From<XxxError> impl
- [ ] 更新 ErrorMapper（如需要）

## 测试
- [ ] 所有测试通过
- [ ] 错误类型编译正确
- [ ] HTTP 错误映射正常工作
```

---

## 行业参考

### 类似系统的架构选择

| 项目 | 架构 | 理由 |
|------|------|------|
| **SQLx** | Trait Object + 统一错误 | 多数据库支持 |
| **SeaORM** | Trait Object + 统一错误 | 数据库抽象 |
| **Diesel** | 泛型单态化 | 编译时类型安全 |
| **GreptimeDB** | SNAFU 堆栈错误 | 复杂系统调试 |
| **本项目** | Trait Object + 统一错误 | 66+ provider、API 网关 |

### 性能基准来源

- [enum_dispatch crate](https://docs.rs/enum_dispatch) - 12x 性能提升数据
- [Rust Error Handling Guide 2025](https://markaicode.com/rust-error-handling-2025-guide/)
- [thiserror vs anyhow vs snafu](https://dev.to/leapcell/rust-error-handling-compared-anyhow-vs-thiserror-vs-snafu-2003)

---

## 常见问题

### Q: 为什么不用 enum dispatch？
A: 66 个 provider 会导致：
- 二进制体积 ~50MB（vs ~10MB）
- 编译时间 ~10 分钟（vs ~2 分钟）
- 每次添加 provider 需要重新编译整个枚举

### Q: 5μs 的性能损失重要吗？
A: 不重要。在典型 LLM 请求中（500ms-5000ms），5μs 占比 0.001%-0.01%，完全可忽略。

### Q: 如何处理 provider 特有的错误？
A: 使用 `ProviderError::Other { provider, message }` 或 `ProviderError::api_error(provider, status, message)`，在 message 中包含详细信息。

### Q: 需要添加新的错误变体怎么办？
A: 修改 `unified_provider.rs` 中的 `ProviderError` 枚举，添加新变体和工厂方法。这只需要改一个文件，而不是 50+ 文件。
