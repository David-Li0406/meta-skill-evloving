# Cloud Concepts

## Table of Contents
- [Networking](#networking)
- [Identity & Access](#identity--access)
- [Storage](#storage)
- [Compute](#compute)
- [Observability](#observability)

## Networking

### Virtual Networks (VPC/VNet/VPC)

**Conceptual model:**
Think of a VPC as your own private data centre in the cloud — isolated network space where you control IP addressing, routing, and security.

| Concept | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Virtual network | VPC | VNet | VPC |
| Subnet | Subnet | Subnet | Subnet |
| Route table | Route table | Route table | Routes |
| Internet gateway | Internet Gateway | (implicit) | (implicit) |
| NAT | NAT Gateway | NAT Gateway | Cloud NAT |
| Firewall rules | Security Groups + NACLs | NSGs | Firewall rules |

### CIDR Fundamentals
```
10.0.0.0/16  = 10.0.0.0 - 10.0.255.255 (65,536 addresses)
10.0.1.0/24  = 10.0.1.0 - 10.0.1.255   (256 addresses)
10.0.1.0/28  = 10.0.1.0 - 10.0.1.15    (16 addresses)
```

**Reserved addresses per subnet:**
- AWS: First 4 + last 1 (network, VPC router, DNS, future, broadcast)
- Azure: First 4 + last 1
- GCP: First 4 (no broadcast reservation)

### Public vs Private Subnets
- **Public:** Has route to internet gateway, resources can have public IPs
- **Private:** No direct internet route, uses NAT for outbound

### Peering vs Transit
**Peering:** Direct connection between two VPCs
- Non-transitive (A↔B and B↔C doesn't mean A↔C)
- No overlapping CIDRs
- Low latency, no bandwidth limits

**Transit Gateway/Hub:** Central hub for many-to-many connectivity
- Transitive routing
- Centralised management
- Additional cost

### Private Connectivity to Cloud Services

| AWS | Azure | GCP |
|-----|-------|-----|
| VPC Endpoints (Gateway/Interface) | Private Endpoints | Private Google Access / Private Service Connect |

**Why use them?**
- Traffic stays on cloud backbone (no internet)
- Required when VPC has no internet access
- Can be cheaper than NAT Gateway data processing

### DNS Resolution
Each cloud provides internal DNS:
- AWS: VPC DNS at base+2 (e.g., 10.0.0.2)
- Azure: 168.63.129.16 (magic IP)
- GCP: 169.254.169.254 (metadata server)

## Identity & Access

### The Principal → Permission → Resource Model
All clouds follow this pattern:
```
WHO (Principal) can do WHAT (Permission/Action) on WHICH (Resource)
```

### Authentication vs Authorisation
- **Authentication (AuthN):** Proving who you are (credentials, tokens)
- **Authorisation (AuthZ):** What you're allowed to do (policies, roles)

### Credential Hierarchy (Prefer Top)
1. **Workload identity / Instance roles** — No credentials to manage
2. **Short-lived tokens** — STS, OAuth tokens with expiry
3. **Service account keys** — Long-lived, avoid if possible
4. **User credentials in code** — Never do this

### Least Privilege Principle
Start with zero permissions, add only what's needed.

**Approach:**
1. Run workload with broad read access (Reader role)
2. Log all API calls (CloudTrail, Activity Log, Audit Logs)
3. Analyse logs to see actual actions used
4. Create policy with only those actions

### Cross-Account/Tenant Patterns

**Trust relationship model:**
1. Trusting account creates role with trust policy
2. Trust policy specifies who can assume (principal)
3. Trusted principal calls AssumeRole/similar
4. Gets temporary credentials scoped to that role

**External ID (AWS):**
Prevents confused deputy attacks when third party assumes role. The third party generates a unique ID that only you both know.

## Storage

### Object Storage (S3/Blob/GCS)

**Key concepts:**
- **Bucket/Container:** Namespace for objects (globally unique in AWS/GCP)
- **Object:** File + metadata
- **Key:** Full path to object (no real folders, just prefixes)

**Consistency models:**
- AWS S3: Strong consistency (since 2020)
- Azure Blob: Strong consistency
- GCP GCS: Strong consistency (since 2021)

**Access patterns:**
| Pattern | Use Case |
|---------|----------|
| IAM policy | Service/role access |
| Bucket/Container policy | Cross-account, conditions |
| Pre-signed URLs | Temporary public access |
| SAS tokens (Azure) | Scoped, time-limited access |

### Block Storage (EBS/Managed Disk/Persistent Disk)

**Key concepts:**
- Attached to single instance (usually)
- Persists independently of instance lifecycle
- Snapshots for backup/replication

**Performance tiers:**
| Tier | Characteristics |
|------|-----------------|
| Standard HDD | Cheap, high latency |
| Standard SSD | Balanced |
| Premium/Provisioned SSD | High IOPS, low latency |
| Ultra/Extreme | Highest performance, highest cost |

### File Storage (EFS/Azure Files/Filestore)

**When to use:**
- Multiple instances need shared filesystem
- Legacy apps that need POSIX filesystem
- NFS/SMB protocol required

**Trade-offs vs object storage:**
- More expensive per GB
- Higher latency for random access
- Familiar filesystem semantics

## Compute

### Instance Types/Sizes
All clouds use family + size naming:
- AWS: `m5.xlarge` (family.size)
- Azure: `Standard_D4s_v3` (tier_family_size_version)
- GCP: `n2-standard-4` (family-type-vcpus)

**Common families:**
| Family | Optimised For |
|--------|---------------|
| General (M/D/N) | Balanced |
| Compute (C) | CPU-intensive |
| Memory (R/E) | RAM-intensive |
| Storage (I/D) | High I/O |
| GPU (P/G/N) | ML, graphics |

### Spot/Preemptible Instances
**The deal:** Spare capacity at 60-90% discount, but can be terminated.

| AWS | Azure | GCP |
|-----|-------|-----|
| Spot Instances | Spot VMs | Spot VMs (was Preemptible) |
| 2-min warning | 30-sec warning | 30-sec warning |
| Variable pricing | Variable pricing | Fixed discount |

**Good for:** Batch processing, CI/CD, stateless workloads
**Bad for:** Databases, user-facing services without fallback

### Auto Scaling
**Horizontal scaling:** Add/remove instances
- Scale-out triggers: CPU %, queue depth, custom metrics
- Scale-in: Be careful about connection draining

**Vertical scaling:** Resize instance
- Usually requires restart
- Useful for databases

### Containers vs VMs vs Serverless

| Aspect | VMs | Containers | Serverless |
|--------|-----|------------|------------|
| Startup | Minutes | Seconds | Milliseconds-seconds |
| Pricing | Per hour | Per hour | Per invocation |
| Control | Full | Moderate | Limited |
| Scaling | Manual/ASG | Orchestrator | Automatic |
| Use case | Legacy, full control | Microservices | Event-driven |

## Observability

### The Three Pillars

**Metrics:** Numeric measurements over time
- CPU, memory, request count, latency percentiles
- Good for alerting, dashboards

**Logs:** Discrete events with context
- Application errors, access logs, audit trails
- Good for debugging, compliance

**Traces:** Request flow across services
- Distributed tracing, spans, correlation IDs
- Good for debugging microservices

### Cloud-Native Services

| | AWS | Azure | GCP |
|-|-----|-------|-----|
| Metrics | CloudWatch Metrics | Azure Monitor Metrics | Cloud Monitoring |
| Logs | CloudWatch Logs | Azure Monitor Logs | Cloud Logging |
| Traces | X-Ray | Application Insights | Cloud Trace |

### Key Metrics to Monitor

| Resource | Critical Metrics |
|----------|------------------|
| Compute | CPU, memory, disk I/O, network |
| Database | Connections, query latency, replication lag |
| Load balancer | Request count, error rate, latency |
| Queue | Queue depth, age of oldest message |
| API | Request rate, error rate, latency (p50, p95, p99) |

### Structured Logging Best Practices
```json
{
  "timestamp": "2024-01-20T10:30:00Z",
  "level": "ERROR",
  "service": "order-service",
  "trace_id": "abc123",
  "message": "Failed to process order",
  "order_id": "12345",
  "error": "connection timeout",
  "duration_ms": 5000
}
```

Key fields:
- **timestamp:** When it happened
- **level:** Severity (DEBUG, INFO, WARN, ERROR)
- **trace_id:** Correlation across services
- **Contextual fields:** What was being processed
