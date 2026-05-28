"""Markdown table formatting utilities."""

from typing import Dict, List, Any


def format_table(headers: List[str], rows: List[List[str]], align: List[str] = None) -> str:
    """
    Format a GitHub-flavored Markdown table.

    Args:
        headers: Column headers
        rows: Table rows (list of string lists)
        align: List of alignments ('left', 'right', 'center'). Default: left for all

    Returns:
        Formatted Markdown table as string
    """
    if not headers:
        return ""

    # Default alignment to left
    if align is None:
        align = ["left"] * len(headers)

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    # Build separator line
    separators = []
    for i, width in enumerate(col_widths):
        if align[i] == "center":
            sep = ":" + "-" * (width - 2) + ":"
        elif align[i] == "right":
            sep = "-" * (width - 1) + ":"
        else:  # left
            sep = ":" + "-" * (width - 1)
        separators.append(sep)

    # Format header row
    header_cells = [str(headers[i]).ljust(col_widths[i]) for i in range(len(headers))]
    header_line = "| " + " | ".join(header_cells) + " |"

    # Format separator row
    separator_cells = [separators[i].ljust(col_widths[i]) for i in range(len(separators))]
    separator_line = "| " + " | ".join(separator_cells) + " |"

    # Format data rows
    data_lines = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            if i < len(col_widths):
                if align[i] == "right":
                    cells.append(str(cell).rjust(col_widths[i]))
                elif align[i] == "center":
                    cells.append(str(cell).center(col_widths[i]))
                else:
                    cells.append(str(cell).ljust(col_widths[i]))
        data_lines.append("| " + " | ".join(cells) + " |")

    # Combine all lines
    result = [header_line, separator_line] + data_lines
    return "\n".join(result)


def format_language_table(stats: Dict[str, Dict[str, int]]) -> str:
    """
    Format statistics grouped by language as a Markdown table.

    Args:
        stats: Dictionary mapping language to stats
            {'Rust': {'files': 10, 'code': 100, 'blank': 20, 'comment': 30}, ...}

    Returns:
        Formatted Markdown table
    """
    if not stats:
        return "No files found."

    headers = ["Language", "Files", "Code", "Blank", "Comment", "Total"]
    rows = []
    align = ["left", "right", "right", "right", "right", "right"]

    # Sort by total lines descending
    sorted_languages = sorted(
        stats.items(),
        key=lambda x: x[1].get("total", 0),
        reverse=True
    )

    for lang, lang_stats in sorted_languages:
        total = lang_stats.get("total", 0)
        rows.append([
            lang,
            str(lang_stats.get("files", 0)),
            str(lang_stats.get("code", 0)),
            str(lang_stats.get("blank", 0)),
            str(lang_stats.get("comment", 0)),
            str(total)
        ])

    return format_table(headers, rows, align)


def format_directory_table(
    stats: Dict[str, Dict[str, Any]],
    depth: int = 2
) -> str:
    """
    Format statistics grouped by directory as a Markdown table.

    Args:
        stats: Dictionary mapping directory to stats
            {'src/': {'files': 10, 'code': 100, 'comment': 30, 'languages': ['Rust', 'Python']}, ...}
        depth: Directory depth limit (for display purposes)

    Returns:
        Formatted Markdown table
    """
    if not stats:
        return "No directories found."

    headers = ["Directory", "Files", "Code", "Comment", "Languages"]
    rows = []
    align = ["left", "right", "right", "right", "left"]

    # Sort by code lines descending
    sorted_dirs = sorted(
        stats.items(),
        key=lambda x: x[1].get("code", 0),
        reverse=True
    )

    for directory, dir_stats in sorted_dirs:
        languages = dir_stats.get("languages", [])
        lang_str = ", ".join(sorted(languages))

        rows.append([
            directory,
            str(dir_stats.get("files", 0)),
            str(dir_stats.get("code", 0)),
            str(dir_stats.get("comment", 0)),
            lang_str
        ])

    return format_table(headers, rows, align)


def format_summary(total_stats: Dict[str, int]) -> str:
    """
    Format summary statistics as Markdown.

    Args:
        total_stats: Dictionary with total counts
            {'files': 100, 'code': 10000, 'blank': 2000, 'comment': 1500}

    Returns:
        Formatted summary string
    """
    lines = [
        "## Summary",
        "",
        f"- **Total Files**: {total_stats.get('files', 0)}",
        f"- **Code Lines**: {total_stats.get('code', 0)}",
        f"- **Blank Lines**: {total_stats.get('blank', 0)}",
        f"- **Comment Lines**: {total_stats.get('comment', 0)}",
        f"- **Total Lines**: {total_stats.get('total', 0)}",
    ]

    if total_stats.get('code', 0) > 0:
        comment_ratio = (total_stats.get('comment', 0) / total_stats.get('code', 1)) * 100
        lines.append(f"- **Comment Ratio**: {comment_ratio:.1f}%")

    return "\n".join(lines)


def combine_tables(*tables: str) -> str:
    """
    Combine multiple tables with spacing.

    Args:
        *tables: Variable number of table strings

    Returns:
        Combined string with double spacing between tables
    """
    return "\n\n".join(filter(None, tables))