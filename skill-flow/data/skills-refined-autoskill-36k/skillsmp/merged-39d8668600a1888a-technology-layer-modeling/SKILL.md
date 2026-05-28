---
name: technology-layer-modeling
description: Use this skill for modeling the technology layer in documentation robotics, capturing infrastructure, software, networks, and services.
---

# Technology Layer Skill

**Layer Number:** 05  
**Specification:** Metadata Model Spec v0.7.0  
**Purpose:** Describes the technology infrastructure including hardware, software, networks, and facilities that support applications.

---

## Layer Overview

The Technology Layer captures **infrastructure and platform**:

- **COMPUTE** - Nodes, devices, system software
- **NETWORK** - Communication networks, paths, interfaces
- **STORAGE** - Artifacts (databases, files, configurations)
- **SERVICES** - Technology services (IaaS, PaaS)
- **AUTOMATION** - Infrastructure as Code (Terraform, Ansible, K8s)

This layer uses **ArchiMate 3.2 Technology Layer** standard with optional properties for Infrastructure as Code references, cloud provider specifics, and operational characteristics.

---

## Entity Types

| Entity Type                 | Description                                             | Key Attributes                                                                               |
| --------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Node**                    | Computational or physical resource that hosts artifacts | Types: server, container, vm, kubernetes-cluster, serverless-function, database-cluster      |
| **Device**                  | Physical IT resource with processing capability         | Types: server, workstation, mobile, iot-device, network-device, storage-appliance            |
| **SystemSoftware**          | Software that provides platform for applications        | Types: operating-system, database, middleware, container-runtime, web-server, message-broker |
| **TechnologyCollaboration** | Aggregate of nodes working together                     | Examples: HA Cluster, CDN Network, Service Mesh                                              |
| **TechnologyInterface**     | Point of access where technology services are available | Protocols: HTTP, HTTPS, TCP, UDP, WebSocket, AMQP, MQTT, SQL, gRPC                           |
| **Path**                    | Link between nodes through which they exchange          | Types: network, vpn, direct-connect, internet, peering                                       |
| **CommunicationNetwork**    | Set of structures that connects nodes                   | Types: lan, wan, vpn, internet, cdn, service-mesh, zero-trust-network                        |
| **TechnologyFunction**      | Collection of technology behavior                       | Examples: Load Balancing, Data Replication, Auto-scaling, Monitoring                         |
| **TechnologyProcess**       | Sequence of technology behaviors (CI/CD, provisioning)  | Automation: ansible, terraform, kubernetes, cloudformation, pulumi                           |
| **TechnologyInteraction**   | Unit of collective technology behavior                  | Examples: Database Replication, Cache Synchronization, Failover                              |
| **TechnologyEvent**         | Technology state change                                 | Types: startup, shutdown, failure, scaling, maintenance, alert                               |
| **TechnologyService**       | Externally visible unit of technology functionality     | Types: infrastructure, platform, storage, compute, network, database, messaging              |
| **Artifact**                | Physical piece of data used or produced                 | Types: database, file, configuration, binary, log, backup, docker-image, helm-chart          |

---

## Intra-Layer Relationships

### Structural Relationships

| Source Type             | Predicate       | Target Type           | Example                                           |
| ----------------------- | --------------- | --------------------- | ------------------------------------------------- |
| Device                  | composes        | Node                  | "Physical Server" composes "Virtual Machine"      |
| Node                    | composes        | TechnologyInterface   | "API Server" composes "HTTPS Endpoint"            |
| SystemSoftware          | composes        | TechnologyInterface   | "PostgreSQL" composes "SQL Interface"             |
| Node                    | aggregates      | Device                | Cluster aggregates multiple physical servers      |
| TechnologyCollaboration | aggregates      | Node                  | "K8s Cluster" aggregates "Worker Nodes"           |
| Artifact                | specializes     | Artifact              | "CustomerDatabase" specializes "Database"         |
| Path                    | realizes        | CommunicationNetwork  | "VPN Tunnel" realizes "Secure Network"            |
| TechnologyFunction      | realizes        | TechnologyService     | "Load Balancing" realizes "Load Balancer Service" |
| TechnologyProcess       | realizes        | TechnologyService     | "CI/CD Pipeline" realizes "Deployment Service"    |
| SystemSoftware          | realizes        | TechnologyService     | "PostgreSQL" realizes "Database Service"          |
| Node                    | assigned-to     | TechnologyFunction    | "Edge Server" assigned to "CDN Caching"           |
| TechnologyCollaboration | assigned-to     | TechnologyInteraction | Cluster performs replication                      |
| Path                    | associated-with | Node                  | Network path connects nodes                       |
| Device                  | associated-with | CommunicationNetwork  | Device connected to network                       |
| TechnologyInterface     | serves          | TechnologyService     | Interface provides service access                 |

