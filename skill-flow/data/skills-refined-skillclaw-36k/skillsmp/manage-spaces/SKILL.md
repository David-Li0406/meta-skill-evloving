---
name: manage-spaces
description: List, create, or manage memory spaces. Use when user says "show my spaces", "create a space", "organize my memories", or wants to manage categorization.
allowed-tools: mcp__aiii__list_spaces, mcp__aiii__create_space
---

# Manage Spaces

Help users view and manage their memory spaces.

## When to Use

- User wants to see available spaces
- User wants to create a new space
- User wants to understand how memories are organized
- User is setting up aiii for the first time

## Instructions

### Listing Spaces

1. **Query available spaces**:
   - Use `list_spaces` tool
   - Include memory counts for each

2. **Present in a clear format**:

   ```
   ## Your Memory Spaces

   | Space | Memories | Icon |
   |-------|----------|------|
   | Work | 47 | 💼 |
   | Health | 12 | 🏥 |
   | Learning | 8 | 📚 |
   ```

3. **Offer actions**:
   - Create new space
   - View memories in a space
   - Explain space purpose

### Creating Spaces

1. **Gather information**:
   - Space name (required)
   - Icon/emoji (optional, suggest based on name)
   - Purpose description

2. **Suggest appropriate names**:
   - Work, Projects, Career
   - Health, Fitness, Nutrition
   - Learning, Reading, Courses
   - Finance, Budget, Investments
   - Personal, Family, Relationships

3. **Create the space**:

   ```json
   {
     "name": "Space Name",
     "icon": "emoji"
   }
   ```

4. **Confirm creation**:
   - Show the new space
   - Explain how to save memories to it
   - Suggest setting up auto-categorization

## Default Spaces

For new users, suggest these starter spaces:

| Space    | Icon | Purpose                              |
| -------- | ---- | ------------------------------------ |
| Work     | 💼   | Professional tasks, coding, meetings |
| Health   | 🏥   | Medical, fitness, nutrition          |
| Learning | 📚   | New skills, courses, reading         |
| Finance  | 💰   | Budget, investments, purchases       |

## Example Interactions

**User:** "Show my spaces"
→ List all spaces with memory counts

**User:** "Create a space for my side project"
→ Ask for name, suggest icon, create space

**User:** "What spaces should I set up?"
→ Explain common spaces, offer to create defaults
