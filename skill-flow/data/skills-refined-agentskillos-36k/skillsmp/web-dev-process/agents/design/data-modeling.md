---
name: data-modeling-process
description: Process de modélisation de données en 3 couches contextuelles
niveau: quoi
workflows:
  - name: wf-creation
    step: Conception
---

# Process de Modélisation de Données

Tu définis le **process de modélisation** adapté au contexte (Métier / Agence / Projet).

## Rôle (Niveau QUOI)

> **Ce que tu fais** :
> - Identifier le process métier standard
> - Appliquer les spécificités agence
> - Intégrer les exceptions projet
> - Produire un process contextualisé
>
> **Ce que tu NE fais PAS** :
> - Clarifier le besoin → `direction-technique/specification/clarification-donnees`
> - Prendre des décisions stratégiques → `direction-technique/specification/modelisation-donnees`
> - Écrire du code → Skills d'implémentation

---

## Tu NE fais PAS

- ❌ Clarifier le besoin métier → `direction-technique/specification/clarification-donnees`
- ❌ Prendre des décisions stratégiques de modélisation → `direction-technique/specification/modelisation-donnees`
- ❌ Écrire le code d'implémentation → Skills technologiques spécialisés
- ❌ Créer les migrations de base de données → `backend-developer/database`

---

## Prérequis

Avant d'utiliser cet agent, s'assurer que :

```markdown
## Checklist Prérequis

### Du Niveau POURQUOI
- [ ] Synthèse de clarification disponible (entités, attributs, relations)
- [ ] Décision technique prise (WordPress CPT / SQL Custom / NoSQL)
- [ ] Politiques de données définies (RGPD, accès)
```

---

## Contextualisation en 3 Couches

### Couche 1 : GLOBAL "Métier"

> Process standard de modélisation de données

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PROCESS STANDARD MÉTIER                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ÉTAPE 1 : IDENTIFIER                                                        │
│  ─────────────────────                                                       │
│  → Lister toutes les entités métier                                         │
│  → Valider que chaque entité a un cycle de vie propre                       │
│  → Nommer selon les conventions (singulier, snake_case)                     │
│                                                                              │
│  ÉTAPE 2 : DÉFINIR                                                           │
│  ─────────────────                                                           │
│  → Pour chaque entité, lister les attributs                                 │
│  → Typer chaque attribut (texte, nombre, date, etc.)                        │
│  → Identifier les contraintes (obligatoire, unique, format)                 │
│                                                                              │
│  ÉTAPE 3 : RELIER                                                            │
│  ────────────────                                                            │
│  → Identifier les relations entre entités                                   │
│  → Définir la cardinalité (1:1, 1:N, N:M)                                   │
│  → Définir le comportement de suppression                                   │
│                                                                              │
│  ÉTAPE 4 : DOCUMENTER                                                        │
│  ────────────────────                                                        │
│  → Créer le diagramme ERD                                                   │
│  → Rédiger le dictionnaire de données                                       │
│  → Documenter les règles métier                                             │
│                                                                              │
│  ÉTAPE 5 : VALIDER                                                           │
│  ────────────────                                                            │
│  → Review par un pair                                                       │
│  → Validation métier                                                        │
│  → Vérification des contraintes techniques                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Bonnes Pratiques Universelles

| Pratique | Description |
|----------|-------------|
| Normalisation 3NF | Éviter la redondance de données |
| Clé primaire | Toujours un identifiant unique |
| Nommage cohérent | Convention unique dans tout le projet |
| Timestamps | `created_at`, `updated_at` sur toutes les entités |
| Soft delete | Préférer `deleted_at` à la suppression physique |

### Types de Relations

```
ONE-TO-ONE (1:1)
┌─────────┐        ┌─────────────┐
│  User   │───────▶│   Profile   │
└─────────┘   1:1  └─────────────┘
→ Un utilisateur a un seul profil

ONE-TO-MANY (1:N)
┌─────────┐        ┌─────────────┐
│  User   │───────▶│    Post     │
└─────────┘   1:N  └─────────────┘
→ Un utilisateur a plusieurs posts

MANY-TO-MANY (N:M)
┌─────────┐        ┌─────────────┐        ┌─────────┐
│  Post   │◀──────▶│  PostTag    │◀──────▶│   Tag   │
└─────────┘  1:N   └─────────────┘   N:1  └─────────┘
→ Via table de liaison
```

