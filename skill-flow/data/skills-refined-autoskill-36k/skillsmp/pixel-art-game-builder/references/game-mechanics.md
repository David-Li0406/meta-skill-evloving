# Game Mechanics Reference

Complete guide for idle game mechanics, economy, and progression systems.

## Core Loop

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│    ┌─────────┐     ┌─────────┐     ┌──────────┐            │
│    │  SCAN   │────►│ DISCOVER│────►│ CATALOG  │            │
│    └─────────┘     └─────────┘     └──────────┘            │
│         │                               │                   │
│         │                               ▼                   │
│         │                        ┌──────────┐              │
│         │                        │  INCOME  │              │
│         │                        └──────────┘              │
│         │                               │                   │
│         │         ┌─────────────────────┘                   │
│         │         ▼                                         │
│         │   ┌──────────┐     ┌──────────┐                  │
│         └───│ UPGRADE  │◄────│  EXPAND  │                  │
│             └──────────┘     └──────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Resources

### Credits (💰)

| Property | Value |
|----------|-------|
| Initial | 0 |
| Cap | None (unlimited) |
| Format | Abbreviated (1.5K, 2.3M) |
| Sources | Passive income, Return rewards |
| Uses | Catalog, Upgrades, Sectors, Employees |

### Energy (⚡)

| Property | Value |
|----------|-------|
| Initial | 100 |
| Base cap | 100 |
| Max cap (upgraded) | 500 |
| Base regen | 1 per 10 seconds |
| Max regen | 1 per 5 seconds |
| Uses | Scanning |

## Income Calculation

```typescript
// Total income per second
function calculateTotalIncome(state: GameState): number {
  const baseIncome = state.cataloguedObjectIds.reduce((total, id) => {
    const obj = getObjectById(id);
    return total + calculateObjectIncome(state, obj);
  }, 0);
  
  return baseIncome * getCollectionMilestoneMultiplier(state);
}

// Single object income
function calculateObjectIncome(state: GameState, obj: LostObject): number {
  let income = obj.baseIncome;
  
  // Upgrade multipliers (multiplicative)
  income *= getUpgradeIncomeMultiplier(state);
  
  // Employee bonuses (multiplicative)
  income *= getEmployeeCategoryBonus(state, obj.category);
  
  // Sector mastery (multiplicative)
  income *= getSectorMasteryBonus(state, obj.sectorId);
  
  return income;
}

// Collection milestone multiplier
function getCollectionMilestoneMultiplier(state: GameState): number {
  const count = state.cataloguedObjectIds.length;
  
  if (count >= 150) return 2.00;
  if (count >= 125) return 1.75;
  if (count >= 100) return 1.50;
  if (count >= 75) return 1.25;
  if (count >= 50) return 1.10;
  if (count >= 25) return 1.05;
  return 1.00;
}
```

### Base Income by Rarity

| Rarity | Base Income (CR/sec) |
|--------|---------------------|
| Common | 0.5 |
| Uncommon | 2 |
| Rare | 10 |
| Epic | 50 |
| Legendary | 500 |

## Scanning Mechanics

### Object Selection Algorithm

```typescript
function selectObject(
  sectorId: string, 
  discoveredIds: string[], 
  rarityBonuses: Record<Rarity, number>
): LostObject | null {
  // 1. Get available objects in sector (not yet discovered)
  const available = allObjects.filter(obj => 
    obj.sectorId === sectorId && 
    !discoveredIds.includes(obj.id)
  );
  
  if (available.length === 0) return null;
  
  // 2. Get sector's base rarity distribution
  const sector = getSectorById(sectorId);
  const baseWeights = { ...sector.rarityDistribution };
  
  // 3. Apply rarity bonuses from upgrades
  for (const [rarity, bonus] of Object.entries(rarityBonuses)) {
    baseWeights[rarity] += bonus;
    baseWeights.common = Math.max(5, baseWeights.common - bonus);
  }
  
  // 4. Filter to available rarities only
  const availableRarities = new Set(available.map(o => o.rarity));
  const finalWeights: Record<string, number> = {};
  for (const [rarity, weight] of Object.entries(baseWeights)) {
    if (availableRarities.has(rarity)) {
      finalWeights[rarity] = weight;
    }
  }
  
  // 5. Select rarity, then random object of that rarity
  const selectedRarity = weightedRandom(
    Object.keys(finalWeights),
    Object.values(finalWeights)
  );
  
  const candidates = available.filter(o => o.rarity === selectedRarity);
  return candidates[Math.floor(Math.random() * candidates.length)];
}
```

