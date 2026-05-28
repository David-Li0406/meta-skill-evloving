"""Command-line interface for Work Memo skill."""

import argparse
import sys
from typing import Dict, Any, Optional

sys.path.insert(0, __file__)

from storage import WorkMemoStorage
from schema import WorkRecord, WorkType, Status, Person, Location
from query_parser import QueryParser
from reporting import Reporting


def cmd_add(args) -> None:
    """Add new work record"""
    storage = WorkMemoStorage()
    storage.initialize()

    parser = QueryParser()

    title = args.title or input("Title: ")

    work_type = WorkType.TASK
    if args.type:
        type_map = {
            'task': WorkType.TASK,
            'meeting': WorkType.MEETING,
            'call': WorkType.CALL,
            'email': WorkType.EMAIL,
            'review': WorkType.REVIEW,
            'coding': WorkType.CODING,
            'design': WorkType.DESIGN,
            'writing': WorkType.WRITING,
            'research': WorkType.RESEARCH,
            'planning': WorkType.PLANNING,
            'documentation': WorkType.DOCUMENTATION,
            'bugfix': WorkType.BUGFIX,
            'feature': WorkType.FEATURE,
        }
        work_type = type_map.get(args.type.lower(), WorkType.TASK)

    urgency = args.urgency or int(input("Urgency (1-5) [default: 3]: ") or 3)
    urgency = max(1, min(5, urgency))

    importance_val = args.importance or int(input("Importance (1-5) [default: 3]: ") or 3)
    importance = max(1, min(5, importance_val))

    difficulty_val = args.difficulty or int(input("Difficulty (1-10) [default: 5]: ") or 5)
    difficulty = max(1, min(10, difficulty_val))

    record = WorkRecord(
        title=title,
        type=work_type,
        status=Status.TODO,
        urgency=urgency,
        importance=importance_val,
        difficulty=difficulty_val,
    )

    if args.description:
        record.description = input("Description: ")

    if args.assignee:
        record.assignee = Person(name=args.assignee)

    if args.due_date:
        record.due_date = args.due_date

    if args.tags:
        record.tags = args.tags

    storage.create(record)
    print(f"✓ Created record: {record.id}")
    print(f"  Title: {record.title}")
    print(f"  Type: {record.type.value}")
    print(f"  Urgency: {record.urgency}, Importance: {record.importance}")
    print(f"  Difficulty: {record.difficulty}")
    if record.due_date:
        print(f"  Due: {record.due_date}")

    storage.close()


