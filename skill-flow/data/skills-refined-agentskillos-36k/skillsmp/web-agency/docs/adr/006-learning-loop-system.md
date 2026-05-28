# ADR-006 : Système de Learning Loop

## Statut

Accepté

## Date

2024-12-24

## Contexte

L'analyse des agents techniques a révélé plusieurs problèmes :

1. **Erreurs répétées** : Les mêmes problèmes (CORS staging, configs hardcodées, etc.) se reproduisent d'un projet à l'autre
2. **Perte de connaissance** : Les solutions trouvées ne sont pas capitalisées
3. **Manque de feedback** : Les agents ne peuvent pas apprendre de l'expérience
4. **Onboarding long** : Chaque nouveau projet repart de zéro

### Besoins Identifiés

- Capitaliser sur les succès et erreurs
- Éviter de reproduire les mêmes erreurs
- Réutiliser les solutions qui fonctionnent
- Améliorer continuellement la qualité

## Décision

Implémenter un **système de Learning Loop à deux niveaux** :

### Niveau 1 : Apprentissage Global

```
.web-agency/learnings/
├── patterns/           # Solutions réutilisables validées
├── anti-patterns/      # Erreurs à éviter
├── decisions/          # Décisions archétypales
├── metrics/            # Métriques de succès
└── templates/          # Templates de documentation
```

**Caractéristiques :**
- Partagé entre tous les projets
- Validé par expérience (>= 2 occurrences)
- Maintenu par les tech leads
- Versionné avec le repo skills

### Niveau 2 : Apprentissage Projet

```
[projet-client]/.learnings/
├── context.md          # Contexte spécifique
├── decisions/          # Décisions projet
├── issues/             # Problèmes rencontrés
├── successes/          # Réussites à capitaliser
└── retrospectives/     # Retours de sprint
```

**Caractéristiques :**
- Spécifique à chaque projet
- Créé à l'initialisation du projet
- Versionné avec le repo projet
- Source de promotion vers le global

### Mécanisme de Promotion

```
PROJET                          GLOBAL
───────────────────────────────────────────

Issue projet           →    Candidat promotion
(occurrence_count >= 2)      (candidate_for_global: true)
                                    │
                                    ▼
                             Review tech lead
                                    │
                                    ▼
                        Pattern ou Anti-pattern global
```

**Critères de promotion :**

| Critère | Seuil |
|---------|-------|
| Occurrence | >= 2 projets |
| Impact | >= 2h d'économie |
| Généricité | >= 50% projets concernés |

### Intégration avec les Agents

Chaque agent technique doit :

**AVANT une tâche :**
1. Consulter `patterns/INDEX.md`
2. Consulter `anti-patterns/INDEX.md`
3. Consulter `.learnings/context.md` du projet
4. Vérifier les issues récentes du projet

**APRÈS une tâche :**
1. Documenter si problème > 30min
2. Documenter si solution innovante
3. Évaluer la promotion vers global

## Conséquences

### Positives

- **Capitalisation** : Connaissance préservée et réutilisable
- **Prévention** : Anti-patterns évités proactivement
- **Qualité** : Amélioration continue mesurable
- **Onboarding** : Nouveaux devs bénéficient de l'expérience collective
- **Traçabilité** : Historique des décisions et problèmes

### Négatives

- **Overhead documentation** : Temps supplémentaire pour documenter
- **Maintenance** : Nécessite des revues périodiques
- **Discipline** : Demande rigueur de la part des équipes

### Métriques de Succès

| Métrique | Baseline | Cible |
|----------|----------|-------|
| Erreurs répétées | Non mesuré | < 10% |
| Pattern usage | 0% | > 60% |
| Temps résolution | Variable | -30% |
| Onboarding dev | Variable | < 15min |

## Références

- [LEARNING-GUIDE.md](../../../../learnings/LEARNING-GUIDE.md)
- [Patterns Index](../../../../learnings/patterns/INDEX.md)
- [Anti-patterns Index](../../../../learnings/anti-patterns/INDEX.md)
- [Analyse Agents Techniques](../../../../../docs/analysis/TECHNICAL-AGENTS-IMPROVEMENTS.md)
