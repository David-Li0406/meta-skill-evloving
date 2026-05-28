#!/usr/bin/env python3
"""
Delete or archive completed todos from Notion Todos [DB].
"""

import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path

try:
    from notion_client import Client
except ImportError:
    print("Error: notion-client not installed. Run: pip install notion-client")
    exit(1)

# Configuration
DATABASE_ID = "9c9b8dcd-e01b-488f-aa87-eaaed7be9a52"
DONE_PROPERTY = "Done ?"


def load_env():
    """Load NOTION_TOKEN from .env files."""
    env_paths = [
        Path.cwd() / ".env",
        Path.home() / ".env",
    ]

    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())

    return os.environ.get("NOTION_TOKEN")


def get_done_todos(client, older_than_days=None):
    """Query all todos where Done ? = true."""
    filter_conditions = {
        "property": DONE_PROPERTY,
        "checkbox": {"equals": True}
    }

    results = []
    has_more = True
    start_cursor = None

    while has_more:
        response = client.databases.query(
            database_id=DATABASE_ID,
            filter=filter_conditions,
            start_cursor=start_cursor,
        )

        for page in response["results"]:
            # Filter by age if specified
            if older_than_days:
                last_edited = datetime.fromisoformat(
                    page["last_edited_time"].replace("Z", "+00:00")
                )
                cutoff = datetime.now(last_edited.tzinfo) - timedelta(days=older_than_days)
                if last_edited > cutoff:
                    continue

            results.append({
                "id": page["id"],
                "title": get_page_title(page),
                "last_edited": page["last_edited_time"],
            })

        has_more = response["has_more"]
        start_cursor = response.get("next_cursor")

    return results


def get_page_title(page):
    """Extract title from page properties."""
    props = page.get("properties", {})
    name_prop = props.get("Name", {})
    title_array = name_prop.get("title", [])
    if title_array:
        return title_array[0].get("plain_text", "Untitled")
    return "Untitled"


def delete_pages(client, pages, archive=False):
    """Delete or archive pages."""
    action = "Archiving" if archive else "Deleting"

    for i, page in enumerate(pages, 1):
        print(f"  [{i}/{len(pages)}] {action}: {page['title'][:50]}...")
        client.pages.update(
            page_id=page["id"],
            archived=True if archive else True,  # Notion API uses archived=True for both
            in_trash=not archive,  # in_trash=True for permanent delete
        )

    return len(pages)


def main():
    parser = argparse.ArgumentParser(
        description="Delete completed todos from Notion Todos [DB]"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List items without deleting",
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Archive instead of permanently deleting",
    )
    parser.add_argument(
        "--older-than",
        type=int,
        metavar="DAYS",
        help="Only delete items completed more than X days ago",
    )

    args = parser.parse_args()

    # Load token
    token = load_env()
    if not token:
        print("Error: NOTION_TOKEN not found in .env")
        print("Add to ~/.env or ./.env: NOTION_TOKEN=secret_xxxxx")
        exit(1)

    # Initialize client
    client = Client(auth=token)

    print(f"Querying Todos [DB] for completed items...")
    if args.older_than:
        print(f"  (filtering: older than {args.older_than} days)")

    # Get done todos
    done_todos = get_done_todos(client, args.older_than)

    if not done_todos:
        print("No completed todos found.")
        return

    print(f"\nFound {len(done_todos)} completed todo(s):")
    for todo in done_todos[:10]:  # Show first 10
        print(f"  - {todo['title'][:60]}")
    if len(done_todos) > 10:
        print(f"  ... and {len(done_todos) - 10} more")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return

    # Confirm
    action = "archive" if args.archive else "permanently delete"
    print(f"\nAbout to {action} {len(done_todos)} item(s).")
    confirm = input("Continue? [y/N]: ").strip().lower()

    if confirm != "y":
        print("Cancelled.")
        return

    # Execute
    print(f"\n{'Archiving' if args.archive else 'Deleting'}...")
    count = delete_pages(client, done_todos, args.archive)

    print(f"\nDone! {count} item(s) {'archived' if args.archive else 'deleted'}.")


if __name__ == "__main__":
    main()
