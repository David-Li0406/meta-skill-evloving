/*!
 * The Universal Axiom - Core Implementation (Rust)
 *
 * Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
 *
 * Foundation Layer: Impulses (A), Elements (B), Pressure (C)
 * Dynamic Layer: Exponential Growth (E_n), Fibonacci Sequence (F_n)
 * Cognitive Layer: Subjectivity Scale (X), Why Axis (Y), TimeSphere (Z)
 */

use serde::{Deserialize, Serialize};

/// Foundation Layer: A · B · C
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FoundationLayer {
    /// A - Fundamental drives
    pub impulses: f64,
    /// B - Core components
    pub elements: f64,
    /// C - Constraints and forces
    pub pressure: f64,
}

impl FoundationLayer {
    pub fn new(impulses: f64, elements: f64, pressure: f64) -> Self {
        Self {
            impulses,
            elements,
            pressure,
        }
    }

    pub fn compute(&self) -> f64 {
        self.impulses * self.elements * self.pressure
    }
}

/// Dynamic Layer: E_n · (1 + F_n)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DynamicLayer {
    /// Current iteration/step
    pub n: usize,
}

impl DynamicLayer {
    pub fn new(n: usize) -> Self {
        Self {
            n,
        }
    }

    /// Exponential growth: E_n = 2 * 3^n - 1
    pub fn exponential_growth(&self) -> f64 {
        2.0 * 3.0_f64.powi(self.n as i32) - 1.0
    }

    /// Fibonacci sequence: F(1)=1, F(2)=2, F(3)=3, F(4)=5, F(5)=8, ...
    /// (Shifted Fibonacci starting from 1, 2 instead of 0, 1)
    pub fn fibonacci(&self) -> u64 {
        if self.n <= 1 {
            return 1;
        }

        let mut a = 1u64;
        let mut b = 1u64;

        for _ in 2..=self.n {
            let temp = a + b;
            a = b;
            b = temp;
        }

        b
    }

    pub fn compute(&self) -> f64 {
        let e_n = self.exponential_growth();
        let f_n = self.fibonacci() as f64;
        e_n * (1.0 + f_n)
    }
}

/// Cognitive Layer: X · Y · Z
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CognitiveLayer {
    /// X - Subjectivity level (0 = objective, 1 = subjective)
    pub subjectivity: f64,
    /// Y - Purpose-driven reasoning strength
    pub purpose: f64,
    /// Z - Temporal continuity and irreversibility
    pub time: f64,
}

impl CognitiveLayer {
    pub fn new(subjectivity: f64, purpose: f64, time: f64) -> Self {
        Self {
            subjectivity,
            purpose,
            time,
        }
    }

    pub fn compute(&self) -> f64 {
        // X represents objectivity: (1 - subjectivity)
        let objectivity = 1.0 - self.subjectivity;
        objectivity * self.purpose * self.time
    }

    pub fn objectivity(&self) -> f64 {
        1.0 - self.subjectivity
    }
}

