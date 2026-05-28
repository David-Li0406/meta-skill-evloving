"""
The Universal Axiom - Core Implementation

Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)

Foundation Layer: Impulses (A), Elements (B), Pressure (C)
Dynamic Layer: Exponential Growth (E_n), Fibonacci Sequence (F_n)
Cognitive Layer: Subjectivity Scale (X), Why Axis (Y), TimeSphere (Z)
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class FoundationLayer:
    """Foundation Layer: A · B · C"""

    impulses: float  # A - Fundamental drives
    elements: float  # B - Core components
    pressure: float  # C - Constraints and forces

    def compute(self) -> float:
        """Compute foundation layer product"""
        return self.impulses * self.elements * self.pressure


@dataclass
class DynamicLayer:
    """Dynamic Layer: E_n · (1 + F_n)"""

    n: int  # Current iteration/step
    base_exponential: float = 3.0  # Base for exponential growth

    def exponential_growth(self) -> float:
        """E_n - Exponential growth component"""
        return (2 * (self.base_exponential**self.n)) - 1

    def fibonacci(self) -> int:
        """F_n - Fibonacci sequence for natural regulation"""
        if self.n <= 1:
            return 1

        a, b = 1, 1
        for _ in range(2, self.n + 1):
            a, b = b, a + b
        return b

    def compute(self) -> float:
        """Compute dynamic layer: E_n · (1 + F_n)"""
        E_n = self.exponential_growth()
        F_n = self.fibonacci()
        return E_n * (1 + F_n)


@dataclass
class CognitiveLayer:
    """Cognitive Layer: X · Y · Z"""

    subjectivity: (
        float  # X - Objectivity measure (0 = fully objective, 1 = fully subjective)
    )
    purpose: float  # Y - Purpose-driven reasoning strength
    time: float  # Z - Temporal continuity and irreversibility

    def compute(self) -> float:
        """Compute cognitive layer product"""
        # X represents objectivity, so we invert: (1 - subjectivity) for objectivity score
        objectivity = 1 - self.subjectivity
        return objectivity * self.purpose * self.time


class UniversalAxiom:
    """
    The Universal Axiom - Complete Intelligence Model

    Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
    """

    def __init__(
        self,
        impulses: float = 1.0,
        elements: float = 1.0,
        pressure: float = 1.0,
        subjectivity: float = 0.0,
        purpose: float = 1.0,
        time: float = 1.0,
        n: int = 1,
    ):
        """
        Initialize The Universal Axiom

        Args:
            impulses: A - Fundamental drives (default: 1.0)
            elements: B - Core components (default: 1.0)
            pressure: C - Constraints and forces (default: 1.0)
            subjectivity: X - Subjectivity level 0-1 (default: 0.0 = fully objective)
            purpose: Y - Purpose strength (default: 1.0)
            time: Z - Temporal factor (default: 1.0)
            n: Current iteration step (default: 1)
        """
        self.foundation = FoundationLayer(impulses, elements, pressure)
        self.dynamic = DynamicLayer(n)
        self.cognitive = CognitiveLayer(subjectivity, purpose, time)
        self.n = n

    def compute_intelligence(self) -> float:
        """
        Compute Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)

        Returns:
            float: The computed intelligence value
        """
        foundation_value = self.foundation.compute()
        dynamic_value = self.dynamic.compute()
        cognitive_value = self.cognitive.compute()

        intelligence = dynamic_value * cognitive_value * foundation_value
        return intelligence

    def evolve(self, delta_time: float = 1.0) -> float:
        """
        Evolve the system forward in time

        Args:
            delta_time: Time step increment

        Returns:
            float: New intelligence value after evolution
        """
        self.n += 1
        self.dynamic.n = self.n
        self.cognitive.time += delta_time

        return self.compute_intelligence()

    def apply_pressure(self, pressure_delta: float) -> float:
        """
        Apply pressure change (e.g., from contradictions or constraints)

        Args:
            pressure_delta: Change in pressure (can be positive or negative)

        Returns:
            float: New intelligence value after pressure application
        """
        self.foundation.pressure += pressure_delta
        # Ensure pressure stays positive
        self.foundation.pressure = max(0.01, self.foundation.pressure)

        return self.compute_intelligence()

    def adjust_subjectivity(self, subjectivity_delta: float) -> float:
        """
        Adjust subjectivity level (moving toward objectivity or away)

        Args:
            subjectivity_delta: Change in subjectivity (-1 to +1)

        Returns:
            float: New intelligence value after adjustment
        """
        self.cognitive.subjectivity += subjectivity_delta
        # Clamp between 0 and 1
        self.cognitive.subjectivity = max(0.0, min(1.0, self.cognitive.subjectivity))

        return self.compute_intelligence()

    def strengthen_purpose(self, purpose_multiplier: float) -> float:
        """
        Strengthen or weaken purpose alignment

        Args:
            purpose_multiplier: Multiplier for purpose (e.g., 1.1 = 10% increase)

        Returns:
            float: New intelligence value after purpose adjustment
        """
        self.cognitive.purpose *= purpose_multiplier
        self.cognitive.purpose = max(0.01, self.cognitive.purpose)

        return self.compute_intelligence()

    def get_state(self) -> Dict:
        """
        Get current state of all variables

        Returns:
            Dict: Complete state dictionary
        """
        return {
            "n": self.n,
            "foundation": {
                "A_impulses": self.foundation.impulses,
                "B_elements": self.foundation.elements,
                "C_pressure": self.foundation.pressure,
                "product": self.foundation.compute(),
            },
            "dynamic": {
                "E_n": self.dynamic.exponential_growth(),
                "F_n": self.dynamic.fibonacci(),
                "product": self.dynamic.compute(),
            },
            "cognitive": {
                "X_subjectivity": self.cognitive.subjectivity,
                "X_objectivity": 1 - self.cognitive.subjectivity,
                "Y_purpose": self.cognitive.purpose,
                "Z_time": self.cognitive.time,
                "product": self.cognitive.compute(),
            },
            "intelligence": self.compute_intelligence(),
        }

    def __repr__(self) -> str:
        state = self.get_state()
        return f"UniversalAxiom(n={self.n}, Intelligence={state['intelligence']:.4f})"


class AxiomSimulator:
    """Simulator for running Universal Axiom scenarios"""

    def __init__(self, axiom: UniversalAxiom):
        self.axiom = axiom
        self.history: List[Dict] = []

    def record_state(self):
        """Record current state to history"""
        self.history.append(self.axiom.get_state())

    def simulate_evolution(
        self, steps: int = 10, delta_time: float = 1.0
    ) -> List[Dict]:
        """
        Simulate evolution over multiple time steps

        Args:
            steps: Number of evolution steps
            delta_time: Time increment per step

        Returns:
            List[Dict]: History of states
        """
        self.history = []
        self.record_state()

        for _ in range(steps):
            self.axiom.evolve(delta_time)
            self.record_state()

        return self.history

    def simulate_contradiction_resolution(
        self, initial_pressure: float = 2.0, resolution_steps: int = 5
    ) -> List[Dict]:
        """
        Simulate how the system handles contradiction

        Args:
            initial_pressure: Initial pressure spike from contradiction
            resolution_steps: Steps to resolve the contradiction

        Returns:
            List[Dict]: History showing pressure resolution
        """
        self.history = []
        self.record_state()

        # Apply initial pressure spike
        self.axiom.apply_pressure(initial_pressure)
        self.record_state()

        # Gradually resolve through objectivity adjustment and pressure release
        for i in range(resolution_steps):
            # Reduce subjectivity (increase objectivity)
            self.axiom.adjust_subjectivity(-0.1)

            # Release pressure as understanding increases
            pressure_release = -initial_pressure / resolution_steps
            self.axiom.apply_pressure(pressure_release)

            # Evolve forward
            self.axiom.evolve()
            self.record_state()

        return self.history

    def get_coherence_metric(self) -> float:
        """
        Calculate coherence metric based on balance of components

        Returns:
            float: Coherence score (higher is more coherent)
        """
        state = self.axiom.get_state()

        # Coherence is high when:
        # - Objectivity is high (low subjectivity)
        # - Purpose is strong
        # - Pressure is moderate (not too high or low)
        # - Components are balanced

        objectivity_score = state["cognitive"]["X_objectivity"]
        purpose_score = min(state["cognitive"]["Y_purpose"] / 2.0, 1.0)
        pressure_score = 1.0 / (1.0 + abs(state["foundation"]["C_pressure"] - 1.0))

        coherence = (objectivity_score + purpose_score + pressure_score) / 3.0
        return coherence


def fibonacci_sequence(n: int) -> List[int]:
    """Generate Fibonacci sequence up to n terms"""
    if n <= 0:
        return []
    elif n == 1:
        return [1]

    sequence = [1, 1]
    for i in range(2, n):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence
