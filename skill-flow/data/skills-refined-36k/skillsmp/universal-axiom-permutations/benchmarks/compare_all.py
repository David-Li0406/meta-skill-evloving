#!/usr/bin/env python3
"""
Cross-language benchmark comparison script
Runs benchmarks for all available languages and generates a comparison report
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def check_language_available(lang):
    """Check if a language implementation is available"""
    if lang == 'python':
        return True  # Always available
    elif lang == 'javascript':
        return (Path(__file__).parent.parent / 'dist' / 'javascript' / 'universal-axiom.js').exists()
    elif lang == 'rust':
        return (Path(__file__).parent.parent / 'src' / 'rust' / 'Cargo.toml').exists()
    elif lang == 'julia':
        try:
            subprocess.run(['julia', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    return False


def run_python_benchmarks():
    """Run Python benchmarks"""
    print("Running Python benchmarks...")
    script = Path(__file__).parent / 'benchmark_python.py'
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Python benchmarks completed")
        return True
    else:
        print(f"✗ Python benchmarks failed: {result.stderr}")
        return False


def run_javascript_benchmarks():
    """Run JavaScript benchmarks"""
    print("Running JavaScript benchmarks...")
    script = Path(__file__).parent / 'benchmark-javascript.js'
    result = subprocess.run(['node', str(script)], capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ JavaScript benchmarks completed")
        return True
    else:
        print(f"✗ JavaScript benchmarks failed: {result.stderr}")
        return False


def run_rust_benchmarks():
    """Run Rust benchmarks"""
    print("Running Rust benchmarks (this may take a while)...")
    rust_dir = Path(__file__).parent.parent / 'src' / 'rust'
    result = subprocess.run(['cargo', 'bench'], cwd=rust_dir, capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Rust benchmarks completed")
        return True
    else:
        print(f"✗ Rust benchmarks failed: {result.stderr}")
        return False


def load_results(lang):
    """Load benchmark results from JSON file"""
    results_file = Path(__file__).parent / f'results_{lang}.json'
    if results_file.exists():
        with open(results_file, 'r') as f:
            return json.load(f)
    return None


def generate_comparison_table(results_data):
    """Generate markdown comparison table"""
    benchmarks = set()
    for data in results_data.values():
        if data and 'benchmarks' in data:
            benchmarks.update(data['benchmarks'].keys())

    benchmarks = sorted(benchmarks)
    languages = sorted(results_data.keys())

    # Generate markdown table
    table = []
    table.append(f"# Benchmark Results Comparison\n")
    table.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    table.append(f"\n## Performance Comparison\n")

    # Header
    header = "| Benchmark |" + "".join(f" {lang.capitalize()} |" for lang in languages)
    table.append(header)
    separator = "|" + "-" * (len("Benchmark") + 2) + "|" + "".join("-" * (len(lang) + 3) + "|" for lang in languages)
    table.append(separator)

    # Data rows
    for benchmark in benchmarks:
        row = f"| {benchmark} |"
        for lang in languages:
            if lang in results_data and results_data[lang]:
                bench_data = results_data[lang].get('benchmarks', {}).get(benchmark)
                if bench_data:
                    mean = bench_data['mean_seconds']
                    formatted = format_time(mean)
                    row += f" {formatted} |"
                else:
                    row += " N/A |"
            else:
                row += " N/A |"
        table.append(row)

    table.append("\n## Operations Per Second\n")

    # Header
    table.append(header)
    table.append(separator)

    # Ops/sec rows
    for benchmark in benchmarks:
        row = f"| {benchmark} |"
        for lang in languages:
            if lang in results_data and results_data[lang]:
                bench_data = results_data[lang].get('benchmarks', {}).get(benchmark)
                if bench_data:
                    ops = bench_data['ops_per_second']
                    row += f" {ops:.2f} |"
                else:
                    row += " N/A |"
            else:
                row += " N/A |"
        table.append(row)

    return "\n".join(table)


def format_time(seconds):
    """Format time in appropriate units"""
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    else:
        return f"{seconds:.2f} s"


def main():
    print("=" * 60)
    print("Universal Axiom - Cross-Language Benchmark Comparison")
    print("=" * 60)

    # Check available languages
    available = {}
    for lang in ['python', 'javascript', 'rust', 'julia']:
        available[lang] = check_language_available(lang)
        status = "✓" if available[lang] else "✗"
        print(f"{status} {lang.capitalize()}: {'Available' if available[lang] else 'Not available'}")

    print("\n" + "=" * 60)

    # Run benchmarks for available languages
    results = {}

    if available['python']:
        if run_python_benchmarks():
            results['python'] = load_results('python')

    if available['javascript']:
        if run_javascript_benchmarks():
            results['javascript'] = load_results('javascript')

    # Rust benchmarks can be slow, so they're optional
    # if available['rust']:
    #     if run_rust_benchmarks():
    #         results['rust'] = load_results('rust')

    # Generate comparison report
    if results:
        print("\n" + "=" * 60)
        print("Generating comparison report...")
        comparison = generate_comparison_table(results)

        output_file = Path(__file__).parent / 'RESULTS.md'
        with open(output_file, 'w') as f:
            f.write(comparison)

        print(f"✓ Report saved to: {output_file}")
        print("\n" + comparison)
    else:
        print("\n✗ No benchmark results available")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
