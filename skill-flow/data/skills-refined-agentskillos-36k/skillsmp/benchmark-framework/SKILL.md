---
name: benchmark-framework
description: Rigorous A/B/C testing framework for empirically evaluating reasoning patterns. Use when you need data-driven pattern selection, want to quantify trade-offs between patterns, or need to validate claims about which cognitive methodology performs best. Enables scientific measurement of quality, cost, and time trade-offs across ToT, BoT, SRC, HE, AR, DR, AT, RTR, and NDF patterns.
license: MIT
---

# Cognitive Skills Benchmarking Framework

## Overview

A rigorous framework for A/B/C testing reasoning patterns to empirically determine which cognitive methodologies perform best across problem categories. This framework enables data-driven pattern selection rather than heuristic-based choices.

## Why Benchmark?

Different reasoning patterns (ToT, BoT, SRC, HE, AR, DR, AT, RTR, NDF) claim different strengths, but without empirical measurement:
- We cannot validate these claims
- We cannot quantify trade-offs (quality vs. cost vs. time)
- We cannot track improvement over time
- Pattern selection remains subjective

This framework provides scientific rigor to cognitive skill evaluation.

---

## Benchmark Structure

### Problem Set Organization

```
benchmark-problems/
├── optimization/           # ToT territory
│   ├── easy/              # 5-10 min problems
│   ├── medium/            # 15-30 min problems
│   └── hard/              # 30-60 min problems
├── exploration/           # BoT territory
│   ├── easy/
│   ├── medium/
│   └── hard/
├── diagnosis/             # HE territory
│   ├── easy/
│   ├── medium/
│   └── hard/
├── security/              # AR territory
│   ├── easy/
│   ├── medium/
│   └── hard/
├── tradeoffs/             # DR territory
│   ├── easy/
│   ├── medium/
│   └── hard/
├── novel/                 # AT territory
│   ├── easy/
│   ├── medium/
│   └── hard/
├── time-critical/         # RTR territory
│   ├── easy/
│   ├── medium/
│   └── hard/
└── stakeholder/           # NDF territory
    ├── easy/
    ├── medium/
    └── hard/
```

### Problem Definition Schema

```yaml
# problem-template.yaml
problem_id: "OPT-001"
domain: "optimization"
difficulty: "medium"
title: "API Rate Limiter Design"
description: |
  Design a rate limiting system for a public API that handles
  10,000 requests/second with fair distribution across users.

context:
  constraints:
    - "Must handle burst traffic gracefully"
    - "Sub-millisecond latency requirement"
    - "Distributed deployment across 5 regions"
  resources:
    - "Redis cluster available"
    - "Current architecture uses nginx"

evaluation_criteria:
  - criterion: "Scalability"
    weight: 0.3
    rubric: |
      5: Handles 10x traffic with linear cost
      4: Handles 5x traffic efficiently
      3: Handles 2x traffic
      2: Handles current load only
      1: Cannot meet requirements

  - criterion: "Fairness"
    weight: 0.25
    rubric: |
      5: Per-user fairness with adaptive limits
      4: Per-user fairness with fixed limits
      3: Global fairness only
      2: Basic fairness, exploitable
      1: No fairness consideration

  - criterion: "Implementability"
    weight: 0.25
    rubric: |
      5: Clear implementation path, <1 week
      4: Implementation path, 1-2 weeks
      3: Requires some research, 2-4 weeks
      2: Significant unknowns
      1: Impractical to implement

  - criterion: "Operational Simplicity"
    weight: 0.2
    rubric: |
      5: Self-healing, minimal ops burden
      4: Standard monitoring/alerting sufficient
      3: Requires dedicated monitoring
      2: High operational complexity
      1: Operational nightmare

ground_truth:
  known_good_solutions:
    - "Token bucket with Redis MULTI/EXEC"
    - "Sliding window log with sorted sets"
  common_pitfalls:
    - "Race conditions in distributed counting"
    - "Memory explosion with naive approaches"
  expert_rating: 4.2  # If available

tags:
  - "distributed-systems"
  - "performance"
  - "redis"
```

