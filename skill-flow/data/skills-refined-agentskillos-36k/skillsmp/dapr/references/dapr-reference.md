# DAPR Reference Materials

## Common Configuration Properties

### DAPR Sidecar Annotations
- `dapr.io/enabled`: Enable DAPR sidecar injection (true/false)
- `dapr.io/app-id`: Unique identifier for the application
- `dapr.io/app-port`: Port the application is listening on
- `dapr.io/config`: Name of DAPR configuration resource
- `dapr.io/components`: Comma-separated list of components to load
- `dapr.io/log-level`: Logging level (debug, info, warn, error)
- `dapr.io/sidecar-cpu-limit`: CPU limit for DAPR sidecar
- `dapr.io/sidecar-memory-limit`: Memory limit for DAPR sidecar
- `dapr.io/sidecar-cpu-request`: CPU request for DAPR sidecar
- `dapr.io/sidecar-memory-request`: Memory request for DAPR sidecar

### State Store Metadata
- `redisHost`: Redis server host and port
- `redisPassword`: Redis server password
- `actorStateStore`: Whether to use this store for actor state
- `keyPrefix`: Prefix for keys in the store
- `ttlInSeconds`: Default TTL for items in the store

### Pub/Sub Metadata
- `redisHost`: Redis server host and port
- `redisPassword`: Redis server password
- `enableTLS`: Whether to enable TLS for Redis connection
- `consumerID`: Consumer group ID for pub/sub

## DAPR Commands Cheat Sheet

### Local Development
```bash
# Run application with DAPR sidecar
dapr run --app-id myapp --app-port 8080 node app.js

# List running DAPR instances
dapr list

# Stop DAPR sidecar
dapr stop --app-id myapp

# Stop all DAPR instances
dapr stop --all

# Check DAPR version
dapr --version

# Get DAPR configuration
dapr configurations

# Get DAPR components
dapr components
```

### Kubernetes Operations
```bash
# Check DAPR status in Kubernetes
dapr status -k

# Get DAPR configurations in Kubernetes
dapr configurations -k

# Get DAPR components in Kubernetes
dapr components -k

# Get DAPR dashboard
dapr dashboard

# Publish a test message
curl -X POST http://localhost:3500/v1.0/publish/pubsub/mytopic -H "Content-Type: application/json" -d '{"message": "Hello DAPR"}'
```

## API Endpoints

### Service Invocation
- `POST /v1.0/invoke/{appId}/method/{method}`: Invoke a method on another service

### State Management
- `POST /v1.0/state/{storeName}`: Save state
- `GET /v1.0/state/{storeName}/{key}`: Get state
- `DELETE /v1.0/state/{storeName}/{key}`: Delete state
- `POST /v1.0/state/{storeName}/bulk`: Get bulk state
- `POST /v1.0/state/{storeName}/transaction`: Execute state transaction

### Pub/Sub
- `POST /v1.0/publish/{pubsubname}/{topic}`: Publish a message to a topic

### Secrets
- `GET /v1.0/secrets/{secretstorename}/{key}`: Get a secret

### Actors
- `POST /v1.0/actors/{actorType}/{actorId}/method/{method}`: Invoke an actor method
- `GET /v1.0/actors/{actorType}/{actorId}/state/{key}`: Get actor state
- `POST /v1.0/actors/{actorType}/{actorId}/state`: Save actor state

### Metadata
- `GET /v1.0/metadata`: Get DAPR metadata

## Component Types

### State Stores
- `state.redis`: Redis-based state store
- `state.postgresql`: PostgreSQL-based state store
- `state.mongodb`: MongoDB-based state store
- `state.azure.blobstorage`: Azure Blob Storage
- `state.aws.dynamodb`: AWS DynamoDB
- `state.gcp.firestore`: Google Cloud Firestore

### Pub/Sub Brokers
- `pubsub.redis`: Redis-based pub/sub
- `pubsub.nats`: NATS-based pub/sub
- `pubsub.rabbitmq`: RabbitMQ-based pub/sub
- `pubsub.azure.servicebus`: Azure Service Bus
- `pubsub.aws.snssqs`: AWS SNS/SQS
- `pubsub.gcp.pubsub`: Google Cloud Pub/Sub

### Secret Stores
- `secretstores.kubernetes`: Kubernetes secret store
- `secretstores.hashicorp.vault`: HashiCorp Vault
- `secretstores.azure.keyvault`: Azure Key Vault
- `secretstores.aws.secretmanager`: AWS Secrets Manager
- `secretstores.gcp.secretmanager`: Google Cloud Secret Manager

## Configuration Options

### Tracing
- `samplingRate`: Trace sampling rate (0.0 to 1.0)
- `stdout`: Whether to output traces to stdout
- `otel.endpointAddress`: OpenTelemetry collector endpoint
- `otel.isSecure`: Whether to use TLS for OTel connection
- `otel.protocol`: Protocol for OTel (http or grpc)

### Metrics
- `enabled`: Whether metrics are enabled
- `rules`: Custom metric rules
- `recordErrorCodes`: Whether to record error codes in metrics

## Health Checks

### DAPR Health Endpoints
- `GET /v1.0/healthz`: DAPR sidecar health check
- `GET /v1.0/virtual-actors/runtime/healthz`: Actor runtime health check

## Best Practices by Scenario

### High-Throughput Scenarios
- Use Redis cluster for state management
- Configure connection pooling for state stores
- Use appropriate partitioning strategies for pub/sub topics
- Monitor and tune DAPR sidecar resource allocation

### Low-Latency Scenarios
- Use in-memory state stores when possible
- Minimize network hops between services
- Use direct service invocation when appropriate
- Optimize component configuration for performance

### Security-Critical Scenarios
- Enable mTLS for all service-to-service communication
- Use secure secret stores with proper access controls
- Implement proper ACLs and access policies
- Enable audit logging for all operations
- Regularly rotate certificates and secrets

### Multi-Cloud Scenarios
- Use platform-agnostic component configurations
- Implement proper configuration management for different environments
- Use consistent naming conventions across clouds
- Ensure portability by avoiding cloud-specific features where possible

## Common Anti-Patterns to Avoid

1. **Hardcoded Service Addresses**: Always use DAPR service invocation instead of direct HTTP calls
2. **Direct State Store Connections**: Use DAPR's state management API instead of connecting directly to state stores
3. **Inconsistent Component Naming**: Use consistent naming for components across environments
4. **Missing Health Checks**: Always implement health checks for DAPR-enabled services
5. **Insufficient Error Handling**: Handle DAPR API errors appropriately
6. **No Circuit Breaking**: Leverage DAPR's built-in circuit breaking and retry policies
7. **Overlooked Security**: Always enable security features in production
8. **Poor Resource Management**: Set appropriate resource limits for DAPR sidecars
