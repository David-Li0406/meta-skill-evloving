#!/usr/bin/env python3
"""
Log Analysis Utilities

This script provides utilities for analyzing and processing log files.
"""

import json
import re
import sys
import argparse
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Any, Optional
import gzip


class LogAnalyzer:
    def __init__(self):
        self.error_patterns = [
            r'error',
            r'exception',
            r'failed',
            r'timeout',
            r'connection.*refused',
            r'file.*not.*found'
        ]

    def parse_json_log_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a JSON log line and return dictionary."""
        try:
            return json.loads(line.strip())
        except json.JSONDecodeError:
            return None

    def parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """Parse various timestamp formats."""
        timestamp_formats = [
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
        ]

        for fmt in timestamp_formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        return None

    def is_error_message(self, message: str) -> bool:
        """Check if a message contains error indicators."""
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in self.error_patterns)

    def analyze_log_file(self, file_path: str, is_json: bool = True) -> Dict[str, Any]:
        """Analyze a log file and return statistics."""
        stats = {
            'total_lines': 0,
            'valid_entries': 0,
            'error_count': 0,
            'log_levels': Counter(),
            'time_range': {'start': None, 'end': None},
            'top_errors': Counter(),
            'hourly_distribution': defaultdict(int),
            'services': Counter()
        }

        def process_lines(lines):
            for line in lines:
                if not line.strip():
                    continue

                stats['total_lines'] += 1

                if is_json:
                    entry = self.parse_json_log_line(line)
                    if not entry:
                        continue

                    stats['valid_entries'] += 1

                    # Extract log level
                    level = entry.get('level', 'unknown')
                    stats['log_levels'][level.upper()] += 1

                    # Check for errors
                    if level.upper() in ['ERROR', 'CRITICAL'] or self.is_error_message(entry.get('event', '')):
                        stats['error_count'] += 1
                        stats['top_errors'][entry.get('event', 'unknown error')] += 1

                    # Extract timestamp
                    timestamp_str = entry.get('timestamp')
                    if timestamp_str:
                        timestamp = self.parse_timestamp(timestamp_str)
                        if timestamp:
                            if stats['time_range']['start'] is None or timestamp < stats['time_range']['start']:
                                stats['time_range']['start'] = timestamp
                            if stats['time_range']['end'] is None or timestamp > stats['time_range']['end']:
                                stats['time_range']['end'] = timestamp

                            # Hourly distribution
                            stats['hourly_distribution'][timestamp.hour] += 1

                    # Extract service name
                    service = entry.get('service', entry.get('logger', 'unknown'))
                    stats['services'][service] += 1

        # Open file (handle gzip)
        if file_path.endswith('.gz'):
            with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                process_lines(f)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                process_lines(f)

        return stats

    def generate_report(self, stats: Dict[str, Any]) -> str:
        """Generate a human-readable report from statistics."""
        report = []
        report.append("=== LOG ANALYSIS REPORT ===\n")

        # Basic stats
        report.append(f"Total lines processed: {stats['total_lines']:,}")
        report.append(f"Valid entries: {stats['valid_entries']:,}")
        report.append(f"Error count: {stats['error_count']:,}")

        if stats['valid_entries'] > 0:
            error_rate = (stats['error_count'] / stats['valid_entries']) * 100
            report.append(f"Error rate: {error_rate:.2f}%")

        report.append("")

        # Log levels
        if stats['log_levels']:
            report.append("LOG LEVELS:")
            for level, count in stats['log_levels'].most_common():
                percentage = (count / stats['valid_entries']) * 100 if stats['valid_entries'] > 0 else 0
                report.append(f"  {level}: {count:,} ({percentage:.1f}%)")
            report.append("")

        # Time range
        if stats['time_range']['start'] and stats['time_range']['end']:
            start_time = stats['time_range']['start'].strftime('%Y-%m-%d %H:%M:%S')
            end_time = stats['time_range']['end'].strftime('%Y-%m-%d %H:%M:%S')
            duration = stats['time_range']['end'] - stats['time_range']['start']
            report.append(f"Time range: {start_time} to {end_time}")
            report.append(f"Duration: {duration}")
            report.append("")

        # Top errors
        if stats['top_errors']:
            report.append("TOP ERRORS:")
            for error, count in stats['top_errors'].most_common(10):
                report.append(f"  {count:,}: {error}")
            report.append("")

        # Services
        if stats['services']:
            report.append("SERVICES:")
            for service, count in stats['services'].most_common():
                percentage = (count / stats['valid_entries']) * 100 if stats['valid_entries'] > 0 else 0
                report.append(f"  {service}: {count:,} ({percentage:.1f}%)")
            report.append("")

        # Hourly distribution
        if stats['hourly_distribution']:
            report.append("HOURLY DISTRIBUTION:")
            for hour in sorted(stats['hourly_distribution'].keys()):
                count = stats['hourly_distribution'][hour]
                report.append(f"  {hour:02d}:00: {count:,}")

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Analyze log files")
    parser.add_argument("log_file", help="Path to log file")
    parser.add_argument("--format", choices=["json", "text"], default="json",
                       help="Log format (default: json)")
    parser.add_argument("--output", help="Output file for report")

    args = parser.parse_args()

    analyzer = LogAnalyzer()

    try:
        print(f"Analyzing {args.log_file}...")
        stats = analyzer.analyze_log_file(args.log_file, is_json=(args.format == "json"))
        report = analyzer.generate_report(stats)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)

    except FileNotFoundError:
        print(f"Error: File {args.log_file} not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()