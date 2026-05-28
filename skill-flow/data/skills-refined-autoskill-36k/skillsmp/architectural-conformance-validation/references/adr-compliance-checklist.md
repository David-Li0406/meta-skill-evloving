# ADR Compliance Checklist

Guidance for validating implementation against specific types of Architectural Decision Records (ADRs).

---

## How to Use This Checklist

For each ADR referenced in the architecture:

1. **Read the ADR** to understand the decision, context, and consequences
2. **Identify the ADR type** (Technology, Security, Algorithm, Integration, etc.)
3. **Apply the relevant checklist** from below to validate conformance
4. **Document violations** with ADR reference, severity, and remediation

---

## Technology Stack ADRs

**Example**: ADR-001: Use FastAPI for API Framework

### Validation Points
- [ ] Framework/library import matches ADR decision
- [ ] No alternative framework imports (e.g., Flask when FastAPI required)
- [ ] Version constraint matches ADR requirements
- [ ] Dependency declarations in requirements.txt/package.json
- [ ] Configuration follows framework conventions

### Common Violations
```python
# ❌ CRITICAL: Violates ADR-001 (FastAPI required)
from flask import Flask, jsonify
app = Flask(__name__)

# ✅ CORRECT: Uses approved framework
from fastapi import FastAPI
app = FastAPI()
```

### Severity Guidelines
- **CRITICAL**: Using unapproved framework/library
- **WARNING**: Using deprecated version
- **INFO**: Could use newer approved version

---

## Security/Authentication ADRs

**Example**: ADR-005: Use JWT for Authentication

### Validation Points
- [ ] Authentication mechanism matches ADR
- [ ] Token format/structure matches specification
- [ ] Encryption algorithm matches ADR requirement
- [ ] No plaintext storage of sensitive data
- [ ] Session management follows ADR pattern

### Common Violations
```typescript
// ❌ CRITICAL: Violates ADR-005 (JWT required)
const sessionToken = btoa(`${username}:${password}`);
localStorage.setItem('auth', sessionToken);

// ✅ CORRECT: Uses JWT as specified
const token = jwt.sign({ userId: user.id }, secret, { expiresIn: '1h' });
res.cookie('auth', token, { httpOnly: true, secure: true });
```

### Severity Guidelines
- **CRITICAL**: Security vulnerability introduced by non-conformance
- **WARNING**: Insecure configuration of approved mechanism
- **INFO**: Could follow best practice more closely

---

## Design Pattern ADRs

**Example**: ADR-018: Use Singleton Pattern for ConfigManager

### Validation Points
- [ ] Pattern implementation matches canonical form
- [ ] Constructor visibility correct (private for Singleton)
- [ ] Static accessor method exists (getInstance)
- [ ] Thread-safety considerations addressed
- [ ] Pattern justification documented if variation used

### Common Violations
```typescript
// ❌ CRITICAL: Violates ADR-018 (Singleton required)
export class ConfigManager {
  constructor() {
    // Public constructor allows multiple instances
  }
}

// ✅ CORRECT: Singleton pattern
export class ConfigManager {
  private static instance?: ConfigManager;

  private constructor() {
    // Private constructor prevents direct instantiation
  }

  public static getInstance(): ConfigManager {
    if (!ConfigManager.instance) {
      ConfigManager.instance = new ConfigManager();
    }
    return ConfigManager.instance;
  }
}
```

### Severity Guidelines
- **CRITICAL**: Pattern completely absent when required
- **WARNING**: Pattern variation without justification
- **INFO**: Could use more idiomatic implementation

---

## Algorithm/Approach ADRs

**Example**: ADR-010: Use Luhn Algorithm for Credit Card Validation

### Validation Points
- [ ] Algorithm implementation matches documented approach
- [ ] No alternative algorithm used
- [ ] Edge cases handled as specified in ADR
- [ ] Performance characteristics match expectations
- [ ] Algorithm correctly cited/attributed

### Common Violations
```python
# ❌ CRITICAL: Violates ADR-010 (Luhn required)
def validate_card(card_number):
    return len(card_number) == 16  # Naive validation

# ✅ CORRECT: Luhn algorithm
def validate_card(card_number):
    def luhn_checksum(card):
        def digits(n):
            return [int(d) for d in str(n)]
        digits_list = digits(card)
        odd_digits = digits_list[-1::-2]
        even_digits = digits_list[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits(d*2))
        return checksum % 10
    return luhn_checksum(card_number) == 0
```

