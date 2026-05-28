---
name: requirement-analysis
description: Use this skill when you need to verify the completeness of requirements, analyze the current state of code, and provide a foundation for design proposals.
---

# Skill: Requirement Analysis

This skill is designed to ensure the completeness of requirements and analyze the existing codebase to inform design decisions.

## Execution Process

1. **Phase A: Requirement Evaluation**
   - **Step 1: Check Knowledge Base Status**
     - Ensure the working directory contains code files and the requirement is not "new project".
     - Use a quick decision tree for evaluation.
   - **Step 2: Gather Project Context**
     - Execute a quick process to gather project context, checking the knowledge base first.
   - **Step 3: Determine Requirement Type**
     - Identify if the requirement triggers product design principles (new project, major feature refactor, etc.).
   - **Step 4: Requirement Completeness Scoring**
     - Score the completeness of the requirement based on clarity, expected outcomes, boundaries, and constraints.
     - If the score is below 7, output follow-up questions to clarify the requirement.

2. **Phase B: Code Analysis (if score ≥ 7)**
   - **Step 5: Extract Key Objectives and Success Criteria**
     - Identify the core objectives from the complete requirements.
   - **Step 6: Code Analysis and Technical Preparation**
     - Assess project scale, locate relevant modules, and perform quality checks.
     - Analyze logs or error messages if available.

## Scoring Criteria

- **Clarity of Objectives (0-3 points)**
- **Expected Outcomes (0-3 points)**
- **Boundary Clarity (0-2 points)**
- **Constraints (0-2 points)**

## Follow-Up Questions (if score < 7)

If the requirement completeness score is below 7, output the following format:

```
❓【HelloAGENTS】- Requirement Analysis

Current requirement completeness score is X/10, unable to clarify optimization goals and expected outcomes.

1. What specific file or module do you want to optimize?
2. What specific issues need optimization? (e.g., performance, code duplication)
3. What outcomes do you expect from the optimization?
4. Are there specific performance metrics or time constraints?

Please respond with the number of your question, or type "continue with current requirements" to skip the follow-up (may affect solution quality).
```

## Output Format

- Use Markdown for reports and ensure clarity in the presentation of information.