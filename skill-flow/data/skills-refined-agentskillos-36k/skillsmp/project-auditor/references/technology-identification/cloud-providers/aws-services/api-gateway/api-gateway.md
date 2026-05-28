# Amazon API Gateway

**Category**: cloud-providers/aws-services
**Description**: Managed API creation, publishing, and management service
**Homepage**: https://aws.amazon.com/api-gateway

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*API Gateway packages*

- `@aws-sdk/client-api-gateway` - API Gateway SDK v3
- `@aws-sdk/client-apigatewayv2` - API Gateway V2 SDK
- `serverless-http` - API Gateway adapter

#### PYPI
*API Gateway Python packages*

- `boto3` - AWS SDK (includes API Gateway)

#### GO
*API Gateway Go packages*

- `github.com/aws/aws-sdk-go-v2/service/apigateway` - API Gateway SDK
- `github.com/aws/aws-sdk-go-v2/service/apigatewayv2` - API Gateway V2

---

## TIER 2: Deep Detection (File-based)

### Code Patterns

**Pattern**: `execute-api\.[a-z0-9-]+\.amazonaws\.com`
- API Gateway invoke URL
- Example: `https://abc123.execute-api.us-east-1.amazonaws.com/prod`

**Pattern**: `API_GATEWAY_URL|APIGW_URL|API_ENDPOINT`
- API Gateway environment variables
- Example: `API_GATEWAY_URL=https://abc123.execute-api...`

**Pattern**: `arn:aws:execute-api:[a-z0-9-]+:[0-9]+:`
- API Gateway ARN
- Example: `arn:aws:execute-api:us-east-1:123456789:abc123/prod/GET/`

**Pattern**: `Type:\s*['"]?AWS::ApiGateway::|Type:\s*['"]?AWS::ApiGatewayV2::`
- CloudFormation API Gateway resources

**Pattern**: `x-amazon-apigateway-|x-apigw-api-id`
- API Gateway headers
- Example: `x-amazon-apigateway-api-id: abc123`

**Pattern**: `openapi.*x-amazon-apigateway|swagger.*x-amazon-apigateway`
- API Gateway OpenAPI extensions

---

## Environment Variables

- `API_GATEWAY_URL` - API Gateway URL
- `API_GATEWAY_STAGE` - Deployment stage
- `API_GATEWAY_API_ID` - API ID
- `AWS_API_GATEWAY_KEY` - API key

## Detection Notes

- REST APIs and HTTP APIs (v2)
- WebSocket APIs for real-time
- API keys for rate limiting
- Usage plans for quotas
- Custom domain names supported

---

## Secrets Detection

### Credentials

#### API Gateway API Key
**Pattern**: `(?:api[_-]?gateway|APIGW).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-zA-Z0-9]{20,})['"]?`
**Severity**: high
**Description**: API Gateway API key
**Example**: `API_GATEWAY_KEY=abc123def456...`

---

## TIER 3: Configuration Extraction

### API ID Extraction

**Pattern**: `https://([a-z0-9]+)\.execute-api\.[a-z0-9-]+\.amazonaws\.com`
- API Gateway API ID from URL
- Extracts: `api_id`
- Example: `abc123` from invoke URL

### Stage Extraction

**Pattern**: `execute-api\.[a-z0-9-]+\.amazonaws\.com/([a-zA-Z0-9_-]+)`
- Deployment stage from URL
- Extracts: `stage`
- Example: `prod` from invoke URL
