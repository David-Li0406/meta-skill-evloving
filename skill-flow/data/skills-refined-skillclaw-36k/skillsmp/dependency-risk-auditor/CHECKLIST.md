# Dependency Audit Checklist

Complete checklist for auditing third-party dependency risks.

---

## Security Vulnerabilities

### Known Vulnerabilities (CVEs)

- [ ] **Critical CVEs** - No critical severity vulnerabilities
- [ ] **High CVEs** - No high severity vulnerabilities unaddressed
- [ ] **Medium CVEs** - Medium vulnerabilities tracked
- [ ] **Exploitability** - Vulnerable code paths actually used
- [ ] **Transitive CVEs** - Vulnerabilities in nested dependencies

### Supply Chain Security

- [ ] **Lock file exists** - package-lock.json, yarn.lock, etc.
- [ ] **Lock file committed** - Lock file in version control
- [ ] **Integrity hashes** - Package integrity verified
- [ ] **Registry trusted** - Using official registries
- [ ] **No typosquatting** - Package names verified (not `lodahs`)
- [ ] **Provenance** - Packages from verified publishers
- [ ] **2FA on publish** - Critical packages have 2FA

### Vulnerability Management

- [ ] **Regular scanning** - Automated security scans in CI
- [ ] **Alert routing** - Security alerts go to right team
- [ ] **SLA defined** - Fix timelines by severity
- [ ] **Upgrade path** - Can update without breaking changes

---

## Abandoned/Risky Dependencies

### Maintenance Health

- [ ] **Recent activity** - Commits within last 12 months
- [ ] **Issue response** - Maintainers respond to issues
- [ ] **PR review** - Pull requests are reviewed
- [ ] **Release cadence** - Regular releases (not stagnant)
- [ ] **Changelog** - Changes documented

### Bus Factor

- [ ] **Multiple maintainers** - Not single maintainer
- [ ] **Active maintainers** - Maintainers actually active
- [ ] **Organization owned** - Owned by org, not individual
- [ ] **Succession plan** - Clear ownership transfer process
- [ ] **Corporate backing** - Backed by sustainable org (if critical)

### Community Health

- [ ] **Download trend** - Not declining rapidly
- [ ] **Community size** - Appropriate to package scope
- [ ] **Documentation** - Well documented
- [ ] **Examples** - Usage examples available
- [ ] **Stack Overflow** - Community support exists

### Red Flags

- [ ] **No deprecation** - Package not deprecated
- [ ] **No security policy** - Has SECURITY.md or disclosure process
- [ ] **No archived** - Repository not archived
- [ ] **No ownership disputes** - No hostile forks
- [ ] **No funding issues** - Sustainable funding (if critical)

---

## Transitive Dependency Risks

### Dependency Depth

- [ ] **Depth reasonable** - Not excessively deep trees
- [ ] **Duplication minimal** - Same package not in multiple versions
- [ ] **Size reasonable** - Total dependencies appropriate

### Hotspot Analysis

- [ ] **Single points of failure** - Identify widely-used transitive deps
- [ ] **Hotspot health** - Critical transitive deps are healthy
- [ ] **Hotspot alternatives** - Know alternatives if hotspot fails
- [ ] **Version alignment** - Transitive deps on compatible versions

### Dependency Management

- [ ] **Overrides documented** - Any resolution overrides explained
- [ ] **Peer deps satisfied** - Peer dependency warnings resolved
- [ ] **Optional deps reviewed** - Optional dependencies intentional
- [ ] **Dev deps isolated** - Dev dependencies not in prod bundle

---

## License Compliance

### License Identification

- [ ] **All licenses known** - No UNKNOWN licenses
- [ ] **License files present** - Each package has license
- [ ] **SPDX identifiers** - Standard license identifiers used
- [ ] **License text matches** - License file matches declared

### Compatibility

- [ ] **Copyleft identified** - GPL, LGPL, AGPL packages flagged
- [ ] **Compatible with distribution** - Licenses allow your use case
- [ ] **Attribution requirements** - Attribution requirements documented
- [ ] **Patent grants** - Patent clauses understood (Apache 2.0)
- [ ] **Commercial use** - Licenses permit commercial use

### Policy Compliance

- [ ] **Allowed list** - Only approved licenses used
- [ ] **Denied list checked** - No explicitly forbidden licenses
- [ ] **Legal review** - Unclear licenses reviewed by legal
- [ ] **License file generated** - Third-party licenses distributed

---

## Lock-in Assessment

### Abstraction Level

