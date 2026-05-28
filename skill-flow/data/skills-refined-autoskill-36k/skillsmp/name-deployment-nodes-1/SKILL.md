---
name: name-deployment-nodes
description: Systematic naming formulas for deployment nodes - {Environment}{Service}Vm for VMs, {Tier} for zones, consistent kebab-case FQNs.
---

# Name Deployment Nodes

Use this skill when creating VMs, zones, or deployment nodes.

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

## Naming Consistency Checklist

- [ ] VMs follow `{Environment}{Service}Vm` pattern
- [ ] FQN identifiers use kebab-case
- [ ] Zones use `{Tier}` or `{Function}Zone` naming
- [ ] External services named `{Provider}{Service}`

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| `ProdApiVM` | `ProdApigwVm` | Inconsistent casing (VM vs Vm) |
| `prod_upload_vm` variable | `ProdUploadVm` | Variable names should be PascalCase |
| `AppServers` zone | `AppTier` zone | Zone names should be singular |
| `dev-upload-vm` for production | `prod-upload-vm` | Environment prefix must match node |
| Generic name `Vm1`, `Server1` | `ProdUploadVm` | Names should indicate purpose |

## Related Skills

- `deployment-node-descriptions` - Documenting zones and VMs with specs
- `deployment-tier-patterns` - Standard tier organization
