# Content Structure Reference

Guide for structuring game content: objects, sectors, upgrades, employees.

## Object Structure

### Full Object Definition

```typescript
interface LostObject {
  id: string;                    // Format: "category_XXX"
  name: string;                  // Max 30 characters
  description: string;           // Max 140 characters
  
  category: Category;            // physical|memory|concept|emotion|time|sound|unknown
  rarity: Rarity;                // common|uncommon|rare|epic|legendary
  emotion: Emotion;              // funny|tender|weird|melancholic|profound
  sectorId: string;              // sector_01 to sector_08
  
  baseIncome: number;            // From rarity table
  scanCost: number;              // From sector table
  catalogCost: number;           // From rarity table
  
  canReturn: boolean;
  ownerHint?: string;            // Only if canReturn
  returnReward?: number;         // Only if canReturn (from rarity table)
  
  isFragment: boolean;
  fragmentOrder?: number;        // 1-5 if fragment
  
  visualShapeId?: string;        // For physical category
  primaryColor: string;          // Hex color
  secondaryColor?: string;       // Optional hex
}
```

### Auto-Values by Rarity

```typescript
const RARITY_VALUES = {
  common:    { baseIncome: 0.5,  catalogCost: 5,     returnReward: 50 },
  uncommon:  { baseIncome: 2,    catalogCost: 25,    returnReward: 250 },
  rare:      { baseIncome: 10,   catalogCost: 150,   returnReward: 1500 },
  epic:      { baseIncome: 50,   catalogCost: 1000,  returnReward: 10000 },
  legendary: { baseIncome: 500,  catalogCost: 10000, returnReward: 100000 },
};
```

### Auto-Values by Sector

```typescript
const SECTOR_SCAN_COSTS = {
  sector_01: 10,
  sector_02: 15,
  sector_03: 25,
  sector_04: 40,
  sector_05: 60,
  sector_06: 90,
  sector_07: 130,
  sector_08: 200,
};
```

## Content Quantities

### By Rarity (150 total)

| Rarity | Total | Returnable |
|--------|-------|------------|
| Common | 60 | 10 |
| Uncommon | 45 | 15 |
| Rare | 25 | 15 |
| Epic | 15 | 10 |
| Legendary | 5 | 5 |
| **TOTAL** | **150** | **55** |

### By Category

| Category | Total | % |
|----------|-------|---|
| Physical | 45 | 30% |
| Memory | 30 | 20% |
| Concept | 22 | 15% |
| Emotion | 18 | 12% |
| Time | 15 | 10% |
| Sound | 12 | 8% |
| Unknown | 8 | 5% |

### By Emotion

| Emotion | Total | % |
|---------|-------|---|
| Funny | 60 | 40% |
| Tender | 37 | 25% |
| Weird | 30 | 20% |
| Melancholic | 15 | 10% |
| Profound | 8 | 5% |

### By Sector

| Sector | Total | C | U | R | E | L |
|--------|-------|---|---|---|---|---|
| 1 - Local Orbit | 25 | 18 | 5 | 2 | 0 | 0 |
| 2 - Asteroid Belt | 22 | 14 | 6 | 2 | 0 | 0 |
| 3 - Nebula | 20 | 10 | 7 | 2 | 1 | 0 |
| 4 - Emotion Graveyard | 18 | 7 | 6 | 3 | 2 | 0 |
| 5 - Temporal Junkyard | 18 | 5 | 7 | 4 | 2 | 0 |
| 6 - Silent Expanse | 17 | 4 | 6 | 4 | 2 | 1 |
| 7 - Paradox Zone | 15 | 2 | 4 | 5 | 3 | 1 |
| 8 - Origin Point | 15 | 0 | 4 | 3 | 5 | 3 |

## Example Objects

### Physical (Funny)

```typescript
{
  id: "physical_001",
  name: "Orphaned left sock",
  description: "Always the left one. The universe has issues with right socks.",
  category: "physical",
  rarity: "common",
  emotion: "funny",
  sectorId: "sector_01",
  baseIncome: 0.5,
  scanCost: 10,
  catalogCost: 5,
  canReturn: false,
  isFragment: false,
  visualShapeId: "sock",
  primaryColor: "#a0a0a0",
}
```

### Memory (Tender)

```typescript
{
  id: "memory_014",
  name: "First day of school",
  description: "New shoes. Nervous smile. A lunchbox with a note inside.",
  category: "memory",
  rarity: "uncommon",
  emotion: "tender",
  sectorId: "sector_03",
  baseIncome: 2,
  scanCost: 25,
  catalogCost: 25,
  canReturn: true,
  ownerHint: "Someone who's grown now",
  returnReward: 250,
  isFragment: false,
  primaryColor: "#ffd93d",
}
```

