---
name: supabase-database
description: Gestion de la base de données Supabase pour MyGGV GPS. Utiliser pour les opérations SQL, migrations, tables et requêtes. NE PAS utiliser pour la documentation (utiliser archon-project).
allowed-tools:
  - mcp__supabase__execute_sql
  - mcp__supabase__apply_migration
  - mcp__supabase__list_tables
  - mcp__supabase__list_extensions
  - mcp__supabase__list_migrations
  - mcp__supabase__get_advisors
  - mcp__supabase__get_logs
  - mcp__supabase__get_project_url
  - mcp__supabase__get_publishable_keys
  - mcp__supabase__generate_typescript_types
---

# Supabase Database - MyGGV GPS

## Objectif

Gérer la base de données Supabase du projet MyGGV GPS : locations (blocs), POIs, et données de navigation.

## Périmètre

### Inclus

- Exécution de requêtes SQL (`execute_sql`)
- Création et application de migrations (`apply_migration`)
- Listing des tables et extensions
- Vérification des advisors (sécurité, performance)
- Consultation des logs
- Génération des types TypeScript

### Exclus

- Documentation Supabase → utiliser `archon-project`
- Déploiement → utiliser `netlify-deploy`

## Tables du Projet

### `locations`

Table principale contenant les blocs du village :

- `id` : UUID
- `name` : Nom du bloc (ex: "Block 1", "Block 2A")
- `coords` : Coordonnées du polygone (JSONB)
- `color` : Couleur d'affichage
- `created_at` : Timestamp

### `public_pois`

Points d'intérêt publics :

- `id` : UUID
- `name` : Nom du POI
- `type` : Type (school, church, pool, etc.)
- `coordinates` : [lng, lat]

## Workflow Type

### Vérifier l'état de la base

```
1. mcp__supabase__list_tables() - Lister les tables
2. mcp__supabase__get_advisors({ type: "security" }) - Vérifier RLS
3. mcp__supabase__get_advisors({ type: "performance" }) - Optimisations
```

### Créer une migration

```
1. Analyser le besoin
2. mcp__supabase__apply_migration({
     name: "add_poi_category",
     query: "ALTER TABLE public_pois ADD COLUMN category TEXT;"
   })
3. Vérifier avec execute_sql
```

### Requête de données

```
mcp__supabase__execute_sql({
  query: "SELECT * FROM locations WHERE name LIKE 'Block%' LIMIT 10;"
})
```

## Bonnes Pratiques

1. **Toujours vérifier les advisors** après une migration DDL
2. **Utiliser des noms snake_case** pour les migrations
3. **Ne jamais hardcoder d'IDs** dans les migrations de données
4. **Vérifier RLS** sur toutes les tables publiques

## Variables d'Environnement

Le projet utilise :

- `VITE_SUPABASE_URL` - URL du projet Supabase
- `VITE_SUPABASE_ANON_KEY` - Clé publique (anon)

Ces variables sont configurées dans `.env` et sur Netlify.
