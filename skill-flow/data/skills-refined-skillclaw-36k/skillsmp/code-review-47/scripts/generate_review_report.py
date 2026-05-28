#!/usr/bin/env python3
"""
Generate comprehensive review report from analysis results.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def load_json_safely(file_path: Path) -> Dict[str, Any]:
    """Load JSON file, return empty dict if not found or invalid."""
    try:
        if file_path.exists():
            return json.loads(file_path.read_text())
    except Exception:
        pass
    return {}

def generate_report(output_dir: str) -> str:
    """Generate markdown report from all analysis results."""
    output_path = Path(output_dir)

    # Load all reports
    complexity_report = load_json_safely(output_path / 'complexity-report.json')
    smells_report = load_json_safely(output_path / 'code-smells-report.json')

    # Start building report
    report = []
    report.append("# Code Review Report")
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Executive Summary
    report.append("## Executive Summary\n")

    total_issues = smells_report.get('total_issues', 0)
    total_functions = complexity_report.get('statistics', {}).get('total_functions', 0)

    report.append(f"- **Total Functions Analyzed**: {total_functions}")
    report.append(f"- **Code Smells Detected**: {total_issues}")

    if smells_report.get('by_severity'):
        severity = smells_report['by_severity']
        report.append(f"  - High Severity: {severity.get('high', 0)}")
        report.append(f"  - Medium Severity: {severity.get('medium', 0)}")
        report.append(f"  - Low Severity: {severity.get('low', 0)}")

    report.append("")

    # Complexity Analysis
    if complexity_report.get('statistics'):
        report.append("## Complexity Analysis\n")
        stats = complexity_report['statistics']

        report.append(f"- **Average Complexity**: {stats.get('avg_complexity', 0):.1f}")
        report.append(f"- **Maximum Complexity**: {stats.get('max_complexity', 0)}")
        report.append(f"- **Average Function Length**: {stats.get('avg_function_length', 0):.1f} lines")
        report.append(f"- **Maximum Function Length**: {stats.get('max_function_length', 0)} lines")
        report.append("")

        # Problematic functions
        problematic = complexity_report.get('problematic_functions', [])
        if problematic:
            report.append("### Functions Needing Attention\n")

            for func in problematic[:10]:  # Top 10
                report.append(f"#### `{func['name']}` in `{func['file']}`\n")
                report.append(f"- Lines: {func['lines']}")
                report.append(f"- Complexity: {func['complexity']}")
                report.append(f"- Nesting Depth: {func['nesting_depth']}")

                if func.get('issues'):
                    report.append(f"- Issues: {', '.join(func['issues'])}")

                report.append("")

    # Code Smells
    if smells_report.get('issues'):
        report.append("## Code Smells\n")

        # Group by type
        by_type = {}
        for issue in smells_report['issues']:
            issue_type = issue.get('type', 'unknown')
            if issue_type not in by_type:
                by_type[issue_type] = []
            by_type[issue_type].append(issue)

        for smell_type, issues in by_type.items():
            report.append(f"### {smell_type.replace('_', ' ').title()}\n")
            report.append(f"Found {len(issues)} occurrences\n")

            for issue in issues[:5]:  # Show first 5 of each type
                report.append(f"**{issue.get('file', 'unknown')}**")

                if issue.get('function'):
                    report.append(f"- Function: `{issue['function']}`")
                if issue.get('class'):
                    report.append(f"- Class: `{issue['class']}`")
                if issue.get('line'):
                    report.append(f"- Line: {issue['line']}")

                report.append(f"- {issue.get('message', '')}")

                if issue.get('suggestion'):
                    report.append(f"- **Suggestion**: {issue['suggestion']}")

                report.append("")

    # Linter Reports Summary
    report.append("## Linter Results\n")

    # ESLint
    eslint_file = output_path / 'eslint-report.json'
    if eslint_file.exists():
        try:
            eslint_data = json.loads(eslint_file.read_text())
            total_errors = sum(f.get('errorCount', 0) for f in eslint_data)
            total_warnings = sum(f.get('warningCount', 0) for f in eslint_data)

            report.append(f"### ESLint\n")
            report.append(f"- Errors: {total_errors}")
            report.append(f"- Warnings: {total_warnings}")
            report.append("")
        except Exception:
            pass

    # TypeScript
    tsc_file = output_path / 'tsc-errors.txt'
    if tsc_file.exists() and tsc_file.stat().st_size > 0:
        content = tsc_file.read_text()
        error_count = content.count('error TS')

        report.append(f"### TypeScript Compiler\n")
        report.append(f"- Errors: {error_count}")
        report.append("")

    # Recommendations
    report.append("## Recommendations\n")

    recommendations = []

    if complexity_report.get('problematic_functions'):
        count = len(complexity_report['problematic_functions'])
        recommendations.append(
            f"- Refactor {count} complex functions to improve maintainability"
        )

    if smells_report.get('by_severity', {}).get('high', 0) > 0:
        recommendations.append(
            f"- Address {smells_report['by_severity']['high']} high-severity code smells"
        )

    if stats.get('avg_complexity', 0) > 5:
        recommendations.append(
            "- Overall code complexity is above recommended levels (avg > 5)"
        )

    if not recommendations:
        recommendations.append("- Code quality looks good! Keep up the good work.")

    report.extend(recommendations)
    report.append("")

    # Next Steps
    report.append("## Next Steps\n")
    report.append("1. Review high-severity issues first")
    report.append("2. Refactor complex functions")
    report.append("3. Address code smells")
    report.append("4. Run tests after refactoring")
    report.append("5. Re-run code review to verify improvements")
    report.append("")

    return '\n'.join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: generate_review_report.py <output-directory>")
        sys.exit(1)

    output_dir = sys.argv[1]

    if not os.path.isdir(output_dir):
        print(f"Error: {output_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    report = generate_report(output_dir)
    print(report)

if __name__ == '__main__':
    main()
