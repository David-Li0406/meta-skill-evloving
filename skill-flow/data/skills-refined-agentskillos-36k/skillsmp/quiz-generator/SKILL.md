---
name: quiz-generator
description: Generate comprehensive educational quizzes based on Bloom's Taxonomy methodology (Remember, Understand, Apply, Analyze, Evaluate, Create). Creates structured True/False quizzes with detailed answer keys and explanations. Use when user requests quiz generation, assessment creation, test materials, practice questions, mentions Bloom's Taxonomy, or provides educational topics for quiz creation. Activates for study topics, course materials, reference files (.md, .txt, .pdf), or educational content requiring systematic assessment.
---

# Quiz Generator

## Purpose

This skill generates comprehensive educational quizzes systematically organized according to Bloom's Taxonomy cognitive levels. It produces True/False assessments with detailed answer keys, explanations, and cognitive level classifications to facilitate learning evaluation and knowledge retention.

## Bloom's Taxonomy Cognitive Levels

The quiz questions shall be organized across six hierarchical cognitive levels:

1. **Remember**: Retrieve relevant knowledge from long-term memory (recall, recognize, identify)
2. **Understand**: Construct meaning from instructional messages (interpret, exemplify, classify, summarize, infer, compare, explain)
3. **Apply**: Carry out or use a procedure in a given situation (execute, implement)
4. **Analyze**: Break material into constituent parts and determine relationships (differentiate, organize, attribute)
5. **Evaluate**: Make judgments based on criteria and standards (check, critique, judge)
6. **Create**: Put elements together to form a coherent whole; reorganize into new pattern (generate, plan, produce, design)

## Instructions

When invoked, execute the following systematic procedure:

### Phase 1: Input Acquisition and Analysis

**Step 1.1**: Determine input source

Identify whether the user has provided:
- A topic title (text-based subject specification)
- A reference file path (existing educational material)
- Both topic and supporting reference materials

**Step 1.2**: Process reference materials (if applicable)

If a reference file is provided:
- Use the Read tool to extract content from the specified file path
- Analyze the content structure, key concepts, and learning objectives
- Identify core terminology, principles, relationships, and factual assertions
- Extract subject domain and complexity level
- Note any existing misconceptions or common errors mentioned

**Step 1.3**: Conduct supplementary research (if necessary)

If the topic is unfamiliar or requires current information:
- Employ WebSearch tool to locate authoritative educational resources
- Use WebFetch tool to retrieve comprehensive explanatory content
- Synthesize multiple sources to ensure accuracy and depth
- Prioritize academic, educational, and authoritative domain sources
- Identify common misconceptions in the domain for use in False statements

### Phase 2: Content Analysis and Concept Mapping

**Step 2.1**: Identify core concepts and factual assertions

Extract or formulate:
- Primary concepts requiring mastery
- Fundamental terminology and definitions
- Key principles, theories, or methodologies
- Factual statements that can be verified as true or false
- Relationships between concepts
- Common misconceptions or errors in the domain
- Procedural knowledge and application contexts

**Step 2.2**: Assess content complexity

Determine appropriate difficulty distribution:
- **Basic**: Foundational concepts, simple factual statements
- **Intermediate**: Conceptual relationships, application scenarios
- **Advanced**: Complex analytical statements, evaluative judgments

**Step 2.3**: Map concepts to Bloom's Taxonomy levels

Systematically categorize identified concepts according to cognitive complexity:
- Level 1 (Remember): Factual statements, definitions, basic identification
- Level 2 (Understand): Conceptual relationships, interpretations, classifications
- Level 3 (Apply): Procedural applications, scenario-based implementations
- Level 4 (Analyze): Structural relationships, comparative analysis, differentiations
- Level 5 (Evaluate): Criteria-based judgments, quality assessments, validity claims
- Level 6 (Create): Design principles, synthesis requirements, optimal solutions

### Phase 3: Quiz Question Generation

**Step 3.1**: Generate 2-3 True/False questions per Bloom's level

For each cognitive level, create True/False questions following this structure:

**True Statement Questions**:
- Formulate accurate statements that test key knowledge at the appropriate cognitive level
- Ensure statements are unambiguously true
- Avoid trivial or overly obvious truths
- Include sufficient context for the statement to be evaluated

**False Statement Questions**:
- Create plausible but incorrect statements
- Base false statements on common misconceptions
- Avoid trick questions with trivial negations (e.g., not just adding "not" to a true statement)
- Ensure the false element is pedagogically meaningful
- Make false statements subtle enough to require genuine understanding

**Step 3.2**: Ensure cognitive alignment

Verify each question employs appropriate cognitive complexity:

**Remember Level** (True/False about facts):
- True: "Python is an interpreted programming language."
- False: "Python was created in the 1970s." (Actually created in 1991)

**Understand Level** (True/False about concepts and relationships):
- True: "Encapsulation in OOP involves bundling data and methods that operate on that data within a single unit."
- False: "Inheritance and composition serve identical purposes in object-oriented design." (They serve different purposes)

