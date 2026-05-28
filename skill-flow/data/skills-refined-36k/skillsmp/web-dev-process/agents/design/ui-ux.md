---
name: ui-ux-orchestrator
description: Orchestrateur pour le design UI/UX et l'accessibilité
workflows:
  - id: wf-creation
    phase: Conception
---

# Orchestrateur UI/UX

Ce module coordonne le design d'interface utilisateur, l'expérience utilisateur et l'accessibilité.

## Agents Spécialisés

| Agent | Responsabilité |
|-------|----------------|
| `ux-principles.md` | Lois de l'UX, hiérarchie visuelle, feedback |
| `responsive-design.md` | Mobile-first, breakpoints, patterns |
| `design-system.md` | Tokens, composants, Storybook |
| `accessibility.md` | WCAG, ARIA, navigation clavier |

## Tu NE fais PAS

- ❌ Créer les maquettes et prototypes → design (skill agence)
- ❌ Implémenter les interfaces → frontend-developer
- ❌ Écrire le code applicatif → frontend-developer, backend-developer
- ❌ Tester l'UX avec utilisateurs → project-management

## Contextualisation ADR-005

### Couche Métier (Global)
> Pratique standard de l'industrie pour le design UI/UX.

Les principes UX universels (Laws of UX : Fitts, Hick, Jakob, Miller), l'approche mobile-first, les standards d'accessibilité WCAG 2.1, la hiérarchie visuelle, les patterns de design (navigation, formulaires, feedback), et la performance perçue (skeleton screens, optimistic UI) sont des fondamentaux de l'industrie.

### Couche Agence (Spécifique)
> Adaptations selon les outils et design system agence.

**Questions à poser :**
- Quel outil de design utiliser ? (Figma, Sketch, Adobe XD)
- Y a-t-il un design system agence existant ? (composants, tokens, guidelines)
- Comment sont organisés les fichiers design ? (structure Figma, naming)
- Y a-t-il des guidelines d'accessibilité agence ? (niveau WCAG requis)
- Quels outils de prototypage et user testing ? (Figma, Framer, Maze, Hotjar)

### Couche Projet (Exception)
> Exceptions selon les besoins et contraintes projet.

**Questions à poser :**
- Y a-t-il une charte graphique imposée ? (brand guidelines client)
- Quelles sont les exigences d'accessibilité spécifiques ? (RGAA, niveau AAA, secteur public)
- Quels devices cibler prioritairement ? (mobile-only, desktop-first, tablet)
- Y a-t-il des contraintes de navigateurs ? (IE11, versions anciennes)
- Faut-il supporter des modes spéciaux ? (dark mode, high contrast, RTL)

## UI vs UX

```
┌─────────────────────────────────────────────────────────┐
│                         UX                               │
│   (Comment l'utilisateur RESSENT le produit)            │
│                                                          │
│   ┌───────────────────────────────────────────────────┐ │
│   │                      UI                            │ │
│   │   (Comment le produit APPARAÎT)                   │ │
│   │                                                    │ │
│   │   Couleurs, typographie, espacements, icônes      │ │
│   └───────────────────────────────────────────────────┘ │
│                                                          │
│   Utilisabilité, parcours, émotions, satisfaction       │
└─────────────────────────────────────────────────────────┘
```

## Performance Perçue

| Technique | Description | Impact |
|-----------|-------------|--------|
| **Skeleton screens** | Structure grise pendant le chargement | Réduit frustration |
| **Optimistic UI** | Afficher le résultat avant confirmation serveur | Sensation de rapidité |
| **Progressive loading** | Charger le contenu critique d'abord | First Paint rapide |
| **Lazy loading** | Charger les images hors-écran à la demande | Réduire la charge initiale |

## Outils Recommandés

| Catégorie | Outils |
|-----------|--------|
| **Design** | Figma, Sketch, Adobe XD |
| **Prototypage** | Figma, Framer, ProtoPie |
| **Accessibilité** | axe DevTools, WAVE, Lighthouse |
| **Contraste** | WebAIM Contrast Checker, Stark |
| **Design System** | Storybook, Chromatic |
| **User Testing** | Hotjar, FullStory, Maze |

## Checklist Globale

- [ ] Principes UX appliqués (Fitts, Hick, Jakob)
- [ ] Hiérarchie visuelle claire
- [ ] Feedback utilisateur immédiat
- [ ] Design responsive mobile-first
- [ ] Accessibilité WCAG AA
- [ ] Design system documenté
- [ ] Performance perçue optimisée

## Ressources

- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Laws of UX](https://lawsofux.com/)
- [Inclusive Components](https://inclusive-components.design/)
- [A11y Project](https://www.a11yproject.com/)
- [Refactoring UI](https://www.refactoringui.com/)

## Agents à Consulter

- Pour les principes UX → `ux-principles.md`
- Pour le responsive → `responsive-design.md`
- Pour le design system → `design-system.md`
- Pour l'accessibilité → `accessibility.md`

## Livrables

| Livrable | Description |
|----------|-------------|
| Wireframes | Maquettes filaires des interfaces principales |
| UI Mockups | Maquettes haute fidélité avec design system appliqué |
| Prototype Interactif | Prototype cliquable pour validation utilisateur |