### Severity Guidelines
- **CRITICAL**: Wrong algorithm used
- **WARNING**: Algorithm implementation has bugs
- **INFO**: Could optimize algorithm implementation

---

## Integration Pattern ADRs

**Example**: ADR-020: Use REST for External API Integration

### Validation Points
- [ ] Integration protocol matches ADR (REST/GraphQL/gRPC)
- [ ] API contract structure follows ADR specification
- [ ] Error handling follows integration pattern
- [ ] Retry logic matches ADR requirements
- [ ] Timeout configuration follows ADR

### Common Violations
```typescript
// ❌ CRITICAL: Violates ADR-020 (REST required)
const client = new GraphQLClient('https://api.example.com/graphql');
const data = await client.request(query);

// ✅ CORRECT: REST integration
const response = await fetch('https://api.example.com/users', {
  method: 'GET',
  headers: { 'Content-Type': 'application/json' }
});
const data = await response.json();
```

### Severity Guidelines
- **CRITICAL**: Wrong integration protocol
- **WARNING**: Missing error handling pattern
- **INFO**: Could add retry logic for resilience

---

## Data Storage/Persistence ADRs

**Example**: ADR-012: Use PostgreSQL for Relational Data

### Validation Points
- [ ] Database technology matches ADR
- [ ] Schema design follows ADR guidelines
- [ ] ORM usage matches ADR specification
- [ ] No direct SQL if ADR requires ORM
- [ ] Connection pooling follows ADR

### Common Violations
```python
# ❌ CRITICAL: Violates ADR-012 (PostgreSQL required)
import sqlite3
conn = sqlite3.connect('app.db')

# ✅ CORRECT: PostgreSQL with ORM
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@localhost/db')
```

### Severity Guidelines
- **CRITICAL**: Wrong database technology
- **WARNING**: Bypassing ORM when required
- **INFO**: Could optimize query patterns

---

## API Contract ADRs

**Example**: ADR-015: Use OpenAPI 3.0 for API Specification

### Validation Points
- [ ] API specification format matches ADR
- [ ] All endpoints documented
- [ ] Request/response schemas match specification
- [ ] Error codes follow ADR standard
- [ ] Versioning strategy follows ADR

### Common Violations
```yaml
# ❌ WARNING: Violates ADR-015 (OpenAPI 3.0 required)
swagger: "2.0"
info:
  title: "My API"

# ✅ CORRECT: OpenAPI 3.0
openapi: "3.0.0"
info:
  title: "My API"
  version: "1.0.0"
```

### Severity Guidelines
- **CRITICAL**: No API specification when required
- **WARNING**: Using deprecated specification format
- **INFO**: Could add more detailed documentation

---

## Error Handling ADRs

**Example**: ADR-008: Use Structured Error Response Format

### Validation Points
- [ ] Error response format matches ADR structure
- [ ] Error codes from approved list
- [ ] Stack traces not exposed in production
- [ ] Logging follows error handling ADR
- [ ] User-facing messages follow guidelines

### Common Violations
```typescript
// ❌ WARNING: Violates ADR-008 (structured format required)
throw new Error("Something went wrong");

// ✅ CORRECT: Structured error
throw new ApplicationError({
  code: "USER_NOT_FOUND",
  message: "User with ID 123 not found",
  statusCode: 404,
  details: { userId: "123" }
});
```

### Severity Guidelines
- **CRITICAL**: Security information leaked in errors
- **WARNING**: Inconsistent error format
- **INFO**: Could add more context to errors

---

## Performance/Scalability ADRs

**Example**: ADR-025: Cache Frequently Accessed Data with Redis

### Validation Points
- [ ] Caching mechanism matches ADR
- [ ] Cache invalidation strategy follows ADR
- [ ] TTL configuration matches requirements
- [ ] No caching of sensitive data if prohibited
- [ ] Cache-aside pattern used if required