### Scan Costs by Sector

| Sector | Base Scan Cost |
|--------|----------------|
| 1 - Local Orbit | 10 |
| 2 - Asteroid Belt | 15 |
| 3 - Nebula | 25 |
| 4 - Emotion Graveyard | 40 |
| 5 - Temporal Junkyard | 60 |
| 6 - Silent Expanse | 90 |
| 7 - Paradox Zone | 130 |
| 8 - Origin Point | 200 |

### Bulk Scanning

| Upgrade | Objects | Cost Multiplier |
|---------|---------|-----------------|
| Bulk Scanner | 2 | 1.5× |
| Triple Scan | 3 | 2.0× |

## Catalog Costs by Rarity

| Rarity | Catalog Cost |
|--------|--------------|
| Common | 5 CR |
| Uncommon | 25 CR |
| Rare | 150 CR |
| Epic | 1,000 CR |
| Legendary | 10,000 CR |

## Upgrade System

### Cost Formula

```typescript
function getUpgradeCost(upgrade: Upgrade, currentLevel: number): number {
  return Math.floor(upgrade.baseCost * Math.pow(1.5, currentLevel));
}

// Example: Base cost 100, Level 3
// Cost = 100 × 1.5² = 225
```

### Upgrade Categories

**Income Upgrades:**
- Basic Amplifier: +10% income per level (max 10)
- Master Amplifier: +50% income (max 1, requires Basic Amplifier 10)
- Time Dilation: ×2 income (max 1, requires Master Amplifier)

**Energy Upgrades:**
- Quick Charger: +20% energy regen per level (max 5)
- Energy Cell: +50 max energy per level (max 8)
- Instant Recharge: Energy fills instantly once per hour (max 1)

**Scan Upgrades:**
- Efficient Scanner: -10% scan cost per level (max 5)
- Bulk Scanner: Scan 2 objects (max 1)
- Triple Scan: Scan 3 objects (max 1, requires Bulk Scanner)

**Rarity Upgrades:**
- Lucky Scanner: +5% uncommon chance per level (max 5)
- Rare Detector: +3% rare chance per level (max 5)
- Epic Radar: +2% epic chance per level (max 3)
- Legendary Beacon: +1% legendary chance (max 1)

**Offline Upgrades:**
- Extended Operation: +4h offline cap per level (max 4, total 24h)
- Interest Protocol: +0.5% of credits per offline hour (max 1)

## Employee System

### Employee Slots

| Slot | Unlock Condition |
|------|------------------|
| 1 | 30 objects catalogued |
| 2 | 50 objects catalogued |
| 3 | 75 objects catalogued |
| 4 | Upgrade: Employee Quarters L1 |
| 5 | Upgrade: Employee Quarters L2 |
| 6 | Upgrade: Employee Quarters L3 |
| 7-8 | Upgrade: Bureau Expansion |

### Employee Types

**Income Boosters:**
- Intern: +10% all income
- Senior Bureaucrat: +20% all income
- Director: +50% all income

**Category Specialists:**
- Memory Keeper: +50% memory category income
- Concept Librarian: +50% concept category income
- Emotion Handler: +50% emotion category income
- Time Curator: +50% time category income
- Sound Archivist: +50% sound category income
- Physical Sorter: +50% physical category income
- Unknown Specialist: +100% unknown category income (×2)

### Employee Salary

```typescript
function calculateEmployeeSalary(employee: Employee, state: GameState): number {
  const baseIncome = calculateTotalIncome(state);
  return baseIncome * employee.salaryPercentage; // 1-5% typically
}
```

Employees work for free if credits reach 0, but show warning message.

## Progression Phases

