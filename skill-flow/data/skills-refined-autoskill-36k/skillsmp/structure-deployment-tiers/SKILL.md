---
name: structure-deployment-tiers
description: Organize deployment infrastructure into logical tiers (DMZ → AppTier → ProcTier → DataTier) with clear responsibility separation and firewall rules between zones.
---

# Structure Deployment Tiers

Use this skill when designing deployment architecture. Organize zones/nodes into logical tiers following the standard layered architecture pattern.

**Prerequisite:** Read `model-deployment` and `name-deployment-nodes` skills for basic structure and naming.

## Core Principle: Show Tier Hierarchy & Parent Context

**All tiers and zones MUST be explicitly nested within their parent environment:**
- Every zone belongs to a specific environment (Production/Development)
- Every VM belongs to a specific zone
- Every service instance belongs to a specific VM
- This creates clear parent-child relationships: Environment → Zone → VM → Instance
- Views of individual tiers must still show their parent environment for context

## Standard Tier Architecture

The refactored reference pattern organizes infrastructure into 4-5 logical tiers:

```
Internet
    ↓
DMZ (Edge Security)
    ├─ API Gateway (Kong)
    ├─ Web Server (Nginx SPA)
    ↓
AppTier (Microservices)
    ├─ Upload Service
    ├─ Retrieval Service
    ↓
ProcTier (Async Processing)
    ├─ Message Queue (RabbitMQ)
    ├─ Worker (Processing)
    ↓
DataTier (Persistence)
    ├─ Database (MongoDB)
    ├─ Object Storage (MinIO)
    ↓
SecZone (Optional: Monitoring)
    └─ Monitoring Stack (Prometheus, Grafana)
InfraZone (Optional: Backup/DR)
    └─ Backup Storage
```

## Tier Responsibilities

### DMZ (Demilitarized Zone)
**Purpose:** Edge security with TLS termination and request routing

**Services:**
- API Gateway (Kong, Nginx Ingress) - Routes requests to microservices
- Web Server (Nginx) - Serves static SPA assets (HTML/JS/CSS)
- Load Balancer (optional) - Distributes traffic across replicas

**Network:**
- Exposed to Internet on HTTPS (port 443)
- Routes internal traffic on HTTP to AppTier
- Highest security restrictions

**Example:**
```likec4
Zone Dmz "Network DMZ (VLAN 100: 10.0.0.0/24)" {
  description """
    Perimeter security zone with TLS termination
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 100 |
    | Network | 10.0.0.0/24 |
    | Gateway | 10.0.0.1 |
    | Internet Facing | HTTPS 443 |
    | Internal Routing | HTTP to AppTier on 80 |
  """
  
  ProdApigwVm = Node_Vm "prod-apigw-vm" {
    technology "Kong / API Gateway"
    apiApp = Node_App "API Gateway" {
      instanceOf vault.api
    }
  }
  
  ProdWebServerVm = Node_Vm "prod-webserver-vm" {
    technology "Nginx"
    webApp = Node_App "Web Server" {
      instanceOf vault.webServer
    }
  }
}
```

### AppTier (Application Tier)
**Purpose:** Microservices implementation layer

**Services:**
- Upload Service - File upload and validation
- Retrieval Service - Document metadata and download
- Search Service (optional) - Full-text search
- Notification Service (optional) - User notifications

**Network:**
- Internal only (not exposed to Internet)
- Receives requests from DMZ on port 80, 443
- Sends queries to DataTier (DB port 27017, storage port 9000)
- Publishes to ProcTier (queue port 5672)

**Scalability:**
- Horizontal scaling: Add VMs as load increases
- Auto-scaling: CPU/memory triggers

