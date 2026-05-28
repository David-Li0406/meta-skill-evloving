# False Positive Handling

## Common False Positive Patterns

### Placeholder Values

These patterns indicate intentionally fake/example values:

```regex
# Explicit placeholders
YOUR_.*_HERE
REPLACE_.*_WITH
<.*_KEY>
\[.*_TOKEN\]
xxx+
placeholder
dummy
fake
example
sample
test123
changeme
todo
fixme

# AWS example key (from documentation)
AKIAIOSFODNN7EXAMPLE
wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# Generic placeholders
^[xX]+$
^0+$
^1234
password123
secret123
```

### Documentation Strings

Context clues that indicate documentation:

```regex
# Markdown code blocks
```.*```

# Comment indicators
^#.*example
^//.*demo
/\*.*sample.*\*/

# Documentation files
README\.md
CONTRIBUTING\.md
docs/.*\.md
\.rst$
```

### Test Fixtures

Files and patterns indicating test data:

```regex
# Test file paths
test/
tests/
__tests__/
spec/
fixtures/
mocks/
__mocks__/

# Test file names
\.test\.(js|ts|py)$
\.spec\.(js|ts|py)$
_test\.(go|py)$
Test\.java$

# Test patterns in content
mock_api_key
test_secret
fake_token
stub_credential
```

### Environment Templates

Template files that are meant to be committed:

```regex
# Template file names
\.env\.example$
\.env\.template$
\.env\.sample$
\.env\.dist$
env\.example$
sample\.env$
config\.example\.(json|yaml|yml)$
```

### Package Lock Files

These often contain hashes that match secret patterns:

```regex
package-lock\.json$
yarn\.lock$
pnpm-lock\.yaml$
Pipfile\.lock$
poetry\.lock$
Gemfile\.lock$
composer\.lock$
Cargo\.lock$
```

### Generated/Compiled Files

```regex
# Build outputs
dist/
build/
out/
\.next/
__pycache__/

# Minified files
\.min\.js$
\.min\.css$

# Source maps
\.map$

# Compiled
\.pyc$
\.class$
\.o$
```

---

## Context-Based False Positives

### URL-Safe Base64 in Non-Secret Contexts

```python
# False positive: Base64 UUID
"id": "dGVzdC1pZC0xMjM0NTY3OA=="  # Not a secret

# True positive: Same format in auth context
"token": "dGVzdC1pZC0xMjM0NTY3OA=="  # Investigate
```

### Hash Values (Not Secrets)

```regex
# Git commit hashes
[a-f0-9]{40}  # In git log context

# Content hashes
sha256-[A-Za-z0-9+/=]{43}=  # SRI hashes
integrity="sha384-..."

# Checksum files
\.sha256$
\.md5$
CHECKSUMS
```

### Public Keys (Not Secrets)

```
-----BEGIN PUBLIC KEY-----
-----BEGIN RSA PUBLIC KEY-----
-----BEGIN CERTIFICATE-----
ssh-rsa AAAA...
ssh-ed25519 AAAA...
```

### UUIDs

```regex
[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}
```

UUIDs are identifiers, not secrets (usually).

---

## Service-Specific False Positives

### AWS

```
# Example key from AWS documentation
AKIAIOSFODNN7EXAMPLE

# ARNs (not secrets, but may be sensitive)
arn:aws:.*

# Region identifiers
us-east-1
eu-west-2
```

### Stripe

```
# Test mode keys (low severity, not false positive)
sk_test_
pk_test_

# Publishable keys (meant to be public)
pk_live_
pk_test_
```

### GitHub

```
# Fine-grained PAT prefix without full token
github_pat_  # Just the prefix

# Action tokens (expected in workflows)
${{ github.token }}
${{ secrets.GITHUB_TOKEN }}
```

---

## Baseline Management

### Creating a Baseline

```bash
# Generate baseline of known false positives
detect-secrets scan --baseline .secrets.baseline

# Review and audit baseline
detect-secrets audit .secrets.baseline
```

### Baseline File Format

```json
{
  "version": "1.4.0",
  "results": {
    "config/example.json": [
      {
        "type": "Secret Keyword",
        "line_number": 5,
        "is_secret": false
      }
    ]
  }
}
```

### Inline Annotations

```python
api_key = "sk_test_fake123"  # pragma: allowlist secret

# Or with detect-secrets
password = "test"  # noqa: E501 detect-secrets
```

---

## Reducing False Positives

### Pattern Refinement

Instead of:
```regex
[A-Za-z0-9]{32}  # Too broad
```

Use:
```regex
sk_live_[A-Za-z0-9]{24}  # Specific to service
```

### Context Requirements

Require contextual keywords near matches:

```regex
# Only match if near "password" or "secret"
(?i)(password|secret|key|token|credential).{0,30}['\"][A-Za-z0-9]{16,}['\"]
```

### File Type Filtering

Limit scanning to relevant files:

```bash
# TruffleHog exclude paths
trufflehog git file://. --exclude-paths=.*_test\.go --exclude-paths=.*\.md

# detect-secrets exclude pattern
detect-secrets scan --exclude-files '.*_test\.go|.*\.md|package-lock\.json'
```

### Entropy Thresholds

Require minimum randomness:

```python
# Low entropy (likely placeholder)
"password": "password123"  # Entropy: ~2.5

# High entropy (likely real secret)
"password": "Kj8#mP2$nQ5@wX9"  # Entropy: ~4.0
```

---

## Handling Confirmed False Positives

### Option 1: Add to Baseline

```bash
# Update baseline
detect-secrets scan --update .secrets.baseline
detect-secrets audit .secrets.baseline  # Mark as false positive
```

### Option 2: Use Allowlist

```bash
# detect-secrets: mark as false positive in baseline
detect-secrets audit .secrets.baseline
# Select finding and mark as "fp" (false positive)
```

### Option 3: Inline Suppression

```python
# For specific tools
API_KEY = "test_key"  # pragma: allowlist secret
API_KEY = "test_key"  # nosec
```

### Option 4: Exclude File

Add files to detection tool configuration or use command-line exclusions.

---

## Triage Workflow

```
1. New finding detected
   │
   ├─> Is file in test/docs/example path?
   │   └─> Yes → Likely false positive, verify and add to baseline
   │
   ├─> Does value contain placeholder keywords?
   │   └─> Yes → False positive, add pattern to allowlist
   │
   ├─> Is this a known example/documentation value?
   │   └─> Yes → False positive, add specific value to allowlist
   │
   ├─> Is entropy low (< 3.0)?
   │   └─> Yes → Likely false positive, verify context
   │
   └─> None of the above
       └─> Treat as true positive, investigate
```
