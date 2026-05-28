# Card Game Design - Sharp Edges

## Card Free Spells

### **Id**
card-free-spells
### **Summary**
"Free spells" at 0 mana break game balance fundamentally
### **Severity**
critical
### **Situation**
  You design a card that costs 0 mana or can be cast for free via an
  alternate cost (Phyrexian mana, exile from hand, etc.)
  
### **Why**
  Free spells break the fundamental resource system of card games. Mana exists
  to create meaningful decisions about what to play when. Free spells enable:
  - Explosive combo turns (multiple free spells in one turn)
  - Resource denial (Force of Will answers anything turn 1)
  - Broken synergies (free spells + "spells matter" effects)
  
  Every broken Magic deck in history has featured free or undercosted spells:
  Affinity, Storm, Phyrexian mana, Delve, etc.
  
### **Solution**
  If you must have a "free" spell:
  1. Make the effect minimal (cannot affect board state)
  2. Require card disadvantage (exile 2 cards for 1 effect)
  3. Limit to once per turn
  4. Make them only playable in specific game states (when behind on board)
  
  Better solution: Make the card cost 1 mana. The difference between 0 and 1
  is infinite - at 1 mana, the player must sequence their turn around it.
  
### **Symptoms**
  - Combo decks consistently winning turn 2-3
  - Every deck running 4x of the free spell
  - Players complaining about "non-games"
