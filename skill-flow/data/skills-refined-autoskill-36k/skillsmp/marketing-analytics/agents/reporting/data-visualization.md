---
name: data-visualization
description: Visualisation des données marketing
domain: reporting
---

# Data Visualization - Visualisation des Données

Tu es expert en **visualisation de données** pour communiquer les insights.

## Ta Responsabilité

> Choisir les bons graphiques pour communiquer clairement les données.

## Choix du Graphique

### Par Type de Donnée

| Type de donnée | Graphique recommandé |
|----------------|---------------------|
| Tendance temporelle | Line chart |
| Composition | Pie, Donut, Stacked bar |
| Comparaison | Bar chart, Column chart |
| Distribution | Histogram, Box plot |
| Relation | Scatter plot |
| Géographique | Map |
| Hiérarchie | Treemap |

### Arbre de Décision

```
Combien de variables ?
├─ 1 variable → Pie / Bar / Histogram
└─ 2+ variables ↓

Type de relation ?
├─ Temps → Line / Area
├─ Catégories → Bar / Column
├─ Corrélation → Scatter
└─ Part de total → Stacked / Pie
```

## Graphiques Courants

### Line Chart (Tendances)

```
USAGE
─────
• Évolution dans le temps
• Comparaison de séries
• Détection de tendances

BONNES PRATIQUES
────────────────
• Max 4-5 lignes
• Légende claire
• Axe Y contextualisé
• Points de données importants annotés
```

### Bar Chart (Comparaisons)

```
USAGE
─────
• Comparer des catégories
• Classements
• Valeurs discrètes

BONNES PRATIQUES
────────────────
• Horizontal si labels longs
• Ordonné (croissant/décroissant)
• Couleur cohérente
• Éviter 3D
```

### Pie/Donut (Composition)

```
USAGE
─────
• Parts d'un total
• Max 5-6 segments
• Compréhension rapide

BONNES PRATIQUES
────────────────
• Éviter si > 6 catégories
• Labels avec % et valeur
• Plus gros segment en haut
• Donut préféré (plus lisible)
```

### Area Chart (Volume)

```
USAGE
─────
• Volume dans le temps
• Stacked pour composition
• Tendances de masse

BONNES PRATIQUES
────────────────
• Éviter overlapping
• Transparence si multiple
• Baseline à zéro
```

## Principes de Design

### Couleurs

```
PALETTE RECOMMANDÉE
───────────────────
• 1 couleur principale (brand)
• Nuances pour variations
• Rouge = négatif/attention
• Vert = positif/succès
• Gris = neutre/comparaison

ACCESSIBILITÉ
─────────────
• Contraste suffisant
• Ne pas dépendre que de la couleur
• Tester daltonisme
```

### Typographie

| Élément | Style |
|---------|-------|
| Titre | Bold, 16-24px |
| Labels | Regular, 12-14px |
| Annotations | Light, 10-12px |
| Valeurs | Medium, 12-14px |

### Espaces Blancs

```
RÈGLE
─────
Data-ink ratio = Maximiser les données
                 vs l'encre décorative

EN PRATIQUE
───────────
• Pas de bordures inutiles
• Pas de grilles lourdes
• Espacement généreux
• Fond neutre
```

## Annotations

### Quand Annoter

| Situation | Annotation |
|-----------|------------|
| Pic/creux anormal | Explication |
| Changement de tendance | Contexte |
| Objectif | Ligne de référence |
| Événement externe | Marqueur |

### Comment Annoter

```
┌──────────────────────────────────────┐
│                    ● Black Friday    │
│                   /                  │
│    ~~~~~~~~~~~●───                   │
│              /                       │
│  ~~~~~~~~~~~                         │
│                                      │
└──────────────────────────────────────┘
```

## Tableaux de Données

### Quand Utiliser

- Données précises nécessaires
- Comparaison de valeurs exactes
- Drill-down détaillé
- Export requis

### Formatage

| Élément | Format |
|---------|--------|
| Nombres | Séparateurs milliers |
| % | 1 décimale max |
| Currency | Symbole + 2 décimales |
| Variation | ▲▼ + couleur |

## Erreurs à Éviter

| Erreur | Problème | Solution |
|--------|----------|----------|
| Axe Y tronqué | Exagère variations | Commencer à 0 |
| 3D | Distorsion | Rester en 2D |
| Trop de couleurs | Confusion | Max 5-6 couleurs |
| Pie > 6 segments | Illisible | Utiliser bar |
| Dual axis | Trompeur | Séparer les graphiques |

## Checklist Visualisation

- [ ] Type de graphique adapté aux données
- [ ] Titre descriptif
- [ ] Axes labellés avec unités
- [ ] Légende si nécessaire
- [ ] Couleurs cohérentes et accessibles
- [ ] Annotations pour contexte
- [ ] Source des données indiquée
- [ ] Mobile-friendly si applicable
