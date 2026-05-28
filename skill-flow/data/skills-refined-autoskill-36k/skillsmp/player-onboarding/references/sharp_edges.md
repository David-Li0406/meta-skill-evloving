# Player Onboarding - Sharp Edges

## Tutorial Jail Syndrome

### **Id**
tutorial-jail-syndrome
### **Summary**
Players quit because they're trapped in tutorial before experiencing the "real" game
### **Severity**
critical
### **Situation**
Tutorial is 10+ minutes before player experiences core gameplay loop
### **Why**
  Studies show 60%+ of players quit during tutorials that exceed 3 minutes on mobile,
  10 minutes on PC/console. Players downloaded your game to PLAY, not to be lectured.
  The longer before "real" gameplay, the higher your drop-off rate.
  
  Actual data from mobile games:
  - 3 minute tutorial: 40% drop-off
  - 5 minute tutorial: 55% drop-off
  - 10 minute tutorial: 75% drop-off
  
  You're literally teaching players to quit.
  
### **Solution**
  # The core loop should start within 30 seconds
  
  # WRONG approach:
  gameStart() {
    this.playIntroVideo()        # 2 min
    this.showStoryExposition()   # 3 min
    this.teachMovement()         # 2 min
    this.teachCombat()           # 3 min
    this.teachInventory()        # 2 min
    this.startRealGame()         # Player left 10 minutes ago
  }
  
  # RIGHT approach:
  gameStart() {
    # Player playing in 10 seconds
    this.dropPlayerIntoAction()
  
    # Teach ONE thing (movement)
    # Then let them play for 60 seconds
  
    # Teach next thing when they need it
    # Sprinkle teaching across first 30 minutes
  }
  
  # Measure: What percentage of players reach core loop?
  # Target: 80%+ should reach real gameplay
  
### **Symptoms**
  - Multi-step forced tutorial before gameplay
  - Players asking "when does the game start"
  - High drop-off before level 1 completion
  - Tutorial completion rate below 60%
### **Detection Pattern**
tutorial.*step.*[5-9]|tutorialPhase.*>.*3

## Information Overload Dump

### **Id**
information-overload-dump
### **Summary**
Overwhelming players with all mechanics at once causes them to remember nothing
### **Severity**
critical
### **Situation**
Showing 5+ controls, mechanics, or systems in first few minutes
### **Why**
  Cognitive psychology: Working memory holds 4 items (not 7 as old studies claimed).
  Dumping 10 controls means players retain maybe 2, randomly.
  
  The "curse of knowledge" - you know your game deeply, so everything feels simple.
  To new players, it's all foreign.
  
  Additionally, anxiety increases with complexity. Overwhelmed players feel
  incompetent and quit to protect ego.
  
### **Solution**
  # Miller's Law in practice: 4 items max at once
  
  class ProgressiveTeaching {
    teachingBudget = 4  # Max 4 things at once
  
    # Pace reveals across HOURS, not minutes
    revealSchedule = {
      minute0: ['move'],
      minute3: ['jump'],
      minute10: ['attack'],
      minute20: ['block'],
      minute45: ['special'],
      hour1: ['inventory'],
      hour2: ['crafting']
    }
  
    # Each new mechanic = practice time before next
    afterTeaching(mechanic) {
      this.lockNewTeaching(5 * 60)  # 5 minutes minimum
      this.createPracticeScenarios(3)  # 3 uses before next lesson
    }
  }
  
  # Breath of the Wild teaches for 10+ HOURS
  # Players don't even realize they're still learning
  
### **Symptoms**
  - Control screen with 8+ bindings
  - Multiple popups in quick succession
  - Players asking "what button does X"
  - Players using only 2-3 mechanics despite knowing more
### **Detection Pattern**
showTutorial.*showTutorial.*showTutorial|hints\.length\s*>\s*3

## Explain Obvious Mechanics

