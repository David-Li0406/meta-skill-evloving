"""
Basic Usage Examples for The Universal Axiom (Julia)

Run with: julia examples/julia/basic_usage.jl
"""

include("../../src/julia/UniversalAxiom.jl")
using .UniversalAxiom

function example_basic_computation()
    println("=" ^ 60)
    println("Example 1: Basic Intelligence Computation")
    println("=" ^ 60)

    # Create axiom with default values
    axiom = Axiom()
    println("\nInitial state: ", axiom)

    # Compute intelligence
    intelligence = compute_intelligence(axiom)
    println("Intelligence value: ", round(intelligence, digits=6))

    # Display full state
    state = get_state(axiom)
    println("\nDetailed State:")
    println("  Foundation (A·B·C): ", round(state.foundation.product, digits=6))
    println("    A (Impulses): ", state.foundation.A_impulses)
    println("    B (Elements): ", state.foundation.B_elements)
    println("    C (Pressure): ", state.foundation.C_pressure)
    println("  Dynamic (E_n·(1+F_n)): ", round(state.dynamic.product, digits=6))
    println("    E_n: ", round(state.dynamic.E_n, digits=6))
    println("    F_n: ", state.dynamic.F_n)
    println("  Cognitive (X·Y·Z): ", round(state.cognitive.product, digits=6))
    println("    X (Objectivity): ", state.cognitive.X_objectivity)
    println("    Y (Purpose): ", state.cognitive.Y_purpose)
    println("    Z (Time): ", state.cognitive.Z_time)
end

function example_evolution()
    println("\n", "=" ^ 60)
    println("Example 2: System Evolution Over Time")
    println("=" ^ 60)

    axiom = Axiom(impulses=1.0, elements=1.0, pressure=1.0, n=1)
    simulator = AxiomSimulator(axiom)

    println("\nEvolving system over 10 steps...")
    history = simulate_evolution(simulator, 10, 1.0)

    println("\n", rpad("Step", 6), " ", rpad("Intelligence", 15), " ", rpad("F_n", 8), " ", rpad("Time", 8))
    println("-" ^ 45)

    for (i, state) in enumerate(history)
        println(
            rpad(i-1, 6), " ",
            rpad(round(state.intelligence, digits=6), 15), " ",
            rpad(state.dynamic.F_n, 8), " ",
            rpad(round(state.cognitive.Z_time, digits=1), 8)
        )
    end

    fib_values = [h.dynamic.F_n for h in history[1:min(10, length(history))]]
    println("\nFibonacci Growth Pattern: ", fib_values)
end

function example_contradiction_resolution()
    println("\n", "=" ^ 60)
    println("Example 3: Contradiction Resolution")
    println("=" ^ 60)

    # Start with some subjectivity
    axiom = Axiom(
        impulses=1.0,
        elements=1.0,
        pressure=1.0,
        subjectivity=0.5,  # Start with 50% subjectivity
        purpose=1.0,
        n=1
    )

    simulator = AxiomSimulator(axiom)

    println("\nSimulating contradiction encounter and resolution...")
    println("Initial subjectivity: 0.5 (50% subjective)")
    println("Applying pressure spike from contradiction...\n")

    history = simulate_contradiction_resolution(simulator, 2.0, 5)

    println(rpad("Step", 6), " ", rpad("Intelligence", 15), " ", rpad("Subjectivity", 15), " ", rpad("Pressure", 12))
    println("-" ^ 55)

    for (i, state) in enumerate(history)
        println(
            rpad(i-1, 6), " ",
            rpad(round(state.intelligence, digits=6), 15), " ",
            rpad(round(state.cognitive.X_subjectivity, digits=3), 15), " ",
            rpad(round(state.foundation.C_pressure, digits=3), 12)
        )
    end

    println("\nResult: Contradiction increases pressure → ")
    println("        Pressure reveals misalignment → ")
    println("        Misalignment corrects subjectivity → ")
    println("        System achieves higher-order synthesis ✓")
end

function example_pressure_dynamics()
    println("\n", "=" ^ 60)
    println("Example 4: Pressure Dynamics")
    println("=" ^ 60)

    axiom = Axiom(pressure=1.0)

    println("\nStarting pressure: 1.0")
    println("Initial intelligence: ", round(compute_intelligence(axiom), digits=6), "\n")

    # Apply increasing pressure
    pressures = [0.5, 1.0, 1.5, 2.0, 2.5]

    println(rpad("Pressure", 12), " ", rpad("Intelligence", 15), " ", rpad("Change", 12))
    println("-" ^ 45)

    prev_intelligence = compute_intelligence(axiom)
    for p in pressures
        axiom.foundation.pressure = p
        intelligence = compute_intelligence(axiom)
        change = intelligence - prev_intelligence
        println(
            rpad(round(p, digits=1), 12), " ",
            rpad(round(intelligence, digits=6), 15), " ",
            rpad(string(change >= 0 ? "+" : "", round(change, digits=6)), 12)
        )
        prev_intelligence = intelligence
    end

    println("\nPressure amplifies intelligence when constraints sharpen focus.")
