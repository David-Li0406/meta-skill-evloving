# API Reference

Complete API reference for The Universal Axiom implementations.

---

## Core Classes

### UniversalAxiom / Axiom

The main class representing The Universal Axiom intelligence model.

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `impulses` | float | 1.0 | A - Fundamental drives |
| `elements` | float | 1.0 | B - Core components |
| `pressure` | float | 1.0 | C - Constraints and forces |
| `subjectivity` | float | 0.0 | X - Subjectivity level (0=objective, 1=subjective) |
| `purpose` | float | 1.0 | Y - Purpose-driven reasoning strength |
| `time` | float | 1.0 | Z - Temporal continuity |
| `n` | int | 1 | Current iteration/step |

#### Methods

##### `compute_intelligence()` / `computeIntelligence()`
Computes the intelligence value using the complete formula.

**Returns**: `float` - The computed intelligence value

**Formula**: `E_n · (1 + F_n) · X · Y · Z · (A · B · C)`

**Example**:
```python
# Python
intelligence = axiom.compute_intelligence()

// JavaScript
const intelligence = axiom.computeIntelligence();

// Rust
let intelligence = axiom.compute_intelligence();

# Julia
intelligence = compute_intelligence(axiom)
```

---

##### `evolve(delta_time)` / `evolve!(delta_time)`
Evolves the system forward in time by incrementing n and adding to time.

**Parameters**:
- `delta_time` (float, default=1.0): Amount of time to advance

**Returns**: `float` - New intelligence value after evolution

**Effects**:
- Increments `n` by 1
- Adds `delta_time` to cognitive layer's time (Z)
- F_n follows Fibonacci sequence (natural growth)

**Example**:
```python
# Python
new_intelligence = axiom.evolve(delta_time=1.0)

// JavaScript
const newIntelligence = axiom.evolve(1.0);

// Rust
let new_intelligence = axiom.evolve(1.0);

# Julia
new_intelligence = evolve!(axiom, 1.0)
```

---

##### `apply_pressure(pressure_delta)` / `apply_pressure!(pressure_delta)`
Applies a change in pressure, simulating constraints or contradictions.

**Parameters**:
- `pressure_delta` (float): Change in pressure (positive or negative)

**Returns**: `float` - New intelligence value after pressure application

**Effects**:
- Adds `pressure_delta` to foundation layer's pressure (C)
- Ensures pressure stays positive (minimum 0.01)

**Use Cases**:
- Simulating contradictions (positive spike)
- Releasing constraints (negative delta)
- Testing pressure dynamics

**Example**:
```python
# Python
# Contradiction spike
axiom.apply_pressure(2.0)
# Gradual release
axiom.apply_pressure(-0.4)

// JavaScript
axiom.applyPressure(2.0);
axiom.applyPressure(-0.4);

// Rust
axiom.apply_pressure(2.0);
axiom.apply_pressure(-0.4);

# Julia
apply_pressure!(axiom, 2.0)
apply_pressure!(axiom, -0.4)
```

---

##### `adjust_subjectivity(subjectivity_delta)` / `adjust_subjectivity!(subjectivity_delta)`
Adjusts the subjectivity level, moving toward or away from objectivity.

**Parameters**:
- `subjectivity_delta` (float): Change in subjectivity (-1 to +1)

**Returns**: `float` - New intelligence value after adjustment

**Effects**:
- Adds `subjectivity_delta` to cognitive layer's subjectivity (X)
- Clamps result between 0.0 and 1.0
- Intelligence increases as subjectivity decreases (toward objectivity)

**Use Cases**:
- Correcting bias (negative delta → more objective)
- Introducing perspective (positive delta → more subjective)
- Balancing viewpoints

**Example**:
```python
# Python
# Move toward objectivity
axiom.adjust_subjectivity(-0.1)
# Add subjectivity
axiom.adjust_subjectivity(0.2)

// JavaScript
axiom.adjustSubjectivity(-0.1);
axiom.adjustSubjectivity(0.2);

// Rust
axiom.adjust_subjectivity(-0.1);
axiom.adjust_subjectivity(0.2);

# Julia
adjust_subjectivity!(axiom, -0.1)
adjust_subjectivity!(axiom, 0.2)
```

