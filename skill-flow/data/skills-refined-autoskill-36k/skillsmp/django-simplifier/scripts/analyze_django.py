#!/usr/bin/env python3
"""
Comprehensive Django code analyzer - runs all Django checks.
"""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def run_analyzer(script_name: str, path: str) -> dict:
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        return {'issues': [], 'error': f'Script not found: {script_name}'}

    cmd = [sys.executable, str(script_path), path, '--format', 'json']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
        return {'issues': [], 'error': result.stderr[:200] if result.stderr else 'No output'}
    except subprocess.TimeoutExpired:
        return {'issues': [], 'error': 'Analysis timed out'}
    except json.JSONDecodeError as e:
        return {'issues': [], 'error': f'JSON parse error: {e}'}
    except Exception as e:
        return {'issues': [], 'error': str(e)[:200]}


def generate_report(path: str) -> dict:
    results = {}

    print("🔍 Checking Django basic issues...", file=sys.stderr)
    results['django_issues'] = run_analyzer('find_django_issues.py', path)

    print("🔍 Checking Django anti-patterns...", file=sys.stderr)
    results['django_antipatterns'] = run_analyzer('find_django_antipatterns.py', path)

    print("🔍 Checking Django over-engineering...", file=sys.stderr)
    oe_result = run_analyzer('find_django_overengineering.py', path)
    results['django_overengineering'] = oe_result.get('issues', []) if isinstance(oe_result, dict) else oe_result

    report = {
        'meta': {
            'analyzed_path': path,
            'timestamp': datetime.now().isoformat(),
            'analyzers_run': list(results.keys())
        },
        'summary': {
            'total_issues': 0,
            'by_severity': {'high': 0, 'medium': 0, 'low': 0},
            'by_category': {}
        },
        'categories': {}
    }

    for category, data in results.items():
        issues = []
        if isinstance(data, list):
            issues = data
        elif isinstance(data, dict) and 'issues' in data:
            issues = data['issues']

        normalized = []
        for issue in issues:
            if isinstance(issue, dict):
                if 'severity' not in issue:
                    issue['severity'] = 'medium'
                issue['analyzer'] = category
                normalized.append(issue)

        report['categories'][category] = {'issues': normalized, 'count': len(normalized)}
        report['summary']['total_issues'] += len(normalized)
        report['summary']['by_category'][category] = len(normalized)

        for issue in normalized:
            sev = issue.get('severity', 'medium')
            if sev in report['summary']['by_severity']:
                report['summary']['by_severity'][sev] += 1

    return report


def print_text_report(report: dict):
    meta = report['meta']
    summary = report['summary']

    print("\n" + "=" * 70)
    print("🎯 DJANGO CODE ANALYSIS REPORT")
    print("=" * 70)
    print(f"Path: {meta['analyzed_path']}")
    print(f"Time: {meta['timestamp']}")
    print()

    print("📈 SUMMARY")
    print("-" * 40)
    print(f"Total issues found: {summary['total_issues']}")
    print()

    severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
    print("By severity:")
    for sev, count in summary['by_severity'].items():
        if count > 0:
            print(f"  {severity_icons[sev]} {sev.upper()}: {count}")
    print()

    print("By analyzer:")
    for cat, count in sorted(summary['by_category'].items(), key=lambda x: -x[1]):
        if count > 0:
            print(f"  {cat}: {count}")
    print()

    if summary['total_issues'] == 0:
        print("✅ No Django issues found! Your code looks great!")
        return

    # High severity issues
    print("=" * 70)
    print("🔴 HIGH SEVERITY ISSUES")
    print("=" * 70)

    high_issues = []
    for cat, data in report['categories'].items():
        for issue in data['issues']:
            if issue.get('severity') == 'high':
                high_issues.append(issue)

    if not high_issues:
        print("None found!")
    else:
        for issue in high_issues[:15]:
            file_loc = f"{issue.get('file', '?')}:{issue.get('line', '?')}"
            print(f"\n📍 {file_loc}")
            issue_type = issue.get('issue_type', issue.get('pattern_type', '?'))
            print(f"   {issue_type}")
            if 'description' in issue:
                print(f"   {issue['description']}")
            if 'suggestion' in issue:
                print(f"   → {issue['suggestion']}")

        if len(high_issues) > 15:
            print(f"\n... and {len(high_issues) - 15} more high severity issues")

    print()

    # Medium severity summary
    print("=" * 70)
    print("🟡 MEDIUM SEVERITY ISSUES (summary)")
    print("=" * 70)

    medium_by_type = defaultdict(int)
    for cat, data in report['categories'].items():
        for issue in data['issues']:
            if issue.get('severity') == 'medium':
                issue_type = issue.get('issue_type', issue.get('pattern_type', 'other'))
                medium_by_type[issue_type] += 1

    if not medium_by_type:
        print("None found!")
    else:
        for type_name, count in sorted(medium_by_type.items(), key=lambda x: -x[1])[:10]:
            print(f"  {type_name}: {count}")

    print()

    # Recommendations
    print("=" * 70)
    print("💡 RECOMMENDATIONS")
    print("=" * 70)

    recommendations = []

    high_count = summary['by_severity'].get('high', 0)
    if high_count > 0:
        recommendations.append(f"• Fix {high_count} high-severity issues first (N+1 queries, security)")

    # Check for specific patterns
    all_issues = []
    for data in report['categories'].values():
        all_issues.extend(data['issues'])

    issue_types = defaultdict(int)
    for issue in all_issues:
        issue_types[issue.get('issue_type', issue.get('pattern_type', ''))] += 1

    if issue_types.get('save_in_loop', 0) + issue_types.get('create_in_loop', 0) > 0:
        recommendations.append("• Use bulk_create/bulk_update instead of saving in loops")

    if issue_types.get('n_plus_one_risk', 0) + issue_types.get('query_in_loop', 0) > 0:
        recommendations.append("• Add select_related/prefetch_related to prevent N+1 queries")

    if issue_types.get('hardcoded_url', 0) > 0:
        recommendations.append("• Replace hardcoded URLs with reverse() calls")

    if issue_types.get('fat_view', 0) + issue_types.get('fat_view_method', 0) > 0:
        recommendations.append("• Extract business logic from views to models/services")

    if issue_types.get('single_impl_abstract_model', 0) + issue_types.get('unused_abstract_model', 0) > 0:
        recommendations.append("• Simplify model hierarchy - remove premature abstractions")

    if not recommendations:
        recommendations.append("• Your Django code is in good shape!")

    for rec in recommendations:
        print(rec)

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive Django code analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Runs all Django analysis checks:
  - Basic issues (N+1, fat views, hardcoded URLs)
  - Anti-patterns (ORM misuse, security, model issues)
  - Over-engineering (unused abstractions, unnecessary patterns)

Examples:
  %(prog)s .                    # Analyze current directory
  %(prog)s myproject/           # Analyze Django project
  %(prog)s . --format json      # JSON output for CI
        """
    )
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--output', '-o', type=str, help='Output file')

    args = parser.parse_args()
    report = generate_report(args.path)

    if args.format == 'json':
        output = json.dumps(report, indent=2)
    else:
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        print_text_report(report)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    if args.output:
        Path(args.output).write_text(output)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
