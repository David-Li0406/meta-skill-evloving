# API Overview

RESTful API at `https://api.anthropic.com` providing programmatic access to Claude models.

## Available APIs

**General Availability:**

| API | Endpoint | Purpose |
|-----|----------|---------|
| Messages | `POST /v1/messages` | Conversational interactions |
| Message Batches | `POST /v1/messages/batches` | Async bulk processing (50% cost reduction) |
| Token Counting | `POST /v1/messages/count_tokens` | Count tokens before sending |
| Models | `GET /v1/models` | List available models |

**Beta:**

| API | Endpoint | Purpose |
|-----|----------|---------|
| Files | `POST /v1/files`, `GET /v1/files` | Upload/manage files across calls |
| Skills | `POST /v1/skills`, `GET /v1/skills` | Custom agent skills |

Access beta features with `anthropic-beta` header.

## Authentication

Required headers for all requests:

| Header | Value | Required |
|--------|-------|----------|
| `x-api-key` | API key from Console | Yes |
| `anthropic-version` | API version (e.g., `2023-06-01`) | Yes |
| `content-type` | `application/json` | Yes |

SDKs handle headers automatically.

**Get API keys:** [Console](https://platform.claude.com) > [Account Settings](https://platform.claude.com/settings/keys)

## Request Size Limits

| Endpoint | Maximum Size |
|----------|--------------|
| Standard (Messages, Token Counting) | 32 MB |
| Batch API | 256 MB |
| Files API | 500 MB |

Exceeding limits returns `413 request_too_large`.

## Response Headers

Every response includes:

- `request-id`: Globally unique request identifier
- `anthropic-organization-id`: Organization ID for the API key

## Rate Limits

Organized into usage tiers that increase automatically:

- **Spend limits**: Maximum monthly cost
- **Rate limits**: Requests per minute (RPM) and tokens per minute (TPM)

View limits: [Console](https://platform.claude.com/settings/limits)

For Priority Tier (enhanced service with committed spend), contact sales.

## Third-Party Platforms

Claude is available through partner platforms with integrated billing and IAM:

| Platform | Provider | Trade-offs |
|----------|----------|------------|
| Amazon Bedrock | AWS | Integrated with AWS billing/IAM, may have feature delays |
| Vertex AI | Google Cloud | Integrated with GCP billing/IAM, may have feature delays |
| Azure AI | Microsoft Azure | Integrated with Azure billing/IAM, may have feature delays |

**Use Claude API for:** Latest features, direct Anthropic support
**Use third-party for:** Existing cloud commitments, compliance requirements, consolidated billing

## Basic Example (curl)

```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello, Claude"}
    ]
  }'
```

**Response:**

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello! How can I assist you today?"
    }
  ],
  "model": "claude-sonnet-4-5-20250929",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 12,
    "output_tokens": 8
  }
}
```
