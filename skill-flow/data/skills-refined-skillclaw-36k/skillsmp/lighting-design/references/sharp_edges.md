# Lighting Design - Sharp Edges

## Lightmap Uv Seam Artifacts

### **Id**
lightmap-uv-seam-artifacts
### **Summary**
Lightmap UV seams cause visible lighting discontinuities
### **Severity**
critical
### **Situation**
Baked lighting shows hard lines or color shifts at mesh UV island boundaries
### **Why**
  Lightmap UVs must have padding between islands to prevent texture bleeding. When
  the GPU samples between texels at a seam, it can pick up data from an adjacent
  island. This is especially visible on curved surfaces where lighting should be
  continuous. The problem is made worse by lightmap compression and mip levels.
  
### **Solution**
  1. Ensure UV island padding in lightmap UVs:
     - Minimum 2-4 texels at target resolution
     - More for lower resolution lightmaps
     - Account for mip chain (double padding per mip)
  
  2. Auto-generate lightmap UVs with padding:
     Unity: Generate Lightmap UVs checkbox, Pack Margin setting
     Unreal: Light Map Resolution, Light Map Coordinate Index
  
  3. For critical meshes:
     - Create dedicated lightmap UV channel (UV1 or UV2)
     - Maximize island size, minimize seam count
     - Place seams at hard edges (normal breaks)
  
  4. Dilate lightmap edges in bake:
     - Most bakers have dilation setting (2-4 pixels)
     - Fills padding area with edge color
  
### **Symptoms**
  - Hard lines visible on smooth curved surfaces
  - Color shifts at mesh seams
  - Lines appear at specific viewing angles
  - Worse after lightmap compression
  - Visible in certain lighting conditions only
### **Detection Pattern**
LightmapParameters|lightmapScaleOffset
### **Version Range**
*
### **Red Flags**
  - Importing meshes without checking lightmap UVs
  - Pack margin set to 0
  - Overlapping lightmap UV islands
  - Single lightmap UV for complex mesh

## Light Probe Bleeding

### **Id**
light-probe-bleeding
### **Summary**
Light probes leak light through walls and floors
### **Severity**
critical
### **Situation**
Dynamic objects in dark rooms pick up bright lighting from adjacent areas
### **Why**
  Light probes are interpolated by position - they have no knowledge of geometry.
  A probe on the bright side of a wall will influence objects near that wall on
  the dark side. The interpolation is based on a tetrahedralization of probe
  positions, not on actual light paths. This is especially problematic in
  multi-story buildings and thin walls.
  
### **Solution**
  1. Dense probe placement at boundaries:
     - Place probes on BOTH sides of walls
     - Very close spacing at transitions (0.5-1m)
     - Probes at floor/ceiling of each level
  
  2. Use probe volumes/regions:
     Unity: Light Probe Groups with dense boundary sampling
     Unreal: Lightmass Importance Volumes with tight bounds
  
  3. Manual probe editing:
     - Remove probes that sample through geometry
     - Add probes in dark corners that are being missed
     - Test by moving object slowly through space
  
  4. Architectural solutions:
     - Thicken walls in geometry
     - Add "blocker" geometry for probe sampling
     - Extend floors/ceilings past walls
  
  5. Consider alternatives for problematic areas:
     - Light Probe Proxy Volumes (LPPV) in Unity
     - Per-object ambient overrides
     - Dedicated indoor/outdoor probe sets
  
### **Symptoms**
  - Characters glow in dark rooms
  - Light "bleeds" through thin walls
  - Upper floors lit by ground floor
  - Brightness pops when crossing thresholds
  - Dynamic objects don't match baked surfaces
### **Detection Pattern**
LightProbe|lightProbeUsage
### **Version Range**
*
### **Red Flags**
  - Single-layer probe grid for multi-story building
  - Thin walls without probe consideration
  - Auto-generated probes without validation
  - No probes in dark areas

## Shadow Acne Peter Panning

### **Id**
shadow-acne-peter-panning
### **Summary**
Shadows show dotted patterns (acne) or float above surfaces (peter panning)
### **Severity**
high
### **Situation**
Self-shadowing produces artifacts, or shadows don't touch their casters
### **Why**
  Shadow mapping compares depth values with limited precision. Shadow acne occurs
  when a surface incorrectly shadows itself due to depth precision limits. Bias
  pushes the shadow test away from the surface - too little causes acne, too much
  causes shadows to detach from objects (peter panning). Normal bias helps but
  can cause light leaking at grazing angles.
  