---

## Metrics Framework

### Core Metrics

| Metric | Type | Range | Description |
|--------|------|-------|-------------|
| **Quality Score** | Aggregate | 0-100 | Weighted sum of evaluation criteria |
| **Confidence** | Self-reported | 0-100% | Pattern's reported confidence in solution |
| **Token Cost** | Integer | 0-∞ | Total tokens consumed (input + output) |
| **Execution Time** | Duration | ms | Wall-clock time to solution |
| **Correctness** | Binary/Partial | 0-1 | Does solution actually work? |
| **Completeness** | Percentage | 0-100% | How much of the problem addressed? |
| **Human Preference** | Rank | 1-N | Human ranking among alternatives |

### Quality Score Calculation

```python
def calculate_quality_score(solution, criteria):
    """
    Calculate weighted quality score from rubric evaluations.

    Args:
        solution: The solution being evaluated
        criteria: List of (criterion, weight, score) tuples

    Returns:
        Quality score 0-100
    """
    weighted_sum = 0
    total_weight = 0

    for criterion, weight, score in criteria:
        # Score is 1-5, normalize to 0-20, then weight
        normalized = (score - 1) * 25  # 1->0, 5->100
        weighted_sum += normalized * weight
        total_weight += weight

    return weighted_sum / total_weight if total_weight > 0 else 0
```

### Efficiency Metrics

```python
@dataclass
class EfficiencyMetrics:
    tokens_per_quality_point: float  # Lower is better
    time_per_quality_point: float    # Lower is better
    quality_per_minute: float        # Higher is better

    @classmethod
    def calculate(cls, quality: float, tokens: int, time_ms: int):
        return cls(
            tokens_per_quality_point=tokens / max(quality, 1),
            time_per_quality_point=time_ms / max(quality, 1),
            quality_per_minute=(quality * 60000) / max(time_ms, 1)
        )
```

### Confidence Calibration

Track how well self-reported confidence predicts actual quality:

```python
def calibration_score(predictions: List[Tuple[float, float]]) -> float:
    """
    Calculate calibration: does confidence predict quality?

    Args:
        predictions: List of (confidence, actual_quality) pairs

    Returns:
        Calibration score (-1 to 1, 1 is perfect)
    """
    if len(predictions) < 10:
        return None  # Insufficient data

    # Bin by confidence and compare to actual
    bins = defaultdict(list)
    for conf, quality in predictions:
        bin_key = int(conf // 10) * 10  # 0-10, 10-20, etc.
        bins[bin_key].append(quality)

    errors = []
    for bin_center, qualities in bins.items():
        expected = bin_center + 5  # Center of bin
        actual = sum(qualities) / len(qualities)
        errors.append(abs(expected - actual))

    # Average error, inverted and normalized
    avg_error = sum(errors) / len(errors) if errors else 50
    return 1 - (avg_error / 50)  # 0 error -> 1, 50 error -> 0
```

---

## A/B/C Testing Protocol

### Experimental Design

```yaml
experiment:
  id: "EXP-2024-001"
  hypothesis: "ToT outperforms BoT on optimization problems"

  conditions:
    - name: "baseline"
      pattern: "direct_analysis"
      description: "No specialized pattern"

    - name: "condition_a"
      pattern: "tree_of_thoughts"
      description: "ToT with default parameters"

    - name: "condition_b"
      pattern: "breadth_of_thought"
      description: "BoT with default parameters"

    - name: "condition_c"
      pattern: "tree_of_thoughts"
      parameters:
        max_branches: 5
        pruning_threshold: 0.6
      description: "ToT with aggressive pruning"

  problem_set:
    domain: "optimization"
    difficulties: ["medium", "hard"]
    sample_size: 30  # Problems per condition

  randomization:
    seed: 42
    counterbalancing: true  # Vary problem order

  controls:
    temperature: 0.7  # Fixed across conditions
    max_tokens: 8000  # Fixed across conditions
    time_limit: 300000  # 5 minutes per problem
```

