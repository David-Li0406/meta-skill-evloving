---
name: java-grpc
description: gRPC service design and evolution with proto conventions, deadlines/timeouts, status/error mapping, and streaming guidelines. Use when you need internal RPC performance or stable contracts.
license: Apache-2.0
compatibility: JDK 17+ (recommended 21+). grpc-java. Protobuf v3. Works with Gradle/Maven.
metadata:
  owner: backend-platform
  version: "1.0"
  tags: [java, grpc, protobuf, rpc, deadlines, retries, streaming, compatibility, testing]
---

# gRPC Playbook (Java)

## Scope

### In scope

- `.proto` conventions (packages, naming, versioning, reserved fields).
- API surface: unary vs streaming; pagination patterns; metadata.
- Reliability: deadlines/timeouts, cancellation, retry policy design.
- Error model: mapping domain errors to gRPC status codes + details.
- Streaming guidelines: flow control, message size, backpressure, ordering.
- Client/server skeletons and testing approaches.

### Out of scope

- Service mesh specifics and advanced LB policy tuning unless requested.

## When to use

- You are introducing internal RPC between services.
- You need performance and strict contracts.
- You are refactoring REST internals to gRPC or diagnosing timeout/retry storms.

## Inputs (required context)

- Service boundaries and critical paths (p99 latency expectations).
- Backward compatibility requirement (multi-version clients).
- Idempotency of methods (safe for retries?).
- Streaming needs and expected message sizes.
- AuthN/AuthZ mechanism (mTLS, tokens, metadata).

## Proto design rules (compatibility-first)

- Use **proto3**.
- Never change numeric field tags; never reuse removed tags—use `reserved`.
- Prefer additive changes: add optional fields; keep old fields until all clients migrate.
- Versioning strategy:
  - Prefer versioned packages: `com.company.foo.v1`
  - Or version service names: `FooServiceV1` only if packages can’t change.

## Error model (status mapping)

- Use standard gRPC status codes:
  - INVALID_ARGUMENT for validation failures
  - NOT_FOUND for missing resources
  - ALREADY_EXISTS for conflicts
  - PERMISSION_DENIED / UNAUTHENTICATED for auth
  - FAILED_PRECONDITION for state conflicts
  - UNAVAILABLE for transient upstream issues
  - INTERNAL for unexpected errors

- Include structured error details when needed (e.g., field violations).

## Deadlines, timeouts, and cancellation (mandatory discipline)

- Clients must set per-RPC **deadlines** based on SLO.
- Servers should propagate cancellation to downstream calls.
- Avoid “infinite” deadlines; they cause resource leaks and queueing collapse.

## Retries (be explicit)

- Retrying non-idempotent methods can create duplicates.
- Only enable retries for idempotent methods or when protected by idempotency keys.
- Use gRPC retry policies via service config (where supported) with maxAttempts, backoff, and retryableStatusCodes.

## Streaming guidelines

- Choose streaming only when it materially improves:
  - large payload chunking
  - server push updates
  - high-frequency telemetry
- Apply backpressure:
  - server must not outpace client’s ability to receive
  - handle flow control events
- Cap message sizes; consider chunking for large blobs.
- Define ordering guarantees: per stream vs global.

## Procedure (step-by-step)

### Step 1 — Create Proto Contract

Create `proto/<service>/v1/<service>.proto`:

- package + java_package + java_multiple_files
- service definition
- request/response messages
- comments for semantics, idempotency, and error mapping

### Step 2 — Generate stubs and implement server

- Implement server handlers.
- Add interceptors for:
  - correlation IDs
  - auth context extraction
  - metrics and tracing
- Ensure exceptions map to StatusRuntimeException with proper status codes.

### Step 3 — Implement client with deadlines and safe retries

- Use shared Channel management (singleton per destination).
- Always set deadlines on stubs.
- For retryable calls: define service config policy; ensure idempotency.

### Step 4 — Add compatibility guardrails

- Add CI checks to prevent breaking proto changes:
  - enforce reserved tags for removed fields
  - forbid renumbering
- Document deprecation windows.

### Step 5 — Testing

- Unit tests: in-process server + stub calls.
- Integration tests: spin real server (or container) and validate deadlines and error mapping.

## Output / Artifacts

- `proto/.../*.proto`
- `src/main/java/.../grpc/server/` implementation
- `src/main/java/.../grpc/client/` client wrapper with deadlines
- `src/test/java/.../grpc/` tests (in-process)
- `docs/rpc/<service>.md` (contract + SLA + retry policy)

## Definition of Done (DoD)

- [ ] Proto contract exists with compatibility rules and comments.
- [ ] Deadlines are enforced by clients and propagated.
- [ ] Error mapping is standardized and tested.
- [ ] Retry policy is explicit and only for idempotent operations (or guarded).
- [ ] Streaming endpoints include backpressure and size caps.
- [ ] Tests cover: deadline exceeded, cancelled, invalid argument, unavailable.

## Guardrails (What NOT to do)

- Never ship client calls without deadlines.
- Never enable retries globally without idempotency analysis.
- Never reuse proto field tags; always reserve.
- Avoid streaming for simple request/response; keep APIs simple.

## Skeletons

### Proto template

```proto
syntax = "proto3";

package com.company.foo.v1;

option java_multiple_files = true;
option java_package = "com.company.foo.v1";

service FooService {
  // Idempotency: YES (safe to retry) if request.idempotency_key is stable
  rpc GetFoo(GetFooRequest) returns (GetFooResponse);
}

message GetFooRequest {
  string foo_id = 1;
}

message GetFooResponse {
  Foo foo = 1;
}

message Foo {
  string id = 1;
  string name = 2;
  // reserved 3; // if removed later
}
```

### Client deadline snippet (grpc-java)

```java
FooServiceGrpc.FooServiceBlockingStub stub = FooServiceGrpc.newBlockingStub(channel)
  .withDeadlineAfter(200, TimeUnit.MILLISECONDS);

GetFooResponse resp = stub.getFoo(GetFooRequest.newBuilder().setFooId(id).build());
```

### Error mapping snippet

```java
throw Status.INVALID_ARGUMENT
  .withDescription("foo_id must be non-empty")
  .asRuntimeException();
```

### Common failure modes & fixes

- Symptom: tail latency spikes → Cause: missing deadlines + queueing → Fix: set deadlines, propagate cancellation.

- Symptom: duplicate side effects → Cause: retries on non-idempotent RPC → Fix: disable retries or add idempotency keys.

- Symptom: clients break after proto change → Cause: field renumber/reuse → Fix: reserved tags, additive evolution.

## References

- Use official gRPC docs for deadlines, status codes, keepalive, retries, and streaming concepts.
- Use official Protobuf guidance for field compatibility and reserved tags.
