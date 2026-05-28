---
name: dapr
description: Comprehensive DAPR (Distributed Application Runtime) skill for building distributed microservices from hello world to professional production systems. Provides guidance on DAPR setup, building blocks (service invocation, state management, pub/sub, actors, secrets), sidecar configuration, component configuration, and Kubernetes integration for scalable distributed applications.
---

# DAPR (Distributed Application Runtime) Skill

This skill provides comprehensive guidance for building distributed microservices using DAPR (Distributed Application Runtime) from hello world examples to professional production systems.

## When to Use This Skill

Use this skill when working with:
- DAPR runtime setup and configuration
- Building blocks implementation (service invocation, state management, pub/sub, actors, secrets)
- Sidecar configuration and deployment
- Component configuration for state stores, pub/sub brokers, and secret stores
- Kubernetes integration and deployment patterns
- Production DAPR deployments
- Troubleshooting DAPR issues

## Prerequisites

- Basic understanding of distributed systems
- Familiarity with containerization and Kubernetes
- Understanding of microservices architecture patterns

## Installation

For detailed installation instructions, refer to the [DAPR Installation Guide](./references/dapr-installation.md) which covers installation on Linux, Windows, and macOS platforms, including various installation methods and troubleshooting tips.

## Quickstarts

For hands-on examples and getting started guides, refer to the [DAPR Quickstarts Guide](./references/dapr-quickstarts.md) which covers the core building blocks with practical examples for state management, service invocation, pub/sub, secrets management, and actors.

## Core Concepts

DAPR (Distributed Application Runtime) is a portable, event-driven runtime that makes it easy for developers to build resilient, stateless, and stateful applications that run on the cloud and edge. It provides APIs as building blocks to simplify the development of resilient, portable, and microservice-based applications.

Key features:
1. **Sidecar Architecture**: DAPR uses a sidecar approach where a lightweight runtime runs alongside your application
2. **Building Blocks**: Pre-built components for common distributed system patterns
3. **Pluggable Components**: Support for various state stores, pub/sub brokers, and secret stores
4. **Language Agnostic**: Works with any programming language
5. **Platform Agnostic**: Runs on any Kubernetes cluster, cloud, or edge

## Getting Started - Hello World

### Basic Service Invocation Example
```bash
# Run a service with DAPR sidecar
dapr run --app-id my-node-app --app-port 3000 node app.js

# Invoke another service
curl -X POST http://localhost:3500/v1.0/invoke/target-service/method/endpoint
```

### Basic State Management Example (Node.js)
```javascript
const express = require('express');
const { DaprClient } = require('@dapr/dapr';

const client = new DaprClient({ daprHost: 'localhost', daprPort: '3500' });

// Save state
await client.state.save('statestore', 'myKey', { name: 'John', age: 30 });

// Get state
const state = await client.state.get('statestore', 'myKey');
console.log(state);

// Delete state
await client.state.delete('statestore', 'myKey');
```

## Building Blocks

### 1. Service-to-Service Invocation
Enable applications to communicate with each other through well-known endpoints using HTTP or gRPC messages. DAPR provides an endpoint that acts as a reverse proxy with built-in service discovery, tracing, and error handling.

**API Endpoint**: `/v1.0/invoke/{appId}/method/{method}`

### 2. State Management
Manage application state using DAPR's state building block. This includes saving, retrieving, deleting, and querying state data with support for metadata and transactions.

**API Endpoints**:
- `POST /v1.0/state/{store_name}` - Save state
- `GET /v1.0/state/{store_name}/{key}` - Get state
- `DELETE /v1.0/state/{store_name}/{key}` - Delete state
- `POST /v1.0/state/{store_name}/bulk` - Get bulk state
- `POST /v1.0/state/{store_name}/transaction` - Execute state transaction

### 3. Publish and Subscribe
Implements a loosely coupled messaging pattern where publishers send messages to a topic, and subscribers receive them.

**API Endpoints**:
- `POST /v1.0/publish/{pubsubname}/{topic}` - Publish a message to a topic
- Subscription is configured via Dapr subscription definitions

### 4. Actors
DAPR provides virtual actors as a building block to develop stateful and stateless services using the Actor pattern.

**API Endpoint**: `/v1.0/actors/{actorType}/{actorId}/{methodName}`

