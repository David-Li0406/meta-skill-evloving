---
name: sast
description: Expert Static Application Security Testing - Analyse statique du code source
---

# SAST - Static Application Security Testing

Tu es expert en **analyse statique de securite** du code source.

## Mission

> Detecter les vulnerabilites dans le code AVANT l'execution.

## Outils Principaux

### Open Source

| Outil | Langages | Forces |
|-------|----------|--------|
| **Semgrep** | Multi-langage | Regles personnalisables, rapide |
| **CodeQL** | Multi-langage | Analyse semantique profonde |
| **Bandit** | Python | Specialise Python |
| **ESLint Security** | JavaScript | Integration facile |
| **Brakeman** | Ruby/Rails | Specialise Rails |

### Commerciaux

| Outil | Forces |
|-------|--------|
| **SonarQube** | Dashboard, historique, qualite + securite |
| **Checkmarx** | Enterprise, compliance |
| **Snyk Code** | Developer-friendly, fix suggestions |
| **Veracode** | Certification, compliance |

## Integration CI/CD

### GitHub Actions

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Semgrep
      - name: Semgrep Scan
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten

      # CodeQL
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: javascript, typescript

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
```

### GitLab CI

```yaml
sast:
  stage: test
  image: returntocorp/semgrep
  script:
    - semgrep --config=p/security-audit --config=p/owasp-top-ten .
  artifacts:
    reports:
      sast: gl-sast-report.json
```

## Regles a Activer

### OWASP Top 10 Coverage

| Vuln | Regles Semgrep |
|------|----------------|
| Injection | `p/sql-injection`, `p/command-injection` |
| XSS | `p/xss` |
| Auth | `p/jwt`, `p/secrets` |
| Crypto | `p/insecure-crypto` |

### Configuration Recommandee Semgrep

```yaml
# .semgrep.yml
rules:
  - id: hardcoded-secret
    pattern: |
      $KEY = "..."
    message: "Potential hardcoded secret detected"
    severity: ERROR

  - id: sql-injection
    patterns:
      - pattern: |
          $QUERY = f"SELECT ... {$INPUT} ..."
    message: "Potential SQL injection"
    severity: ERROR
```

## Configuration SonarQube

```properties
# sonar-project.properties
sonar.projectKey=my-project
sonar.sources=src
sonar.exclusions=**/node_modules/**,**/test/**

# Quality Gate
sonar.qualitygate.wait=true

# Security Hotspots
sonar.security.hotspots.inheritedRiskOfFailure=true
```

## Bonnes Pratiques

### 1. Shift Left
- Executer SAST des le commit (pre-commit hooks)
- Bloquer les PR avec vulns critiques
- Eduquer les devs sur les patterns detectes

### 2. Reduire les Faux Positifs
- Affiner les regles au contexte projet
- Utiliser les suppressions documentees
- Maintenir une baseline

### 3. Priorisation

| Severite | Action | Delai |
|----------|--------|-------|
| Critical | Bloquer CI, fix immediat | < 24h |
| High | Bloquer merge, fix urgent | < 7j |
| Medium | Tracker, planifier fix | < 30j |
| Low | Backlog | Opportuniste |

## Limitations

- Ne detecte pas les vulns runtime
- Faux positifs possibles
- Ne remplace pas DAST/pentest

## Voir Aussi

- `appsec/dast` pour tests dynamiques
- `appsec/sca` pour dependances
- `secure-coding/validation` pour patterns
