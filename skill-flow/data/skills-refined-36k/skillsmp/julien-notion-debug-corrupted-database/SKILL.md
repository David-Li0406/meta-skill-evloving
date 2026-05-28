---
name: julien-notion-debug-corrupted-database
version: 1.0.0
description: Diagnoses and repairs corrupted Notion databases. Use when database entries show "Oops! Something went wrong", queryCollection returns 400, or MCP validation errors occur.
author: Julien
license: Apache-2.0
tags: [notion, debug, corruption, database, repair, diagnostic]
allowed-tools: [Read, Bash, Grep, Glob, Edit, Write]
triggers:
  # French
  - "database corrompue"
  - "base de données cassée"
  - "notion erreur"
  - "réparer database"
  - "debug database notion"
  - "entrée ne s'ouvre pas"
  - "queryCollection échoue"
  # English
  - "corrupted database"
  - "broken database"
  - "notion error"
  - "oops something went wrong"
  - "can't open database entry"
  - "queryCollection fails"
  - "MCP validation_error"
  - "database 400 error"
  - "fix notion database"
  - "debug notion collection"
---

# Notion Database Corruption Debugger

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-notion-debug-corrupted-database" activated
📊 Running database corruption diagnostic...
```

## Description

Guide complet pour diagnostiquer et réparer les bases de données Notion corrompues.
Basé sur un cas réel de corruption qui bloquait l'ouverture des entrées de database.

---

## Symptômes de Corruption

### 1. Erreur "Oops! Something went wrong"
- Apparaît quand on clique sur une entrée de database (ouverture en modal/side panel)
- La page fonctionne en accès direct (URL complète) mais pas depuis la vue database

### 2. Erreur MCP/API "validation_error"
```json
{
  "code": "validation_error",
  "message": "Expected value to never occur: {\"name\":\"PropertyName\",\"type\":\"rich_text\"}"
}
```

### 3. queryCollection retourne 400
```
[queryCollection] Something went wrong. (400)
```

### 4. Impossibilité de modifier la collection
Toute tentative de `saveTransactionsFanout` échoue avec 400 ou 500.

---

## Checklist de Diagnostic

### Étape 1: Vérifier le Schema

```python
async def check_schema(api, collection_id):
    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'collection', 'id': collection_id}, 'version': -1}]
    })

    coll = result.get('recordMap', {}).get('collection', {}).get(collection_id, {})
    schema = coll.get('value', {}).get('value', {}).get('schema', {})

    issues = []
    for pid, pdata in schema.items():
        # CHECK 1: ID trop long (format UUID au lieu de 4 chars)
        if len(pid) > 20:
            issues.append(f"UUID-style ID: {pid} ({pdata.get('name')})")

        # CHECK 2: Type manquant
        if not pdata.get('type'):
            issues.append(f"Missing type: {pid}")

        # CHECK 3: Nom manquant (sauf title)
        if not pdata.get('name') and pid != 'title':
            issues.append(f"Missing name: {pid}")

    return issues
```

**Problèmes courants:**
- **ID au format UUID** (`99b7d827-8fab-4d9d-9eec-da3dbba31784`) au lieu de 4 chars (`FT\`f`)
- **Type non supporté** ou mal formé

### Étape 2: Vérifier le deleted_schema

```python
async def check_deleted_schema(api, collection_id):
    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'collection', 'id': collection_id}, 'version': -1}]
    })

    coll = result.get('recordMap', {}).get('collection', {}).get(collection_id, {})
    deleted_schema = coll.get('value', {}).get('value', {}).get('deleted_schema', {})

    if deleted_schema:
        print(f"deleted_schema contient {len(deleted_schema)} propriétés supprimées:")
        for pid, pdata in deleted_schema.items():
            flag = "LONG ID" if len(pid) > 20 else ""
            print(f"  {pid}: {pdata.get('name')} ({pdata.get('type')}) {flag}")

    return deleted_schema
```

**Le `deleted_schema` peut contenir des propriétés corrompues qui bloquent les opérations!**

### Étape 3: Vérifier le Format de la Collection

```python
async def check_collection_format(api, collection_id):
    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'collection', 'id': collection_id}, 'version': -1}]
    })

    coll = result.get('recordMap', {}).get('collection', {}).get(collection_id, {})
    format_data = coll.get('value', {}).get('value', {}).get('format', {})

    issues = []

    # CHECK 1: Clés numériques (array mal converti en dict)
    numeric_keys = [k for k in format_data.keys() if k.isdigit()]
    if numeric_keys:
        issues.append(f"Numeric keys in format: {numeric_keys}")

    # CHECK 2: property_visibility avec refs orphelines
    schema_keys = set(schema.keys())
    schema_keys.add('title')

    for item in format_data.get('property_visibility', []):
        if isinstance(item, dict):
            pid = item.get('property')
            if pid and pid not in schema_keys:
                issues.append(f"Orphan in property_visibility: {pid}")

    # CHECK 3: collection_page_properties avec refs orphelines
    for item in format_data.get('collection_page_properties', []):
        if isinstance(item, dict):
            pid = item.get('property')
            if pid and pid not in schema_keys:
                issues.append(f"Orphan in collection_page_properties: {pid}")

    return issues
```

