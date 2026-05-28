# Real-Time VFX Artist

## Patterns


---
  #### **Name**
Shape-Timing-Color Framework
  #### **Description**
The foundational framework for creating readable, satisfying effects
  #### **When**
Designing any new visual effect
  #### **Why**
Ensures effects communicate clearly and feel physically grounded
  #### **Example**
    // The STC Framework for a sword slash effect:
    
    // 1. SHAPE - The silhouette tells the story
    // - Arc trajectory matches swing animation
    // - Width tapers from handle to tip
    // - Sharp leading edge, soft trailing edge
    // - Reads as a single swoosh, not noise
    
    // 2. TIMING - Physics sold through animation
    // - Anticipation: 0-3 frames, scale up from 0
    // - Main action: 3-6 frames, full arc travel
    // - Follow-through: 6-12 frames, fade while stretching
    // - Total: ~12 frames at 60fps = 200ms
    // - Use ease-out for deceleration feel
    
    // 3. COLOR - Readability and hierarchy
    // - Core: Pure white (255,255,255) - highest value
    // - Mid: Saturated hue (weapon element color)
    // - Edge: Dark outline or complementary color
    // - Additive blending for the core, alpha for edges
    // - Test on dark AND light backgrounds
    

---
  #### **Name**
Anticipation-Action-Follow Through
  #### **Description**
Disney's 12 principles applied to VFX timing
  #### **When**
Any effect that needs to feel impactful
  #### **Why**
Human perception requires setup and payoff for satisfaction
  #### **Example**
    // Explosion timing breakdown (60fps):
    
    // ANTICIPATION (frames 0-4): ~67ms
    // - Bright core flash, small scale
    // - Slight inward pull (optional)
    // - Player's brain registers "something is about to happen"
    
    // ACTION (frames 4-8): ~67ms
    // - Rapid expansion, max brightness
    // - Primary debris spawn
    // - Screen shake peaks
    // - This is where the "hit" registers
    
    // FOLLOW-THROUGH (frames 8-60+): ~1000ms+
    // - Smoke billows outward (slower than initial burst)
    // - Embers drift with gravity
    // - Light fades logarithmically, not linearly
    // - Secondary debris falls
    // - This sells the aftermath
    
    // The ratio matters: ~10% anticipation, 10% action, 80% follow-through
    // Cutting follow-through short makes effects feel "cheap"
    

---
  #### **Name**
Secondary Motion System
  #### **Description**
Particles spawning particles for organic complexity
  #### **When**
Effects feel too simple or mechanical
  #### **Why**
Real phenomena have cascading reactions - fire spawns smoke spawns embers
  #### **Example**
    // Niagara: Fire with smoke and embers
    // Three emitter system with spawn-from-source
    
    // EMITTER 1: Core Fire (primary)
    // - Spawn rate: 30/sec
    // - Lifetime: 0.3-0.5 sec
    // - Color: Orange -> Red -> Black
    // - Additive blending
    
    // EMITTER 2: Smoke (secondary from fire)
    // - Spawn from Emitter 1 particle death location
    // - Inherit 50% parent velocity
    // - Lifetime: 2-4 sec (much longer)
    // - Color: Dark gray, low alpha
    // - Alpha blending
    // - Add turbulence noise
    
    // EMITTER 3: Embers (tertiary)
    // - Burst spawn on fire particle death
    // - 1-3 embers per fire particle
    // - Strong initial velocity upward
    // - Gravity pulls down over time
    // - Color: Bright orange -> fade
    // - Additive, small size
    
    // This creates a living system from simple rules
    

---
  #### **Name**
Soft Particles for Intersection
  #### **Description**
Depth-based fade to avoid hard clipping against geometry
  #### **When**
Particles intersect world geometry
  #### **Why**
Hard particle/geometry intersection looks broken and cheap
  #### **Example**
    // GLSL/HLSL soft particle implementation:
    
    // 1. Sample scene depth at particle pixel
    float sceneDepth = LinearEyeDepth(depthTexture.Sample(uv));
    
    // 2. Get particle's depth
    float particleDepth = input.projectedPosition.w;
    
    // 3. Calculate fade based on depth difference
    float depthDifference = sceneDepth - particleDepth;
    float softFade = saturate(depthDifference / _SoftParticleDistance);
    
    // 4. Apply fade to alpha
    // _SoftParticleDistance: 0.5-2.0 units typical
    output.a *= softFade;
    
    // CRITICAL: This requires depth texture access
    // - Unity: Enable depth texture in camera/pipeline
    // - Unreal: Use SceneDepth node in material
    // - Godot: DEPTH_TEXTURE in shader
    
    // PERFORMANCE: One extra texture sample per particle pixel
    // Worth it for quality, but disable on low-end
    