### **Id**
explain-obvious-mechanics
### **Summary**
Telling players to "move with WASD" insults intelligence and creates prompt fatigue
### **Severity**
high
### **Situation**
Explaining movement, camera, or other genre-standard controls
### **Why**
  Every gamer knows WASD/Arrow keys = movement, mouse = camera, Space = jump.
  Explaining this:
  1. Wastes precious first-impression time
  2. Insults the player ("do they think I'm stupid?")
  3. Trains players to IGNORE all prompts
  
  Once players learn your prompts are obvious, they'll skip important ones too.
  
### **Solution**
  # Only teach what's NOT obvious
  
  # Standard controls that DON'T need teaching:
  skipTeaching = [
    'WASD/Arrow movement',
    'Mouse camera control',
    'Space to jump',
    'Click to select',
    'Escape for menu',
    'Scroll to zoom'
  ]
  
  # Controls that DO need teaching:
  needsTeaching = [
    'Game-specific mechanics',
    'Non-standard bindings',
    'Hidden features',
    'Combo systems',
    'Context-sensitive actions'
  ]
  
  # Test: Can you find someone who doesn't know this?
  # If everyone knows it, don't teach it.
  
### **Symptoms**
  - Tutorial for standard FPS/platformer controls
  - "Move with WASD" popup
  - Teaching mouse look in first-person game
  - Players visibly annoyed at basic prompts
### **Detection Pattern**
wasd|arrow.*keys|move.*left.*right|mouse.*look

## Forced Watching Before Playing

### **Id**
forced-watching-before-playing
### **Summary**
Making players watch before they can interact loses them immediately
### **Severity**
high
### **Situation**
Cutscenes, videos, or text before first input
### **Why**
  The single most predictive metric for retention is "time to first input."
  Every second of watching = percentage of players lost.
  
  Mobile games measure in SECONDS:
  - 5s to first input: Baseline
  - 10s to first input: 10% drop-off
  - 30s to first input: 25% drop-off
  
  Players came to PLAY. Passive content is the opposite of play.
  
### **Solution**
  # First input within 5 seconds
  
  class GameStart {
    constructor() {
      # NO unskippable logos
      # NO unskippable cutscenes
      # NO "press any key to start" screens
  
      # Player mashing buttons from splash screen?
      # Catch that input and START THE GAME.
  
      this.timeToFirstInput = 0
      this.targetTime = 5  # seconds
  
      # If story is important, tell it DURING gameplay
      # Voice over while running
      # Environmental storytelling
      # Dialog during downtime
    }
  
    # Start with action, explain later
    # "In medias res" - drop into the middle of things
  }
  
### **Symptoms**
  - Logos before gameplay
  - Multi-minute intro cutscene
  - Lore dump at start
  - "Press Start" screen
### **Detection Pattern**
playVideo.*await|cutscene.*skipEnabled.*false

## Hard Fail During Tutorial

### **Id**
hard-fail-during-tutorial
### **Summary**
Punishing players for experimentation during learning phase
### **Severity**
high
### **Situation**
Game over, lost progress, or harsh penalties during first attempts
### **Why**
  Learning requires failure. If failure is punished, players stop experimenting.
  Fear of failure → conservative play → never learn advanced techniques.
  
  Worse: embarrassing deaths during tutorial = rage quit.
  "I can't even beat the TUTORIAL?"
  
  The tutorial should be impossible to fail, or failure should be instant-retry.
  
### **Solution**
  class SafeLearning {
    constructor() {
      # During tutorial phases:
      this.tutorialMode = {
        deathPenalty: 'none',
        respawnLocation: 'nearby',
        resourceLoss: false,
        enemyDamage: 0.25,  # Enemies hurt less
        playerDamage: 2.0,  # Player hits harder
      }
  
      # Make it HARD to fail initially
      this.trainingWheels = {
        autoAim: 'generous',
        hitboxes: 'forgiving',
        timingWindows: 'wide',
        enemyAggression: 'low'
      }
    }
  
    onTutorialDeath() {
      # Instant respawn, no loading screen
      this.respawnAt(this.lastSafePoint)
  
      # Subtle help (don't patronize)
      this.increaseHealthPickups()
      this.reduceEnemyDamage()
  
      # Never show game over screen during tutorial
    }
  }
  
