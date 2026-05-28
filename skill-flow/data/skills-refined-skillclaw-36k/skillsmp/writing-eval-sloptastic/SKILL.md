---
name: writing-eval-sloptastic
description: Quantitative framework for detecting AI-generated "slop" in prose through systematic analysis of structural, lexical, rhetorical, and logical patterns. Use when analyzing text authenticity, evaluating writing quality, detecting AI-generated content, or assessing whether prose has characteristic AI patterns like excessive parallelism, abstraction laddering, chiasmus abuse, platitudes, tautologies, or rhetorical overengineering.
---

# AI Slop Evaluation Framework

## Overview

This skill provides a quantifiable methodology for analyzing prose to detect AI-generated "slop"—text that employs rhetorical devices to sound profound while lacking substantive content. The framework evaluates six key dimensions with weighted scoring to produce an objective "AI Slop Score."

## Core Methodology

Evaluate text across six dimensions, each scored 0-100% based on specific quantifiable patterns:

1. **Structural Formulaicity** - Pattern density and mechanical construction
2. **Lexical Vapor** - Abstract vs. concrete language ratio
3. **Rhetorical Overengineering** - Overuse of literary devices
4. **Tonal Uncanniness** - Absence of hedging and human messiness
5. **Logical Void** - Circular reasoning and evidence-free claims
6. **Output Format** - Analysis structure and presentation

## Evaluation Process

### 1. Structural Formulaicity (Weight: 20%)

**What to measure:**
- **Parallel construction density**: Count explicit parallel structures (e.g., "You X, she Y" repeated patterns)
  - AI tell: >3% density indicates robotic sustaining of parallelism
- **Connector disease**: Count overused logical connectors ("That's why...", "This is because...")
  - AI tell: >1.5% of text indicates simulated coherence
- **Definitional tautology**: Count negation-redefinition patterns ("X isn't just Y, it's Z")
  - AI tell: >2 instances suggests strawman correction habit

**Scoring rubric:**
- 0-30%: Natural variation, broken patterns for emphasis
- 31-60%: Some repetitive structures but not systematic
- 61-85%: High pattern density, mechanical feel
- 86-100%: Robotic parallelism, formulaic throughout

### 2. Lexical Vapor (Weight: 15%)

**What to measure:**
- **Concrete-to-abstract ratio**: Count concrete vs. abstract nouns
  - Calculate ratio (concrete:abstract)
  - AI tell: Ratio <1:2 indicates abstraction overuse
- **Platitude density**: Count vague intensifiers and meaningless profundities
  - Examples: "real X", "natural growth", "stress is softened", "chaos becomes calm"
  - AI tell: One platitude per <2 sentences

**Scoring rubric:**
- 0-30%: Rich concrete details, specific examples
- 31-60%: Some abstraction but grounded
- 61-85%: High abstraction, vague language dominates
- 86-100%: Almost entirely abstract vapor

### 3. Rhetorical Overengineering (Weight: 15%)

**What to measure:**
- **Chiasmus abuse**: Count chiastic structures (X→Y, Y→X patterns)
  - AI tell: >4 instances per 200 words = systematic deployment
- **Abstraction laddering**: Track sentences that climb abstraction levels without returning to ground
  - Example: concrete → abstract → metaphysical → cosmic
- **Contradiction patterns**: Note claims of subtlety followed by obvious manifestations
  - Example: "This is quiet... It shows up in how [loud obvious things]"

**Scoring rubric:**
- 0-30%: Sparing use of devices for emphasis
- 31-60%: Some overuse but varied
- 61-85%: Systematic device deployment
- 86-100%: Every paragraph uses multiple devices

### 4. Tonal Uncanniness (Weight: 10%)

**What to measure:**
- **Hedging absence**: Count epistemic humility markers (maybe, sometimes, might, could, often)
  - AI tell: Zero instances in subjective claims = absolute certainty
- **Emotional labor asymmetry**: Compare action verbs assigned to different subjects
  - Calculate ratio of action burden
- **Defensive preemption**: Note vague gestures toward balance that don't address core issues

**Scoring rubric:**
- 0-30%: Natural hedging, epistemic humility present
- 31-60%: Some absolutes but balanced
- 61-85%: Mostly absolute claims, minimal hedging
- 86-100%: Zero hedging, universal quantifiers only

### 5. Logical Void (Weight: 20%)

**What to measure:**
- **Tautology count**: Identify circular definitions
  - Example: Defining X by assuming X
- **Evidence-free universalism**: Count universal claims without support
  - Example: "That's why men who provide feel like kings" (citation needed)
- **Confidence-specificity ratio**: Note inverse relationship
  - AI tell: Highest confidence in most abstract claims

