# Player Onboarding

## Patterns


---
  #### **Name**
The Nintendo 1-1 Method
  #### **Description**
Teach through environmental design, not text. The first level IS the tutorial.
  #### **When**
Designing the opening sequence of any game
  #### **Example**
    # World 1-1 teaches without a single word:
    #
    # 1. Mario starts facing RIGHT -> Move right
    # 2. Goomba approaches slowly -> You'll die if you don't act
    # 3. ? block is perfectly positioned -> You'll likely jump into it
    # 4. Mushroom moves toward you -> Collectibles are good
    # 5. First pipe is too short to trap you -> Learn pipes are interactive
    # 6. First pit is small -> Learn about falling with low stakes
    
    # Implementation pattern:
    class TutorialLevel {
      constructor() {
        # Force player in desired direction through level geometry
        this.startPosition = { x: 100, y: GROUND }  # Near left edge
        this.firstReward = { x: 300, y: GROUND + 64 }  # Just ahead
    
        # Slow, predictable first enemy
        this.firstEnemy = new Enemy({
          speed: 0.5,  # Half normal speed
          pattern: 'linear',  # No surprises
          telegraph: 2.0  # Player sees it coming
        })
    
        # Safe fail zone - can't die from first pit
        this.firstPit = new Pit({
          width: 32,  # Tiny gap
          recovery: true  # Ledge to grab if fall
        })
      }
    }
    

---
  #### **Name**
The 30-Second Hook
  #### **Description**
Something memorable and exciting must happen within 30 seconds of starting
  #### **When**
Player launches game for the first time
  #### **Example**
    # Players decide if they like your game within 30 seconds
    # Don't waste this on logos, menus, or cutscenes
    
    # WRONG flow:
    # Studio logo (5s) -> Publisher logo (5s) -> Title screen (wait for input)
    # -> Menu (player clicks New Game) -> Cutscene (2 min) -> Tutorial text
    # = Player waited 3 minutes before playing anything
    
    # RIGHT flow:
    # Title fades in over gameplay -> Press any key to play -> PLAYING (5s)
    
    class GameStart {
      constructor() {
        # Skip logos on first play (show on subsequent boots)
        if (this.isFirstPlay()) {
          this.skipToGameplay()
        }
    
        # Start in medias res - action already happening
        this.setupHookMoment({
          # Something visually impressive
          visualImpact: 'explosion',
    
          # Player has agency immediately
          immediateAction: 'dodge',
    
          # Low-stakes but feels high-stakes
          actualRisk: 'low',
          perceivedRisk: 'high'
        })
      }
    
      # The hook should showcase your core fantasy
      # If you're a shooter: let them shoot immediately
      # If you're a puzzle: give them an "aha" moment
      # If you're a racer: put them in a car moving fast
    }
    

---
  #### **Name**
Progressive Disclosure
  #### **Description**
Reveal complexity gradually as players demonstrate mastery of basics
  #### **When**
Game has multiple mechanics, systems, or controls
  #### **Example**
    # WRONG: Dump all controls at start
    # "Move with WASD, Jump with Space, Attack with J, Block with K,
    #  Dodge with Shift, Special with E, Inventory with I, Map with M..."
    
    # RIGHT: Layer introduction based on need and mastery
    
    class ProgressiveUnlock {
      constructor() {
        this.mechanicsQueue = [
          { mechanic: 'move', unlockAt: 'start' },
          { mechanic: 'jump', unlockAt: 'firstGap' },
          { mechanic: 'attack', unlockAt: 'firstEnemy' },
          { mechanic: 'block', unlockAt: 'afterFirstDeath' },
          { mechanic: 'dodge', unlockAt: 'level2' },
          { mechanic: 'special', unlockAt: 'bossIntro' }
        ]
      }
    
      # Each mechanic follows the cycle:
      # 1. Introduce in isolation (safe space to practice)
      # 2. Test basic competency (easy challenge using mechanic)
      # 3. Combine with known mechanics (build complexity)
      # 4. Master challenge (optional hard test)
    
      introduceMechanic(mechanic) {
        # Pause or slow the game
        this.timeSlow(0.25)
    
        # Show control clearly
        this.showPrompt(`Press ${mechanic.key} to ${mechanic.verb}`)
    
        # Wait for successful execution
        this.waitForAction(mechanic.action)
    
        # Celebrate success
        this.playFeedback('success')
    
        # Resume normal play
        this.timeSlow(1.0)
      }
    }
    

---
  #### **Name**
Contextual Just-In-Time Teaching
  #### **Description**
Teach mechanics exactly when players need them, not before
  #### **When**
