---
name: model-system-containers
description: Model C2 Containers - break system into major deployable units with independent runtime boundaries. Show container relationships and technologies.
---

# Model System Containers (C2)

Use this skill to design the C2 Container diagram - the system's major building blocks.

**Prerequisite:** Read `model-system-context` for C1 context. Then read `create-element` for element basics.

## What is C2 Containers?

C2 answers: **"What are the major building blocks of the system and how do they communicate?"**

**Audience:** Architects and developers  
**Detail Level:** System internals - major deployable units and their interactions

## What is a Container?

A container represents a **runtime boundary** - something that must be running for the system to work. It's defined by:
- **Independent deployment unit** - Can be deployed separately
- **Separate process space** - Not the same runtime as other containers
- **Persistent existence** - Runs continuously or on schedule, not on-demand only

**NOT a Docker container!** (confusing naming). A container is defined by its deployment boundary, not the infrastructure platform.

### Examples of Containers

- ✅ Server-side web application (Node.js, Django, Spring Boot)
- ✅ Client-side web application (React SPA in browser)
- ✅ Desktop or mobile application
- ✅ Microservice or serverless function
- ✅ Database (MongoDB instance, PostgreSQL schema)
- ✅ Message queue (RabbitMQ, Kafka)
- ✅ Object storage (S3, MinIO)
- ✅ Cache (Redis, Memcached)
- ✅ Batch process or scheduled task

### NOT Containers (Common Mistakes)