**Apply Level** (True/False about applications):
- True: "In a binary search tree with root value 10, a node with value 5 would be located in the left subtree."
- False: "The quicksort algorithm always has O(n log n) time complexity regardless of input." (Worst case is O(n²))

**Analyze Level** (True/False about analysis):
- True: "The primary difference between arrays and linked lists is that arrays provide O(1) random access while linked lists require O(n) traversal."
- False: "Hash tables and binary search trees have identical time complexity characteristics for all operations." (They differ significantly)

**Evaluate Level** (True/False about judgments):
- True: "Using a microservices architecture is more appropriate than a monolithic architecture when different components need to scale independently."
- False: "Test-driven development (TDD) is always superior to writing tests after implementation in all software projects." (Context-dependent)

**Create Level** (True/False about design and synthesis):
- True: "When designing a caching system for a high-traffic website, setting expiration times based on data update frequency is a sound strategy."
- False: "The optimal database schema design always involves complete normalization to 3rd normal form without exception." (Denormalization is sometimes appropriate)

**Step 3.3**: Maintain balanced True/False distribution

Across the entire quiz, maintain approximately:
- 50% True statements
- 50% False statements

Avoid patterns (e.g., alternating T/F or multiple consecutive same answers) that enable answering without reading.

### Phase 4: Answer Key and Explanation Generation

**Step 4.1**: Create comprehensive answer key

For each question, provide:

```markdown
**Question [Number]**: [Bloom's Level] - [Difficulty]

**Statement**: [The True/False statement]

**Answer**: [True/False]

**Explanation**:
[Detailed explanation of why the statement is true or false, including:
- Core concept being tested
- Relevant facts or principles
- Why the statement is correct or what makes it incorrect
- Additional context for understanding]

**Common Misconception** (if applicable):
[Why students might incorrectly answer this question]

**Related Concepts**:
- [Related concept 1]
- [Related concept 2]
```

**Step 4.2**: Ensure pedagogical value

Verify that explanations:
- Clarify the underlying concept, not just the answer
- Provide learning value beyond answer verification
- Address potential misconceptions
- Connect to broader conceptual understanding
- Reference authoritative principles where applicable

### Phase 5: Quality Assurance

**Step 5.1**: Verify statement accuracy

Confirm all True statements are factually correct and all False statements are genuinely incorrect. Cross-reference authoritative sources when uncertain.

**Step 5.2**: Assess cognitive level alignment

Ensure each question genuinely tests the designated Bloom's level:
- Remember: Tests factual recall, not reasoning
- Understand: Tests conceptual comprehension, not mere memorization
- Apply: Tests procedural application in scenarios
- Analyze: Tests ability to identify relationships and structures
- Evaluate: Tests judgment based on criteria
- Create: Tests understanding of optimal design and synthesis

**Step 5.3**: Eliminate ambiguity

Verify that:
- Statements are clear and unambiguous
- No statement can be reasonably interpreted as both true and false
- Context is sufficient for evaluation
- Terminology is used correctly and consistently

**Step 5.4**: Check pedagogical quality

Ensure:
- False statements represent meaningful misconceptions, not trivial errors
- Questions test important concepts, not obscure trivia
- Difficulty is appropriate for the target learning level
- Coverage is comprehensive across the topic domain

### Phase 6: Output Formatting and Delivery

**Step 6.1**: Structure the quiz document

Organize the output markdown file with the following structure:

```markdown
# Quiz: [Topic Title]

**Generated**: [Current Date]
**Cognitive Framework**: Bloom's Taxonomy
**Question Type**: True/False
**Total Questions**: [Count]
**Recommended Time**: [Estimate based on question count]

---

## Instructions

Read each statement carefully and determine whether it is TRUE or FALSE. Consider the statement as a whole and apply your understanding of [topic].

---

## Questions

### Level 1: Remember (Knowledge Recall)

**Question 1**: [Bloom's Level - Remember] [Difficulty: Basic/Intermediate/Advanced]

[True/False statement]

- [ ] True
- [ ] False

---

**Question 2**: [Bloom's Level - Remember] [Difficulty: Basic/Intermediate/Advanced]

[True/False statement]

- [ ] True
- [ ] False

---

[Continue for all Remember level questions]

### Level 2: Understand (Comprehension)

[Questions 3-5 for Understand level]

### Level 3: Apply (Application)

[Questions 6-8 for Apply level]

### Level 4: Analyze (Analysis)

[Questions 9-11 for Analyze level]

### Level 5: Evaluate (Evaluation)

[Questions 12-14 for Evaluate level]

### Level 6: Create (Synthesis)

[Questions 15-18 for Create level]

---

## Answer Key

### Level 1: Remember

**Question 1**: Remember - [Difficulty]

**Statement**: [Repeat statement]

**Answer**: [True/False]

**Explanation**:
[Detailed explanation]

**Common Misconception** (if applicable):
[Why students might answer incorrectly]

**Related Concepts**:
- [Concept 1]
- [Concept 2]

---

[Continue for all questions across all levels]

---

## Quiz Statistics

- **Total Questions**: [Number]
- **True Statements**: [Count]
- **False Statements**: [Count]
- **Distribution by Level**:
  - Remember: [Count] questions
  - Understand: [Count] questions
  - Apply: [Count] questions
  - Analyze: [Count] questions
  - Evaluate: [Count] questions
  - Create: [Count] questions

---

## Study Recommendations

[Provide guidance on how to use this quiz effectively for learning]
```

