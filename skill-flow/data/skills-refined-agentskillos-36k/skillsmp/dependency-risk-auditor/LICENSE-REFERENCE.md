# License Reference Guide

Quick reference for open source license compatibility and risks.

---

## License Categories

### Permissive Licenses ✅

Can use in proprietary software with minimal obligations.

| License | Attribution | Source Disclosure | Patent Grant |
|---------|-------------|-------------------|--------------|
| **MIT** | Yes | No | No |
| **ISC** | Yes | No | No |
| **BSD-2-Clause** | Yes | No | No |
| **BSD-3-Clause** | Yes | No | No |
| **Apache-2.0** | Yes | No | Yes |
| **Unlicense** | No | No | No |
| **CC0-1.0** | No | No | No |
| **WTFPL** | No | No | No |

**Typical Obligations:**
- Include copyright notice in source
- Include license text in binary distributions

---

### Weak Copyleft ⚠️

Can use in proprietary software, but modifications to the library itself must be shared.

| License | When Source Disclosure Required |
|---------|--------------------------------|
| **LGPL-2.1** | If you modify the library itself |
| **LGPL-3.0** | If you modify the library itself |
| **MPL-2.0** | If you modify files containing MPL code |
| **EPL-2.0** | If you modify the code |

**Key Points:**
- Can link dynamically without disclosure
- Must share changes to the library itself
- Usually safe for most applications

---

### Strong Copyleft :red_circle:

Using these typically requires sharing your entire codebase under the same license.

| License | Trigger |
|---------|---------|
| **GPL-2.0** | Distribution of binary using GPL code |
| **GPL-3.0** | Distribution of binary using GPL code |
| **AGPL-3.0** | Network use (SaaS) counts as distribution |

**Key Points:**
- :red_circle: **AGPL**: Even running as a service requires source disclosure
- GPL: Distribution triggers copyleft
- Internal use without distribution is typically OK
- Consult legal before using in commercial products

---

### Non-Commercial / Restricted ❌

Generally not suitable for commercial use.

| License | Restriction |
|---------|-------------|
| **CC-BY-NC** | Non-commercial use only |
| **CC-BY-NC-SA** | Non-commercial + share-alike |
| **Proprietary** | Requires paid license |
| **BUSL** | Commercial use restricted for period |
| **SSPL** | Extreme copyleft (MongoDB) |

---

## Compatibility Matrix

Can you combine code under these licenses?

```
                Using As Dependency (Column) In Project Licensed As (Row)
                ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
                │ MIT │ BSD │Apch2│LGPL │MPL-2│GPL-3│AGPL │
        ┌───────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
        │ Prop. │ ✅  │ ✅  │ ✅  │ ⚠️  │ ⚠️  │ ❌  │ ❌  │
        ├───────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
        │ MIT   │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │
        ├───────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
        │ Apch2 │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │ ⚠️  │ ⚠️  │
        ├───────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
        │ LGPL  │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │
        ├───────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
        │ GPL-3 │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │
        └───────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘

✅ = Compatible    ⚠️ = Check specifics    ❌ = Incompatible
```

---

## Common Scenarios

### Scenario 1: Proprietary SaaS Application

**Safe to use:**
- MIT, ISC, BSD ✅
- Apache-2.0 ✅
- LGPL (if dynamically linked) ⚠️
- MPL-2.0 (if not modifying) ⚠️

**Must avoid:**
- GPL ❌
- AGPL ❌ (SaaS triggers disclosure!)

---

### Scenario 2: Open Source Project (MIT licensed)

**Safe to use:**
- All permissive licenses ✅
- LGPL ✅
- GPL (your project becomes GPL) ⚠️

**Note:** Using GPL dependencies means your project effectively becomes GPL.

---

### Scenario 3: Client Deliverable (Proprietary)

**Safe to use:**
- MIT, ISC, BSD ✅
- Apache-2.0 ✅

**Require legal review:**
- LGPL ⚠️
- MPL ⚠️

**Cannot use:**
- GPL ❌
- AGPL ❌

---

### Scenario 4: Mobile App (App Store Distribution)

**Safe to use:**
- MIT, ISC, BSD ✅
- Apache-2.0 ✅

**Problematic:**
- GPL ❌ (App Store terms may conflict)
- LGPL ⚠️ (static linking issues on iOS)

---

## License Obligations Quick Reference

### MIT
```
Copyright (c) [year] [author]

Permission is hereby granted...
```
**You must:** Include copyright + license in source and binary distributions.

### Apache-2.0
**You must:**
- Include copyright notice
- Include NOTICE file if present
- State changes to files
- Include license text

**You get:** Patent grant from contributors

### LGPL
**You must:**
- Allow users to replace the LGPL library
- Provide source for LGPL modifications
- Include license text

**For dynamic linking:** Typically compliant without source disclosure.

### GPL
**You must:**
- License entire combined work under GPL
- Provide complete source code
- Include license text

### AGPL
**Same as GPL, plus:**
- Network users can request source code
- SaaS deployment counts as distribution

---

## Handling Unknown/Missing Licenses

### Investigation Steps

1. **Check package.json/setup.py** - Often declares license
2. **Look for LICENSE file** - May be named differently (COPYING, LICENSE.txt)
3. **Check README** - Sometimes stated there
4. **Check source headers** - License may be in code comments
5. **Contact author** - Ask for clarification
6. **Check npm/PyPI page** - Registries often show license

### If No License Found

:red_circle: **No license = All rights reserved (legally)**

Options:
- Contact author to add license
- Find alternative package
- Get explicit written permission
- Have legal assess risk

---

## License Audit Commands

```bash
# Node.js - List all licenses
npx license-checker --summary
npx license-checker --csv > licenses.csv

# Node.js - Fail on forbidden licenses
npx license-checker --production --failOn "GPL;AGPL;LGPL"

# Node.js - Only allow specific licenses
npx license-checker --production --onlyAllow "MIT;ISC;Apache-2.0;BSD-3-Clause"

# Python
pip-licenses --format=csv > licenses.csv
pip-licenses --fail-on="GPL"

# Go
go-licenses csv . 2>/dev/null

# Generate third-party notice file
npx license-checker --production --customPath format.json > THIRD_PARTY_LICENSES.txt
```

---

## License Red Flags

| Flag | Risk | Action |
|------|------|--------|
| `UNKNOWN` | Legal uncertainty | Investigate |
| `GPL` in proprietary | License violation | Replace or get permission |
| `AGPL` in SaaS | Must open source | Replace |
| `UNLICENSED` | No permission | Cannot use |
| Conflicting licenses | Legal mess | Legal review |
| `Commons Clause` | Commercial restriction | Verify use case |
| `SSPL` | Extreme copyleft | Likely replace |
| Dual license | May need paid option | Check terms |

---

## Attribution Template

For binary distributions, include a file like:

```
THIRD-PARTY LICENSES
====================

This software includes the following third-party packages:

lodash
------
MIT License
Copyright (c) JS Foundation and other contributors

[Full MIT license text]

---

axios
-----
MIT License
Copyright (c) 2014-present Matt Zabriskie

[Full MIT license text]

...
```

---

## When to Involve Legal

- Any GPL/AGPL in commercial product
- Unknown or custom licenses
- License compatibility questions
- Preparing for acquisition/IPO
- Distributing to customers
- Government/regulated customers
