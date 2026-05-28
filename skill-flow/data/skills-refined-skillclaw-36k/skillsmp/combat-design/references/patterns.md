# Combat Systems Designer

## Patterns


---
  #### **Name**
Hitbox/Hurtbox Separation
  #### **Description**
Separate attack collision (hitboxes) from damage reception (hurtboxes)
  #### **When**
Implementing any melee combat system
  #### **Why**
Allows independent tuning of offensive and defensive collision
  #### **Example**
    // The Fundamental Combat Collision Model
    //
    // HURTBOX: Where the character CAN BE HIT
    // - Usually follows character model closely
    // - Can shrink during dodges/i-frames
    // - Often multiple boxes (head, torso, legs)
    // - Persists throughout all states
    //
    // HITBOX: Where the attack DEALS DAMAGE
    // - Only active during attack's active frames
    // - Does NOT follow weapon model exactly - often larger
    // - Shape matches perceived attack arc, not mesh
    // - Can be multiple hitboxes for one attack
    
    // Example implementation:
    class CombatEntity {
      hurtboxes: Collider[]     // Always present
      activeHitboxes: Hitbox[]  // Only during attacks
    
      // Hitbox data for a sword slash
      attackData = {
        startup: 6,           // Frames before hitbox appears
        active: 4,            // Frames hitbox is dangerous
        recovery: 12,         // Frames after hitbox disappears
        hitbox: {
          offset: { x: 0.5, y: 0.3 },
          size: { width: 1.2, height: 0.8 },  // LARGER than sword mesh
          shape: 'arc',       // Match visual sweep
          arcAngle: 120       // Degrees of coverage
        }
      }
    }
    
    // CRITICAL: Hitbox should be LARGER than visual
    // Players aim at center of target
    // Give them the hit when it looks like a hit
    //
    // From Software, Platinum, and Capcom all use hitboxes
    // 20-40% larger than the weapon mesh
    
    // ADVANCED: Multi-hit prevention
    class Hitbox {
      hitEntities: Set<Entity> = new Set()
    
      checkCollision(hurtbox: Hurtbox): boolean {
        // Already hit this entity this attack
        if (this.hitEntities.has(hurtbox.owner)) return false
    
        // Check collision
        if (this.intersects(hurtbox)) {
          this.hitEntities.add(hurtbox.owner)
          return true
        }
        return false
      }
    
      reset() {
        this.hitEntities.clear()  // Called when attack ends
      }
    }
    

---
  #### **Name**
Input Buffering System
  #### **Description**
Queue inputs during uncommitted states for responsive controls
  #### **When**
Player inputs must feel responsive during animations
  #### **Why**
Human timing is imprecise; buffering bridges intention and execution
  #### **Example**
    // Input Buffer - The secret to responsive combat
    //
    // Without buffer: Player presses attack 2 frames early = input lost
    // With buffer: Input queued, executes when possible = feels responsive
    //
    // Fighting games: 3-10 frame buffer (50-167ms)
    // Action games: 6-15 frame buffer (100-250ms)
    // Casual games: 10-20 frame buffer (167-333ms)
    
    class InputBuffer {
      buffer: BufferedInput[] = []
      bufferDuration: number = 10  // Frames to hold input
    
      addInput(action: string) {
        this.buffer.push({
          action,
          frameAdded: currentFrame,
          expiresAt: currentFrame + this.bufferDuration
        })
      }
    
      consumeInput(action: string): boolean {
        const now = currentFrame
    
        // Find valid buffered input
        const index = this.buffer.findIndex(
          b => b.action === action && b.expiresAt >= now
        )
    
        if (index !== -1) {
          this.buffer.splice(index, 1)
          return true
        }
        return false
      }
    
      update() {
        // Clear expired inputs
        this.buffer = this.buffer.filter(b => b.expiresAt >= currentFrame)
      }
    }
    
    // Usage in combat system
    class Player {
      update() {
        if (input.justPressed('attack')) {
          if (this.canAttack()) {
            this.attack()
          } else {
            inputBuffer.addInput('attack')  // Buffer for later
          }
        }
    
        // Check buffer when becoming actionable
        if (this.canAttack() && inputBuffer.consumeInput('attack')) {
          this.attack()
        }
      }
    }
    
    // ADVANCED: Priority buffering
    // Buffer dodge/roll at higher priority than attack
    // Let players escape combos they're stuck in
    

---
  #### **Name**
Coyote Time and Jump Buffering
  #### **Description**
Forgiveness windows that respect player intent
  #### **When**
Implementing platforming in action games
  #### **Why**