### Statistical Requirements

#### Sample Size Calculation

```python
def required_sample_size(
    effect_size: float = 0.5,  # Cohen's d
    alpha: float = 0.05,       # Significance level
    power: float = 0.80        # Statistical power
) -> int:
    """
    Calculate minimum sample size for meaningful comparison.

    For quality score comparisons (continuous 0-100):
    - Small effect (d=0.2): n=393 per condition
    - Medium effect (d=0.5): n=64 per condition
    - Large effect (d=0.8): n=26 per condition
    """
    from scipy import stats

    # Two-tailed t-test
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)

    n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
    return int(np.ceil(n))
```

#### Minimum Requirements

| Comparison Type | Minimum N | Statistical Test |
|-----------------|-----------|------------------|
| Two patterns | 30/condition | Independent t-test |
| Multiple patterns | 30/condition | ANOVA + Tukey HSD |
| Paired (same problem) | 20 problems | Paired t-test |
| Win/loss record | 50 comparisons | Sign test |

### Confound Control

```yaml
confound_controls:
  # Problem-level controls
  problem_randomization:
    enabled: true
    seed_per_experiment: true

  # Order effects
  counterbalancing:
    method: "latin_square"
    wash_out_period: true  # Clear context between conditions

  # LLM variability
  temperature_control:
    fixed_temperature: 0.7
    multiple_runs: 3  # Run each problem 3x, average

  # Time effects
  session_controls:
    max_problems_per_session: 10
    break_between_conditions: true

  # Evaluator bias
  blind_evaluation:
    enabled: true
    solutions_anonymized: true
    random_order: true
```

### Running an A/B/C Test

```python
async def run_abc_test(experiment_config: dict) -> ExperimentResults:
    """
    Execute A/B/C test according to protocol.
    """
    results = ExperimentResults(experiment_id=experiment_config['id'])

    # Load problem set
    problems = load_problems(
        domain=experiment_config['problem_set']['domain'],
        difficulties=experiment_config['problem_set']['difficulties']
    )

    # Randomize
    random.seed(experiment_config['randomization']['seed'])
    random.shuffle(problems)

    # Sample required number
    problems = problems[:experiment_config['problem_set']['sample_size']]

    for problem in problems:
        problem_results = {}

        for condition in experiment_config['conditions']:
            # Clear context (wash-out)
            await clear_context()

            # Run pattern
            start_time = time.time()
            solution = await run_pattern(
                pattern=condition['pattern'],
                parameters=condition.get('parameters', {}),
                problem=problem,
                controls=experiment_config['controls']
            )
            execution_time = time.time() - start_time

            # Collect metrics
            problem_results[condition['name']] = {
                'solution': solution,
                'quality_score': evaluate_quality(solution, problem),
                'confidence': solution.confidence,
                'tokens': solution.token_count,
                'execution_time': execution_time,
                'correctness': verify_correctness(solution, problem)
            }

        results.add_problem_results(problem.id, problem_results)

    # Statistical analysis
    results.analyze()

    return results
```

---

## Problem Categories

### 1. Optimization Problems (ToT Territory)

**Characteristics**: Single best solution, prunable search space, clear evaluation criteria.

```yaml
example_problems:
  - id: "OPT-001"
    title: "Database Query Optimization"
    type: "performance"

  - id: "OPT-002"
    title: "Memory Allocation Strategy"
    type: "resource"

  - id: "OPT-003"
    title: "API Response Caching"
    type: "architecture"

expected_pattern_performance:
  tree_of_thoughts: "primary"
  breadth_of_thought: "secondary"
  direct_analysis: "baseline"
```

### 2. Exploration Problems (BoT Territory)

**Characteristics**: Multiple valid solutions, unknown solution space, need diversity.

