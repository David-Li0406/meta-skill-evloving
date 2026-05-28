# Computer Science Writing Conventions

CS-specific academic writing conventions and standards.

---

## Algorithm Description

### Pseudocode Standards

**Use consistent formatting:**
```
Algorithm 1: Name of Algorithm
Input: description of inputs
Output: description of outputs

1:  procedure AlgorithmName(params)
2:      for each element x in set S do
3:          if condition then
4:              action
5:          end if
6:      end for
7:      return result
8:  end procedure
```

**Key conventions:**
- Line numbers for reference
- Keywords in **bold** or `small caps`
- Indentation shows structure
- Comments in italic

**Common algorithm environments:**
- LaTeX: `algorithm2e`, `algorithmicx`, `algorithm`
- Use consistent package throughout paper

### Complexity Analysis

**Standard notation:**
- Time complexity: O(n), O(n log n), O(n^2)
- Space complexity: O(1), O(n)
- Always specify what n represents

**Phrasing:**
```
"Algorithm X runs in O(n log n) time and O(n) space, where n is the number of elements."
```

---

## System Architecture Documentation

### Diagram Standards

**Component diagrams should include:**
- Clear component boundaries
- Data flow arrows with labels
- Interface descriptions
- Technology stack labels where relevant

**Common diagram types:**
- System architecture (components and connections)
- Data flow diagrams
- Sequence diagrams (for interactions)
- Class diagrams (for design)

**Tools:** Draw.io, Lucidchart, PlantUML, TikZ (LaTeX)

### Describing Architecture

**Standard structure:**
```
1. High-level overview (one paragraph)
2. Component-by-component description
3. Data flow explanation
4. Design rationale (why this architecture)
```

**Example phrasing:**
```
"Our system consists of three main components: (1) the data ingestion
module, which..., (2) the processing engine, which..., and (3) the
output interface, which..."
```

---

## Evaluation Methodology

### Experimental Setup

**Always report:**
- Hardware specifications (CPU, GPU, RAM)
- Software versions (libraries, frameworks, OS)
- Hyperparameters and their selection method
- Random seeds for reproducibility
- Training/validation/test splits

**Example:**
```
"Experiments were conducted on a machine with an NVIDIA RTX 3090 GPU
(24GB), Intel i9-10900K CPU, and 64GB RAM, running Ubuntu 20.04 with
PyTorch 1.9.0 and CUDA 11.1."
```

### Metrics

**Common CS metrics by area:**

| Area | Metrics |
|------|---------|
| Classification | Accuracy, Precision, Recall, F1, AUC-ROC |
| Detection | mAP, IoU, Precision@K |
| Generation | BLEU, ROUGE, Perplexity, Human eval |
| Systems | Latency, Throughput, Memory usage |
| ML | Loss, Convergence time, Sample efficiency |

**Always include:**
- Baseline comparisons
- Statistical significance (p-values, confidence intervals)
- Number of runs/trials
- Variance measures (std dev, error bars)

### Ablation Studies

**Standard format:**
```
"To understand the contribution of each component, we conducted ablation
studies by systematically removing each component. Table X shows that
removing component Y decreases performance by Z%."
```

---

## Reproducibility Requirements

### Code Availability

**Best practices:**
- GitHub/GitLab repository link
- DOI via Zenodo for permanence
- Clear README with setup instructions
- Requirements file (requirements.txt, environment.yml)

**Example statement:**
```
"Code is available at https://github.com/author/project.
A permanent archive is available at https://doi.org/10.5281/zenodo.XXXXXX."
```

### Data Documentation

**Include:**
- Data sources and licensing
- Preprocessing steps
- Data statistics (size, splits, distributions)
- Data availability statement

---

## Code and Pseudocode in Papers

### Inline Code

**Formatting:**
- Use `monospace font` for inline code
- Brief snippets only (< 5 lines)
- Longer code goes in figures or appendix

### Code Listings

**Best practices:**
- Line numbers for reference
- Syntax highlighting if possible
- Caption explaining what code does
- Highlight key lines

**LaTeX packages:** `listings`, `minted`

### What to Include vs. Omit

**Include:**
- Novel algorithms
- Key implementation details
- API usage examples

**Omit:**
- Boilerplate code
- Standard library usage
- Implementation details available in supplementary materials

---

## Dataset Documentation

### Describing Datasets

**Always include:**
- Size (samples, features, classes)
- Source and licensing
- Collection methodology
- Any preprocessing applied
- Known biases or limitations

### Custom Datasets

**Must document:**
- Collection protocol
- Annotation guidelines
- Inter-annotator agreement
- Ethical considerations
- Data availability

---

## Mathematical Notation

### Conventions

| Notation | Meaning |
|----------|---------|
| Lowercase italic (x, y) | Scalars |
| Bold lowercase (**x**, **y**) | Vectors |
| Bold uppercase (**X**, **Y**) | Matrices |
| Calligraphic (X, Y) | Sets |
| Greek letters | Parameters |

### Equation Formatting

- Number important equations
- Reference equations in text: "as shown in Equation (3)"
- Define all symbols on first use
- Use consistent notation throughout

---

## Terminology

### Preferred Terms

| Avoid | Prefer |
|-------|--------|
| "We claim" | "Our results suggest" |
| "Obviously" | "As shown in Figure X" |
| "Prove" (empirically) | "Demonstrate" |
| "Optimal" (without proof) | "Effective" |

### Capitalization

| Term | Rule |
|------|------|
| Algorithm names | Capitalize: "Algorithm X", "Transformer" |
| Method names | As introduced: "our method, XNet" |
| General terms | Lowercase: "neural network", "machine learning" |
| Acronyms | All caps: "CNN", "GAN", "BERT" |

### Acronym Definitions

**First use:** "Large Language Models (LLMs)"
**Subsequent:** "LLMs"

**Well-known acronyms (no definition needed):**
- API, CPU, GPU, RAM
- URL, HTTP, JSON
- AI, ML (context-dependent)

---

## Common Mistakes

1. **Inconsistent notation** - Using x and X interchangeably
2. **Undefined symbols** - Using Greek letters without definition
3. **Vague performance claims** - "Our method is faster"
4. **Missing baselines** - No comparison to prior work
5. **Unreported hyperparameters** - Can't reproduce results
6. **No error bars** - Single-run results presented as definitive
7. **Cherry-picked results** - Only showing favorable cases
8. **Missing statistical tests** - Claiming significance without p-values

---

## Resources

- ACM Computing Surveys Author Guidelines
- IEEE Computer Society Style Guide
- ICML/NeurIPS Reproducibility Checklist
- Papers With Code: https://paperswithcode.com/
