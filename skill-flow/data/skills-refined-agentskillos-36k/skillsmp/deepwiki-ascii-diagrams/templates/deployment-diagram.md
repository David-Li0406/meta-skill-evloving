# Deployment Diagram Templates

Deployment diagrams show the physical/cloud deployment architecture, how systems are distributed across infrastructure, and how different components are deployed to servers, containers, or cloud platforms.

---

## Template 1: Traditional Monolithic Deployment

**Purpose**: Show deployment of a monolithic application with load balancing and databases

```
┌─────────────────────────────────────────────────────────────────┐
│                    Production Environment                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            Cloud Provider (AWS/Azure/GCP)              │   │
│  │                                                          │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │          Load Balancer (ALB/NLB)                   │ │   │
│  │  │          - SSL/TLS termination                     │ │   │
│  │  │          - Health checks                           │ │   │
│  │  └────────────────┬───────────────────────────────────┘ │   │
│  │                   │                                       │   │
│  │     ┌─────────────┼─────────────┐                        │   │
│  │     │             │             │                        │   │
│  │     ▼             ▼             ▼                        │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐               │   │
│  │  │ Web App │  │ Web App │  │ Web App │               │   │
│  │  │Instance │  │Instance │  │Instance │               │   │
│  │  │  (EC2)  │  │  (EC2)  │  │  (EC2)  │               │   │
│  │  │ Port 80 │  │ Port 80 │  │ Port 80 │               │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘               │   │
│  │       │            │            │                     │   │
│  │       └────────────┼────────────┘                     │   │
│  │                    │                                  │   │
│  │                    ▼                                  │   │
│  │       ┌────────────────────────────┐                 │   │
│  │       │   Database Cluster         │                 │   │
│  │       │   (RDS - Multi-AZ)         │                 │   │
│  │       │                            │                 │   │
│  │       │ ┌──────────────────────┐  │                 │   │
│  │       │ │ Primary Database     │  │                 │   │
│  │       │ │ (PostgreSQL)         │  │                 │   │
│  │       │ └──────────────────────┘  │                 │   │
│  │       │ ┌──────────────────────┐  │                 │   │
│  │       │ │ Read Replica 1       │  │                 │   │
│  │       │ │ (Standby)            │  │                 │   │
│  │       │ └──────────────────────┘  │                 │   │
│  │       │ ┌──────────────────────┐  │                 │   │
│  │       │ │ Read Replica 2       │  │                 │   │
│  │       │ │ (Analytics)          │  │                 │   │
│  │       │ └──────────────────────┘  │                 │   │
│  │       └────────────────────────────┘                 │   │
│  │                                                       │   │
│  │  ┌─────────────────────────────────────────────────┐ │   │
│  │  │ Cache Layer (ElastiCache - Redis)              │ │   │
│  │  │ - Session storage                              │ │   │
│  │  │ - Query result caching                         │ │   │
│  │  └─────────────────────────────────────────────────┘ │   │
│  │                                                        │   │
│  │  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │   │
│  │  ┃ Object Storage (S3)                           ┃ │   │
│  │  ┃ - Product images                              ┃ │   │
│  │  ┃ - User uploads                                ┃ │   │
│  │  ┃ - Backup files                                ┃ │   │
│  │  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │   │
│  │                                                        │   │
│  │  ┌─────────────────────────────────────────────────┐ │   │
│  │  │ Monitoring & Logging                            │ │   │
│  │  │ - CloudWatch / Application Insights            │ │   │
│  │  │ - ELK Stack / Datadog                          │ │   │
│  │  │ - Alerting & Dashboards                        │ │   │
│  │  └─────────────────────────────────────────────────┘ │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            External Services                             │   │
│  │                                                          │   │
│  │  ┌──────────────┐     ┌──────────────┐                 │   │
│  │  │ Payment API  │     │ Email Service│                 │   │
│  │  │ (Stripe)     │     │ (SendGrid)   │                 │   │
│  │  └──────────────┘     └──────────────┘                 │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

[Monolithic deployment shows load-balanced instances with clustered database and caching]
```

### Key Elements
- **Load Balancer**: Distributes traffic across instances
- **Application Instances**: Multiple identical copies for high availability
- **Database Cluster**: Primary with replicas for failover and read scaling
- **Cache Layer**: Distributed cache for session and query results
- **Object Storage**: Scalable storage for static assets
- **Monitoring**: Observability across all components

