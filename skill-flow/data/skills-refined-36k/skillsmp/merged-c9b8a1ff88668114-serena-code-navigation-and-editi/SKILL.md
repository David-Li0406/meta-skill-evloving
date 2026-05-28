---
name: serena-code-navigation-and-editing
description: Use this skill for precise code exploration and editing by targeting symbols in the project without reading entire files.
---

# Serena Code Navigation and Editing

## Objectif

Explorer et modifier le code du projet MyGGV GPS de manière efficace en utilisant la navigation symbolique et l'édition ciblée.

## Périmètre

### Inclus
- Vue d'ensemble des symboles d'un fichier
- Recherche de symboles par nom ou pattern
- Navigation vers les définitions
- Trouver les références d'un symbole
- Modifier le corps d'une fonction/hook
- Renommer un symbole
- Ajouter ou supprimer un symbole

### Exclus
- Lecture de fichiers complets → éviter, utiliser les symboles
- Mémoire projet → utiliser `serena-memory`
- Création de nouveaux fichiers → utiliser `Write`

## Outils Disponibles

### Exploration
1. **get_symbols_overview**: Vue d'ensemble des symboles d'un fichier.
   ```javascript
   mcp__serena__get_symbols_overview({ file_path: "src/hooks/useRouteManager.js" })
   ```

2. **find_symbol**: Trouver un symbole spécifique.
   ```javascript
   mcp__serena__find_symbol({ symbol_name: "useNavigationState" })
   ```

3. **search_for_pattern**: Recherche par pattern regex.
   ```javascript
   mcp__serena__search_for_pattern({ pattern: "use.*Map.*", file_types: ["js", "jsx"] })
   ```

4. **get_symbol_references**: Où un symbole est-il utilisé ?
   ```javascript
   mcp__serena__get_symbol_references({ symbol_name: "haversineDistance" })
   ```

### Édition
1. **replace_symbol_body**: Remplacer le contenu d'une fonction.
   ```javascript
   mcp__serena__replace_symbol_body({
     symbol_name: "getPolygonCenter",
     file_path: "src/hooks/useMapConfig.js",
     new_body: `...`
   })
   ```

2. **rename_symbol**: Renommer un symbole partout dans le projet.
   ```javascript
   mcp__serena__rename_symbol({ old_name: "handleArrival", new_name: "onDestinationReached", scope: "project" })
   ```

3. **add_symbol**: Ajouter une nouvelle fonction/constante.
   ```javascript
   mcp__serena__add_symbol({
     file_path: "src/utils/geoUtils.js",
     symbol_type: "function",
     symbol_name: "calculateMidpoint",
     body: `...`
   })
   ```

4. **delete_symbol**: Supprimer un symbole.
   ```javascript
   mcp__serena__delete_symbol({ symbol_name: "unusedHelper", file_path: "src/utils/geoUtils.js" })
   ```

## Workflow d'Exploration et d'Édition

### Comprendre un fichier
```
1. get_symbols_overview → Liste des symboles
2. find_symbol → Détails d'un symbole intéressant
3. get_related_symbols → Dépendances
```

### Modifier une fonction existante
```
1. find_symbol → Vérifier la signature actuelle
2. replace_symbol_body → Appliquer les changements
3. Vérifier le build (npm run build)
```

### Refactoring avec renommage
```
1. get_symbol_references → Voir l'impact
2. rename_symbol → Renommer partout
3. Vérifier les imports
```

### Ajouter une nouvelle fonctionnalité
```
1. get_symbols_overview → Voir la structure du fichier
2. add_symbol → Ajouter le nouveau code
3. Mettre à jour les exports si nécessaire
```

## Bonnes Pratiques

1. **Toujours commencer par get_symbols_overview** avant de chercher ou modifier.
2. **Tester après chaque modification** avec `npm run build`.
3. **Utiliser rename_symbol** plutôt que rechercher-remplacer manuel.
4. **Préserver les exports** lors de modifications.

## Anti-Patterns

❌ **Ne pas faire :**
```javascript
// Lire un fichier entier pour trouver une fonction
Read({ file_path: "src/lib/navigation.js" })  // 1248 lignes !
```

✅ **Faire :**
```javascript
// Cibler directement
mcp__serena__find_symbol({ symbol_name: "createRoute" })
```

❌ **Ne pas faire :**
```javascript
// Réécrire tout le fichier pour changer une fonction
Write({ file_path: "src/utils/geoUtils.js", content: "... 200 lignes ..." })
```

✅ **Faire :**
```javascript
// Cibler précisément
mcp__serena__replace_symbol_body({ symbol_name: "targetFunction", new_body: "... juste le nouveau corps ..." })
```