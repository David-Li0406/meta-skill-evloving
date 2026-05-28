#!/usr/bin/env python3
"""
Manage documentation asset inventory CSV
Supports add, update, find, list, and sync operations
"""

import csv
import json
import os
import sys
from pathlib import Path
from datetime import datetime

class AssetInventory:
    def __init__(self, csv_path=None):
        """Initialize with CSV inventory file

        Args:
            csv_path: Path to inventory CSV. If None, auto-detects from:
                1. Script relative path (../documentation/documentation_assets.csv)
                2. Environment variable ASSET_INVENTORY_CSV
        """
        # Auto-detect CSV path if not provided
        if not csv_path:
            script_dir = Path(__file__).parent
            csv_path = script_dir.parent.parent.parent / 'documentation' / 'documentation_assets.csv'
            # Fallback to environment variable
            if not csv_path.exists():
                csv_path = os.environ.get('ASSET_INVENTORY_CSV', csv_path)

        self.csv_path = Path(csv_path)

        # CSV column schema
        self.fieldnames = [
            'filename',
            'r2_key',
            'production_url',
            'source_type',
            'file_type',
            'file_size',
            'file_size_bytes',
            'url_exists',
            'article_ids',
            'article_count',
            'last_modified',
            'etag',
            'ai_caption_alt',
            'ai_caption_descriptive',
            'ai_caption_seo',
            'needs_caption'
        ]

        # Create CSV if doesn't exist
        if not self.csv_path.exists():
            self._create_csv()

    def _create_csv(self):
        """Create new CSV with headers"""
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

    def add_asset(self, asset_data):
        """
        Add new asset to inventory

        Args:
            asset_data: dict with asset information

        Returns:
            dict with added record
        """
        # Ensure all fields present with defaults
        record = {field: asset_data.get(field, '') for field in self.fieldnames}

        # Auto-fill some fields if not provided
        if not record.get('last_modified'):
            record['last_modified'] = datetime.now().isoformat()

        if not record.get('source_type'):
            record['source_type'] = 'native'

        if not record.get('url_exists'):
            record['url_exists'] = True

        # Write to CSV
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(record)

        return record

    def find_asset(self, r2_key=None, filename=None, url=None):
        """
        Find asset by r2_key, filename, or URL

        Args:
            r2_key: R2 bucket key
            filename: Asset filename
            url: Production URL

        Returns:
            dict or None
        """
        if not self.csv_path.exists():
            return None

        with open(self.csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if r2_key and row.get('r2_key') == r2_key:
                    return row
                if filename and row.get('filename') == filename:
                    return row
                if url and row.get('production_url') == url:
                    return row

        return None

    def update_asset(self, r2_key, updates):
        """
        Update existing asset record

        Args:
            r2_key: R2 key to find asset
            updates: dict of fields to update

        Returns:
            bool (success)
        """
        if not self.csv_path.exists():
            return False

        rows = []
        updated = False

        with open(self.csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('r2_key') == r2_key:
                    row.update(updates)
                    row['last_modified'] = datetime.now().isoformat()
                    updated = True
                rows.append(row)

        if updated:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        return updated

    def delete_asset(self, r2_key):
        """Delete asset from inventory"""
        if not self.csv_path.exists():
            return False

        rows = []
        deleted = False

        with open(self.csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('r2_key') == r2_key:
                    deleted = True
                else:
                    rows.append(row)

        if deleted:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        return deleted

    def get_all_assets(self):
        """Get all assets as list of dicts"""
        if not self.csv_path.exists():
            return []

        assets = []
        with open(self.csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            assets = list(reader)
        return assets

    def get_statistics(self):
        """Get inventory statistics"""
        assets = self.get_all_assets()

        stats = {
            'total_assets': len(assets),
            'by_source_type': {},
            'by_file_type': {},
            'with_captions': 0,
            'missing_captions': 0,
            'active_assets': 0,
            'orphaned_assets': 0,
            'missing_assets': 0
        }

        for asset in assets:
            # Count by source type
            source = asset.get('source_type', 'unknown')
            stats['by_source_type'][source] = stats['by_source_type'].get(source, 0) + 1

            # Count by file type
            ftype = asset.get('file_type', 'unknown')
            stats['by_file_type'][ftype] = stats['by_file_type'].get(ftype, 0) + 1

            # Count captions
            if asset.get('ai_caption_alt'):
                stats['with_captions'] += 1
            elif asset.get('needs_caption') == 'yes':
                stats['missing_captions'] += 1

            # Count by type
            if source == 'native':
                stats['active_assets'] += 1
            elif source == 'orphaned':
                stats['orphaned_assets'] += 1
            elif source == 'missing':
                stats['missing_assets'] += 1

        return stats


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Manage asset inventory')
    parser.add_argument('--action', required=True,
                       choices=['add', 'find', 'update', 'delete', 'list', 'stats'],
                       help='Action to perform')
    parser.add_argument('--r2-key', help='R2 bucket key')
    parser.add_argument('--filename', help='Asset filename')
    parser.add_argument('--url', help='Production URL')
    parser.add_argument('--data', help='JSON data for add/update')
    parser.add_argument('--csv',
                       help='CSV inventory file path (default: auto-detect)')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    try:
        inventory = AssetInventory(args.csv)

        if args.action == 'add':
            if not args.data:
                parser.error('--data required for add action')
            data = json.loads(args.data)
            result = inventory.add_asset(data)
            print(json.dumps({'success': True, 'record': result}, indent=2))

        elif args.action == 'find':
            result = inventory.find_asset(
                r2_key=args.r2_key,
                filename=args.filename,
                url=args.url
            )
            if result:
                print(json.dumps({'success': True, 'record': result}, indent=2))
            else:
                print(json.dumps({'success': False, 'error': 'Asset not found'}, indent=2))
                sys.exit(1)

        elif args.action == 'update':
            if not args.r2_key or not args.data:
                parser.error('--r2-key and --data required for update action')
            data = json.loads(args.data)
            success = inventory.update_asset(args.r2_key, data)
            print(json.dumps({'success': success}, indent=2))
            if not success:
                sys.exit(1)

        elif args.action == 'delete':
            if not args.r2_key:
                parser.error('--r2-key required for delete action')
            success = inventory.delete_asset(args.r2_key)
            print(json.dumps({'success': success}, indent=2))
            if not success:
                sys.exit(1)

        elif args.action == 'list':
            assets = inventory.get_all_assets()
            print(json.dumps({'success': True, 'count': len(assets), 'assets': assets}, indent=2))

        elif args.action == 'stats':
            stats = inventory.get_statistics()
            print(json.dumps({'success': True, 'statistics': stats}, indent=2))

        if args.output:
            # Output already printed to stdout, optionally save to file
            pass

        sys.exit(0)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
