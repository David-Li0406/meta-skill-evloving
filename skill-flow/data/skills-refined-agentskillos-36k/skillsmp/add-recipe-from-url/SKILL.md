---
name: add-recipe-from-url
description: Import a recipe from a URL, categorize it, and validate the Cooklang format
user-invocable: true
disable-model-invocation: true
---

# Add Recipe from URL

Import a recipe from a cooking website into the meal planner system.

## Workflow

When the user provides a recipe URL:

1. **Ask for category** if not provided:
   - breakfast
   - lunch
   - dinner
   - snacks
   - desserts

2. **Import the recipe** using CookCLI:
   ```bash
   cd /Users/beno/Documents/Projects/lifeAutomations/mealPlanner
   ./scripts/import-recipe.sh url "<URL>" <category>
   ```

3. **Find the imported file**:
   - CookCLI creates the file in `recipes/<category>/`
   - Look for the most recently created `.cook` file

4. **Preview the recipe**:
   ```bash
   cook recipe <imported-file-path>
   ```
   Show the user:
   - Recipe name
   - Ingredients list
   - Cooking steps
   - Any metadata (servings, time, etc.)

5. **Validate the recipe**:
   ```bash
   ./scripts/validate-recipes.sh
   ```
   Report any warnings or errors in the Cooklang syntax

6. **Sync to Notion** (automatic):
   - Auto-sync hook triggers after recipe file is created
   - Recipe is synced to Notion Recipes database
   - Notion page URL is available for immediate browsing

7. **Summarize** what was imported and where it's located

## Example Usage

```
User: /add-recipe-from-url https://example.com/chicken-curry
→ "Which category? (breakfast/lunch/dinner/snacks/desserts)"
→ User: "dinner"
→ Import recipe to recipes/dinner/
→ Preview imported content
→ Run validation
→ "Successfully imported Chicken Curry to recipes/dinner/chicken-curry.cook"
```

## Error Handling

- If the URL is invalid or inaccessible, inform the user
- If CookCLI can't parse the recipe, suggest using the manual import mode
- If validation shows errors, explain what needs to be fixed

## Notes

- CookCLI supports many popular recipe websites
- Some sites may not be supported - offer manual text import as alternative
- The imported recipe may need manual cleanup for optimal formatting
