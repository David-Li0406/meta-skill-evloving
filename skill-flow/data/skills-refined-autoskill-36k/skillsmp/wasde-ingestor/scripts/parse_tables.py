"""
WASDE Table Parser Script

Parses WASDE PDF/HTML reports and extracts supply-demand tables.
"""

import re
import json
from typing import Dict, List, Optional, Any
from difflib import SequenceMatcher


# Table name aliases for fuzzy matching
TABLE_ALIASES = {
    # Grains - US
    "wheat_us": [
        "U.S. Wheat Supply and Use",
        "Wheat: U.S. Supply and Use",
        "U.S. Wheat Supply and Disappearance"
    ],
    "corn_us": [
        "U.S. Feed Grain and Corn Supply and Use",
        "Corn: U.S. Supply and Use",
        "U.S. Corn Supply and Disappearance"
    ],
    "rice_us": [
        "U.S. Rice Supply and Use",
        "Rice: U.S. Supply and Use"
    ],

    # Grains - World
    "wheat_world": [
        "World Wheat Supply and Use",
        "Wheat: World Supply and Use"
    ],
    "corn_world": [
        "World Corn Supply and Use",
        "Corn: World Supply and Use",
        "Coarse Grains: World Supply and Use"
    ],

    # Oilseeds - US
    "soybeans_us": [
        "U.S. Soybeans Supply and Use",
        "Soybeans: U.S. Supply and Use",
        "U.S. Soybeans and Products Supply and Use"
    ],
    "soybean_oil_us": [
        "U.S. Soybean Oil Supply and Use",
        "Soybean Oil: U.S. Supply and Use"
    ],
    "soybean_meal_us": [
        "U.S. Soybean Meal Supply and Use",
        "Soybean Meal: U.S. Supply and Use"
    ],

    # Oilseeds - World
    "soybeans_world": [
        "World Soybean Supply and Use",
        "Soybeans: World Supply and Use"
    ],

    # Cotton
    "cotton_us": [
        "U.S. Cotton Supply and Use",
        "Cotton: U.S. Supply and Use",
        "U.S. Upland Cotton Supply and Use"
    ],
    "cotton_world": [
        "World Cotton Supply and Use",
        "Cotton: World Supply and Use"
    ],

    # Livestock
    "beef_us": [
        "U.S. Beef Supply and Use",
        "Beef: U.S. Supply and Use"
    ],
    "pork_us": [
        "U.S. Pork Supply and Use",
        "Pork: U.S. Supply and Use"
    ],
    "broiler_us": [
        "U.S. Broiler Supply and Use",
        "Broiler: U.S. Supply and Use"
    ],

    # Sugar
    "sugar_us": [
        "U.S. Sugar Supply and Use",
        "Sugar: U.S. Supply and Use"
    ],
    "sugar_mexico": [
        "Mexico Sugar Supply and Use",
        "Sugar: Mexico Supply and Use"
    ]
}


def parse_wasde_pdf(
    pdf_path: str,
    tables: List[str],
    fuzzy_match: bool = True,
    fuzzy_threshold: float = 0.8
) -> Dict[str, Any]:
    """
    Parse WASDE PDF and extract specified tables.

    Args:
        pdf_path: Path to PDF file
        tables: List of table IDs to extract
        fuzzy_match: Use fuzzy matching for table titles
        fuzzy_threshold: Minimum similarity for fuzzy match

    Returns:
        dict: Parsed table data keyed by table ID
    """
    try:
        import pdfplumber
    except ImportError:
        print("pdfplumber not installed. Install with: pip install pdfplumber")
        return {}

    results = {}
    tables_found = set()

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            # Extract text for table identification
            text = page.extract_text() or ""

            # Extract tables from page
            page_tables = page.extract_tables()

            for table_data in page_tables:
                if not table_data or len(table_data) < 2:
                    continue

                # Try to identify table
                table_id = _identify_table(
                    text, table_data,
                    tables, tables_found,
                    fuzzy_match, fuzzy_threshold
                )

                if table_id and table_id not in tables_found:
                    parsed = _parse_table_data(table_data, table_id)
                    if parsed:
                        parsed['source_page'] = page_num
                        results[table_id] = parsed
                        tables_found.add(table_id)

    # Report missing tables
    missing = set(tables) - tables_found
    if missing:
        print(f"Warning: Could not find tables: {missing}")

    return results


