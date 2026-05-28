# Code Quality Patterns

## Clean Code Principles

### 1. Naming Conventions

```typescript
// ❌ Bad
const d = 42;                    // What is d?
const data = fetchData();        // What kind of data?
function process(x: any) {}      // Process what?

// ✅ Good
const daysInSeason = 42;
const playerProfile = fetchPlayerProfile();
function calculateBetPayout(bet: Bet): number {}
```

**Naming Rules:**
- Variables: Nouns (`score`, `playerCoins`, `selectedHex`)
- Functions: Verbs (`calculateScore`, `updateResources`, `renderHex`)
- Booleans: Question form (`isActive`, `hasWon`, `canAfford`)
- Constants: SCREAMING_SNAKE (`MAX_BET_AMOUNT`, `DEFAULT_STAMINA`)

### 2. Function Design

```typescript
// ❌ Bad: Does too many things
function updateGame(player, bet, hex, time) {
  // 50 lines of mixed logic
  player.coins -= bet.amount;
  if (hex.hasTrouble) {
    // handle trouble
  }
  if (time.phase === 'resolution') {
    // resolve bets
  }
  // ... more mixed concerns
}

// ✅ Good: Single responsibility
function deductBetFromBalance(player: Player, amount: number): Player {
  return { ...player, coins: player.coins - amount };
}

function resolveTrouble(hex: Hex, severity: number): Hex {
  return { ...hex, trouble: null, damage: calculateDamage(severity) };
}

function processPhaseResolution(state: GameState): GameState {
  return pipe(
    resolveBets,
    applyTroubleEffects,
    updateScore
  )(state);
}
```

**Function Rules:**
- Max 20-30 lines (excluding comments)
- Max 3-4 parameters (use object if more)
- One level of abstraction
- Do one thing well

### 3. Avoiding Magic Numbers

```typescript
// ❌ Bad
if (player.coins >= 100) {
  player.stamina = 100;
  if (day > 42) {
    endSeason();
  }
}

// ✅ Good
const MIN_BET_AMOUNT = 100;
const MAX_STAMINA = 100;
const DAYS_PER_SEASON = 42;

if (player.coins >= MIN_BET_AMOUNT) {
  player.stamina = MAX_STAMINA;
  if (day > DAYS_PER_SEASON) {
    endSeason();
  }
}
```

### 4. Early Returns

```typescript
// ❌ Bad: Deep nesting
function processHex(hex: Hex) {
  if (hex) {
    if (hex.isActive) {
      if (!hex.hasTrouble) {
        if (hex.growthStage < MAX_GROWTH) {
          // finally do something
          return growTulip(hex);
        }
      }
    }
  }
  return hex;
}

// ✅ Good: Guard clauses
function processHex(hex: Hex | null): Hex | null {
  if (!hex) return null;
  if (!hex.isActive) return hex;
  if (hex.hasTrouble) return hex;
  if (hex.growthStage >= MAX_GROWTH) return hex;
  
  return growTulip(hex);
}
```

## React Patterns

### Component Organization

```typescript
// Recommended file structure for a component
// src/components/MetaPotPanel/
//   ├── MetaPotPanel.tsx       (main component)
//   ├── MetaPotPanel.test.tsx  (tests)
//   ├── MetaPotPanel.css       (styles if not using Tailwind)
//   ├── useBetting.ts          (custom hook)
//   └── index.ts               (export)

// MetaPotPanel.tsx
import { useBetting } from './useBetting';

export function MetaPotPanel({ pots }: MetaPotPanelProps) {
  const { placeBet, activeBets } = useBetting();
  
  return (
    <div className="meta-pot-panel">
      {pots.map(pot => (
        <PotCard 
          key={pot.id}
          pot={pot}
          onBet={placeBet}
          isActive={activeBets.has(pot.id)}
        />
      ))}
    </div>
  );
}
```

### Custom Hook Extraction

```typescript
// ❌ Bad: Logic mixed in component
function GameBoard() {
  const [selectedHex, setSelectedHex] = useState(null);
  const [hoveredHex, setHoveredHex] = useState(null);
  
  const handleHexClick = (hex) => {
    if (selectedHex?.id === hex.id) {
      setSelectedHex(null);
    } else {
      setSelectedHex(hex);
    }
  };
  
  const handleHexHover = (hex) => {
    setHoveredHex(hex);
  };
  
  // ... more logic
}

// ✅ Good: Logic extracted to hook
function useHexSelection() {
  const [selectedHex, setSelectedHex] = useState<Hex | null>(null);
  const [hoveredHex, setHoveredHex] = useState<Hex | null>(null);
  
  const selectHex = useCallback((hex: Hex) => {
    setSelectedHex(prev => prev?.id === hex.id ? null : hex);
  }, []);
  
  const hoverHex = useCallback((hex: Hex | null) => {
    setHoveredHex(hex);
  }, []);
  
  return { selectedHex, hoveredHex, selectHex, hoverHex };
}

function GameBoard() {
  const { selectedHex, hoveredHex, selectHex, hoverHex } = useHexSelection();
  // Component is now focused on rendering
}
```

### Prop Drilling Solutions

