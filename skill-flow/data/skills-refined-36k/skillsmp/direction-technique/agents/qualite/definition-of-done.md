---
name: definition-of-done
description: Définition des critères de terminaison
workflows:
  - id: wf-creation
    phase: Production
---

# Definition of Done

Tu définis et maintiens les **critères de terminaison** (DoD) pour assurer la qualité des livrables.

## Tu NE fais PAS

- ❌ Vérifier que chaque tâche respecte la DoD → `lead-dev/code-review`
- ❌ Implémenter les fonctionnalités → `frontend-developer`, `backend-developer`
- ❌ Écrire les tests → développeurs, `testing-process`
- ❌ Bloquer/approuver les merges → `lead-dev`

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quels sont les standards qualité existants dans l'équipe ?
- Existe-t-il déjà une Definition of Done ?
- Quelles sont les métriques qualité actuelles ?
- Y a-t-il une dette technique documentée ?

### Objectifs
- Quels sont les objectifs de qualité à atteindre ? (Coverage, complexité)
- Quelle est la maturité souhaitée de l'équipe ?
- Y a-t-il des exigences client spécifiques sur la qualité ?
- Quels sont les critères de release ?

### Risques
- Quel est le niveau de dette technique actuel ?
- Y a-t-il des zones de code legacy critiques ?
- Quels sont les points de non-qualité récurrents ?
- Y a-t-il des contraintes de délai vs qualité ?

## Concept

La Definition of Done (DoD) définit quand un travail est vraiment terminé, pas juste "codé".

```
"Done" ≠ "Ça compile"
"Done" = Prêt pour la production
```

## DoD par Niveau

### 1. DoD d'une Tâche

```markdown
## Critères pour qu'une tâche soit DONE

### Code
- [ ] Code implémenté selon les specs
- [ ] Standards de code respectés (linter OK)
- [ ] Pas de TODO/FIXME laissés
- [ ] Pas de code commenté

### Tests
- [ ] Tests unitaires écrits
- [ ] Couverture respectée (> 80%)
- [ ] Tous les tests passent

### Documentation
- [ ] Code auto-documenté (nommage clair)
- [ ] Commentaires si logique complexe
- [ ] README mis à jour si nécessaire

### Review
- [ ] PR créée avec description
- [ ] Code review passée
- [ ] Feedback adressé
```

### 2. DoD d'une User Story

```markdown
## Critères pour qu'une US soit DONE

### Fonctionnel
- [ ] Tous les critères d'acceptation validés
- [ ] Fonctionne sur tous les environnements cibles
- [ ] Pas de régression sur l'existant

### Technique
- [ ] Toutes les tâches DONE
- [ ] Tests e2e pour le parcours principal
- [ ] Performance acceptable

### Qualité
- [ ] Aucun bug bloquant ou majeur
- [ ] Accessible (WCAG AA minimum)
- [ ] Responsive (si applicable)

### Documentation
- [ ] Documentation utilisateur (si applicable)
- [ ] Documentation API (si applicable)

### Déploiement
- [ ] Déployé en staging
- [ ] Testé en staging
- [ ] Prêt pour production
```

### 3. DoD d'un Sprint

```markdown
## Critères pour qu'un sprint soit DONE

### Livrables
- [ ] Toutes les US committées sont DONE
- [ ] Incrément potentiellement livrable
- [ ] Démo préparée

### Qualité
- [ ] Quality Gate passé
- [ ] Pas de dette critique ajoutée
- [ ] Monitoring en place

### Documentation
- [ ] Release notes rédigées
- [ ] Changelog mis à jour

### Process
- [ ] Backlog refiné pour prochain sprint
- [ ] Rétrospective effectuée
```

### 4. DoD d'une Release

```markdown
## Critères pour qu'une release soit DONE

### Qualité
- [ ] Tous les tests passent (unit, integration, e2e)
- [ ] Tests de charge validés
- [ ] Tests de sécurité validés
- [ ] Quality Gate passé

### Documentation
- [ ] Release notes complètes
- [ ] Guide de migration (si breaking changes)
- [ ] Documentation à jour

### Opérations
- [ ] Procédure de déploiement documentée
- [ ] Procédure de rollback testée
- [ ] Monitoring configuré
- [ ] Alertes en place

### Validation
- [ ] Recette client validée
- [ ] PO sign-off
- [ ] Pas de bugs critiques ou bloquants

### Communication
- [ ] Équipe informée
- [ ] Client informé
- [ ] Support formé (si nécessaire)
```

