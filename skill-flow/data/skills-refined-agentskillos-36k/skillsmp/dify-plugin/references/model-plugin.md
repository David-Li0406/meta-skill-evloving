# Model Plugin Development

Model plugins add AI model providers (LLM, Embedding, TTS, etc.) to Dify.

## File Structure

```
my-model/
├── manifest.yaml                # Plugin manifest
├── main.py                      # Entry point
├── pyproject.toml               # Dependencies (uv)
├── README.md                    # Documentation
├── _assets/
│   ├── icon_s_en.svg            # Small icon
│   └── icon_l_en.png            # Large icon
├── provider/
│   ├── {provider_name}.yaml     # Provider config
│   └── {provider_name}.py       # Provider validation
└── models/
    ├── llm/                     # Large Language Model
    │   ├── _position.yaml       # Model ordering
    │   ├── {model_name}.yaml    # Model definition
    │   └── llm.py               # LLM implementation
    ├── text_embedding/          # Text Embedding
    │   ├── text_embedding.yaml
    │   └── text_embedding.py
    ├── rerank/                  # Reranking
    │   ├── rerank.yaml
    │   └── rerank.py
    ├── tts/                     # Text-to-Speech
    │   ├── tts.yaml
    │   └── tts.py
    ├── speech2text/             # Speech-to-Text
    │   ├── speech2text.yaml
    │   └── speech2text.py
    └── moderation/              # Content Moderation
        ├── moderation.yaml
        └── moderation.py
```

**Note**: You don't need all model types. Create only the subdirectories you need.

## manifest.yaml

```yaml
version: 0.0.1
type: plugin
author: your-name
name: my_model_provider
label:
  en_US: My Model Provider
  zh_Hans: 我的模型提供商
description:
  en_US: Custom model provider
icon: icon.svg

meta:
  version: 0.0.1
  arch: [amd64, arm64]
  runner:
    language: python
    version: "3.12"
    entrypoint: main

plugins:
  models:
    - provider/my_provider.yaml

resource:
  memory: 1048576
  permission:
    tool:
      enabled: true
    model:
      enabled: true
      llm: true
```

## provider.yaml

Note: Use `provider` field (not `identity.name`). No `identity` section.

```yaml
provider: my_provider
label:
  en_US: My Provider
  zh_Hans: 我的提供商
description:
  en_US: Custom LLM provider
background: "#F0F0EB"
icon_small:
  en_US: icon_s_en.svg
icon_large:
  en_US: icon_l_en.png

supported_model_types:
  - llm
  - text-embedding

configurate_methods:
  - predefined-model
  - customizable-model    # Enable custom model names

help:
  title:
    en_US: Get API Key
  url:
    en_US: https://example.com/api-keys

# For customizable-model: per-model credentials
model_credential_schema:
  model:
    label:
      en_US: Model Name
    placeholder:
      en_US: Enter your model name
  credential_form_schemas:
    - variable: api_key
      type: secret-input
      required: true
      label:
        en_US: API Key
      placeholder:
        en_US: Enter your API key

# For predefined-model: provider-level credentials
provider_credential_schema:
  credential_form_schemas:
    - variable: api_key
      type: secret-input
      required: true
      label:
        en_US: API Key
      placeholder:
        en_US: Enter your API key
    - variable: api_base
      type: text-input
      required: false
      label:
        en_US: API Base URL
      placeholder:
        en_US: https://api.example.com

models:
  llm:
    predefined:
      - models/llm/*.yaml
    position: models/llm/_position.yaml

extra:
  python:
    provider_source: provider/my_provider.py
    model_sources:
      - models/llm/llm.py
```

## Model Definition (models/llm/model-name.yaml)