### Étape 4: Vérifier les Vues

```python
async def check_views(api, db_block_id, schema_keys):
    # Get view IDs
    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'block', 'id': db_block_id}, 'version': -1}]
    })

    block = result.get('recordMap', {}).get('block', {}).get(db_block_id, {})
    view_ids = block.get('value', {}).get('value', {}).get('view_ids', [])

    # Check each view
    for vid in view_ids:
        view_result = await api._client._post('syncRecordValuesMain', {
            'requests': [{'pointer': {'table': 'collection_view', 'id': vid}, 'version': -1}]
        })

        view = view_result.get('recordMap', {}).get('collection_view', {}).get(vid, {})
        format_data = view.get('value', {}).get('value', {}).get('format', {})

        # Check list_properties, table_properties, etc.
        for key in ['list_properties', 'table_properties', 'gallery_cover', 'board_cover_properties']:
            props = format_data.get(key, [])
            if isinstance(props, list):
                for p in props:
                    if isinstance(p, dict):
                        pid = p.get('property')
                        if pid and pid not in schema_keys:
                            print(f"View {vid[:8]}: orphan in {key}: {pid}")
```

---

## Réparations

### Fix 1: Nettoyer deleted_schema

**C'est souvent la cause principale!**

```python
async def clear_deleted_schema(api, collection_id):
    space_id = await api._client.ensure_space_id()

    operations = [{
        'pointer': {'table': 'collection', 'id': collection_id, 'spaceId': space_id},
        'command': 'set',
        'path': ['deleted_schema'],
        'args': {}  # Empty dict
    }]

    await api._client.execute_raw_transaction(operations)
```

### Fix 2: Nettoyer les références orphelines dans les vues

```python
async def clean_view_orphans(api, view_id, schema_keys):
    space_id = await api._client.ensure_space_id()

    # Get current view
    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'collection_view', 'id': view_id}, 'version': -1}]
    })

    view = result.get('recordMap', {}).get('collection_view', {}).get(view_id, {})
    format_data = view.get('value', {}).get('value', {}).get('format', {})

    # Clean each property list
    for key in ['list_properties', 'table_properties']:
        props = format_data.get(key, [])
        if isinstance(props, list):
            clean_props = [p for p in props if p.get('property') in schema_keys]

            if len(clean_props) < len(props):
                operations = [{
                    'pointer': {'table': 'collection_view', 'id': view_id, 'spaceId': space_id},
                    'command': 'set',
                    'path': ['format', key],
                    'args': clean_props
                }]
                await api._client.execute_raw_transaction(operations)
```

### Fix 3: Nettoyer property_visibility de la collection

```python
async def clean_collection_property_visibility(api, collection_id, schema_keys):
    space_id = await api._client.ensure_space_id()

    # Get current format
    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'collection', 'id': collection_id}, 'version': -1}]
    })

    coll = result.get('recordMap', {}).get('collection', {}).get(collection_id, {})
    format_data = coll.get('value', {}).get('value', {}).get('format', {})

    # Clean property_visibility
    prop_vis = format_data.get('property_visibility', [])
    if isinstance(prop_vis, list):
        clean_vis = [p for p in prop_vis if p.get('property') in schema_keys]

        operations = [{
            'pointer': {'table': 'collection', 'id': collection_id, 'spaceId': space_id},
            'command': 'update',
            'path': ['format'],
            'args': {'property_visibility': clean_vis}
        }]
        await api._client.execute_raw_transaction(operations)
```

### Fix 4: Supprimer les clés numériques du format

```python
async def remove_numeric_keys(api, collection_id):
    space_id = await api._client.ensure_space_id()

    # Get current format
    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'collection', 'id': collection_id}, 'version': -1}]
    })

    coll = result.get('recordMap', {}).get('collection', {}).get(collection_id, {})
    format_data = coll.get('value', {}).get('value', {}).get('format', {})

    numeric_keys = [k for k in format_data.keys() if k.isdigit()]

    for key in numeric_keys:
        operations = [{
            'pointer': {'table': 'collection', 'id': collection_id, 'spaceId': space_id},
            'command': 'set',
            'path': ['format', key],
            'args': None  # Remove the key
        }]
        await api._client.execute_raw_transaction(operations)
```

---

## Ordre de Réparation Recommandé

1. **Nettoyer deleted_schema** (souvent suffisant!)
2. **Nettoyer les vues** (références orphelines)
3. **Nettoyer property_visibility** de la collection
4. **Supprimer les clés numériques** du format
5. **Si toujours bloqué**: Migration vers nouvelle DB