Players press jump slightly after leaving edge; punishing this feels unfair
  #### **Example**
    // COYOTE TIME (named after Wile E. Coyote)
    // Allow jumping for X frames after leaving ground
    //
    // Typical values:
    // Hardcore: 4-6 frames (67-100ms)
    // Standard: 8-12 frames (133-200ms)
    // Forgiving: 15-20 frames (250-333ms)
    
    class PlatformingController {
      grounded: boolean = false
      lastGroundedFrame: number = 0
      coyoteFrames: number = 8
    
      update() {
        if (this.isOnGround()) {
          this.grounded = true
          this.lastGroundedFrame = currentFrame
        } else {
          this.grounded = false
        }
      }
    
      canJump(): boolean {
        // Actually grounded
        if (this.grounded) return true
    
        // Within coyote time
        const framesSinceGrounded = currentFrame - this.lastGroundedFrame
        if (framesSinceGrounded <= this.coyoteFrames) return true
    
        return false
      }
    }
    
    // JUMP BUFFERING (the companion to coyote time)
    // Buffer jump input BEFORE landing
    //
    // Player presses jump 5 frames before landing
    // Without buffer: Jump doesn't happen, feels broken
    // With buffer: Jump queued, executes on landing
    
    class JumpBuffer {
      jumpBuffered: boolean = false
      bufferExpiresAt: number = 0
      bufferDuration: number = 10
    
      bufferJump() {
        this.jumpBuffered = true
        this.bufferExpiresAt = currentFrame + this.bufferDuration
      }
    
      consumeJump(): boolean {
        if (this.jumpBuffered && currentFrame <= this.bufferExpiresAt) {
          this.jumpBuffered = false
          return true
        }
        return false
      }
    
      // Clear expired buffer
      update() {
        if (currentFrame > this.bufferExpiresAt) {
          this.jumpBuffered = false
        }
      }
    }
    
    // Combined in player controller
    if (input.justPressed('jump')) {
      if (this.canJump()) {
        this.jump()
      } else {
        jumpBuffer.bufferJump()
      }
    }
    
    // On landing
    if (this.justLanded && jumpBuffer.consumeJump()) {
      this.jump()
    }
    

---
  #### **Name**
Hitstop (Hit Freeze) System
  #### **Description**
Brief pause on hit to sell impact
  #### **When**
Attacks need to feel impactful
  #### **Why**
Hitstop gives the brain time to register the hit; without it, combat feels floaty
  #### **Example**
    // HITSTOP - The most important combat feel technique
    //
    // When attack connects, BOTH attacker and target pause
    // Duration scales with attack power
    // Creates the "crunch" that sells impact
    //
    // Reference values (at 60fps):
    // Light attack: 3-5 frames (50-83ms)
    // Medium attack: 6-10 frames (100-167ms)
    // Heavy attack: 12-18 frames (200-300ms)
    // Critical/Finishing: 20-30 frames (333-500ms)
    
    class HitstopManager {
      hitstopRemaining: number = 0
    
      applyHitstop(frames: number) {
        // Take the larger hitstop if overlapping
        this.hitstopRemaining = Math.max(this.hitstopRemaining, frames)
      }
    
      update(): boolean {
        if (this.hitstopRemaining > 0) {
          this.hitstopRemaining--
          return true  // Game is frozen
        }
        return false  // Normal update
      }
    }
    
    // Usage in game loop
    function gameLoop(delta) {
      // Check if in hitstop
      if (hitstopManager.update()) {
        // Still render, just don't update positions
        render()
        return
      }
    
      // Normal update
      updateGame(delta)
      render()
    }
    
    // When hit connects
    function onHitConfirmed(attacker, target, damage) {
      const hitstopFrames = calculateHitstop(damage)
    
      // Both freeze (critical for game feel)
      attacker.applyHitstop(hitstopFrames)
      target.applyHitstop(hitstopFrames)
    
      // Global hitstop for camera shake timing
      hitstopManager.applyHitstop(hitstopFrames)
    
      // The "crunch" happens during hitstop
      screenShake(damage)
      spawnHitParticles(target.position)
      playHitSound(damage)
    }
    
    // ADVANCED: Asymmetric hitstop
    // Attacker freezes less than target
    // Creates feeling of follow-through
    function applyAsymmetricHitstop(attacker, target, baseFrames) {
      attacker.applyHitstop(baseFrames * 0.7)  // 70%
      target.applyHitstop(baseFrames)           // 100%
    }
    
    // ADVANCED: Hitstop ramping for combos
    // Each hit in combo adds slightly more hitstop
    // Creates escalating satisfaction
    function comboHitstop(baseFrames, comboCount) {
      const ramp = 1 + (comboCount * 0.1)  // +10% per hit
      const maxMultiplier = 2.0
      return Math.round(baseFrames * Math.min(ramp, maxMultiplier))
    }
    