### Common Violations
```python
# ❌ WARNING: Violates ADR-025 (Redis required)
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user(user_id):
    return db.query(User).filter_by(id=user_id).first()

# ✅ CORRECT: Redis caching
import redis
cache = redis.Redis(host='localhost', port=6379)

def get_user(user_id):
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    user = db.query(User).filter_by(id=user_id).first()
    cache.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

### Severity Guidelines
- **CRITICAL**: No caching when required for scalability
- **WARNING**: Wrong caching mechanism
- **INFO**: Could optimize cache hit rate

---

## Compliance ADRs (HIPAA, PCI DSS, GDPR)

**Example**: ADR-030: Encrypt PHI at Rest (HIPAA)

### Validation Points
- [ ] Encryption mechanism matches ADR
- [ ] Encryption algorithm approved (AES-256)
- [ ] Key management follows ADR
- [ ] Audit logging for PHI access
- [ ] No PHI in logs or error messages

### Common Violations
```python
# ❌ CRITICAL: Violates ADR-030 (encryption required)
def save_patient_data(patient):
    with open(f'patients/{patient.id}.json', 'w') as f:
        json.dump(patient.to_dict(), f)

# ✅ CORRECT: Encrypted storage
from cryptography.fernet import Fernet

def save_patient_data(patient):
    key = load_encryption_key()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(json.dumps(patient.to_dict()).encode())
    with open(f'patients/{patient.id}.enc', 'wb') as f:
        f.write(encrypted)
    audit_log.info(f"PHI accessed: patient_id={patient.id}")
```

### Severity Guidelines
- **CRITICAL**: Compliance violation (legal/regulatory risk)
- **WARNING**: Incomplete compliance implementation
- **INFO**: Could enhance compliance posture

---

## Logging/Observability ADRs

**Example**: ADR-022: Use Structured Logging with JSON Format

### Validation Points
- [ ] Logging library matches ADR
- [ ] Log format matches specification (JSON)
- [ ] Log levels used correctly
- [ ] No sensitive data in logs
- [ ] Correlation IDs included

### Common Violations
```python
# ❌ WARNING: Violates ADR-022 (structured JSON required)
print(f"User {user_id} logged in at {timestamp}")

# ✅ CORRECT: Structured JSON logging
logger.info("user_login", extra={
    "user_id": user_id,
    "timestamp": timestamp,
    "correlation_id": request_id,
    "event": "authentication.login.success"
})
```

### Severity Guidelines
- **CRITICAL**: Sensitive data logged (PII, secrets)
- **WARNING**: Unstructured logs when structured required
- **INFO**: Could add more context to logs

---

## Testing Strategy ADRs

**Example**: ADR-018: Maintain 80% Code Coverage

### Validation Points
- [ ] Coverage threshold meets ADR requirement
- [ ] Test types match ADR (unit/integration/e2e)
- [ ] Testing framework matches ADR
- [ ] Critical paths tested
- [ ] Edge cases covered

### Common Violations
```python
# ❌ WARNING: Violates ADR-018 (coverage too low)
# Only 1 test for module with 10 functions

def test_happy_path():
    assert add(1, 2) == 3

# ✅ CORRECT: Comprehensive coverage
def test_add_positive_numbers():
    assert add(1, 2) == 3

def test_add_negative_numbers():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 5) == 5

def test_add_floats():
    assert add(1.5, 2.3) == 3.8
```

### Severity Guidelines
- **CRITICAL**: No tests for critical functionality
- **WARNING**: Coverage below ADR threshold
- **INFO**: Could add more edge case tests

---

## Validation Process

For each ADR:

1. **Identify ADR Type** from categories above
2. **Read ADR** to understand decision details
3. **Apply Checklist** for that ADR type
4. **Search Code** for conformance to decision
5. **Document Violations** with severity
6. **Propose Remediation** with code examples

---

## ADR Compliance Scoring

**Per-ADR Score Calculation:**
- Start at 100 points per ADR
- Deduct 20 points per CRITICAL violation
- Deduct 5 points per WARNING violation
- Deduct 1 point per INFO item
- Minimum score: 0

**Overall ADR Compliance:**
- Average score across all checked ADRs
- Weight more heavily ADRs marked as "Critical" in ADR index

---

**Last Updated**: 2025-01-21
