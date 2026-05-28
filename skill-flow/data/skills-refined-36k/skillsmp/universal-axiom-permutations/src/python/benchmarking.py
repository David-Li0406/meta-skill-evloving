"""
Benchmarking utilities for comparing AI models against and with The Universal Axiom.
"""

from dataclasses import dataclass
from enum import Enum
from statistics import mean, median
from typing import Dict, Iterable, List, Mapping, Protocol, Sequence

from .universal_axiom import AxiomSimulator, UniversalAxiom


class AxiomBenchmarkMode(Enum):
    """Benchmark modes for comparing baseline vs axiom-guided behavior."""

    BASELINE = "baseline"
    AXIOM_GUIDED = "axiom_guided"


@dataclass(frozen=True)
class AxiomSignals:
    """Signals mapped to the Universal Axiom variables (A, B, C, X, Y, Z, n)."""

    impulses: float
    elements: float
    pressure: float
    subjectivity: float
    purpose: float
    time: float
    n: int = 1

    def to_axiom(self) -> UniversalAxiom:
        """Create a UniversalAxiom instance from the signals."""
        return UniversalAxiom(
            impulses=self.impulses,
            elements=self.elements,
            pressure=self.pressure,
            subjectivity=self.subjectivity,
            purpose=self.purpose,
            time=self.time,
            n=self.n,
        )


@dataclass(frozen=True)
class AxiomBenchmarkScenario:
    """Benchmark scenario configuration."""

    scenario_id: str
    prompt: str
    axiom_context: str | None = None

    def render_prompt(self, mode: AxiomBenchmarkMode) -> str:
        """Render the prompt for the selected benchmark mode."""
        if mode == AxiomBenchmarkMode.AXIOM_GUIDED and self.axiom_context:
            return f"{self.prompt}\n\n{self.axiom_context}"
        return self.prompt


@dataclass(frozen=True)
class AxiomBenchmarkResult:
    """Benchmark result containing both axiom metrics and response details."""

    model_id: str
    scenario_id: str
    mode: AxiomBenchmarkMode
    prompt: str
    response: str
    signals: AxiomSignals
    intelligence: float
    coherence: float


@dataclass(frozen=True)
class BenchmarkRunConfig:
    """Configuration for running benchmarks."""

    modes: Sequence[AxiomBenchmarkMode] = (
        AxiomBenchmarkMode.BASELINE,
        AxiomBenchmarkMode.AXIOM_GUIDED,
    )
    repetitions: int = 1


@dataclass(frozen=True)
class AxiomBenchmarkModeStats:
    """Aggregate statistics for a single benchmark mode."""

    count: int
    intelligence_mean: float
    intelligence_median: float
    coherence_mean: float
    coherence_median: float


@dataclass(frozen=True)
class AxiomBenchmarkSummary:
    """Summary aggregates and deltas for a benchmark run."""

    per_mode: Mapping[AxiomBenchmarkMode, AxiomBenchmarkModeStats]
    intelligence_delta: float | None
    coherence_delta: float | None


class AxiomModelAdapter(Protocol):
    """Adapter interface for generating model responses."""

    model_id: str

    def generate(self, prompt: str, mode: AxiomBenchmarkMode) -> str:
        """Generate a response for the given prompt."""


class AxiomSignalExtractor(Protocol):
    """Extractor interface for mapping responses to Axiom signals."""

    def extract(self, prompt: str, response: str) -> AxiomSignals:
        """Extract A, B, C, X, Y, Z, n signals from the response."""


class AxiomScenarioSource(Protocol):
    """Scenario source for loading benchmark scenarios."""

    def load(self) -> Sequence[AxiomBenchmarkScenario]:
        """Load benchmark scenarios."""


class AxiomBenchmarkResultWriter(Protocol):
    """Writer interface for persisting benchmark results."""

    def write(self, results: Sequence[AxiomBenchmarkResult], summary: AxiomBenchmarkSummary) -> None:
        """Persist benchmark results."""


@dataclass
class AxiomBenchmarkRunner:
    """Run benchmark scenarios against a model adapter."""

    adapter: AxiomModelAdapter
    extractor: AxiomSignalExtractor
    modes: Sequence[AxiomBenchmarkMode] = (
        AxiomBenchmarkMode.BASELINE,
        AxiomBenchmarkMode.AXIOM_GUIDED,
    )

    def run(self, scenarios: Iterable[AxiomBenchmarkScenario]) -> List[AxiomBenchmarkResult]:
        """Run all scenarios across the configured modes."""
        return self.run_with_config(scenarios, BenchmarkRunConfig(modes=self.modes))

    def run_with_config(
        self, scenarios: Iterable[AxiomBenchmarkScenario], config: BenchmarkRunConfig
    ) -> List[AxiomBenchmarkResult]:
        """Run scenarios with explicit configuration."""
        results: List[AxiomBenchmarkResult] = []

        for scenario in scenarios:
            for mode in config.modes:
                for _ in range(config.repetitions):
                    prompt = scenario.render_prompt(mode)
                    response = self.adapter.generate(prompt, mode)
                    signals = self.extractor.extract(prompt, response)
                    axiom = signals.to_axiom()
                    intelligence = axiom.compute_intelligence()
                    coherence = AxiomSimulator(axiom).get_coherence_metric()

                    results.append(
                        AxiomBenchmarkResult(
                            model_id=self.adapter.model_id,
                            scenario_id=scenario.scenario_id,
                            mode=mode,
                            prompt=prompt,
                            response=response,
                            signals=signals,
                            intelligence=intelligence,
                            coherence=coherence,
                        )
                    )

        return results


class AxiomBenchmarkAggregator:
    """Aggregate benchmark results into summary statistics."""

    @staticmethod
    def summarize(results: Sequence[AxiomBenchmarkResult]) -> AxiomBenchmarkSummary:
        """Summarize benchmark results across modes."""
        grouped: Dict[AxiomBenchmarkMode, List[AxiomBenchmarkResult]] = {}
        for result in results:
            grouped.setdefault(result.mode, []).append(result)

        per_mode: Dict[AxiomBenchmarkMode, AxiomBenchmarkModeStats] = {}
        for mode, mode_results in grouped.items():
            intelligence_values = [item.intelligence for item in mode_results]
            coherence_values = [item.coherence for item in mode_results]

            per_mode[mode] = AxiomBenchmarkModeStats(
                count=len(mode_results),
                intelligence_mean=mean(intelligence_values),
                intelligence_median=median(intelligence_values),
                coherence_mean=mean(coherence_values),
                coherence_median=median(coherence_values),
            )

        baseline_stats = per_mode.get(AxiomBenchmarkMode.BASELINE)
        guided_stats = per_mode.get(AxiomBenchmarkMode.AXIOM_GUIDED)

        intelligence_delta = None
        coherence_delta = None
        if baseline_stats and guided_stats:
            intelligence_delta = guided_stats.intelligence_mean - baseline_stats.intelligence_mean
            coherence_delta = guided_stats.coherence_mean - baseline_stats.coherence_mean

        return AxiomBenchmarkSummary(
            per_mode=per_mode,
            intelligence_delta=intelligence_delta,
            coherence_delta=coherence_delta,
        )
