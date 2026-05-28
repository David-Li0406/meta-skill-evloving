"""
Markdown parsing and manipulation utilities for spec files.
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class SpecParser:
    """Parse and manipulate markdown spec files preserving formatting."""

    @staticmethod
    def parse_table(content: str, section_header: str) -> List[Dict[str, str]]:
        """
        Parse markdown table from a section.

        Args:
            content: Full file content
            section_header: Header text to find table under (e.g., "## Edge Cases")

        Returns:
            List of dicts, one per table row (excluding header)

        Example:
            | ID | Name | Value |
            |----|------|-------|
            | 1  | Foo  | Bar   |
            | 2  | Baz  | Qux   |

            Returns: [
                {'ID': '1', 'Name': 'Foo', 'Value': 'Bar'},
                {'ID': '2', 'Name': 'Baz', 'Value': 'Qux'}
            ]
        """
        # Find section
        section_pattern = re.compile(
            rf'^{re.escape(section_header)}\s*$',
            re.MULTILINE
        )
        match = section_pattern.search(content)
        if not match:
            return []

        # Get content after section header
        section_start = match.end()
        next_section = re.search(r'\n#{1,6}\s', content[section_start:])
        section_end = section_start + next_section.start() if next_section else len(content)
        section_content = content[section_start:section_end]

        # Find table
        table_lines = []
        in_table = False
        for line in section_content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('|') and stripped.endswith('|'):
                in_table = True
                table_lines.append(stripped)
            elif in_table and not stripped.startswith('|'):
                break

        if len(table_lines) < 2:
            return []

        # Parse header
        header_line = table_lines[0]
        headers = [h.strip() for h in header_line.split('|')[1:-1]]

        # Skip separator line (|----|-----|)
        # Parse data rows
        rows = []
        for line in table_lines[2:]:
            if not line.strip():
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if len(cells) == len(headers):
                row_dict = dict(zip(headers, cells))
                rows.append(row_dict)

        return rows

    @staticmethod
    def update_table_row(content: str, section_header: str, id_column: str,
                        id_value: str, data: Dict[str, str]) -> str:
        """
        Update a specific row in a table, identified by ID column value.

        Args:
            content: Full file content
            section_header: Header text to find table under
            id_column: Name of ID column (e.g., "ID", "#")
            id_value: Value to match in ID column
            data: Dict of column_name -> new_value

        Returns:
            Updated content

        Raises:
            ValueError: If row not found
        """
        lines = content.split('\n')
        in_section = False
        in_table = False
        updated = False
        result_lines = []

        for line in lines:
            # Check if we're entering the section
            if line.strip() == section_header:
                in_section = True
                result_lines.append(line)
                continue

            # Check if we're leaving the section
            if in_section and re.match(r'^#{1,6}\s', line):
                in_section = False
                in_table = False

            # Process table lines in section
            if in_section and line.strip().startswith('|') and line.strip().endswith('|'):
                if not in_table:
                    # Header line
                    in_table = True
                    result_lines.append(line)
                    continue

                # Parse row
                cells = [c.strip() for c in line.split('|')[1:-1]]

                # Check if this is the target row
                # First, get headers from previous lines to find ID column index
                header_line = result_lines[-2]  # Header is 2 lines back (header, separator, data)
                headers = [h.strip() for h in header_line.split('|')[1:-1]]

                if id_column in headers:
                    id_index = headers.index(id_column)
                    if id_index < len(cells) and cells[id_index] == id_value:
                        # Update this row
                        for col, val in data.items():
                            if col in headers:
                                col_index = headers.index(col)
                                cells[col_index] = val
                        result_lines.append('| ' + ' | '.join(cells) + ' |')
                        updated = True
                        continue

            result_lines.append(line)

        if not updated:
            raise ValueError(f"Row with {id_column}={id_value} not found in {section_header}")

        return '\n'.join(result_lines)

    @staticmethod
    def append_table_row(content: str, section_header: str, data: Dict[str, str]) -> str:
        """
        Append a row to a table.

        Args:
            content: Full file content
            section_header: Header text to find table under
            data: Dict of column_name -> value

        Returns:
            Updated content

        Raises:
            ValueError: If table not found
        """
        lines = content.split('\n')
        in_section = False
        table_end_index = None
        header_line_index = None

        for i, line in enumerate(lines):
            # Check if we're entering the section
            if line.strip() == section_header:
                in_section = True
                continue

            # Check if we're leaving the section
            if in_section and re.match(r'^#{1,6}\s', line):
                break

            # Find table header
            if in_section and line.strip().startswith('|') and line.strip().endswith('|'):
                if header_line_index is None:
                    header_line_index = i
                table_end_index = i

        if header_line_index is None:
            raise ValueError(f"Table not found in section: {section_header}")

        # Get headers
        header_line = lines[header_line_index]
        headers = [h.strip() for h in header_line.split('|')[1:-1]]

        # Build new row
        cells = [data.get(h, '') for h in headers]
        new_row = '| ' + ' | '.join(cells) + ' |'

        # Insert after last table row
        lines.insert(table_end_index + 1, new_row)

        return '\n'.join(lines)

    @staticmethod
    def extract_section(content: str, section_header: str) -> str:
        """
        Extract content of a section.

        Args:
            content: Full file content
            section_header: Header text (e.g., "## Problem Statement")

        Returns:
            Section content (excluding header)
        """
        section_pattern = re.compile(
            rf'^{re.escape(section_header)}\s*$',
            re.MULTILINE
        )
        match = section_pattern.search(content)
        if not match:
            return ""

        section_start = match.end()
        next_section = re.search(r'\n#{1,6}\s', content[section_start:])
        section_end = section_start + next_section.start() if next_section else len(content)

        return content[section_start:section_end].strip()

    @staticmethod
    def replace_section(content: str, section_header: str, new_content: str) -> str:
        """
        Replace content of a section.

        Args:
            content: Full file content
            section_header: Header text
            new_content: New section content (excluding header)

        Returns:
            Updated content
        """
        section_pattern = re.compile(
            rf'^{re.escape(section_header)}\s*$',
            re.MULTILINE
        )
        match = section_pattern.search(content)
        if not match:
            # Section doesn't exist, append it
            return content + f"\n\n{section_header}\n\n{new_content}"

        section_start = match.end()
        next_section = re.search(r'\n#{1,6}\s', content[section_start:])
        section_end = section_start + next_section.start() if next_section else len(content)

        # Replace section content
        before = content[:section_start]
        after = content[section_end:]

        return before + '\n\n' + new_content + '\n' + after

    @staticmethod
    def find_story_section(content: str, story_num: int) -> Tuple[int, int]:
        """
        Find start and end positions of a story section.

        Args:
            content: Full file content
            story_num: Story number to find

        Returns:
            Tuple of (start_pos, end_pos) or (-1, -1) if not found
        """
        # Pattern: ### User Story N - ...
        pattern = re.compile(
            rf'^### (?:🔄 )?User Story {story_num}\s',
            re.MULTILINE
        )
        match = pattern.search(content)
        if not match:
            return (-1, -1)

        start_pos = match.start()

        # Find next story or section
        next_match = re.search(
            r'\n### (?:🔄 )?User Story \d+|^\n## ',
            content[match.end():],
            re.MULTILINE
        )
        end_pos = match.end() + next_match.start() if next_match else len(content)

        return (start_pos, end_pos)

    @staticmethod
    def extract_collapsible_section(content: str, summary: str) -> str:
        """
        Extract content from a <details><summary> section.

        Args:
            content: Content containing collapsible section
            summary: Summary text to find

        Returns:
            Content inside <details> tags or empty string if not found
        """
        pattern = re.compile(
            rf'<details>\s*<summary>{re.escape(summary)}</summary>(.*?)</details>',
            re.DOTALL
        )
        match = pattern.search(content)
        return match.group(1).strip() if match else ""
