---
name: sync-to-notion
description: Sync recipes and meal plans to Notion for enhanced browsing
user-invocable: true
disable-model-invocation: false
---

# Sync to Notion

Synchronize meal planning files to Notion databases for rich visual browsing, meal planning calendar views, and recipe enrichments.

## What This Does

Syncs your file-based meal planner (.cook recipes, .txt meal plans) to Notion databases:
- **Recipes** → Notion Recipes database (with ingredients, instructions, metadata)
- **Meal Plans** → Notion Meal Plans + Meal Entries databases (calendar view)
- Maintains file ↔ page mappings for incremental updates
- Tracks sync state to avoid unnecessary re-syncing

## Usage Examples

- `/sync-to-notion` - Full sync (all recipes + meal plans)
- `/sync-to-notion recipes` - Sync only recipes
- `/sync-to-notion meal-plans` - Sync only meal plans ✅ NOW WORKING!

## How It Works

**For Recipes**:
1. **Parse Files**: Uses CookCLI to parse .cook files
2. **Check Existing**: Queries Notion for existing recipe pages by File Path
3. **Auto-Find Images** ✅ NEW: Automatically searches for recipe images
   - Matches keywords from recipe names (pasta, chicken, tacos, etc.)
   - Uses curated high-quality Unsplash food photography
   - 3-tier fallback system (curated → generic → safe default)
   - Always provides an image (100% coverage)
   - Preserves manually uploaded images
4. **Create/Update**: Creates new pages or updates existing ones
5. **Track State**: Saves sync timestamps to `.notion/sync-state.json`

**For Meal Plans** (NEW):
1. **Parse Meal Plan**: Reads pipe-delimited .txt file
2. **Extract Week Date**: From filename (week-YYYY-MM-DD.txt) or comments
3. **Create Meal Plan**: Creates/updates Meal Plan page with week info
4. **Create Meal Entries**: For each meal, creates Meal Entry with relations to:
   - Meal Plan page (parent plan)
   - Recipe page (which recipe to make)
5. **Link Recipes**: Looks up recipe pages by file path
6. **Archive Old Entries**: Replaces old meal entries on re-sync
7. **Check Shopping List**: Sets checkbox if shopping list exists

## Sync Behavior

- **First Sync**: Creates all pages in Notion
- **Subsequent Syncs**: Updates only changed pages
- **File Path**: Used as unique identifier to link files ↔ pages
- **Enrichments**: Tags, ratings, images added in Notion are preserved

## Output

Shows sync statistics:
```
📊 Sync Summary
Recipes: 12 synced, 0 failed
Meal Plans: 2 synced, 0 failed

🔗 View in Notion: [database URL]
```

## Notion Databases

Your meal planner uses three databases:
1. **Recipes**: Gallery view with images, tags, ratings, last cooked date
2. **Meal Plans**: Calendar view by week
3. **Meal Entries**: Individual meals linked to recipes and meal plans

## When to Use

- After importing new recipes
- After creating a meal plan
- When you want to browse recipes visually in Notion
- To share recipes with others via Notion

## Manual Sync

You can also sync manually:
```bash
./scripts/sync-to-notion.sh recipes
./scripts/sync-to-notion.sh meal-plans
./scripts/sync-to-notion.sh all
```

## Configuration

- Database IDs: `.notion/config.json`
- Sync state: `.notion/sync-state.json`
- Both files are gitignored for security

## Workflow Integration

This skill is automatically triggered by:
- Editing/writing .cook files (auto-sync hook)
- Using `/add-recipe-from-url` skill
- Using `/plan-and-shop` skill (coming soon)

---

**Note**: Files remain the source of truth. Notion is an enhancement layer for browsing and enrichment.
