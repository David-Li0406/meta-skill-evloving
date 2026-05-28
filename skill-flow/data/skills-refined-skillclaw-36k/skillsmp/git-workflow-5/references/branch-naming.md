# Branch Naming Guide

## Format

```
{type}/{scope}-{description}
```

- **type**: Branch purpose (feature, refactor, fix, hotfix, release)
- **scope**: Affected service/module
- **description**: Short kebab-case description

## Examples by Type

### Feature Branches

```bash
feature/chat-crud-api
feature/auth-oauth2-google
feature/location-kakao-map-integration
feature/chat_worker-image-generation
feature/users-profile-avatar
```

### Refactor Branches

```bash
refactor/chat_worker-clean-architecture
refactor/auth-port-adapter-pattern
refactor/reward-fanout-exchange
refactor/location-grpc-migration
```

### Fix Branches

```bash
fix/auth-token-refresh-race
fix/chat-sse-connection-leak
fix/location-null-coordinates
fix/users-email-validation
```

### Hotfix Branches

```bash
hotfix/security-jwt-validation
hotfix/database-connection-pool
hotfix/critical-payment-bug
```

### Release Branches

```bash
release/v1.0.0
release/v1.2.0-rc1
release/v2.0.0-beta
```

## Scope Reference

### Services (apps/)

| Scope | Service |
|-------|---------|
| `auth` | Authentication service |
| `users` | User management |
| `chat` | Chat API |
| `chat_worker` | Chat worker (LangGraph) |
| `location` | Location service |
| `character` | Character service |
| `scan` | Waste scan service |
| `images` | Image processing |

### Infrastructure

| Scope | Area |
|-------|------|
| `infra` | General infrastructure |
| `k8s` | Kubernetes manifests |
| `terraform` | Terraform configs |
| `helm` | Helm charts |
| `ci` | CI/CD pipelines |

## Anti-patterns

```bash
# Bad: Too vague
feature/update
fix/bug

# Bad: No scope
feature/add-new-endpoint

# Bad: Too long
feature/chat-worker-add-new-intent-classification-with-multi-intent-support-and-rag

# Bad: Spaces or special chars
feature/chat worker
feature/chat@api

# Good: Clear and concise
feature/chat-multi-intent-classification
fix/chat_worker-rag-timeout
```

## Branch Lifecycle

```
1. Create from develop
   git checkout develop && git pull
   git checkout -b feature/chat-crud-api

2. Work and commit
   git add . && git commit -m "feat(chat): add CRUD API"

3. Push and PR
   git push -u origin feature/chat-crud-api
   gh pr create --base develop

4. After merge, delete branch
   git checkout develop && git pull
   git branch -d feature/chat-crud-api
```
