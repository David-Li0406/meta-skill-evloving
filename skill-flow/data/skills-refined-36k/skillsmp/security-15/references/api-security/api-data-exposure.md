# API Data Exposure

**Category**: api-security/data-exposure
**Description**: Detection patterns for excessive data exposure and sensitive data leakage in APIs
**CWE**: CWE-200, CWE-209, CWE-204, CWE-532, CWE-915

---

## OWASP API Security Top 10

- **API3:2023** - Broken Object Property Level Authorization
- **API6:2023** - Unrestricted Access to Sensitive Business Flows

---

## Excessive Data Exposure

### Full Object in Response
**Pattern**: `res\.(json|send)\s*\(\s*(user|account|profile|customer)\s*\)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Returning full user object without filtering
- CWE-200: Information Exposure

### Select All Without Filter
**Pattern**: `(SELECT|select)\s+\*\s+FROM.*(res\.|return|response)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- SELECT * in API response
- CWE-200: Information Exposure

### ORM Find Without Select
**Pattern**: `\.(find|findOne|findAll|findById)\s*\([^)]*\)(?!.*\.(select|lean|attributes))`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Mongoose/Sequelize find without field selection
- CWE-200: Information Exposure

---

## Password in Response

### Password Not Excluded
**Pattern**: `(toJSON|toObject)\s*\([^)]*\)(?!.*password).*res\.(json|send)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Password field not excluded from response
- CWE-200: Information Exposure

### Password Hash in Response
**Pattern**: `(password|password_hash|passwordHash|hashed_password)\s*[=:][^,}]*[,}][^}]*(res\.|return|response)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- Password hash in API response
- CWE-200: Information Exposure

---

## Sensitive Fields Exposure

### PII in Response
**Pattern**: `(ssn|social_security|credit_card|creditCard|cardNumber|card_number|tax_id|taxId)\s*[=:][^}]*(res\.|return|response)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- SSN, credit card, or PII in response
- CWE-200: Information Exposure

### Internal IDs Exposed
**Pattern**: `(_id|internal_id|internalId|system_id|db_id)\s*[=:][^}]*(res\.|return|response)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- Internal database IDs exposed
- CWE-200: Information Exposure

---

## Debug Information Leakage

### Stack Trace in Error
**Pattern**: `(res\.(json|send)|return)\s*\([^)]*\b(stack|stackTrace|trace)\b`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Stack trace in error response
- CWE-209: Error Message Information Leak

### SQL Error Details
**Pattern**: `catch\s*\([^)]*\)\s*\{[^}]*(res\.(json|send)|return)[^}]*\berr(or)?\.(message|stack)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- SQL error details exposed
- CWE-209: Error Message Information Leak

---

## Verbose Error Messages

### Database Error in Response
**Pattern**: `(SequelizeError|MongoError|PrismaClientKnownRequestError|DatabaseError)[^}]*(res\.|return)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Database error details in response
- CWE-209: Error Message Information Leak

---

## API Enumeration

### User Enumeration
**Pattern**: `(user|email|account)\s+(not found|doesn't exist|does not exist|invalid)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, python]
- Different error messages for existing vs non-existing users
- CWE-204: Observable Response Discrepancy

---

## GraphQL Introspection

### Introspection Enabled
**Pattern**: `introspection\s*[=:]\s*true`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- GraphQL introspection enabled in production
- CWE-200: Information Exposure

### Missing Introspection Disable
**Pattern**: `(ApolloServer|GraphQLServer|graphqlHTTP)\s*\(\s*\{(?!.*introspection\s*[=:]\s*false)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- GraphQL server without introspection disabled
- CWE-200: Information Exposure

---

## Sensitive Data in Logs

### Logging Secrets
**Pattern**: `(log|logger|console)\.(info|debug|warn|error)\s*\([^)]*\b(password|token|secret|apiKey|api_key|authorization)\b`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- Logging passwords or tokens
- CWE-532: Insertion of Sensitive Information into Log File

---

## Mass Assignment Exposure

### Direct Body to Model
**Pattern**: `(create|update|save)\s*\(\s*req\.body\s*\)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Direct request body to model
- CWE-915: Mass Assignment

### Spread Operator With Body
**Pattern**: `\{\s*\.\.\.req\.body\s*\}`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Spread operator with request body
- CWE-915: Mass Assignment

---

## Internal Endpoint Exposure

### Unprotected Internal Endpoints
**Pattern**: `(\/internal|\/admin|\/debug|\/metrics|\/health|\/status).*app\.(get|post|use)(?!.*auth)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Internal/admin endpoints without protection
- CWE-200: Information Exposure

### Actuator Endpoints
**Pattern**: `(\/actuator|\/env|\/heapdump|\/threaddump)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python, java]
- Actuator endpoints exposed
- CWE-200: Information Exposure

---

## Response Header Leakage

### Server Version in Headers
**Pattern**: `(X-Powered-By|Server)\s*[=:]\s*['"][^'"]+['"]`
**Type**: regex
**Severity**: low
**Languages**: [javascript, typescript]
- Server version in headers
- CWE-200: Information Exposure

---

## Detection Confidence

**Regex Detection**: 85%
**Security Pattern Detection**: 80%

---

## References

- [OWASP API3:2023 - Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [CWE-200: Exposure of Sensitive Information](https://cwe.mitre.org/data/definitions/200.html)
- [CWE-209: Error Message Information Leak](https://cwe.mitre.org/data/definitions/209.html)
