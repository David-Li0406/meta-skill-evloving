# Bench Configuration Reference

Complete reference for crafting bench configuration and fuel settings.

## Bench Configuration Overview

Each bench type has configuration that controls its behavior, available recipes, and processing characteristics.

## Crafting Bench Configuration

Standard crafting table configuration.

```json
{
  "BenchType": "Crafting",
  "BlockId": "hytale:crafting_table",
  "Config": {
    "GridSize": 3,
    "Categories": ["Tools", "Weapons", "Armor", "Building", "Misc"],
    "Tier": 1,
    "CraftingSpeedMultiplier": 1.0,
    "AllowFieldcraft": false
  }
}
```

### Crafting Config Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `GridSize` | int | 3 | Crafting grid size (2 or 3) |
| `Categories` | string[] | all | Allowed recipe categories |
| `Tier` | int | 1 | Bench tier for tiered recipes |
| `CraftingSpeedMultiplier` | float | 1.0 | Speed modifier |
| `AllowFieldcraft` | bool | false | Can craft fieldcraft recipes |

### Tiered Crafting Tables

```json
// Basic Crafting Table (Tier 1)
{
  "BlockId": "hytale:crafting_table",
  "Config": {
    "Tier": 1,
    "Categories": ["Tools", "Weapons", "Building"]
  }
}

// Advanced Workbench (Tier 2)
{
  "BlockId": "mymod:advanced_workbench",
  "Config": {
    "Tier": 2,
    "Categories": ["Tools", "Weapons", "Armor", "Building", "Magic"],
    "CraftingSpeedMultiplier": 1.5
  }
}

// Master Forge (Tier 3)
{
  "BlockId": "mymod:master_forge",
  "Config": {
    "Tier": 3,
    "Categories": ["Weapons", "Armor", "Magic", "Legendary"],
    "CraftingSpeedMultiplier": 2.0
  }
}
```

## Processing Bench Configuration

Furnace and smelting configuration.

```json
{
  "BenchType": "Processing",
  "BlockId": "hytale:furnace",
  "Config": {
    "ProcessingSpeedMultiplier": 1.0,
    "FuelEfficiency": 1.0,
    "AcceptedFuelTags": ["fuel", "burnable"],
    "AcceptedFuelItems": [],
    "MaxFuelStorage": 64,
    "KeepProgressOnClose": true,
    "AllowAutomation": true,
    "Slots": {
      "Input": 0,
      "Fuel": 1,
      "Output": 2
    }
  }
}
```

### Processing Config Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `ProcessingSpeedMultiplier` | float | 1.0 | Processing speed modifier |
| `FuelEfficiency` | float | 1.0 | Fuel consumption rate |
| `AcceptedFuelTags` | string[] | ["fuel"] | Item tags for valid fuel |
| `AcceptedFuelItems` | string[] | [] | Specific valid fuel items |
| `MaxFuelStorage` | int | 64 | Max fuel stack size |
| `KeepProgressOnClose` | bool | true | Maintain progress when closed |
| `AllowAutomation` | bool | true | Allow hopper/pipe interaction |

### Specialized Processing Benches

```json
// Blast Furnace - Faster, ores only
{
  "BlockId": "hytale:blast_furnace",
  "Config": {
    "ProcessingSpeedMultiplier": 2.0,
    "FuelEfficiency": 0.5,
    "AcceptedInputTags": ["ore", "raw_metal"],
    "AcceptedOutputTags": ["ingot", "metal"]
  }
}

// Smoker - Food only
{
  "BlockId": "hytale:smoker",
  "Config": {
    "ProcessingSpeedMultiplier": 2.0,
    "AcceptedInputTags": ["raw_food"],
    "AcceptedOutputTags": ["cooked_food"]
  }
}

// Kiln - Ceramics and glass
{
  "BlockId": "mymod:kiln",
  "Config": {
    "ProcessingSpeedMultiplier": 1.5,
    "AcceptedInputTags": ["clay", "sand"],
    "AcceptedOutputTags": ["ceramic", "glass"],
    "FuelEfficiency": 0.8
  }
}
```

## Fuel Configuration

Define fuel items and their burn times.

### Fuel Registry

