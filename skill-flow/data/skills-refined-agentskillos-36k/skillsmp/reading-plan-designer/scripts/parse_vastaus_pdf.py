#!/usr/bin/env python3
"""
Parse the Vastaus.net Bible reading plan PDF and convert to project format.

The PDF contains a 365-day reading plan with 4 daily readings:
- Old Testament (VT)
- New Testament (UT)
- Psalms (Ps)
- Proverbs (Sananl)

Usage:
    python parse_vastaus_pdf.py --input raamatunlukuslma.pdf --output vastaus-365.json --sql

Requires: pip install pymupdf
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: pymupdf not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)


# Finnish month names to month number
FINNISH_MONTHS = {
    "TAMMIKUU": 1, "HELMIKUU": 2, "MAALISKUU": 3, "HUHTIKUU": 4,
    "TOUKOKUU": 5, "KESÄKUU": 6, "HEINÄKUU": 7, "ELOKUU": 8,
    "SYYSKUU": 9, "LOKAKUU": 10, "MARRASKUU": 11, "JOULUKUU": 12
}

# Days in each month (non-leap year)
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Book abbreviation normalization (PDF format -> project format)
BOOK_ALIASES = {
    # OT books
    "1moos": "1. Moos", "2moos": "2. Moos", "3moos": "3. Moos",
    "4moos": "4. Moos", "5moos": "5. Moos",
    "ms": "1. Moos",  # Typo in PDF (day 14)
    "joos": "Joos", "tuom": "Tuom", "ruut": "Ruut",
    "1sam": "1. Sam", "1 sam": "1. Sam",
    "2sam": "2. Sam", "2 sam": "2. Sam",
    "1kun": "1. Kun", "1 kun": "1. Kun",
    "2kun": "2. Kun", "2 kun": "2. Kun",
    "1aik": "1. Aik", "1 aik": "1. Aik",
    "2aik": "2. Aik", "2 aik": "2. Aik",
    "esra": "Esra", "neh": "Neh", "est": "Est",
    "job": "Job", "ps": "Ps",
    "sananl": "Sananl", "snl": "Sananl",
    "saarn": "Saarn", "laul. l.": "Laul. l.", "laul.l.": "Laul. l.",
    "laul. l": "Laul. l.", "laul.": "Laul. l.",
    "jes": "Jes", "jer": "Jer",
    "valit": "Val.", "val": "Val.",
    "hes": "Hes", "dan": "Dan",
    "hoos": "Hoos", "joel": "Joel", "jooel": "Joel",
    "aam": "Aam", "ob": "Ob", "joona": "Joona",
    "miika": "Miika", "nah": "Nah", "hab": "Hab",
    "sef": "Sef", "hagg": "Hagg", "sak": "Sak", "mal": "Mal",
    # NT books
    "matt": "Matt", "mark": "Mark", "luuk": "Luuk", "joh": "Joh",
    "ap.t.": "Ap. t.", "ap.t": "Ap. t.", "ap. t.": "Ap. t.",
    "room": "Room",
    "1kor": "1. Kor", "1 kor": "1. Kor", "1kr": "1. Kor", "1kr.": "1. Kor",
    "2kor": "2. Kor", "2 kor": "2. Kor",
    "gal": "Gal", "ef": "Ef", "fil": "Fil", "kol": "Kol",
    "1tess": "1. Tess", "1 tess": "1. Tess",
    "2tess": "2. Tess", "2 tess": "2. Tess",
    "1tim": "1. Tim", "1 tim": "1. Tim",
    "2tim": "2. Tim", "2 tim": "2. Tim",
    "tit": "Tiit", "tiit": "Tiit",
    "filem": "Filem",
    "hepr": "Hepr", "jaak": "Jaak",
    "1piet": "1. Piet", "1 piet": "1. Piet",
    "2piet": "2. Piet", "2 piet": "2. Piet",
    "1joh": "1. Joh", "1 joh": "1. Joh",
    "2joh": "2. Joh", "2 joh": "2. Joh",
    "3joh": "3. Joh", "3 joh": "3. Joh",
    "juud": "Juud", "ilm": "Ilm",
}


def normalize_book(book: str) -> str:
    """Normalize book abbreviation to project format."""
    book_clean = book.strip().lower()
    # Remove trailing period if present
    if book_clean.endswith('.') and book_clean not in ['ap.t.', 'laul. l.']:
        book_clean = book_clean[:-1]

    if book_clean in BOOK_ALIASES:
        return BOOK_ALIASES[book_clean]

    # Try with lowercase
    return BOOK_ALIASES.get(book_clean, book.strip())


def parse_reference(ref_str: str) -> dict:
    """
    Parse a Bible reference string to ReadingReference format.

    Formats handled:
    - "1Moos.1:1 – 2:25"  (cross-chapter with en-dash)
    - "Matt.1:1-2:12"    (cross-chapter with hyphen)
    - "Ps.1:1-6"         (single chapter verse range)
    - "Ps.90:1–91:16"    (cross-chapter with en-dash)
    - "1 Sam.1:1 – 2:21" (book with space in name)
    - "Ap.t.10:23a"      (verse with letter suffix)
    - "Fil.3:4b-4:1"     (verse range with letter suffix)
    """
    ref_str = ref_str.strip()
    if not ref_str:
        return None

    # Normalize dashes: en-dash (–) and em-dash (—) to hyphen (-)
    ref_str = ref_str.replace('–', '-').replace('—', '-')

    # Remove letter suffixes from verse numbers (like 23a, 4b)
    ref_str = re.sub(r'(\d+)[a-z](?=\s*[-,]|\s*$)', r'\1', ref_str)

    # Handle books with numbers (1Sam, 2Moos, etc.)
    # Pattern: book.chapter:verse or book chapter:verse
    # Examples: 1Moos.1:1, Ps.1:1-6, 1 Sam.1:1 - 2:21

    # Split book from reference
    # Try to find the book name (may include number prefix and space)
    book_match = re.match(r'^(\d?\s?[A-Za-zäöåÄÖÅ.]+\.?\s?[A-Za-z]*\.?)\s*\.?\s*', ref_str)
    if not book_match:
        print(f"Warning: Could not parse book from '{ref_str}'", file=sys.stderr)
        return None

    book_raw = book_match.group(1).strip()
    rest = ref_str[book_match.end():].strip()

    # Remove trailing period from book if it has one and rest starts with number
    if book_raw.endswith('.') and rest and rest[0].isdigit():
        book_raw = book_raw[:-1]

    book = normalize_book(book_raw)

    # Parse the chapter:verse part
    # Patterns:
    # - "1:1-6"           single chapter, verse range
    # - "1:1 - 2:25"      chapter:verse - chapter:verse
    # - "1:1-2:12"        chapter:verse-chapter:verse (no spaces)
    # - "1"               just chapter (rare in this PDF)

    if not rest:
        # Just book name, no chapter (shouldn't happen)
        return {"book": book, "chapter_start": 1}

    # Check if this is a cross-book reference (book name appears after dash)
    # e.g., "50:1 - 2Moos.2:10" or "27:14 - 4Moos.1:54"
    cross_book_match = re.match(r'(\d+):(\d+)\s*-\s*\d+[A-Za-z]', rest)
    if cross_book_match:
        # Just return the first part (we'll handle the second book separately)
        return {
            "book": book,
            "chapter_start": int(cross_book_match.group(1)),
            "verse_start": int(cross_book_match.group(2)),
        }

    # Check for cross-chapter range (contains two colons separated by hyphen)
    cross_chapter_match = re.match(r'(\d+):(\d+)\s*-\s*(\d+):(\d+)', rest)
    if cross_chapter_match:
        return {
            "book": book,
            "chapter_start": int(cross_chapter_match.group(1)),
            "verse_start": int(cross_chapter_match.group(2)),
            "chapter_end": int(cross_chapter_match.group(3)),
            "verse_end": int(cross_chapter_match.group(4))
        }

    # Single chapter with verse range: "1:1-6"
    single_chapter_match = re.match(r'(\d+):(\d+)-(\d+)$', rest)
    if single_chapter_match:
        return {
            "book": book,
            "chapter_start": int(single_chapter_match.group(1)),
            "verse_start": int(single_chapter_match.group(2)),
            "verse_end": int(single_chapter_match.group(3))
        }

    # Single chapter single verse: "1:1"
    single_verse_match = re.match(r'(\d+):(\d+)$', rest)
    if single_verse_match:
        return {
            "book": book,
            "chapter_start": int(single_verse_match.group(1)),
            "verse_start": int(single_verse_match.group(2)),
            "verse_end": int(single_verse_match.group(2))
        }

    # Just chapter: "1"
    chapter_only_match = re.match(r'(\d+)$', rest)
    if chapter_only_match:
        return {
            "book": book,
            "chapter_start": int(chapter_only_match.group(1))
        }

    print(f"Warning: Could not parse reference '{rest}' for book '{book}'", file=sys.stderr)
    return {"book": book, "chapter_start": 1}


def split_readings(line: str) -> list:
    """
    Split a line into individual reading references.

    The line format is: DAY OT_REF, NT_REF, PS.X:Y, SANANL.X:Y

    Tricky cases:
    - Cross-book references like "1Moos.50:1 - 2Moos.2:10"
    - Periods instead of commas as delimiters
    - Letter suffixes in verse numbers (23a, 4b)
    - Spaces in verse numbers (5: 15-21)
    """
    # First, remove the day number at the start
    line = re.sub(r'^\d+\s+', '', line)

    # Normalize dashes: en-dash (–) and em-dash (—) to hyphen (-)
    line = line.replace('–', '-').replace('—', '-')

    # Remove page headers that might have been picked up
    line = re.sub(r'RAAMATUN LUKUSUUNNITELMA.*?VASTAUS\.NET', '', line, flags=re.IGNORECASE)

    # Normalize spaces in verse numbers (e.g., "5: 15-21" -> "5:15-21")
    line = re.sub(r'(\d+):\s+(\d+)', r'\1:\2', line)

    # Normalize spaces around dashes in verse ranges (e.g., "6:12- 15" -> "6:12-15")
    line = re.sub(r'(\d+)-\s+(\d+)', r'\1-\2', line)
    line = re.sub(r'(\d+)\s+-(\d+)', r'\1-\2', line)

    # Fix double commas (e.g., ", ," -> ", ")
    line = re.sub(r',\s*,', ',', line)

    # Normalize: replace periods used as delimiters (followed by space and Ps or Sananl/Snl)
    # E.g., "Joh.8:21-30. Ps.111:1-10" -> "Joh.8:21-30, Ps.111:1-10"
    line = re.sub(r'\.\s+(Ps\.|Sananl\.|Snl\.)', r', \1', line)

    # Handle cross-book OT references BEFORE splitting
    # Pattern: "1Moos.50:1 - 2Moos.2:10" -> "1Moos.50:1, 2Moos.2:10"
    # This regex finds book transitions across OT books
    line = re.sub(
        r'(\d[A-Za-z]+\.?\d+:\d+)\s*-\s*(\d[A-Za-z]+\.)',
        r'\1, \2',
        line
    )
    # Also handle "Tuom.21:1 - Ruut 1:22" type patterns (book with space before chapter)
    line = re.sub(
        r'([A-Za-z]+\.?\s*\d+:\d+)\s*-\s*([A-Za-z]+)\s+(\d)',
        r'\1, \2 \3',
        line
    )

    # Handle "5Moos.34:1 - Joos.2:24" pattern (numbered book to non-numbered book)
    line = re.sub(
        r'(\d[A-Za-z]+\.?\s*\d+:\d+)\s*-\s*([A-Za-z]+)\.(\d)',
        r'\1, \2.\3',
        line
    )

    # Handle "5Moos.34:1 - Joos.2:24" with space after book period
    line = re.sub(
        r'(\d[A-Za-z]+\.\d+:\d+)\s*-\s*([A-Za-z]+)\.\s*(\d)',
        r'\1, \2.\3',
        line
    )

    # Split by comma
    parts = []
    current = ""

    for char in line:
        if char == ',':
            # Check if this looks like a complete reference
            # A complete reference should end with a verse number (possibly with letter suffix)
            if re.search(r'\d+[a-z]?$', current.strip()):
                parts.append(current.strip())
                current = ""
            else:
                current += char
        else:
            current += char

    if current.strip():
        parts.append(current.strip())

    return parts


def extract_pdf_text(pdf_path: str) -> str:
    """Extract all text from PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def parse_pdf_content(text: str) -> list:
    """
    Parse the PDF text content into daily readings.

    Returns list of dicts with day_number and readings.
    """
    lines = text.split('\n')
    days = []
    current_month = 0
    day_offset = 0  # Days before current month
    pending_continuation = None  # For handling line continuations

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if not line:
            continue

        # Check for month header
        for month_name, month_num in FINNISH_MONTHS.items():
            if line.upper() == month_name:
                current_month = month_num
                # Calculate day offset (sum of days in previous months)
                day_offset = sum(DAYS_IN_MONTH[:month_num - 1])
                break

        # Check for day line (starts with number 1-31)
        day_match = re.match(r'^(\d{1,2})\s+(.+)', line)
        if day_match and current_month > 0:
            day_in_month = int(day_match.group(1))

            # Skip if day number seems too high (probably not a day line)
            if day_in_month > 31:
                continue

            readings_str = day_match.group(2)

            # Check if next line is a continuation (doesn't start with number or month)
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line:
                    i += 1
                    continue
                # If next line starts with a number or is a month, it's not a continuation
                if re.match(r'^\d+\s', next_line) or next_line.upper() in FINNISH_MONTHS:
                    break
                # It's a continuation line - append it
                readings_str += " " + next_line
                i += 1

            # Calculate absolute day number (1-365)
            day_number = day_offset + day_in_month

            # Split into individual readings
            reading_parts = split_readings(str(day_in_month) + " " + readings_str)

            readings = []
            for part in reading_parts:
                ref = parse_reference(part)
                if ref:
                    readings.append(ref)

            if readings:
                days.append({
                    "day_number": day_number,
                    "title": None,
                    "readings": readings
                })

    return days


