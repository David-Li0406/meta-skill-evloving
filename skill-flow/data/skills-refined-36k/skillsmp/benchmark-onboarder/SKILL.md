---
name: benchmark-onboarder
description: Onboard AI creativity benchmarks into HELM-compliant Scenario implementations. Use when asked to onboard a benchmark, create a HELM scenario, process a paper into evaluation code, convert a dataset to HELM format, or when the user mentions "creativity benchmark", "task.py", or "scenario.py".
allowed-tools: Read, Write, WebFetch, Grep, Glob, Bash, Task
user-invocable: true
---

# HELM Benchmark Onboarder

Transform creativity benchmark datasets into HELM Scenario implementations.

## Core Principles

1. **Dataset-first** - The dataset defines what's possible; the paper provides context
2. **Skip model outputs** - We want original prompts/stimuli, not what GPT-4 generated
3. **Verify everything** - Every field must map to real data

## Resources

- For HELM code patterns, see [helm-template.md](helm-template.md)
- For working examples, see [examples/](examples/)
  - [brainteaser.py](examples/brainteaser.py) - Multiple choice with distractor answers
  - [analobench.py](examples/analobench.py) - Analogical reasoning MC task
  - [riddlesense.py](examples/riddlesense.py) - Riddle QA with CommonsenseQA format
- For benchmark queue, see [benchmarks.json](benchmarks.json)
- For team-accumulated learnings, see [LEARNINGS.md](LEARNINGS.md)

## Tool Usage

- **WebFetch**: Read dataset documentation, READMEs, and papers
- **Read**: Examine dataset files, existing scenarios, and example code
- **Bash**: Load dataset samples to inspect field structure
- **Glob**: Find relevant files in benchmark repos
- **Task (Explore)**: For complex benchmarks, explore dataset structure first
- **Write**: Generate the final scenario.py

## When to Use

User says things like:
- "Onboard the BRAINTEASER benchmark"
- "Create a HELM scenario for this paper"
- "Process this benchmark into evaluation code"

## Workflow

### Step 1: Qualify the Benchmark

Before doing any work, check if this benchmark is suitable:

**Ask yourself:**
- Is this a creativity benchmark?
- Is there a publicly available dataset?
- Is there an evaluation method? (accuracy, human ratings, metrics)

If the answer to any is NO, tell the user why this benchmark doesn't qualify and stop.

**Focus on primary creativity tasks.** Some papers include multiple tasks or secondary experiments (e.g., MMLU baselines, general QA comparisons). Identify and implement only the core creativity evaluation tasks described in the paper.

### Handling Multi-Task Benchmarks

Some papers contain multiple tasks, not all creativity-related. When onboarding:

1. **Identify the primary creativity task(s)** - Read the paper abstract/introduction to understand the main contribution
2. **Skip secondary experimental tasks** - Papers often include baseline comparisons (e.g., MMLU, general QA) that aren't creativity benchmarks
3. **When unclear, ask the user** - If you can't determine which tasks are the main creativity evaluations, ask before proceeding

### Step 2: Examine the Dataset

Load a few examples and understand the structure:

```python
from datasets import load_dataset
ds = load_dataset("org/dataset-name", split="test")
print(ds[0])  # See field names and structure
```

**Identify fields:**
- **Stimulus/Question**: The input text (question, prompt, story, etc.)
- **Choices**: For MC tasks, the answer options
- **Answer/Label**: The correct answer or ground truth
- **Metadata**: Split info, IDs, categories

**Use judgment on fields:** Avoid fields that contain model-generated outputs (e.g., fields named "gpt_response" or containing experiment results). Long text fields may be legitimate inputs for evaluation tasks (e.g., stories to analyze, passages to read). When uncertain, check the paper to understand what each field represents.

### Step 3: Extract Task Instructions and Evaluation Setup

Read source materials **once** to extract both what goes into the Scenario and what's needed for evaluation configuration. This avoids redundant passes through papers.

#### 3a. Task Instructions (→ Scenario)