### **Detection Pattern**
cost:\s*0|manaCost:\s*["']?0|freeCast:\s*true|alternateCost
### **Version Range**
all
### **Examples**
  - Mental Misstep (Phyrexian mana counter) - banned in Legacy/Modern
  - Gitaxian Probe (2 life draw + info) - banned everywhere
  - Mox Opal/Chrome Mox (free mana) - banned in Modern
  - Force of Will (free counter) - only balanced in formats with it

## Card Mana Doubling

### **Id**
card-mana-doubling
### **Summary**
Mana doubling effects lead to broken combos
### **Severity**
critical
### **Situation**
  You design a card that doubles mana production or reduces all costs by
  a significant amount.
  
### **Why**
  Mana is meant to be a limiting factor. When you double mana or halve costs:
  - X-cost spells become absurd (deal 20 damage for 10 mana = deal 40)
  - Card advantage becomes irrelevant (play 2 big things per turn)
  - Combos emerge that you didn't anticipate
  
  The problem compounds: double + double = quadruple. Multiple cost reducers
  in play can make spells free unexpectedly.
  
### **Solution**
  1. Never print "double mana" effects without massive restrictions
  2. Cost reducers should cap at 1-2 mana maximum
  3. Add "costs can't be reduced below 1" clauses
  4. Limit to specific card types (only creature spells, only your turn)
  5. Make the doubling effect itself very expensive (8+ mana)
  
### **Symptoms**
  - Players generating 20+ mana before turn 6
  - X-cost spells being played for X=15+
  - Games ending on the turn the doubler lands
### **Detection Pattern**
double.*mana|mana.*double|costs?.*reduced?.*by|mana.*add.*equal
### **Version Range**
all
### **Examples**
  - Nyxbloom Ancient (triple mana) - nearly banned level
  - Urza's Saga (2 mana from 1 land) - broken in combo
  - Goblin Electromancer (costs 1 less) - enables Storm kills

## Card Tutor Consistency

### **Id**
card-tutor-consistency
### **Summary**
Tutors (search effects) break variance and enable combo
### **Severity**
critical
### **Situation**
  You design a card that searches your library for any card and puts it
  in your hand or on top of your library.
  
### **Why**
  Card games rely on variance to prevent repetitive games. Tutors eliminate
  variance, meaning:
  - Games feel same-y (always find the same card)
  - Combo decks become consistent (always have the combo)
  - Best card in deck is effectively an 8-of
  
  Tutors also create decision paralysis ("what should I search for?") and
  slow games down with shuffling.
  
### **Solution**
  1. Restrict what can be tutored (only creatures, only costs 2 or less)
  2. Make tutors expensive (4+ mana for unrestricted tutoring)
  3. Add randomness (look at top 5, choose 1)
  4. Reveal the tutored card (opponent knows what's coming)
  5. Add deck position restrictions (top of library, not hand)
  6. Consider "Discover" mechanics (choose from 3 random options)
  
### **Symptoms**
  - Every game in mirror match plays identically
  - Combo decks winning consistently on same turn
  - Players shuffling excessively (slow play)
### **Detection Pattern**
search.*library|tutor|look.*library.*put.*hand
### **Version Range**
all
### **Examples**
  - Demonic Tutor (any card, 2 mana) - restricted in Vintage
  - Diabolic Intent (any card, sac cost) - combo staple
  - Chord of Calling (creature, instant speed) - enables combo toolbox

## Card Alternate Win

### **Id**
card-alternate-win
### **Summary**
Alternate win conditions need very careful balancing
### **Severity**
critical
### **Situation**
  You design a card with an alternate win condition ("you win the game" text).
  
### **Why**
  Alternate win conditions bypass normal game interaction. When they're
  too easy to achieve:
  - Games become solitaire (ignore opponent, achieve condition)
  - Normal gameplay is invalidated (why fight if they just win?)
  - Feels unfair to lose to (no gradual defeat)
  
  When they're too hard, they're never played and waste design space.
  
### **Solution**
  1. Win condition should require 2+ turns of setup after playing the card
  2. Opponent must have multiple opportunities to interact
  3. Condition should be difficult to achieve accidentally
  4. The card should do almost nothing until the win is achieved
  5. Consider "you lose the game" clauses for safety valves
  
  Classic formula: "At upkeep, if [condition], you win" (gives opponent a turn)
  
### **Symptoms**
  - Games ending without combat
  - Players ignoring board to pursue condition
  - Feelsbad moments with no counterplay
### **Detection Pattern**
win.*game|you win the game|wins the game
### **Version Range**
all
### **Examples**
  - Felidar Sovereign (win at 40 life) - too easy in lifegain decks
  - Laboratory Maniac (win with no cards) - fair because fragile
  - Thassa's Oracle (win with no deck) - broken because instant

## Card Card Draw Engine

### **Id**
card-card-draw-engine
### **Summary**
Repeatable card draw breaks games over time
### **Severity**
high
### **Situation**
  You design a permanent that draws cards repeatedly (tap to draw, triggers
  to draw, draw on upkeep).
  
### **Why**
  Cards are the fundamental resource of card games. A permanent that draws
  cards every turn creates inevitable card advantage:
  - Turn 3: Draw engine lands
  - Turn 6: Opponent is down 3 cards
  - Turn 9: Game is unwinnable for opponent
  
  Unlike mana, extra cards persist. Card advantage compounds.
  
### **Solution**
  1. Require activation cost (mana + tap)
  2. Add life payment or other resource cost
  3. Limit triggers (once per turn maximum)
  4. Make the creature fragile (1 toughness, no hexproof)
  5. Consider "looting" (draw + discard) instead of pure draw
  6. Delayed draw (draw next turn, not immediately)
  
### **Symptoms**
  - Control mirrors devolving to "who finds draw engine first"
  - Games lasting 20+ turns with one player always ahead on cards
  - Draw engine becoming auto-include in all decks of its color
### **Detection Pattern**
draw a card.*whenever|upkeep.*draw|tap.*draw a card
### **Version Range**
all
### **Examples**
  - Dark Confidant (draw on upkeep, life cost) - powerful but fair
  - Sylvan Library (draw 2, pain) - borderline too strong
  - Consecrated Sphinx (draw 2 when they draw) - banned in Duel Commander

## Card Etb Removal

### **Id**
card-etb-removal
### **Summary**
Enter-the-battlefield removal creates oppressive play patterns
### **Severity**
high
### **Situation**
  You design a creature that destroys/exiles a permanent when it enters
  the battlefield.
  
### **Why**
  ETB removal is inherently 2-for-1 card advantage:
  - You get a creature (card 1)
  - You destroy their thing (card 2)
  - They can't even interact (no "in response, kill your creature")
  
  Blink/bounce effects turn ETB removal into repeatable removal, and the
  creature sticks around to attack/block.
  
### **Solution**
  1. Use "dies" triggers instead (opponent can respond, removal is risky)
  2. Add mana cost to ETB effect ("when enters, you may pay 2...")
  3. Make the creature very expensive (6+ mana)
  4. Limit target scope (only artifacts, only tokens)
  5. Make creature stats terrible (1/1 or 0/1)
  6. Consider exile instead of destroy to prevent graveyard abuse
  
### **Symptoms**
  - Creature decks unable to stick threats
  - ETB creature becoming the only creature played
  - Blink decks dominating metagame
### **Detection Pattern**
enters the battlefield.*destroy|etb.*exile.*target|when.*enters.*remove
### **Version Range**
all
### **Examples**
  - Ravenous Chupacabra (4 mana, destroy creature) - format-warping in limited
  - Skyclave Apparition (3 mana, exile) - multi-format staple
  - Solitude (free with pitch) - extremely powerful

## Card Scaling Stat Bonus

### **Id**
card-scaling-stat-bonus
### **Summary**
"For each" stat bonuses can create infinitely large creatures
### **Severity**
high
### **Situation**
  You design a creature with +1/+1 for each of something (cards in hand,
  creatures in play, cards in graveyard).
  
### **Why**
  "For each" scales linearly with game state, meaning:
  - Early game: Reasonable size (3/3, 4/4)
  - Late game: Absurd size (15/15, 20/20)
  - Combo potential: Mill yourself, get 30/30
  
  When the condition is easy to inflate (cards in graveyard), the card
  becomes a one-card win condition.
  
### **Solution**
  1. Cap the bonus ("up to +5/+5" or "maximum power 10")
  2. Count things that don't grow infinitely (lands in play ~5-7)
  3. Count opponent's resources (they can deplete them)
  4. Add a divider (half, rounded down)
  5. Make base stats 0/0 so it dies without the condition
  
### **Symptoms**
  - Self-mill decks creating 20/20 on turn 4
  - Creature becoming "must-answer or lose"
  - Limited games decided by who draws the scaling creature
### **Detection Pattern**
for each|gets \+1/\+1.*each|\+X/\+X where X is
### **Version Range**
all
### **Examples**
  - Tarmogoyf (count types in grave) - multi-format staple because capped
  - Consuming Aberration (cards in grave) - can hit 40/40
  - Serra Avatar (equal to life) - one-shot kills

## Card Land Ramp

### **Id**
card-land-ramp
### **Summary**
Land-based ramp is difficult to interact with
### **Severity**
high
### **Situation**
  You design cards that put extra lands into play, especially at low mana costs.
  
### **Why**
  Land-based mana acceleration is permanent and hard to disrupt:
  - Land destruction is unfun and rarely printed
  - Lands persist through board wipes
  - 1-mana ramp + 2-land = 4 mana on turn 2
  
  Ramp also creates "nothing happening" turns where the ramping player
  doesn't affect the board, only their future mana.
  
### **Solution**
  1. Ramp spells should cost 2+ mana (so turn 1 ramp isn't possible)
  2. Consider "enters tapped" on ramped lands
  3. Create creature-based ramp (vulnerable to removal)
  4. Limit to basic lands (prevents color fixing abuse)
  5. Add meaningful cost (life, card disadvantage, tempo loss)
  6. Cap total lands per turn effects
  
### **Symptoms**
  - Green decks playing 6-drops on turn 3
  - Aggro decks unable to race the ramp
  - Ramp mirrors becoming "who draws more ramp"
### **Detection Pattern**
put.*land.*onto the battlefield|land.*play.*additional|search.*land.*put.*play
### **Version Range**
all
### **Examples**
  - Rampant Growth (2 mana, 1 land) - baseline acceptable
  - Explore (2 mana, extra land play) - powerful when lands available
  - Arboreal Grazer (1 mana creature, extra land) - too fast

## Card Graveyard As Hand

### **Id**
card-graveyard-as-hand
### **Summary**
Graveyard recursion turns discard pile into second hand
### **Severity**
high
### **Situation**
  You design cards that can be cast from the graveyard or return from
  graveyard to hand easily.
  
### **Why**
  The graveyard is meant to be a resource sink, not a resource. When cards
  come back:
  - Card disadvantage effects (discard, mill) backfire
  - Games go long as both players recycle answers
  - Combo potential with self-mill
  
  Graveyard-focused blocks often require banning key pieces.
  
### **Solution**
  1. Exile after use ("cast from graveyard, then exile")
  2. Require significant mana investment to recur
  3. Single-use recursion only (not loops)
  4. Make graveyard hate widely available and maindeckable
  5. Limit recursion to specific card types (creatures only)
  
### **Symptoms**
  - Mill strategies being unplayable (just fuels opponent)
  - Games going 40+ turns with neither player running out of cards
  - Graveyard hate being mandatory sideboard
### **Detection Pattern**
from your graveyard|cast.*from.*graveyard|return.*from.*graveyard
### **Version Range**
all
### **Examples**
  - Flashback mechanic - balanced because exiles after use
  - Unearth - balanced because exiles at end of turn
  - Hogaak (cast from GY repeatedly) - banned everywhere

## Card Hexproof Pushed

### **Id**
card-hexproof-pushed
### **Summary**
Pushed creatures with hexproof create uninteractive games
### **Severity**
medium
### **Situation**
  You design a creature with hexproof and strong stats or abilities.
  
### **Why**
  Hexproof creatures can only be answered by:
  - Board wipes (expensive, not always available)
  - Sacrifice effects (narrow, not in all colors)
  - -X/-X effects (rare)
  
  When the hexproof creature is efficient, every game becomes about
  racing it, and control decks have no tools.
  
### **Solution**
  1. Hexproof creatures should have bad stats (1/1 or 2/2 max)
  2. Consider "ward" instead (can target with extra cost)
  3. Hexproof should be conditional (on your turn only, until damaged)
  4. Large hexproof creatures should cost 6+ mana
  5. Never put hexproof on creatures with built-in card advantage
  
### **Symptoms**
  - Aura/equipment decks becoming dominant
  - Removal-heavy decks becoming unplayable
  - Games decided by "did they draw the hexproof creature"
### **Detection Pattern**
hexproof|can't be the target.*opponent.*controls
### **Version Range**
all
### **Examples**
  - Slippery Bogle (1/1 hexproof, 1 mana) - enables degenerate Bogles deck
  - Carnage Tyrant (hexproof + can't be countered) - format-warping
  - True-Name Nemesis (protection from a player) - Legacy nightmare

## Card Flash Creatures

### **Id**
card-flash-creatures
### **Summary**
Flash creatures blur the line between spells and creatures
### **Severity**
medium
### **Situation**
  You design a creature with flash (can be cast any time you could cast an instant).
  
### **Why**
  Flash creatures are tactically superior to sorcery-speed creatures:
  - Can ambush attackers
  - Opponent must play around them even when not in hand
  - Hold up interaction OR play threat (no commitment)
  
  When flash creatures have strong ETB effects, they become "spells with
  bodies attached" that are always better than equivalent sorceries.
  
### **Solution**
  1. Flash creatures should have lower stats than sorcery-speed equivalents
  2. ETB effects on flash creatures should be weaker
  3. Flash can be a drawback (costs 1 more mana than sorcery version)
  4. Consider "flash until end of turn" type restrictions
  5. Balance flash by making creature fragile (1 toughness)
  
### **Symptoms**
  - Control decks playing only flash creatures
  - Sorcery-speed creatures becoming unplayable
  - Games becoming "draw-go" standoffs
### **Detection Pattern**
flash|cast.*any time|as though it had flash
### **Version Range**
all
### **Examples**
  - Snapcaster Mage (flash, flashback) - format staple for years
  - Restoration Angel (flash, blink) - created oppressive play patterns
  - Vendilion Clique (flash, hand disruption) - multi-format staple

## Card Color Pie Breaks

### **Id**
card-color-pie-breaks
### **Summary**
Color pie violations undermine faction identity
### **Severity**
medium
### **Situation**
  You design a card that gives a color access to abilities it shouldn't have
  (e.g., red card draw that's better than blue, green counterspells).
  
### **Why**
  The color pie exists so that:
  - Each color has strengths and weaknesses
  - Multicolor has meaning (access to multiple pies)
  - Deckbuilding has consequences (mono-color has gaps)
  
  When colors can do everything, color choice becomes meaningless and
  multicolor loses its appeal.
  
### **Solution**
  1. Maintain strict color pie discipline
  2. If bending, require significant cost or condition
  3. Color-shifted effects should be much weaker than original
  4. Document color pie breaks and limit them to 1-2 per set
  5. Consider artifact/colorless for effects that don't fit colors
  
### **Symptoms**
  - Mono-color decks having no weaknesses
  - Multicolor decks becoming suboptimal
  - Colors feeling "samey" without distinct identity
### **Detection Pattern**

### **Version Range**
all
### **Examples**
  - Red Elemental Blast (red counterspell) - acceptable because narrow
  - Beast Within (green destroy any permanent) - controversial break
  - Oko (green creature transformation) - not in green's pie, was broken

## Card Enters Tapped Matters

### **Id**
card-enters-tapped-matters
### **Summary**
"Enters tapped" lands create feel-bad tempo loss
### **Severity**
medium
### **Situation**
  You design lands that enter tapped to balance their effects.
  
### **Why**
  Enters-tapped lands are necessary for balance but create problems:
  - Early game: Devastating tempo loss (behind by a full mana)
  - Late game: Nearly irrelevant (already have enough mana)
  - Land-heavy hands: Multiple tapped lands = disaster
  
  Too many tapped lands make decks clunky; too few makes mana too free.
  
### **Solution**
  1. Use "check lands" (enters untapped if condition met)
  2. Consider "pay life" alternatives (Shock lands)
  3. Limit tapped lands to 4-8 per deck
  4. Dual lands should have a real cost (life, bounce, tapped)
  5. Provide untapped mono-color options at lower rarity
  
### **Symptoms**
  - Aggro decks unplayable due to tapped lands
  - Control mirrors decided by land sequencing
  - "Lucky land" draws deciding games
### **Detection Pattern**
enters the battlefield tapped|comes into play tapped|etb tapped
### **Version Range**
all
### **Examples**
  - Shock lands (pay 2 life or tapped) - excellent design
  - Check lands (condition = untapped) - fair trade-off
  - Tap lands with no upside - feel terrible in constructed

## Card Daynight Tracking

### **Id**
card-daynight-tracking
### **Summary**
Day/Night and other global tracking mechanics add complexity
### **Severity**
low
### **Situation**
  You design a mechanic that tracks global game state (day/night, monarch,
  initiative, etc.).
  
### **Why**
  Global tracking mechanics:
  - Add memory burden for both players
  - Require tokens/indicators to track
  - Can be confusing for new players
  - Interact with all other cards in game
  
  These mechanics are fine but need restraint in frequency.
  
### **Solution**
  1. Limit to 1-2 global mechanics per set
  2. Provide clear visual indicators (tokens, cards)
  3. Make state changes obvious and triggered
  4. Ensure the mechanic is worth the tracking cost
  5. Digital games should automate tracking
  
### **Symptoms**
  - Players forgetting current state
  - Judge calls about state tracking
  - New players overwhelmed by tracking requirements
### **Detection Pattern**
day|night|monarch|initiative|dungeon
### **Version Range**
all
### **Examples**
  - Day/Night (Innistrad) - two states to track
  - Monarch (Conspiracy) - creates fun subgame
  - Dungeon (AFR) - most complex global tracking

## Card Reminder Text Creep

### **Id**
card-reminder-text-creep
### **Summary**
Reminder text takes valuable card real estate
### **Severity**
low
### **Situation**
  You design a card with a new keyword and want to add reminder text.
  
### **Why**
  Reminder text helps new players but costs:
  - Card real estate (less room for abilities)
  - Visual clutter
  - Reduces perceived power level (looks like more text)
  
  Experienced players ignore reminder text, new players need it.
  
### **Solution**
  1. Omit reminder text on rares/mythics (experienced players know keywords)
  2. Use reminder text at common/uncommon
  3. Consider reminder text on first instance only in a set
  4. Digital games can have hover/tap for reminder text
  5. Keep reminder text concise (under 2 lines)
  
### **Symptoms**
  - Cards feeling "crowded" with text
  - Players misreading abilities due to text density
  - Cool abilities being cut for text space
### **Detection Pattern**

### **Version Range**
all
### **Examples**
  - Flying (reminder text at common only) - good practice
  - Deathtouch (minimal reminder) - one sentence
  - Banding (complex reminder) - infamously confusing

## Card Templating Inconsistency

### **Id**
card-templating-inconsistency
### **Summary**
Inconsistent card templating creates rules confusion
### **Severity**
low
### **Situation**
  You write card text that differs from established templating conventions.
  
### **Why**
  Card templating follows specific conventions:
  - "Target" means it can be countered by shroud/hexproof
  - "Choose" means it bypasses hexproof
  - "Up to" means you can choose zero
  - Order of words matters for timing
  
  Inconsistent templating creates rules edge cases and player confusion.
  
### **Solution**
  1. Follow established templating guides religiously
  2. When in doubt, use existing cards as templates
  3. Have rules experts review all card text
  4. Maintain internal templating document
  5. Use consistent action words (destroy, exile, sacrifice)
  
### **Symptoms**
  - Players arguing about card interactions
  - Rules questions requiring official rulings
  - Cards working differently than players expect
### **Detection Pattern**

### **Version Range**
all
### **Examples**
  - "Target creature gets +2/+2" - standard, works as expected
  - "Choose a creature. It gets +2/+2" - bypasses hexproof
  - "Creature gets +2/+2" - affects all creatures? Unclear!