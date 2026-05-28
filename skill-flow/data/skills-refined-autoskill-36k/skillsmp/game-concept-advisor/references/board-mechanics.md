# Board Game Mechanics

## Spatial Mechanics

### Hex Grid Mechanics

```
HEX ADVANTAGES
──────────────
• 6 neighbors (vs 4 for square)
• Uniform distance to all neighbors
• Natural for organic shapes
• No diagonal ambiguity
• Beautiful tessellation

HEX-SPECIFIC MECHANICS:

"Ripple Effects"
├─ Effect spreads to all 6 neighbors
├─ Then to their neighbors (weaker)
├─ Creates circular influence zones
└─ Distance = power falloff

"Line of Sight"
├─ Draw lines through hex centers
├─ Blocking hexes interrupt
├─ Simulins see in straight lines
└─ Strategic positioning matters

"Ring Control"
├─ Control center hex + all 6 neighbors
├─ Complete ring = control bonus
├─ Opponent can break rings
└─ Territorial mini-game

"Hex Rotation"
├─ Hexes can rotate (6 orientations)
├─ Different sides face neighbors
├─ Rotation affects connections/flow
└─ Puzzle-like optimization
```

### Area Control

```
AREA CONTROL PATTERNS
─────────────────────
• Majority scoring (most pieces wins area)
• Presence scoring (any piece = partial points)
• Connection scoring (linked areas multiply)
• Enclosure (surround to capture)

FARMING IN PURRIA APPLICATIONS:

"Field Sections"
├─ Hex grid divided into 5 sections
├─ Most thriving tulips in section = section bonus
├─ End of season: section majorities pay out
├─ Strategic: Focus resources or spread wide?

"Trouble Territory"
├─ Trouble claims hexes
├─ Adjacent trouble creates "blighted zone"
├─ Reclaim zones for comeback bonuses
├─ Territory war: tulips vs trouble
```

### Tile Placement

```
TILE PLACEMENT PATTERNS
───────────────────────
• Fitting (tiles must match edges)
• Open placement (anywhere legal)
• Adjacency bonuses (matching types boost each other)
• Negative adjacency (some tiles hurt each other)
• Building toward complete pictures

FARMING IN PURRIA APPLICATIONS:

"Farm Expansion"
├─ Start with 7 hexes
├─ Earn new hex tiles through play
├─ Choose where to attach new tiles
├─ Some tiles: Special terrain effects
└─ Placement: Strategic adjacency decisions

"Garden Design"
├─ Tulip tiles of different colors
├─ Matching colors adjacent: beauty bonus
├─ Pattern completion: achievement
└─ Express personal aesthetic
```

## Worker Placement

### Classic Worker Placement

```
CORE MECHANICS
──────────────
• Limited workers (actions per turn)
• Limited spaces (first come, first served)
• Blocking (taking space denies others)
• Retrieval (get workers back to use again)

VARIATIONS:
• Bumping (pay to displace opponent)
• Multi-worker spaces (stronger action with more workers)
• Shared spaces (weaker action, but available)
• Worker specialization (certain workers for certain spaces)

FARMING IN PURRIA APPLICATIONS:

"Simulin Deployment"
├─ 3 Simulins available
├─ Each day: assign to tasks
├─ Tasks: Tend hex, watch pot, scout weather, shop
├─ One Simulin per task (usually)
├─ Task blocked = missed opportunity
└─ Single-player but resource management tension

"Action Spaces"
├─ Morning: Scouting, Planning (limited slots)
├─ Action: Betting, Tending (limited per hex)
├─ Resolution: Bonus spaces for winners
└─ Night: Recovery spaces (all available)
```

### Action Selection

```
ACTION SELECTION PATTERNS
─────────────────────────
• Simultaneous selection (reveal together)
• Sequential selection (take turns)
• Auction selection (bid for action order)
• Rondel (circular track of actions)

FARMING IN PURRIA APPLICATIONS:

"Morning Planning Rondel"
├─ Circular track of 8 actions
├─ Move your token clockwise
├─ Can move 1-3 spaces
├─ Land on action = do it
├─ Skip powerful action = it charges up
└─ Rhythm of circling through actions

"Phase Action Grid"
├─ 4×4 grid of possible actions
├─ Take whole row OR whole column
├─ Different combinations = different strategies
└─ Drafting-meets-action-selection
```

## Engine Building

### Classic Engine Building

```
ENGINE BUILDING FUNDAMENTALS
────────────────────────────
• Early game: Build production
• Mid game: Production compounds
• Late game: Production pays off dramatically
• Satisfying acceleration curve

KEY CONCEPTS:
• Startup cost vs long-term yield
• Synergies between engine pieces
• Timing: When to stop building, start scoring
• Engine diversity vs specialization

FARMING IN PURRIA APPLICATIONS:

"Farm Infrastructure"
├─ Day 1: Just hexes
├─ Earn upgrades: Irrigation (+water), Sunlamps (+sun)
├─ Upgrades produce resources passively
├─ End of season: Infrastructure really paying off
└─ Next season: Keep some infrastructure

"Tulip Breeding Engine"
├─ Basic tulips: Low value
├─ Cross-breed: Create varieties
├─ Rare varieties: Breed for rarer
├─ Engine: Self-sustaining variety production
└─ Compound value of breeding investment
```

### Resource Conversion Chains

```
CONVERSION PATTERNS
───────────────────
• Linear: A → B → C → D
• Branching: A → B or C (choose)
• Combining: A + B → C
• Splitting: A → B + C
• Cycling: A → B → C → A (with yield)

FARMING IN PURRIA APPLICATIONS:

"Resource Ecosystem"
├─ Seeds → Planted Seeds (costs stamina)
├─ Planted Seeds + Water + Sun → Tulips (time)
├─ Tulips → Bulbs or Coins (choice)
├─ Bulbs → Better Seeds (breeding)
├─ Coins → Upgrades or Bets (choice)
└─ Interconnected conversion economy
```

