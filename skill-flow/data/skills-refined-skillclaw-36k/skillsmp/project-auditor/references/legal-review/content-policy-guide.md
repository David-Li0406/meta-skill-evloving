<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Code Content Policy & Legal Risk Detection Guide

Comprehensive guide for detecting inappropriate content, legal risks, and policy violations in source code.

## Table of Contents

- [Profanity & Offensive Content](#profanity--offensive-content)
- [Legal & Regulatory Risks](#legal--regulatory-risks)
- [Intellectual Property Issues](#intellectual-property-issues)
- [Security & Privacy](#security--privacy)
- [Inclusive Language](#inclusive-language)
- [Detection Techniques](#detection-techniques)
- [Remediation Strategies](#remediation-strategies)

## Profanity & Offensive Content

### Categories of Inappropriate Content

1. **Profanity** - Vulgar or obscene language
2. **Hate Speech** - Discriminatory or derogatory content
3. **Sexual Content** - Explicit or inappropriate sexual references
4. **Violent Language** - Threats or violent imagery
5. **Harassment** - Bullying or intimidating content

### Detection Patterns

**Profanity in Code Elements**:
```regex
# Variable/function names
def (fuck|shit|damn|hell).*\(
var (asshole|bastard|bitch).*=
class (crap|piss).*\{

# Comments
#.*(fuck|shit|damn).*
//.*(asshole|bastard).*
/\*(.|\n)*?(profanity)(.|\n)*?\*/
```

**Context-Aware Detection**:
```python
# High confidence - Clear profanity
function_name = "shitty_implementation"  # ⚠️ High
comment = "// This fucking sucks"        # ⚠️ High

# Medium confidence - Possible profanity
variable = "damn_counter"                 # ⚠️ Medium
comment = "// Hell if I know"            # ⚠️ Medium

# Low confidence - Technical terms
daemon = "systemd"                        # ✅ OK (technical term)
class_name = "AssemblerAssembler"        # ✅ OK (contains 'ass' but legitimate)
```

### Common Profanity Patterns

**Identifiers to Flag**:
```
# Functions/variables
fuck, shit, damn, hell, ass, bitch, bastard, crap, piss, cock
wtf, omg, ffs, bs, bs_detector

# Leetspeak variations
fuc

k, sh1t, a$$, b1tch, d4mn

# Partial matches in context
shitty_code, fucking_magic, damn_it, holy_hell
```

**Exemptions**:
```
# Technical terms (whitelist)
daemon, assembly, password, class, assertion, associate
Scunthorpe problem, bass, glass, grass, mass

# Domain-specific
assassin (security), cockpit (aviation), bastard (typography)
```

### Hate Speech & Discriminatory Content

**Protected Categories**:
- Race, ethnicity, national origin
- Religion
- Gender, sexual orientation
- Disability
- Age

**Detection Patterns**:
```regex
# Slurs and derogatory terms
(racial_slur|homophobic_term|sexist_term)

# Discriminatory phrases
(stereotype).*?(group)
(group).*?(negative_characteristic)

# Dog whistles and coded language
# (Requires contextual analysis)
```

**Examples to Flag**:
```python
# Stereotyping
if user.gender == "female":
    intelligence = 0.8  # ⚠️ Sexist assumption

# Derogatory naming
class LazyMexican:  # ⚠️ Racist stereotype
    pass

# Exclusionary language
def master_slave_config():  # ⚠️ Problematic terminology
    pass
```

## Legal & Regulatory Risks

### Export Control & ITAR

**Restricted Technologies**:
- Strong encryption (>= 56-bit symmetric, >= 512-bit asymmetric)
- Military applications
- Satellite technology
- Nuclear technology

**Detection Patterns**:
```python
# Cryptography detection
import (cryptography|pycrypto|openssl)
AES-(128|192|256)
RSA-\d{4,}  # >= 1024 bit
elliptic curve

# Export control keywords
ITAR, EAR, ECCN
military grade, weapons system
munitions, defense article
```

**Compliance Requirements**:
- EAR (Export Administration Regulations)
- ITAR (International Traffic in Arms Regulations)
- BIS (Bureau of Industry and Security) classifications

### Privacy Law Violations

**GDPR Concerns**:
```python
# PII collection without consent
user_data = {
    "name": name,
    "email": email,
    "ip_address": request.remote_addr,  # ⚠️ PII
    "location": geoip(request.ip),      # ⚠️ PII
}
# Missing: consent, purpose, retention policy

# Hardcoded data retention
DELETE FROM users WHERE created_at < NOW() - INTERVAL '10 YEARS'
# ⚠️ May violate "right to be forgotten"
```

**CCPA Concerns**:
```python
# Selling personal data
analytics.track(user_id, {
    "purchase_history": purchases,
    "browsing_history": clicks,
})
# ⚠️ Requires opt-out mechanism
```

**HIPAA Concerns**:
```python
# Protected Health Information (PHI)
patient_record = {
    "ssn": "123-45-6789",           # ⚠️ PHI
    "diagnosis": "Type 2 Diabetes",  # ⚠️ PHI
    "medical_history": [...],        # ⚠️ PHI
}
# Requires: encryption, access controls, audit logs
```

### Trademark Infringement

**Detection Patterns**:
```regex
# Company/product names
(Google|Microsoft|Apple|Amazon|Meta|Twitter|Oracle)

# Trademark symbols
®|™|℠

# Domain squatting
(famous_brand)-(similar_name)
```

**Examples**:
```python
# Potentially infringing
class GoogleSearch:  # ⚠️ Trademark
    pass

class ApplePayment:  # ⚠️ Trademark
    pass

# Acceptable fair use
def search_google(query):  # ✅ Descriptive use
    pass

# Proper attribution
# Uses Google Maps API under license
```

### Patent Claims

**Red Flags**:
```python
# Patent numbers in code
# US Patent 1234567
# Patented algorithm

# Known patent areas
# - Image compression (GIF, JPEG)
# - Cryptographic methods
# - Database techniques
# - UI/UX patterns
```

**Detection**:
- Comments mentioning patents
- Algorithms with known patent claims
- Third-party code without clear license

## Intellectual Property Issues

### Unlicensed Third-Party Code

**Detection**:
```bash
# Code copied from Stack Overflow
# Source: https://stackoverflow.com/questions/...

# Code from GitHub without attribution
# Copied from: github.com/user/repo

# Proprietary code patterns
# Copyright (c) CompanyName Inc. All rights reserved.
# Proprietary and Confidential
```

**Red Flags**:
- No license header
- "All rights reserved" notices
- "Confidential" or "Proprietary" markers
- Commercial product names

### Trade Secret Exposure

**Sensitive Information**:
```python
# Proprietary algorithms
def secret_ranking_algorithm(data):
    # ⚠️ Company's competitive advantage
    # DO NOT SHARE EXTERNALLY
    pass

# Business logic
PRICING_TIERS = {
    "enterprise": {
        "discount": 0.45,  # ⚠️ Internal pricing
        "margin": 0.65,    # ⚠️ Profit margin
    }
}

# Customer lists
VIP_CUSTOMERS = ["Company A", "Company B"]  # ⚠️ Confidential
```

### Reverse-Engineered Code

**Indicators**:
```python
# Decompiled or reverse-engineered
# Decompiled from CompetitorProduct.dll
# Reverse engineered from binary

# Violates EULA/TOS
# Based on analysis of [Proprietary Software]
```

## Security & Privacy

### Hardcoded Credentials

**Detection Patterns**:
```regex
# API keys
(api_key|apikey|api-key)\s*[:=]\s*["'][a-zA-Z0-9]{20,}["']

# Passwords
(password|passwd|pwd)\s*[:=]\s*["'][^"']+["']

# Tokens
(token|auth|secret)\s*[:=]\s*["'][a-zA-Z0-9_\-\.]{20,}["']

# AWS keys
AKIA[0-9A-Z]{16}

# Private keys
-----BEGIN (RSA |DSA )?PRIVATE KEY-----
```

**Examples**:
```python
# ⚠️ Hardcoded secrets
API_KEY = "sk_live_abcdef1234567890"
DB_PASSWORD = "SuperSecret123!"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# ✅ Proper handling
import os
API_KEY = os.environ.get("API_KEY")
DB_PASSWORD = get_secret("database/password")
```

### Personal Identifiable Information (PII)

**PII Categories**:
```python
# Direct identifiers
- SSN, passport number, driver's license
- Full name + DOB
- Biometric data
- Financial account numbers

# Quasi-identifiers
- IP address
- Device ID
- Location data
- Email address (in some contexts)

# Sensitive data
- Health information
- Criminal records
- Financial data
- Sexual orientation
```

**Detection**:
```regex
# SSN (US)
\d{3}-\d{2}-\d{4}

# Credit card
\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}

# Email
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# IP address
\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}

# Phone number
\+?1?\d{3}[-.]?\d{3}[-.]?\d{4}
```

### Backdoors & Malicious Code

**Suspicious Patterns**:
```python
# Hidden functionality
if request.headers.get("X-Magic-Header") == "secret_value":
    exec(request.data)  # ⚠️ Remote code execution backdoor

# Obfuscated code
eval(base64.b64decode("encoded_payload"))  # ⚠️ Suspicious

# Unexpected network access
if os.environ.get("USER") == "admin":
    send_to_external_server(sensitive_data)  # ⚠️ Data exfiltration
```

## Inclusive Language

### Non-Inclusive Technical Terms

**Master/Slave → Leader/Follower, Primary/Replica**:
```python
# Before
master_db = "db1"
slave_db = "db2"
def master_slave_replication():
    pass

# After
primary_db = "db1"
replica_db = "db2"
def primary_replica_replication():
    pass
```

**Whitelist/Blacklist → Allowlist/Denylist**:
```python
# Before
whitelist = ["allowed_ip1", "allowed_ip2"]
blacklist = ["blocked_ip1", "blocked_ip2"]

# After
allowlist = ["allowed_ip1", "allowed_ip2"]
denylist = ["blocked_ip1", "blocked_ip2"]
```

**Grandfathered → Legacy, Exempt**:
```python
# Before
grandfathered_users = get_old_users()

# After
legacy_users = get_old_users()
exempt_users = get_privileged_users()
```

**Sanity Check → Validation, Verification**:
```python
# Before
def sanity_check(data):
    pass

# After
def validate_data(data):
    pass
```

### Gender-Neutral Language

**Avoid Gendered Pronouns**:
```python
# Before
# Get the user's preferences and update his profile
def update_user(user):
    profile = user.get_his_profile()

# After
# Get the user's preferences and update their profile
def update_user(user):
    profile = user.get_profile()
```

### Accessibility Considerations

```python
# Use descriptive names
is_visible = True  # ✅ Clear
can_see = True     # ⚠️ Assumes visual ability

# Avoid ableist language
crazy_optimization  # ⚠️ Ableist
complex_optimization  # ✅ Better

dummy_data  # ⚠️ Can be offensive
sample_data  # ✅ Better

crippled_mode  # ⚠️ Ableist
limited_mode  # ✅ Better
```

## Detection Techniques

### Static Analysis

**Regex-Based Scanning**:
```python
import re

PROFANITY_PATTERNS = [
    r'\b(fuck|shit|damn|ass|bitch)\w*\b',
    r'\b(wtf|omfg|bs)\b',
]

def scan_for_profanity(code):
    violations = []
    for pattern in PROFANITY_PATTERNS:
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for match in matches:
            violations.append({
                "type": "profanity",
                "text": match.group(),
                "position": match.span(),
            })
    return violations
```

**AST-Based Analysis**:
```python
import ast

class InappropriateContentChecker(ast.NodeVisitor):
    def visit_Name(self, node):
        if contains_profanity(node.id):
            self.violations.append(f"Variable name: {node.id}")

    def visit_FunctionDef(self, node):
        if contains_profanity(node.name):
            self.violations.append(f"Function name: {node.name}")
        self.generic_visit(node)
```

### Natural Language Processing

**Context-Aware Detection**:
```python
from transformers import pipeline

classifier = pipeline("text-classification",
                     model="unitary/toxic-bert")

def check_comment_toxicity(comment):
    result = classifier(comment)
    if result[0]['label'] == 'toxic' and result[0]['score'] > 0.7:
        return {
            "toxic": True,
            "confidence": result[0]['score'],
            "comment": comment,
        }
```

### Secret Detection

**Entropy-Based Detection**:
```python
import math

def calculate_entropy(string):
    prob = [float(string.count(c)) / len(string)
            for c in dict.fromkeys(list(string))]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

def is_high_entropy_string(s, threshold=4.5):
    # High entropy suggests random string (potential secret)
    return len(s) > 20 and calculate_entropy(s) > threshold
```

**Pattern-Based Detection**:
```python
import re

SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "GitHub Token": r"gh[pousr]_[A-Za-z0-9]{36}",
    "Slack Token": r"xox[baprs]-[0-9]{10,12}-[0-9]{10,12}-[A-Za-z0-9]{24}",
    "Private Key": r"-----BEGIN (RSA |DSA )?PRIVATE KEY-----",
    "Generic API Key": r"[aA][pP][iI]_?[kK][eE][yY].*['\"][0-9a-zA-Z]{32,}['\"]",
}

def scan_for_secrets(code):
    findings = []
    for secret_type, pattern in SECRET_PATTERNS.items():
        matches = re.finditer(pattern, code)
        for match in matches:
            findings.append({
                "type": secret_type,
                "match": match.group(),
                "line": code[:match.start()].count('\n') + 1,
            })
    return findings
```

### Machine Learning Classification

**Training Classifier**:
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Train on labeled dataset
X_train = vectorizer.fit_transform(code_samples)
y_train = labels  # ['appropriate', 'profanity', 'hateful', etc.]

classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

# Predict
X_test = vectorizer.transform([new_code_sample])
prediction = classifier.predict(X_test)
```

## Remediation Strategies

### Severity Classification

**Critical** - Immediate action required:
- Hardcoded credentials
- PII exposure
- Security vulnerabilities
- Hate speech

**High** - Review required:
- Profanity in public APIs
- Trademark infringement
- License violations
- Export control issues

**Medium** - Should fix:
- Profanity in internal code
- Non-inclusive language
- Unclear licensing

**Low** - Consider fixing:
- Minor language issues
- Style preferences
- Documentation quality

### Automated Remediation

**Safe Replacements**:
```python
REPLACEMENTS = {
    # Profanity
    "shitty": "poor quality",
    "damn": "darn",
    "wtf": "unexpected",

    # Non-inclusive
    "master": "primary",
    "slave": "replica",
    "whitelist": "allowlist",
    "blacklist": "denylist",
    "grandfathered": "legacy",
}

def auto_fix(code):
    for old, new in REPLACEMENTS.items():
        code = re.sub(rf'\b{old}\b', new, code, flags=re.IGNORECASE)
    return code
```

**Secret Masking**:
```python
def mask_secrets(code):
    for pattern_name, pattern in SECRET_PATTERNS.items():
        code = re.sub(pattern, "[REDACTED]", code)
    return code
```

### Manual Review Process

1. **Triage** - Classify violation severity
2. **Context Analysis** - Understand intent
3. **Impact Assessment** - Legal/business risk
4. **Remediation Plan** - Fix or accept risk
5. **Documentation** - Record decision
6. **Prevention** - Update policies/tools

### False Positive Handling

**Whitelisting**:
```python
# .legalignore file
# Technical terms that may trigger false positives
daemon.*
.*password.*  # Legitimate use
assembly.*

# Specific exceptions
src/security/password_manager.py:12  # Line-specific
```

**Context Exemptions**:
```python
# Allow in test files
if file.endswith('_test.py'):
    severity = max(severity - 1, 0)

# Allow in documentation
if file.endswith('.md'):
    check_only_examples = True
```

## Reporting & Documentation

### Violation Report Format

```json
{
  "scan_id": "scan-2024-01-01-001",
  "timestamp": "2024-01-01T00:00:00Z",
  "repository": "org/repo",
  "violations": [
    {
      "id": "violation-001",
      "type": "profanity",
      "severity": "medium",
      "file": "src/utils.py",
      "line": 42,
      "column": 10,
      "matched_text": "shitty_code",
      "context": "def shitty_code_detector():",
      "recommendation": "Rename to 'poor_quality_code_detector'",
      "auto_fixable": true
    }
  ],
  "summary": {
    "total_violations": 15,
    "by_severity": {
      "critical": 0,
      "high": 2,
      "medium": 8,
      "low": 5
    },
    "by_type": {
      "profanity": 10,
      "non_inclusive": 5
    }
  }
}
```

### Compliance Dashboard

**Metrics to Track**:
- Violations per commit
- Time to remediation
- False positive rate
- Policy compliance percentage
- Violation trends over time

## Tool Integration

### Pre-commit Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running legal content scan..."
python scripts/legal_scan.py --staged

if [ $? -ne 0 ]; then
    echo "❌ Legal violations detected. Commit blocked."
    echo "Run 'python scripts/legal_scan.py --fix' to auto-fix"
    exit 1
fi

echo "✅ Legal scan passed"
```

### CI/CD Integration

```yaml
# GitHub Actions
name: Legal Scan
on: [push, pull_request]

jobs:
  legal-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Scan for inappropriate content
        run: |
          python -m pip install legal-scanner
          legal-scanner scan . --report report.json

      - name: Check severity
        run: |
          if grep -q '"severity": "critical"' report.json; then
            echo "❌ Critical violations found"
            exit 1
          fi

      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: legal-scan-report
          path: report.json
```

### IDE Integration

**VSCode Extension Example**:
```json
{
  "settings": {
    "legalScanner.enabled": true,
    "legalScanner.severity": "medium",
    "legalScanner.showInlineWarnings": true,
    "legalScanner.categories": [
      "profanity",
      "secrets",
      "non-inclusive",
      "pii"
    ]
  }
}
```

## Industry Standards (2025)

### Corporate Policies

**Major Tech Companies**:
- **Google**: Inclusive naming, automated secret detection
- **Microsoft**: Responsible AI commitments, bias detection
- **GitHub**: Inclusive language in product and code
- **Red Hat**: Diversity and inclusion in technical terms

### Regulatory Frameworks

- **EU AI Act** - Bias and discrimination in code
- **GDPR** - Privacy by design
- **CCPA** - Data protection
- **SOC 2** - Security controls
- **ISO 27001** - Information security

### Open Source Initiatives

- **Inclusive Naming Initiative** - https://inclusivenaming.org/
- **REUSE Software** - Licensing clarity
- **OpenSSF** - Security best practices
- **TODO Group** - Open source program offices

## Summary

Key takeaways for code content policy:

1. **Automate detection** - Use static analysis, regex, and ML
2. **Context matters** - Not all flagged content is problematic
3. **Educate developers** - Clear policies and training
4. **Continuous monitoring** - Integrate into CI/CD
5. **Balance strictness** - Avoid over-flagging technical terms
6. **Document exceptions** - Whitelist legitimate uses
7. **Regular updates** - Evolve policies with standards
8. **Legal review** - Consult counsel for complex cases

Content policy enforcement protects your organization from legal, reputational, and regulatory risks while fostering an inclusive development environment.