---

## Template 2: Microservices Container Deployment (Kubernetes)

**Purpose**: Show deployment of microservices in Kubernetes

```
┌──────────────────────────────────────────────────────────────────┐
│                  Kubernetes Cluster (EKS/AKS/GKE)                │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Ingress Controller (AWS ALB / NGINX)                       │  │
│  │ - TLS/SSL termination                                      │  │
│  │ - Request routing                                          │  │
│  └────────────────┬───────────────────────────────────────────┘  │
│                   │                                                │
│  ┌────────────────┴─────────────────────────────────────────┐   │
│  │              Worker Nodes (EC2 Instances)                │   │
│  │                                                           │   │
│  │  ┌──────────────────┐    ┌──────────────────┐           │   │
│  │  │ Node 1           │    │ Node 2           │           │   │
│  │  │ (2 CPU, 8GB RAM) │    │ (2 CPU, 8GB RAM) │           │   │
│  │  │                  │    │                  │           │   │
│  │  │ ┌──────────────┐ │    │ ┌──────────────┐ │           │   │
│  │  │ │ API Gateway  │ │    │ │ User Service │ │           │   │
│  │  │ │ Pod          │ │    │ │ Pod          │ │           │   │
│  │  │ │ (3 replicas) │ │    │ │ (2 replicas) │ │           │   │
│  │  │ │              │ │    │ │              │ │           │   │
│  │  │ │ Requests: 100│ │    │ │ Requests: 50 │ │           │   │
│  │  │ │ Limit: 200   │ │    │ │ Limit: 100   │ │           │   │
│  │  │ └──────────────┘ │    │ └──────────────┘ │           │   │
│  │  │                  │    │                  │           │   │
│  │  │ ┌──────────────┐ │    │ ┌──────────────┐ │           │   │
│  │  │ │ Order Service│ │    │ │ Product Svc  │ │           │   │
│  │  │ │ Pod          │ │    │ │ Pod          │ │           │   │
│  │  │ │ (2 replicas) │ │    │ │ (3 replicas) │ │           │   │
│  │  │ └──────────────┘ │    │ └──────────────┘ │           │   │
│  │  │                  │    │                  │           │   │
│  │  │ ┌──────────────┐ │    │ ┌──────────────┐ │           │   │
│  │  │ │ Prometheus   │ │    │ │ Fluentd      │ │           │   │
│  │  │ │ (Metrics)    │ │    │ │ (Logs)       │ │           │   │
│  │  │ └──────────────┘ │    │ └──────────────┘ │           │   │
│  │  └──────────────────┘    └──────────────────┘           │   │
│  │                                                           │   │
│  │  ┌──────────────────┐    ┌──────────────────┐           │   │
│  │  │ Node 3           │    │ Node 4           │           │   │
│  │  │ (GPU, 16GB RAM)  │    │ (2 CPU, 8GB RAM) │           │   │
│  │  │                  │    │                  │           │   │
│  │  │ ┌──────────────┐ │    │ ┌──────────────┐ │           │   │
│  │  │ │ ML Service   │ │    │ │ Cache        │ │           │   │
│  │  │ │ Pod          │ │    │ │ (Redis)      │ │           │   │
│  │  │ │ (1 replica)  │ │    │ │ (1 replica)  │ │           │   │
│  │  │ └──────────────┘ │    │ └──────────────┘ │           │   │
│  │  └──────────────────┘    └──────────────────┘           │   │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Persistent Storage                                         │  │
│  │                                                            │  │
│  │ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │  │
│  │ │ Database     │  │ Message      │  │ Object Store │     │  │
│  │ │ (RDS/Cosmos) │  │ Queue (SQS)  │  │ (S3/Blob)    │     │  │
│  │ └──────────────┘  └──────────────┘  └──────────────┘     │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Control Plane (Managed by Cloud Provider)                 │  │
│  │ - API Server                                              │  │
│  │ - etcd (State storage)                                    │  │
│  │ - Scheduler & Controller Manager                          │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘

[Kubernetes deployment shows multiple services across nodes with persistent storage]
```

