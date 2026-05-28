<p align="center">
  <img src="assets/logo.png" alt="AgentSkillOS" height="140">
</p>

<p align="center">
  English | <a href="README_zh.md">简体中文</a>
</p>

<h2 align="center">
  Build your agent from 200,000+ skills via skill <br><ins>RETRIEVAL</ins> & <ins>ORCHESTRATION</ins><br>
  <br style="line-height:0.1;">
  通过技能<ins>检索</ins>与<ins>编排</ins>，从 200,000+ 技能中构建Agent
</h2>



<p align="center">
  <a href="https://ynulihao.github.io/AgentSkillOS/"><img src="https://img.shields.io/badge/🌐_Main_Page-AgentSkillOS-purple" alt="Main Page"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
  <a href="https://arxiv.org/abs/2603.02176"><img src="https://img.shields.io/badge/arXiv-2603.02176-b31b1b.svg" alt="arXiv"></a>
  <a href="https://huggingface.co/datasets/NPULH/agentskillos-benchmark"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-agentskillos--benchmark-yellow" alt="Hugging Face Dataset"></a>

</p>

<p align="center">
  <a href="#️-method"><img src="https://img.shields.io/badge/🏗️_Method-blue?style=for-the-badge" alt="Method"></a>
  <a href="#-benchmark"><img src="https://img.shields.io/badge/📈_Benchmark-green?style=for-the-badge" alt="Benchmark"></a>
  <a href="#-examples"><img src="https://img.shields.io/badge/💡_Examples-orange?style=for-the-badge" alt="Examples"></a>
  <a href="#-how-to-use"><img src="https://img.shields.io/badge/🚀_How_to_Use-red?style=for-the-badge" alt="How to Use"></a>
</p>

