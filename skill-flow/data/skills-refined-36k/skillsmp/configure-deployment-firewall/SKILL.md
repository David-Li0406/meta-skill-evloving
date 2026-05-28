---
name: configure-deployment-firewall
description: Document firewall rules between tiers and define scaling strategies (horizontal vs vertical) for production infrastructure.
---

# Configure Deployment Firewall

Use this skill when documenting network security and scaling strategies for deployment infrastructure.

**Prerequisite:** Read `deployment-tier-patterns` first to understand tier organization.

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

**When to use:**
- Stateless services (AppTier microservices)
- Async workers (ProcTier)
- Load can be distributed

### Vertical Scaling

Increase resources for DataTier (databases rarely scale horizontally):
```
DataTier: 4 GB RAM → 16 GB RAM → 64 GB RAM
DataTier: 100 GB disk → 1 TB disk → 10 TB disk
```

**When to use:**
- Stateful services (databases)
- Single-instance services (message queue broker)
- Memory/disk constraints

## Zone Description Firewall Format

Include firewall rules in zone descriptions:

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
    | Scaling | Horizontal (CPU-based autoscaling) |
  """
}
```

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| No firewall documentation | Document in zone descriptions + relationships | Security team needs this |
| Generic "network traffic" | Specific ports and protocols | Enables firewall rule creation |
| No scaling strategy | Document horizontal vs vertical | Operations needs capacity planning |
| Scale databases horizontally without clustering | Vertical scaling or managed DB clusters | Databases are stateful |

## Related Skills

- `structure-deployment-tiers` - Tier organization and responsibilities
- `create-relationship` - Model inter-tier communication
