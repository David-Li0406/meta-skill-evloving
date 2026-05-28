---
name: output-filter
description: Security pattern for filtering data before sending to external entities. Use when preventing excessive data exposure, implementing data minimization, protecting sensitive information in API responses, or ensuring clients receive only necessary data. Addresses "Entity receives excessive data" problem and OWASP API3:2019 Excessive Data Exposure.
---

# Output Filter Security Pattern

Filter data before sending it to an external entity, ensuring that only necessary and authorized data elements are transmitted. This prevents excessive data exposure and enforces data minimization.

## Problem Addressed

**Entity receives excessive data**: System sends more data than the receiver needs or is authorized to see, leading to:
- Exposure of sensitive data (PII, credentials, internal identifiers)
- Privacy violations (GDPR, CCPA)
- Increased attack surface
- Data leakage through traffic interception

## Core Principle

**Never rely on the client to filter sensitive data.**

Data filtering must occur at the server/API level before sending, not at the client level after receiving.

## Why Client-Side Filtering Fails

| Attack Vector | Description |
|---------------|-------------|
| **Traffic sniffing** | Attackers intercept API responses before client filtering |
| **Direct API calls** | Attackers bypass client applications entirely |
| **Client manipulation** | Attackers modify client code to reveal hidden data |
| **Mobile app reverse engineering** | Attackers extract API endpoints and call directly |

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Sender** | Entity | System that sends data |
| **Output Filter** | Enforcement Point | Filters outgoing data |
| **Filter Specification** | Information Point | Defines what data to include/exclude |
| **Receiver** | Entity | External entity receiving data |

### Data Elements

- **raw_data**: Complete data before filtering
- **filtered_data**: Data after filtering (only necessary elements)
- **filter_spec**: Rules defining what to include/exclude
- **context**: Information about receiver, request type, authorization level

## Pattern Flow

```
Sender → [raw_data] → Output Filter
Output Filter → [get_filter_spec(context)] → Filter Specification
Filter Specification → [filter_spec] → Output Filter
Output Filter → [apply filter to raw_data] → Output Filter
Output Filter → [filtered_data] → Receiver
```

1. Sender prepares complete data
2. Output Filter retrieves filter specification based on context
3. Output Filter applies specification, removing unauthorized/unnecessary data
4. Only filtered data is sent to Receiver

## Filtering Strategies

### Allowlist (Preferred)
Explicitly define which fields to include:
```
Include: [id, name, email, created_at]
// All other fields excluded by default
```

### Blocklist (Use with Caution)
Define which fields to exclude:
```
Exclude: [ssn, password_hash, internal_id, credit_card]
// All other fields included by default
```

**Warning**: Blocklists fail when new sensitive fields are added but not blocked.

### Context-Based Filtering
Different filters based on:
- User role/authorization level
- Request type (list vs. detail)
- API version
- Consumer type (internal vs. external)

## Implementation Approaches

### 1. Response Schema Validation
Define explicit response schemas for each endpoint:
- Only fields in schema are returned
- Validates responses match contract
- Catches accidental data exposure

### 2. Data Transfer Objects (DTOs)
Create specific response objects:
```
// Instead of returning database entity directly
User (DB) → UserResponseDTO (filtered)

UserResponseDTO {
    id, name, email, avatar_url
    // Excludes: password_hash, ssn, internal_flags
}
```

### 3. Projection/Selection
Query only needed fields from data source:
```
SELECT id, name, email FROM users
// Instead of SELECT * FROM users
```

### 4. View-Specific Serialization
Custom serializers per context:
- Public API serializer (minimal fields)
- Admin API serializer (more fields)
- Internal API serializer (full access)

## Security Considerations

### Avoid Generic Serialization
Never use generic methods that expose all properties:
```
// AVOID
return user.to_json()
return user.to_dict()
return serialize(user)

// PREFER
return {
    'id': user.id,
    'name': user.name,
    'email': user.email
}
```

### Protect Nested Objects
Data exposure often occurs in nested/related objects:
```
// User response includes related data
{
    "id": 1,
    "name": "Alice",
    "manager": {
        "id": 2,
        "name": "Bob",
        "salary": 150000  // LEAK! Manager salary exposed
    }
}
```

Filter nested objects recursively.

### Error Responses
Don't leak data in error messages:
- Avoid stack traces with internal data
- Don't reveal database structure
- Use generic error codes externally

### Pagination Metadata
Even metadata can leak information:
- Total counts may reveal data existence
- Filter appropriately

### Different Endpoints, Same Data
Ensure consistent filtering across:
- List vs. detail endpoints
- Search endpoints
- Export/download features
- Related resource endpoints

## Common Data to Filter

| Category | Sensitive Fields |
|----------|------------------|
| **Authentication** | password_hash, auth_tokens, API keys, session_ids |
| **Personal (PII)** | SSN, tax_id, credit_card, bank_account |
| **Internal** | internal_id, debug_flags, feature_flags |
| **System** | created_by_system, internal_notes, audit_data |
| **Relationships** | Detailed data of related entities |
| **Metadata** | IP addresses, user agents, timestamps (if sensitive) |

## Relationship to Other Patterns

### Output Filter vs. Authorization
- **Authorization**: Can this user access this resource?
- **Output Filter**: What properties of this resource should user see?

Both are required. User may be authorized to see a resource but not all its properties.

### Output Filter vs. Input Validation
- **Input Validation**: Filter/validate incoming data
- **Output Filter**: Filter outgoing data

Complementary patterns for complete data flow security.

## Implementation Checklist

- [ ] All API endpoints have defined response schemas
- [ ] Response schemas use allowlist approach
- [ ] No generic serialization (to_json, to_dict) for external responses
- [ ] Nested/related objects filtered appropriately
- [ ] Error responses don't leak sensitive data
- [ ] Context-based filtering for different user roles
- [ ] List and detail endpoints have appropriate schemas
- [ ] Export/download features apply same filters
- [ ] Response schema validation in place
- [ ] DTOs or projections used instead of raw entities
- [ ] Regular review of response schemas for new sensitive fields

## Testing for Excessive Data Exposure

1. **Compare responses to schemas**: Actual vs. documented
2. **Test with different roles**: Verify role-based filtering
3. **Inspect raw API responses**: Use proxy tools (Burp, ZAP)
4. **Review database queries**: Check for SELECT *
5. **Audit new fields**: Ensure added to filter specs

## Related Patterns

- **Data Validation** (filter incoming data)
- **Authorisation** (determine resource access)
- **Selective Encrypted Transmission** (protect data in transit)
- **Log Entity Actions** (log data access)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/05_01_001__output_filter/
- OWASP API Security Top 10 - API3:2019 Excessive Data Exposure
- OWASP API Security Top 10 2023 - Broken Object Property Level Authorization
- GDPR Article 5(1)(c) - Data Minimization Principle