**Example:**
```likec4
AppTier = Zone "Application Tier (VLAN 101: 10.1.0.0/24)" {
  description """
    Microservices deployment zone
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 101 |
    | Network | 10.1.0.0/24 |
    | Gateway | 10.1.0.1 |
    | Firewall In | DMZ → AppTier (443) |
    | Firewall Out | AppTier → DataTier (27017, 9000) |
    | Firewall Out | AppTier → ProcTier (5672) |
    | Monitoring | Prometheus 9090 |
  """
  
  ProdUploadVm = Node_Vm "prod-upload-vm" {
    uploadApp = Node_App "Upload Service" {
      instanceOf vault.uploadService
    }
  }
  
  ProdRetrievalVm = Node_Vm "prod-retrieval-vm" {
    retrievalApp = Node_App "Retrieval Service" {
      instanceOf vault.retrievalService
    }
  }
}
```

### ProcTier (Processing Tier)
**Purpose:** Async job processing and event handling

**Services:**
- Message Queue (RabbitMQ) - Job queue broker
- Worker (Processing) - Async job consumer and executor
- Cache (Redis) - Optional: Fast lookup cache

**Network:**
- Internal only
- Receives messages from AppTier (queue publish port 5672)
- Sends to DataTier (DB writes on 27017, storage writes on 9000)
- No incoming API traffic

**Async Pattern:**
- AppTier publishes events (not calls) to queue
- Worker consumes events (not called by AppTier)
- Worker persists results to DataTier
- No synchronous responses

**Example:**
```likec4
ProcTier = Zone "Processing Tier (VLAN 102: 10.2.0.0/24)" {
  description """
    Async job processing zone
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 102 |
    | Network | 10.2.0.0/24 |
    | Gateway | 10.2.0.1 |
    | Firewall In | AppTier → ProcTier (5672 RabbitMQ) |
    | Firewall Out | ProcTier → DataTier (27017, 9000) |
    | Consumer | RabbitMQ consumer pool |
    | Workers | 4 concurrent processors |
  """
  
  ProdQueueVm = Node_Vm "prod-queue-vm" {
    technology "RabbitMQ"
    queueApp = Node_App "Message Queue" {
      instanceOf vault.jobs
    }
  }
  
  ProdWorkerVm = Node_Vm "prod-worker-vm" {
    technology "GoLang"
    workerApp = Node_App "Processing Worker" {
      instanceOf vault.worker
    }
  }
}
```

### DataTier (Data Tier)
**Purpose:** Persistent storage and data access layer

**Services:**
- Database (MongoDB) - Document metadata storage
- Object Storage (MinIO) - Encrypted file storage with replication
- Backup Storage (optional) - Off-site backup copies

**Network:**
- Internal only (never exposed to Internet)
- Receives queries from AppTier (DB port 27017, storage port 9000)
- Receives writes from ProcTier (same ports)
- Replicates to backup/DR tier (optional)

**High Availability:**
- Multi-node clusters (MongoDB replicas, MinIO distributed)
- Replication across zones
- Regular backups to separate tier

**Example:**
```likec4
DataTier = Zone "Data Tier (VLAN 103: 10.3.0.0/24)" {
  description """
    Persistence and storage zone
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 103 |
    | Network | 10.3.0.0/24 |
    | Gateway | 10.3.0.1 |
    | Firewall In | AppTier, ProcTier → DataTier |
    | Firewall Out | DataTier → InfraZone (backup) |
    | Replication | 3-node cluster (high availability) |
    | Backup | Daily snapshots to InfraZone |
    | Retention | 30 days |
  """
  
  ProdDatabaseVm = Node_Vm "prod-database-vm" {
    technology "MongoDB"
    dbApp = Node_App "Database" {
      instanceOf vault.docDB
    }
  }
  
  ProdStorageVm = Node_Vm "prod-storage-vm" {
    technology "MinIO S3-compatible"
    storageApp = Node_App "Object Storage" {
      instanceOf vault.minio
    }
  }
}
```

### SecZone (Security & Monitoring) - Optional

**Purpose:** Observability, monitoring, and security infrastructure

