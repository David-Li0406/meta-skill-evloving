---
name: technical-documentation-optimizer
description: Use this skill when you need to enhance technical documentation by ensuring accuracy, clarity, and consistency between code and documentation.
---

# Skill body

## Overview

This skill is designed to optimize technical documentation, ensuring it is accurate, clear, and consistent with the corresponding code. It combines content refinement with strict documentation maintenance rules.

## Process

When provided with a draft of technical documentation or code changes, follow these steps:

### 1. Review Logic and Code

- **Technical Accuracy**: Verify that technical concepts and principles are correctly described. Note any significant errors.
- **Logical Completeness**: Identify any circular reasoning, logical fallacies, or weak arguments.
- **Code Correctness**: Ensure code snippets adhere to best practices and are correctly formatted. Highlight any pseudocode that is not clearly defined.
- **Output**: Summarize findings in a review report. If no issues are found, state "Review passed."

### 2. Eliminate Redundancies and Refine Content

#### 2.1 Paragraph-Level Redundancy Detection

- **Synonymous Repetition**: Merge paragraphs that express the same idea while retaining unique arguments, data, and examples.
- **Beginning and Ending Repetition**: Ensure the introduction and conclusion do not restate the same content; the conclusion should focus on "next steps" or "further reading."
- **Transitional Redundancy**: Remove phrases like "as mentioned earlier" and replace them with logical transitions.

#### 2.2 Sentence-Level Refinement

- **Weak Verbs**: Replace phrases like "made an optimization" with "optimized."
- **Redundant Modifiers**: Simplify phrases such as "very important" to "critical."
- **Contentless Sentences**: Remove transitional sentences that do not add substantial information.

### 3. Handle Ambiguous Expressions

- **Data-Supported Claims**: Retain and ensure the accuracy of data.
- **Unsupported Claims**: Avoid fabricating data. Replace vague phrases like "significantly improved" with "improved" or add a note: `<!-- TODO: Add specific data -->`.
- **Vague Quantifiers**: Replace terms like "many" or "significant" with more cautious expressions if they cannot be quantified.

### 4. Professionalize Tone and Remove "AI Flavor"

- **Prohibited Vocabulary**: Avoid phrases like "let's explore" or "this article will introduce." Use direct statements instead.
- **Tone Requirements**: Adopt an authoritative and direct tone, akin to that of a seasoned engineer.

### 5. Documentation Maintenance Rules

#### Rule 1: Adding New Modules

When creating a new top-level folder (module) in the business module directory:

1. Create a corresponding `[module-name].md` in `tap-agents/prompts/modules/`.
2. Update `tap-agents/prompts/module-map.md` with a module description.

#### Rule 2: Modifying Existing Modules

When modifying a module's code:

1. Check if the module's documentation exists.
2. If it exists but is outdated, update the relevant sections.
3. If it does not exist, create it.
4. Notify the user: "Updated [module-name] documentation."

#### Rule 3: Major Refactoring

For cross-module refactoring, deletion, or code movement:

1. Update all involved modules' documentation.
2. Mark deprecated modules in `module-map.md`.

#### Rule 4: Handling Documentation-Code Inconsistencies

- **Code Newer than Documentation**: Trust the code and automatically update the documentation.
- **Indeterminate State**: Stop modifications and consult the user about discrepancies.
- **Clear Errors**: Directly fix documentation errors.

#### Rule 5: Automatic Documentation Maintenance

Automatically create documentation when code is modified and the corresponding documentation does not exist.

### 6. SEO and Metadata Optimization

- **Title**: Ensure it is accurate, professional, and includes keywords.
- **Meta Description**: Provide a concise summary of less than 160 characters.

## Output Format

### Review Report

```markdown
## Review Report

### Technical Accuracy and Logic
[Technical errors, logical fallacies list, or "Review passed"]

### Code Review
[Code issues list, or "Review passed"]

### Redundancy Issues
[Identified paragraph/sentence-level redundancies and resolutions]

### Structural Issues
[Title hierarchy, narrative flow issues, and corrections]

### SEO Suggestions
- **Title**: [Suggested title]
- **Meta**: [Suggested description]
```

### Optimized Complete Content

Directly output the optimized complete Markdown document without additional explanation.