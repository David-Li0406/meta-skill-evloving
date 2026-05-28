# Combat Design - Validations

## Combat Input Without Buffering

### **Id**
combat-no-input-buffer
### **Severity**
warning
### **Type**
regex
### **Pattern**
(justPressed|isJustPressed|GetButtonDown)\s*\([^)]*\)\s*(?!.*buffer)
### **Message**
Input check without buffering. Combat inputs should be buffered for responsiveness.
### **Fix Action**
Add input buffering: store input with timestamp, consume when action becomes possible
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd
  - *.cpp

## Frame-Critical Raw Input

### **Id**
combat-raw-input-timing
### **Severity**
warning
### **Type**
regex
### **Pattern**
if\s*\(\s*(Input|input)\.(justPressed|GetButtonDown|is_action_just_pressed)\s*\([^)]*\)\s*\)\s*\{
### **Message**
Raw input for combat action. Consider input buffering for frame-perfect actions.
### **Fix Action**
Buffer combat inputs: queue input, check buffer when action window opens
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Slow Animation Blend for Combat

### **Id**
combat-slow-blend-time
### **Severity**
warning
### **Type**
regex
### **Pattern**
(crossFade|CrossFade|blend_time|transitionDuration)\s*[=:(\s]+\s*0\.[2-9]
### **Message**
Slow animation blend (>= 0.2s) in potential combat context. Attack animations should blend in < 50ms.
### **Fix Action**
Use faster blend for combat: crossFade(anim, 0.033) for 2-frame transition
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Animation Without Damage Frame Event

### **Id**
combat-no-animation-event
### **Severity**
info
### **Type**
regex
### **Pattern**
(attackAnim|attack_anim|AttackAnimation)\s*[=:]\s*["'][^"']+["'](?!.*event|notify)
### **Message**
Attack animation reference without visible event/notify setup. Damage timing should use animation events.
### **Fix Action**
Add animation events for damage frames, sound triggers, and VFX spawning
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Hitbox Without Deactivation

### **Id**
combat-hitbox-always-active
### **Severity**
error
### **Type**
regex
### **Pattern**
(hitbox|Hitbox|hit_box)\.(enabled|active|SetActive)\s*[=(\s]+\s*true(?![^}]*false)
### **Message**
Hitbox enabled without corresponding disable. Hitboxes should only be active during attack's active frames.
### **Fix Action**
Disable hitbox after active frames: hitbox.enabled = false in recovery phase
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Hitbox Without Multi-Hit Prevention

### **Id**
combat-no-hitbox-reset
### **Severity**
warning
### **Type**
regex
### **Pattern**
class\s+Hitbox[^{]*\{(?![^}]*(hitEntities|alreadyHit|hitList|hit_entities))
### **Message**
Hitbox class without hit tracking. Same hitbox can hit same target multiple times per swing.
### **Fix Action**
Track hit entities per attack: Set<Entity> hitThisSwing, check before applying damage
### **Applies To**
  - *.ts
  - *.js
  - *.cs

## Damage Without Hitstop

### **Id**
combat-damage-no-hitstop
### **Severity**
warning
### **Type**
regex
### **Pattern**
(applyDamage|takeDamage|TakeDamage|deal_damage)\s*\([^)]*\)(?![^;{]*(?:hitstop|hitStop|freeze|Freeze|pause|Pause))
### **Message**
Damage dealt without hitstop/freeze frame. Hits may feel weightless.
### **Fix Action**
Add hitstop on hit: freeze both attacker and target for 3-15 frames based on damage
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Damage Without Screen Shake

### **Id**
combat-damage-no-screenshake
### **Severity**
info
### **Type**
regex
### **Pattern**
(applyDamage|takeDamage|TakeDamage|deal_damage)\s*\([^)]*\)(?![^;{]*(?:shake|Shake|trauma|Trauma|camera))
### **Message**
Damage dealt without camera shake. Consider adding screen shake for impact feedback.
### **Fix Action**
Add screen shake on hit: camera.addTrauma(damage / maxDamage)
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Combat Hit Without Visual Effect

### **Id**
combat-no-hit-vfx
### **Severity**
info
### **Type**
regex
### **Pattern**
(onHit|on_hit|OnHitConfirmed)\s*[=:(\s]+(?![^}]*(vfx|VFX|particle|Particle|effect|Effect|spawn))
### **Message**
Hit handler without VFX spawn. Visual feedback reinforces impact.
### **Fix Action**
Spawn hit particles at impact point scaled to damage
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Attack Without Recovery Definition

### **Id**
combat-no-recovery-frames
### **Severity**
warning
### **Type**
regex
### **Pattern**
attack(Data)?[=:\s]+\{[^}]*(startup|active)(?![^}]*recovery)
### **Message**
Attack data defines startup/active but not recovery frames. All attacks need recovery windows.
### **Fix Action**
Define recovery frames: period after active frames where attacker is vulnerable
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Hardcoded Frame Data Values

### **Id**
combat-magic-frame-numbers
### **Severity**
info
### **Type**
regex
### **Pattern**
(startup|active|recovery)\s*[=:]\s*\d+(?!\s*[/*])
### **Message**
Hardcoded frame data values. Consider using named constants or data-driven config.
### **Fix Action**
Use named constants: LIGHT_ATTACK_STARTUP = 5, or load from config file
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## I-Frame Without Duration Limit

### **Id**
combat-iframe-no-duration
### **Severity**
error
### **Type**
regex
### **Pattern**
(invincible|isInvincible|invulnerable)\s*=\s*true(?![^}]*(timer|duration|frames|setTimeout|yield))
### **Message**
Invincibility enabled without clear duration. I-frames should have explicit frame count.
### **Fix Action**
Set i-frame duration: this.iframeFrames = 12; disable when counter reaches 0
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Dodge Without I-Frame Implementation

### **Id**
combat-dodge-no-iframe
### **Severity**
warning
### **Type**
regex
### **Pattern**
(startDodge|dodge|roll|Roll)\s*\([^)]*\)\s*\{(?![^}]*(invincible|iframe|iFrame|invulnerable))
### **Message**
Dodge function without i-frame implementation. Dodges typically grant invincibility frames.
### **Fix Action**
Add i-frames to dodge: set invincible after startup, clear after i-frame window
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Combat Action Without Resource Cost

### **Id**
combat-action-no-cost
### **Severity**
info
### **Type**
regex
### **Pattern**
(attack|dodge|roll|heavyAttack)\s*\([^)]*\)\s*\{(?![^}]*(stamina|energy|cost|resource))
### **Message**
Combat action without resource cost. Consider stamina/energy costs for strategic depth.
### **Fix Action**
Add resource costs: if (!stamina.canAfford(DODGE_COST)) return; stamina.spend(DODGE_COST)
### **Applies To**
  - *.ts
  - *.js
  - *.cs

## Stamina With Immediate Regeneration

### **Id**
combat-stamina-instant-regen
### **Severity**
info
### **Type**
regex
### **Pattern**
stamina\s*\+=(?!.*delay|.*timer|.*after)
### **Message**
Stamina regenerating without delay. Consider delay after action before regen starts.
### **Fix Action**
Add regen delay: lastActionTime = now; only regen if (now - lastActionTime) > regenDelay
### **Applies To**
  - *.ts
  - *.js
  - *.cs

## Enemy Attack Without Startup

### **Id**
combat-enemy-instant-attack
### **Severity**
warning
### **Type**
regex
### **Pattern**
enemy(Attack)?[=:\s]+\{[^}]*damage(?![^}]*startup|telegraph)
### **Message**
Enemy attack data without startup/telegraph frames. Enemies need readable wind-ups.
### **Fix Action**
Add startup frames >= 12 (200ms) for reactable attacks, >= 24 for comfortable reactions
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Boss Without Phase System

### **Id**
combat-boss-no-phases
### **Severity**
info
### **Type**
regex
### **Pattern**
class\s+Boss[^{]*\{(?![^}]*(phase|Phase|state|State|threshold))
### **Message**
Boss class without visible phase system. Long boss fights need phase transitions for variety.
### **Fix Action**
Add phases: check HP thresholds, unlock new attacks, change behavior patterns
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Combo Without Input Window

### **Id**
combat-combo-no-window
### **Severity**
warning
### **Type**
regex
### **Pattern**
(comboNext|nextAttack|chainAttack)\s*(?!.*window|timer|frame)
### **Message**
Combo system without input window tracking. Combos need defined input windows.
### **Fix Action**
Add combo window: accept next input only during frames X-Y of current attack
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Cancel System Without Priority

### **Id**
combat-cancel-no-hierarchy
### **Severity**
info
### **Type**
regex
### **Pattern**
(canCancel|canInterrupt)\s*[=:\s]+(?!.*priority|hierarchy|level)
### **Message**
Cancel system without priority hierarchy. Cancels should follow: Normal < Special < Super.
### **Fix Action**
Implement cancel hierarchy: special cancels normal, super cancels special
### **Applies To**
  - *.ts
  - *.js
  - *.cs

## Combat Timing Without Delta Time

### **Id**
combat-frame-rate-dependent
### **Severity**
error
### **Type**
regex
### **Pattern**
(frameCount|frame_count)\s*[\+\-]=\s*1(?!.*delta|.*Time)
### **Message**
Frame counting without delta time consideration. Combat timing may vary with frame rate.
### **Fix Action**
Use fixed timestep for combat logic, or multiply by (targetFrameRate / actualFrameRate)
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Combat Logic Skipping Frames

### **Id**
combat-update-frame-skip
### **Severity**
warning
### **Type**
regex
### **Pattern**
(attackFrame|combatTimer)\s*\+=\s*(delta|deltaTime|Delta)(?!.*fixed|.*step)
### **Message**
Combat frame counter using raw delta time. Frame data may be inconsistent.
### **Fix Action**
Use fixed timestep: accumulator += delta; while (accumulator >= FIXED_STEP) {...}
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Jump Without Coyote Time

### **Id**
combat-no-coyote-time
### **Severity**
warning
### **Type**
regex
### **Pattern**
(canJump|CanJump)\s*[=:(\s]+\s*(isGrounded|is_on_floor|IsGrounded)(?!.*coyote|.*grace)
### **Message**
Jump check using only ground state. Add coyote time for forgiving platform combat.
### **Fix Action**
Track lastGroundedFrame; allow jump if (currentFrame - lastGroundedFrame) <= coyoteFrames
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Jump Without Input Buffering

### **Id**
combat-no-jump-buffer
### **Severity**
info
### **Type**
regex
### **Pattern**
if\s*\([^)]*jump[^)]*\)\s*\{[^}]*\}(?![^}]*buffer)
### **Message**
Jump input without buffering. Buffer jump presses before landing for responsiveness.
### **Fix Action**
Buffer jump input; on landing check if (jumpBuffer.hasBufferedInput()) jump()
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Expensive Collision Every Frame

### **Id**
combat-collision-every-frame
### **Severity**
warning
### **Type**
regex
### **Pattern**
(update|Update|_process)\s*\([^)]*\)\s*\{[^}]*(checkCollision|CheckCollision|overlap|Overlap)
### **Message**
Collision checking in update loop. May cause performance issues; only check when hitbox active.
### **Fix Action**
Only check collisions when hitbox is active, use collision layers, spatial partitioning
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Hitbox Without Once-Per-Swing Check

### **Id**
combat-no-hit-once-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
(onTriggerEnter|OnTriggerEnter|body_entered)\s*\([^)]*\)\s*\{(?![^}]*(already|hasHit|hitList|hitThisSwing))
### **Message**
Collision handler without hit-once check. Same hitbox may deal damage multiple times.
### **Fix Action**
Track hit entities: if (hitThisSwing.has(entity)) return; hitThisSwing.add(entity)
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Combat State Boolean Soup

### **Id**
combat-state-boolean-soup
### **Severity**
warning
### **Type**
regex
### **Pattern**
is(Attacking|Dodging|Blocking)[^&|]*&&[^&|]*is(Attacking|Dodging|Blocking)
### **Message**
Multiple boolean state checks. Use a state machine for combat states.
### **Fix Action**
Replace booleans with state enum: CombatState.ATTACKING, use switch statement
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Combat State Without Exit Handler

### **Id**
combat-no-exit-state
### **Severity**
info
### **Type**
regex
### **Pattern**
(enterState|onEnter|Enter)\s*\([^)]*\)\s*\{(?![^}]*(exit|Exit|leave|Leave))
### **Message**
State machine with enter but no exit handler. Clean up state on transitions.
### **Fix Action**
Add onExit handler: disable hitboxes, reset timers, restore movement
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd

## Lock-On Without Target Validation

### **Id**
combat-lockon-no-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
(lockOn|LockOn|lockedTarget)\s*=\s*[^;]+(?!.*valid|alive|exists|null)
### **Message**
Lock-on target set without validation. Target may be dead or out of range.
### **Fix Action**
Validate lock-on target each frame: if (!target.isAlive || distance > maxRange) unlock()
### **Applies To**
  - *.ts
  - *.js
  - *.cs
  - *.gd