---

##### `strengthen_purpose(purpose_multiplier)` / `strengthen_purpose!(purpose_multiplier)`
Multiplies the purpose strength by a factor.

**Parameters**:
- `purpose_multiplier` (float): Multiplier for purpose (e.g., 1.1 = 10% increase)

**Returns**: `float` - New intelligence value after adjustment

**Effects**:
- Multiplies cognitive layer's purpose (Y) by multiplier
- Ensures purpose stays positive (minimum 0.01)

**Use Cases**:
- Strengthening goal alignment (>1.0)
- Weakening directionless exploration (<1.0)
- Testing purpose sensitivity

**Example**:
```python
# Python
# Strengthen by 20%
axiom.strengthen_purpose(1.2)
# Weaken by 10%
axiom.strengthen_purpose(0.9)

// JavaScript
axiom.strengthenPurpose(1.2);
axiom.strengthenPurpose(0.9);

// Rust
axiom.strengthen_purpose(1.2);
axiom.strengthen_purpose(0.9);

# Julia
strengthen_purpose!(axiom, 1.2)
strengthen_purpose!(axiom, 0.9)
```

---

##### `get_state()` / `getState()`
Returns a complete snapshot of all variables and computed values.

**Returns**: Object/Struct containing:
- `n`: Current iteration
- `foundation`: Object with A, B, C values and product
- `dynamic`: Object with E_n, F_n values and product
- `cognitive`: Object with X, Y, Z values, objectivity, and product
- `intelligence`: Current intelligence value

**Example**:
```python
# Python
state = axiom.get_state()
print(f"Intelligence: {state['intelligence']}")
print(f"Fibonacci: {state['dynamic']['F_n']}")
print(f"Objectivity: {state['cognitive']['X_objectivity']}")

// JavaScript
const state = axiom.getState();
console.log(`Intelligence: ${state.intelligence}`);
console.log(`Fibonacci: ${state.dynamic.F_n}`);
console.log(`Objectivity: ${state.cognitive.X_objectivity}`);

// Rust
let state = axiom.get_state();
println!("Intelligence: {}", state.intelligence);
println!("Fibonacci: {}", state.dynamic.f_n);
println!("Objectivity: {}", state.cognitive.x_objectivity);

# Julia
state = get_state(axiom)
println("Intelligence: ", state.intelligence)
println("Fibonacci: ", state.dynamic.F_n)
println("Objectivity: ", state.cognitive.X_objectivity)
```

---

## Simulator Classes

### AxiomSimulator

Helper class for running scenarios and tracking history.

#### Constructor

```python
# Python
simulator = AxiomSimulator(axiom)

// JavaScript
const simulator = new AxiomSimulator(axiom);

// Rust
let simulator = AxiomSimulator::new(axiom);

# Julia
simulator = AxiomSimulator(axiom)
```

#### Methods

##### `simulate_evolution(steps, delta_time)` / `simulateEvolution(steps, deltaTime)`
Simulates evolution over multiple time steps and records history.

**Parameters**:
- `steps` (int, default=10): Number of evolution steps
- `delta_time` (float, default=1.0): Time increment per step

**Returns**: Array/Vector of AxiomState objects (history)

**Example**:
```python
# Python
history = simulator.simulate_evolution(steps=10, delta_time=1.0)
for i, state in enumerate(history):
    print(f"Step {i}: Intelligence={state['intelligence']:.4f}")

// JavaScript
const history = simulator.simulateEvolution(10, 1.0);
history.forEach((state, i) => {
    console.log(`Step ${i}: Intelligence=${state.intelligence.toFixed(4)}`);
});

// Rust
let history = simulator.simulate_evolution(10, 1.0);
for (i, state) in history.iter().enumerate() {
    println!("Step {}: Intelligence={:.4}", i, state.intelligence);
}

# Julia
history = simulate_evolution(simulator, 10, 1.0)
for (i, state) in enumerate(history)
    println("Step $(i-1): Intelligence=$(round(state.intelligence, digits=4))")
end
```

---