```json
{
  "FuelRegistry": [
    {
      "ItemId": "hytale:coal",
      "BurnTime": 1600,
      "BurnTemperature": 1000
    },
    {
      "ItemId": "hytale:charcoal",
      "BurnTime": 1600,
      "BurnTemperature": 900
    },
    {
      "ItemTag": "logs",
      "BurnTime": 300,
      "BurnTemperature": 600
    },
    {
      "ItemTag": "planks",
      "BurnTime": 200,
      "BurnTemperature": 500
    },
    {
      "ItemId": "hytale:blaze_rod",
      "BurnTime": 2400,
      "BurnTemperature": 1500
    },
    {
      "ItemId": "hytale:lava_bucket",
      "BurnTime": 20000,
      "BurnTemperature": 2000,
      "ReturnItem": "hytale:bucket"
    }
  ]
}
```

### Fuel Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `ItemId` | string | Specific fuel item |
| `ItemTag` | string | Tag for fuel items |
| `BurnTime` | int | Ticks of burn time (20 ticks = 1 second) |
| `BurnTemperature` | int | Heat level (for temp-based recipes) |
| `ReturnItem` | string | Item returned after burning |

### Standard Fuel Values

| Item | Burn Time (ticks) | Items Smelted |
|------|-------------------|---------------|
| Stick | 100 | 0.5 |
| Wooden Tools | 200 | 1 |
| Planks | 200 | 1 |
| Logs | 300 | 1.5 |
| Coal | 1600 | 8 |
| Charcoal | 1600 | 8 |
| Blaze Rod | 2400 | 12 |
| Coal Block | 16000 | 80 |
| Lava Bucket | 20000 | 100 |

### Calculating Fuel Requirements

```
Items smelted = BurnTime / RecipeTime
RecipeTime (default) = 200 ticks (10 seconds)

Example:
Coal (1600 ticks) / 200 = 8 items per coal
```

## Diagram Crafting Configuration

Blueprint workbench configuration.

```json
{
  "BenchType": "DiagramCrafting",
  "BlockId": "hytale:diagram_table",
  "Config": {
    "MaxDiagramSlots": 9,
    "RequireDiagramItem": true,
    "DiagramCategories": ["Weapons", "Armor", "Magic"],
    "UnlockMethod": "knowledge",
    "ShowLockedRecipes": true,
    "PreviewEnabled": true
  }
}
```

### Diagram Config Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `MaxDiagramSlots` | int | 9 | Material input slots |
| `RequireDiagramItem` | bool | false | Need physical blueprint item |
| `DiagramCategories` | string[] | all | Available recipe categories |
| `UnlockMethod` | string | "knowledge" | How recipes are unlocked |
| `ShowLockedRecipes` | bool | true | Display unlearned recipes |
| `PreviewEnabled` | bool | true | Show output preview |

### Unlock Methods

| Method | Description |
|--------|-------------|
| `knowledge` | Player knowledge system |
| `item` | Requires blueprint item in slot |
| `achievement` | Unlocked by achievements |
| `level` | Player level requirement |
| `always` | Always available |

## Structural Crafting Configuration

Construction bench configuration.

```json
{
  "BenchType": "StructuralCrafting",
  "BlockId": "hytale:construction_bench",
  "Config": {
    "MaxMaterialTypes": 10,
    "PreviewRange": 50,
    "PlacementMode": "ghost",
    "RequireEmptySpace": true,
    "AllowRotation": true,
    "ConstructionPhases": true,
    "PhaseCompletionTime": 60
  }
}
```

### Structural Config Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `MaxMaterialTypes` | int | 10 | Different materials allowed |
| `PreviewRange` | int | 50 | Preview render distance |
| `PlacementMode` | string | "ghost" | Preview style |
| `RequireEmptySpace` | bool | true | Clear area before building |
| `AllowRotation` | bool | true | Can rotate structure |
| `ConstructionPhases` | bool | false | Multi-phase building |
| `PhaseCompletionTime` | int | 60 | Seconds per phase |

### Placement Modes

| Mode | Description |
|------|-------------|
| `ghost` | Transparent preview |
| `outline` | Wire frame preview |
| `hologram` | Glowing holographic preview |
| `none` | No preview |

## Fieldcraft Configuration

Pocket crafting configuration.

```json
{
  "BenchType": "Fieldcraft",
  "Config": {
    "GridSize": 2,
    "Categories": ["Basic", "Survival"],
    "AlwaysAvailable": true,
    "CraftingDelay": 0
  }
}
```

### Fieldcraft Restrictions

- Maximum 2x2 grid
- Limited recipe categories
- No complex recipes
- Always available without bench

## Registering Custom Benches

### Via JSON