### Key Elements
- **Ingress Controller**: Entry point for external traffic
- **Worker Nodes**: VMs running multiple pods
- **Pods**: Containerized service instances with resource requests/limits
- **Service Discovery**: Kubernetes service DNS for inter-pod communication
- **Persistent Storage**: External databases and storage services
- **Control Plane**: Managed Kubernetes control infrastructure

---

## Template 3: Serverless/Function Deployment

**Purpose**: Show deployment using serverless functions

```
┌─────────────────────────────────────────────────────────────┐
│              Serverless Architecture (AWS/Azure)             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ API Gateway                                          │  │
│  │ - REST/HTTP endpoints                               │  │
│  │ - Request validation & transformation               │  │
│  └─────────────────┬──────────────────────────────────┘  │
│                    │                                       │
│        ┌───────────┼───────────┬──────────────┐          │
│        │           │           │              │          │
│        ▼           ▼           ▼              ▼          │
│  ┌─────────────┐ ┌─────────┐ ┌──────────┐ ┌─────────┐  │
│  │ Lambda Fn   │ │Lambda   │ │ Lambda   │ │ Lambda  │  │
│  │ GetProducts │ │CreateOrd│ │ Auth     │ │ Webhook │  │
│  │             │ │         │ │ Verifier │ │ Handler │  │
│  │ Memory: 512 │ │Memory:  │ │Memory:256│ │Memory:  │  │
│  │ Timeout: 30 │ │1024     │ │Timeout:5 │ │128      │  │
│  │             │ │Timeout: │ │          │ │Timeout:5│  │
│  │ Concurrent: │ │60       │ │          │ │         │  │
│  │ Reserved 50 │ │Resvd:25 │ │Resvd: 10 │ │Resvd: 5 │  │
│  └──────┬──────┘ └────┬────┘ └────┬─────┘ └────┬────┘  │
│         │             │            │            │        │
│         └─────────────┼────────────┼────────────┘        │
│                       │            │                     │
│         ┌─────────────┴───┬────────┴──────┐              │
│         │                 │               │              │
│         ▼                 ▼               ▼              │
│   ┌──────────────┐  ┌─────────────┐  ┌───────────┐     │
│   │ CloudWatch   │  │ SNS/SQS     │  │ DynamoDB  │     │
│   │ Events       │  │ (Messaging) │  │ (Database)│     │
│   │ (Triggers)   │  │             │  │           │     │
│   └──────────────┘  └─────────────┘  └───────────┘     │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Event Sources                                    │  │
│  │                                                  │  │
│  │  ┌──────────┐ ┌────────┐ ┌───────┐ ┌────────┐  │  │
│  │  │ S3       │ │ RDS    │ │ HTTP  │ │ Stripe │  │  │
│  │  │ Events   │ │ Events │ │ API   │ │ Webhook│  │  │
│  │  └──────────┘ └────────┘ └───────┘ └────────┘  │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Storage Layer                                    │  │
│  │                                                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │  │
│  │  │ S3       │  │ RDS      │  │ ElastiCache  │  │  │
│  │  │ (Objects)│  │ (SQL)    │  │ (Cache)      │  │  │
│  │  └──────────┘  └──────────┘  └──────────────┘  │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Monitoring                                       │  │
│  │ - CloudWatch Logs                               │  │
│  │ - X-Ray Tracing                                 │  │
│  │ - Custom Metrics                                │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘

[Serverless deployment shows functions triggered by various events with managed services]
```

### Key Elements
- **API Gateway**: Entry point for HTTP requests
- **Lambda Functions**: Serverless compute units with resource limits
- **Event Sources**: S3, databases, HTTP APIs, webhooks
- **Managed Services**: DynamoDB, RDS, ElastiCache for data persistence
- **Monitoring**: Automatic logging and tracing with CloudWatch/X-Ray
- **Auto-scaling**: Automatic scaling based on demand (no manual provisioning)

---

## Template 4: Hybrid Cloud Deployment

**Purpose**: Show deployment across multiple cloud providers