```yaml
example_problems:
  - id: "EXP-001"
    title: "Architecture Options for New Service"
    type: "greenfield"

  - id: "EXP-002"
    title: "Possible Causes of Intermittent Bug"
    type: "diagnostic"

  - id: "EXP-003"
    title: "Migration Strategy Alternatives"
    type: "strategic"

expected_pattern_performance:
  breadth_of_thought: "primary"
  tree_of_thoughts: "secondary"
  direct_analysis: "baseline"
```

### 3. Diagnosis Problems (HE Territory)

**Characteristics**: Information uncertainty, need for multiple hypotheses, testing required.

```yaml
example_problems:
  - id: "DIA-001"
    title: "Production Latency Spike Investigation"
    type: "performance"

  - id: "DIA-002"
    title: "Data Inconsistency Root Cause"
    type: "data"

  - id: "DIA-003"
    title: "Memory Leak Identification"
    type: "resource"

expected_pattern_performance:
  hypothesis_engine: "primary"
  self_reflecting_chain: "secondary"
  direct_analysis: "baseline"
```

### 4. Security Problems (AR Territory)

**Characteristics**: Adversarial thinking, attack vectors, defense in depth.

```yaml
example_problems:
  - id: "SEC-001"
    title: "Authentication Flow Security Review"
    type: "authentication"

  - id: "SEC-002"
    title: "API Endpoint Vulnerability Assessment"
    type: "api_security"

  - id: "SEC-003"
    title: "Data Encryption Strategy"
    type: "data_protection"

expected_pattern_performance:
  adversarial_reasoning: "primary"
  hypothesis_engine: "secondary"
  direct_analysis: "baseline"
```

### 5. Trade-off Problems (DR Territory)

**Characteristics**: Competing values, no perfect solution, stakeholder tensions.

```yaml
example_problems:
  - id: "TRD-001"
    title: "Consistency vs. Availability Trade-off"
    type: "cap_theorem"

  - id: "TRD-002"
    title: "Technical Debt vs. Feature Velocity"
    type: "strategic"

  - id: "TRD-003"
    title: "Privacy vs. Personalization"
    type: "product"

expected_pattern_performance:
  dialectical_reasoning: "primary"
  negotiated_decision: "secondary"
  direct_analysis: "baseline"
```

### 6. Novel Problems (AT Territory)

**Characteristics**: No established approaches, requires creativity, analogical thinking.

```yaml
example_problems:
  - id: "NOV-001"
    title: "AI-Native UX Paradigm"
    type: "design"

  - id: "NOV-002"
    title: "Cross-Domain Integration Pattern"
    type: "architecture"

  - id: "NOV-003"
    title: "Emergent Technology Application"
    type: "strategic"

expected_pattern_performance:
  analogical_transfer: "primary"
  breadth_of_thought: "secondary"
  direct_analysis: "baseline"
```

### 7. Time-Critical Problems (RTR Territory)

**Characteristics**: Minutes not hours, good enough now, actionable immediately.

```yaml
example_problems:
  - id: "RTR-001"
    title: "Production Incident Triage"
    type: "incident"

  - id: "RTR-002"
    title: "Deadline-Driven Decision"
    type: "strategic"

  - id: "RTR-003"
    title: "Security Breach Response"
    type: "security"

expected_pattern_performance:
  rapid_triage_reasoning: "primary"
  direct_analysis: "secondary"
  tree_of_thoughts: "too_slow"
```

### 8. Stakeholder Problems (NDF Territory)

**Characteristics**: Multiple parties, competing interests, need consensus.

```yaml
example_problems:
  - id: "STK-001"
    title: "Cross-Team Resource Allocation"
    type: "organizational"

  - id: "STK-002"
    title: "Feature Prioritization Conflict"
    type: "product"

  - id: "STK-003"
    title: "Architecture Decision with Team Buy-in"
    type: "technical"

expected_pattern_performance:
  negotiated_decision: "primary"
  dialectical_reasoning: "secondary"
  direct_analysis: "baseline"
```

---

## Benchmark Reporting

