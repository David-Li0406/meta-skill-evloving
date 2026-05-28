# Cohere

**Category**: ai-ml/apis
**Description**: Enterprise AI platform for language understanding, generation, and search

## Package Detection

### NPM
- `cohere-ai`

### PYPI
- `cohere`

### Related Packages
- `@langchain/cohere`

## Import Detection

### Python
File extensions: .py

**Pattern**: `import cohere|from cohere import`
- Cohere SDK import
- Example: `import cohere`

**Pattern**: `cohere\.Client\(`
- Cohere client initialization
- Example: `co = cohere.Client(api_key)`

### Javascript
File extensions: .js, .ts

**Pattern**: `from ['"]cohere-ai['"]|require\(['"]cohere-ai['"]\)`
- Cohere SDK import
- Example: `import { CohereClient } from 'cohere-ai';`

### Common Imports
- `cohere`
- `cohere-ai`

## Environment Variables

*Cohere API environment variables*

- `COHERE_API_KEY`
- `CO_API_KEY`

## Detection Notes

- Cohere for enterprise AI
- Command models for generation
- Embed models for search/RAG

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 75% (MEDIUM)
