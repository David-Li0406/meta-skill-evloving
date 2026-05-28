---
name: create-relationship
description: Create typed relationships with FQN, proper kinds (calls/async/reads/writes), descriptive labels, and no return relationships.
---

# Create LikeC4 Relationship

Use this skill when connecting elements in model or deployment files.

## Async & Event-Driven Patterns

### The Async Relationship Kind

Use `-[async]->` for message queue and event-driven flows. This creates **no return path** — workers never call back to the publisher.

```likec4
// ✅ Correct: Upload service queues a job, worker consumes it
uploadService -[async]-> jobQueue 'Queue file for processing'
jobQueue -[async]-> worker 'Deliver job'

// ❌ Wrong: Do NOT create call relationships FROM/TO workers
worker -[calls]-> uploadService   // ANTI-PATTERN!
uploadService -[calls]-> worker   // ANTI-PATTERN!
```

### Fail-Fast Pattern with Sync Validation

Validation happens **synchronously** in the producer service BEFORE queuing:

```likec4
model {
  vault = System {
    // Upload service validates FIRST (synchronous)
    uploadService = Container_Service 'Upload Service' {
      validateModule = Component 'Validate' { ... }
      queueModule = Component 'Queue Publisher' { ... }
    }
    
    jobs = Container_Queue 'Job Queue' { ... }
    
    worker = Container_Service 'Worker' {
      // Worker ONLY consumes and processes
      consumerModule = Component 'Consumer' { ... }
    }
  }
  
  // Flow: Validation (sync) → Queue (async) → Processing (async)
  vault.uploadService.validateModule -[uses]-> vault.uploadService.queueModule 'Publish if valid'
  vault.uploadService.queueModule -[async]-> vault.jobs 'Queue validated job'
  vault.worker.consumerModule -[async]-> vault.jobs 'Consume jobs'
}
```

### Relationship Kinds for Async

```likec4
// Async patterns (one-way, no return)
-[async]->       // Message queue, events, notifications
-[sends]->       // Email, alerts, webhooks
-[writes]->      // Database persist (not a call, just mutation)
-[reads]->       // Database query (not a call, just retrieval)

// Example upload → processing flow
uploadService -[async]-> jobQueue 'Queue file'     // ✅ One direction
jobQueue -[async]-> worker 'Deliver job'          // ✅ Message flow
worker -[writes]-> database 'Update status'       // ✅ Persistence, not call
worker -[writes]-> storage 'Save file'            // ✅ Persistence, not call
```

### Retrieval Flow Pattern

For services that fetch from storage/cache, use `-[reads]->` not `-[calls]->`:

```likec4
// ✅ Correct: Reading from database/cache
retrievalService -[reads]-> metadata 'Fetch document metadata'
retrievalService -[reads]-> cache 'Check cache for data'
retrievalService -[reads]-> storage 'Fetch encrypted file'

// ❌ Wrong: Database queries are not "calls"
retrievalService -[calls]-> metadata   // ANTI-PATTERN!
```

## Example

```likec4
mySystem.api -[calls]-> externalService 'Fetches data' {
  description 'HTTPS REST API with OAuth 2.0'
}
```

## Anti-patterns

```likec4
❌ api -> service 'Calls'                    // Missing relationship kind
❌ mySystem.api -[invokes]-> service         // Invalid relationship kind
❌ client -[calls]-> server 'Request'
   server -[calls]-> client 'Response'      // No return relationships!
```
