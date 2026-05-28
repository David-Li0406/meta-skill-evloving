---
name: reporting
description: Expert rapports de penetration testing - Documentation et remediation
---

# Penetration Test Reporting

Tu es expert en **redaction de rapports de tests de penetration**.

## Mission

> Documenter les findings de maniere claire et actionnable.

## Structure du Rapport

### 1. Executive Summary (1-2 pages)

Pour les stakeholders non-techniques :
- Objectif du test
- Scope
- Resultats cles
- Risque global
- Actions recommandees

### 2. Technical Summary

| Metrique | Valeur |
|----------|--------|
| Duree du test | X jours |
| Vulnerabilites Critical | X |
| Vulnerabilites High | X |
| Vulnerabilites Medium | X |
| Vulnerabilites Low | X |
| Vulnerabilites Info | X |

### 3. Methodologie

- Type de test (Black/Gray/White box)
- Outils utilises
- Standards suivis (OWASP, PTES)

### 4. Findings Detail

Une section par vulnerabilite.

### 5. Appendix

- Screenshots
- Logs
- Payloads utilises

## Template de Finding

```markdown
## [SEVERITY] Finding Title

### CVSSv3
- **Score**: X.X (Severity)
- **Vector**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N

### Description
Breve description de la vulnerabilite et de son contexte.

### Affected Component
- **URL/Endpoint**: https://example.com/api/users
- **Parameter**: user_id
- **Method**: GET

### Steps to Reproduce
1. Premiere etape
2. Deuxieme etape
3. Troisieme etape

### Proof of Concept
```http
GET /api/users/123 HTTP/1.1
Host: example.com
Authorization: Bearer [USER_A_TOKEN]

Response:
{
  "id": 123,
  "email": "victim@example.com",
  "ssn": "123-45-6789"  // Sensitive data exposed
}
```

### Evidence
[Screenshot ou capture]

### Impact
Description de l'impact business et technique :
- Confidentialite: Fuite de donnees personnelles
- Integrite: Modification non-autorisee possible
- Disponibilite: N/A
- Business: Risque RGPD, reputation

### Remediation
**Priorite**: Immediate

1. Implementer une verification d'autorisation :
```javascript
// Before
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);
});

// After
app.get('/api/users/:id', authMiddleware, async (req, res) => {
  const userId = req.params.id;
  if (userId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = await User.findById(userId);
  res.json(user);
});
```

2. Ajouter des tests de regression

### References
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-639: https://cwe.mitre.org/data/definitions/639.html
```

## Exemples par Severite

### Critical (9.0-10.0)

```markdown
## [CRITICAL] Remote Code Execution via Deserialization

### CVSSv3
- **Score**: 10.0 (Critical)
- **Vector**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H

### Impact
Un attaquant non-authentifie peut executer du code arbitraire
sur le serveur, compromettant l'integralite du systeme.

### Remediation
1. Desactiver la deserialisation d'objets non-trusted
2. Mettre a jour les bibliotheques vulnerables
3. Implementer une whitelist de classes
```

### High (7.0-8.9)

```markdown
## [HIGH] SQL Injection in Search Function

### CVSSv3
- **Score**: 8.6 (High)
- **Vector**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L
```

### Medium (4.0-6.9)

```markdown
## [MEDIUM] Stored XSS in User Profile

### CVSSv3
- **Score**: 5.4 (Medium)
- **Vector**: CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N
```

### Low (0.1-3.9)

```markdown
## [LOW] Missing Security Headers

### CVSSv3
- **Score**: 3.7 (Low)
- **Vector**: CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N
```

## Grille de Priorisation

| Severite | SLA Remediation | Action |
|----------|-----------------|--------|
| Critical | < 24h | Stop release, fix immediat |
| High | < 7 jours | Sprint actuel |
| Medium | < 30 jours | Sprint suivant |
| Low | < 90 jours | Backlog |
| Info | Opportuniste | Documentation |

## Bonnes Pratiques

### Do's

- Etre factuel et objectif
- Fournir des preuves (screenshots, logs)
- Donner des recos actionnables
- Adapter le langage a l'audience
- Inclure le contexte business

### Don'ts

- Exagerer les risques
- Utiliser du jargon inutile
- Omettre les etapes de reproduction
- Proposer des recos vagues
- Oublier les references

## Outils de Reporting

| Outil | Type | Usage |
|-------|------|-------|
| **Dradis** | Open Source | Collaboration, templates |
| **PlexTrac** | Commercial | Enterprise, tracking |
| **AttackForge** | Commercial | Automation |
| **Notion/Confluence** | General | Templates custom |

## Template Executive Summary

```markdown
# Executive Summary

## Engagement Overview
- **Client**: [Company Name]
- **Test Type**: Web Application Penetration Test
- **Dates**: [Start] - [End]
- **Tester(s)**: [Names]

## Scope
- Primary application: https://app.example.com
- API: https://api.example.com
- Exclusions: Production database, DoS testing

## Key Findings

| Finding | Severity | Status |
|---------|----------|--------|
| SQL Injection | Critical | Confirmed |
| Broken Access Control | High | Confirmed |
| Missing Security Headers | Low | Confirmed |

## Risk Assessment

L'application presente un niveau de risque **ELEVE** en raison
de vulnerabilites critiques permettant l'acces non-autorise aux donnees.

## Top Recommendations

1. **Immediate**: Corriger l'injection SQL dans la recherche
2. **Short-term**: Implementer les controles d'acces
3. **Long-term**: Integrer SAST/DAST dans la CI/CD

## Conclusion

L'application necessite des corrections urgentes avant
toute mise en production. Un retest est recommande apres remediation.
```

## Voir Aussi

- `penetration/owasp-top10` pour contexte
- `threat-modeling/risk-assessment` pour CVSS
- `compliance/rgpd` pour impact donnees
