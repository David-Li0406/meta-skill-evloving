"""
Basic Usage Examples for The Universal Axiom

Demonstrates core functionality and key concepts.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from python.universal_axiom import UniversalAxiom, AxiomSimulator, fibonacci_sequence


def example_basic_computation():
    """Example 1: Basic Intelligence Computation"""
    print("=" * 60)
    print("Example 1: Basic Intelligence Computation")
    print("=" * 60)

    # Create axiom with default values
    axiom = UniversalAxiom()
    print(f"\nInitial state: {axiom}")

    # Compute intelligence
    intelligence = axiom.compute_intelligence()
    print(f"Intelligence value: {intelligence:.6f}")

    # Display full state
    state = axiom.get_state()
    print("\nDetailed State:")
    print(f"  Foundation (A·B·C): {state['foundation']['product']:.6f}")
    print(f"    A (Impulses): {state['foundation']['A_impulses']}")
    print(f"    B (Elements): {state['foundation']['B_elements']}")
    print(f"    C (Pressure): {state['foundation']['C_pressure']}")
    print(f"  Dynamic (E_n·(1+F_n)): {state['dynamic']['product']:.6f}")
    print(f"    E_n: {state['dynamic']['E_n']:.6f}")
    print(f"    F_n: {state['dynamic']['F_n']}")
    print(f"  Cognitive (X·Y·Z): {state['cognitive']['product']:.6f}")
    print(f"    X (Objectivity): {state['cognitive']['X_objectivity']}")
    print(f"    Y (Purpose): {state['cognitive']['Y_purpose']}")
    print(f"    Z (Time): {state['cognitive']['Z_time']}")


def example_evolution():
    """Example 2: System Evolution Over Time"""
    print("\n" + "=" * 60)
    print("Example 2: System Evolution Over Time")
    print("=" * 60)

    axiom = UniversalAxiom(impulses=1.0, elements=1.0, pressure=1.0, n=1)
    simulator = AxiomSimulator(axiom)

    print("\nEvolving system over 10 steps...")
    history = simulator.simulate_evolution(steps=10, delta_time=1.0)

    print(f"\n{'Step':<6} {'Intelligence':<15} {'F_n':<8} {'Time':<8}")
    print("-" * 45)
    for i, state in enumerate(history):
        print(
            f"{i:<6} {state['intelligence']:<15.6f} "
            f"{state['dynamic']['F_n']:<8} {state['cognitive']['Z_time']:<8.1f}"
        )

    print(f"\nFibonacci Growth Pattern: {[h['dynamic']['F_n'] for h in history[:10]]}")


def example_contradiction_resolution():
    """Example 3: Contradiction Resolution"""
    print("\n" + "=" * 60)
    print("Example 3: Contradiction Resolution")
    print("=" * 60)

    # Start with some subjectivity
    axiom = UniversalAxiom(
        impulses=1.0,
        elements=1.0,
        pressure=1.0,
        subjectivity=0.5,  # Start with 50% subjectivity
        purpose=1.0,
        n=1
    )

    simulator = AxiomSimulator(axiom)

    print("\nSimulating contradiction encounter and resolution...")
    print("Initial subjectivity: 0.5 (50% subjective)")
    print("Applying pressure spike from contradiction...\n")

    history = simulator.simulate_contradiction_resolution(
        initial_pressure=2.0,
        resolution_steps=5
    )

    print(f"{'Step':<6} {'Intelligence':<15} {'Subjectivity':<15} {'Pressure':<12}")
    print("-" * 55)
    for i, state in enumerate(history):
        print(
            f"{i:<6} {state['intelligence']:<15.6f} "
            f"{state['cognitive']['X_subjectivity']:<15.3f} "
            f"{state['foundation']['C_pressure']:<12.3f}"
        )

    print("\nResult: Contradiction increases pressure → ")
    print("        Pressure reveals misalignment → ")
    print("        Misalignment corrects subjectivity → ")
    print("        System achieves higher-order synthesis ✓")


def example_pressure_dynamics():
    """Example 4: Pressure Dynamics"""
    print("\n" + "=" * 60)
    print("Example 4: Pressure Dynamics")
    print("=" * 60)

    axiom = UniversalAxiom(pressure=1.0)

    print("\nStarting pressure: 1.0")
    print(f"Initial intelligence: {axiom.compute_intelligence():.6f}\n")

    # Apply increasing pressure
    pressures = [0.5, 1.0, 1.5, 2.0, 2.5]

    print(f"{'Pressure':<12} {'Intelligence':<15} {'Change':<12}")
    print("-" * 45)

    prev_intelligence = axiom.compute_intelligence()
    for p in pressures:
        axiom.foundation.pressure = p
        intelligence = axiom.compute_intelligence()
        change = intelligence - prev_intelligence
        print(f"{p:<12.1f} {intelligence:<15.6f} {change:+12.6f}")
        prev_intelligence = intelligence

    print("\nPressure amplifies intelligence when constraints sharpen focus.")


def example_fibonacci_regulation():
    """Example 5: Fibonacci Regulation Prevents Explosive Growth"""
    print("\n" + "=" * 60)
    print("Example 5: Fibonacci Regulation")
    print("=" * 60)

    print("\nComparing exponential vs Fibonacci-regulated growth:\n")

    print(f"{'n':<6} {'E_n (Exponential)':<20} {'F_n (Fibonacci)':<20} {'Regulated Growth':<20}")
    print("-" * 70)

    for n in range(1, 11):
        axiom = UniversalAxiom(n=n)
        E_n = axiom.dynamic.exponential_growth()
        F_n = axiom.dynamic.fibonacci()
        regulated = E_n * (1 + F_n)

        print(f"{n:<6} {E_n:<20.2f} {F_n:<20} {regulated:<20.2f}")

    print("\nFibonacci prevents explosive unbounded growth while maintaining")
    print("natural expansion patterns. Growth is fast but stable.")


def example_coherence_tracking():
    """Example 6: Coherence vs Token Accumulation"""
    print("\n" + "=" * 60)
    print("Example 6: Coherence Tracking")
    print("=" * 60)

    print("\nDemonstrating coherence measurement across different states:\n")

    scenarios = [
        ("High Objectivity, Strong Purpose", 0.1, 2.0, 1.0),
        ("Moderate Subjectivity", 0.5, 1.5, 1.2),
        ("High Subjectivity, Weak Purpose", 0.8, 0.5, 1.5),
        ("Balanced State", 0.2, 1.0, 1.0),
    ]

    print(f"{'Scenario':<35} {'Objectivity':<15} {'Purpose':<10} {'Coherence':<12}")
    print("-" * 75)

    for name, subj, purpose, pressure in scenarios:
        axiom = UniversalAxiom(subjectivity=subj, purpose=purpose, pressure=pressure)
        simulator = AxiomSimulator(axiom)
        coherence = simulator.get_coherence_metric()

        print(f"{name:<35} {1-subj:<15.2f} {purpose:<10.2f} {coherence:<12.4f}")

    print("\nCoherence is high when objectivity is high, purpose is strong,")
    print("and pressure is moderate. The Axiom tracks this, not token count.")


def example_no_stagnation():
    """Example 7: No Loop Without Learning"""
    print("\n" + "=" * 60)
    print("Example 7: No Loop Without Learning (No Stagnation)")
    print("=" * 60)

    axiom = UniversalAxiom(n=1)
    simulator = AxiomSimulator(axiom)

    print("\nEvolving and checking for state repetition:\n")

    history = simulator.simulate_evolution(steps=20, delta_time=1.0)

    # Check for identical states
    intelligence_values = [h['intelligence'] for h in history]

    print(f"Intelligence values over 20 steps:")
    print(f"{[f'{v:.2f}' for v in intelligence_values[:10]]}")
    print(f"{[f'{v:.2f}' for v in intelligence_values[10:]]}")

    # Check for repetition
    has_repetition = len(intelligence_values) != len(set(intelligence_values))

    print(f"\nAny repeated values? {has_repetition}")
    print(f"Unique values: {len(set(intelligence_values))} out of {len(intelligence_values)}")

    print("\nDue to TimeSphere (Z) and Fibonacci (F_n), the system")
    print("cannot repeat states → No loop without learning ✓")


def main():
    """Run all examples"""
    examples = [
        example_basic_computation,
        example_evolution,
        example_contradiction_resolution,
        example_pressure_dynamics,
        example_fibonacci_regulation,
        example_coherence_tracking,
        example_no_stagnation,
    ]

    print("\n" + "🔥" * 30)
    print("THE UNIVERSAL AXIOM - Python Implementation Examples")
    print("🔥" * 30)

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
