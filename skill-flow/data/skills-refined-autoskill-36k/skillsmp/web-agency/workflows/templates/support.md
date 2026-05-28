---
id: wf-support
name: Workflow Support
type: template
version: 1.1.0
description: Workflow pour le traitement des tickets et incidents
duration_range: "1h-5 jours"
phases: 4
applicable_to:
  - ticket-support
  - incident
  - demande-information
  - bug-report
  - reclamation
references:
  - acceptance/matrice-positionnement.md
  - acceptance/livrables-par-workflow.md
  - acceptance/criteres-acceptation.md
---

# Workflow Support

> Template pour le traitement des demandes de support et incidents.

## Vue d'Ensemble

```
RECEPTION → DIAGNOSTIC → RESOLUTION → CLOTURE
```

| Phase | Durée | Validation |
|-------|-------|------------|
| Réception | 5-10% | Ticket qualifié |
| Diagnostic | 20-30% | Cause identifiée |
| Résolution | 40-50% | Problème résolu |
| Clôture | 10-20% | Client satisfait |

---

## Phase 1: Réception

### Objectif
Qualifier et prioriser la demande entrante.

### Activités
1. Réception du ticket (email, tel, chat)
2. Création/enrichissement du ticket
3. Qualification (type, urgence, impact)
4. Assignation au bon interlocuteur

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Ticket créé** | Ticket dans l'outil avec informations complètes | Tous |
| **Accusé réception** | Client informé de la prise en charge | Tous |
| **Catégorisation** | Type, priorité et catégorie assignés | Tous |
| **Assignation** | Responsable identifié selon compétences | Tous |

```yaml
livrables_reception:
  ticket_cree:
    criteres:
      - CA-REC-001: "Ticket créé dans l'outil de suivi"
      - CA-REC-002: "Description du problème complète"
      - CA-REC-003: "Informations client renseignées"
      - CA-REC-004: "Environnement précisé (navigateur, OS, URL)"
      - CA-REC-005: "Étapes de reproduction si bug"
    preuve: "Ticket dans l'outil"

  accuse_reception:
    criteres:
      - CA-REC-010: "Accusé envoyé dans les délais SLA"
      - CA-REC-011: "Numéro de ticket communiqué"
      - CA-REC-012: "Délai de réponse estimé indiqué"
      - CA-REC-013: "Canal de suivi précisé"
    preuve: "Email/notification AR"

  categorisation:
    criteres:
      - CA-REC-020: "Type de demande identifié (bug, question, demande)"
      - CA-REC-021: "Priorité assignée selon matrice (P1-P4)"
      - CA-REC-022: "Catégorie fonctionnelle attribuée"
      - CA-REC-023: "Impact utilisateurs évalué"
    preuve: "Champs ticket renseignés"

  assignation:
    criteres:
      - CA-REC-030: "Responsable assigné selon compétences"
      - CA-REC-031: "Niveau de support approprié (N1/N2/N3)"
      - CA-REC-032: "Responsable notifié"
    preuve: "Assignation dans ticket"
```

### SLA par Priorité

| Priorité | Description | Réponse | Résolution |
|----------|-------------|---------|------------|
| P1 | Critique (site down) | 15 min | 4h |
| P2 | Majeur (fonction KO) | 1h | 8h |
| P3 | Modéré (dégradé) | 4h | 48h |
| P4 | Mineur (cosmétique) | 24h | 5 jours |

### Critères de Sortie
- Ticket qualifié et priorisé
- Client informé
- Responsable assigné

---

## Phase 2: Diagnostic

### Objectif
Identifier la cause du problème.

### Activités
1. Reproduction du problème
2. Analyse des logs/données
3. Identification de la cause racine
4. Évaluation des options de résolution

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Analyse cause** | Cause racine identifiée et documentée | Tous |
| **Estimation résolution** | Temps et effort estimés | Tous |
| **Escalade** | Escalade effectuée si nécessaire | Tous |
| **Communication** | Client informé de l'avancement | Tous |

```yaml
livrables_diagnostic:
  analyse_cause:
    criteres:
      - CA-DIAG-001: "Problème reproduit (ou non-reproductible documenté)"
      - CA-DIAG-002: "Logs et traces analysés"
      - CA-DIAG-003: "Cause racine identifiée"
      - CA-DIAG-004: "Périmètre d'impact évalué"
    preuve: "Notes diagnostic dans ticket"

  estimation_resolution:
    criteres:
      - CA-DIAG-010: "Temps de résolution estimé"
      - CA-DIAG-011: "Complexité évaluée (simple/complexe)"
      - CA-DIAG-012: "Ressources nécessaires identifiées"
      - CA-DIAG-013: "Options de résolution listées si multiples"
    preuve: "Estimation dans ticket"

  escalade:
    criteres:
      - CA-DIAG-020: "Critères d'escalade évalués"
      - CA-DIAG-021: "Escalade effectuée si temps diagnostic > 30min"
      - CA-DIAG-022: "Niveau approprié sollicité (N2/N3/N4)"
      - CA-DIAG-023: "Contexte complet transmis"
    preuve: "Historique escalade"

  communication_client:
    criteres:
      - CA-DIAG-030: "Client informé de l'avancement"
      - CA-DIAG-031: "Cause expliquée en termes compréhensibles"
      - CA-DIAG-032: "Délai résolution communiqué"
      - CA-DIAG-033: "Alternatives proposées si délai long"
    preuve: "Communication client"
```

### Critères de Sortie
- Cause racine identifiée
- Solution viable trouvée
- Client informé

---

## Phase 3: Résolution

### Objectif
Résoudre le problème et restaurer le service.