---
  #### **Name**
Screen Shake for Impact
  #### **Description**
Camera trauma that reinforces hit feedback
  #### **When**
Attacks connect, explosions occur, heavy landings
  #### **Why**
Visual shake combined with hitstop creates visceral impact
  #### **Example**
    // SCREEN SHAKE - The partner to hitstop
    //
    // Types of shake:
    // 1. TRAUMA-BASED: Decaying shake from single events
    // 2. CONTINUOUS: Ongoing shake for rumble/engines
    // 3. DIRECTIONAL: Shake in attack direction
    
    class ScreenShake {
      trauma: number = 0        // 0-1, decays over time
      maxOffset: number = 10    // Max pixel displacement
      maxRotation: number = 2   // Max degrees rotation
      decayRate: number = 0.8   // Per-frame multiplier
    
      // Add trauma from hit (0-1 based on damage)
      addTrauma(amount: number) {
        this.trauma = Math.min(1, this.trauma + amount)
      }
    
      update() {
        if (this.trauma > 0) {
          // Quadratic falloff feels more natural
          const shake = this.trauma * this.trauma
    
          // Perlin noise for smooth shake
          const offsetX = this.maxOffset * shake * noise(time * 20)
          const offsetY = this.maxOffset * shake * noise(time * 20 + 100)
          const rotation = this.maxRotation * shake * noise(time * 20 + 200)
    
          camera.offset.x = offsetX
          camera.offset.y = offsetY
          camera.rotation = rotation
    
          // Decay trauma
          this.trauma *= this.decayRate
          if (this.trauma < 0.01) this.trauma = 0
        }
      }
    }
    
    // Directional shake - punch in attack direction
    function directionalShake(direction: Vector2, power: number) {
      // Initial push in hit direction
      camera.offset.x += direction.x * power * 0.5
      camera.offset.y += direction.y * power * 0.5
    
      // Then normal trauma shake
      screenShake.addTrauma(power)
    }
    
    // TRAUMA VALUES BY ATTACK TYPE
    const SHAKE_VALUES = {
      lightAttack: 0.15,
      mediumAttack: 0.3,
      heavyAttack: 0.5,
      criticalHit: 0.7,
      finisher: 1.0,
    
      // Environmental
      landing: 0.1,
      explosion: 0.8,
      bossSlam: 0.9
    }
    
    // IMPORTANT: Shake during hitstop
    // Shake happens WHILE frozen, not after
    // This is when impact registers
    

---
  #### **Name**
Invincibility Frames (I-Frames)
  #### **Description**
Periods where player cannot be hit
  #### **When**
Implementing dodges, rolls, backsteps
  #### **Why**
I-frames reward timing and create strategic depth
  #### **Example**
    // I-FRAMES - The soul of defensive combat
    //
    // Dodge/roll i-frames create risk/reward:
    // - Too many: Dodge spam trivializes combat
    // - Too few: Dodging feels useless
    // - Timed right: Rewards mastery
    //
    // Reference values (at 60fps):
    //
    // Dark Souls roll: ~13 i-frames in 30-frame roll
    // Bloodborne dodge: ~10 i-frames in 26-frame quickstep
    // DMC5 dodge: ~8 i-frames, but very responsive
    // Sekiro deflect: Frame-perfect with generous window
    
    class DodgeSystem {
      state: 'ready' | 'startup' | 'iframes' | 'recovery' = 'ready'
      stateFrame: number = 0
    
      dodgeData = {
        startup: 2,      // Vulnerable startup
        iframes: 12,     // Invincible period
        recovery: 8,     // Vulnerable recovery
        cooldown: 6      // Before can dodge again
      }
    
      startDodge(direction: Vector2) {
        this.state = 'startup'
        this.stateFrame = 0
        this.direction = direction
      }
    
      update() {
        this.stateFrame++
    
        switch (this.state) {
          case 'startup':
            if (this.stateFrame >= this.dodgeData.startup) {
              this.state = 'iframes'
              this.stateFrame = 0
            }
            break
    
          case 'iframes':
            if (this.stateFrame >= this.dodgeData.iframes) {
              this.state = 'recovery'
              this.stateFrame = 0
            }
            break
    
          case 'recovery':
            if (this.stateFrame >= this.dodgeData.recovery) {
              this.state = 'ready'
            }
            break
        }
      }
    
      isInvincible(): boolean {
        return this.state === 'iframes'
      }
    
      canDodge(): boolean {
        return this.state === 'ready'
      }
    }
    
    // ADVANCED: Variable i-frames based on timing
    // Reward players who dodge INTO attacks
    function calculateIframes(dodgeDirection, attackDirection) {
      const dot = dodgeDirection.dot(attackDirection)
    
      // Dodging into attack: More i-frames
      if (dot > 0.7) return 15
      // Neutral dodge: Standard i-frames
      if (dot > -0.3) return 12
      // Dodging away: Fewer i-frames
      return 8
    }
    
    // PARRY WINDOWS (even more demanding)
    // Perfect parry: 3-6 frames (50-100ms)
    // Generous parry: 8-12 frames (133-200ms)
    //
    // Parry is high risk, high reward
    // Failed parry often means taking hit
    

