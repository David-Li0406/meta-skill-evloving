#!/usr/bin/env python3
"""
Fetch Bible reading plan from various sources and convert to project format.

Sources supported:
1. IQ Bible API (requires RapidAPI key)
2. Bible.com/YouVersion reading plans (public)
3. Generate from book/chapter data locally

Usage:
    # Generate a local plan (no API needed)
    python fetch_reading_plan.py --generate --book John --days 21 --output john_plan.json

    # Generate NT in 90 days
    python fetch_reading_plan.py --generate --sections NT --days 90 --output nt_90.json

    # With SQL output
    python fetch_reading_plan.py --generate --book Psalms --days 30 --sql --output psalms.json
"""

import argparse
import json
import sys
from datetime import datetime

# Book data: (Finnish abbrev, English name, chapters)
BIBLE_BOOKS = [
    # Old Testament
    ("1. Moos", "Genesis", 50), ("2. Moos", "Exodus", 40), ("3. Moos", "Leviticus", 27),
    ("4. Moos", "Numbers", 36), ("5. Moos", "Deuteronomy", 34), ("Joos", "Joshua", 24),
    ("Tuom", "Judges", 21), ("Ruut", "Ruth", 4), ("1. Sam", "1 Samuel", 31),
    ("2. Sam", "2 Samuel", 24), ("1. Kun", "1 Kings", 22), ("2. Kun", "2 Kings", 25),
    ("1. Aik", "1 Chronicles", 29), ("2. Aik", "2 Chronicles", 36), ("Esra", "Ezra", 10),
    ("Neh", "Nehemiah", 13), ("Est", "Esther", 10), ("Job", "Job", 42), ("Ps", "Psalms", 150),
    ("Sananl", "Proverbs", 31), ("Saarn", "Ecclesiastes", 12), ("Laul. l.", "Song of Solomon", 8),
    ("Jes", "Isaiah", 66), ("Jer", "Jeremiah", 52), ("Val.", "Lamentations", 5),
    ("Hes", "Ezekiel", 48), ("Dan", "Daniel", 12), ("Hoos", "Hosea", 14), ("Joel", "Joel", 3),
    ("Aam", "Amos", 9), ("Ob", "Obadiah", 1), ("Joona", "Jonah", 4), ("Miika", "Micah", 7),
    ("Nah", "Nahum", 3), ("Hab", "Habakkuk", 3), ("Sef", "Zephaniah", 3), ("Hagg", "Haggai", 2),
    ("Sak", "Zechariah", 14), ("Mal", "Malachi", 4),
    # New Testament
    ("Matt", "Matthew", 28), ("Mark", "Mark", 16), ("Luuk", "Luke", 24), ("Joh", "John", 21),
    ("Ap. t.", "Acts", 28), ("Room", "Romans", 16), ("1. Kor", "1 Corinthians", 16),
    ("2. Kor", "2 Corinthians", 13), ("Gal", "Galatians", 6), ("Ef", "Ephesians", 6),
    ("Fil", "Philippians", 4), ("Kol", "Colossians", 4), ("1. Tess", "1 Thessalonians", 5),
    ("2. Tess", "2 Thessalonians", 3), ("1. Tim", "1 Timothy", 6), ("2. Tim", "2 Timothy", 4),
    ("Tiit", "Titus", 3), ("Filem", "Philemon", 1), ("Hepr", "Hebrews", 13), ("Jaak", "James", 5),
    ("1. Piet", "1 Peter", 5), ("2. Piet", "2 Peter", 3), ("1. Joh", "1 John", 5),
    ("2. Joh", "2 John", 1), ("3. Joh", "3 John", 1), ("Juud", "Jude", 1), ("Ilm", "Revelation", 22)
]

OT_BOOKS = BIBLE_BOOKS[:39]
NT_BOOKS = BIBLE_BOOKS[39:]

# Common book name aliases
BOOK_ALIASES = {
    "genesis": "1. Moos", "gen": "1. Moos",
    "exodus": "2. Moos", "exod": "2. Moos",
    "psalms": "Ps", "psalm": "Ps",
    "proverbs": "Sananl", "prov": "Sananl",
    "matthew": "Matt", "matt": "Matt",
    "mark": "Mark",
    "luke": "Luuk",
    "john": "Joh",
    "acts": "Ap. t.",
    "romans": "Room", "rom": "Room",
    "revelation": "Ilm", "rev": "Ilm",
}