### 5. Secrets Management
Retrieve secrets from various secret stores in a unified way.

**API Endpoint**: `/v1.0/secrets/{secret_store_name}/{key}`

## Sidecar Configuration

### Kubernetes Annotations
Configure the DAPR sidecar using Kubernetes annotations:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"                 # Enable DAPR sidecar
        dapr.io/app-id: "myapp"               # Unique app identifier
        dapr.io/app-port: "8080"              # Application port
        dapr.io/config: "myappconfig"         # DAPR configuration name
        dapr.io/log-level: "info"             # Log level
        dapr.io/sidecar-cpu-limit: "4.0"      # CPU limit for sidecar
        dapr.io/sidecar-memory-limit: "512Mi" # Memory limit for sidecar
```

### Standalone Configuration
For local development with DAPR CLI:

```bash
dapr run \
  --app-id myapp \
  --app-port 8080 \
  --dapr-http-port 3500 \
  --dapr-grpc-port 50001 \
  --config config.yaml \
  --components-path ./components \
  node app.js
```

## Component Configuration

### State Store Component (Redis)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
```

### Pub/Sub Component (Redis)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```

### Secret Store Component (Kubernetes)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

## Kubernetes Integration

### Deployment with DAPR Sidecar
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodeapp
  labels:
    app: nodeapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nodeapp
  template:
    metadata:
      labels:
        app: nodeapp
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "nodeapp"
        dapr.io/app-port: "3000"
    spec:
      containers:
      - name: nodeapp
        image: nodeapp:latest
        ports:
        - containerPort: 3000
        imagePullPolicy: Always
```

### Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nodeapp
  labels:
    app: nodeapp
spec:
  ports:
  - port: 3000
    protocol: TCP
    targetPort: 3000
  selector:
    app: nodeapp
  type: LoadBalancer
```

## Security Configuration

### API Token Authentication
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: api-token-configuration
spec:
  authentication:
    http:
      signingKey: "your-32-byte-signing-key-here"
```

### Access Control Lists (ACLs)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: appconfig
spec:
  accessControl:
    defaultAction: allow
    trustDomain: "mydomain"
    policies:
    - appId: app1
      defaultAction: allow
      trustDomain: "mydomain"
      namespace: "default"
      operations:
      - name: /api/v1/users
        httpVerb: ["GET", "POST"]
        action: allow
```

## Monitoring and Observability

### Tracing Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: tracing
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
```

### Metrics Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: metrics
spec:
  metrics:
    enabled: true
    rules:
    - name: dapr_http_requests_total
      labels:
      - name: app_id
        regex: ".*"
```

## Production Best Practices

### Resource Management
- Set resource limits and requests for DAPR sidecars
- Configure appropriate health probes
- Use dedicated namespaces for DAPR system components

### Component Configuration
- Use production-grade state stores (Redis cluster, PostgreSQL, etc.)
- Configure proper authentication and encryption for all components
- Implement proper backup and disaster recovery procedures

### Deployment Strategies
- Use DAPR operators for Kubernetes
- Implement proper rollout strategies
- Monitor DAPR sidecar health and performance

### Security
- Enable mTLS for service-to-service communication
- Use secure secret stores
- Implement proper access control policies
- Regularly update DAPR runtime

## Common Patterns

### Event Sourcing
Use pub/sub building blocks to implement event sourcing patterns where state changes are stored as a sequence of events.

### CQRS (Command Query Responsibility Segregation)
Separate read and write operations using different DAPR building blocks.

### Saga Pattern
Coordinate distributed transactions across multiple services using DAPR pub/sub and state management.

## Troubleshooting

### Common Issues
- Sidecar not injecting: Check annotations and DAPR injector status
- Service invocation failing: Verify app IDs and network connectivity
- State operations failing: Check component configuration and permissions
- Pub/sub not working: Verify component configuration and topic names

### Diagnostic Commands
```bash
# Check DAPR runtime status
dapr status -k

# List DAPR sidecars in Kubernetes
kubectl get pods -l app=dapr-sidecar-injector

# Check DAPR logs
kubectl logs -l app=myapp -c daprd

# Get DAPR configuration
dapr configurations -k

# Get DAPR components
dapr components -k
```