### Activités
1. Application de la solution
2. Tests de vérification
3. Déploiement si nécessaire
4. Validation avec le demandeur

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Correction appliquée** | Fix déployé et vérifié | Tous |
| **Communication** | Client informé de la résolution | Tous |
| **Documentation KB** | Solution documentée si récurrent | Si applicable |
| **Tests** | Non-régression vérifiée | Tous |

```yaml
livrables_resolution:
  correction_appliquee:
    criteres:
      - CA-RES-001: "Solution implémentée"
      - CA-RES-002: "Tests de vérification passés"
      - CA-RES-003: "Déploiement effectué si nécessaire"
      - CA-RES-004: "Fonctionnalité restaurée"
    preuve: "Ticket mis à jour + déploiement"

  communication_resolution:
    criteres:
      - CA-RES-010: "Client notifié de la résolution"
      - CA-RES-011: "Solution expliquée"
      - CA-RES-012: "Actions client requises précisées si applicable"
      - CA-RES-013: "Demande de validation envoyée"
    preuve: "Email/notification résolution"

  documentation_kb:
    criteres:
      - CA-RES-020: "Problème documenté si récurrent (> 2 occurrences)"
      - CA-RES-021: "Solution détaillée étape par étape"
      - CA-RES-022: "Mots-clés pour recherche ajoutés"
      - CA-RES-023: "Catégorie KB appropriée"
    preuve: "Article KB créé/mis à jour"

  tests_validation:
    criteres:
      - CA-RES-030: "Scénario initial rejoué avec succès"
      - CA-RES-031: "Pas de régression introduite"
      - CA-RES-032: "Performance maintenue"
      - CA-RES-033: "Validation par demandeur obtenue"
    preuve: "Confirmation tests + validation"
```

### Critères de Sortie
- Problème résolu
- Service restauré
- Demandeur confirme

---

## Phase 4: Clôture

### Objectif
Clôturer proprement et capitaliser.

### Activités
1. Confirmation de résolution avec client
2. Enquête de satisfaction
3. Documentation de la solution (KB)
4. Analyse post-mortem si P1/P2
5. Clôture du ticket

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Ticket fermé** | Statut clôturé avec résolution documentée | Tous |
| **Enquête satisfaction** | Feedback client collecté | Tous |
| **Analyse récurrence** | Patterns identifiés si applicable | Si récurrent |
| **Post-mortem** | Analyse si incident majeur | P1/P2 uniquement |

```yaml
livrables_cloture:
  ticket_ferme:
    criteres:
      - CA-CLO-001: "Statut ticket = Fermé/Résolu"
      - CA-CLO-002: "Résolution documentée dans le ticket"
      - CA-CLO-003: "Temps passé renseigné"
      - CA-CLO-004: "Catégorie de résolution précisée"
    preuve: "Ticket clôturé"

  enquete_satisfaction:
    criteres:
      - CA-CLO-010: "Enquête CSAT envoyée"
      - CA-CLO-011: "Score collecté si réponse"
      - CA-CLO-012: "Commentaires analysés"
      - CA-CLO-013: "Actions correctives si insatisfaction"
    preuve: "Résultat enquête"

  analyse_recurrence:
    criteres:
      - CA-CLO-020: "Tickets similaires identifiés"
      - CA-CLO-021: "Pattern récurrence documenté si > 3 occurrences"
      - CA-CLO-022: "Cause racine systémique identifiée"
      - CA-CLO-023: "Action corrective proposée"
    preuve: "Rapport récurrence"

  postmortem:
    criteres:
      - CA-CLO-030: "Timeline incident documentée"
      - CA-CLO-031: "Cause racine analysée"
      - CA-CLO-032: "Impact quantifié (durée, utilisateurs)"
      - CA-CLO-033: "Actions correctives avec responsables"
      - CA-CLO-034: "Enseignements partagés avec équipe"
    preuve: "Document post-mortem"
```

### Critères de Sortie
- Ticket fermé
- Client satisfait
- Connaissance capitalisée
- Actions correctives planifiées si nécessaire

---

## Escalade

### Niveaux d'Escalade

| Niveau | Interlocuteur | Quand |
|--------|---------------|-------|
| N1 | Support front | Demandes simples |
| N2 | Support technique | Problèmes techniques |
| N3 | Développeur | Bugs, évolutions |
| N4 | Lead/Architecte | Incidents critiques |

### Critères d'Escalade

Escalader si:
- Temps de diagnostic > 30 min sans avancée
- Compétence requise non disponible
- Client VIP ou contrat spécifique
- Impact business significatif

---

## Gestion des Incidents

### Incident Majeur (P1/P2)

```
ALERTE → MOBILISATION → RESOLUTION → POSTMORTEM
```

1. **Alerte**: Notification immédiate des stakeholders
2. **Mobilisation**: War room, toutes ressources
3. **Résolution**: Focus unique sur restauration
4. **Postmortem**: Analyse à froid dans les 48h

### Template Postmortem

```markdown
## Incident: [Titre]

**Date**: [Date et heure]
**Durée**: [Temps d'indisponibilité]
**Impact**: [Utilisateurs affectés, perte business]

### Timeline
- HH:MM - Événement 1
- HH:MM - Événement 2

### Cause Racine
[Analyse de la cause]

### Actions Correctives
- [ ] Action 1 (responsable, deadline)
- [ ] Action 2 (responsable, deadline)

### Enseignements
[Ce qu'on a appris]
```

---

## Métriques

| Métrique | Description | Cible |
|----------|-------------|-------|
| MTTR | Mean Time To Resolve | < 4h (P1) |
| First Response | Temps avant 1ère réponse | < SLA |
| Resolution Rate | % tickets résolus | > 95% |
| CSAT | Satisfaction client | > 4/5 |
| Reopening Rate | % tickets réouverts | < 5% |