---
  #### **Name**
Flipbook Motion Blur
  #### **Description**
Texture animation with proper inter-frame blending
  #### **When**
Using sprite sheet animations for effects
  #### **Why**
Hard frame cuts look choppy; smooth blending feels fluid
  #### **Example**
    // Flipbook with inter-frame blend (shader approach):
    
    uniform float _Time;
    uniform float _FPS;          // e.g., 30
    uniform int _Columns;        // e.g., 8
    uniform int _Rows;           // e.g., 8
    uniform float _TotalFrames;  // e.g., 64
    
    void main() {
      // Current time in frames
      float frameTime = _Time * _FPS;
    
      // Two adjacent frames
      float frame1 = floor(frameTime);
      float frame2 = frame1 + 1.0;
      float blend = fract(frameTime);
    
      // Loop the animation
      frame1 = mod(frame1, _TotalFrames);
      frame2 = mod(frame2, _TotalFrames);
    
      // Calculate UVs for each frame
      vec2 uv1 = GetFrameUV(frame1, uv, _Columns, _Rows);
      vec2 uv2 = GetFrameUV(frame2, uv, _Columns, _Rows);
    
      // Sample both frames
      vec4 color1 = texture(flipbookTex, uv1);
      vec4 color2 = texture(flipbookTex, uv2);
    
      // Blend between frames
      vec4 finalColor = mix(color1, color2, blend);
    
      // Optional: Apply curve to blend for smoother motion
      // blend = smoothstep(0.0, 1.0, blend);
    }
    
    // This doubles texture samples but eliminates stutter
    

---
  #### **Name**
Depth Fade for Volumetric Feel
  #### **Description**
Fading effects based on camera distance for atmospheric depth
  #### **When**
Effects need to feel like they exist in 3D space
  #### **Why**
Atmospheric perspective makes effects feel grounded in the world
  #### **Example**
    // Depth-based fade for fog/dust/atmosphere:
    
    // Calculate distance from camera
    float distanceFromCamera = length(worldPos - cameraPos);
    
    // Near fade: particles too close to camera
    float nearFade = smoothstep(_NearFadeStart, _NearFadeEnd, distanceFromCamera);
    
    // Far fade: particles disappearing into distance
    float farFade = 1.0 - smoothstep(_FarFadeStart, _FarFadeEnd, distanceFromCamera);
    
    // Combine fades
    float distanceFade = nearFade * farFade;
    
    // Apply to alpha
    output.a *= distanceFade;
    
    // Typical values:
    // _NearFadeStart: 0.0 (camera position)
    // _NearFadeEnd: 2.0 (2 meters from camera)
    // _FarFadeStart: 50.0
    // _FarFadeEnd: 100.0
    
    // Also fade SIZE with distance for perspective
    

---
  #### **Name**
Effect Layering Hierarchy
  #### **Description**
Composing complex effects from simple layers with clear hierarchy
  #### **When**
Creating any multi-element effect
  #### **Why**
Layered effects are easier to tune, debug, and optimize
  #### **Example**
    // Magic projectile - 5 layer hierarchy:
    
    // LAYER 1: CORE (highest priority, never cut)
    // - Solid bright center
    // - Additive blending
    // - Small, high value contrast
    // - Communicates: "this is the hitbox"
    
    // LAYER 2: INNER GLOW
    // - Soft falloff around core
    // - Same hue, lower saturation
    // - Subtle pulsing scale
    // - Communicates: "energy/power level"
    
    // LAYER 3: PARTICLE TRAIL
    // - Spawns from core position
    // - Inherits some velocity
    // - Fades over distance
    // - Communicates: "motion direction"
    
    // LAYER 4: DISTORTION (medium priority)
    // - Screen-space refraction
    // - Follows core loosely
    // - Very subtle - 2-5 pixel offset max
    // - Communicates: "bending reality"
    
    // LAYER 5: AMBIENT PARTICLES (lowest priority, cut first)
    // - Loose orbiting specs
    // - Random velocities
    // - First to disable on low-end
    // - Communicates: "magical nature"
    
    // LOD STRATEGY:
    // Ultra: All 5 layers
    // High: Layers 1-4 (cut ambient)
    // Medium: Layers 1-3 (cut distortion)
    // Low: Layers 1-2 only
    // Potato: Layer 1 only (never cut core!)
    

---
  #### **Name**