### Pattern Performance Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PATTERN PERFORMANCE MATRIX                                │
│                    Experiment: EXP-2024-001                                  │
│                    Problems: 240 (30 per category)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Domain          │ ToT   │ BoT   │ SRC   │ HE    │ AR    │ DR    │ Direct  │
│  ────────────────┼───────┼───────┼───────┼───────┼───────┼───────┼─────────│
│  Optimization    │ 82.3* │ 71.2  │ 68.4  │ 65.1  │ 62.3  │ 64.8  │ 58.2    │
│  Exploration     │ 69.1  │ 84.7* │ 72.3  │ 74.2  │ 68.9  │ 71.5  │ 55.3    │
│  Diagnosis       │ 71.4  │ 73.8  │ 78.2  │ 85.6* │ 72.1  │ 69.4  │ 61.7    │
│  Security        │ 68.9  │ 71.2  │ 74.5  │ 76.3  │ 86.2* │ 70.8  │ 57.9    │
│  Trade-offs      │ 65.4  │ 72.1  │ 70.3  │ 68.7  │ 71.2  │ 83.9* │ 54.6    │
│  Novel           │ 62.8  │ 78.4  │ 71.6  │ 69.2  │ 65.7  │ 72.3  │ 51.2    │
│  Time-critical   │ 48.2  │ 45.6  │ 52.3  │ 55.1  │ 51.8  │ 49.7  │ 62.4    │
│  Stakeholder     │ 64.7  │ 71.3  │ 68.9  │ 70.2  │ 69.5  │ 78.4  │ 52.8    │
│  ────────────────┼───────┼───────┼───────┼───────┼───────┼───────┼─────────│
│  OVERALL         │ 66.6  │ 71.0  │ 69.6  │ 70.6  │ 68.5  │ 70.1  │ 56.8    │
│                                                                              │
│  * = Best in category (p < 0.05)                                            │
│  Quality scores normalized 0-100                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Win/Loss Records

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HEAD-TO-HEAD RECORDS                                 │
│                         (wins-losses-ties)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│              │ ToT      │ BoT      │ SRC      │ HE       │ Direct   │       │
│  ────────────┼──────────┼──────────┼──────────┼──────────┼──────────│       │
│  ToT         │    -     │ 98-127-15│ 112-108-20│ 105-118-17│ 178-52-10│       │
│  BoT         │ 127-98-15│    -     │ 124-103-13│ 119-108-13│ 189-42-9 │       │
│  SRC         │ 108-112-20│103-124-13│    -     │ 115-112-13│ 175-58-7 │       │
│  HE          │ 118-105-17│108-119-13│ 112-115-13│    -     │ 182-48-10│       │
│  Direct      │ 52-178-10│ 42-189-9 │ 58-175-7 │ 48-182-10│    -     │       │
│                                                                              │
│  Statistical significance: Chi-square test, p < 0.05 for all vs Direct      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Cost-Quality Trade-offs

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      COST-QUALITY ANALYSIS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Pattern    │ Avg Quality │ Avg Tokens │ Tokens/Point │ ROI vs Direct │     │
│  ───────────┼─────────────┼────────────┼──────────────┼───────────────│     │
│  Direct     │    56.8     │    2,100   │     37.0     │     1.00x     │     │
│  ToT        │    66.6     │    8,500   │    127.6     │     0.29x     │     │
│  BoT        │    71.0     │   12,200   │    171.8     │     0.22x     │     │
│  SRC        │    69.6     │    6,400   │     92.0     │     0.40x     │     │
│  HE         │    70.6     │    7,800   │    110.5     │     0.34x     │     │
│  AR         │    68.5     │    9,100   │    132.8     │     0.28x     │     │
│  DR         │    70.1     │    8,900   │    127.0     │     0.29x     │     │
│                                                                              │
│  ROI = Quality improvement per token spent (relative to Direct)              │
│  Higher ROI = more efficient pattern                                         │
│                                                                              │
│  RECOMMENDATION: SRC offers best efficiency for moderate quality gains       │
│                  BoT/HE justified when problem fits their specialty          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Report Template

