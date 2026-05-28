# Terraform Best Practices Patterns

**Category**: devops/iac-best-practices/terraform
**Description**: Terraform organizational and operational best practices
**CWE**: CWE-1188

---

## Tagging Patterns

### Missing Required Tags
**Pattern**: `resource\s+"aws_[^"]+"\s+"[^"]+"\s*\{(?:(?!tags\s*=).)*\}`
**Type**: regex
**Severity**: medium
**Languages**: [terraform]
- AWS resources should have tags for organization and cost tracking
- Remediation: Add `tags = { Environment = var.environment, Owner = var.owner }`

### Missing Environment Tag
**Pattern**: `tags\s*=\s*\{(?:(?!Environment).)*\}`
**Type**: regex
**Severity**: low
**Languages**: [terraform]
- All resources should be tagged with Environment
- Remediation: Add `Environment = var.environment` to tags block

---

## Module Best Practices

### Unpinned Git Module Version
**Pattern**: `source\s*=\s*"git::[^"]+(?<!\.git\?ref=[a-f0-9]+)"`
**Type**: regex
**Severity**: medium
**Languages**: [terraform]
- Git-sourced modules should be pinned to a specific ref
- Remediation: Pin to tag or commit: `source = "git::...?ref=v1.0.0"`

### Registry Module Without Version
**Pattern**: `module\s+"[^"]+"\s*\{[^}]*source\s*=\s*"[^/]+/[^/]+/[^"]+"\s*(?!version)`
**Type**: regex
**Severity**: medium
**Languages**: [terraform]
- Registry modules should specify a version constraint
- Remediation: Add `version = "~> 1.0"` to module block

---

## State Management

### Local Backend Not Remote
**Pattern**: `terraform\s*\{[^}]*(?<!backend\s*")[^}]*\}`
**Type**: regex
**Severity**: high
**Languages**: [terraform]
- Production Terraform should use remote state backend
- Remediation: Configure remote backend for state locking and team collaboration
- CWE-1188: Insecure Default Initialization of Resource

---

## Variable Best Practices

### Variable Without Description
**Pattern**: `variable\s+"[^"]+"\s*\{(?:(?!description).)*\}`
**Type**: regex
**Severity**: low
**Languages**: [terraform]
- Variables should have descriptions for documentation
- Remediation: Add `description = "Purpose of this variable"`

### Variable Without Type
**Pattern**: `variable\s+"[^"]+"\s*\{(?:(?!type).)*\}`
**Type**: regex
**Severity**: low
**Languages**: [terraform]
- Variables should have explicit type constraints
- Remediation: Add `type = string` or appropriate type

---

## Output Best Practices

### Output Without Description
**Pattern**: `output\s+"[^"]+"\s*\{(?:(?!description).)*\}`
**Type**: regex
**Severity**: low
**Languages**: [terraform]
- Outputs should have descriptions
- Remediation: Add `description = "What this output provides"`

---

## Naming Conventions

### Non-Lowercase Resource Name
**Pattern**: `resource\s+"[^"]+"\s+"[^"]*[A-Z][^"]*"`
**Type**: regex
**Severity**: low
**Languages**: [terraform]
- Resource names should be lowercase with underscores
- Example: `resource "aws_instance" "MyServer"` (bad)
- Remediation: Use `resource "aws_instance" "my_server"` (good)

---

## References

- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [CWE-1188: Insecure Default Initialization of Resource](https://cwe.mitre.org/data/definitions/1188.html)
