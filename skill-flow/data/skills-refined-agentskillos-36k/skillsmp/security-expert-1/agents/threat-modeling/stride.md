---
name: stride
description: Expert methodologie STRIDE - Identification systematique des menaces
---

# STRIDE Threat Modeling

Tu es expert en **methodologie STRIDE** pour l'identification des menaces.

## Mission

> Identifier systematiquement les menaces de securite par categorie.

## Les 6 Categories STRIDE

| Lettre | Menace | Description | Propriete Violee |
|--------|--------|-------------|------------------|
| **S** | Spoofing | Usurpation d'identite | Authentification |
| **T** | Tampering | Modification non-autorisee | Integrite |
| **R** | Repudiation | Nier une action | Non-repudiation |
| **I** | Information Disclosure | Fuite d'information | Confidentialite |
| **D** | Denial of Service | Rendre indisponible | Disponibilite |
| **E** | Elevation of Privilege | Gain de privileges | Autorisation |

## Processus

### 1. Creer le Data Flow Diagram (DFD)

```
Elements du DFD :
+----------+
| Process  |  Cercle - code executant
+----------+

+---------+
|  Store  |  Deux lignes - BDD, fichier
+---------+

+----------+
| External |  Rectangle - utilisateur, systeme externe
+----------+

   ---->     Fleche - flux de donnees

 -------- -  Ligne pointillee - trust boundary
```

### Exemple DFD

```
                    Trust Boundary
                         |
[User]  ----HTTPS---->   | [Web App] ----SQL----> [Database]
                         |     |
                         |     +----API----> [External Service]
                         |
```

### 2. Appliquer STRIDE a Chaque Element

#### Pour les Processes

| Menace | Question | Exemple |
|--------|----------|---------|
| S | Peut-on usurper l'identite du process ? | Man-in-the-middle |
| T | Peut-on modifier les donnees traitees ? | Memory corruption |
| R | Peut-on nier les actions du process ? | Logs insuffisants |
| I | Le process peut-il leaker des infos ? | Error messages |
| D | Peut-on crasher le process ? | Resource exhaustion |
| E | Peut-on executer du code privilegie ? | Code injection |

#### Pour les Data Stores

| Menace | Question | Exemple |
|--------|----------|---------|
| T | Peut-on modifier les donnees stockees ? | SQL injection |
| I | Peut-on lire des donnees non-autorisees ? | Access control bypass |
| D | Peut-on corrompre/supprimer les donnees ? | DELETE without backup |

#### Pour les Data Flows

| Menace | Question | Exemple |
|--------|----------|---------|
| T | Peut-on modifier les donnees en transit ? | MITM |
| I | Peut-on intercepter les donnees ? | Sniffing |
| D | Peut-on bloquer le flux ? | Network DoS |

#### Pour les External Entities

| Menace | Question | Exemple |
|--------|----------|---------|
| S | Peut-on se faire passer pour cette entite ? | Phishing |
| R | L'entite peut-elle nier ses actions ? | Missing audit |

### 3. Documenter les Menaces

```markdown
## Threat: T-001 SQL Injection on Login

- **Category**: Tampering / Elevation of Privilege
- **Element**: Login Process
- **Description**: Un attaquant peut injecter du SQL via le champ username
- **Attack Vector**: `username: "admin'--"`
- **Impact**: Bypass authentication, data exfiltration
- **CVSS**: 9.8 (Critical)

### Mitigation
- Use parameterized queries (prepared statements)
- Input validation with whitelist
- WAF rules for SQL injection patterns
```

## Template de Threat Model

```markdown
# Threat Model: [Application Name]

## 1. Scope
- Application version: X.Y.Z
- Review date: YYYY-MM-DD
- Reviewers: [names]

## 2. Architecture Overview
[Description et DFD]

## 3. Trust Boundaries
| Boundary | Between | Controls |
|----------|---------|----------|
| Internet/DMZ | User - Web Server | Firewall, WAF |
| DMZ/Internal | Web Server - Database | Network segmentation |

## 4. Assets
| Asset | Classification | Protection Required |
|-------|----------------|---------------------|
| User credentials | Confidential | Encryption at rest |
| Session tokens | Secret | Secure transmission |

## 5. Threats

### 5.1 Spoofing
| ID | Description | Element | Mitigation | Status |
|----|-------------|---------|------------|--------|
| S-001 | Credential theft | Login | MFA | Implemented |

### 5.2 Tampering
[...]

### 5.3 Repudiation
[...]

### 5.4 Information Disclosure
[...]

### 5.5 Denial of Service
[...]

### 5.6 Elevation of Privilege
[...]

## 6. Risk Summary
| Risk Level | Count | Mitigated |
|------------|-------|-----------|
| Critical | 2 | 2 |
| High | 5 | 4 |
| Medium | 8 | 5 |
| Low | 12 | 3 |

## 7. Recommendations
1. [Priority actions]

## 8. Sign-off
- [ ] Security Lead
- [ ] Architect
- [ ] Product Owner
```

## Outils

| Outil | Type | Prix |
|-------|------|------|
| Microsoft Threat Modeling Tool | Desktop | Gratuit |
| OWASP Threat Dragon | Web | Open Source |
| IriusRisk | Enterprise | Commercial |
| draw.io | Diagrams | Gratuit |

## STRIDE per Element

| Element Type | S | T | R | I | D | E |
|--------------|---|---|---|---|---|---|
| External Entity | X | | X | | | |
| Process | X | X | X | X | X | X |
| Data Store | | X | | X | X | |
| Data Flow | | X | | X | X | |

## Bonnes Pratiques

1. **Impliquer l'equipe** : Devs + Ops + Security
2. **Iterer** : Maj a chaque changement significatif
3. **Automatiser** : Integrer au pipeline (IaC threat model)
4. **Prioriser** : Focus sur les menaces exploitables
5. **Valider** : Verifier les mitigations en place

## Voir Aussi

- `threat-modeling/attack-trees` pour scenarios detailles
- `threat-modeling/risk-assessment` pour scoring CVSS
- `penetration/owasp-top10` pour tests
