---
name: backend-architect
description: Backend architecture specialist for Faiston NEXO. Use PROACTIVELY for FastAPI endpoints, Lambda handlers, DynamoDB schemas, S3 presigned URLs, Cognito auth, and AgentCore integration.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Backend Architect Skill

Backend architecture specialist for Faiston NEXO serverless infrastructure.

For detailed patterns and templates, see [reference.md](reference.md).

## Faiston NEXO Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI + Python 3.11 |
| Runtime | AWS Lambda (Mangum adapter) |
| Database | DynamoDB (single-table design) |
| Storage | S3 (presigned URLs, CORS) |
| Auth | Cognito JWT validation |
| AI Agents | AgentCore (direct invocation) |
| Gateway | API Gateway v2 (HTTP API) |
| IaC | Terraform |

## Key Files

| Purpose | Path |
|---------|------|
| FastAPI App | `server/main.py` |
| Lambda Handler | `server/lambda_handler.py` |
| Community Routes | `server/community/routes.py` |
| AgentCore Entry | `server/agentcore/main.py` |
| CORS Config | `terraform/main/locals.tf` |
| Lambda Config | `terraform/main/lambda.tf` |

## FastAPI Patterns

### Endpoint Structure

```python
# server/community/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api", tags=["community"])

class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: str = Field(default="geral")

class PostResponse(BaseModel):
    post_id: str
    title: str
    content: str
    created_at: str

@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, user_id: str = Depends(get_current_user)):
    """Create a new community post."""
    # DynamoDB put_item
    return {"post_id": "...", **post.model_dump()}
```

### Error Handling

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

# Use HTTPException for client errors
raise HTTPException(status_code=404, detail="Post not found")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

## Lambda/Mangum Pattern

```python
# server/lambda_handler.py
from mangum import Mangum
from server.main import app

# Mangum adapter for Lambda
handler = Mangum(app, lifespan="off")
```

**Lambda Configuration (terraform/main/lambda.tf):**
- Timeout: 30 seconds (API Gateway max: 29s)
- Memory: 512MB minimum
- Handler: `lambda_handler.handler`

## DynamoDB Patterns

### Single-Table Design

```python
# PK/SK pattern for community posts
{
    "PK": "POST#category#duvidas",
    "SK": "2025-01-01T12:00:00#post123",
    "post_id": "post123",
    "title": "Question about Python",
    "content": "...",
    "user_id": "user456",
    "GSI1PK": "USER#user456",
    "GSI1SK": "POST#2025-01-01T12:00:00"
}
```

### Query Patterns

```python
import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table("faiston-nexo-community")

# Get posts by category (sorted by date desc)
response = table.query(
    KeyConditionExpression=Key("PK").eq(f"POST#category#{category}"),
    ScanIndexForward=False,  # Descending order
    Limit=20
)

# Get posts by user (using GSI)
response = table.query(
    IndexName="GSI1",
    KeyConditionExpression=Key("GSI1PK").eq(f"USER#{user_id}")
)
```

## S3 Presigned URLs

**CRITICAL**: Use regional endpoint to avoid 307 redirects:

```python
from botocore.config import Config

s3_client = boto3.client(
    's3',
    region_name='us-east-2',
    config=Config(
        signature_version='s3v4',
        s3={'addressing_style': 'virtual'}
    )
)

# Generate upload URL
upload_url = s3_client.generate_presigned_url(
    'put_object',
    Params={
        'Bucket': 'faiston-nexo-assets',
        'Key': f'audio/{episode_id}/{filename}',
        'ContentType': 'audio/mpeg'
    },
    ExpiresIn=3600
)

# Generate download URL
download_url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': key},
    ExpiresIn=7200
)
```

## Cognito JWT Validation

```python
from jose import jwt, JWTError
import httpx

COGNITO_REGION = "us-east-2"
COGNITO_USER_POOL_ID = "us-east-2_6Vzhr0J6M"
COGNITO_CLIENT_ID = "dqqebean5q4fq14bkp2bofnsj"

# JWKS URL
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"

async def validate_token(token: str) -> dict:
    """Validate Cognito JWT token."""
    # Fetch JWKS (cache in production)
    async with httpx.AsyncClient() as client:
        jwks = await client.get(JWKS_URL)

    # Decode and validate
    payload = jwt.decode(
        token,
        jwks.json(),
        algorithms=["RS256"],
        audience=COGNITO_CLIENT_ID
    )
    return payload
```

## CORS Configuration

**IMPORTANT**: CORS is configured ONLY in `terraform/main/locals.tf`:

```hcl
locals {
  cors_allowed_origins = [
    "http://localhost:8081",
    "https://nexo.faiston.com"
  ]
}
```

Do NOT add CORS middleware to FastAPI - it causes duplicate headers!

## Architecture Decisions

### When to Use Lambda vs AgentCore

| Use Case | Solution | Reason |
|----------|----------|--------|
| CRUD operations | Lambda + API Gateway | Fast, simple, cost-effective |
| AI agent chat | AgentCore direct | No timeout, streaming support |
| File upload | Lambda + S3 presigned | Secure, scalable |
| Long operations | AgentCore | >30s operations |

### API Gateway Limits

- Timeout: 29 seconds max
- Payload: 10 MB max
- For larger/longer: Use AgentCore direct invocation

## Output Format

- Be extremely concise, sacrifice grammar for brevity
- Lead with the recommendation, follow with brief reasoning
- Use bullet points and structured formats
- Include code snippets or schemas when helpful
- Flag critical issues with clear warnings

Remember: Never deploy from local console - use GitHub Actions only!
