"""
Notion Database Corruption Debugger

Usage:
    python debug_database.py <database_block_id>

Example:
    python debug_database.py afbf024b-2d2c-49eb-b035-99a4d495f19f
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "2025.09 Notion Uploader"))

from core.api import NotionAPI


async def get_collection_info(api, db_block_id: str) -> dict:
    """Get database block and collection info."""
    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'block', 'id': db_block_id}, 'version': -1}]
    })

    block = result.get('recordMap', {}).get('block', {}).get(db_block_id, {})
    val = block.get('value', {}).get('value', {})

    collection_id = val.get('collection_id')
    view_ids = val.get('view_ids', [])

    # Get collection
    if collection_id:
        coll_result = await api._client._post('syncRecordValuesMain', {
            'requests': [{'pointer': {'table': 'collection', 'id': collection_id}, 'version': -1}]
        })
        coll = coll_result.get('recordMap', {}).get('collection', {}).get(collection_id, {})
        coll_val = coll.get('value', {}).get('value', {})
    else:
        coll_val = {}

    return {
        'db_block_id': db_block_id,
        'collection_id': collection_id,
        'view_ids': view_ids,
        'schema': coll_val.get('schema', {}),
        'format': coll_val.get('format', {}),
        'deleted_schema': coll_val.get('deleted_schema', {}),
        'name': coll_val.get('name', [['Unknown']])[0][0] if isinstance(coll_val.get('name'), list) else 'Unknown'
    }


async def check_schema(schema: dict) -> list:
    """Check schema for corruption."""
    issues = []

    for pid, pdata in schema.items():
        pname = pdata.get('name', 'NO NAME')
        ptype = pdata.get('type', 'NO TYPE')

        # CHECK 1: UUID-style ID
        if len(pid) > 20:
            issues.append({
                'type': 'UUID_STYLE_ID',
                'property_id': pid,
                'property_name': pname,
                'property_type': ptype,
                'severity': 'HIGH',
                'message': f"Property '{pname}' has UUID-style ID instead of short ID"
            })

        # CHECK 2: Missing type
        if not pdata.get('type'):
            issues.append({
                'type': 'MISSING_TYPE',
                'property_id': pid,
                'property_name': pname,
                'severity': 'HIGH',
                'message': f"Property '{pname}' has no type"
            })

        # CHECK 3: Missing name (except title)
        if not pdata.get('name') and pid != 'title':
            issues.append({
                'type': 'MISSING_NAME',
                'property_id': pid,
                'severity': 'MEDIUM',
                'message': f"Property {pid} has no name"
            })

    return issues


async def check_deleted_schema(deleted_schema: dict) -> list:
    """Check deleted_schema for problematic entries."""
    issues = []

    for pid, pdata in deleted_schema.items():
        pname = pdata.get('name', 'NO NAME')
        ptype = pdata.get('type', 'NO TYPE')

        # Any entry in deleted_schema can cause issues
        issue = {
            'type': 'DELETED_SCHEMA_ENTRY',
            'property_id': pid,
            'property_name': pname,
            'property_type': ptype,
            'severity': 'MEDIUM',
            'message': f"Deleted property '{pname}' ({ptype}) in deleted_schema"
        }

        # UUID-style IDs are especially problematic
        if len(pid) > 20:
            issue['severity'] = 'HIGH'
            issue['message'] += " - HAS UUID-STYLE ID"

        # rich_text type can cause MCP issues
        if ptype == 'rich_text':
            issue['severity'] = 'HIGH'
            issue['message'] += " - rich_text type may block MCP"

        issues.append(issue)

    return issues


async def check_format(format_data: dict, schema_keys: set) -> list:
    """Check collection format for corruption."""
    issues = []

    # CHECK 1: Numeric keys (corrupted array)
    numeric_keys = [k for k in format_data.keys() if k.isdigit()]
    if numeric_keys:
        issues.append({
            'type': 'NUMERIC_KEYS',
            'keys': numeric_keys,
            'severity': 'MEDIUM',
            'message': f"Format has {len(numeric_keys)} numeric keys (corrupted array)"
        })

    # CHECK 2: Orphan refs in property_visibility
    prop_vis = format_data.get('property_visibility', [])
    if isinstance(prop_vis, list):
        for item in prop_vis:
            if isinstance(item, dict):
                pid = item.get('property')
                if pid and pid not in schema_keys:
                    issues.append({
                        'type': 'ORPHAN_PROPERTY_VISIBILITY',
                        'property_id': pid,
                        'severity': 'MEDIUM',
                        'message': f"Orphan property '{pid}' in property_visibility"
                    })

    # CHECK 3: Orphan refs in collection_page_properties
    cpp = format_data.get('collection_page_properties', [])
    if isinstance(cpp, list):
        for item in cpp:
            if isinstance(item, dict):
                pid = item.get('property')
                if pid and pid not in schema_keys:
                    issues.append({
                        'type': 'ORPHAN_PAGE_PROPERTIES',
                        'property_id': pid,
                        'severity': 'MEDIUM',
                        'message': f"Orphan property '{pid}' in collection_page_properties"
                    })

    return issues


async def check_views(api, view_ids: list, schema_keys: set) -> list:
    """Check all views for corruption."""
    issues = []

    if not view_ids:
        return issues

    # Fetch all views
    requests = [{'pointer': {'table': 'collection_view', 'id': vid}, 'version': -1} for vid in view_ids]
    result = await api._client._post('syncRecordValuesMain', {'requests': requests})

    for vid in view_ids:
        view = result.get('recordMap', {}).get('collection_view', {}).get(vid, {})
        val = view.get('value', {}).get('value', {})
        view_name = val.get('name', 'Unnamed')
        view_type = val.get('type', 'unknown')
        format_data = val.get('format', {})

        # Check property lists
        for key in ['list_properties', 'table_properties', 'gallery_cover', 'board_cover_properties']:
            props = format_data.get(key, [])
            if isinstance(props, list):
                for p in props:
                    if isinstance(p, dict):
                        pid = p.get('property')
                        if pid and pid not in schema_keys:
                            issues.append({
                                'type': 'ORPHAN_VIEW_PROPERTY',
                                'view_id': vid,
                                'view_name': view_name,
                                'view_type': view_type,
                                'property_id': pid,
                                'format_key': key,
                                'severity': 'MEDIUM',
                                'message': f"View '{view_name}' has orphan property '{pid}' in {key}"
                            })

    return issues


async def test_query(api, collection_id: str, view_id: str) -> bool:
    """Test if queryCollection works."""
    try:
        await api._client._post('queryCollection', {
            'collection': {'id': collection_id},
            'collectionView': {'id': view_id},
            'loader': {
                'type': 'reducer',
                'reducers': {
                    'collection_group_results': {'type': 'results', 'limit': 1}
                }
            }
        })
        return True
    except Exception:
        return False


async def test_minimal_update(api, collection_id: str) -> bool:
    """Test if minimal schema update works."""
    try:
        space_id = await api._client.ensure_space_id()
        operations = [{
            'pointer': {'table': 'collection', 'id': collection_id, 'spaceId': space_id},
            'command': 'update',
            'path': ['schema', 'title'],
            'args': {'name': 'Name', 'type': 'title'}
        }]
        await api._client.execute_raw_transaction(operations)
        return True
    except Exception:
        return False


async def diagnose(db_block_id: str):
    """Run full diagnostic on a database."""
    print("=" * 60)
    print("NOTION DATABASE CORRUPTION DIAGNOSTIC")
    print("=" * 60)

    async with NotionAPI() as api:
        # Get collection info
        print("\n[1/6] Getting collection info...")
        info = await get_collection_info(api, db_block_id)
        print(f"  Database: {info['name']}")
        print(f"  Collection ID: {info['collection_id']}")
        print(f"  Views: {len(info['view_ids'])}")
        print(f"  Schema properties: {len(info['schema'])}")
        print(f"  Deleted schema entries: {len(info['deleted_schema'])}")

        schema_keys = set(info['schema'].keys())
        schema_keys.add('title')

        all_issues = []

        # Check schema
        print("\n[2/6] Checking schema...")
        schema_issues = await check_schema(info['schema'])
        all_issues.extend(schema_issues)
        print(f"  Found {len(schema_issues)} issues")

        # Check deleted_schema
        print("\n[3/6] Checking deleted_schema...")
        deleted_issues = await check_deleted_schema(info['deleted_schema'])
        all_issues.extend(deleted_issues)
        print(f"  Found {len(deleted_issues)} issues")

        # Check format
        print("\n[4/6] Checking collection format...")
        format_issues = await check_format(info['format'], schema_keys)
        all_issues.extend(format_issues)
        print(f"  Found {len(format_issues)} issues")

        # Check views
        print("\n[5/6] Checking views...")
        view_issues = await check_views(api, info['view_ids'], schema_keys)
        all_issues.extend(view_issues)
        print(f"  Found {len(view_issues)} issues")

        # Test operations
        print("\n[6/6] Testing operations...")
        query_works = await test_query(api, info['collection_id'], info['view_ids'][0]) if info['view_ids'] else False
        print(f"  queryCollection: {'OK' if query_works else 'FAILS'}")

        update_works = await test_minimal_update(api, info['collection_id'])
        print(f"  Minimal update: {'OK' if update_works else 'FAILS'}")

        # Summary
        print("\n" + "=" * 60)
        print("DIAGNOSTIC SUMMARY")
        print("=" * 60)

        high_issues = [i for i in all_issues if i.get('severity') == 'HIGH']
        medium_issues = [i for i in all_issues if i.get('severity') == 'MEDIUM']

        print(f"\nTotal issues: {len(all_issues)}")
        print(f"  HIGH severity: {len(high_issues)}")
        print(f"  MEDIUM severity: {len(medium_issues)}")

        if high_issues:
            print("\n--- HIGH SEVERITY ISSUES ---")
            for issue in high_issues:
                print(f"  [{issue['type']}] {issue['message']}")

        if medium_issues:
            print("\n--- MEDIUM SEVERITY ISSUES ---")
            for issue in medium_issues[:10]:  # Limit output
                print(f"  [{issue['type']}] {issue['message']}")
            if len(medium_issues) > 10:
                print(f"  ... and {len(medium_issues) - 10} more")

        # Recommendations
        print("\n" + "=" * 60)
        print("RECOMMENDATIONS")
        print("=" * 60)

        if info['deleted_schema']:
            print("\n1. CLEAR deleted_schema (often fixes the issue!):")
            print("   Run: fix_deleted_schema(api, collection_id)")

        if view_issues:
            print("\n2. Clean orphan properties from views")

        if format_issues:
            print("\n3. Clean collection format (property_visibility, numeric keys)")

        if high_issues and not query_works and not update_works:
            print("\n4. If all else fails: MIGRATE to new database or contact Notion support")

        return {
            'info': info,
            'issues': all_issues,
            'query_works': query_works,
            'update_works': update_works
        }


# ============================================================
# REPAIR FUNCTIONS
# ============================================================

async def fix_deleted_schema(api, collection_id: str):
    """Clear deleted_schema."""
    space_id = await api._client.ensure_space_id()
    operations = [{
        'pointer': {'table': 'collection', 'id': collection_id, 'spaceId': space_id},
        'command': 'set',
        'path': ['deleted_schema'],
        'args': {}
    }]
    await api._client.execute_raw_transaction(operations)
    print("deleted_schema cleared!")


async def fix_view_orphans(api, view_id: str, schema_keys: set):
    """Remove orphan properties from a view."""
    space_id = await api._client.ensure_space_id()

    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'collection_view', 'id': view_id}, 'version': -1}]
    })

    view = result.get('recordMap', {}).get('collection_view', {}).get(view_id, {})
    format_data = view.get('value', {}).get('value', {}).get('format', {})

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
                print(f"Cleaned {len(props) - len(clean_props)} orphans from {key}")


async def fix_property_visibility(api, collection_id: str, schema_keys: set):
    """Clean property_visibility in collection format."""
    space_id = await api._client.ensure_space_id()

    result = await api._client._post('syncRecordValuesMain', {
        'requests': [{'pointer': {'table': 'collection', 'id': collection_id}, 'version': -1}]
    })

    coll = result.get('recordMap', {}).get('collection', {}).get(collection_id, {})
    format_data = coll.get('value', {}).get('value', {}).get('format', {})

    prop_vis = format_data.get('property_visibility', [])
    if isinstance(prop_vis, list):
        clean_vis = [p for p in prop_vis if p.get('property') in schema_keys]
        if len(clean_vis) < len(prop_vis):
            operations = [{
                'pointer': {'table': 'collection', 'id': collection_id, 'spaceId': space_id},
                'command': 'update',
                'path': ['format'],
                'args': {'property_visibility': clean_vis}
            }]
            await api._client.execute_raw_transaction(operations)
            print(f"Cleaned {len(prop_vis) - len(clean_vis)} orphans from property_visibility")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_database.py <database_block_id>")
        print("Example: python debug_database.py afbf024b-2d2c-49eb-b035-99a4d495f19f")
        sys.exit(1)

    db_id = sys.argv[1]
    asyncio.run(diagnose(db_id))