- ❌ A folder or package in code (that's code organization)
- ❌ A class or module (too fine-grained)
- ❌ A microservice that doesn't run persistently (too conceptual)
- ❌ Multiple related services deployed together (still separate containers)

## Container Design Strategy

Design containers around **independent deployment**, NOT by:
- ❌ Technology stack (orthogonal concern)
- ❌ Team ownership alone (too organizational)
- ❌ Code organization (JAR files, modules - code-level only)

Focus on: **"Can this be deployed independently? Does it have its own process space?"**

## Example: Good vs Bad Container Design

```likec4
// RIGHT: Design by runtime boundary and independent deployment
model {
  vault = System 'Secure Vault' {
    frontend = Container_Spa 'Web UI' {
      technology 'React SPA'
      description 'React single-page app running in browser (separate process space)'
    }
    
    api = Container_API 'REST API' {
      technology 'Node.js, Express'
      description 'REST API backend (independently deployable microservice)'
    }
    
    worker = Container_API 'Processing Worker' {
      technology 'Node.js'
      description 'Async job processor (independently deployable, runs on schedule)'
    }
    
    database = Container_Database 'Database' {
      technology 'MongoDB'
      description 'Document database (independent data store)'
    }
    
    storage = Container_Storage 'Object Storage' {
      technology 'MinIO S3-compatible'
      description 'File storage system (independent storage tier)'
    }
    
    queue = Container_Queue 'Message Queue' {
      technology 'RabbitMQ'
      description 'Job queue (independent messaging broker)'
    }
  }
}

// WRONG: Don't create containers for code organization
// ❌ UserService.js as a container
// ❌ models/ folder as a container
// ❌ repositories/ as a container
// These are code-level organization, not runtime boundaries
```

## Step 1: Identify System Containers

List major deployable units needed for the system to work:

```likec4
model {
  vault = System 'Secure Vault' {
    // User-facing interface
    webapp = Container_Spa 'Web UI' {
      technology 'React 18'
      description 'Single-page web application for users'
    }
    
    // API backend
    api = Container_API 'Upload Service' {
      technology 'Node.js, Express'
      description 'REST API for file uploads and metadata'
    }
    
    // Async processing
    worker = Container_API 'Processing Worker' {
      technology 'Node.js'
      description 'Asynchronous worker processing files'
    }
    
    // Persistence
    database = Container_Database 'Metadata Store' {
      technology 'MongoDB 5.0'
      description 'Document database storing metadata'
    }
    
    storage = Container_Storage 'File Storage' {
      technology 'MinIO S3-compatible'
      description 'Encrypted file object storage'
    }
    
    // Messaging
    queue = Container_Queue 'Job Queue' {
      technology 'RabbitMQ'
      description 'Message queue for async jobs'
    }
  }
}
```

**Key questions:**
- What runs in its own process space?
- What can be deployed independently?
- What would need to be restarted separately?

## Step 2: Create Container Relationships

Connect containers showing HOW they interact:

```likec4
model {
  // Synchronous flows (API calls)
  webapp -> api 'Browser calls via HTTPS'
  api -> database 'Query and update metadata'
  api -> storage 'Upload and download files'
  
  // Asynchronous flows (messaging)
  api -> queue 'Publish processing job to'
  queue -> worker 'Deliver job to'
  worker -> database 'Update job status'
  worker -> storage 'Access file for processing'
  
  // External integrations
  api -> scanner 'Scan file via VirusTotal API'
}
```

**Relationship types:**
- **Synchronous:** `-[calls]->` `api -> database` (request/response)
- **Asynchronous:** `-[async]->` `api -> queue` (fire-and-forget, messaging)
- **Reads/Writes:** `-[reads]->` `worker -> database` (data access)

### Patterns to Show

**HTTP/REST:**
```likec4
webapp -> api 'Browser calls upload API'
```

**Database queries:**
```likec4
api -> database 'Query file metadata'
```

**Message queue (async):**
```likec4
api -> queue 'Publish processing job'
worker -> database 'Update status after processing'
```

**External APIs:**
```likec4
api -> externalService 'Call third-party service'
```

## Complete C2 Example

```likec4
model {
  customer = Actor_Person 'Customer' {
    description 'End user'
  }
  
  browser = Container_Browser 'Web Browser' {
    description 'User browser'
  }
  
  vault = System 'Secure Vault' {
    webapp = Container_Spa 'Web UI' {
      technology 'React 18'
      description 'Single-page app for uploading and managing files'
    }
    
    api = Container_API 'Upload Service' {
      technology 'Node.js, Express'
      description 'REST API for file operations'
    }
    
    worker = Container_API 'Processing Worker' {
      technology 'Node.js'
      description 'Background job processor'
    }
    
    database = Container_Database 'Database' {
      technology 'MongoDB'
      description 'Metadata and job status'
    }
    
    storage = Container_Storage 'Object Storage' {
      technology 'MinIO'
      description 'Encrypted file storage'
    }
    
    queue = Container_Queue 'Job Queue' {
      technology 'RabbitMQ'
      description 'Async job queue'
    }
  }
  
  scanner = Actor_System 'Virus Scanner' {
    description 'VirusTotal scanning service'
  }
  
  // Relationships
  customer -> browser 'Uses'
  browser -> webapp 'Accesses via browser'
  webapp -> api 'API calls to'
  
  api -> database 'Queries and updates'
  api -> storage 'Uploads and downloads'
  api -> queue 'Publishes jobs to'
  
  queue -> worker 'Delivers jobs to'
  worker -> database 'Updates status in'
  worker -> storage 'Reads and processes'
  worker -> scanner 'Scans via'
}
```

## C2 View

Create the C2 Container view:

```likec4
views {
  view c2_containers {
    title 'C2 / Secure Vault System Internals'
    description 'Major containers and their interactions'
    
    include customer, browser
    include vault.*
    include scanner
  }
}
```

## C2 Design Checklist

- [ ] System broken into logical, independently deployable units
- [ ] Each container has clear purpose and responsibility
- [ ] Technologies documented for each container
- [ ] All major relationships between containers shown
- [ ] Synchronous vs asynchronous patterns clear
- [ ] One C2 Container view showing all containers
- [ ] View description explains scope and audience

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| Too few containers (everything in one) | Separate by deployment unit | Limits scaling and independent evolution |
| Too many containers (every class) | Group by runtime boundary | C2 becomes unreadable, loses architecture |
| Missing relationships | Show all significant interactions | Doesn't reveal how system actually works |
| Vague container names | Descriptive names: "UploadService" not "Service" | Clear purpose and responsibility |
| Skip relationships | Document how containers communicate | Others can't understand system design |

## Next Steps

After defining C2:
1. Read `model-system-components` to detail complex containers
2. Use `create-relationship` for precise protocol documentation

## Related Skills

- `model-system-context` - C1 Context (start here first)
- `model-system-components` - C3 detailed components
- `create-element` - Creating individual elements
- `create-relationship` - Defining relationships
