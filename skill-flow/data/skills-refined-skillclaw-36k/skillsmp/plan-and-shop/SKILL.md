---
name: plan-and-shop
description: Interactive meal planning for the week with automatic shopping list generation
user-invocable: true
disable-model-invocation: true
---

# Plan and Shop

Guide the user through weekly meal planning and automatically generate a shopping list.

## Workflow

1. **Get the week starting date**:
   - Ask user for the week starting date (YYYY-MM-DD format)
   - Default to next Monday if not specified

2. **Check calendar** ✅ NOW WORKING:
   - Query Notion Calendar for the week using `scripts/calendar_integration.py`
   - Run: `python3 scripts/calendar_integration.py --week <date>`
   - Analyze each day's schedule to determine:
     - Number of events (busyness level)
     - Available cooking time (e.g., "30-45 min", "60+ min")
     - Estimated attendees (2 default, 4+ if family/party events)
     - Whether eating out for any meals
   - Display calendar summary showing constraints for each day
   - Use constraints to filter and suggest appropriate recipes

3. **List available recipes**:
   - Scan all recipe categories:
     ```bash
     cd /Users/beno/Documents/Projects/lifeAutomations/mealPlanner
     find recipes/breakfast -name "*.cook" -exec basename {} .cook \;
     find recipes/lunch -name "*.cook" -exec basename {} .cook \;
     find recipes/dinner -name "*.cook" -exec basename {} .cook \;
     find recipes/snacks -name "*.cook" -exec basename {} .cook \;
     find recipes/desserts -name "*.cook" -exec basename {} .cook \;
     ```
   - Display recipes organized by category

3. **Create meal plan file**:
   - Copy the template:
     ```bash
     cp meal-plans/week-template.txt meal-plans/week-<date>.txt
     ```
   - Fill in the date placeholder

4. **Help user plan meals** (with calendar-aware suggestions):
   - For each day (Monday-Sunday):
     - **Show calendar constraints** if available:
       - Display available cooking time (e.g., "Monday: Busy day, 30-45 min available")
       - Show attendee count if differs from usual (e.g., "4 people - family dinner")
       - Note if eating out ("Dinner out - skip cooking")
     - **Suggest appropriate recipes** based on constraints:
       - Busy days → Quick recipes (<30 min)
       - Guests/family → Recipes that serve 4+
       - Ample time → Any recipe
     - Ask what they want for breakfast, lunch, dinner
     - Reference available recipes by category
     - Fill in the meal plan using format: `Day | Meal | category/recipe-name.cook`
   - Ask about snacks for the week

5. **Save the meal plan**:
   - Write the completed meal plan to `meal-plans/week-<date>.txt`
   - Show the user a summary of planned meals

6. **Generate shopping list**:
   ```bash
   ./scripts/generate-shopping-list.sh meal-plans/week-<date>.txt
   ```

7. **Sync to Notion** ✅ NOW WORKING:
   - After creating meal plan file, automatically sync to Notion
   - Creates Meal Plan page with week date
   - Creates Meal Entries for each meal with recipe relations
   - Enables visual calendar view in Notion
   - Run: `python3 scripts/sync-to-notion.py --mode meal-plans`

8. **Display the shopping list**:
   - Show the consolidated ingredient list
   - Indicate where the file was saved
   - Note that duplicate ingredients are automatically combined

## Example Interaction

