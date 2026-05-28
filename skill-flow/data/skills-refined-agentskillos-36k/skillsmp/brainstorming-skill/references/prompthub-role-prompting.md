# PromptHub: Role Prompting Empirical Research

**Source URL**: <https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference>

**Publication Date**: 2024

---

## Executive Summary

Comprehensive meta-analysis of persona/role-prompting effectiveness across multiple research studies (2023-2024) reveals a nuanced landscape: simple personas ("You are X") provide minimal-to-negative effects on accuracy tasks, while detailed, automatically-generated personas show moderate improvements on specific domains. Effectiveness is sharply divided by task category, persona construction method, and model generation (older models show larger gains than GPT-4/Claude).

**Key Verdict**: Personas are NOT universally beneficial. Task type and persona complexity determine actual impact.

---

## Research Studies & Empirical Findings

### Study 1: "Better Zero-Shot Reasoning with Role-Play Prompting" (March 2024)

**Model Tested**: GPT-3.5-turbo-0613

**Methodology**: Two-stage approach

- Role-Setting Prompt (establish persona)
- Role-Feedback Prompt (reinforce persona context)

**Key Results**:

| Task Type              | Baseline Accuracy | With Persona          | Improvement          |
| ---------------------- | ----------------- | --------------------- | -------------------- |
| AQuA (math problems)   | 53.5%             | 63.8%                 | +10.3%               |
| Arithmetic             | ~baseline         | ~baseline+10%         | ~+10% average        |
| Common sense reasoning | Variable          | Variable              | Variable gains       |
| Symbolic reasoning     | Baseline          | Strongest improvement | High gains           |
| Data understanding     | Baseline          | Moderate gains        | Moderate improvement |

**Critical Caveats**:

- Requires handcrafted prompts (not automated)
- Unclear if results generalize to newer models (GPT-4, Claude)
- Multiple model runs required for optimization

---

### Study 2: "When 'A Helpful Assistant' Is Not Really Helpful" (November 2024)

**Scope**: Comprehensive analysis across 4 model families, 2,410+ factual questions (MMLU dataset)

**Verdict**: Personas in system prompts showed **NO IMPROVEMENT** and "sometimes negative effects"

**Critical Finding**: Research team originally supported personas but **reversed position after reanalysis**

**Performance by Gender-Based Role**:

| Role Type            | Performance Effect        | Effect Size                           |
| -------------------- | ------------------------- | ------------------------------------- |
| Gender-neutral roles | Slight positive           | Negligibly small                      |
| Masculine roles      | Minimal positive          | Negligibly small                      |
| Feminine roles       | Negative effect           | Negligibly small                      |
| Overall effect       | No meaningful improvement | Effect too small to predict best role |

**Key Insight**: "Adding personas in system prompts did not improve model performance"

---

### Study 3: "Persona is a Double-edged Sword" (August 2024)

**Framework**: Jekyll & Hyde (automatic persona generation + dual-path solving + evaluation)

**Models Tested**: GPT-4, Llama 3-8b

**Results by Dataset**:

| Dataset                  | Base Performance | With Persona | Outcome            |
| ------------------------ | ---------------- | ------------ | ------------------ |
| AQuA                     | Baseline         | +Large gains | Persona helps      |
| Multiarith (GPT-4)       | Strong           | Weaker       | Base outperforms   |
| Single Equation          | Strong           | Weaker       | Base outperforms   |
| Average (GPT-4 backbone) | Baseline         | +9.98%       | Modest improvement |

**Critical Observation**: "Gap between 'Persona' and 'Base' for GPT-4 is very small"

**Implication**: Automated persona generation helps some tasks but introduces inconsistency across domains.

---

### Study 4: "ExpertPrompting: Instructing Large Language Models to be Distinguished Experts" (May 2023)

**Methodology**: LLM-generated detailed personas using in-context learning

**Persona Construction Requirements**:

- Specific, detailed descriptions (not generic roles)
- Generated automatically via LLM
- Includes domain-specific context
- Built with in-context learning examples

**Performance Comparison**:

| Approach                               | Performance  | Notes                        |
| -------------------------------------- | ------------ | ---------------------------- |
| Vanilla prompting                      | Baseline     | No persona                   |
| Vanilla + static description           | ~Baseline    | Minimal improvement          |
| Expert Prompting (automated, detailed) | Strong gains | "Destroys the other methods" |

**Key Principle**: Personas must be **specific, detailed, and automated** to provide meaningful gains

**Critical Finding**: Simple personas underperform; complex, LLM-generated personas excel

---

### Study 5: Learn Prompting Experiment (Summer 2024)

**Dataset**: 2,000 MMLU questions

**Model**: GPT-4-turbo

**Personas Tested**: 12 different roles including:

- Genius persona (emphasized expertise, always correct)
- Idiot persona (emphasized incompetence, failure)
- Domain specialist roles
- Neutral baseline

**Finding**: Persona effects were **negligible across all 12 roles**

**Striking Result**: "Idiot" persona outperformed "genius" persona

**Implication**: Intuitive assumptions about persona quality (expertise = better performance) are contradicted by empirical data