### **Solution**
  1. Balanced bias settings:
     Depth Bias: Start at 1-2 (units vary by engine)
     Normal Bias: Start at 1-2
     Iterate: Fix acne first, then reduce until peter-panning gone
  
  2. Per-light tuning:
     - Directional lights need different bias than point/spot
     - Large shadow distances need more bias
     - Near objects need less bias
  
  3. Shadow map resolution:
     - Higher resolution = less bias needed
     - But comes with performance cost
     - Balance quality vs performance
  
  4. Slope-scale bias:
     - Automatically adjusts bias based on surface angle
     - Better for varied geometry
     - Most engines have this option
  
  5. Alternative techniques:
     - Normal offset shadows (offset in normal direction)
     - VSM/ESM (different artifacts, no acne)
     - Raytraced shadows (expensive, no bias issues)
  
### **Symptoms**
  - Dotted/striped patterns on surfaces
  - Shadows float above ground
  - Shadows disconnect at steep angles
  - Moire patterns in shadows
  - Worse at grazing angles
### **Detection Pattern**
shadowBias|normalBias|shadowNormalBias|depthBias
### **Version Range**
*
### **Red Flags**
  - Same bias values for all light types
  - Zero bias settings
  - Very low shadow resolution with complex geometry
  - Large shadow distance without cascade adjustment

## Bake Time Explosion

### **Id**
bake-time-explosion
### **Summary**
Lightmap baking takes hours or days instead of minutes
### **Severity**
high
### **Situation**
Adding content causes bake time to increase exponentially
### **Why**
  Lightmap baking is O(n * m * samples) where n = texels, m = light bounces.
  High resolution lightmaps on large scenes explode quickly. Additionally,
  GPU bakers can run out of VRAM, falling back to slow CPU paths. Overlapping
  geometry causes resampling. Unnecessary bounces add more time.
  
### **Solution**
  1. Resolution audit:
     - Lower resolution for non-hero surfaces
     - 4-8 texels/unit is fine for distant objects
     - Use resolution per object/group, not global
  
  2. Reduce bounce counts:
     - 2-3 bounces is usually sufficient
     - First bounce is 80% of GI contribution
     - More bounces = diminishing returns + time
  
  3. Scene segmentation:
     Unity: Bake selected objects only
     Unreal: Lightmass Importance Volumes
  
  4. GPU baking optimization:
     - Ensure GPU baking is enabled
     - Check VRAM isn't exceeded (watch for fallback)
     - Close other GPU applications
  
  5. Geometry cleanup:
     - Remove overlapping faces
     - Delete interior faces player never sees
     - Simplify distant geometry
  
  6. Iterative workflow:
     - Use preview/fast bake for iteration
     - Only full quality for final
     - Bake zones independently when possible
  
### **Symptoms**
  - Bake time in hours instead of minutes
  - Each added object multiplies bake time
  - GPU memory errors during bake
  - Progress bar barely moves
  - Editor becomes unresponsive
### **Detection Pattern**
lightmapResolution|indirectResolution|Lightmapping
### **Version Range**
*
### **Red Flags**
  - Global high resolution lightmap settings
  - 5+ light bounces
  - Entire world in single bake
  - Overlapping/z-fighting geometry

## Overlapping Lights Overbright

### **Id**
overlapping-lights-overbright
### **Summary**
Multiple overlapping lights cause blown-out overbright areas
### **Severity**
high
### **Situation**
Areas with multiple lights become completely white/overexposed
### **Why**
  Light is additive. Two 1-intensity lights in the same spot = 2 intensity.
  This is physically correct but often unintended. Combined with bloom,
  areas quickly become blown out. Artists often create lights without
  checking combined contribution.
  
### **Solution**
  1. Light intensity audit:
     - View scene without post-processing
     - Check luminance/exposure values
     - Keep important areas in 0-1 range for LDR
  
  2. Light overlap planning:
     - Visualize light radius/attenuation
     - Reduce intensity of overlapping lights
     - Key light should dominate, fills should be subtle
  
  3. Use light groups:
     - Isolate lights to check individual contribution
     - A/B test light combinations
     - Document intended combined intensity
  
  4. Exposure/tonemapping adjustment:
     - Set exposure for brightest intended area
     - Use highlight compression (filmic tonemapping)
     - Bloom threshold relative to scene luminance
  
  5. Physical light units:
     - Use real-world values (lumens, lux)
     - Natural attenuation prevents overbright
     - Requires proper exposure workflow
  
### **Symptoms**
  - White/blown out areas
  - Bloom explosion in certain spots
  - Brightness varies wildly across scene
  - Can't see detail in bright areas
  - Looks fine without post-processing