/// Complete state of the Universal Axiom
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AxiomState {
    pub n: usize,
    pub foundation: FoundationState,
    pub dynamic: DynamicState,
    pub cognitive: CognitiveState,
    pub intelligence: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FoundationState {
    pub a_impulses: f64,
    pub b_elements: f64,
    pub c_pressure: f64,
    pub product: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DynamicState {
    pub e_n: f64,
    pub f_n: u64,
    pub product: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CognitiveState {
    pub x_subjectivity: f64,
    pub x_objectivity: f64,
    pub y_purpose: f64,
    pub z_time: f64,
    pub product: f64,
}

/// The Universal Axiom - Complete Intelligence Model
///
/// Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
#[derive(Debug, Clone)]
pub struct UniversalAxiom {
    pub foundation: FoundationLayer,
    pub dynamic: DynamicLayer,
    pub cognitive: CognitiveLayer,
    pub n: usize,
}

impl UniversalAxiom {
    pub fn new() -> Self {
        Self::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1)
    }

    pub fn with_params(
        impulses: f64,
        elements: f64,
        pressure: f64,
        subjectivity: f64,
        purpose: f64,
        time: f64,
        n: usize,
    ) -> Self {
        Self {
            foundation: FoundationLayer::new(impulses, elements, pressure),
            dynamic: DynamicLayer::new(n),
            cognitive: CognitiveLayer::new(subjectivity, purpose, time),
            n,
        }
    }

    /// Compute Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
    pub fn compute_intelligence(&self) -> f64 {
        let foundation_value = self.foundation.compute();
        let dynamic_value = self.dynamic.compute();
        let cognitive_value = self.cognitive.compute();

        dynamic_value * cognitive_value * foundation_value
    }

    /// Evolve the system forward in time
    pub fn evolve(&mut self, delta_time: f64) -> f64 {
        self.n += 1;
        self.dynamic.n = self.n;
        self.cognitive.time += delta_time;

        self.compute_intelligence()
    }

    /// Apply pressure change (e.g., from contradictions or constraints)
    pub fn apply_pressure(&mut self, pressure_delta: f64) -> f64 {
        self.foundation.pressure += pressure_delta;
        // Ensure pressure stays positive
        self.foundation.pressure = self.foundation.pressure.max(0.01);

        self.compute_intelligence()
    }

    /// Adjust subjectivity level (moving toward objectivity or away)
    pub fn adjust_subjectivity(&mut self, subjectivity_delta: f64) -> f64 {
        self.cognitive.subjectivity += subjectivity_delta;
        // Clamp between 0 and 1
        self.cognitive.subjectivity = self.cognitive.subjectivity.clamp(0.0, 1.0);

        self.compute_intelligence()
    }

    /// Strengthen or weaken purpose alignment
    pub fn strengthen_purpose(&mut self, purpose_multiplier: f64) -> f64 {
        self.cognitive.purpose *= purpose_multiplier;
        self.cognitive.purpose = self.cognitive.purpose.max(0.01);

        self.compute_intelligence()
    }

    /// Get current state of all variables
    pub fn get_state(&self) -> AxiomState {
        AxiomState {
            n: self.n,
            foundation: FoundationState {
                a_impulses: self.foundation.impulses,
                b_elements: self.foundation.elements,
                c_pressure: self.foundation.pressure,
                product: self.foundation.compute(),
            },
            dynamic: DynamicState {
                e_n: self.dynamic.exponential_growth(),
                f_n: self.dynamic.fibonacci(),
                product: self.dynamic.compute(),
            },
            cognitive: CognitiveState {
                x_subjectivity: self.cognitive.subjectivity,
                x_objectivity: self.cognitive.objectivity(),
                y_purpose: self.cognitive.purpose,
                z_time: self.cognitive.time,
                product: self.cognitive.compute(),
            },
            intelligence: self.compute_intelligence(),
        }
    }
}

impl Default for UniversalAxiom {
    fn default() -> Self {
        Self::new()
    }
}

/// Simulator for running Universal Axiom scenarios
pub struct AxiomSimulator {
    axiom: UniversalAxiom,
    history: Vec<AxiomState>,
}

impl AxiomSimulator {
    pub fn new(axiom: UniversalAxiom) -> Self {
        Self {
            axiom,
            history: Vec::new(),
        }
    }

    pub fn record_state(&mut self) {
        self.history.push(self.axiom.get_state());
    }

    /// Simulate evolution over multiple time steps
    pub fn simulate_evolution(&mut self, steps: usize, delta_time: f64) -> &Vec<AxiomState> {
        self.history.clear();
        self.record_state();

        for _ in 0..steps {
            self.axiom.evolve(delta_time);
            self.record_state();
        }

        &self.history
    }

    /// Simulate how the system handles contradiction
    pub fn simulate_contradiction_resolution(
        &mut self,
        initial_pressure: f64,
        resolution_steps: usize,
    ) -> &Vec<AxiomState> {
        self.history.clear();
        self.record_state();

        // Apply initial pressure spike
        self.axiom.apply_pressure(initial_pressure);
        self.record_state();

        // Gradually resolve through objectivity adjustment and pressure release
        for _ in 0..resolution_steps {
            // Reduce subjectivity (increase objectivity)
            self.axiom.adjust_subjectivity(-0.1);

            // Release pressure as understanding increases
            let pressure_release = -initial_pressure / resolution_steps as f64;
            self.axiom.apply_pressure(pressure_release);

            // Evolve forward
            self.axiom.evolve(1.0);
            self.record_state();
        }

        &self.history
    }

    /// Calculate coherence metric based on balance of components
    pub fn get_coherence_metric(&self) -> f64 {
        let state = self.axiom.get_state();

        let objectivity_score = state.cognitive.x_objectivity;
        let purpose_score = (state.cognitive.y_purpose / 2.0).min(1.0);
        let pressure_score = 1.0 / (1.0 + (state.foundation.c_pressure - 1.0).abs());

        (objectivity_score + purpose_score + pressure_score) / 3.0
    }

    pub fn get_history(&self) -> &Vec<AxiomState> {
        &self.history
    }
}

/// Generate Fibonacci sequence up to n terms
/// Generate a Fibonacci sequence of length n
/// Returns the first n terms: [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ...]
pub fn fibonacci_sequence(n: usize) -> Vec<u64> {
    if n == 0 {
        return vec![];
    }
    if n == 1 {
        return vec![1];
    }

    let mut sequence = vec![1, 1];
    for i in 2..n {
        sequence.push(sequence[i - 1] + sequence[i - 2]);
    }

    sequence
}

/// A proof step annotated with an axiom-aligned insight.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProofStep {
    pub statement: String,
    pub axiom_insight: String,
}

impl ProofStep {
    pub fn new(statement: impl Into<String>, axiom_insight: impl Into<String>) -> Self {
        Self {
            statement: statement.into(),
            axiom_insight: axiom_insight.into(),
        }
    }
}

/// Container for an Erdos problem and its axiom-aligned proof steps.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ErdosProblem {
    pub identifier: String,
    pub title: String,
    pub statement: String,
    pub status: String,
    pub axiom_insight: String,
    pub proof_steps: Vec<ProofStep>,
}

