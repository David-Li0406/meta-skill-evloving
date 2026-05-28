# Kaizen Configuration Patterns

Complete guide to domain configs, BaseAgentConfig, and auto-conversion patterns in Kaizen.

## Core Concept: Domain Config Auto-Extraction

**Key Innovation**: Use domain-specific configs, BaseAgent auto-converts to BaseAgentConfig.

**Benefits:**
- ✅ No boilerplate BaseAgentConfig creation
- ✅ Keep domain-specific fields separate
- ✅ Type-safe configuration
- ✅ Cleaner, more maintainable code

## Pattern: Domain Config (Recommended)

```python
from kaizen.core.base_agent import BaseAgent
from dataclasses import dataclass

# Step 1: Define domain configuration
@dataclass
class QAConfig:
    """
    Domain-specific configuration for Q&A agents.
    NOT BaseAgentConfig - BaseAgent extracts what it needs.
    """
    # BaseAgent extracts these automatically:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000

    # Domain-specific fields (BaseAgent ignores these):
    enable_fact_checking: bool = True
    min_confidence_threshold: float = 0.7
    max_retries: int = 3

# Step 2: Use directly with BaseAgent
class QAAgent(BaseAgent):
    def __init__(self, config: QAConfig):
        # BaseAgent auto-extracts: llm_provider, model, temperature, max_tokens
        super().__init__(config=config, signature=QASignature())
        self.qa_config = config  # Keep reference for domain fields

    def ask(self, question: str) -> dict:
        result = self.run(question=question)

        # Use domain-specific config
        if result.get("confidence", 0) < self.qa_config.min_confidence_threshold:
            if self.qa_config.enable_fact_checking:
                result = self._recheck_with_facts(result)

        return result
```

## What BaseAgent Auto-Extracts

BaseAgent looks for these fields in your domain config:

```python
# Core fields (extracted automatically)
llm_provider: str     # "openai", "anthropic", "ollama", "mock"
model: str            # Model name (e.g., "gpt-4")
temperature: float    # Sampling temperature (0.0-1.0)
max_tokens: int       # Maximum tokens to generate

# Optional fields (extracted if present)
timeout: int          # Request timeout in seconds
retry_attempts: int   # Number of retries on failure
max_turns: int        # Enable BufferMemory if > 0
provider_config: dict # Provider-specific configuration
```

**All other fields** are ignored by BaseAgent and available for your domain logic.

## Configuration Patterns

### 1. Basic Configuration

```python
@dataclass
class BasicConfig:
    """Minimal configuration for simple agents."""
    llm_provider: str = "openai"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7

agent = SimpleQAAgent(BasicConfig())
```

### 2. Production Configuration

```python
@dataclass
class ProductionConfig:
    """Production-ready configuration with all features."""
    # Core LLM settings
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.3  # Lower for consistency
    max_tokens: int = 2000

    # Performance settings
    timeout: int = 60
    retry_attempts: int = 3

    # Memory settings
    max_turns: int = 50  # Enable BufferMemory with limit

    # Domain settings
    enable_logging: bool = True
    log_level: str = "INFO"
    enable_metrics: bool = True
```

### 3. Development Configuration

```python
@dataclass
class DevConfig:
    """Development configuration with debugging."""
    llm_provider: str = "mock"  # No API calls
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 500

    # Debug settings
    debug: bool = True
    verbose: bool = True
    save_prompts: bool = True
```

### 4. Environment-Based Configuration

```python
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class EnvConfig:
    """Configuration from environment variables."""
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    model: str = os.getenv("LLM_MODEL", "gpt-4")
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "1000"))

    # API keys loaded automatically by providers
    # OPENAI_API_KEY, ANTHROPIC_API_KEY from .env
```

### 5. Multi-Provider Configuration

```python
@dataclass
class MultiProviderConfig:
    """Support multiple LLM providers."""
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000

    # Fallback provider
    fallback_provider: str = "anthropic"
    fallback_model: str = "claude-3-opus-20240229"

    # Provider-specific settings
    provider_config: dict = None

    def __post_init__(self):
        if self.provider_config is None:
            self.provider_config = {
                "openai": {"api_version": "2024-01"},
                "anthropic": {"max_retries": 3}
            }
```

## Memory Configuration

### Enable Memory with max_turns

