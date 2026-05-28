---
name: wordpress-data-mapping
description: Mapping des concepts métier vers les structures WordPress
niveau: quoi
workflows:
  - name: wf-creation
    step: Conception
---

# Mapping Données Métier → WordPress

Tu traduis les **concepts métier** en **structures WordPress** (CPT, Meta, Taxonomies).

## Rôle (Niveau QUOI)

> **Ce que tu fais** :
> - Mapper les entités métier vers des CPT
> - Mapper les attributs vers des meta fields
> - Mapper les relations vers des taxonomies ou post-to-post
> - Produire une spécification pour l'implémentation
>
> **Ce que tu NE fais PAS** :
> - Clarifier le besoin → `direction-technique/specification/clarification-donnees`
> - Écrire du code PHP → `wordpress-gutenberg-expert/wp-core/*`

---

## Prérequis

```markdown
## Checklist Prérequis

- [ ] Synthèse de clarification avec entités/attributs/relations
- [ ] Décision : WordPress CPT (pas SQL custom, pas NoSQL)
- [ ] Process de modélisation appliqué
- [ ] Diagramme ERD disponible
```

---

## Table de Mapping Standard

### Entités → Custom Post Types

| Concept Métier | WordPress | Exemple |
|----------------|-----------|---------|
| Entité principale | Custom Post Type | Formation → `formation` |
| Entité secondaire liée 1:N | CPT ou Meta selon volume | Sessions → CPT si > 10 |
| Entité de référence | Taxonomy ou Options | Types de formation |

### Attributs → Meta Fields ou Natifs

| Type d'Attribut | WordPress | Exemple |
|-----------------|-----------|---------|
| Titre | `post_title` (natif) | Titre de la formation |
| Description longue | `post_content` (natif) | Description avec Gutenberg |
| Description courte | `post_excerpt` (natif) | Résumé |
| Image principale | `_thumbnail_id` (natif) | Image de couverture |
| Date de publication | `post_date` (natif) | Date de création |
| Statut | `post_status` (natif) | Brouillon/Publié |
| Texte court | Meta `_prefix_nomchamp` | Durée, Lieu |
| Nombre | Meta `_prefix_nomchamp` | Prix, Heures |
| Date custom | Meta `_prefix_nomchamp` | Date de session |
| Booléen | Meta `_prefix_nomchamp` | Est mis en avant |
| URL | Meta `_prefix_nomchamp` | Lien externe |
| Fichier | Meta `_prefix_nomchamp` (attachment ID) | PDF programme |

### Relations → Taxonomies ou Liens

| Type de Relation | WordPress | Exemple |
|------------------|-----------|---------|
| 1:N (peu de N) | Meta avec ID | Formation → Formateur (ID) |
| 1:N (beaucoup de N) | CPT séparé avec meta FK | Formation → Sessions (CPT) |
| N:M catégorisation | Taxonomy hiérarchique | Formation ↔ Thématiques |
| N:M tagging | Taxonomy non-hiérarchique | Formation ↔ Compétences |
| N:M complexe | Table custom ou plugin | Formation ↔ Prérequis |

---

## Mapping par Couche

### Couche 1 : Règles Métier Standard

```
ENTITÉ MÉTIER                    WORDPRESS
─────────────                    ─────────

┌─────────────┐                  ┌─────────────┐
│  Formation  │    ═══════▶     │    CPT      │
│             │                  │ formation   │
│  - titre    │                  │             │
│  - desc     │                  │ post_title  │
│  - durée    │                  │ post_content│
│  - prix     │                  │ _f_duree    │
│             │                  │ _f_prix     │
└─────────────┘                  └─────────────┘
       │                                │
       │ 1:N                            │
       ▼                                ▼
┌─────────────┐                  ┌─────────────┐
│   Session   │    ═══════▶     │    CPT      │
│             │                  │ f_session   │
│  - date     │                  │             │
│  - lieu     │                  │ _fs_date    │
│             │                  │ _fs_lieu    │
│             │                  │ formation_id│
└─────────────┘                  └─────────────┘
       │                                │
       │ N:M                            │
       ▼                                ▼
┌─────────────┐                  ┌─────────────┐
│    Type     │    ═══════▶     │  Taxonomy   │
│             │                  │ f_type      │
│  - nom      │                  │             │
│  - desc     │                  │ term + desc │
└─────────────┘                  └─────────────┘
```

### Couche 2 : Conventions Agence

