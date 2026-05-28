---
name: security-expert
description: |-
  Expert securite applicative et infrastructure - OWASP, pentest, secure coding, threat modeling. Utilise ce skill quand: (1) audit de securite applicative, (2) implementation SAST/DAST/IAST, (3) secure coding practices, (4) threat modeling et analyse de risques, (5) tests de penetration, (6) conformite RGPD/SOC2/ISO27001.
metadata:
  version: 1.0.0
  status: active
---

# Security Expert Skill

## Quick Start

```bash
# 1. Navigation rapide vers un agent
security-expert/agents/appsec/sast              # Analyse statique du code
security-expert/agents/appsec/dast              # Tests dynamiques
security-expert/agents/secure-coding/validation # Validation des entrees
security-expert/agents/threat-modeling/stride   # Methodologie STRIDE
security-expert/agents/penetration/owasp-top10  # Tests OWASP Top 10
security-expert/agents/compliance/rgpd          # Implementation RGPD

# 2. Executer les tests de validation
cd .web-agency/skills/security-expert && npm test

# 3. Questions frequentes
"Comment implementer SAST dans ma CI ?"     -> appsec/sast
"Valider les entrees utilisateur ?"         -> secure-coding/validation
"Faire un threat model de mon app ?"        -> threat-modeling/stride
"Tester les vulnerabilites OWASP ?"         -> penetration/owasp-top10
"Implementer le RGPD techniquement ?"       -> compliance/rgpd
```

## Position dans l'Architecture

Ce skill est au **NIVEAU 3 : IMPLEMENTATION**. Il implemente les politiques de securite definies par `direction-technique/securite`.

```
+---------------------------------------------------------------------------+
|  NIVEAU 1 : STRATEGIE (direction-technique/securite)                       |
|  -> POURQUOI : Politique securite, exigences conformite, budget            |
+----------------------------------------------------------------------------+
|  NIVEAU 2 : PROCESSUS                                                      |
|  +----------------------------+  +----------------------------+            |
|  |     testing-process        |  |       web-dev-process      |            |
|  |  security/ (methodologie)  |  |  testing/security/         |            |
|  |  QUOI : Quels tests faire  |  |  QUOI : Quand tester       |            |
|  +----------------------------+  +----------------------------+            |
+----------------------------------------------------------------------------+
|  NIVEAU 3 : IMPLEMENTATION                                                 |
|  +------------------------------------------------------------------+     |
|  |                    security-expert <- CE SKILL                    |     |
|  |  COMMENT : SAST, DAST, secure coding, pentest, compliance impl    |     |
|  +------------------------------------------------------------------+     |
+----------------------------------------------------------------------------+
```

## Philosophie

> Securiser par design, valider en continu.

Ce skill :
- Implemente les outils de securite (SAST, DAST, IAST)
- Guide le secure coding avec des patterns concrets
- Realise les threat models et analyses de risques
- Execute les tests de penetration
- Implemente la conformite (RGPD, SOC2, ISO27001)

Il ne fait PAS :
- Les decisions strategiques de securite -> `direction-technique/securite`
- La definition des process de tests securite -> `testing-process/security`
- La gestion des incidents -> `direction-technique/support/gestion-incidents`
- La configuration infrastructure securisee -> `devops/infrastructure`

## Domaines et Agents (24 agents)

### 1. appsec/ - Application Security (5 agents)

Outils et implementation de la securite applicative.

| Agent | Responsabilite | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination AppSec | - |
| `sast` | Analyse statique du code | SonarQube, Semgrep, CodeQL |
| `dast` | Tests dynamiques | OWASP ZAP, Burp Suite, Nuclei |
| `iast` | Instrumentation runtime | Contrast, Hdiv |
| `sca` | Analyse des dependances | Snyk, npm audit, Dependabot |

### 2. secure-coding/ - Developpement Securise (5 agents)

Patterns et pratiques de code securise.

| Agent | Responsabilite | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination secure coding | - |
| `validation` | Validation des entrees | Zod, Joi, express-validator |
| `authentication` | Auth securisee | JWT, OAuth2, OIDC, MFA |
| `authorization` | Controle d'acces | RBAC, ABAC, policies |
| `cryptography` | Chiffrement et hachage | bcrypt, argon2, AES, RSA |