### Behavioral Relationships

| Source Type           | Predicate | Target Type        | Example                                             |
| --------------------- | --------- | ------------------ | --------------------------------------------------- |
| TechnologyEvent       | triggers  | TechnologyProcess  | "Node Failure" triggers "Failover Process"          |
| TechnologyEvent       | triggers  | TechnologyFunction | "CPU Threshold" triggers "Auto-scaling Function"    |
| TechnologyProcess     | triggers  | TechnologyEvent    | "Deployment Complete" triggers "Health Check Event" |
| TechnologyProcess     | flows-to  | TechnologyProcess  | "Build" flows to "Deploy"                           |
| TechnologyService     | flows-to  | TechnologyService  | Service dependency chain                            |
| SystemSoftware        | accesses  | Artifact           | "Database" accesses "Data Files"                    |
| TechnologyFunction    | accesses  | Artifact           | "Backup Function" accesses "Backup Files"           |
| TechnologyProcess     | accesses  | Artifact           | "Deployment" accesses "Docker Images"               |
| TechnologyInteraction | accesses  | Artifact           | "Replication" accesses "Database Replica"           |

---

## Cross-Layer References

### Outgoing References (Technology → Other Layers)

| Target Layer              | Reference Type                                     | Example                                |
| ------------------------- | -------------------------------------------------- | -------------------------------------- |
| **Layer 1 (Motivation)**  | TechnologyService supports **Goal**                | Infrastructure supports business goals |
| **Layer 1 (Motivation)**  | TechnologyService governed by **Principle**        | Cloud-native principle                 |
| **Layer 1 (Motivation)**  | Node governed by **Principle**                     | Infrastructure principles              |
| **Layer 1 (Motivation)**  | Node constrained by **Constraint**                 | Budget, region, compliance constraints |
| **Layer 1 (Motivation)**  | Node fulfills **Requirement**                      | Performance, availability requirements |
| **Layer 1 (Motivation)**  | SystemSoftware governed by **Principle**           | Open-source principle                  |
| **Layer 1 (Motivation)**  | SystemSoftware constrained by **Constraint**       | Licensing, version constraints         |
| **Layer 1 (Motivation)**  | SystemSoftware fulfills **Requirement**            | Technical requirements                 |
| **Layer 1 (Motivation)**  | CommunicationNetwork governed by **Principle**     | Zero-trust principle                   |
| **Layer 1 (Motivation)**  | CommunicationNetwork constrained by **Constraint** | Network segmentation                   |
| **Layer 1 (Motivation)**  | Artifact constrained by **Constraint**             | Data residency, retention              |
| **Layer 4 (Application)** | Node hosts **ApplicationComponent**                | K8s pod hosts service                  |
| **Layer 4 (Application)** | TechnologyService serves **ApplicationService**    | Database serves application            |
| **Layer 4 (Application)** | Artifact stores **DataObject**                     | Database stores application data       |
| **Layer 3 (Security)**    | Artifact has **encryption** property               | Data-at-rest encryption                |
| **Layer 3 (Security)**    | Artifact has **classification** property           | Data classification level              |
| **Layer 3 (Security)**    | Artifact has **pii** property                      | Contains PII                           |
| **Layer 3 (Security)**    | CommunicationNetwork has **security-policy**       | Network security rules                 |
| **Layer 11 (APM)**        | TechnologyService has **sla-target**               | Availability, latency targets          |
| **Layer 11 (APM)**        | TechnologyService has **health-check**             | Health monitoring endpoint             |
| **Layer 11 (APM)**        | Node has **monitoring-agent**                      | APM agent installation                 |

### Incoming References (Lower Layers → Technology)

Lower layers reference Technology layer to show:

- Applications depend on infrastructure
- APIs run on technology platforms
- Data stored in technology artifacts

---

## Codebase Detection Patterns

### Pattern 1: Kubernetes Deployment

```yaml
# Kubernetes deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
        - name: user-service
          image: myregistry/user-service:1.0.0
          ports:
            - containerPort: 8080
```

**Maps to:**

- Node: "K8s Cluster Production" (type: kubernetes-cluster)
- Node: "User Service Pod" (type: container)
- Artifact: "myregistry/user-service:1.0.0" (type: docker-image)
- TechnologyInterface: "Port 8080" (protocol: HTTP)

### Pattern 2: Terraform Infrastructure