### **Symptoms**
  - Game over during first level
  - Progress loss on early mistakes
  - Loading screens after tutorial deaths
  - "YOU DIED" screen for new players
### **Detection Pattern**
gameOver.*tutorial|death.*penalty.*tutorial

## Skipping Breaks Game

### **Id**
skipping-breaks-game
### **Summary**
Skip tutorial but game assumes you completed it, causing confusion or softlock
### **Severity**
high
### **Situation**
Skip option exists but doesn't properly initialize game state
### **Why**
  If you offer skip, 30-50% of players will use it.
  If their game is then broken, they'll leave a 1-star review.
  
  Common failures:
  - Items that should have been collected
  - Abilities that should be unlocked
  - NPCs in wrong state
  - Triggers never fired
  
### **Solution**
  class TutorialSkip {
    skipTutorial() {
      # Grant EVERYTHING the tutorial would have given
      this.grantItems(['sword', 'shield', 'potion'])
      this.unlockAbilities(['jump', 'attack', 'block'])
  
      # Set all flags that would have been set
      this.setFlag('metMentor', true)
      this.setFlag('visitedVillage', true)
  
      # Put player in correct state for post-tutorial game
      this.player.level = 2
      this.player.experience = 100
  
      # Teleport to post-tutorial location
      this.teleport('townSquare')
  
      # Optional: Offer reference card
      this.offerControlsReminder()
    }
  
    # TEST: Play entire game with skip
    # The skipped experience should be identical to completed
  }
  
### **Symptoms**
  - Players stuck after skipping
  - Missing abilities or items
  - NPCs reference events player skipped
  - Softlocks for skip users
### **Detection Pattern**
skipTutorial(?!.*grant|.*unlock|.*setFlag)

## No Skip On Replay

### **Id**
no-skip-on-replay
### **Summary**
Forcing the tutorial every new game punishes replayability
### **Severity**
high
### **Situation**
Tutorial is mandatory on every playthrough
### **Why**
  Players who love your game want to replay it.
  Forcing them through baby-steps tutorial is punishment for being fans.
  
  Speedrunners, achievement hunters, content creators all suffer.
  Some will simply stop replaying.
  
### **Solution**
  class ReplayableOnboarding {
    constructor() {
      # Remember at account/device level, not just save file
      this.storage = globalStorage  # Not save-specific
  
      # First play: Full tutorial
      # Second play: Ask
      # Third play: Auto-skip with reminder
    }
  
    onNewGame() {
      const completions = this.storage.get('tutorialCompletions', 0)
  
      if (completions === 0) {
        this.playFullTutorial()
      } else if (completions === 1) {
        this.offerChoice('Play tutorial again?', ['Yes', 'Skip'])
      } else {
        this.skipTutorial()
        this.showBriefReminder('Controls: F1')
      }
    }
  }
  
### **Symptoms**
  - No memory of tutorial completion
  - Forced tutorial every new game
  - Player complaints about replay
  - Speedrunners avoiding your game
### **Detection Pattern**
newGame(?!.*checkTutorialComplete|.*skipOption)

## Wrong Thing First

### **Id**
wrong-thing-first
### **Summary**
Teaching secondary mechanics before core loop causes confusion about game identity
### **Severity**
medium
### **Situation**
Tutorial for crafting before combat, or inventory before movement
### **Why**
  Players form mental model of your game in first 2 minutes.
  If first thing they learn is inventory management, they think it's inventory game.
  Then when combat starts, they're confused about "what this game is."
  
  Core fantasy must be delivered first.
  
### **Solution**
  class TeachingOrder {
    constructor() {
      # Define your core fantasy
      # What is the MAIN thing players will do?
  
      this.coreMechanic = 'combat'  # Example: action game
      this.secondaryMechanics = ['movement', 'abilities']
      this.tertiaryMechanics = ['inventory', 'crafting', 'trading']
  
      # Teaching order follows importance
      this.order = [
        this.coreMechanic,       # First
        ...this.secondaryMechanics,
        ...this.tertiaryMechanics  # Last (or never in tutorial)
      ]
    }
  
    # First 5 minutes should scream "THIS IS WHAT THIS GAME IS"
    # Not "here's the inventory UI"
  }
  
  # Example:
  # Shooter: Shoot within 30 seconds
  # Puzzle: Solve puzzle within 60 seconds
  # Racing: Drive car within 10 seconds
  # RPG: Combat encounter within 2 minutes
  
