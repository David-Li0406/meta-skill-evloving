# Game Feel Compendium

## What Is Game Feel?

Game feel (also called "juice" or "polish") is the visceral, tactile sensation of interacting with a game. It's what makes pressing a button feel satisfying, even before you see the result.

```
GAME FEEL = Input Response + Sensory Feedback + Simulated Physics

It's the difference between:
"I clicked a button"        →    "I FIRED a weapon"
"The enemy disappeared"     →    "I DESTROYED the enemy"
"I got points"              →    "I WON the jackpot"
```

### The Feel Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│ LEVEL 5: MEANING                                                │
│ "This action has significance in the world"                     │
├─────────────────────────────────────────────────────────────────┤
│ LEVEL 4: CONSEQUENCE                                            │
│ "The world changed because of what I did"                       │
├─────────────────────────────────────────────────────────────────┤
│ LEVEL 3: FEEDBACK                                               │
│ "The game acknowledged my action"                               │
├─────────────────────────────────────────────────────────────────┤
│ LEVEL 2: RESPONSE                                               │
│ "Something happened when I acted"                               │
├─────────────────────────────────────────────────────────────────┤
│ LEVEL 1: INPUT                                                  │
│ "The game received my input"                                    │
└─────────────────────────────────────────────────────────────────┘

Every level matters. Missing any one creates disconnection.
```

## The Juice Framework

"Juice" is excessive positive feedback for small actions. It makes ordinary interactions feel extraordinary.

### The Juice Formula

```
JUICE = Anticipation + Impact + Aftermath

For a button press:

ANTICIPATION:
• Hover state change
• Subtle scale/glow
• Audio: UI hover sound

IMPACT:
• Immediate visual change
• Scale/position shift
• Audio: Click/activation sound
• Screen effects (if major)

AFTERMATH:
• Return animation (overshoot)
• Particle trails/residue
• Lingering audio tail
• State change confirmation
```

### Jan Willem Nijman's Juice Techniques

From the legendary "The Art of Screenshake" talk:

```
1. TWEENING
   Don't just change values—animate between them
   
2. EASING
   Use curves, not linear interpolation
   Ease out for responsive feel
   
3. OVERSHOOT
   Go past the target, then settle back
   Spring physics, squash and stretch
   
4. SCREENSHAKE
   Directional, brief, scaled to importance
   Never random—always purposeful
   
5. PERMANENCE
   Leave traces of actions
   Particles that linger, marks on environment
   
6. FEEDBACK LAYERING
   Visual + Audio + Haptic + Numeric
   Multiple channels reinforce each other
```

## Feedback Design

### The Feedback Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                     FEEDBACK CHANNELS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  VISUAL        │  AUDIO         │  HAPTIC       │  NUMERIC     │
│  ────────      │  ──────        │  ───────      │  ────────    │
│  • Animation   │  • Sound FX    │  • Vibration  │  • Score     │
│  • Particles   │  • Music swell │  • Force      │  • Damage    │
│  • Color       │  • Voice       │  • Resistance │  • Currency  │
│  • Shape       │  • Silence     │  • Weight     │  • Timer     │
│  • Position    │  • Rhythm      │               │  • Progress  │
│  • Light       │                │               │              │
│                                                                 │
│  Primary for   │  Often most    │  Mobile/      │  Confirms    │
│  most games    │  emotional     │  console      │  permanence  │
│                │                │  specific     │              │
└─────────────────────────────────────────────────────────────────┘
```

### Feedback Timing

```
INPUT ──► FEEDBACK

0-50ms:    INSTANTANEOUS - Player feels "connected"
50-100ms:  RESPONSIVE    - Feels fast, controllable  
100-200ms: ACCEPTABLE    - Noticeable but tolerable
200-500ms: SLUGGISH      - Disconnected feeling
500ms+:    BROKEN        - Player questions if it worked
```

**Critical Insight:** The first feedback (visual change, audio cue) must happen within 100ms. Full animations can take longer, but acknowledgment must be immediate.

### Feedback Proportionality

```
ACTION IMPORTANCE          FEEDBACK INTENSITY
───────────────────────────────────────────────
Minor (UI hover)           Subtle (color shift)
Standard (button click)    Moderate (sound + animation)
Significant (place bet)    Strong (multi-channel)
Major (win pot)            Explosive (celebration)
Rare (jackpot)             Unforgettable (everything)
```

## Sound Design for Feel

### The Importance of Audio

> "Remove the sound from any game and it loses 50% of its impact."

```
SOUND ADDS:
• Immediacy (faster than visual processing)
• Emotion (music is feeling)
• Confirmation (audio receipt)
• Weight (impacts feel heavy)
• Space (environment presence)
• Rhythm (gameplay pacing)
```

### Audio Categories

```
UI SOUNDS
─────────
• Hover: Soft, high, brief
• Click: Crisp, satisfying, percussive
• Confirm: Positive, clear
• Cancel: Soft rejection
• Error: Gentle alert, not harsh

GAME SOUNDS
───────────
• Actions: Immediate, proportional
• Impacts: Weight and material
• Success: Celebration, warmth
• Failure: Sympathetic, not punishing
• Ambient: World presence

MUSIC
─────
• State-reactive (tension/calm)
• Victory swells
• Defeat softening
• Anticipation building
```

### Sound Design Principles for Farming in Purria

```
WORLD SOUND PALETTE:
• Organic (wood, brass, plants)
• Mechanical (gears, clockwork)
• Whimsical (chimes, soft bells)
• Warm (not synthetic or cold)

BETTING PHASE:
• Chips/coins: Ceramic, satisfying
• Bet placement: Confident thunk
• Stakes raising: Tension building
• Final commitment: Decisive click

RESOLUTION:
• Pot filling: Liquid satisfaction
• Win: Musical celebration, coins
• Loss: Sympathetic, not harsh
• Near miss: Hopeful, "almost!"

SIMULINS:
• Movement: Soft mechanical whir
• Acknowledgment: Warm chirps
• Success: Happy beep patterns
• Idle: Gentle ambient presence
```