def parse_wasde_html(
    html_content: str,
    tables: List[str],
    fuzzy_match: bool = True,
    fuzzy_threshold: float = 0.8
) -> Dict[str, Any]:
    """
    Parse WASDE HTML page and extract specified tables.

    Args:
        html_content: HTML content
        tables: List of table IDs to extract
        fuzzy_match: Use fuzzy matching
        fuzzy_threshold: Minimum similarity

    Returns:
        dict: Parsed table data
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("BeautifulSoup not installed. Install with: pip install beautifulsoup4")
        return {}

    soup = BeautifulSoup(html_content, 'html.parser')
    results = {}
    tables_found = set()

    # Find all tables
    html_tables = soup.find_all('table')

    for html_table in html_tables:
        # Get surrounding text for identification
        context = _get_table_context(html_table)

        # Convert to list of lists
        table_data = _html_table_to_list(html_table)

        if not table_data or len(table_data) < 2:
            continue

        # Try to identify
        table_id = _identify_table(
            context, table_data,
            tables, tables_found,
            fuzzy_match, fuzzy_threshold
        )

        if table_id and table_id not in tables_found:
            parsed = _parse_table_data(table_data, table_id)
            if parsed:
                results[table_id] = parsed
                tables_found.add(table_id)

    return results


def _identify_table(
    context: str,
    table_data: List[List],
    target_tables: List[str],
    already_found: set,
    fuzzy_match: bool,
    threshold: float
) -> Optional[str]:
    """Identify table from context and content."""

    context_lower = context.lower()

    for table_id in target_tables:
        if table_id in already_found:
            continue

        aliases = TABLE_ALIASES.get(table_id, [])

        for alias in aliases:
            alias_lower = alias.lower()

            # Exact match
            if alias_lower in context_lower:
                return table_id

            # Fuzzy match
            if fuzzy_match:
                similarity = SequenceMatcher(None, alias_lower, context_lower).ratio()
                if similarity >= threshold:
                    return table_id

    return None


def _parse_table_data(
    table_data: List[List],
    table_id: str
) -> Optional[Dict]:
    """Parse table data into structured format."""

    if not table_data or len(table_data) < 2:
        return None

    # First row(s) are headers
    headers = _clean_headers(table_data[0])

    # Find data rows (skip header rows)
    data_start = 1
    for i, row in enumerate(table_data[1:], 1):
        if _is_data_row(row):
            data_start = i
            break

    # Parse data rows
    records = []
    for row in table_data[data_start:]:
        if not _is_data_row(row):
            continue

        record = {}
        for j, (header, cell) in enumerate(zip(headers, row)):
            if header and cell:
                cleaned_header = _normalize_field_name(header)
                cleaned_value = _parse_cell_value(cell)
                record[cleaned_header] = cleaned_value

        if record:
            records.append(record)

    return {
        "table_id": table_id,
        "headers": headers,
        "records": records,
        "raw_data": table_data
    }


def _clean_headers(row: List) -> List[str]:
    """Clean and normalize header row."""
    headers = []
    for cell in row:
        if cell:
            # Remove line breaks, extra spaces
            cleaned = re.sub(r'\s+', ' ', str(cell).strip())
            headers.append(cleaned)
        else:
            headers.append("")
    return headers


def _normalize_field_name(name: str) -> str:
    """Normalize field name to snake_case."""
    # Remove special characters
    name = re.sub(r'[^\w\s]', '', name)
    # Convert to lowercase with underscores
    name = re.sub(r'\s+', '_', name.lower().strip())
    return name


def _parse_cell_value(cell: str) -> Any:
    """Parse cell value to appropriate type."""
    if not cell or cell.strip() in ['', '-', '--', 'N/A', 'n.a.', '*']:
        return None

    cell = str(cell).strip()

    # Handle negative numbers in parentheses: (100) -> -100
    if cell.startswith('(') and cell.endswith(')'):
        cell = '-' + cell[1:-1]

    # Remove thousand separators
    cell = cell.replace(',', '')

    # Try to parse as number
    try:
        if '.' in cell:
            return float(cell)
        else:
            return int(cell)
    except ValueError:
        return cell


def _is_data_row(row: List) -> bool:
    """Check if row contains data (not headers/notes)."""
    if not row:
        return False

    # Count non-empty cells
    non_empty = sum(1 for cell in row if cell and str(cell).strip())

    # Count numeric cells
    numeric = 0
    for cell in row:
        if cell:
            try:
                _parse_cell_value(str(cell))
                numeric += 1
            except:
                pass

    # Data row should have multiple numeric values
    return non_empty >= 2 and numeric >= 1


def _html_table_to_list(table) -> List[List]:
    """Convert HTML table to list of lists."""
    rows = []
    for tr in table.find_all('tr'):
        cells = []
        for td in tr.find_all(['td', 'th']):
            cells.append(td.get_text(strip=True))
        if cells:
            rows.append(cells)
    return rows


def _get_table_context(table) -> str:
    """Get context text around a table element."""
    context_parts = []

    # Previous sibling text
    prev = table.find_previous_sibling()
    if prev:
        context_parts.append(prev.get_text(strip=True)[:200])

    # Caption if exists
    caption = table.find('caption')
    if caption:
        context_parts.append(caption.get_text(strip=True))

    # First row (often contains title)
    first_row = table.find('tr')
    if first_row:
        context_parts.append(first_row.get_text(strip=True)[:200])

    return ' '.join(context_parts)


def get_tables_for_commodities(
    commodities: List[str],
    scope: List[str]
) -> List[str]:
    """
    Get list of table IDs for specified commodities and scope.

    Args:
        commodities: List of commodity names or groups
        scope: List of scopes ("us", "world")

    Returns:
        list: Table IDs to parse
    """
    # Expand commodity groups
    expanded = []
    for c in commodities:
        if c == "all":
            expanded.extend(TABLE_ALIASES.keys())
        elif c == "grains":
            expanded.extend([k for k in TABLE_ALIASES.keys()
                          if any(g in k for g in ['wheat', 'corn', 'rice', 'barley', 'sorghum', 'oats'])])
        elif c == "oilseeds":
            expanded.extend([k for k in TABLE_ALIASES.keys()
                          if 'soy' in k])
        elif c == "cotton":
            expanded.extend([k for k in TABLE_ALIASES.keys()
                          if 'cotton' in k])
        elif c == "livestock":
            expanded.extend([k for k in TABLE_ALIASES.keys()
                          if any(l in k for l in ['beef', 'pork', 'broiler', 'turkey', 'egg', 'dairy'])])
        elif c == "sugar":
            expanded.extend([k for k in TABLE_ALIASES.keys()
                          if 'sugar' in k])
        else:
            # Single commodity
            expanded.extend([k for k in TABLE_ALIASES.keys() if c in k])

    # Filter by scope
    filtered = []
    for table_id in set(expanded):
        if 'us' in scope and table_id.endswith('_us'):
            filtered.append(table_id)
        if 'world' in scope and table_id.endswith('_world'):
            filtered.append(table_id)

    return sorted(set(filtered))


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse WASDE tables")
    parser.add_argument("--pdf", type=str, help="PDF file path")
    parser.add_argument("--html", type=str, help="HTML file path")
    parser.add_argument("--tables", type=str, default="all", help="Tables to parse (comma-separated)")
    parser.add_argument("--output", type=str, help="Output JSON file")

    args = parser.parse_args()

    tables = get_tables_for_commodities(
        args.tables.split(','),
        ['us', 'world']
    )

    if args.pdf:
        results = parse_wasde_pdf(args.pdf, tables)
    elif args.html:
        with open(args.html, 'r') as f:
            html_content = f.read()
        results = parse_wasde_html(html_content, tables)
    else:
        print("Please specify --pdf or --html")
        exit(1)

    output = json.dumps(results, indent=2, default=str)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Results written to: {args.output}")
    else:
        print(output)
