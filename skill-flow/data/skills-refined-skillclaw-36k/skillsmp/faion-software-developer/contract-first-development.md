# Contract-First Development

**ID:** contract-first-development

## Problem

Code-first leads to inconsistent APIs. Teams wait for implementation to integrate.

## Framework

**Development Workflow:**

```
1. Design API (OpenAPI spec)
        |
2. Review & Approve (Team)
        |
3. Generate (Server stubs, Client SDKs, Tests)
        |
4. Implement (Fill in business logic)
        |
5. Validate (Spec compliance)
        |
6. Deploy
```

## Design Phase

```yaml
# 1. Start with OpenAPI spec
openapi: 3.1.0
info:
  title: Payment API
  version: 1.0.0

paths:
  /payments:
    post:
      operationId: createPayment
      summary: Create a new payment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreatePaymentRequest'
      responses:
        '201':
          description: Payment created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Payment'
        '400':
          $ref: '#/components/responses/ValidationError'

components:
  schemas:
    CreatePaymentRequest:
      type: object
      required: [amount, currency, customer_id]
      properties:
        amount:
          type: integer
          minimum: 1
          description: Amount in cents
        currency:
          type: string
          enum: [USD, EUR, GBP]
        customer_id:
          type: string
          format: uuid
```

## Code Generation

```bash
# Generate Python server with FastAPI
openapi-generator generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o ./server \
  --additional-properties=packageName=payment_api

# Generate TypeScript client
openapi-generator generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./client

# Generate test stubs
openapi-generator generate \
  -i openapi.yaml \
  -g python \
  -o ./tests \
  --global-property=apiTests=true
```

## Implementation

```python
# Generated stub (server/payment_api/apis/payments_api.py)
from payment_api.models import CreatePaymentRequest, Payment

class PaymentsApi:
    async def create_payment(
        self,
        create_payment_request: CreatePaymentRequest
    ) -> Payment:
        # TODO: Implement business logic
        raise NotImplementedError()

# Your implementation
class PaymentsApiImpl(PaymentsApi):
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    async def create_payment(
        self,
        create_payment_request: CreatePaymentRequest
    ) -> Payment:
        payment = await self.payment_service.process_payment(
            amount=create_payment_request.amount,
            currency=create_payment_request.currency,
            customer_id=create_payment_request.customer_id
        )
        return Payment(
            id=payment.id,
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status
        )
```

## Validation

```python
# Validate implementation against spec
from openapi_core import OpenAPI
from openapi_core.testing.mock import MockRequest, MockResponse

spec = OpenAPI.from_file_path("openapi.yaml")

def test_create_payment_matches_spec():
    # Make real request
    response = client.post("/payments", json={
        "amount": 1000,
        "currency": "USD",
        "customer_id": "550e8400-e29b-41d4-a716-446655440000"
    })

    # Validate against spec
    mock_request = MockRequest("http://localhost", "POST", "/payments")
    mock_response = MockResponse(
        data=response.content,
        status_code=response.status_code
    )

    result = spec.validate_response(mock_request, mock_response)
    assert not result.errors, f"Spec validation failed: {result.errors}"
```

## Linting & Review

```bash
# Lint OpenAPI spec with Spectral
spectral lint openapi.yaml

# Rules (.spectral.yaml)
extends: spectral:oas
rules:
  operation-operationId: error
  operation-description: warn
  info-contact: warn
  oas3-schema: error

# Redocly CLI for validation
redocly lint openapi.yaml
redocly preview-docs openapi.yaml
```

## CI/CD Integration

```yaml
# .github/workflows/api.yml
name: API Contract CI

on:
  pull_request:
    paths:
      - 'openapi.yaml'
      - 'server/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint OpenAPI spec
        run: npx spectral lint openapi.yaml

      - name: Generate server code
        run: |
          openapi-generator generate \
            -i openapi.yaml \
            -g python-fastapi \
            -o ./generated

      - name: Compare with implementation
        run: diff -r ./generated/models ./server/models

      - name: Run contract tests
        run: pytest tests/contract/
```

## Best Practices

- Treat OpenAPI spec as source of truth
- Review spec changes like code
- Regenerate clients on spec changes
- Run spec validation in CI
- Use breaking change detection
- Version your API contracts
- Generate documentation from spec

## Agent

faion-api-agent
