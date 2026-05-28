---
name: "hallucinated-packages-anti-pattern"
description: "Security anti-pattern for hallucinated (non-existent) packages (CWE-1357). Use when generating or reviewing AI-assisted code that imports packages, dependencies, or libraries. CRITICAL AI-specific vulnerability with 5-21% hallucination rate. Detects dependency confusion and slopsquatting risks."
---

# Hallucinated Packages Anti-Pattern

**Severity:** Critical

## Summary

AI models hallucinate non-existent software packages at rates of 5-21%. Attackers exploit this through slopsquatting: registering hallucinated package names with malicious code. Developers installing AI-suggested packages without verification execute attacker code, leading to malware execution, credential theft, and system compromise. This AI-specific supply chain attack exploits the trust gap between AI suggestions and package verification.

## The Anti-Pattern

Never install AI-suggested packages without verifying existence, legitimacy, and reputation in official registries.

### BAD Code Example

```python
# An AI model generates the following code snippet and instruction:
# "To handle advanced image processing, you should use the `numpy-magic` library.
# First, install it using pip:"
#
# $ pip install numpy-magic

import numpy_magic as npmagic

def process_image(image_path):
    # The developer assumes `numpy-magic` is a real, safe library.
    # However, it doesn't exist, and an attacker has registered it on PyPI.
    # The moment it was installed, the attacker's code ran.
    # The import itself could also trigger malicious code.
    processed = npmagic.enhance(image_path)
    return processed

```

In this scenario, the developer follows the AI's instructions without question. The `numpy-magic` package is not a real library. An attacker, anticipating this hallucination, has published a malicious package with that exact name. The developer's `pip install` command downloads and executes the attacker's code, compromising their machine and potentially the entire project.

### GOOD Code Example

```python
# SECURE: Verify the package before installing.

# Before installing `numpy-magic`, the developer performs a few checks.

# 1. Search for the package on the official repository (e.g., PyPI, npm).
#    A search for "numpy-magic" on PyPI yields no results or shows a package
#    with very low downloads and a recent creation date. This is a major red flag.

# 2. Look for signs of legitimacy.
#    - Does the package have a link to a GitHub repository?
#    - Is the repository active?
#    - How many weekly downloads does it have? (Is it in the single digits or thousands?)
#    - Who are the maintainers?
#    - Are there any open issues or security advisories?

# 3. Search for the *functionality* instead of the package name.
#    A search for "advanced numpy image processing" leads to well-known libraries
#    like `scikit-image`, `OpenCV (cv2)`, or `Pillow (PIL)`, which are reputable.

# The developer chooses a legitimate, well-known library instead.
from skimage import io, filters

def process_image(image_path):
    image = io.imread(image_path)
    # Use a function from a verified, reputable library.
    processed = filters.gaussian(image, sigma=1)
    return processed
```

### Language-Specific Examples

**JavaScript/Node.js:**
```javascript
// VULNERABLE: AI suggests non-existent package
// AI: "Install express-jwt-secure for enhanced JWT security"
// $ npm install express-jwt-secure

const jwtSecure = require('express-jwt-secure'); // Malicious package!

app.use(jwtSecure.protect());
```

```javascript
// SECURE: Verify before installing
// 1. Check npm: $ npm view express-jwt-secure
//    Result: "404 Not Found" - hallucination detected!
// 2. Search for real alternatives: "express jwt authentication"
// 3. Use verified packages with high download counts

const jwt = require('jsonwebtoken'); // 20M+ weekly downloads
const expressJWT = require('express-jwt'); // 1M+ weekly downloads

app.use(expressJWT({
  secret: process.env.JWT_SECRET,
  algorithms: ['HS256']
}));
```

**Java/Maven:**
```xml
<!-- VULNERABLE: AI suggests non-existent dependency -->
<!-- AI: "Add apache-commons-cryptography for encryption" -->
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-cryptography</artifactId>
    <version>1.0.0</version>
</dependency>
```

```xml
<!-- SECURE: Verify on Maven Central first -->
<!-- Search: https://search.maven.org/search?q=commons-cryptography -->
<!-- No results - hallucination! -->
<!-- Real alternative: Apache Commons Crypto -->
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-crypto</artifactId>
    <version>1.2.0</version>
</dependency>
```

## Detection

- **Verify Package Existence:** Search official registries before installing:
  - Python: `pip index versions <package-name>` or visit `pypi.org`
  - Node.js: `npm view <package-name>` or visit `npmjs.com`
  - Reject packages created within 48 hours or with < 100 weekly downloads
- **Check for Typosquatting:** Compare against popular packages using `pip search` or fuzzy matching tools
- **Review Package Statistics:** Check downloads, release history, maintainers, GitHub stars:
  - `npm view <package> time created dist-tags downloads`
  - Inspect package.json repository field for active GitHub repos
- **Use Auditing Tools:** Integrate into CI/CD:
  - `npm audit` / `pip-audit` for known vulnerabilities
  - `socket.dev` for AI hallucination detection
  - `osv-scanner` for supply chain risks

## Prevention

- [ ] **Always verify a package's existence** and reputation on its official registry before installing it.
- [ ] **Never blindly trust a package name** suggested by an AI. Treat it as a hint, not a command.
- [ ] **Check package download counts, creation dates, and maintainer reputation.**
- [ ] **Use lockfiles** (`package-lock.json`, `Pipfile.lock`, `yarn.lock`) to ensure that you are always installing the same version of a dependency.
- [ ] **Configure a private registry** or an approved list of packages for your organization to prevent developers from installing untrusted dependencies.
- [ ] **Integrate dependency scanning** and auditing tools into your CI/CD pipeline.

## Related Security Patterns & Anti-Patterns

- [Missing Input Validation Anti-Pattern](../missing-input-validation/): The core issue is a failure to validate the "input" from the AI model.

## References

- [OWASP Top 10 A03:2025 - Software Supply Chain Failures](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/)
- [OWASP GenAI LLM03:2025 - Supply Chain](https://genai.owasp.org/llmrisk/llm03-supply-chain/)
- [OWASP API Security API10:2023 - Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)
- [CWE-1357: Reliance on Unverified Package](https://cwe.mitre.org/data/definitions/1357.html)
- [CAPEC-538: Open-Source Library Manipulation](https://capec.mitre.org/data/definitions/538.html)
- [USENIX Study on Package Hallucination](https://arxiv.org/abs/2406.10279)
- [Socket.dev: AI Package Hallucinations](https://socket.dev/blog/ai-package-hallucinations)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
