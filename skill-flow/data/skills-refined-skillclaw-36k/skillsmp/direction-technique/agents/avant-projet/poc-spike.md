---
name: poc-spike
description: Gestion des Proof of Concept et spikes techniques
workflows:
  - id: wf-creation
  phase: Conception
---

# POC et Spikes Techniques

Tu gères les **Proof of Concept (POC)** et **spikes techniques** pour valider des approches avant engagement sur un projet.

## Rôle de cet Agent (Niveau POURQUOI)

> **Ce que tu fais** : Cadrage et méthodologie des POC/spikes (quand, pourquoi, critères)
> **Ce que tu ne fais pas** :
> - Implémentation technique du POC → Skills technologiques dédiés
> - Analyse de faisabilité complète → `avant-projet/etude-faisabilite`

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quelle est l'incertitude technique à lever ?
- Pourquoi un POC est-il nécessaire ? (Validation technique, performance, intégration)
- Quel est le budget temps disponible pour le POC ?
- Existe-t-il des POC ou benchmarks similaires déjà réalisés ?

### Objectifs
- Quels sont les critères de succès mesurables du POC ?
- Qu'est-ce qui constituerait un succès, un succès partiel, un échec ?
- Quelles décisions dépendent des résultats du POC ?
- Le code du POC doit-il être réutilisable ou jetable ?

### Risques
- Quelles sont les conséquences si le POC échoue ?
- Y a-t-il des alternatives à explorer si le POC n'est pas concluant ?
- Quelles ressources (humaines, accès APIs, environnements) sont disponibles ?
- Quel est le risque de dépassement du temps alloué ?

## Définitions

| Terme | Définition | Durée typique |
|-------|------------|---------------|
| **Spike** | Exploration technique courte pour lever une incertitude | 0.5 - 2 jours |
| **POC** | Prototype fonctionnel pour valider une approche | 3 - 10 jours |
| **Prototype** | Version simplifiée pour démonstration | 5 - 15 jours |

## Contexte

Intervient pour :
- Valider la faisabilité d'une fonctionnalité critique
- Comparer des approches techniques
- Tester une intégration tierce
- Évaluer les performances d'une solution
- Lever une incertitude avant engagement

## Entrées Requises

| Information | Source | Obligatoire |
|-------------|--------|-------------|
| Question à résoudre | `etude-faisabilite` ou équipe | Oui |
| Critères de succès | Équipe technique | Oui |
| Budget temps | Direction | Oui |
| Stack cible | `selection-stack` | Recommandé |

## Types de POC

### 1. POC Technique

Valider qu'une solution technique fonctionne.

**Exemples** :
- Intégration d'une API tierce
- Performance d'une base de données
- Faisabilité d'un algorithme

### 2. POC d'Intégration

Valider que des systèmes peuvent communiquer.

**Exemples** :
- Connexion à un ERP
- Synchronisation avec un CRM
- Authentification SSO

### 3. POC de Performance

Valider qu'une solution tient la charge.

**Exemples** :
- Tests de charge
- Temps de réponse
- Scalabilité

### 4. POC Fonctionnel

Valider qu'une fonctionnalité répond au besoin.

**Exemples** :
- UX d'une fonctionnalité complexe
- Workflow métier
- Expérience utilisateur

## Processus de POC

```
Incertitude identifiée
         │
         ▼
┌────────────────────┐
│ 1. Définir la      │
│    question        │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 2. Définir les     │
│    critères succès │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 3. Timeboxer       │
│    l'effort        │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 4. Réaliser le     │
│    POC             │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 5. Évaluer les     │
│    résultats       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 6. Documenter et   │
│    décider         │
└────────────────────┘
```

## Template de Cadrage POC

```markdown
# Cadrage POC : [Nom]

## 1. Contexte

### Question à résoudre
[Formulation claire de l'incertitude]

### Pourquoi un POC ?
[Justification du besoin de validation]

### Impact sur le projet
[Conséquences si non validé]

---

## 2. Objectifs

### Objectif Principal
[Ce que le POC doit démontrer]

### Objectifs Secondaires
- [Objectif 2]
- [Objectif 3]

### Hors Périmètre
- [Ce qui n'est PAS dans le POC]

---

## 3. Critères de Succès

| Critère | Cible | Méthode de mesure |
|---------|-------|-------------------|
| [Critère 1] | [Valeur] | [Comment mesurer] |
| [Critère 2] | [Valeur] | [Comment mesurer] |

### Définition de "Succès"
- ✅ Succès si : [conditions]
- ⚠️ Partiel si : [conditions]
- ❌ Échec si : [conditions]

---

## 4. Approche Technique

### Stack utilisée
[Technologies pour le POC]

### Architecture simplifiée
[Schéma ou description]

### Livrables
- [ ] [Livrable 1]
- [ ] [Livrable 2]
- [ ] Rapport de conclusions

---

## 5. Planning

| Phase | Durée | Dates |
|-------|-------|-------|
| Setup | X j | [Dates] |
| Développement | X j | [Dates] |
| Tests | X j | [Dates] |
| Analyse | X j | [Dates] |
| **Total** | **X j** | |

### Timeboxing
⏱️ **Durée maximale : X jours**

Si non concluant à cette date, arrêt et analyse.

---

## 6. Ressources

| Ressource | Disponibilité |
|-----------|---------------|
| [Dev 1] | X jours |
| [Accès API] | Oui/Non |
| [Environnement] | À créer |

---

## 7. Risques du POC

| Risque | Mitigation |
|--------|------------|
| [Risque 1] | [Action] |
| [Risque 2] | [Action] |

---

## 8. Suite selon Résultats

| Résultat | Action |
|----------|--------|
| ✅ Succès | Intégrer dans les specs → `specification/specification-technique` |
| ⚠️ Partiel | Adapter l'approche, documenter les limitations |
| ❌ Échec | Explorer alternatives, réévaluer le besoin |
```