def cmd_memo(args) -> None:
    """Quick add using natural language description"""
    storage = WorkMemoStorage()
    storage.initialize()
    parser = QueryParser()

    description = args.description
    parsed = parser.parse(description)

    print(f"\nParsed from: '{description}'")
    print(f"  Title: {parsed.get('title', description)}")
    if 'type' in parsed:
        print(f"  Type: {parsed['type']}")
    if 'urgency_min' in parsed:
        print(f"  Urgency: {parsed['urgency_min']}")
    if 'importance_min' in parsed:
        print(f"  Importance: {parsed['importance_min']}")
    if 'due_date_end' in parsed:
        print(f"  Due: {parsed['due_date_end']}")
    if 'tags' in parsed:
        print(f"  Tags: {parsed['tags']}")
    if 'contexts' in parsed:
        print(f"  Contexts: {parsed['contexts']}")

    record = WorkRecord(
        title=parsed.get('title', description),
        status=Status.TODO
    )

    if 'type' in parsed:
        type_map = {
            'task': WorkType.TASK,
            'meeting': WorkType.MEETING,
            'call': WorkType.CALL,
            'email': WorkType.EMAIL,
            'review': WorkType.REVIEW,
            'coding': WorkType.CODING,
            'design': WorkType.DESIGN,
            'writing': WorkType.WRITING,
            'research': WorkType.RESEARCH,
            'planning': WorkType.PLANNING,
            'documentation': WorkType.DOCUMENTATION,
            'bugfix': WorkType.BUGFIX,
            'feature': WorkType.FEATURE,
        }
        record.type = type_map.get(parsed['type'], WorkType.TASK)

    record.urgency = parsed.get('urgency_min', 3)
    if record.urgency < 1:
        record.urgency = 1
    elif record.urgency > 5:
        record.urgency = 5

    record.importance = parsed.get('importance_min', 3)
    if record.importance < 1:
        record.importance = 1
    elif record.importance > 5:
        record.importance = 5

    record.difficulty = 5

    if 'due_date_end' in parsed:
        record.due_date = parsed['due_date_end']

    if 'tags' in parsed:
        record.tags = parsed['tags']

    if 'contexts' in parsed:
        record.contexts = parsed['contexts']

    if args.interactive:
        if 'urgency_min' not in parsed:
            try:
                record.urgency = int(input(f"Urgency (1-5) [current: {record.urgency}]: ") or record.urgency)
            except (EOFError, KeyboardInterrupt):
                record.urgency = 3
        if 'importance_min' not in parsed:
            try:
                record.importance = int(input(f"Importance (1-5) [current: {record.importance}]: ") or record.importance)
            except (EOFError, KeyboardInterrupt):
                record.importance = 3
        if parsed.get('difficulty_min') is None:
            try:
                record.difficulty = int(input(f"Difficulty (1-10) [current: {record.difficulty}]: ") or record.difficulty)
            except (EOFError, KeyboardInterrupt):
                record.difficulty = 5

    if args.interactive:
        try:
            user_desc = input(f"Description [optional]: ") or ""
        except (EOFError, KeyboardInterrupt):
            user_desc = ""
        if user_desc.strip():
            record.description = user_desc

    if args.interactive:
        try:
            assignee_name = input(f"Assignee [optional]: ") or ""
        except (EOFError, KeyboardInterrupt):
            assignee_name = ""
        if assignee_name.strip():
            record.assignee = Person(name=assignee_name)

    storage.create(record)
    print(f"\n✓ Created memo: {record.id}")
    print(f"  Title: {record.title}")
    print(f"  Type: {record.type.value}")
    print(f"  Status: {record.status.value}")
    print(f"  Urgency: {record.urgency}, Importance: {record.importance}, Difficulty: {record.difficulty}")
    if record.due_date:
        print(f"  Due: {record.due_date}")
    if record.tags:
        print(f"  Tags: {', '.join(record.tags)}")
    if record.contexts:
        print(f"  Contexts: {', '.join(record.contexts)}")
    if record.assignee:
        print(f"  Assignee: {record.assignee.name}")
    print(f"  Eisenhower: {record.get_eisenhower_quadrant()}")

    storage.close()


def cmd_search(args) -> None:
    """Search work records"""
    storage = WorkMemoStorage()
    storage.initialize()

    parser = QueryParser()

    query = args.query if args.query else input("Search query: ")
    filters = parser.parse(query)

    results = storage.search(filters)

    if not results:
        print("No matching records found")
        storage.close()
        return

    print(f"Found {len(results)} matching record(s):\n")

    for i, record in enumerate(results, 1):
        urgency_str = f"[U{record.urgency}]" if record.urgency >= 4 else ""
        importance_str = f"[I{record.importance}]" if record.importance >= 4 else ""

        print(f"{i}. {record.title} {urgency_str}{importance_str}")
        print(f"   Type: {record.type.value}, Status: {record.status.value}")
        if record.due_date:
            print(f"   Due: {record.due_date}")
        if record.tags:
            print(f"   Tags: {', '.join(record.tags)}")
        print()

    storage.close()


def cmd_list(args) -> None:
    """List all work records"""
    storage = WorkMemoStorage()
    storage.initialize()

    records = storage.get_all()

    if not records:
        print("No records found")
        storage.close()
        return

    if args.quadrant:
        quadrant = args.quadrant.upper()
        records = storage.get_by_quadrant(quadrant)
        print(f"=== Eisenhower Quadrant {quadrant} ({len(records)} records) ===")
    else:
        print(f"=== All Records ({len(records)}) ===")

    for i, record in enumerate(records, 1):
        urgency_str = f"[U{record.urgency}]" if record.urgency >= 4 else ""
        importance_str = f"[I{record.importance}]" if record.importance >= 4 else ""
        quadrant_str = f" [{record.get_eisenhower_quadrant()}]"

        print(f"{i}. {record.title} {urgency_str}{importance_str}{quadrant_str}")
        print(f"   Type: {record.type.value}, Status: {record.status.value}")
        if record.due_date:
            print(f"   Due: {record.due_date}")
        if record.tags:
            print(f"   Tags: {', '.join(record.tags)}")
        print()

    storage.close()


