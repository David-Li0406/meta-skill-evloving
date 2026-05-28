# Tool Plugin Development

Tool plugins integrate external APIs into Dify workflows.

## File Structure

```
my-tool/
├── manifest.yaml                # Plugin manifest
├── main.py                      # Entry: plugin = Plugin(DifyPluginEnv())
├── pyproject.toml               # Dependencies (uv)
├── README.md                    # Documentation
├── _assets/
│   └── icon.svg                 # Plugin icon
├── provider/
│   ├── {provider_name}.yaml     # Provider config (credentials)
│   └── {provider_name}.py       # Provider validation logic
└── tools/
    ├── {tool_name}.yaml         # Tool definition (parameters)
    └── {tool_name}.py           # Tool implementation (invoke method)
```

## manifest.yaml

```yaml
version: 0.0.1
type: plugin
author: your-name
name: my_tool
label:
  en_US: My Tool
  zh_Hans: 我的工具
description:
  en_US: Tool description
  zh_Hans: 工具描述
icon: icon.svg

meta:
  version: 0.0.1
  arch: [amd64, arm64]
  runner:
    language: python
    version: "3.12"
    entrypoint: main

plugins:
  tools:
    - provider/my_provider.yaml

resource:
  memory: 1048576
  permission:
    tool:
      enabled: true
    model:
      enabled: false  # Set true only if using LLM
      llm: false

tags:
  - utilities  # Valid: search, image, videos, weather, finance, design, travel,
               # social, news, medical, productivity, education, business,
               # entertainment, utilities, agent, rag, trigger, other
```

## provider.yaml

```yaml
identity:
  author: your-name
  name: my_provider
  label:
    en_US: My Provider
    zh_Hans: 我的提供商
  description:
    en_US: Provider description
  icon: icon.svg
  tags:
    - utilities

credentials_for_provider:
  api_key:
    type: secret-input
    required: true
    label:
      en_US: API Key
    placeholder:
      en_US: Enter your API key
    help:
      en_US: Get your API key from dashboard
    url: https://example.com/api-keys

tools:
  - tools/search.yaml
  - tools/create.yaml

extra:
  python:
    source: provider/my_provider.py
```

## tool.yaml

```yaml
identity:
  name: search
  author: your-name
  label:
    en_US: Search
    zh_Hans: 搜索

description:
  human:
    en_US: Search for items
    zh_Hans: 搜索项目
  llm: Search for items by query. Returns list of matching results.

parameters:
  - name: query
    type: string
    required: true
    form: llm           # LLM fills this parameter
    label:
      en_US: Query
    human_description:
      en_US: Search query
    llm_description: The search query to execute

  - name: limit
    type: number
    required: false
    form: form          # User fills in UI
    default: 10
    min: 1
    max: 100
    label:
      en_US: Limit

  - name: category
    type: select
    required: false
    form: form
    options:
      - value: all
        label:
          en_US: All
      - value: products
        label:
          en_US: Products

extra:
  python:
    source: tools/search.py
```

## Tool Implementation

```python
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
import httpx

class SearchTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        # Get parameters
        query = tool_parameters.get("query", "")
        limit = tool_parameters.get("limit", 10)

        if not query:
            yield self.create_text_message("Query is required")
            return

        # Get credentials
        api_key = self.runtime.credentials["api_key"]

        # Call API
        try:
            result = self._call_api(query, limit, api_key)
            yield self.create_json_message(result)
        except httpx.HTTPError as e:
            yield self.create_text_message(f"API error: {e}")

    def _call_api(self, query: str, limit: int, api_key: str) -> dict:
        response = httpx.get(
            "https://api.example.com/search",
            params={"q": query, "limit": limit},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
```

## Provider Validation (Optional)

```python
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

class MyProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        api_key = credentials.get("api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError("API Key required")

        # Test API
        try:
            response = httpx.get(
                "https://api.example.com/me",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise ToolProviderCredentialValidationError(f"Invalid API key: {e}")
```

