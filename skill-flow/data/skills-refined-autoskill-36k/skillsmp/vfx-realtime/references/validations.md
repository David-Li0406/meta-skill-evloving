# Vfx Realtime - Validations

## Extreme Particle Spawn Rate

### **Id**
vfx-extreme-spawn-rate
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - SpawnRate\s*[=:]\s*[1-9]\d{3,}
  - spawn.*rate.*[=:]\s*[1-9]\d{3,}
  - emissionRate\s*[=:]\s*[1-9]\d{3,}
  - rateOverTime\s*[=:]\s*[1-9]\d{3,}
### **Message**
Spawn rate > 1000/sec will cause severe overdraw. Even with short lifetime, this creates performance issues.
### **Fix Action**
Reduce spawn rate to < 200/sec for most effects. Use larger, fewer particles with more impact each.
### **Applies To**
  - *.prefab
  - *.asset
  - *.uasset
  - *.vfx
  - *.tscn
  - *.tres
  - *.cs
  - *.cpp

## Missing Max Particles Limit

### **Id**
vfx-no-max-particles
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - maxParticles\s*[=:]\s*0(?!\d)
  - MaxParticles\s*[=:]\s*-1
  - capacity\s*[=:]\s*Infinity
  - unlimited.*particles
### **Message**
No max particle limit can cause memory exhaustion and frame drops during sustained effects.
### **Fix Action**
Set explicit MaxParticles limit. Tier 1 effects: 10000 max. Tier 2: 500. Tier 3: 100.
### **Applies To**
  - *.prefab
  - *.asset
  - *.uasset
  - *.vfx
  - *.tscn
  - *.cs
  - *.cpp

## Distortion Effect Without Mobile Guard

### **Id**
vfx-distortion-mobile
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - GrabPass|_GrabTexture
  - _CameraOpaqueTexture.*distort
  - Distortion.*mobile|distortion.*MOBILE
  - refraction|Refraction
### **Message**
Distortion effects require framebuffer read - catastrophic on mobile TBDR GPUs.
### **Fix Action**
Disable distortion on mobile platforms. Use alternative visual (glow, color shift) instead.
### **Applies To**
  - *.shader
  - *.shadergraph
  - *.vfx
  - *.material

## Unscaled Time in Gameplay Effect

### **Id**
vfx-unscaled-time-gameplay
### **Severity**
error
### **Type**
regex
### **Pattern**
  - Time\.unscaledTime
  - Time\.unscaledDeltaTime
  - getRealTimeSeconds
  - FApp::GetDeltaTime\(\)
### **Message**
Using unscaled/real time means effect won't respect slow-mo, pause, or hitstop.
### **Fix Action**
Use deltaTime (scaled) for gameplay VFX. Reserve unscaled time for UI effects only.
### **Applies To**
  - *.cs
  - *.cpp
  - *.gd
  - *.shader

## Additive Blending on Smoke/Dust

### **Id**
vfx-additive-smoke
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)smoke.*Blend\s*One\s*One
  - (?i)dust.*BlendMode.*Additive
  - (?i)cloud.*(?:additive|Add)
  - smoke.*blend.*add
### **Message**
Smoke/dust should use alpha blending, not additive. Additive makes occluding effects transparent.
### **Fix Action**
Use Blend SrcAlpha OneMinusSrcAlpha (alpha blend) for smoke, dust, clouds, and debris.
### **Applies To**
  - *.shader
  - *.material
  - *.mat
  - *.prefab
  - *.vfx

## Sorting Enabled on All Particle Systems

### **Id**
vfx-sort-all-particles
### **Severity**
error
### **Type**
regex
### **Pattern**
  - sortMode.*ByDistance|SortByDistance.*true
  - transparencySortMode.*SortByDistance
  - renderingOrder.*SortByDepth
### **Message**
Sorting all particles is expensive (O(n log n)). Only sort when transparency requires it.
### **Fix Action**
Disable sorting for additive effects. Limit sorted particle count to < 1000 per frame.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.uasset