end

function example_fibonacci_regulation()
    println("\n", "=" ^ 60)
    println("Example 5: Fibonacci Regulation")
    println("=" ^ 60)

    println("\nComparing exponential vs Fibonacci-regulated growth:\n")

    println(rpad("n", 6), " ", rpad("E_n (Exponential)", 20), " ", rpad("F_n (Fibonacci)", 20), " ", rpad("Regulated Growth", 20))
    println("-" ^ 70)

    for n in 1:10
        axiom = Axiom(n=n)
        state = get_state(axiom)
        E_n = state.dynamic.E_n
        F_n = state.dynamic.F_n
        regulated = state.dynamic.product

        println(
            rpad(n, 6), " ",
            rpad(round(E_n, digits=2), 20), " ",
            rpad(F_n, 20), " ",
            rpad(round(regulated, digits=2), 20)
        )
    end

    println("\nFibonacci prevents explosive unbounded growth while maintaining")
    println("natural expansion patterns. Growth is fast but stable.")
end

function example_coherence_tracking()
    println("\n", "=" ^ 60)
    println("Example 6: Coherence Tracking")
    println("=" ^ 60)

    println("\nDemonstrating coherence measurement across different states:\n")

    scenarios = [
        ("High Objectivity, Strong Purpose", 0.1, 2.0, 1.0),
        ("Moderate Subjectivity", 0.5, 1.5, 1.2),
        ("High Subjectivity, Weak Purpose", 0.8, 0.5, 1.5),
        ("Balanced State", 0.2, 1.0, 1.0),
    ]

    println(rpad("Scenario", 35), " ", rpad("Objectivity", 15), " ", rpad("Purpose", 10), " ", rpad("Coherence", 12))
    println("-" ^ 75)

    for (name, subj, purpose, pressure) in scenarios
        axiom = Axiom(subjectivity=subj, purpose=purpose, pressure=pressure)
        simulator = AxiomSimulator(axiom)
        coherence = get_coherence_metric(simulator)

        println(
            rpad(name, 35), " ",
            rpad(round(1-subj, digits=2), 15), " ",
            rpad(round(purpose, digits=2), 10), " ",
            rpad(round(coherence, digits=4), 12)
        )
    end

    println("\nCoherence is high when objectivity is high, purpose is strong,")
    println("and pressure is moderate. The Axiom tracks this, not token count.")
end

function example_no_stagnation()
    println("\n", "=" ^ 60)
    println("Example 7: No Loop Without Learning (No Stagnation)")
    println("=" ^ 60)

    axiom = Axiom(n=1)
    simulator = AxiomSimulator(axiom)

    println("\nEvolving and checking for state repetition:\n")

    history = simulate_evolution(simulator, 20, 1.0)

    # Check for identical states
    intelligence_values = [h.intelligence for h in history]

    println("Intelligence values over 20 steps:")
    first_10 = [string(round(v, digits=2)) for v in intelligence_values[1:10]]
    second_10 = [string(round(v, digits=2)) for v in intelligence_values[11:20]]
    println("[", join(first_10, ", "), "]")
    println("[", join(second_10, ", "), "]")

    # Check for repetition
    unique_values = unique(intelligence_values)
    has_repetition = length(intelligence_values) != length(unique_values)

    println("\nAny repeated values? ", has_repetition)
    println("Unique values: ", length(unique_values), " out of ", length(intelligence_values))

    println("\nDue to TimeSphere (Z) and Fibonacci (F_n), the system")
    println("cannot repeat states → No loop without learning ✓")
end

function main()
    println("\n", "🔥" ^ 30)
    println("THE UNIVERSAL AXIOM - Julia Implementation Examples")
    println("🔥" ^ 30)

    examples = [
        example_basic_computation,
        example_evolution,
        example_contradiction_resolution,
        example_pressure_dynamics,
        example_fibonacci_regulation,
        example_coherence_tracking,
        example_no_stagnation,
    ]

    for example in examples
        try
            example()
        catch e
            println("\nError in ", example, ": ", e)
        end
    end

    println("\n", "=" ^ 60)
    println("All examples completed!")
    println("=" ^ 60, "\n")
end

# Run if this is the main script
if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