```markdown
# Benchmark Report: [Experiment ID]

## Executive Summary
- **Best Overall Pattern**: [Pattern] (avg quality: X)
- **Most Efficient Pattern**: [Pattern] (tokens/point: X)
- **Biggest Surprise**: [Finding that contradicted expectations]
- **Key Recommendation**: [Actionable insight]

## Methodology
- Problems tested: [N]
- Patterns compared: [List]
- Statistical tests: [Tests used]
- Significance level: α = 0.05

## Results by Category

### [Category 1]
| Pattern | Quality | Tokens | Time | Sig |
|---------|---------|--------|------|-----|
| ...     | ...     | ...    | ...  | ... |

**Winner**: [Pattern] (p = X)
**Analysis**: [Why this pattern excelled]

[Repeat for each category]

## Statistical Analysis

### ANOVA Results
- F-statistic: X
- p-value: X
- Effect size (η²): X

### Post-hoc Comparisons (Tukey HSD)
[Significant pairwise differences]

## Limitations
- [Sample size constraints]
- [Problem selection bias]
- [Evaluator variability]

## Recommendations
1. [Primary recommendation]
2. [Secondary recommendation]
3. [Areas for further research]

## Appendix: Raw Data
[Link to detailed results]
```

---

## ChromaDB Integration

### Schema Definition

```python
# Benchmark results collection
BENCHMARK_SCHEMA = {
    "collection_name": "cognitive_benchmarks",
    "embedding_function": "sentence-transformers/all-MiniLM-L6-v2",
    "metadata_schema": {
        "experiment_id": "string",
        "problem_id": "string",
        "pattern": "string",
        "domain": "string",
        "difficulty": "string",
        "quality_score": "float",
        "confidence": "float",
        "tokens": "int",
        "execution_time_ms": "int",
        "correctness": "float",
        "timestamp": "datetime",
        "session_id": "string"
    }
}
```

### Storage Operations

```python
import chromadb
from datetime import datetime
from typing import List, Dict, Any

class BenchmarkStore:
    def __init__(self, persist_directory: str = "./benchmark_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="cognitive_benchmarks",
            metadata={"description": "Cognitive pattern benchmark results"}
        )

    def store_result(self, result: Dict[str, Any]) -> str:
        """Store a single benchmark result."""
        doc_id = f"{result['experiment_id']}_{result['problem_id']}_{result['pattern']}"

        # Create searchable document text
        document = f"""
        Pattern: {result['pattern']}
        Domain: {result['domain']}
        Problem: {result['problem_id']}
        Quality: {result['quality_score']}
        Solution summary: {result.get('solution_summary', '')}
        """

        self.collection.upsert(
            ids=[doc_id],
            documents=[document],
            metadatas=[{
                "experiment_id": result['experiment_id'],
                "problem_id": result['problem_id'],
                "pattern": result['pattern'],
                "domain": result['domain'],
                "difficulty": result['difficulty'],
                "quality_score": result['quality_score'],
                "confidence": result['confidence'],
                "tokens": result['tokens'],
                "execution_time_ms": result['execution_time_ms'],
                "correctness": result['correctness'],
                "timestamp": datetime.now().isoformat(),
                "session_id": result.get('session_id', 'default')
            }]
        )

        return doc_id

    def store_experiment(self, experiment_results: List[Dict[str, Any]]) -> int:
        """Store all results from an experiment."""
        count = 0
        for result in experiment_results:
            self.store_result(result)
            count += 1
        return count

    def query_pattern_performance(
        self,
        pattern: str,
        domain: str = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Query historical performance for a pattern."""
        where_clause = {"pattern": pattern}
        if domain:
            where_clause = {
                "$and": [
                    {"pattern": pattern},
                    {"domain": domain}
                ]
            }

        results = self.collection.query(
            query_texts=[f"pattern {pattern} performance"],
            where=where_clause,
            n_results=limit
        )

        return results['metadatas'][0] if results['metadatas'] else []

    def get_improvement_trend(
        self,
        pattern: str,
        domain: str,
        window_days: int = 30
    ) -> Dict[str, float]:
        """Calculate performance trend over time."""
        results = self.query_pattern_performance(pattern, domain, limit=1000)

        if len(results) < 10:
            return {"trend": None, "insufficient_data": True}

        # Sort by timestamp
        sorted_results = sorted(results, key=lambda x: x['timestamp'])

        # Split into early and recent
        midpoint = len(sorted_results) // 2
        early_avg = sum(r['quality_score'] for r in sorted_results[:midpoint]) / midpoint
        recent_avg = sum(r['quality_score'] for r in sorted_results[midpoint:]) / (len(sorted_results) - midpoint)

        return {
            "early_average": early_avg,
            "recent_average": recent_avg,
            "improvement": recent_avg - early_avg,
            "improvement_pct": ((recent_avg - early_avg) / early_avg) * 100,
            "sample_size": len(sorted_results)
        }

    def compare_sessions(
        self,
        session_a: str,
        session_b: str
    ) -> Dict[str, Any]:
        """Compare performance across sessions."""
        results_a = self.collection.get(
            where={"session_id": session_a}
        )
        results_b = self.collection.get(
            where={"session_id": session_b}
        )

        # Aggregate by pattern
        def aggregate(results):
            by_pattern = {}
            for meta in results['metadatas']:
                pattern = meta['pattern']
                if pattern not in by_pattern:
                    by_pattern[pattern] = []
                by_pattern[pattern].append(meta['quality_score'])
            return {p: sum(s)/len(s) for p, s in by_pattern.items()}

        agg_a = aggregate(results_a)
        agg_b = aggregate(results_b)

        comparison = {}
        for pattern in set(agg_a.keys()) | set(agg_b.keys()):
            comparison[pattern] = {
                "session_a": agg_a.get(pattern, None),
                "session_b": agg_b.get(pattern, None),
                "difference": (agg_b.get(pattern, 0) - agg_a.get(pattern, 0))
                    if pattern in agg_a and pattern in agg_b else None
            }

        return comparison
```