---

## Pattern Effectiveness Comparison

### Effectiveness by Pattern Type

| Pattern Type                             | Task Category           | Effectiveness        | Strength of Evidence      |
| ---------------------------------------- | ----------------------- | -------------------- | ------------------------- |
| Simple personas ("You are X")            | Accuracy/Classification | Minimal to negative  | Strong (multiple studies) |
| Simple personas                          | Creative/Open-ended     | High                 | Moderate                  |
| Detailed, automated personas             | Accuracy/Classification | Moderate             | Moderate                  |
| Detailed, automated personas             | Specialized reasoning   | Moderate to positive | Moderate                  |
| LLM-generated personas (ExpertPrompting) | General tasks           | Positive             | Moderate                  |
| Gender-based personas                    | Factual questions       | Negligible           | Strong                    |

### Effectiveness by Model Generation

| Model Family      | Simple Persona Effect           | Detailed Persona Effect | Notes                                  |
| ----------------- | ------------------------------- | ----------------------- | -------------------------------------- |
| GPT-3.5-turbo     | +10% average improvement        | Moderate gains          | Older model; larger persona impact     |
| GPT-4             | Minimal effect (very small gap) | Small to moderate gains | Newer model; personas less impactful   |
| Claude (inferred) | Minimal effect (very small gap) | Small to moderate gains | Newer model; personas less impactful   |
| Llama 3-8b        | Mixed results (task-dependent)  | Task-dependent          | Open-source; variable persona response |

---

## Task-Based Performance Patterns

### High-Effectiveness Domains for Personas

1. **Open-ended/Creative Tasks**

   - Content generation
   - Brainstorming
   - Creative writing
   - Problem ideation
   - Expected gain: High

2. **Safety/Values Alignment**

   - Establishing guardrails
   - Content filtering
   - Behavior guidance
   - Expected gain: Moderate to high

3. **Complex Reasoning with Detailed Personas**
   - Multi-step problem solving
   - Symbolic reasoning
   - Arithmetic reasoning (with ExpertPrompting)
   - Expected gain: Moderate

### Low-Effectiveness Domains for Personas

1. **Factual Accuracy Tasks**

   - MMLU classification
   - Knowledge-based QA
   - Factual recall
   - Expected gain: Negligible to negative

2. **Classification/Labeling Tasks**

   - Document categorization
   - Sentiment analysis
   - Text classification
   - Expected gain: Negligible

3. **Tasks with Modern Language Models**
   - GPT-4 based
   - Claude-based
   - Newer Llama versions
   - Expected gain: Minimal (gap "very small")

---

## Critical Variables Affecting Persona Effectiveness

### 1. Persona Complexity

**Finding**: Complexity level directly correlates with effectiveness

**Spectrum**:

- Generic roles ("You are a lawyer"): Minimal effect
- Detailed roles (with background, expertise, context): Moderate effect
- Automatically-generated roles (LLM-crafted with domain context): Best effect

### 2. Construction Method

**Effective**: LLM-generated personas using in-context learning

- Uses model's own knowledge to create detailed context
- Includes domain-specific nuances
- Maintains consistency with task requirements

**Ineffective**: Manual, simple role descriptions

- Generic descriptions
- No domain-specific context
- No customization per task

### 3. Task Structure

**Personas help**: Open-ended, creative, or abstract tasks **Personas fail**: Accuracy-dependent, classification, or factual tasks

**Mechanism**: Personas establish tone/style (helpful for creativity) but don't add knowledge/accuracy (required for facts)

### 4. Model Capability Level

**Inverse relationship observed**:

- Older/weaker models (GPT-3.5): Larger persona gains (~10%)
- Newer/stronger models (GPT-4, Claude): Negligible gains (gap "very small")

**Interpretation**: Advanced models already follow instructions optimally; personas add minimal signal

### 5. Gender/Demographic Representation

**Surprising Finding**: Gender of persona shows measurable but negligible effects

- Masculine personas: Minimal positive effect
- Feminine personas: Negative effect
- Gender-neutral personas: Slight positive effect

**Overall**: Effect "so small" that predicting best role is unsolved

---

## Practical Guidance for Brainstorming Applications

### When to Use Personas in Brainstorming

**Effective Use Cases**:

1. **Establishing creative tone**: "You are a visionary product designer brainstorming radical innovations"

   - Helps generate bold, unconventional ideas
   - Shifts perspective and ideation patterns
   - Expected benefit: High

2. **Cross-disciplinary ideation**: "You are a biologist approaching this business problem"

   - Brings domain-specific thinking patterns
   - Encourages novel solution approaches
   - Expected benefit: Moderate to high

3. **Safety/values alignment**: "You are an ethical AI reviewing ideas for potential harms"

   - Establishes evaluation criteria
   - Guides feedback tone
   - Expected benefit: Moderate to high

4. **Ensemble brainstorming**: Multiple detailed personas generating ideas separately, then synthesized
   - Leverages persona diversity
   - Combines multiple perspectives
   - Expected benefit: Moderate (if personas differ meaningfully)

