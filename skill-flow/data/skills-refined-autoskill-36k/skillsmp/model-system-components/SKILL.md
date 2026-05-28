---
name: model-system-components
description: Model C3 Components - show internal modules within containers. Group related code into logical components with responsibilities for complex containers only.
---

# Model System Components (C3)

Use this skill to design C3 Component diagrams - the internal structure of important containers.

**Prerequisite:** Read `model-system-containers` for C2. Only create C3 for complex/critical containers.

## What is C3 Components?

C3 answers: **"What are the internal modules of this container and how do they interact?"**

**Audience:** Developers implementing the container  
**Detail Level:** Code-level organization - logical groupings of related functionality

**Important:** C3 is OPTIONAL - only create for complex containers. Simple containers don't need C3.

## What is a Component?

A component is a **logical grouping of related functionality** within a container.

**Critical distinctions:**
- **NOT separately deployable** - All components in a container execute in the same process
- **NOT individual classes** - Components group multiple classes/modules
- **NOT code organization** - Not about folders or packages
- **Code-level design** - How code is logically organized, not infrastructure

### Examples of Components

- ✅ A group of related classes implementing a service interface
- ✅ A JavaScript module with exported functions
- ✅ A microservice layer (controllers, services, repositories)
- ✅ A set of C files in a functional group
- ✅ A functional programming module grouping related functions

### NOT Components

- ❌ Individual UserService.js class
- ❌ Individual UserRepository.js class
- ❌ models/ folder as component (code organization)
- ❌ utils/ folder (generic utilities, not a component)
- ❌ controllers/ as separate component (architectural layer, not business responsibility)

## Component Design: Grouping Strategy

