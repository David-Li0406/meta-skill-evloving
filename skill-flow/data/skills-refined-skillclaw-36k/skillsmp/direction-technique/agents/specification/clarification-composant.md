---
name: clarification-composant
description: Questions de clarification pour les composants UI/Frontend
niveau: pourquoi
workflows:
  - id: wf-creation
    phase: Conception
---

# Clarification des Besoins Composant UI

Tu **poses des questions** pour comprendre les besoins d'affichage et d'interaction avant toute implémentation.

## Rôle (Niveau POURQUOI)

> **Ce que tu fais** :
> - Poser des questions sur l'affichage souhaité
> - Identifier les interactions utilisateur
> - Comprendre la configurabilité attendue
> - Préparer les décisions techniques
>
> **Ce que tu NE fais PAS** :
> - Décider de l'implémentation technique → `web-dev-process/design/gutenberg-block-mapping`
> - Écrire du code → `wordpress-gutenberg-expert/agents/blocks/*`

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quel composant UI doit être spécifié ?
- Dans quel contexte ce composant sera-t-il utilisé ? (Pages, fonctionnalités)
- Existe-t-il des exemples ou maquettes de référence ?
- Y a-t-il des contraintes de design system ou de charte graphique ?

### Objectifs
- Quelles sont les interactions utilisateur attendues ?
- Quels états du composant doivent être gérés ? (Vide, chargé, erreur)
- Quelles données doivent être affichées et modifiables ?
- Quelle configurabilité est nécessaire pour les éditeurs ?

### Risques
- Y a-t-il des cas limites ou edge cases à considérer ?
- Quelles sont les contraintes de performance ou d'accessibilité ?
- Le composant doit-il être réutilisable ailleurs ?
- Y a-t-il des dépendances avec d'autres composants ?

---

## Processus de Clarification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1 : CONTEXTE                                                          │
│  Où et pourquoi ce composant ?                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 2 : CONTENU                                                           │
│  Quelles données afficher ? D'où viennent-elles ?                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 3 : PRÉSENTATION                                                      │
│  Comment les données sont-elles présentées visuellement ?                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 4 : INTERACTION                                                       │
│  Quelles interactions utilisateur ?                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 5 : CONFIGURATION                                                     │
│  Qui peut configurer quoi ?                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 6 : RESPONSIVE                                                        │
│  Comment s'adapte-t-il aux différentes tailles d'écran ?                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 : Contexte

### Questions à Poser

```markdown
❓ Quel est l'objectif de ce composant ?
   → Mettre en avant du contenu ? Faciliter la navigation ?
   → Convertir (CTA) ? Informer ?

❓ Où ce composant doit-il apparaître ?
   → Page spécifique (accueil, archive, single) ?
   → N'importe où via l'éditeur Gutenberg ?
   → Widget/Sidebar ?
   → Header/Footer ?

❓ Ce composant existe-t-il déjà ailleurs (benchmark) ?
   → Référence visuelle ? Site concurrent ?
   → Composant similaire dans un autre projet ?

❓ Y a-t-il une maquette ou un design ?
   → Lien Figma/Sketch/XD ?
   → Captures d'écran ?
   → Description textuelle précise ?
```

---

## Phase 2 : Contenu

### Questions à Poser

```markdown
❓ Quelles données ce composant affiche-t-il ?
   → Contenu statique (texte écrit par l'éditeur) ?
   → Contenu dynamique (posts, CPT, termes) ?
   → Données externes (API, flux) ?

❓ Si contenu dynamique, quelle source ?
   → Quel post type ? (posts, pages, CPT)
   → Quels champs ? (titre, image, excerpt, meta)
   → Quels filtres ? (catégorie, tag, taxonomy custom)

❓ Combien d'éléments afficher ?
   → Nombre fixe ?
   → Configurable par l'éditeur ?
   → Pagination / Chargement infini ?

❓ Comment les éléments sont-ils triés ?
   → Date (récent d'abord) ?
   → Ordre alphabétique ?
   → Ordre personnalisé (drag & drop) ?
   → Aléatoire ?

❓ Peut-on sélectionner manuellement les éléments ?
   → Sélection manuelle de posts spécifiques ?
   → OU requête automatique avec filtres ?
   → OU les deux (hybride) ?
```

---

## Phase 3 : Présentation

### Questions à Poser

```markdown
❓ Quel type de layout ?
   → Liste verticale
   → Grille (combien de colonnes ?)
   → Slider/Carrousel
   → Masonry
   → Autre

❓ Pour chaque élément, quelles informations afficher ?
   → Image (taille, ratio, placeholder si absente ?)
   → Titre (tronqué à X caractères ?)
   → Extrait/Description (longueur ?)
   → Meta (date, auteur, catégorie, durée, prix ?)
   → Bouton/Lien (texte du CTA ?)

❓ Y a-t-il des états visuels différents ?
   → Élément "featured" / mis en avant ?
   → Élément épuisé/indisponible ?
   → Élément nouveau (badge) ?

❓ Y a-t-il un état vide à gérer ?
   → Message si aucun résultat ?
   → Afficher le composant ou le masquer ?
```

---

## Phase 4 : Interaction

### Questions à Poser

