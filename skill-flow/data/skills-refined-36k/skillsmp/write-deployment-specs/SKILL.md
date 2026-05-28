---
name: write-deployment-specs
description: Rich descriptions for zones and VMs using markdown tables with VLAN/network specs, infrastructure details, and self-documenting templates.
---

# Write Deployment Specs

Use this skill when documenting zones and VMs with infrastructure specifications.

**Prerequisite:** Read `naming-deployment-conventions` first.

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
    }
  }
}
```

## Checklist for Zone Descriptions

- [ ] VLAN number included (e.g., `VLAN 101`)
- [ ] Network CIDR included (e.g., `10.1.0.0/24`)
- [ ] Gateway IP included (e.g., `10.1.0.1`)
- [ ] Firewall rules documented
- [ ] Purpose clearly stated
- [ ] Uses markdown table format for readability

## Checklist for VM Descriptions

- [ ] Hostname specified
- [ ] IP address with CIDR notation (e.g., `10.1.0.12/24`)
- [ ] Operating system version (e.g., `Ubuntu 22.04 LTS`)
- [ ] CPU count (vCPU)
- [ ] RAM amount (GB)
- [ ] Disk size and type (e.g., `100 GB SSD`)
- [ ] Primary port (if applicable)
- [ ] Container runtime (Docker, Podman, etc.)
- [ ] Monitoring endpoint (usually 9090)

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| No VLAN in description | `VLAN 101: 10.1.0.0/24` in description | Networks require VLAN/CIDR for ops |
| Generic "web server" | Full table with IP, OS, CPU, RAM | Operations needs complete specs |
| Missing IP address | Always include `10.x.x.y/24` format | Network team needs this |
| Vague firewall rules | `DMZ → AppTier (443), AppTier → DataTier (27017)` | Enables firewall team to work autonomously |

## Related Skills

- `name-deployment-nodes` - Naming formulas
- `structure-deployment-tiers` - Organizing zones into tiers
- `write-rich-descriptions` - System element descriptions (not deployment)
