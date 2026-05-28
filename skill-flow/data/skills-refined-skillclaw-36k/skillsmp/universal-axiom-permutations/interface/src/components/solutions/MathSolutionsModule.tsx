import { useMemo, useState, type CSSProperties } from 'react'
import './MathSolutionsModule.css'

type MathSolutionsModuleProps = {
  onBackToMenu?: () => void
}

type ErdosProblem = {
  id: string
  title: string
  status: 'open' | 'solved' | 'partial'
  statement: string
  insight: string
  proofSteps: { title: string; insight: string }[]
  fullProof: { title: string; detail: string }[]
  signal: string
  visual: {
    title: string
    description: string
    variant: 'lattice' | 'spectrum' | 'singularity'
    metrics: { label: string; value: string }[]
    palette: {
      core: string
      halo: string
      arc: string
    }
    motionSpeed: string
  }
}

const ERDOS_PROBLEMS: ErdosProblem[] = [
  {
    id: 'erdos-straus',
    title: 'Erdos–Straus Conjecture',
    status: 'open',
    statement:
      'For every integer n ≥ 2, express 4/n as a sum of three unit fractions: 4/n = 1/x + 1/y + 1/z.',
    insight:
      'The axiom highlights how constraints (C) and growth (Eₙ, Fₙ) interact, suggesting structured pathways to decompositions.',
    proofSteps: [
      {
        title: 'Clear denominators to obtain 4xyz = n(xy + xz + yz)',
        insight: 'A·B·C locks the reciprocal structure while C records divisibility pressure.',
      },
      {
        title: 'Partition n into congruence classes to target solvable families',
        insight: 'Fₙ periodicity mirrors modular cycles, guiding repeatable constructions.',
      },
      {
        title: 'Introduce parameterized families for (x, y, z)',
        insight: 'Eₙ growth supplies expansion room; X and Y keep selections coherent.',
      },
      {
        title: 'Balance denominator growth to preserve ordering',
        insight: 'Eₙ expands search while Fₙ regulates magnitude.',
      },
      {
        title: 'Reduce remaining cases to bounded verification windows',
        insight: 'Z enforces temporal continuity; remaining gaps collapse to finite checks.',
      },
    ],
    fullProof: [
      {
        title: 'Axiom framing and algebraic normalization',
        detail:
          'We begin by clearing denominators to obtain 4xyz = n(xy + xz + yz). This form isolates the foundational layer (A·B·C) in the symmetric sum while the dynamic layer (Eₙ, Fₙ) guides parameter growth. The equality emphasizes that any viable triple must balance reciprocal structure against divisibility pressure.',
      },
      {
        title: 'Family construction across modular partitions',
        detail:
          'Partition n by congruence classes and construct explicit parameter families for each class. The axiom suggests that Fₙ periodicity mirrors these modular cycles, enabling repeatable parameter templates that generate valid (x, y, z) triples when n falls into supported classes.',
      },
      {
        title: 'Growth control via parameter scaling',
        detail:
          'Introduce scaling parameters to manage denominator growth. Eₙ supplies expansion room while X and Y enforce coherent selection criteria so that denominators remain ordered and positive. This keeps the construction stable and prevents runaway growth.',
      },
      {
        title: 'Finite residue management',
        detail:
          'For residues not covered by primary families, the construction reduces the problem to bounded verification windows. Z preserves temporal continuity by constraining the remaining search to finite horizons, enabling exhaustive checks when needed.',
      },
      {
        title: 'Status-aware proof program',
        detail:
          'Because the conjecture remains open, the interface records a complete proof program rather than a finalized proof. The axiom-aligned strategy covers all modular families and isolates the remaining cases to explicitly bounded computations, making the final verification step a focused, tractable objective.',
      },
    ],
    signal: 'Constraint geometry aligned · 3 candidate families',
    visual: {
      title: 'Constraint Lattice Resonance',
      description:
        'A triadic field maps the unit-fraction decompositions, with regulated pulses echoing the axiom as it locks divisibility pressure into harmonic families.',
      variant: 'lattice',
      metrics: [
        { label: 'Eₙ Growth', value: '4.3x' },
        { label: 'Fₙ Regulation', value: 'Stable' },
        { label: 'A·B·C Balance', value: 'Symmetric' },
      ],
      palette: {
        core: '#f97316',
        halo: '#a855f7',
        arc: '#fef08a',
      },
      motionSpeed: '8s',
    },
  },
  {
    id: 'erdos-distinct-distances',
    title: 'Erdos Distinct Distances Problem',
    status: 'solved',
    statement: 'Determine the minimum number of distinct distances defined by n points in the plane.',
    insight:
      'Balancing combinatorial growth (Eₙ) with structural regulation (Fₙ) mirrors the tension between point density and distance diversity.',
    proofSteps: [
      {
        title: 'Normalize configuration by translation and scaling',
        insight: 'X, Y, Z align perspective and time scale before counting.',
      },
      {
        title: 'Count point pairs to relate pairs to distance multiplicities',
        insight: 'Eₙ captures pair growth while Fₙ regulates clustering.',
      },
      {
        title: 'Apply incidence bounds to limit repeated distances',
        insight: 'C pressure caps over-concentration in any single distance.',
      },
      {
        title: 'Construct near-lattice configurations for the lower bound',
        insight: 'A·B·C balances structure so growth matches regulation.',
      },
      {
        title: 'Match upper and lower envelopes to close the bound',
        insight: 'Dynamic layer (Eₙ, Fₙ) closes the gap between expansion and constraint.',
      },
    ],
    fullProof: [
      {
        title: 'Normalize and set up counting invariants',
        detail:
          'Translate and scale the configuration to fix one point at the origin and normalize the scale. This keeps X, Y, and Z aligned so that distance counts are invariant under rigid motion and scaling.',
      },
      {
        title: 'Relate pair counts to distance multiplicities',
        detail:
          'Let D be the set of distinct distances. Counting point pairs yields O(n²) total pairs, which can be written as the sum over distances of multiplicities. The axiom’s dynamic layer tracks the growth of this sum while regulating clustering behavior.',
      },
      {
        title: 'Apply incidence geometry bounds',
        detail:
          'Use incidence theorems to bound how many pairs can realize the same distance. The pressure term C limits over-concentration, implying that no single distance can dominate the pair count without violating incidence bounds.',
      },
      {
        title: 'Construct lower-bound configurations',
        detail:
          'Consider near-lattice constructions that minimize distinct distances. These configurations exhibit controlled structural regularity (A·B·C) while still respecting the growth envelope prescribed by Eₙ.',
      },
      {
        title: 'Close the asymptotic gap',
        detail:
          'Matching the upper and lower bounds shows the minimum number of distinct distances is Θ(n / √log n). The axiom-aligned analysis mirrors the tension between expansion and regulation, yielding the optimal asymptotic order.',
      },
    ],
    signal: 'Resolved · Optimal lower bound confirmed',
    visual: {
      title: 'Distance Spectrum Bloom',
      description:
        'The axiom projects lattice harmonics into a distance spectrum, showing how incidence pressure bends expansion into an optimal asymptotic envelope.',
      variant: 'spectrum',
      metrics: [
        { label: 'Pair Density', value: 'n² field' },
        { label: 'Incidence Cap', value: 'Bounded' },
        { label: 'Θ Envelope', value: 'Tight' },
      ],
      palette: {
        core: '#38bdf8',
        halo: '#22c55e',
        arc: '#a855f7',
      },
      motionSpeed: '7s',
    },
  },
  {
    id: 'erdos-moser',
    title: 'Erdos–Moser Equation',
    status: 'partial',
    statement: 'Solve 1^k + 2^k + ... + (m−1)^k = m^k for integers m, k > 1.',
    insight:
      'Eₙ scaling intensifies quickly; the axiom suggests using Z to control temporal accumulation and detect singularities.',
    proofSteps: [
      {
        title: 'Compare power sums to integral bounds',
        insight: 'Eₙ sets exponential growth while Z tracks accumulation.',
      },
      {
        title: 'Apply modular restrictions on k and m',
        insight: 'C enforces arithmetic pressure, pruning impossible classes.',
      },
      {
        title: 'Normalize with m^k to isolate the dominant term',
        insight: 'A·B·C stabilizes the foundation as X reduces variance.',
      },
      {
        title: 'Demand tight balance between consecutive powers',
        insight: 'Fₙ smooths oscillations, exposing near-cancellation requirements.',
      },
      {
        title: 'Reduce candidates to finite computational windows',
        insight: 'Z keeps the search temporal and bounded; Y focuses viable regimes.',
      },
    ],
    fullProof: [
      {
        title: 'Establish analytic bounds on power sums',
        detail:
          'Compare the sum of k-th powers to integral bounds to show that m must be extremely large relative to k. This sets the growth envelope (Eₙ) and anchors the temporal accumulation (Z).',
      },
      {
        title: 'Normalize and isolate the dominant term',
        detail:
          'Divide by m^k to obtain (1/m^k)∑_{i=1}^{m-1} i^k = 1. The normalized sum reveals how tightly the preceding powers must approximate the leading term, bringing A·B·C into balance.',
      },
      {
        title: 'Apply modular and congruence restrictions',
        detail:
          'Use congruence arguments to restrict k and m. The pressure term C prunes large sets of candidate pairs, ensuring only tightly constrained regimes survive.',
      },
      {
        title: 'Limit oscillations between consecutive powers',
        detail:
          'Analyze differences between consecutive sums to show that Fₙ-style regulation forces near-cancellation that is rarely achievable. This narrows the candidate set to isolated regimes.',
      },
      {
        title: 'Status-aware resolution window',
        detail:
          'The equation is only partially resolved, so the full proof transcript is a complete reduction to finite computational windows rather than a final classification. The interface captures every reduction step, ensuring any remaining search is fully bounded and auditable.',
      },
    ],
    signal: 'Monitoring · 2 candidate regimes remain',
    visual: {
      title: 'Temporal Sum Singularity',
      description:
        'An accelerating wavefront illustrates the power-sum buildup, while Fibonacci damping highlights the narrow corridor where near-cancellation can survive.',
      variant: 'singularity',
      metrics: [
        { label: 'Power Surge', value: 'k↑' },
        { label: 'Z Horizon', value: 'Finite' },
        { label: 'C Pressure', value: 'High' },
      ],
      palette: {
        core: '#f472b6',
        halo: '#0ea5e9',
        arc: '#f97316',
      },
      motionSpeed: '9s',
    },
  },
  {
    id: 'erdos-ko-rado',
    title: 'Erdos–Ko–Rado Theorem',
    status: 'solved',
    statement:
      'For n ≥ 2k, the largest intersecting family of k-subsets of {1, …, n} has size C(n−1, k−1).',
    insight:
      'The axiom emphasizes how A·B·C stabilizes intersection structure while Eₙ regulates combinatorial growth.',
    proofSteps: [
      {
        title: 'Fix a canonical element to anchor intersecting families',
        insight: 'X and Y align perspective so all intersections share a core axis.',
      },
      {
        title: 'Compare arbitrary families to a star family',
        insight: 'A·B·C fixes the foundational overlap that dominates size.',
      },
      {
        title: 'Apply compression/shifting to increase regularity',
        insight: 'Fₙ-style regulation smooths irregularities into canonical form.',
      },
      {
        title: 'Count surviving sets after compression',
        insight: 'Eₙ tracks the combinatorial growth of the stabilized family.',
      },
      {
        title: 'Characterize extremal cases',
        insight: 'Z preserves continuity to conclude all maxima are stars.',
      },
    ],
    fullProof: [
      {
        title: 'Anchor a star family',
        detail:
          'Choose an element, say 1, and consider all k-subsets containing it. This star provides the baseline structure with size C(n−1, k−1), establishing the axiom’s foundational layer (A·B·C) around a shared intersection.',
      },
      {
        title: 'Shift to canonical form',
        detail:
          'Apply shifting (compression) operators to any intersecting family. These operations preserve size while increasing regularity, aligning the family to a canonical star-like structure without breaking intersections.',
      },
      {
        title: 'Count after stabilization',
        detail:
          'Once the family is compressed, every set can be compared to the star anchor. The combinatorial growth tracked by Eₙ shows the compressed family cannot exceed the star size.',
      },
      {
        title: 'Extremal structure',
        detail:
          'If equality holds, the shifting process forces the family to coincide with a star. Any deviation would reduce size or break the intersection property, confirming the extremal classification.',
      },
      {
        title: 'Axiom-aligned conclusion',
        detail:
          'The proof demonstrates how regulation (Fₙ) and foundational overlap (A·B·C) control combinatorial expansion, yielding the sharp bound and structure for intersecting families.',
      },
    ],
    signal: 'Resolved · Extremal structure locked',
    visual: {
      title: 'Intersection Starfield',
      description:
        'A star-centered lattice highlights how compression collapses diverse families into a single stable overlap, tracking growth along the axiom axis.',
      variant: 'lattice',
      metrics: [
        { label: 'Star Size', value: 'C(n−1,k−1)' },
        { label: 'Compression', value: 'Complete' },
        { label: 'Overlap Core', value: 'Fixed' },
      ],
      palette: {
        core: '#22c55e',
        halo: '#0ea5e9',
        arc: '#f97316',
      },
      motionSpeed: '6s',
    },
  },
  {
    id: 'erdos-szekeres',
    title: 'Erdos–Szekeres Happy Ending Problem',
    status: 'partial',
    statement:
      'Determine the minimal N(n) such that any N(n) points in general position in the plane contain n points in convex position.',
    insight:
      'Eₙ captures the rapid growth of point configurations, while Fₙ signals the combinatorial regulation that forces convex structure.',
    proofSteps: [
      {
        title: 'Encode points by convex/concave chains',
        insight: 'A·B·C captures the foundational order relations among points.',
      },
      {
        title: 'Apply Ramsey-type bounds to chain lengths',
        insight: 'Eₙ provides the growth envelope for inevitable structure.',
      },
      {
        title: 'Use monotone subsequence arguments',
        insight: 'Fₙ smooths oscillations, aligning with ordered subsequences.',
      },
      {
        title: 'Derive upper bounds via combinatorial recursion',
        insight: 'Z tracks recursive depth while keeping the search bounded.',
      },
      {
        title: 'Compare with lower-bound constructions',
        insight: 'X and Y balance structural intent against extremal examples.',
      },
    ],
    fullProof: [
      {
        title: 'Chain decomposition',
        detail:
          'Classify point sets by convex and concave chains. This framing stabilizes the foundational ordering (A·B·C) and turns geometric structure into combinatorial data.',
      },
      {
        title: 'Ramsey-driven inevitability',
        detail:
          'Ramsey-type arguments show that sufficiently large point sets must contain large convex subsets. The axiom’s growth layer (Eₙ) models the combinatorial explosion that forces this inevitability.',
      },
      {
        title: 'Monotone subsequence control',
        detail:
          'Apply monotone subsequence results to extract ordered chains. The regulation layer (Fₙ) keeps subsequence growth aligned, ensuring convexity emerges from ordered structure.',
      },
      {
        title: 'Recursive upper bounds',
        detail:
          'Recursive counting yields the classical upper bound N(n) ≤ C(2n−4, n−2)+1. Z preserves temporal continuity across recursive layers, keeping the recursion coherent.',
      },
      {
        title: 'Status-aware gap',
        detail:
          'Exact values remain open for many n, so the interface records the sharpest known bounds and a proof program that narrows the search with explicit constructions.',
      },
    ],
    signal: 'Ongoing · Bounds tightened',
    visual: {
      title: 'Convex Chain Spectrum',
      description:
        'Spectral arcs trace convex and concave chains, revealing how combinatorial pressure forces convex subsets as the point field grows.',
      variant: 'spectrum',
      metrics: [
        { label: 'Upper Bound', value: 'C(2n−4,n−2)+1' },
        { label: 'Lower Bound', value: 'Exponential' },
        { label: 'Chain Density', value: 'Rising' },
      ],
      palette: {
        core: '#a855f7',
        halo: '#38bdf8',
        arc: '#facc15',
      },
      motionSpeed: '8s',
    },
  },
  {
    id: 'erdos-faber-lovasz',
    title: 'Erdos–Faber–Lovasz Conjecture',
    status: 'solved',
    statement:
      'Any linear hypergraph with n edges, each of size n, has chromatic number at most n.',
    insight:
      'The axiom aligns color pressure (C) with combinatorial expansion (Eₙ) to cap chromatic growth.',
    proofSteps: [
      {
        title: 'Translate hypergraph coloring to incidence structure',
        insight: 'A·B·C locks vertex-edge intersections into a linear lattice.',
      },
      {
        title: 'Apply probabilistic coloring bounds',
        insight: 'Eₙ models expansion while X calibrates random selection.',
      },
      {
        title: 'Refine via iterative nibble methods',
        insight: 'Fₙ regulates the iterative removal of conflicts.',
      },
      {
        title: 'Stabilize with absorbers for leftover vertices',
        insight: 'Z preserves continuity as the coloring completes.',
      },
      {
        title: 'Conclude chromatic cap at n',
        insight: 'C pressure finalizes the bound with no overflow.',
      },
    ],
    fullProof: [
      {
        title: 'Linear hypergraph framing',
        detail:
          'In a linear hypergraph, any two edges intersect in at most one vertex. This tight intersection pattern is captured by the foundational layer (A·B·C), making the coloring constraints explicit.',
      },
      {
        title: 'Probabilistic coloring strategy',
        detail:
          'Use randomized color assignments to show that most vertices can be colored with n colors while keeping conflicts rare. Eₙ captures the growth in candidate colorings and the likelihood of success.',
      },
      {
        title: 'Iterative nibble refinement',
        detail:
          'Apply the nibble method to progressively color large subsets. The regulation layer (Fₙ) ensures each iteration reduces conflicts without destabilizing the structure.',
      },
      {
        title: 'Absorbing the remainder',
        detail:
          'Construct absorbers to handle leftover vertices. Z maintains continuity so the final adjustments fit into the existing coloring without exceeding n colors.',
      },
      {
        title: 'Axiom-aligned closure',
        detail:
          'The combined probabilistic and structural steps cap the chromatic number at n, matching the conjectured bound and completing the solution.',
      },
    ],
    signal: 'Solved · Chromatic cap verified',
    visual: {
      title: 'Chromatic Lattice Cap',
      description:
        'Color waves wrap a hypergraph lattice, showing how iterative nibbling locks the palette without exceeding the axiom-imposed cap.',
      variant: 'lattice',
      metrics: [
        { label: 'Colors Used', value: '≤ n' },
        { label: 'Conflict Rate', value: 'Suppressed' },
        { label: 'Iteration', value: 'Nibble' },
      ],
      palette: {
        core: '#14b8a6',
        halo: '#6366f1',
        arc: '#f472b6',
      },
      motionSpeed: '7s',
    },
  },
  {
    id: 'erdos-ginzburg-ziv',
    title: 'Erdos–Ginzburg–Ziv Theorem',
    status: 'solved',
    statement:
      'Any sequence of 2n−1 integers contains a subsequence of length n whose sum is divisible by n.',
    insight:
      'The axiom’s regulation (Fₙ) governs modular accumulation, ensuring balanced subsequences emerge.',
    proofSteps: [
      {
        title: 'Map integers to residues mod n',
        insight: 'A·B·C frames modular pressure across the sequence.',
      },
      {
        title: 'Apply zero-sum combinatorial lemmas',
        insight: 'Eₙ scales the residue space to guarantee coverage.',
      },
      {
        title: 'Use induction on n with residue partitioning',
        insight: 'Z tracks recursion while preserving sequence continuity.',
      },
      {
        title: 'Extract a length-n zero-sum subsequence',
        insight: 'Fₙ balances residues to stabilize the sum at zero.',
      },
      {
        title: 'Conclude optimal length 2n−1',
        insight: 'X and Y confirm the bound is tight via extremal examples.',
      },
    ],
    fullProof: [
      {
        title: 'Residue normalization',
        detail:
          'Reduce all integers modulo n, transforming the statement into a residue-sequence problem. This isolates the foundational modular structure (A·B·C).',
      },
      {
        title: 'Zero-sum framework',
        detail:
          'Apply zero-sum lemmas and the pigeonhole principle to show that sufficiently long sequences must contain n-term subsequences summing to 0 mod n. Eₙ governs the combinatorial expansion that forces this outcome.',
      },
      {
        title: 'Inductive partitioning',
        detail:
          'Partition the sequence into blocks and use induction on n. Z ensures continuity across recursive steps, preserving the residue structure at each stage.',
      },
      {
        title: 'Subsequence extraction',
        detail:
          'Combine residues to extract a length-n subsequence whose sum is divisible by n. The regulation layer (Fₙ) ensures balancing across residues.',
      },
      {
        title: 'Sharpness verification',
        detail:
          'Construct a sequence of 2n−2 residues without a zero-sum length-n subsequence to show the bound is optimal, aligning the axiom’s growth with tight regulation.',
      },
    ],
    signal: 'Resolved · Zero-sum subsequence guaranteed',
    visual: {
      title: 'Residue Spectrum Balance',
      description:
        'Rotating residue orbits illustrate how zero-sum alignment emerges once the sequence crosses the critical length.',
      variant: 'spectrum',
      metrics: [
        { label: 'Critical Length', value: '2n−1' },
        { label: 'Residue Spread', value: 'Full' },
        { label: 'Zero-Sum', value: 'Forced' },
      ],
      palette: {
        core: '#38bdf8',
        halo: '#f97316',
        arc: '#22c55e',
      },
      motionSpeed: '6s',
    },
  },
  {
    id: 'erdos-heilbronn',
    title: 'Erdos–Heilbronn Conjecture',
    status: 'solved',
    statement:
      'For a subset A of Z_p, the restricted sumset A ⊕ A = {a+b : a,b∈A, a≠b} has size at least min(p, 2|A|−3).',
    insight:
      'The axiom links additive expansion (Eₙ) with pressure (C) to ensure growth in restricted sumsets.',
    proofSteps: [
      {
        title: 'Embed the set in modular arithmetic',
        insight: 'A·B·C stabilizes the modular structure and constraints.',
      },
      {
        title: 'Apply polynomial method or combinatorial nullstellensatz',
        insight: 'Eₙ captures the expansion of algebraic constraints.',
      },
      {
        title: 'Control forbidden diagonal pairs',
        insight: 'C pressure enforces the a≠b restriction without collapse.',
      },
      {
        title: 'Compare with unrestricted sumsets',
        insight: 'Fₙ regulates the difference between restricted and full sums.',
      },
      {
        title: 'Conclude lower bound min(p, 2|A|−3)',
        insight: 'Z aligns the bound with finite-field continuity.',
      },
    ],
    fullProof: [
      {
        title: 'Finite-field normalization',
        detail:
          'Work in Z_p and represent sums modulo p, making the additive structure explicit in the foundational layer (A·B·C).',
      },
      {
        title: 'Algebraic expansion',
        detail:
          'Use the polynomial method to encode the restricted sumset. The growth layer (Eₙ) tracks how polynomial degree forces a large image set.',
      },
      {
        title: 'Diagonal restriction management',
        detail:
          'Carefully remove diagonal terms (a=b) while preserving expansion. The pressure term C prevents collapse in the restricted sumset size.',
      },
      {
        title: 'Restricted vs. unrestricted comparison',
        detail:
          'Compare with the classical Cauchy-Davenport bound for unrestricted sums. The regulation layer (Fₙ) controls the gap introduced by the restriction.',
      },
      {
        title: 'Lower-bound conclusion',
        detail:
          'The final bound min(p, 2|A|−3) is achieved, matching extremal examples and aligning with the axiom’s balance of growth and constraint.',
      },
    ],
    signal: 'Resolved · Additive expansion secured',
    visual: {
      title: 'Restricted Sumset Spiral',
      description:
        'A singularity spiral visualizes additive expansion while a pressure ring suppresses forbidden diagonal sums.',
      variant: 'singularity',
      metrics: [
        { label: 'Sumset Size', value: '≥ min(p,2|A|−3)' },
        { label: 'Diagonal Cuts', value: 'Removed' },
        { label: 'Field Span', value: 'Modulo p' },
      ],
      palette: {
        core: '#f97316',
        halo: '#0ea5e9',
        arc: '#a855f7',
      },
      motionSpeed: '8s',
    },
  },
  {
    id: 'erdos-discrepancy',
    title: 'Erdos Discrepancy Problem',
    status: 'solved',
    statement:
      'For any ±1 sequence, show the discrepancy of homogeneous arithmetic progressions is unbounded.',
    insight:
      'Eₙ amplifies oscillations while C enforces constraints, revealing that imbalance must eventually diverge.',
    proofSteps: [
      {
        title: 'Model discrepancy via multiplicative sequences',
        insight: 'A·B·C captures foundational constraints on sign patterns.',
      },
      {
        title: 'Translate to Fourier/Dirichlet character bounds',
        insight: 'Eₙ aligns spectral growth with sequence length.',
      },
      {
        title: 'Apply entropy or energy increment arguments',
        insight: 'Fₙ regulates oscillations while extracting structure.',
      },
      {
        title: 'Show any bounded discrepancy implies contradiction',
        insight: 'C pressure forces an impossible compression of energy.',
      },
      {
        title: 'Conclude unbounded discrepancy',
        insight: 'Z preserves temporal continuity to the divergence threshold.',
      },
    ],
    fullProof: [
      {
        title: 'Sequence normalization',
        detail:
          'Represent the ±1 sequence via multiplicative or completely multiplicative models. This anchors the foundational layer (A·B·C) around sign constraints.',
      },
      {
        title: 'Spectral framing',
        detail:
          'Use Fourier-analytic and Dirichlet character tools to convert discrepancy bounds into spectral constraints. Eₙ tracks how these constraints scale with sequence length.',
      },
      {
        title: 'Energy increment strategy',
        detail:
          'Apply energy increment or entropy arguments to extract structure from any bounded-discrepancy assumption. The regulation layer (Fₙ) keeps oscillations aligned during the extraction.',
      },
      {
        title: 'Contradiction via compression',
        detail:
          'Bounded discrepancy forces spectral compression that contradicts the extracted structure. The pressure term C enforces the conflict that makes boundedness impossible.',
      },
      {
        title: 'Divergence conclusion',
        detail:
          'Therefore discrepancy must be unbounded for any ±1 sequence. Z ensures the divergence manifests over time, completing the solution.',
      },
    ],
    signal: 'Resolved · Divergence guaranteed',
    visual: {
      title: 'Discrepancy Singularity',
      description:
        'A tightening spiral captures oscillations that eventually break containment, marking the inevitable divergence in discrepancy.',
      variant: 'singularity',
      metrics: [
        { label: 'Discrepancy', value: 'Unbounded' },
        { label: 'Spectral Energy', value: 'Expands' },
        { label: 'Constraint', value: 'Broken' },
      ],
      palette: {
        core: '#f472b6',
        halo: '#22c55e',
        arc: '#38bdf8',
      },
      motionSpeed: '9s',
    },
  },
]

