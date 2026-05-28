# Mistral AI

**Category**: ai-ml/apis
**Description**: Mistral AI API client library for open-weight and proprietary large language models
**Homepage**: https://mistral.ai

## Package Detection

### NPM
*Mistral AI Node.js client*

- `@mistralai/mistralai`

### PYPI
*Mistral AI Python client*

- `mistralai`

### Related Packages
- `@langchain/mistralai`
- `mistral-common`

## Import Detection

### Javascript
File extensions: .js, .ts

**Pattern**: `import.*from ['"]@mistralai/mistralai['"]`
- Mistral AI client import
- Example: `import MistralClient from '@mistralai/mistralai';`

**Pattern**: `new MistralClient\(`
- Mistral AI client instantiation
- Example: `const client = new MistralClient(process.env.MISTRAL_API_KEY);`

### Python
File extensions: .py

**Pattern**: `^import mistralai`
- Mistral AI Python import
- Example: `import mistralai`

**Pattern**: `^from mistralai import`
- Mistral AI specific imports
- Example: `from mistralai.client import MistralClient`

### Common Imports
- `mistralai`
- `mistralai.client.MistralClient`
- `@mistralai/mistralai`

## Environment Variables

*Mistral AI API configuration*

- `MISTRAL_API_KEY`
- `MISTRAL_MODEL`

## Detection Notes

- Check for Mistral API key in environment (MISTRAL_API_KEY)
- Look for model names (mistral-large, mistral-medium, mistral-small, codestral)
- Common with LangChain and AI frameworks

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
