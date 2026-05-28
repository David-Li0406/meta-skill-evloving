# Advanced Writing Patterns

## Algorithm Documentation Pattern

### Structure
```
Algorithm X.Y: [Algorithm Name]

**Input**: [Formal specification of inputs]
**Output**: [Formal specification of outputs]
**Preconditions**: [Required state before execution]
**Postconditions**: [Guaranteed state after execution]

**Procedure**:
1. Initialize [variables] with [values]
2. While [condition]:
   2.1. Execute [operation]
   2.2. Update [state]
3. Return [result]

**Complexity Analysis**:
- Time Complexity: O(...)
- Space Complexity: O(...)
```

## System Architecture Documentation

### Component Description Pattern
```
X.Y [Component Name]

The [component name] subsystem implements [primary function] within the 
[larger system] architecture. The component maintains responsibility for 
[specific duties] and interfaces with [other components] through [protocols].

**Responsibilities**:
- [Responsibility 1]: [Description]
- [Responsibility 2]: [Description]

**Interfaces**:
- **Inbound**: [Protocol/API] for [purpose]
- **Outbound**: [Protocol/API] to [destination]

**State Management**:
The component maintains [state type] through [mechanism], ensuring 
[consistency guarantee] across [scope].
```

## Infrastructure as Code Documentation

### Resource Definition Pattern
```
Resource Type X.Y: [Resource Name]

**Purpose**: [Infrastructure role and function]
**Provider**: [AWS/Azure/GCP/Kubernetes]
**Dependencies**: [Required resources]

**Configuration Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| param_1   | string | Yes | - | [Purpose] |
| param_2   | integer | No | 10 | [Purpose] |

**Provisioning Sequence**:
1. Validate prerequisites
2. Create resource with specified configuration
3. Configure networking/security rules
4. Establish monitoring/logging
5. Verify operational status
```

## API Documentation Pattern

### Endpoint Specification
```
Endpoint X.Y: [HTTP Method] [Path]

**Purpose**: [Business function]
**Authentication**: [Method and requirements]
**Rate Limiting**: [Requests per time unit]

**Request**:
```
Content-Type: application/json
Authorization: Bearer [token]

{
  "field1": "string",
  "field2": integer
}
```

**Response** (Success - 200 OK):
```
{
  "status": "success",
  "data": {
    "id": "string",
    "created_at": "ISO-8601"
  }
}
```

**Error Responses**:
- **400 Bad Request**: Malformed request syntax
- **401 Unauthorized**: Invalid or missing credentials
- **429 Too Many Requests**: Rate limit exceeded
```

## Database Schema Documentation

### Table Definition Pattern
```
Table X.Y: [table_name]

**Purpose**: Stores [data type] for [business function]
**Engine**: [InnoDB/PostgreSQL/etc.]
**Partitioning**: [Strategy if applicable]

**Schema**:
| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| status | ENUM | NOT NULL | Processing state |

**Indexes**:
- **idx_created**: (created_at DESC) - Temporal queries
- **idx_status**: (status, created_at) - Status filtering

**Relationships**:
- **Foreign Keys**: user_id REFERENCES users(id)
- **Cascading**: ON DELETE CASCADE
```

## Deployment Process Documentation

### Pipeline Stage Pattern
```
Stage X.Y: [Stage Name]

**Trigger**: [Condition or event]
**Duration**: [Typical time range]
**Rollback**: [Recovery mechanism]

**Prerequisites**:
1. [Requirement 1]
2. [Requirement 2]

**Execution Steps**:
1. **Validation**: [Checks performed]
2. **Preparation**: [Environment setup]
3. **Deployment**: [Actual deployment action]
4. **Verification**: [Health checks]
5. **Notification**: [Status communication]

**Failure Handling**:
Upon failure at step [n], the system:
1. Halts subsequent operations
2. Initiates rollback procedure
3. Notifies designated personnel
4. Logs failure details for analysis
```

## Security Configuration Documentation

### Policy Definition Pattern
```
Policy X.Y: [Policy Name]

**Scope**: [Resources/Users affected]
**Enforcement**: [Mandatory/Advisory]
**Compliance**: [Standards met]

**Rules**:
1. **Rule Name**: 
   - Condition: [When applied]
   - Action: [Allow/Deny]
   - Resource: [Target]
   - Effect: [Result]

**Exceptions**:
- [Exception case 1]: [Justification]
- [Exception case 2]: [Justification]

**Audit Requirements**:
- Log all [action types]
- Retain logs for [duration]
- Review frequency: [interval]
```

## Performance Optimization Documentation

### Optimization Technique Pattern
```
Optimization X.Y: [Technique Name]

**Target Metric**: [Latency/Throughput/Memory]
**Baseline Performance**: [Current measurements]
**Expected Improvement**: [Percentage or absolute]

**Implementation**:
1. **Analysis Phase**: Profile [component] to identify [bottleneck]
2. **Modification Phase**: Apply [technique] to [component]
3. **Validation Phase**: Measure [metric] under [conditions]

**Trade-offs**:
- **Gains**: [Improvements achieved]
- **Costs**: [Resources/complexity added]
- **Constraints**: [Limitations introduced]

**Measurement Protocol**:
- Load Pattern: [Description]
- Duration: [Time period]
- Metrics Collected: [List]
- Statistical Significance: [Confidence level]
```