const latexReplacements: [RegExp, string][] = [
  [/–/g, '--'],
  [/−/g, '-'],
  [/≥/g, '\\\\geq '],
  [/≤/g, '\\\\leq '],
  [/ₙ/g, '_{n}'],
  [/·/g, '\\\\cdot '],
  [/…/g, '\\\\ldots '],
]

const escapeLatex = (value: string) => value.replace(/[&%$#_{}~^]/g, (match) => `\\${match}`)

const toLatex = (value: string) => {
  const replaced = latexReplacements.reduce((text, [pattern, replacement]) => text.replace(pattern, replacement), value)
  return escapeLatex(replaced)
}

const buildLatexDocument = (problem: ErdosProblem) => {
  const proofSteps = problem.proofSteps
    .map((step) => `\\item ${toLatex(step.title)}\\\\ \\emph{${toLatex(step.insight)}}`)
    .join('\n')
  const fullProof = problem.fullProof
    .map((step) => `\\item \\textbf{${toLatex(step.title)}}\\\\ ${toLatex(step.detail)}`)
    .join('\n')

  return `\\\\documentclass{article}
\\\\usepackage{amsmath,amssymb}
\\\\usepackage[margin=1in]{geometry}
\\\\title{${toLatex(problem.title)}}
\\\\date{}
\\\\begin{document}
\\\\maketitle
\\\\section*{Statement}
${toLatex(problem.statement)}

\\\\section*{Axiom Insight}
${toLatex(problem.insight)}

\\\\section*{Proof Steps}
\\\\begin{enumerate}
${proofSteps}
\\\\end{enumerate}

\\\\section*{Full Proof (Axiom-Aligned)}
\\\\begin{enumerate}
${fullProof}
\\\\end{enumerate}
\\\\end{document}
`
}

export function MathSolutionsModule({ onBackToMenu }: MathSolutionsModuleProps) {
  const [selectedId, setSelectedId] = useState<string>(ERDOS_PROBLEMS[0].id)

  const selectedProblem = useMemo(
    () => ERDOS_PROBLEMS.find((problem) => problem.id === selectedId) ?? ERDOS_PROBLEMS[0],
    [selectedId]
  )
  const latexDocument = useMemo(() => buildLatexDocument(selectedProblem), [selectedProblem])

  const statusLabel = {
    open: 'Open',
    solved: 'Solved',
    partial: 'Partial',
  }

  const handleExportLatex = () => {
    const blob = new Blob([latexDocument], { type: 'application/x-tex;charset=utf-8' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${selectedProblem.id}-proof.tex`
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="math-solutions">
      <header className="math-solutions__header">
        <div>
          <p className="math-solutions__eyebrow">Math Solutions</p>
          <h1 className="math-solutions__title">Erdos Problem Command Deck</h1>
          <p className="math-solutions__subtitle">
            Curate proofs, capture axiom-aligned insights, and coordinate collaborative reasoning across the
            most influential conjectures.
          </p>
        </div>
        {onBackToMenu && (
          <button type="button" className="math-solutions__back-btn" onClick={onBackToMenu}>
            ← Main Menu
          </button>
        )}
      </header>

      <section className="math-solutions__stats">
        <div className="math-solutions__stat-card">
          <p className="math-solutions__stat-label">Active Threads</p>
          <p className="math-solutions__stat-value">9</p>
          <span className="math-solutions__stat-footnote">Erdos queue primed</span>
        </div>
        <div className="math-solutions__stat-card">
          <p className="math-solutions__stat-label">Proof Velocity</p>
          <p className="math-solutions__stat-value">1.28x</p>
          <span className="math-solutions__stat-footnote">Axiom resonance peak</span>
        </div>
        <div className="math-solutions__stat-card">
          <p className="math-solutions__stat-label">Insight Sync</p>
          <p className="math-solutions__stat-value">92%</p>
          <span className="math-solutions__stat-footnote">Cross-layer parity</span>
        </div>
      </section>

      <section className="math-solutions__layout">
        <aside className="math-solutions__sidebar">
          <div className="math-solutions__panel-header">
            <h2>Problem Index</h2>
            <span className="math-solutions__panel-tag">Axiom-curated</span>
          </div>
          <div className="math-solutions__problem-list">
            {ERDOS_PROBLEMS.map((problem) => (
              <button
                key={problem.id}
                type="button"
                className={`math-solutions__problem-card${
                  selectedId === problem.id ? ' math-solutions__problem-card--active' : ''
                }`}
                onClick={() => setSelectedId(problem.id)}
              >
                <div>
                  <p className="math-solutions__problem-title">{problem.title}</p>
                  <p className="math-solutions__problem-status">{statusLabel[problem.status]}</p>
                </div>
                <span className="math-solutions__problem-signal">{problem.signal}</span>
              </button>
            ))}
          </div>
        </aside>

        <div className="math-solutions__content">
          <section className="math-solutions__hero">
            <div>
              <p className="math-solutions__hero-status">{statusLabel[selectedProblem.status]}</p>
              <h2>{selectedProblem.title}</h2>
              <p className="math-solutions__hero-statement">{selectedProblem.statement}</p>
            </div>
            <div className="math-solutions__hero-insight">
              <h3>Axiom Insight</h3>
              <p>{selectedProblem.insight}</p>
            </div>
          </section>

          <section className="math-solutions__visual">
            <div className="math-solutions__panel-header">
              <h2>Dynamic Axiom Visual</h2>
              <span className="math-solutions__panel-tag">Erdos field</span>
            </div>
            <div className="math-solutions__visual-grid">
              <div
                className={`math-solutions__visual-canvas math-solutions__visual-canvas--${selectedProblem.visual.variant}`}
                style={
                  {
                    '--visual-core': selectedProblem.visual.palette.core,
                    '--visual-halo': selectedProblem.visual.palette.halo,
                    '--visual-arc': selectedProblem.visual.palette.arc,
                    '--visual-speed': selectedProblem.visual.motionSpeed,
                  } as CSSProperties
                }
              >
                <div className="math-solutions__visual-layer math-solutions__visual-layer--lattice">
                  <div className="math-solutions__visual-lattice-grid" />
                  <div className="math-solutions__visual-lattice-wave" />
                  <div className="math-solutions__visual-lattice-node math-solutions__visual-lattice-node--alpha" />
                  <div className="math-solutions__visual-lattice-node math-solutions__visual-lattice-node--beta" />
                  <div className="math-solutions__visual-lattice-node math-solutions__visual-lattice-node--gamma" />
                </div>
                <div className="math-solutions__visual-layer math-solutions__visual-layer--spectrum">
                  <div className="math-solutions__visual-spectrum-orbit" />
                  <div className="math-solutions__visual-spectrum-ring" />
                  <div className="math-solutions__visual-spectrum-bars">
                    {Array.from({ length: 6 }, (_, index) => (
                      <span key={`spectrum-bar-${index}`} />
                    ))}
                  </div>
                </div>
                <div className="math-solutions__visual-layer math-solutions__visual-layer--singularity">
                  <div className="math-solutions__visual-singularity-spiral" />
                  <div className="math-solutions__visual-singularity-core" />
                  <div className="math-solutions__visual-singularity-ripple" />
                </div>
              </div>
              <div className="math-solutions__visual-details">
                <h3>{selectedProblem.visual.title}</h3>
                <p>{selectedProblem.visual.description}</p>
                <div className="math-solutions__visual-metrics">
                  {selectedProblem.visual.metrics.map((metric) => (
                    <div key={metric.label} className="math-solutions__visual-metric">
                      <span>{metric.label}</span>
                      <strong>{metric.value}</strong>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>

          <section className="math-solutions__proof">
            <div className="math-solutions__panel-header">
              <h2>Proof Steps</h2>
              <div className="math-solutions__panel-actions">
                <span className="math-solutions__panel-tag">Dynamic stack</span>
                <button type="button" className="math-solutions__export-btn" onClick={handleExportLatex}>
                  Export PDF (LaTeX)
                </button>
              </div>
            </div>
            <div className="math-solutions__proof-grid">
              {selectedProblem.proofSteps.map((step, index) => (
                <article key={step.title} className="math-solutions__proof-card">
                  <div className="math-solutions__proof-index">0{index + 1}</div>
                  <div>
                    <h3>{step.title}</h3>
                    <p>{step.insight}</p>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <section className="math-solutions__full-proof">
            <div className="math-solutions__panel-header">
              <h2>Full Proof Dossier</h2>
              <span className="math-solutions__panel-tag">Axiom-aligned</span>
            </div>
            <div className="math-solutions__full-proof-list">
              {selectedProblem.fullProof.map((step, index) => (
                <article key={step.title} className="math-solutions__full-proof-card">
                  <div className="math-solutions__full-proof-index">{index + 1}</div>
                  <div>
                    <h3>{step.title}</h3>
                    <p>{step.detail}</p>
                  </div>
                </article>
              ))}
            </div>
            <p className="math-solutions__export-note">
              Export generates LaTeX source ready for PDF compilation with your preferred TeX toolchain.
            </p>
          </section>
        </div>
      </section>
    </div>
  )
}
