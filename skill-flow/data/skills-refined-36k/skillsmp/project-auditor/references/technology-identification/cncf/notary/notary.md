# Notary Project

**Category**: cncf
**Description**: Standards-based container signing and verification
**Homepage**: https://notaryproject.dev

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Notary Go packages*

- `github.com/notaryproject/notation-go` - Notation Go library
- `github.com/notaryproject/notation-core-go` - Core library
- `github.com/notaryproject/notary` - Legacy Notary v1

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Notary usage*

- `trustpolicy.json` - Notation trust policy
- `signingkeys.json` - Signing key configuration
- `config.json` - Notation configuration

### Configuration Directories
*Known directories that indicate Notary usage*

- `~/.config/notation/` - Notation config directory
- `/etc/notation/` - System notation config

### Code Patterns

**Pattern**: `notaryproject|notation`
- Notary Project references
- Example: `ghcr.io/notaryproject/notation`

**Pattern**: `notation\s+(sign|verify|list|key|cert|policy|plugin)`
- Notation CLI commands
- Example: `notation sign myregistry.io/myrepo:v1`

**Pattern**: `trustPolicy:|version:|trustPolicies:`
- Trust policy structure
- Example: `"trustPolicies": [`

**Pattern**: `signatureVerification:|trustStores:|trustedIdentities:`
- Trust policy fields
- Example: `"signatureVerification": {"level": "strict"}`

**Pattern**: `io\.cncf\.notary|application/vnd\.cncf\.notary`
- Notary content types
- Example: `application/vnd.cncf.notary.signature`

**Pattern**: `x509/ca|x509/signingAuthority|x509/tsa`
- Trust store types
- Example: `"trustStores": ["ca:acme-rockets"]`

**Pattern**: `--signature-format|--plugin|--key`
- Notation CLI flags
- Example: `notation sign --key my-key myregistry.io/myrepo:v1`

**Pattern**: `NOTATION_|notation\.config`
- Notation environment and config
- Example: `NOTATION_CONFIG`

---

## Environment Variables

- `NOTATION_CONFIG` - Config directory path
- `NOTATION_LIBEXEC` - Plugin directory
- `NOTATION_EXPERIMENTAL` - Enable experimental features

## Detection Notes

- Successor to Notary v1 (TUF-based)
- Notation is the reference implementation
- Signs OCI artifacts
- Trust policies define verification rules
- Plugin architecture for signing

---

## Secrets Detection

### Credentials

#### Signing Key Reference
**Pattern**: `keyPath["':\s]+['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Path to signing key

#### Certificate Path
**Pattern**: `certPath["':\s]+['"]?([^\s'"]+)['"]?`
**Severity**: medium
**Description**: Path to signing certificate

---

## TIER 3: Configuration Extraction

### Registry Scope Extraction

**Pattern**: `registryScopes["':\s]+\[['"]?([^\]'"]+)['"]?\]`
- Registry scope for trust policy
- Extracts: `registry_scope`
- Example: `"registryScopes": ["registry.io/repo"]`

### Signature Format Extraction

**Pattern**: `signatureFormat["':\s]+['"]?(jws|cose)['"]?`
- Signature format
- Extracts: `signature_format`
- Example: `"signatureFormat": "jws"`

### Verification Level Extraction

**Pattern**: `level["':\s]+['"]?(strict|permissive|audit|skip)['"]?`
- Signature verification level
- Extracts: `verification_level`
- Example: `"level": "strict"`
