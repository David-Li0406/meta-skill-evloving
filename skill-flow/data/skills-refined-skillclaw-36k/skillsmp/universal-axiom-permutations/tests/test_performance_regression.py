"""
Performance regression tests for The Universal Axiom.

These tests track performance metrics over time to detect regressions.
Baseline performance metrics are stored and compared against current runs.
"""

import json
import time
from pathlib import Path
from typing import Dict, List

import pytest
from python.benchmarking import (
    AxiomBenchmarkAggregator,
    AxiomBenchmarkMode,
    AxiomBenchmarkRunner,
    AxiomBenchmarkScenario,
    AxiomSignals,
    BenchmarkRunConfig,
)
from python.universal_axiom import AxiomSimulator, UniversalAxiom


# Performance baseline thresholds (in milliseconds)
PERFORMANCE_THRESHOLDS = {
    "axiom_compute_intelligence": 1.0,  # Should complete in < 1ms
    "axiom_evolution_10_steps": 10.0,  # 10 evolution steps < 10ms
    "simulator_evolution_100_steps": 100.0,  # 100 simulation steps < 100ms
    "benchmark_runner_10_scenarios": 1000.0,  # 10 scenarios < 1s
}


class SimpleAdapter:
    """Simple adapter for performance testing"""

    model_id = "perf-test-model"

    def generate(self, prompt: str, mode: AxiomBenchmarkMode) -> str:
        return f"Response for: {prompt}"


class SimpleExtractor:
    """Simple extractor for performance testing"""

    def extract(self, prompt: str, response: str) -> AxiomSignals:
        return AxiomSignals(
            impulses=1.0,
            elements=1.0,
            pressure=1.0,
            subjectivity=0.5,
            purpose=1.0,
            time=1.0,
            n=1,
        )


def measure_execution_time(func, *args, **kwargs):
    """Measure execution time of a function in milliseconds"""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    elapsed_ms = (end - start) * 1000
    return result, elapsed_ms


class TestPerformanceRegression:
    """Performance regression test suite"""

    def test_axiom_compute_intelligence_performance(self):
        """Test that computing intelligence is fast enough"""
        axiom = UniversalAxiom(
            impulses=2.0,
            elements=1.5,
            pressure=1.2,
            subjectivity=0.3,
            purpose=1.0,
            time=1.0,
            n=5,
        )

        _, elapsed = measure_execution_time(axiom.compute_intelligence)

        threshold = PERFORMANCE_THRESHOLDS["axiom_compute_intelligence"]
        assert (
            elapsed < threshold
        ), f"Intelligence computation took {elapsed:.2f}ms (threshold: {threshold}ms)"

    def test_axiom_evolution_performance(self):
        """Test that evolving the axiom is performant"""
        axiom = UniversalAxiom()

        def evolve_10_times():
            for _ in range(10):
                axiom.evolve()

        _, elapsed = measure_execution_time(evolve_10_times)

        threshold = PERFORMANCE_THRESHOLDS["axiom_evolution_10_steps"]
        assert elapsed < threshold, f"10 evolutions took {elapsed:.2f}ms (threshold: {threshold}ms)"

    def test_simulator_evolution_performance(self):
        """Test that simulation is performant"""
        axiom = UniversalAxiom(
            impulses=1.5, elements=1.2, pressure=1.1, subjectivity=0.4, purpose=1.0, time=1.0
        )
        simulator = AxiomSimulator(axiom)

        _, elapsed = measure_execution_time(simulator.simulate_evolution, steps=100)

        threshold = PERFORMANCE_THRESHOLDS["simulator_evolution_100_steps"]
        assert (
            elapsed < threshold
        ), f"100 simulation steps took {elapsed:.2f}ms (threshold: {threshold}ms)"

    def test_benchmark_runner_performance(self):
        """Test that benchmarking scenarios run efficiently"""
        runner = AxiomBenchmarkRunner(adapter=SimpleAdapter(), extractor=SimpleExtractor())

        scenarios = [
            AxiomBenchmarkScenario(
                scenario_id=f"perf-test-{i}",
                prompt=f"Test scenario {i}",
                axiom_context="Performance test context",
            )
            for i in range(10)
        ]

        config = BenchmarkRunConfig(
            modes=[AxiomBenchmarkMode.BASELINE, AxiomBenchmarkMode.AXIOM_GUIDED], repetitions=1
        )

        _, elapsed = measure_execution_time(runner.run_with_config, scenarios, config)

        threshold = PERFORMANCE_THRESHOLDS["benchmark_runner_10_scenarios"]
        assert (
            elapsed < threshold
        ), f"10 scenarios took {elapsed:.2f}ms (threshold: {threshold}ms)"

    def test_large_n_scaling(self):
        """Test performance scaling with large n values"""
        # Test that performance doesn't degrade exponentially with n
        timings: List[float] = []

        for n in [1, 10, 50, 100]:
            axiom = UniversalAxiom(n=n)
            _, elapsed = measure_execution_time(axiom.compute_intelligence)
            timings.append(elapsed)

        # Each step should not be more than 2x slower than previous
        # (allowing for some variance due to Fibonacci computation)
        for i in range(1, len(timings)):
            ratio = timings[i] / timings[0] if timings[0] > 0 else 1
            # n=100 should not be more than 50x slower than n=1
            assert ratio < 50, f"Performance degraded significantly at n={[1, 10, 50, 100][i]}"

    def test_aggregator_performance(self):
        """Test that result aggregation is performant"""
        runner = AxiomBenchmarkRunner(adapter=SimpleAdapter(), extractor=SimpleExtractor())

        # Create 50 scenarios with 2 repetitions each (100 total results)
        scenarios = [
            AxiomBenchmarkScenario(scenario_id=f"agg-test-{i}", prompt=f"Test {i}")
            for i in range(50)
        ]

        config = BenchmarkRunConfig(
            modes=[AxiomBenchmarkMode.BASELINE, AxiomBenchmarkMode.AXIOM_GUIDED], repetitions=2
        )

        results = runner.run_with_config(scenarios, config)

        # Measure aggregation performance
        _, elapsed = measure_execution_time(AxiomBenchmarkAggregator.summarize, results)

        # Aggregation should be very fast (< 10ms for 200 results)
        assert elapsed < 10, f"Aggregation took {elapsed:.2f}ms (threshold: 10ms)"

    def test_memory_efficiency(self):
        """Test that simulations don't consume excessive memory"""
        import sys

        axiom = UniversalAxiom()
        simulator = AxiomSimulator(axiom)

        # Run simulation and check history size (use smaller steps to avoid overflow)
        simulator.simulate_evolution(steps=100)

        # Each history entry should be a small dict
        # 100 entries should be < 100KB
        history_size = sys.getsizeof(simulator.history)
        for entry in simulator.history:
            history_size += sys.getsizeof(entry)

        # Allow up to 100KB for 100 history entries
        max_size_kb = 100
        max_size_bytes = max_size_kb * 1024

        assert (
            history_size < max_size_bytes
        ), f"History consumed {history_size / 1024:.2f}KB (max: {max_size_kb}KB)"


