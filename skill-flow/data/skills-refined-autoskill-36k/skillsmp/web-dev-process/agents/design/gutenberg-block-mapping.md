---
name: gutenberg-block-mapping
description: Process de mapping composant UI vers implémentation Gutenberg
niveau: quoi
workflows:
  - name: wf-creation
    step: Conception
---

# Mapping Composant UI → Gutenberg

Tu définis le **process de mapping** d'un composant UI vers les solutions Gutenberg adaptées.

## Rôle (Niveau QUOI)

> **Ce que tu fais** :
> - Recevoir la synthèse de clarification composant
> - Mapper vers les solutions Gutenberg appropriées
> - Appliquer les spécificités agence
> - Produire les spécifications techniques

> **Ce que tu NE fais PAS** :
> - Clarifier le besoin UI → `direction-technique/specification/clarification-composant`
> - Écrire du code → `wordpress-gutenberg-expert/agents/blocks/*`

---

## Prérequis

Avant d'utiliser cet agent, s'assurer que :

```markdown
## Checklist Prérequis

### Du Niveau POURQUOI
- [ ] Synthèse composant disponible (clarification-composant.md)
- [ ] Contexte défini (où, pourquoi)
- [ ] Contenu défini (source, quantité, tri)
- [ ] Présentation définie (layout, card structure)
- [ ] Interactions définies (hover, clic, slider behavior)
- [ ] Configuration définie (qui peut modifier quoi)
- [ ] Responsive défini (breakpoints)
```

---

## Contextualisation en 3 Couches

### Couche 1 : GLOBAL "Métier"