impl ErdosProblem {
    pub fn new(
        identifier: impl Into<String>,
        title: impl Into<String>,
        statement: impl Into<String>,
        status: impl Into<String>,
        axiom_insight: impl Into<String>,
    ) -> Self {
        Self {
            identifier: identifier.into(),
            title: title.into(),
            statement: statement.into(),
            status: status.into(),
            axiom_insight: axiom_insight.into(),
            proof_steps: Vec::new(),
        }
    }

    pub fn add_proof_step(&mut self, statement: impl Into<String>, axiom_insight: impl Into<String>) {
        self.proof_steps
            .push(ProofStep::new(statement, axiom_insight));
    }

    pub fn add_proof_steps(&mut self, steps: Vec<ProofStep>) {
        self.proof_steps.extend(steps);
    }
}

/// Registry for mathematical problems and axiom-aligned proof steps.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MathSolutions {
    pub problems: Vec<ErdosProblem>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProblemSummary {
    pub identifier: String,
    pub title: String,
    pub status: String,
}

impl MathSolutions {
    pub fn new() -> Self {
        Self {
            problems: Vec::new(),
        }
    }

    pub fn erdos_seed() -> Self {
        Self {
            problems: seed_erdos_problems(),
        }
    }

    pub fn add_problem(&mut self, problem: ErdosProblem) {
        if let Some(existing) = self
            .problems
            .iter_mut()
            .find(|item| item.identifier == problem.identifier)
        {
            *existing = problem;
        } else {
            self.problems.push(problem);
        }
    }

    pub fn get_problem(&self, identifier: &str) -> Option<&ErdosProblem> {
        self.problems
            .iter()
            .find(|problem| problem.identifier == identifier)
    }

    pub fn get_problem_mut(&mut self, identifier: &str) -> Option<&mut ErdosProblem> {
        self.problems
            .iter_mut()
            .find(|problem| problem.identifier == identifier)
    }

    pub fn list_problems(&self) -> &Vec<ErdosProblem> {
        &self.problems
    }

    pub fn summaries(&self) -> Vec<ProblemSummary> {
        self.problems
            .iter()
            .map(|problem| ProblemSummary {
                identifier: problem.identifier.clone(),
                title: problem.title.clone(),
                status: problem.status.clone(),
            })
            .collect()
    }

    pub fn add_proof_step(
        &mut self,
        identifier: &str,
        statement: impl Into<String>,
        axiom_insight: impl Into<String>,
    ) -> Result<(), String> {
        match self.get_problem_mut(identifier) {
            Some(problem) => {
                problem.add_proof_step(statement, axiom_insight);
                Ok(())
            }
            None => Err(format!("Unknown problem identifier: {identifier}")),
        }
    }
}

