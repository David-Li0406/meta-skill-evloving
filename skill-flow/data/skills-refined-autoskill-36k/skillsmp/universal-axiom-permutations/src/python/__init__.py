"""
The Universal Axiom & The Epiphany Engine

A fundamental framework for modeling intelligence through immutable natural laws.

This module provides the core implementation of The Universal Axiom, which models
intelligence as a multiplicative interaction of:

- Foundation Layer (A · B · C): Physical reality
- Dynamic Layer (E_n · (1 + F_n)): Growth and regulation
- Cognitive Layer (X · Y · Z): Alignment and evolution

Example:
    >>> from universal_axiom import UniversalAxiom
    >>> axiom = UniversalAxiom(impulses=[1.0, 0.8], elements=[0.9, 0.7], pressure=1.2)
    >>> intelligence = axiom.compute_intelligence(n=5, subjectivity=6, why=0.9, time=1.0)
    >>> print(f"Intelligence: {intelligence}")

Website: https://www.epiphanyengine.ai
GitHub: https://github.com/TheUniversalAxiom/pointy-stick
"""

from .benchmarking import (
    AxiomBenchmarkMode,
    AxiomBenchmarkModeStats,
    AxiomBenchmarkResult,
    AxiomBenchmarkRunner,
    AxiomBenchmarkScenario,
    AxiomBenchmarkSummary,
    AxiomBenchmarkAggregator,
    AxiomBenchmarkResultWriter,
    AxiomScenarioSource,
    AxiomSignals,
    BenchmarkRunConfig,
)
from .math_solutions import ErdosProblem, MathSolutions, ProofStep
from .universal_axiom import UniversalAxiom

__version__ = "0.1.0"
__author__ = "Matt Belanger"
__email__ = "matt@epiphanyengine.ai"

__all__ = [
    "AxiomBenchmarkAggregator",
    "AxiomBenchmarkModeStats",
    "AxiomBenchmarkMode",
    "AxiomBenchmarkResult",
    "AxiomBenchmarkResultWriter",
    "AxiomBenchmarkRunner",
    "AxiomBenchmarkScenario",
    "AxiomBenchmarkSummary",
    "AxiomScenarioSource",
    "AxiomSignals",
    "BenchmarkRunConfig",
    "ErdosProblem",
    "MathSolutions",
    "ProofStep",
    "UniversalAxiom",
]