Looping Effect Seamless Transition
  #### **Description**
Creating perfectly looping effects without visible seams
  #### **When**
Any continuous effect (ambient particles, fire, energy shields)
  #### **Why**
Visible loop seams destroy immersion and look amateur
  #### **Example**
    // Three techniques for seamless loops:
    
    // 1. PING-PONG NOISE
    // Instead of: noise(time)
    // Use: noise(sin(time * PI * 2 / loopDuration))
    // The sine creates smooth reversal at loop point
    
    // 2. CROSSFADE SPAWN
    // As particles near end of loop duration:
    float loopProgress = fmod(particleAge, loopDuration) / loopDuration;
    float fadeOut = 1.0 - smoothstep(0.8, 1.0, loopProgress);
    float fadeIn = smoothstep(0.0, 0.2, loopProgress);
    // New particles fade in as old ones fade out
    
    // 3. OFFSET SPAWN GROUPS
    // Spawn particles in groups offset by 1/N of loop duration
    // Group A: spawns at t=0
    // Group B: spawns at t=loopDuration/3
    // Group C: spawns at t=loopDuration*2/3
    // Each group fades independently, always some visible
    
    // 4. FLIPBOOK LOOP CHECK
    // For texture animations:
    // - First frame and last frame must blend
    // - Export with "loop" option in DCC tool
    // - Test at 0.5x speed to catch seams
    
    // PRO TIP: Record effect, check frame 0 vs frame N
    // If they don't match, you have a seam
    

---
  #### **Name**
Value Contrast Priority
  #### **Description**
Designing effects that read in any lighting condition
  #### **When**
Effects must work across different environments
  #### **Why**
Color is unreliable for readability; value (brightness) is universal
  #### **Example**
    // The Value Hierarchy for a heal effect:
    
    // STEP 1: Design in grayscale FIRST
    // - Core pulse: 100% white
    // - Inner ring: 70% gray
    // - Outer glow: 40% gray
    // - Particles: 90% white (small, need to pop)
    
    // STEP 2: Add color only after values work
    // - Core: White (stays white for punch)
    // - Inner ring: Saturated green
    // - Outer glow: Desaturated green
    // - Particles: Light green/white
    
    // STEP 3: Test against problem backgrounds
    // - Test on white snow: effect still reads?
    // - Test on black cave: effect still reads?
    // - Test on green forest: not lost in environment?
    
    // DARK OUTLINE TECHNIQUE:
    // Add subtle dark edge to bright effects
    // Creates separation from any background
    // Just 1-2 pixels of darker hue around core
    
    // WHY THIS MATTERS:
    // A red effect on green reads (complementary)
    // A red effect on red is invisible (same hue)
    // High value contrast ALWAYS reads
    

---
  #### **Name**
GPU Particle Simulation
  #### **Description**
Leveraging GPU compute for massive particle counts
  #### **When**
Need thousands of particles without CPU bottleneck
  #### **Why**
CPU particles max at ~10K, GPU particles can do 1M+
  #### **Example**
    // VFX Graph (Unity) GPU particle structure:
    
    // 1. INITIALIZE CONTEXT
    // - Set capacity (e.g., 100,000 particles)
    // - Bounds for culling
    // - Initial attribute values
    
    // 2. UPDATE CONTEXT (runs on GPU every frame)
    // - Apply forces (gravity, turbulence)
    // - Update position: pos += velocity * dt
    // - Update attributes (size over life, color over life)
    // - Kill conditions (age > lifetime, outside bounds)
    
    // 3. OUTPUT CONTEXT
    // - Mesh type (billboard, mesh, strip)
    // - Material binding
    // - Sorting mode (affects performance!)
    
    // KEY PERFORMANCE NOTES:
    // - Capacity = memory allocated, not particle count
    // - Avoid Sort: Depth unless transparency requires
    // - Use Bounds aggressively for culling
    // - Strip particles (trails) are expensive - limit count
    
    // Niagara equivalent:
    // - Emitter: GPU Compute Sim
    // - System: Scalability settings per quality level
    // - Modules: Stack-based, order matters
    

---
  #### **Name**
Screen-Space Effect Integration
  #### **Description**
Combining particle effects with post-processing for cohesion
  #### **When**
Effects need to feel integrated with the rendered scene
  #### **Why**