> Process standard de mapping vers Gutenberg

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ARBRE DE DÉCISION GUTENBERG                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ❓ Le composant affiche-t-il du contenu dynamique (posts, CPT) ?           │
│  ├── NON → Block statique (save en JS)                                      │
│  └── OUI ↓                                                                  │
│                                                                              │
│  ❓ La requête est-elle simple (derniers posts d'une catégorie) ?           │
│  ├── OUI → Query Loop Block + variations/patterns                           │
│  └── NON ↓                                                                  │
│                                                                              │
│  ❓ Y a-t-il besoin de sélection manuelle de posts ?                        │
│  ├── OUI → Block dynamique custom avec EntityProvider                       │
│  └── NON ↓                                                                  │
│                                                                              │
│  ❓ Y a-t-il des interactions complexes (slider, filtres AJAX) ?            │
│  ├── OUI → Block dynamique + view.js (Interactivity API ou vanilla)        │
│  └── NON → Block dynamique simple (render_callback)                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Matrice de Décision Layout

| Layout Souhaité | Solution Gutenberg | Librairie JS |
|-----------------|-------------------|--------------|
| Liste verticale | Query Loop + Post Template | Aucune |
| Grille statique | Query Loop + Grid variation | Aucune |
| Grille Masonry | Block custom + CSS Grid | Aucune ou Masonry.js |
| Slider/Carrousel | Block custom dynamique | Swiper / Splide / Embla |
| Tabs | Block custom | Aucune (CSS + JS natif) |
| Accordion | Block custom ou Pattern | Aucune (details/summary) |

### Matrice de Décision Slider

| Besoin | Swiper.js | Splide | Embla | Native CSS |
|--------|-----------|--------|-------|------------|
| Taille bundle | ~140KB | ~30KB | ~20KB | 0KB |
| Loop infini | ✅ | ✅ | ✅ | ⚠️ Limité |
| Autoplay | ✅ | ✅ | ✅ | ❌ |
| Breakpoints | ✅ | ✅ | ✅ | ✅ |
| Accessibilité | ✅ | ✅ | ⚠️ | ⚠️ |
| Virtual slides | ✅ | ❌ | ✅ | ❌ |
| Touch/Swipe | ✅ | ✅ | ✅ | ⚠️ |

---

### Couche 2 : AGENCE "Spécifique"

> Conventions et choix techniques de l'agence

```markdown
## Stack Technique Agence

### Librairies Approuvées

| Usage | Librairie | Version | Justification |
|-------|-----------|---------|---------------|
| Slider | Swiper | 11.x | Complet, bien maintenu |
| Animation | GSAP | 3.x | Si nécessaire uniquement |
| Icons | Dashicons + Custom SVG | - | Natif WP + custom |

### Conventions Blocks

| Élément | Convention |
|---------|------------|
| Namespace | `theme-name/` |
| Nommage block | `theme-name/{type}-{nom}` |
| Nommage pattern | `theme-name/{page}-{section}` |
| Fichier block | `blocks/{nom}/` avec block.json |

### Structure Block Standard

```
blocks/
├── {nom}/
│   ├── block.json        # Manifest
│   ├── edit.js           # Interface éditeur
│   ├── save.js           # Rendu statique (ou null si dynamique)
│   ├── index.js          # Enregistrement
│   ├── style.scss        # Styles frontend
│   ├── editor.scss       # Styles éditeur
│   ├── view.js           # Scripts frontend (si interactif)
│   └── render.php        # Rendu dynamique (si SSR)
```

### Règles Agence

1. **Préférer Query Loop** quand possible (maintenabilité)
2. **Pas de jQuery** dans les nouveaux blocks
3. **CSS Grid/Flexbox** plutôt que librairies CSS
4. **Interactivity API** pour les interactions simples
5. **View.js séparé** pour les interactions complexes
```

---

### Couche 3 : PROJET "Exception"

> Exceptions spécifiques au projet en cours

```markdown
## Questions de Contextualisation Projet

❓ Y a-t-il des blocks existants à réutiliser ?
   → Vérifier le thème parent
   → Vérifier les plugins installés

❓ Y a-t-il des contraintes de compatibilité ?
   → Version WordPress minimum
   → Support navigateurs legacy

❓ Le slider doit-il fonctionner sans JS ?
   → Fallback CSS scroll-snap
   → Mode dégradé acceptable ?

❓ Y a-t-il des patterns existants à étendre ?
   → Patterns du thème
   → Patterns du core à personnaliser
```

---

## Mapping Types de Composants

### Slider de Cards (Posts/CPT)

```markdown
## Mapping Slider → Gutenberg

### Input (de clarification-composant)
- Layout : Slider
- Source : CPT Formation
- Cards : Image, Titre, Extrait, CTA
- Navigation : Flèches + Dots + Swipe
- Autoplay : Oui, 5s, pause au hover
- Responsive : 3 → 2 → 1 slides

### Output (décision technique)

| Aspect | Décision | Justification |
|--------|----------|---------------|
| Type block | Block dynamique custom | Slider + sélection posts |
| Rendu | render.php (SSR) | SEO, performance |
| Slider lib | Swiper.js | Features complètes |
| Interactivité | view.js avec Swiper init | Séparé du bundle éditeur |

### Spécifications Block

**block.json**
- name: `theme/formation-slider`
- category: `theme-blocks`
- supports: align (wide, full), spacing

**Attributs**
| Attribut | Type | Défaut | Description |
|----------|------|--------|-------------|
| postType | string | "formation" | CPT source |
| postsPerPage | number | 6 | Nombre de posts |
| selectedPosts | array | [] | Sélection manuelle |
| showImage | boolean | true | Afficher image |
| showExcerpt | boolean | true | Afficher extrait |
| autoplay | boolean | true | Lecture auto |
| autoplayDelay | number | 5000 | Délai ms |
| slidesPerView | object | {desktop:3, tablet:2, mobile:1} | Responsive |

**Prochaine étape**
→ `wordpress-gutenberg-expert/agents/blocks/dynamic-block`
```

### Grille de Posts Filtrable

```markdown
## Mapping Grille Filtrable → Gutenberg

### Input
- Layout : Grille 3 colonnes
- Filtres : Par catégorie (tabs)
- Résultats : AJAX sans rechargement
- Pagination : Load more

### Output

| Aspect | Décision | Justification |
|--------|----------|---------------|
| Type block | Block dynamique custom | Filtres AJAX |
| Rendu | render.php + REST API | Chargement dynamique |
| Interactivité | Interactivity API | Natif WP, léger |

### Spécifications Block

**Attributs**
| Attribut | Type | Défaut | Description |
|----------|------|--------|-------------|
| postType | string | "post" | CPT source |
| taxonomy | string | "category" | Taxonomie filtres |
| columns | object | {desktop:3, tablet:2, mobile:1} | Colonnes |
| postsPerPage | number | 9 | Posts par page |

**API REST**
- Endpoint custom ou Query standard avec paramètres

**Prochaine étape**
→ `wordpress-gutenberg-expert/agents/blocks/filterable-grid`
```

---

## Output : Spécifications Mapping

```markdown
# Mapping Gutenberg - [Nom Composant]

## 1. Contexte (de clarification-composant)

- **Objectif** : [Résumé]
- **Layout** : [Slider/Grille/Liste]
- **Source** : [CPT/Posts/Statique]
- **Interactions** : [Liste]

## 2. Décision Technique

| Aspect | Choix | Alternative Écartée | Justification |
|--------|-------|---------------------|---------------|
| Type | [Block custom/Query Loop/Pattern] | [X] | [Pourquoi] |
| Rendu | [Statique/Dynamique/Hybride] | [X] | [Pourquoi] |
| Librairie | [Swiper/Splide/Aucune] | [X] | [Pourquoi] |

## 3. Spécifications Block

### Manifest (block.json)
- **name** : `namespace/block-name`
- **title** : [Titre affiché]
- **category** : [Catégorie]
- **supports** : [align, spacing, color, ...]

### Attributs
| Nom | Type | Défaut | UI Control |
|-----|------|--------|------------|
| [attr] | [type] | [value] | [control] |

### Structure Fichiers
```
blocks/{nom}/
├── block.json
├── edit.js
├── [save.js | render.php]
├── style.scss
└── [view.js]
```

## 4. Dépendances

- [ ] CPT existant : [Oui/Non - lequel]
- [ ] Taxonomie existante : [Oui/Non - laquelle]
- [ ] Librairie JS : [Oui/Non - laquelle]
- [ ] Patterns requis : [Oui/Non - lesquels]

## 5. Exceptions Projet

| Standard | Exception | Justification |
|----------|-----------|---------------|
| [Règle] | [Exception] | [Pourquoi] |

## 6. Prochaine Étape

→ Déléguer à `wordpress-gutenberg-expert/agents/blocks/{type-block}`

**Issue à créer** : Utiliser template `issue-management.md` → Block Request
```

---

## Références

| Niveau | Agent |
|--------|-------|
| POURQUOI | `direction-technique/specification/clarification-composant` |
| QUOI | `wordpress-data-mapping` (si CPT à créer) |
| COMMENT | `wordpress-gutenberg-expert/agents/blocks/*` |
| COMMENT | `wordpress-gutenberg-expert/agents/tooling/issue-management` |

## Livrables

| Livrable | Description |
|----------|-------------|
| Block Mapping Document | Documentation du mapping composants vers blocks Gutenberg |
| Block Specifications | Spécifications techniques de chaque block custom avec attributs |
| Block Architecture | Architecture des blocks avec dépendances et interactions |
