#!/usr/bin/env python3
"""
Bibliography metadata lookup for DEVONthink records.
Matches file paths against Zotero JSON/BibTeX exports to find citation keys.

Usage:
  # Set environment variable once (add to ~/.zshrc or ~/.bashrc):
  export BIBLIOGRAPHY_JSON="~/Library/CloudStorage/Dropbox/pkm/bibliography.json"

  # Then use without --bib-json:
  python bib_lookup.py --citation-key "smith2024"
  python bib_lookup.py --path "/path/to/file.pdf"
  python bib_lookup.py --citation-key "smith2024" --find-devonthink

  # Or override with --bib-json:
  python bib_lookup.py --citation-key "smith2024" --bib-json "~/other/bibliography.json"
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse


def expand_path(path: str) -> str:
    """Expand ~ and environment variables in path."""
    return os.path.expanduser(os.path.expandvars(path))


def normalize_path(path: str) -> str:
    """Normalize a path for comparison."""
    if not path:
        return ""

    # Handle file:// URLs
    if path.lower().startswith("file://"):
        try:
            parsed = urlparse(path)
            path = unquote(parsed.path)
        except:
            pass

    # Handle Zotero-style paths with colons
    if path.startswith(":"):
        path = path[1:]
    if path.endswith(":"):
        path = path[:-1]

    # Normalize slashes and expand home
    path = path.replace("\\", "/")
    path = expand_path(path)

    # URL decode
    try:
        path = unquote(path)
    except:
        pass

    return path


def get_filename(path: str) -> str:
    """Extract filename from a path."""
    normalized = normalize_path(path)
    return normalized.split("/")[-1] if "/" in normalized else normalized


def is_local_attachment(value: str, key_hint: str = "") -> bool:
    """Check if a string looks like a local file path."""
    if not value or not value.strip():
        return False

    trimmed = value.strip()

    # Skip URLs
    if re.match(r'^(https?|zotero|attachment)://', trimmed, re.I):
        return False

    # Path hint keys
    path_hints = {"path", "localpath", "file", "uri", "url", "relativepath"}
    if key_hint.lower() in path_hints:
        return True

    normalized = normalize_path(trimmed)

    # Starts with path indicators
    if normalized.startswith("/") or normalized.startswith("~") or normalized.startswith(":"):
        return True

    # Windows path
    if re.match(r'^[A-Za-z]:[\\/]', trimmed):
        return True

    # Has file extension
    ext_pattern = r'\.(pdf|docx?|pptx?|rtf|txt|md|html?|epub|zip|gz|xlsx?|csv|png|jpe?g|gif|tiff|heic)$'
    if re.search(ext_pattern, normalized, re.I):
        return True

    return False


def collect_attachment_paths(item: dict) -> list[str]:
    """Recursively collect attachment paths from a bibliography item."""
    paths = set()

    def visit(value, key_hint=""):
        if isinstance(value, str):
            if is_local_attachment(value, key_hint):
                normalized = normalize_path(value)
                if normalized:
                    paths.add(normalized)
        elif isinstance(value, list):
            for entry in value:
                visit(entry, key_hint)
        elif isinstance(value, dict):
            for k, v in value.items():
                visit(v, k)

    visit(item)

    # Also check the 'file' field explicitly (common in CSL-JSON)
    if 'file' in item and isinstance(item['file'], str):
        normalized = normalize_path(item['file'])
        if normalized:
            paths.add(normalized)

    return list(paths)


def load_json_bibliography(json_path: str) -> list[dict]:
    """Load and parse a JSON bibliography file."""
    path = expand_path(json_path)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both array and object with items property
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        if 'items' in data and isinstance(data['items'], list):
            return data['items']
        return [data]

    return []


def get_citation_key(item: dict) -> Optional[str]:
    """Extract citation key from a bibliography item."""
    return (
        item.get('citationKey') or
        item.get('citationkey') or
        item.get('id') or
        item.get('key')
    )


def lookup_by_path(finder_path: str, json_path: str) -> Optional[dict]:
    """Look up bibliography metadata by file path."""
    entries = load_json_bibliography(json_path)
    search_filename = get_filename(finder_path).lower()
    search_normalized = normalize_path(finder_path).lower()

    for item in entries:
        if not isinstance(item, dict):
            continue

        attachment_paths = collect_attachment_paths(item)

        for att_path in attachment_paths:
            att_normalized = att_path.lower()
            att_filename = get_filename(att_path).lower()

            # Match by filename or full path
            if (search_filename == att_filename or
                search_filename in att_normalized or
                search_normalized in att_normalized or
                att_normalized in search_normalized):

                return {
                    'success': True,
                    'citationKey': get_citation_key(item),
                    'title': item.get('title'),
                    'type': item.get('type'),
                    'matchedPath': att_path,
                    'attachments': attachment_paths,
                    'item': item
                }

    return None


def lookup_by_citation_key(citation_key: str, json_path: str) -> Optional[dict]:
    """Look up bibliography metadata by citation key."""
    entries = load_json_bibliography(json_path)
    key_lower = citation_key.lower().strip()

    for item in entries:
        if not isinstance(item, dict):
            continue

        item_key = get_citation_key(item)
        if item_key and item_key.lower().strip() == key_lower:
            attachment_paths = collect_attachment_paths(item)

            return {
                'success': True,
                'citationKey': item_key,
                'title': item.get('title'),
                'type': item.get('type'),
                'attachments': attachment_paths,
                'item': item
            }

    return None


def find_devonthink_records(file_paths: list[str]) -> list[dict]:
    """Find DEVONthink records matching the given file paths using JXA."""
    if not file_paths:
        return []

    # Build JXA script to look up records by path
    paths_json = json.dumps(file_paths)

    script = f'''
    (() => {{
      const theApp = Application("DEVONthink");
      theApp.includeStandardAdditions = true;

      try {{
        const paths = {paths_json};
        const results = [];
        const seen = {{}};

        for (const searchPath of paths) {{
          try {{
            // Try lookupRecordsWithPath
            const matches = theApp.lookupRecordsWithPath(searchPath);
            if (matches && matches.length > 0) {{
              for (const record of matches) {{
                try {{
                  const uuid = record.uuid();
                  if (seen[uuid]) continue;
                  seen[uuid] = true;

                  const r = {{}};
                  r["id"] = record.id();
                  r["uuid"] = uuid;
                  r["name"] = record.name();
                  r["path"] = record.path();
                  r["location"] = record.location();
                  r["recordType"] = record.recordType();
                  results.push(r);
                }} catch (e) {{}}
              }}
            }}
          }} catch (e) {{}}

          // Also try by filename
          try {{
            const filename = searchPath.split("/").pop();
            if (filename) {{
              const matches = theApp.lookupRecordsWithFile(filename);
              if (matches && matches.length > 0) {{
                for (const record of matches) {{
                  try {{
                    const uuid = record.uuid();
                    if (seen[uuid]) continue;
                    seen[uuid] = true;

                    const r = {{}};
                    r["id"] = record.id();
                    r["uuid"] = uuid;
                    r["name"] = record.name();
                    r["path"] = record.path();
                    r["location"] = record.location();
                    r["recordType"] = record.recordType();
                    results.push(r);
                  }} catch (e) {{}}
                }}
              }}
            }}
          }} catch (e) {{}}
        }}

        return JSON.stringify({{ success: true, records: results }});
      }} catch (error) {{
        return JSON.stringify({{ success: false, error: error.toString() }});
      }}
    }})();
    '''

    try:
        result = subprocess.run(
            ['osascript', '-l', 'JavaScript', '-e', script],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip())
            if data.get('success') and 'records' in data:
                return data['records']
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        pass

    return []


def main():
    parser = argparse.ArgumentParser(description='Look up bibliography metadata')
    parser.add_argument('--path', help='Finder path to look up')
    parser.add_argument('--citation-key', help='Citation key to look up')
    parser.add_argument('--bib-json',
                        default=os.environ.get('BIBLIOGRAPHY_JSON'),
                        help='Path to bibliography JSON file (or set BIBLIOGRAPHY_JSON env var)')
    parser.add_argument('--full', action='store_true', help='Include full item metadata')
    parser.add_argument('--find-devonthink', action='store_true',
                        help='Also find matching DEVONthink records')

    args = parser.parse_args()

    if not args.path and not args.citation_key:
        parser.error('Either --path or --citation-key is required')

    if not args.bib_json:
        parser.error('--bib-json is required (or set BIBLIOGRAPHY_JSON environment variable)')

    try:
        if args.path:
            result = lookup_by_path(args.path, args.bib_json)
        else:
            result = lookup_by_citation_key(args.citation_key, args.bib_json)

        if result:
            # Find DEVONthink records if requested
            if args.find_devonthink and result.get('attachments'):
                dt_records = find_devonthink_records(result['attachments'])
                result['devonthinkRecords'] = dt_records

            if not args.full:
                # Remove full item for cleaner output
                result.pop('item', None)

            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({
                'success': False,
                'error': 'No matching entry found'
            }, indent=2))
            sys.exit(1)

    except FileNotFoundError as e:
        print(json.dumps({
            'success': False,
            'error': f'File not found: {e.filename}'
        }, indent=2))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({
            'success': False,
            'error': f'Invalid JSON: {str(e)}'
        }, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
        }, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