Group related code by **business responsibility and functionality**, NOT by:
- ❌ Code organization (folders, packages, modules)
- ❌ Technology framework (controllers, services, repos as separate components)
- ❌ Architectural layers (don't create one component per layer)

DO group by:
- ✅ Shared responsibility or feature
- ✅ Related business concepts
- ✅ Well-defined internal interface

### Example: Good vs Bad Grouping

```likec4
// RIGHT: Components by business responsibility
api = Container_API 'Upload Service' {
  // Handles API request routing and lifecycle
  router = Component_Service 'API Router' {
    description 'Express middleware routes HTTP requests'
  }
  
  // Authentication and authorization
  auth = Component_Service 'Authentication' {
    description 'JWT validation, user identity verification'
  }
  
  // Core business logic
  upload = Component_Service 'Upload Handler' {
    description 'Processes file uploads, validation, queuing'
  }
  
  // Data access abstraction
  dataAccess = Component_Service 'Data Repository' {
    description 'Database queries abstraction layer'
  }
  
  // External integrations
  external = Component_Service 'External Services' {
    description 'Calls to VirusTotal, payments, notifications'
  }
}

// WRONG: Components by code organization or framework
// ❌ Create separate components for:
// - controllers/ folder
// - services/ folder
// - repositories/ folder
// - models/ folder
// These are organizational structure, not functional groupings

// ALSO WRONG: Too granular
// ❌ UserController, UserService, UserRepository as separate components
// Group these together as "User Management" or "Authentication"
```

## Step 1: Identify Complex Containers

Before creating C3, decide WHICH containers need detail:

**Create C3 for:**
- ✅ Complex containers (many responsibilities)
- ✅ Critical containers (business-critical, high-risk)
- ✅ Containers others will need to understand deeply
- ✅ Frequently modified containers

**Skip C3 for:**
- ❌ Simple containers (few, obvious responsibilities)
- ❌ Simple databases or storage
- ❌ Third-party services you don't control
- ❌ Containers everyone understands already

**Example decision:**
```
✅ Create C3: Upload Service (complex business logic)
✅ Create C3: Processing Worker (orchestration logic)
❌ Skip C3: Database (it's just MongoDB)
❌ Skip C3: Message Queue (it's just RabbitMQ)
❌ Skip C3: External Scanner API (we don't control it)
```

## Step 2: Define Components for Selected Containers

For complex containers, break into logical components:

```likec4
api = Container_API 'Upload Service' {
  description 'REST API for file upload and metadata management'
  
  // API request routing and middleware
  router = Component 'Request Router' {
    description 'Express.js middleware routing HTTP requests to handlers'
  }
  
  // Authentication and access control
  auth = Component 'Authentication Module' {
    description 'JWT token validation, user identity verification'
  }
  
  // File upload processing logic
  upload = Component 'Upload Handler' {
    description 'File validation, size checks, queuing for processing'
  }
  
  // Database query abstraction
  storage = Component 'Data Access' {
    description 'Abstracts MongoDB queries, maintains data consistency'
  }
  
  // External API interactions
  integrations = Component 'External Services' {
    description 'Calls to VirusTotal, payment gateway, notifications'
  }
}
```

## Step 3: Create Component Relationships

Show how components interact WITHIN the container:

```likec4
model {
  api = Container_API 'Upload Service' {
    router = Component 'Router' { ... }
    auth = Component 'Auth' { ... }
    upload = Component 'Upload Handler' { ... }
    storage = Component 'Data Access' { ... }
    integrations = Component 'External Services' { ... }
    
    // Internal interactions
    router -> auth 'Validates token via'
    router -> upload 'Routes upload to'
    upload -> storage 'Queries and updates via'
    upload -> integrations 'Calls external services via'
  }
}
```

## Complete C3 Example: Upload Service

```likec4
model {
  browser = Container_Browser 'Browser' { ... }
  database = Container_Database 'Database' { ... }
  scanner = System 'Virus Scanner' { ... }
  
  api = Container_API 'Upload Service' {
    description 'REST API for secure file uploads with validation and scanning'
    
    // Entry point - HTTP routing
    router = Component 'API Router' {
      #router
      technology 'Express.js middleware'
      description 'Routes HTTP requests to appropriate handlers'
    }
    
    // Security layer
    auth = Component 'Authentication' {
      #security
      technology 'JWT'
      description 'Validates JWT tokens, identifies users'
    }
    
    // Business logic
    upload = Component 'Upload Handler' {
      #business
      technology 'Node.js'
      description 'Validates file (size, type), queues for processing, returns upload ID'
    }
    
    // Data persistence
    dataAccess = Component 'Data Repository' {
      #persistence
      technology 'MongoDB driver'
      description 'Abstracts database queries for uploads, metadata, quotas'
    }
    
    // External integrations
    external = Component 'External Services' {
      #integration
      technology 'HTTP clients'
      description 'Calls VirusTotal API, payment systems, notification service'
    }
  }
  
  // Component interactions (within container)
  router -> auth 'Validates token'
  auth -> router 'Returns user identity'
  router -> upload 'Routes valid requests'
  upload -> dataAccess 'Checks quota, stores metadata'
  dataAccess -> database 'Query/update operations'
  upload -> external 'Notifies payment system'
  
  // Container interactions (with outside world)
  browser -> router 'HTTP POST /upload'
  upload -> queue 'Publish scan job'
}
```

## C3 View

Create C3 Component view for the container:

```likec4
views {
  view c3_upload_service {
    title 'C3 / Upload Service'
    description 'Internal components of the Upload Service container'
    
    include customer, browser
    include vault.api.*
    include vault.api
    include vault.minio.*
    include vault.queue.*
    include scanner
  }
}
```

## When to Create C3

**Key principle:** Create C3 diagrams **sparingly** (typically 2-5 maximum for entire system)

Create C3 when:
- Container is complex (many responsibilities)
- Multiple teams need to understand internals
- High-risk / business-critical functionality
- Frequently modified or refactored

**Do NOT create C3 for:**
- Simple containers (obvious structure)
- Databases and storage (no components to show)
- Third-party services (you don't control internals)
- Simple microservices (responsibilities are obvious)

## C3 Naming Conventions

**Component IDs:** Use descriptive names reflecting responsibility
```likec4
router = Component 'API Router'           // ✅ Clear purpose
auth = Component 'Authentication'         // ✅ Business term
upload = Component 'Upload Handler'       // ✅ Specific action
storage = Component 'Data Repository'     // ✅ Role in container

❌ Component 'Service'                    // Too vague
❌ Component 'Handler'                    // Too generic
❌ Component 'Module'                     // Meaningless
```

**View naming:** Reference the container name
```likec4
c3_upload_service → "C3 / Upload Service"
c3_worker → "C3 / Processing Worker"
```

## C3 Design Checklist

- [ ] Only created for complex/critical containers (2-5 max)
- [ ] Each component has clear responsibility
- [ ] Components grouped by business function, not code organization
- [ ] All significant internal interactions shown
- [ ] Component descriptions explain purpose, not implementation
- [ ] One C3 view per component diagram
- [ ] View title references container name: "C3 / [Container Name]"

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| Create C3 for every container | Only complex/critical containers | Reduces documentation burden |
| Components = code organization (folders) | Components = business responsibility | C3 explains architecture, not folder structure |
| Too granular (class-level components) | Logical groupings of related classes | Components abstract away code details |
| Components as architectural layers | Components by shared responsibility | Avoids artificial separation |
| Unclear component names | Descriptive names: "RequestRouter", "UserAuth" | Purpose immediately clear |

## Next Steps

After defining C3:
1. Use `design-view` to organize all C1/C2/C3 views
2. Use `validate-model` to check consistency
3. Create deployment diagrams with `model-deployment-hierarchy`

## Related Skills

- `model-system-context` - C1 Context (start here first)
- `model-system-containers` - C2 Containers (prerequisite)
- `design-view-hierarchy` - Organizing views in hierarchy
- `create-relationship` - Detailed relationship documentation
