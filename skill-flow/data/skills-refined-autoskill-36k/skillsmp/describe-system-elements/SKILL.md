---
name: describe-system-elements
description: Write descriptions for system model elements using metadata blocks for structured business/technical data. Makes architecture queryable and reportable.
---

# Describe System Elements

Use this skill to create comprehensive descriptions for system model containers and components.

**Use metadata blocks for structured, queryable business/technical context.**

## Metadata Blocks: Why Use Them

**Advantages over plain text descriptions:**
- Structured data accessible via LikeC4 API
- Filterable: Find all services with `tags: ['backend']`
- Queryable: Group by `team`, `framework`, `regions`
- Reportable: Generate compliance/dependency reports
- Version-controlled: Easy to track changes

## Container/Component Metadata Format

```likec4
uploadService = Container_Service 'Upload Service' {
  #backend #microservice #critical
  technology 'Node.js / Express'
  
  link https://docs.company.com/upload-api 'API Documentation'
  link https://wiki.company.com/runbooks/upload-service 'Runbook'
  link https://github.com/company/upload-service 'Source Code'
  
  description """
    Handles file uploads and validates content before 
    queuing for async processing.
    
    **Responsibilities:**
    - Receive multipart file uploads
    - Fail-fast validation (size, type, malware scan)
    - Queue validated files for processing
  """
  
  metadata {
    team 'Platform'
    team_contact 'platform@company.com'
    owner 'alice@company.com'
    framework 'Node.js'
    framework_version '18.0'
    language 'JavaScript'
    sla '99.9%'
    rto '5 minutes'
    rpo '1 hour'
    compliance_tags ['PCI', 'SOC2']
    contact_channels ['platform@company.com', '#platform-team']
  }
}
```

## Metadata Best Practices

### Links: External Resources

Use `link` property for documentation (rendered in diagrams):

```likec4
element MyService {
  link https://docs.company.com/api 'API Documentation'
  link https://github.com/org/repo 'Source Code'
  link https://grafana.company.com/d/service 'Dashboard'
  link ../src/service/index.ts#L1-L50 'Implementation'
  
  description "Service description..."
}
```

### Single Values: Key-Value Pairs

```likec4
metadata {
  team 'Backend Team'
  sla '99.9%'
  owner 'alice@company.com'
  rto '5 minutes'
}
```

### Multiple Values: Arrays (Explicit Syntax)

```likec4
metadata {
  compliance_tags ['PCI', 'SOC2', 'HIPAA']
  regions ['us-east-1', 'eu-west-1']
  owners ['alice@company.com', 'bob@company.com']
  dependencies ['database', 'queue', 'cache']
  contact_channels ['team@company.com', '#team-slack']
}
```

### Avoid Duplication

Don't repeat model-level properties or relationship-derived data:

```likec4
// ❌ Bad - duplicating tags and ports
element MyService {
  #backend #critical
  metadata {
    tags ['backend', 'critical']  // Already on element!
    port '443'  // Derived from HTTPS relationship
  }
}

// ✅ Good - only additional metadata
element MyService {
  #backend #critical
  metadata {
    team 'Platform'
    sla '99.9%'
    compliance_tags ['SOC2']  // Different from architectural tags
  }
}
```

### Structured Data: YAML/JSON Strings

For complex structured data, use triple-quoted strings:

```likec4
metadata {
  slo_config '''
    availability: 99.9%
    latency_p99: 200ms
    error_rate: 0.1%
  '''
  
  deployment_config '''
    {
      "replicas": 3,
      "cpu": "2",
      "memory": "4Gi",
      "env": "production"
    }
  '''
}
```

## Template: Service Container

```likec4
uploadService = Container_Service 'Upload Service' {
  #backend #microservice #critical
  technology 'Node.js / Express'
  
  link https://docs.company.com/upload-api 'API Documentation'
  link https://wiki.company.com/runbooks/upload-service 'Runbook'
  link https://github.com/company/upload-service 'Repository'
  
  description """
    Handles file uploads and validates content before queuing for processing.
    
    **Responsibilities:**
    - Receive multipart file uploads
    - Fail-fast validation (size, type, malware scan)
    - Queue validated files for async processing
    
    **Dependencies:**
    - RabbitMQ (job queue)
    - MongoDB (metadata storage)
    
    **Performance:**
    - Max upload size: 5GB
    - Response time: <2s for validation
    - Throughput: 100 requests/sec
  """
  
  metadata {
    team 'Platform'
    owner 'alice@company.com'
    framework 'Node.js 18'
    sla '99.9%'
    rto '5 minutes'
    rpo '1 hour'
    contact_channels ['platform@company.com', '#platform-team']
  }
}
```

## Template: Component

```likec4
validateModule = Component 'File Validator' {
  #validation #security
  technology 'Multer + Custom validation'
  
  link https://wiki.company.com/validation-rules 'Validation Rules'
  
  description """
    Validates uploaded files against security and format policies.
    
    **Validates:**
    - File size (max 5GB)
    - MIME type whitelist
    - ClamAV virus signature
    
    **Returns:**
    - ValidationResult { isValid, reason, fileId }
  """
  
  metadata {
    owner 'alice@company.com'
    complexity 'high'
    coverage '95%'  // test coverage
  }
}
```

## Querying Metadata (For Tooling)

Metadata becomes accessible via the LikeC4 API:

```typescript
// Find all critical services
const critical = model.elements()
  .filter(e => {
    const tags = e.getMetadata('compliance_tags')
    return Array.isArray(tags) && tags.includes('critical')
  })

// Group by team
const byTeam = new Map()
for (const element of model.elements()) {
  const team = element.getMetadata('team')
  if (team) {
    if (!byTeam.has(team)) byTeam.set(team, [])
    byTeam.get(team).push(element)
  }
}

// Find multi-region services
const multiRegion = model.elements()
  .filter(e => {
    const regions = e.getMetadata('regions')
    return Array.isArray(regions) && regions.length > 1
  })
```

## Common Metadata Keys

### Ownership & Contact

```likec4
metadata {
  team 'Platform'
  team_contact 'platform@company.com'
  owner 'alice@company.com'
  owners ['alice@company.com', 'bob@company.com']
  contact_channels ['team@company.com', '#team-slack', '+1-555-0100']
}
```

### Technical Details

```likec4
metadata {
  framework 'Node.js'
  framework_version '18.0'
  language 'JavaScript'
  database 'MongoDB'
  cache 'Redis'
  messaging 'RabbitMQ'
}
```

### SLOs & Reliability

```likec4
metadata {
  sla '99.9%'
  rto '5 minutes'
  rpo '1 hour'
  max_latency_p99 '200ms'
  error_budget_monthly '43.2 minutes'
}
```

### Compliance & Security

```likec4
metadata {
  compliance_tags ['PCI', 'SOC2', 'HIPAA']
  data_classification 'sensitive'
  encryption 'TLS 1.3'
  authentication 'OAuth 2.0'
}
```

### Deployment & Scaling

```likec4
metadata {
  regions ['us-east-1', 'eu-west-1']
  replicas '3'
  auto_scaling 'enabled'
  max_replicas '10'
  deployment_frequency 'continuous'
}
```

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| Skip metadata, use only descriptions | Use both metadata + description | Metadata enables tooling/queries |
| Duplicate tags in metadata | Tags go in `#tags`, not metadata | Single source of truth |
| Store all data in descriptions | Use structured metadata keys | Enables reporting |
| Empty metadata blocks | Include relevant keys only | Focused, useful metadata |

## Related Skills

- `describe-deployment-elements` - Deployment element descriptions with specs
- `create-element` - Creating elements with basic properties
