# ADR-006: Clarification de la Hiérarchie lead-dev / web-dev-process

## Statut

**Accepté** - 2024-12-27

## Contexte

La hiérarchie des skills présentait une ambiguïté :

- `lead-dev` se positionnait comme "NIVEAU INTERMÉDIAIRE : COORDINATION" entre direction-technique (NIVEAU 1) et web-dev-process (NIVEAU 2)
- `web-dev-process` se positionnait comme "NIVEAU 2 : QUOI"
- Cela créait une hiérarchie à 4 niveaux confuse

### Problèmes identifiés

1. **Incohérence** : lead-dev "au-dessus" de web-dev-process, mais les deux traitent de sujets similaires
2. **Chevauchements** : Code review et Deployment présents dans les deux skills
3. **Confusion routage** : Impossible de savoir vers quel skill router sans contexte

### Chevauchements concrets

| Domaine | lead-dev | web-dev-process |
|---------|----------|-----------------|
| Code Review | 6 agents (pr-review, quality-gate, etc.) | 1 agent (code-review.md) |
| Deployment | 6 agents (delivery/) | 4 agents (deployment/) |

## Décision

**lead-dev et web-dev-process sont positionnés au même niveau (NIVEAU 2: OPÉRATIONS)** avec des responsabilités complémentaires mais distinctes.

### Nouvelle hiérarchie

```
┌─────────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : STRATÉGIE (direction-technique)                         │
│  → POURQUOI : Décisions, politiques, standards                      │
├─────────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : OPÉRATIONS                                              │
│  ┌────────────────────────────┐  ┌────────────────────────────┐    │
│  │     web-dev-process        │  │       lead-dev             │    │
│  │                            │  │                            │    │
│  │  QUOI : Méthodologie       │  │  QUI : Coordination        │    │
│  │  • 7 phases projet         │  │  • Code review (faire)     │    │
│  │  • Process standards       │  │  • Team coordination       │    │
│  │  • Checklists, workflows   │  │  • Delivery/release        │    │
│  │  • "Comment organiser ?"   │  │  • "Qui fait quoi ?"       │    │
│  └────────────────────────────┘  └────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : IMPLÉMENTATION (skills techniques)                      │
│  → COMMENT : Code, configuration, patterns                          │
└─────────────────────────────────────────────────────────────────────┘
```

### Distinction des responsabilités

| Concern | web-dev-process | lead-dev |
|---------|-----------------|----------|
| Code Review | **Process** : Checklist, critères, workflow | **Exécution** : Faire la review, donner feedback |
| Deployment | **Process** : Étapes staging → prod, rollback | **Coordination** : Planifier release, valider |
| Standards | **Process** : Définir les conventions | **Application** : Faire respecter |
| Tests | **Process** : Pyramide, stratégie | - (skills techniques) |

### Règle de routage

- **"Comment organiser X ?"** → web-dev-process
- **"Qui fait X ? Valider X ?"** → lead-dev

## Conséquences

### Positives

1. **Clarté** : Hiérarchie à 3 niveaux cohérente
2. **Routage simple** : QUOI vs QUI comme critère de décision
3. **Pas de refonte majeure** : Les agents existants restent pertinents

### Négatives

1. **Documentation à mettre à jour** : 3 SKILL.md modifiés
2. **Habitudes à changer** : Les utilisateurs doivent apprendre la distinction

## Alternatives considérées

### Alternative 1 : Fusionner lead-dev dans web-dev-process

**Rejeté** car :
- web-dev-process est agnostique (process), lead-dev est opérationnel (personnes)
- La séparation QUOI/QUI est conceptuellement claire
- Trop de travail de refactoring

### Alternative 2 : Garder la hiérarchie à 4 niveaux

**Rejeté** car :
- Confusion persistante
- Difficile à expliquer et maintenir
- Chevauchements non résolus

## Notes d'implémentation

### Fichiers modifiés

- `lead-dev/SKILL.md` → v1.1.0
- `web-dev-process/SKILL.md` → v1.2.0
- `web-agency/SKILL.md` → v2.6.0

### Tests de validation

Exécuter les tests après modification :

```bash
cd .web-agency/skills/lead-dev && npm test
cd .web-agency/skills/web-dev-process && npm test
```

## Références

- [ADR-005: Frontières entre Skills](./005-skill-responsibility-boundaries.md)
- [Analyse Separation of Concerns](../analysis/SEPARATION-OF-CONCERNS-REVIEW.md)
