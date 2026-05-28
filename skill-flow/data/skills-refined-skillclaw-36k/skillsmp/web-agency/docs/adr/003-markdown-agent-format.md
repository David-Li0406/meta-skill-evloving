# ADR-003 : Format Markdown pour les Agents

## Statut

Accepté

## Contexte

Les agents doivent être définis dans un format qui :
- Est lisible par les humains
- Est parsable par les outils de test
- Supporte les métadonnées (nom, description)
- Permet une structure claire

Formats considérés : JSON, YAML, Markdown, XML, format custom.

## Décision

Utiliser le **format Markdown avec frontmatter YAML** pour définir les agents :

```markdown
---
name: collecte-besoin
description: Collecte et extraction des informations client
---

# Agent Collecte Besoin

Tu es spécialisé dans **[responsabilité]**.

## Ta Responsabilité Unique

> [Description]

Tu NE fais PAS :
- [Délégation 1]
- [Délégation 2]

## Template de Sortie

```markdown
# Output
[Format attendu]
```
```

### Structure Imposée

| Section | Obligatoire | Description |
|---------|-------------|-------------|
| Frontmatter YAML | ✅ | `name` et `description` |
| Ta Responsabilité Unique | ✅ | Définition SRP |
| Tu NE fais PAS | ✅ | Délégations explicites |
| Template de Sortie | ✅ | Format de l'output |
| Input Attendu | ⬜ | Types d'entrées |
| Processus | ⬜ | Étapes de traitement |

## Conséquences

### Positives

- **Lisibilité** : Markdown natif, lisible sans outil
- **Familiarité** : Format connu de tous les développeurs
- **Métadonnées** : Frontmatter YAML pour les propriétés
- **Versioning** : Diff Git lisible
- **Testabilité** : Regex simple pour parser les sections
- **Documentation intégrée** : Le fichier EST la documentation

### Négatives

- **Parsing complexe** : Markdown n'a pas de schéma strict
- **Validation manuelle** : Pas de validation native des sections
- **Structure flexible** : Risque de dérive du format

## Alternatives Considérées

### 1. JSON/YAML pur

```yaml
name: collecte-besoin
description: ...
responsibility: ...
delegations:
  - agent: formalisation-brief
    reason: ...
```

**Rejeté car** :
- Moins lisible pour les longues descriptions
- Difficile d'inclure des exemples markdown
- Perte de la documentation intégrée

### 2. Format custom (.agent)

Un format spécifique au projet.

**Rejeté car** :
- Courbe d'apprentissage
- Pas d'outillage existant
- Maintenance du parser

### 3. Fichiers séparés (meta.yaml + content.md)

Séparer métadonnées et contenu.

**Rejeté car** :
- Double maintenance
- Risque de désynchronisation
- Plus de fichiers à gérer

## Validation

Les tests valident automatiquement :

```javascript
// validate-agents.test.js
- Présence frontmatter (name, description)
- Section "Ta Responsabilité Unique"
- Section "Tu NE fais PAS"
- Longueur minimale du contenu
```

## Évolution Future

Si le format devient insuffisant :
1. Migrer vers MDX pour composants interactifs
2. Ajouter un schéma JSON pour validation stricte
3. Créer un langage DSL si nécessaire

Pour l'instant, Markdown avec conventions suffit.
