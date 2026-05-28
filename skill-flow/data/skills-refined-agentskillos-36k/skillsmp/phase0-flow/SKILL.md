---
name: phase0-flow
description: A markdown-driven conversational meal planning workflow that results in verified shopping lists and PDF recipes.
---

# Phase 0 Conversational Meal Planning Workflow

This skill guides you through the "Phase 0" markdown-driven conversational meal planning flow. The goal is to produce a complete meal plan, a verified shopping list, and PDF recipes without a UI.

## Table of Contents

- [Overview](#overview)
- [Workflow Steps](#workflow-steps)
  - [Step 1: The Request](#step-1-the-request)
  - [Step 2: The Options](#step-2-the-options)
  - [Step 3: Ingredient Verification & Provisional Recipes](#step-3-ingredient-verification--provisional-recipes)
  - [Step 4: Shopping List Verification](#step-4-shopping-list-verification)
  - [Step 5: Final Plan & PDFs](#step-5-final-plan--pdfs)
- [File Structure](#file-structure)

## Overview

- **Tone**: Use plenty of emojis to make the process fun and engaging! 🥳
- **Agent's Role**: You are responsible for creating, editing, and deleting markdown files in `phase0_flow/plans/`. You must commit changes after each step.
- **Tools**: Use standard file operations. For PDF generation, use the `just` command.

## Workflow Steps

### Step 1: The Request

1.  **Context**: The user has created a `01-request.md` in a new plan directory (e.g., `phase0_flow/plans/YYYY-MM-DD_my-plan/`).
2.  **Action**: Read `01-request.md`, `phase0_flow/stock_lists/`, and `phase0_flow/general_preferences/`.
3.  **Goal**: Understand the user's needs, constraints, and current inventory.

### Step 2: The Options

1.  **Action**: Generate 4-5 high-level meal plan summaries based on the request.
2.  **Output**: Create `02-options.md` in the plan directory.
    -   Each option should have a theme.
    -   List key *new* ingredients to buy for each option.
3.  **Commit**: Commit the changes.
4.  **Interaction**: **STOP EXECUTION.** Present the options to the user and ask them to choose one via chat. Do not proceed to Step 3 until the user has made a choice.

### Step 3: Ingredient Verification & Provisional Recipes

1.  **Trigger**: User selects an option.
2.  **Action**: Create a comprehensive ingredient checklist AND provisional recipes for the selected plan.
3.  **Output 1**: Create `03-verification.md`.
    -   List *all* ingredients required for the plan.
    -   Categorize them (Produce, Dairy, Pantry, etc.).
    -   Pre-check (`[x]`) items you believe are in stock based on `stock_lists`.
    -   Leave unknown/out-of-stock items unchecked (`[ ]`).
4.  **Output 2**: Create individual markdown files for each recipe in a `recipes/` subdirectory.
    -   These are "provisional" drafts to ensure all spices, garnishes, and techniques (like velveting) are documented.
    -   Ensure recipes include specific "Flavor Layer" and "Kid Submeal" notes.
5.  **Commit**: Commit the changes.
6.  **Interaction**: **STOP EXECUTION.** Ask the user to review the provisional recipes and `03-verification.md`. Do not proceed to Step 4 until the user confirms the ingredients and recipes.

### Step 4: Shopping List Verification

*Crucial Step: Ensure nothing is missed!*

1.  **Trigger**: User confirms inventory.
2.  **Action**:
    -   Read the updated `03-verification.md`.
    -   **Cross-Reference**: Explicitly check *every single ingredient* in the planned recipes against the user's verified inventory.
    -   Identify any discrepancies or missing items.
3.  **Interaction**: **STOP EXECUTION.** If you find missing items or ambiguities, ask the user for clarification before proceeding. If everything is perfect, you may ask for final confirmation to proceed to generation.

### Step 5: Final Plan & PDFs

1.  **Action**: Generate the final assets.
2.  **Output 1: Markdown Plan**: Create `04-final-plan.md`.
    -   Include the final menu.
    -   Include the **Consolidated Shopping List** (only items strictly needed).
    -   Include full recipes with instructions.
3.  **Output 2: Recipe Files**: Finalize individual recipe markdown files in the `recipes/` subdirectory.
    -   Format them according to standard recipe markdown (Title, Ingredients, Instructions).
4.  **Output 3: PDFs**: Run the PDF generation command.
    -   Command: `just all` (This targets the latest plan directory automatically).
5.  **Commit**: Commit all new files (markdown plan, recipe files, and generated PDFs).
6.  **Completion**: Inform the user that the plan and PDFs are ready! 📄✨

## File Structure Reference

```text
phase0_flow/
  stock_lists/
    pantry.md, fridge.md, ...
  general_preferences/
    staple_meals.md, ...
  plans/
    YYYY-MM-DD_plan-name/
      01-request.md
      02-options.md
      03-verification.md
      04-final-plan.md
      recipes/
        recipe-1.md
        pdfs/
          recipe-1.pdf
```