def generate_sql_migration(plan_data: dict) -> str:
    """Generate SQL migration for the reading plan."""
    plan = plan_data["plan"]
    days = plan_data["days"]

    def escape_sql(s):
        if s is None:
            return "NULL"
        return "'" + s.replace("'", "''") + "'"

    sql = f"""-- Reading Plan: {plan['name_fi']}
-- Source: vastaus.net
-- Generated: {datetime.now().isoformat()}

-- Step 1: Create the plan
INSERT INTO bible_schema.reading_plans (
  id, slug, name_fi, name_en, description_fi, description_en, duration_days, is_active, sort_order
) VALUES (
  gen_random_uuid(),
  {escape_sql(plan["slug"])},
  {escape_sql(plan["name_fi"])},
  {escape_sql(plan.get("name_en"))},
  {escape_sql(plan.get("description_fi"))},
  {escape_sql(plan.get("description_en"))},
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
    parser = argparse.ArgumentParser(
        description="Parse Vastaus.net Bible reading plan PDF"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input PDF file path"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file path (default: stdout)"
    )
    parser.add_argument(
        "--sql",
        action="store_true",
        help="Also generate SQL migration file"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug information"
    )

    args = parser.parse_args()

    # Check input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Extract PDF text
    print(f"Reading PDF: {args.input}", file=sys.stderr)
    text = extract_pdf_text(args.input)

    if args.debug:
        print("--- PDF Text ---", file=sys.stderr)
        print(text[:2000], file=sys.stderr)
        print("--- End PDF Text ---", file=sys.stderr)

    # Parse content
    print("Parsing readings...", file=sys.stderr)
    days = parse_pdf_content(text)

    # Build plan data
    plan_data = {
        "plan": {
            "slug": "vastaus-365",
            "name_fi": "Raamattu vuodessa",
            "name_en": "Bible in a Year",
            "description_fi": "Lue Raamattu vuodessa: Vanha testamentti, Uusi testamentti, Psalmit ja Sananlaskut joka päivä",
            "description_en": "Read the Bible in a year: Old Testament, New Testament, Psalms and Proverbs every day",
            "duration_days": len(days),
            "is_active": True,
            "sort_order": 10
        },
        "days": days
    }

    # Output JSON
    json_output = json.dumps(plan_data, indent=2, ensure_ascii=False)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json_output, encoding="utf-8")
        print(f"Saved plan to {args.output}", file=sys.stderr)

        if args.sql:
            sql_path = output_path.with_suffix(".sql")
            sql_output = generate_sql_migration(plan_data)
            sql_path.write_text(sql_output, encoding="utf-8")
            print(f"Saved SQL migration to {sql_path}", file=sys.stderr)
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

    # Verify expected count
    if len(days) != 365:
        print(f"\nWarning: Expected 365 days but got {len(days)}", file=sys.stderr)

    # Check for days with wrong number of readings
    for day in days:
        if len(day["readings"]) != 4:
            print(f"  Day {day['day_number']}: {len(day['readings'])} readings (expected 4)", file=sys.stderr)


if __name__ == "__main__":
    main()
