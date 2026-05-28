"""
Output formatting functions for helix-memory CLI.

Provides consistent formatting across all CLI commands for displaying memories
in various contexts (single-line, with tags, with dates, detailed view).
"""

from datetime import datetime
from typing import Optional


def format_date(dt: datetime) -> str:
    """
    Format datetime for display.

    Args:
        dt: datetime object to format

    Returns:
        Formatted string: 'YYYY-MM-DD HH:MM'

    Example:
        >>> format_date(datetime(2026, 1, 12, 14, 30))
        '2026-01-12 14:30'
    """
    return dt.strftime('%Y-%m-%d %H:%M')


def format_memory_line(memory: dict, max_content_length: int = 80) -> str:
    """
    Format memory as single line: [CATEGORY - importance] content...

    Args:
        memory: Memory dict with 'category', 'importance', 'content' keys
        max_content_length: Maximum content length before truncation

    Returns:
        Formatted single-line string

    Example:
        >>> format_memory_line({'category': 'fact', 'importance': 7, 'content': 'Example memory'})
        '[FACT - 7] Example memory'
    """
    importance = memory.get('importance', '?')
    category = memory.get('category', 'unknown').upper()
    content = memory.get('content', '')[:max_content_length]

    # Add ellipsis if truncated
    if len(memory.get('content', '')) > max_content_length:
        content += '...'

    return f"[{category} - {importance}] {content}"


def format_memory_with_tags(memory: dict, max_content_length: int = 100) -> str:
    """
    Format memory with tags and ID on separate lines.

    Args:
        memory: Memory dict with 'category', 'importance', 'content', 'tags', 'id' keys
        max_content_length: Maximum content length before truncation

    Returns:
        Multi-line formatted string with content, tags, and ID

    Example:
        >>> mem = {'category': 'fact', 'importance': 7, 'content': 'Example', 'tags': 'test,demo', 'id': 'abc123'}
        >>> print(format_memory_with_tags(mem))
        [FACT - 7] Example...
          Tags: test,demo
          ID: abc123
    """
    importance = memory.get('importance', '?')
    category = memory.get('category', 'unknown').upper()
    content = memory.get('content', '')[:max_content_length]
    tags = memory.get('tags', '')
    mid = memory.get('id', '')

    # Add ellipsis if truncated
    if len(memory.get('content', '')) > max_content_length:
        content += '...'

    lines = [f"[{category} - {importance}] {content}"]
    lines.append(f"  Tags: {tags}")
    lines.append(f"  ID: {mid}")

    return '\n'.join(lines)


def format_memory_with_date(memory: dict, date_field: str = '_created_at') -> str:
    """
    Format memory with date on first line.

    Args:
        memory: Memory dict with date field and standard memory keys
        date_field: Name of datetime field in memory dict (default: '_created_at')

    Returns:
        Multi-line formatted string with date, content, and ID

    Example:
        >>> from datetime import datetime
        >>> mem = {
        ...     'category': 'fact',
        ...     'importance': 7,
        ...     'content': 'Example memory',
        ...     'id': 'abc123',
        ...     '_created_at': datetime(2026, 1, 12, 14, 30)
        ... }
        >>> print(format_memory_with_date(mem))
        [FACT - 7] 2026-01-12 14:30
          Example memory...
          ID: abc123
    """
    importance = memory.get('importance', '?')
    category = memory.get('category', 'unknown').upper()
    content = memory.get('content', '')[:80]
    mid = memory.get('id', '')

    # Add ellipsis if truncated
    if len(memory.get('content', '')) > 80:
        content += '...'

    lines = []

    # First line: [CATEGORY - importance] date
    if date_field in memory:
        created_dt = memory[date_field]
        created_str = format_date(created_dt)
        lines.append(f"[{category} - {importance}] {created_str}")
    else:
        # No date available, use standard format
        lines.append(f"[{category} - {importance}]")

    # Content and ID
    lines.append(f"  {content}")
    lines.append(f"  ID: {mid}")

    return '\n'.join(lines)


def format_memory_detail(memory: dict) -> str:
    """
    Format memory for detailed display (cmd_show).

    Shows all fields with full content (no truncation).

    Args:
        memory: Memory dict with all standard fields

    Returns:
        Multi-line detailed format with separator lines

    Example:
        >>> mem = {
        ...     'id': 'abc123',
        ...     'category': 'fact',
        ...     'importance': 7,
        ...     'content': 'Detailed memory content',
        ...     'tags': 'test,example',
        ...     'created_at': '2026-01-12T14:30:00'
        ... }
        >>> print(format_memory_detail(mem))
        ============================================================
        [FACT-7] abc123
        ============================================================
        Content:    Detailed memory content
        Category:   fact
        Importance: 7
        Tags:       test,example
        Created:    2026-01-12T14:30:00
        Full ID:    abc123
    """
    full_id = memory.get('id', '')
    category = memory.get('category', '?').upper()
    importance = memory.get('importance', 0)
    content = memory.get('content', '')
    tags = memory.get('tags', '')
    created_at = memory.get('created_at', '?')

    lines = []
    lines.append("=" * 60)
    lines.append(f"[{category}-{importance}] {full_id[:8]}")
    lines.append("=" * 60)
    lines.append(f"Content:    {content}")
    lines.append(f"Category:   {category.lower()}")
    lines.append(f"Importance: {importance}")
    lines.append(f"Tags:       {tags}")
    lines.append(f"Created:    {created_at}")
    lines.append(f"Full ID:    {full_id}")

    return '\n'.join(lines)


def print_memory_list(
    memories: list[dict],
    show_tags: bool = False,
    show_dates: bool = False,
    show_id: bool = True,
    max_content_length: int = 80
) -> None:
    """
    Print a list of memories with consistent formatting.

    Args:
        memories: List of memory dicts
        show_tags: Include tags in output
        show_dates: Include dates in output (requires '_created_at' field)
        show_id: Include memory ID in output
        max_content_length: Maximum content length before truncation

    Example:
        >>> memories = [
        ...     {'category': 'fact', 'importance': 7, 'content': 'First', 'tags': 'test', 'id': 'abc123'},
        ...     {'category': 'decision', 'importance': 9, 'content': 'Second', 'tags': 'important', 'id': 'def456'}
        ... ]
        >>> print_memory_list(memories, show_tags=True)
        [FACT - 7] First
          Tags: test
          ID: abc123

        [DECISION - 9] Second
          Tags: important
          ID: def456
    """
    for memory in memories:
        if show_dates and '_created_at' in memory:
            # Use date format
            print(format_memory_with_date(memory))
        elif show_tags:
            # Use tags format
            print(format_memory_with_tags(memory, max_content_length))
        else:
            # Simple format with ID
            importance = memory.get('importance', '?')
            category = memory.get('category', 'unknown').upper()
            content = memory.get('content', '')[:max_content_length]

            if len(memory.get('content', '')) > max_content_length:
                content += '...'

            print(f"[{category} - {importance}] {content}")

            if show_id:
                mid = memory.get('id', '')
                print(f"  ID: {mid}")

        # Blank line between memories
        print()
