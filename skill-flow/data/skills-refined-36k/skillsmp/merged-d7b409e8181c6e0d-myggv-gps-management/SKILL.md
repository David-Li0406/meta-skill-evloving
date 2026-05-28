---
name: myggv-gps-management
description: Use this skill for managing the MyGGV GPS project, including database operations and project documentation.
---

# MyGGV GPS Management

## Objectif

Gérer le projet MyGGV GPS, incluant la gestion de la base de données Supabase et la documentation du projet dans Archon.

## Périmètre

### Inclus

- **Base de données Supabase** :
  - Exécution de requêtes SQL
  - Création et application de migrations
  - Listing des tables et extensions
  - Vérification des advisors (sécurité, performance)
  - Consultation des logs
  - Génération des types TypeScript

- **Gestion de projet dans Archon** :
  - Gestion des tâches (todo, doing, review, done)
  - Documentation de projet (specs, notes, guides)
  - Recherche dans la knowledge base

### Exclus

- Documentation Supabase → utiliser Archon
- Déploiement → utiliser `netlify-deploy`
- Code de navigation → utiliser `maplibre-navigation`

## Workflow de Gestion de Base de Données

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
     name: "<migration_name>",
     query: "<migration_query>"
   })
3. Vérifier avec execute_sql
```

### Requête de données

```
mcp__supabase__execute_sql({
  query: "<sql_query>"
})
```

## Workflow de Gestion de Projet

### Trouver le projet

```javascript
mcp__archon__find_projects({
  query: "ggv gps",
});
```

### Créer/Mettre à jour le projet

```javascript
mcp__archon__manage_project({
  action: "create",
  title: "MyGGV GPS",
  description: "Application GPS web pour Garden Grove Village",
  github_repo: "<github_repo_url>",
});
```

### Gérer les tâches

```javascript
// Créer une tâche
mcp__archon__manage_task({
  action: "create",
  project_id: "<project-id>",
  title: "<task_title>",
  description: "<task_description>",
  status: "todo",
  feature: "<feature_name>",
});

// Mettre à jour le statut
mcp__archon__manage_task({
  action: "update",
  task_id: "<task-id>",
  status: "doing",
});
```

## Bonnes Pratiques

1. **Toujours vérifier les advisors** après une migration DDL
2. **Utiliser des noms snake_case** pour les migrations
3. **Ne jamais hardcoder d'IDs** dans les migrations de données
4. **Queries RAG courtes** : 2-5 mots-clés max
5. **Une tâche "doing" à la fois** : Focus sur une seule chose
6. **Documenter les décisions** : Créer des documents pour les choix architecturaux

## Variables d'Environnement

Le projet utilise :

- `VITE_SUPABASE_URL` - URL du projet Supabase
- `VITE_SUPABASE_ANON_KEY` - Clé publique (anon)

Ces variables sont configurées dans `.env` et sur Netlify.