```python
@dataclass
class MemoryEnabledConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    max_turns: int = 10  # Enable BufferMemory, keep last 10 turns

agent = MemoryAgent(MemoryEnabledConfig())

# Use session_id for memory continuity
result1 = agent.ask("My name is Alice", session_id="user123")
result2 = agent.ask("What's my name?", session_id="user123")
# Returns: "Your name is Alice"
```

### Disable Memory

```python
@dataclass
class NoMemoryConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    max_turns: int = 0  # Disable memory (default)

agent = StatelessAgent(NoMemoryConfig())
```

## Provider-Specific Configuration

### OpenAI Configuration

```python
@dataclass
class OpenAIConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000

    # OpenAI-specific settings
    provider_config: dict = None

    def __post_init__(self):
        self.provider_config = {
            "api_version": "2024-01-01",
            "organization": "org-xyz",
            "seed": 42,  # Reproducibility
            "top_p": 0.9
        }
```

### Anthropic Configuration

```python
@dataclass
class AnthropicConfig:
    llm_provider: str = "anthropic"
    model: str = "claude-3-opus-20240229"
    temperature: float = 0.7
    max_tokens: int = 2000

    provider_config: dict = None

    def __post_init__(self):
        self.provider_config = {
            "api_version": "2023-06-01",
            "max_retries": 3
        }
```

### Ollama Configuration (Local)

```python
@dataclass
class OllamaConfig:
    llm_provider: str = "ollama"
    model: str = "llama2"
    temperature: float = 0.7
    max_tokens: int = 1000

    provider_config: dict = None

    def __post_init__(self):
        self.provider_config = {
            "base_url": "http://localhost:11434",
            "num_gpu": 1
        }
```

### Azure AI Foundry Configuration (v0.7.1)

```python
@dataclass
class AzureConfig:
    """Azure AI Foundry configuration.

    Prerequisites:
        export AZURE_AI_INFERENCE_ENDPOINT="https://your-endpoint.azure.com"
        export AZURE_AI_INFERENCE_API_KEY="your-key"
    """
    llm_provider: str = "azure"
    model: str = "gpt-4o"  # Or any deployed model
    temperature: float = 0.7
    max_tokens: int = 1000

    provider_config: dict = None

    def __post_init__(self):
        self.provider_config = {
            "api_version": "2024-02-01"
        }
```

**Features**: Chat completions, vision/multi-modal support, embeddings, tool calling, async support.

### Docker Model Runner Configuration (v0.7.1)

```python
@dataclass
class DockerConfig:
    """Docker Model Runner configuration (FREE local inference).

    Prerequisites:
        1. Docker Desktop 4.40+ with Model Runner enabled
        2. Enable TCP access: docker desktop enable model-runner --tcp 12434
        3. Pull model: docker model pull ai/llama3.2
    """
    llm_provider: str = "docker"
    model: str = "ai/llama3.2"  # Or ai/qwen3, ai/gemma3, ai/mxbai-embed-large
    temperature: float = 0.7
    max_tokens: int = 1000

    provider_config: dict = None

    def __post_init__(self):
        self.provider_config = {
            "base_url": "http://localhost:12434/engines/llama.cpp/v1"
        }
```

**Features**: OpenAI-compatible API, GPU acceleration (Metal/CUDA/Vulkan), embeddings, model-dependent tool calling.

**Tool-Capable Models**: `ai/qwen3`, `ai/llama3.3`, `ai/gemma3` (check with `provider.supports_tools(model)`).

### Google Gemini Configuration (v0.8.2)

```python
@dataclass
class GoogleGeminiConfig:
    """Google Gemini configuration (Cloud, multimodal).

    Prerequisites:
        export GOOGLE_API_KEY="your-api-key"
        # Or: export GEMINI_API_KEY="your-api-key"

    Install dependency:
        pip install kailash-kaizen[google]
    """
    llm_provider: str = "google"  # Or "gemini" (alias)
    model: str = "gemini-2.0-flash"  # Fast, efficient model
    temperature: float = 0.7
    max_tokens: int = 1000

    provider_config: dict = None

    def __post_init__(self):
        self.provider_config = {
            "top_p": 0.9,
            "top_k": 40
        }
```

**Available Models**:
- Chat: `gemini-2.0-flash`, `gemini-1.5-pro`, `gemini-1.5-flash`
- Embeddings: `text-embedding-004` (768 dimensions)

