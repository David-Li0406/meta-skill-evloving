# C4 Model - Container Diagram

## AISTRALE Container Architecture

This diagram shows the high-level technical building blocks (containers) that make up AISTRALE.

```mermaid
C4Container
    title Container Diagram for AISTRALE

    Person(admin, "Administrator")
    Person(user, "LLM Engineer")

    System_Boundary(aistrale, "AISTRALE") {
        Container(webapp, "Web Application", "React, TypeScript, Vite", "Single-page application providing UI for LLM engineering")
        Container(api, "API Application", "FastAPI, Python 3.11", "RESTful API providing business logic and LLM integration")
        ContainerDb(database, "Database", "PostgreSQL 17 with pgvector", "Stores users, tokens, prompts, telemetry, audit logs, encryption keys")
        Container(cache, "Cache", "Redis", "Session storage and caching")
    }

    System_Ext(hf, "HuggingFace Hub")
    System_Ext(openai, "OpenAI API")
    System_Ext(groq, "Groq API")
    System_Ext(anthropic, "Anthropic API")
    System_Ext(gemini, "Google Gemini API")

    System_Ext(prometheus, "Prometheus")
    System_Ext(grafana, "Grafana")
    System_Ext(jaeger, "Jaeger")
    System_Ext(loki, "Loki")
    System_Ext(sentry, "Sentry")

    Rel(admin, webapp, "Uses", "HTTPS")
    Rel(user, webapp, "Uses", "HTTPS")

    Rel(webapp, api, "Makes API calls", "HTTPS/REST")

    Rel(api, database, "Reads from and writes to", "SQL")
    Rel(api, cache, "Stores sessions", "Redis Protocol")

    Rel(api, hf, "Runs inference", "HTTPS/API")
    Rel(api, openai, "Runs inference", "HTTPS/API")
    Rel(api, groq, "Runs inference", "HTTPS/API")
    Rel(api, anthropic, "Runs inference", "HTTPS/API")
    Rel(api, gemini, "Runs inference", "HTTPS/API")

    Rel(api, prometheus, "Exports metrics", "HTTP")
    Rel(api, jaeger, "Sends traces", "HTTP")
    Rel(api, loki, "Sends logs", "HTTP")
    Rel(api, sentry, "Sends errors", "HTTPS")
    Rel(prometheus, grafana, "Provides data", "HTTP")

    UpdateElementStyle(webapp, $bgColor="#1565C0", $fontColor="#FFFFFF")
    UpdateElementStyle(api, $bgColor="#1565C0", $fontColor="#FFFFFF")
    UpdateElementStyle(database, $bgColor="#388E3C")
    UpdateElementStyle(cache, $bgColor="#FF8F00")
```

## Container Descriptions

### Web Application (Frontend)

- **Technology**: React 18, TypeScript 5, Vite, Tailwind CSS
- **Purpose**: Provides the user interface for all AISTRALE features
- **Responsibilities**:
  - User authentication UI
  - Inference chat interface
  - Prompt template management
  - Token management
  - Telemetry and analytics visualization
  - Admin controls (for administrators)

### API Application (Backend)

- **Technology**: FastAPI, Python 3.11, SQLModel, Pydantic
- **Purpose**: Core business logic and LLM provider integration
- **Responsibilities**:
  - Session-based authentication
  - LLM inference orchestration
  - Token encryption/decryption
  - Telemetry tracking
  - Cost calculation
  - Security audit logging
  - Encryption key rotation
  - Observability (metrics, logs, traces)

### Database

- **Technology**: PostgreSQL 17 with pgvector extension
- **Purpose**: Persistent data storage
- **Stores**:
  - Users and authentication data
  - Encrypted API tokens
  - Prompt templates
  - Telemetry records
  - Security audit logs
  - Encryption keys

### Cache

- **Technology**: Redis
- **Purpose**: Session storage and caching
- **Stores**:
  - User sessions (HTTP-only cookies)
  - Temporary data

## Technology Decisions

- **FastAPI**: High-performance async Python framework
- **PostgreSQL with pgvector**: Future-proof for vector embeddings
- **Redis**: Fast session storage for scalability
- **React + TypeScript**: Type-safe, modern frontend
- **Session-based auth**: More secure than JWT for web apps
