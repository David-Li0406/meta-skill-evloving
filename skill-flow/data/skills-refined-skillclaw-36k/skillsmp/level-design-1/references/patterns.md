# Level Design

## Patterns


---
  #### **Name**
The Three-Beat Level Structure
  #### **Description**
Structure levels as Setup, Confrontation, Resolution - borrowed from story structure
  #### **When**
Designing linear or semi-linear levels with clear progression
  #### **Example**
    # Three-Beat Structure
    
    ## Beat 1: Setup (20-30% of level)
    - Introduce the space and its rules
    - Safe exploration with light challenges
    - Teach mechanics through controlled encounters
    - Establish the visual language and mood
    - Plant the "weenie" - show the destination
    
    ## Beat 2: Confrontation (50-60% of level)
    - Escalate complexity and danger
    - Combine mechanics in new ways
    - Push/pull pacing - intense combat, then breather
    - Introduce the complication or twist
    - Multiple paths with meaningful choices
    
    ## Beat 3: Resolution (15-25% of level)
    - Climax encounter or puzzle
    - Test mastery of level's mechanics
    - Payoff for exploration and setup
    - Clear sense of completion
    - Set up next level's hook
    

---
  #### **Name**
Push and Pull Pacing
  #### **Description**
Alternate between high-intensity and low-intensity spaces to prevent fatigue
  #### **When**
Designing any level longer than 5 minutes
  #### **Example**
    # Push and Pull Rhythm
    
    ## The Pattern
    PUSH (High Intensity) → PULL (Low Intensity) → PUSH → PULL
    
    ## PUSH Spaces (20-40% of playtime)
    - Combat arenas
    - Timed challenges
    - High-stakes traversal
    - Boss encounters
    - Stealth sections
    
    ## PULL Spaces (40-60% of playtime)
    - Exploration zones
    - Safe rooms / save points
    - Narrative moments
    - Puzzle sections (depending on stress)
    - Scenic vistas and rewards
    - Resource collection areas
    
    ## Why It Works
    - Players need mental recovery time
    - Contrast makes intensity feel more intense
    - Provides reflection time for story
    - Creates memorable rhythm
    
    ## Common Mistake
    Back-to-back combat with no breather = player fatigue
    All exploration with no tension = player boredom
    

---
  #### **Name**
Weenies and Landmarks (Disney Principle)
  #### **Description**
Large visible landmarks that orient players and draw them forward
  #### **When**
Designing open spaces or areas where players might get lost
  #### **Example**
    # Weenie Design (Term from Walt Disney)
    
    ## What is a Weenie?
    A large, visible landmark that:
    - Can be seen from multiple locations
    - Draws player attention and curiosity
    - Provides consistent orientation
    - Rewards the journey when reached
    
    ## Hierarchy of Landmarks
    1. GLOBAL WEENIE (visible from 70%+ of map)
       - The mountain, tower, castle, smoke column
       - "You can always see where you need to go"
    
    2. LOCAL WEENIES (visible from current area)
       - Distinctive buildings, trees, rock formations
       - Guide through sub-areas
    
    3. MICRO-LANDMARKS (immediate orientation)
       - Unique props, color patches, lighting
       - "I remember this corner"
    
    ## Implementation
    ```
    // Ensure weenie visibility
    - Place on elevated terrain
    - Use contrasting colors/silhouette
    - Add lighting (glow, spotlight, fire)
    - Keep sightlines clear to it
    - Make it architecturally distinct
    ```
    
    ## Famous Examples
    - Disneyland: Sleeping Beauty Castle (all paths lead to it)
    - Half-Life 2: The Citadel (always visible in City 17)
    - Breath of the Wild: Every tower and Divine Beast
    

---
  #### **Name**
Breadcrumbing Player Attention
  #### **Description**
Use visual cues to subtly guide players without explicit markers
  #### **When**
Guiding players through environments without UI waypoints
  #### **Example**
    # Breadcrumbing Techniques
    
    ## Light as Primary Guide
    - Brighter areas draw the eye naturally
    - Exit doors slightly brighter than walls
    - Critical paths use warmer/more saturated light
    - Danger areas can use red/warning light
    
    ## Composition and Framing
    - Doorways frame the next destination
    - Converging lines point to objectives
    - Break symmetry where you want attention
    - Use leading lines (pipes, wires, floor patterns)
    
    ## Environmental Hints
    - NPC eye-lines and body language
    - Audio cues (distant sounds, music shifts)
    - Particle effects (dust, steam, sparks)
    - Color contrast on interactive elements
    - "Damaged" areas suggest traversal paths
    
    ## The Valve Method (Left 4 Dead / Half-Life)
    1. Make the correct path obvious but not intrusive
    2. Wrong paths are darker, lead to dead ends quickly
    3. Reward exploration but don't punish main path
    4. Every detail supports the goal
    
    ## Test: The Blur Test
    Blur your level screenshot heavily. Can you still
    see where players should go? If not, your
    composition needs work.
    