## Push Your Luck

### Risk Escalation

```
PUSH YOUR LUCK PATTERNS
───────────────────────
• Accumulating rewards
• Increasing risk of bust
• Bank or continue decision
• Catch-up mechanisms for those behind

CLASSIC EXAMPLES:
• Blackjack (hit until bust)
• Can't Stop (roll until bust or bank)
• Incan Gold (press deeper or escape)

FARMING IN PURRIA APPLICATIONS:

"Growth Pushing"
├─ Base tulip value: 10
├─ Add growth: +5, total 15
├─ Add more growth: +5 OR trouble (50%)
├─ Add again: +5 OR trouble (70%)
├─ Player decides when to "bank" growth
└─ Trouble = lose all accumulated growth

"Harvest Timing"
├─ Tulip value grows each day
├─ But each day: chance of weather damage
├─ Harvest now for guaranteed value
├─ Wait for potentially higher value
└─ Classic push-your-luck with seasonal theme
```

### Press Your Luck Elements

```
PRESSING ELEMENTS
─────────────────
• Sequential reveals with escalating risk
• Known probability shifts
• All-or-nothing possibilities
• Soft failures (lose some, not all)

FARMING IN PURRIA APPLICATIONS:

"Pot Pushing"
├─ Pot at 40% filled
├─ Option: Push for more fill
├─ Success: +15% fill
├─ Failure: -10% fill
├─ Each push: Success rate decreases
└─ How many times to push?
```

## Deduction & Hidden Information

### Hidden Information Patterns

```
INFORMATION ASYMMETRY
─────────────────────
• Hidden identity (who is who)
• Hidden hands (what do others have)
• Hidden objectives (what are others trying to do)
• Hidden board state (fog of war)
• Hidden economy (others' resources)

FARMING IN PURRIA APPLICATIONS:

"Hidden Trouble"
├─ Some hexes have face-down trouble
├─ Could be minor or severe
├─ Scout to reveal (costs action)
├─ Or bet blind (risk vs efficiency)
└─ Tension of unknown threats

"Weather Forecasting"
├─ Tomorrow's weather: Hidden
├─ Pay to see forecast
├─ Forecast might be wrong (% accuracy)
├─ Strategic: When is forecasting worth it?
```

### Deduction Mechanics

```
DEDUCTION PATTERNS
──────────────────
• Process of elimination
• Clue gathering
• Information trading
• Logical inference

FARMING IN PURRIA APPLICATIONS:

"Pot State Deduction"
├─ Pot fill visible
├─ Contributing factors: partially hidden
├─ Observe which actions affect which pots
├─ Deduce relationships for better betting
└─ Learn the "tells" of the game

"Trouble Tracking"
├─ Trouble spawns semi-randomly
├─ Patterns emerge (certain conditions = certain trouble)
├─ Track and predict trouble spawns
└─ Deduction rewards attention
```

## Time & Phase Mechanics

### Time Pressure

```
TIME PRESSURE PATTERNS
──────────────────────
• Real-time (physical speed)
• Turn limit (X turns to finish)
• Resource clock (run out = game ends)
• Escalating threat (bad things get worse)

FARMING IN PURRIA APPLICATIONS:

"Season Countdown"
├─ 42 days per season
├─ Day counter always visible
├─ Season end: Evaluation and reset
├─ Urgency increases as season ends
└─ Not real-time, but persistent countdown

"Trouble Escalation"
├─ Untreated trouble: Spreads
├─ Each spread: Worse trouble
├─ Neglect too long: Catastrophic
└─ Time pressure to address problems
```

### Phase Structure

```
PHASE PATTERNS
──────────────
• Fixed phases (A → B → C → A)
• Player-triggered phases
• Event-triggered phases
• Nested phases (macro and micro)

FARMING IN PURRIA APPLICATIONS:

"The Four Phases" (Existing)
├─ Morning: Assessment, planning
├─ Action: Betting, management
├─ Resolution: Outcomes revealed
├─ Night: Growth, recovery
└─ Clean, predictable rhythm

"Phase Variants" (Ideas)
├─ Weather can add emergency phases
├─ Achievements unlock bonus phases
├─ Skip phases for efficiency (risk)
└─ Phase manipulation as strategy
```

## Social & Negotiation

### Trading Mechanics

```
TRADING PATTERNS
────────────────
• Resource trading (I'll give you X for Y)
• Service trading (I'll do X if you do Y)
• Information trading (I'll tell you if you tell me)
• Promise trading (I'll help you later)

FARMING IN PURRIA APPLICATIONS (MULTIPLAYER):

"Farmer's Market"
├─ Trade resources between players
├─ Negotiate prices
├─ Exclusive deals (only you can buy my gold tulips)
├─ Reputation system (trustworthy traders get deals)
└─ Social economy layer

"Tip Sharing"
├─ Share forecasts/tips with other players
├─ Build relationships
├─ Cooperative AND competitive
└─ Social without requiring it
```

### Cooperative Elements

```
COOPERATION PATTERNS
────────────────────
• Shared objectives (team win condition)
• Complementary roles (asymmetric abilities)
• Information sharing (can help each other)
• Shared resources (pool that all can use)

FARMING IN PURRIA APPLICATIONS:

"Seasonal Cooperative Goals"
├─ Everyone contributes to community goal
├─ "Grow 10,000 tulips this season" (all players combined)
├─ Community rewards if achieved
├─ Individual + collective success
└─ Friendly competition within cooperation
```