```yaml
model: my-model-v1
label:
  en_US: my-model-v1
model_type: llm

features:
  - agent-thought      # Supports chain-of-thought
  - multi-tool-call    # Supports tool calling
  - stream-tool-call   # Supports streaming tool calls
  - vision             # Supports image input

model_properties:
  mode: chat
  context_size: 128000

parameter_rules:
  - name: temperature
    use_template: temperature
  - name: top_p
    use_template: top_p
  - name: max_tokens
    use_template: max_tokens
    required: true
    default: 4096
    min: 1
    max: 4096
  - name: response_format
    use_template: response_format
  - name: custom_param
    type: int
    label:
      en_US: Custom Parameter
    help:
      en_US: Description of custom parameter
    required: false
    default: 0
    min: 0
    max: 100

pricing:
  input: "1.00"
  output: "3.00"
  unit: "0.000001"
  currency: USD
```

## Model Position (_position.yaml)

```yaml
- my-model-v1
- my-model-v2
- my-model-legacy
```

## Provider Implementation

```python
from dify_plugin import ModelProvider
from dify_plugin.entities.model import ModelType
from dify_plugin.errors.model import CredentialsValidateFailedError
import logging

logger = logging.getLogger(__name__)

class MyProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        """Validate provider credentials"""
        try:
            model_instance = self.get_model_instance(ModelType.LLM)
            model_instance.validate_credentials(
                model="my-model-v1",
                credentials=credentials
            )
        except CredentialsValidateFailedError as ex:
            raise ex
        except Exception as ex:
            logger.exception("Credentials validation failed")
            raise CredentialsValidateFailedError(str(ex))
```

## LLM Implementation

```python
from typing import Generator, Sequence, Optional, Union
from dify_plugin.interfaces.model.large_language_model import LargeLanguageModel
from dify_plugin.entities.model.llm import (
    LLMResult, LLMResultChunk, LLMResultChunkDelta, LLMUsage
)
from dify_plugin.entities.model.message import (
    PromptMessage, AssistantPromptMessage, UserPromptMessage, SystemPromptMessage
)
from dify_plugin.errors.model import (
    CredentialsValidateFailedError,
    InvokeAuthorizationError,
    InvokeBadRequestError,
    InvokeConnectionError,
    InvokeRateLimitError,
    InvokeServerUnavailableError,
)
import httpx

class MyLLM(LargeLanguageModel):
    def _invoke(
        self,
        model: str,
        credentials: dict,
        prompt_messages: Sequence[PromptMessage],
        model_parameters: dict,
        tools: Optional[list] = None,
        stop: Optional[list] = None,
        stream: bool = True,
        user_id: Optional[str] = None,
        callbacks: Optional[list] = None,
    ) -> Union[LLMResult, Generator[LLMResultChunk, None, None]]:
        """Invoke LLM"""
        api_key = credentials.get("api_key")
        api_base = credentials.get("api_base", "https://api.example.com")

        # Convert messages
        messages = self._convert_messages(prompt_messages)

        # Prepare request
        payload = {
            "model": model,
            "messages": messages,
            **model_parameters,
        }

        if tools:
            payload["tools"] = self._convert_tools(tools)
        if stop:
            payload["stop"] = stop

        if stream:
            return self._stream_invoke(api_base, api_key, payload)
        else:
            return self._sync_invoke(api_base, api_key, payload)

    def _stream_invoke(
        self, api_base: str, api_key: str, payload: dict
    ) -> Generator[LLMResultChunk, None, None]:
        """Streaming invocation"""
        payload["stream"] = True

        with httpx.Client() as client:
            with client.stream(
                "POST",
                f"{api_base}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
                timeout=60,
            ) as response:
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        if data.get("choices"):
                            delta = data["choices"][0].get("delta", {})
                            yield LLMResultChunk(
                                model=payload["model"],
                                prompt_messages=[],
                                delta=LLMResultChunkDelta(
                                    index=0,
                                    message=AssistantPromptMessage(
                                        content=delta.get("content", "")
                                    ),
                                ),
                            )

    def _sync_invoke(
        self, api_base: str, api_key: str, payload: dict
    ) -> LLMResult:
        """Synchronous invocation"""
        response = httpx.post(
            f"{api_base}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        return LLMResult(
            model=payload["model"],
            prompt_messages=[],
            message=AssistantPromptMessage(
                content=data["choices"][0]["message"]["content"]
            ),
            usage=LLMUsage(
                prompt_tokens=data["usage"]["prompt_tokens"],
                completion_tokens=data["usage"]["completion_tokens"],
            ),
        )

    def _convert_messages(self, messages: Sequence[PromptMessage]) -> list:
        """Convert Dify messages to API format"""
        result = []
        for msg in messages:
            if isinstance(msg, SystemPromptMessage):
                result.append({"role": "system", "content": msg.content})
            elif isinstance(msg, UserPromptMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AssistantPromptMessage):
                result.append({"role": "assistant", "content": msg.content})
        return result

    def validate_credentials(self, model: str, credentials: dict) -> None:
        """Validate model credentials"""
        try:
            api_key = credentials.get("api_key")
            api_base = credentials.get("api_base", "https://api.example.com")

            response = httpx.get(
                f"{api_base}/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise CredentialsValidateFailedError("Invalid API key")
            raise CredentialsValidateFailedError(str(e))
        except Exception as e:
            raise CredentialsValidateFailedError(str(e))

    def get_num_tokens(
        self,
        model: str,
        credentials: dict,
        prompt_messages: Sequence[PromptMessage],
        tools: Optional[list] = None,
    ) -> int:
        """Estimate token count"""
        # Simple estimation: ~4 chars per token
        total_chars = sum(len(str(msg.content)) for msg in prompt_messages)
        return total_chars // 4
```