```
User: /plan-and-shop

Claude: "What week are you planning for? (YYYY-MM-DD for Monday)"
User: "2026-01-27"

Claude: "Checking your calendar for week of 2026-01-27..."

📅 WEEK ANALYSIS
Monday, January 27
- 2 event(s): Team meeting, Dentist appointment
- ⏱️  Available prep time: 45-60 min
- 💡 Suggestions: Moderate complexity recipes okay

Tuesday, January 28
- 📭 No events - full day available
- ⏱️  Dinner prep time: 90+ min

Wednesday, January 29
- 1 event(s): Dinner with friends
- 🍽️  Dinner out - skip cooking

Thursday, January 30
- 3 event(s): Client call, Workshop, Pickup kids
- ⏱️  Available prep time: 30-45 min
- 👥 Estimated attendees: 4 (Event with guests)
- 💡 Suggestions: Busy day - suggest quick recipes, plan for 4 people

Claude: "Here are your available recipes (filtered by calendar constraints):
BREAKFAST: oatmeal, pancakes
LUNCH: caesar-salad, chicken-wrap
DINNER: pasta-carbonara, stir-fry
..."

Claude: "Let's plan your week. Monday breakfast?"
User: "pancakes"

Claude: "Monday dinner? (45-60 min available)"
User: "pasta-carbonara"

Claude: "Tuesday dinner? (90+ min available - full day free)"
User: "slow-cooker-beef-stew"

Claude: "Wednesday: Dinner out - skipping cooking"

Claude: "Thursday dinner? (30-45 min available, 4 people)"
Suggested quick recipes: chicken-tacos (20 min, serves 4), stir-fry (25 min, serves 4)
User: "chicken-tacos"

... (continues for remaining meals)

Claude: "Meal plan saved to meal-plans/week-2026-01-27.txt"
Claude: "Generating shopping list..."
Claude: "Shopping list created at shopping-lists/shopping-list-20260122-143000.txt

Your shopping list:
- spaghetti: 400 g
- bacon: 200 g
- eggs: 4
..."
```

## Planning Options

- **Quick plan**: User can provide meals upfront: "pasta carbonara Monday dinner, stir fry Tuesday dinner"
- **Skip meals**: Leave blank for meals eating out or leftovers
- **Repeat meals**: Same recipe can be used multiple times

## Tips

- Start with dinners (usually most important)
- Consider batch cooking for multiple lunches
- Leave some flexibility for eating out
- Check pantry before generating list

## Shortcuts

If user says:
- "Same as last week" → Copy previous week's meal plan
- "Just dinners" → Only ask for dinner meals
- "Skip breakfast" → Leave breakfast slots empty

## Error Handling

- If recipe doesn't exist, suggest similar names or list all recipes
- If no recipes available in a category, suggest importing some first
- If meal plan file already exists, ask whether to overwrite or edit

## Calendar Integration

Calendar integration is **fully functional** and provides smart meal suggestions:

**How It Works**:
1. Queries Notion Calendar database for the week being planned
2. Analyzes each day's schedule complexity:
   - 0 events → Full day available (90+ min dinner prep)
   - 1-2 events → Moderate (45-60 min dinner prep)
   - 3+ events → Busy day (30-45 min dinner prep)
3. Detects special conditions:
   - Eating out (dinner/lunch out keywords)
   - Family/guest events (suggests 4+ servings)
   - Available cooking time windows
4. Filters recipe suggestions by time and servings constraints

**Calendar Analysis Output**:
```
📅 Analyzing calendar for week of 2026-01-27...

Monday, January 27
- 2 event(s): Team meeting, Dentist
- ⏱️  Available prep time: 45-60 min

Thursday, January 30
- 3 event(s): Client call, Workshop, Pickup kids
- ⏱️  Available prep time: 30-45 min
- 👥 Estimated attendees: 4
- 💡 Suggestions: Busy day - suggest quick recipes, plan for 4 people
```

**Recipe Filtering**:
- Busy days → Recipes with time ≤ 30 min
- Moderate days → Recipes with time ≤ 60 min
- Free days → All recipes available
- Guest events → Recipes that scale to 4+ servings

**Configuration**:
- Calendar database ID must be set in `.notion/config.json`
- If calendar not configured, proceeds with normal meal planning

## Integration

This skill combines:
1. `./scripts/meal-plan.sh` functionality (interactive planning)
2. `./scripts/generate-shopping-list.sh` (shopping list generation)
3. `./scripts/calendar_integration.py` (smart recipe suggestions)
4. `./scripts/sync-to-notion.py` (Notion sync)

Into a single streamlined workflow.