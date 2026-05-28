---
name: name-deployment-nodes
description: Systematic naming for deployment nodes (VMs, zones, environments) enables consistent infrastructure documentation. Use {Environment}{Service}Vm for VMs, {Tier} for zones, and include VLAN/network details.
---

# Name Deployment Nodes Consistently

Use this skill when creating VMs, zones, or deployment nodes in deployment.c4 or operations.c4.

**Prerequisite:** Read `model-deployment` skill for basic structure and hierarchy.

## Naming Formula

### Virtual Machines (VMs)
**Pattern:** `{Environment}{ServiceName}Vm` (PascalCase)

```likec4
// Examples following pattern
ProdApigwVm      // prod + apigw + vm = production API gateway VM
ProdUploadVm     // prod + upload + vm = production upload service VM
ProdWorkerVm     // prod + worker + vm = production processing worker VM
StagingApiVm     // staging + api + vm = staging API VM
DevDatabaseVm    // dev + database + vm = development database VM
```

**Rules:**
- Environment prefix: `Prod`, `Staging`, `Dev`, `Test`
- Service name: Meaningful abbreviation (Apigw, Upload, Worker, Database, Queue)
- Suffix: Always `Vm` for consistency
- FQN identifier: Use lowercase kebab-case: `prod-apigw-vm`, `prod-upload-vm`

### Zones (Network Segments / VLAN Regions)
**Pattern:** `{Tier}Tier` or `{Function}Zone` (PascalCase)

```likec4
// Tier-based naming (for layered architectures)
Dmz          // Demilitarized Zone (edge security)
AppTier      // Application tier (microservices)
ProcTier     // Processing tier (async workers)
DataTier     // Data tier (databases, storage)

// Function-based naming (for specialized infrastructure)
SecZone      // Security & monitoring
InfraZone    // Backup & disaster recovery
NetworkZone  // Load balancing & CDN
```

**Rules:**
- Use `Tier` suffix for layered architecture (App, Proc, Data, Dmz)
- Use `Zone` suffix for functional groupings (Sec, Infra, Network)
- Each zone should have a description with VLAN details
- Never abbreviate inconsistently (not `AppT` or `ProcZone`)

### Environments
**Pattern:** `{Environment}` (PascalCase)

```likec4
Prod       // Production (customer-facing)
Staging    // Staging (pre-production testing)
Dev        // Development (local testing)
Test       // Test (automated testing)
```

### External Nodes
**Pattern:** `{Provider}{Service}` (PascalCase)

```likec4
VirusTotalService     // SaaS antivirus provider
AwsS3Bucket           // AWS cloud storage
GoogleAnalyticsApi    // Google SaaS analytics
DatadogMonitoring     // SaaS monitoring platform
```

---

## Rich Zone Descriptions with Network Details

Always include network and infrastructure specifications in zone descriptions:

```likec4
AppTier = Zone "Application Tier (VLAN 101: 10.1.0.0/24)" {
  description """
    Microservices deployment zone
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 101 |
    | Network | 10.1.0.0/24 |
    | Gateway | 10.1.0.1 |
    | Firewall | DMZ → AppTier (ingress 443) |
    | Firewall | AppTier → DataTier (egress 27017, 9000) |
    | Purpose | Production microservices |
  """
  
  // VMs in this zone
  ProdUploadVm = Node_Vm "prod-upload-vm" { ... }
  ProdRetrievalVm = Node_Vm "prod-retrieval-vm" { ... }
}
```

### Zone Description Template

```likec4
Zone SomeTier "Human Readable Zone Name (VLAN N: CIDR)" {
  description """
    Brief purpose of this zone
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 101 |
    | Network | 10.1.0.0/24 |
    | Gateway | 10.1.0.1 |
    | Firewall Rules | List relevant rules |
    | Purpose | What runs here |
    | Tags | #Production #Networking |
  """
}
```

---

## VM Description with Infrastructure Specs

Use Markdown tables to make deployment specs scannable and self-documenting:

```likec4
ProdUploadVm = Node_Vm "prod-upload-vm" {
  #Deployment
  technology "Node.js + Docker"
  
  description """
    File upload handler and validation service (fail-fast validation)
    
    | Property | Value |
    |:---------|:------|
    | Hostname | prod-upload-vm |
    | IP Address | 10.1.0.12/24 |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 2 vCPU |
    | RAM | 4 GB |
    | Disk | 100 GB SSD |
    | Port | 3001 |
    | Protocol | HTTP/2 |
    | Container | Docker |
    | Monitoring | Prometheus metrics on 9090 |
    | Backup | Daily snapshots |
  """
  
  uploadApp = Node_App "Upload Service" {
    instanceOf vault.uploadService
  }
}
```

### VM Description Template

