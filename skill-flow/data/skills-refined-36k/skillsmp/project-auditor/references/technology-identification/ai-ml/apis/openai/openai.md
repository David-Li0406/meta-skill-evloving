# OpenAI

**Category**: ai-ml/apis
**Description**: OpenAI API client library for GPT-4, ChatGPT, DALL-E, and other AI models
**Homepage**: https://openai.com

## Package Detection

### NPM
*OpenAI Node.js client*

- `openai`

### PYPI
*OpenAI Python client*

- `openai`

### Related Packages
- `@langchain/openai`
- `openai-edge`
- `gpt-tokenizer`
- `tiktoken`

## Import Detection

### Javascript
File extensions: .js, .ts

**Pattern**: `import.*from ['"]openai['"]`
- OpenAI client import
- Example: `import OpenAI from 'openai';`

**Pattern**: `new OpenAI\(`
- OpenAI client instantiation
- Example: `const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });`

### Python
File extensions: .py

**Pattern**: `^import openai`
- OpenAI Python import
- Example: `import openai`

**Pattern**: `^from openai import`
- OpenAI specific imports
- Example: `from openai import OpenAI`

### Common Imports
- `openai`
- `openai.OpenAI`
- `openai.ChatCompletion`

## Environment Variables

*OpenAI API configuration*

- `OPENAI_API_KEY`
- `OPENAI_ORG_ID`
- `OPENAI_MODEL`

## Detection Notes

- Check for OpenAI API key in environment (OPENAI_API_KEY)
- Look for GPT model names in code (gpt-4, gpt-3.5-turbo)
- Common with LangChain and AI frameworks

## Secrets Detection

### API Keys

#### OpenAI API Key
**Pattern**: `sk-[A-Za-z0-9]{48}`
**Severity**: critical
**Description**: OpenAI API key - provides access to GPT, DALL-E, and other OpenAI models
**Example**: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
**Environment Variable**: `OPENAI_API_KEY`

#### OpenAI Project API Key (New Format)
**Pattern**: `sk-proj-[A-Za-z0-9_-]{100,}`
**Severity**: critical
**Description**: OpenAI project-scoped API key (newer format)
**Example**: `sk-proj-xxxx...` (100+ characters)

#### OpenAI Organization ID
**Pattern**: `org-[A-Za-z0-9]{24}`
**Severity**: medium
**Description**: OpenAI organization identifier (not a secret but sensitive)
**Example**: `org-xxxxxxxxxxxxxxxxxxxxxxxxx`

### Validation

#### API Documentation
- **API Reference**: https://platform.openai.com/docs/api-reference
- **Authentication**: https://platform.openai.com/docs/api-reference/authentication
- **Rate Limits**: https://platform.openai.com/docs/guides/rate-limits

#### Validation Endpoint
**API**: OpenAI Models List
**Endpoint**: `https://api.openai.com/v1/models`
**Method**: GET
**Headers**:
- `Authorization: Bearer <your_api_key>`
**Purpose**: Validates API key without incurring costs

```bash
# Validate OpenAI API key (free endpoint)
curl -s https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | head -c 100
```

#### Validation Code (Python)
```python
from openai import OpenAI, AuthenticationError

def validate_openai_key(api_key):
    """Validate OpenAI API key by listing models (free endpoint)"""
    try:
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        return {'valid': True, 'models_count': len(list(models))}
    except AuthenticationError as e:
        return {'valid': False, 'error': str(e)}
```

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
- **Secret Pattern Detection**: 95% (HIGH) - Distinctive `sk-` prefix
