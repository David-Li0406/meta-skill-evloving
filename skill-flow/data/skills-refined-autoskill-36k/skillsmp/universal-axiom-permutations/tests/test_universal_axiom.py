"""
Test suite for The Universal Axiom
Tests the core formula: Intelligence_n = E_n⋅(1+F_n)⋅X⋅Y⋅Z⋅(A⋅B⋅C)
Based on PROMPT.md principles and The Epiphany Engine specifications
"""

import csv
import math
from pathlib import Path

import pytest
from python.universal_axiom import (
    FoundationLayer,
    DynamicLayer,
    CognitiveLayer,
    UniversalAxiom,
    AxiomSimulator,
    fibonacci_sequence,
)
from python.math_solutions import ErdosProblem, MathSolutions, ProofStep


class TestFoundationLayer:
    """Test Foundation Layer (A·B·C) - Impulses, Elements, Pressure"""

    def test_initialization(self):
        """Test foundation layer initializes correctly per PROMPT.md"""
        foundation = FoundationLayer(impulses=1.0, elements=1.0, pressure=1.0)
        assert foundation.impulses == 1.0
        assert foundation.elements == 1.0
        assert foundation.pressure == 1.0

    def test_compute_product(self):
        """Test A·B·C product calculation"""
        foundation = FoundationLayer(impulses=2.0, elements=3.0, pressure=1.5)
        assert foundation.compute() == 2.0 * 3.0 * 1.5


class TestDynamicLayer:
    """Test Dynamic Layer (E_n·(1+F_n)) - Exponential growth with Fibonacci regulation"""

    def test_fibonacci_sequence_generation(self):
        """Test Fibonacci sequence generation as per PROMPT.md"""
        sequence = fibonacci_sequence(12)
        expected = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        assert sequence == expected

    def test_fibonacci_sequence_edge_cases(self):
        """Test Fibonacci sequence edge cases"""
        assert fibonacci_sequence(0) == []
        assert fibonacci_sequence(-1) == []
        assert fibonacci_sequence(1) == [1]
        assert fibonacci_sequence(2) == [1, 1]

    def test_fibonacci_at_n(self):
        """Test F_n Fibonacci component"""
        dynamic = DynamicLayer(n=1)
        assert dynamic.fibonacci() == 1

        dynamic = DynamicLayer(n=10)
        assert dynamic.fibonacci() == 89

    def test_exponential_growth(self):
        """Test E_n = 2 * 3^n - 1 exponential component"""
        dynamic = DynamicLayer(n=1)
        assert dynamic.exponential_growth() == 5

        dynamic = DynamicLayer(n=2)
        assert dynamic.exponential_growth() == 17

    def test_compute_product(self):
        """Test E_n·(1+F_n) product"""
        dynamic = DynamicLayer(n=1)
        E_n = 5
        F_n = 1
        expected = E_n * (1 + F_n)
        assert abs(dynamic.compute() - expected) < 1e-6


class TestCognitiveLayer:
    """Test Cognitive Layer (X·Y·Z) - Objectivity, Purpose, Time"""

    def test_subjectivity_objectivity_relationship(self):
        """Test X = 1 - subjectivity per PROMPT.md subjectivity scale"""
        cognitive = CognitiveLayer(subjectivity=0.3, purpose=1.0, time=1.0)
        objectivity = 1 - cognitive.subjectivity
        assert objectivity == 0.7

    def test_compute_product(self):
        """Test X·Y·Z product"""
        cognitive = CognitiveLayer(subjectivity=0.2, purpose=1.5, time=2.0)
        expected = 0.8 * 1.5 * 2.0  # objectivity * purpose * time
        assert cognitive.compute() == expected