def cmd_report(args) -> None:
    """Generate reports"""
    storage = WorkMemoStorage()
    storage.initialize()
    reporting = Reporting(storage)

    if args.daily:
        report = reporting.get_daily_report(args.daily)
        print(reporting.format_daily_report(report))
    elif args.weekly:
        report = reporting.get_weekly_report()
        print(reporting.format_weekly_report(report))
    elif args.monthly:
        report = reporting.get_monthly_report()
        print(reporting.format_monthly_report(report))
    else:
        print("Please specify --daily, --weekly, or --monthly")

    storage.close()


def cmd_suggest(args) -> None:
    """Get work recommendations"""
    storage = WorkMemoStorage()
    storage.initialize()

    records = storage.get_all()

    pending = [r for r in records if r.status.value != 'done']

    if not pending:
        print("No pending tasks to suggest")
        storage.close()
        return

    for record in pending:
        score = record.get_priority_score()

    sorted_records = sorted(pending, key=lambda r: r.get_priority_score(), reverse=True)

    print(f"=== Work Recommendations (Top {args.limit or 10}) ===\n")

    for i, record in enumerate(sorted_records[:args.limit or 10], 1):
        score = record.get_priority_score()
        quadrant = record.get_eisenhower_quadrant()

        urgency_str = f"[U{record.urgency}]" if record.urgency >= 4 else ""
        importance_str = f"[I{record.importance}]" if record.importance >= 4 else ""

        print(f"{i}. {record.title} {urgency_str}{importance_str} [{quadrant}]")
        print(f"   Priority Score: {score:.2f}, Difficulty: {record.difficulty}")
        if record.due_date:
            print(f"   Due: {record.due_date}")
        if record.tags:
            print(f"   Tags: {', '.join(record.tags)}")
        print()

    storage.close()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Work Memo: Personal work record management system",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    parser_add = subparsers.add_parser('add', help='Add new work record')
    parser_add.add_argument('title', help='Work title')
    parser_add.add_argument('--type', help='Work type (task, meeting, call, etc.)')
    parser_add.add_argument('--urgency', type=int, help='Urgency level (1-5)')
    parser_add.add_argument('--importance', type=int, help='Importance level (1-5)')
    parser_add.add_argument('--difficulty', type=int, help='Difficulty level (1-10)')
    parser_add.add_argument('--description', help='Detailed description')
    parser_add.add_argument('--assignee', help='Person assigned to')
    parser_add.add_argument('--due-date', help='Due date (ISO 8601 format)')
    parser_add.add_argument('--tags', nargs='+', help='Tags')

    parser_memo = subparsers.add_parser('memo', help='Quick add using natural language description')
    parser_memo.add_argument('description', help='Natural language work description')
    parser_memo.add_argument('--interactive', action='store_true', help='Interactive mode for missing fields')

    parser_search = subparsers.add_parser('search', help='Search work records')
    parser_search.add_argument('query', help='Natural language search query')

    parser_list = subparsers.add_parser('list', help='List all records')
    parser_list.add_argument('--quadrant', help='Filter by Eisenhower quadrant (Q1-Q4)')

    parser_report = subparsers.add_parser('report', help='Generate reports')
    parser_report.add_argument('--daily', help='Daily report')
    parser_report.add_argument('--weekly', action='store_true', help='Weekly report')
    parser_report.add_argument('--monthly', action='store_true', help='Monthly report')

    parser_suggest = subparsers.add_parser('suggest', help='Get work recommendations')
    parser_suggest.add_argument('--limit', type=int, default=10, help='Number of suggestions')

    args = parser.parse_args()

    if args.command == 'add':
        cmd_add(args)
    elif args.command == 'memo':
        cmd_memo(args)
    elif args.command == 'search':
        cmd_search(args)
    elif args.command == 'list':
        cmd_list(args)
    elif args.command == 'report':
        cmd_report(args)
    elif args.command == 'suggest':
        cmd_suggest(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