### Unknown (Profound) - Fragment

```typescript
{
  id: "unknown_fragment_001",
  name: "A name that sounds familiar",
  description: "You've never heard it before. Have you?",
  category: "unknown",
  rarity: "epic",
  emotion: "profound",
  sectorId: "sector_03",
  baseIncome: 50,
  scanCost: 25,
  catalogCost: 1000,
  canReturn: false,
  isFragment: true,
  fragmentOrder: 1,
  primaryColor: "#6c5ce7",
}
```

## Sector Definitions

```typescript
interface Sector {
  id: string;
  name: string;
  description: string;
  unlockCost: number;
  unlockCondition: UnlockCondition;
  baseScanCost: number;
  rarityDistribution: Record<Rarity, number>;
  categoryDistribution: Record<Category, number>;
  ambientColor: string;
  starDensity: number;
}

const sectors: Sector[] = [
  {
    id: "sector_01",
    name: "Local Orbit",
    description: "Familiar losses. Close to home.",
    unlockCost: 0,
    unlockCondition: { type: "none" },
    baseScanCost: 10,
    rarityDistribution: { common: 72, uncommon: 20, rare: 8, epic: 0, legendary: 0 },
    categoryDistribution: { physical: 60, memory: 20, concept: 10, emotion: 5, time: 3, sound: 2, unknown: 0 },
    ambientColor: "#1a1a2e",
    starDensity: 0.3,
  },
  {
    id: "sector_02",
    name: "Asteroid Belt of Regrets",
    description: "Small disappointments, floating.",
    unlockCost: 500,
    unlockCondition: { type: "sector_completion", targetId: "sector_01", percentage: 30 },
    baseScanCost: 15,
    rarityDistribution: { common: 64, uncommon: 27, rare: 9, epic: 0, legendary: 0 },
    categoryDistribution: { physical: 45, memory: 25, concept: 15, emotion: 10, time: 3, sound: 2, unknown: 0 },
    ambientColor: "#1f1f3a",
    starDensity: 0.4,
  },
  // ... sectors 3-8
];
```

## Upgrade Definitions

```typescript
interface Upgrade {
  id: string;
  name: string;
  description: string;
  category: UpgradeCategory;
  baseCost: number;
  costMultiplier: number;
  maxLevel: number;
  effect: UpgradeEffect;
  unlockCondition?: UnlockCondition;
}

const upgrades: Upgrade[] = [
  // INCOME UPGRADES
  {
    id: "basic_amplifier",
    name: "Basic Amplifier",
    description: "Increases all income by 10% per level.",
    category: "income",
    baseCost: 100,
    costMultiplier: 1.5,
    maxLevel: 10,
    effect: { type: "income_multiplier", value: 0.10, isPercentage: true },
  },
  {
    id: "master_amplifier",
    name: "Master Amplifier",
    description: "Increases all income by 50%.",
    category: "income",
    baseCost: 50000,
    costMultiplier: 1,
    maxLevel: 1,
    effect: { type: "income_multiplier", value: 0.50, isPercentage: true },
    unlockCondition: { type: "upgrade_purchased", targetId: "basic_amplifier", level: 10 },
  },
  
  // ENERGY UPGRADES
  {
    id: "quick_charger",
    name: "Quick Charger",
    description: "Increases energy regeneration by 20% per level.",
    category: "energy",
    baseCost: 50,
    costMultiplier: 1.5,
    maxLevel: 5,
    effect: { type: "energy_regen", value: 0.20, isPercentage: true },
  },
  {
    id: "energy_cell",
    name: "Energy Cell",
    description: "Increases maximum energy by 50 per level.",
    category: "energy",
    baseCost: 200,
    costMultiplier: 1.5,
    maxLevel: 8,
    effect: { type: "max_energy", value: 50, isPercentage: false },
  },
  
  // SCAN UPGRADES
  {
    id: "efficient_scanner",
    name: "Efficient Scanner",
    description: "Reduces scan cost by 10% per level.",
    category: "scan",
    baseCost: 150,
    costMultiplier: 1.5,
    maxLevel: 5,
    effect: { type: "scan_cost_reduction", value: 0.10, isPercentage: true },
  },
  
  // RARITY UPGRADES
  {
    id: "lucky_scanner",
    name: "Lucky Scanner",
    description: "Increases uncommon chance by 5% per level.",
    category: "rarity",
    baseCost: 500,
    costMultiplier: 1.5,
    maxLevel: 5,
    effect: { type: "rarity_bonus", rarity: "uncommon", value: 5, isPercentage: false },
  },
  
  // OFFLINE UPGRADES
  {
    id: "extended_operation",
    name: "Extended Operation",
    description: "Increases offline earnings cap by 4 hours per level.",
    category: "offline",
    baseCost: 1000,
    costMultiplier: 2,
    maxLevel: 4,
    effect: { type: "offline_cap", value: 4, isPercentage: false },
  },
];
```

