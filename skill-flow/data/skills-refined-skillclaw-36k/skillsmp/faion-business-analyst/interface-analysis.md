---
id: interface-analysis
name: "Interface Analysis"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Interface Analysis

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #interface #integration #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Systems are built in isolation. Integration with other systems is an afterthought. Data flows between systems are undocumented. When systems need to communicate, it becomes a scramble. Interface requirements are discovered during development.

Without interface analysis:
- Integration failures
- Data inconsistencies
- Undefined handoffs
- Late surprises

---

## Framework

### What is Interface Analysis?

Interface analysis identifies and documents the boundaries and connections between:
- The solution and external systems
- The solution and users
- Different components of the solution
- The solution and external parties

### Interface Types

| Type | Description | Examples |
|------|-------------|----------|
| **User interface** | Human interaction points | Screens, reports, forms |
| **System interface** | System-to-system connections | APIs, file transfers, databases |
| **Hardware interface** | Physical device connections | Scanners, printers, sensors |
| **Communication interface** | Data exchange protocols | HTTP, SFTP, message queues |

### Step 1: Identify Interfaces

List all connection points:

**Questions:**
- What systems will this solution connect to?
- What data comes in and goes out?
- Who are the users?
- What devices are involved?
- What external parties interact?

### Step 2: Document Interface Details

For each interface, capture:

| Attribute | Description |
|-----------|-------------|
| **Name** | Identifier for the interface |
| **Type** | User/System/Hardware/Communication |
| **Direction** | Inbound/Outbound/Bidirectional |
| **Source/Target** | What systems/users are connected |
| **Data** | What information is exchanged |
| **Format** | Data structure and encoding |
| **Protocol** | How exchange happens |
| **Frequency** | When exchange occurs |
| **Volume** | How much data |
| **Security** | Authentication, encryption |
| **Error handling** | What happens on failure |

### Step 3: Define Data Elements

For each interface, specify data:

| Element | Type | Required | Validation | Description |
|---------|------|----------|------------|-------------|
| [Field] | [Type] | Y/N | [Rules] | [Meaning] |

### Step 4: Specify Behaviors

Define how interface operates:
- Normal flow
- Error scenarios
- Retry logic
- Timeout handling

### Step 5: Validate with Stakeholders

Review interfaces with:
- Technical teams of connected systems
- Users for UI interfaces
- Operations for monitoring
- Security for access control

---

## Templates

### Interface Specification Template

```markdown
# Interface Specification: [Interface Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]

## Overview

| Attribute | Value |
|-----------|-------|
| **Interface ID** | [IF-XXX] |
| **Interface Name** | [Name] |
| **Type** | [User/System/Hardware] |
| **Direction** | [In/Out/Bidirectional] |
| **Description** | [What this interface does] |

## Connected Systems

| System | Role | Contact |
|--------|------|---------|
| [This solution] | [Provider/Consumer] | [Name] |
| [External system] | [Provider/Consumer] | [Name] |

## Data Specification

### [Message/Payload Name]

**Direction:** [Inbound/Outbound]
**Format:** [JSON/XML/CSV/Binary]
**Encoding:** [UTF-8/ASCII]

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| [field_name] | [type] | Y/N | [rules] | [description] |

### Example Payload
```json
{
  "field1": "value1",
  "field2": 123
}
```

## Technical Specification

| Attribute | Value |
|-----------|-------|
| **Protocol** | [REST/SOAP/File/Queue] |
| **Endpoint** | [URL or path] |
| **Method** | [GET/POST/PUT/etc.] |
| **Authentication** | [OAuth/API Key/etc.] |
| **Rate Limit** | [X requests per Y] |
| **Timeout** | [X seconds] |

## Operational Specification

| Attribute | Value |
|-----------|-------|
| **Frequency** | [Real-time/Batch/On-demand] |
| **Schedule** | [If batch, when] |
| **Volume** | [Expected messages/records] |
| **SLA** | [Availability, response time] |

## Error Handling

| Error Condition | Response | Retry? | Notification |
|-----------------|----------|--------|--------------|
| [Condition 1] | [Action] | Y/N | [Who/How] |
| [Condition 2] | [Action] | Y/N | [Who/How] |

## Security Requirements
- [Security requirement 1]
- [Security requirement 2]

## Dependencies
- [Dependency 1]
- [Dependency 2]
```

### Interface Catalog Template

```markdown
# Interface Catalog: [System Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]

## Interface Summary

| ID | Name | Type | Direction | External System | Status |
|----|------|------|-----------|-----------------|--------|
| IF-001 | [Name] | API | Out | [System] | Active |
| IF-002 | [Name] | File | In | [System] | Design |
| IF-003 | [Name] | UI | Bi | User | Active |

## Interface Diagram

```
[External System A] ─── IF-001 ───> [Our System] ─── IF-003 ───> [User]
                                          │
                                          │
                                          ▼
                                    [IF-002 File]
                                          │
                                          ▼
                                  [External System B]
```

## Detailed Specifications
- [IF-001 Specification](link)
- [IF-002 Specification](link)
- [IF-003 Specification](link)
```

---

## Examples

### Example 1: REST API Interface

**Interface:** Customer Data API

| Attribute | Value |
|-----------|-------|
| Type | System Interface |
| Direction | Outbound (we provide) |
| Protocol | REST |
| Format | JSON |

**Endpoint:** `GET /api/v1/customers/{id}`

**Response:**
```json
{
  "id": "C-12345",
  "name": "Acme Corp",
  "email": "contact@acme.com",
  "created": "2026-01-15T10:30:00Z"
}
```

**Error Codes:**
- 200: Success
- 404: Customer not found
- 401: Unauthorized
- 500: Server error

### Example 2: File Transfer Interface

**Interface:** Daily Sales Report

| Attribute | Value |
|-----------|-------|
| Type | System Interface |
| Direction | Inbound |
| Protocol | SFTP |
| Format | CSV |

**File specification:**
- Name: `SALES_YYYYMMDD.csv`
- Schedule: Daily at 02:00 UTC
- Volume: ~50,000 records

**Fields:**
| Field | Type | Example |
|-------|------|---------|
| order_id | String | ORD-123456 |
| date | Date | 2026-01-15 |
| amount | Decimal | 1234.56 |
| currency | String(3) | USD |

---

## Common Mistakes

1. **Assuming compatibility** - Not specifying data formats
2. **Ignoring errors** - Only happy path documented
3. **No versioning** - Interface changes break integrations
4. **Missing security** - Authentication not specified
5. **Volume underestimated** - System cannot handle load

---

## Interface Questions Checklist

**For each interface:**
- [ ] Who/what is on each end?
- [ ] What data is exchanged?
- [ ] What is the format?
- [ ] How is it triggered?
- [ ] How often?
- [ ] How much data?
- [ ] What can go wrong?
- [ ] How are errors handled?
- [ ] What security is needed?
- [ ] Who is responsible?

---

## Context Diagram

Show all interfaces visually:

```
                    +------------------+
                    |    Our System    |
                    +------------------+
                           |
      +--------------------+--------------------+
      |                    |                    |
      v                    v                    v
+----------+        +------------+        +---------+
| CRM      |        | Payment    |        | User    |
| System   |        | Gateway    |        |         |
+----------+        +------------+        +---------+
```

---

## Next Steps

After interface analysis:
1. Coordinate with external system owners
2. Define integration testing approach
3. Plan implementation sequence
4. Document SLAs
5. Connect to BA Knowledge Areas Summary methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- BA industry Interface Analysis Guidelines