---
  #### **Name**
Attack Cancel Windows
  #### **Description**
When attacks can be interrupted into other actions
  #### **When**
Building combo systems or responsive combat
  #### **Why**
Cancels create depth through player expression and mix-ups
  #### **Example**
    // CANCEL WINDOWS - The grammar of combo systems
    //
    // Cancel types (in order of commitment):
    // 1. Normal -> Normal (attack chains)
    // 2. Normal -> Special (combo extensions)
    // 3. Any -> Dodge (escape option)
    // 4. Any -> Super (resource-gated escape)
    //
    // Fighting game notation:
    // Startup -> Active -> Recovery
    // Cancels happen during Active or early Recovery
    
    class AttackData {
      frames = {
        startup: 5,
        active: 3,
        recovery: 12
      }
    
      cancelWindows = {
        // Frame ranges where cancels are allowed
        normalCancel: { start: 8, end: 16 },    // Cancel into next normal
        specialCancel: { start: 6, end: 18 },   // Cancel into special
        jumpCancel: { start: 10, end: 20 },     // Cancel into jump
        dodgeCancel: { start: 5, end: 15 }      // Cancel into dodge
      }
    
      // On-hit only cancels (reward landing the hit)
      onHitCancels = {
        launcher: { start: 8, end: 12 },        // Only if hit confirmed
        finisher: { start: 10, end: 14 }
      }
    }
    
    class ComboSystem {
      currentAttack: AttackData | null = null
      attackFrame: number = 0
      hitConfirmed: boolean = false
    
      canCancelInto(cancelType: string): boolean {
        if (!this.currentAttack) return false
    
        const window = this.currentAttack.cancelWindows[cancelType]
        if (!window) return false
    
        return this.attackFrame >= window.start &&
               this.attackFrame <= window.end
      }
    
      canCancelOnHit(cancelType: string): boolean {
        if (!this.hitConfirmed) return false
    
        const window = this.currentAttack.onHitCancels[cancelType]
        if (!window) return false
    
        return this.attackFrame >= window.start &&
               this.attackFrame <= window.end
      }
    }
    
    // DMC-STYLE COMBO SYSTEM
    // Chain hierarchy: Normal < Special < Super
    // Each level cancels the one below
    // Creates the "triangle" of options
    
    // SOULS-LIKE COMMITMENT
    // Minimal cancels - recovery is punishable
    // Only dodge cancel, and it costs stamina
    // Creates deliberate, tactical combat
    
    // PLATINUM STYLE
    // Liberal cancels but with "just frame" bonuses
    // Dodge Offset: Hold attack, dodge, release to continue combo
    // Creates expression through execution
    

---
  #### **Name**
Enemy Archetype System
  #### **Description**
Design enemies with clear combat roles
  #### **When**
Populating a game with varied combat encounters
  #### **Why**
