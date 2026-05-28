# Replicate

**Category**: ai-ml/apis
**Description**: Replicate API for running open-source ML models in the cloud
**Homepage**: https://replicate.com

## Package Detection

### NPM
*Replicate Node.js client*

- `replicate`

### PYPI
*Replicate Python client*

- `replicate`

### Related Packages
- `@langchain/replicate`

## Import Detection

### Javascript
File extensions: .js, .ts

**Pattern**: `import.*Replicate.*from ['"]replicate['"]`
- Replicate client import
- Example: `import Replicate from 'replicate';`

**Pattern**: `new Replicate\(`
- Replicate client instantiation
- Example: `const replicate = new Replicate({ auth: process.env.REPLICATE_API_TOKEN });`

### Python
File extensions: .py

**Pattern**: `^import replicate`
- Replicate Python import
- Example: `import replicate`

**Pattern**: `replicate\.run\(`
- Replicate model execution
- Example: `replicate.run('stability-ai/stable-diffusion')`

### Common Imports
- `replicate`

## Environment Variables

*Replicate API configuration*

- `REPLICATE_API_TOKEN`
- `REPLICATE_API_KEY`

## Detection Notes

- Check for Replicate API key in environment (REPLICATE_API_TOKEN)
- Used for running Stable Diffusion, LLaMA, and other models
- Model references in format owner/model:version

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