**Scoring rubric:**
- 0-30%: Claims supported, specific evidence given
- 31-60%: Some unsupported claims but not pervasive
- 61-85%: Many tautologies and universal claims
- 86-100%: Almost entirely circular reasoning

### 6. Platitude Density (Weight: 20%)

**What to measure:**
- **Meaningful-nothing phrases**: Count statements that sound profound but carry zero specific meaning
  - Examples: "multiply the life you're building", "growth feels natural", "aligned with intention"
- **Frequency**: Calculate platitudes per sentence
  - AI tell: >1 platitude per 2 sentences

**Scoring rubric:**
- 0-30%: Specific, concrete language throughout
- 31-60%: Some vague phrases but mostly substantive
- 61-85%: High platitude frequency
- 86-100%: Nearly every sentence is a platitude

## Output Format

Structure your analysis as follows:

1. **The Original Text** - Quote the full text being analyzed at the top

2. **Table of Contents** - Link to all major sections for easy navigation

3. **Detailed Analysis** - For each dimension:
   - Section header with percentage score
   - Subsections (A, B, C) for specific patterns
   - Quantified counts and ratios
   - **AI Tell** callouts highlighting key patterns
   - Examples from the text with specific quotes

4. **Quantified Scoring Table** - Present all metrics with:
   - Metric name
   - Raw score (0-100%)
   - Weight (percentage)
   - Weighted contribution
   - **Total AI Slop Score** (sum of weighted scores)

5. **Core Theory Section** - Synthesize findings into overarching patterns:
   - Name the phenomenon (e.g., "Rhetorical Autopilot")
   - List 3-5 key principles explaining why it reads as AI
   - Conclude with **The Fatal Tell** - a memorable one-sentence summary

6. **References** - If applicable, cite sources

## Key Principles

### The "Rhetorical Autopilot" Theory

AI slop emerges from five core patterns:

1. **Pattern over substance**: Optimizes for *sounding* persuasive through formulaic devices rather than building actual arguments
2. **Abstraction escape velocity**: Each sentence drifts higher into abstraction to avoid falsifiable claims
3. **Symmetry addiction**: Overuse of balanced structures creates artificial harmony masking logical gaps
4. **Emotional LARP**: Mimics emotional depth through vocabulary without demonstrating it through specificity
5. **Zero revision markers**: No human messiness—no enjambment, broken patterns, or self-correction

### The Fatal Tell

**It reads like a first draft that thinks it's a final draft.**

Human writers create messy first drafts, then refine. AI generates pre-polished text that mistakes rhetorical flourish for earned wisdom.

## Examples

### High AI Slop Score (83%+)

**Characteristics:**
- 4%+ parallel construction density
- 1:3+ abstract-to-concrete ratio
- 6+ chiastic structures per 200 words
- Zero hedging language
- One platitude every 1.8 sentences
- Universal claims without evidence

### Low AI Slop Score (<30%)

**Characteristics:**
- Broken patterns and natural variation
- Rich concrete details and specific examples
- Sparing use of rhetorical devices
- Epistemic humility markers present
- Claims supported with evidence
- Revision markers and organic flow

## Analysis Tips

- **Count systematically**: Don't estimate—actually count patterns, structures, and word types
- **Calculate ratios**: Use precise ratios (e.g., 1:3.3) not ranges
- **Quote extensively**: Pull exact phrases to demonstrate patterns
- **Use tables**: Present quantified data in clear tables
- **Highlight AI tells**: Use ==highlighting== or **bold** for key AI patterns
- **Be precise**: Give exact percentages and counts, not approximations
- **Stay objective**: Focus on measurable patterns, not subjective judgment

## Advanced Patterns

### Compound Patterns

Watch for combinations that amplify AI tells:

- Parallel construction + chiasmus + platitude = Triple threat
- Abstraction ladder + tautology = Circular ascent
- Zero hedging + universal claims = Absolute vapor

### Visual Structure Tells

**Emoji Overuse as Structure**

AI frequently uses emojis mechanically as formatting devices rather than for genuine emotional expression:

**AI Tell patterns:**
- **Emoji bullet points**: Using emojis instead of standard bullets (✓, ✗, 🚀, 💡, 🎯)
- **Systematic deployment**: One emoji per item in a list, mechanically applied
- **Category markers**: Using emojis to mark sections (:brain: for thinking, :computer: for technical)
- **Forced visual interest**: Adding emojis to "break up" text without organic need

**Examples of mechanical emoji usage:**
```
:rocket: Started the process
:brain: Recognized the pattern
:computer: Automated the workflow
```

**Human pattern:** Emojis used sparingly, irregularly, or for actual emotional emphasis ("This is amazing! 🎉")

