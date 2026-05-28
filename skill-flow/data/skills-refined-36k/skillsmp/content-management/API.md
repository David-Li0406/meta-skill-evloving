# API Reference - Content Management

Documentation des endpoints API et webhooks pour le skill content-management.

## Base URL

```
Production: https://api.example.com/content/v1
Staging:    https://api-staging.example.com/content/v1
```

## Authentication

```yaml
authentication:
  type: Bearer Token
  header: Authorization
  format: "Bearer {access_token}"

  # OAuth2 endpoints
  token_url: /oauth/token
  refresh_url: /oauth/refresh

  # API Key (for webhooks)
  api_key_header: X-API-Key
```

---

## Content Endpoints

### Create Content

```http
POST /content
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "Guide SEO 2025",
  "type": "article",
  "status": "draft",
  "locale": "fr-FR",
  "body": "...",
  "metadata": {
    "author": "user-123",
    "category": "marketing",
    "tags": ["seo", "guide", "2025"]
  }
}
```

**Response: 201 Created**
```json
{
  "id": "CONTENT-2025-001234",
  "title": "Guide SEO 2025",
  "status": "draft",
  "created_at": "2025-01-10T14:00:00Z",
  "urls": {
    "self": "/content/CONTENT-2025-001234",
    "edit": "/content/CONTENT-2025-001234/edit",
    "preview": "/preview/CONTENT-2025-001234"
  }
}
```

### Get Content

```http
GET /content/{content_id}
Authorization: Bearer {token}
Accept-Language: fr-FR
```

**Response: 200 OK**
```json
{
  "id": "CONTENT-2025-001234",
  "title": "Guide SEO 2025",
  "type": "article",
  "status": "published",
  "locale": "fr-FR",
  "body": "...",
  "metadata": {
    "author": "user-123",
    "created_at": "2025-01-10T14:00:00Z",
    "updated_at": "2025-01-10T16:30:00Z",
    "published_at": "2025-01-10T18:00:00Z"
  },
  "seo": {
    "title": "Guide SEO 2025 : Techniques et Bonnes Pratiques",
    "description": "Découvrez les meilleures pratiques SEO...",
    "canonical_url": "/guides/seo-2025"
  },
  "translations": {
    "en-US": "/content/CONTENT-2025-001234-en",
    "de-DE": "/content/CONTENT-2025-001234-de"
  }
}
```

### Update Content

```http
PATCH /content/{content_id}
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "Guide SEO 2025 - Mise à jour",
  "body": "..."
}
```

### Publish Content

```http
POST /content/{content_id}/publish
Authorization: Bearer {token}

{
  "schedule": "2025-01-15T10:00:00Z",  // Optional
  "channels": ["website", "rss"]
}
```

### List Content

```http
GET /content?status=published&type=article&limit=20&offset=0
Authorization: Bearer {token}
```

**Query Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| status | string | draft, review, published, archived |
| type | string | article, page, email, social |
| locale | string | fr-FR, en-US, etc. |
| author | string | User ID |
| tag | string | Filter by tag |
| limit | int | Max results (default: 20, max: 100) |
| offset | int | Pagination offset |
| sort | string | created_at, updated_at, title |
| order | string | asc, desc |

---

## Asset Endpoints

### Upload Asset

```http
POST /assets
Content-Type: multipart/form-data
Authorization: Bearer {token}

file: (binary)
alt_text: "Description de l'image"
folder: "/images/blog/2025/"
tags: ["hero", "marketing"]
```

**Response: 201 Created**
```json
{
  "id": "ASSET-2025-001234",
  "filename": "hero-banner.webp",
  "mime_type": "image/webp",
  "size": 156000,
  "dimensions": {
    "width": 1600,
    "height": 900
  },
  "urls": {
    "original": "https://cdn.example.com/.../hero-banner.webp",
    "thumbnail": "https://cdn.example.com/.../hero-banner-thumb.webp",
    "srcset": {
      "400w": "https://cdn.example.com/.../hero-banner-400w.webp",
      "800w": "https://cdn.example.com/.../hero-banner-800w.webp",
      "1200w": "https://cdn.example.com/.../hero-banner-1200w.webp"
    }
  },
  "processing": {
    "status": "completed",
    "compression_ratio": 0.78
  }
}
```

### Get Asset

```http
GET /assets/{asset_id}
Authorization: Bearer {token}
```

### Delete Asset

```http
DELETE /assets/{asset_id}
Authorization: Bearer {token}
```

### Batch Upload

```http
POST /assets/batch
Content-Type: multipart/form-data
Authorization: Bearer {token}

files[]: (binary)
files[]: (binary)
folder: "/images/batch/"
```

**Response: 202 Accepted**
```json
{
  "batch_id": "BATCH-2025-001234",
  "status": "processing",
  "total": 10,
  "progress_url": "/assets/batch/BATCH-2025-001234/status"
}
```

---

## Translation Endpoints

### Request Translation

```http
POST /content/{content_id}/translate
Authorization: Bearer {token}

{
  "target_locales": ["en-US", "de-DE"],
  "priority": "normal",
  "callback_url": "https://myapp.com/webhooks/translation"
}
```

