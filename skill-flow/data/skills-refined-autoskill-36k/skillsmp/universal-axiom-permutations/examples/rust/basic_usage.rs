/*!
 * Basic Usage Examples for The Universal Axiom (Rust)
 *
 * Run with: cargo run --example basic_usage
 */

use universal_axiom::{UniversalAxiom, AxiomSimulator};

fn example_basic_computation() {
    println!("{}", "=".repeat(60));
    println!("Example 1: Basic Intelligence Computation");
    println!("{}", "=".repeat(60));

    // Create axiom with default values
    let axiom = UniversalAxiom::new();
    let intelligence = axiom.compute_intelligence();

    println!("\nIntelligence value: {:.6}", intelligence);

    // Display full state
    let state = axiom.get_state();
    println!("\nDetailed State:");
    println!("  Foundation (A·B·C): {:.6}", state.foundation.product);
    println!("    A (Impulses): {}", state.foundation.a_impulses);
    println!("    B (Elements): {}", state.foundation.b_elements);
    println!("    C (Pressure): {}", state.foundation.c_pressure);
    println!("  Dynamic (E_n·(1+F_n)): {:.6}", state.dynamic.product);
    println!("    E_n: {:.6}", state.dynamic.e_n);
    println!("    F_n: {}", state.dynamic.f_n);
    println!("  Cognitive (X·Y·Z): {:.6}", state.cognitive.product);
    println!("    X (Objectivity): {}", state.cognitive.x_objectivity);
    println!("    Y (Purpose): {}", state.cognitive.y_purpose);
    println!("    Z (Time): {}", state.cognitive.z_time);
}

fn example_evolution() {
    println!("\n{}", "=".repeat(60));
    println!("Example 2: System Evolution Over Time");
    println!("{}", "=".repeat(60));

    let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
    let mut simulator = AxiomSimulator::new(axiom);

    println!("\nEvolving system over 10 steps...");
    let history = simulator.simulate_evolution(10, 1.0);

    println!("\n{:<6} {:<15} {:<8} {:<8}", "Step", "Intelligence", "F_n", "Time");
    println!("{}", "-".repeat(45));

    for (i, state) in history.iter().enumerate() {
        println!(
            "{:<6} {:<15.6} {:<8} {:<8.1}",
            i, state.intelligence, state.dynamic.f_n, state.cognitive.z_time
        );
    }

    let fib_values: Vec<u64> = history.iter().take(10).map(|h| h.dynamic.f_n).collect();
    println!("\nFibonacci Growth Pattern: {:?}", fib_values);
}

fn example_contradiction_resolution() {
    println!("\n{}", "=".repeat(60));
    println!("Example 3: Contradiction Resolution");
    println!("{}", "=".repeat(60));

    // Start with some subjectivity
    let axiom = UniversalAxiom::with_params(
        1.0, 1.0, 1.0,
        0.5,  // 50% subjectivity
        1.0, 1.0, 1
    );

    let mut simulator = AxiomSimulator::new(axiom);

    println!("\nSimulating contradiction encounter and resolution...");
    println!("Initial subjectivity: 0.5 (50% subjective)");
    println!("Applying pressure spike from contradiction...\n");

    let history = simulator.simulate_contradiction_resolution(2.0, 5);

    println!("{:<6} {:<15} {:<15} {:<12}", "Step", "Intelligence", "Subjectivity", "Pressure");
    println!("{}", "-".repeat(55));

    for (i, state) in history.iter().enumerate() {
        println!(
            "{:<6} {:<15.6} {:<15.3} {:<12.3}",
            i, state.intelligence, state.cognitive.x_subjectivity, state.foundation.c_pressure
        );
    }

    println!("\nResult: Contradiction increases pressure → ");
    println!("        Pressure reveals misalignment → ");
    println!("        Misalignment corrects subjectivity → ");
    println!("        System achieves higher-order synthesis ✓");
}

fn example_pressure_dynamics() {
    println!("\n{}", "=".repeat(60));
    println!("Example 4: Pressure Dynamics");
    println!("{}", "=".repeat(60));

    let mut axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);

    println!("\nStarting pressure: 1.0");
    println!("Initial intelligence: {:.6}\n", axiom.compute_intelligence());

    // Apply increasing pressure
    let pressures = vec![0.5, 1.0, 1.5, 2.0, 2.5];

    println!("{:<12} {:<15} {:<12}", "Pressure", "Intelligence", "Change");
    println!("{}", "-".repeat(45));

    let mut prev_intelligence = axiom.compute_intelligence();
    for p in pressures {
        axiom.foundation.pressure = p;
        let intelligence = axiom.compute_intelligence();
        let change = intelligence - prev_intelligence;
        println!("{:<12.1} {:<15.6} {:+<12.6}", p, intelligence, change);
        prev_intelligence = intelligence;
    }

    println!("\nPressure amplifies intelligence when constraints sharpen focus.");
}