Archetypes create encounter variety without exponential design work
  #### **Example**
    // THE FUNDAMENTAL ENEMY ARCHETYPES
    //
    // 1. FODDER/GRUNT
    // - Low HP, low damage
    // - Simple attack patterns (1-2 attacks)
    // - Short telegraphs
    // - Purpose: Warm-up, combo building, group pressure
    
    const GRUNT = {
      hp: 30,
      damage: 10,
      attacks: [
        { name: 'slash', startup: 15, active: 5, recovery: 20 }
      ],
      behavior: 'approach_and_swing',
      stagger: 'on_any_hit'
    }
    
    // 2. RANGED
    // - Low-medium HP
    // - Attacks from distance
    // - Forces player movement
    // - Purpose: Area denial, pressure during melee
    
    const RANGED = {
      hp: 25,
      damage: 15,
      preferredDistance: 10,
      attacks: [
        { name: 'projectile', startup: 20, active: 1, recovery: 30 }
      ],
      behavior: 'maintain_distance_and_fire',
      stagger: 'on_any_hit'
    }
    
    // 3. TANK/ARMORED
    // - High HP, high poise
    // - Slow but dangerous attacks
    // - Long recovery windows
    // - Purpose: Teaches patience, punish timing
    
    const TANK = {
      hp: 150,
      damage: 40,
      poise: 50,  // Takes 50 damage before stagger
      attacks: [
        { name: 'overhead_slam', startup: 40, active: 8, recovery: 60 }
      ],
      behavior: 'approach_slowly_attack_when_close',
      stagger: 'only_when_poise_broken'
    }
    
    // 4. AGILE/ASSASSIN
    // - Low HP, high damage
    // - Fast attacks, short openings
    // - Dodges/teleports
    // - Purpose: Teaches aggression, don't let them breathe
    
    const ASSASSIN = {
      hp: 40,
      damage: 35,
      attacks: [
        { name: 'quick_slash', startup: 8, active: 3, recovery: 15 },
        { name: 'backstab', startup: 25, active: 5, recovery: 10 }
      ],
      behavior: 'circle_and_strike_dodge_often',
      stagger: 'on_any_hit_brief'
    }
    
    // 5. ELITE/MINIBOSS
    // - High HP, varied moveset
    // - Multiple attack phases
    // - Tests everything player has learned
    // - Purpose: Skill check, gatekeeper
    
    const ELITE = {
      hp: 300,
      phases: [
        { threshold: 1.0, moveset: ['combo_a', 'ranged_attack'] },
        { threshold: 0.5, moveset: ['combo_a', 'combo_b', 'grab'] },
        { threshold: 0.25, moveset: ['enraged_combo', 'aoe_attack'] }
      ]
    }
    
    // ENCOUNTER DESIGN FORMULA
    // Start: 2-3 grunts (warmup)
    // Build: Add ranged enemy (positioning)
    // Tension: Add tank OR assassin (focus target)
    // Peak: Mixed group OR elite
    // Breather: Few grunts, resources
    

---
  #### **Name**
Attack Telegraph System
  #### **Description**
Visual and audio cues that warn of incoming attacks
  #### **When**
Designing enemy attacks players must react to
  #### **Why**
Telegraphs make combat about skill, not memorization or luck
  #### **Example**
    // TELEGRAPH HIERARCHY
    // Every attack needs multiple layers of warning
    //
    // 1. STANCE/POSTURE (earliest warning)
    // 2. WIND-UP ANIMATION (primary tell)
    // 3. VFX INDICATORS (reinforcement)
    // 4. AUDIO CUE (accessibility, off-screen)
    
    class AttackTelegraph {
      // Telegraph timing relative to attack
      phases = {
        stance: -30,      // 30 frames before wind-up
        windUp: -20,      // 20 frames of wind-up animation
        vfxWarn: -15,     // VFX starts 15 frames before hit
        audioWarn: -12,   // Audio cue 12 frames before hit
        attack: 0         // Hit frame
      }
    
      // VFX indicators by attack type
      vfxIndicators = {
        melee: 'weapon_glow',
        slam: 'ground_target_circle',
        projectile: 'charge_particles',
        grab: 'grab_range_indicator',
        aoe: 'danger_zone_fill'
      }
    }
    
    // TELEGRAPH DURATION BY DIFFICULTY
    // The same attack can feel fair or unfair based on telegraph time
    
    const TELEGRAPH_SCALING = {
      // Human reaction time: ~200-300ms (12-18 frames at 60fps)
    
      easy: {
        fastAttack: 24,   // 400ms - comfortable reaction
        mediumAttack: 36, // 600ms - leisurely
        heavyAttack: 60   // 1000ms - obvious
      },
      normal: {
        fastAttack: 18,   // 300ms - reactable for most
        mediumAttack: 28, // 467ms - comfortable
        heavyAttack: 45   // 750ms - clear
      },
      hard: {
        fastAttack: 12,   // 200ms - at reaction limit
        mediumAttack: 20, // 333ms - requires attention
        heavyAttack: 35   // 583ms - standard
      },
      expert: {
        fastAttack: 8,    // 133ms - prediction required
        mediumAttack: 15, // 250ms - tight reaction
        heavyAttack: 25   // 417ms - punishing
      }
    }
    
    // ATTACK TELLS - What makes a good telegraph
    //
    // GOOD TELEGRAPH:
    // - Distinct silhouette from other animations
    // - Clear direction of incoming attack
    // - Consistent timing (same wind-up = same timing)
    // - Audio reinforcement
    //
    // BAD TELEGRAPH:
    // - Looks similar to non-threatening animation
    // - Variable timing (sometimes fast, sometimes slow)
    // - No audio (off-screen attacks feel unfair)
    // - Too subtle (only visible if you already know it)
    
    // FROM SOFTWARE EXAMPLE:
    // Margit's dagger throw has explicit wind-up
    // Changes stance, pulls arm back, pauses, throws
    // Even first-time players can see it coming
    // But timing is tight enough to punish bad dodges
    

---
  #### **Name**
Damage Feedback Hierarchy
  #### **Description**
