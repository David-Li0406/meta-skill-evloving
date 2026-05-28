# Airweave SDK Reference

Complete reference for the Airweave Python and TypeScript SDKs.

## Installation

```bash
# Python
pip install airweave-sdk

# TypeScript/JavaScript
npm install @airweave/sdk
```

## Client Initialization

### Python

```python
from airweave import AirweaveSDK

# Cloud (default)
client = AirweaveSDK(api_key="YOUR_API_KEY")

# Self-hosted
client = AirweaveSDK(
    api_key="YOUR_API_KEY",
    base_url="http://localhost:8001"
)
```

### TypeScript

```typescript
import { AirweaveSDKClient, AirweaveSDKEnvironment } from "@airweave/sdk";

// Cloud
const client = new AirweaveSDKClient({ apiKey: "YOUR_API_KEY" });

// Self-hosted
const client = new AirweaveSDKClient({
    apiKey: "YOUR_API_KEY",
    environment: AirweaveSDKEnvironment.Local
});
```

## Collections API

### Create Collection

**Python:**
```python
collection = client.collections.create(name="My Collection")
# Returns: Collection object with readable_id
```

**TypeScript:**
```typescript
const collection = await client.collections.create({ name: "My Collection" });
```

### List Collections

**Python:**
```python
collections = client.collections.list()
for c in collections:
    print(f"{c.name}: {c.readable_id}")
```

**TypeScript:**
```typescript
const collections = await client.collections.list();
```

### Get Collection

**Python:**
```python
collection = client.collections.get(readable_id="my-collection-abc123")
```

### Delete Collection

**Python:**
```python
client.collections.delete(readable_id="my-collection-abc123")
```

## Source Connections API

### Create Source Connection

**Python (API Key Auth):**
```python
source = client.source_connections.create(
    name="My Stripe Connection",
    short_name="stripe",
    readable_collection_id=collection.readable_id,
    authentication={
        "credentials": {"api_key": "sk_live_..."}
    }
)
```

**OAuth Sources (Google, Microsoft, etc.):**

OAuth sources require user authorization via the Airweave UI at https://app.airweave.ai or implementing the OAuth flow in your application. The SDK does not provide a direct OAuth helper—use the web UI for the simplest setup.

### Available Source Short Names

**Productivity & Docs:**
| Source | Short Name | Auth Type |
|--------|------------|-----------|
| Notion | `notion` | Integration Token |
| Google Drive | `google_drive` | OAuth |
| Google Docs | `google_docs` | OAuth |
| Google Slides | `google_slides` | OAuth |
| Dropbox | `dropbox` | OAuth |
| OneDrive | `onedrive` | OAuth |
| SharePoint | `sharepoint` | OAuth |
| Box | `box` | OAuth |
| Airtable | `airtable` | API Key |
| Excel | `excel` | OAuth |
| Word | `word` | OAuth |
| OneNote | `onenote` | OAuth |

**Communication:**
| Source | Short Name | Auth Type |
|--------|------------|-----------|
| Slack | `slack` | OAuth |
| Gmail | `gmail` | OAuth |
| Outlook Mail | `outlook_mail` | OAuth |
| Outlook Calendar | `outlook_calendar` | OAuth |
| Google Calendar | `google_calendar` | OAuth |
| Teams | `teams` | OAuth |

**Project Management:**
| Source | Short Name | Auth Type |
|--------|------------|-----------|
| Jira | `jira` | API Token |
| Linear | `linear` | API Key |
| Asana | `asana` | OAuth |
| Trello | `trello` | API Key |
| Monday | `monday` | API Key |
| ClickUp | `clickup` | OAuth |
| Todoist | `todoist` | OAuth |

**Development:**
| Source | Short Name | Auth Type |
|--------|------------|-----------|
| GitHub | `github` | Personal Access Token / OAuth |
| GitLab | `gitlab` | Personal Access Token |
| Bitbucket | `bitbucket` | OAuth |
| Confluence | `confluence` | API Token |

