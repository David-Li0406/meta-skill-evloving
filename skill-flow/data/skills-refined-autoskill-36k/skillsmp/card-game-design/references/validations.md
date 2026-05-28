# Card Game Design - Validations

## Zero Mana Cost Detection

### **Id**
card-zero-cost-validation
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - manaCost["\':\s]*0
  - cost["\':\s]*0
  - "mana":\s*0
  - mana_cost:\s*0
  - castingCost:\s*0
### **Message**
  Zero mana cost detected. Free spells are historically the most broken
  cards in TCG design. Consider adding a minimum cost of 1, or adding
  significant alternate costs (exile cards, pay life, sacrifice).
  
### **Fix Action**
  Change cost to 1 or add meaningful alternate costs:
  - Pay 2 life
  - Exile a card from hand
  - Sacrifice a permanent
  - Discard a card
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js
  - *.xml

## Free Cast Mechanic Detection

### **Id**
card-free-cast-detection
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - freeCast["\':\s]*true
  - canCastForFree
  - alternateCost["\':\s]*0
  - castWithoutPaying
  - without paying.*mana cost
  - play.*for free
### **Message**
  Free casting mechanic detected. Cards that can be cast without paying
  their mana cost break resource systems and enable degenerate combos.
  Every banned card in Magic's history involved free spells.
  
### **Fix Action**
  Add meaningful restrictions to free casting:
  - Once per turn only
  - Only during specific game states (opponent attacking)
  - Require significant resource payment (exile 2 cards)
  - Limit to low-impact effects
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Unrestricted Tutor Detection

### **Id**
card-unrestricted-tutor
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - searchLibrary.*any.*card
  - tutor.*any
  - search.*deck.*choose.*any
  - find any card
  - search your library for a card
### **Message**
  Unrestricted tutor effect detected. Tutors that find any card eliminate
  variance and enable consistent combo kills. Consider adding restrictions
  on what can be searched for.
  
### **Fix Action**
  Add restrictions to the tutor:
  - Limit by card type (creature, instant, etc.)
  - Limit by mana cost (costs 2 or less)
  - Limit by other criteria (color, subtype)
  - Consider "reveal" clause for opponent knowledge
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Instant Win Condition Detection

### **Id**
card-instant-win
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - you win the game
  - wins the game
  - winGame\(\)
  - gameWin\s*[:=]
  - alternateWinCondition
### **Message**
  Alternate win condition detected. "You win the game" effects need
  extremely careful balancing. The condition should require multiple
  turns to achieve and provide opponent with interaction opportunities.
  
### **Fix Action**
  Ensure the win condition:
  1. Cannot be achieved instantly (requires upkeep trigger)
  2. Has a multi-step setup
  3. Can be disrupted by common game actions
  4. Consider adding a "you lose the game" safety valve
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Mana Doubling Effect Detection

### **Id**
card-mana-doubling
### **Severity**
error
### **Type**
regex
### **Pattern**
  - double.*mana
  - mana.*double
  - add.*twice.*mana
  - manaMultiplier
  - mana.*\*\s*2
  - multiply.*mana
### **Message**
  Mana doubling effect detected. Mana doublers break the resource curve
  and enable degenerate combos with X-cost spells. Consider using
  fixed mana addition instead.
  
### **Fix Action**
  Replace doubling with fixed addition:
  - "Add 2 mana" instead of "double mana"
  - Cap the bonus (add up to 3 extra mana)
  - Add "once per turn" restriction
  - Make the effect very expensive (7+ mana)
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Repeatable Card Draw Detection

### **Id**
card-repeatable-draw
### **Severity**
error
### **Type**
regex
### **Pattern**
  - tap.*draw a card
  - upkeep.*draw
  - whenever.*draw a card
  - draw.*each turn
  - repeatableDraw
### **Message**
  Repeatable card draw effect detected. Engines that draw cards every
  turn create inevitable card advantage that's difficult to overcome.
  Ensure there's a meaningful cost or limitation.
  
### **Fix Action**
  Add costs and restrictions:
  - Mana cost for activation (2+ mana)
  - Life payment
  - "Once per turn" limitation
  - Condition that opponent can disrupt
  - Make the permanent fragile (1 toughness)
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Uncapped Stat Scaling Detection

### **Id**
card-uncapped-scaling
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \+1/\+1 for each
  - power.*equal to.*number
  - toughness.*equal to.*count
  - gets.*\+X/\+X where X
  - forEachBonus
  - countBasedStats
### **Message**
  Uncapped stat scaling detected. "For each" effects can create
  arbitrarily large creatures that trivialize combat. Consider adding
  a maximum cap.
  
### **Fix Action**
  Add scaling limits:
  - "up to +5/+5" cap
  - Use diminishing returns (each beyond first is +1/+0)
  - Count things that don't grow infinitely (lands, ~5-7 max)
  - Count opponent's resources (they can deplete them)
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Pushed Hexproof Creature Detection

### **Id**
card-hexproof-pushed
### **Severity**
error
### **Type**
regex
### **Pattern**
  - hexproof.*power.*[3-9]
  - power.*[3-9].*hexproof
  - hexproof.*stats.*efficient
  - "hexproof".*"power":\s*[3-9]
### **Message**
  Powerful hexproof creature detected. Hexproof creatures with good
  stats create uninteractive games where opponents have no answers.
  Consider using ward instead or reducing stats.
  
### **Fix Action**
  Balance hexproof creatures:
  - Reduce stats (2/2 maximum for hexproof)
  - Use ward instead (can target with extra cost)
  - Make hexproof conditional (until end of turn, when blocking)
  - Increase mana cost significantly (6+ for any meaningful stats)
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Graveyard Loop Detection

### **Id**
card-graveyard-loop
### **Severity**
error
### **Type**
regex
### **Pattern**
  - return.*graveyard.*hand.*return
  - graveyard.*battlefield.*graveyard
  - recursion.*infinite
  - graveyardLoop
  - when.*dies.*return
### **Message**
  Potential graveyard loop detected. Cards that can return themselves
  from the graveyard repeatedly create infinite value engines. Ensure
  there's a terminus (exile after use).
  
### **Fix Action**
  Add loop prevention:
  - "Exile instead of graveyard" clause
  - "Once per game" restriction
  - Significant mana cost for recursion
  - Exile after being cast from graveyard (like Flashback)
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Early Land Acceleration Detection

### **Id**
card-land-acceleration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - manaCost["\':\s]*1.*land.*battlefield
  - cost.*1.*addLand
  - one mana.*extra land
  - turn one.*land
### **Message**
  1-mana land acceleration detected. Early ramp is very powerful and
  can lead to unfair mana advantages. Consider making the effect cost
  2+ mana or add significant drawbacks.
  
### **Fix Action**
  Balance early ramp:
  - Increase cost to 2 mana minimum
  - Ramped land enters tapped
  - Limit to basic lands only
  - Add meaningful drawback (life loss, tapped creature)
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## ETB Removal Detection

### **Id**
card-etb-removal
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - enters.*destroy.*target
  - etb.*exile.*permanent
  - when.*enters.*remove
  - entersBattlefield.*destroy
### **Message**
  Enter-the-battlefield removal detected. ETB removal provides inherent
  2-for-1 card advantage. Ensure the creature has low stats or high
  mana cost to compensate.
  
### **Fix Action**
  Balance ETB removal:
  - Creature should have poor stats (1/1 or 2/2 at most)
  - Mana cost should be high (4+ mana)
  - Consider making effect optional with mana cost
  - Limit target scope (only artifacts, only creatures cost 3+)
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Flash with ETB Effect Detection

### **Id**
card-flash-etb
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - flash.*enters the battlefield
  - flash.*etb
  - instant speed.*when.*enters
  - "flash".*"entersTrigger"
### **Message**
  Flash creature with ETB effect detected. This combination is
  inherently powerful, providing both tactical flexibility and
  guaranteed value. Reduce stats or increase cost.
  
### **Fix Action**
  Balance flash + ETB:
  - Add 1-2 mana to cost compared to sorcery-speed version
  - Reduce power/toughness
  - Make ETB effect weaker than instant spell equivalent
  - Consider conditional flash (only on opponent's turn)
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Complex Common Card Detection

### **Id**
card-complexity-common
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - rarity.*common.*triggered.*triggered
  - rarity.*common.*whenever.*whenever
  - common.*abilities.*length.*[4-9]
### **Message**
  Common card with multiple triggered abilities detected. Following
  New World Order, commons should be simple. Move complex cards to
  uncommon or higher rarity.
  
### **Fix Action**
  Simplify commons:
  - Limit to 1 triggered ability maximum
  - Keep rules text under 3 lines
  - No "for each" or counting mechanics
  - Move to uncommon if complexity is needed
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml
  - *.ts
  - *.js

## Targeting Language Inconsistency

### **Id**
card-targeting-inconsistency
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - choose.*creature.*destroy
  - select.*target
  - pick.*target
### **Message**
  Inconsistent targeting language detected. In card games, "target" has
  specific rules meaning (can be countered by hexproof/shroud). Use
  "target" for effects that can be countered, "choose" for those that can't.
  
### **Fix Action**
  Use consistent terminology:
  - "Target" = affected by hexproof/shroud
  - "Choose" = ignores hexproof/shroud (no targeting)
  - Never use "select" or "pick" for targeting
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml

## Missing Card Rarity

### **Id**
card-missing-rarity
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - "name":\s*"[^"]+"\s*,\s*(?!"rarity")
  - name:.*\n(?!\s*rarity:)
### **Message**
  Card definition may be missing rarity. Every card needs a rarity
  for proper set distribution and draft balance.
  
### **Fix Action**
  Add rarity field:
  - "common" for simple, frequently appearing cards
  - "uncommon" for moderate complexity, synergy pieces
  - "rare" for powerful, complex cards
  - "mythic" for splashy, game-changing cards
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml

## Stats Without Creature Type

### **Id**
card-stats-without-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - power.*[0-9].*(?!creature|type)
  - toughness.*[0-9].*(?!creature|type)
  - "attack":\s*[0-9]+\s*(?!.*"type")
### **Message**
  Power/toughness defined without creature type. Non-creature cards
  should not have combat stats unless they become creatures.
  
### **Fix Action**
  Either:
  - Add creature type to the card
  - Remove power/toughness stats
  - Add "becomes a creature" clause if needed
  
### **Applies To**
  - *.json
  - *.yaml
  - *.yml

## Random Effect Without Seed

### **Id**
card-rng-without-seed
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Math\.random\(\)
  - random\(\)(?!\s*\(seed)
  - flip.*coin.*Math\.random
### **Message**
  Random effect using unseeded random. For reproducibility in replays,
  testing, and anti-cheat, use seeded random number generators.
  
### **Fix Action**
  Use seeded RNG:
  - Pass game state seed to random function
  - Store random results in game log
  - Enable deterministic replay of games
  
### **Applies To**
  - *.ts
  - *.js

## Direct Card State Mutation

### **Id**
card-state-mutation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - card\.[a-z]+\s*=
  - \.power\s*\+=
  - \.toughness\s*=
### **Message**
  Direct card state mutation detected. Card games should use immutable
  state updates for proper undo/redo, networking, and debugging.
  
### **Fix Action**
  Use immutable patterns:
  - Create new card object with updated values
  - Use game state management (Redux, Zustand)
  - Apply mutations through action dispatchers
  
### **Applies To**
  - *.ts
  - *.js

## Async Effect Without Queue

### **Id**
card-async-effect-resolution
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - async.*resolveEffect
  - await.*castCard
  - promise.*trigger
### **Message**
  Async card effect without proper queue management detected. Card
  games need deterministic effect ordering. Use an effect stack/queue.
  
### **Fix Action**
  Implement effect queue:
  - Add effects to queue in LIFO order
  - Resolve one at a time
  - Handle interrupts/responses properly
  - Never use raw async/await for game logic
  
### **Applies To**
  - *.ts
  - *.js