---
  #### **Name**
Safe Zone Introduction
  #### **Description**
Start new areas with safe spaces where players learn mechanics without pressure
  #### **When**
Introducing new mechanics, abilities, or enemies
  #### **Example**
    # Safe Zone Design
    
    ## The Safety Bubble Pattern
    Before any challenge, provide:
    1. Clear overview of the space
    2. Observation point (see before doing)
    3. Safe practice area (fail without consequence)
    4. Gradual difficulty ramp
    
    ## Nintendo's Teaching Method
    1. SAFE: Introduce mechanic in zero-risk setting
    2. GUIDED: Simple challenge with clear solution
    3. TWIST: Add complexity or combine mechanics
    4. MASTERY: Test full understanding
    
    ## Example: Teaching Wall Jump
    ```
    Room 1: Pit with spikes, but respawn is instant
            and landing pad is obvious. Learn timing.
    
    Room 2: Same mechanic, now over longer pit.
            Builds confidence.
    
    Room 3: Wall jump PLUS moving platform.
            Combines with existing skill.
    
    Room 4: Full challenge with meaningful stakes.
            Player has earned this difficulty.
    ```
    
    ## Key Principle
    Players should understand a mechanic BEFORE
    they're punished for failing it.
    

---
  #### **Name**
Lock and Key Gating
  #### **Description**
Control progression through various gating mechanisms
  #### **When**
Designing metroidvania, RPG, or any game with progression-based exploration
  #### **Example**
    # Gating Types
    
    ## Hard Gates (Absolute Blocks)
    - KEY GATES: Literal keys, keycards, passwords
    - ABILITY GATES: Requires specific power (double jump, grapple)
    - STORY GATES: Plot event must trigger first
    - NPC GATES: Character blocks until condition met
    
    ## Soft Gates (Skill/Resource Dependent)
    - COMBAT GATES: Enemy too strong without leveling
    - RESOURCE GATES: Need X items to proceed
    - PUZZLE GATES: Solution requires observation/knowledge
    - SKILL GATES: Technically possible, very difficult
    
    ## Design Guidelines
    1. Show the gate before players reach it
       "I can see where I need to go, just not how"
    
    2. Make the unlock feel earned
       Key should require effort to obtain
    
    3. Returning should feel rewarding
       New shortcuts, narrative callbacks, enemy placement changes
    
    4. Avoid "find the key" hunts
       Key location should be hinted or logical
    
    ## Metroidvania Pattern
    ```
    [ Area A ] --> [GATE: Double Jump] --> [ Area B ]
         |                                      |
         v                                      v
    [ Area C ] --> [GATE: Grapple] --> [ Area D ]
    
    - Double Jump found in Area C
    - Grapple found in Area B (after unlocking)
    - Creates satisfying loop of unlock -> explore
    ```
    

---
  #### **Name**
Combat Arena Design
  #### **Description**
Design spaces optimized for action gameplay with proper flow and pacing
  #### **When**
Creating areas where combat is the primary activity
  #### **Example**
    # Combat Arena Principles
    
    ## Shape Language
    - CIRCULAR: 360-degree threats, no safe corners
    - RECTANGULAR: Classic, provides corner refuges
    - ELONGATED: Ranged combat emphasis, flanking lanes
    - IRREGULAR: Organic feel, unpredictable cover
    - TIERED: Verticality creates positioning strategy
    
    ## Cover and Flow
    ```
    [ ] = Full Cover  [/] = Half Cover  [o] = Pillar
    
    Bad Arena:                Good Arena:
    +-------------+          +-------------+
    |             |          |  [/]    [o] |
    |             |          |      []     |
    |             |          |  [o]    [/] |
    +-------------+          +-------------+
    
    Cover placement creates:
    - Movement decisions
    - Tactical positioning
    - Breather opportunities
    - Interesting combat dance
    ```
    
    ## Entry/Exit Points
    - Entry: Give player overview before entering
    - During: Lock doors or spawn waves
    - Exit: Clearly different from entry
    - Reward: Loot, narrative beat, vista
    
    ## Wave Design
    1. First wave: Tutorial wave, low threat
    2. Middle waves: Escalating difficulty
    3. Final wave: Climax, new enemy or combo
    4. Post-combat: Cooldown, resource pickup
    
    ## Multiplayer Considerations
    - Spawn points have 3+ exit options
    - No spawn point has line-of-sight to another
    - Power positions are contestable, not impenetrable
    - Multiple routes to any objective
    