**CRM & Sales:**
| Source | Short Name | Auth Type |
|--------|------------|-----------|
| Salesforce | `salesforce` | OAuth |
| HubSpot | `hubspot` | OAuth |
| Attio | `attio` | API Key |
| Zendesk | `zendesk` | OAuth |
| Pipedrive | `pipedrive` | OAuth |
| Zoho CRM | `zoho_crm` | OAuth |
| Shopify | `shopify` | OAuth |

**Data:**
| Source | Short Name | Auth Type |
|--------|------------|-----------|
| Stripe | `stripe` | API Key |
| PostgreSQL | `postgresql` | Connection String |

### List Source Connections

**Python:**
```python
sources = client.source_connections.list(
    readable_collection_id=collection.readable_id
)
```

### Trigger Sync

**Python:**
```python
client.source_connections.sync(
    source_connection_id=source.id
)
```

## Search API

### Basic Search

**Python:**
```python
results = client.collections.search(
    readable_id=collection.readable_id,
    query="Find customer complaints about shipping"
)
```

**TypeScript:**
```typescript
const results = await client.collections.search(
    collection.readableId,
    { query: "Find customer complaints about shipping" }
);
```

### Search with Parameters

**Python:**
```python
results = client.collections.search(
    readable_id=collection.readable_id,
    query="API documentation",
    search_type="hybrid",           # "semantic" (default) or "hybrid"
    limit=20,                       # Max results
    offset=0,                       # For pagination
    recency_bias=0.5,              # 0-1, favor recent content
    enable_reranking=True,         # AI reranking
    enable_query_expansion=True,   # Expand query variations
    top_k=50                       # Internal retrieval count
)
```

**TypeScript:**
```typescript
const results = await client.collections.search(
    collection.readableId,
    {
        query: "API documentation",
        searchType: "hybrid",
        limit: 20,
        recencyBias: 0.5,
        enableReranking: true,
        enableQueryExpansion: true,
        topK: 50
    }
);
```

### AI Completion Response

Instead of raw results, get an AI-synthesized answer:

**Python:**
```python
answer = client.collections.search(
    readable_id=collection.readable_id,
    query="What is our vacation policy?",
    response_type="completion",
    enable_reranking=True
)
# Returns synthesized answer based on search results
```

### Advanced Search with Filters

**Python:**
```python
from airweave import SearchRequest, Filter, FieldCondition, MatchAny, Range

search_request = SearchRequest(
    query="bug reports",
    filter=Filter(
        must=[
            FieldCondition(
                key="source_name",
                match=MatchAny(any=["GitHub", "Jira"])
            )
        ],
        should=[
            FieldCondition(
                key="priority",
                match=MatchAny(any=["high", "critical"])
            )
        ]
    ),
    recency_bias=0.6,
    enable_reranking=True,
    limit=25
)

results = client.collections.search_advanced(
    readable_id=collection.readable_id,
    search_request=search_request
)
```

## Search Result Structure

```python
results.results  # List of result objects

# Each result contains:
{
    "id": "...",
    "score": 0.87,
    "payload": {
        "md_content": "The actual content...",
        "source_name": "Slack",
        "source_type": "slack",
        "url": "https://...",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        # Additional source-specific metadata
    }
}
```

## Error Handling

**Python:**
```python
try:
    results = client.collections.search(
        readable_id="invalid-id",
        query="test"
    )
except Exception as e:
    # Handle API errors - check status code or message
    error_msg = str(e)
    if "404" in error_msg:
        print("Collection not found")
    elif "401" in error_msg or "403" in error_msg:
        print("Invalid API key or access denied")
    else:
        print(f"API error: {e}")
```

## Rate Limits

- The API has rate limits for protection
- Implement exponential backoff for production use
- Contact support for higher limits if needed

```python
import time

def search_with_retry(client, collection_id, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.collections.search(
                readable_id=collection_id,
                query=query
            )
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
```