class TestPerformanceMetrics:
    """Record and compare performance metrics over time"""

    METRICS_FILE = Path(__file__).parent / ".performance_metrics.json"

    def _load_metrics(self) -> Dict:
        """Load existing performance metrics"""
        if self.METRICS_FILE.exists():
            with open(self.METRICS_FILE, "r") as f:
                return json.load(f)
        return {}

    def _save_metrics(self, metrics: Dict):
        """Save performance metrics"""
        with open(self.METRICS_FILE, "w") as f:
            json.dump(metrics, f, indent=2)

    def test_record_baseline_metrics(self):
        """Record current performance as baseline (optional test)"""
        # This test records metrics but doesn't fail - use for establishing baselines
        metrics = self._load_metrics()

        # Measure current performance
        current = {}

        # Test 1: Intelligence computation
        axiom = UniversalAxiom(n=5)
        _, elapsed = measure_execution_time(axiom.compute_intelligence)
        current["intelligence_computation_n5"] = elapsed

        # Test 2: Evolution
        axiom = UniversalAxiom()
        _, elapsed = measure_execution_time(lambda: [axiom.evolve() for _ in range(10)])
        current["evolution_10_steps"] = elapsed

        # Test 3: Simulation
        axiom = UniversalAxiom()
        simulator = AxiomSimulator(axiom)
        _, elapsed = measure_execution_time(simulator.simulate_evolution, steps=100)
        current["simulation_100_steps"] = elapsed

        # Save as baseline if none exists, or record as latest
        if "baseline" not in metrics:
            metrics["baseline"] = current
            metrics["latest"] = current
        else:
            metrics["latest"] = current

        self._save_metrics(metrics)

        # Always pass - this is just recording
        assert True

    @pytest.mark.skipif(
        not Path(__file__).parent.joinpath(".performance_metrics.json").exists(),
        reason="No baseline metrics available",
    )
    def test_compare_against_baseline(self):
        """Compare current performance against baseline (requires baseline)"""
        metrics = self._load_metrics()
        baseline = metrics.get("baseline", {})

        if not baseline:
            pytest.skip("No baseline metrics available")

        # Measure current performance
        current = {}

        axiom = UniversalAxiom(n=5)
        _, elapsed = measure_execution_time(axiom.compute_intelligence)
        current["intelligence_computation_n5"] = elapsed

        axiom = UniversalAxiom()
        _, elapsed = measure_execution_time(lambda: [axiom.evolve() for _ in range(10)])
        current["evolution_10_steps"] = elapsed

        axiom = UniversalAxiom()
        simulator = AxiomSimulator(axiom)
        _, elapsed = measure_execution_time(simulator.simulate_evolution, steps=100)
        current["simulation_100_steps"] = elapsed

        # Check for regressions (allow 50% degradation tolerance)
        for key, baseline_time in baseline.items():
            current_time = current.get(key, 0)
            if baseline_time > 0:
                ratio = current_time / baseline_time
                assert (
                    ratio < 1.5
                ), f"{key}: Performance regressed by {(ratio - 1) * 100:.1f}% ({current_time:.2f}ms vs {baseline_time:.2f}ms baseline)"
