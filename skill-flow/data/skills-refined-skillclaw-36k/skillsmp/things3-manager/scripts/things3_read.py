#!/usr/bin/env python3
"""
Things3 Read Operations - Uses things.py library for fast database queries.
Requires: pip install things.py
"""

import json
import sys
import argparse

try:
    import things
except ImportError:
    print("Error: things.py not installed. Run: pip install things.py", file=sys.stderr)
    sys.exit(1)


def format_task(task, indent=0):
    """Format a task dict for display."""
    prefix = "  " * indent
    status_icon = {"incomplete": "○", "completed": "✓", "canceled": "✗"}.get(task.get("status"), "?")
    
    line = f"{prefix}{status_icon} {task.get('title', 'Untitled')}"
    
    # Add metadata
    meta = []
    if task.get("when"):
        meta.append(f"when:{task['when']}")
    if task.get("deadline"):
        meta.append(f"due:{task['deadline']}")
    if task.get("tags"):
        meta.append(f"tags:{','.join(task['tags'])}")
    if task.get("area_title"):
        meta.append(f"area:{task['area_title']}")
    if task.get("project_title"):
        meta.append(f"project:{task['project_title']}")
    
    if meta:
        line += f"  [{' | '.join(meta)}]"
    
    return line


def format_tasks(tasks_list, show_notes=False):
    """Format a list of tasks for display."""
    lines = []
    for task in tasks_list:
        lines.append(format_task(task))
        if show_notes and task.get("notes"):
            for note_line in task["notes"].split("\n")[:3]:
                lines.append(f"    {note_line}")
        # checklist might be True/False or a list
        checklist = task.get("checklist")
        if checklist and isinstance(checklist, list):
            for item in checklist:
                icon = "✓" if item.get("status") == "completed" else "○"
                lines.append(f"    {icon} {item.get('title', '')}")
    return "\n".join(lines)


def cmd_inbox(args):
    tasks = things.inbox()
    if args.json:
        print(json.dumps(tasks, indent=2, default=str))
    else:
        print(f"📥 Inbox ({len(tasks)} items)\n")
        print(format_tasks(tasks) if tasks else "  (empty)")


def cmd_today(args):
    tasks = things.today()
    if args.json:
        print(json.dumps(tasks, indent=2, default=str))
    else:
        print(f"⭐ Today ({len(tasks)} items)\n")
        print(format_tasks(tasks) if tasks else "  (empty)")


def cmd_upcoming(args):
    tasks = things.upcoming()
    if args.json:
        print(json.dumps(tasks, indent=2, default=str))
    else:
        print(f"📅 Upcoming ({len(tasks)} items)\n")
        print(format_tasks(tasks) if tasks else "  (empty)")


def cmd_anytime(args):
    tasks = things.anytime()
    if args.json:
        print(json.dumps(tasks, indent=2, default=str))
    else:
        print(f"📦 Anytime ({len(tasks)} items)\n")
        print(format_tasks(tasks) if tasks else "  (empty)")


def cmd_someday(args):
    tasks = things.someday()
    if args.json:
        print(json.dumps(tasks, indent=2, default=str))
    else:
        print(f"💭 Someday ({len(tasks)} items)\n")
        print(format_tasks(tasks) if tasks else "  (empty)")


def cmd_logbook(args):
    limit = args.limit or 20
    tasks = things.logbook()[:limit]
    if args.json:
        print(json.dumps(tasks, indent=2, default=str))
    else:
        print(f"📕 Logbook (showing {len(tasks)} items)\n")
        print(format_tasks(tasks) if tasks else "  (empty)")


def cmd_deadlines(args):
    tasks = things.deadlines()
    if args.json:
        print(json.dumps(tasks, indent=2, default=str))
    else:
        print(f"⏰ Deadlines ({len(tasks)} items)\n")
        print(format_tasks(tasks) if tasks else "  (no deadlines)")


def cmd_projects(args):
    projects = things.projects()
    if args.area:
        # Filter by area
        areas_list = things.areas()
        area_match = next((a for a in areas_list if args.area.lower() in a["title"].lower()), None)
        if area_match:
            projects = [p for p in projects if p.get("area") == area_match["uuid"]]
    
    if args.json:
        print(json.dumps(projects, indent=2, default=str))
    else:
        print(f"📁 Projects ({len(projects)} items)\n")
        for p in projects:
            status = "✓" if p.get("status") == "completed" else "○"
            area_info = f" [{p.get('area_title')}]" if p.get("area_title") else ""
            print(f"  {status} {p['title']}{area_info}")


def cmd_areas(args):
    areas_list = things.areas(include_items=args.include_items)
    if args.json:
        print(json.dumps(areas_list, indent=2, default=str))
    else:
        print(f"🏷️ Areas ({len(areas_list)} items)\n")
        for area in areas_list:
            print(f"  • {area['title']}")
            if args.include_items and area.get("items"):
                for item in area["items"][:5]:
                    print(f"      {format_task(item)}")
                if len(area.get("items", [])) > 5:
                    print(f"      ... and {len(area['items']) - 5} more")