```likec4
Node_Vm "vm-name" {
  technology "Runtime + Tools"
  
  description """
    Human-readable purpose and role
    
    | Property | Value |
    |:---------|:------|
    | Hostname | prod-service-vm |
    | IP | 10.x.x.y/24 |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 2 vCPU |
    | RAM | 4 GB |
    | Port | 3001 |
    | Container | Docker |
    | Monitoring | Port 9090 |
  """
}
```

---

## Complete Example: Multi-Tier Deployment

```likec4
deployment {
  Prod = Node_Environment 'Production Datacenter - EU' {
    #Production
    
    // Edge security zone
    Zone Dmz "Network DMZ (VLAN 100: 10.0.0.0/24)" {
      description """
        Perimeter security zone with TLS termination
        
        | Property | Value |
        |:---------|:------|
        | VLAN | 100 |
        | Network | 10.0.0.0/24 |
        | Gateway | 10.0.0.1 |
        | Purpose | Edge services |
      """
      
      ProdApigwVm = Node_Vm "prod-apigw-vm" {
        technology "Kong / API Gateway"
        description """
          Edge API gateway terminates TLS and routes
          
          | Property | Value |
          |:---------|:------|
          | IP | 10.0.0.10/24 |
          | OS | Ubuntu 22.04 LTS |
          | CPU | 4 vCPU |
          | RAM | 8 GB |
          | Port | 443 |
        """
        
        apiApp = Node_App "API Gateway" {
          instanceOf vault.api
        }
      }
    }
    
    // Application services tier
    AppTier = Zone "Application Tier (VLAN 101: 10.1.0.0/24)" {
      description """
        Microservices deployment zone
        
        | Property | Value |
        |:---------|:------|
        | VLAN | 101 |
        | Network | 10.1.0.0/24 |
        | Gateway | 10.1.0.1 |
      """
      
      ProdUploadVm = Node_Vm "prod-upload-vm" {
        description """
          | IP | 10.1.0.12/24 |
          | Port | 3001 |
        """
        uploadApp = Node_App "Upload Service" {
          instanceOf vault.uploadService
        }
      }
      
      ProdRetrievalVm = Node_Vm "prod-retrieval-vm" {
        description """
          | IP | 10.1.0.13/24 |
          | Port | 3002 |
        """
        retrievalApp = Node_App "Retrieval Service" {
          instanceOf vault.retrievalService
        }
      }
    }
    
    // Processing tier
    ProcTier = Zone "Processing Tier (VLAN 102: 10.2.0.0/24)" {
      ProdQueueVm = Node_Vm "prod-queue-vm" {
        description "| IP | 10.2.0.14/24 | | Port | 5672 |"
        queueApp = Node_App "Message Broker" {
          instanceOf vault.jobs
        }
      }
      
      ProdWorkerVm = Node_Vm "prod-worker-vm" {
        description "| IP | 10.2.0.15/24 |"
        workerApp = Node_App "Processing Worker" {
          instanceOf vault.worker
        }
      }
    }
    
    // Data tier
    DataTier = Zone "Data Tier (VLAN 103: 10.3.0.0/24)" {
      ProdDatabaseVm = Node_Vm "prod-database-vm" {
        description "| IP | 10.3.0.16/24 | | Port | 27017 |"
        dbApp = Node_App "Database" {
          instanceOf vault.docDB
        }
      }
      
      ProdStorageVm = Node_Vm "prod-storage-vm" {
        description "| IP | 10.3.0.17/24 | | Port | 9000 |"
        storageApp = Node_App "Object Storage" {
          instanceOf vault.minio
        }
      }
    }
  }
}
```

---

## Naming Consistency Checklist

- [ ] VMs follow `{Environment}{Service}Vm` pattern (e.g., `ProdUploadVm`)
- [ ] FQN identifiers use kebab-case (e.g., `prod-upload-vm`)
- [ ] Zones use `{Tier}` or `{Function}Zone` naming
- [ ] Zone descriptions include VLAN number and CIDR block
- [ ] VM descriptions include table with IP, OS, CPU, RAM, Port
- [ ] External services named `{Provider}{Service}` (e.g., `VirusTotalService`)
- [ ] All zones have descriptive purpose in comments
- [ ] All VMs have technology specified
- [ ] Each VM has one `Node_App` with `instanceOf` linking to model container

---

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| `ProdApiVM` | `ProdApigwVm` | Inconsistent casing (VM vs Vm) |
| `prod_upload_vm` variable | `ProdUploadVm` | Variable names should be PascalCase |
| `AppServers` zone | `AppTier` zone | Zone names should be singular, use Tier/Zone suffix |
| No VLAN in description | `VLAN 101: 10.1.0.0/24` in description | Networks require VLAN/CIDR for ops |
| `dev-upload-vm` for production | `prod-upload-vm` | Environment prefix must match node |
| Generic name `Vm1`, `Server1` | `ProdUploadVm` | Names should indicate purpose |

---

## Related Skills

- `model-deployment` - Deployment structure and hierarchy
- `write-rich-descriptions` - Detailed markdown tables in element descriptions
- `structure-deployment-tiers` - Organizing zones into logical tiers
