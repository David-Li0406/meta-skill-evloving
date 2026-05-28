# Helm Chart Best Practices Patterns

**Category**: devops/iac-best-practices/helm
**Description**: Helm chart organizational and operational best practices
**CWE**: CWE-1188

---

## Chart.yaml Best Practices

### Missing Chart Description
**Pattern**: `name:\s*[^\n]+\n(?:(?!description:).)*version:`
**Type**: regex
**Severity**: low
**Languages**: [yaml, helm]
- Charts should have a description in Chart.yaml
- Remediation: Add `description: "What this chart deploys"`

### Missing Chart Keywords
**Pattern**: `version:\s*[^\n]+\n(?:(?!keywords:).)*$`
**Type**: regex
**Severity**: low
**Languages**: [yaml, helm]
- Consider adding keywords for discoverability
- Remediation: Add `keywords: [keyword1, keyword2]`

### Missing Maintainers
**Pattern**: `version:\s*[^\n]+\n(?:(?!maintainers:).)*$`
**Type**: regex
**Severity**: low
**Languages**: [yaml, helm]
- Charts should list maintainers for support
- Remediation: Add `maintainers: [{ name: "Name", email: "email" }]`

---

## Values.yaml Best Practices

### Uncommented Values
**Pattern**: `^[a-zA-Z]+:\s*[^\n#]+$`
**Type**: structural
**Severity**: low
**Languages**: [yaml, helm]
- Values should have comments explaining purpose and options
- Remediation: Add comments above each configurable value

### Missing Image Tag Configuration
**Pattern**: `image:\s*\n\s+repository:[^\n]+\n(?:(?!tag:).)*\n`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, helm]
- Image configuration should include separate tag field
- Remediation: Add `tag: "latest"` for versioning flexibility

### Missing Resource Defaults
**Pattern**: `^(?:(?!resources:).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, helm]
- values.yaml should define default resource requests/limits
- Remediation: Add `resources: { requests: {...}, limits: {...} }`

---

## Template Best Practices

### Missing NOTES.txt
**Pattern**: `templates/(?!NOTES\.txt)`
**Type**: structural
**Severity**: low
**Languages**: [helm]
- Charts should include templates/NOTES.txt for post-install guidance
- Remediation: Create NOTES.txt with usage instructions

### Missing Helper Functions
**Pattern**: `templates/(?!_helpers\.tpl)`
**Type**: structural
**Severity**: low
**Languages**: [helm]
- Charts should use _helpers.tpl for reusable template functions
- Remediation: Define common labels and name functions in _helpers.tpl

### Hardcoded Values in Templates
**Pattern**: `replicas:\s*\d+(?!\s*\||\s*\})`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, helm]
- Avoid hardcoded values; use .Values references
- Example: `replicas: 3` (bad)
- Remediation: Use `replicas: {{ .Values.replicaCount }}` (good)

---

## Security Best Practices

### Missing Service Account Configuration
**Pattern**: `^values\.yaml$(?:(?!serviceAccount:).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, helm]
- Charts should allow service account configuration
- Remediation: Add `serviceAccount: { create: true, name: "" }`

### Missing Pod Security Context
**Pattern**: `^values\.yaml$(?:(?!podSecurityContext:).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, helm]
- Charts should define pod security context options
- Remediation: Add `podSecurityContext: { runAsNonRoot: true }`

---

## References

- [Helm Chart Best Practices](https://helm.sh/docs/chart_best_practices/)
- [CWE-1188: Insecure Default Initialization of Resource](https://cwe.mitre.org/data/definitions/1188.html)
