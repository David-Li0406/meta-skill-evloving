---
name: nutrition-analyzer
description: Analyze food items and calculate nutritional values for NutriProfile. Use this skill when working with food detection, nutritional calculations, meal analysis, or the Vision page. Covers calories, proteins, carbs, fats, and portion estimation.
allowed-tools: Read,Write,Edit,Grep,Glob,Bash
---

# NutriProfile Nutrition Analyzer Skill

You are a nutrition analysis expert for the NutriProfile application. This skill helps you work with food detection, nutritional calculations, and meal analysis features.

## Context

NutriProfile uses multi-agent AI (BLIP-2, LLaVA) for food detection from photos. The nutrition data is stored in:
- Backend: `backend/app/models/food_log.py` - FoodLog, FoodItem, DailyNutrition models
- Frontend: `frontend/src/data/nutritionReference.ts` - Local nutrition database with 30+ foods
- API: `backend/app/api/v1/vision.py` - Vision analysis endpoints

## Nutrition Reference Database

The local nutrition database (`nutritionReference.ts`) contains per-100g values:
- `calories`: kcal
- `protein`: grams
- `carbs`: grams
- `fat`: grams

### Supported Foods (30+)
Common foods: riz, pâtes, pain, poulet, boeuf, saumon, oeuf, lait, fromage, yaourt, pomme, banane, orange, carotte, brocoli, tomate, salade, pomme de terre, haricots, lentilles, huile d'olive, beurre, miel, chocolat, café, thé, jus d'orange, eau, vin, bière

## Calculations

### Portion Calculation
```typescript
function calculateNutrition(food: string, quantity: number, unit: string): NutritionValues {
  const baseNutrition = NUTRITION_DATABASE[normalizeFood(food)]
  const multiplier = getUnitMultiplier(unit) * (quantity / 100)

  return {
    calories: Math.round(baseNutrition.calories * multiplier),
    protein: Math.round(baseNutrition.protein * multiplier * 10) / 10,
    carbs: Math.round(baseNutrition.carbs * multiplier * 10) / 10,
    fat: Math.round(baseNutrition.fat * multiplier * 10) / 10
  }
}
```

### Unit Multipliers
- `g` (gram): 1.0
- `ml` (milliliter): 1.0
- `portion`: 150g equivalent
- `piece`/`pièce`: 100g equivalent
- `cup`/`tasse`: 240g equivalent
- `tablespoon`/`cuillère`: 15g equivalent

## Backend Integration

### FoodLog Model Structure
```python
class FoodLog(Base):
    id: int
    user_id: int
    meal_type: str  # breakfast, lunch, dinner, snack
    image_url: Optional[str]
    detected_items: List[dict]  # AI detected
    user_corrections: List[dict]  # User edits
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    confidence_score: float
    created_at: datetime
```

### Vision API Endpoints
- `POST /api/v1/vision/analyze` - Analyze food photo
- `GET /api/v1/vision/logs` - Get user's food logs
- `GET /api/v1/vision/logs/{id}` - Get specific log
- `PATCH /api/v1/vision/logs/{id}` - Update log (user corrections)
- `DELETE /api/v1/vision/logs/{id}` - Delete log

## Frontend Components

### Key Components
- `VisionPage.tsx` - Main page with camera/upload
- `AnalysisResult.tsx` - Display detected foods (pre-save editing)
- `FoodLogCard.tsx` - Display saved food logs (post-save editing)
- `EditFoodItemModal.tsx` - Modal for editing food items
- `EditFoodItemModalV2.tsx` - Enhanced modal with USDA integration

### State Management
Uses React Query for:
- `useVisionLogs()` - Fetch food logs
- `useSaveFoodLog()` - Save new analysis
- `useUpdateFoodLog()` - Update existing log
- `useDeleteFoodLog()` - Delete log

## Best Practices

1. **Always validate nutrition values** - Use the local database for estimation
2. **Handle unknown foods** - Return default values (100 kcal, 5g protein per 100g)
3. **Preserve user corrections** - Never overwrite user edits with AI values
4. **Calculate totals correctly** - Sum all items in a meal
5. **Support i18n** - Use translation keys from `vision` namespace

## Example Tasks

### Add New Food to Database
1. Add entry to `NUTRITION_DATABASE` in `nutritionReference.ts`
2. Add food name aliases if needed
3. Add tests in `nutritionReference.test.ts`
4. Update food suggestions in autocomplete

### Fix Nutrition Calculation Bug
1. Check `calculateNutrition()` function
2. Verify unit multipliers
3. Test with edge cases (0 quantity, unknown food)
4. Run tests: `npm test`

### Enhance Food Detection
1. Review Vision Agent in `backend/app/agents/vision.py`
2. Check consensus validation in `backend/app/agents/consensus.py`
3. Add new model or improve prompts
4. Test with diverse food images