Layered feedback that communicates damage magnitude
  #### **When**
Hits need to communicate impact level
  #### **Why**
Players need to understand if attacks are effective
  #### **Example**
    // FEEDBACK LAYERS (all should scale with damage)
    //
    // 1. HITSTOP (timing)
    // 2. SCREEN SHAKE (camera)
    // 3. HIT VFX (particles)
    // 4. HIT SFX (audio)
    // 5. ANIMATION (target reaction)
    // 6. HAPTICS (controller rumble)
    // 7. UI (damage numbers, health bar)
    
    class DamageFeedbackSystem {
      applyFeedback(damage: number, isCritical: boolean, position: Vector2) {
        // Normalize damage to 0-1 for scaling
        const intensity = Math.min(damage / 100, 1)
    
        // 1. HITSTOP - Most important
        const hitstopFrames = this.calculateHitstop(intensity, isCritical)
        hitstopManager.apply(hitstopFrames)
    
        // 2. SCREEN SHAKE
        screenShake.addTrauma(intensity * (isCritical ? 1.5 : 1))
    
        // 3. HIT VFX
        const vfxScale = 0.5 + intensity * 0.5
        const vfxType = isCritical ? 'critical_hit' : 'normal_hit'
        vfxSystem.spawn(vfxType, position, vfxScale)
    
        // 4. HIT SFX
        const sfxType = this.selectHitSound(intensity, isCritical)
        audioManager.play(sfxType, position)
    
        // 5. HAPTICS
        const rumbleIntensity = intensity * (isCritical ? 1.0 : 0.6)
        haptics.rumble(rumbleIntensity, hitstopFrames / 60)
    
        // 6. UI
        if (showDamageNumbers) {
          ui.spawnDamageNumber(damage, position, isCritical)
        }
      }
    
      calculateHitstop(intensity: number, critical: boolean): number {
        // Light hit: 3-5 frames
        // Heavy hit: 10-15 frames
        // Critical: 1.5x multiplier
        const base = 3 + Math.round(intensity * 12)
        return critical ? Math.round(base * 1.5) : base
      }
    
      selectHitSound(intensity: number, critical: boolean): string {
        if (critical) return 'hit_critical'
        if (intensity > 0.7) return 'hit_heavy'
        if (intensity > 0.3) return 'hit_medium'
        return 'hit_light'
      }
    }
    
    // CRITICAL HIT SPECIAL TREATMENT
    // Critical hits should feel EXCEPTIONAL:
    // - Longer hitstop (1.5-2x)
    // - Unique audio sting
    // - Distinct VFX (different color, more particles)
    // - Slow-motion optional (for finishers)
    // - UI fanfare (flash, scale)
    
    // OVERKILL FEEDBACK
    // When enemy dies, scale feedback to remaining damage
    // Makes "just enough" feel different from "overwhelming power"
    
    function applyKillingBlow(target, damage, overkillAmount) {
      const overkillRatio = overkillAmount / target.maxHp
    
      // Overkill = bigger explosion
      if (overkillRatio > 0.5) {
        vfx.spawn('death_explosion_large', target.position)
        screenShake.addTrauma(0.8)
        timeScale.pulse(0.1, 200)  // Slow-mo pulse
      } else {
        vfx.spawn('death_explosion_normal', target.position)
        screenShake.addTrauma(0.4)
      }
    }
    

---
  #### **Name**
Recovery and Punishment Windows
  #### **Description**
Frame-data driven openings after attacks
  #### **When**
Combat needs risk/reward depth
  #### **Why**
