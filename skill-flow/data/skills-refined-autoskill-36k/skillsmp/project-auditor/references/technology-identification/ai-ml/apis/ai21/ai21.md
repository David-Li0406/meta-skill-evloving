# AI21 Labs

**Category**: ai-ml/apis
**Description**: AI21 Labs API client for Jurassic-2 and other language models
**Homepage**: https://www.ai21.com

## Package Detection

### PYPI
*AI21 Labs Python client*

- `ai21`

### Related Packages
- `@langchain/ai21`
- `ai21-tokenizer`

## Import Detection

### Python
File extensions: .py

**Pattern**: `^import ai21`
- AI21 Labs Python import
- Example: `import ai21`

**Pattern**: `^from ai21 import`
- AI21 Labs specific imports
- Example: `from ai21 import AI21Client`

### Common Imports
- `ai21`
- `ai21.AI21Client`

## Environment Variables

*AI21 Labs API configuration*

- `AI21_API_KEY`
- `AI21_MODEL`

## Detection Notes

- Check for AI21 API key in environment (AI21_API_KEY)
- Look for model names (j2-ultra, j2-mid, j2-light)
- Used for text generation and comprehension

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