## Fixed Particle Lifetime Without Randomization

### **Id**
vfx-fixed-lifetime-no-random
### **Severity**
error
### **Type**
regex
### **Pattern**
  - lifetime\s*[=:]\s*[\d.]+\s*[;,\n](?!.*random)
  - startLifetime\s*[=:]\s*\{\s*m_Mode\s*[=:]\s*0
  - lifeTime\s*[=:]\s*Constant
### **Message**
Fixed lifetime causes all particles to die simultaneously, creating visible loop seams.
### **Fix Action**
Add +/- 20% random lifetime variation. Use Random Between Two Constants or similar.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.tscn
  - *.cs

## Large Billboard Particles Without LOD

### **Id**
vfx-large-billboard-no-lod
### **Severity**
error
### **Type**
regex
### **Pattern**
  - startSize.*>\s*[5-9]|startSize.*>\s*\d{2,}
  - size.*[=:]\s*[5-9][\d.]*
  - particleSize.*[=:]\s*[5-9]
### **Message**
Large particles (>5 units) cause extreme overdraw. Need LOD to reduce at distance.
### **Fix Action**
Implement size reduction with camera distance. Large effects should fade/shrink when far.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.uasset

## No Velocity Inheritance for Moving Emitter

### **Id**
vfx-no-velocity-inheritance
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - inheritVelocity\s*[=:]\s*0(?:\.0)?
  - InheritVelocity.*false
  - velocityInherit\s*[=:]\s*0
### **Message**
Particles spawned from moving object should inherit some velocity for physical coherence.
### **Fix Action**
Set velocity inheritance to 0.3-0.7 for effects attached to moving characters/vehicles.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.tscn

## World Space Simulation Without Consideration

### **Id**
vfx-simulation-world-space
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - simulationSpace.*World
  - SimulationSpace\s*[=:]\s*0
  - world_coordinate_particles
### **Message**
World space particles detach from moving emitters. Intentional for projectiles, wrong for attached effects.
### **Fix Action**
Use Local space for effects that should follow the emitter (auras, trails on characters).
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.tscn

## Hardcoded Gravity Value

### **Id**
vfx-hardcoded-gravity
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - gravity\s*[=:]\s*-?[\d.]+\s*(?!.*gamePhysics)
  - gravityModifier\s*[=:]\s*[\d.]+
  - GravityForce.*\(\s*-?[\d.]+\s*\)
### **Message**
Hardcoded gravity may not match game physics, causing effects to feel floaty or wrong.
### **Fix Action**
Reference game physics gravity constant. Use Physics.gravity or project settings value.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.cs
  - *.cpp
  - *.gd

## Flipbook Without Frame Blending

### **Id**
vfx-flipbook-no-blend
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - uvAnimation.*blend.*false
  - FlipbookBlending\s*[=:]\s*false
  - flipbook.*mode.*simple
### **Message**
Flipbook without inter-frame blending shows visible stepping at low frame rates.
### **Fix Action**
Enable flipbook blending in particle renderer or implement in shader for smooth animation.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.material

## Constant Particle Color Over Lifetime

### **Id**
vfx-constant-color
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - colorOverLifetime.*m_Mode\s*[=:]\s*0
  - ColorOverLife.*Constant
  - color_ramp.*null
### **Message**
Constant color makes particles look static. Color variation over lifetime adds life and physics feel.
### **Fix Action**
Add color gradient over lifetime. Fire: bright->dark. Smoke: light->transparent. Energy: pulse.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx

## No Noise or Turbulence on Organic Effects

### **Id**
vfx-no-noise-turbulence
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(?:fire|smoke|flame|steam)(?!.*noise)(?!.*turbulence)(?!.*curl)
### **Message**
Organic effects (fire, smoke, steam) without noise look mechanical and computer-generated.
### **Fix Action**
Add curl noise, turbulence, or perlin noise to velocity for organic motion.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.uasset

## Complex Effect in Single Emitter

### **Id**
vfx-single-emitter-complex
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - emission.*subEmitters.*\[\]
  - SubEmitters\s*[=:]\s*null
### **Message**
Complex effects benefit from multiple emitter layers (core, glow, debris). Single emitter limits flexibility.
### **Fix Action**
Separate effect into layers: primary action, secondary motion, ambient detail. Easier to tune and LOD.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx

## Missing Quality/Scalability Settings

### **Id**
vfx-no-quality-scalability
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - qualityLevel.*null
  - scalability.*\[\]|scalability.*undefined
  - effectQuality.*none
### **Message**
No quality settings means effect can't scale for different hardware or player preferences.
### **Fix Action**
Implement quality tiers. Reduce particle count, disable secondary emitters, simplify shaders at lower tiers.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.uasset

## Magic Number Spawn Values

### **Id**
vfx-magic-spawn-numbers
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - spawnRate\s*[=:]\s*(?:37|43|67|73|137|173|257)\b
  - burstCount\s*[=:]\s*(?:17|31|37|47|83)\b
### **Message**
Unusual spawn numbers suggest arbitrary values. Use round numbers or calculated values.
### **Fix Action**
Use intentional values: 10, 25, 50, 100. Or calculate based on duration and desired density.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.cs

## Missing Particle System Bounds

### **Id**
vfx-missing-bounds
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - boundsMode.*None
  - bounds.*null
  - customBounds.*false
### **Message**
Missing bounds prevents frustum culling. Off-screen effects will still render.
### **Fix Action**
Set appropriate bounds for particle system. Use Auto or manually specify based on max extent.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx

## Continuous Effect Without Prewarm

### **Id**
vfx-no-prewarm
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - prewarm\s*[=:]\s*false.*(?:loop|continuous|ambient)
  - (?:loop|continuous).*prewarm\s*[=:]\s*false
### **Message**
Looping/ambient effects without prewarm start empty, building up unnaturally.
### **Fix Action**
Enable prewarm for continuous effects so they appear fully populated immediately.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx

## Potential Overdraw Issues

### **Id**
vfx-overdraw-audit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - emitter\s*\{[^}]*emitter\s*\{[^}]*emitter\s*\{
  - sub_emitter.*sub_emitter
  - layers\s*[=:]\s*[4-9]|\d{2,}
### **Message**
Multiple layered emitters detected. Audit overdraw in GPU profiler.
### **Fix Action**
Profile with overdraw visualization. Target < 4x average, < 8x peak overdraw.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.uasset

## Effect Needs Mobile Audit

### **Id**
vfx-mobile-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - platform.*mobile|MOBILE
  - android|ios|Android|iOS
  - mobileQuality
### **Message**
Mobile platform detected. Verify effect meets mobile fill rate budget (< 2x overdraw).
### **Fix Action**
Create mobile-specific variant with reduced particles, simpler shaders, no distortion.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.uasset
  - *.cs
  - *.cpp

## Soft Particles Performance Check

### **Id**
vfx-soft-particles-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - softParticles\s*[=:]\s*true
  - SoftParticle.*enabled
  - depthFade\s*[=:]\s*true
### **Message**
Soft particles require depth texture sample per particle pixel. Expensive on mobile/low-end.
### **Fix Action**
Disable soft particles on low quality settings. Verify depth texture is available.
### **Applies To**
  - *.prefab
  - *.asset
  - *.vfx
  - *.material

## VFX Texture Resolution Audit

### **Id**
vfx-texture-resolution-check
### **Severity**
warning
### **Type**
file
### **Pattern**
  - *_flipbook_*.png
  - *_vfx_*.tga
  - *_particle_*.png
### **Message**
VFX texture detected. Verify compression settings and resolution appropriate for use case.
### **Fix Action**
Flipbooks: 128x128+ per frame. Use BC7/ASTC for quality. Add padding between frames.
### **Applies To**
  - *.png
  - *.tga
  - *.psd
  - *.tif