##### `simulate_contradiction_resolution(initial_pressure, resolution_steps)`
Simulates how the system handles and resolves contradictions.

**Parameters**:
- `initial_pressure` (float, default=2.0): Initial pressure spike
- `resolution_steps` (int, default=5): Steps to resolve contradiction

**Returns**: Array/Vector of AxiomState objects showing resolution process

**Process**:
1. Records initial state
2. Applies pressure spike
3. Records pressured state
4. For each resolution step:
   - Reduces subjectivity by 0.1
   - Releases pressure gradually
   - Evolves forward one step
   - Records state

**Example**:
```python
# Python
history = simulator.simulate_contradiction_resolution(
    initial_pressure=2.0,
    resolution_steps=5
)
print(f"Initial pressure: {history[0]['foundation']['C_pressure']}")
print(f"Final pressure: {history[-1]['foundation']['C_pressure']}")
print(f"Initial subjectivity: {history[0]['cognitive']['X_subjectivity']}")
print(f"Final subjectivity: {history[-1]['cognitive']['X_subjectivity']}")

// JavaScript
const history = simulator.simulateContradictionResolution(2.0, 5);
console.log(`Initial pressure: ${history[0].foundation.C_pressure}`);
console.log(`Final pressure: ${history[history.length-1].foundation.C_pressure}`);

// Rust
let history = simulator.simulate_contradiction_resolution(2.0, 5);
println!("Initial pressure: {}", history[0].foundation.c_pressure);
println!("Final pressure: {}", history.last().unwrap().foundation.c_pressure);

# Julia
history = simulate_contradiction_resolution(simulator, 2.0, 5)
println("Initial pressure: ", history[1].foundation.C_pressure)
println("Final pressure: ", history[end].foundation.C_pressure)
```

---

##### `get_coherence_metric()` / `getCoherenceMetric()`
Calculates a coherence score based on component balance.

**Returns**: `float` - Coherence score (0.0 to 1.0)

**Formula**:
```
coherence = (objectivity_score + purpose_score + pressure_score) / 3

where:
  objectivity_score = 1 - subjectivity
  purpose_score = min(purpose / 2.0, 1.0)
  pressure_score = 1.0 / (1.0 + |pressure - 1.0|)
```

**Interpretation**:
- High coherence (>0.7): Well-balanced, objective, purposeful
- Medium coherence (0.4-0.7): Functional but improvable
- Low coherence (<0.4): Imbalanced, needs adjustment

**Example**:
```python
# Python
coherence = simulator.get_coherence_metric()
print(f"System coherence: {coherence:.4f}")

// JavaScript
const coherence = simulator.getCoherenceMetric();
console.log(`System coherence: ${coherence.toFixed(4)}`);

// Rust
let coherence = simulator.get_coherence_metric();
println!("System coherence: {:.4}", coherence);

# Julia
coherence = get_coherence_metric(simulator)
println("System coherence: $(round(coherence, digits=4))")
```

---

## Utility Functions

### `fibonacci_sequence(n)` / `fibonacciSequence(n)`
Generates Fibonacci sequence up to n terms.

**Parameters**:
- `n` (int): Number of terms to generate

**Returns**: Array/Vector of Fibonacci numbers