---
  #### **Name**
Metric Standards
  #### **Description**
Define and adhere to consistent spatial measurements based on character controller
  #### **When**
Starting any level design project or blocking out spaces
  #### **Example**
    # Level Design Metrics
    
    ## Core Player Metrics (Establish First!)
    ```
    CHARACTER_HEIGHT    = 1.8m (typical humanoid)
    CROUCH_HEIGHT      = 0.9m
    WALK_SPEED         = 3.5 m/s
    RUN_SPEED          = 6.0 m/s
    JUMP_HEIGHT        = 1.2m (comfortable)
    JUMP_DISTANCE      = 3.0m (comfortable horizontal)
    MAX_JUMP_DISTANCE  = 4.5m (skilled players only)
    ```
    
    ## Space Standards
    ```
    CORRIDOR_MIN_WIDTH     = CHARACTER_WIDTH * 2.5
    CORRIDOR_COMBAT_WIDTH  = CHARACTER_WIDTH * 4
    DOOR_HEIGHT            = CHARACTER_HEIGHT * 1.3
    DOOR_WIDTH             = CHARACTER_WIDTH * 2
    CEILING_COMFORTABLE    = CHARACTER_HEIGHT * 1.5
    CEILING_OPPRESSIVE     = CHARACTER_HEIGHT * 1.1
    ```
    
    ## Jump Distance Guidelines
    ```
    TRIVIAL GAP       = JUMP_DISTANCE * 0.6  (no thought)
    COMFORTABLE GAP   = JUMP_DISTANCE * 0.8  (standard)
    CHALLENGING GAP   = JUMP_DISTANCE * 0.95 (focus required)
    SKILL GAP         = JUMP_DISTANCE * 1.0  (tight timing)
    IMPOSSIBLE GAP    = JUMP_DISTANCE * 1.2  (blocks path)
    ```
    
    ## Sightline Standards
    ```
    SNIPER_RANGE      = Effective weapon range * 1.2
    ENGAGEMENT_RANGE  = 15-30m typical shooters
    MELEE_ARENA       = 10-20m diameter
    COMFORTABLE_VIEW  = 50-100m to landmarks
    ```
    
    ## The Golden Rule
    ALWAYS derive metrics from your character controller.
    Change the controller? Update all metrics immediately.
    

---
  #### **Name**
Teaching Without Tutorials
  #### **Description**
Design levels that teach mechanics through play rather than text prompts
  #### **When**
Introducing any new mechanic, enemy, or system
  #### **Example**
    # Wordless Teaching Design
    
    ## The Valve Method (Portal, Half-Life 2)
    1. ISOLATED INTRODUCTION
       Show mechanic alone, nothing else happening
       Player can't proceed without engaging
    
    2. SAFE FAILURE
       First attempt has minimal punishment
       Instant respawn, no progress loss
    
    3. OBSERVABLE SOLUTION
       Answer is visible if player looks
       NPCs or environment demonstrates
    
    4. COMPLEXITY LAYERING
       Add one thing at a time
       Build on what player knows
    
    ## Practical Example: Teaching Pressure Plates
    ```
    Room 1: Door won't open. Pressure plate glows.
            No enemies. Player experiments.
            Standing on plate opens door.
            LESSON: Pressure plates open doors.
    
    Room 2: Same setup, but box nearby.
            Player standing on plate, door opens.
            But they can't walk through while on plate.
            They see the box. Put box on plate.
            LESSON: Objects work too.
    
    Room 3: Two plates required. One box.
            Player AND box needed.
            LESSON: Combination is possible.
    
    Room 4: Real puzzle with stakes.
            Combines everything learned.
            MASTERY TEST.
    ```
    
    ## The Questions Test
    Before adding tutorial text, ask:
    - Can the environment teach this?
    - Can failure teach this safely?
    - Is there an observable solution?
    - Does player have time to experiment?
    
    If all yes, no text needed.
    

---
  #### **Name**
Verticality and Sightlines
  #### **Description**
Use height variation to create interesting spaces and strategic depth
  #### **When**
