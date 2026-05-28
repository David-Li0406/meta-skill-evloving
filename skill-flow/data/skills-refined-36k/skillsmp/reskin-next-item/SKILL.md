---
name: reskin-next-item
description: Select and execute a single legacy reskin checklist item by priority (repositories before services) and by fewest dependencies; use when choosing the next item from docs\progress\checklist.md or when progressing the reskin one item at a time.
---

# Reskin Next Item

Use this skill to pick one checklist item to work on, then scope the work to just that item while following the reskin plan and extraction loop.

## Workflow

### 1) Load reskin rules and checklist
- Read the reskin definition at `docs\refactor-plan\reskin-definition.md`.
- Read the sequencing rules and constraints at `docs\refactor-plan\refactor-plan.md`.
- Read the extraction loop checklist at `docs\refactor-plan\refactor-todo.md`.
- Open `docs\progress\checklist.md` and collect all unchecked items.

### 2) Build the candidate set
- If any unchecked repositories exist, choose only from repositories.
- Otherwise choose from services.

### 3) Score candidates by dependency count
Goal: select the item with the fewest dependencies on other checklist items.

For each candidate item:
- Use the path from the checklist to open the file.
- Build a list of other checklist item names (repositories + services).
- Count unique references from the candidate file to other checklist item names.
  - Prefer using `rg -n -F` on the candidate file for each name or with a names list file.
  - Treat each distinct referenced item as a dependency (count once).

Service-specific rule:
- Services typically depend on repositories. If a service references unchecked repositories, treat those as dependencies and prefer services with fewer or already-reskinned repositories.

### 4) Pick the next item
- Select the candidate with the smallest dependency count.
- Tie-breaker order: fewer unchecked dependencies, then alphabetical by item name.
- Do not reorder the checklist; only select the next item to act on.

### 5) Execute only that item
- Follow the extraction loop checklist in `docs\refactor-plan\refactor-todo.md`.
- Keep changes scoped to the selected item and its minimal required dependencies.
- If you discover an unknown pattern, add it to the Unknown Patterns Backlog in `docs\refactor-plan\refactor-todo.md`.
- Mark the item as reskinned in `docs\progress\checklist.md` only when the reskin definition is met.

### 6) Report in the response
Include:
- Selected item name and path.
- Dependency count and the specific dependencies found.
- Why it was chosen (priority + dependency rationale).
- Next actions to complete the item.