```json
// assets/Server/Content/Benches/my_workbench.json
{
  "BlockId": "mymod:advanced_workbench",
  "BenchType": "Crafting",
  "Config": {
    "Tier": 2,
    "Categories": ["Tools", "Weapons", "Magic"],
    "CraftingSpeedMultiplier": 1.5
  },
  "Display": {
    "Title": "Advanced Workbench",
    "Icon": "textures/gui/workbench_icon.png"
  }
}
```

### Via Plugin Code

```java
public class MyPlugin extends JavaPlugin {
    
    @Override
    protected void setup() {
        BenchRegistry benchRegistry = getBenchRegistry();
        
        BenchConfig config = BenchConfig.builder()
            .blockId(BlockId.of("mymod:super_furnace"))
            .benchType(BenchType.Processing)
            .processingSpeed(3.0f)
            .fuelEfficiency(0.5f)
            .acceptedFuels(List.of(ItemTags.FUEL, ItemTags.MAGIC_FUEL))
            .build();
        
        benchRegistry.register(config);
    }
}
```

## Bench Block Entity

Link configuration to block entity.

```java
public class AdvancedWorkbenchBlockEntity extends BenchBlockEntity {
    
    private static final BenchConfig CONFIG = BenchConfig.builder()
        .benchType(BenchType.Crafting)
        .tier(2)
        .categories(List.of("Tools", "Weapons", "Magic"))
        .speedMultiplier(1.5f)
        .build();
    
    public AdvancedWorkbenchBlockEntity(BlockPos pos, BlockState state) {
        super(pos, state, CONFIG);
    }
    
    @Override
    public BenchConfig getBenchConfig() {
        return CONFIG;
    }
}
```

## Multi-Block Benches

Configuration for benches spanning multiple blocks.

```json
{
  "BlockId": "mymod:forge_controller",
  "BenchType": "Processing",
  "MultiBlock": {
    "Pattern": [
      ["B", "B", "B"],
      ["B", "C", "B"],
      ["B", "B", "B"]
    ],
    "Key": {
      "C": "mymod:forge_controller",
      "B": "hytale:brick"
    },
    "FormationBonus": {
      "ProcessingSpeed": 2.0,
      "FuelEfficiency": 1.5
    }
  },
  "Config": {
    "ProcessingSpeedMultiplier": 1.0,
    "FuelEfficiency": 1.0
  }
}
```

### Multi-Block Detection

```java
public class ForgeMultiBlock implements MultiBlockStructure {
    
    @Override
    public boolean isFormed(World world, BlockPos controllerPos) {
        // Check surrounding blocks match pattern
        for (int x = -1; x <= 1; x++) {
            for (int z = -1; z <= 1; z++) {
                BlockPos checkPos = controllerPos.offset(x, 0, z);
                if (!isValidBlock(world.getBlock(checkPos), x, z)) {
                    return false;
                }
            }
        }
        return true;
    }
    
    @Override
    public BenchConfig getFormedConfig() {
        return BenchConfig.builder()
            .benchType(BenchType.Processing)
            .processingSpeed(2.0f)
            .fuelEfficiency(1.5f)
            .build();
    }
}
```

## Bench Upgrades

Configurable upgrade system for benches.

```json
{
  "BlockId": "mymod:upgradeable_furnace",
  "BenchType": "Processing",
  "Upgrades": {
    "Slots": [
      { "Slot": 3, "AcceptedTags": ["furnace_upgrade"] }
    ],
    "UpgradeEffects": {
      "mymod:speed_upgrade": {
        "ProcessingSpeedMultiplier": 0.5,
        "Stackable": true,
        "MaxStacks": 4
      },
      "mymod:efficiency_upgrade": {
        "FuelEfficiency": 0.25,
        "Stackable": true,
        "MaxStacks": 4
      }
    }
  }
}
```

### Upgrade Application

```java
public class UpgradeableFurnace extends ProcessingBenchBlockEntity {
    
    @Override
    public float getProcessingSpeed() {
        float baseSpeed = super.getProcessingSpeed();
        int speedUpgrades = countUpgrade("mymod:speed_upgrade");
        return baseSpeed * (1 + (speedUpgrades * 0.5f));
    }
    
    @Override
    public float getFuelEfficiency() {
        float baseEfficiency = super.getFuelEfficiency();
        int efficiencyUpgrades = countUpgrade("mymod:efficiency_upgrade");
        return baseEfficiency * (1 + (efficiencyUpgrades * 0.25f));
    }
}
```
