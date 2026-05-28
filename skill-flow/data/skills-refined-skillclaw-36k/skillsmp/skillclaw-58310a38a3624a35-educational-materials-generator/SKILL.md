---
name: educational-materials-generator
description: Use this skill when you need to create structured educational materials such as notes, quizzes, or flashcards based on Bloom's Taxonomy, tailored to specific topics or learning objectives.
---

# Educational Materials Generator

## Purpose

This skill generates comprehensive educational materials, including notes, quizzes, and flashcards, systematically organized according to Bloom's Taxonomy cognitive levels. It adapts to the complexity of the topic and provides structured learning resources to enhance understanding and retention.

## Bloom's Taxonomy Cognitive Levels

The materials will be organized across six hierarchical cognitive levels:

1. **Remember**: Recall facts, terms, and basic concepts.
2. **Understand**: Explain ideas and interpret information.
3. **Apply**: Use knowledge in concrete situations.
4. **Analyze**: Break down information and identify relationships.
5. **Evaluate**: Make judgments and critique information.
6. **Create**: Synthesize information and produce original work.

## Instructions

### Phase 1: Input Acquisition and Analysis

**Step 1.1: Determine Input Source**

Identify whether the user has provided:
- A topic title (text-based subject specification)
- A reference file path (existing educational material)
- Both topic and supporting reference materials

**Step 1.2: Process Reference Materials (if applicable)**

If a reference file is provided:
- Use the Read tool to extract content from the specified file path.
- Analyze the content structure, key concepts, and learning objectives.
- Identify core terminology, principles, and relationships.
- Extract subject domain and complexity level.

**Step 1.3: Conduct Supplementary Research (if necessary)**

If the topic is ambiguous or lacks sufficient detail:
- Use WebSearch to gather authoritative information:
  ```
  Query pattern: "[topic] tutorial", "[topic] fundamentals", "[topic] comprehensive guide"
  ```
- Use WebFetch to retrieve 2-3 high-quality sources (educational sites, documentation, academic resources).
- Synthesize gathered information.

### Phase 2: Material Generation

**Step 2.1: Generate Notes**

- Structure notes based on the identified Bloom's Taxonomy levels.
- Include summaries, practice questions, and visual diagrams as appropriate.

**Step 2.2: Generate Quizzes**

- Create True/False quizzes or other formats based on the cognitive levels.
- Provide detailed answer keys and explanations.

**Step 2.3: Generate Flashcards**

- Develop flashcards with difficulty ratings, detailed explanations, and practice hints.
- Organize flashcards according to the cognitive levels for effective review.

### Final Output

Deliver the generated educational materials in a structured format suitable for the user's needs, ensuring clarity and educational value.