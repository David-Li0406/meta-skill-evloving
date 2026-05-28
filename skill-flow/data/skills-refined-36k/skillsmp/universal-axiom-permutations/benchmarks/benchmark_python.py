#!/usr/bin/env python3
"""
Performance benchmarks for Python implementation of The Universal Axiom
"""

import sys
import time
import statistics
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'python'))

from universal_axiom import UniversalAxiom, AxiomSimulator


def benchmark(func, iterations=1000, warmup=100):
    """Run a benchmark function multiple times and collect statistics"""
    # Warmup
    for _ in range(warmup):
        func()

    # Actual benchmark
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)

    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
        'iterations': iterations
    }


def benchmark_basic_computation_n1():
    """Benchmark basic computation at n=1"""
    axiom = UniversalAxiom(n=1)
    axiom.compute_intelligence()


def benchmark_basic_computation_n10():
    """Benchmark basic computation at n=10"""
    axiom = UniversalAxiom(n=10)
    axiom.compute_intelligence()


def benchmark_basic_computation_n20():
    """Benchmark basic computation at n=20"""
    axiom = UniversalAxiom(n=20)
    axiom.compute_intelligence()


def benchmark_evolution_10_steps():
    """Benchmark evolution over 10 steps"""
    axiom = UniversalAxiom(n=1)
    for _ in range(10):
        axiom.evolve()


def benchmark_evolution_100_steps():
    """Benchmark evolution over 100 steps"""
    axiom = UniversalAxiom(n=1)
    for _ in range(100):
        axiom.evolve()


def benchmark_fibonacci_generation_n12():
    """Benchmark Fibonacci sequence generation"""
    from universal_axiom import fibonacci_sequence
    fibonacci_sequence(12)


def benchmark_fibonacci_generation_n50():
    """Benchmark Fibonacci sequence generation for larger n"""
    from universal_axiom import fibonacci_sequence
    fibonacci_sequence(50)


def benchmark_state_access():
    """Benchmark state access and inspection"""
    axiom = UniversalAxiom(n=10)
    axiom.get_state()


def benchmark_contradiction_resolution():
    """Benchmark contradiction resolution"""
    axiom = UniversalAxiom(n=5, subjectivity=0.8)
    simulator = AxiomSimulator(axiom)
    simulator.simulate_contradiction_resolution(initial_pressure=1.5, resolution_steps=5)


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


def print_results(name, results):
    """Print benchmark results in a formatted way"""
    print(f"\n{name}")
    print(f"  Mean:       {format_time(results['mean'])}")
    print(f"  Median:     {format_time(results['median'])}")
    print(f"  Std Dev:    {format_time(results['stdev'])}")
    print(f"  Min:        {format_time(results['min'])}")
    print(f"  Max:        {format_time(results['max'])}")
    print(f"  Ops/sec:    {1/results['mean']:.2f}")
    print(f"  Iterations: {results['iterations']}")


def main():
    print("=" * 60)
    print("Python Universal Axiom Performance Benchmarks")
    print("=" * 60)

    benchmarks = [
        ("Basic Computation (n=1)", benchmark_basic_computation_n1, 1000),
        ("Basic Computation (n=10)", benchmark_basic_computation_n10, 1000),
        ("Basic Computation (n=20)", benchmark_basic_computation_n20, 1000),
        ("Evolution (10 steps)", benchmark_evolution_10_steps, 100),
        ("Evolution (100 steps)", benchmark_evolution_100_steps, 10),
        ("Fibonacci Generation (n=12)", benchmark_fibonacci_generation_n12, 1000),
        ("Fibonacci Generation (n=50)", benchmark_fibonacci_generation_n50, 1000),
        ("State Access", benchmark_state_access, 1000),
        ("Contradiction Resolution", benchmark_contradiction_resolution, 100),
    ]

    results_summary = {}

    for name, func, iterations in benchmarks:
        print(f"\nRunning: {name}...", end='', flush=True)
        results = benchmark(func, iterations=iterations, warmup=min(100, iterations//10))
        print(" Done")
        print_results(name, results)
        results_summary[name] = results

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"\n{'Benchmark':<40} {'Mean Time':<15} {'Ops/sec':<10}")
    print("-" * 60)

    for name, results in results_summary.items():
        print(f"{name:<40} {format_time(results['mean']):<15} {1/results['mean']:<10.2f}")

    print("\n" + "=" * 60)

    # Export results for comparison
    export_results(results_summary)


def export_results(results):
    """Export results to a JSON file for cross-language comparison"""
    import json

    export_data = {
        'language': 'python',
        'timestamp': time.time(),
        'benchmarks': {}
    }

    for name, data in results.items():
        export_data['benchmarks'][name] = {
            'mean_seconds': data['mean'],
            'median_seconds': data['median'],
            'stdev_seconds': data['stdev'],
            'ops_per_second': 1/data['mean']
        }

    output_file = Path(__file__).parent / 'results_python.json'
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"\nResults exported to: {output_file}")


if __name__ == '__main__':
    main()
