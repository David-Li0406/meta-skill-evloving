# Content Patterns

Reusable patterns for consistent, high-quality documentation content.

---

## 1. Axioms Pattern

Define guiding principles with rationale. Use for design decisions, conventions, and standards.

### Structure

```markdown
### [Axiom Name]

**Axiom**: [Clear statement of the principle]

**Examples**:
- `example1` - Description of correct usage
- `example2` - Description of correct usage

**Rationale**:
1. **Benefit 1**: Why this matters
2. **Benefit 2**: What problem it solves
3. **Benefit 3**: What it enables

**Anti-patterns**:
- ❌ `bad-example` - Why it's wrong
- ❌ `bad-example` - What problems it causes
```

### Example

```markdown
### Message Topic Naming Convention

**Axiom**: All AMQP topic names follow the pattern `usecase.typeoftopic.function`

**Examples**:
- `orders.state.created` - Order creation state change
- `orders.event.shipped` - Order shipped event
- `payments.command.process` - Payment processing command

**Rationale**:
1. **Clarity**: Three-part structure makes purpose obvious
2. **Scalability**: Easy to add new use cases and types
3. **Filtering**: Topic patterns enable selective subscription

**Anti-patterns**:
- ❌ `OrderCreatedTopic` - Too generic, no structure
- ❌ `statebroadcast` - Missing context and hierarchy
```

---

## 2. Trade-offs Pattern

Document decisions with pros, cons, and mitigations. Use for architecture decisions and technology choices.

### Structure

```markdown
## Trade-Offs Summary

| Decision | Pros | Cons | Mitigation |
|----------|------|------|------------|
| [Decision 1] | [Benefits] | [Drawbacks] | [How addressed] |
| [Decision 2] | [Benefits] | [Drawbacks] | [How addressed] |
```

### Example

```markdown
## Trade-Offs Summary

| Decision | Pros | Cons | Mitigation |
|----------|------|------|------------|
| Pub/Sub state sync | Fast, scalable, observable | Requires RabbitMQ | Already required for other features |
| Sidecar pattern | Language-specific optimization | More containers to manage | Small footprint (64Mi) |
| In-memory state | Sub-millisecond latency | Lost on pod restart | Reload from ConfigMap on startup |
| Event sourcing | Full audit trail | Storage growth | 30-day retention policy |
```

---

## 3. Command Examples Pattern

Provide copy-paste ready commands with context. Use for setup, deployment, and operational tasks.

### Structure

```markdown
### [Task Name]

```bash
# Step 1: [Description]
[command]

# Step 2: [Description]
[command]

# Step 3: [Description]
[command]
```

**Expected Output:**
```
[sample output]
```

**If this fails:**
- Check [thing to check]
- Verify [thing to verify]
```

### Example

```markdown
### Deploy to Kubernetes

```bash
# Switch to correct context
kubectl config use-context production-cluster

# Apply manifests using kustomize
kubectl apply -k k8s/overlays/production/

# Wait for rollout to complete
kubectl rollout status deployment/api -n app --timeout=120s

# Verify all pods are healthy
kubectl get pods -n app -l app=api
```

**Expected Output:**
```
deployment "api" successfully rolled out
NAME                   READY   STATUS    RESTARTS   AGE
api-6d5f5947dd-55fzt   3/3     Running   0          42s
api-6d5f5947dd-7k2mw   3/3     Running   0          42s
```

**If this fails:**
- Check image pull secrets: `kubectl get secrets -n app`
- Verify resource quotas: `kubectl describe quota -n app`
- Check events: `kubectl get events -n app --sort-by='.lastTimestamp'`
```

---

## 4. Configuration Examples Pattern

Show YAML/JSON with inline comments explaining each setting. Use for config files and environment setup.

### Structure

```markdown
### [Configuration Name]

```yaml
# [filename]
section:
  setting1: value           # [Explanation of what this controls]
  setting2: value           # [Explanation of what this controls]
  nested:
    option1: value          # [Explanation]
    option2: value          # [Explanation]
```

**Critical Settings:**
- `setting1`: [Why this value matters]
- `nested.option2`: [What happens if wrong]
```

### Example

```markdown
### Queue Configuration

```yaml
# settings.yaml
queues:
  - name: OrderStateChangeTopic
    category: application         # Must be 'application' for business queues
    type: topic
    exchange:
      name: orders.state
      type: topic
      durable: true               # Survive broker restarts
    queue:
      name: order-state-changes
      durable: true
      autoack: false              # Manual acknowledgment for reliability
    routingkey: orders.state.*
    protocol: json
```

**Critical Settings:**
- `autoack: false` - Required for at-least-once delivery; if true, messages may be lost on crash
- `durable: true` - Messages persist across broker restarts; set to false only for ephemeral data
- `category: application` - Infrastructure queues use 'system' and have different retention
```

---

## 5. Troubleshooting Pattern

Organize by symptom with diagnostic steps. Use for operational runbooks and debugging guides.

### Structure

```markdown
### [Symptom Description]

**Symptom**: [What the user observes]

**Diagnostic Steps:**
```bash
# 1. Check [first thing to check]
[command]

# 2. Verify [second thing to check]
[command]

# 3. Look for [pattern or error]
[command]
```

**Common Causes:**
- [Cause 1] - [Brief explanation]
- [Cause 2] - [Brief explanation]
- [Cause 3] - [Brief explanation]

**Resolution:**
```bash
# [Fix description]
[command]
```
```

