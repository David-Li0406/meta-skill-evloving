---
name: julien-notion-todoDB-delete-done
description: Deletes all completed tasks (Done=true) from Notion Todos [DB]. Use when user wants to clean up finished todos, archive completed tasks, or purge done items from the todo database.
triggers:
  - "supprimer les tâches terminées"
  - "delete done todos"
  - "clean up todos"
  - "nettoyer les todos"
  - "purger les tâches faites"
  - "supprimer done"
  - "archiver les tâches terminées"
  - "vider les todos complétés"
---

# Delete Done Todos from Notion

Supprime toutes les tâches marquées "Done ?" = true de la base Todos [DB].

## Prérequis

1. Token API Notion dans `~/.env` ou `.env` local :
   ```
   NOTION_TOKEN=secret_xxxxx
   ```

2. Installer la dépendance :
   ```bash
   pip install notion-client
   ```

## Exécution

```bash
python scripts/delete_done_todos.py
```

### Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Liste les items sans supprimer |
| `--archive` | Archive au lieu de supprimer définitivement |
| `--older-than DAYS` | Supprime uniquement les items Done depuis plus de X jours |

### Exemples

```bash
# Voir ce qui serait supprimé
python scripts/delete_done_todos.py --dry-run

# Archiver les tâches terminées
python scripts/delete_done_todos.py --archive

# Supprimer les tâches terminées depuis plus de 30 jours
python scripts/delete_done_todos.py --older-than 30
```

## Configuration

Base de données cible :
- **Database ID**: `9c9b8dcd-e01b-488f-aa87-eaaed7be9a52`
- **Propriété filtrée**: `Done ?` (checkbox)

## Skill Chaining

### Skills Required Before
- None

### Input Expected
- Token Notion valide dans `.env`
- Accès à la base Todos [DB]

### Output Produced
- **Format**: Rapport console (nombre d'items supprimés)
- **Side effects**: Suppression/archivage des pages Notion
- **Duration**: ~1-5 minutes selon le nombre d'items

### Compatible Skills After
- Aucune

### Tools Used
- `Bash` (exécution du script Python)
- `Read` (vérification .env si besoin)