fn seed_erdos_problems() -> Vec<ErdosProblem> {
    let mut erdos_straus = ErdosProblem::new(
        "erdos-straus",
        "Erdos–Straus Conjecture",
        "For every integer n ≥ 2, the rational 4/n can be expressed as the sum of three unit fractions: 4/n = 1/x + 1/y + 1/z for integers x, y, z.",
        "open",
        "The axiom highlights how constraints (C) and growth (E_n, F_n) interact, suggesting structured pathways to decompositions.",
    );
    erdos_straus.add_proof_steps(vec![
        ProofStep::new(
            "Clear denominators to obtain 4xyz = n(xy + xz + yz), exposing the shared ABC constraint.",
            "A·B·C locks the reciprocal structure while C records divisibility pressure.",
        ),
        ProofStep::new(
            "Partition n into congruence classes to target families where n divides xy + xz + yz.",
            "F_n periodicity mirrors modular cycles, guiding repeatable constructions.",
        ),
        ProofStep::new(
            "Introduce parameterized families for (x, y, z) that satisfy the cleared equation.",
            "E_n growth supplies expansion room; X and Y keep selections coherent.",
        ),
        ProofStep::new(
            "Balance denominator growth so x, y, z remain positive and ordered, avoiding runaway residues.",
            "E_n expands search while F_n regulates magnitude.",
        ),
        ProofStep::new(
            "Cover dense residue families and reduce remaining cases to bounded verification windows.",
            "Z enforces temporal continuity; remaining gaps collapse to finite checks.",
        ),
    ]);

    let mut erdos_distinct = ErdosProblem::new(
        "erdos-distinct-distances",
        "Erdos Distinct Distances Problem",
        "Determine the minimum number of distinct distances defined by n points in the plane.",
        "solved",
        "Balancing combinatorial growth (E_n) with structural regulation (F_n) mirrors the tension between point density and distance diversity.",
    );
    erdos_distinct.add_proof_steps(vec![
        ProofStep::new(
            "Normalize the configuration by translation and scaling to fix baseline spacing.",
            "X, Y, Z align perspective and time scale before counting.",
        ),
        ProofStep::new(
            "Count point pairs to relate total pairs to distance multiplicities.",
            "E_n captures pair growth while F_n regulates clustering.",
        ),
        ProofStep::new(
            "Apply incidence bounds to limit how often a distance can repeat.",
            "C pressure caps over-concentration in any single distance.",
        ),
        ProofStep::new(
            "Construct near-lattice configurations to achieve the lower-bound regime.",
            "A·B·C balances structure so growth matches regulation.",
        ),
        ProofStep::new(
            "Conclude the asymptotic bound by matching upper and lower envelopes.",
            "Dynamic layer (E_n, F_n) closes the gap between expansion and constraint.",
        ),
    ]);

    let mut erdos_moser = ErdosProblem::new(
        "erdos-moser",
        "Erdos–Moser Equation",
        "Solve 1^k + 2^k + ... + (m−1)^k = m^k for integers m, k > 1.",
        "partial",
        "E_n scaling intensifies quickly; the axiom suggests using Z to control temporal accumulation and detect singularities.",
    );
    erdos_moser.add_proof_steps(vec![
        ProofStep::new(
            "Compare the power sum to integral bounds to bracket growth of Σ i^k versus m^k.",
            "E_n sets exponential growth while Z tracks accumulation.",
        ),
        ProofStep::new(
            "Use modular restrictions on k and m to eliminate incompatible residues.",
            "C enforces arithmetic pressure, pruning impossible classes.",
        ),
        ProofStep::new(
            "Isolate the dominant term by normalizing with m^k and bounding the remainder.",
            "A·B·C stabilizes the foundation as X reduces variance.",
        ),
        ProofStep::new(
            "Show candidate solutions require extremely tight balance between consecutive powers.",
            "F_n smooths oscillations, exposing near-cancellation requirements.",
        ),
        ProofStep::new(
            "Reduce remaining candidates to finite computational windows for verification.",
            "Z keeps the search temporal and bounded; Y focuses viable regimes.",
        ),
    ]);

    let mut erdos_ko_rado = ErdosProblem::new(
        "erdos-ko-rado",
        "Erdos–Ko–Rado Theorem",
        "For n ≥ 2k, the largest intersecting family of k-subsets of {1, …, n} has size C(n−1, k−1).",
        "solved",
        "The axiom emphasizes how A·B·C stabilizes intersection structure while E_n regulates combinatorial growth.",
    );
    erdos_ko_rado.add_proof_steps(vec![
        ProofStep::new(
            "Fix a canonical element to anchor intersecting families.",
            "X and Y align perspective so all intersections share a core axis.",
        ),
        ProofStep::new(
            "Compare arbitrary families to a star family.",
            "A·B·C fixes the foundational overlap that dominates size.",
        ),
        ProofStep::new(
            "Apply compression/shifting to increase regularity.",
            "F_n-style regulation smooths irregularities into canonical form.",
        ),
        ProofStep::new(
            "Count surviving sets after compression.",
            "E_n tracks the combinatorial growth of the stabilized family.",
        ),
        ProofStep::new(
            "Characterize extremal cases.",
            "Z preserves continuity to conclude all maxima are stars.",
        ),
    ]);

    let mut erdos_szekeres = ErdosProblem::new(
        "erdos-szekeres",
        "Erdos–Szekeres Happy Ending Problem",
        "Determine the minimal N(n) such that any N(n) points in general position in the plane contain n points in convex position.",
        "partial",
        "E_n captures the rapid growth of point configurations, while F_n signals the combinatorial regulation that forces convex structure.",
    );
    erdos_szekeres.add_proof_steps(vec![
        ProofStep::new(
            "Encode points by convex/concave chains.",
            "A·B·C captures the foundational order relations among points.",
        ),
        ProofStep::new(
            "Apply Ramsey-type bounds to chain lengths.",
            "E_n provides the growth envelope for inevitable structure.",
        ),
        ProofStep::new(
            "Use monotone subsequence arguments.",
            "F_n smooths oscillations, aligning with ordered subsequences.",
        ),
        ProofStep::new(
            "Derive upper bounds via combinatorial recursion.",
            "Z tracks recursive depth while keeping the search bounded.",
        ),
        ProofStep::new(
            "Compare with lower-bound constructions.",
            "X and Y balance structural intent against extremal examples.",
        ),
    ]);

    let mut erdos_faber_lovasz = ErdosProblem::new(
        "erdos-faber-lovasz",
        "Erdos–Faber–Lovasz Conjecture",
        "Any linear hypergraph with n edges, each of size n, has chromatic number at most n.",
        "solved",
        "The axiom aligns color pressure (C) with combinatorial expansion (E_n) to cap chromatic growth.",
    );
    erdos_faber_lovasz.add_proof_steps(vec![
        ProofStep::new(
            "Translate hypergraph coloring to incidence structure.",
            "A·B·C locks vertex-edge intersections into a linear lattice.",
        ),
        ProofStep::new(
            "Apply probabilistic coloring bounds.",
            "E_n models expansion while X calibrates random selection.",
        ),
        ProofStep::new(
            "Refine via iterative nibble methods.",
            "F_n regulates the iterative removal of conflicts.",
        ),
        ProofStep::new(
            "Stabilize with absorbers for leftover vertices.",
            "Z preserves continuity as the coloring completes.",
        ),
        ProofStep::new(
            "Conclude chromatic cap at n.",
            "C pressure finalizes the bound with no overflow.",
        ),
    ]);

    let mut erdos_ginzburg_ziv = ErdosProblem::new(
        "erdos-ginzburg-ziv",
        "Erdos–Ginzburg–Ziv Theorem",
        "Any sequence of 2n−1 integers contains a subsequence of length n whose sum is divisible by n.",
        "solved",
        "The axiom’s regulation (F_n) governs modular accumulation, ensuring balanced subsequences emerge.",
    );
    erdos_ginzburg_ziv.add_proof_steps(vec![
        ProofStep::new(
            "Map integers to residues mod n.",
            "A·B·C frames modular pressure across the sequence.",
        ),
        ProofStep::new(
            "Apply zero-sum combinatorial lemmas.",
            "E_n scales the residue space to guarantee coverage.",
        ),
        ProofStep::new(
            "Use induction on n with residue partitioning.",
            "Z tracks recursion while preserving sequence continuity.",
        ),
        ProofStep::new(
            "Extract a length-n zero-sum subsequence.",
            "F_n balances residues to stabilize the sum at zero.",
        ),
        ProofStep::new(
            "Conclude optimal length 2n−1.",
            "X and Y confirm the bound is tight via extremal examples.",
        ),
    ]);

    let mut erdos_heilbronn = ErdosProblem::new(
        "erdos-heilbronn",
        "Erdos–Heilbronn Conjecture",
        "For a subset A of Z_p, the restricted sumset A ⊕ A = {a+b : a,b∈A, a≠b} has size at least min(p, 2|A|−3).",
        "solved",
        "The axiom links additive expansion (E_n) with pressure (C) to ensure growth in restricted sumsets.",
    );
    erdos_heilbronn.add_proof_steps(vec![
        ProofStep::new(
            "Embed the set in modular arithmetic.",
            "A·B·C stabilizes the modular structure and constraints.",
        ),
        ProofStep::new(
            "Apply polynomial method or combinatorial nullstellensatz.",
            "E_n captures the expansion of algebraic constraints.",
        ),
        ProofStep::new(
            "Control forbidden diagonal pairs.",
            "C pressure enforces the a≠b restriction without collapse.",
        ),
        ProofStep::new(
            "Compare with unrestricted sumsets.",
            "F_n regulates the difference between restricted and full sums.",
        ),
        ProofStep::new(
            "Conclude lower bound min(p, 2|A|−3).",
            "Z aligns the bound with finite-field continuity.",
        ),
    ]);

    let mut erdos_discrepancy = ErdosProblem::new(
        "erdos-discrepancy",
        "Erdos Discrepancy Problem",
        "For any ±1 sequence, show the discrepancy of homogeneous arithmetic progressions is unbounded.",
        "solved",
        "E_n amplifies oscillations while C enforces constraints, revealing that imbalance must eventually diverge.",
    );
    erdos_discrepancy.add_proof_steps(vec![
        ProofStep::new(
            "Model discrepancy via multiplicative sequences.",
            "A·B·C captures foundational constraints on sign patterns.",
        ),
        ProofStep::new(
            "Translate to Fourier/Dirichlet character bounds.",
            "E_n aligns spectral growth with sequence length.",
        ),
        ProofStep::new(
            "Apply entropy or energy increment arguments.",
            "F_n regulates oscillations while extracting structure.",
        ),
        ProofStep::new(
            "Show any bounded discrepancy implies contradiction.",
            "C pressure forces an impossible compression of energy.",
        ),
        ProofStep::new(
            "Conclude unbounded discrepancy.",
            "Z preserves temporal continuity to the divergence threshold.",
        ),
    ]);

    vec![
        erdos_straus,
        erdos_distinct,
        erdos_moser,
        erdos_ko_rado,
        erdos_szekeres,
        erdos_faber_lovasz,
        erdos_ginzburg_ziv,
        erdos_heilbronn,
        erdos_discrepancy,
    ]
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::path::PathBuf;

    struct GoldenCase {
        name: String,
        impulses: f64,
        elements: f64,
        pressure: f64,
        subjectivity: f64,
        purpose: f64,
        time: f64,
        n: usize,
        expected_intelligence: f64,
    }

    fn load_golden_cases() -> Vec<GoldenCase> {
        let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        path.push("..");
        path.push("..");
        path.push("tests");
        path.push("golden_cases.csv");

        let content = fs::read_to_string(path).expect("failed to read golden_cases.csv");
        content
            .lines()
            .skip(1)
            .filter(|line| !line.trim().is_empty())
            .map(|line| {
                let parts: Vec<&str> = line.split(',').collect();
                GoldenCase {
                    name: parts[0].to_string(),
                    impulses: parts[1].parse().expect("impulses"),
                    elements: parts[2].parse().expect("elements"),
                    pressure: parts[3].parse().expect("pressure"),
                    subjectivity: parts[4].parse().expect("subjectivity"),
                    purpose: parts[5].parse().expect("purpose"),
                    time: parts[6].parse().expect("time"),
                    n: parts[7].parse().expect("n"),
                    expected_intelligence: parts[8].parse().expect("expected_intelligence"),
                }
            })
            .collect()
    }

    // Foundation Layer Tests
    #[test]
    fn test_foundation_initialization() {
        let foundation = FoundationLayer::new(1.0, 1.0, 1.0);
        assert_eq!(foundation.impulses, 1.0);
        assert_eq!(foundation.elements, 1.0);
        assert_eq!(foundation.pressure, 1.0);
    }

    #[test]
    fn test_foundation_compute_product() {
        let foundation = FoundationLayer::new(2.0, 3.0, 1.5);
        assert_eq!(foundation.compute(), 2.0 * 3.0 * 1.5);
    }

    // Dynamic Layer Tests
    #[test]
    fn test_fibonacci_sequence_generation() {
        let sequence = fibonacci_sequence(12);
        let expected = vec![1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144];
        assert_eq!(sequence, expected);
    }

    #[test]
    fn test_fibonacci_at_n() {
        let dynamic1 = DynamicLayer::new(1);
        assert_eq!(dynamic1.fibonacci(), 1);

        let dynamic2 = DynamicLayer::new(2);
        assert_eq!(dynamic2.fibonacci(), 2);

        let dynamic3 = DynamicLayer::new(3);
        assert_eq!(dynamic3.fibonacci(), 3);

        let dynamic10 = DynamicLayer::new(10);
        assert_eq!(dynamic10.fibonacci(), 89);
    }

    #[test]
    fn test_exponential_growth() {
        let dynamic = DynamicLayer::new(1);
        let expected_n1 = 2.0 * 3.0_f64.powi(1) - 1.0; // 5.0
        assert!((dynamic.exponential_growth() - expected_n1).abs() < 1e-6);

        let dynamic2 = DynamicLayer::new(2);
        let expected_n2 = 2.0 * 3.0_f64.powi(2) - 1.0; // 17.0
        assert!((dynamic2.exponential_growth() - expected_n2).abs() < 1e-6);
    }

    #[test]
    fn test_dynamic_compute_product() {
        let dynamic = DynamicLayer::new(1);
        let e_n = 5.0; // 2 * 3^1 - 1 = 5
        let f_n = 1.0; // F(1) = 1
        let expected = e_n * (1.0 + f_n); // 5 * 2 = 10
        assert!((dynamic.compute() - expected).abs() < 1e-6);
    }

    // Cognitive Layer Tests
    #[test]
    fn test_subjectivity_objectivity_relationship() {
        let cognitive = CognitiveLayer::new(0.3, 1.0, 1.0);
        let objectivity = cognitive.objectivity();
        assert_eq!(objectivity, 0.7);
    }

    #[test]
    fn test_cognitive_compute_product() {
        let cognitive = CognitiveLayer::new(0.2, 1.5, 2.0);
        let expected = 0.8 * 1.5 * 2.0;
        assert_eq!(cognitive.compute(), expected);
    }

    // Universal Axiom Core Formula Tests
    #[test]
    fn test_axiom_initialization() {
        let axiom = UniversalAxiom::new();
        assert_eq!(axiom.n, 1);
    }

    #[test]
    fn test_core_formula_computation() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);

        let a_b_c = 1.0 * 1.0 * 1.0;
        let e_n = 5.0; // 2 * 3^1 - 1
        let f_n = 1.0; // F(1) = 1
        let e_f = e_n * (1.0 + f_n); // 5 * 2 = 10
        let x_y_z = 1.0 * 1.0 * 1.0;
        let expected = e_f * x_y_z * a_b_c; // 10

        let intelligence = axiom.compute_intelligence();
        assert!((intelligence - expected).abs() < 1e-6);
    }

    #[test]
    fn test_intelligence_at_n_1() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let intelligence = axiom.compute_intelligence();
        assert!((intelligence - 10.0).abs() < 1e-6); // E_n=5, F_n=1 → 5*(1+1) = 10
    }

    #[test]
    fn test_intelligence_at_n_10() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 10);
        let intelligence = axiom.compute_intelligence();
        // E_n=118097, F_n=89 → 118097*(1+89)*1*1*1 = 10,628,730
        assert!((intelligence - 10_628_730.0).abs() < 1.0);
    }

    #[test]
    fn test_evolve_increases_intelligence() {
        let mut axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let intelligence_before = axiom.compute_intelligence();
        axiom.evolve(1.0);
        let intelligence_after = axiom.compute_intelligence();
        assert!(intelligence_after > intelligence_before);
    }

    #[test]
    fn test_apply_pressure_increases_foundation() {
        let mut axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let intelligence_before = axiom.compute_intelligence();
        axiom.apply_pressure(1.0);
        let intelligence_after = axiom.compute_intelligence();
        assert!(intelligence_after > intelligence_before);
    }

    #[test]
    fn test_pressure_clamping_minimum() {
        let mut axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        axiom.apply_pressure(-10.0);
        assert_eq!(axiom.foundation.pressure, 0.01);
    }

    #[test]
    fn test_adjust_subjectivity_changes_objectivity() {
        let mut axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1);
        let intelligence_before = axiom.compute_intelligence();
        axiom.adjust_subjectivity(-0.2);
        let intelligence_after = axiom.compute_intelligence();
        assert!(intelligence_after > intelligence_before);
        assert_eq!(axiom.cognitive.subjectivity, 0.3);
    }

    #[test]
    fn test_subjectivity_clamping() {
        let mut axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1);
        axiom.adjust_subjectivity(1.0);
        assert_eq!(axiom.cognitive.subjectivity, 1.0);

        axiom.adjust_subjectivity(-2.0);
        assert_eq!(axiom.cognitive.subjectivity, 0.0);
    }

    #[test]
    fn test_strengthen_purpose_multiplier() {
        let mut axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let intelligence_before = axiom.compute_intelligence();
        axiom.strengthen_purpose(1.5);
        assert_eq!(axiom.cognitive.purpose, 1.5);
        let intelligence_after = axiom.compute_intelligence();
        assert!(intelligence_after > intelligence_before);
    }

    #[test]
    fn test_get_state_completeness() {
        let axiom = UniversalAxiom::new();
        let state = axiom.get_state();
        assert_eq!(state.n, 1);
        assert!(state.intelligence > 0.0);
    }

    #[test]
    fn test_negative_impulses() {
        let axiom = UniversalAxiom::with_params(-1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let intelligence = axiom.compute_intelligence();
        assert!(intelligence < 0.0);
    }

    #[test]
    fn test_extreme_subjectivity() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1);
        let intelligence = axiom.compute_intelligence();
        assert_eq!(intelligence, 0.0);
    }

    #[test]
    fn test_math_solutions_seed_contains_problem() {
        let solutions = MathSolutions::erdos_seed();
        let expected = vec![
            ("erdos-straus", "open"),
            ("erdos-distinct-distances", "solved"),
            ("erdos-moser", "partial"),
            ("erdos-ko-rado", "solved"),
            ("erdos-szekeres", "partial"),
            ("erdos-faber-lovasz", "solved"),
            ("erdos-ginzburg-ziv", "solved"),
            ("erdos-heilbronn", "solved"),
            ("erdos-discrepancy", "solved"),
        ];

        assert_eq!(solutions.list_problems().len(), expected.len());
        for (identifier, status) in expected {
            let problem = solutions.get_problem(identifier);
            assert!(problem.is_some());
            let problem = problem.unwrap();
            assert_eq!(problem.status, status);
            assert_eq!(problem.proof_steps.len(), 5);
        }
    }

    #[test]
    fn test_math_solutions_add_proof_step() {
        let mut solutions = MathSolutions::erdos_seed();
        let result = solutions.add_proof_step(
            "erdos-straus",
            "Normalize the equation to isolate reciprocal structure.",
            "Use the axiom's foundation layer (A·B·C) to align constraints.",
        );
        assert!(result.is_ok());
        let problem = solutions.get_problem("erdos-straus").unwrap();
        assert_eq!(problem.proof_steps.len(), 6);
        let last_step = problem.proof_steps.last().unwrap();
        assert!(last_step.statement.contains("Normalize the equation"));
    }

    #[test]
    fn test_extreme_objectivity() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let intelligence = axiom.compute_intelligence();
        assert!(intelligence > 0.0);
    }

    // AxiomSimulator Tests
    #[test]
    fn test_simulator_initialization() {
        let axiom = UniversalAxiom::new();
        let _simulator = AxiomSimulator::new(axiom);
    }

    #[test]
    fn test_simulate_evolution_tracks_history() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let mut simulator = AxiomSimulator::new(axiom);
        let history = simulator.simulate_evolution(5, 1.0);

        assert_eq!(history.len(), 6); // initial + 5 steps
        assert_eq!(history[0].n, 1);
        assert_eq!(history[5].n, 6);
    }

    #[test]
    fn test_contradiction_resolution_reduces_subjectivity() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1);
        let initial_subjectivity = axiom.cognitive.subjectivity;
        let mut simulator = AxiomSimulator::new(axiom);

        let history = simulator.simulate_contradiction_resolution(2.0, 5);
        let final_subjectivity = history[history.len() - 1].cognitive.x_subjectivity;

        assert!(final_subjectivity < initial_subjectivity);
    }

    #[test]
    fn test_coherence_metric_high_objectivity() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.1, 2.0, 1.0, 1);
        let simulator = AxiomSimulator::new(axiom);
        let coherence = simulator.get_coherence_metric();
        assert!(coherence > 0.8);
    }

    #[test]
    fn test_coherence_decreases_with_subjectivity() {
        let axiom_objective = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.1, 1.0, 1.0, 1);
        let coherence_objective = AxiomSimulator::new(axiom_objective).get_coherence_metric();

        let axiom_subjective = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.8, 1.0, 1.0, 1);
        let coherence_subjective = AxiomSimulator::new(axiom_subjective).get_coherence_metric();

        assert!(coherence_objective > coherence_subjective);
    }

    #[test]
    fn test_no_stagnation_with_evolution() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let mut simulator = AxiomSimulator::new(axiom);
        let history = simulator.simulate_evolution(10, 1.0);

        let intelligences: Vec<f64> = history.iter().map(|s| s.intelligence).collect();

        // Verify monotonic increase
        for i in 1..intelligences.len() {
            assert!(intelligences[i] > intelligences[i - 1]);
        }
    }

    #[test]
    fn test_golden_cases_parity() {
        let cases = load_golden_cases();
        for case in cases {
            let axiom = UniversalAxiom::with_params(
                case.impulses,
                case.elements,
                case.pressure,
                case.subjectivity,
                case.purpose,
                case.time,
                case.n,
            );
            let actual = axiom.compute_intelligence();
            let delta = (actual - case.expected_intelligence).abs();
            assert!(
                delta <= 1e-6,
                "case {} mismatch: expected {}, got {}",
                case.name,
                case.expected_intelligence,
                actual
            );
        }
    }

    // PROMPT.md Compliance Tests
    #[test]
    fn test_axiom_is_deterministic() {
        let axiom1 = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 5);
        let axiom2 = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 5);
        assert_eq!(axiom1.compute_intelligence(), axiom2.compute_intelligence());
    }

    #[test]
    fn test_fibonacci_regulation_of_dynamics() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let mut simulator = AxiomSimulator::new(axiom);
        let history = simulator.simulate_evolution(10, 1.0);

        let fib_values: Vec<u64> = history.iter().take(10).map(|s| s.dynamic.f_n).collect();
        let expected = vec![1, 2, 3, 5, 8, 13, 21, 34, 55, 89];

        assert_eq!(fib_values, expected);
    }

    #[test]
    fn test_pressure_reveals_contradictions() {
        let mut axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1);
        axiom.apply_pressure(2.0);
        assert_eq!(axiom.foundation.pressure, 3.0);
    }

    #[test]
    fn test_timesphere_advancement() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        let mut simulator = AxiomSimulator::new(axiom);
        let history = simulator.simulate_evolution(5, 1.0);

        let times: Vec<f64> = history.iter().map(|s| s.cognitive.z_time).collect();
        let expected = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0];

        for (i, &time) in times.iter().enumerate() {
            assert!((time - expected[i]).abs() < 1e-6);
        }
    }

    #[test]
    fn test_foundation_abc_variables() {
        let axiom = UniversalAxiom::with_params(2.0, 3.0, 1.5, 0.0, 1.0, 1.0, 1);
        let state = axiom.get_state();

        assert_eq!(state.foundation.a_impulses, 2.0);
        assert_eq!(state.foundation.b_elements, 3.0);
        assert_eq!(state.foundation.c_pressure, 1.5);
        assert_eq!(state.foundation.product, 2.0 * 3.0 * 1.5);
    }

    #[test]
    fn test_cognitive_xyz_variables() {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.3, 1.5, 2.0, 1);
        let state = axiom.get_state();

        assert_eq!(state.cognitive.x_subjectivity, 0.3);
        assert_eq!(state.cognitive.x_objectivity, 0.7);
        assert_eq!(state.cognitive.y_purpose, 1.5);
        assert_eq!(state.cognitive.z_time, 2.0);
    }

    #[test]
    fn test_large_n_fibonacci_growth() {
        let mut axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1);
        for _ in 0..19 {
            axiom.evolve(1.0);
        }

        let intelligence = axiom.compute_intelligence();
        assert!(intelligence > 0.0);
        assert!(intelligence.is_finite());
    }
}