| Phase | Objects | Unlocks |
|-------|---------|---------|
| 1 | 0-10 | Core loop, Sector 1 |
| 2 | 10-30 | Auto-scanner, basic upgrades |
| 3 | 30-50 | Sector 2-3, employees |
| 4 | 50-90 | Sector 4-5, advanced upgrades |
| 5 | 90-120 | Sector 6-7, Keep/Return choice |
| 6 | 120-150 | Sector 8, narrative revelations |
| 7 | 150+ | Endings available |

### Phase 5: Keep/Return System

At 90 objects catalogued, returnable objects show choice:

- **KEEP**: +1 Keeper score, object stays in collection
- **RETURN**: +1 Return score, object removed, return reward received

**Important:** Objects catalogued BEFORE Phase 5 are auto-kept (no choice).

## Narrative System

### The 3 Endings

| Ending | Name | Trigger | Theme |
|--------|------|---------|-------|
| A | The Eternal Keeper | Keep score ≥ 40/55 | Become universe's museum |
| B | The Return | Return score ≥ 40/55 | Reunite what was lost |
| C | The Lost One | Find 5 Fragments + Answer Call | Discover you're lost too |

### The 5 Fragments (Ending C)

| # | Fragment | Sector | Unlock Condition |
|---|----------|--------|------------------|
| 1 | A name that sounds familiar | 3 | 25 objects catalogued |
| 2 | A purpose you once had | 5 | First employee hired |
| 3 | A memory of creation | 6 | 5 objects returned |
| 4 | A doubt about existing | 7 | 5 objects kept |
| 5 | A call from somewhere | 8 | Fragments 1-4 found |

When all 5 fragments found: "Answer the Call" button appears.

## Offline Mechanics

### Offline Income

```typescript
function calculateOfflineEarnings(state: GameState, offlineSeconds: number): number {
  const maxOfflineSeconds = getOfflineCap(state) * 3600; // Convert hours to seconds
  const cappedSeconds = Math.min(offlineSeconds, maxOfflineSeconds);
  
  const income = calculateTotalIncome(state);
  let earnings = income * cappedSeconds;
  
  // Interest bonus (if upgrade purchased)
  if (state.purchasedUpgrades['interest_protocol']) {
    const hours = cappedSeconds / 3600;
    earnings += state.credits * 0.005 * hours;
  }
  
  return earnings;
}
```

### Offline Cap

| Upgrades | Cap |
|----------|-----|
| Base | 8 hours |
| Extended Operation L1 | 12 hours |
| Extended Operation L2 | 16 hours |
| Extended Operation L3 | 20 hours |
| Extended Operation L4 | 24 hours |

### Auto-Scan (NOT offline)

- Fixed 30-second interval
- Only works when app is open
- Requires energy > scan cost
- Can be toggled off

## Object States

```
┌─────────┐     ┌────────────┐     ┌───────────┐
│AVAILABLE│────►│ DISCOVERED │────►│ CATALOGUED│
└─────────┘     └────────────┘     └───────────┘
     │                                    │
     │                                    ▼ (if returnable & Phase 5+)
     │                             ┌───────────┐
     │                             │ RETURNED  │
     │                             └───────────┘
     │
     └──────────► (Object never discovered)
```

## Formulas Summary

```javascript
// Income
objectIncome = baseIncome × upgradeMultiplier × employeeBonus × sectorMastery
totalIncome = Σ(objectIncome) × collectionMilestone

// Costs
scanCost = sector.baseCost × (1 - scanCostReduction)
catalogCost = rarity.baseCost × (1 - catalogCostReduction)
upgradeCost = baseCost × 1.5^(currentLevel)

// Energy
energyRegen = min(baseRegen × quickChargerBonus, 0.2)  // Cap at 0.2/sec
maxEnergy = 100 + energyBonuses

// Offline
offlineEarnings = min(offlineTime, offlineCap) × totalIncome
interestBonus = currentCredits × 0.005 × offlineHours

// Rarity adjustment
adjustedWeight[rarity] = sectorWeight[rarity] + upgradeBonus[rarity]
adjustedWeight[common] = max(5, sectorWeight[common] - totalBonus)
```
