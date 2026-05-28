# Together AI

**Category**: ai-ml/apis
**Description**: Together AI platform for running and fine-tuning open-source LLMs
**Homepage**: https://www.together.ai

## Package Detection

### NPM
*Together AI Node.js client*

- `together-ai`

### PYPI
*Together AI Python client*

- `together`

### Related Packages
- `@langchain/community`
- `openai`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]together-ai['"]`
- Type: esm_import

**Pattern**: `require\(['"]together-ai['"]\)`
- Type: commonjs_require

### Python

**Pattern**: `^from together import`
- Type: python_import

**Pattern**: `^import together$`
- Type: python_import

**Pattern**: `^from together.client import`
- Type: python_import

## Environment Variables

*Together AI API key*

*Together AI API key (alternative)*


## Detection Notes

- OpenAI-compatible API format
- Check for api.together.xyz endpoint
- Hosts open-source models like Llama, Mistral

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