class TestUniversalAxiom:
    """Test the core Universal Axiom: Intelligence_n = E_n⋅(1+F_n)⋅X⋅Y⋅Z⋅(A⋅B⋅C)"""

    def test_initialization(self):
        """Test axiom initializes with all layers"""
        axiom = UniversalAxiom()
        assert axiom.foundation is not None
        assert axiom.dynamic is not None
        assert axiom.cognitive is not None
        assert axiom.n == 1

    def test_core_formula_computation(self):
        """Test Intelligence_n = E_n⋅(1+F_n)⋅X⋅Y⋅Z⋅(A⋅B⋅C)"""
        axiom = UniversalAxiom(impulses=1.0, elements=1.0, pressure=1.0, n=1)

        # Manual calculation per PROMPT.md
        A_B_C = 1.0 * 1.0 * 1.0
        E_n = 5
        F_n = 1
        E_F = E_n * (1 + F_n)
        X_Y_Z = 1.0 * 1.0 * 1.0
        expected = E_F * X_Y_Z * A_B_C

        intelligence = axiom.compute_intelligence()
        assert abs(intelligence - expected) < 1e-6

    def test_intelligence_at_n_1(self):
        """Test intelligence value at n=1 matches TEST_RESULTS.md"""
        axiom = UniversalAxiom(n=1)
        intelligence = axiom.compute_intelligence()
        assert abs(intelligence - 10.0) < 0.001

    def test_intelligence_at_n_10(self):
        """Test intelligence value at n=10 matches TEST_RESULTS.md"""
        axiom = UniversalAxiom(n=1)
        for _ in range(9):
            axiom.evolve()
        intelligence = axiom.compute_intelligence()
        # n=10 value with new formula (base 3.0): 106,287,300
        assert intelligence == 106_287_300

    def test_evolve_increases_intelligence(self):
        """Test evolution increases intelligence per PROMPT.md"""
        axiom = UniversalAxiom(n=1)
        intelligence_before = axiom.compute_intelligence()
        axiom.evolve()
        intelligence_after = axiom.compute_intelligence()
        assert intelligence_after > intelligence_before

    def test_apply_pressure_increases_foundation(self):
        """Test pressure application (C variable) affects foundation"""
        axiom = UniversalAxiom(pressure=1.0)
        intelligence_before = axiom.compute_intelligence()
        axiom.apply_pressure(1.0)
        intelligence_after = axiom.compute_intelligence()
        assert intelligence_after > intelligence_before

    def test_pressure_clamping_minimum(self):
        """Test pressure is clamped to minimum 0.01"""
        axiom = UniversalAxiom(pressure=1.0)
        axiom.apply_pressure(-10.0)  # Try to make negative
        assert axiom.foundation.pressure == 0.01

    def test_adjust_subjectivity_changes_objectivity(self):
        """Test adjusting subjectivity changes X (objectivity) component"""
        axiom = UniversalAxiom(subjectivity=0.5)
        intelligence_before = axiom.compute_intelligence()
        axiom.adjust_subjectivity(-0.2)  # Reduce subjectivity, increase objectivity
        intelligence_after = axiom.compute_intelligence()
        assert intelligence_after > intelligence_before
        assert axiom.cognitive.subjectivity == 0.3

    def test_subjectivity_clamping(self):
        """Test subjectivity clamped to [0.0, 1.0]"""
        axiom = UniversalAxiom(subjectivity=0.5)
        axiom.adjust_subjectivity(1.0)  # Try to exceed 1.0
        assert axiom.cognitive.subjectivity == 1.0

        axiom.adjust_subjectivity(-2.0)  # Try to go below 0.0
        assert axiom.cognitive.subjectivity == 0.0

    def test_strengthen_purpose_multiplier(self):
        """Test purpose strengthening uses multiplier"""
        axiom = UniversalAxiom(purpose=1.0)
        intelligence_before = axiom.compute_intelligence()
        axiom.strengthen_purpose(1.5)  # 1.5x multiplier
        assert axiom.cognitive.purpose == 1.5
        intelligence_after = axiom.compute_intelligence()
        assert intelligence_after > intelligence_before

    def test_get_state_completeness(self):
        """Test state snapshot includes all components"""
        axiom = UniversalAxiom()
        state = axiom.get_state()

        assert "n" in state
        assert "intelligence" in state
        assert "foundation" in state
        assert "dynamic" in state
        assert "cognitive" in state

    def test_negative_impulses(self):
        """Test negative impulses (per PROMPT.md A can be positive or negative)"""
        axiom = UniversalAxiom(impulses=-1.0)
        intelligence = axiom.compute_intelligence()
        assert intelligence < 0  # Negative impulse = negative intelligence

    def test_extreme_subjectivity(self):
        """Test extreme subjectivity (base static processing per PROMPT.md)"""
        axiom = UniversalAxiom(subjectivity=1.0)  # Maximum subjectivity
        intelligence = axiom.compute_intelligence()
        assert intelligence == 0.0  # Zero objectivity = zero intelligence

    def test_axiom_repr(self):
        """Test UniversalAxiom string representation"""
        axiom = UniversalAxiom(n=5)
        repr_str = repr(axiom)
        assert "UniversalAxiom" in repr_str
        assert "n=5" in repr_str
        assert "Intelligence=" in repr_str