**Step 6.2**: Generate output file

Use the Write tool to create a markdown file named:
`[topic-name]-quiz.md`

Where `[topic-name]` is the kebab-case version of the topic title.

**Step 6.3**: Deliver completion summary

Provide the user with:
- Confirmation of successful generation
- Total question count (target: 12-18 questions)
- File path for the generated quiz
- Recommended completion time estimate
- Brief usage recommendations

## Advanced Considerations

### Avoiding Common Pitfalls in True/False Question Design

**Pitfall 1: Trivial Negation**
- **Poor**: "Python is not an interpreted language." (Just negates a fact)
- **Better**: "Python compiles directly to machine code like C." (Tests understanding of compilation vs interpretation)

**Pitfall 2: Absolute Language Creating Obvious Answers**
- **Poor**: "All loops in programming are while loops." (Absolute language signals false)
- **Better**: "Loop structures in programming serve the fundamental purpose of repeating code blocks." (True statement without absolute language)

**Pitfall 3: Multiple Concepts in Single Statement**
- **Poor**: "Python is interpreted and dynamically typed and uses garbage collection." (Multiple testable elements)
- **Better**: Split into separate questions testing each concept individually

**Pitfall 4: Opinion Presented as Fact**
- **Poor**: "Python is the best programming language for beginners." (Subjective opinion)
- **Better**: "Python's syntax is designed to emphasize code readability." (Verifiable design principle)

### Crafting Effective False Statements

False statements should:
1. **Test Misconceptions**: Base false statements on actual common errors students make
2. **Require Understanding**: Students must understand the concept to identify the falsehood
3. **Be Plausible**: False statements should seem potentially true to someone with incomplete knowledge
4. **Avoid Trick Wording**: Don't rely on tricky phrasing or obscure semantic details

**Example of Effective False Statement**:
- Statement: "In object-oriented programming, composition means one class inheriting from another class."
- Why Effective: Confuses composition with inheritance, a common misconception; requires understanding the distinction
- Not Effective Alternative: "Composition is not a concept in object-oriented programming." (Obviously false, not educational)

### Balancing Difficulty

Distribute questions across difficulty levels:
- **Basic** (40%): Test foundational knowledge and clear concepts
- **Intermediate** (40%): Test application and conceptual relationships
- **Advanced** (20%): Test nuanced understanding and complex scenarios

Higher Bloom's levels (Analyze, Evaluate, Create) naturally tend toward intermediate/advanced difficulty.

## Error Handling

**Insufficient Input**:
If the user provides neither a clear topic nor reference file, request:
- Specific topic title or subject area
- Optional reference file path for context

**Reference File Unavailable**:
If the specified reference file cannot be read:
- Inform the user of the file access issue
- Offer to proceed with topic-based generation using web research

**Topic Unfamiliarity**:
If the topic is highly specialized or obscure:
- Conduct thorough web research using WebSearch and WebFetch
- Inform the user that research-based generation is in progress
- Request user validation of accuracy for highly technical domains

**Insufficient Content**:
If the topic or reference material provides insufficient content for 12-18 questions:
- Generate fewer questions while maintaining Bloom's level distribution
- Inform user of reduced question count and reasoning
- Suggest supplementary topics or materials for comprehensive coverage

## Quality Standards

All generated quizzes shall conform to:

1. **Bloom's Taxonomy Alignment**: Each question correctly categorized by cognitive level
2. **Statement Clarity**: All True/False statements are unambiguous and clearly written
3. **Factual Accuracy**: All True statements are verifiable; all False statements are genuinely incorrect
4. **Pedagogical Value**: Questions test important concepts and meaningful understanding
5. **Answer Key Completeness**: Every question has detailed explanation and related concepts
6. **Balanced Distribution**: Approximately 50% True, 50% False across entire quiz
7. **Misconception-Based**: False statements target actual common misunderstandings
8. **Difficulty Appropriateness**: Complexity matches designated Bloom's level and difficulty rating

## Example Invocation Scenarios

**Scenario 1**: Topic-based generation
```
User: "Generate a quiz for Python list comprehensions"
Agent: [Conducts web research, generates 12-18 True/False questions across Bloom's levels]
```

**Scenario 2**: Reference file-based generation
```
User: "Create a quiz from my machine learning notes at notes/ml-basics.md"
Agent: [Reads file, extracts concepts, generates structured quiz with answer key]
```

**Scenario 3**: Combined approach
```
User: "Generate a quiz for photosynthesis based on my biology-notes.pdf"
Agent: [Reads PDF, supplements with web research, generates comprehensive quiz]
```

## References

This skill implements pedagogical principles derived from:
- Bloom's Taxonomy of Educational Objectives (Bloom et al., 1956; Anderson & Krathwohl, 2001)
- Assessment design principles for True/False question construction
- Cognitive science research on effective assessment and misconception identification
- Educational testing standards for valid and reliable assessment instruments
