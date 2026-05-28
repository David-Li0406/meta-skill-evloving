---
name: model-deployment-hierarchy
description: Model deployment infrastructure hierarchy (environments, zones, VMs, apps) with proper nesting and instanceOf links. Show parent-child relationships clearly.
---

# Model Deployment Hierarchy

Use this skill when defining physical infrastructure in deployment.c4.

**Prerequisite:** Read `structure-deployment-tiers` for tier organization patterns.

## Core Principles

1. **Use shared spec node kinds** - Use deployment kinds from `shared/spec-deployment.c4`
2. **Use shared spec tags** - Use tags defined in `spec-deployment.c4` (#Production, #Networking, #Service, #Monitoring)
3. **PascalCase variables** - Use `ProdApiVm` not `prod_api_vm` in deployment
4. **instanceOf (camelCase!)** - Link `Node_App` to model Container using `instanceOf` (NOT `instanceof`) with FQN
5. **Parent containment** - Always nest VMs within zones, zones within environments
6. **Infrastructure relationships** - Use `https`, `tcp`, etc. with port descriptions

## Always Show Parent Containers

**Deployment hierarchy MUST show parent-child relationships:**
- **VMs always within zones** - Never show VMs floating outside infrastructure
- **Zones always within environments** - Never show zones without datacenter/environment context
- **Instances always within VMs** - Never show services floating free of infrastructure
- This ensures infrastructure is always contextualized: "Where does this run? In what network? In what environment?"

## Hierarchy Structure

```
Node_Environment (Production/Development)
  └─ Zone (VLAN/Network segment)
      └─ Node_Vm/Node_Server
          └─ Node_App (instanceOf Container from model)
```

## Complete Multi-Tier Example

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
        | Purpose | Edge services |
      """
      
      ProdApigwVm = Node_Vm "prod-apigw-vm" {
        technology "Kong / API Gateway"
        description """
          | eth0 | 10.0.0.10/24 |
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
        | Property | Value |
        |:---------|:------|
        | VLAN | 101 |
        | Network | 10.1.0.0/24 |
      """
      
      ProdUploadVm = Node_Vm "prod-upload-vm" {
        description "| eth0 | 10.1.0.12/24 | | Port | 3001 |"
        uploadApp = Node_App "Upload Service" {
          instanceOf vault.uploadService
        }
      }
    }
    
    // Processing tier
    ProcTier = Zone "Processing Tier (VLAN 102: 10.2.0.0/24)" {
      ProdWorkerVm = Node_Vm "prod-worker-vm" {
        description "| eth0 | 10.2.0.15/24 |"
        workerApp = Node_App "Worker" {
          instanceOf vault.worker
        }
      }
    }
    
    // Data tier
    DataTier = Zone "Data Tier (VLAN 103: 10.3.0.0/24)" {
      ProdDatabaseVm = Node_Vm "prod-database-vm" {
        description "| eth0 | 10.3.0.16/24 | | Port | 27017 |"
        dbApp = Node_App "Database" {
          instanceOf vault.docDB
        }
      }
    }
  }
}
```

## Shared Spec Principle

**Before creating a new deployment node kind or tag:**
1. Check `shared/spec-deployment.c4` for existing kinds and tags
2. Use what's already defined
3. If something is needed that's not in spec:
   - Ask user permission first
   - Suggest contributing to shared spec
   - Don't create project-specific custom kinds
   - Add to spec so all projects can use it

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| VMs outside zones | VMs always within Zone | Shows network context |
| Zones outside environments | Zones always within Environment | Shows datacenter context |
| Custom deployment kinds | Use kinds from shared spec | Consistency across projects |
| App instances floating free | Apps always within VMs | Clear infrastructure mapping |
| `instanceOf` (lowercase 'O') | `instanceOf` (camelCase) | LikeC4 requires camelCase |

## Related Skills

- `model-deployment-relationships` - Mirror system relationships in deployment
- `structure-deployment-tiers` - Standard tier organization
- `write-deployment-specs` - Rich infrastructure specifications
