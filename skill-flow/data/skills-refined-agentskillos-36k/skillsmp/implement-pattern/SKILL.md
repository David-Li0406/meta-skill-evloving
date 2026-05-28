---
name: implement-pattern
description: Apply common patterns (external integration, async processing, multi-tier, caching). Provides tested templates.
---

# Apply LikeC4 Common Patterns

Use this skill when implementing standard architectural patterns.

## Pattern: External System Integration

```likec4
externalService = System_External 'Third-Party API' {
  technology 'REST API'
  description 'External payment processor'
  #External
}

mySystem.api -[calls]-> externalService 'Process payment'
```

## Pattern: Async Processing

```likec4
queue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
  description 'Async job processing'
}

api -[async]-> queue 'Publishes jobs'
worker -[async]-> queue 'Consumes jobs'
```

## Pattern: Multi-Tier Architecture

```likec4
webapp = Container_Webapp 'Web App' {
  technology 'React'
  description 'User interface'
}

api = Container_Api 'API' {
  technology 'Node.js'
  description 'Business logic'
}

database = Container_Database 'Database' {
  technology 'PostgreSQL'
  description 'Data persistence'
}

webapp -[calls]-> api 'API requests'
api -[reads]-> database 'Queries'
api -[writes]-> database 'Updates'
```