**Where to look (in order):**
1. Dataset README on HuggingFace/GitHub
2. Paper Methods section
3. Paper Appendix (often has exact prompts)
4. Codebase evaluation scripts (if available)

**What to capture:**
- Exact prompt wording given to models (if specified)
- Input formatting requirements
- Any few-shot examples used

**Priority:**
1. Explicit instructions from paper/README → use exactly as written, cite location
2. Standard format for task type → note "Standard MC format" in header
3. Unclear → ask user before proceeding

**Critical:** Never invent or paraphrase prompts. If the paper doesn't specify exact wording, use standard formatting and note this in the header.

#### 3b. Evaluation Setup (→ Companion files)

While reading source materials, identify the evaluation approach. In HELM, Scenarios just load data—metrics are configured separately in RunSpecs.

| Eval Type | HELM RunSpec Pattern | Additional Output |
|-----------|---------------------|-------------------|
| `exact_match` | `get_exact_match_metric_specs()` | None needed |
| `open_ended` | `get_open_ended_generation_metric_specs()` | None (includes BLEU-1, BLEU-4, ROUGE-L, F1) |
| `summarization` | `get_summarization_metric_specs()` | None needed |
| `llm_judge` | Custom with Annotator | `annotator_notes.md` |
| `custom` | Needs new metric implementation | `metric_notes.md` |

**For standard metrics (exact_match, open_ended, summarization):**

Just note the eval_type in benchmarks.json. The Scenario stays pure.

**For LLM-as-judge benchmarks, extract and output to `scenarios/benchmark_name/annotator_notes.md`:**

```markdown
# Annotator Requirements: BenchmarkName

Source: Paper Appendix B, Section 4.2

## Configuration for LLMAsJuryAnnotator

Judge model: GPT-4-turbo
Dimensions: novelty, feasibility, significance
Scale: 1-5 Likert per dimension

## Judge Prompt Template

Rate the following response on {dimension} from 1 to 5.

Question: {QUESTION}
Response: {RESPONSE}

Provide your rating as a single number.

## Notes
- Human correlation: 0.82 (Paper Table 3)
- Authors noted position bias in judge
```

**For custom metrics, output to `scenarios/benchmark_name/metric_notes.md`:**

Document what the paper measured and how, for future metric implementation.

**Update benchmarks.json:**
```json
{
  "name": "BenchmarkName",
  "eval_type": "open_ended|exact_match|llm_judge|custom",
  "notes": "any special considerations"
}
```

### Step 4: Generate the HELM Scenario

Follow HELM's standard Scenario structure:

```python
"""
HELM Scenario: BENCHMARK_NAME

Paper: [citation or URL]
Code: [GitHub repo if available]

Prompt format:
  Question: {question}
  A) {choice_a}  B) {choice_b}  C) {choice_c}  D) {choice_d}
  Answer:

Fields used: question, choices, answer
Fields skipped: gpt4_response (model output)
"""

from datasets import load_dataset
from helm.benchmark.scenarios.scenario import (
    Scenario, Instance, Input, Output, Reference,
    CORRECT_TAG, TEST_SPLIT
)

class BenchmarkScenario(Scenario):
    name = "benchmark_name"  # lowercase, underscores
    description = "org/dataset-name"  # data source, NOT task description
    tags = ["creativity", "relevant_tag"]

    def get_instances(self, output_path):
        dataset = load_dataset("org/dataset-name", split="test")

        instances = []
        for item in dataset:
            # Build prompt from dataset fields
            prompt = f"Question: {item['question']}\n"

            # Build references (all choices for MC, correct answer tagged)
            references = [...]

            instances.append(Instance(
                input=Input(text=prompt),
                references=references,
                split=TEST_SPLIT
            ))
        return instances
```

**Note:** Evaluation configuration (metrics, annotators) is NOT part of the Scenario. Document those separately per Step 3b.

**HELM conventions:**
- For multiple choice: ALL choices become References, only correct one gets CORRECT_TAG
- For binary (yes/no): Both options are References
- For open-ended: Reference can be empty or contain gold response
- `description` field = data source, not task description

