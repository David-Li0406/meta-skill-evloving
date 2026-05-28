# Phase 2: Technical Requirements

## Objective

Translate user needs into technical capabilities the system must provide.

## Step 1: Derive Functional Requirements

For each user story, identify technical capabilities:

```markdown
### Technical Requirement: [TR-ID]

**Derived From**: [User Story ID(s)]

**Capability**: The system shall [specific technical capability]

**Technical Details**:
- Input: [What the system receives]
- Processing: [What the system does]
- Output: [What the system produces]

**Validation Criteria**:
- [ ] [Technical criterion 1]
- [ ] [Technical criterion 2]
```

### Functional Requirement Categories

| Category | Examples | Questions to Ask |
|----------|----------|-----------------|
| **Data** | Storage, retrieval, transformation | What data? How much? How fast? |
| **Processing** | Calculations, workflows, orchestration | What logic? What order? What triggers? |
| **Integration** | APIs, events, file formats | What systems? What protocols? What data exchange? |
| **Security** | AuthN, AuthZ, encryption | Who can access? What's protected? Audit trails? |

## Step 2: Define Non-Functional Requirements

Present options for each category:

### Performance Requirements

```markdown
### Decision: Performance Targets

| Metric | Option A (Recommended)** | Option B | Option C |
|--------|-------------------------|----------|----------|
| Response Time | p95 < 200ms | p95 < 500ms | p95 < 1s |
| Throughput | 1000 req/s | 500 req/s | 100 req/s |
| Concurrent Users | 10,000 | 1,000 | 100 |

**User Impact**:
- Option A: Snappy experience, higher infra cost
- Option B: Acceptable experience, moderate cost
- Option C: Noticeable delays, lowest cost

**Recommendation**: [Based on user personas and their expectations]
```

### Reliability Requirements

```markdown
### Decision: Reliability Targets

| Metric | Description | Target |
|--------|-------------|--------|
| **Availability** | Uptime percentage | [99.9% / 99.99% / etc.] |
| **Durability** | Data loss tolerance | [Zero loss / Best effort] |
| **Recovery Time** | Max downtime per incident | [Minutes / Hours] |
| **Recovery Point** | Max data loss per incident | [Seconds / Minutes] |
```

### Scalability Requirements

```markdown
### Decision: Scalability Strategy

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **Horizontal (Recommended)** | Add more instances | Linear scaling, resilient | Complexity, state management |
| **Vertical** | Bigger machines | Simple, no code changes | Ceiling limit, single point |
| **Hybrid** | Both approaches | Flexible | Complex operations |
```

### Security Requirements

```markdown
### Security Requirement: [SR-ID]

| Aspect | Requirement | Rationale |
|--------|-------------|-----------|
| **Authentication** | [Method] | [Why] |
| **Authorization** | [Model: RBAC/ABAC/etc.] | [Why] |
| **Data Protection** | [At rest / In transit] | [Why] |
| **Audit** | [What to log] | [Why] |
| **Compliance** | [Standards: SOC2/HIPAA/etc.] | [Why] |
```

## Step 3: Identify Technical Constraints

```markdown
### Technical Constraint Analysis

| Constraint | Source | Impact | Mitigation |
|------------|--------|--------|------------|
| [Language/Runtime] | [Team expertise / Existing system] | [What it limits] | [How to work with it] |
| [Infrastructure] | [Cloud provider / On-prem] | [What it limits] | [How to work with it] |
| [Dependencies] | [External services / Libraries] | [What it limits] | [How to work with it] |
| [Data] | [Existing schemas / Formats] | [What it limits] | [How to work with it] |
```

## Step 4: Define Dependencies

```markdown
### Dependency Map

| Dependency | Type | Criticality | Fallback Strategy |
|------------|------|-------------|-------------------|
| [Service A] | External API | Critical | [Cache / Queue / Fail] |
| [Database] | Internal | Critical | [Replica / Backup] |
| [Library X] | Code | Medium | [Alternative / Fork] |
```

## Step 5: Critical Reflection

### Feasibility Check
- Can we meet all performance targets with available resources?
- Are non-functional requirements consistent with each other?
- What's the cost of these requirements?

### Risk Assessment
- What are the hardest technical requirements?
- Where are we most likely to fail?
- What's our backup plan?

### Trade-off Analysis
- What are we sacrificing for performance?
- What are we sacrificing for simplicity?
- Are these trade-offs acceptable?

## Phase 2 Approval Gate

```markdown
## Phase 2 Summary: Technical Requirements

### Functional Requirements: [N]
| Category | Count |
|----------|-------|
| Data | [X] |
| Processing | [Y] |
| Integration | [Z] |
| Security | [W] |

### Non-Functional Targets
| Aspect | Target |
|--------|--------|
| Response Time | [Value] |
| Availability | [Value] |
| Scalability | [Strategy] |

### Key Technical Decisions
[List major technical choices made]

### Technical Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Plan] |

### Open Technical Questions
[Any unresolved items]

---

**Do you approve Phase 2? Any changes needed before proceeding to Requirements Integration?**
```