Player encounters new situation requiring new skill
  #### **Example**
    # WRONG: Frontload all teaching
    onGameStart() {
      this.showTutorial('movement')
      this.showTutorial('jumping')
      this.showTutorial('combat')
      this.showTutorial('inventory')
      this.showTutorial('crafting')
      # Player has forgotten movement by the time they start
    }
    
    # RIGHT: Contextual triggers
    class ContextualHints {
      constructor() {
        this.hintTriggers = new Map()
    
        # Only show jump tutorial when player reaches a gap
        this.addTrigger('firstGap', {
          condition: () => this.player.nearGap && !this.player.hasJumped,
          hint: 'Press SPACE to jump',
          timeout: 5000,  # Show after 5s of being stuck
          maxShows: 2
        })
    
        # Only show attack when enemy is present
        this.addTrigger('firstEnemy', {
          condition: () => this.nearbyEnemy && !this.player.hasAttacked,
          hint: 'Click to attack',
          timeout: 3000,
          maxShows: 1
        })
      }
    
      update() {
        for (const [id, trigger] of this.hintTriggers) {
          if (trigger.condition() && trigger.shows < trigger.maxShows) {
            this.showHint(trigger.hint)
            trigger.shows++
          }
        }
      }
    }
    

---
  #### **Name**
Safe Failure Space
  #### **Description**
Let players fail without punishment to encourage experimentation
  #### **When**
Introducing any new mechanic or challenge
  #### **Example**
    # Players learn best when failure is safe
    # The first time they encounter something should be forgiving
    
    class SafeFailure {
      createLearningZone(mechanic) {
        # Remove permadeath consequences
        this.deathPenalty = 'respawnNearby'
    
        # Provide extra resources
        this.healPickups = 'abundant'
    
        # Make enemies weaker
        this.enemyDamage = 0.5
    
        # Add visual safety net
        this.showSafeZoneIndicator()
      }
    
      # Breath of the Wild's Great Plateau example:
      # - Isolated from main world (can't get lost)
      # - All 4 core abilities introduced in any order
      # - Shrines are self-contained learning spaces
      # - Death respawns you nearby with no loss
      # - Once you've proven mastery, world opens up
    }
    
    class TutorialEnemy {
      constructor() {
        this.behaviors = {
          # First encounter: telegraph everything
          telegraph: 2.0,  # Huge wind-up
          recovery: 3.0,  # Long pause after attack
          damage: 5,  # Low damage
    
          # As player improves, increase challenge
          veteranBehavior: {
            telegraph: 0.5,
            recovery: 0.5,
            damage: 20
          }
        }
      }
    }
    

---
  #### **Name**
Show Don't Tell
  #### **Description**
Demonstrate mechanics through gameplay, not text boxes
  #### **When**
