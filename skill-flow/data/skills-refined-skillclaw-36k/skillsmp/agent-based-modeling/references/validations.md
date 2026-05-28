# Agent Based Modeling - Validations

## Fixed Agent Update Order

### **Id**
fixed-agent-order
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for\s+agent\s+in\s+agents:\s*\n\s+agent\.(step|update|act)
  - for\s+agent\s+in\s+self\.agents(?!.*shuffle)
### **Message**
Fixed agent order creates synchronization artifacts. Shuffle each step.
### **Fix Action**
Add: np.random.shuffle(agents) or random.shuffle(agents) before loop
### **Applies To**
  - **/*.py

## O(N^2) Neighbor Search

### **Id**
quadratic-neighbor-search
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*agent.*in.*agents.*:\s*\n.*for.*other.*in.*agents
  - for.*in.*agents.*:\s*\n.*distance\(.*,.*\)
### **Message**
O(N^2) neighbor search doesn't scale. Use spatial data structures.
### **Fix Action**
Use cKDTree, spatial hashing, or grid-based lookups
### **Applies To**
  - **/*.py

## ABM Without Reproducible Random Seed

### **Id**
no-random-seed
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class.*Environment.*:(?!.*seed|random_state)
  - def\s+run.*simulation(?!.*seed)
### **Message**
ABM results should be reproducible. Accept and use random seed.
### **Fix Action**
Add seed parameter: def __init__(self, seed=None): self.rng = np.random.default_rng(seed)
### **Applies To**
  - **/*.py

## Missing Boundary Condition Handling

### **Id**
no-boundary-handling
### **Severity**
info
### **Type**
regex
### **Pattern**
  - position\s*\+=.*velocity(?!.*wrap|bound|clamp|periodic)
### **Message**
Agent movement should handle environment boundaries.
### **Fix Action**
Add boundary handling: position = np.clip(position, 0, env_size) or periodic wrap
### **Applies To**
  - **/*.py

## Global Mutable Agent List

### **Id**
global-agent-list
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^agents\s*=\s*\[|^AGENTS\s*=
  - global\s+agents
### **Message**
Global agent list causes issues with multiple simulations.
### **Fix Action**
Use instance variable: self.agents in Environment class
### **Applies To**
  - **/*.py

## Simulation Without Metrics Collection

### **Id**
no-metrics-collection
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def\s+step\(.*\):(?!.*metric|log|record|history)
### **Message**
Collect metrics during simulation for analysis and validation.
### **Fix Action**
Add: self.history.append({'step': self.step, 'population': len(agents), ...})
### **Applies To**
  - **/*.py

## Fully Deterministic Agent Behavior

### **Id**
deterministic-behavior
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def\s+decide\(.*\):(?!.*random|prob|np\.random)
### **Message**
Consider adding stochasticity to agent decisions for realism.
### **Fix Action**
Add exploration: if np.random.random() < epsilon: random_action()
### **Applies To**
  - **/*.py

## ABM Without Validation Against Data

### **Id**
no-validation-data
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class.*Model.*:(?!.*validate|empirical|target)
### **Message**
ABM should be validated against empirical data or known patterns.
### **Fix Action**
Add validation: def validate(self, empirical_data): compare metrics
### **Applies To**
  - **/*.py

## Hardcoded Agent Parameters

### **Id**
hardcoded-parameters
### **Severity**
info
### **Type**
regex
### **Pattern**
  - vision_range\s*=\s*\d+\.?\d*(?!.*config|param)
  - speed\s*=\s*\d+\.?\d*(?!.*config)
### **Message**
Agent parameters should be configurable for sensitivity analysis.
### **Fix Action**
Accept parameters: def __init__(self, config): self.speed = config.speed
### **Applies To**
  - **/*.py

## Drawing Conclusions From Single Run

### **Id**
single-run-analysis
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - result\s*=\s*run_simulation\(\)\s*\n.*print.*result(?!.*replicate|mean)
### **Message**
ABM results are stochastic. Run multiple replications for statistics.
### **Fix Action**
Run replications: results = [run() for _ in range(100)]; report mean, std
### **Applies To**
  - **/*.py