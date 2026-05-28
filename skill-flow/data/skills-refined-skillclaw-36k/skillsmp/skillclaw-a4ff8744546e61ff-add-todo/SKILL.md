---
name: add-todo
description: Use this skill to add a properly formatted TODO item to TODOS.md, ensuring it integrates with existing systems and follows the correct structure.
---

# Add TODO Item

This skill allows you to add a new TODO item to `TODOS.md` with proper formatting.

## Instructions

1. **Check for `TODOS.md`:**
   - If it exists, read it to understand the current structure.
   - If it does not exist, create it with the standard template.

2. **Gather Information:**
   - Use the following questions to collect details for the TODO item:
     - **Title:** What is the TODO item? (brief, actionable title)
     - **Priority:** What priority level? (P0, P1, P2)
     - **Effort:** What is the estimated effort? (Low, Medium, High)
     - **Description:** (Optional) Provide a brief description of the item.

3. **Format the TODO Item:**
   - Use the following format for the TODO item:
     ```markdown
     - [ ] **[{Priority} / {Effort}]** {Title} — {Brief description}
     ```
   - Ensure to include any relevant tags or status markers as needed.

4. **Add the Item:**
   - Insert the formatted TODO item into the appropriate section of `TODOS.md`:
     - Quick fixes → **Quick Add**
     - New features → **Features**
     - Bug reports → **Bugs**
     - UI/UX issues → **Fixes**
     - Code quality items → **Technical Debt**

5. **Confirm Addition:**
   - Review what was added and where to ensure accuracy.

## Example TODO Item

```markdown
- [ ] **[P1 / Medium]** Add user authentication — Support OAuth and email/password
```