### **Symptoms**
  - UI tutorial before gameplay
  - Inventory before core loop
  - Settings/customization before play
  - Players confused about game genre
### **Detection Pattern**
teach.*inventory|tutorial.*menu|settings.*first

## Single Path Assumption

### **Id**
single-path-assumption
### **Summary**
Tutorial assumes one correct solution, breaking for creative players
### **Severity**
medium
### **Situation**
Player solves tutorial "wrong" and gets stuck or confused
### **Why**
  Players are creative. They'll try unexpected solutions.
  If your tutorial only works one way, creative players get stuck.
  
  Example: Tutorial says "jump on box to reach ledge."
  Player uses rocket jump instead. Box is still there, blocking progress.
  
### **Solution**
  class FlexibleTutorial {
    constructor() {
      # Define goal, not path
      this.objective = 'reachLedge'
  
      # Accept any valid solution
      this.validSolutions = [
        'jumpOnBox',
        'doubleJump',
        'wallJump',
        'rocketJump',
        'grapplingHook'
      ]
  
      # Clear the objective when ANY valid solution used
      this.onAnySuccess(() => this.clearObjective())
    }
  
    # Test with: What if player does X instead?
    # For every step, imagine 3 alternative solutions
    # Support all of them
  }
  
### **Symptoms**
  - Players stuck despite solving puzzle
  - That's not how you're supposed to do it
  - Tutorial only works one way
  - Creative solutions break progression
### **Detection Pattern**
if.*===.*&&.*expectedSolution

## Hint Spam Annoyance

### **Id**
hint-spam-annoyance
### **Summary**
Relentless hints that won't stop even when player is exploring
### **Severity**
medium
### **Situation**
"Did you forget to press X?" appearing every 10 seconds
### **Why**
  Not every pause is confusion. Sometimes players want to explore.
  Constant hints communicate "you're doing it wrong."
  
  Hint fatigue: After being interrupted 5 times, players ignore ALL hints.
  When they actually need help later, they've learned to dismiss.
  
### **Solution**
  class RespectfulHints {
    constructor() {
      # Escalating delay between hints
      this.hintDelays = [30, 60, 120, 300]  # seconds
  
      # Detect if player is exploring vs stuck
      this.detectIntent = {
        exploring: player.isMoving && player.isLooking,
        stuck: player.idle > 30 && player.sameArea
      }
  
      # Hint counter with max
      this.maxHintsPerObjective = 3
    }
  
    shouldShowHint(objective) {
      if (this.detectIntent.exploring) return false
      if (this.hintsShown[objective] >= this.maxHintsPerObjective) return false
      if (this.timeSinceLastHint < this.currentDelay) return false
  
      return this.detectIntent.stuck
    }
  
    onHintDismissed() {
      # Player dismissed = they're not stuck
      this.increaseDelay()
      this.reduceHintFrequency()
    }
  }
  
### **Symptoms**
  - Same hint appearing multiple times
  - Hints during exploration
  - No cooldown between hints
  - Players complaining about nagging
### **Detection Pattern**
showHint(?!.*cooldown|.*maxShows|.*delay)

## No Reinforcement After Teaching

### **Id**
no-reinforcement-after-teaching
### **Summary**
Teaching mechanic once and never using it again means players forget
### **Severity**
medium
### **Situation**
Showed jump tutorial in level 1, next jump required in level 5
### **Why**
  Learning decay is real. Skills unused for 10 minutes start fading.
  If you teach then don't reinforce, the teaching was wasted.
  
  The "use it or lose it" principle applies to game mechanics too.
  
