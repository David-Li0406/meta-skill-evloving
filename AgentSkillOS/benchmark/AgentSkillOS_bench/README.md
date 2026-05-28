# AgentSkillOS Bench

<p align="center">
  <a href="https://arxiv.org/abs/2603.02176"><img src="https://img.shields.io/badge/arXiv-2603.02176-b31b1b.svg" alt="arXiv"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
</p>

Official benchmark for **[Organizing, Orchestrating, and Benchmarking Agent Skills at Ecosystem Scale](https://arxiv.org/abs/2603.02176)**.

AgentSkillOS Bench evaluates how well AI agents can retrieve, orchestrate, and execute modular skills to produce multi-format creative outputs. It contains **30 tasks** across **5 categories**, each requiring the agent to combine multiple skills (e.g., data visualization, document generation, video animation) to produce concrete deliverables.

## Benchmark Summary

| Property | Value |
|----------|-------|
| Total tasks | 30 |
| Categories | 5 |
| Output formats | DOCX, PPTX, XLSX, PDF, PNG, MP4, HTML, JSON, MD, PKL |
| Objective evaluation | Structural checks only (file existence, format, content keywords) — does **not** assess output quality |
| Pass threshold | Weighted sum >= 60% (of structural checks) |
| Quality evaluation | Separate ranking module: pairwise LLM judging + Bradley-Terry model |

## Task Categories

| Category | Count | Description | Example Outputs | Example Skills |
|----------|-------|-------------|-----------------|----------------|
| Data Computation | 6 | Statistical analysis, simulation, symbolic math, ML model comparison | DOCX, PPTX, XLSX, JSON, PNG, PKL | `sympy`, `scientific-visualization`, `xlsx` |
| Document Creation | 6 | Academic summaries, contracts, presentations, educational diagrams | DOCX, PPTX, PDF, HTML, PNG | `docx`, `pptx`, `scientific-slides`, `citation-management` |
| Motion Video | 6 | Mathematical animations, puzzle solving, algorithm visualization | MP4, JSON, PDF, TXT | `manim`, `remotion`, `sympy` |
| Visual Creation | 6 | Scientific figures, social media packs, memes, illustration series | PNG, JSON | `generate-image`, `meme-factory`, `media-processing` |
| Web Interaction | 6 | Competitor analysis, web scraping, bug reports, data dashboards | PNG, DOCX, XLSX, JSON, HTML, MD | `dev-browser`, `firecrawl-scraper`, `data-storytelling` |

## Directory Structure

```
AgentSkillOS_bench/
├── __init__.py              # Benchmark registration and exports
├── types.py                 # Type definitions (TaskConfig, EvaluatorResult, etc.)
├── registry.py              # @evaluator decorator and global registry
├── orchestrator.py          # Evaluation engine (topological sort, execution, aggregation)
├── tasks/                   # 30 task definition JSON files
│   ├── data_computation_task1.json
│   ├── data_computation_task2.json
│   ├── ...
│   └── web_interaction_task6.json
├── task_data/               # Input data files referenced by tasks
│   ├── data_computation_task1/
│   │   └── penguins.csv
│   ├── data_computation_task5/
│   │   └── ml_project/
│   └── ...
├── evaluators/
│   └── objective/           # Deterministic evaluators (return 0 or 1)
│       ├── file_evaluators.py       # file_exists, file_content_check, files_match_pattern
│       ├── document_evaluators.py   # pptx_slide_count, pptx_content_check, docx_heading_count, etc.
│       ├── format_evaluators.py     # json_valid, json_schema_valid, json_has_keys, etc.
│       ├── numeric_evaluators.py    # json_array_length, json_field_numeric_compare
│       └── pddl_evaluators.py       # pddl_plan_validates, puzzle_8_plan_validates
├── ranking/                 # Post-hoc quality comparison module
│   ├── compare.py           # Pairwise LLM comparison (A vs B)
│   ├── rank.py              # Multi-method Bradley-Terry ranking
│   └── checkpoint.py        # Checkpoint persistence for resumable ranking
└── utils/
    ├── file_utils.py        # File reading, JSON parsing, document text extraction
    ├── file_converters.py   # PDF/PPTX/DOCX/HTML rendering to images
    ├── code_utils.py        # Subprocess execution helpers
    └── llm_clients.py       # LLM API clients for ranking judge
```

## Task Schema

Each task is defined as a JSON file in `tasks/`. Here is a trimmed example (`data_computation_task1.json`):

```json
{
  "task_id": "data_computation_task1",
  "task_name": "Penguin Species Research Report and Presentation",
  "description": "Analyze penguin morphological data to identify species-specific characteristics...",
  "skills": ["pptx", "docx", "scientific-visualization", "data-storytelling"],
  "prompt": "I am a zoologist, and I need to present my research findings on penguins...",
  "outputs": ["report.docx", "presentation.pptx"],
  "category": "data_computation",
  "aggregation": {
    "strategy": "weighted_sum"
  },
  "evaluators": [
    {
      "id": "report_exists",
      "type": "objective_usability",
      "op_func": "file_exists",
      "description": "Check that report.docx exists",
      "weight": 3,
      "op_args": { "path": "report.docx", "min_size": 1 }
    },
    {
      "id": "presentation_slide_count",
      "type": "objective_usability",
      "op_func": "pptx_slide_count",
      "description": "Check that the presentation has at least 10 slides",
      "weight": 3,
      "op_args": { "path": "presentation.pptx", "operator": ">=", "expected": 10 },
      "depends_on": ["presentation_exists"]
    }
  ]
}
```

Key fields:

- **`skills`** — Skills the agent is expected to retrieve and use
- **`outputs`** — Expected deliverable files
- **`evaluators`** — Ordered list of objective checks, each with a weight and optional dependency chain
- **`aggregation.strategy`** — How evaluator scores are combined (default: `weighted_sum`)

## Evaluation Framework

The benchmark uses a **two-tier evaluation** design:

1. **Objective evaluation** (automated) — Deterministic structural checks that verify whether the agent produced the expected deliverables in the correct format. These evaluators check properties like file existence, minimum file size, slide count, required keywords, JSON schema conformance, etc. They do **not** judge the quality, aesthetics, or correctness of the content itself.
2. **Quality ranking** (LLM-based) — A separate post-hoc module that uses pairwise LLM comparison and a Bradley-Terry model to rank multiple methods by output quality. This is decoupled from the pass/fail scoring above.

### Objective Evaluators

All objective evaluators are deterministic structural checks that return a binary score (0 or 1). They verify format compliance and deliverable completeness — for example, whether a file exists and is non-empty, whether a PPTX has the minimum required number of slides, or whether a JSON output conforms to the expected schema. They do **not** evaluate the quality or correctness of the generated content. Available functions:

| Module | Functions |
|--------|-----------|
| `file_evaluators` | `file_exists`, `file_content_check`, `files_match_pattern` |
| `document_evaluators` | `pptx_slide_count`, `pptx_content_check`, `docx_heading_count`, `docx_content_check`, `pdf_page_count`, `pdf_orientation`, `pdf_dimensions` |
| `format_evaluators` | `json_valid`, `json_schema_valid`, `json_has_keys`, `json_array_item_check` |
| `numeric_evaluators` | `json_array_length`, `json_field_numeric_compare` |
| `pddl_evaluators` | `pddl_plan_validates`, `pddl_plan_step_count`, `puzzle_8_plan_validates` |

### Scoring

- Each evaluator contributes `score * weight` to the total
- Final score is the weighted average scaled to 0–100
- A task is considered **passed** if `total_score >= 60` (this reflects structural completeness, not output quality)

### Dependency-Based Execution

Evaluators support a `depends_on` field that references other evaluator IDs. The orchestrator performs a topological sort before execution — if a dependency fails (score = 0), all downstream evaluators are automatically skipped.

### Ranking Module

For subjective quality comparison across methods, the ranking module uses:

1. **Pairwise LLM judging** — Each pair of runs is compared in both presentation orders (A-first and B-first) to mitigate position bias
2. **Bradley-Terry model** — Win/loss/tie counts are fed into an MM algorithm to produce standardized scores (0–100)
3. **Per-task and per-category aggregation** — Scores are computed at the task level, then averaged by category and overall

```bash
# Compare two runs
python -m benchmark.AgentSkillOS_bench.ranking.compare \
  --run-a results/run_A --run-b results/run_B

# Rank multiple methods
python -m benchmark.AgentSkillOS_bench.ranking.rank \
  --runs results/run1:GPT4 results/run2:Claude results/run3:Gemini
```

## Dependencies

### Core (from `pyproject.toml`)

```
claude-agent-sdk >= 0.1.0
pydantic >= 2.0.0
rich >= 13.0.0
pyyaml >= 6.0.0
loguru >= 0.7.0
python-dotenv >= 1.0.0
```

### Objective Evaluators

These packages are lazy-imported by evaluator functions and required only when the corresponding evaluators are used:

```
python-pptx     # pptx_slide_count, pptx_content_check, pptx text extraction
python-docx     # docx_heading_count, docx_content_check, docx text extraction
PyMuPDF (fitz)  # pdf_page_count, pdf_orientation, pdf_dimensions, PDF→image rendering
jsonschema      # json_schema_valid
```

### File Reading Utilities

Used by `utils/file_utils.py` for extracting text from binary document formats (called by `file_content_check` and ranking module):

```
pdfplumber      # PDF text extraction (read_file for .pdf)
openpyxl        # XLSX text extraction (read_file for .xlsx)
```

### Ranking Module

```
numpy           # Bradley-Terry model fitting (top-level import in rank.py)
openai          # OpenAI-compatible API backend for LLM judging (alternative to claude-agent-sdk)
Pillow          # Image resizing, GIF generation for visual comparison
opencv-python   # Video key-frame extraction for LLM visual judging
playwright      # HTML→screenshot rendering via headless Chromium
```

### System-Level Tools

The ranking module's file converters invoke these external binaries via `subprocess`. They are **not** Python packages and must be installed separately:

```
LibreOffice     # DOCX/PPTX→PDF conversion (preserves styles & images)
                # macOS: brew install --cask libreoffice
                # Linux: sudo apt install libreoffice

ffprobe/ffmpeg  # Video metadata extraction (resolution, FPS, duration, codec)
                # macOS: brew install ffmpeg
                # Linux: sudo apt install ffmpeg

Chromium        # Used by playwright for HTML rendering
                # After pip install: playwright install chromium
```

### Dev

```
pytest >= 7.0.0
pytest-asyncio >= 0.21.0
```

## Quick Start

### CLI

```bash
# Run evaluation on a single task
python run.py --config config/eval/skill-1000/batch-dag-plan-0.yaml
```

### Programmatic API

```python
from benchmark.AgentSkillOS_bench import evaluate_task, evaluate_task_sync

# Async
result = await evaluate_task("path/to/task_config.json", "path/to/workspace")

# Sync
result = evaluate_task_sync("path/to/task_config.json", "path/to/workspace")

print(result.passed)       # True if total_score >= 60
print(result.total_score)  # Weighted score (0-100)
print(result.to_dict())    # Full result as dict
```

## Citation

If you use AgentSkillOS Bench in your research, please cite:

```bibtex
@article{li2026agentskillos,
      title={Organizing, Orchestrating, and Benchmarking Agent Skills at Ecosystem Scale},
      author={Hao Li and Chunjiang Mu and Jianhao Chen and Siyue Ren and Zhiyao Cui and Yiqun Zhang and Lei Bai and Shuyue Hu},
      year={2026},
      eprint={2603.02176},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2603.02176},
}
```
