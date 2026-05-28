#!/usr/bin/env python3
"""
Performance Profiling Template - Phase-Boundary Instrumentation

Use this template for profiling multi-stage pipelines with time.perf_counter()
at phase boundaries to identify bottlenecks.
"""

import time
import tracemalloc
from typing import Dict


def profile_pipeline_example():
    """
    Example profiling function for multi-stage data pipeline.

    Adapt this template to your pipeline by:
    1. Replace phase names (download, extract, parse, ingest)
    2. Replace function calls with your actual operations
    3. Add/remove phases as needed
    4. Run 3+ times and average results for accuracy
    """
    results: dict[str, float] = {}

    # Optional: Track memory usage
    tracemalloc.start()
    mem_start = tracemalloc.get_traced_memory()[0] / 1024 / 1024  # MB

    print("=" * 80)
    print("PERFORMANCE PROFILING")
    print("=" * 80)

    # Phase 1: Download
    print("\n[Phase 1: Download]")
    start = time.perf_counter()
    # ↓ Replace with your download operation
    data = download_data_from_source()
    # ↑
    duration = time.perf_counter() - start
    results["download"] = duration
    print(f"  Duration: {duration:.3f}s")

    # Phase 2: Extract/Decompress
    print("\n[Phase 2: Extract]")
    start = time.perf_counter()
    # ↓ Replace with your extraction operation
    extracted_data = extract_or_decompress(data)
    # ↑
    duration = time.perf_counter() - start
    results["extract"] = duration
    print(f"  Duration: {duration:.3f}s")

    # Phase 3: Parse/Transform
    print("\n[Phase 3: Parse]")
    start = time.perf_counter()
    # ↓ Replace with your parsing operation
    parsed_data = parse_and_transform(extracted_data)
    # ↑
    duration = time.perf_counter() - start
    results["parse"] = duration
    print(f"  Duration: {duration:.3f}s")

    # Phase 4: Write/Ingest
    print("\n[Phase 4: Ingest]")
    start = time.perf_counter()
    # ↓ Replace with your ingestion operation
    row_count = ingest_to_database(parsed_data)
    # ↑
    duration = time.perf_counter() - start
    results["ingest"] = duration
    print(f"  Duration: {duration:.3f}s")
    print(f"  Rows processed: {row_count:,}")

    # Memory tracking (optional)
    mem_end = tracemalloc.get_traced_memory()[0] / 1024 / 1024  # MB
    mem_peak = tracemalloc.get_traced_memory()[1] / 1024 / 1024  # MB
    tracemalloc.stop()

    # Analysis
    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)

    total_time = sum(results.values())
    print(f"\nTotal Duration: {total_time:.3f}s")
    print(f"Throughput: {row_count / total_time:,.0f} rows/sec")

    print("\nPhase Breakdown:")
    print(f"{'Phase':<20} {'Duration (s)':<15} {'% of Total':<15} {'Bottleneck?'}")
    print("-" * 70)

    # Sort by duration (descending) to identify bottleneck
    sorted_phases = sorted(results.items(), key=lambda x: x[1], reverse=True)

    for phase, duration in sorted_phases:
        pct = (duration / total_time) * 100
        is_bottleneck = "🔴 YES" if pct > 50 else ("🟡 MAYBE" if pct > 20 else "")
        print(f"{phase:<20} {duration:<15.3f} {pct:<15.1f} {is_bottleneck}")

    print("\nMemory Usage:")
    print(f"  Start: {mem_start:.1f} MB")
    print(f"  End: {mem_end:.1f} MB")
    print(f"  Peak: {mem_peak:.1f} MB")
    print(f"  Delta: {mem_end - mem_start:.1f} MB")

    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)

    primary_bottleneck = sorted_phases[0]
    if primary_bottleneck[1] / total_time > 0.5:
        print(f"\n🔴 PRIMARY BOTTLENECK: {primary_bottleneck[0]}")
        print(f"   Accounts for {(primary_bottleneck[1] / total_time * 100):.1f}% of total time")
        print("   Recommendation: Focus optimization efforts here first")
    else:
        print(f"\n🟡 NO SINGLE BOTTLENECK (largest phase: {primary_bottleneck[0]} at {(primary_bottleneck[1] / total_time * 100):.1f}%)")
        print("   Recommendation: Optimize multiple phases or parallelize pipeline")

    return results


# Placeholder functions - replace with your actual operations
def download_data_from_source():
    """Replace with your download logic."""
    time.sleep(0.1)  # Simulate download
    return b"sample_data"


def extract_or_decompress(data):
    """Replace with your extraction logic."""
    time.sleep(0.05)  # Simulate extraction
    return "extracted_data"


def parse_and_transform(data):
    """Replace with your parsing logic."""
    time.sleep(0.05)  # Simulate parsing
    return [{"id": i, "value": i * 2} for i in range(1000)]


def ingest_to_database(data):
    """Replace with your ingestion logic."""
    time.sleep(0.05)  # Simulate ingestion
    return len(data)


if __name__ == "__main__":
    # Run profiling 3 times and average results
    print("Running 3 profiling iterations...")
    all_results = []

    for iteration in range(3):
        print(f"\n\nITERATION {iteration + 1}/3")
        results = profile_pipeline_example()
        all_results.append(results)

    # Average results
    print("\n\n" + "=" * 80)
    print("AVERAGED RESULTS (3 iterations)")
    print("=" * 80)

    avg_results = {}
    for phase in all_results[0].keys():
        avg_results[phase] = sum(r[phase] for r in all_results) / len(all_results)

    total_avg = sum(avg_results.values())
    print(f"\n{'Phase':<20} {'Avg Duration (s)':<15} {'% of Total'}")
    print("-" * 50)
    for phase, duration in sorted(avg_results.items(), key=lambda x: x[1], reverse=True):
        pct = (duration / total_avg) * 100
        print(f"{phase:<20} {duration:<15.3f} {pct:.1f}%")