> **News**
> - [2026/03] Our new [project homepage](https://ynulihao.github.io/AgentSkillOS/) is now live!
> - [2026/03] **Benchmark** released — 30 multi-format creative tasks across 5 categories with pairwise Bradley-Terry evaluation.
> - [2026/03] **Modular Architecture** released — pluggable retrieval/orchestration modules. See [ARCHITECTURE.md](ARCHITECTURE.md) for details.
> - [2026/03] **Batch CLI** released — headless parallel execution with YAML configs, resume support, and Rich progress UI.

## 🌐 Overview

<p align="center" style="font-size: 1.1em;">
  🔥 <b>The agent skill ecosystem is exploding—over 200,000+</span>skills are now publicly available.</b>
</p>

<div align="center">

</div>

<p align="center">
  <i>
    But with so many options, how do you find the right skills for your task? And when one skill isn’t enough, how do you compose and orchestrate multiple skills into a working pipeline?<br>
    <br>
    <b>AgentSkillOS</b> is the operating system for agent skills—helping you <b>discover, compose, and run skill pipelines end-to-end</b>.
  </i>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=trh7doIZ3aA">
    <img src="./assets/cover.png" alt="Watch the video" style="zoom:100%;" height="384">
  </a>
</p>

<p align="center">
  <img src="assets/workflow_en.png" alt="Skill Workflow Overview" style="zoom:90%;" height="454">
</p>

<p align="center">
  <sub><b>WEB UI</b> · Visual workflow overview in the browser</sub>
</p>

<p align="center">
  <img src="assets/workflow_cli.gif" alt="CLI Workflow Run" style="zoom:80%;" height="380">
</p>

<p align="center">
  <sub><b>CLI</b> · Headless execution with terminal progress and logs</sub>
</p>

 ## 🌟 Highlights

- 🔍 **Skill Search & Discovery** — Creatively discover task-relevant skills with a skill tree that organizes skills into a hierarchy based on their capabilities.
- 🔗 **Skill Orchestration** — Compose and orchestrate multiple skills into a single workflow with a directed acyclic graph, automatically managing execution order, dependencies, and data flow across steps.
- 🖥️ **GUI (Human-in-the-Loop)** — A built-in GUI enables human intervention at every step, making workflows controllable, auditable, and easy to steer.
- ⭐ **High-Quality Skill Pool** — A curated collection of high-quality skills, selected based on Claude's implementation, GitHub stars, and download volume.
- 📊 **Observability & Debugging** — Trace each step with logs and metadata to debug faster and iterate on workflows with confidence.
- 🧩 **Extensible Skill Registry** — Easily plug in new skills, bring your own skills via a flexible registry.
- 📈 **Benchmark** — 30 multi-format creative tasks across 5 categories, evaluated with pairwise comparison and Bradley-Terry aggregation.

## 💡 Examples

👉 [**View detailed workflows on Landing Page →**](https://ynulihao.github.io/AgentSkillOS/)

📊 [**Check out the comparison report: AgentSkillOS vs. without skills →**](comparison_en.md)

![Case Study](docs/assets/paper_figures/fig_case_study.png)
> Qualitative comparison between the vanilla baseline and AgentSkillOS Quality-First outputs.

<table>
<tr>
<td width="50%" align="center">
<a href="https://ynulihao.github.io/AgentSkillOS/example-bug.html">
<img src="docs/assets/case1_bug_report/before_after_merged.png" alt="Bug Diagnosis Report" />
</a>
<br><b>Example 01 · Bug Diagnosis Report</b>
<br><sub>Mobile bug localization, fix validation, and visual bug report generation with before/after evidence.</sub>
</td>
<td width="50%" align="center">
<a href="https://ynulihao.github.io/AgentSkillOS/example-ui.html">
<img src="docs/assets/case2_ui_design/fusion_design_merged.png" alt="UI Design Research" />
</a>
<br><b>Example 02 · UI Design Research</b>
<br><sub>Design-language research, report generation, and multi-direction concept mockups for knowledge software.</sub>
</td>
</tr>
<tr>
<td width="50%" align="center">
<a href="https://ynulihao.github.io/AgentSkillOS/example-paper.html">
<img src="docs/assets/case3_paper_promotion/scientific_slide.png" alt="Paper Promotion" />
</a>
<br><b>Example 03 · Paper Promotion</b>
<br><sub>Transforms academic papers into social slides, scientific pages, and platform-specific promotion content.</sub>
</td>
<td width="50%" align="center">
<a href="https://ynulihao.github.io/AgentSkillOS/example-video.html">
<img src="docs/assets/case4_cat_meme/video1.gif" alt="Meme Video" />
</a>
<br><b>Example 04 · Meme Video</b>
<br><sub>Green-screen compositing, subtitle timing, and viral short-video production with multi-version outputs.</sub>
</td>
</tr>
</table>

<!-- 
> Capability Tree organizes skills hierarchically → Complementarity-aware Retrieval selects diverse skill sets → Graph-based Orchestration executes them as DAG -->
## 🏗️ Method
- Skill tree construction: Organizes over 200,000+ skills into a capability tree, providing structured, coarse-to-fine access for efficient and creative skill discovery.
- Skill retrieval: Automatically selects a task-relevant subset of usable skills given a user’s request.
- Skill orchestration: Composes the selected skills into a coordinated plan (e.g., a DAG-based workflow) to solve tasks beyond the reach of any single skill. Note that we also support a freestyle mode (i.e., Claude Code).

![AgentSkillOS Framework](docs/assets/paper_figures/fig_framework.png)
### 🌲 Why Skill Tree?

![Skill Retrieval Comparison](assets/skill_retrieval_academic_comparison.png)
> **Left**: Pure semantic retrieval prioritizes texutal similarity, often missing skills that look unrelated in embedding space but are crucial for actually solving the task—leading to narrow, myopic skill usage.
>
> **Right**: Our LLM + Skill Tree navigates the capability hierarchy to surface non-obvious but functionally relevant skills, enabling broader, more creative, and more effective skill composition.

<table>
<tr>
<td align="center"><b>200 Skills</b></td>
<td align="center"><b>1,000 Skills</b></td>
<td align="center"><b>10,000 Skills</b></td>
</tr>
<tr>
<td><img src="docs/assets/capability_trees/tree_200_expand.gif" width="280"></td>
<td><img src="docs/assets/capability_trees/tree_1000_expand.gif" width="280"></td>
<td><img src="docs/assets/capability_trees/tree_10000_expand.gif" width="280"></td>
</tr>
</table>

## 📈 Benchmark

We propose a benchmark of **30 multi-format creative tasks** spanning **5 categories**, evaluated via pairwise comparison with Bradley-Terry aggregation.

Three key properties:
- **Multi-format creative tasks** — Tasks require end-user artifacts in formats such as PDF, PPTX, DOCX, HTML, video, and generated images.
- **Pairwise evaluation** — Outputs are compared in both orders to reduce position bias and capture reliable preference signals.
- **Bradley-Terry scores** — Pairwise preferences are aggregated into continuous ranking scores for fine-grained system comparisons.

<table>
<tr>
<td width="50%" align="center">
<img src="docs/assets/paper_figures/fig_benchmark.png" alt="Benchmark Framework" />
</td>
<td width="50%" align="center">
<img src="docs/assets/paper_figures/fig_task_overview.png" alt="Task Overview" />
</td>
</tr>
</table>

## 🧪 Experiments

Evaluated across 200 / 1K / 200K skill ecosystems, AgentSkillOS demonstrates consistent superiority over baselines, with ablation confirming that both retrieval and orchestration are indispensable, and strategy selection producing structurally distinct execution graphs.

**Key findings:**
- **Substantial Gains over Baselines at Every Scale** — All three AgentSkillOS variants achieve the highest Bradley-Terry scores across 200 / 1K / 200K ecosystems. The w/ Full Pool baseline scores poorly because a growing fraction of skills becomes invisible — structured retrieval and orchestration overcome this scalability bottleneck.
- **Ablation: Both Retrieval and Orchestration Are Essential** — Removing components reveals a clear degradation gradient: without DAG orchestration, retrieval alone is insufficient; without retrieval, even oracle skills cannot close the gap. Quality-First shows only a modest deficit versus the oracle upper bound, and the gap narrows as the ecosystem grows.
- **Strategy Choice Shapes Execution Structure** — Each orchestration strategy faithfully translates its design intent into a distinct DAG topology. Quality-First builds deep, multi-stage pipelines; Efficiency-First trades depth for width to maximize parallelism; Simplicity-First retains only essential steps.

<table>
<tr>
<td colspan="2" align="center">
<img src="docs/assets/paper_figures/fig_radar.png" alt="Category Radar" width="60%" />
<br><sub><b>Category Radar</b> — Per-category Bradley-Terry performance across ecosystem scales.</sub>
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="docs/assets/paper_figures/fig_ablation.png" alt="Ablation Study" width="100%" />
<br><sub><b>Ablation</b> — Separates retrieval and orchestration effects; confirms both are required.</sub>
</td>
<td width="50%" align="center">
<img src="docs/assets/paper_figures/fig_dag_metrics.png" alt="DAG Structure Metrics" width="100%" />
<br><sub><b>DAG Structure Metrics</b> — Different orchestration strategies induce distinct topology profiles.</sub>
</td>
</tr>
</table>

## 🚀 How to Use

<details>
<summary><b>Installation & Configuration</b></summary>

### Prerequisites
- Python 3.10+
- [Claude Code](https://github.com/anthropics/claude-code) (must be installed and available in PATH)
- Use [cc-switch](https://github.com/farion1231/cc-switch) to switch to other LLM providers

### Install & Run
```bash
git clone https://github.com/ynulihao/AgentSkillOS.git
cd AgentSkillOS
pip install -e .
cp .env.example .env  # Edit with your API keys
python run.py --port 8765
```

### Download Pre-built Trees
| Tree | Skills | Description |
|------|--------|-------------|
| 🌱 `skill_seeds` | ~50 | Curated skill set (default) |
| 📦 `skill_200` | 200 | 200 skills |
| 🗃️ `skill_1000` | ~1,000 | 1,000 skills |
| 🏗️ `skill_10000` | ~10,000 | 10,000 active + layered dormant skills |

- [Google Drive](https://drive.google.com/file/d/1IHbnrv9aSnsnMGYHzVTZJ8EtQl0dJfUL/view?usp=sharing) | [Baidu Pan (cei9)](https://pan.baidu.com/s/1Sg_a33PjLbYrBZj4hmsb-w?pwd=cei9)

### Configuration
```bash
# .env
LLM_MODEL=openai/anthropic/claude-opus-4.5
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=your-key

EMBEDDING_MODEL=openai/text-embedding-3-large
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_API_KEY=your-key
```

### Custom Skill Groups
1. Create `data/my_skills/skill-name/SKILL.md`
2. Register in `src/config.py` → `SKILL_GROUPS`
3. Build: `python run.py build -g my_skills -v`

</details>

<details>
<summary><b>Batch Execution (Headless CLI)</b></summary>

### Run a Batch

Run multiple tasks in parallel without the Web UI:

```bash
python run.py cli --task config/batch.yaml
```

See [`config/eval/`](config/eval/) for ready-made batch configs covering different skill managers (`tree`, `vector`), orchestrators (`dag`, `free-style`), and skill pool sizes.

### Batch Config (YAML)

```yaml
batch_id: my_batch

defaults:
  skill_mode: auto          # "auto" (discover) or "specified"
  skill_group: skill_200    # Which skill pool to use
  output_dir: ./runs
  continue_on_error: true

execution:
  parallel: 2               # Max concurrent tasks
  retry_failed: 0

tasks:
  - file: path/to/task1.json
  - file: path/to/task2.json
  - dir: path/to/tasks/     # Scan directory
    pattern: "*.json"
```

### CLI Flags

| Flag | Description |
|------|-------------|
| `--task PATH`, `-T` | Path to batch YAML config (required) |
| `--parallel N`, `-p` | Override parallel task count |
| `--resume PATH`, `-R` | Resume an interrupted batch run |
| `--output-dir PATH`, `-o` | Override output directory |
| `--dry-run` | Preview tasks without execution |
| `--verbose`, `-v` | Show detailed logs |
| `--manager PLUGIN`, `-m` | Override skill manager (e.g., `tree`, `vector`) |
| `--orchestrator PLUGIN` | Override orchestrator (e.g., `dag`, `free-style`) |

### Resume Interrupted Runs

```bash
python run.py cli -T config/batch.yaml --resume ./runs/my_batch_20260306_120000
```

Completed tasks are skipped; only remaining tasks are re-executed.

### Output Structure

```
./runs/{batch_id}/
├── batch_result.json          # Batch summary (metrics, costs, eval scores)
└── {task_id}__{run_id}/       # Per-task directory
    ├── meta.json
    ├── result.json
    ├── evaluation.json
    └── artifacts/             # Task outputs (PDF, HTML, video, etc.)
```

</details>

## 🔮 Future Work

- [x] Recipe Generation & Storage
- [ ] Interactive Agent Execution
- [ ] Plan Refinement
- [ ] Auto Skill Import
- [ ] Dependency Detection
- [ ] History Management
- [ ] Multi-CLI Support (Codex, Gemini CLI, Cursor)


## Citation

If you find AgentSKillOS useful, consider citing our paper:
```bibtex
@article{li2026organizing,
  title={Organizing, Orchestrating, and Benchmarking Agent Skills at Ecosystem Scale},
  author={Li, Hao and Mu, Chunjiang and Chen, Jianhao and Ren, Siyue and Cui, Zhiyao and Zhang, Yiqun and Bai, Lei and Hu, Shuyue},
  journal={arXiv preprint arXiv:2603.02176},
  year={2026}
}
```