Recovery windows create strategy; attacks have consequences
  #### **Example**
    // RECOVERY FRAMES - Where strategy lives
    //
    // Every attack should have a period of vulnerability after
    // This is the "cost" of swinging
    //
    // Formula: Power = Startup + Active + Recovery
    // Stronger attacks = longer total commitment
    
    class AttackFrameData {
      // Light attack: Quick but weak
      lightAttack = {
        startup: 5,     // Fast to come out
        active: 3,      // Brief hitbox
        recovery: 10,   // Short vulnerability
        total: 18,      // 300ms commitment
        onBlock: -4     // Slight disadvantage if blocked
      }
    
      // Heavy attack: Strong but risky
      heavyAttack = {
        startup: 15,    // Telegraphed
        active: 5,      // Extended hitbox
        recovery: 25,   // Long vulnerability
        total: 45,      // 750ms commitment
        onBlock: -15    // Very punishable if blocked
      }
    
      // Special attack: High risk/reward
      specialAttack = {
        startup: 20,
        active: 8,
        recovery: 30,   // Whiff = death sentence
        total: 58,      // Almost 1 second
        onBlock: -20    // Free punish if blocked
      }
    }
    
    // FRAME ADVANTAGE/DISADVANTAGE
    // The currency of fighting game strategy
    //
    // Positive (+) = You recover first, can act
    // Neutral (0) = Equal, reset to neutral
    // Negative (-) = Opponent recovers first
    //
    // Example: Your move is -5 on block
    // Enemy blocks, they can act 5 frames before you
    // If they have a 5-frame startup attack = guaranteed
    
    function calculateFrameAdvantage(
      attackerRecovery: number,
      targetBlockstun: number
    ): number {
      // Positive = attacker advantage
      // Negative = defender advantage
      return targetBlockstun - attackerRecovery
    }
    
    // ENEMY RECOVERY WINDOWS
    // This is where bosses feel fair or unfair
    //
    // Fair boss: Long recovery after big attacks
    // Unfair boss: Instantly can attack again
    
    const BOSS_ATTACK_EXAMPLE = {
      name: 'overhead_slam',
      startup: 45,         // Long wind-up, very readable
      active: 10,          // Extended danger zone
      recovery: 60,        // ONE SECOND of vulnerability
      // This is the "hit me" window
      // Player learns: Dodge, then punish
    
      punishWindow: {
        frames: 60,        // 1 second
        playerAttackStartup: 15,  // Player's attack
        maxPunishHits: 2   // Can get 2 hits in safely
      }
    }
    
    // RULE OF THUMB:
    // Recovery frames should be >= player's fastest punish option
    // Otherwise the "opening" isn't really an opening
    

---
  #### **Name**
Stamina and Resource Management
  #### **Description**
Action economy that creates strategic decisions
  #### **When**
Combat needs pacing and decision-making
  #### **Why**
Resources prevent spam and create risk/reward
  #### **Example**
    // STAMINA SYSTEM (Souls-like)
    //
    // Every action costs stamina
    // Creates strategic decisions:
    // - Do I attack or save stamina for dodge?
    // - Do I block this or roll?
    // - Can I afford another swing?
    
    class StaminaSystem {
      current: number = 100
      max: number = 100
    
      costs = {
        lightAttack: 15,
        heavyAttack: 30,
        roll: 20,
        sprint: 5,    // Per second
        block: 0      // But regen paused while blocking
      }
    
      recovery = {
        rate: 30,           // Per second
        delayAfterAction: 0.5,  // Seconds before regen starts
        blockingPenalty: 0.5,   // 50% regen while blocking
        emptyPenalty: 1.5       // Extra delay when depleted
      }
    
      lastActionTime: number = 0
    
      canAfford(action: string): boolean {
        return this.current >= this.costs[action]
      }
    
      spend(action: string): boolean {
        if (!this.canAfford(action)) return false
    
        this.current -= this.costs[action]
        this.lastActionTime = time.now()
    
        return true
      }
    
      update(delta: number) {
        // Check regen delay
        const timeSinceAction = time.now() - this.lastActionTime
        const delay = this.current <= 0
          ? this.recovery.emptyPenalty
          : this.recovery.delayAfterAction
    
        if (timeSinceAction < delay) return
    
        // Apply regen
        let regenRate = this.recovery.rate
        if (this.isBlocking) regenRate *= this.recovery.blockingPenalty
    
        this.current = Math.min(this.max, this.current + regenRate * delta)
      }
    }
    
    // BLOCK STAMINA (different from action stamina)
    // Taking hits while blocking drains stamina
    // Block broken = staggered, vulnerable
    
    function onBlockedAttack(damage: number) {
      const staminaDrain = damage * 0.5
      stamina.current -= staminaDrain
    
      if (stamina.current <= 0) {
        // Guard break!
        player.stagger(60)  // 1 second stun
        vfx.spawn('guard_break')
        sfx.play('guard_break')
      }
    }
    
    // POISE/POSTURE SYSTEM (Sekiro-style)
    // Taking hits builds "posture damage"
    // Full posture = vulnerable to critical
    // Creates aggressive play incentive
    
    class PostureSystem {
      current: number = 0  // Starts empty
      max: number = 100
      recoveryRate: number = 5  // Per second
    
      takeDamage(damage: number, isBlocked: boolean) {
        // Blocked attacks deal more posture damage
        const multiplier = isBlocked ? 1.5 : 1.0
        this.current += damage * multiplier
    
        if (this.current >= this.max) {
          this.triggerPostureBreak()
        }
      }
    
      triggerPostureBreak() {
        // Open for deathblow/critical
        owner.enterVulnerableState(120)  // 2 seconds
        vfx.spawn('posture_break')
        sfx.play('posture_break')
        this.current = 0
      }
    }
    

## Anti-Patterns


---
  #### **Name**
Invisible Hitboxes
  #### **Description**
