# in-toto

**Category**: cncf
**Description**: Framework for software supply chain integrity
**Homepage**: https://in-toto.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### PYPI
*in-toto Python packages*

- `in-toto` - in-toto Python implementation
- `securesystemslib` - Security library dependency

#### GO
*in-toto Go packages*

- `github.com/in-toto/in-toto-golang` - Go implementation
- `github.com/in-toto/attestation` - Attestation library

#### NPM
*in-toto Node.js packages*

- `in-toto-js` - JavaScript implementation

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate in-toto usage*

- `*.link` - in-toto link metadata
- `*.layout` - in-toto layout
- `root.layout` - Root layout file

### Code Patterns

**Pattern**: `in-toto|in_toto`
- in-toto references
- Example: `import in_toto`

**Pattern**: `_type["':\s]+['"]?link['"]?|_type["':\s]+['"]?layout['"]?`
- in-toto document types
- Example: `"_type": "link"`

**Pattern**: `signed:|signatures:|payload:|payloadType:`
- in-toto envelope structure
- Example: `"signatures": [`

**Pattern**: `steps:|inspect:|expected_materials:|expected_products:`
- Layout sections
- Example: `"steps": [`

**Pattern**: `in-toto-run|in-toto-record|in-toto-verify`
- in-toto CLI commands
- Example: `in-toto-run --step-name build`

**Pattern**: `keyid:|sig:|method:|key_type:`
- Signature fields
- Example: `"keyid": "2f89b927"`

**Pattern**: `byproducts:|command:|materials:|products:`
- Link metadata fields
- Example: `"materials": {`

**Pattern**: `MATCH\s+|DELETE\s+|ALLOW\s+|DISALLOW\s+|REQUIRE\s+`
- Artifact rules
- Example: `["MATCH", "foo", "WITH", "PRODUCTS"]`

---

## Environment Variables

- `IN_TOTO_ARTIFACT_BASE_PATH` - Base path for artifacts
- `IN_TOTO_SIGNING_KEY` - Signing key path

## Detection Notes

- Protects software supply chain
- Layouts define pipeline policy
- Links record step execution
- Supports multiple key types
- Integrates with TUF

---

## Secrets Detection

### Credentials

#### Signing Key
**Pattern**: `in.toto.*key|IN_TOTO.*KEY`
**Severity**: critical
**Description**: in-toto signing key reference

#### Private Key
**Pattern**: `keyval.*private`
**Severity**: critical
**Description**: Private key in key file

---

## TIER 3: Configuration Extraction

### Step Name Extraction

**Pattern**: `name["':\s]+['"]?([a-zA-Z0-9_-]+)['"]?`
- Pipeline step name
- Extracts: `step_name`
- Example: `"name": "build"`

### Key ID Extraction

**Pattern**: `keyid["':\s]+['"]?([a-f0-9]+)['"]?`
- Key identifier
- Extracts: `key_id`
- Example: `"keyid": "2f89b927..."`

### Threshold Extraction

**Pattern**: `threshold["':\s]+([0-9]+)`
- Signature threshold
- Extracts: `threshold`
- Example: `"threshold": 1`