```
┌──────────────────────────────────────────────────────────────┐
│              Hybrid Cloud Architecture                        │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              On-Premises Data Center                   │  │
│  │                                                         │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │ Firewall & VPN                                  │ │  │
│  │  │ - VPN Gateway to Cloud                          │ │  │
│  │  │ - DDoS Protection                               │ │  │
│  │  └──────────────┬───────────────────────────────────┘ │  │
│  │                │                                       │  │
│  │  ┌─────────────▼───────────────────────────────────┐  │  │
│  │  │ Legacy Applications                            │  │  │
│  │  │                                                │  │  │
│  │  │  ┌──────────┐      ┌──────────────┐           │  │  │
│  │  │  │ ERP      │      │ CRM          │           │  │  │
│  │  │  │ System   │      │ System       │           │  │  │
│  │  │  └──────────┘      └──────────────┘           │  │  │
│  │  └──────────────┬───────────────────────────────────┘  │  │
│  │                │                                       │  │
│  │  ┌─────────────▼───────────────────────────────────┐  │  │
│  │  │ Local Database                                  │  │  │
│  │  │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓   │  │  │
│  │  │ ┃ PostgreSQL (Primary)                   ┃   │  │  │
│  │  │ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛   │  │  │
│  │  │                                                │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  └─────────────────┬──────────────────────────────────────┘  │
│                    │                                          │
│                    │ VPN / AWS Direct Connect                │
│                    │ Replication & Sync                      │
│                    │                                          │
└────────┬───────────┼──────────────────────────────────────────┘
         │           │
         │           │
         ▼           ▼
    ┌──────────────────────────────────────────────────────┐
    │         AWS Cloud (Primary)                          │
    │                                                      │
    │  ┌────────────────────────────────────────────────┐ │
    │  │ VPC & Networking                              │ │
    │  │ - Subnets (Public, Private)                   │ │
    │  │ - Security Groups & NACLs                     │ │
    │  └────────────────────────────────────────────────┘ │
    │           │         │         │         │           │
    │           ▼         ▼         ▼         ▼           │
    │  ┌──────────────────────────────────────────────┐  │
    │  │ Services                                     │  │
    │  │                                              │  │
    │  │  ┌─────────────┐  ┌──────────────┐         │  │
    │  │  │ ECS / EKS   │  │ Lambda       │         │  │
    │  │  │ Containers  │  │ Functions    │         │  │
    │  │  └─────────────┘  └──────────────┘         │  │
    │  │                                              │  │
    │  └──────────────────────────────────────────────┘  │
    │           │         │         │                    │
    │           ▼         ▼         ▼                    │
    │  ┌──────────────────────────────────────────────┐  │
    │  │ Data & Storage                               │  │
    │  │ ┌──────────────────────────────────────────┐ │  │
    │  │ │ RDS (Aurora) - Replica                  │ │  │
    │  │ │ S3 (Data warehouse)                     │ │  │
    │  │ │ DMS (Data migration service)            │ │  │
    │  │ └──────────────────────────────────────────┘ │  │
    │  └──────────────────────────────────────────────┘  │
    │                                                      │
    └──────────────────────────────────────────────────────┘

[Hybrid deployment shows on-premises legacy systems connected to AWS cloud]
```

### Key Elements
- **On-Premises**: Legacy systems and local databases
- **VPN/Direct Connect**: Secure connection between data centers
- **AWS Cloud**: Modern services and cloud infrastructure
- **Replication**: Data synchronization between locations
- **Security**: Firewalls and network isolation
- **Resilience**: Redundancy across physical locations

---

## Best Practices

### Do's ✓
- Show resource allocation (CPU, RAM, ports)
- Include scaling information and limits
- Clarify network boundaries and security
- Show data storage redundancy
- Include monitoring and logging infrastructure
- Label external services and integrations

### Don'ts ✗
- Overcomplicate with too many details
- Omit security/network considerations
- Forget to show high availability setup
- Mix deployment and architecture concerns
- Skip resource constraints information

---

## Tips for Effective Deployment Diagrams

1. **Cloud Architecture**: Show VPCs, subnets, and availability zones
2. **Load Distribution**: Clearly indicate load balancers and replication
3. **Resource Labels**: Include instance types, memory, CPU, storage
4. **Data Persistence**: Show databases, backups, and disaster recovery
5. **Network Flow**: Indicate connections and data replication paths
6. **Scalability**: Show auto-scaling groups and replica sets
7. **Monitoring**: Include logging and metrics collection points

---

**Template Version**: 1.0
**Best for**: Infrastructure documentation, deployment guides, cloud architecture, ops runbooks