Hitboxes that don't match visual attacks
  #### **Why**
Players die to attacks that visually missed; feels unfair and random
  #### **Instead**
    Make hitboxes LARGER than visuals, not smaller.
    If an attack looks like it should hit, it should hit.
    Test with hitbox visualization enabled.
    
    // Debug visualization is mandatory during development
    function renderHitboxDebug() {
      for (const hitbox of activeHitboxes) {
        drawWireframe(hitbox, COLOR_RED)
      }
      for (const hurtbox of allHurtboxes) {
        drawWireframe(hurtbox, COLOR_GREEN)
      }
    }
    

---
  #### **Name**
Unreadable Attack Tells
  #### **Description**
Enemy attacks with no clear warning
  #### **Why**
Players can't react to what they can't see; memorization replaces skill
  #### **Instead**
    Every attack needs telegraph time >= human reaction time (~250ms).
    Fast attacks are fine IF telegraphed by stance/behavior.
    Add audio cues for attacks - accessibility and fairness.
    
    Rule of thumb: If playtesters say "I didn't see that coming"
    more than 10% of the time, the telegraph is too subtle.
    

---
  #### **Name**
No Recovery Windows
  #### **Description**
Enemies that can attack again immediately after attacking
  #### **Why**
No punishment opportunity means no strategy; just dodge forever
  #### **Instead**
    Every attack should have a clear window where the enemy is vulnerable.
    Recovery >= player's fastest punish.
    If unsure, make recovery too long then tune shorter.
    
    // Boss attack formula:
    // Big wind-up (readable) + Extended recovery (punishable) = Fair
    // Quick attack + Instant followup = Frustrating
    

---
  #### **Name**
Damage Sponges
  #### **Description**
Enemies with massive HP but simple patterns
  #### **Why**
Long fights without variety are boring; repetition without depth
  #### **Instead**
    Reduce HP, add phases or new attacks.
    If a fight lasts > 3 minutes, it needs phase transitions.
    Interesting fights are about adaptation, not endurance.
    
    // Instead of:
    bossHP = 5000
    attackPattern = [attack1, attack2, attack1, attack2...]
    
    // Do:
    bossHP = 2000
    phases = [
      { threshold: 1.0, attacks: [attack1, attack2] },
      { threshold: 0.5, attacks: [attack1, attack2, attack3, newMechanic] },
      { threshold: 0.25, attacks: [enragedCombo, desperationMove] }
    ]
    

---
  #### **Name**
Input Delay Ignoring
  #### **Description**
Not accounting for input-to-action delay
  #### **Why**
Combat feels sluggish; players blame the game, not themselves
  #### **Instead**
    Measure total input latency: Input -> Action visible on screen.
    Target: < 100ms for responsive games, < 66ms for fighting games.
    Compensate for platform (TV game mode, wireless controllers).
    
    // Common sources of delay:
    // - Controller polling (8-16ms wireless)
    // - Input processing (1 frame = 16.67ms)
    // - Animation blend time (variable)
    // - Display lag (16-60ms on TVs)
    //
    // Total can easily reach 100-200ms if not careful
    

---
  #### **Name**
Cancel Everything Always
  #### **Description**
Every attack can cancel into any other action at any time
  #### **Why**
No commitment means no risk; combat becomes mash-fest
  #### **Instead**
    Cancels should be strategic choices, not universal escapes.
    Design cancel hierarchies: Normal < Special < Super.
    Some attacks SHOULD be committal - that's where reads happen.
    
    // Good cancel design:
    // Early frames: Can cancel into dodge (escape option)
    // Active frames: Committed (risk)
    // Late recovery: Can cancel into combo followup (reward for hit)
    

---
  #### **Name**
Inconsistent Frame Data
  #### **Description**
Same-looking attacks with different timings
  #### **Why**
Players can't build reliable muscle memory; reactions feel random
  #### **Instead**
    Visual similarity should mean timing similarity.
    If two attacks look the same, they should have same frame data.
    Exceptions must have clear visual distinction.
    
    // Enemy has "quick slash" and "delayed slash"
    // BAD: Both use same animation at different speeds
    // GOOD: Delayed slash has distinct wind-up pose and effect
    

---
  #### **Name**
Perfect Play Required
  #### **Description**
Combat that only works if player never makes mistakes
  #### **Why**
Most players will give up; only 1% finish your game
  #### **Instead**
    Design for "good enough" play, not perfect play.
    Recovery from mistakes should be possible (healing, distance, etc).
    Difficulty comes from consistency over time, not single execution tests.
    
    // Dark Souls works because:
    // Individual mistakes are recoverable (heal, back off)
    // Difficulty is cumulative (resource management over time)
    // Victory requires consistency, not perfection
    