def get_book_info(book_name: str) -> tuple:
    """Find book info by name (case insensitive, supports aliases)."""
    book_lower = book_name.lower().strip()

    # Check aliases first
    if book_lower in BOOK_ALIASES:
        fi_abbrev = BOOK_ALIASES[book_lower]
        for fi, en, chapters in BIBLE_BOOKS:
            if fi == fi_abbrev:
                return (fi, en, chapters)

    # Search by Finnish abbreviation or English name
    for fi, en, chapters in BIBLE_BOOKS:
        if fi.lower() == book_lower or en.lower() == book_lower:
            return (fi, en, chapters)

    return None


def get_section_books(section: str) -> list:
    """Get books for a section (OT, NT, or OT+NT)."""
    if section.upper() == "OT":
        return OT_BOOKS
    elif section.upper() == "NT":
        return NT_BOOKS
    else:
        return BIBLE_BOOKS


def generate_plan_from_book(book_name: str, days: int) -> dict:
    """Generate a reading plan for a single book."""
    book_info = get_book_info(book_name)
    if not book_info:
        print(f"Error: Unknown book '{book_name}'", file=sys.stderr)
        sys.exit(1)

    fi_abbrev, en_name, total_chapters = book_info

    # Adjust days if more days requested than chapters
    actual_days = min(days, total_chapters)

    # Distribute chapters across days evenly
    plan_days = []
    chapters_assigned = 0

    for day_num in range(1, actual_days + 1):
        # Calculate how many chapters this day should have
        remaining_days = actual_days - day_num + 1
        remaining_chapters = total_chapters - chapters_assigned
        chapters_today = remaining_chapters // remaining_days

        start_chapter = chapters_assigned + 1
        end_chapter = chapters_assigned + chapters_today

        reading = {"book": fi_abbrev, "chapter_start": start_chapter}
        if end_chapter > start_chapter:
            reading["chapter_end"] = end_chapter

        plan_days.append({
            "day_number": day_num,
            "title": None,
            "readings": [reading]
        })

        chapters_assigned = end_chapter

    return {
        "plan": {
            "slug": f"{en_name.lower().replace(' ', '-')}-{actual_days}-days",
            "name_fi": f"{en_name} {actual_days} päivässä",
            "name_en": f"{en_name} in {actual_days} Days",
            "description_fi": f"Lue {en_name} {actual_days} päivässä",
            "description_en": f"Read {en_name} in {actual_days} days",
            "duration_days": actual_days,
            "is_active": True,
            "sort_order": 100
        },
        "days": plan_days
    }


def generate_plan_from_section(section: str, days: int) -> dict:
    """Generate a reading plan for a Bible section (OT, NT, or full)."""
    books = get_section_books(section)
    total_chapters = sum(chapters for _, _, chapters in books)
    chapters_per_day = total_chapters / days

    plan_days = []
    book_idx = 0
    chapter = 1

    for day_num in range(1, days + 1):
        day_readings = []
        chapters_today = 0
        target_chapters = chapters_per_day if day_num < days else float('inf')

        while chapters_today < target_chapters and book_idx < len(books):
            fi_abbrev, _, book_chapters = books[book_idx]

            # How many chapters from this book?
            remaining_in_book = book_chapters - chapter + 1
            chapters_needed = target_chapters - chapters_today
            chapters_to_read = min(remaining_in_book, max(1, int(chapters_needed)))

            reading = {"book": fi_abbrev, "chapter_start": chapter}
            end_chapter = chapter + chapters_to_read - 1
            if end_chapter > chapter:
                reading["chapter_end"] = end_chapter

            day_readings.append(reading)
            chapters_today += chapters_to_read

            if end_chapter >= book_chapters:
                # Move to next book
                book_idx += 1
                chapter = 1
            else:
                chapter = end_chapter + 1

        if day_readings:
            plan_days.append({
                "day_number": day_num,
                "title": None,
                "readings": day_readings
            })

        if book_idx >= len(books):
            break

    section_names = {
        "OT": ("Vanha testamentti", "Old Testament"),
        "NT": ("Uusi testamentti", "New Testament"),
        "OT+NT": ("Raamattu", "Bible")
    }
    fi_name, en_name = section_names.get(section.upper(), ("Raamattu", "Bible"))

    return {
        "plan": {
            "slug": f"{en_name.lower().replace(' ', '-')}-{days}-days",
            "name_fi": f"{fi_name} {days} päivässä",
            "name_en": f"{en_name} in {days} Days",
            "description_fi": f"Lue {fi_name} {days} päivässä",
            "description_en": f"Read {en_name} in {days} days",
            "duration_days": len(plan_days),
            "is_active": True,
            "sort_order": 100
        },
        "days": plan_days
    }


