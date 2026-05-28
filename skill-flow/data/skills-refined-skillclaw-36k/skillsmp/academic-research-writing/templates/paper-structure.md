# Paper Structure Templates

Structural templates for scientific manuscript sections.

---

## Introduction Arc

### Template

```markdown
## Introduction

[BROAD CONTEXT - 1-2 sentences]
Establish the general importance of the field/topic. Why should anyone care?

[NARROW FOCUS - 2-3 sentences]
What has been done in this specific area? What do we already know?

[KNOWLEDGE GAP - 1-2 sentences]
What is missing? What remains unknown? Use explicit gap language:
- "However, X remains poorly understood..."
- "Despite these advances, it is unclear whether..."
- "A critical unanswered question is..."

[HYPOTHESIS/OBJECTIVE - 1-2 sentences]
What will this study address? Be specific:
- "Here, we test the hypothesis that..."
- "In this study, we aimed to..."
- "We investigated whether..."
```

### Example

```
Cancer remains a leading cause of mortality worldwide, with metastasis
accounting for the majority of cancer-related deaths [BROAD CONTEXT].
Epithelial-to-mesenchymal transition (EMT) has been identified as a key
process enabling tumor cell invasion and dissemination, with transcription
factor X shown to be overexpressed in aggressive tumors [NARROW FOCUS].
However, the molecular mechanisms by which X promotes metastasis remain
incompletely understood [KNOWLEDGE GAP]. Here, we test the hypothesis
that X drives metastasis through direct transcriptional activation of
pro-migratory genes Y and Z [HYPOTHESIS].
```

---

## Results Paragraph

### Template

```markdown
[QUESTION - What did this experiment address?]
To determine whether [specific question]...

[APPROACH - How was it done?]
We performed [method] using [key details]...

[FINDING - What was observed? Include numbers]
We found that [quantitative result] (Figure X). Specifically,
[detailed finding with statistics: mean +/- SD, p-value, n]...

[INTERPRETATION - What does this mean?]
This result indicates that [biological/clinical meaning]...
```

### Example

```
To determine whether compound X inhibits tumor cell migration, we performed
transwell migration assays using MDA-MB-231 breast cancer cells [QUESTION +
APPROACH]. Treatment with compound X (10 uM) reduced cell migration by 65%
compared to vehicle control (p<0.001, n=6; Figure 2A) [FINDING]. Furthermore,
this inhibition was dose-dependent, with IC50 = 2.3 uM (Figure 2B). These
results indicate that compound X is a potent inhibitor of tumor cell
migration at pharmacologically relevant concentrations [INTERPRETATION].
```

---

## Discussion Opening

### Template

```markdown
[MAIN FINDING SUMMARY - 1-2 sentences]
In this study, we demonstrated that [main finding]. This finding
[supports/refutes/extends] our hypothesis that [restate hypothesis].

[SIGNIFICANCE STATEMENT - 1 sentence]
These results are significant because [why this matters].
```

### Example

```
In this study, we demonstrated that compound X inhibits tumor cell migration
through direct binding to receptor Y, leading to reduced downstream signaling.
This finding supports our hypothesis that the X-Y interaction represents a
druggable node in the metastatic cascade. These results are significant because
they identify a novel therapeutic target for preventing cancer metastasis.
```

---

## Limitations Section

### Template

```markdown
[LIMITATION 1]
Our study has several limitations. First, [limitation] which may affect
[how it impacts interpretation]. Future studies should [how to address].

[LIMITATION 2]
Second, [limitation]. Although we attempted to mitigate this by [what
you did], [residual concern].

[LIMITATION 3]
Finally, [limitation]. This will be important to address in [future work].

[CONCLUDING STATEMENT]
Despite these limitations, our findings [what can still be concluded].
```

### Common Limitations by Category

| Category | Examples |
|----------|----------|
| **Sample** | Small n, specific population, cell lines vs. primary cells |
| **Methods** | Single timepoint, indirect measurements, lack of gold standard |
| **Scope** | One disease model, limited conditions tested |
| **Causation** | Correlation vs. causation, lack of mechanism |
| **Generalizability** | In vitro vs. in vivo, model limitations |

---

## Standard Paper Structure

```
1. Title and Abstract
   - Concise title reflecting the main contribution
   - Abstract: 150-250 words (context, gap, approach, findings)

2. Introduction
   - Motivation and problem statement
   - Research gap and significance
   - Main contributions (3-5 bullet points)
   - Paper organization paragraph

3. Related Work / Background
   - Literature review by theme
   - Comparison with existing approaches
   - Positioning of current work

4. Methodology / Approach / System Design
   - Detailed description of proposed method
   - Architecture diagrams if applicable
   - Algorithms or procedures
   - Design decisions and rationale

5. Implementation (if applicable)
   - Technical details
   - Tools and technologies
   - Challenges and solutions

6. Evaluation / Experiments / Results
   - Experimental setup
   - Datasets or test scenarios
   - Performance metrics
   - Results presentation (tables, graphs)
   - Analysis and interpretation

7. Discussion
   - Implications of results
   - Limitations and threats to validity
   - Lessons learned

8. Conclusion and Future Work
   - Summary of contributions
   - Impact and significance
   - Future research directions

9. References
   - Comprehensive bibliography
```
