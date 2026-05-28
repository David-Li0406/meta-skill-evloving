# Recipe Format Reference

Complete JSON schema reference for all Hytale crafting recipe types.

## Base Recipe Schema

All recipes share this base structure:

```json
{
  "$schema": "hytale://recipe",
  "Type": "CraftingRecipe",
  "Id": "namespace:recipe_id",
  "Input": [],
  "Output": [],
  "PrimaryOutput": "namespace:item_id",
  "BenchRequirement": [],
  "Category": "Category Name",
  "KnowledgeRequired": false,
  "KnowledgeId": "namespace:knowledge_id",
  "TimeSeconds": 0,
  "Priority": 0
}
```

## Field Definitions

### Id

Unique identifier for the recipe.

```json
"Id": "mymod:iron_sword_recipe"
```

**Constraints:**
- Must be unique across all recipes
- Format: `namespace:name`
- Lowercase, underscores allowed

### Input

Array of required materials.

```json
"Input": [
  { "ItemId": "hytale:iron_ingot", "Quantity": 2 },
  { "ItemTag": "planks", "Quantity": 4 },
  { "ResourceTypeId": "hytale:magic", "Quantity": 1 }
]
```

### MaterialQuantity Object

```json
{
  "ItemId": "namespace:item_id",      // Specific item (mutually exclusive)
  "ItemTag": "tag_name",              // Any item with tag (mutually exclusive)
  "ResourceTypeId": "namespace:type", // Resource type (mutually exclusive)
  "Quantity": 1,                      // Required amount (default: 1)
  "ConsumeOnCraft": true             // Whether consumed (default: true)
}
```

### Output

Array of resulting items.

```json
"Output": [
  { 
    "ItemId": "hytale:iron_sword", 
    "Quantity": 1 
  },
  { 
    "ItemId": "hytale:iron_nugget", 
    "Quantity": 2,
    "Chance": 0.5
  }
]
```

### OutputQuantity Object

```json
{
  "ItemId": "namespace:item_id",      // Output item
  "Quantity": 1,                      // Amount produced
  "Chance": 1.0,                      // Drop chance (0.0-1.0)
  "MinQuantity": 1,                   // Minimum if variable
  "MaxQuantity": 3,                   // Maximum if variable
  "NBT": {}                          // Custom NBT data
}
```

### PrimaryOutput

Main output for recipe book display and lookup.

```json
"PrimaryOutput": "hytale:iron_sword"
```

### BenchRequirement

Array of valid crafting stations.

```json
"BenchRequirement": [
  {
    "BenchType": "Crafting",
    "BlockId": "hytale:crafting_table",
    "MinTier": 1,
    "MaxTier": 3
  }
]
```

### BenchRequirement Object

```json
{
  "BenchType": "Crafting",            // Required bench type
  "BlockId": "namespace:block_id",    // Specific block (optional)
  "MinTier": 1,                       // Minimum bench tier (optional)
  "MaxTier": 10,                      // Maximum bench tier (optional)
  "Properties": {}                   // Additional requirements (optional)
}
```

### BenchType Values

| Value | Description |
|-------|-------------|
| `Crafting` | Standard crafting table |
| `Fieldcraft` | Pocket/inventory crafting |
| `Processing` | Furnace/smelting |
| `DiagramCrafting` | Blueprint workbench |
| `StructuralCrafting` | Construction bench |

### Category

Recipe category for UI organization.

```json
"Category": "Weapons"
```

**Standard Categories:**
- `Tools`
- `Weapons`
- `Armor`
- `Building`
- `Food`
- `Materials`
- `Magic`
- `Misc`

### Knowledge Fields

```json
"KnowledgeRequired": true,
"KnowledgeId": "mymod:advanced_smithing"
```

If `KnowledgeId` is omitted, uses recipe ID as knowledge ID.

### TimeSeconds

Processing time for Processing bench type.

```json
"TimeSeconds": 10
```

Only applicable when `BenchType` is `Processing`.

### Priority

Recipe selection priority when multiple match.

```json
"Priority": 100
```

Higher priority recipes are checked first.

## Shaped Recipe Format

Pattern-based recipe placement.

```json
{
  "Type": "ShapedRecipe",
  "Pattern": [
    "III",
    " S ",
    " S "
  ],
  "Key": {
    "I": { "ItemId": "hytale:iron_ingot" },
    "S": { "ItemId": "hytale:stick" }
  },
  "Output": [
    { "ItemId": "hytale:iron_pickaxe", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "Crafting" }
  ]
}
```

