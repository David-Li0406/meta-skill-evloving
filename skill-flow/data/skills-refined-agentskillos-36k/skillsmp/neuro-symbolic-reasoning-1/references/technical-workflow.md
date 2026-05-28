# Technical Specialist Workflow

## When to Use

| Query Type | Example |
|------------|---------|
| Background Q&A | "What is the connection between Boolean algebras and polynomial rings?" |
| Literature Review | "How does Logic-LM compare to our pipeline?" |
| Code Review | "Debug this Z3 encoding" |
| Implementation | "Implement a SAT-based solver for K3 logic" |
| Validation | "Test this NL-to-FOL converter" |

## Workflow

### 1. Assess Query
- Check `technical_references/project_pipeline/` for project context
- Check `technical_references/reference_pipeline/` for related work

### 2. Validate Answer
- Code is syntactically correct with tests/examples
- Claims are factually grounded with citations
- Compare to reference pipeline when relevant
- State uncertainty clearly

### 3. Output
- Clear headings and structure
- Summary of assumptions and reasoning
- Citations and sources for nontrivial claims
- Clean code blocks with comments

## Code Analysis

When working with implementation code:

**What to look for:**
- Overall system structure and module organization
- How components interact (LLM, symbolic solver, data processing)
- Prompt templates and few-shot examples
- Solver integration and error handling
- Self-refinement mechanisms
- Evaluation scripts and metrics computation

**Typical code structure:**
```
project/
├── prompts/           # Few-shot examples and prompt templates
├── src/
│   ├── formulator.py  # NL → symbolic translation
│   ├── solver.py      # Symbolic reasoning engine
│   ├── refiner.py     # Self-refinement logic
│   └── pipeline.py    # End-to-end orchestration
├── data/              # Datasets (FOLIO, ProofWriter, etc.)
├── eval/              # Evaluation and analysis scripts
└── configs/           # Hyperparameters and settings
```

**Key checks:**
- Paper-code consistency (do descriptions match implementation?)
- Hardcoded values vs. configurable parameters
- Random seed handling for reproducibility
- Discrepancies in hyperparameters, prompts, or procedures

## Technical Considerations

### Symbolic Formalism Selection
- Which logic/formalism best fits the problem type?
- Trade-offs between expressiveness and tractability
- How to handle problems requiring multiple formalisms

### NL-to-Symbolic Translation Quality
- How to improve formulation accuracy?
- Handling implicit information and world knowledge
- Maintaining consistency in predicate/constant naming

### Error Handling and Recovery
- Beyond syntax error refinement
- Detecting and correcting semantic errors
- Confidence estimation for predictions

### Faithfulness and Interpretability
- How to verify reasoning traces?
- Explaining symbolic reasoning to users
- Handling uncertain/unknown conclusions appropriately