## Model Types

| Type Value | Base Class | Purpose |
|------------|------------|---------|
| `llm` | `LargeLanguageModel` | Text generation, chat |
| `text-embedding` | `TextEmbeddingModel` | Text embeddings |
| `tts` | `TTSModel` | Text-to-speech |
| `speech2text` | `Speech2TextModel` | Speech recognition |
| `moderation` | `ModerationModel` | Content moderation |
| `rerank` | `RerankModel` | Document reranking |
| `text2img` | `Text2ImageModel` | Text to image generation |
| `multimodal-embedding` | `MultimodalEmbeddingModel` | Multimodal embeddings |
| `multimodal-rerank` | `MultimodalRerankModel` | Multimodal reranking |

## Configuration Methods

| Method | Description |
|--------|-------------|
| `predefined-model` | Use provider-level credentials for predefined models |
| `customizable-model` | Allow custom model names with per-model credentials |

## Error Handling

```python
from dify_plugin.errors.model import (
    CredentialsValidateFailedError,   # Invalid credentials
    InvokeAuthorizationError,         # Auth failed during invoke
    InvokeBadRequestError,           # Bad request format
    InvokeConnectionError,           # Network error
    InvokeRateLimitError,            # Rate limited
    InvokeServerUnavailableError,    # Server error
)

# Map API errors to Dify errors
def _handle_error(self, status_code: int, message: str):
    if status_code == 401:
        raise InvokeAuthorizationError(message)
    elif status_code == 400:
        raise InvokeBadRequestError(message)
    elif status_code == 429:
        raise InvokeRateLimitError(message)
    elif status_code >= 500:
        raise InvokeServerUnavailableError(message)
```

## Feature Flags

```yaml
features:
  - agent-thought      # Chain-of-thought reasoning
  - multi-tool-call    # Function/tool calling
  - stream-tool-call   # Streaming tool calls
  - vision             # Image understanding
  - document           # Document processing
```

## OpenAI Compatible Provider

For OpenAI-compatible APIs, extend `OAICompatLargeLanguageModel`:

```python
from dify_plugin import OAICompatLargeLanguageModel

class MyOAICompatLLM(OAICompatLargeLanguageModel):
    def _invoke(self, model, credentials, prompt_messages, ...):
        # Override only if customization needed
        # Base class handles OpenAI-compatible API calls
        return super()._invoke(model, credentials, prompt_messages, ...)
```

## Best Practices

1. **Handle streaming** - Implement both sync and stream modes
2. **Token estimation** - Implement `get_num_tokens` for cost calculation
3. **Error mapping** - Map API errors to appropriate Dify error types
4. **Timeout handling** - Use reasonable timeouts (60s for generation)
5. **Validate early** - Check credentials before expensive operations