### Pattern

Array of strings representing the crafting grid.

```json
"Pattern": [
  "AAA",
  "ABA",
  "AAA"
]
```

**Rules:**
- Maximum 3 rows, 3 columns
- Space character = empty slot
- Each character maps to Key
- Pattern can be smaller than 3x3

### Key

Maps pattern characters to materials.

```json
"Key": {
  "A": { "ItemId": "hytale:iron_ingot" },
  "B": { "ItemTag": "gems" }
}
```

**Rules:**
- Single character keys
- Space cannot be used as key
- Supports ItemId, ItemTag, ResourceTypeId

### Pattern Variations

```json
// 2x2 pattern
"Pattern": [
  "AA",
  "AA"
]

// 1x3 pattern (vertical)
"Pattern": [
  "A",
  "A",
  "A"
]

// 3x1 pattern (horizontal)
"Pattern": [
  "AAA"
]

// L-shape
"Pattern": [
  "A  ",
  "A  ",
  "AA "
]
```

## Shapeless Recipe Format

Items can be placed in any arrangement.

```json
{
  "Type": "ShapelessRecipe",
  "Input": [
    { "ItemId": "hytale:red_dye", "Quantity": 1 },
    { "ItemId": "hytale:white_wool", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:red_wool", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "Crafting" }
  ]
}
```

## Processing Recipe Format

Time-based conversion recipes.

```json
{
  "Type": "ProcessingRecipe",
  "Input": [
    { "ItemId": "hytale:iron_ore", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:iron_ingot", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "Processing" }
  ],
  "TimeSeconds": 10,
  "FuelMultiplier": 1.0,
  "Experience": 10
}
```

### Processing-Specific Fields

```json
{
  "TimeSeconds": 10,              // Base processing time
  "FuelMultiplier": 1.0,          // Fuel consumption rate
  "Experience": 10,               // XP granted on completion
  "RequiresFuel": true,           // Whether fuel is needed
  "ContinuousProcessing": true   // Auto-process next item
}
```

## Diagram Recipe Format

Blueprint-based crafting.

```json
{
  "Type": "DiagramRecipe",
  "Input": [
    { "ItemId": "hytale:refined_steel", "Quantity": 10 },
    { "ItemId": "hytale:dragon_scale", "Quantity": 3 },
    { "ItemId": "hytale:magic_crystal", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:dragon_armor", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "DiagramCrafting" }
  ],
  "DiagramId": "hytale:dragon_armor_blueprint",
  "KnowledgeRequired": true,
  "DiagramDisplay": {
    "Icon": "textures/diagrams/dragon_armor.png",
    "Description": "Legendary armor forged from dragon scales"
  }
}
```

### Diagram-Specific Fields

```json
{
  "DiagramId": "namespace:diagram_id",
  "DiagramDisplay": {
    "Icon": "path/to/icon.png",
    "Description": "Recipe description",
    "Rarity": "Legendary"
  },
  "UnlockConditions": {
    "RequiredLevel": 50,
    "RequiredQuest": "namespace:dragon_slayer"
  }
}
```

## Structural Recipe Format

Multi-block construction.

```json
{
  "Type": "StructuralRecipe",
  "Input": [
    { "ItemId": "hytale:stone_brick", "Quantity": 50 },
    { "ItemId": "hytale:wooden_beam", "Quantity": 20 },
    { "ItemId": "hytale:iron_fitting", "Quantity": 8 }
  ],
  "Output": [
    { "StructureId": "hytale:watchtower" }
  ],
  "BenchRequirement": [
    { "BenchType": "StructuralCrafting" }
  ],
  "Structure": {
    "TemplateFile": "structures/watchtower.nbt",
    "PreviewFile": "structures/watchtower_preview.json",
    "PlacementRules": {
      "RequiresFlatGround": true,
      "MinClearance": 10,
      "AllowedBiomes": ["plains", "forest"]
    }
  }
}
```

### Structure-Specific Fields

```json
{
  "Structure": {
    "TemplateFile": "path/to/structure.nbt",
    "PreviewFile": "path/to/preview.json",
    "Size": { "X": 5, "Y": 10, "Z": 5 },
    "PlacementRules": {
      "RequiresFlatGround": true,
      "MinClearance": 10,
      "MaxSlope": 15,
      "AllowedBiomes": [],
      "ForbiddenBiomes": [],
      "RequiresFoundation": true
    },
    "ConstructionPhases": [
      { "Name": "Foundation", "Progress": 0.25 },
      { "Name": "Walls", "Progress": 0.5 },
      { "Name": "Roof", "Progress": 0.75 },
      { "Name": "Finishing", "Progress": 1.0 }
    ]
  }
}
```