Post-processing unifies all elements under same visual treatment
  #### **Example**
    // The post-process VFX integration stack:
    
    // 1. BLOOM FEEDING
    // - Effects should emit HDR values to trigger bloom
    // - Don't just use white; use values > 1.0
    // - Core of explosion: (10.0, 8.0, 5.0) in linear space
    // - Bloom picks this up and creates glow automatically
    
    // 2. DOF INTERACTION
    // - Particles should respect depth of field
    // - Enable "Receive DOF" on particle materials
    // - Or: Apply DOF in particle shader for custom control
    
    // 3. MOTION BLUR CONSIDERATION
    // - Fast particles may streak unpleasantly
    // - Option A: Disable motion blur for VFX layer
    // - Option B: Use stretched billboards instead of point sprites
    // - Option C: Pre-stretched flipbook with blur baked in
    
    // 4. COLOR GRADING AWARENESS
    // - Your "pure white" won't be white after grading
    // - Test effects WITH final color grading enabled
    // - Consider "hero" effects that bypass grading
    
    // 5. SCREEN DISTORTION LAYERING
    // - Distortion effects should stack properly
    // - Use normal maps, not screen-space offset directly
    // - Combine in single pass when possible
    
    // POST-FX ORDER MATTERS:
    // 1. Render particles
    // 2. Apply distortion
    // 3. Bloom extraction
    // 4. Motion blur
    // 5. DOF
    // 6. Color grading
    // 7. Final composite
    

---
  #### **Name**
Procedural Noise for Organic Motion
  #### **Description**
Using noise functions to break up mechanical patterns
  #### **When**
Particles look too uniform or computer-generated
  #### **Why**
Real phenomena have chaotic variation; noise simulates this
  #### **Example**
    // Noise application layers for organic fire:
    
    // 1. SPAWN POSITION NOISE
    // Offset spawn point with low-frequency noise
    float3 spawnOffset = noise3D(time * 0.5) * _SpawnRadius;
    // Creates wandering emission point
    
    // 2. VELOCITY NOISE (TURBULENCE)
    // Add turbulence force to particle velocity
    float3 turbulence = curlNoise(position * _TurbulenceScale);
    velocity += turbulence * _TurbulenceStrength;
    // Use CURL noise - divergence-free, realistic fluid motion
    
    // 3. SIZE/ALPHA VARIATION
    // Modulate size with noise over lifetime
    float sizeNoise = noise1D(particleID + time);
    size *= lerp(0.8, 1.2, sizeNoise);
    // Each particle pulses independently
    
    // 4. COLOR NOISE
    // Slight hue/saturation variation per particle
    float colorNoise = noise1D(particleID * 7.3);
    color = shiftHue(baseColor, colorNoise * 10.0); // +/- 10 degrees
    
    // NOISE FREQUENCY GUIDE:
    // - Position offset: 0.5-2 Hz (slow wander)
    // - Turbulence: 1-5 Hz (medium churning)
    // - Size pulse: 2-8 Hz (visible shimmer)
    // - Spawn timing: Variable (natural bursts)
    
    // CRITICAL: Use DIFFERENT noise seeds per attribute
    // Same noise on everything looks robotic
    

---
  #### **Name**
Performance Budget Framework
  #### **Description**
Structured approach to VFX performance allocation
  #### **When**
Planning VFX for a scene or game
  #### **Why**
Without budgets, VFX artists will tank frame rate
  #### **Example**
    // VFX PERFORMANCE BUDGET TEMPLATE
    
    // TOTAL FRAME BUDGET: 16.67ms (60fps)
    // VFX ALLOCATION: ~2ms (12% of frame)
    
    // BREAKDOWN:
    // - GPU Simulation: 0.5ms
    // - Particle Rendering: 0.8ms
    // - Post-processing VFX: 0.5ms
    // - Screen distortion: 0.2ms
    // - Buffer for spikes: remaining
    
    // PER-EFFECT LIMITS:
    // Tier 1 (Hero effects - boss death, ultimate):
    //   - Max 10,000 particles
    //   - Full shader complexity
    //   - Distortion + multiple layers
    //   - Expected: 0.3ms
    
    // Tier 2 (Combat effects - hits, abilities):
    //   - Max 500 particles
    //   - Simple shader
    //   - No distortion
    //   - Expected: 0.05ms each, budget for 10 concurrent
    
    // Tier 3 (Ambient - dust, leaves, fire):
    //   - Max 100 particles per emitter
    //   - Minimal shader
    //   - First to LOD out
    //   - Expected: 0.01ms each
    
    // OVERDRAW BUDGET:
    // Target: <4x average overdraw
    // Measure: GPU profiler overdraw visualization
    // Mobile: <2x overdraw
    
    // FILL RATE CALCULATION:
    // particles * avg_screen_coverage * shader_cost
    // Example: 1000 particles * 0.001 screen * 100 ALU = manageable
    // Example: 1000 particles * 0.01 screen * 100 ALU = problem!
    

