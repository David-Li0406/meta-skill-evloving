<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Open Source License Compliance & Legal Review Guide

Comprehensive guide for detecting, analyzing, and ensuring compliance with open source licenses in software projects.

## Table of Contents

- [License Detection](#license-detection)
- [Common Open Source Licenses](#common-open-source-licenses)
- [License Compliance Requirements](#license-compliance-requirements)
- [License Compatibility](#license-compatibility)
- [Copyright & Attribution](#copyright--attribution)
- [Compliance Automation](#compliance-automation)
- [Best Practices](#best-practices)

## License Detection

### Detection Methods

1. **SPDX Identifiers**
   - Standardized short identifiers (e.g., `MIT`, `Apache-2.0`, `GPL-3.0-only`)
   - Found in file headers, package manifests, LICENSE files
   - SPDX License List: https://spdx.org/licenses/

2. **License Text Matching**
   - Full text comparison against known licenses
   - Fuzzy matching for minor variations
   - Tools: ScanCode, Licensee, FOSSA

3. **File Locations**
   ```
   LICENSE
   LICENSE.txt
   LICENSE.md
   COPYING
   COPYING.txt
   COPYRIGHT
   NOTICE
   README.md (license section)
   package.json (license field)
   pom.xml (licenses section)
   Cargo.toml (license field)
   setup.py (license argument)
   ```

4. **Package Manifest Fields**
   ```json
   // package.json
   {
     "license": "MIT",
     "licenses": [{"type": "MIT", "url": "..."}]
   }
   ```

   ```toml
   # Cargo.toml
   [package]
   license = "MIT OR Apache-2.0"
   ```

   ```xml
   <!-- pom.xml -->
   <licenses>
     <license>
       <name>Apache License 2.0</name>
       <url>https://www.apache.org/licenses/LICENSE-2.0</url>
     </license>
   </licenses>
   ```

### SPDX License Expressions

Complex licensing can be expressed using SPDX expressions:

```
MIT                           # Single license
MIT OR Apache-2.0             # Dual licensing (choice)
MIT AND Apache-2.0            # Both licenses apply
GPL-3.0-only WITH Classpath-exception-2.0  # License with exception
```

Operators:
- `AND` - Both licenses apply
- `OR` - Either license (user's choice)
- `WITH` - License with exception

## Common Open Source Licenses

### Permissive Licenses

#### MIT License
- **Type**: Permissive
- **SPDX**: `MIT`
- **Requirements**:
  - Include copyright notice
  - Include license text
- **Permissions**: Commercial use, modification, distribution, sublicense
- **Compatibility**: Compatible with most licenses including GPL
- **Common in**: JavaScript/npm ecosystem

#### Apache License 2.0
- **Type**: Permissive with patent grant
- **SPDX**: `Apache-2.0`
- **Requirements**:
  - Include copyright notice
  - Include license text
  - Include NOTICE file if present
  - State significant changes
- **Permissions**: Commercial use, modification, distribution, sublicense, patent use
- **Patent Grant**: Express patent license from contributors
- **Compatibility**: Compatible with GPL-3.0+, incompatible with GPL-2.0
- **Common in**: Apache projects, Android, Kubernetes

#### BSD Licenses
- **BSD-2-Clause** (`BSD-2-Clause`): Simple, permissive
  - Include copyright notice
  - Include license text

- **BSD-3-Clause** (`BSD-3-Clause`): Adds non-endorsement clause
  - Same as BSD-2-Clause plus
  - Cannot use project name for endorsement without permission

### Copyleft Licenses

#### GNU General Public License (GPL)

**GPL-2.0** (`GPL-2.0-only` or `GPL-2.0-or-later`)
- **Type**: Strong copyleft
- **Requirements**:
  - Distribute source code
  - License derivative works under GPL-2.0
  - Include copyright notices
  - Include license text
- **Trigger**: Binary distribution, not SaaS
- **Linking**: Static/dynamic linking triggers copyleft
- **Compatibility**: Incompatible with Apache-2.0

**GPL-3.0** (`GPL-3.0-only` or `GPL-3.0-or-later`)
- **Type**: Strong copyleft
- **Additional protections**:
  - Patent retaliation clause
  - Anti-tivoization (DRM restrictions)
  - Explicit compatibility with Apache-2.0
- **Requirements**: Same as GPL-2.0 plus:
  - Installation information for user products
  - No patent litigation

#### GNU Lesser General Public License (LGPL)
- **SPDX**: `LGPL-2.1-only`, `LGPL-3.0-only`
- **Type**: Weak copyleft
- **Difference from GPL**: Allows proprietary software to link to LGPL libraries
- **Requirements**:
  - Modifications to LGPL code must be LGPL
  - Can link from proprietary code
  - Must allow user to replace LGPL library

#### GNU Affero General Public License (AGPL)
- **SPDX**: `AGPL-3.0-only`
- **Type**: Network copyleft
- **Key Difference**: SaaS/network use triggers distribution requirements
- **Use Case**: Prevents "SaaS loophole"
- **Compatibility**: One-way compatible to GPL-3.0

### Other Important Licenses

#### Mozilla Public License 2.0 (MPL-2.0)
- **Type**: Weak copyleft (file-level)
- **Requirements**: MPL files stay MPL, can combine with proprietary files
- **Compatibility**: Compatible with GPL-2.0+, Apache-2.0

#### Eclipse Public License 2.0 (EPL-2.0)
- **Type**: Weak copyleft
- **Requirements**: Similar to MPL, module-level copyleft
- **Compatibility**: Compatible with GPL

#### Unlicense / CC0 / 0BSD
- **Type**: Public domain dedication
- **Requirements**: None
- **Use**: "Do whatever you want"

## License Compliance Requirements

### Attribution Requirements

Most licenses require:
1. **Copyright notices** - Preserve original copyright statements
2. **License text** - Include full license text
3. **NOTICE files** - Include if present (Apache-2.0)
4. **Change documentation** - Document significant modifications

### Example Attribution for MIT

```
Copyright (c) 2024 Original Author

Permission is hereby granted, free of charge...
[Full MIT license text]
```

### Example Attribution for Apache-2.0

```
This product includes software developed by...

Copyright 2024 Original Author

Licensed under the Apache License, Version 2.0...

[Include NOTICE file if present]
```

### Source Code Availability

Copyleft licenses require source code:

| License | Source Required | Trigger |
|---------|----------------|---------|
| MIT | No | N/A |
| Apache-2.0 | No | N/A |
| BSD | No | N/A |
| GPL-2.0/3.0 | Yes | Binary distribution |
| LGPL | Yes (for LGPL code only) | Binary distribution |
| AGPL | Yes | Network use (SaaS) |
| MPL-2.0 | Yes (for MPL files) | Binary distribution |

### Compliance Obligations by License

#### MIT/BSD Compliance Checklist
- [ ] Include copyright notice in source
- [ ] Include license text
- [ ] Preserve notices in distributions

#### Apache-2.0 Compliance Checklist
- [ ] Include copyright notice
- [ ] Include LICENSE file
- [ ] Include NOTICE file (if exists)
- [ ] Document significant changes
- [ ] Preserve attribution notices
- [ ] Include patent grant notice

#### GPL-3.0 Compliance Checklist
- [ ] Provide complete source code
- [ ] Include all build scripts
- [ ] Include LICENSE file
- [ ] Preserve copyright notices
- [ ] License derivative works under GPL-3.0
- [ ] Provide installation information (user products)
- [ ] Include written offer for source (if distributing binaries)

## License Compatibility

### Compatibility Matrix

| From ↓ / To → | MIT | Apache-2.0 | GPL-2.0 | GPL-3.0 | LGPL-3.0 | AGPL-3.0 | MPL-2.0 | Proprietary |
|---------------|-----|------------|---------|---------|----------|----------|---------|-------------|
| MIT           | ✅  | ✅         | ✅      | ✅      | ✅       | ✅       | ✅      | ✅          |
| Apache-2.0    | ✅  | ✅         | ❌      | ✅      | ✅       | ✅       | ✅      | ✅          |
| BSD-3         | ✅  | ✅         | ✅      | ✅      | ✅       | ✅       | ✅      | ✅          |
| GPL-2.0       | ❌  | ❌         | ✅      | ❌      | ❌       | ❌       | ❌      | ❌          |
| GPL-3.0       | ❌  | ❌         | ❌      | ✅      | ✅       | ✅       | ✅      | ❌          |
| LGPL-3.0      | ❌  | ❌         | ❌      | ✅      | ✅       | ✅       | ✅      | ⚠️ (linking) |
| AGPL-3.0      | ❌  | ❌         | ❌      | ✅      | ✅       | ✅       | ❌      | ❌          |
| MPL-2.0       | ❌  | ❌         | ❌      | ✅      | ✅       | ❌       | ✅      | ⚠️ (file-level)|

✅ = Compatible
❌ = Incompatible
⚠️ = Conditional compatibility

### Copyleft Strength Hierarchy

```
Public Domain (CC0, Unlicense)
    ↓
Permissive (MIT, BSD, Apache-2.0)
    ↓
Weak Copyleft (LGPL, MPL)
    ↓
Strong Copyleft (GPL)
    ↓
Network Copyleft (AGPL)
```

**Rule**: You can generally relicense "up" the hierarchy but not "down"

### Common Incompatibilities

1. **GPL-2.0 + Apache-2.0** ❌
   - Apache's patent clause incompatible with GPL-2.0
   - **Solution**: Use GPL-3.0 which is compatible with Apache-2.0

2. **GPL + Proprietary** ❌
   - Cannot combine GPL code with proprietary code
   - **Exceptions**:
     - LGPL allows proprietary linking
     - System library exception
     - Linking through network APIs (for non-AGPL)

3. **Multiple Copyleft Licenses** ❌
   - Cannot mix GPL + MPL in same file
   - **Solution**: Use dual licensing or keep in separate files

### Dual Licensing

Many projects offer choice of licenses:

```toml
# Rust ecosystem common pattern
license = "MIT OR Apache-2.0"
```

Users can choose which license to follow. This allows:
- **MIT OR Apache-2.0**: User picks most suitable
- **GPL-2.0-or-later**: Can use as GPL-2.0 or any later GPL version

## Copyright & Attribution

### Copyright Notice Detection

Pattern matching for copyright statements:

```regex
# Standard patterns
Copyright\s+(?:©|\(c\)|&copy;)?\s*(?:\d{4}(?:-\d{4})?(?:,\s*\d{4}(?:-\d{4})?)*)\s+(.+?)(?:\n|$)

# Variations
©\s*\d{4}
\(c\)\s*\d{4}
Copyright:?\s+\d{4}

# Examples:
Copyright (c) 2024 John Doe
Copyright © 2020-2024 Acme Corp
© 2024 Developer Name
(c) 2024 Company Inc.
```

### Copyright Year Ranges

Valid formats:
- `2024` - Single year
- `2020-2024` - Range
- `2020, 2022, 2024` - Specific years
- `2020-2024, 2025` - Combination

### Attribution File Formats

**NOTICE File (Apache-2.0)**
```
Project Name
Copyright 2024 Project Authors

This product includes software developed by...

Third-party dependencies:
- Library Name (License): Copyright 2024 Author
```

**ATTRIBUTION File**
```markdown
# Third-Party Attributions

## library-name (MIT)
Copyright (c) 2024 Author Name
https://github.com/author/library

## another-lib (Apache-2.0)
Copyright (c) 2020-2024 Another Author
https://apache.org/licenses/LICENSE-2.0
```

## Compliance Automation

### License Scanning Tools

1. **ScanCode Toolkit**
   ```bash
   scancode --license --copyright --package --json-pp output.json path/to/code
   ```
   - Comprehensive license and copyright detection
   - SPDX identifier support
   - 30,000+ license texts

2. **Licensee (GitHub)**
   ```bash
   licensee detect path/to/repo
   ```
   - Confidence scoring
   - Multiple license detection
   - Used by GitHub

3. **FOSSA**
   - Commercial SaaS platform
   - Dependency license scanning
   - Compliance policy enforcement

4. **FOSSology**
   - Open source compliance platform
   - License obligations tracking
   - Clearance workflow

5. **OSS Review Toolkit (ORT)**
   ```bash
   ort analyze -i path/to/project
   ort scan -i analyzer-result.yml
   ```
   - Complete compliance workflow
   - Multiple package managers
   - Policy evaluation

### SPDX Document Generation

Example SPDX 3.0 document:

```json
{
  "spdxVersion": "SPDX-3.0",
  "creationInfo": {
    "created": "2024-01-01T00:00:00Z",
    "createdBy": ["Tool: scanner-v1.0"]
  },
  "packages": [{
    "SPDXID": "SPDXRef-Package",
    "name": "my-project",
    "versionInfo": "1.0.0",
    "licenseConcluded": "MIT",
    "licenseDeclared": "MIT",
    "copyrightText": "Copyright 2024 Author",
    "filesAnalyzed": true
  }]
}
```

## Best Practices

### 1. License File Placement

**Root LICENSE file**
- Include at repository root
- Use SPDX identifier in file header
- Consider LICENSE.md for better rendering

**Per-file SPDX headers**
```javascript
// SPDX-License-Identifier: MIT
// Copyright (c) 2024 Author Name
```

```python
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Project Contributors
```

### 2. Dependency License Review

**Pre-approval workflow**:
1. Scan new dependencies before adding
2. Check against approved license list
3. Review license compatibility
4. Document license decisions

**Approved license lists**:
```json
{
  "allowed": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"],
  "review_required": ["MPL-2.0", "LGPL-3.0"],
  "denied": ["GPL-2.0", "GPL-3.0", "AGPL-3.0", "SSPL"]
}
```

### 3. License Policy Enforcement

**CI/CD Integration**:
```yaml
# Example GitHub Action
- name: License Scan
  run: |
    scancode --license --json licenses.json .
    python check_licenses.py licenses.json
```

**Policy checks**:
- No GPL in proprietary products
- All dependencies have licenses
- No incompatible license combinations
- Attribution requirements met

### 4. Documentation Requirements

**README.md**:
```markdown
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Third-Party Licenses

This project uses the following open source packages:
- [package-name](link) - MIT License
- [another-package](link) - Apache-2.0 License

See [ATTRIBUTION](ATTRIBUTION.md) for full attribution notices.
```

### 5. Dual Licensing Strategy

When to use dual licensing:
- **MIT + Apache-2.0**: Maximum compatibility (Rust ecosystem standard)
- **GPL + Commercial**: Open source with commercial option
- **LGPL + Commercial**: Library with proprietary use option

### 6. License Headers

Consistent header format:
```bash
# Standard header for all files
SPDX-License-Identifier: MIT
Copyright (c) 2024 Company Name

For full license text, see LICENSE file in repository root.
```

### 7. Continuous Monitoring

- **Regular dependency audits**: Quarterly license reviews
- **Automated scanning**: On every commit/PR
- **Policy updates**: Track license list changes
- **Legal review**: Annual comprehensive audit

## Enterprise License Management

### License Compliance Program

1. **Policy Definition**
   - Approved licenses list
   - Review process for exceptions
   - Compliance requirements

2. **Tool Selection**
   - Automated scanning
   - Policy enforcement
   - Reporting capabilities

3. **Training**
   - Developer education
   - License implications
   - Compliance procedures

4. **Audit Process**
   - Regular reviews
   - Third-party audits
   - M&A due diligence

### Risk Assessment

License risk levels:

**Low Risk**:
- MIT, BSD, Apache-2.0
- Well-understood obligations
- Commercial-friendly

**Medium Risk**:
- LGPL, MPL (weak copyleft)
- Requires legal review
- Integration restrictions

**High Risk**:
- GPL, AGPL (strong copyleft)
- Significant obligations
- May prohibit commercial use

**Critical Risk**:
- Unknown/custom licenses
- No license (all rights reserved)
- License conflicts

## Common Scenarios

### Scenario 1: Using GPL Library in Proprietary Software

**Problem**: Cannot link GPL code with proprietary code

**Solutions**:
1. Find alternative library with permissive license
2. Communicate via network APIs (not applicable for AGPL)
3. Use LGPL version if available
4. Obtain commercial license
5. Release product as GPL

### Scenario 2: Apache-2.0 + GPL-2.0 Dependencies

**Problem**: Apache-2.0 incompatible with GPL-2.0

**Solutions**:
1. Upgrade GPL-2.0 to GPL-3.0 (if `-or-later`)
2. Remove Apache-2.0 dependency
3. Request GPL-2.0 project upgrade to GPL-3.0

### Scenario 3: Multiple Licenses in Single Project

**Solution**: License stacking
- Different files can have different licenses
- Document clearly in README
- Ensure compatibility
- Comply with all license requirements

## 2025 Updates & Trends

### SPDX 3.0 Adoption
- Enhanced security metadata
- Better SBOM integration
- Improved relationship modeling
- AI/ML dataset licensing

### Software Heritage Integration
- Persistent software identifiers (SWHIDs)
- Long-term source archival
- License preservation

### AI/ML Model Licensing
- Training data licenses
- Model weight licenses
- RAI (Responsible AI) licenses
- RAIL (Responsible AI License)

### Supply Chain Security
- SLSA provenance + licensing
- Sigstore integration
- License attestations
- VEX + licensing correlation

## Tools & Resources

### Open Source Tools
- **ScanCode**: https://github.com/nexB/scancode-toolkit
- **Licensee**: https://github.com/licensee/licensee
- **OSS Review Toolkit**: https://github.com/oss-review-toolkit/ort
- **FOSSology**: https://www.fossology.org/
- **REUSE**: https://reuse.software/

### Commercial Tools
- **FOSSA**: https://fossa.com/
- **Black Duck**: https://www.blackducksoftware.com/
- **WhiteSource/Mend**: https://www.mend.io/
- **Snyk**: https://snyk.io/

### Standards & References
- **SPDX License List**: https://spdx.org/licenses/
- **SPDX Specification**: https://spdx.github.io/spdx-spec/
- **tl;drLegal**: https://tldrlegal.com/
- **Choose a License**: https://choosealicense.com/
- **OSI Approved Licenses**: https://opensource.org/licenses/

### Legal Resources
- **Software Freedom Law Center**: https://softwarefreedom.org/
- **Free Software Foundation**: https://www.fsf.org/
- **Apache Software Foundation**: https://www.apache.org/legal/
- **Linux Foundation**: https://www.linuxfoundation.org/legal/

## Summary

Key takeaways for license compliance:

1. **Always detect and document licenses** in dependencies
2. **Understand license obligations** (attribution, copyleft, patents)
3. **Check compatibility** before combining code
4. **Automate compliance** with CI/CD scanning
5. **Maintain NOTICE/ATTRIBUTION** files
6. **Use SPDX identifiers** for clarity
7. **Regular audits** prevent compliance issues
8. **Legal review** for complex scenarios

License compliance is an ongoing process, not a one-time check. Automate where possible, but involve legal counsel for significant decisions.