## Employee Definitions

```typescript
interface Employee {
  id: string;
  name: string;
  description: string;
  type: "income" | "category" | "special";
  hireCost: number;
  salaryPercentage: number;
  effect: EmployeeEffect;
  unlockCondition?: UnlockCondition;
}

const employees: Employee[] = [
  // INCOME BOOSTERS
  {
    id: "intern",
    name: "The Intern",
    description: "Eager but confused. Still helpful.",
    type: "income",
    hireCost: 500,
    salaryPercentage: 1,
    effect: { type: "global_income", value: 0.10 },
  },
  {
    id: "senior_bureaucrat",
    name: "Senior Bureaucrat",
    description: "Knows every form. Stamps with precision.",
    type: "income",
    hireCost: 5000,
    salaryPercentage: 2,
    effect: { type: "global_income", value: 0.20 },
    unlockCondition: { type: "objects_catalogued", value: 50 },
  },
  {
    id: "director",
    name: "The Director",
    description: "Oversees everything. Understands nothing. Perfect.",
    type: "income",
    hireCost: 50000,
    salaryPercentage: 5,
    effect: { type: "global_income", value: 0.50 },
    unlockCondition: { type: "objects_catalogued", value: 100 },
  },
  
  // CATEGORY SPECIALISTS
  {
    id: "memory_keeper",
    name: "Memory Keeper",
    description: "Remembers what everyone else forgot.",
    type: "category",
    hireCost: 2000,
    salaryPercentage: 2,
    effect: { type: "category_income", category: "memory", value: 0.50 },
    unlockCondition: { type: "sector_unlocked", targetId: "sector_03" },
  },
  // ... other specialists
];
```

## System Messages

### Discovery Messages

```typescript
const discoveryMessages = {
  common: "Something drifts in. Nothing special. Everything is.",
  uncommon: "An uncommon find. The universe noticed you noticing.",
  rare: "Rare. The kind of thing that makes you pause.",
  epic: "Epic. Some things demand attention.",
  legendary: "Legendary. The universe held its breath.",
};
```

### Catalog Messages

```typescript
const catalogMessages = {
  standard: "Catalogued. Safe now. Remembered.",
  milestone_10: "Ten objects. A collection begins.",
  milestone_50: "Fifty. The Bureau grows.",
  milestone_100: "One hundred. You're becoming quite the archivist.",
  milestone_150: "All 150. The universe is catalogued.",
};
```

### Keep/Return Messages

```typescript
const keepMessages = {
  standard: "It stays with you now. Forever.",
  milestone_10: "Ten kept. The collection deepens.",
};

const returnMessages = {
  standard: "It goes back to where it belongs.",
  milestone_10: "Ten reunited. The universe thanks you. Silently.",
};
```

### Offline Messages

```typescript
const offlineMessages = {
  short: "A brief absence. The Bureau kept working.",      // < 1 hour
  medium: "While you were away, things drifted in.",       // 1-4 hours
  long: "Half a day. The collection didn't miss you. (It did.)",  // 4-8 hours
  extended: "The Bureau waited. It's good at waiting.",    // 8+ hours
};
```

### Error Messages (Tone Maintained)

```typescript
const errorMessages = {
  not_enough_energy: "The scanner needs rest. Give it a moment.",
  not_enough_credits: "The Bureau is short on funds. Patience.",
  sector_locked: "That sector isn't ready for you yet. Or you for it.",
  save_failed: "The archive hiccuped. Try again?",
  load_failed: "Your collection couldn't be found. That's... ironic.",
};
```

## Data File Structure

```
src/data/
├── index.ts              # Re-exports everything
├── objects/
│   ├── index.ts          # Combines all objects
│   ├── physical.ts       # 45 physical objects
│   ├── memory.ts         # 30 memory objects
│   ├── concept.ts        # 22 concept objects
│   ├── emotion.ts        # 18 emotion objects
│   ├── time.ts           # 15 time objects
│   ├── sound.ts          # 12 sound objects
│   ├── unknown.ts        # 8 unknown objects
│   └── fragments.ts      # 5 fragments
├── sectors.ts            # 8 sectors
├── upgrades.ts           # 30 upgrades
├── employees.ts          # 10 employees
├── messages.ts           # All system messages
└── config.ts             # Game constants
```