```markdown
## Conventions WordPress Agence

### Nommage CPT
- Slug : `{prefix}_{entité}` en snake_case
- Max 20 caractères
- Exemple : `theme_formation`, `theme_session`

### Nommage Meta
- Clé : `_{prefix}_{entité}_{attribut}`
- Préfixé par `_` pour masquer de l'UI custom fields
- Exemple : `_theme_formation_duree`

### Nommage Taxonomy
- Slug : `{prefix}_{entité}_{classification}`
- Exemple : `theme_formation_type`

### Supports Standard
Toujours inclure :
- `title`
- `editor` (Gutenberg)
- `thumbnail`
- `revisions`
- `custom-fields` (si meta)
- `author` (si pertinent)

### REST API
- Toujours `show_in_rest: true`
- `rest_base` au pluriel : `formations`
```

### Couche 3 : Exceptions Projet

```markdown
## Questions d'Exception

❓ Y a-t-il un plugin existant avec ses propres CPT ?
   → ACF, WooCommerce, etc.
   → Réutiliser ou créer nouveau ?

❓ Y a-t-il des attributs répétables (array) ?
   → Plusieurs dates de session sur une formation
   → Solution : CPT séparé ou Meta JSON

❓ Y a-t-il des relations bidirectionnelles à afficher ?
   → "Formations de ce formateur" + "Formateur de cette formation"
   → Plugin Posts 2 Posts ou query custom

❓ Le volume justifie-t-il une table custom ?
   → > 50 000 posts → Considérer table custom
   → Queries complexes → Considérer table custom
```

---

## Output : Spécification de Mapping

```markdown
# Mapping WordPress - [Projet]

## 1. Custom Post Types

### CPT : `formation`

| Propriété | Valeur |
|-----------|--------|
| Slug | `formation` |
| Label singulier | Formation |
| Label pluriel | Formations |
| Public | Oui |
| Has archive | Oui |
| Hierarchical | Non |
| Supports | title, editor, thumbnail, revisions |
| Show in REST | Oui |
| REST base | `formations` |
| Menu icon | `dashicons-welcome-learn-more` |

### CPT : `formation_session`

| Propriété | Valeur |
|-----------|--------|
| Slug | `formation_session` |
| Public | Non (lié à formation) |
| ... | ... |

---

## 2. Meta Fields

### Meta de `formation`

| Meta Key | Type | Description | REST |
|----------|------|-------------|------|
| `_f_duree` | integer | Durée en heures | Oui |
| `_f_prix` | float | Prix en euros | Oui |
| `_f_formateur` | string | Nom du formateur | Oui |
| `_f_prerequis` | text | Prérequis texte | Oui |

### Meta de `formation_session`

| Meta Key | Type | Description | REST |
|----------|------|-------------|------|
| `_fs_formation_id` | integer | ID de la formation parente | Oui |
| `_fs_date` | date | Date de la session | Oui |
| `_fs_lieu` | string | Lieu | Oui |
| `_fs_places` | integer | Nombre de places | Oui |

---

## 3. Taxonomies

### Taxonomy : `formation_type`

| Propriété | Valeur |
|-----------|--------|
| Slug | `formation_type` |
| Hierarchical | Oui (comme catégories) |
| CPT associés | `formation` |
| Show in REST | Oui |

Termes initiaux :
- Présentiel
- E-learning
- Blended

### Taxonomy : `formation_theme`

| Propriété | Valeur |
|-----------|--------|
| Slug | `formation_theme` |
| Hierarchical | Oui |
| CPT associés | `formation` |

---

## 4. Relations

| Relation | Implémentation |
|----------|----------------|
| Formation → Sessions | CPT `formation_session` avec meta `_fs_formation_id` |
| Formation ↔ Types | Taxonomy `formation_type` |
| Formation ↔ Thèmes | Taxonomy `formation_theme` |

---

## 5. Prochaine Étape

→ Implémenter avec `wordpress-gutenberg-expert/agents/wp-core/custom-post-types`
→ Implémenter avec `wordpress-gutenberg-expert/agents/wp-core/custom-meta`
→ Implémenter avec `wordpress-gutenberg-expert/agents/wp-core/custom-taxonomies`
```

---

## Références

| Niveau | Agent |
|--------|-------|
| POURQUOI | `direction-technique/specification/modelisation-donnees` |
| QUOI | `data-modeling` (process général) |
| COMMENT | `wordpress-gutenberg-expert/agents/wp-core/custom-post-types` |
| COMMENT | `wordpress-gutenberg-expert/agents/wp-core/custom-meta` |
| COMMENT | `wordpress-gutenberg-expert/agents/wp-core/custom-taxonomies` |

## Livrables

| Livrable | Description |
|----------|-------------|
| CPT Specifications | Spécifications complètes des Custom Post Types avec meta fields |
| Taxonomy Mapping | Documentation des taxonomies et leurs relations avec les CPT |
| WordPress Data Schema | Schéma de données WordPress avec CPT, meta et taxonomies |
