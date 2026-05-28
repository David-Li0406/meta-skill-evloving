# Anthropic Claude

**Category**: ai-ml/apis
**Description**: Anthropic's Claude AI models - Advanced language models for analysis, content creation, and conversation

## Package Detection

### NPM
- `@anthropic-ai/sdk`

### PYPI
- `anthropic`

### Related Packages
- `@langchain/anthropic`

## Import Detection

### Python
File extensions: .py

**Pattern**: `from anthropic import|import anthropic`
- Anthropic SDK import
- Example: `from anthropic import Anthropic`

**Pattern**: `Anthropic\(|anthropic\.Anthropic`
- Anthropic client initialization
- Example: `client = Anthropic(api_key=api_key)`

### Javascript
File extensions: .js, .ts

**Pattern**: `from ['"]@anthropic-ai/sdk['"]|require\(['"]@anthropic-ai/sdk['"]\)`
- Anthropic SDK import
- Example: `import Anthropic from '@anthropic-ai/sdk';`

### Common Imports
- `anthropic`
- `@anthropic-ai/sdk`

## Environment Variables

*Anthropic API environment variables*

- `ANTHROPIC_API_KEY`
- `ANTHROPIC_MODEL`
- `CLAUDE_API_KEY`

## Detection Notes

- Claude models via Anthropic API
- Supports Claude 3 family (Opus, Sonnet, Haiku)
- Multi-modal capabilities

## Secrets Detection

### API Keys

#### Anthropic API Key
**Pattern**: `sk-ant-[A-Za-z0-9_-]{90,}`
**Severity**: critical
**Description**: Anthropic API key for Claude models - provides access to Claude API
**Example**: `sk-ant-api03-xxxx...` (95+ characters)
**Environment Variable**: `ANTHROPIC_API_KEY`

### Validation

#### API Documentation
- **API Reference**: https://docs.anthropic.com/en/api/getting-started
- **Authentication**: https://docs.anthropic.com/en/api/getting-started#authentication
- **Rate Limits**: https://docs.anthropic.com/en/api/rate-limits

#### Validation Endpoint
**API**: Anthropic Messages API
**Endpoint**: `https://api.anthropic.com/v1/messages`
**Method**: POST
**Headers**:
- `x-api-key: <your_api_key>`
- `anthropic-version: 2023-06-01`
- `content-type: application/json`
**Purpose**: Validates API key by making a minimal request

```bash
# Validate Anthropic API key
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-haiku-20240307","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}'
```

#### Validation Code (Python)
```python
import anthropic
from anthropic import APIError

def validate_anthropic_key(api_key):
    """Validate Anthropic API key by making a minimal request"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        # Use smallest/cheapest model with minimal tokens
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1,
            messages=[{"role": "user", "content": "hi"}]
        )
        return {'valid': True, 'model': response.model}
    except APIError as e:
        return {'valid': False, 'error': str(e)}
```

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 70% (MEDIUM)
- **Secret Pattern Detection**: 98% (HIGH) - Very distinctive prefix