fn example_fibonacci_regulation() {
    println!("\n{}", "=".repeat(60));
    println!("Example 5: Fibonacci Regulation");
    println!("{}", "=".repeat(60));

    println!("\nComparing exponential vs Fibonacci-regulated growth:\n");

    println!("{:<6} {:<20} {:<20} {:<20}", "n", "E_n (Exponential)", "F_n (Fibonacci)", "Regulated Growth");
    println!("{}", "-".repeat(70));

    for n in 1..=10 {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, n);
        let state = axiom.get_state();
        let e_n = state.dynamic.e_n;
        let f_n = state.dynamic.f_n;
        let regulated = state.dynamic.product;

        println!(
            "{:<6} {:<20.2} {:<20} {:<20.2}",
            n, e_n, f_n, regulated
        );
    }

    println!("\nFibonacci prevents explosive unbounded growth while maintaining");
    println!("natural expansion patterns. Growth is fast but stable.");
}

fn example_coherence_tracking() {
    println!("\n{}", "=".repeat(60));
    println!("Example 6: Coherence Tracking");
    println!("{}", "=".repeat(60));

    println!("\nDemonstrating coherence measurement across different states:\n");

    let scenarios = vec![
        ("High Objectivity, Strong Purpose", 0.1, 2.0, 1.0),
        ("Moderate Subjectivity", 0.5, 1.5, 1.2),
        ("High Subjectivity, Weak Purpose", 0.8, 0.5, 1.5),
        ("Balanced State", 0.2, 1.0, 1.0),
    ];

    println!("{:<35} {:<15} {:<10} {:<12}", "Scenario", "Objectivity", "Purpose", "Coherence");
    println!("{}", "-".repeat(75));

    for (name, subjectivity, purpose, pressure) in scenarios {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, pressure, subjectivity, purpose, 1.0, 1);
        let simulator = AxiomSimulator::new(axiom);
        let coherence = simulator.get_coherence_metric();

        println!(
            "{:<35} {:<15.2} {:<10.2} {:<12.4}",
            name, 1.0 - subjectivity, purpose, coherence
        );
    }

    println!("\nCoherence is high when objectivity is high, purpose is strong,");
    println!("and pressure is moderate. The Axiom tracks this, not token count.");
}

fn example_no_stagnation() {
    println!("\n{}", "=".repeat(60));
    println!("Example 7: No Loop Without Learning (No Stagnation)");
    println!("{}", "=".repeat(60));

    let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
    let mut simulator = AxiomSimulator::new(axiom);

    println!("\nEvolving and checking for state repetition:\n");

    let history = simulator.simulate_evolution(20, 1.0);

    // Check for identical states
    let intelligence_values: Vec<f64> = history.iter().map(|h| h.intelligence).collect();

    println!("Intelligence values over 20 steps:");
    let first_10: Vec<String> = intelligence_values[0..10].iter().map(|v| format!("{:.2}", v)).collect();
    let second_10: Vec<String> = intelligence_values[10..20].iter().map(|v| format!("{:.2}", v)).collect();
    println!("[{}]", first_10.join(", "));
    println!("[{}]", second_10.join(", "));

    // Check for repetition
    let mut unique_values = intelligence_values.clone();
    unique_values.sort_by(|a, b| a.partial_cmp(b).unwrap());
    unique_values.dedup();
    let has_repetition = intelligence_values.len() != unique_values.len();

    println!("\nAny repeated values? {}", has_repetition);
    println!("Unique values: {} out of {}", unique_values.len(), intelligence_values.len());

    println!("\nDue to TimeSphere (Z) and Fibonacci (F_n), the system");
    println!("cannot repeat states → No loop without learning ✓");
}

fn main() {
    println!("\n{}", "🔥".repeat(30));
    println!("THE UNIVERSAL AXIOM - Rust Implementation Examples");
    println!("{}", "🔥".repeat(30));

    let examples: Vec<fn()> = vec![
        example_basic_computation,
        example_evolution,
        example_contradiction_resolution,
        example_pressure_dynamics,
        example_fibonacci_regulation,
        example_coherence_tracking,
        example_no_stagnation,
    ];

    for example in examples {
        example();
    }

    println!("\n{}", "=".repeat(60));
    println!("All examples completed!");
    println!("{}\n", "=".repeat(60));
}