### **Solution**
  class ReinforcementSchedule {
    constructor() {
      # Spaced repetition after teaching
      this.reinforcement = {
        jump: [
          { level: 1, uses: 5 },   # Intro: 5 easy jumps
          { level: 2, uses: 3 },   # Reinforce: 3 moderate
          { level: 3, uses: 2 },   # Combine with other skills
          # Now it's part of regular vocabulary
        ]
      }
    }
  
    afterTeaching(mechanic) {
      # Schedule 3-5 uses in next 10 minutes
      this.scheduleReinforcement(mechanic, {
        usesRequired: 4,
        timeWindow: '10min',
        difficultyRamp: 'gradual'
      })
    }
  }
  
  # Pattern: Teach -> Use x3 easy -> Use x2 medium -> Combine
  # Then mechanic is "learned" and can appear anywhere
  
### **Symptoms**
  - Large gaps between mechanic uses
  - Players forgetting taught mechanics
  - Mechanic used once then shelved
  - Need to re-teach later
### **Detection Pattern**


## Metrics Blind Onboarding

### **Id**
metrics-blind-onboarding
### **Summary**
Not measuring where players drop off means you can't fix problems
### **Severity**
high
### **Situation**
No analytics for tutorial completion, step timing, or drop-off
### **Why**
  You cannot improve what you don't measure.
  Without data, you're guessing why players leave.
  
  Every minute of onboarding is a funnel step.
  Measuring each step reveals exactly where players churn.
  
### **Solution**
  class OnboardingMetrics {
    constructor() {
      this.funnel = [
        'game_launched',
        'first_input',
        'tutorial_step_1',
        'tutorial_step_2',
        'tutorial_complete',
        'core_loop_reached',
        'first_session_complete',
        'd1_return',
        'd7_return'
      ]
    }
  
    trackStep(step) {
      analytics.track('onboarding_funnel', {
        step,
        timeFromStart: performance.now() - this.startTime,
        deaths: this.deathCount,
        hintsShown: this.hintCount,
        hintsClicked: this.hintClickCount,
        skippedContent: this.skippedCount
      })
    }
  
    # Dashboard should show:
    # - Conversion at each step
    # - Average time per step
    # - Drop-off spikes
    # - Correlation with retention
  }
  
  # Key questions analytics should answer:
  # - What % complete tutorial?
  # - Where is the biggest drop?
  # - Are hints helping?
  # - Does skip hurt retention?
  
### **Symptoms**
  - No tutorial analytics
  - Can't answer "where do players quit"
  - Guessing at improvements
  - No A/B testing capability
### **Detection Pattern**
tutorial(?!.*track|.*analytics|.*metrics)

## Mobile First Minutes Failure

### **Id**
mobile-first-minutes-failure
### **Summary**
Mobile players decide in 3 minutes; desktop patterns don't transfer
### **Severity**
critical
### **Situation**
Applying PC/console onboarding length to mobile game
### **Why**
  Mobile attention span is measured in seconds, not minutes.
  Mobile players often in interruptible contexts (commute, waiting).
  They need to feel value IMMEDIATELY.
  
  The "3-minute rule": Within 3 minutes, mobile player must:
  1. Understand core loop
  2. Experience first reward
  3. Feel anticipation for return
  
### **Solution**
  class MobileFTUE {
    constructor() {
      # Timeline in seconds
      this.timeline = {
        0: 'Splash/logo (skip on tap)',
        5: 'First touch input',
        15: 'Core mechanic demonstrated',
        30: 'First reward collected',
        60: 'Core loop completed once',
        90: 'First "real" challenge',
        120: 'Session goal achieved',
        150: 'Return hook (daily reward, energy, event)',
        180: 'Natural stopping point'
      }
  
      # Every second counts
      this.maxTimeToFirstInput = 5
      this.maxTimeToReward = 30
      this.maxTimeToLoop = 60
    }
  
    # Mobile-specific patterns:
    # - One-finger controls only initially
    # - Portrait mode first (most intimate)
    # - Haptic feedback on every action
    # - Save constantly (could close any moment)
    # - Show progress visually (no text reading)
  }
  
### **Symptoms**
  - 5+ minute tutorial on mobile
  - Complex controls in first session
  - No clear stopping points
  - No return hook setup
### **Detection Pattern**
tutorialDuration.*>.*180|mobileTimeout.*>.*60