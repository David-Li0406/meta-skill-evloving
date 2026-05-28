# DAPR Quickstarts Guide

## Overview
This guide provides hands-on examples to help developers quickly get started with DAPR's building blocks for microservices. It covers the core building blocks with practical examples that demonstrate common distributed application scenarios.

## Prerequisites
- DAPR CLI installed
- DAPR initialized (`dapr init`)
- Docker Desktop
- Programming language runtime (Python, JavaScript, .NET, Java, or Go)

## Quickstart 1: State Management

### Objective
Learn how to save, retrieve, and delete state using DAPR's state management building block.

### Step 1: Run the DAPR sidecar
```bash
dapr run --app-id myapp --dapr-http-port 3500
```

### Step 2: Save state
```bash
curl -X POST -H "Content-Type: application/json" -d '[{ "key": "name", "value": "Bruce Wayne"}]' http://localhost:3500/v1.0/state/statestore
```

### Step 3: Get state
```bash
curl http://localhost:3500/v1.0/state/statestore/name
```

### Step 4: Delete state
```bash
curl -X DELETE http://localhost:3500/v1.0/state/statestore/name
```

### Using SDKs

#### Python Example
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Save state
    client.state.save(
        store_name='statestore',
        key='name',
        value='Bruce Wayne'
    )

    # Get state
    response = client.state.get('statestore', 'name')
    print(response.data)

    # Delete state
    client.state.delete('statestore', 'name')
```

#### JavaScript Example
```javascript
import { DaprClient } from "@dapr/dapr";

const client = new DaprClient();

// Save state
await client.state.save("statestore", "name", "Bruce Wayne");

// Get state
const state = await client.state.get("statestore", "name");
console.log(state);

// Delete state
await client.state.delete("statestore", "name");
```

## Quickstart 2: Service Invocation

### Objective
Enable applications to communicate reliably and securely with other applications using DAPR's service invocation building block.

### Example: Invoking another service
```bash
# From your service, invoke another service named 'target-service'
curl -X POST http://localhost:3500/v1.0/invoke/target-service/method/endpoint
```

### Using SDKs

#### Python Example
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Invoke a method on another service
    response = client.invoke_method(
        app_id='target-service',
        method_name='endpoint',
        data={'message': 'Hello'},
        http_verb='POST'
    )
    print(response.data)
```

#### JavaScript Example
```javascript
import { DaprClient } from "@dapr/dapr";

const client = new DaprClient();

// Invoke a method on another service
const response = await client.invoker.invoke(
    "target-service",
    "endpoint",
    { message: "Hello" }
);
console.log(response);
```

## Quickstart 3: Publish and Subscribe

### Objective
Implement a loosely coupled messaging pattern where publishers send messages to a topic, and subscribers receive them.

### Example: Publishing a message
```bash
curl -X POST http://localhost:3500/v1.0/publish/pubsub/orders \
  -H "Content-Type: application/json" \
  -d '{"orderId": "123", "status": "created"}'
```

### Example: Subscribing to a topic
Applications need to implement an HTTP endpoint that DAPR will call when messages arrive:

```
POST http://<app-host>:<app-port>/orders
Content-Type: application/json

{
  "data": {
    "orderId": "123",
    "status": "created"
  },
  "topic": "orders",
  "pubsubname": "pubsub",
  "traceid": "00-63acd99a71bf231b27829f263fc28f10-5fa65a0e9d1ac018-01",
  "traceparent": "00-63acd99a71bf231b27829f263fc28f10-5fa65a0e9d1ac018-01",
  "tracestate": "",
  "datacontenttype": "application/json"
}
```

### Using SDKs

#### Python Example
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Publish a message
    client.publish_event(
        pubsub_name='pubsub',
        topic_name='orders',
        data={'orderId': '123', 'status': 'created'}
    )
```

#### JavaScript Example
```javascript
import { DaprClient } from "@dapr/dapr";

const client = new DaprClient();

// Publish a message
await client.pubsub.publish("pubsub", "orders", {
    orderId: "123",
    status: "created"
});
```

## Quickstart 4: Secrets Management

### Objective
Retrieve secrets from various secret stores in a unified way using DAPR's secrets building block.

### Example: Retrieving a secret
```bash
curl http://localhost:3500/v1.0/secrets/localsecretstore/mysecret
```

### Component Configuration (local-secret-store.yaml)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: localsecretstore
spec:
  type: secretstores.local.file
  version: v1
  metadata:
  - name: secretsFile
    value: secrets.json
  - name: nestedSeparator
    value: ":"
```

### Using SDKs

#### Python Example
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Get a secret
    secret_response = client.get_secret(
        store_name='localsecretstore',
        key='secret'
    )
    secret_value = secret_response.data['secret']
    print(f'Secret value: {secret_value}')
```

#### JavaScript Example
```javascript
import { DaprClient } from "@dapr/dapr";

const client = new DaprClient();

// Get a secret
const secret = await client.secret.get("localsecretstore", "secret");
console.log(`Secret value: ${secret.secret}`);
```

## Quickstart 5: Actors

### Objective
Build stateful and stateless services using the Actor pattern with DAPR's actors building block.

### Example: Invoking an actor method
```bash
curl -X POST http://localhost:3500/v1.0/actors/CounterActor/myactor/inc \
  -H "Content-Type: application/json" \
  -d '{"value": 1}'
```

### Using SDKs

#### Python Example
```python
from dapr.actor import ActorInterface, actormethod
from dapr.clients import DaprClient

class CounterActorInterface(ActorInterface):
    @actormethod(name="Inc")
    async def increment(self, value: int) -> int:
        pass

# In your service
with DaprClient() as client:
    # Invoke actor method
    response = client.invoke_actor(
        actor_type='CounterActor',
        actor_id='myactor',
        method='Inc',
        data={'value': 1}
    )
```

## Common Component Configurations

### Redis State Store
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

### Redis Pub/Sub
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

## Running Applications with DAPR

### Single Application
```bash
dapr run --app-id myapp --app-port 3000 -- python app.py
```

### Multi-App Run (using configuration file)
```bash
dapr run -f ./appconfig.yaml
```

### With Custom Components
```bash
dapr run --app-id myapp --resources-path ./components -- python app.py
```

## Troubleshooting Common Issues

### 1. DAPR Sidecar Not Starting
- Verify DAPR is initialized: `dapr init`
- Check Docker is running
- Verify available ports

### 2. Service Invocation Failures
- Check app IDs match between caller and callee
- Verify services are running with DAPR sidecars
- Check network connectivity

### 3. State Management Issues
- Verify component configuration files
- Check if the state store is accessible
- Ensure proper permissions

### 4. Pub/Sub Problems
- Verify topic names match
- Check if the pub/sub component is configured correctly
- Ensure subscribers are properly registered

### 5. Secret Retrieval Issues
- Verify component configuration
- Check if the secret store is accessible
- Ensure the secret key exists

## Best Practices

### 1. Component Naming
- Use consistent naming conventions
- Make names descriptive and meaningful
- Follow your organization's naming standards

### 2. Security
- Use secure secret stores in production
- Enable mTLS for service-to-service communication
- Implement proper access controls

### 3. Error Handling
- Implement proper error handling for DAPR API calls
- Use retry policies for transient failures
- Log errors appropriately for debugging

### 4. Resource Management
- Set appropriate resource limits for DAPR sidecars
- Monitor DAPR sidecar performance
- Use health checks for DAPR-enabled services