**Example**:
```python
# Python
from universal_axiom import fibonacci_sequence
seq = fibonacci_sequence(10)
# [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

// JavaScript
import { fibonacciSequence } from './universal-axiom';
const seq = fibonacciSequence(10);
// [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

// Rust
use universal_axiom::fibonacci_sequence;
let seq = fibonacci_sequence(10);
// vec![1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

# Julia
using .UniversalAxiom
seq = fibonacci_sequence(10)
# [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

---

## Layer Classes

### FoundationLayer

Represents the foundation layer: A · B · C

**Properties**:
- `impulses` (A): Fundamental drives
- `elements` (B): Core components
- `pressure` (C): Constraints and forces

**Methods**:
- `compute()`: Returns A × B × C

---

### DynamicLayer

Represents the dynamic layer: E_n · (1 + F_n)

**Properties**:
- `n`: Current iteration
- `base_exponential`: Base for exponential growth (default: 3)

**Methods**:
- `exponential_growth()`: Returns 2 × base^n - 1
- `fibonacci()`: Returns nth Fibonacci number (1, 1, 2, 3, ...)
- `compute()`: Returns E_n × (1 + F_n)

---

### CognitiveLayer

Represents the cognitive layer: X · Y · Z

**Properties**:
- `subjectivity` (X): Subjectivity level (0-1)
- `purpose` (Y): Purpose strength
- `time` (Z): Temporal value

**Methods**:
- `compute()`: Returns (1-X) × Y × Z
- `objectivity()`: Returns 1 - subjectivity

---

## Type Definitions

### AxiomState

Complete state snapshot returned by `get_state()`.

**Structure**:
```typescript
{
  n: number,
  foundation: {
    A_impulses: number,
    B_elements: number,
    C_pressure: number,
    product: number
  },
  dynamic: {
    E_n: number,
    F_n: number,
    product: number
  },
  cognitive: {
    X_subjectivity: number,
    X_objectivity: number,
    Y_purpose: number,
    Z_time: number,
    product: number
  },
  intelligence: number
}
```

---

## Best Practices

### 1. Initialization
Always start with sensible defaults:
```python
axiom = UniversalAxiom(
    impulses=1.0,      # Neutral drive
    elements=1.0,      # Neutral components
    pressure=1.0,      # Moderate constraints
    subjectivity=0.0,  # Start objective
    purpose=1.0,       # Clear purpose
    time=1.0,          # Start time
    n=1                # First iteration
)
```

### 2. Gradual Changes
Make incremental adjustments:
```python
# Good: Gradual adjustment
axiom.adjust_subjectivity(-0.1)

# Avoid: Extreme jumps
axiom.adjust_subjectivity(-0.9)
```

### 3. Monitor Coherence
Track system balance:
```python
simulator = AxiomSimulator(axiom)
coherence = simulator.get_coherence_metric()
if coherence < 0.5:
    # System needs rebalancing
    axiom.adjust_subjectivity(-0.1)
```

### 4. Use Simulation for Exploration
Test scenarios before production:
```python
simulator = AxiomSimulator(axiom)
history = simulator.simulate_evolution(100, 1.0)
# Analyze history before committing to changes
```

---

## Error Handling

All implementations ensure:
- Pressure never goes below 0.01
- Subjectivity clamped to [0.0, 1.0]
- Purpose never goes below 0.01
- Time always increases (TimeSphere irreversibility)

Invalid inputs are automatically corrected rather than raising errors.

---

## Performance Tips

### Python
- Use NumPy arrays for batch operations
- Profile with cProfile for bottlenecks
- Consider Cython for performance-critical sections

### JavaScript
- Batch state updates
- Use Web Workers for heavy simulations
- Consider WASM compilation for performance

### Rust
- Use release builds (`cargo build --release`)
- Enable LTO for maximum optimization
- Profile with perf/flamegraph

### Julia
- Let functions warm up (JIT compilation)
- Use @time macro for benchmarking
- Avoid global variables in loops

---

## Integration Examples

### With LLMs (Python)
```python
def enhance_llm_with_axiom(llm_output, context):
    axiom = UniversalAxiom(
        subjectivity=detect_bias(llm_output),
        purpose=extract_intent(context),
        pressure=measure_contradiction(llm_output)
    )

    coherence = AxiomSimulator(axiom).get_coherence_metric()

    if coherence < 0.5:
        # Re-prompt with objectivity guidance
        return refine_output(llm_output, axiom.get_state())

    return llm_output
```

### Real-time Systems (Rust)
```rust
fn process_input(input: &Input) -> Response {
    let mut axiom = UniversalAxiom::new();

    // Update based on input
    axiom.apply_pressure(calculate_pressure(input));
    axiom.adjust_subjectivity(detect_bias(input));

    // Evolve
    let intelligence = axiom.evolve(1.0);

    generate_response(intelligence, axiom.get_state())
}
```

---

## Further Reading

- [Implementation Guide](../IMPLEMENTATION.md)
- [Framework Documentation](../framework/)
- [Examples Directory](../../examples/)
