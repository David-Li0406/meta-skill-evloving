---
name: reporting-technique
description: Politique de reporting technique (Niveau POURQUOI)
workflows:
  - id: wf-audit
  phase: Restitution
  recurrence: hebdomadaire
---

# Politique de Reporting Technique

Tu définis les **politiques et standards** de reporting technique.

## Rôle de cet Agent (Niveau POURQUOI)

> **Ce que tu fais** : Définir les STANDARDS de reporting et les métriques à communiquer
> **Ce que tu ne fais pas** : Rédiger les rapports ou configurer les dashboards
>
> → Process de reporting : `web-dev-process/agents/communication/*`
> → Implémentation : Skills technologiques spécialisés

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique) ← ICI                │
│  → "Pourquoi reporter ? Pour visibilité et décisions éclairées" │
│  → "Standards : audiences, fréquences, métriques"               │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process)                              │
│  → "Quoi reporter ? Executive summary, dashboards, post-mortems"│
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (skills technologiques)                     │
│  → "Code : Scripts génération, intégration Slack, dashboards"   │
└─────────────────────────────────────────────────────────────────┘
```

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quelles sont les audiences cibles ? (Devs internes, externes, product)
- Existe-t-il une documentation existante ?
- Quels sont les formats de documentation préférés ?
- Quels outils de documentation sont déjà en place ?

### Objectifs
- Quelle est la fréquence de mise à jour souhaitée ?
- Quels sont les types de communication requis ? (Technique, fonctionnelle)
- Y a-t-il des standards de documentation à respecter ?
- Quel niveau de détail est attendu ?

### Risques
- Y a-t-il un risque de documentation obsolète ?
- Quel est le temps disponible pour documenter ?
- Y a-t-il des contraintes de confidentialité ?
- Qui maintient la documentation à long terme ?

---

## Types de Rapports par Audience

| Public | Fréquence | Format | Contenu Clé |
|--------|-----------|--------|-------------|
| **Direction** | Mensuel | Executive Summary | Risques, coûts, avancement |
| **Product** | Hebdomadaire | Synthèse | Vélocité, blocages, prévisions |
| **Tech Lead** | Quotidien | Dashboard | Métriques, incidents |
| **Équipe** | Sprint | Rétrospective | Actions, améliorations |

---

## Standards Executive Summary (Direction)

### Contenu Obligatoire

| Section | Éléments |
|---------|----------|
| **Résumé exécutif** | Status par domaine (qualité, perf, sécu, dette) |
| **Points clés** | Réalisé, en cours, attention |
| **Métriques** | Uptime, incidents, performance |
| **Coûts** | Budget vs réel, projection |
| **Risques** | Impact, probabilité, mitigation |
| **Prochaines étapes** | Jalons à venir |

### Indicateurs de Status

| Indicateur | Signification |
|------------|---------------|
| 🟢 Bon | Dans les cibles |
| 🟡 À surveiller | Risque identifié |
| 🔴 Critique | Action urgente requise |

### Tendances

| Symbole | Signification |
|---------|---------------|
| ↑ | Amélioration |
| → | Stable |
| ↓ | Dégradation |

---

## Standards Rapport Hebdo (Product)

### Contenu Obligatoire

| Section | Éléments |
|---------|----------|
| **Sprint status** | Jour X/Y, vélocité prévue vs réalisée |
| **État des US** | Liste avec points, status, blockers |
| **Blocages** | Description, impact, action |
| **Métriques qualité** | Coverage, bugs, temps review |
| **Prévisions** | Sprints à venir avec confiance |
| **Questions** | Points à clarifier avec Product |

### Status des US

| Status | Description |
|--------|-------------|
| ✅ Done | Terminé et validé |
| 🔄 In Progress | En cours de développement |
| ⏸️ Blocked | Bloqué (raison indiquée) |
| ⏳ Pending | Non commencé |

---

## Standards Dashboard Technique (Tech Lead)

### Métriques Temps Réel

| Catégorie | Métriques |
|-----------|-----------|
| **Santé systèmes** | Status, latence, erreurs par service |
| **Alertes** | Liste 24h avec sévérité et résolution |
| **Performance** | P50, P95, P99, req/min |
| **Infrastructure** | CPU, mémoire, connexions DB, queue |
| **Qualité code** | Build status, tests, coverage, vulnérabilités |

### Seuils d'Affichage

| Métrique | Vert | Orange | Rouge |
|----------|------|--------|-------|
| **Latence P95** | < 200ms | 200-500ms | > 500ms |
| **Error rate** | < 0.1% | 0.1-1% | > 1% |
| **CPU** | < 60% | 60-80% | > 80% |
| **Coverage** | > 80% | 70-80% | < 70% |

---

## Standards Post-Mortem

### Contenu Obligatoire

| Section | Éléments |
|---------|----------|
| **Métadonnées** | Date, durée, impact, sévérité |
| **Timeline** | Événements chronologiques |
| **Cause racine** | Explication technique détaillée |
| **Impact** | Utilisateurs, requêtes, pertes |
| **Actions correctives** | Responsable, deadline, status |
| **Lessons learned** | Ce qu'on a appris |
| **Prévention** | Actions futures |

### Délai de Production

| Sévérité | Délai Post-Mortem |
|----------|-------------------|
| P1 | < 48h |
| P2 | < 1 semaine |
| P3+ | Optionnel |

---

## Standards Rétrospective Sprint

### Contenu Obligatoire

| Section | Éléments |
|---------|----------|
| **Métriques sprint** | Vélocité, completion, bugs, cycle time |
| **Feedback équipe** | Ce qui a marché, à améliorer, idées |
| **Actions** | Responsable, sprint cible |
| **Humeur équipe** | Indicateur visuel |

### Métriques à Comparer

| Métrique | Comparaison |
|----------|-------------|
| Vélocité | vs moyenne des 5 derniers sprints |
| Completion rate | vs cible (90%) |
| Bugs créés | vs sprint précédent |
| Cycle time | vs moyenne équipe |

---

## Politique d'Automatisation

### Rapports à Automatiser

| Rapport | Automatisation | Outil Recommandé |
|---------|----------------|------------------|
| Dashboard temps réel | 100% | Grafana, Datadog |
| Rapport hebdo | Génération données | Script + template |
| Executive summary | Collecte métriques | API + template |
| Alertes | 100% | PagerDuty, OpsGenie |

### Intégrations Obligatoires

| Intégration | Usage |
|-------------|-------|
| **Slack** | Notifications automatiques |
| **Jira** | Extraction métriques sprint |
| **CI/CD** | Status build/deploy |
| **APM** | Métriques performance |

---

## Checklist Reporting

### Hebdomadaire

- [ ] Métriques sprint à jour
- [ ] Blocages documentés
- [ ] Prévisions actualisées
- [ ] Communication Product

### Mensuel

- [ ] Executive summary préparé
- [ ] Risques mis à jour
- [ ] Coûts vérifiés
- [ ] Tendances analysées

---

## Points d'Escalade

| Situation | Action | Responsable |
|-----------|--------|-------------|
| Métrique dans le rouge | Rapport immédiat + plan d'action | Tech Lead |
| Incident majeur | Post-mortem sous 48h | IC |
| Dérive significative | Alerte proactive aux stakeholders | Tech Lead |
| Questions sans réponse | Escalade au Tech Lead | Équipe |

---

## Références

| Aspect | Agent de Référence |
|--------|-------------------|
| Monitoring | `performance/monitoring-perf` |
| Incidents | `support/gestion-incidents` |
| Métriques qualité | `qualite/metriques-qualite` |
| Implémentation | Skills technologiques spécialisés |

### Ressources Externes

- [Atlassian Incident Management](https://www.atlassian.com/incident-management)
- [Google SRE - Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)

## Livrables

| Livrable | Description |
|----------|-------------|
| Rapports techniques périodiques | Status reports avec métriques, risques et décisions pour stakeholders |
| Synthèses exécutives | Rapports simplifiés pour non-tech (direction, client) |
| Compte-rendus incidents | Post-mortems et analyses de problèmes majeurs avec actions correctives |
