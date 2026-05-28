# Microservices Example

This example demonstrates how to configure a microservices architecture with multiple independent repositories.

## Structure

```
workspace/
├── frontend/                 # React frontend
│   └── .claude/
│       ├── config.json
│       └── context.md
├── auth-service/            # Authentication service
│   └── .claude/
│       ├── config.json
│       └── context.md
├── user-service/            # User management service
│   └── .claude/
│       ├── config.json
│       └── context.md
├── product-service/         # Product catalog service
│   └── .claude/
│       ├── config.json
│       └── context.md
├── api-gateway/             # API Gateway
│   └── .claude/
│       ├── config.json
│       └── context.md
├── shared-types/            # Shared TypeScript types
│   └── .claude/
│       ├── config.json
│       └── context.md
└── .workspace/
    └── config.json
```

## Workspace Configuration

See `.workspace/config.json` for the complete workspace setup.

## Usage with Claude

```
@workspace init microservices
# Claude will detect all services

@workspace analyze
# Shows service dependencies and API contracts

@workspace task "Add new user profile endpoint"
# Claude identifies: user-service, api-gateway, frontend need changes
```

## Key Features

- **Independent services**: Each service can be deployed independently
- **Shared types**: TypeScript types shared across services
- **API Gateway**: Single entry point for all services
- **Service mesh**: Services communicate via REST/gRPC

## Service Dependencies

```
frontend → api-gateway
api-gateway → auth-service, user-service, product-service
user-service → auth-service
product-service → auth-service
all services → shared-types
```

## Communication Patterns

- **Frontend ↔ API Gateway**: REST API
- **API Gateway ↔ Services**: REST/gRPC
- **Service ↔ Service**: Event-driven (message queue)

## Development

```bash
# Start all services
docker-compose up

# Start individual service
cd auth-service && npm run dev

# Run tests for all services
./scripts/test-all.sh
```

## Deployment

Each service has its own:
- Dockerfile
- CI/CD pipeline
- Kubernetes deployment
- Environment configuration