class TestMathSolutions:
    """Test MathSolutions interface for Erdos problems."""

    def test_erdos_seed_contains_problem(self):
        solutions = MathSolutions.erdos_seed()
        expected = {
            "erdos-straus": "open",
            "erdos-distinct-distances": "solved",
            "erdos-moser": "partial",
            "erdos-ko-rado": "solved",
            "erdos-szekeres": "partial",
            "erdos-faber-lovasz": "solved",
            "erdos-ginzburg-ziv": "solved",
            "erdos-heilbronn": "solved",
            "erdos-discrepancy": "solved",
        }

        problems = solutions.list_problems()
        assert len(problems) == len(expected)

        for identifier, status in expected.items():
            problem = solutions.get_problem(identifier)
            assert isinstance(problem, ErdosProblem)
            assert problem.status == status
            assert len(problem.proof_steps) == 5

    def test_add_proof_step(self):
        solutions = MathSolutions.erdos_seed()
        solutions.add_proof_step(
            "erdos-straus",
            "Normalize the equation to isolate reciprocal structure.",
            "Use the axiom's foundation layer (A·B·C) to align constraints.",
        )

        problem = solutions.get_problem("erdos-straus")
        assert len(problem.proof_steps) == 6
        step = problem.proof_steps[-1]
        assert isinstance(step, ProofStep)
        assert "Normalize the equation" in step.statement

    def test_proof_step_to_dict(self):
        """Test ProofStep serialization to dictionary"""
        step = ProofStep(
            statement="Test statement",
            axiom_insight="Test insight"
        )
        result = step.to_dict()
        assert result == {
            "statement": "Test statement",
            "axiom_insight": "Test insight"
        }

    def test_erdos_problem_to_dict(self):
        """Test ErdosProblem serialization to dictionary"""
        problem = ErdosProblem(
            identifier="test-problem",
            title="Test Problem",
            statement="Test statement",
            status="open",
            axiom_insight="Test insight"
        )
        problem.add_proof_step("Step 1", "Insight 1")
        result = problem.to_dict()

        assert result["identifier"] == "test-problem"
        assert result["title"] == "Test Problem"
        assert result["statement"] == "Test statement"
        assert result["status"] == "open"
        assert result["axiom_insight"] == "Test insight"
        assert len(result["proof_steps"]) == 1
        assert result["proof_steps"][0]["statement"] == "Step 1"

    def test_erdos_problem_add_proof_steps(self):
        """Test adding multiple proof steps at once"""
        problem = ErdosProblem(
            identifier="test-multi",
            title="Test Multiple Steps",
            statement="Test",
            status="open",
            axiom_insight="Test"
        )
        steps = [
            ProofStep("Step 1", "Insight 1"),
            ProofStep("Step 2", "Insight 2"),
            ProofStep("Step 3", "Insight 3")
        ]
        problem.add_proof_steps(steps)

        assert len(problem.proof_steps) == 3
        assert problem.proof_steps[0].statement == "Step 1"
        assert problem.proof_steps[1].statement == "Step 2"
        assert problem.proof_steps[2].statement == "Step 3"

    def test_math_solutions_summaries(self):
        """Test MathSolutions.summaries() method"""
        solutions = MathSolutions.erdos_seed()
        summaries = solutions.summaries()

        assert len(summaries) > 0
        for summary in summaries:
            assert "identifier" in summary
            assert "title" in summary
            assert "status" in summary
            # Check that these are the only keys
            assert set(summary.keys()) == {"identifier", "title", "status"}

    def test_extreme_objectivity(self):
        """Test extreme objectivity (apex dynamic processing)"""
        axiom = UniversalAxiom(subjectivity=0.0)  # Maximum objectivity
        intelligence = axiom.compute_intelligence()
        assert intelligence > 0