---

## Cas Non Réparables

Si la propriété corrompue est dans le **schema principal** avec un ID UUID-style, il peut être impossible de la supprimer via l'API. Dans ce cas:

1. **Contacter le support Notion** - Ils peuvent réparer côté serveur
2. **Migration** - Créer nouvelle DB et migrer les données

### Script de Migration

```python
async def migrate_database(api, old_collection_id, new_parent_id):
    # 1. Get all entries via search (queryCollection peut être cassé)
    all_entries = []
    queries = ['', 'a', 'e', 'i', 'o', 'http', 'github']

    for q in queries:
        results = await api.search.search(SearchParams(
            query=q,
            filters=SearchFilters(ancestors=[old_db_block_id]),
            limit=100
        ))
        for r in results.results:
            all_entries.add(r.id)

    # 2. Fetch full data for each entry
    # 3. Create new database with clean schema
    # 4. Copy entries (properties + content)
```

---

## Debugging Tips

### Accès Direct vs Modal
- Si une page fonctionne via URL directe mais pas en modal depuis la DB, le problème est dans la collection/vue, pas dans la page elle-même.

### API Interne vs Officielle
- L'API Officielle (MCP) est plus stricte sur la validation
- L'API Interne peut parfois réussir là où l'Officielle échoue
- Utiliser `syncRecordValuesMain` pour lire, `saveTransactionsFanout` pour écrire

### Test Minimal
Pour vérifier si la collection accepte des modifications:
```python
operations = [{
    'pointer': {'table': 'collection', 'id': collection_id, 'spaceId': space_id},
    'command': 'update',
    'path': ['schema', 'title'],
    'args': {'name': 'Name', 'type': 'title'}
}]
await api._client.execute_raw_transaction(operations)
```

Si cette opération minimale échoue, la collection est profondément corrompue.

---

## Ressources

- **Notion Internal API Guide**: `.claude/skills/notion-internal-api-guide/`
- **SDK Notion Uploader**: `core/api/clients/databases.py`
- **HydraSpecter**: Pour validation visuelle des réparations

---

## Skill Chaining

### Skills Required Before
- **notion-internal-api-guide** (recommended): Understand Notion Internal API structure
- **notion-fetch-url** (optional): To fetch database info from URL

### Input Expected
- **Database block ID** (UUID format): `afbf024b-2d2c-49eb-b035-99a4d495f19f`
- OR **Notion URL**: `https://www.notion.so/workspace/database-id?v=...`
- Access to NotionAPI from the SDK

### Output Produced
- **Format**: Diagnostic report with issues list and severity
- **Side effects**:
  - May clear `deleted_schema` (repair)
  - May clean orphan properties from views
  - May clean `property_visibility` in collection format
- **Duration**: 1-5 minutes depending on database size

### Compatible Skills After
- **notion-sdk**: For further database operations after repair
- **HydraSpecter**: Visual validation that entries open correctly

### Tools Used
- `Read` (usage: read SDK files for API patterns)
- `Bash` (usage: run `debug_database.py` diagnostic script)
- `Grep` (usage: search for corruption patterns in API responses)

### Visual Workflow

```
User: "Ma database est corrompue / Database shows error"
    ↓
[THIS SKILL]
    ├─► Get database block ID
    ├─► Run diagnostic (6 checks)
    │   ├─ Schema (UUID-style IDs, missing type)
    │   ├─ deleted_schema (corrupted entries)
    │   ├─ Collection format (orphan refs)
    │   ├─ Views (orphan properties)
    │   ├─ queryCollection test
    │   └─ Minimal update test
    ├─► Generate issue report
    └─► Suggest repairs
    ↓
Issues found?
    YES → Execute repairs (with approval)
    │   ├─ 1. Clear deleted_schema (most common fix!)
    │   ├─ 2. Clean view orphans
    │   ├─ 3. Clean property_visibility
    │   └─ 4. Remove numeric keys
    NO  → Database is healthy ✅
    ↓
Still broken?
    YES → Contact Notion support / Migrate data
    NO  → Done ✅
```

### Usage Example

**Scenario**: Database entries show "Oops! Something went wrong"

**Command**:
```bash
python debug_database.py afbf024b-2d2c-49eb-b035-99a4d495f19f
```

**Result**:
```
[2/6] Checking deleted_schema...
  Found 2 issues
--- HIGH SEVERITY ISSUES ---
  [DELETED_SCHEMA_ENTRY] Deleted property 'Conv_ID' (rich_text) - HAS UUID-STYLE ID

RECOMMENDATIONS
1. CLEAR deleted_schema (often fixes the issue!)
```

**Fix**:
```python
await fix_deleted_schema(api, collection_id)
# Result: Database entries open correctly again ✅
```
