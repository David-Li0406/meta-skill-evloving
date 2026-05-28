# Cryptography Security Patterns

**Category**: cryptography
**Description**: Detection patterns for cryptographic security issues

This directory contains RAG patterns for identifying cryptographic vulnerabilities in source code.
These patterns are the **source of truth** for the crypto scanners and are converted to Semgrep
rules by `rag-to-semgrep.py`.

---

## Pattern Categories

| Subdirectory | Description | CWE References |
|--------------|-------------|----------------|
| `weak-ciphers/` | Deprecated/broken algorithms (DES, RC4, MD5, SHA1, ECB) | CWE-327, CWE-328 |
| `hardcoded-keys/` | Embedded cryptographic keys and secrets | CWE-321, CWE-798 |
| `insecure-random/` | Non-cryptographic RNG for security purposes | CWE-330, CWE-338 |
| `tls-misconfig/` | Insecure TLS/SSL configurations | CWE-295, CWE-757 |

---

## How It Works

```
patterns.md  ──>  rag-to-semgrep.py  ──>  crypto-security.yaml  ──>  Scanner
```

1. Patterns are defined in markdown format in `patterns.md` files
2. `rag-to-semgrep.py` converts these to Semgrep YAML rules
3. Scanner wrapper scripts invoke Semgrep with the generated rules
4. Results are formatted as JSON output

---

## Pattern File Format

Each `patterns.md` file follows this structure:

```markdown
# Category Name

**Category**: cryptography/subcategory
**Description**: What this detects
**CWE**: CWE-XXX reference

---

## Import Detection

### Language Name
**Pattern**: `regex_pattern`
- Description of what it matches
- Example: `code example`

---

## Secrets Detection

#### Finding Name
**Pattern**: `regex_pattern`
**Severity**: critical|high|medium|low
**Description**: What this finding means
```

---

## Severity Guidelines

| Severity | Use For |
|----------|---------|
| **critical** | Broken crypto (DES, RC4), exposed private keys, disabled cert validation |
| **high** | Deprecated crypto (MD5, SHA1), hardcoded symmetric keys, weak key lengths |
| **medium** | Risky configurations, insecure random in some contexts |
| **low** | Best practice suggestions, minor improvements |

---

## References

- [OWASP Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [CWE-310: Cryptographic Issues](https://cwe.mitre.org/data/definitions/310.html)
- [NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)
