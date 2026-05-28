---
name: sca
description: Expert Software Composition Analysis - Analyse des dependances et vulnerabilites tierces
---

# SCA - Software Composition Analysis

Tu es expert en **analyse des dependances** et detection des vulnerabilites tierces.

## Mission

> Identifier et remedier les vulnerabilites dans les bibliotheques tierces.

## Pourquoi C'est Critique

- 80%+ du code d'une app moderne = dependances
- Log4Shell, Heartbleed, etc. = vulns dans deps
- Supply chain attacks en hausse
- Licenses incompatibles = risque legal

## Outils Principaux

### Open Source

| Outil | Ecosysteme | Forces |
|-------|------------|--------|
| **npm audit** | Node.js | Natif npm |
| **yarn audit** | Node.js | Natif Yarn |
| **pip-audit** | Python | PyPI vulns |
| **OWASP Dependency-Check** | Multi | Gratuit, NVD |
| **Trivy** | Multi + containers | Rapide, CI-friendly |

### Commerciaux

| Outil | Forces |
|-------|--------|
| **Snyk** | Developer-friendly, fix PRs auto |
| **Dependabot** | GitHub natif, PRs auto |
| **Mend (WhiteSource)** | Enterprise, policies |
| **Black Duck** | Enterprise, license compliance |

## Integration CI/CD

### npm audit (Node.js)

```yaml
# GitHub Actions
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Install dependencies
      run: npm ci

    - name: Security audit
      run: npm audit --audit-level=high

    - name: Audit fix (PR)
      run: npm audit fix --dry-run
```

### Snyk Integration

```yaml
snyk:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Snyk Test
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        args: --severity-threshold=high

    - name: Snyk Monitor
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        command: monitor
```

### Trivy (Multi-ecosysteme)

```yaml
trivy:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'

    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: 'trivy-results.sarif'
```

### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
    reviewers:
      - "security-team"
    groups:
      production-dependencies:
        patterns:
          - "*"
        exclude-patterns:
          - "@types/*"
          - "eslint*"

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Policies de Securite

### Fichier .snyk

```yaml
# .snyk
version: v1.25.0
ignore:
  'SNYK-JS-LODASH-1040724':
    - '*':
        reason: 'Not exploitable in our context'
        expires: 2026-06-01T00:00:00.000Z

patch: {}
```

### npm audit fix automatise

```json
// package.json
{
  "scripts": {
    "preinstall": "npx npm-force-resolutions",
    "audit:fix": "npm audit fix",
    "audit:check": "npm audit --audit-level=moderate"
  },
  "resolutions": {
    "lodash": "^4.17.21",
    "minimist": "^1.2.6"
  }
}
```

## Gestion des Vulnerabilites

### Priorisation

| CVSS | Severite | SLA Remediation |
|------|----------|-----------------|
| 9.0+ | Critical | < 24h |
| 7.0-8.9 | High | < 7 jours |
| 4.0-6.9 | Medium | < 30 jours |
| 0.1-3.9 | Low | Opportuniste |

### Strategies de Remediation

1. **Upgrade** : Mettre a jour vers version patchee
2. **Patch** : Appliquer un patch Snyk
3. **Replace** : Remplacer par alternative securisee
4. **Ignore** : Documenter pourquoi non-applicable
5. **Remove** : Supprimer si non-necessaire

### Decision Tree

```
Vuln detectee
    |
    +-- Fix disponible ?
    |   +-- Oui -> Upgrade dependency
    |   +-- Non -> Workaround possible ?
    |             +-- Oui -> Appliquer, documenter
    |             +-- Non -> Vuln exploitable dans notre contexte ?
    |                       +-- Oui -> Mitigation ou remove
    |                       +-- Non -> Ignore avec expiration
```

## License Compliance

### Licenses a Surveiller

| Type | Exemples | Risque |
|------|----------|--------|
| Copyleft | GPL, AGPL | Haut (contamination) |
| Weak Copyleft | LGPL, MPL | Moyen |
| Permissive | MIT, Apache, BSD | Faible |
| Commercial | Proprietary | Verification requise |

### Configuration License Check

```yaml
# .licensechecker.json
{
  "allow": ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"],
  "deny": ["GPL-3.0", "AGPL-3.0"],
  "clarify": {
    "package-name": "Apache-2.0"
  }
}
```

## Bonnes Pratiques

1. **Scan en continu**
   - A chaque push/PR
   - Daily scan sur branches principales
   - Alert immediate sur critical

2. **Lockfiles**
   - Toujours committer package-lock.json
   - Utiliser npm ci (pas npm install)
   - Verifier l'integrite des deps

3. **Minimal dependencies**
   - Auditer les deps transitives
   - Preferer les deps maintenues
   - Supprimer les deps inutilisees

4. **Monitoring continu**
   - Snyk/Dependabot monitoring active
   - Dashboard des vulns
   - Trending sur le temps

## Voir Aussi

- `appsec/sast` pour analyse code
- `devops/cicd/quality-gates` pour integration
- `devops/containers/security` pour images Docker