- [ ] **Interface abstraction** - Critical deps behind interfaces
- [ ] **Standard protocols** - Using standards vs proprietary
- [ ] **Data portability** - Data format not vendor-specific
- [ ] **API compatibility** - APIs follow standards

### Migration Path

- [ ] **Alternatives exist** - Know alternatives for critical deps
- [ ] **Migration documented** - Migration path documented
- [ ] **Exit cost estimated** - Understand switching cost
- [ ] **Data export** - Can export data in standard format

### Vendor Risk

- [ ] **Vendor viability** - Vendor is financially stable
- [ ] **Vendor terms** - Terms of service acceptable
- [ ] **Price lock** - Understand pricing model changes
- [ ] **API stability** - API versioning and deprecation policy

---

## Upgrade Strategy

### Current State

- [ ] **Versions documented** - All versions in lock file
- [ ] **Update age** - Know how far behind latest
- [ ] **Breaking changes** - Identify major version gaps
- [ ] **Deprecations** - Track deprecated API usage

### Upgrade Planning

- [ ] **Security first** - Security updates prioritized
- [ ] **Test coverage** - Tests catch breaking changes
- [ ] **Staged rollout** - Can test upgrades incrementally
- [ ] **Rollback plan** - Can revert if upgrade fails

### Automation

- [ ] **Dependabot/Renovate** - Automated update PRs
- [ ] **Auto-merge patches** - Low-risk updates auto-merged
- [ ] **CI validation** - Updates tested before merge
- [ ] **Version pinning** - Appropriate version constraints

---

## Build & Bundle

### Production Bundle

- [ ] **No dev deps in prod** - Development deps excluded
- [ ] **Tree shaking** - Unused code eliminated
- [ ] **Bundle size** - Bundle size monitored
- [ ] **Duplicate code** - No duplicate package code

### Build Security

- [ ] **Build reproducible** - Same source = same output
- [ ] **No postinstall scripts** - Or scripts are audited
- [ ] **No network in build** - Build doesn't fetch at build time
- [ ] **Pinned CI deps** - CI tool versions pinned

---

## Specific Package Type Checks

### Node.js/npm

- [ ] **npm audit clean** - No npm audit findings
- [ ] **No .npmrc secrets** - No tokens in .npmrc
- [ ] **engines specified** - Node version requirements clear
- [ ] **package-lock version 3** - Modern lock file format

### Python/pip

- [ ] **pip-audit clean** - No pip-audit findings
- [ ] **requirements pinned** - Versions pinned (not `>=`)
- [ ] **Virtual env used** - Isolated environments
- [ ] **No system packages** - Not relying on system python

### Go

- [ ] **go.sum committed** - Checksums in version control
- [ ] **go mod tidy** - No unused dependencies
- [ ] **Vendoring decision** - Clear vendor policy
- [ ] **Replace directives** - Documented if used

### Rust/Cargo

- [ ] **cargo audit clean** - No cargo audit findings
- [ ] **Cargo.lock committed** - Lock file versioned
- [ ] **No unsafe** - Or unsafe usage audited
- [ ] **Feature flags minimal** - Only needed features enabled

---

## Risk Scoring

### Severity Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **CRITICAL** | Known exploited CVE, abandoned critical dep | Immediate fix |
| **HIGH** | High CVE, license violation, abandoned dep | This sprint |
| **MEDIUM** | Medium CVE, declining maintenance | Plan upgrade |
| **LOW** | Outdated but stable, minor issues | Monitor |
| **INFO** | Observation, improvement suggestion | Backlog |

### Package Risk Score

Calculate per-package risk:

```
Base Score:
- Critical CVE: +100
- High CVE: +50
- Medium CVE: +20
- No updates 12+ months: +30
- Single maintainer: +20
- <100 weekly downloads: +20
- Copyleft license: +40
- No license: +50
- Deep transitive: +10

Risk Level:
- 100+: CRITICAL
- 50-99: HIGH
- 20-49: MEDIUM
- 1-19: LOW
- 0: CLEAN
```

---

## Remediation Priority

### Immediate (P0)
- Critical CVE in direct dependency
- Abandoned critical dependency
- License violation blocking release
- Supply chain compromise indicator

### This Sprint (P1)
- High CVE in any dependency
- Deprecated package with no alternative
- License requiring legal review

### Next Sprint (P2)
- Medium CVE in direct dependency
- Package with declining maintenance
- Major version behind

### Backlog (P3)
- Minor version updates
- Dev dependency updates
- Nice-to-have alternatives