### **Detection Pattern**
intensity|lightIntensity|color.*\\*
### **Version Range**
*
### **Red Flags**
  - Multiple point lights in same area
  - No consideration of additive contribution
  - Bloom threshold set too low
  - No exposure compensation

## Dynamic Objects Baked Mismatch

### **Id**
dynamic-objects-baked-mismatch
### **Summary**
Dynamic objects look wrong in baked lighting environments
### **Severity**
critical
### **Situation**
Characters/props don't match the lighting of the baked environment
### **Why**
  Baked lighting stores in textures (lightmaps) only for static geometry.
  Dynamic objects use light probes for indirect light and realtime lights
  for direct. If probes don't capture the baked lighting accurately, or
  if the main light is different for baked vs realtime, dynamic objects
  look pasted in.
  
### **Solution**
  1. Ensure main light matches:
     - Realtime light with same direction/color as baked
     - Mixed mode: same light for both bake and realtime
     - Match shadow softness and color
  
  2. Accurate probe placement:
     - Dense probes in player-accessible areas
     - Capture all lighting variations
     - Validate by moving debug sphere through scene
  
  3. Reflection probe alignment:
     - Interior probes for indoor spaces
     - Box projection for rooms
     - Update probes if environment changes
  
  4. Consider hybrid approaches:
     - Realtime GI for dynamic contribution (expensive)
     - SSGI/RTGI for additional indirect
     - Ambient override per area
  
  5. Art direction tricks:
     - Dedicated character rim light
     - Subtle ambient boost on characters
     - Match key light exactly
  
### **Symptoms**
  - Characters look "pasted in"
  - Wrong color tint on dynamic objects
  - Missing indirect lighting on characters
  - Reflections don't match environment
  - Moving objects "pop" at probe boundaries
### **Detection Pattern**
lightProbe|useLightProbes|ContributeGI
### **Version Range**
*
### **Red Flags**
  - Only skybox reflection, no reflection probes
  - Different sun angle for bake vs realtime
  - Sparse light probes in player areas
  - No mixed mode lights

## Reflection Probe Parallax Errors

### **Id**
reflection-probe-parallax-errors
### **Summary**
Reflections slide/stretch incorrectly on surfaces
### **Severity**
medium
### **Situation**
Metallic surfaces show reflections in wrong positions
### **Why**
  Standard reflection probes capture from a single point. When the reflecting
  surface is far from that point, the reflection appears in the wrong place.
  Box projection helps for rooms but requires careful setup. Probe blending
  at boundaries can also cause issues.
  
### **Solution**
  1. Enable box projection:
     - Set probe bounds to match room geometry
     - Adjust box offset to room center
     - Works best for box-shaped rooms
  
  2. Probe placement:
     - Center of room for interiors
     - One probe per distinct space
     - More probes for large/complex areas
  
  3. Blend distance tuning:
     - Reduce blend distance to minimize overlap
     - Sharp transition sometimes better than wrong blend
     - Test metallic objects at boundaries
  
  4. For complex geometry:
     - Multiple probes with careful blending
     - Accept limitations of probe-based reflections
     - Consider SSR for accurate reflections (more expensive)
  
  5. Planar reflections:
     - For flat surfaces (water, mirrors)
     - More expensive but accurate
     - Only enable where needed
  
### **Symptoms**
  - Reflections slide as camera moves
  - Wrong objects visible in reflection
  - Stretching at room edges
  - Reflection "pops" at probe boundaries
  - Metallic objects look incorrect
### **Detection Pattern**
ReflectionProbe|boxProjection|blendDistance
### **Version Range**
*
### **Red Flags**
  - Single reflection probe for entire level
  - Box projection disabled in interiors
  - Probes placed in walls/corners
  - Very large blend distances

## Mobile Lighting Performance

### **Id**
mobile-lighting-performance
### **Summary**
Lighting design that works on PC destroys mobile performance
### **Severity**
critical
### **Situation**
Game runs well on desktop, terribly on mobile devices
### **Why**
  Mobile GPUs are fundamentally different from desktop. They're tile-based,
  bandwidth limited, and thermal constrained. Desktop lighting strategies
  don't transfer. Realtime shadows are luxury. Multiple realtime lights are
  expensive. Lightmaps hit memory limits.
  