class TestAxiomSimulator:
    """Test AxiomSimulator for scenario execution"""

    def test_initialization(self):
        """Test simulator initializes with axiom"""
        axiom = UniversalAxiom()
        simulator = AxiomSimulator(axiom)
        assert simulator.axiom == axiom

    def test_simulate_evolution_tracks_history(self):
        """Test evolution simulation tracks state history"""
        axiom = UniversalAxiom(n=1)
        simulator = AxiomSimulator(axiom)
        history = simulator.simulate_evolution(steps=5)

        assert len(history) == 6  # initial + 5 steps
        assert history[0]["n"] == 1
        assert history[-1]["n"] == 6

    def test_contradiction_resolution_reduces_subjectivity(self):
        """Test contradiction resolution per PROMPT.md pressure dynamics"""
        axiom = UniversalAxiom(subjectivity=0.5, pressure=1.0)
        simulator = AxiomSimulator(axiom)

        initial_subjectivity = axiom.cognitive.subjectivity
        history = simulator.simulate_contradiction_resolution(
            initial_pressure=2.0, resolution_steps=5
        )

        final_subjectivity = history[-1]["cognitive"]["X_subjectivity"]
        assert final_subjectivity < initial_subjectivity

    def test_coherence_metric_high_objectivity(self):
        """Test coherence tracking per PROMPT.md"""
        axiom = UniversalAxiom(subjectivity=0.1, purpose=2.0, pressure=1.0)
        simulator = AxiomSimulator(axiom)
        coherence = simulator.get_coherence_metric()

        # High objectivity + strong purpose = high coherence
        assert coherence > 0.8

    def test_coherence_decreases_with_subjectivity(self):
        """Test coherence decreases as subjectivity increases"""
        axiom_objective = UniversalAxiom(subjectivity=0.1)
        coherence_objective = AxiomSimulator(axiom_objective).get_coherence_metric()

        axiom_subjective = UniversalAxiom(subjectivity=0.8)
        coherence_subjective = AxiomSimulator(axiom_subjective).get_coherence_metric()

        assert coherence_objective > coherence_subjective

    def test_no_stagnation_with_evolution(self):
        """Test system doesn't stagnate - intelligence grows over time"""
        axiom = UniversalAxiom(n=1)
        simulator = AxiomSimulator(axiom)
        history = simulator.simulate_evolution(steps=10)

        intelligences = [state["intelligence"] for state in history]

        # Verify monotonic increase
        for i in range(1, len(intelligences)):
            assert intelligences[i] > intelligences[i - 1]