Designing any space larger than a single room
  #### **Example**
    # Verticality Design
    
    ## Why Verticality Matters
    - Creates tactical options (high ground advantage)
    - Provides natural landmarks and orientation
    - Enables layered exploration
    - Adds visual interest and scale
    - Creates dramatic reveals
    
    ## Height Categories
    ```
    DEPRESSION    : -2m to -5m (pits, trenches, basements)
    GROUND LEVEL  : 0m (reference point)
    LOW ELEVATION : +1m to +3m (platforms, small stairs)
    MID ELEVATION : +4m to +8m (balconies, rooftops)
    HIGH GROUND   : +10m+ (towers, cliffs, overviews)
    ```
    
    ## Sightline Management
    ```
    REVEAL SIGHTLINES
    - Control what player sees first
    - Frame destinations through openings
    - Use elevation to show scale
    
    BLOCKING SIGHTLINES
    - Prevent seeing end from beginning
    - Create mystery around corners
    - Hide secrets behind geometry
    
    COMBAT SIGHTLINES
    - Long sightlines favor ranged combat
    - Short sightlines favor melee/shotgun
    - Broken sightlines create tension
    ```
    
    ## The Vista Moment
    After climbing or effort, reward with a view:
    - Shows progress (where player came from)
    - Shows goal (where player is going)
    - Provides moment of rest
    - Screenshot opportunity
    
    ## Multiplayer Height Rules
    - High ground should be contestable
    - Multiple routes to elevated positions
    - Height advantage has counters (no fortress)
    - Spawn points at neutral elevation
    

## Anti-Patterns


---
  #### **Name**
Art Before Blockout
  #### **Description**
Creating final art assets before proving the level is fun in graybox
  #### **Why**
You'll spend weeks on art for spaces that get cut. Blockout changes are cheap, art changes are expensive.
  #### **Instead**
Complete blockout, playtest, iterate until fun is proven. THEN begin art pass. Valve blocks out for months before any art.

---
  #### **Name**
The Maze
  #### **Description**
Complex, winding paths with no orientation cues or landmarks
  #### **Why**
Players get lost, frustrated, and quit. Looking at a map is not gameplay.
  #### **Instead**
Use weenies, distinctive areas, and environmental cues. Players should always have a sense of direction.

---
  #### **Name**
Symmetric Multiplayer Maps
  #### **Description**
Perfectly mirrored multiplayer maps with no distinctive landmarks
  #### **Why**
Players can't call out positions effectively. "I'm at the pillar" - which one? Breaks team communication.
  #### **Instead**
Asymmetric landmarks, color-coded areas, distinctive names. Mirror gameplay balance, not visuals.

---
  #### **Name**
Dead Ends Without Purpose
  #### **Description**
Paths that lead nowhere and offer nothing
  #### **Why**
Players feel punished for exploration. Breaks trust that the game rewards curiosity.
  #### **Instead**
Every dead end has a reward - loot, lore, shortcut unlock, or at minimum a vista. Or eliminate the path entirely.

---
  #### **Name**
Backtracking Without Change
  #### **Description**
Forcing players to walk through the same space again with nothing new
  #### **Why**
Backtracking feels like padding. Players notice when you waste their time.
  #### **Instead**
Change the space (new enemies, opened shortcuts, environmental shift) or create one-way flow.

---
  #### **Name**
The Difficulty Cliff
  #### **Description**
Sudden spike in difficulty without proper teaching ramp
  #### **Why**
Players feel the game is unfair. They didn't fail because they're bad, they failed because you didn't teach them.
  #### **Instead**
Gradual difficulty curves. Test every new challenge - if most players fail first try, the teaching failed.

---
  #### **Name**
Metric Violations
  #### **Description**
Jumps that require pixel-perfect timing, corridors too narrow for combat
  #### **Why**
Players can't articulate why something feels bad, but they feel it. Inconsistent metrics destroy trust.
  #### **Instead**
Establish metrics from character controller. Use them religiously. Comfortable margins everywhere.

---
  #### **Name**
Linear Open World
  #### **Description**
Open world map where all content is encountered in fixed order anyway
  #### **Why**
Open world promises player agency. Linear content in open wrapper is a lie.
  #### **Instead**
If content is linear, make the space linear. If space is open, make content truly optional/reorderable.

---
  #### **Name**
Exhaustive Exploration Required
  #### **Description**
Hiding critical items in obscure locations with no hints
  #### **Why**
Most players won't explore every corner. Required items should be findable by typical players.
  #### **Instead**
Critical path items on main route or clearly hinted. Obscure locations for optional bonuses only.

---
  #### **Name**
Tutorial Text Overload
  #### **Description**
Stopping gameplay to show text explaining mechanics
  #### **Why**
Breaks flow. Players skip text. Learning by doing is more memorable.
  #### **Instead**
Design spaces that teach through play. Text only when absolutely unavoidable.