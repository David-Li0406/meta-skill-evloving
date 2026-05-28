#!/usr/bin/env python3
"""
Comprehensive Python code analyzer - runs all checks and produces unified report.
"""

import argparse
import json
import subprocess
import sys
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


def generate_report(path: str, skip_duplicates: bool = False) -> dict:
    results = {}

    print("🔍 Analyzing complexity...", file=sys.stderr)
    results['complexity'] = run_analyzer('analyze_complexity.py', path)

    print("🔍 Finding code smells...", file=sys.stderr)
    results['code_smells'] = run_analyzer('find_code_smells.py', path)

    print("🔍 Detecting over-engineering...", file=sys.stderr)
    oe_result = run_analyzer('find_overengineering.py', path)
    results['overengineering'] = oe_result.get('issues', []) if isinstance(oe_result, dict) else oe_result

    print("🔍 Finding dead code...", file=sys.stderr)
    results['dead_code'] = run_analyzer('find_dead_code.py', path)

    print("🔍 Detecting unpythonic patterns...", file=sys.stderr)
    results['unpythonic'] = run_analyzer('find_unpythonic.py', path)

    print("🔍 Analyzing coupling/cohesion...", file=sys.stderr)
    results['coupling'] = run_analyzer('find_coupling_issues.py', path)

    if not skip_duplicates:
        print("🔍 Finding duplicates...", file=sys.stderr)
        results['duplicates'] = run_analyzer('find_duplicates.py', path)

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
        elif isinstance(data, dict):
            if 'issues' in data:
                issues = data['issues']

        normalized = []
        for issue in issues:
            if isinstance(issue, dict):
                if 'severity' not in issue:
                    if 'confidence' in issue:
                        conf = issue['confidence']
                        issue['severity'] = 'high' if conf >= 90 else ('medium' if conf >= 70 else 'low')
                    else:
                        issue['severity'] = 'medium'
                issue['category'] = category
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
    print("📊 PYTHON CODE ANALYSIS REPORT")
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

    print("By category:")
    for cat, count in sorted(summary['by_category'].items(), key=lambda x: -x[1]):
        if count > 0:
            print(f"  {cat}: {count}")
    print()

    if summary['total_issues'] == 0:
        print("✅ No issues found! Your code looks great!")
        return

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
        for issue in high_issues[:20]:
            file_loc = f"{issue.get('file', '?')}:{issue.get('line', '?')}"
            print(f"\n📍 {file_loc}")
            print(f"   [{issue['category']}] {issue.get('issue_type', issue.get('smell_type', issue.get('pattern_type', '?')))}")
            if 'description' in issue:
                print(f"   {issue['description']}")
            if 'suggestion' in issue:
                print(f"   → {issue['suggestion']}")

        if len(high_issues) > 20:
            print(f"\n... and {len(high_issues) - 20} more high severity issues")

    print()
    print("=" * 70)
    print("💡 RECOMMENDATIONS")
    print("=" * 70)

    recommendations = []
    if summary['by_category'].get('complexity', 0) > 5:
        recommendations.append("• Reduce function complexity - extract methods, use early returns")
    if summary['by_category'].get('code_smells', 0) > 5:
        recommendations.append("• Address code smells - fix mutable defaults, bare excepts")
    if summary['by_category'].get('overengineering', 0) > 0:
        recommendations.append("• Simplify architecture - remove unused abstractions (YAGNI)")
    if summary['by_category'].get('dead_code', 0) > 5:
        recommendations.append("• Clean up dead code - remove unused imports and functions")
    if summary['by_category'].get('duplicates', 0) > 0:
        recommendations.append("• Extract duplicate code into shared functions")
    if summary['by_category'].get('coupling', 0) > 3:
        recommendations.append("• Improve class design - increase cohesion, reduce coupling")

    if not recommendations:
        recommendations.append("• Your code is in good shape! Consider minor improvements.")

    for rec in recommendations:
        print(rec)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive Python code analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Runs all analysis checks:
  - Complexity (cyclomatic, cognitive, nesting)
  - Code smells (mutable defaults, bare excepts, etc.)
  - Over-engineering (unused abstractions, YAGNI)
  - Dead code (unused imports, functions)
  - Unpythonic patterns (range(len), == True)
  - Coupling/cohesion (feature envy, message chains)
  - Duplicate code (AST-based similarity)

Examples:
  %(prog)s .                    # Analyze current directory
  %(prog)s myproject/           # Analyze specific project
  %(prog)s . --format json      # JSON output for CI
        """
    )
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--skip-duplicates', action='store_true')
    parser.add_argument('--output', '-o', type=str, help='Output file')

    args = parser.parse_args()
    report = generate_report(args.path, skip_duplicates=args.skip_duplicates)

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
