---
name: escalation
description: Points d'escalade vers supervision humaine
---

# Points d'Escalade Humaine

Ce document définit quand et comment escalader vers une supervision humaine.

## Philosophie

> Les skills exécutent, les humains supervisent et décident.

```
CLIENT ←→ HUMAIN (supervision) ←→ SKILLS (exécution)
```

## Matrice d'Escalade par Domaine

### Project Management

| Situation | Raison | Action |
|-----------|--------|--------|
| Brief incomplet après 2 relances | Décision commerciale | Alerter le commercial |
| Estimation hors fourchette | Risque financier | Valider avec la direction |
| Dépassement > 20% budget | Impact financier | Arbitrage nécessaire |
| Conflit ou tension client | Relationnel sensible | Intervention humaine |
| Demande hors périmètre | Avenant potentiel | Négociation commerciale |
| Retard > 1 semaine | Communication client | Chef de projet décide |
| Facture impayée > 60 jours | Recouvrement | Procédure à décider |

### Direction Technique

| Situation | Raison | Action |
|-----------|--------|--------|
| Choix de stack long terme | Décision stratégique | Validation direction technique |
| Architecture complexe/innovante | Risque technique | Review par tech lead |
| Estimation > 50 jours/homme | Engagement important | Validation chef de projet |
| Dette technique critique | Impact maintenance | Arbitrage avec PO/client |
| Faille de sécurité identifiée | Urgence | Escalade immédiate |
| Incident P1 en production | Criticité | War room |
| Données personnelles exposées | RGPD | DPO + légal |
| Migration majeure de stack | Impact équipe | Validation management |

### Web Dev Process

| Situation | Raison | Action |
|-----------|--------|--------|
| Tests échouent en boucle | Blocage technique | Pair programming |
| Code review bloquée | Désaccord technique | Arbitrage tech lead |
| Dépendance vulnérable critique | Sécurité | Décision immédiate |
| Rollback nécessaire | Impact production | Validation avant action |

### WordPress

| Situation | Raison | Action |
|-----------|--------|--------|
| Plugin tiers défaillant | Choix alternatif | Validation fonctionnelle |
| Mise à jour majeure WP | Risque régression | Planification |
| Performance dégradée | Impact utilisateurs | Investigation prioritaire |

### Design System

| Situation | Raison | Action |
|-----------|--------|--------|
| Breaking change | Impact multi-projets | Validation équipes |
| Nouveau pattern | Cohérence système | Review design |
| Accessibilité non-conforme | Légal | Correction prioritaire |

## Niveaux de Criticité

### P1 - Critique (Escalade immédiate)

```
┌─────────────────────────────────────────────────────────────────┐
│ ESCALADE IMMÉDIATE                                               │
├─────────────────────────────────────────────────────────────────┤
│ • Site en production DOWN                                        │
│ • Faille de sécurité exploitable                                │
│ • Données personnelles exposées                                  │
│ • Paiements impossibles                                          │
└─────────────────────────────────────────────────────────────────┘

Action : Interrompre, alerter, war room
```

### P2 - Haute (Escalade < 4h)

```
┌─────────────────────────────────────────────────────────────────┐
│ ESCALADE RAPIDE                                                  │
├─────────────────────────────────────────────────────────────────┤
│ • Fonctionnalité critique dégradée                              │
│ • Client VIP mécontent                                           │
│ • Deadline à risque                                              │
│ • Bug bloquant plusieurs utilisateurs                           │
└─────────────────────────────────────────────────────────────────┘

Action : Notifier responsable, prioriser
```

### P3 - Moyenne (Escalade < 24h)

```
┌─────────────────────────────────────────────────────────────────┐
│ ESCALADE NORMALE                                                 │
├─────────────────────────────────────────────────────────────────┤
│ • Dépassement budget modéré                                      │
│ • Retard non-critique                                            │
│ • Désaccord technique                                            │
│ • Changement de scope demandé                                    │
└─────────────────────────────────────────────────────────────────┘

Action : Ajouter au backlog prioritaire
```

### P4 - Basse (Escalade asynchrone)

```
┌─────────────────────────────────────────────────────────────────┐
│ ESCALADE DIFFÉRÉE                                                │
├─────────────────────────────────────────────────────────────────┤
│ • Amélioration suggérée                                          │
│ • Dette technique non-urgente                                    │
│ • Question stratégique long terme                               │
└─────────────────────────────────────────────────────────────────┘

Action : Documenter pour prochaine rétrospective
```

## Format d'Escalade

```markdown
## Escalade - [P1/P2/P3/P4]

**Contexte** : [Description de la situation]

**Impact** : [Qui/quoi est affecté]

**Options** :
1. [Option A] - Avantages / Inconvénients
2. [Option B] - Avantages / Inconvénients

**Recommandation** : [Option préférée et pourquoi]

**Décision requise avant** : [Date/heure]
```

## Règles d'Escalade

### À Faire

- Escalader AVANT que la situation empire
- Fournir le contexte complet
- Proposer des options (pas juste le problème)
- Indiquer l'urgence clairement
- Documenter la décision prise

### À Éviter

- Escalader sans données factuelles
- Escalader pour des décisions triviales
- Attendre le dernier moment
- Escalader au mauvais niveau hiérarchique
- Oublier de clôturer l'escalade

## Références

- [Règles de routage](./routing.md)
- [Composition des skills](./composition.md)