### Example

```markdown
### State Not Synchronizing Across Pods

**Symptom**: Different pods return different state versions when queried

**Diagnostic Steps:**
```bash
# 1. Check state-monitor version (must be v1.0.8+)
kubectl get deployment api -n app \
  -o jsonpath='{.spec.template.spec.containers[?(@.name=="state-monitor")].image}'

# 2. Verify RabbitMQ connectivity from pod
kubectl exec -n app deployment/api -c state-monitor -- \
  nc -zv rabbitmq.messaging 5672

# 3. Check for broadcast messages in logs
kubectl logs -n app -l app=api -c state-monitor --tail=100 | \
  grep -E "(broadcast|publish|state)"
```

**Common Causes:**
- state-monitor v1.0.7 or earlier (missing broadcast function)
- RabbitMQ vhost permissions not configured
- Network policy blocking AMQP traffic on port 5672
- Exchange not declared (first-pod race condition)

**Resolution:**
```bash
# Update to latest image
kubectl set image deployment/api \
  state-monitor=registry.example.com/state-monitor:v1.0.9 -n app

# Force rollout to apply changes
kubectl rollout restart deployment/api -n app
```
```

---

## 6. Version History Pattern

Track significant changes with context. Use for documenting evolution and breaking changes.

### Structure

```markdown
## Evolution

### v[X.Y.Z] → v[X.Y.Z]: [Change Name]

**Change**: [What was changed]

**Problem**: [What problem it solved]

**Solution**: [How it was solved]

```[language]
// Before
[old code or config]

// After
[new code or config]
```

**Result**: [Outcome]
**Status**: [✅ Verified | ⚠️ Testing | ❌ Rolled back] on [environment]
```

### Example

```markdown
## Evolution

### v1.0.8 → v1.0.9: Version-Based Change Detection

**Change**: Fixed critical bug in `hasStateChanged()` function

**Problem**: State changes weren't detected when using identical test data repeatedly, causing state sync failures in CI environments

**Solution**: Added version check as first condition before data comparison:

```go
// Before (v1.0.8)
func hasStateChanged(old, new StateData) bool {
    return !reflect.DeepEqual(old.Data, new.Data)
}

// After (v1.0.9)
func hasStateChanged(old, new StateData) bool {
    // Check version first (catches metadata-only updates)
    if old.Metadata.Version != new.Metadata.Version {
        return true
    }
    return !reflect.DeepEqual(old.Data, new.Data)
}
```

**Result**: State synchronization works correctly across all pods, including identical data scenarios
**Status**: ✅ Verified on EKS (arm64) and MicroK8s (amd64)
```

---

## 7. Status Table Pattern

Track component or feature status. Use for project overviews and implementation tracking.

### Structure

```markdown
### [Category] Status

| [Item] | Status | Notes |
|--------|--------|-------|
| [Item 1] | ✅ Complete | [Details] |
| [Item 2] | ⚠️ Partial | [What's missing] |
| [Item 3] | ❌ Not Started | [Blockers or timeline] |
```

### Example

```markdown
### Service Implementation Status

| Service | Status | Notes |
|---------|--------|-------|
| API Gateway | ✅ Complete | v2.1.0 deployed, rate limiting enabled |
| Auth Service | ✅ Complete | OAuth2 + JWT, refresh token rotation |
| Order Service | ⚠️ Partial | CRUD done, webhooks pending |
| Payment Service | ⚠️ Partial | Stripe integration done, PayPal pending |
| Notification Service | ❌ Not Started | Blocked on email provider selection |
| Analytics Service | ❌ Not Started | Q2 roadmap |
```

---

## 8. API Documentation Pattern

Document endpoints with request/response examples. Use for REST APIs and service interfaces.

### Structure

```markdown
### [HTTP Method] [Endpoint]

**Description**: [What this endpoint does]

**Authentication**: [Required auth method]

**Request:**
```bash
curl -X [METHOD] '[URL]' \
  -H 'Authorization: Bearer [token]' \
  -H 'Content-Type: application/json' \
  -d '{
    "field1": "value",
    "field2": "value"
  }'
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "uuid",
    "field1": "value"
  }
}
```

**Error Responses:**

| Status | Description |
|--------|-------------|
| 400 | Invalid request body |
| 401 | Missing or invalid token |
| 404 | Resource not found |
```

### Example

```markdown
### POST /api/v1/orders

**Description**: Create a new order

**Authentication**: Bearer token required

**Request:**
```bash
curl -X POST 'https://api.example.com/api/v1/orders' \
  -H 'Authorization: Bearer eyJhbG...' \
  -H 'Content-Type: application/json' \
  -d '{
    "customerId": "cust_123",
    "items": [
      {"productId": "prod_456", "quantity": 2}
    ],
    "shippingAddress": {
      "street": "123 Main St",
      "city": "Seattle",
      "zip": "98101"
    }
  }'
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "ord_789",
    "status": "pending",
    "total": 4999,
    "currency": "USD",
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
```

**Error Responses:**

| Status | Description |
|--------|-------------|
| 400 | Invalid request - missing required fields |
| 401 | Invalid or expired token |
| 422 | Validation error - invalid product ID or quantity |
```