### Query Patterns

```python
# Find best pattern for a domain
def recommend_pattern(store: BenchmarkStore, domain: str) -> str:
    patterns = ["ToT", "BoT", "SRC", "HE", "AR", "DR", "AT", "RTR", "NDF"]

    best_pattern = None
    best_score = 0

    for pattern in patterns:
        results = store.query_pattern_performance(pattern, domain)
        if results:
            avg_score = sum(r['quality_score'] for r in results) / len(results)
            if avg_score > best_score:
                best_score = avg_score
                best_pattern = pattern

    return best_pattern

# Track calibration over time
def calibration_trend(store: BenchmarkStore, pattern: str) -> Dict:
    results = store.query_pattern_performance(pattern, limit=500)

    predictions = [(r['confidence'], r['quality_score']) for r in results]

    # Calculate calibration for different time periods
    # ... (implementation as before)

    return {"pattern": pattern, "calibration_history": [...]}
```

---

## Templates

### Running a Benchmark

```yaml
# benchmark-run-template.yaml
benchmark_run:
  experiment_id: "EXP-YYYY-NNN"
  date: "YYYY-MM-DD"
  operator: "[Name]"

  configuration:
    patterns_under_test:
      - name: "tree_of_thoughts"
        version: "1.0"
        parameters: {}

    baseline:
      name: "direct_analysis"

    problem_set:
      source: "benchmark-problems/optimization/"
      selection: "random"
      count: 30

    controls:
      temperature: 0.7
      max_tokens: 8000
      runs_per_problem: 3

  execution_checklist:
    - [ ] Problem set loaded and verified
    - [ ] Patterns configured correctly
    - [ ] ChromaDB connection verified
    - [ ] Evaluation rubrics reviewed
    - [ ] Blind evaluation setup complete

  notes: |
    [Pre-run observations and expectations]
```

### Recording Results

