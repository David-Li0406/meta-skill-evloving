# Claude Code for Benchmark Onboarding

## Overview for Project Collaborators

---

## Part 1: What is Claude Code?

Claude Code is Anthropic's command-line AI assistant designed for software development and research workflows. Unlike the chat interface (claude.ai), Claude Code operates directly in your terminal with full access to your local filesystem, enabling it to read, write, and execute code autonomously.

### Key Capabilities

- **File System Access**: Reads project files, creates new code, edits existing files
- **Code Execution**: Runs scripts, tests, and build commands directly
- **Web Access**: Fetches documentation, papers, and dataset information
- **Agentic Workflows**: Completes multi-step tasks with minimal supervision
- **Context Awareness**: Understands your entire project structure

### Skills System

Claude Code supports custom "skills" — instruction files that teach it domain-specific workflows. Skills are markdown files placed in `.claude/skills/` that Claude reads before tackling relevant tasks. This allows teams to encode best practices, enforce standards, and create reproducible workflows.

---

## Part 2: Benchmark Onboarding in Our Project

We've developed a custom skill that automates the conversion of creativity benchmarks into a standardized evaluation format. This addresses a core challenge: our systematic review identified **283 unique benchmarks** across diverse formats, and manually writing integration code for each would be prohibitive.

### Why HELM?

We're standardizing benchmarks into [HELM](https://crfm.stanford.edu/helm/) (Holistic Evaluation of Language Models), Stanford's framework for systematic LLM evaluation. HELM provides infrastructure for running benchmarks at scale across many models with consistent metrics. By converting creativity benchmarks into HELM "Scenarios" (standardized data loaders), we can evaluate any model on any benchmark without per-benchmark custom code. The Scenario handles data loading and prompt formatting; HELM handles the rest (model calls, metrics, reporting).

### The Problem

Each benchmark exists in different forms:
- HuggingFace datasets with varying schemas
- GitHub repositories with custom formats
- PDFs with prompts described in prose
- Different evaluation paradigms (MC, open-ended, rating scales)

### Our Solution: The Benchmark Onboarder Skill

The skill encodes a 5-step workflow that Claude follows automatically. See SKILL.md for implementation details. Your role is quality control and decision-making, not executing these steps manually.

### What Matters for GAs

**Prompts are sacred.** Benchmark prompts must be extracted exactly from source papers — never generated or inferred. Your job is to verify Claude got this right by checking the cited section/page.

**Everything is traceable.** Every scenario must cite its source (paper, section, dataset). If you can't trace a prompt back to its origin, flag it.

### Example Workflow

```
User: Onboard the RiddleSense benchmark

Claude Code:
1. Fetches paper (ACL 2021)
2. Examines HuggingFace dataset schema
3. Notes: test split has no labels → uses validation
4. Generates scenario.py with proper MC format
5. Shows example prompt for verification
```

### Output

Each onboarded benchmark produces:
- `scenario.py` — Standardized loader following HELM Scenario pattern
- Documentation header citing prompt source
- Field mapping (used vs. skipped)

### Benefits

- **Consistency**: All benchmarks follow identical structure
- **Traceability**: Every prompt cites its paper source
- **Speed**: Minutes per benchmark vs. hours of manual work
- **Quality Control**: Built-in verification checklist

---

## Part 3: Team Workflow

Benchmarks are pre-assigned in `benchmarks.json` to GAs via the `assigned_to` field.

### Setup for Each GA

1. **API Key**: Each GA gets their own Claude API key (usage trackable per key)
2. **Clone repo**: `git clone https://github.com/rebeaty/amazon-creativity-benchmark`
3. **Set key**: `export ANTHROPIC_API_KEY=sk-...`
4. **Run**: `claude` in project directory

### Tracking Progress

In `benchmarks.json`, each benchmark has:
```json
{
  "name": "BenchmarkName",
  "paper_id": "abc123",
  "url": "https://...",
  "status": "pending|in_progress|completed|failed|skipped",
  "assigned_to": "CL",
  "scenario_file": "scenarios/benchmark_name.py",
  "eval_type": "exact_match|open_ended|llm_judge|custom",
  "notes": "Any issues encountered"
}
```

**Eval types (aligned with HELM RunSpec patterns):**
- `exact_match` — Gold labels, uses `get_exact_match_metric_specs()`
- `open_ended` — Generation tasks, uses `get_open_ended_generation_metric_specs()` (includes BLEU, ROUGE, F1)
- `summarization` — Uses `get_summarization_metric_specs()`
- `llm_judge` — LLM evaluates outputs; requires `annotator_notes.md`
- `custom` — Needs new metric implementation; requires `metric_notes.md`

**Companion files (for non-standard eval):**
- `scenarios/benchmark_name/annotator_notes.md` — LLM judge config (model, prompt, dimensions)
- `scenarios/benchmark_name/metric_notes.md` — Custom metric requirements

### Git Push Policy

**Push immediately:**
- LEARNINGS.md updates (team learns from issues right away)
- Skipped/failed benchmarks (so others don't duplicate effort)

**Batch (every 3-5 benchmarks or end of session):**
- Completed scenario.py files
- benchmarks.json status updates

Simple rule: **Push when you take a break.**

### Sharing Learnings

Claude automatically appends notes to LEARNINGS.md when it encounters issues. No manual copy-paste needed — just commit and push so the team sees updates.

Example of what gets added:

| Benchmark | Issue | Solution |
|-----------|-------|----------|
| RiddleSense | Test split has no labels | Use validation split |

Team knowledge builds automatically across sessions.

### What GAs Actually Do

Running the skill is the easy part. Your job is quality control and decision-making.

**Session Management**
- Run 2-3 onboarding sessions in parallel using terminal tabs or tmux
- Respond when Claude asks questions or hits issues
- Use `/compact` between benchmarks to manage context

**Quality Checks**

For each completed scenario, verify:
- Prompt text matches the source paper (check cited section/page)
- Dataset fields are mapped correctly (no model outputs used as inputs)
- Code loads without errors (Claude should test, but double-check)

**Decision Points**

Claude will ask for input when:
- Multiple tasks exist and it's unclear which is the primary creativity task
- Dataset has issues (missing labels, private access, unusual format)
- Paper doesn't specify exact prompt wording

Your judgment matters here — you know the project goals better than Claude does.

**Knowledge Sharing**
- Commit LEARNINGS.md updates promptly so the team benefits
- Flag recurring patterns in weekly sync
- Note any benchmarks that need PI review

**Rough Time Allocation**
- ~20% monitoring sessions, responding to prompts
- ~40% reviewing generated scenarios against papers
- ~20% making judgment calls on edge cases
- ~20% tracking progress, committing, syncing

### Workflow Commands

```bash
# Start Claude Code in project directory
claude

# Onboard a specific benchmark
> Onboard the [benchmark name] benchmark

# See your assigned benchmarks
> Show my assigned benchmarks (I'm [initials])
```

### Weekly Sync

1. Pull latest (especially LEARNINGS.md)
2. Push any uncommitted work
3. Quick standup: blockers, patterns discovered
4. Reassign if someone finishes early

---

## Getting Started

1. Install Claude Code: `npm install -g @anthropic-ai/claude-code`
2. Get your API key from the project lead
3. Set key: `export ANTHROPIC_API_KEY=sk-...`
4. Clone repo and navigate to project directory
5. Run `claude` to start

The skill activates automatically when you mention benchmark onboarding.