```typescript
// ❌ Bad: Props passed through many levels
<App>
  <GameContainer coins={coins}>
    <GameBoard coins={coins}>
      <HexGrid coins={coins}>
        <Hex coins={coins} />  {/* Finally used here */}
      </HexGrid>
    </GameBoard>
  </GameContainer>
</App>

// ✅ Good: Use Zustand (already in your stack)
// Access directly where needed
function Hex({ id }: { id: string }) {
  const coins = useGameStore(state => state.resources.coins);
  // ...
}

// ✅ Also Good: Context for truly global UI state
const GameUIContext = createContext<GameUIState>(null);

function Hex({ id }: { id: string }) {
  const { showTooltips } = useContext(GameUIContext);
  // ...
}
```

## TypeScript Patterns

### Strict Typing

```typescript
// ❌ Bad
function handleBet(pot: any, amount: any) {
  return { result: pot.value * amount };
}

// ✅ Good
interface Pot {
  id: string;
  type: 'water' | 'sun' | 'pest' | 'growth';
  fillLevel: number;
  multiplier: number;
}

interface BetResult {
  success: boolean;
  payout: number;
  newBalance: number;
}

function handleBet(pot: Pot, amount: number): BetResult {
  const payout = pot.fillLevel >= 50 ? amount * pot.multiplier : 0;
  return {
    success: payout > 0,
    payout,
    newBalance: currentBalance - amount + payout,
  };
}
```

### Discriminated Unions

```typescript
// Model game states that are mutually exclusive
type GamePhase = 
  | { type: 'morning'; troubleSpawned: boolean }
  | { type: 'action'; betsPlaced: Bet[] }
  | { type: 'resolution'; results: BetResult[] }
  | { type: 'night'; bonusApplied: boolean };

function renderPhaseUI(phase: GamePhase) {
  switch (phase.type) {
    case 'morning':
      return <MorningUI troubleSpawned={phase.troubleSpawned} />;
    case 'action':
      return <ActionUI bets={phase.betsPlaced} />;
    case 'resolution':
      return <ResolutionUI results={phase.results} />;
    case 'night':
      return <NightUI bonusApplied={phase.bonusApplied} />;
  }
}
```

### Utility Types

```typescript
// Make all properties optional for updates
type PlayerUpdate = Partial<Player>;

// Pick specific fields
type PlayerDisplay = Pick<Player, 'name' | 'avatar' | 'level'>;

// Omit sensitive fields
type PublicPlayer = Omit<Player, 'email' | 'password'>;

// Make specific fields required
type CreatePlayer = Required<Pick<Player, 'name' | 'email'>> & Partial<Player>;

// Record for maps
type HexMap = Record<string, Hex>;
```

## Refactoring Recipes

### Extract Method

```typescript
// Before
function processDay(state: GameState): GameState {
  // Spawn trouble
  const troubleHexes = findEmptyHexes(state.hexes);
  const newTroubles = troubleHexes
    .filter(() => Math.random() < 0.3)
    .map(hex => createTrouble(hex));
  
  // ... 30 more lines
}

// After
function spawnDailyTrouble(hexes: Map<string, Hex>): Trouble[] {
  const SPAWN_CHANCE = 0.3;
  return findEmptyHexes(hexes)
    .filter(() => Math.random() < SPAWN_CHANCE)
    .map(hex => createTrouble(hex));
}

function processDay(state: GameState): GameState {
  const newTroubles = spawnDailyTrouble(state.hexes);
  // ... cleaner
}
```

### Replace Conditional with Polymorphism

```typescript
// Before
function calculateReward(potType: string, fillLevel: number): number {
  if (potType === 'water') {
    return fillLevel >= 50 ? 100 : 0;
  } else if (potType === 'sun') {
    return fillLevel >= 40 ? 150 : 0;
  } else if (potType === 'pest') {
    return fillLevel >= 60 ? 200 : 0;
  }
  return 0;
}

// After
interface PotConfig {
  threshold: number;
  baseReward: number;
}

const POT_CONFIGS: Record<PotType, PotConfig> = {
  water: { threshold: 50, baseReward: 100 },
  sun: { threshold: 40, baseReward: 150 },
  pest: { threshold: 60, baseReward: 200 },
  growth: { threshold: 70, baseReward: 300 },
};

function calculateReward(potType: PotType, fillLevel: number): number {
  const config = POT_CONFIGS[potType];
  return fillLevel >= config.threshold ? config.baseReward : 0;
}
```

### Introduce Parameter Object

```typescript
// Before
function createHex(
  q: number,
  r: number,
  s: number,
  state: HexState,
  tulipType: TulipType | null,
  growthStage: number,
  hasTrouble: boolean,
  troubleType: TroubleType | null
): Hex { ... }

// After
interface CreateHexParams {
  coords: CubeCoord;
  state?: HexState;
  tulip?: {
    type: TulipType;
    growthStage: number;
  };
  trouble?: {
    type: TroubleType;
  };
}

function createHex(params: CreateHexParams): Hex {
  return {
    ...params.coords,
    state: params.state ?? 'empty',
    tulip: params.tulip ?? null,
    trouble: params.trouble ?? null,
  };
}
```

## Code Smells to Watch

| Smell | Symptom | Fix |
|-------|---------|-----|
| Long Method | >30 lines | Extract methods |
| Long Parameter List | >4 params | Use parameter object |
| Duplicated Code | Same logic twice | Extract function |
| Feature Envy | Uses other class data a lot | Move method |
| Data Clumps | Same fields always together | Extract class/type |
| Primitive Obsession | Using strings for types | Create enum/type |
| Switch Statements | Long switch blocks | Use polymorphism/map |
| Shotgun Surgery | One change = many files | Consolidate logic |
| Comments Explaining Code | // This adds 1 to x | Rename to be clear |