```hcl
# Terraform AWS infrastructure
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  availability_zone = "us-east-1a"

  tags = {
    Name = "Web Server"
    Environment = "production"
  }
}

resource "aws_db_instance" "postgres" {
  engine         = "postgres"
  engine_version = "14.7"
  instance_class = "db.t3.medium"
  storage_type   = "gp3"
}
```

**Maps to:**

- Node: "Web Server EC2" (type: server, provider: aws, instance-type: t3.medium, region: us-east-1, az: us-east-1a)
- Node: "PostgreSQL RDS" (type: database-cluster, provider: aws)
- SystemSoftware: "PostgreSQL 14.7" (type: database, version: 14.7)
- Properties: iac-tool=terraform, iac-file=main.tf

### Pattern 3: Docker Compose

```yaml
# docker-compose.yml
version: "3.8"
services:
  api:
    image: myapp/api:latest
    ports:
      - "8080:8080"
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: admin
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres-data:
```

**Maps to:**

- TechnologyCollaboration: "Docker Compose Stack"
- Node: "API Container" (type: container)
- SystemSoftware: "PostgreSQL 14" (type: database)
- SystemSoftware: "Redis 7" (type: middleware, subtype: cache)
- Artifact: "postgres-data" (type: volume)
- TechnologyInterface: "Redis Port 6379" (protocol: TCP)

### Pattern 4: Database Configuration

```python
# Database connection configuration
DATABASE_CONFIG = {
    "host": "prod-db.example.com",
    "port": 5432,
    "database": "customer_db",
    "user": "app_user",
    "password": "${DB_PASSWORD}",
    "pool_size": 20,
    "max_overflow": 10,
    "pool_timeout": 30
}
```

**Maps to:**

- Node: "Production Database" (type: database-cluster, host: prod-db.example.com)
- SystemSoftware: "PostgreSQL" (type: database, port: 5432)
- Artifact: "customer_db" (type: database)
- TechnologyInterface: "PostgreSQL Interface" (protocol: SQL, port: 5432)
- Properties: pool-size=20, max-overflow=10

### Pattern 5: CI/CD Pipeline

```yaml
# GitHub Actions CI/CD
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myregistry/myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: kubectl apply -f k8s/deployment.yaml
```

**Maps to:**

- TechnologyProcess: "CI/CD Pipeline" (pattern: ci-cd, automation: github-actions)
- Sub-processes: "Build", "Deploy"
- TechnologyFunction: "Docker Build", "Kubernetes Deploy"
- Artifact: "Docker Image" (type: docker-image)

### Pattern 6: Load Balancer Configuration

```nginx
# NGINX load balancer
upstream backend {
    least_conn;
    server app1.example.com:8080 weight=1;
    server app2.example.com:8080 weight=1;
    server app3.example.com:8080 weight=1;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        proxy_pass http://backend;
    }
}
```

**Maps to:**

- Node: "NGINX Load Balancer" (type: server)
- SystemSoftware: "NGINX" (type: web-server, subtype: load-balancer)
- TechnologyFunction: "Load Balancing" (strategy: least-conn)
- TechnologyInterface: "HTTPS Endpoint" (protocol: HTTPS, port: 443)
- TechnologyCollaboration: "Backend Pool" (aggregates app1, app2, app3)

---

## Modeling Workflow

### Step 1: Identify Infrastructure Nodes

```bash
# Kubernetes cluster
dr add technology node "k8s-cluster-prod" \
  --properties type=kubernetes-cluster,provider=aws,region=us-east-1,version=1.28 \
  --description "Production Kubernetes cluster"

# Virtual machines
dr add technology node "web-server-01" \
  --properties type=vm,provider=aws,instance-type=t3.large,az=us-east-1a \
  --description "Web application server VM"

# Serverless function
dr add technology node "order-processor-lambda" \
  --properties type=serverless-function,provider=aws,runtime=node.11,memory=512 \
  --description "Lambda function for order processing"

# Database cluster
dr add technology node "postgres-cluster" \
  --properties type=database-cluster,provider=aws,instance-class=db.r5.xlarge \
  --description "PostgreSQL RDS cluster"
```

### Step 2: Define System Software

```bash
# Database system
dr add technology system-software "postgresql-14" \
  --properties type=database,version=14.7,license=open-source \
  --description "PostgreSQL relational database"

# Container runtime
dr add technology system-software "docker" \
  --properties type=container-runtime,version=24.0.5 \
  --description "Docker container runtime"

# Web server
dr add technology system-software "nginx" \
  --properties type=web-server,version=1.24.0,subtype=load-balancer \
  --description "NGINX web server and load balancer"

# Message broker