# CloudFormation Best Practices Patterns

**Category**: devops/iac-best-practices/cloudformation
**Description**: AWS CloudFormation template organizational and operational best practices
**CWE**: CWE-1188

---

## Template Metadata

### Missing Description
**Pattern**: `AWSTemplateFormatVersion[^\n]+\n(?:(?!Description:).)*Resources:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, cloudformation]
- Templates should have a Description for documentation
- Remediation: Add `Description: "Purpose of this template"`

### Outdated Template Version
**Pattern**: `AWSTemplateFormatVersion:\s*["']?2010-09-09["']?`
**Type**: regex
**Severity**: informational
**Languages**: [yaml, cloudformation]
- Consider using latest CloudFormation features
- Note: 2010-09-09 is still the only valid version

---

## Parameter Best Practices

### Parameter Without Description
**Pattern**: `Parameters:\s*\n\s+\w+:\s*\n\s+Type:[^\n]+\n(?:(?!Description:).)*\n\s+\w+:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, cloudformation]
- Parameters should have descriptions
- Remediation: Add `Description: "What this parameter controls"`

### Parameter Without Default
**Pattern**: `Parameters:\s*\n\s+\w+:\s*\n\s+Type:[^\n]+\n(?:(?!Default:).)*\n\s+\w+:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, cloudformation]
- Consider providing sensible defaults for optional parameters
- Remediation: Add `Default: <value>` where appropriate

### Parameter Without Constraints
**Pattern**: `Type:\s*String\s*\n(?:(?!AllowedPattern:|AllowedValues:).)*\n\s+\w+:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, cloudformation]
- String parameters should have validation constraints
- Remediation: Add `AllowedPattern` or `AllowedValues`

---

## Tagging Best Practices

### Resource Without Tags
**Pattern**: `Type:\s*AWS::[^\n]+\n\s+Properties:\s*\n(?:(?!Tags:).)*\n\s+\w+:`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, cloudformation]
- AWS resources should be tagged for organization
- Remediation: Add `Tags:` with Environment, Owner, CostCenter

---

## Output Best Practices

### Missing Outputs Section
**Pattern**: `Resources:\s*\n(?:(?!Outputs:).)*$`
**Type**: regex
**Severity**: low
**Languages**: [yaml, cloudformation]
- Templates should export useful values via Outputs
- Remediation: Add `Outputs:` section with key resource references

### Output Without Description
**Pattern**: `Outputs:\s*\n\s+\w+:\s*\n\s+Value:[^\n]+\n(?:(?!Description:).)*\n\s+\w+:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, cloudformation]
- Outputs should have descriptions
- Remediation: Add `Description: "What this output provides"`

### Output Without Export
**Pattern**: `Outputs:\s*\n\s+\w+:\s*\n\s+Value:[^\n]+\n(?:(?!Export:).)*\n\s+\w+:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, cloudformation]
- Consider exporting outputs for cross-stack references
- Remediation: Add `Export: { Name: !Sub "${AWS::StackName}-<name>" }`

---

## Naming Conventions

### Hardcoded Resource Names
**Pattern**: `(?:BucketName|TableName|FunctionName):\s*["'][^$!][^"']+["']`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, cloudformation]
- Avoid hardcoded names; use dynamic naming with stack name
- Example: `BucketName: "my-bucket"` (bad)
- Remediation: Use `!Sub "${AWS::StackName}-bucket"` (good)

---

## References

- [AWS CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
- [CWE-1188: Insecure Default Initialization of Resource](https://cwe.mitre.org/data/definitions/1188.html)
