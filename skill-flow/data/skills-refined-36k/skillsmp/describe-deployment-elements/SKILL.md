---
name: describe-deployment-elements
description: Write descriptions for deployment elements using markdown tables with VLAN/network specs, infrastructure details, and metadata for automation.
---

# Describe Deployment Elements

Use this skill when documenting deployment infrastructure zones and VMs.

**Use markdown tables in descriptions for human-readable specs + metadata blocks for automation.**

## Markdown Table Format for Deployment

**Always put network interfaces (eth0, eth1) FIRST - operators need networking immediately.**

### Zone Description Template

```likec4
AppTier = Zone "Application Tier (VLAN 101: 10.1.0.0/24)" {
  description """
    Production microservices deployment zone.
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 101 |
    | Network | 10.1.0.0/24 |
    | Gateway | 10.1.0.1 |
    | Monitoring Port | 9090 |
    | Capacity | 10 Gbps link to core |
  """
  
  metadata {
    vlan '101'
    network '10.1.0.0/24'
    gateway '10.1.0.1'
    monitoring_port '9090'
    capacity '10 Gbps'
  }
}
```

### VM Description Template

**RULE: eth0 and network interfaces come FIRST in the table. Duplicate data in metadata for automation.**

```likec4
ProdUploadVm = Node_Vm "prod-upload-vm" {
  #Deployment
  technology "Node.js + Docker"
  
  description """
    File upload handler and validation service with fail-fast validation.
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 10.1.0.12/24 |
    | eth1 | 10.4.0.12/24 (monitoring sideband) |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 2 vCPU (2 GHz) |
    | RAM | 4 GB |
    | Disk | 100 GB SSD |
    | Container Runtime | Docker 20.10 |
    | Health Check | GET /health:3001 (30s) |
    | Logging | ELK → 10.4.0.10:5044 |
    | RTO | 5 min |
    | RPO | 1 hour |
  """
  
  metadata {
    eth0 '10.1.0.12/24'
    eth1 '10.4.0.12/24'
    os 'Ubuntu 22.04 LTS'
    cpu '2 vCPU'
    ram '4 GB'
    disk '100 GB SSD'
    container_runtime 'Docker 20.10'
    health_check 'GET /health:3001 (30s)'
    logging_endpoint '10.4.0.10:5044'
    rto '5 min'
    rpo '1 hour'
  }
  
  uploadApp = Node_App "Upload Service" {
    instanceOf vault.uploadService
  }
}
```

**Key Rule:** Network interfaces first because operators need this immediately. Metadata duplicates table data for automation/tooling.

## Zone Description Details

### Standard Zone Table

```likec4
Zone Dmz "Network DMZ (VLAN 100: 10.0.0.0/24)" {
  description """
    Perimeter security zone with TLS termination
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 100 |
    | Network | 10.0.0.0/24 |
    | Gateway | 10.0.0.1 |
    | Purpose | Edge services |
    | Capacity | 5 Gbps uplink |
    | Monitoring | Prometheus on 9090 |
  """
  
  metadata {
    vlan '100'
    network '10.0.0.0/24'
    gateway '10.0.0.1'
    purpose 'Edge services'
    capacity '5 Gbps'
    monitoring_port '9090'
  }
}
```

## VM Description Details

### Network-First Specification

Always lead with network interfaces:

```likec4
ProdDatabaseVm = Node_Vm "prod-database-vm" {
  technology "MongoDB 5.0"
  
  description """
    High-availability MongoDB cluster node
    
    **Network:**
    | Interface | Value |
    |:---------|:------|
    | eth0 | 10.3.0.16/24 (primary) |
    | eth1 | 10.4.0.16/24 (replication) |
    | Gateway | 10.3.0.1 |
    
    **Hardware:**
    | Property | Value |
    |:---------|:------|
    | OS | Ubuntu 22.04 LTS |
    | CPU | 4 vCPU |
    | RAM | 16 GB |
    | Disk | 500 GB SSD (primary storage) |
    | Disk | 200 GB SSD (journal) |
    
    **Database:**
    | Property | Value |
    |:---------|:------|
    | Port | 27017 |
    | Replicas | 3 nodes |
    | Backup | Daily to InfraZone |
    | Retention | 30 days |
  """
  
  metadata {
    eth0 '10.3.0.16/24'
    eth1 '10.4.0.16/24'
    os 'Ubuntu 22.04 LTS'
    cpu '4 vCPU'
    ram '16 GB'
    disk_primary '500 GB SSD'
    disk_journal '200 GB SSD'
    port '27017'
    replicas '3'
    backup_location 'InfraZone'
    backup_retention '30 days'
  }
}
```

## Common Infrastructure Metadata

### Network Metadata

```likec4
metadata {
  eth0 '10.1.0.12/24'
  eth1 '10.4.0.12/24'
  gateway '10.1.0.1'
  dns_primary '8.8.8.8'
  dns_secondary '8.8.4.4'
}
```

### Compute Metadata

```likec4
metadata {
  os 'Ubuntu 22.04 LTS'
  cpu '2 vCPU'
  cpu_frequency '2.4 GHz'
  ram '4 GB'
  disk_os '50 GB'
  disk_data '100 GB'
  disk_type 'SSD'
}
```

### Application Metadata

```likec4
metadata {
  service_port '3001'
  protocol 'HTTP/2'
  container_runtime 'Docker 20.10'
  health_check_endpoint '/health'
  health_check_interval '30s'
  health_check_timeout '5s'
}
```

### Monitoring & Logging

```likec4
metadata {
  monitoring_port '9090'
  monitoring_tool 'Prometheus'
  logging_endpoint '10.4.0.10:5044'
  logging_tool 'ELK'
  log_level 'INFO'
}
```

### Reliability & Recovery

```likec4
metadata {
  rto '5 minutes'
  rpo '1 hour'
  backup_destination 'InfraZone'
  backup_frequency 'daily'
  backup_retention '30 days'
  replication_target 'eu-west-1'
}
```

## Checklist for Zone Descriptions

- [ ] VLAN number included (e.g., `VLAN 101`)
- [ ] Network CIDR included (e.g., `10.1.0.0/24`)
- [ ] Gateway IP included (e.g., `10.1.0.1`)
- [ ] Purpose clearly stated
- [ ] Firewall rules documented
- [ ] Uses markdown table format for readability
- [ ] Metadata block duplicates key values

## Checklist for VM Descriptions

- [ ] eth0 listed FIRST (network comes first)
- [ ] All network interfaces documented
- [ ] IP addresses with CIDR notation
- [ ] Operating system version
- [ ] CPU count (vCPU)
- [ ] RAM amount (GB)
- [ ] Disk specifications
- [ ] Service port (if applicable)
- [ ] Container runtime
- [ ] Monitoring endpoint
- [ ] Metadata block with structured data

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| Bury network info in table | Put eth0 first in table | Operators need this immediately |
| Generic "web server" details | Full specs: OS, CPU, RAM, disk | Operations needs complete specs |
| Missing IP addresses | Always `10.x.x.y/24` format | Network team needs CIDR |
| Vague port specifications | `MongoDB 10.3.0.16:27017` | Enables firewall rules |
| No metadata block | Duplicate table data in metadata | Enables automation/tooling |

## Related Skills

- `write-deployment-specs` - Rich specifications using markdown tables
- `model-deployment-hierarchy` - Infrastructure hierarchy and structure
