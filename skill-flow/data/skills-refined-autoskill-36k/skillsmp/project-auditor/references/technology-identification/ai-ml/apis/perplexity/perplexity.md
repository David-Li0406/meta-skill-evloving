# Perplexity AI

**Category**: ai-ml/apis
**Description**: Perplexity AI API for real-time web search and AI-powered answers
**Homepage**: https://www.perplexity.ai

## Package Detection

### NPM
*Perplexity AI Node.js SDK*

- `perplexity-sdk`

### PYPI
*Perplexity AI Python client*

- `perplexity-client`

### Related Packages
- `@langchain/community`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]perplexity-sdk['"]`
- Type: esm_import

**Pattern**: `require\(['"]perplexity-sdk['"]\)`
- Type: commonjs_require

### Python

**Pattern**: `from\s+perplexity`
- Type: python_import

**Pattern**: `import\s+perplexity`
- Type: python_import

## Environment Variables

*Perplexity AI API key*

*Perplexity AI API key (alternative)*


## Detection Notes

- Uses OpenAI-compatible API format
- Check for api.perplexity.ai endpoint usage
- Look for pplx-api model names

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