### 3. threat-modeling/ - Modelisation des Menaces (4 agents)

Identification et analyse des risques.

| Agent | Responsabilite | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination threat modeling | - |
| `stride` | Methodologie STRIDE | Diagrammes, matrices |
| `attack-trees` | Arbres d'attaque | Threat modeling tools |
| `risk-assessment` | Evaluation des risques | CVSS, matrices de risques |

### 4. penetration/ - Tests de Penetration (5 agents)

Tests offensifs et identification de vulnerabilites.

| Agent | Responsabilite | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination pentest | - |
| `owasp-top10` | Tests OWASP Top 10 | Injection, XSS, CSRF, etc. |
| `api-security` | Securite des APIs | OWASP API Top 10 |
| `web-vulnerabilities` | Vulnerabilites web | SQLi, XSS, SSRF, IDOR |
| `reporting` | Rapports de pentest | Templates, CVSS, remediation |

### 5. compliance/ - Conformite (5 agents)

Implementation des standards de conformite.

| Agent | Responsabilite | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination conformite | - |
| `rgpd` | Implementation RGPD | Consentement, DPO, droits |
| `soc2` | Conformite SOC2 | Controles, evidence, audit |
| `iso27001` | Implementation ISO 27001 | SMSI, controles, certification |
| `pci-dss` | Conformite PCI DSS | Cartes de paiement, tokenization |

**Total : 24 agents specialises**

## Regles de Routage

### Par Type de Question

| Question | Domaine |
|----------|---------|
| SAST, DAST, analyse de code, scan | `appsec/` |
| Validation, auth, chiffrement, code securise | `secure-coding/` |
| Threat model, STRIDE, risques, attaques | `threat-modeling/` |
| Pentest, OWASP, vulnerabilites, injection | `penetration/` |
| RGPD, SOC2, ISO27001, conformite | `compliance/` |

### Par Mots-Cles

| Mots-cles | Domaine/Agent |
|-----------|---------------|
| SonarQube, Semgrep, CodeQL, analyse statique | `appsec/sast` |
| ZAP, Burp, scan dynamique, fuzzing | `appsec/dast` |
| Snyk, npm audit, dependances, CVE | `appsec/sca` |
| input validation, sanitize, escape, Zod | `secure-coding/validation` |
| JWT, OAuth, session, MFA, auth | `secure-coding/authentication` |
| RBAC, permissions, policies, access control | `secure-coding/authorization` |
| bcrypt, hash, encrypt, AES, RSA, salt | `secure-coding/cryptography` |
| STRIDE, threat model, DFD, trust boundary | `threat-modeling/stride` |
| attack tree, kill chain, threat actor | `threat-modeling/attack-trees` |
| CVSS, risk matrix, impact, likelihood | `threat-modeling/risk-assessment` |
| OWASP Top 10, injection, XSS, CSRF | `penetration/owasp-top10` |
| API security, broken auth, mass assignment | `penetration/api-security` |
| SQLi, SSRF, IDOR, path traversal | `penetration/web-vulnerabilities` |
| RGPD, GDPR, consentement, DPO, droits | `compliance/rgpd` |
| SOC2, audit trail, evidence, controls | `compliance/soc2` |

## Arbre de Decision

