#!/usr/bin/env python3
"""
Things3 Write Operations - Uses Things URL Scheme for creating/updating tasks.
Opens things:// URLs to execute commands in Things app.
"""

import json
import sys
import argparse
import urllib.parse
import subprocess
import time

try:
    import things
except ImportError:
    things = None  # Token retrieval will fail, but basic adds still work


def get_auth_token():
    """Get the Things URL scheme auth token (required for updates)."""
    if things:
        token = things.token()
        if not token:
            print("Error: Things URL scheme not enabled.", file=sys.stderr)
            print("Enable it in: Things → Settings → General → Enable Things URLs", file=sys.stderr)
        return token
    print("Error: things.py not installed. Run: pip install things.py", file=sys.stderr)
    return None


def build_url(command, **params):
    """Build a things:// URL with the given command and parameters."""
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    if params:
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return f"things:///{command}?{query}"
    return f"things:///{command}"


def open_url(url, dry_run=False):
    """Open a things:// URL."""
    if dry_run:
        print(f"[DRY RUN] Would open: {url}")
        return True
    
    try:
        subprocess.run(["open", url], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error opening URL: {e}", file=sys.stderr)
        return False


def cmd_add_todo(args):
    """Add a new to-do."""
    params = {
        "title": args.title,
        "notes": args.notes,
        "when": args.when,
        "deadline": args.deadline,
        "tags": ",".join(args.tags) if args.tags else None,
        "list-id": args.list_id,
        "list": args.list,
        "heading": args.heading,
        "checklist-items": "\n".join(args.checklist) if args.checklist else None,
        "show-quick-entry": "true" if args.quick_entry else None,
    }
    
    url = build_url("add", **params)
    
    if args.show_url:
        print(url)
        return
    
    if open_url(url, args.dry_run):
        if not args.dry_run:
            print(f"✓ Added todo: {args.title}")


def cmd_add_project(args):
    """Add a new project."""
    params = {
        "title": args.title,
        "notes": args.notes,
        "when": args.when,
        "deadline": args.deadline,
        "tags": ",".join(args.tags) if args.tags else None,
        "area-id": args.area_id,
        "area": args.area,
        "to-dos": "\n".join(args.todos) if args.todos else None,
        "show-quick-entry": "true" if args.quick_entry else None,
    }
    
    url = build_url("add-project", **params)
    
    if args.show_url:
        print(url)
        return
    
    if open_url(url, args.dry_run):
        if not args.dry_run:
            print(f"✓ Added project: {args.title}")


def cmd_update_todo(args):
    """Update an existing to-do."""
    token = get_auth_token()
    if not token:
        sys.exit(1)
    
    params = {
        "id": args.id,
        "auth-token": token,
        "title": args.title,
        "notes": args.notes,
        "prepend-notes": args.prepend_notes,
        "append-notes": args.append_notes,
        "when": args.when,
        "deadline": args.deadline,
        "tags": ",".join(args.tags) if args.tags else None,
        "add-tags": ",".join(args.add_tags) if args.add_tags else None,
        "list-id": args.list_id,
        "list": args.list,
        "heading": args.heading,
        "completed": "true" if args.completed else None,
        "canceled": "true" if args.canceled else None,
        "checklist-items": "\n".join(args.checklist) if args.checklist else None,
        "append-checklist-items": "\n".join(args.append_checklist) if args.append_checklist else None,
    }
    
    url = build_url("update", **params)
    
    if args.show_url:
        print(url)
        return
    
    if open_url(url, args.dry_run):
        if not args.dry_run:
            print(f"✓ Updated todo: {args.id}")


def cmd_update_project(args):
    """Update an existing project."""
    token = get_auth_token()
    if not token:
        sys.exit(1)
    
    params = {
        "id": args.id,
        "auth-token": token,
        "title": args.title,
        "notes": args.notes,
        "prepend-notes": args.prepend_notes,
        "append-notes": args.append_notes,
        "when": args.when,
        "deadline": args.deadline,
        "tags": ",".join(args.tags) if args.tags else None,
        "add-tags": ",".join(args.add_tags) if args.add_tags else None,
        "area-id": args.area_id,
        "area": args.area,
        "completed": "true" if args.completed else None,
        "canceled": "true" if args.canceled else None,
    }
    
    url = build_url("update-project", **params)
    
    if args.show_url:
        print(url)
        return
    
    if open_url(url, args.dry_run):
        if not args.dry_run:
            print(f"✓ Updated project: {args.id}")


def cmd_complete(args):
    """Mark a to-do or project as complete."""
    token = get_auth_token()
    if not token:
        sys.exit(1)
    
    params = {
        "id": args.id,
        "auth-token": token,
        "completed": "true",
    }
    
    url = build_url("update", **params)
    
    if args.show_url:
        print(url)
        return
    
    if open_url(url, args.dry_run):
        if not args.dry_run:
            print(f"✓ Completed: {args.id}")


def cmd_cancel(args):
    """Mark a to-do or project as canceled (moves to Logbook)."""
    token = get_auth_token()
    if not token:
        sys.exit(1)
    
    params = {
        "id": args.id,
        "auth-token": token,
        "canceled": "true",
    }
    
    url = build_url("update", **params)
    
    if args.show_url:
        print(url)
        return
    
    if open_url(url, args.dry_run):
        if not args.dry_run:
            print(f"✓ Canceled: {args.id}")


def cmd_delete(args):
    """
    Delete a to-do or project (moves to Trash).
    Note: Things URL scheme doesn't support delete directly.
    We use AppleScript as a fallback.
    """
    if args.dry_run:
        print(f"[DRY RUN] Would delete: {args.id}")
        return
    
    # Use AppleScript to delete
    script = f'''
    tell application "Things3"
        set targetTodo to to do id "{args.id}"
        move targetTodo to list "Trash"
    end tell
    '''
    
    try:
        subprocess.run(["osascript", "-e", script], check=True, capture_output=True, text=True)
        print(f"✓ Deleted (moved to Trash): {args.id}")
    except subprocess.CalledProcessError as e:
        # Try as project
        script_project = f'''
        tell application "Things3"
            set targetProject to project id "{args.id}"
            move targetProject to list "Trash"
        end tell
        '''
        try:
            subprocess.run(["osascript", "-e", script_project], check=True, capture_output=True, text=True)
            print(f"✓ Deleted project (moved to Trash): {args.id}")
        except subprocess.CalledProcessError as e2:
            print(f"Error deleting: {e2.stderr}", file=sys.stderr)
            sys.exit(1)


def cmd_show(args):
    """Show a specific item or list in Things."""
    if args.id:
        url = build_url("show", id=args.id)
    elif args.list:
        # Built-in lists
        list_map = {
            "inbox": "inbox",
            "today": "today",
            "upcoming": "upcoming",
            "anytime": "anytime",
            "someday": "someday",
            "logbook": "logbook",
            "trash": "trash",
        }
        list_id = list_map.get(args.list.lower(), args.list)
        url = build_url("show", id=list_id)
    else:
        print("Error: Must specify --id or --list", file=sys.stderr)
        sys.exit(1)
    
    if args.show_url:
        print(url)
        return
    
    open_url(url, args.dry_run)


def cmd_search_in_app(args):
    """Open Things search with a query."""
    url = build_url("search", query=args.query)
    
    if args.show_url:
        print(url)
        return
    
    open_url(url, args.dry_run)


def cmd_json_import(args):
    """Import items via JSON (powerful bulk operations)."""
    token = get_auth_token()
    
    if args.file:
        with open(args.file) as f:
            data = json.load(f)
    else:
        data = json.loads(args.data)
    
    # Add auth token if any updates are present
    needs_auth = False
    if isinstance(data, list):
        for item in data:
            if item.get("operation") == "update":
                needs_auth = True
                break
    
    if needs_auth and not token:
        print("Error: Cannot get auth token for update operations.", file=sys.stderr)
        sys.exit(1)
    
    params = {"data": json.dumps(data)}
    if needs_auth:
        params["auth-token"] = token
    
    url = build_url("json", **params)
    
    if args.show_url:
        print(url)
        return
    
    if open_url(url, args.dry_run):
        if not args.dry_run:
            print("✓ JSON import executed")


def cmd_batch(args):
    """Execute batch operations on multiple items."""
    token = get_auth_token()
    if not token:
        sys.exit(1)
    
    ids = args.ids
    operation = args.operation
    delay = args.delay
    
    success_count = 0
    fail_count = 0
    
    for i, item_id in enumerate(ids):
        params = {
            "id": item_id,
            "auth-token": token,
        }
        
        if operation == "complete":
            params["completed"] = "true"
        elif operation == "cancel":
            params["canceled"] = "true"
        elif operation == "reschedule":
            if not args.when:
                print("Error: --when required for reschedule operation", file=sys.stderr)
                sys.exit(1)
            params["when"] = args.when
        elif operation == "move":
            if args.list:
                params["list"] = args.list
            elif args.list_id:
                params["list-id"] = args.list_id
            else:
                print("Error: --list or --list-id required for move operation", file=sys.stderr)
                sys.exit(1)
        elif operation == "add-tag":
            if not args.tag:
                print("Error: --tag required for add-tag operation", file=sys.stderr)
                sys.exit(1)
            params["add-tags"] = args.tag
        
        url = build_url("update", **params)
        
        if args.dry_run:
            print(f"[DRY RUN] [{i+1}/{len(ids)}] Would {operation}: {item_id}")
            success_count += 1
        elif args.show_url:
            print(url)
        else:
            if open_url(url):
                print(f"✓ [{i+1}/{len(ids)}] {operation}: {item_id}")
                success_count += 1
            else:
                print(f"✗ [{i+1}/{len(ids)}] Failed: {item_id}")
                fail_count += 1
            
            # Small delay between operations to avoid overwhelming Things
            if i < len(ids) - 1 and delay > 0:
                time.sleep(delay)
    
    print(f"\nBatch {operation} complete: {success_count} succeeded, {fail_count} failed")


def main():
    parser = argparse.ArgumentParser(description="Things3 Write Operations")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    parser.add_argument("--show-url", action="store_true", help="Print URL instead of opening")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add todo
    add_parser = subparsers.add_parser("add", help="Add a new to-do")
    add_parser.add_argument("title", help="Title of the to-do")
    add_parser.add_argument("--notes", help="Notes")
    add_parser.add_argument("--when", help="When: today, tomorrow, evening, someday, or date")
    add_parser.add_argument("--deadline", help="Deadline date")
    add_parser.add_argument("--tags", nargs="+", help="Tags")
    add_parser.add_argument("--list-id", help="UUID of project/area")
    add_parser.add_argument("--list", help="Name of project/area")
    add_parser.add_argument("--heading", help="Heading within project")
    add_parser.add_argument("--checklist", nargs="+", help="Checklist items")
    add_parser.add_argument("--quick-entry", action="store_true", help="Show quick entry dialog")
    
    # Add project
    proj_parser = subparsers.add_parser("add-project", help="Add a new project")
    proj_parser.add_argument("title", help="Title of the project")
    proj_parser.add_argument("--notes", help="Notes")
    proj_parser.add_argument("--when", help="When: today, tomorrow, evening, someday, or date")
    proj_parser.add_argument("--deadline", help="Deadline date")
    proj_parser.add_argument("--tags", nargs="+", help="Tags")
    proj_parser.add_argument("--area-id", help="UUID of area")
    proj_parser.add_argument("--area", help="Name of area")
    proj_parser.add_argument("--todos", nargs="+", help="To-dos to create in project")
    proj_parser.add_argument("--quick-entry", action="store_true", help="Show quick entry dialog")
    
    # Update todo
    update_parser = subparsers.add_parser("update", help="Update a to-do")
    update_parser.add_argument("id", help="UUID of the to-do")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--notes", help="Replace notes")
    update_parser.add_argument("--prepend-notes", help="Prepend to notes")
    update_parser.add_argument("--append-notes", help="Append to notes")
    update_parser.add_argument("--when", help="When")
    update_parser.add_argument("--deadline", help="Deadline")
    update_parser.add_argument("--tags", nargs="+", help="Replace tags")
    update_parser.add_argument("--add-tags", nargs="+", help="Add tags")
    update_parser.add_argument("--list-id", help="Move to project/area UUID")
    update_parser.add_argument("--list", help="Move to project/area name")
    update_parser.add_argument("--heading", help="Move to heading")
    update_parser.add_argument("--completed", action="store_true", help="Mark completed")
    update_parser.add_argument("--canceled", action="store_true", help="Mark canceled")
    update_parser.add_argument("--checklist", nargs="+", help="Replace checklist")
    update_parser.add_argument("--append-checklist", nargs="+", help="Append to checklist")
    
    # Update project
    uproj_parser = subparsers.add_parser("update-project", help="Update a project")
    uproj_parser.add_argument("id", help="UUID of the project")
    uproj_parser.add_argument("--title", help="New title")
    uproj_parser.add_argument("--notes", help="Replace notes")
    uproj_parser.add_argument("--prepend-notes", help="Prepend to notes")
    uproj_parser.add_argument("--append-notes", help="Append to notes")
    uproj_parser.add_argument("--when", help="When")
    uproj_parser.add_argument("--deadline", help="Deadline")
    uproj_parser.add_argument("--tags", nargs="+", help="Replace tags")
    uproj_parser.add_argument("--add-tags", nargs="+", help="Add tags")
    uproj_parser.add_argument("--area-id", help="Move to area UUID")
    uproj_parser.add_argument("--area", help="Move to area name")
    uproj_parser.add_argument("--completed", action="store_true", help="Mark completed")
    uproj_parser.add_argument("--canceled", action="store_true", help="Mark canceled")
    
    # Complete
    complete_parser = subparsers.add_parser("complete", help="Mark item complete")
    complete_parser.add_argument("id", help="UUID of item")
    
    # Cancel
    cancel_parser = subparsers.add_parser("cancel", help="Mark item canceled (moves to Logbook)")
    cancel_parser.add_argument("id", help="UUID of item")
    
    # Delete
    delete_parser = subparsers.add_parser("delete", help="Delete item (moves to Trash)")
    delete_parser.add_argument("id", help="UUID of item")
    
    # Show
    show_parser = subparsers.add_parser("show", help="Show item/list in Things")
    show_parser.add_argument("--id", help="UUID of item")
    show_parser.add_argument("--list", help="List name: inbox, today, upcoming, anytime, someday, logbook, trash")
    
    # Search in app
    search_parser = subparsers.add_parser("search-app", help="Open search in Things")
    search_parser.add_argument("query", help="Search query")
    
    # JSON import
    json_parser = subparsers.add_parser("json", help="Import via JSON")
    json_parser.add_argument("--data", help="JSON string")
    json_parser.add_argument("--file", help="JSON file path")
    
    # Batch operations
    batch_parser = subparsers.add_parser("batch", help="Batch operations on multiple items")
    batch_parser.add_argument("operation", choices=["complete", "cancel", "reschedule", "move", "add-tag"],
                             help="Operation to perform")
    batch_parser.add_argument("ids", nargs="+", help="UUIDs of items to update")
    batch_parser.add_argument("--when", help="For reschedule: target date")
    batch_parser.add_argument("--list", help="For move: target project/area name")
    batch_parser.add_argument("--list-id", help="For move: target project/area UUID")
    batch_parser.add_argument("--tag", help="For add-tag: tag to add")
    batch_parser.add_argument("--delay", type=float, default=0.3, help="Delay between operations (seconds)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    commands = {
        "add": cmd_add_todo,
        "add-project": cmd_add_project,
        "update": cmd_update_todo,
        "update-project": cmd_update_project,
        "complete": cmd_complete,
        "cancel": cmd_cancel,
        "delete": cmd_delete,
        "show": cmd_show,
        "search-app": cmd_search_in_app,
        "json": cmd_json_import,
        "batch": cmd_batch,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