**AI pattern:** Emojis as structural scaffolding, one per parallel item, creating artificial visual hierarchy

**Scoring impact:** Presence of 3+ mechanical emojis in short text adds +10-15% to slop score

### Context Matters

Consider the domain:

- **Marketing copy**: Higher tolerance for parallelism and abstraction
- **Academic writing**: Higher tolerance for hedging and qualifiers
- **Social media**: Lower expectations for evidence and support
- **Literary prose**: Natural use of rhetorical devices

Adjust thresholds based on genre expectations.

## Common AI Phrases

These phrases are strong indicators of AI-generated content. Human writers rarely use them, but they appear frequently in LLM outputs:

### Opening Phrases
- "what impressed me most"
- "what struck me most"
- "what stands out most"
- "what's fascinating is"
- "what's remarkable is"
- "what's particularly interesting"

### Transition/Connector Phrases
- "it's worth noting that"
- "it's important to note that"
- "it's interesting to note that"
- "it's crucial to understand"
- "it's essential to recognize"
- "this is particularly important"

### Action Verbs (Overused)
- "dive deep into"
- "delve into"
- "unpack this"
- "navigate the complexities"
- "let's explore"
- "let's break this down"

### Hedging Absolutes (Contradictory)
- "here's the thing"
- "the reality is"
- "the truth is"
- "it's no secret that"
- "goes without saying"

### Temporal Clichés
- "at the end of the day"
- "in today's world"
- "in today's landscape"

### Summary Phrases
- "the key takeaway is"
- "the bottom line is"

**Usage tip**: Even one of these phrases in a short text is a significant AI tell. Multiple occurrences strongly suggest AI generation.

## Deterministic Script Usage

This skill includes a Python script (`scripts/sloptastic-analyzer.py`) that calculates deterministic metrics without requiring AI/NLP analysis.

### Quick Start

```bash
# Analyze text from file
python3 scripts/sloptastic-analyzer.py text.txt

# Analyze text from clipboard (macOS)
pbpaste | python3 scripts/sloptastic-analyzer.py --stdin

# Analyze text from stdin
echo "Your text here" | python3 scripts/sloptastic-analyzer.py --stdin
```

### What It Measures

The deterministic script calculates:
- **Connector Disease**: "that's why", "this is because" patterns (>1.5% = AI tell)
- **Hedging Language**: "maybe", "might", "could" markers (zero = absolute certainty)
- **Universal Quantifiers**: "always", "never", "every" (>3 per 100 words = absolutism)
- **Definitional Tautologies**: "X isn't just Y, it's Z" patterns (>2 = strawman habit)
- **Vague Intensifiers**: "real X", "natural growth", "authentic Y"
- **Platitude Density**: Known platitudes from dictionary (>0.5 per sentence = vapor)
- **Common AI Phrases**: "what impressed me most", "it's worth noting", "dive deep", "at the end of the day"
- **Contradiction Patterns**: "quiet/subtle" followed by "shows up in"

### Example: Mild Slop Text

**Input:**
```
What impressed me most (and what was much needed) was how {Person} engaged
with the attendees, listened to their needs, and committed to support their
efforts. On more than one occasion they shared "we're working on it!" in
response to requests from the community.
```

**Output:**
```
## Summary of AI Tells

✗ ZERO hedging language (absolute certainty)
✗ Common AI phrases detected (1)
```

**Interpretation:**
- 2 flags detected
- **Common AI phrase**: "What impressed me most" is a telltale AI opening
- Zero hedging language (no "maybe", "perhaps", "often")
- No connector disease, tautologies, platitudes, or vague intensifiers
- Has specific concrete details ("engaged with attendees", direct quote)
- **Estimated AI Slop Score: ~25-35%** (mild slop - likely AI-influenced or AI-generated)

### Example: High Slop Text

For high slop text (86%+ score), the script will flag:
- ✗ High connector density (1.4%+)
- ✗ ZERO hedging language
- ✗ Multiple tautologies (3+)
- ✗ High platitude density (1.0+ per sentence)
- ✗ Contradiction patterns detected

### When to Use

- **Quick triage**: Fast check before full manual analysis
- **Batch processing**: Analyze multiple texts systematically
- **Objective baseline**: Get quantified metrics to supplement qualitative judgment
- **CI/CD integration**: Automated content quality checks

### Limitations

The script handles deterministic patterns only. For complete analysis, manual review is needed for:
- Parallel construction density (requires parsing)
- Concrete vs abstract noun ratio (requires NLP)
- Chiasmus detection (requires structure analysis)
- Emotional labor asymmetry (requires subject-verb analysis)

## References

For detailed examples and additional patterns, see:
- `references/sloptastic-examples.md` - Complete analysis examples with annotations