## NBT Data in Outputs

Apply custom data to crafted items.

```json
"Output": [
  {
    "ItemId": "hytale:enchanted_sword",
    "Quantity": 1,
    "NBT": {
      "Enchantments": [
        { "Id": "sharpness", "Level": 3 }
      ],
      "CustomName": "Blade of Fire",
      "Lore": [
        "Forged in dragon flame"
      ],
      "CustomModelData": 1001
    }
  }
]
```

## Conditional Recipes

Recipes with conditions.

```json
{
  "Type": "ConditionalRecipe",
  "Conditions": [
    { "Type": "ModLoaded", "ModId": "expansion_pack" },
    { "Type": "ConfigEnabled", "Config": "advanced_recipes" }
  ],
  "Recipe": {
    "Input": [...],
    "Output": [...],
    "BenchRequirement": [...]
  }
}
```

### Condition Types

```json
// Mod loaded
{ "Type": "ModLoaded", "ModId": "namespace" }

// Config flag
{ "Type": "ConfigEnabled", "Config": "config_key" }

// Item exists
{ "Type": "ItemExists", "ItemId": "namespace:item" }

// Tag not empty
{ "Type": "TagNotEmpty", "Tag": "tag_name" }
```

## Recipe Groups

Group related recipes.

```json
{
  "Type": "RecipeGroup",
  "GroupId": "mymod:colored_wool",
  "Recipes": [
    {
      "Input": [
        { "ItemId": "hytale:white_wool" },
        { "ItemId": "hytale:red_dye" }
      ],
      "Output": [{ "ItemId": "hytale:red_wool" }]
    },
    {
      "Input": [
        { "ItemId": "hytale:white_wool" },
        { "ItemId": "hytale:blue_dye" }
      ],
      "Output": [{ "ItemId": "hytale:blue_wool" }]
    }
  ],
  "BenchRequirement": [
    { "BenchType": "Crafting" }
  ]
}
```

## Validation Rules

### Required Fields

| Recipe Type | Required Fields |
|-------------|-----------------|
| All | Input, Output, BenchRequirement |
| Shaped | Pattern, Key |
| Processing | TimeSeconds |
| Diagram | DiagramId |
| Structural | Structure |

### Quantity Limits

- Input quantity: 1-64 per slot
- Output quantity: 1-64 per item
- Pattern size: 1x1 to 3x3
- Processing time: 0.1-3600 seconds

### ID Format

```
namespace:recipe_name
├── namespace: lowercase, a-z, 0-9, underscores
└── recipe_name: lowercase, a-z, 0-9, underscores
```

## Example Complete Recipes

### Full Crafting Recipe

```json
{
  "$schema": "hytale://recipe",
  "Type": "ShapedRecipe",
  "Id": "mymod:diamond_pickaxe",
  "Pattern": [
    "DDD",
    " S ",
    " S "
  ],
  "Key": {
    "D": { "ItemId": "hytale:diamond" },
    "S": { "ItemId": "hytale:stick" }
  },
  "Output": [
    { 
      "ItemId": "mymod:diamond_pickaxe", 
      "Quantity": 1,
      "NBT": {
        "Durability": 1561
      }
    }
  ],
  "PrimaryOutput": "mymod:diamond_pickaxe",
  "BenchRequirement": [
    { "BenchType": "Crafting", "MinTier": 1 }
  ],
  "Category": "Tools",
  "KnowledgeRequired": false,
  "Priority": 0
}
```

### Full Processing Recipe

```json
{
  "$schema": "hytale://recipe",
  "Type": "ProcessingRecipe",
  "Id": "mymod:steel_smelting",
  "Input": [
    { "ItemId": "hytale:iron_ingot", "Quantity": 1 },
    { "ItemId": "hytale:coal", "Quantity": 2 }
  ],
  "Output": [
    { "ItemId": "mymod:steel_ingot", "Quantity": 1 },
    { "ItemId": "hytale:slag", "Quantity": 1, "Chance": 0.25 }
  ],
  "PrimaryOutput": "mymod:steel_ingot",
  "BenchRequirement": [
    { 
      "BenchType": "Processing", 
      "BlockId": "mymod:blast_furnace" 
    }
  ],
  "Category": "Materials",
  "TimeSeconds": 20,
  "FuelMultiplier": 1.5,
  "Experience": 15,
  "KnowledgeRequired": false
}
```