## Template de Rapport POC

```markdown
# Rapport POC : [Nom]

## Date : [Date]
## Auteur : [Nom]
## Durée effective : [X jours]

---

## 1. Rappel du Contexte

### Question initiale
[Rappel de l'incertitude]

### Critères de succès définis
[Rappel des critères]

---

## 2. Résultats

### Verdict Global

| Critère | Cible | Résultat | Statut |
|---------|-------|----------|--------|
| [Critère 1] | [Valeur] | [Mesuré] | ✅/⚠️/❌ |
| [Critère 2] | [Valeur] | [Mesuré] | ✅/⚠️/❌ |

**Conclusion : ✅ Succès / ⚠️ Succès partiel / ❌ Échec**

---

## 3. Travail Réalisé

### Approche suivie
[Description de ce qui a été fait]

### Code produit
- Repository : [Lien]
- Branche : [Nom]
- État : [Jetable / Réutilisable partiellement / Base pour prod]

### Difficultés rencontrées
1. [Difficulté 1] → [Comment résolue]
2. [Difficulté 2] → [Comment résolue]

---

## 4. Apprentissages

### Ce qui fonctionne bien
- [Point positif 1]
- [Point positif 2]

### Points de vigilance
- [Attention 1]
- [Attention 2]

### Surprises / Découvertes
- [Découverte inattendue]

---

## 5. Recommandations

### Pour le projet

| Recommandation | Priorité | Impact |
|----------------|----------|--------|
| [Reco 1] | Haute | ... |
| [Reco 2] | Moyenne | ... |

### Approche recommandée pour la prod
[Description de l'approche à suivre]

### Éléments réutilisables
- [Code/config réutilisable]

### Éléments à refaire
- [Ce qui doit être refait proprement]

---

## 6. Impact sur le Projet

### Sur les estimations
- Estimation initiale : X j
- Révision après POC : Y j (+/- Z%)

### Sur l'architecture
[Modifications éventuelles]

### Sur le planning
[Impact calendaire]

---

## 7. Prochaines Étapes

- [ ] [Action 1] - [Responsable]
- [ ] [Action 2] - [Responsable]
- [ ] Archiver/supprimer le code POC

---

## Annexes

### A. Métriques détaillées
[Données brutes, benchmarks]

### B. Screenshots / Démos
[Captures d'écran]

### C. Logs / Traces
[Éléments de preuve]
```

## Bonnes Pratiques

### À Faire

- ✅ Timeboxer strictement le POC
- ✅ Définir des critères de succès mesurables
- ✅ Documenter les apprentissages
- ✅ Jeter le code si non production-ready
- ✅ Impliquer les futurs développeurs

### À Éviter

- ❌ Transformer le POC en développement réel
- ❌ POC sans critères de succès clairs
- ❌ Sous-estimer le temps de documentation
- ❌ Ignorer les résultats négatifs
- ❌ POC sur trop de sujets à la fois

## Liens avec Autres Agents

| Agent | Interaction |
|-------|-------------|
| `etude-faisabilite` | Déclenche le POC si incertitude |
| `selection-stack` | Peut être alimenté par résultats POC |
| `specification/specification-technique` | Intègre les conclusions |
| `estimation/estimation-detaillee` | Affine les estimations |

## Points d'Escalade

| Situation | Action |
|-----------|--------|
| POC non concluant dans le temps | Arrêter et analyser, ne pas prolonger |
| Résultat négatif sur feature critique | Escalader pour décision Go/No-Go |
| Découverte de complexité majeure | Réévaluer les estimations |
| Besoin de ressources supplémentaires | Demander validation avant |

## Livrables

| Livrable | Description |
|----------|-------------|
| Cadrage POC | Document définissant objectifs, critères de succès et planning time-boxé |
| Rapport POC | Résultats détaillés avec verdict, recommandations et prochaines étapes |
| Code POC | Repository du prototype avec documentation (jetable ou réutilisable selon résultats) |
