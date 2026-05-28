---
name: create-sequence-view
description: Create sequence views showing temporal flows and user interactions. Uses plain arrows with descriptive labels (no relationship kinds).
---

# Create Dynamic Sequence View

Use this skill when documenting use case flows and interactions.

## Core Requirement: Always Include Initiating Actors

**Dynamic views MUST explicitly show the actor(s) that initiate the flow for context:**
- Start every sequence with the external actor (user, external system, scheduler)
- Show which user action triggers which internal flows
- Make causality explicit: "Who does what? When? Why?"
- This answers: "What triggers this behavior? Who is involved?"

## Organization & Purpose

Place sequence/dynamic views in the `'Use Cases'` subfolder to show **temporal flows** - how the system behaves during important operations.

**Types of use cases to document:**
- **User workflows:** Upload → validation → processing → storage (happy path)
- **Validation & error flows:** Input validation, exception handling, retries
- **Async patterns:** Message queues, background jobs, notifications
- **Data flows:** Data movement through system (retrieval, transformation, storage)
- **Disaster recovery:** Failover, replication, recovery procedures
- **Integration patterns:** External system interactions, polling, webhooks

```likec4
views 'Use Cases' {
  dynamic view upload_flow { ... }
  dynamic view retrieval_flow { ... }
  dynamic view backup_replication { ... }
  dynamic view error_handling { ... }
}
```

## Requirements

1. **Use `dynamic view`** with descriptive ID
2. **Include initiating actor** - ALWAYS start with external actor (user, system, scheduler)
3. **No relationship kinds:** Use plain `->` not `-[kind]->`
4. **Step labels:** Add descriptive text for each interaction explaining WHAT happens
5. **Temporal order:** Steps execute top-to-bottom showing sequence
6. **Folder organization:** Group all use cases in `views 'Use Cases'` subfolder
7. **Title format:** "Use Cases / [WorkflowName]" (e.g., "Use Cases / Upload")

## Example

```likec4
views 'Use Cases' {
  dynamic view sequence_upload {
    title 'Use Cases / Document Upload Flow'
  
  user -> mySystem.webapp 'Opens upload form'
  mySystem.webapp -> mySystem.api 'POST /upload'
  mySystem.api -> mySystem.storage 'Store file'
  mySystem.api -> mySystem.queue 'Queue processing job'
  mySystem.queue -> mySystem.worker 'Execute job'
  mySystem.worker -> mySystem.database 'Update metadata'
}
```