## Parameter Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text input | query, name |
| `number` | Numeric | limit, count |
| `boolean` | True/false | enabled |
| `select` | Dropdown | category |
| `secret-input` | Encrypted | api_key |
| `file` | Single file | document |
| `files` | Multiple files | images |
| `app-selector` | Dify app picker | app reference |
| `model-selector` | Model picker | LLM selection |
| `dynamic-select` | Fetches options dynamically | repository list |
| `array` | Array of values | list of items |
| `object` | Nested object | complex config |
| `checkbox` | Multiple selection | event types |
| `any` | Flexible type | context data |

### Parameter Form Types

| Form | Description |
|------|-------------|
| `schema` | Defined by JSON schema |
| `form` | User fills in UI form |
| `llm` | LLM fills automatically |

## Message Types

### Response Type Reference

| Type | Method | Use Case |
|------|--------|----------|
| `text` | `create_text_message` | Plain text content |
| `json` | `create_json_message` | Structured data (preferred) |
| `link` | `create_link_message` | URL references |
| `blob` | `create_blob_message` | Binary data (images, files) |
| `blob_chunk` | (streaming) | Large file streaming transfer |
| `image` | `create_image_message` | Image data |
| `image_link` | (via json) | Image URL reference |
| `file` | `create_file_message` | File reference |
| `variable` | `create_variable_message` | Workflow variables |
| `log` | `create_log_message` | Execution logs |

### Usage Examples

```python
# Text response
yield self.create_text_message(text="Hello")

# JSON response (preferred for structured data)
yield self.create_json_message(json={"key": "value", "items": [1, 2, 3]})

# Link
yield self.create_link_message(link="https://example.com")

# Binary data (images, files)
yield self.create_blob_message(
    blob=image_bytes,
    meta={"mime_type": "image/png", "file_name": "result.png"}
)
```

### Blob Transmission Limits

For large file transfers using `blob_chunk`:

| Limit | Value |
|-------|-------|
| Single chunk max | 8 KB |
| Single file max | 15 MB |

Blob chunk message fields:
- `id`: Unique identifier
- `blob`: Base64 encoded data chunk
- `total_length`: Total file length
- `end`: Boolean indicating last chunk

## Using LLM in Tools

Only if `permission.model.enabled: true` in manifest.yaml:

```python
def _invoke(self, tool_parameters: dict[str, Any]):
    raw_data = self._fetch_data()

    # Summarize with LLM
    summary = self.session.model.summary.invoke(
        text=raw_data,
        instruction="Summarize the key points"
    )
    yield self.create_text_message(summary)
```

## Error Handling

**Important**: Execution status is determined by whether an exception is raised, NOT by message content.

| Code Behavior | Execution Status |
|---|---|
| `yield self.create_text_message("Error...")` + normal return | SUCCESS |
| `raise Exception("Error...")` | FAILURE |

```python
from dify_plugin.errors.tool import (
    ToolProviderCredentialValidationError,
    ToolInvokeError,
)

# In provider validation
raise ToolProviderCredentialValidationError("Invalid credentials")

# In tool invocation - use exceptions for real errors
raise ToolInvokeError("Failed to process request")
raise ValueError("Resource not found")  # Also works

# ❌ Wrong - this still shows SUCCESS status
yield self.create_text_message("Error: Resource not found")

# ✅ Correct - this shows FAILURE status
raise ValueError("Resource not found")
```

See [best-practices.md](best-practices.md) for detailed error handling guidelines.

## Best Practices

1. **Return JSON** - Use `create_json_message` for structured data
2. **Handle errors** - Catch `httpx.HTTPError`, return helpful messages
3. **Set timeouts** - Always use `timeout=30` for HTTP calls
4. **Validate early** - Check required parameters before API calls
5. **Avoid LLM abuse** - Don't use LLM just for formatting
