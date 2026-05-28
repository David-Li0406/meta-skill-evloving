# AISTRALE Architecture Documentation

## C4 Model Compliance

AISTRALE follows the C4 Model for software architecture documentation, providing clear visualizations at multiple levels of abstraction.

## Architecture Overview

AISTRALE is an LLM engineering platform that provides:

- Multi-provider LLM inference (HuggingFace, OpenAI, Groq, Anthropic, Gemini)
- Prompt template management
- Secure token/credential management with encryption
- Comprehensive telemetry and cost analytics
- Security audit logging
- Full observability stack (metrics, logs, traces)

## C4 Model Diagrams

### Level 1: Context Diagram

**File**: `01-context-diagram.md`

Shows AISTRALE in the context of:

- **Users**: Administrators and LLM Engineers
- **External Systems**: LLM providers (HuggingFace, OpenAI, Groq, Anthropic, Gemini)
- **Observability Services**: Prometheus, Grafana, Jaeger, Loki, Sentry

**Key Relationships**:

- Users interact with AISTRALE via HTTPS
- AISTRALE calls LLM provider APIs for inference
- AISTRALE sends observability data to monitoring services

### Level 2: Container Diagram

**File**: `02-container-diagram.md`

Shows the high-level technical building blocks:

- **Web Application**: React SPA (frontend)
- **API Application**: FastAPI backend
- **Database**: PostgreSQL 17 with pgvector
- **Cache**: Redis for sessions

**Technology Stack**:

- Frontend: React 18, TypeScript 5, Vite, Tailwind CSS
- Backend: FastAPI, Python 3.11, SQLModel, Pydantic
- Database: PostgreSQL 17 with pgvector extension
- Cache: Redis for session storage

### Level 3: Component Diagram

**File**: `03-component-diagram.md`

Shows how the API application is decomposed into components:

- **API Routers**: Auth, Users, Tokens, Inference, Prompts, Telemetry, Security Audit, Admin
- **Services**: Auth, Inference, Pricing, Key Rotation, Security Audit
- **LLM Providers**: Factory pattern with provider implementations
- **Infrastructure**: Session middleware, Observability, Scheduler

**Design Patterns**:

- Factory Pattern: Provider factory creates LLM provider instances
- Strategy Pattern: Different providers implement the same interface
- Repository Pattern: Database access through SQLModel
- Middleware Pattern: Session and observability middleware

### Level 4: Deployment Diagram

**File**: `04-deployment-diagram.md`

Shows how AISTRALE is deployed:

- **Load Balancer**: Routes traffic to API instances
- **API Cluster**: Horizontally scalable API instances
- **Web Cluster**: Multiple web instances for redundancy
- **Database Cluster**: Primary/replica setup
- **Cache Cluster**: Redis primary/replica
- **Monitoring Stack**: Prometheus, Grafana, Jaeger, Loki, Alertmanager

**Scalability**:

- Horizontal scaling of API instances
- Database read replicas
- Redis clustering
- Stateless design enables easy scaling

## Architecture Principles

### 1. Separation of Concerns

- Frontend handles UI/UX
- Backend handles business logic
- Database handles persistence
- Cache handles session storage

### 2. Provider Abstraction

- All LLM providers implement the same interface
- Easy to add new providers
- Consistent error handling and telemetry

### 3. Security First

- Session-based authentication (HTTP-only cookies)
- Token encryption at rest
- Encryption key rotation
- Security audit logging
- Role-based access control

### 4. Observability

- Structured logging (structlog)
- Prometheus metrics
- OpenTelemetry distributed tracing
- Sentry error tracking
- Loki log aggregation

### 5. Scalability

- Stateless API design
- Horizontal scaling support
- Database read replicas
- Redis session storage

## Key Architectural Decisions

### Why FastAPI?

- High performance async framework
- Automatic API documentation
- Type safety with Pydantic
- Python ecosystem for ML/AI

### Why PostgreSQL with pgvector?

- Future-proof for vector embeddings
- ACID compliance
- Mature ecosystem
- pgvector extension for similarity search

### Why Session-Based Auth?

- More secure than JWT for web apps
- Server-side session control
- Easy revocation
- HTTP-only cookies prevent XSS

### Why Provider Abstraction?

- Easy to add new LLM providers
- Consistent interface
- Centralized error handling
- Unified telemetry

### Why Observability Stack?

- Full visibility into system behavior
- Debug production issues
- Performance optimization
- Cost tracking and analytics

## Data Flow

### Inference Request Flow

1. User submits inference request via Web App
2. Web App calls API `/api/inference/run`
3. API validates request and user session
4. Inference Service gets provider from factory
5. Provider calls external LLM API
6. Response is logged to telemetry
7. Cost is calculated
8. Response returned to user

### Authentication Flow

1. User submits credentials via Web App
2. Web App calls API `/api/auth/login`
3. API validates credentials
4. Session created in Redis
5. HTTP-only cookie set
6. User info returned

### Key Rotation Flow

1. Admin triggers key rotation via Admin API
2. Key Rotation Service generates new key
3. All tokens re-encrypted with new key
4. Old key deactivated
5. Audit log entry created

## Security Architecture

### Authentication

- Session-based with HTTP-only cookies
- Password hashing with bcrypt
- Session stored in Redis
- Automatic session expiration

### Authorization

- Role-based access control (RBAC)
- Admin and User roles
- Route-level permission checks
- Deny-by-default policy

### Data Protection

- Token encryption at rest (Fernet)
- Encryption key rotation
- Security audit logging
- Input validation (Pydantic)

## Observability Architecture

### Logging

- Structured logging with structlog
- JSON format for parsing
- Correlation IDs for tracing
- Log levels: DEBUG, INFO, WARNING, ERROR

### Metrics

- Prometheus metrics collection
- Custom business metrics
- System metrics
- LLM-specific metrics (tokens, cost, latency)

### Tracing

- OpenTelemetry distributed tracing
- Trace all LLM API calls
- Request/response logging
- Performance analysis

### Error Tracking

- Sentry integration
- Error context and stack traces
- Alerting on critical errors

## Deployment Architecture

### Development

- Docker Compose for local development
- All services in containers
- Hot reload for development

### Production

- Containerized deployment
- Load balancer for traffic distribution
- Horizontal scaling
- Database replication
- Redis clustering
- Monitoring stack

## Future Considerations

### Vector Search

- pgvector extension ready
- Can add vector embeddings for prompts
- Semantic search capabilities

### Additional Providers

- Easy to add via provider abstraction
- Just implement the interface
- Factory handles instantiation

### Microservices

- Current monolith can be split
- Service boundaries already defined
- API-first design enables this

## Compliance Checklist

- [x] Context diagram created
- [x] Container diagram created
- [x] Component diagram created
- [x] Deployment diagram created
- [x] Architecture principles documented
- [x] Technology decisions documented
- [x] Data flows documented
- [x] Security architecture documented
- [x] Observability architecture documented

## References

- [C4 Model](https://c4model.com/)
- [Mermaid Diagrams](https://mermaid.js.org/)
