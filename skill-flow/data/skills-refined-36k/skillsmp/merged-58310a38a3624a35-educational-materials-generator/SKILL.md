---
name: educational-materials-generator
description: Use this skill to generate comprehensive educational materials, including notes, quizzes, and flashcards, based on Bloom's Taxonomy methodology. Ideal for creating structured learning resources, assessments, and review materials across various topics.
---

# Educational Materials Generator

## Purpose

This skill generates structured educational materials, including notes, quizzes, and flashcards, organized according to Bloom's Taxonomy cognitive levels. It produces comprehensive learning resources that facilitate understanding, retention, and assessment.

## Bloom's Taxonomy Cognitive Levels

The materials will be organized across six hierarchical cognitive levels:

1. **Remember**: Retrieve relevant knowledge from long-term memory (recall, recognize, identify)
2. **Understand**: Construct meaning from instructional messages (interpret, exemplify, classify, summarize, infer, compare, explain)
3. **Apply**: Carry out or use a procedure in a given situation (execute, implement)
4. **Analyze**: Break material into constituent parts and determine relationships (differentiate, organize, attribute)
5. **Evaluate**: Make judgments based on criteria and standards (check, critique, judge)
6. **Create**: Put elements together to form a coherent whole; reorganize into new patterns (generate, plan, produce, design)

## Instructions

### Phase 1: Input Acquisition and Analysis

**Step 1.1: Determine Input Source**

Identify whether the user has provided:
- A topic title (text-based subject specification)
- A reference file path (existing educational material)
- Both topic and supporting reference materials

**Step 1.2: Process Reference Materials (if applicable)**

If a reference file is provided:
- Use the Read tool to extract content from the specified file path
- Analyze the content structure, key concepts, and learning objectives
- Identify core terminology, principles, and relationships
- Extract subject domain and complexity level

**Step 1.3: Conduct Supplementary Research (if necessary)**

If the topic is unfamiliar or requires current information:
- Employ WebSearch tool to locate authoritative educational resources
- Use WebFetch tool to retrieve comprehensive explanatory content
- Synthesize multiple sources to ensure accuracy and depth
- Prioritize academic, educational, and authoritative domain sources

### Phase 2: Content Analysis and Concept Mapping

**Step 2.1: Identify Core Concepts and Learning Objectives**

Extract or formulate:
- Primary concepts requiring mastery
- Fundamental terminology and definitions
- Key principles, theories, or methodologies
- Practical applications and use cases
- Complex analytical relationships
- Critical evaluation criteria
- Creative synthesis opportunities

**Step 2.2: Assess Content Complexity**

Determine appropriate difficulty distribution:
- **Beginner**: Foundational concepts, basic terminology, simple recall
- **Intermediate**: Conceptual understanding, application, comparative analysis
- **Advanced**: Complex analysis, critical evaluation, creative synthesis

**Step 2.3: Map Concepts to Bloom's Taxonomy Levels**

Systematically categorize identified concepts according to cognitive complexity:
- Level 1 (Remember): Facts, definitions, terminology, basic concepts
- Level 2 (Understand): Explanations, interpretations, relationships, examples
- Level 3 (Apply): Procedures, implementations, practical applications
- Level 4 (Analyze): Component relationships, structural analysis, differentiations
- Level 5 (Evaluate): Criteria-based judgments, critiques, assessments
- Level 6 (Create): Novel solutions, designs, integrated syntheses

### Phase 3: Material Generation

#### Notes Generation

**Step 3.1: Generate Structured Notes**

For each selected Bloom level, generate structured points and a visual diagram. Include an executive summary, practice questions, and references.

#### Quiz Generation

**Step 3.2: Generate True/False Questions**

For each cognitive level, create 2-3 True/False questions. Ensure cognitive alignment and maintain a balanced distribution of true and false statements.

#### Flashcard Generation

**Step 3.3: Generate Flashcards**

For each cognitive level, create 5-8 flashcards. Include difficulty ratings, detailed explanations, and practice hints.

### Phase 4: Quality Assurance

**Step 4.1: Verify Content Accuracy**

Confirm all factual content is accurate, current, and appropriately sourced.

**Step 4.2: Assess Pedagogical Effectiveness**

Verify that:
- Questions and materials are clear, unambiguous, and appropriately scoped
- Answers and explanations provide meaningful learning value
- Related concepts enhance conceptual understanding

### Phase 5: Output Formatting and Delivery

**Step 5.1: Structure the Output Document**

Organize the output markdown file with the following structure:

```markdown
# Educational Materials: [Topic Title]

**Generated**: [Current Date]
**Cognitive Framework**: Bloom's Taxonomy
**Total Materials**: [Count]

---

## Notes

[Structured notes content]

---

## Quiz

[Quiz questions and answer key]

---

## Flashcards

[Flashcards content]

---

## Study Recommendations

[Provide brief guidance on how to use these materials effectively]
```

**Step 5.2: Generate Output File**

Use the Write tool to create a markdown file named:
`[topic-name]-materials.md`

Where `[topic-name]` is the kebab-case version of the topic title.

**Step 5.3: Deliver Completion Summary**

Provide the user with:
- Confirmation of successful generation
- Total materials count
- File path for the generated educational materials
- Brief usage recommendations

## Advanced Features Implementation

### Difficulty Ratings

Assign difficulty based on:
- Cognitive level (higher levels tend toward intermediate/advanced)
- Concept complexity (specialized terminology, abstract concepts)
- Required prerequisite knowledge
- Multi-step reasoning requirements

### Answer Explanations

Elaborations shall:
- Provide contextual background
- Clarify reasoning processes
- Connect to broader conceptual frameworks
- Anticipate common misconceptions

## Error Handling

**Insufficient Input**:
If the user provides neither a clear topic nor reference file, request:
- Specific topic title or subject area
- Optional reference file path for context

**Reference File Unavailable**:
If the specified reference file cannot be read:
- Inform the user of the file access issue
- Offer to proceed with topic-based generation using web research

## Quality Standards

All generated materials shall conform to:

1. **Bloom's Taxonomy Alignment**: Each material correctly categorized by cognitive level
2. **Pedagogical Soundness**: Questions facilitate genuine learning, not mere memorization
3. **Factual Accuracy**: All content verified against authoritative sources
4. **Clarity**: Questions and answers are unambiguous and well-articulated
5. **Completeness**: All components present and well-structured
6. **Systematic Coverage**: Balanced distribution across Bloom's levels

## Example Invocation Scenarios

**Scenario 1**: Topic-based generation
```
User: "Generate educational materials for Python list comprehensions"
Agent: [Conducts web research, generates structured notes, quiz, and flashcards]
```

**Scenario 2**: Reference file-based generation
```
User: "Create educational materials from my notes on machine learning at notes/ml-basics.md"
Agent: [Reads file, extracts concepts, generates structured educational materials]
```

**Scenario 3**: Combined approach
```
User: "Generate educational materials for quantum computing based on lecture-notes.pdf"
Agent: [Reads PDF, supplements with web research, generates comprehensive educational materials]
```

## References

This skill implements pedagogical principles derived from:
- Bloom's Taxonomy of Educational Objectives (Bloom et al., 1956; Anderson & Krathwohl, 2001)
- Cognitive science principles of effective assessment and learning strategies