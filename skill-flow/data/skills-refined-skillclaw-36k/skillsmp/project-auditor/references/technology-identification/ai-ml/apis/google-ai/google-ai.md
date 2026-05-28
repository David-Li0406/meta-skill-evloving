# Google AI

**Category**: ai-ml/apis
**Description**: Google's AI platforms including Gemini and Vertex AI for advanced AI capabilities

## Package Detection

### NPM
- `@google/generative-ai`
- `@google-cloud/vertexai`

### PYPI
- `google-generativeai`
- `google-cloud-aiplatform`

### Related Packages
- `@langchain/google-genai`
- `google-auth-library`

## Import Detection

### Python
File extensions: .py

**Pattern**: `from google\.generativeai import|import google\.generativeai`
- Google Generative AI import
- Example: `import google.generativeai as genai`

**Pattern**: `from google\.cloud import aiplatform`
- Vertex AI import
- Example: `from google.cloud import aiplatform`

### Javascript
File extensions: .js, .ts

**Pattern**: `from ['"]@google/generative-ai['"]|require\(['"]@google/generative-ai['"]\)`
- Google Generative AI SDK
- Example: `import { GoogleGenerativeAI } from '@google/generative-ai';`

### Common Imports
- `google.generativeai`
- `@google/generative-ai`
- `google.cloud.aiplatform`

## Environment Variables

*Google AI environment variables*

- `GOOGLE_API_KEY`
- `GOOGLE_APPLICATION_CREDENTIALS`
- `GCP_PROJECT_ID`
- `GEMINI_API_KEY`

## Configuration Files

- `service-account.json`
- `gcp-credentials.json`

## Detection Notes

- Gemini for consumer AI
- Vertex AI for enterprise
- Multi-modal models

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 80% (MEDIUM)
- **API Endpoint Detection**: 75% (MEDIUM)
