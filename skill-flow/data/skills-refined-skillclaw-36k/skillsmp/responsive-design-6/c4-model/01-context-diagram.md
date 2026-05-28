# C4 Model - Context Diagram

## AISTRALE System Context

This diagram shows AISTRALE in the context of its users and external systems.

```mermaid
C4Context
    title System Context Diagram for AISTRALE

    Person(admin, "Administrator", "Manages users, security, and system configuration")
    Person(user, "LLM Engineer", "Uses AISTRALE to run inference, manage prompts, and analyze telemetry")

    System(aistrale, "AISTRALE", "LLM Engineering Platform - Turn AI from a black box into an engineered system")

    System_Ext(hf, "HuggingFace Hub", "Open-source model repository and inference API")
    System_Ext(openai, "OpenAI API", "GPT models and inference service")
    System_Ext(groq, "Groq API", "Fast LLM inference service")
    System_Ext(anthropic, "Anthropic API", "Claude models and inference service")
    System_Ext(gemini, "Google Gemini API", "Gemini models and inference service")

    System_Ext(sentry, "Sentry", "Error tracking and monitoring")
    System_Ext(grafana, "Grafana", "Metrics visualization and dashboards")
    System_Ext(jaeger, "Jaeger", "Distributed tracing")
    System_Ext(prometheus, "Prometheus", "Metrics collection")
    System_Ext(loki, "Loki", "Log aggregation")

    Rel(admin, aistrale, "Manages system", "HTTPS")
    Rel(user, aistrale, "Runs inference, manages prompts/tokens, views analytics", "HTTPS")

    Rel(aistrale, hf, "Runs model inference", "HTTPS/API")
    Rel(aistrale, openai, "Runs model inference", "HTTPS/API")
    Rel(aistrale, groq, "Runs model inference", "HTTPS/API")
    Rel(aistrale, anthropic, "Runs model inference", "HTTPS/API")
    Rel(aistrale, gemini, "Runs model inference", "HTTPS/API")

    Rel(aistrale, sentry, "Sends error reports", "HTTPS")
    Rel(aistrale, prometheus, "Exports metrics", "HTTP")
    Rel(aistrale, jaeger, "Sends traces", "HTTP")
    Rel(aistrale, loki, "Sends logs", "HTTP")
    Rel(prometheus, grafana, "Provides metrics data", "HTTP")

    UpdateElementStyle(aistrale, $bgColor="#1565C0", $fontColor="#FFFFFF")
    UpdateElementStyle(admin, $bgColor="#FF8F00")
    UpdateElementStyle(user, $bgColor="#00ACC1")
```

## Description

**AISTRALE** is an LLM engineering platform that provides:

- Multi-provider LLM inference (HuggingFace, OpenAI, Groq, Anthropic, Gemini)
- Prompt template management
- Token/credential management with encryption
- Telemetry and cost analytics
- Security audit logging
- Comprehensive observability (metrics, logs, traces)

**Users:**

- **Administrators**: Manage users, security settings, encryption keys, and view audit logs
- **LLM Engineers**: Run inference, manage prompts and tokens, view analytics

**External Systems:**

- **LLM Providers**: Various AI model providers for inference
- **Observability Stack**: Prometheus, Grafana, Jaeger, Loki, Sentry for monitoring and debugging