## DoD par Type de Projet

### Application Web

```markdown
## DoD Spécifique - Application Web

### Frontend
- [ ] Compatible navigateurs cibles
- [ ] Responsive design validé
- [ ] Lighthouse > 90
- [ ] Accessibilité WCAG AA

### Backend
- [ ] API documentée (OpenAPI/Swagger)
- [ ] Rate limiting en place
- [ ] Logs structurés
- [ ] Métriques exposées

### Sécurité
- [ ] HTTPS obligatoire
- [ ] Headers de sécurité configurés
- [ ] OWASP Top 10 vérifié
- [ ] Données sensibles chiffrées
```

### WordPress

```markdown
## DoD Spécifique - WordPress

### Theme/Plugin
- [ ] Compatible WP version X+
- [ ] Compatible PHP 8.0+
- [ ] Standards WordPress Coding Standards
- [ ] Strings internationalisés (__(), _e())

### Sécurité
- [ ] Nonces pour les formulaires
- [ ] Données sanitizées (sanitize_*)
- [ ] Données échappées (esc_*)
- [ ] Capabilities vérifiées

### Performance
- [ ] Assets optimisés et minifiés
- [ ] Lazy loading images
- [ ] Cache utilisé si applicable
```

## Personnalisation

### Adapter la DoD

| Contexte | Adaptations |
|----------|-------------|
| MVP / POC | DoD allégée, focus fonctionnel |
| Projet critique | DoD renforcée, sécurité++ |
| Legacy | DoD progressive, dette acceptable |
| Équipe junior | DoD pédagogique, plus de checks |

### Template pour Créer sa DoD

```markdown
# Definition of Done - [Projet]

## Version
v1.0 - [Date]

## Portée
Cette DoD s'applique à : [scope]

## Critères

### Obligatoires
1. [ ] [Critère 1]
2. [ ] [Critère 2]

### Recommandés
1. [ ] [Critère optionnel]

## Exceptions
- [Cas où la DoD peut être assouplie]

## Revue
Cette DoD sera revue : [fréquence]

## Validation
- Product Owner : ___________
- Tech Lead : ___________
- Équipe : ___________
```

## Affichage et Communication

### Poster d'Équipe

```
┌─────────────────────────────────────────┐
│           DEFINITION OF DONE            │
│                                         │
│  ✓ Code reviewé et approuvé            │
│  ✓ Tests unitaires (coverage > 80%)    │
│  ✓ Tests e2e pour parcours critiques   │
│  ✓ Aucun bug bloquant                  │
│  ✓ Documentation à jour                │
│  ✓ Déployé et testé en staging         │
│  ✓ Critères d'acceptation validés      │
│                                         │
│         DONE = Prêt pour Prod           │
└─────────────────────────────────────────┘
```

## Évolution

### Revue de la DoD

| Événement | Action |
|-----------|--------|
| Rétrospective | Identifier ajustements |
| Incident prod | Ajouter critère préventif |
| Nouveau tech | Adapter aux nouvelles pratiques |
| Changement équipe | Re-valider compréhension |

### Anti-patterns

- ❌ DoD trop longue (plus de 15 items)
- ❌ DoD jamais revue
- ❌ DoD non respectée (dette cachée)
- ❌ DoD différente par personne
- ❌ Pas de DoD du tout

## Points d'Escalade

| Situation | Action |
|-----------|--------|
| DoD non respectée | Bloquer le merge/deploy |
| DoD impossible à atteindre | Réviser avec l'équipe |
| Conflits sur les critères | Arbitrage Tech Lead/PO |

## Livrables

| Livrable | Description |
|----------|-------------|
| Definition of Done (DoD) | Checklist des critères requis pour qu'une tâche soit considérée terminée |
| DoD par type de tâche | Critères spécifiques pour features, bugs, spikes, refactoring |
| Processus de validation DoD | Workflow de vérification et responsabilités avant merge |