```yaml
# result-template.yaml
result:
  problem_id: "OPT-001"
  pattern: "tree_of_thoughts"
  run_number: 1

  solution:
    summary: "[Brief description of solution approach]"
    full_response: "[Complete pattern output]"

  raw_metrics:
    tokens_input: 2500
    tokens_output: 3200
    execution_time_ms: 45000
    self_reported_confidence: 85

  evaluation:
    evaluator: "[Name or 'blind']"

    criteria_scores:
      - criterion: "Scalability"
        score: 4
        justification: "[Why this score]"

      - criterion: "Implementability"
        score: 5
        justification: "[Why this score]"

    correctness_check:
      verified: true
      method: "[How verified - test, review, etc.]"
      issues_found: []

    calculated_quality: 82.5

  notes: |
    [Observations about this run]
```

### Experiment Summary

```yaml
# experiment-summary-template.yaml
experiment_summary:
  experiment_id: "EXP-YYYY-NNN"
  status: "completed"
  completion_date: "YYYY-MM-DD"

  overview:
    total_problems: 90
    total_runs: 270
    patterns_tested: 3

  aggregate_results:
    by_pattern:
      tree_of_thoughts:
        mean_quality: 82.3
        std_quality: 8.7
        mean_tokens: 5800
        mean_time_ms: 42000

      breadth_of_thought:
        mean_quality: 71.2
        std_quality: 12.4
        mean_tokens: 8200
        mean_time_ms: 58000

      direct_analysis:
        mean_quality: 58.2
        std_quality: 15.1
        mean_tokens: 2100
        mean_time_ms: 18000

  statistical_tests:
    anova:
      f_statistic: 24.7
      p_value: 0.00001
      significant: true

    pairwise:
      - comparison: "ToT vs Direct"
        difference: 24.1
        p_value: 0.00001
        significant: true

      - comparison: "ToT vs BoT"
        difference: 11.1
        p_value: 0.003
        significant: true

  conclusions:
    winner: "tree_of_thoughts"
    key_finding: |
      ToT significantly outperformed both BoT and Direct analysis
      on optimization problems, with a large effect size (d=1.2).

    caveats:
      - "Limited to optimization domain"
      - "Single difficulty level tested"

    recommendations:
      - "Use ToT as default for optimization problems"
      - "Extend testing to other domains"
      - "Investigate ToT parameter sensitivity"

  chromadb_stored: true
  storage_ids: ["EXP-YYYY-NNN_*"]
```

---

## Best Practices

### Problem Design
1. **Clear evaluation criteria**: Every problem must have explicit rubrics
2. **Known baselines**: Include problems with known good solutions
3. **Difficulty calibration**: Pre-test problems to verify difficulty ratings
4. **Domain balance**: Equal representation across categories

### Test Execution
1. **Randomization**: Always randomize problem order
2. **Wash-out periods**: Clear context between conditions
3. **Multiple runs**: Run each problem 3x minimum for reliability
4. **Blind evaluation**: Anonymize solutions before scoring

### Analysis
1. **Statistical rigor**: Report confidence intervals, not just means
2. **Effect sizes**: Cohen's d alongside p-values
3. **Practical significance**: Is the difference meaningful?
4. **Honest limitations**: Acknowledge constraints

### Reporting
1. **Reproducibility**: Include all configuration details
2. **Raw data availability**: Store complete results
3. **Negative results**: Report when hypotheses fail
4. **Actionable recommendations**: What should change?

---

## Appendix: Statistical Reference

### Effect Size Interpretation (Cohen's d)
| d | Interpretation |
|---|----------------|
| 0.2 | Small |
| 0.5 | Medium |
| 0.8 | Large |
| 1.2 | Very large |

### Sample Size Requirements
| Desired Power | Small Effect | Medium Effect | Large Effect |
|---------------|--------------|---------------|--------------|
| 0.80 | 393 | 64 | 26 |
| 0.90 | 526 | 86 | 34 |
| 0.95 | 651 | 105 | 42 |

### Multiple Comparison Correction
When comparing N patterns:
- Bonferroni: α_adjusted = 0.05 / N(N-1)/2
- For 6 patterns: α_adjusted = 0.05 / 15 = 0.0033

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-01-XX | Initial framework |
