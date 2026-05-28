# HashiCorp Terraform Provider Best Practices

## Core Design Principles

### 1. Single API/Problem Domain Focus
Providers should manage "a single collection of components based on the underlying API or SDK." This approach:
- Simplifies authentication
- Improves practitioner discovery
- Enables system composition
- Allows maintainers to develop deep expertise

### 2. Single API Object per Resource
Resources represent individual components with create, read, delete, and optional update operations. Complex abstractions belong in Terraform Modules rather than provider logic, reducing:
- Maintainer burden
- Blast radius of issues

### 3. Schema Alignment with Underlying API
"Resource and attribute schema should closely match the underlying API, unless it degrades the user experience." This:
- Prevents naming collisions
- Eases code generation
- Allows operators to work across multiple tools seamlessly

**Schema Requirements:**
- Dates/times must use RFC 3339 format
- Boolean attributes: true = action enabled, false = disabled (sometimes requires inverting API logic)
- Recursive types unsupported (use dynamic types as workaround)

### 4. Importability Support
Resources must support `terraform import`, enabling:
- Hybrid manual/automated provisioning
- Brownfield environment adoption

### 5. State and Versioning Continuity
Maintain backward compatibility post-release. Follow Semantic Versioning 2.0.0:
- Major version for breaking changes
- Minor for additions
- Patch for bug fixes

## Naming Conventions

### Resource Names
- Use **singular nouns**
- Must begin with provider name followed by underscore
- Example: `postgresql_database`
- Align with upstream API terminology

### Data Sources
- Follow noun-based conventions like resources
- Can use **plural forms** when returning multiple items
- Example: `aws_availability_zones`

### Function Names
- Use **verb-based names**
- All lowercase with underscores separating words
- **Do not** include provider prefix
- Example: `parse_rfc3339` (called as `provider::time::parse_rfc3339`)

### Attributes
- **Single-value attributes**: Use singular nouns (e.g., `ami`, `instance_type`)
- **Boolean attributes**: Nouns describing what's enabled
- **Collection attributes**: Use **plural nouns** (e.g., `vpc_security_group_ids`, `tags`)
- **Sub-blocks**: Singular nouns, even if multiple instances permitted
- **Write-only arguments**: Append `_wo` suffix (e.g., `password_wo` vs. `password`)
- **Style**: All lowercase with underscores

## Versioning Strategy

Follow **Semantic Versioning**: `MAJOR.MINOR.PATCH`

### MAJOR Version (Breaking Changes)
Increment for:
- Removing resources, data sources, or attributes
- Renaming resources, data sources, or attributes
- Changing authentication or configuration precedence
- Modifying resource/import ID formats
- Altering attribute types incompatibly (e.g., TypeSet to TypeList)
- Changing attribute defaults incompatible with existing state

**Recommendation**: Release major versions no more than once per year

### MINOR Version (New Features)
Increment for:
- Marking resources or attributes as deprecated
- Adding new resources or data sources
- Implementing new attributes or validation
- Compatible type changes (e.g., TypeInt to TypeFloat)

### PATCH Version (Bug Fixes)
- Bug fixes only
- Functionally equivalent to previous release

## Changelog Requirements

**File**: `CHANGELOG` or `CHANGELOG.md` at project root

**Structure**:
```
## X.Y.Z (Unreleased)

[CATEGORY]:

* subsystem: Description [GH-1234]
```

**Categories** (in order):
- BREAKING CHANGES
- NOTES
- FEATURES
- IMPROVEMENTS/ENHANCEMENTS
- BUG FIXES

**Entry Format**: List cross-cutting provider changes first, then order entries lexicographically by subsystem

## Sensitive Data Handling

### Recommended Approaches

**1. Ephemeral Resources (Preferred)**
- Available only in Terraform Plugin Framework
- Guarantees data will not be persisted in plan or state
- Use for sensitive API objects like tokens or secrets

**2. Sensitive Flag**
- Enable on schema fields containing sensitive information
- Prevents values from appearing in CLI output
- Does **not** encrypt values within state files
- Available in both Plugin Framework and SDKv2

### Deprecated: PGP Key-Based Encryption
HashiCorp discourages PGP encryption of state values:
- Values encrypted with PGP keys cannot be reliably interpolated
- Poor user experience when keys are missing
- Incompatible with modern Terraform protocol requirements

**Modern Solution**: Use state backends with native encryption at rest (e.g., HCP Terraform)

## Function Design Patterns

### Single Computational Operation
Each function performs one purpose—avoid conditional logic with "option" arguments

### Pure and Offline Execution
Functions must:
- Produce identical results for identical inputs
- Avoid environment, time, or network dependencies
- Use data sources for operations requiring provider configuration or API access

## Supported Programming Language

**Go is the only language currently supported by HashiCorp** for building Terraform providers.

### HashiCorp Libraries

**1. Terraform Plugin Framework (Recommended)**
- Most recent SDK
- Current recommendation for new provider development
- Represents the current direction

**2. Terraform Plugin SDK (SDKv2)**
- Earlier SDK still used by many existing providers
- Maintained for Terraform 1.x and earlier
- Feature development has largely ceased

**3. Terraform Plugin Go**
- Low-level gRPC bindings
- For advanced use cases requiring minimal abstraction

## Interacting with Providers

### ❌ Unsupported: Direct Go Module Imports
Importing providers as Go modules is explicitly unsupported. Provider versioning communicates Terraform configuration interface compatibility, not Go API interface compatibility.

### ✅ Supported: Schema Export
For projects needing only schema information:
```bash
terraform providers schema -json
```

### ✅ Supported: gRPC Protocol
For projects requiring actual provider functionality:
- Use the gRPC protocol that powers Terraform CLI
- Versioning based on protocol version (not provider version)
- Changes infrequently, ensuring stability
- Officially supported compatibility guarantees