### **Solution**
  1. Realtime light limits:
     - 1-2 realtime lights max (often just sun)
     - Avoid point/spot shadows entirely if possible
     - Use baked shadows with realtime directional
  
  2. Lightmap optimization:
     - Lower resolution (10-20% of desktop)
     - Aggressive compression
     - Fewer bounces (1-2 max)
     - ASTC compression for size
  
  3. Simplified probe setups:
     - Fewer, larger probe volumes
     - Lower resolution probe capture
     - Consider flat ambient for some scenes
  
  4. Shadow simplification:
     - Single cascade, shorter distance
     - Lower resolution shadow maps
     - Consider blob shadows for characters
  
  5. Quality tiers:
     - Separate lighting setups per tier
     - Mobile: baked only, simple probes
     - PC: full realtime, high-res everything
  
  6. Avoid:
     - Volumetric lighting
     - Screen-space effects (SSAO, SSR)
     - HDR rendering (if possible)
     - Complex tonemapping
  
### **Symptoms**
  - Frame rate drops below 30 fps
  - Device overheats
  - Battery drains rapidly
  - Visual quality same but performance terrible
  - Works in editor, dies on device
### **Detection Pattern**
QualitySettings|graphicsTier|mobile
### **Version Range**
*
### **Red Flags**
  - Same lighting settings for mobile and desktop
  - Realtime shadows on mobile
  - No mobile testing during development
  - No quality tier system

## Emissive No Contribution

### **Id**
emissive-no-contribution
### **Summary**
Emissive materials don't actually light the environment
### **Severity**
medium
### **Situation**
Bright glowing materials don't illuminate nearby surfaces
### **Why**
  By default, emissive materials only affect their own appearance - they
  don't contribute to scene lighting. This is a common misconception.
  Emission contribution to lightmaps requires explicit settings, and
  realtime emission contribution requires actual lights or advanced GI.
  
### **Solution**
  1. For baked GI contribution:
     Unity: Enable "Contribute Global Illumination" on mesh
            Set Emission > Global Illumination > Baked
     Unreal: Set Emissive for Static Lighting on material
             Bake lightmaps
  
  2. Pair with actual lights:
     - Place point light at emissive surface
     - Match light color and rough intensity
     - Light does the work, emissive provides visual
  
  3. For realtime emission:
     - Lumen (UE5) handles this automatically
     - RTGI solutions can capture emission
     - Otherwise, must use actual lights
  
  4. Area light matching:
     - If engine supports, use area light shaped to emissive
     - Rectangle lights for screens
     - Disc lights for circular emissives
  
### **Symptoms**
  - Neon sign doesn't light nearby wall
  - TV screen doesn't illuminate room
  - Glowing material looks bright but no light cast
  - Emissive looks wrong compared to actual lights
### **Detection Pattern**
emission|emissive|_EmissionColor|Global Illumination
### **Version Range**
*
### **Red Flags**
  - Expecting emission to light scene without configuration
  - No separate light paired with emissive
  - Emissive intensity not set for GI contribution
  - Realtime emission expected without proper GI

## Hdr Bloom Clipping

### **Id**
hdr-bloom-clipping
### **Summary**
Bloom looks wrong due to improper HDR handling
### **Severity**
medium
### **Situation**
Bloom appears as harsh circles or doesn't appear at all
### **Why**
  Bloom extracts bright pixels above a threshold. If your brightest value
  is 1.0 (LDR), bloom threshold of 1.0 captures nothing. If values are
  too high without proper tonemapping, bloom explodes. The threshold must
  be set relative to your scene's actual luminance values.
  
### **Solution**
  1. Work in true HDR:
     - Render target: R16G16B16A16_Float
     - Light intensities can exceed 1.0
     - Sun at 5-10 intensity, indoor lights lower
  
  2. Set threshold properly:
     - Threshold relative to scene values
     - If max scene value is 3.0, threshold at 1.5
     - Soft knee/threshold for gradual falloff
  
  3. Bloom before tonemapping:
     - Extract bloom in HDR space
     - Apply tonemapping after bloom composite
     - Otherwise bloom loses energy
  
  4. Physical light values help:
     - Use lumens/lux for lights
     - Natural range informs threshold
     - Consistent across scenes
  
  5. Intensity and scatter:
     - Lower intensity for subtle bloom
     - Higher scatter for softer, larger bloom
     - Avoid harsh circular artifacts
  
### **Symptoms**
  - No bloom on bright objects
  - Bloom as harsh circles/halos
  - Bloom intensity varies wildly between scenes
  - Tonemapped image has no bloom at all
  - Bloom applies to everything or nothing
### **Detection Pattern**
bloom|Bloom|threshold|intensity
### **Version Range**
*
### **Red Flags**
  - Bloom threshold = 1.0 with LDR values
  - Bloom after tonemapping
  - No consideration of scene luminance range
  - Same bloom settings for all scenes