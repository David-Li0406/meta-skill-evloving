#!/usr/bin/env python3
"""Clean ~/.claude.json to reduce file size."""

import json
import os
import shutil
import glob
from datetime import datetime, timedelta
from pathlib import Path

def create_backup(path: str) -> str:
    """Create timestamped backup, keep only last 3."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = f"{path}.backup-{timestamp}"
    shutil.copy(path, backup_path)

    # Clean old backups (keep last 3)
    backup_pattern = f"{path}.backup-*"
    backups = sorted(glob.glob(backup_pattern), reverse=True)
    for old_backup in backups[3:]:
        os.remove(old_backup)
        print(f"  Removed old backup: {os.path.basename(old_backup)}")

    return backup_path

def clean_caches(data: dict) -> tuple[dict, int]:
    """Clear all cache sections (safe, auto-regenerate)."""
    saved = 0
    cache_keys = [
        'cachedChangelog',
        'cachedStatsigGates',
        'cachedDynamicConfigs',
        'cachedGrowthBookFeatures',
    ]

    for key in cache_keys:
        if key in data:
            old_size = len(json.dumps(data[key]))
            if isinstance(data[key], list):
                data[key] = []
            elif isinstance(data[key], dict):
                data[key] = {}
            else:
                data[key] = None
            saved += old_size
            print(f"  Cleared '{key}' ({old_size:,} chars)")

    return data, saved

def clean_old_projects(data: dict, days: int = 30) -> tuple[dict, int]:
    """Remove project entries older than N days."""
    if 'projects' not in data:
        return data, 0

    saved = 0
    projects = data['projects']
    cutoff = datetime.now() - timedelta(days=days)
    cutoff_ts = cutoff.timestamp() * 1000  # JS timestamp

    old_size = len(json.dumps(projects))
    cleaned_projects = {}

    for path, project_data in projects.items():
        # Keep if has recent activity
        last_used = project_data.get('lastUsed', 0)
        if last_used > cutoff_ts:
            cleaned_projects[path] = project_data
        else:
            print(f"  Removed old project: {path[:50]}...")

    data['projects'] = cleaned_projects
    new_size = len(json.dumps(cleaned_projects))
    saved = old_size - new_size

    kept = len(cleaned_projects)
    removed = len(projects) - kept
    print(f"  Projects: kept {kept}, removed {removed} ({saved:,} chars saved)")

    return data, saved

def main():
    path = os.path.expanduser('~/.claude.json')

    if not os.path.exists(path):
        print("ERROR: ~/.claude.json not found")
        return

    print("=" * 60)
    print("CLAUDE.JSON CLEANUP")
    print("=" * 60)

    # Get initial size
    initial_size = os.path.getsize(path)
    print(f"\nInitial size: {initial_size:,} bytes ({initial_size // 1024} KB)")

    # Create backup
    print("\n[1/3] Creating backup...")
    backup_path = create_backup(path)
    print(f"  Backup: {os.path.basename(backup_path)}")

    # Load data
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_saved = 0

    # Clean caches (always safe)
    print("\n[2/3] Cleaning caches (safe)...")
    data, saved = clean_caches(data)
    total_saved += saved

    # Ask about projects
    print("\n[3/3] Cleaning old projects...")
    projects_size = len(json.dumps(data.get('projects', {})))
    if projects_size > 20000:
        print(f"  Projects section is large ({projects_size:,} chars)")
        data, saved = clean_old_projects(data, days=30)
        total_saved += saved
    else:
        print(f"  Projects section is reasonable ({projects_size:,} chars), skipping")

    # Save
    print("\nSaving...")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    final_size = os.path.getsize(path)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Before:  {initial_size:,} bytes ({initial_size // 1024} KB)")
    print(f"After:   {final_size:,} bytes ({final_size // 1024} KB)")
    print(f"Saved:   {initial_size - final_size:,} bytes ({(initial_size - final_size) / initial_size * 100:.1f}%)")
    print(f"\nBackup:  {backup_path}")

    # Check if now readable
    estimated_tokens = final_size // 4
    if estimated_tokens < 25000:
        print(f"\nFile should now be readable by Claude (~{estimated_tokens:,} tokens)")
    else:
        print(f"\nWARNING: Still large (~{estimated_tokens:,} tokens). May need manual cleanup.")

if __name__ == '__main__':
    main()
