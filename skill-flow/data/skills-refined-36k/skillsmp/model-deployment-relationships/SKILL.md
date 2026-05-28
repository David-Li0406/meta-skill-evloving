---
name: model-deployment-relationships
description: Mirror system model relationships in deployment with concrete protocols, ports, and network flows. Create inter-tier connectivity showing actual TCP/UDP communication.
---

# Model Deployment Relationships

Use this skill when creating relationships between deployment infrastructure elements.

**Prerequisite:** Read `model-deployment-hierarchy` for basic infrastructure structure.

## Core Principle: Mirror System Relationships

**For every relationship in the system model, create a corresponding deployment relationship with specific protocol/port details.**

This ensures:
1. **Deployment completeness** - Every logical interaction has physical implementation
2. **Firewall rule derivation** - Security teams can extract exact port/protocol requirements
3. **Network diagram accuracy** - Shows actual TCP/UDP flows between infrastructure
4. **Troubleshooting** - Operators know which ports to check when debugging connectivity

## System Model → Deployment Mapping

| System Model Relationship | Deployment Relationship | Protocol |
|---------------------------|-------------------------|----------|
| `frontend -[calls]-> api` | `frontendInstance -> apiInstance` | HTTPS/443 |
| `api -[calls]-> service` | `apiInstance -> serviceInstance` | HTTP or custom port |
| `service -[async]-> queue` | `serviceInstance -> queueInstance` | AMQP/5672, MQTT, etc. |
| `service -[reads]-> db` | `serviceInstance -> dbInstance` | TCP with DB port (3306, 5432, 27017) |
| `service -[writes]-> storage` | `serviceInstance -> storageInstance` | S3/9000, NFS, etc. |

## Pattern: Concrete Protocol Relationships

**System model shows logical interactions:**
```likec4
// system-model.c4
vault.frontend -[calls]-> vault.api 'Makes API requests'
vault.api -[calls]-> vault.uploadService 'Route uploads'
vault.uploadService -[async]-> jobs 'Queue for processing'
vault.worker -[reads]-> docDB 'Fetch metadata'
```

**Deployment model shows physical connectivity:**
```likec4
// deployment.c4
UserBrowser.browserApp.frontend -> Prod.Dmz.ProdApigwVm.apiApp "API requests" {
  description "any -> 443 (HTTPS)"
}

Prod.Dmz.ProdApigwVm.apiApp -> Prod.AppTier.ProdUploadVm.uploadApp "Route uploads" {
  description "443 -> 3001"
}

Prod.AppTier.ProdUploadVm.uploadApp -> Prod.ProcTier.ProdQueueVm.queueApp "Queue jobs" {
  description "3001 -> 5672 (AMQP)"
}

Prod.ProcTier.ProdWorkerVm.workerApp -> Prod.DataTier.ProdDatabaseVm.dbApp "Persist metadata" {
  description "any -> 27017 (MongoDB)"
}
```

## Common Protocol Mappings

### HTTP/HTTPS Services
- **System:** `-[calls]->`
- **Deployment:** `-> ... { description "... -> 443 (HTTPS)" }` or custom port

### Message Queues
- **System:** `-[async]->`
- **Deployment:** `-> ... { description "... -> 5672 (AMQP)" }` or other message protocol

### Databases
- **System:** `-[reads]->` or `-[writes]->`
- **Deployment:** `-> ... { description "... -> 27017 (MongoDB)" }` or specific DB port

### Object Storage
- **System:** `-[writes]->` to storage
- **Deployment:** `-> ... { description "... -> 9000 (S3 API)" }`

### External APIs
- **System:** `-[calls]-> externalService`
- **Deployment:** `-[https]-> ... { description "any -> 443" }`

## Anti-Pattern: Missing Deployment Relationships

❌ **Bad:** System model shows relationships, deployment only shows instances
```likec4
// system-model.c4
api -[calls]-> uploadService
uploadService -[async]-> queue

// deployment.c4 - INCOMPLETE!
apiApp = Node_App { instanceOf vault.api }
uploadApp = Node_App { instanceOf vault.uploadService }
// Missing: apiApp -> uploadApp relationship!
```

✅ **Good:** Every system relationship mirrored in deployment
```likec4
// system-model.c4
api -[calls]-> uploadService

// deployment.c4 - COMPLETE
apiApp = Node_App { instanceOf vault.api }
uploadApp = Node_App { instanceOf vault.uploadService }
apiApp -> uploadApp "Route uploads" {
  description "443 -> 3001 (HTTP)"
}
```

## Complete Tier-to-Tier Example

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    Zone Dmz { 
      ProdApigwVm = Node_Vm {
        apiApp = Node_App { instanceOf vault.api }
      }
    }
    
    AppTier = Zone {
      ProdUploadVm = Node_Vm {
        uploadApp = Node_App { instanceOf vault.uploadService }
      }
    }
    
    DataTier = Zone {
      ProdDatabaseVm = Node_Vm {
        dbApp = Node_App { instanceOf vault.docDB }
      }
    }
  }
}

// Relationships showing tier-to-tier connectivity
Prod.Dmz.ProdApigwVm.apiApp -> Prod.AppTier.ProdUploadVm.uploadApp {
  description "10.0.0.10 -> 10.1.0.12:3001 (HTTP)"
}

Prod.AppTier.ProdUploadVm.uploadApp -> Prod.DataTier.ProdDatabaseVm.dbApp {
  description "10.1.0.12 -> 10.3.0.16:27017 (MongoDB)"
}
```

## Firewall Rule Derivation

From deployment relationships, security teams can extract firewall rules:

```
From: Prod.AppTier.ProdUploadVm.uploadApp
To:   Prod.DataTier.ProdDatabaseVm.dbApp
Port: 27017
Rule: AppTier → DataTier TCP/27017
```

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| Generic "network traffic" | Specific ports and protocols | Enables firewall rule creation |
| Relationships in system only | Mirror in deployment with ports | Operators need actual connectivity |
| Multiple protocol descriptions | One direction, one protocol | Clear and unambiguous |

## Related Skills

- `model-deployment-hierarchy` - Infrastructure hierarchy and structure
- `configure-deployment-firewall` - Extract and document firewall rules