## Animation Principles for Feel

### The 12 Principles Applied to UI

From Disney animation, adapted for game interfaces:

```
1. SQUASH & STRETCH
   Buttons compress on press, spring back
   Numbers squeeze on change

2. ANTICIPATION
   Brief wind-up before action
   Hover states prepare for click

3. STAGING
   Direct attention to important elements
   Dim/pause non-critical elements during key moments

4. FOLLOW-THROUGH & OVERLAPPING
   Elements don't stop all at once
   Trailing particles, secondary motion

5. SLOW IN & SLOW OUT
   Ease curves everywhere
   Never linear motion

6. ARCS
   Natural motion follows curves
   Avoid straight-line paths

7. SECONDARY ACTION
   Background elements react to primary
   Nearby objects respond to explosions

8. TIMING
   Speed communicates weight and importance
   Fast = light, urgent; Slow = heavy, dramatic

9. EXAGGERATION
   Push reactions beyond realistic
   100 coins doesn't just appear—it BURSTS

10. APPEAL
    Characters and elements have personality
    Even UI can be charming
```

### Easing Reference

```
LINEAR
No personality, robotic
Use only for: Progress bars, timers

EASE-OUT (Decelerate)
Responsive, snappy
Use for: Responses to input, UI appearing

EASE-IN (Accelerate)
Anticipation, wind-up
Use for: Elements leaving, charging

EASE-IN-OUT (Smooth)
Natural, graceful
Use for: Idle animations, loops

BOUNCE
Playful, energetic
Use for: Rewards, celebrations, Simulins

ELASTIC
Springy, organic
Use for: Overshoots, game elements

BACK
Wind-up and overshoot
Use for: Dramatic reveals, important actions
```

## Applying Feel to Farming in Purria

### Hex Interaction Feel

```
HOVER:
├─ Visual: Subtle glow, slight lift (translateY: -2px)
├─ Audio: Soft hover tone
└─ Timing: 150ms ease-out

SELECT:
├─ Visual: Ring appears, scale 1.05, elevation increase
├─ Audio: Satisfying click
├─ Particles: Subtle dust/sparkle
└─ Timing: 200ms spring

DESELECT:
├─ Visual: Ring fades, settles back
├─ Audio: Soft release sound
└─ Timing: 150ms ease-out
```

### Betting Feel

```
FOLD:
├─ Visual: Cards slide away, dim
├─ Audio: Soft card shuffle, resigned tone
└─ Timing: 300ms ease-in-out

CALL:
├─ Visual: Coins slide to pot, satisfying stack
├─ Audio: Chip clack, confident placement
├─ Numeric: Coin count animates down
└─ Timing: 400ms with follow-through

ALL-IN:
├─ Visual: All coins sweep dramatically, dramatic lighting
├─ Audio: Heavy chip cascade, tension build
├─ Numeric: Big number sweep
├─ Screen: Subtle vignette, focus
└─ Timing: 600ms dramatic
```

### Win/Loss Feel

```
WIN - SMALL:
├─ Visual: Coins fly to you, +number pops
├─ Audio: Cha-ching, pleasant chime
├─ Particles: Coin sparkles
└─ Timing: 500ms celebration

WIN - BIG:
├─ Visual: Explosion of coins, screen flash, number BURSTS
├─ Audio: Jackpot sound, music swell, coin cascade
├─ Particles: Confetti, coins, sparkles everywhere
├─ Screen: Brief shake, vignette, slow-mo moment
└─ Timing: 1-2 second spectacle

LOSS:
├─ Visual: Coins fade/fall away, subtle dim
├─ Audio: Soft "aww" tone, NOT harsh buzzer
├─ Numeric: Gentle decrement
├─ Message: Sympathetic, forward-looking
└─ Timing: 300ms, don't dwell
```

### Pot Resolution Feel

```
POT FILLING (ANTICIPATION):
├─ Visual: Meter climbing, glow intensifying
├─ Audio: Rising tone, liquid filling
├─ Timing: Build over 1-2 seconds

THRESHOLD CROSSING:
├─ Visual: Flash at 50%/80%, tier indicators light
├─ Audio: Level-up chime, milestone marker
└─ Timing: Brief pause at threshold

FINAL REVEAL:
├─ Visual: Dramatic pause, then result
├─ Audio: Drum roll or tension hold
└─ Timing: 500ms pause before resolution
```

## Feel Debugging

### Signs of Missing Feel

```
SYMPTOMS:
• "It works but something feels off"
• Testers clicking multiple times
• Confusion if action registered
• "It feels like a prototype"
• No emotional response to wins

DIAGNOSIS:
□ Is feedback instantaneous? (<100ms)
□ Is there audio for every action?
□ Do animations have easing?
□ Is feedback proportional to importance?
□ Are there multiple feedback channels?
□ Do elements have overshoot/settle?
□ Is there anticipation before big moments?
```

### The Feel Audit

```
For each interaction, verify:

INPUT ACKNOWLEDGMENT
□ Visual change within 50ms
□ Audio cue appropriate
□ State clearly indicated

TRANSITION QUALITY
□ Animated, not instant
□ Proper easing curve
□ Appropriate duration

COMPLETION SATISFACTION
□ Clear end state
□ Feels finished
□ Proportional to importance

OVERALL IMPRESSION
□ Would I do this repeatedly just for fun?
□ Does it feel like a $60 game?
□ Is there joy in the interaction itself?
```