**Services:**
- Monitoring (Prometheus, Grafana) - Metrics collection and visualization
- Log Aggregation (ELK Stack) - Centralized logging
- Alert Management - Incident alerting

**Network:**
- Internal only
- Scrapes metrics from all tiers (port 9090)
- Receives logs from AppTier and ProcTier
- Sends alerts to on-call engineers

**Example:**
```likec4
SecZone = Zone "Security & Monitoring (VLAN 104: 10.4.0.0/24)" {
  description """
    Monitoring and observability infrastructure
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 104 |
    | Network | 10.4.0.0/24 |
    | Firewall Out | Scrape metrics (9090) from all tiers |
    | Firewall In | Log push from AppTier/ProcTier (5044) |
  """
}
```

### InfraZone (Infrastructure & Disaster Recovery) - Optional

**Purpose:** Backup, disaster recovery, and operational tools

**Services:**
- Backup Storage (Bacula, Veeam) - Off-site backup copies
- Disaster Recovery Failover - Secondary databases, replicated storage
- CI/CD (optional) - Build and deployment pipeline

**Network:**
- Internal only
- Receives backups from DataTier
- Can be in separate region for true DR

## Firewall Rules Template

Document firewall rules between tiers for security review:

```likec4
// Internet → DMZ
Prod.Dmz.ProdApigwVm -[https]-> Internet "Client requests" {
  description "Internet clients → prod-apigw-vm:443"
}

// DMZ → AppTier
Prod.Dmz.ProdApigwVm -[http]-> Prod.AppTier.ProdUploadVm "Route requests" {
  description "10.0.0.10 → 10.1.0.12:3001 (internal)"
}

// AppTier → DataTier
Prod.AppTier.ProdUploadVm -[tcp]-> Prod.DataTier.ProdDatabaseVm "Persist metadata" {
  description "10.1.0.12 → 10.3.0.16:27017 (MongoDB)"
}

// AppTier → ProcTier (Event Publishing)
Prod.AppTier.ProdUploadVm -[amqp]-> Prod.ProcTier.ProdQueueVm "Queue job" {
  description "10.1.0.12 → 10.2.0.14:5672 (RabbitMQ)"
}

// ProcTier → DataTier (Job Results)
Prod.ProcTier.ProdWorkerVm -[tcp]-> Prod.DataTier.ProdDatabaseVm "Update status" {
  description "10.2.0.15 → 10.3.0.16:27017 (write metadata)"
}

// Monitoring (SecZone outbound)
Prod.SecZone.Monitoring -[tcp]-> Prod.AppTier.** "Scrape metrics" {
  description "10.4.0.19 → tier VMs:9090"
}
```

## Tier Scaling Strategy

### Horizontal Scaling
Add more VMs in AppTier and ProcTier as load increases:
```
AppTier: 1 VM → 3 VMs → 5 VMs (auto-scale by CPU)
ProcTier: 1 worker → 4 workers (process queue faster)
```

### Vertical Scaling
Increase resources for DataTier (databases rarely scale horizontally):
```
DataTier: 4 GB RAM → 16 GB RAM → 64 GB RAM
DataTier: 100 GB disk → 1 TB disk → 10 TB disk
```

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| Workers called from AppTier | Workers consume from queue | Prevents tight coupling |
| Database exposed to Internet | Database internal only | Security isolation |
| Mixed purposes in one zone | Separate tiers by concern | Easy to reason about and scale |
| No firewall documentation | Include firewall rules in zone descriptions | Operators understand security model |
| All services in one VM | One service per VM | Easier to scale and maintain |
| No monitoring in architecture | Explicit SecZone for monitoring | Observability is a first-class concern |

## Related Skills

- `model-deployment` - Deployment infrastructure basics
- `name-deployment-nodes` - Naming VMs and zones
- `write-rich-descriptions` - Document tier purposes and firewall rules
- `create-relationship` - Model communication between tiers