```
Requete Security
|
+-- Concerne les outils de scan/analyse ?
|   +-- Analyse statique du code -> appsec/sast
|   +-- Tests dynamiques -> appsec/dast
|   +-- Runtime instrumentation -> appsec/iast
|   +-- Dependances vulnerables -> appsec/sca
|
+-- Concerne le code securise ?
|   +-- Validation entrees -> secure-coding/validation
|   +-- Authentification -> secure-coding/authentication
|   +-- Autorisation -> secure-coding/authorization
|   +-- Chiffrement -> secure-coding/cryptography
|
+-- Concerne l'analyse des risques ?
|   +-- Threat modeling STRIDE -> threat-modeling/stride
|   +-- Arbres d'attaque -> threat-modeling/attack-trees
|   +-- Evaluation risques -> threat-modeling/risk-assessment
|
+-- Concerne les tests de penetration ?
|   +-- OWASP Top 10 -> penetration/owasp-top10
|   +-- Securite API -> penetration/api-security
|   +-- Vulns web specifiques -> penetration/web-vulnerabilities
|   +-- Rapports pentest -> penetration/reporting
|
+-- Concerne la conformite ?
|   +-- RGPD/GDPR -> compliance/rgpd
|   +-- SOC2 -> compliance/soc2
|   +-- ISO 27001 -> compliance/iso27001
|   +-- PCI DSS -> compliance/pci-dss
|
+-- Decision strategique securite ?
|   +-- -> direction-technique/securite
|
+-- Methodologie de test securite ?
    +-- -> testing-process/security
```

## Interaction avec les Autres Skills

### Flux Entrants

```
direction-technique/securite --> security-expert (politique -> implementation)
testing-process/security --> security-expert (methodologie -> outils)
web-dev-process/testing --> security-expert (phase testing -> execution)
```

### Flux Sortants

```
security-expert --> backend-developer (patterns securises backend)
security-expert --> frontend-developer (patterns securises frontend)
security-expert --> devops (integration CI/CD securite)
```

## Points d'Escalade

### Vers direction-technique

| Situation | Raison |
|-----------|--------|
| Vulnerabilite critique trouvee | Decision remediation urgente |
| Non-conformite majeure | Impact legal/business |
| Choix d'outils securite | Decision strategique |
| Budget securite | Validation financiere |

### Vers l'humain

| Situation | Raison |
|-----------|--------|
| Pentest sur prod | Autorisation explicite requise |
| Fuite de donnees suspectee | Responsabilite legale |
| Choix architectural securite | Impact business |
| Tests destructifs | Risque operationnel |

## Security Principles

### Defense in Depth

```
+------------------------------------------+
|              WAF / CDN                   |
|  +------------------------------------+  |
|  |         Load Balancer              |  |
|  |  +------------------------------+  |  |
|  |  |    Application (validated)   |  |  |
|  |  |  +-----------------------+   |  |  |
|  |  |  |   Business Logic     |   |  |  |
|  |  |  |  +----------------+  |   |  |  |
|  |  |  |  | Data (encrypted)|  |   |  |  |
|  |  |  |  +----------------+  |   |  |  |
|  |  |  +-----------------------+   |  |  |
|  |  +------------------------------+  |  |
|  +------------------------------------+  |
+------------------------------------------+
```

### OWASP Top 10 Coverage

| # | Vulnerability | Agent(s) |
|---|---------------|----------|
| A01 | Broken Access Control | `secure-coding/authorization`, `penetration/owasp-top10` |
| A02 | Cryptographic Failures | `secure-coding/cryptography` |
| A03 | Injection | `secure-coding/validation`, `penetration/web-vulnerabilities` |
| A04 | Insecure Design | `threat-modeling/stride` |
| A05 | Security Misconfiguration | `appsec/sast`, `devops/containers/security` |
| A06 | Vulnerable Components | `appsec/sca` |
| A07 | Auth Failures | `secure-coding/authentication` |
| A08 | Software & Data Integrity | `appsec/sast`, `devops/cicd` |
| A09 | Logging & Monitoring | `devops/monitoring` |
| A10 | SSRF | `penetration/web-vulnerabilities` |

## Skills Associes

| Skill | Niveau | Relation |
|-------|--------|----------|
| `direction-technique` | STRATEGIE | Recoit les politiques securite |
| `testing-process` | PROCESSUS | Suit la methodologie tests |
| `devops` | IMPLEMENTATION | Integration CI/CD |
| `backend-developer` | IMPLEMENTATION | Patterns securises backend |
| `frontend-developer` | IMPLEMENTATION | Patterns securises frontend |

## Changelog

### v1.0.0
- Creation initiale avec 5 domaines et 24 agents
- Position : NIVEAU 3 IMPLEMENTATION
- Couverture : appsec, secure-coding, threat-modeling, penetration, compliance