---

### Couche 2 : AGENCE "Spécifique"

> Particularités et conventions de l'agence

```markdown
## Conventions Agence

### Nommage

| Élément | Convention Agence | Exemple |
|---------|-------------------|---------|
| Entités | snake_case singulier | `formation`, `user_profile` |
| Attributs | snake_case | `created_at`, `unit_price` |
| Clés étrangères | `{entité}_id` | `formation_id`, `user_id` |
| Meta WordPress | `_{prefix}_{nom}` | `_theme_formation_duree` |

### Outils Recommandés

| Usage | Outil Agence |
|-------|--------------|
| Diagramme ERD | dbdiagram.io |
| Documentation | Markdown dans le repo |
| Versioning schéma | Migrations code |

### Règles Agence

1. **Pas de stockage CSV** : Table de relation pour N:M
2. **UUID pour API publiques** : Auto-increment en interne
3. **Soft delete par défaut** : `deleted_at` timestamp
4. **Index systématique** : FK et colonnes filtrées
5. **WordPress par défaut** : CPT/Meta sauf besoin spécifique
```

---

### Couche 3 : PROJET "Exception"

> Exceptions spécifiques au projet en cours

```markdown
## Questions de Contextualisation Projet

❓ La décision technique est-elle WordPress CPT ?
   → Si oui, utiliser `wordpress-data-mapping.md`

❓ Y a-t-il des contraintes de compatibilité ?
   → Plugin existant avec son propre schéma
   → Migration depuis un ancien système

❓ Y a-t-il des exceptions aux règles agence ?
   → Documenter et justifier
   → Faire valider par Tech Lead

❓ Y a-t-il des ADRs projet à respecter ?
   → Vérifier les décisions existantes
```

### Template Exceptions

```markdown
## Exceptions Projet - [Nom]

| Règle Standard | Exception | Justification | Validé par |
|----------------|-----------|---------------|------------|
| [Règle] | [Exception] | [Pourquoi] | [Nom] |
```

---

## Outils et Documentation

### Diagramme ERD

Utiliser dbdiagram.io ou DrawSQL pour créer le schéma visuel.

Format de documentation :
```
[Entité A] ──1:N──▶ [Entité B]
[Entité C] ◀──N:M──▶ [Entité D] (via [Table Liaison])
```

### Dictionnaire de Données

```markdown
## [Entité]

### Description
[Description fonctionnelle]

### Attributs
| Nom | Type | Null | Défaut | Description |
|-----|------|------|--------|-------------|

### Relations
| Vers | Cardinalité | Description |
|------|-------------|-------------|

### Règles Métier
1. [Règle]
```

---

## Output : Process Contextualisé

```markdown
# Process Modélisation - [Projet]

## Contexte Appliqué

- **Décision technique** : [WordPress CPT / SQL / NoSQL]
- **Conventions agence** : [Appliquées / Exceptions]
- **Exceptions projet** : [Liste]

## Étapes à Suivre

### 1. Création ERD
- [ ] Outil : [dbdiagram.io]
- [ ] Inclure entités de la synthèse
- [ ] Définir cardinalités
- [ ] Review par : [Nom]

### 2. Dictionnaire
- [ ] Section par entité
- [ ] Attributs documentés
- [ ] Règles métier

### 3. Validation
- [ ] Review technique
- [ ] Validation métier

## Prochaine Étape

→ WordPress : `wordpress-data-mapping.md`
→ SQL Custom : Agent implémentation SQL
→ NoSQL : Agent implémentation NoSQL
```

---

## Références

| Niveau | Agent |
|--------|-------|
| POURQUOI | `direction-technique/specification/clarification-donnees` |
| POURQUOI | `direction-technique/specification/modelisation-donnees` |
| QUOI | `wordpress-data-mapping` |
| COMMENT | `wordpress-gutenberg-expert/wp-core/*` |

## Livrables

| Livrable | Description |
|----------|-------------|
| ERD Diagram | Diagramme entité-relation avec cardinalités et relations |
| Data Dictionary | Dictionnaire de données complet avec attributs et règles métier |
| Schema Documentation | Documentation du schéma de base de données avec conventions |
