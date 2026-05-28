# C4 Model - Deployment Diagram

## AISTRALE Deployment Architecture

This diagram shows how AISTRALE is deployed in a production environment.

```mermaid
C4Deployment
    title Deployment Diagram for AISTRALE

    Deployment_Node(cloud, "Cloud Provider", "AWS/GCP/Azure") {
        Deployment_Node(load_balancer, "Load Balancer", "NGINX/ALB", "Routes traffic to API instances")

        Deployment_Node(api_cluster, "API Cluster") {
            Deployment_Node(api1, "API Instance 1", "Docker Container", "FastAPI application")
            Deployment_Node(api2, "API Instance 2", "Docker Container", "FastAPI application")
            Deployment_Node(api3, "API Instance N", "Docker Container", "FastAPI application (scalable)")
        }

        Deployment_Node(web_cluster, "Web Cluster") {
            Deployment_Node(web1, "Web Instance 1", "Docker Container", "React SPA (Nginx)")
            Deployment_Node(web2, "Web Instance 2", "Docker Container", "React SPA (Nginx)")
        }

        Deployment_Node(db_cluster, "Database Cluster") {
            Deployment_Node(primary_db, "Primary DB", "PostgreSQL 17", "Primary database with pgvector")
            Deployment_Node(replica_db, "Replica DB", "PostgreSQL 17", "Read replica for scaling")
        }

        Deployment_Node(cache_cluster, "Cache Cluster") {
            Deployment_Node(redis1, "Redis Primary", "Redis", "Session storage")
            Deployment_Node(redis2, "Redis Replica", "Redis", "Session replication")
        }

        Deployment_Node(monitoring, "Monitoring Stack") {
            Deployment_Node(prometheus, "Prometheus", "Docker Container", "Metrics collection")
            Deployment_Node(grafana, "Grafana", "Docker Container", "Metrics visualization")
            Deployment_Node(jaeger, "Jaeger", "Docker Container", "Distributed tracing")
            Deployment_Node(loki, "Loki", "Docker Container", "Log aggregation")
            Deployment_Node(promtail, "Promtail", "Docker Container", "Log shipping")
            Deployment_Node(alertmanager, "Alertmanager", "Docker Container", "Alert management")
        }

        Deployment_Node(external, "External Services") {
            Deployment_Node(sentry, "Sentry", "SaaS", "Error tracking")
        }
    }

    Person(admin, "Administrator")
    Person(user, "LLM Engineer")

    System_Ext(hf, "HuggingFace Hub")
    System_Ext(openai, "OpenAI API")
    System_Ext(groq, "Groq API")
    System_Ext(anthropic, "Anthropic API")
    System_Ext(gemini, "Google Gemini API")

    Rel(admin, load_balancer, "Uses", "HTTPS")
    Rel(user, load_balancer, "Uses", "HTTPS")

    Rel(load_balancer, api_cluster, "Routes to", "HTTP")
    Rel(load_balancer, web_cluster, "Serves", "HTTPS")

    Rel(api1, primary_db, "Reads/writes", "SQL")
    Rel(api2, primary_db, "Reads/writes", "SQL")
    Rel(api1, replica_db, "Reads from", "SQL")
    Rel(api2, replica_db, "Reads from", "SQL")

    Rel(api1, redis1, "Stores sessions", "Redis Protocol")
    Rel(api2, redis1, "Stores sessions", "Redis Protocol")
    Rel(redis1, redis2, "Replicates to")

    Rel(api1, prometheus, "Exports metrics", "HTTP")
    Rel(api2, prometheus, "Exports metrics", "HTTP")
    Rel(api1, jaeger, "Sends traces", "HTTP")
    Rel(api2, jaeger, "Sends traces", "HTTP")
    Rel(api1, loki, "Sends logs", "HTTP")
    Rel(api2, loki, "Sends logs", "HTTP")
    Rel(api1, sentry, "Sends errors", "HTTPS")
    Rel(api2, sentry, "Sends errors", "HTTPS")

    Rel(promtail, loki, "Ships logs", "HTTP")
    Rel(prometheus, grafana, "Provides data", "HTTP")
    Rel(prometheus, alertmanager, "Sends alerts", "HTTP")

    Rel(api1, hf, "Runs inference", "HTTPS")
    Rel(api1, openai, "Runs inference", "HTTPS")
    Rel(api1, groq, "Runs inference", "HTTPS")
    Rel(api1, anthropic, "Runs inference", "HTTPS")
    Rel(api1, gemini, "Runs inference", "HTTPS")

    UpdateElementStyle(api1, $bgColor="#1565C0", $fontColor="#FFFFFF")
    UpdateElementStyle(api2, $bgColor="#1565C0", $fontColor="#FFFFFF")
    UpdateElementStyle(primary_db, $bgColor="#388E3C")
    UpdateElementStyle(redis1, $bgColor="#FF8F00")
```

## Deployment Architecture

### Load Balancing

- **Load Balancer**: Routes traffic to multiple API instances
- **Health Checks**: Monitors API instance health
- **SSL Termination**: Handles HTTPS at the edge

### API Cluster

- **Horizontal Scaling**: Multiple API instances for high availability
- **Stateless Design**: Each instance is independent
- **Session Storage**: Sessions stored in Redis (shared across instances)

### Web Cluster

- **Static Assets**: React SPA served via Nginx
- **CDN Ready**: Can be deployed to CDN for global distribution
- **Multiple Instances**: For redundancy

### Database Cluster

- **Primary/Replica**: Write to primary, read from replicas
- **pgvector Extension**: For future vector search capabilities
- **Backup Strategy**: Automated backups

### Cache Cluster

- **Redis Primary/Replica**: High availability session storage
- **Replication**: Automatic failover

### Monitoring Stack

- **Prometheus**: Collects metrics from all API instances
- **Grafana**: Visualizes metrics and creates dashboards
- **Jaeger**: Distributed tracing across services
- **Loki + Promtail**: Centralized log aggregation
- **Alertmanager**: Manages alerts and notifications

## Scalability

- **API Instances**: Can scale horizontally based on load
- **Database Replicas**: Can add read replicas for scaling reads
- **Redis Cluster**: Can scale Redis for higher session capacity
- **Stateless Design**: Enables easy horizontal scaling

## High Availability

- **Multiple API Instances**: No single point of failure
- **Database Replication**: Automatic failover
- **Redis Replication**: Session persistence across failures
- **Load Balancer**: Distributes load and handles failures

## Security

- **HTTPS**: All external communication encrypted
- **Session Security**: HTTP-only cookies, Redis-backed
- **Token Encryption**: Tokens encrypted at rest
- **Network Isolation**: Internal services not exposed externally