### When to Avoid Personas

**Ineffective Use Cases**:

1. Expecting personas to improve accuracy or correctness

   - Won't help factual accuracy
   - Won't improve technical correctness
   - Won't enhance knowledge-based answers

2. Using generic, simple role descriptions

   - "You are a business expert" provides no value
   - "Think like a scientist" offers minimal signal
   - Research shows these are negligible

3. Relying on intuitive persona selection
   - "Genius" persona empirically underperformed "Idiot" persona
   - Intuitive assumptions about what makes good personas are unreliable
   - Requires automated/detailed construction to be effective

### Best Practices for Persona-Based Brainstorming

**If Using Personas**:

1. **Generate detailed, specific personas automatically**

   - Use ExpertPrompting approach: LLM generates detailed persona with context
   - Include background, expertise specifics, and domain knowledge
   - Don't rely on manual one-liners

2. **Match persona to creative goal**

   - Use open-ended brainstorming (where personas excel)
   - Avoid accuracy-dependent evaluation (where personas fail)
   - Combine persona-based ideation with separate verification step

3. **Use multiple diverse personas in ensemble**

   - Generate 3-5 contrasting personas
   - Have each solve/brainstorm independently
   - Synthesize results manually or via meta-reasoning
   - This approach leverages persona diversity for richer output

4. **Combine personas with other prompt techniques**

   - Personas alone show modest gains
   - Personas + structured templates: Better
   - Personas + example outputs: Better
   - Personas + chain-of-thought reasoning: Better

5. **Verify creative outputs separately**
   - Personas help ideation quality
   - Don't assume personas improve accuracy
   - Use separate verification/evaluation step for correctness
   - This matches study findings: personas help creativity, not accuracy

---

## Consensus & Limitations

### Research Consensus

**Key Points of Agreement Across Studies**:

1. Simple personas provide minimal-to-negative effects on accuracy tasks
2. Detailed, automatically-generated personas show promise but modest gains
3. Newer models (GPT-4, Claude) show diminished persona effects vs. older models
4. Task type matters more than persona type
5. Open-ended tasks benefit; accuracy tasks don't

### Known Limitations

1. **Generalization uncertainty**: Most studies use GPT-3.5 and GPT-4

   - Unclear how findings apply to other models (Claude variants, open-source LLMs)
   - Model capabilities improve; persona effects may shift

2. **Task representation bias**: Heavy focus on factual/academic tasks (MMLU, math)

   - Creative task evaluation is harder to quantify
   - Real-world brainstorming effects under-researched

3. **Interaction effects under-explored**:

   - How do personas combine with other prompt techniques?
   - Multi-prompt strategies not well studied
   - Ensemble effects mentioned but not systematically evaluated

4. **Persona construction methods**:
   - ExpertPrompting showed promise but limited replication
   - Automated persona generation methods not standardized
   - Template-based personas (vs. LLM-generated) need more comparison

---

## Implications for Brainstorming Skill Design

### Recommended Approach

**Personas are valuable for brainstorming but require proper implementation**:

1. **Frame personas as perspective-shifters, not accuracy-enhancers**

   - Document that personas help ideation, not verification
   - Recommend detailed personas over simple ones
   - Suggest ensemble (multiple personas) over single persona

2. **Provide detailed persona templates for brainstorming**

   - Include background, expertise, thinking style
   - Don't rely on generic descriptions
   - Make personas specific to ideation domain

3. **Combine personas with structured output**

   - Personas + templates: Better ideation
   - Personas + examples: Clearer direction
   - Personas + evaluation criteria: Better filtering

4. **Document effectiveness trade-offs**
   - Personas work best for creative/open-ended tasks
   - Don't recommend for accuracy-dependent phases
   - Use separate verification steps

### Documentation Priority

For brainstorming skill:

1. HIGH: Creative persona use cases (where personas excel)
2. MEDIUM: Detailed persona construction (ExpertPrompting model)
3. MEDIUM: Ensemble brainstorming strategies
4. LOW: Accuracy applications (where personas fail)

---

## References

1. "Better Zero-Shot Reasoning with Role-Play Prompting" (March 2024) - GPT-3.5-turbo, AQuA dataset, +10.3% improvement
2. "When 'A Helpful Assistant' Is Not Really Helpful" (November 2024) - 4 model families, 2,410+ MMLU questions, no improvement finding
3. "Persona is a Double-edged Sword" (August 2024) - Jekyll & Hyde framework, GPT-4 + Llama 3-8b, mixed results
4. "ExpertPrompting: Instructing Large Language Models to be Distinguished Experts" (May 2023) - Detailed persona approach, strong gains
5. Learn Prompting Experiment (Summer 2024) - 2,000 MMLU questions, GPT-4-turbo, 12 personas tested, negligible effects

---

## See Also

[Pattern Categories and Documentation](./pattern-categories-and-documentation.md) - Comprehensive brainstorming pattern library

[Synthesis: What Makes These Patterns Work](./synthesis-what-makes-these-patterns-work.md) - Underlying mechanisms for brainstorming effectiveness
