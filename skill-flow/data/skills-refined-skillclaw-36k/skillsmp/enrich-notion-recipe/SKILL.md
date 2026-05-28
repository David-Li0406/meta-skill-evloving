---
name: enrich-notion-recipe
description: Guide for enriching recipes in Notion with images, tags, ratings, and notes
user-invocable: true
disable-model-invocation: false
---

# Enrich Notion Recipes

Guide for manually enriching recipes in Notion with additional metadata that enhances browsing and planning.

## What is Recipe Enrichment?

Recipe enrichment means adding extra information to your recipes in Notion beyond what's in the .cook files:
- **Images**: Recipe photos for visual browsing
- **Tags**: Dietary tags, cuisine types, cooking method tags
- **Ratings**: Star ratings (1-5) after cooking
- **Last Cooked**: Track when you last made this recipe
- **Notes**: Variations, substitutions, what worked/didn't work

## Why Enrich in Notion?

Files (.cook) remain the source of truth for recipes. Notion is where you add:
- Visual elements (images, ratings)
- Subjective data (ratings, personal notes)
- Organizational metadata (tags for filtering)
- Cooking history (last cooked dates)

These enrichments persist across syncs and make browsing/planning easier.

## How to Enrich

### 1. Add Recipe Images

Two ways to add images:

**Auto-lookup (coming soon - Phase 2.2)**:
- Sync script will automatically search for recipe images
- Images are added as external URLs during first sync

**Manual upload**:
1. Open recipe in Notion
2. Click the Image property
3. Upload a photo or paste image URL
4. Best sources: recipe website, your own photos

### 2. Add Tags

Click the Tags multi-select property and add:

**Dietary Tags**:
- vegetarian
- vegan
- gluten-free
- dairy-free

**Speed Tags**:
- quick (<30 min)
- batch-friendly
- slow-cooker

**Audience Tags**:
- kid-friendly
- entertaining
- meal-prep

**Cuisine Tags**:
- Italian
- Mexican
- Asian
- Mediterranean
- American

### 3. Rate Recipes

After cooking a recipe:
1. Open in Notion
2. Set Rating property: ⭐ to ⭐⭐⭐⭐⭐
3. Use ratings to find your favorites
4. Filter recipes by 4-5 stars for special occasions

### 4. Track Last Cooked

1. Set Last Cooked date property after making a recipe
2. Use this for meal rotation:
   - Avoid repeating recipes too often
   - Rediscover recipes you haven't made recently
3. Sort by Last Cooked to find forgotten favorites

### 5. Add Notes

Use the Notes rich text field for:
- Variations you've tried
- Ingredient substitutions that worked
- Adjustments to cooking times/temperatures
- Serving suggestions
- What family members thought

## Enrichment Workflow

Recommended workflow:

1. **After importing**: Add tags if obvious (vegetarian, quick, etc.)
2. **After first cook**: Rate the recipe, add Last Cooked date
3. **After multiple cooks**: Add notes about variations/adjustments
4. **Periodically**: Upload photos for your favorite recipes

## Views to Use

### Gallery View (Default)
- Visual grid of recipes with images
- Great for browsing
- Filter by tags/ratings

### Table View
- Detailed list with all properties
- Good for planning and analysis
- Sort by Last Cooked, Rating, Time Required

### Filtered Views
Create custom views:
- "Quick Dinners": Time Required <30 min, Category=dinner
- "Favorites": Rating ⭐⭐⭐⭐⭐
- "Need to Retry": Last Cooked >60 days ago, Rating ⭐⭐⭐+

## Sync Behavior

**Enrichments are preserved**:
- When files sync to Notion, enrichments (tags, ratings, images, notes) are NOT overwritten
- Only recipe content fields (ingredients, instructions, metadata) are updated
- Your enrichments persist across syncs

**What gets updated**:
- Name (from filename)
- Category (from directory)
- Source, Time Required, Servings (from YAML frontmatter)
- Ingredients, Instructions (from .cook file content)
- File Path (identifier)
- Last Synced (timestamp)

**What is preserved**:
- Image (unless empty)
- Tags
- Rating
- Last Cooked
- Notes

## Example Enrichment Session

```
User: "I just made pasta carbonara and it was amazing. Help me enrich it in Notion."

Claude: "Great! Let's enrich the Pasta Carbonara recipe:

1. Rating: How would you rate it? (1-5 stars)"
User: "5 stars!"

Claude: "2. Tags: Should I add any tags? Suggestions:
   - Italian (cuisine)
   - quick (<30 min)
   - kid-friendly"
User: "Yes, all of those"

Claude: "3. Last Cooked: Marking as cooked today (2026-01-23)"

Claude: "4. Notes: Any variations or observations?"
User: "I added extra black pepper and used guanciale instead of bacon"

Claude: "Updated! Your Pasta Carbonara is now enriched:
⭐⭐⭐⭐⭐ | Italian, quick, kid-friendly | Last cooked: 2026-01-23
Notes: Extra black pepper, guanciale substitution

View in Notion: [URL]"
```

## Tips

- Don't over-enrich initially - add details as you cook recipes
- Use consistent tag names across recipes
- Take photos of your best results to upload later
- Review ratings after 2-3 cooks to confirm initial impression
- Use notes field liberally - future you will thank you

---

**Remember**: Files are source of truth for recipes. Notion is for enhancement and organization.