**Features**: Chat completions, vision/multimodal support, embeddings, tool calling, async support.

**Direct Provider Usage**:
```python
from kaizen.nodes.ai import GoogleGeminiProvider

provider = GoogleGeminiProvider()

# Chat
response = provider.chat(
    messages=[{"role": "user", "content": "Hello!"}],
    model="gemini-2.0-flash"
)

# Vision (multimodal)
import base64
with open("image.png", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

response = provider.chat(
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {"type": "image", "base64": image_b64, "media_type": "image/png"}
        ]
    }],
    model="gemini-2.0-flash"
)

# Embeddings
embeddings = provider.embed(
    texts=["Hello world"],
    model="text-embedding-004"
)
# Returns: [[0.01, -0.02, ...]] (768-dim vectors)

# Async
response = await provider.chat_async(messages=[...], model="gemini-2.0-flash")
embeddings = await provider.embed_async(texts=[...], model="text-embedding-004")
```

## Configuration Validation

### With Validation Rules

```python
from typing import Optional

@dataclass
class ValidatedConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 30

    def __post_init__(self):
        # Validate temperature
        if not 0.0 <= self.temperature <= 1.0:
            raise ValueError("temperature must be between 0.0 and 1.0")

        # Validate max_tokens
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")

        # Validate timeout
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")

        # Validate provider
        valid_providers = ["openai", "azure", "anthropic", "google", "gemini", "ollama", "docker", "cohere", "huggingface", "mock"]
        if self.llm_provider not in valid_providers:
            raise ValueError(f"Invalid provider: {self.llm_provider}")
```

## Configuration Hierarchy

### Base + Specialized Configs

```python
@dataclass
class BaseConfig:
    """Base configuration shared across agents."""
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000

@dataclass
class ResearchConfig(BaseConfig):
    """Research agent specific configuration."""
    enable_web_search: bool = True
    max_sources: int = 5
    citation_style: str = "APA"

@dataclass
class CodeGenConfig(BaseConfig):
    """Code generation specific configuration."""
    target_language: str = "python"
    style_guide: str = "PEP8"
    include_tests: bool = True
```

## Anti-Patterns (DON'T DO THIS)

### ❌ Manual BaseAgentConfig Creation

```python
# WRONG - Don't do this!
from kaizen.core.config import BaseAgentConfig

agent_config = BaseAgentConfig(
    llm_provider=config.llm_provider,
    model=config.model,
    temperature=config.temperature,
    max_tokens=config.max_tokens
)
super().__init__(config=agent_config, ...)
```

### ✅ Use Auto-Conversion Instead

```python
# RIGHT - Let BaseAgent do the work
super().__init__(config=config, ...)
```

## Configuration Testing

```python
def test_config_auto_extraction():
    """Test that domain config is properly extracted."""
    @dataclass
    class TestConfig:
        llm_provider: str = "mock"
        model: str = "test-model"
        temperature: float = 0.5
        custom_field: str = "custom_value"  # Ignored by BaseAgent

    agent = TestAgent(TestConfig())

    # BaseAgent extracted core fields
    assert agent.config.llm_provider == "mock"
    assert agent.config.model == "test-model"
    assert agent.config.temperature == 0.5

    # Domain config still accessible
    assert agent.domain_config.custom_field == "custom_value"
```

## CRITICAL RULES

**ALWAYS:**
- ✅ Use domain configs (e.g., `QAConfig`, `RAGConfig`)
- ✅ Let BaseAgent auto-extract core fields
- ✅ Keep domain-specific fields in domain config
- ✅ Load `.env` with `load_dotenv()` before creating configs

**NEVER:**
- ❌ Create BaseAgentConfig manually
- ❌ Mix BaseAgent fields with domain fields in BaseAgentConfig
- ❌ Skip config validation for production code
- ❌ Hardcode API keys in config (use environment variables)

## Related Skills

- **kaizen-baseagent-quick** - Using configs with BaseAgent
- **kaizen-ux-helpers** - Config convenience methods
- **kaizen-agent-execution** - Config-based execution patterns

## References

- **Source**: `apps/kailash-kaizen/src/kaizen/core/config.py`
- **Examples**: All agents in `apps/kailash-kaizen/examples/`
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 249-267