**Response: 202 Accepted**
```json
{
  "job_id": "TRANS-2025-001234",
  "source_locale": "fr-FR",
  "target_locales": ["en-US", "de-DE"],
  "status": "pending",
  "estimated_completion": "2025-01-10T20:00:00Z"
}
```

### Get Translation Status

```http
GET /translations/{job_id}
Authorization: Bearer {token}
```

---

## Workflow Endpoints

### Trigger Workflow

```http
POST /workflows/{workflow_name}/trigger
Authorization: Bearer {token}

{
  "input": {
    "brief_id": "BRIEF-001",
    "priority": "high"
  },
  "callback_url": "https://myapp.com/webhooks/workflow"
}
```

**Available Workflows:**
- `brief-to-article`
- `content-to-multilang`
- `media-to-cdn`
- `request-to-brief`

### Get Workflow Status

```http
GET /workflows/runs/{run_id}
Authorization: Bearer {token}
```

**Response: 200 OK**
```json
{
  "run_id": "RUN-2025-001234",
  "workflow": "brief-to-article",
  "status": "running",
  "current_step": "seo_optimization",
  "progress": {
    "completed": 3,
    "total": 6,
    "percentage": 50
  },
  "started_at": "2025-01-10T14:00:00Z",
  "steps": [
    { "name": "validate_brief", "status": "completed" },
    { "name": "create_draft", "status": "completed" },
    { "name": "write_content", "status": "completed" },
    { "name": "seo_optimization", "status": "running" },
    { "name": "review", "status": "pending" },
    { "name": "publish", "status": "pending" }
  ]
}
```

---

## Webhooks

### Webhook Configuration

```http
POST /webhooks
Authorization: Bearer {token}

{
  "url": "https://myapp.com/webhooks/content",
  "events": [
    "content.created",
    "content.published",
    "content.updated",
    "asset.uploaded",
    "translation.completed",
    "workflow.completed"
  ],
  "secret": "whsec_..."
}
```

### Webhook Events

| Event | Description | Payload |
|-------|-------------|---------|
| `content.created` | New content created | Content object |
| `content.updated` | Content modified | Content object + changes |
| `content.published` | Content published | Content object + URLs |
| `content.unpublished` | Content unpublished | Content ID |
| `asset.uploaded` | Asset uploaded | Asset object |
| `asset.processed` | Asset processing complete | Asset object + variants |
| `translation.requested` | Translation job started | Job object |
| `translation.completed` | Translation finished | Job object + content IDs |
| `workflow.started` | Workflow triggered | Run object |
| `workflow.completed` | Workflow finished | Run object + outputs |
| `workflow.failed` | Workflow failed | Run object + error |

### Webhook Payload

```json
{
  "id": "evt_001234",
  "type": "content.published",
  "created_at": "2025-01-10T18:00:00Z",
  "data": {
    "content_id": "CONTENT-2025-001234",
    "title": "Guide SEO 2025",
    "url": "https://example.com/guides/seo-2025",
    "locale": "fr-FR"
  }
}
```

### Webhook Signature Verification

```javascript
const crypto = require('crypto');

function verifyWebhookSignature(payload, signature, secret) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(`sha256=${expected}`)
  );
}
```

---

## Error Responses

### Error Format

```json
{
  "error": {
    "code": "CONTENT_NOT_FOUND",
    "message": "Content with ID CONTENT-999 not found",
    "details": {
      "content_id": "CONTENT-999"
    },
    "request_id": "req_abc123"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `CONTENT_NOT_FOUND` | 404 | Content does not exist |
| `ASSET_NOT_FOUND` | 404 | Asset does not exist |
| `VALIDATION_ERROR` | 422 | Invalid request data |
| `FILE_TOO_LARGE` | 413 | Upload exceeds size limit |
| `UNSUPPORTED_FORMAT` | 415 | File type not supported |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| Content CRUD | 100/min | Per user |
| Asset Upload | 20/min | Per user |
| Batch Operations | 5/min | Per user |
| Webhooks | 1000/min | Per app |

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704902400
```

---

## SDKs

### JavaScript/Node.js

```javascript
import { ContentManagementClient } from '@web-agency/content-sdk';

const client = new ContentManagementClient({
  baseUrl: 'https://api.example.com/content/v1',
  apiKey: process.env.CONTENT_API_KEY
});

// Create content
const content = await client.content.create({
  title: 'Mon Article',
  type: 'article',
  body: '...'
});

// Upload asset
const asset = await client.assets.upload({
  file: fs.createReadStream('image.png'),
  altText: 'Description'
});
```

### Python

```python
from content_management import Client

client = Client(
    base_url="https://api.example.com/content/v1",
    api_key=os.environ["CONTENT_API_KEY"]
)

# Create content
content = client.content.create(
    title="Mon Article",
    type="article",
    body="..."
)
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2025-01-10 | Initial release |

## References

- [SKILL.md](./SKILL.md) - Skill overview
- [OPERATIONS.md](./OPERATIONS.md) - Operations guide
- [SECURITY.md](./SECURITY.md) - Security guide
