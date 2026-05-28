# API Mass Assignment

**Category**: api-security/mass-assignment
**Description**: Detection patterns for mass assignment and parameter pollution vulnerabilities
**CWE**: CWE-915, CWE-1321, CWE-235, CWE-20

---

## OWASP API Security Top 10

- **API3:2023** - Broken Object Property Level Authorization
- **API6:2023** - Unrestricted Access to Sensitive Business Flows

---

## Direct Request Body Assignment

### Direct Body to Create/Update
**Pattern**: `\.(create|update|updateOne|findOneAndUpdate|save)\s*\(\s*req\.body\s*\)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Direct body to create/update
- CWE-915: Mass Assignment

### Spread Operator With Body
**Pattern**: `\{\s*\.\.\.req\.body\s*[,}]`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Spread operator with request body
- CWE-915: Mass Assignment

### Object.assign With Body
**Pattern**: `Object\.assign\s*\([^,]+,\s*req\.body`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Object.assign with request body
- CWE-915: Mass Assignment

---

## Python Mass Assignment

### SQLAlchemy Update
**Pattern**: `\.(update|filter)\s*\([^)]*\)\.(update|values)\s*\(\s*\*\*request\.(json|form)`
**Type**: regex
**Severity**: high
**Languages**: [python]
- SQLAlchemy update with request data
- CWE-915: Mass Assignment

### Django Update
**Pattern**: `\.(create|update|update_or_create)\s*\(\s*\*\*request\.(POST|data|json)`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Django update with request data
- CWE-915: Mass Assignment

### Pydantic Without Validation
**Pattern**: `\w+Model\s*\(\s*\*\*request\.(json|data)\s*\)`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Pydantic model from request without validation
- CWE-915: Mass Assignment

---

## Mongoose Mass Assignment

### Mongoose Update Without Restriction
**Pattern**: `(findByIdAndUpdate|findOneAndUpdate|updateOne|updateMany)\s*\([^,]+,\s*req\.body`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Mongoose update without field restriction
- CWE-915: Mass Assignment

### New Model From Body
**Pattern**: `new\s+\w+Model\s*\(\s*req\.body\s*\)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- New model from request body
- CWE-915: Mass Assignment

---

## Sequelize Mass Assignment

### Sequelize Create From Body
**Pattern**: `\w+\.(create|update|bulkCreate)\s*\(\s*req\.body`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Sequelize create/update from body
- CWE-915: Mass Assignment

---

## Prisma Mass Assignment

### Prisma Create From Body
**Pattern**: `prisma\.\w+\.(create|update|upsert)\s*\(\s*\{\s*data\s*:\s*req\.body`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Prisma create/update from body
- CWE-915: Mass Assignment

---

## Ruby on Rails Mass Assignment

### Unpermitted Params
**Pattern**: `\.(create|update|new)\s*\(\s*params(?!\.(permit|require))`
**Type**: regex
**Severity**: high
**Languages**: [ruby]
- Unpermitted params to create/update
- CWE-915: Mass Assignment

---

## Sensitive Field Modification

### Role/Permission Modification
**Pattern**: `(role|isAdmin|is_admin|admin|permission|permissions|privilege)\s*[=:]\s*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- Role/permission fields in request
- CWE-915: Mass Assignment

### Account Status Modification
**Pattern**: `(status|active|verified|approved|enabled)\s*[=:]\s*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- Account status modification via request
- CWE-915: Mass Assignment

---

## HTTP Parameter Pollution

### Array Params Without Validation
**Pattern**: `req\.(query|params)\[['"][^'"]+['"]\]\s*(?!\.filter|\.map|\.every|\.some)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Array parameters without validation
- CWE-235: HTTP Parameter Pollution

---

## GraphQL Mass Assignment

### GraphQL Input to Database
**Pattern**: `(args|input)\s*=>\s*\w+\.(create|update)\s*\(\s*(args|input)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- GraphQL input directly to database
- CWE-915: Mass Assignment

---

## Prototype Pollution

### Object Merge With Input
**Pattern**: `(merge|extend|assign|defaults)\s*\([^,]+,\s*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Object merge with user input
- CWE-1321: Prototype Pollution

### Lodash Merge Vulnerability
**Pattern**: `_\.(merge|defaultsDeep|set)\s*\([^,]+,\s*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Lodash merge vulnerability
- CWE-1321: Prototype Pollution

---

## Field Blacklist (Weak)

### Delete Sensitive Fields
**Pattern**: `delete\s+req\.body\.(password|role|admin|isAdmin)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Blacklist approach (weaker than whitelist)
- CWE-915: Mass Assignment

---

## Missing Input Validation

### Route Without Validation
**Pattern**: `app\.(post|put|patch)\s*\([^)]+,\s*(?!.*validate|validator|schema|joi|yup|zod).*\(req`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Route without validation middleware
- CWE-20: Improper Input Validation

---

## Detection Confidence

**Regex Detection**: 85%
**Security Pattern Detection**: 80%

---

## References

- [OWASP Mass Assignment](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)
- [CWE-915: Improperly Controlled Modification](https://cwe.mitre.org/data/definitions/915.html)
- [CWE-1321: Prototype Pollution](https://cwe.mitre.org/data/definitions/1321.html)