Any teaching moment
  #### **Example**
    # WRONG: Text explanation
    this.showMessage("Press the A button to jump. Jumping allows you to
      traverse gaps and reach higher platforms. You can also jump on
      enemies to defeat them.")
    
    # RIGHT: Environmental demonstration
    
    class ShowDontTell {
      teachJumping() {
        # Place player in front of small gap with reward on other side
        this.createRewardBait({
          type: 'shinyCollectible',
          position: 'beyondGap'
        })
    
        # If player hasn't jumped in 10 seconds, show minimal prompt
        this.delayed(10000, () => {
          if (!this.player.hasJumped) {
            this.showMinimalPrompt('A')  # Just the button, no text
          }
        })
    
        # NPC demonstration (Valve's method)
        # Have an NPC perform the action where player can see
        this.npc.demonstrate('jump', {
          position: 'playerView',
          timing: 'beforePlayerAttempts'
        })
      }
    
      teachCombat() {
        # Create a situation where combat is the obvious solution
        # Enemy blocks path to clear objective
        # Enemy is slow and weak
        # Success is extremely obvious (explosion, loot, path opens)
      }
    }
    

---
  #### **Name**
The 3-Minute Mobile Rule
  #### **Description**
Mobile players decide within 3 minutes if they'll return
  #### **When**
Designing mobile or casual game onboarding
  #### **Example**
    # Mobile FTUE must accomplish in 3 minutes:
    # 1. Teach core loop
    # 2. Deliver first reward
    # 3. Hook for return (anticipation)
    
    class MobileFTUE {
      constructor() {
        this.timeline = {
          # 0-30s: First input and immediate feedback
          firstInput: {
            maxTime: 10,  # Seconds to first player action
            feedback: 'satisfying',  # Immediate dopamine
          },
    
          # 30-60s: Core loop demonstrated
          coreLoop: {
            action: 'simplified',  # Easiest version
            reward: 'guaranteed',  # Always succeed first time
            celebration: 'overTheTop'  # Make them feel amazing
          },
    
          # 60-120s: First "real" challenge
          firstChallenge: {
            difficulty: 0.3,  # Very easy but feels like accomplishment
            reward: 'meaningful',  # Something they'll use
            hint: 'available'  # Help if stuck
          },
    
          # 120-180s: Setup return hook
          returnHook: {
            # Show something they CAN'T have yet
            preview: 'futureUnlock',
            # Create timer/energy/daily anticipation
            anticipation: 'comeBackTomorrow',
            # Make it easy to leave and return
            savePoint: 'automatic'
          }
        }
      }
    
      # Minimize text - mobile players don't read
      # Maximize touch feedback - haptics, sounds, particles
      # Never gate progress on watching/reading
    }
    

---
  #### **Name**
Veteran Respect Pattern
  #### **Description**
Always provide skip options for experienced players
  #### **When**
Any tutorial or onboarding sequence
  #### **Example**
    class RespectfulTutorial {
      constructor() {
        # Always offer skip prominently
        this.skipButton = {
          visible: true,
          position: 'topRight',
          label: 'Skip Tutorial',
          confirmation: false  # Don't ask "are you sure?"
        }
    
        # Detect veteran behavior
        this.veteranDetection = {
          # If they're using advanced controls, they know the basics
          advancedInput: () => this.detectAdvancedInput(),
          # If they're moving fast and confident
          confidenceLevel: () => this.measureConfidence(),
          # If they skip prompts
          promptSkipping: () => this.trackSkippedPrompts()
        }
      }
    
      adaptToVeteran() {
        if (this.isVeteran()) {
          # Reduce hint frequency
          this.hintCooldown *= 3
    
          # Remove basic prompts
          this.disableBasicPrompts()
    
          # Speed up any mandatory teaching
          this.tutorialSpeed = 2.0
    
          # Unlock all mechanics faster
          this.unlockAccelerator = 2.0
        }
      }
    
      # For sequels or genre-standard games:
      offerExperienceChoice() {
        this.showChoice({
          beginner: "I'm new to [genre]",
          intermediate: "I've played games like this",
          expert: "Skip everything, I know what I'm doing"
        })
      }
    }
    

---
  #### **Name**
Layered Difficulty Curve
  #### **Description**
Start trivially easy, increase difficulty in small steps
  #### **When**
Designing level progression and challenge scaling
  #### **Example**
    # The ideal difficulty curve:
    #
    # Difficulty
    # ^
    # |                    ****
    # |               *****
    # |          *****     ^-- Mastery challenges (optional)
    # |     *****
    # |****                ^-- Main progression
    # +------------------------> Time
    # ^-- "Too easy" phase is intentional
    
    class DifficultyManager {
      constructor() {
        # First 5 minutes should be embarrassingly easy
        this.phases = [
          { name: 'tutorial', difficulty: 0.1, duration: '5min' },
          { name: 'early', difficulty: 0.3, duration: '15min' },
          { name: 'learning', difficulty: 0.5, duration: '30min' },
          { name: 'competent', difficulty: 0.7, duration: '1hr' },
          { name: 'challenge', difficulty: 1.0, duration: 'ongoing' }
        ]
      }
    
      # Never increase difficulty on failure
      onPlayerDeath() {
        this.consecutiveDeaths++
    
        if (this.consecutiveDeaths > 2) {
          this.subtlyDecreaseDifficulty()
          # Resident Evil 4's "Dynamic Difficulty" - secretly helps struggling players
        }
      }
    
      subtlyDecreaseDifficulty() {
        # Hidden assistance (player shouldn't feel helped)
        this.enemyAggression -= 0.1
        this.enemyAccuracy -= 0.1
        this.pickupFrequency += 0.2
        # Player thinks they improved - that's the goal
      }
    }
    

---
  #### **Name**
Onboarding Analytics
  #### **Description**
Measure drop-off at every step to find and fix problems
  #### **When**
Tracking new player experience effectiveness
  #### **Example**
    class OnboardingAnalytics {
      constructor() {
        this.funnelSteps = [
          'game_launched',
          'first_input',
          'tutorial_started',
          'mechanic_1_learned',
          'mechanic_2_learned',
          'first_challenge_completed',
          'tutorial_completed',
          'core_loop_completed',
          'session_2_started',  # Critical retention metric
          'day_7_return'
        ]
      }
    
      trackStep(step) {
        analytics.track('onboarding_funnel', {
          step: step,
          timeInGame: this.sessionTime,
          deaths: this.deathCount,
          hintsShown: this.hintCount,
          skippedPrompts: this.skippedCount
        })
      }
    
      # Key metrics to track:
      metrics = {
        # Where do players quit?
        dropOffPoints: 'step-by-step funnel',
    
        # How long to learn each mechanic?
        mechanicTime: 'time per teaching moment',
    
        # Are hints working?
        hintEffectiveness: 'action after hint vs timeout',
    
        # Are players returning?
        retention: 'D1, D7, D30 return rates',
    
        # What's the average first session?
        sessionLength: 'time to first quit',
    
        # Are veterans skipping?
        skipRate: 'percentage using skip option'
      }
    }
    

---
  #### **Name**
The Valve Playtesting Method
  #### **Description**
Watch players struggle silently, then fix what you learn
  #### **When**
Validating onboarding design
  #### **Example**
    # Valve's rules for playtesting:
    # 1. Never help the player
    # 2. Never explain anything
    # 3. Just watch and take notes
    # 4. If 3 players get stuck at the same spot, it's your fault
    
    class PlaytestSession {
      constructor() {
        this.rules = {
          observerSpeaks: false,  # Never help
          playerAsksQuestion: 'note it, don't answer',
          frustrationVisible: 'note timing and location',
          playerGivesUp: 'session complete'
        }
    
        this.observations = {
          # Track where eyes look
          attentionHeatmap: [],
          # Track where players click/move
          actionHeatmap: [],
          # Track verbal expressions
          frustrationMoments: [],
          # Track "aha" moments
          delightMoments: []
        }
      }
    
      analyze() {
        # If 2+ players confused at same spot = redesign required
        # If player says "I don't know what to do" = hint system failed
        # If player dies 3+ times at same spot = too difficult
        # If player skips content = it's not engaging
        # If player asks "is this supposed to happen?" = unclear feedback
      }
    }
    

## Anti-Patterns


---
  #### **Name**
Tutorial Jail
  #### **Description**
Forcing players through extensive tutorial before "real" game
  #### **Why**
Players came to play, not to be lectured. Long tutorials cause massive drop-off. Many players will quit before reaching actual gameplay.
  #### **Instead**
Get to gameplay in 30 seconds. Integrate teaching into first real level. Make tutorial skippable.

---
  #### **Name**
Front-Loading All Information
  #### **Description**
Dumping every control and mechanic at game start
  #### **Why**
Humans can hold 4 items in working memory. Showing 12 controls means they remember 0. Players forget everything by the time they need it.
  #### **Instead**
Teach one thing at a time, when player needs it. Progressive disclosure over first hour.

---
  #### **Name**
Teach Then Test Immediately
  #### **Description**
Showing a mechanic once then immediately testing mastery
  #### **Why**
Learning requires practice. One demo isn't learning. Immediate high-stakes test after introduction creates anxiety.
  #### **Instead**
Introduce -> Safe practice -> Easy test -> Combine with known skills -> Mastery test.

---
  #### **Name**
Unskippable Tutorials on Replay
  #### **Description**
Forcing returning players through tutorial every playthrough
  #### **Why**
Disrespects player time. Punishes replays. Veterans will quit rather than sit through basics again.
  #### **Instead**
Remember completion. Offer skip always. Detect veteran behavior and adapt.

---
  #### **Name**
Explaining What's Obvious
  #### **Description**
Tutorial prompts for intuitive actions like "move with arrow keys"
  #### **Why**
Insults player intelligence. Creates prompt fatigue. Players learn to ignore all prompts.
  #### **Instead**
Only teach non-obvious mechanics. Trust players to figure out standard conventions.

---
  #### **Name**
Text Wall Explanations
  #### **Description**
Long text descriptions of mechanics
  #### **Why**
Players don't read. Text breaks immersion. Dense text causes skip-reflex. Even good readers skim.
  #### **Instead**
Show, don't tell. Use visual demonstrations. If you must use text, 5 words or fewer.

---
  #### **Name**
Interrupting Flow for Teaching
  #### **Description**
Stopping gameplay for forced tutorial popups
  #### **Why**
Breaks immersion. Builds resentment. Players remember interruption, not lesson.
  #### **Instead**
Teach during natural pauses. Use environmental teaching. Contextual hints that don't block.

---
  #### **Name**
One-Size-Fits-All Difficulty
  #### **Description**
Same tutorial difficulty regardless of player skill
  #### **Why**
Bores veterans. Overwhelms newbies. Neither group is served.
  #### **Instead**
Detect player skill. Offer difficulty options. Adapt in real-time based on performance.

---
  #### **Name**
Hiding Skip Until End
  #### **Description**
Making skip button invisible or only showing after sitting through content
  #### **Why**
Wastes player time. Builds resentment. Veterans bounce before finding skip.
  #### **Instead**
Visible skip from first frame. No confirmation dialogs. Respect player agency.

---
  #### **Name**
Critical Path Tutorial Only
  #### **Description**
Only teaching mechanics used in main story, ignoring optional depth
  #### **Why**
Players miss rich systems. Optional mechanics never discovered. Reduced engagement with full game.
  #### **Instead**
Surface optional mechanics gradually. Create curiosity about depth. Let players discover.