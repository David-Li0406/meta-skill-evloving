---
name: collaborative_design
description: 実装方針・作業内容の吟味・修正を、ユーザーとAIの会話で行う。ユーザーからの指示があるまでは、勝手にコーディング作業に取りかからない
---

# Collaborative Design & Planning

This skill serves as a guideline for ensuring the AI does not proceed with implementation unilaterally, but instead determines the optimal design and policy through dialogue with the user.

## Core Principle: Conversation First

When high-level design decisions (API design, selection of complex physical logic, large-scale refactoring) are required, the AI prioritizes making a **proposal** and obtaining user approval above all else.

### 1. Pre-implementation "Review" Process
- **Presentation of Choices**: Clearly state trade-offs such as Proposal A (Batch processing/Simple) vs. Proposal B (Extraction-based/Memory-efficient), and present the pros and cons to the user.
- **Verification of Physical/Mathematical Validity**: Discuss with the user whether the equations or normalizations are physically correct before implementation.
- **User Experience (UX) of the API**: Align beforehand on how the user will call the code (e.g., `field.psd()` vs. `compute_psd(field)`).

### 2. Trigger for Starting Work (Explicit Approval)
- While discussing plans or designs, **do not modify the project's source code**, no matter how confident you are.
- Update and share the implementation plan using `setup_plan` or `archive_plan`, and explicitly ask the user, "May I proceed with this plan?"
- Only use coding tools (e.g., `write_to_file`) after receiving affirmative instructions from the user, such as "Proceed," "Go," or "Approved."

### 3. Permitted "Pre-work"
Non-destructive tasks to enhance the accuracy of discussion and analysis can be performed in parallel.
- **Analysis of Existing Code**: Understand the current state using `view_file` or `grep_search`.
- **Prototype Verification**: Create and execute temporary verification scripts (without modifying the project core).
- **Skill Updates**: Solidify knowledge gained through dialogue into agent skills.

## Workflow
1.  **Listen**: Deeply understand the user's requirements and the underlying intent.
2.  **Propose**: Present plan or design proposals in Markdown format.
3.  **Refine**: Receive user feedback and revise/improve the proposal until satisfied.
4.  **Commitment**: After obtaining approval, complete the implementation in one go.
