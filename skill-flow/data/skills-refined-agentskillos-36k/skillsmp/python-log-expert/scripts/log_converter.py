#!/usr/bin/env python3
"""
Log Format Converter

This script converts between different log formats (text to JSON, JSON to text, etc.).
"""

import json
import re
import sys
import argparse
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import gzip


class LogConverter:
    def __init__(self):
        # Common log level patterns
        self.level_patterns = {
            'DEBUG': [r'\bDEBUG\b', r'\bTRACE\b'],
            'INFO': [r'\bINFO\b', r'\bINFORMATION\b'],
            'WARNING': [r'\bWARNING\b', r'\bWARN\b'],
            'ERROR': [r'\bERROR\b', r'\bERR\b', r'\bFATAL\b'],
            'CRITICAL': [r'\bCRITICAL\b', r'\bCRIT\b', r'\bFATAL\b']
        }

        # Timestamp patterns
        self.timestamp_patterns = [
            (r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[\.\d]*Z?)', '%Y-%m-%dT%H:%M:%S'),
            (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[\.\d]*)', '%Y-%m-%d %H:%M:%S'),
            (r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})', '%m/%d/%Y %H:%M:%S'),
            (r'(\w{3} \d{2} \d{2}:\d{2}:\d{2})', '%b %d %H:%M:%S')
        ]

    def extract_timestamp(self, line: str) -> Optional[datetime]:
        """Extract timestamp from a log line."""
        for pattern, fmt in self.timestamp_patterns:
            match = re.search(pattern, line)
            if match:
                timestamp_str = match.group(1)
                try:
                    if 'T' in timestamp_str and timestamp_str.endswith('Z'):
                        # Handle ISO format with Z suffix
                        timestamp_str = timestamp_str.replace('Z', '+00:00')
                        return datetime.fromisoformat(timestamp_str)
                    elif '.' in timestamp_str:
                        return datetime.strptime(timestamp_str, fmt + '.%f')
                    else:
                        return datetime.strptime(timestamp_str, fmt)
                except ValueError:
                    continue
        return None

    def extract_log_level(self, line: str) -> str:
        """Extract log level from a log line."""
        line_upper = line.upper()
        for level, patterns in self.level_patterns.items():
            for pattern in patterns:
                if re.search(pattern, line_upper):
                    return level
        return 'INFO'  # Default level

    def parse_apache_common_log(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse Apache Common Log Format."""
        # Apache Common Log: %h %l %u %t "%r" %>s %b
        pattern = r'^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d+) (\S+)'
        match = re.match(pattern, line)

        if match:
            return {
                'client_ip': match.group(1),
                'ident': match.group(2),
                'user': match.group(3),
                'timestamp': match.group(4),
                'request': match.group(5),
                'status_code': int(match.group(6)),
                'size': match.group(7),
                'event': 'http_request',
                'level': 'INFO' if int(match.group(6)) < 400 else 'ERROR'
            }
        return None

    def parse_syslog(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse syslog format."""
        # Syslog: timestamp hostname process[pid]: message
        pattern = r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+([^:\[]+)(?:\[(\d+)\])?:\s*(.*)'
        match = re.match(pattern, line)

        if match:
            return {
                'timestamp': match.group(1),
                'hostname': match.group(2),
                'process': match.group(3),
                'pid': int(match.group(4)) if match.group(4) else None,
                'message': match.group(5),
                'event': 'syslog_message',
                'level': self.extract_log_level(match.group(5))
            }
        return None

    def text_to_json(self, line: str, format_type: str = 'auto') -> Optional[Dict[str, Any]]:
        """Convert text log line to JSON format."""
        if format_type == 'apache':
            parsed = self.parse_apache_common_log(line)
            if parsed:
                return parsed

        elif format_type == 'syslog':
            parsed = self.parse_syslog(line)
            if parsed:
                return parsed

        # Generic parsing
        timestamp = self.extract_timestamp(line)
        level = self.extract_log_level(line)

        # Extract message (everything after timestamp and level)
        message = line.strip()

        if timestamp:
            timestamp_str = timestamp.isoformat()
            message = message.replace(timestamp.strftime('%Y-%m-%d %H:%M:%S'), '', 1)
            message = message.replace(timestamp.isoformat(), '', 1)

        # Remove level from message
        for level_name, patterns in self.level_patterns.items():
            for pattern in patterns:
                message = re.sub(pattern, '', message, flags=re.IGNORECASE)

        message = message.strip('- ').strip()

        return {
            'timestamp': timestamp.isoformat() if timestamp else datetime.now().isoformat(),
            'level': level,
            'event': message or 'log_message',
            'original_message': line.strip()
        }

    def json_to_text(self, log_entry: Dict[str, Any], format_type: str = 'simple') -> str:
        """Convert JSON log entry to text format."""
        timestamp = log_entry.get('timestamp', datetime.now().isoformat())
        level = log_entry.get('level', 'INFO')
        event = log_entry.get('event', '')

        if format_type == 'simple':
            return f"{timestamp} - {level} - {event}"

        elif format_type == 'detailed':
            parts = [timestamp, level]

            # Add optional fields
            for field in ['service', 'logger', 'user_id', 'request_id']:
                if field in log_entry:
                    parts.append(f"{field}={log_entry[field]}")

            parts.append(event)
            return ' '.join(parts)

        elif format_type == 'colored':
            colors = {
                'DEBUG': '\033[36m',    # Cyan
                'INFO': '\033[32m',     # Green
                'WARNING': '\033[33m',  # Yellow
                'ERROR': '\033[31m',    # Red
                'CRITICAL': '\033[35m', # Magenta
            }

            reset = '\033[0m'
            color = colors.get(level.upper(), '')

            return f"{timestamp} {color}{level}{reset} {event}"

        else:
            return f"{timestamp} [{level}] {event}"

    def convert_file(self, input_file: str, output_file: str,
                    input_format: str = 'auto', output_format: str = 'json',
                    text_format: str = 'simple') -> Dict[str, int]:
        """Convert a log file from one format to another."""
        stats = {
            'total_lines': 0,
            'converted': 0,
            'errors': 0,
            'skipped': 0
        }

        def process_lines(lines):
            for line in lines:
                if not line.strip():
                    continue

                stats['total_lines'] += 1

                try:
                    if output_format == 'json':
                        # Convert to JSON
                        json_entry = self.text_to_json(line, input_format)
                        if json_entry:
                            output_line = json.dumps(json_entry) + '\n'
                            stats['converted'] += 1
                        else:
                            output_line = line  # Keep original if parsing fails
                            stats['skipped'] += 1

                    else:  # output_format == 'text'
                        # Convert from JSON to text
                        try:
                            json_entry = json.loads(line.strip())
                            output_line = self.json_to_text(json_entry, text_format) + '\n'
                            stats['converted'] += 1
                        except json.JSONDecodeError:
                            # Line is already text, format it
                            if input_format == 'json':
                                # Expected JSON but got text
                                stats['errors'] += 1
                                continue
                            else:
                                # Reformat text
                                json_entry = self.text_to_json(line, input_format)
                                output_line = self.json_to_text(json_entry, text_format) + '\n'
                                stats['converted'] += 1

                    output_file.write(output_line)

                except Exception as e:
                    stats['errors'] += 1
                    # Write original line as fallback
                    output_file.write(line)

        # Open files (handle gzip)
        if input_file.endswith('.gz'):
            input_fh = gzip.open(input_file, 'rt', encoding='utf-8')
        else:
            input_fh = open(input_file, 'r', encoding='utf-8')

        if output_file.endswith('.gz'):
            output_fh = gzip.open(output_file, 'wt', encoding='utf-8')
        else:
            output_fh = open(output_file, 'w', encoding='utf-8')

        try:
            with input_fh, output_fh:
                process_lines(input_fh)
        except Exception as e:
            print(f"Error during conversion: {e}", file=sys.stderr)
            stats['errors'] += 1

        return stats


def main():
    parser = argparse.ArgumentParser(description="Convert log formats")
    parser.add_argument("input_file", help="Input log file")
    parser.add_argument("output_file", help="Output log file")
    parser.add_argument("--input-format", choices=['auto', 'json', 'text', 'apache', 'syslog'],
                       default='auto', help="Input format")
    parser.add_argument("--output-format", choices=['json', 'text'],
                       default='json', help="Output format")
    parser.add_argument("--text-format", choices=['simple', 'detailed', 'colored'],
                       default='simple', help="Text output format")
    parser.add_argument("--stats", action="store_true", help="Show conversion statistics")

    args = parser.parse_args()

    converter = LogConverter()

    try:
        stats = converter.convert_file(
            args.input_file,
            args.output_file,
            args.input_format,
            args.output_format,
            args.text_format
        )

        print(f"Converted {args.input_file} to {args.output_file}")

        if args.stats:
            print(f"\nConversion Statistics:")
            print(f"  Total lines: {stats['total_lines']:,}")
            print(f"  Converted: {stats['converted']:,}")
            print(f"  Errors: {stats['errors']:,}")
            print(f"  Skipped: {stats['skipped']:,}")

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()