## Anti-Patterns


---
  #### **Name**
Overdraw Overload
  #### **Description**
Stacking too many transparent particles causing massive fill rate cost
  #### **Why Bad**
Every pixel rendered multiple times multiplies GPU fragment work linearly
  #### **Fix**
    1. Reduce particle count, increase individual particle impact
    2. Use opaque particles with alpha testing where possible
    3. Sort and kill particles that would render behind others
    4. Use particle LOD based on camera distance
    5. Set hard limits in particle system settings
    
  #### **Severity**
critical

---
  #### **Name**
Additive Blending Abuse
  #### **Description**
Using additive blending for everything, causing washed-out effects
  #### **Why Bad**
Additive particles sum to white, lose color information, blow out HDR
  #### **Fix**
    Use additive for: cores, energy, light sources
    Use alpha blend for: smoke, dust, debris, anything with mass
    Use multiply/overlay for: shadows, stains
    Rule: If it blocks light, don't use additive
    
  #### **Severity**
high

---
  #### **Name**
Static Flipbook Timing
  #### **Description**
All particles playing flipbook at same speed and start frame
  #### **Why Bad**
Creates visible synchronization, looks artificial
  #### **Fix**
    1. Randomize start frame per particle
    2. Vary playback speed +/- 20%
    3. Consider particle age-based offset
    4. Use random lifetime to desync death frames
    
  #### **Severity**
medium

---
  #### **Name**
Ignoring Value Hierarchy
  #### **Description**
Creating effects purely based on color, ignoring brightness contrast
  #### **Why Bad**
Effects become unreadable on certain backgrounds, especially for colorblind players
  #### **Fix**
    Design in grayscale first. Core = brightest. Edges = darker.
    Test against white, black, and matching-hue backgrounds.
    Add dark outline for universal separation.
    
  #### **Severity**
high

---
  #### **Name**
Missing Anticipation
  #### **Description**
Effects that start at full intensity with no buildup
  #### **Why Bad**
Feels sudden and unsatisfying; player doesn't register the event
  #### **Fix**
    Add 2-4 frames of buildup before main effect.
    Scale from small to large, dim to bright.
    Audio cue should start before visual.
    
  #### **Severity**
medium

---
  #### **Name**
Symmetrical Particles
  #### **Description**
Using perfectly symmetrical textures for organic effects
  #### **Why Bad**
Bilateral symmetry reads as artificial; nature is asymmetric
  #### **Fix**
    Break symmetry in source textures.
    Rotate particles randomly.
    Use multiple texture variants.
    
  #### **Severity**
low

---
  #### **Name**
Fill Rate on Mobile
  #### **Description**
Desktop-quality effects destroying mobile performance
  #### **Why Bad**
Mobile GPU fill rate is 1/10th of desktop; effects that run fine on PC tank on phone
  #### **Fix**
    1. Maximum 2x overdraw on mobile
    2. Half particle counts at minimum
    3. Simpler shaders (no distortion, minimal sampling)
    4. Smaller particle sizes to reduce coverage
    5. Test on lowest-spec target device
    
  #### **Severity**
critical

---
  #### **Name**
Particle Sorting Always On
  #### **Description**
Forcing depth sort on all particle systems
  #### **Why Bad**
Sorting is O(n log n) per frame; thousands of particles = CPU spike
  #### **Fix**
    Only sort when transparency order matters.
    Use additive blending (order-independent).
    Limit sorted particle count.
    Consider depth-write with alpha test instead.
    
  #### **Severity**
high

---
  #### **Name**
No Effect LOD
  #### **Description**
Full-quality effects rendering regardless of distance or importance
  #### **Why Bad**
Distant effects wasting GPU cycles; effects during intense combat piling up
  #### **Fix**
    Implement quality tiers (Epic/High/Medium/Low/Off).
    Reduce particles with distance.
    Cull off-screen effects.
    Pool and recycle particle systems.
    
  #### **Severity**
high

---
  #### **Name**
Velocity Inheritance Without Damping
  #### **Description**
Particles inherit full parent velocity and maintain it forever
  #### **Why Bad**
Particles shoot away unnaturally fast and never settle
  #### **Fix**
    Use velocity inheritance with multiplier (0.3-0.7, not 1.0).
    Apply drag to dampen velocity over time.
    Consider initial burst vs sustained velocity.
    
  #### **Severity**
medium