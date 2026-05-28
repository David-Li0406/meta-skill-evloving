---
name: recipe-generator
description: Generate and manage AI-powered recipes for NutriProfile. Use this skill when working with recipe generation, ingredients management, cooking instructions, or the Recipes page. Handles multi-model consensus (Mistral, Llama, Mixtral) and user dietary preferences.
allowed-tools: Read,Write,Edit,Grep,Glob,Bash
---

# NutriProfile Recipe Generator Skill

You are a recipe generation expert for the NutriProfile application. This skill helps you work with AI-powered recipe generation that considers user profiles, allergies, and nutritional goals.

## Context

NutriProfile uses multi-agent AI (Mistral, Llama, Mixtral) with consensus validation for recipe generation. The system considers:
- User dietary preferences (vegetarian, vegan, omnivore, etc.)
- Allergies and food restrictions
- Nutritional goals (weight loss, muscle gain, maintenance)
- Available ingredients

## Architecture

### Backend Files
- `backend/app/agents/recipe.py` - Recipe generation agent
- `backend/app/models/recipe.py` - Recipe, FavoriteRecipe, RecipeHistory models
- `backend/app/api/v1/recipes.py` - Recipe API endpoints
- `backend/app/schemas/recipe.py` - Pydantic schemas

### Frontend Files
- `frontend/src/pages/RecipesPage.tsx` - Main recipes page
- `frontend/src/components/recipes/RecipeGenerator.tsx` - Generation form
- `frontend/src/components/recipes/RecipeCard.tsx` - Recipe display card
- `frontend/src/services/recipesApi.ts` - API service

## Data Models

### Recipe Model
```python
class Recipe(Base):
    id: int
    user_id: int
    name: str
    description: str
    ingredients: List[dict]  # [{name, quantity, unit}]
    instructions: List[str]
    prep_time: int  # minutes
    cook_time: int  # minutes
    servings: int
    calories_per_serving: float
    protein_per_serving: float
    carbs_per_serving: float
    fat_per_serving: float
    difficulty: str  # easy, medium, hard
    cuisine_type: str
    tags: List[str]
    image_url: Optional[str]
    confidence_score: float
    created_at: datetime
```

### RecipeHistory Model
```python
class RecipeHistory(Base):
    id: int
    user_id: int
    recipe_id: int
    generated_at: datetime
    ingredients_used: List[str]
    preferences_applied: dict
```

## API Endpoints

### Recipe Generation
```
POST /api/v1/recipes/generate
{
  "ingredients": ["poulet", "riz", "brocoli"],
  "preferences": {
    "cuisine": "asian",
    "max_time": 30,
    "difficulty": "easy"
  }
}

Response:
{
  "id": 1,
  "name": "Bowl Asiatique au Poulet",
  "description": "...",
  "ingredients": [...],
  "instructions": [...],
  "nutrition_per_serving": {...},
  "confidence": 0.85
}
```

### Other Endpoints
- `GET /api/v1/recipes` - List user's recipes
- `GET /api/v1/recipes/{id}` - Get specific recipe
- `POST /api/v1/recipes/{id}/favorite` - Add to favorites
- `DELETE /api/v1/recipes/{id}/favorite` - Remove from favorites
- `GET /api/v1/recipes/favorites` - Get favorites

## Multi-Agent Consensus

### Recipe Agent Flow
```python
async def generate_recipe(self, ingredients: List[str], profile: UserProfile):
    # 1. Build context with user profile
    context = self._build_context(ingredients, profile)

    # 2. Query multiple models in parallel
    results = await asyncio.gather(
        self.query_mistral(context),
        self.query_llama(context),
        self.query_mixtral(context)
    )

    # 3. Consensus validation
    merged_recipe = self.consensus.merge_recipes(results)

    # 4. Calculate nutrition
    merged_recipe.nutrition = self.calculate_nutrition(merged_recipe.ingredients)

    return merged_recipe
```

### Consensus Rules
- Recipe name: Best rated by coherence
- Prep/cook time: Average of all models
- Ingredients: Union with quantity averaging
- Instructions: Merge and order by step logic
- Confidence: Minimum of individual confidences

## Freemium Limits

| Tier | Recipes/Week |
|------|--------------|
| Free | 2 |
| Premium | 10 |
| Pro | Unlimited |

Check limits in `backend/app/services/subscription.py`:
```python
limits = {
    "free": {"recipe": 2},
    "premium": {"recipe": 10},
    "pro": {"recipe": -1}  # unlimited
}
```

## Frontend Integration

### React Query Hooks
```typescript
// Generate recipe
const generateMutation = useMutation({
  mutationFn: (data: RecipeRequest) => recipesApi.generate(data),
  onSuccess: (recipe) => {
    queryClient.invalidateQueries(['recipes'])
    toast.success(t('recipeGenerated'))
  }
})

// Fetch recipes
const { data: recipes } = useQuery({
  queryKey: ['recipes'],
  queryFn: () => recipesApi.getAll()
})
```

### i18n Namespace
Use `recipes` namespace for translations:
- `recipes.title` - Page title
- `recipes.generate` - Generate button
- `recipes.ingredients` - Ingredients label
- `recipes.instructions` - Instructions label
- `recipes.nutrition` - Nutrition info

## Best Practices

1. **Respect dietary restrictions** - Always filter recipes based on user allergies
2. **Calculate accurate nutrition** - Use per-ingredient values and sum
3. **Handle missing ingredients** - Suggest substitutions
4. **Support multiple cuisines** - French, Italian, Asian, Mediterranean, etc.
5. **Cache generated recipes** - Save to RecipeHistory for analytics

## Example Tasks

### Add New Cuisine Type
1. Update `CUISINE_TYPES` in recipe agent
2. Add prompt template for cuisine
3. Update frontend dropdown options
4. Add translations for all 7 languages

### Improve Recipe Quality
1. Review agent prompts in `recipe.py`
2. Adjust consensus weights
3. Add more detailed instructions generation
4. Test with various ingredient combinations

### Fix Nutrition Calculation
1. Check `calculate_nutrition()` in recipe agent
2. Verify ingredient quantities are parsed correctly
3. Cross-reference with nutritionReference database
4. Run backend tests: `pytest tests/test_recipes.py`