class TestGoldenCases:
    """Cross-language golden data cases for parity checks."""

    def test_golden_cases_match_expected(self):
        """Validate intelligence results against golden case expectations."""
        golden_path = Path(__file__).with_name("golden_cases.csv")
        with golden_path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                axiom = UniversalAxiom(
                    impulses=float(row["impulses"]),
                    elements=float(row["elements"]),
                    pressure=float(row["pressure"]),
                    subjectivity=float(row["subjectivity"]),
                    purpose=float(row["purpose"]),
                    time=float(row["time"]),
                    n=int(row["n"]),
                )
                expected = float(row["expected_intelligence"])
                actual = axiom.compute_intelligence()
                assert math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-6), row[
                    "name"
                ]


class TestPROMPTCompliance:
    """Test compliance with PROMPT.md specifications"""

    def test_axiom_is_deterministic(self):
        """Test axiom mirrors physics laws - same inputs = same outputs"""
        axiom1 = UniversalAxiom(n=5, impulses=1.0, elements=1.0)
        axiom2 = UniversalAxiom(n=5, impulses=1.0, elements=1.0)

        assert axiom1.compute_intelligence() == axiom2.compute_intelligence()

    def test_fibonacci_regulation_of_dynamics(self):
        """Test Fibonacci sequence regulates system dynamics per PROMPT.md"""
        axiom = UniversalAxiom(n=1)
        simulator = AxiomSimulator(axiom)
        history = simulator.simulate_evolution(steps=10)

        # Extract Fibonacci values
        fib_values = [state["dynamic"]["F_n"] for state in history[:10]]
        expected = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

        assert fib_values == expected

    def test_pressure_reveals_contradictions(self):
        """Test pressure dynamics reveal contradictions per PROMPT.md"""
        axiom = UniversalAxiom(subjectivity=0.5, pressure=1.0)

        # Apply pressure spike (contradiction)
        axiom.apply_pressure(2.0)

        # Pressure should be elevated
        assert axiom.foundation.pressure == 3.0

    def test_timesphere_advancement(self):
        """Test TimeSphere (Z) represents objective nature over time"""
        axiom = UniversalAxiom(time=1.0)
        simulator = AxiomSimulator(axiom)
        history = simulator.simulate_evolution(steps=5)

        # Time should advance with evolution
        times = [state["cognitive"]["Z_time"] for state in history]
        assert times == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

    def test_foundation_abc_variables(self):
        """Test Foundation Layer A, B, C per PROMPT.md definitions"""
        axiom = UniversalAxiom(impulses=2.0, elements=3.0, pressure=1.5)
        state = axiom.get_state()

        # A = Impulses (Current)
        assert state["foundation"]["A_impulses"] == 2.0

        # B = Elements (Energy, Matter, State)
        assert state["foundation"]["B_elements"] == 3.0

        # C = Pressure (Direction, Momentum, Integrity)
        assert state["foundation"]["C_pressure"] == 1.5

        # Product = A·B·C
        assert state["foundation"]["product"] == 2.0 * 3.0 * 1.5

    def test_cognitive_xyz_variables(self):
        """Test Cognitive Layer X, Y, Z per PROMPT.md definitions"""
        axiom = UniversalAxiom(subjectivity=0.3, purpose=1.5, time=2.0)
        state = axiom.get_state()

        # X = subjectivity scaling aggregate (0 to 1)
        assert state["cognitive"]["X_subjectivity"] == 0.3
        assert state["cognitive"]["X_objectivity"] == 0.7

        # Y = The Why Axis scale (purpose)
        assert state["cognitive"]["Y_purpose"] == 1.5

        # Z = flux of Time (TimeSphere)
        assert state["cognitive"]["Z_time"] == 2.0

    def test_large_n_fibonacci_growth(self):
        """Test system handles large n values with Fibonacci regulation"""
        axiom = UniversalAxiom(n=1)
        for _ in range(19):  # n=20
            axiom.evolve()

        intelligence = axiom.compute_intelligence()
        assert intelligence > 0
        assert math.isfinite(intelligence)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