### Step 5: Verify Before Finishing

Check these before delivering:

- [ ] Dataset loads without errors
- [ ] All template variables map to real data fields
- [ ] No model output fields used as inputs
- [ ] References have non-empty text (for MC/closed tasks)
- [ ] Correct split used (test if labels available, validation otherwise)
- [ ] Test with a few examples to confirm formatting

## Output

Create `scenario.py` with:
- Header comment noting prompt source, fields used/skipped, paper reference
- Clean, minimal code following HELM patterns

### Auto-Capture Notes to LEARNINGS.md

When you encounter issues or discover patterns, append directly to LEARNINGS.md (in this skill folder):

1. Read the current LEARNINGS.md file
2. Add your note to the appropriate section (Dataset Quirks table, Common Patterns, etc.)
3. Write the updated file

**Always capture notes for:**
- Split issues (test has no labels, etc.)
- Field name mismatches (docs say X, actual field is Y)
- Special loading requirements (trust_remote_code, config names)
- Skipped tasks (secondary experiments, non-creativity baselines, etc.)

This ensures team knowledge is captured immediately without manual intervention.

## Common Issues

| Problem | Solution |
|---------|----------|
| Test split has no labels | Use validation split instead (see riddlesense.py) |
| Dataset requires special loading | Add `trust_remote_code=True` to load_dataset() |
| Field names don't match docs | Print `ds[0]` to see actual field names |
| Empty references | Wrong answer field - check the schema |
| Very long prompts | Might be using wrong field (model outputs) |
| Multimodal benchmark | Include if there's a text evaluation component; note modality in tags |
| No explicit prompt in paper | Use standard formatting, note in header |

## Complex Benchmarks

For benchmarks with multiple subsets or complex evaluation:

1. Use **Task tool with Explore agent** to understand the dataset structure first
2. Break into sub-tasks if multiple scenario files are needed
3. Use `/compact` between benchmarks if onboarding multiple in one session

## Benchmarks with LLM-as-Judge Evaluation

In HELM's architecture:
- **Scenarios** load data and format prompts
- **Annotators** handle LLM-based judging (e.g., `LLMAsJuryAnnotator`)
- **Metrics** compute final scores from annotations

These are separate components. Your Scenario stays pure—evaluation config goes elsewhere.

**When you encounter an LLM-as-judge benchmark:**

1. **Create the Scenario as normal** — data loading, prompt formatting
2. **References may be empty** for open-ended generation tasks—that's fine
3. **Extract annotator requirements per Step 3b** → output to `annotator_notes.md`
4. **Flag in benchmarks.json** with `"eval_type": "llm_judge"`

The `annotator_notes.md` file documents what's needed to implement the `LLMAsJuryAnnotator` configuration (judge model, prompt template, dimensions, scale). This is a separate implementation task from Scenario creation.

## Examples

### Example A: Paper specifies instructions (ANALOBENCH)

1. **Qualify**: Creativity benchmark (analogical reasoning)? Yes. Dataset? Yes. Eval? Yes (accuracy).

2. **Examine dataset**:
   ```python
   ds = load_dataset("jhu-clsp/AnaloBench", "T1S1-Subset", split="train")
   print(ds[0].keys())  # ['Index', 'Sentence', 'Options', 'Label']
   ```

3. **Check instructions**: Paper Section 3 specifies "Which of the following is the most analogous story?" → use exactly

4. **Generate scenario**: Paper instruction + dataset fields, MC pattern

5. **Verify**: 340 examples, Labels are A/B/C/D

### Example B: Standard format (RiddleSense)

1. **Qualify**: Creativity benchmark (riddles + commonsense)? Yes. Dataset? Yes. Eval? Yes.

2. **Examine dataset**: Fields are `question`, `choices`, `answerKey`

3. **Check instructions**: No specific wording in paper → use standard MC format, note in header

4. **Generate scenario**: Standard "Question: X\n\nA. ..." format

5. **Verify**: Test split has no labels → switch to validation split
