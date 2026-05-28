---
name: hypothesis-generation
description: Generate testable hypotheses from observations, design experiments, explore competing explanations, and develop predictions for scientific inquiry across various domains.
---

# Scientific Hypothesis Generation

## Overview

Hypothesis generation is a systematic process for developing testable explanations. Formulate evidence-based hypotheses from observations, design experiments, explore competing explanations, and develop predictions. Apply this skill for scientific inquiry across domains.

## When to Use This Skill

This skill should be used when:
- Developing hypotheses from observations or preliminary data
- Designing experiments to test scientific questions
- Exploring competing explanations for phenomena
- Formulating testable predictions for research
- Conducting literature-based hypothesis generation
- Planning mechanistic studies across scientific domains

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every hypothesis generation report MUST include at least 1-2 AI-generated figures using the scientific-schematics skill.**

This is not optional. Hypothesis reports without visual elements are incomplete. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., hypothesis framework showing competing explanations).
2. Prefer 2-3 figures for comprehensive reports (mechanistic pathway, experimental design flowchart, prediction decision tree).

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams.
- Simply describe your desired diagram in natural language.
- The AI will automatically generate, review, and refine the schematic.

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting.
- Review and refine through multiple iterations.
- Ensure accessibility (colorblind-friendly, high contrast).
- Save outputs in the figures/ directory.

**When to add schematics:**
- Hypothesis framework diagrams showing competing explanations.
- Experimental design flowcharts.
- Mechanistic pathway diagrams.
- Prediction decision trees.
- Causal relationship diagrams.
- Theoretical model visualizations.
- Any complex concept that benefits from visualization.

---

## Workflow

Follow this systematic process to generate robust scientific hypotheses:

### 1. Understand the Phenomenon

Start by clarifying the observation, question, or phenomenon that requires explanation:
- Identify the core observation or pattern that needs explanation.
- Define the scope and boundaries of the phenomenon.
- Note any constraints or specific contexts.
- Clarify what is already known vs. what is uncertain.
- Identify the relevant scientific domain(s).

### 2. Conduct Comprehensive Literature Search

Search existing scientific literature to ground hypotheses in current evidence. Use both PubMed (for biomedical topics) and general web search (for broader scientific domains):
- For biomedical topics, use WebFetch with PubMed URLs to access relevant literature.
- For all scientific domains, use WebSearch to find recent papers, preprints, and reviews.

**Search strategy:**
- Begin with broad searches to understand the landscape.
- Narrow to specific mechanisms, pathways, or theories.
- Look for contradictory findings or unresolved debates.

### 3. Synthesize Existing Evidence

Analyze and integrate findings from literature search:
- Summarize current understanding of the phenomenon.
- Identify established mechanisms or theories that may apply.
- Note conflicting evidence or alternative viewpoints.
- Recognize gaps, limitations, or unanswered questions.

### 4. Generate Competing Hypotheses

Develop 3-5 distinct hypotheses that could explain the phenomenon. Each hypothesis should:
- Provide a mechanistic explanation (not just description).
- Be distinguishable from other hypotheses.
- Draw on evidence from the literature synthesis.

### 5. Evaluate Hypothesis Quality

Assess each hypothesis against established quality criteria:
- **Testability:** Can the hypothesis be empirically tested?
- **Falsifiability:** What observations would disprove it?
- **Parsimony:** Is it the simplest explanation that fits the evidence?
- **Explanatory Power:** How much of the phenomenon does it explain?
- **Scope:** What range of observations does it cover?
- **Consistency:** Does it align with established principles?
- **Novelty:** Does it offer new insights beyond existing explanations?

### 6. Design Experimental Tests

For each viable hypothesis, propose specific experiments or studies to test it:
- What would be measured or observed?
- What comparisons or controls are needed?
- What methods or techniques would be used?

### 7. Formulate Testable Predictions

For each hypothesis, generate specific, quantitative predictions:
- State what should be observed if the hypothesis is correct.
- Specify expected direction and magnitude of effects when possible.

### 8. Present Structured Output

Generate a professional LaTeX document using the provided template. The report should be well-formatted with colored boxes for visual organization and divided into a concise main text with comprehensive appendices.

**Document Structure:**
- **Executive Summary** - Brief overview.
- **Competing Hypotheses** - Each hypothesis in its own colored box with brief mechanistic explanation and key evidence.
- **Testable Predictions** - Key predictions in amber boxes.
- **Critical Comparisons** - Priority comparison boxes.

## Quality Standards

Ensure all generated hypotheses meet these standards:
- **Evidence-based:** Grounded in existing literature with citations.
- **Testable:** Include specific, measurable predictions.
- **Mechanistic:** Explain how/why, not just what.
- **Comprehensive:** Consider alternative explanations.
- **Rigorous:** Include experimental designs to test predictions.

## Resources

### references/
- `hypothesis_quality_criteria.md` - Framework for evaluating hypothesis quality.
- `experimental_design_patterns.md` - Common experimental approaches across domains.
- `literature_search_strategies.md` - Effective search techniques for PubMed and general scientific sources.

### assets/
- `hypothesis_generation.sty` - LaTeX style package providing colored boxes and professional formatting.
- `hypothesis_report_template.tex` - Complete LaTeX template with main text structure and comprehensive appendix sections.
- `FORMATTING_GUIDE.md` - Quick reference guide with examples of all box types, color schemes, citation practices, and troubleshooting tips.

### Related Skills

When preparing hypothesis-driven research for publication, consult the **venue-templates** skill for writing style guidance.