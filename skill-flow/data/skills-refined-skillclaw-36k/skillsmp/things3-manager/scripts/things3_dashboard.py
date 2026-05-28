#!/usr/bin/env python3
"""
Things3 Dashboard - Single call to get full overview.
"""

import json
import sys
import subprocess
import time
from datetime import date

try:
    import things
except ImportError:
    print("Error: things.py not installed. Run: pip install things.py", file=sys.stderr)
    sys.exit(1)


def ensure_things_synced(wait_seconds=0.5):
    """
    Ensure Things3 is running and data is fresh.
    Activates Things briefly to trigger sync if needed.
    """
    if "--no-sync" in sys.argv:
        return
    
    try:
        # Briefly activate Things to ensure database is up to date
        subprocess.run(["open", "-g", "-a", "Things3"], check=True, capture_output=True)
        time.sleep(wait_seconds)
    except subprocess.CalledProcessError:
        pass  # Things might not be installed, continue anyway


def format_task(task):
    """Format a task for display."""
    status_icon = {"incomplete": "○", "completed": "✓", "canceled": "✗"}.get(task.get("status"), "?")
    line = f"{status_icon} {task.get('title', 'Untitled')}"
    
    meta = []
    if task.get("deadline"):
        meta.append(f"due:{task['deadline']}")
    if task.get("tags"):
        meta.append(f"tags:{','.join(task['tags'][:2])}")  # limit tags shown
    if task.get("project_title"):
        meta.append(f"proj:{task['project_title']}")
    elif task.get("area_title"):
        meta.append(f"area:{task['area_title']}")
    
    if meta:
        line += f"  [{' | '.join(meta)}]"
    return line


def main():
    output_json = "--json" in sys.argv
    
    # Ensure Things is synced before reading
    ensure_things_synced()
    
    # Fetch all data in parallel-ish (single process but minimal calls)
    inbox = things.inbox()
    today_tasks = things.today()
    upcoming = things.upcoming()
    anytime = things.anytime()
    someday = things.someday()
    projects = things.projects()
    areas = things.areas()
    deadlines = things.deadlines()
    
    # Calculate overdue
    today_str = date.today().isoformat()
    overdue = [t for t in deadlines if t.get("deadline") and t["deadline"] < today_str]
    
    if output_json:
        print(json.dumps({
            "inbox": inbox,
            "today": today_tasks,
            "upcoming": upcoming,
            "anytime": anytime,
            "someday": someday,
            "projects": projects,
            "areas": areas,
            "overdue": overdue,
            "deadlines": deadlines,
        }, indent=2, default=str))
        return
    
    # Pretty print dashboard
    print("=" * 50)
    print("📋 THINGS3 DASHBOARD")
    print("=" * 50)
    
    # Overdue (priority)
    if overdue:
        print(f"\n🚨 OVERDUE ({len(overdue)})")
        for t in overdue:
            print(f"  {format_task(t)}")
    
    # Today
    print(f"\n⭐ TODAY ({len(today_tasks)})")
    for t in today_tasks[:10]:
        print(f"  {format_task(t)}")
    if len(today_tasks) > 10:
        print(f"  ... and {len(today_tasks) - 10} more")
    
    # Inbox
    print(f"\n📥 INBOX ({len(inbox)})")
    if inbox:
        for t in inbox[:5]:
            print(f"  {format_task(t)}")
        if len(inbox) > 5:
            print(f"  ... and {len(inbox) - 5} more")
    else:
        print("  (empty)")
    
    # Upcoming
    print(f"\n📅 UPCOMING ({len(upcoming)})")
    if upcoming:
        for t in upcoming[:5]:
            print(f"  {format_task(t)}")
    else:
        print("  (empty)")
    
    # Projects summary
    print(f"\n📁 PROJECTS ({len(projects)})")
    for p in projects:
        area_info = f" [{p.get('area_title')}]" if p.get("area_title") else ""
        print(f"  ○ {p['title']}{area_info}")
    
    # Areas summary
    print(f"\n🏷️ AREAS ({len(areas)})")
    for a in areas:
        print(f"  • {a['title']}")
    
    # Counts
    print(f"\n📊 COUNTS")
    print(f"  Anytime: {len(anytime)} | Someday: {len(someday)} | Deadlines: {len(deadlines)}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
