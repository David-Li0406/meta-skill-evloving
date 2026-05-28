# Paper Section Review Guide

What to look for when reviewing each section of a research paper.

## Abstract

- States problem clearly in first 1-2 sentences
- Summarizes approach at appropriate abstraction level
- Reports key quantitative results
- Claims match actual contributions
- No undefined acronyms or jargon

## Introduction

- Motivates the problem with concrete examples or statistics
- Clearly states what gap exists in prior work
- Articulates contributions as numbered list
- Scope and limitations acknowledged upfront
- Roadmap to rest of paper (optional but helpful)

## Related Work

- Covers all major relevant categories
- Discusses relationship to proposed work (not just lists papers)
- Identifies what's missing that this work addresses
- Recent work included (within last 2-3 years)
- Fair characterization of prior approaches

## Method

- Clear problem formulation with notation defined
- Each component motivated before described
- Assumptions stated explicitly
- Pseudocode or algorithm box for complex procedures
- Sufficient detail for reimplementation
- Complexity analysis where relevant

## Experiments

**Setup:**
- Datasets described with statistics
- Baselines justified and fairly implemented
- Evaluation metrics appropriate for the task
- Hyperparameter selection process explained
- Hardware/compute resources mentioned

**Results:**
- Tables/figures clearly labeled and captioned
- Statistical significance or confidence intervals
- Results support claims made in abstract/intro
- Failure cases or limitations analyzed
- Ablation studies for key components

**Analysis:**
- Error analysis by category
- Qualitative examples (good and bad)
- Comparison to baselines is fair
- Discussion of why method works/fails

## Conclusion

- Summarizes contributions (should match intro)
- Acknowledges limitations honestly
- Future work directions are concrete
- No new claims or results introduced

## Common Issues

| Issue | Red Flag |
|-------|----------|
| Overclaiming | "State-of-the-art" without proper comparison |
| Cherry-picking | Only showing favorable examples |
| Missing baselines | Not comparing to obvious alternatives |
| P-hacking | Testing many hypotheses, reporting best |
| Reproducibility | Key details missing (seeds, hyperparams) |
| Self-promotion | Excessive self-citation, biased framing |