def generate_sql_migration(plan_data: dict) -> str:
    """Generate SQL migration for the reading plan."""
    plan = plan_data["plan"]
    days = plan_data["days"]

    def escape_sql(s):
        if s is None:
            return "NULL"
        return "'" + s.replace("'", "''") + "'"

    sql = f"""-- Reading Plan: {plan['name_fi']}
-- Generated: {datetime.now().isoformat()}

-- Step 1: Create the plan
INSERT INTO bible_schema.reading_plans (
  id, slug, name_fi, name_en, description_fi, duration_days, is_active, sort_order
) VALUES (
  gen_random_uuid(),
  {escape_sql(plan["slug"])},
  {escape_sql(plan["name_fi"])},
  {escape_sql(plan.get("name_en"))},
  {escape_sql(plan.get("description_fi"))},
  {plan["duration_days"]},
  {str(plan["is_active"]).lower()},
  {plan["sort_order"]}
);

-- Step 2: Add daily readings
WITH plan AS (
  SELECT id FROM bible_schema.reading_plans WHERE slug = {escape_sql(plan["slug"])}
)
INSERT INTO bible_schema.reading_plan_days (id, plan_id, day_number, title, readings)
SELECT
  gen_random_uuid(),
  plan.id,
  day_num,
  title,
  readings::jsonb
FROM plan, (VALUES
"""

    values = []
    for day in days:
        readings_json = json.dumps(day["readings"], ensure_ascii=False)
        title = f"'{day['title']}'" if day['title'] else 'NULL'
        values.append(f"  ({day['day_number']}, {title}, '{readings_json}')")

    sql += ",\n".join(values)
    sql += "\n) AS days(day_num, title, readings);\n"

    return sql


def main():
    parser = argparse.ArgumentParser(description="Generate Bible reading plan")
    parser.add_argument("--generate", action="store_true", help="Generate plan locally")
    parser.add_argument("--book", help="Single book to read (e.g., John, Psalms)")
    parser.add_argument("--sections", default="OT+NT", choices=["OT", "NT", "OT+NT"],
                        help="Bible sections to include")
    parser.add_argument("--days", type=int, required=True, help="Number of days for the plan")
    parser.add_argument("--name-fi", help="Finnish name (auto-generated if not provided)")
    parser.add_argument("--name-en", help="English name (auto-generated if not provided)")
    parser.add_argument("--output", "-o", help="Output JSON file (default: stdout)")
    parser.add_argument("--sql", action="store_true", help="Also generate SQL migration")

    args = parser.parse_args()

    # Generate plan
    if args.book:
        plan_data = generate_plan_from_book(args.book, args.days)
    else:
        plan_data = generate_plan_from_section(args.sections, args.days)

    # Override names if provided
    if args.name_fi:
        plan_data["plan"]["name_fi"] = args.name_fi
    if args.name_en:
        plan_data["plan"]["name_en"] = args.name_en

    # Output JSON
    json_output = json.dumps(plan_data, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"Saved plan to {args.output}", file=sys.stderr)

        if args.sql:
            sql_file = args.output.replace(".json", ".sql")
            sql_output = generate_sql_migration(plan_data)
            with open(sql_file, "w", encoding="utf-8") as f:
                f.write(sql_output)
            print(f"Saved SQL migration to {sql_file}", file=sys.stderr)
    else:
        print(json_output)

        if args.sql:
            print("\n-- SQL MIGRATION --\n", file=sys.stderr)
            print(generate_sql_migration(plan_data), file=sys.stderr)

    # Print summary
    print(f"\nPlan Summary:", file=sys.stderr)
    print(f"  Name: {plan_data['plan']['name_fi']}", file=sys.stderr)
    print(f"  Days: {plan_data['plan']['duration_days']}", file=sys.stderr)
    total_readings = sum(len(d["readings"]) for d in plan_data["days"])
    print(f"  Total reading blocks: {total_readings}", file=sys.stderr)


if __name__ == "__main__":
    main()