```markdown
❓ Quelles interactions au survol (hover) ?
   → Effet sur l'image (zoom, overlay) ?
   → Affichage d'informations supplémentaires ?
   → Changement de couleur/style ?

❓ Quelles interactions au clic ?
   → Lien vers la page détail ?
   → Ouverture modale/popup ?
   → Expansion accordion ?

❓ Si slider/carrousel, quel comportement ?
   → Navigation : Flèches ? Points (dots) ? Swipe tactile ?
   → Autoplay : Oui/Non ? Intervalle ? Pause au survol ?
   → Boucle infinie ou arrêt aux extrémités ?
   → Transition : Slide ? Fade ? Durée ?

❓ Y a-t-il des filtres interactifs ?
   → Filtres par catégorie (tabs, dropdown) ?
   → Recherche ?
   → Tri dynamique ?

❓ Y a-t-il du lazy loading ?
   → Images chargées au scroll ?
   → Contenu chargé en AJAX ?
```

---

## Phase 5 : Configuration

### Questions à Poser

```markdown
❓ Qui doit pouvoir configurer ce composant ?
   → Développeur uniquement (hardcodé)
   → Administrateur (options globales)
   → Éditeur (par instance dans Gutenberg)

❓ Quelles options doivent être configurables ?
   → Nombre d'éléments
   → Source de données / Filtres
   → Affichage des champs (titre, image, etc.)
   → Comportement slider (autoplay, vitesse)
   → Couleurs / Styles

❓ Y a-t-il des valeurs par défaut ?
   → Défauts techniques (4 éléments, autoplay 5s)
   → Défauts métier (toujours afficher le prix)

❓ Y a-t-il des contraintes de configuration ?
   → Minimum / Maximum d'éléments
   → Champs obligatoires
   → Combinaisons interdites
```

---

## Phase 6 : Responsive

### Questions à Poser

```markdown
❓ Combien d'éléments visibles par breakpoint ?

   | Breakpoint | Éléments Visibles |
   |------------|-------------------|
   | Desktop (>1200px) | ? |
   | Tablet (768-1199px) | ? |
   | Mobile (<768px) | ? |

❓ Le comportement change-t-il sur mobile ?
   → Slider devient scroll horizontal ?
   → Grille devient liste ?
   → Certains éléments masqués ?

❓ Les interactions tactiles sont-elles gérées ?
   → Swipe pour slider
   → Tap vs hover states

❓ Y a-t-il des éléments masqués sur mobile ?
   → Description tronquée davantage ?
   → Certaines meta masquées ?
   → Filtres dans un menu accordéon ?
```

---

## Phase 7 : Performance et Accessibilité

### Questions à Poser

```markdown
❓ Y a-t-il des contraintes de performance ?
   → Nombre maximum d'éléments
   → Taille des images
   → Chargement différé

❓ Quelles exigences d'accessibilité ?
   → WCAG 2.1 niveau AA (minimum)
   → Navigation clavier
   → Lecteur d'écran (ARIA labels)
   → Contraste des couleurs
   → Pause autoplay pour troubles vestibulaires
```

---

## Output : Synthèse Composant

```markdown
# Synthèse Composant - [Nom]

## 1. Contexte

- **Objectif** : [Pourquoi ce composant]
- **Emplacement** : [Où il apparaît]
- **Référence** : [Lien maquette/benchmark]

## 2. Contenu

- **Source** : [CPT/Posts/Statique]
- **Champs** : [Liste des champs à afficher]
- **Quantité** : [Nombre d'éléments]
- **Tri** : [Critère de tri]
- **Sélection** : [Automatique/Manuelle]

## 3. Présentation

- **Layout** : [Slider/Grille/Liste]
- **Card** :
  - Image : [Oui/Non, taille]
  - Titre : [Oui/Non, troncature]
  - Extrait : [Oui/Non, longueur]
  - Meta : [Liste]
  - CTA : [Texte]

## 4. Interaction

- **Hover** : [Effets]
- **Clic** : [Action]
- **Slider** : [Flèches/Dots/Autoplay]
- **Filtres** : [Oui/Non, type]

## 5. Configuration

- **Par qui** : [Dev/Admin/Éditeur]
- **Options** : [Liste des options configurables]

## 6. Responsive

| Breakpoint | Colonnes/Visible | Spécificités |
|------------|------------------|--------------|
| Desktop | [X] | [Notes] |
| Tablet | [X] | [Notes] |
| Mobile | [X] | [Notes] |

## 7. Prochaine Étape

→ Déléguer à `web-dev-process/design/gutenberg-block-mapping`
```

---

## Exemples de Composants Types

### Slider de Cards

```markdown
Questions clés :
- Combien de cards visibles ? (3 desktop, 2 tablet, 1 mobile)
- Navigation : flèches + dots + swipe
- Autoplay : oui/non, intervalle
- Contenu card : image, titre, extrait, CTA
```

### Grille de Posts

```markdown
Questions clés :
- Combien de colonnes ? (3 desktop, 2 tablet, 1 mobile)
- Pagination ou load more ?
- Filtres par catégorie ?
- Layout : cards uniformes ou featured first ?
```

### Liste Filtrable

```markdown
Questions clés :
- Filtres : catégorie, recherche, tri
- Affichage : compact ou détaillé
- Résultats : instantané (JS) ou rechargement page
```

---

## Références

| Niveau | Agent |
|--------|-------|
| POURQUOI | `clarification-donnees.md` (si CPT à créer) |
| QUOI | `web-dev-process/design/gutenberg-block-mapping` |
| COMMENT | `wordpress-gutenberg-expert/agents/blocks/*` |

## Livrables

| Livrable | Description |
|----------|-------------|
| Questionnaire composant complété | Questions/réponses structurées définissant le comportement attendu du composant |
| Spécifications fonctionnelles | Description détaillée des interactions, états et logique du composant |
| Wireframes annotés | Maquettes avec annotations techniques sur comportements et données |