def cmd_tags(args):
    tags_list = things.tags()
    if args.json:
        print(json.dumps(tags_list, indent=2, default=str))
    else:
        print(f"🏷️ Tags ({len(tags_list)} items)\n")
        for tag in tags_list:
            print(f"  • {tag['title']}")


def cmd_search(args):
    query = args.query
    results = things.search(query)
    if args.json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print(f"🔍 Search: '{query}' ({len(results)} results)\n")
        print(format_tasks(results, show_notes=True) if results else "  (no results)")


def cmd_get(args):
    """Get a specific task/project by UUID."""
    item = things.get(args.uuid)
    if item:
        if args.json:
            print(json.dumps(item, indent=2, default=str))
        else:
            print(f"📌 {item.get('type', 'item').title()}: {item.get('title')}\n")
            print(f"  UUID: {item['uuid']}")
            print(f"  Status: {item.get('status', 'unknown')}")
            if item.get("notes"):
                print(f"  Notes: {item['notes'][:100]}...")
            if item.get("when"):
                print(f"  When: {item['when']}")
            if item.get("deadline"):
                print(f"  Deadline: {item['deadline']}")
            if item.get("tags"):
                print(f"  Tags: {', '.join(item['tags'])}")
    else:
        print(f"Not found: {args.uuid}", file=sys.stderr)
        sys.exit(1)


def cmd_token(args):
    """Get the Things URL scheme auth token."""
    token = things.token()
    if token:
        print(token)
    else:
        print("Error: Could not read auth token. Is Things URL scheme enabled?", file=sys.stderr)
        sys.exit(1)


def cmd_overdue(args):
    """Show overdue tasks."""
    tasks = things.deadlines()
    from datetime import date
    today = date.today().isoformat()
    overdue = [t for t in tasks if t.get("deadline") and t["deadline"] < today]
    
    if args.json:
        print(json.dumps(overdue, indent=2, default=str))
    else:
        print(f"🚨 Overdue ({len(overdue)} items)\n")
        print(format_tasks(overdue) if overdue else "  (nothing overdue!)")


def cmd_project_tasks(args):
    """List tasks in a specific project."""
    projects = things.projects()
    match = None
    for p in projects:
        if args.project.lower() in p["title"].lower() or args.project == p["uuid"]:
            match = p
            break
    
    if not match:
        print(f"Project not found: {args.project}", file=sys.stderr)
        sys.exit(1)
    
    # Get tasks in this project
    project_detail = things.projects(uuid=match["uuid"])
    tasks_list = project_detail.get("items", []) if isinstance(project_detail, dict) else []
    
    if args.json:
        print(json.dumps({"project": match, "tasks": tasks_list}, indent=2, default=str))
    else:
        print(f"📁 Project: {match['title']} ({len(tasks_list)} items)\n")
        for item in tasks_list:
            if item.get("type") == "heading":
                print(f"\n  📑 {item['title']}")
                for sub in item.get("items", []):
                    print(f"    {format_task(sub)}")
            else:
                print(f"  {format_task(item)}")


def main():
    parser = argparse.ArgumentParser(description="Things3 Read Operations")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # List commands
    subparsers.add_parser("inbox", help="Show Inbox")
    subparsers.add_parser("today", help="Show Today")
    subparsers.add_parser("upcoming", help="Show Upcoming")
    subparsers.add_parser("anytime", help="Show Anytime")
    subparsers.add_parser("someday", help="Show Someday")
    subparsers.add_parser("deadlines", help="Show tasks with deadlines")
    subparsers.add_parser("overdue", help="Show overdue tasks")
    
    logbook_parser = subparsers.add_parser("logbook", help="Show Logbook")
    logbook_parser.add_argument("--limit", type=int, help="Limit results")
    
    projects_parser = subparsers.add_parser("projects", help="List projects")
    projects_parser.add_argument("--area", help="Filter by area name")
    
    areas_parser = subparsers.add_parser("areas", help="List areas")
    areas_parser.add_argument("--include-items", action="store_true", help="Include items in each area")
    
    subparsers.add_parser("tags", help="List tags")
    
    search_parser = subparsers.add_parser("search", help="Search tasks")
    search_parser.add_argument("query", help="Search query")
    
    get_parser = subparsers.add_parser("get", help="Get item by UUID")
    get_parser.add_argument("uuid", help="UUID of item")
    
    project_parser = subparsers.add_parser("project-tasks", help="List tasks in a project")
    project_parser.add_argument("project", help="Project name or UUID")
    
    subparsers.add_parser("token", help="Get URL scheme auth token")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    commands = {
        "inbox": cmd_inbox,
        "today": cmd_today,
        "upcoming": cmd_upcoming,
        "anytime": cmd_anytime,
        "someday": cmd_someday,
        "logbook": cmd_logbook,
        "deadlines": cmd_deadlines,
        "overdue": cmd_overdue,
        "projects": cmd_projects,
        "areas": cmd_areas,
        "tags": cmd_tags,
        "search": cmd_search,
        "get": cmd_get,
        "project-tasks": cmd_project_tasks,
        "token": cmd_token,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
