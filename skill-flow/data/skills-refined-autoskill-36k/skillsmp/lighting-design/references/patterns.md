# Game Lighting Design

## Patterns


---
  #### **Name**
Three-Point Lighting for Games
  #### **Description**
Adapting cinematography's key/fill/rim setup for interactive 3D
  #### **When**
Setting up character or scene lighting, establishing visual hierarchy
  #### **Example**
    // Classic Three-Point adapted for games:
    
    KEY LIGHT (Primary directional)
    - Brightest light, defines main shadow direction
    - Usually the sun or main light source
    - Cast shadows enabled (only this light in many setups)
    - Warm color for daytime (5500K-6500K)
    
    FILL LIGHT (Ambient/indirect)
    - Softens shadows, adds detail in dark areas
    - In games: ambient light, GI bounce, or fill directional
    - Cooler than key (add blue tint)
    - No shadows or very soft shadows
    - Typically 30-50% intensity of key
    
    RIM/BACK LIGHT (Separation)
    - Highlights edges, separates from background
    - In games: environmental rim, specular highlights
    - Can be baked into environment
    - Especially important for readability in combat
    
    // Game-specific adaptations:
    - Player can face any direction - rim becomes "hero light"
    - Consider camera-relative fill for consistent look
    - Use light layers to control character vs environment
    - Dynamic objects need light probe data for indirect
    

---
  #### **Name**
Lightmap Resolution Budgeting
  #### **Description**
Strategic allocation of lightmap texels across the scene
  #### **When**
Planning lightmap bakes, optimizing memory, fixing quality issues
  #### **Example**
    // Lightmap resolution hierarchy (texels per world unit):
    
    HERO AREAS (player sees up close, lingers)
      Resolution: 40-64 texels/unit
      Examples: Main character area, key story moments
      Memory: High but limited surfaces
    
    PRIMARY GAMEPLAY (main paths, combat areas)
      Resolution: 20-32 texels/unit
      Examples: Corridors, rooms, playable spaces
      Memory: Bulk of your budget
    
    SECONDARY AREAS (visible but not focal)
      Resolution: 8-16 texels/unit
      Examples: Distant buildings, side rooms
      Memory: Moderate, many surfaces
    
    BACKGROUND (far away, rarely focused on)
      Resolution: 2-4 texels/unit
      Examples: Skybox elements, far terrain
      Memory: Low but adds up
    
    // Budget calculation:
    Total_Texels = Sum(Surface_Area * Resolution^2)
    Memory = Total_Texels * 4 bytes (RGBM) or 8 bytes (RGBHDR)
    
    // Unity example:
    // Set per-object in MeshRenderer:
    meshRenderer.scaleInLightmap = 2.0f; // Double resolution
    meshRenderer.scaleInLightmap = 0.5f; // Half resolution
    
    // Unreal example:
    // Set in Static Mesh settings or per-instance:
    // Overridden Light Map Res: 64 (texels)
    

---
  #### **Name**
Light Layers for Gameplay Clarity
  #### **Description**
Separating lighting by purpose using render layers
  #### **When**
Player readability is important, enemies need to stand out
  #### **Example**
    // Layer strategy for action games:
    
    LAYER 0: Environment Base
      - Main sun/key light
      - Ambient/GI
      - Static lightmaps
    
    LAYER 1: Player Highlight
      - Dedicated player rim light (follows player)
      - Subtle fill from camera direction
      - Always visible regardless of environment
    
    LAYER 2: Enemy Highlighting
      - Distinct rim color (often red/orange tint)
      - Ensures enemies readable against any background
      - Can intensify when enemy is alerted
    
    LAYER 3: Interactive Objects
      - Subtle glow or highlight
      - Pickup items, doors, objectives
      - Can pulse or animate
    
    LAYER 4: VFX/Special
      - Muzzle flashes, explosions
      - Don't affect static environment
      - High intensity, short duration
    
    // Unity URP/HDRP:
    // Use Light Layers in light component
    // Match to Rendering Layer Mask on objects
    
    // Unreal:
    // Use Lighting Channels (0-2)
    // Set on lights and primitives
    

---
  #### **Name**
Light Probe Placement Strategy
  #### **Description**
Optimal positioning of probes for dynamic object lighting
  #### **When**
Dynamic characters/objects need to match baked environment
  #### **Example**
    // Probe placement rules:
    
    1. TRANSITION ZONES (Critical)
       - Place probes at lighting boundaries
       - Doorways between bright/dark areas
       - Shadow edges from large occluders
       - Every color temperature change
    
    2. VERTICAL DISTRIBUTION
       - Not just on ground plane
       - Player head height AND ground level
       - Under overhangs and stairs
       - Above and below platforms
    
    3. DENSITY GUIDELINES
       - Indoor: 2-3 meter spacing
       - Outdoor: 4-6 meter spacing
       - Transitions: 1 meter or less
       - Corners: Always place a probe
    
    4. AVOID INVALID POSITIONS
       - Never inside geometry (black probes)
       - Avoid very near walls (bleeding)
       - Don't place in direct shadows only
       - Test by moving object through area
    
    // Unity Probe Group settings:
    // - Use Auto mode for base placement
    // - Manually add at transitions
    // - Remove probes inside walls
    
    // Debug visualization:
    // - Render probe spheres
    // - Show interpolation weights
    // - Check for zero-contribution probes
    

---
  #### **Name**
Shadow Cascade Configuration
  #### **Description**
Optimizing cascaded shadow maps for quality and performance
  #### **When**
Outdoor scenes with directional light shadows
  #### **Example**
    // Cascade shadow map strategy:
    
    // 4-CASCADE SETUP (quality focused):
    Cascade 0: 0-10m   (2048x2048) - Highest detail near player
    Cascade 1: 10-30m  (2048x2048) - Near-mid range
    Cascade 2: 30-80m  (2048x2048) - Mid-far range
    Cascade 3: 80-200m (2048x2048) - Distance
    
    // 2-CASCADE SETUP (performance focused):
    Cascade 0: 0-20m   (2048x2048) - Near player
    Cascade 1: 20-100m (2048x2048) - Everything else
    
    // KEY SETTINGS:
    
    1. Cascade Split Distribution
       - Logarithmic: Better for large outdoor areas
       - Uniform: Better for controlled indoor/outdoor mix
       - Manual: When you know your gameplay distances
    
    2. Shadow Distance
       - Match to gameplay needs, not art desires
       - Shadows beyond fog distance are wasted
       - Consider LOD - distant shadows can be lower res
    
    3. Bias and Normal Bias
       - Shadow Bias: 0.05-0.1 (prevents acne)
       - Normal Bias: 0.4-1.0 (prevents peter-panning)
       - Too much bias = floating shadows
       - Too little = shadow acne
    
    4. Soft Shadows
       - PCF (cheap): 3x3 or 5x5 samples
       - PCSS (expensive): Contact hardening
       - VSM (tricky): Light bleeding issues
       - Consider cascade 0 only for soft
    

---
  #### **Name**
Time-of-Day System Architecture
  #### **Description**
Smooth day/night cycle with proper lighting transitions
  #### **When**
Game needs dynamic time progression, open world
  #### **Example**
    // Time-of-day system components:
    
    1. SUN/MOON ROTATION
       float sunAngle = (timeOfDay / 24.0) * 360.0 - 90.0;
       sun.rotation = Quaternion.Euler(sunAngle, sunAzimuth, 0);
    
       // Smooth intensity curve (not linear!)
       float sunIntensity = Mathf.Clamp01(
         Mathf.Sin(sunAngle * Mathf.Deg2Rad) * 1.5
       );
    
    2. COLOR TEMPERATURE GRADIENT
       TimeOfDay  | Color Temp | Color
       -----------|------------|------------------
       Sunrise    | 2000K      | Deep orange-red
       Golden     | 3500K      | Warm yellow-orange
       Midday     | 6500K      | Neutral white-blue
       Golden PM  | 3500K      | Warm yellow-orange
       Sunset     | 2500K      | Orange-red-purple
       Blue Hour  | 12000K     | Deep blue
       Night      | 4100K      | Cool moonlight
    
    3. AMBIENT/SKY TRANSITIONS
       // Blend between sky presets
       skyMaterial.SetFloat("_AtmosphereThickness",
         Mathf.Lerp(dayThickness, nightThickness, nightBlend));
    
       // Update ambient gradient
       RenderSettings.ambientSkyColor = Color.Lerp(
         daySkyColor, nightSkyColor, nightBlend);
    
    4. LIGHT PROBE RE-EVALUATION
       // Options:
       // A) Multiple baked probe sets (blend between)
       // B) Realtime GI update (expensive)
       // C) Scriptable probe adjustment (fake but cheap)
    
    5. EXPOSURE ADAPTATION
       // HDR eye adaptation for transitions
       // Going into dark tunnel = slow adaptation
       // Exiting to bright = faster adaptation
    

---
  #### **Name**
Interior vs Exterior Lighting Balance
  #### **Description**
Managing the extreme contrast between indoors and outdoors
  #### **When**
Player transitions between indoor and outdoor spaces
  #### **Example**
    // The problem: Real world has 100,000:1 contrast
    // Games typically render 10:1 or less visible range
    // Solution: Careful exposure and lighting design
    
    EXTERIOR LIGHTING:
      Sun: 100,000+ lux (in HDR)
      Sky: 10,000 lux
      Shadows: 1,000-5,000 lux (ambient only)
    
    INTERIOR LIGHTING:
      Indoor ambient: 100-500 lux
      Windows: 10,000 lux (sky visible)
      Artificial: 300-800 lux (lamps)
    
    // KEY TECHNIQUE: Exposure Zones
    
    // Define exposure volumes:
    EXTERIOR: EV 14-15 (bright sunny day)
    TRANSITION: EV 11-13 (covered porch, doorway)
    INTERIOR: EV 8-10 (indoor ambient)
    DARK: EV 4-6 (basement, cave)
    
    // Blend between exposures as player moves
    float targetEV = GetExposureForPosition(playerPos);
    currentEV = Mathf.Lerp(currentEV, targetEV, adaptSpeed * dt);
    
    // DESIGN RULES:
    1. Always have a transition zone (porch, awning, hallway)
    2. Make windows bright but not blinding
    3. Add interior rim lights facing windows
    4. Artificial lights should look intentional
    5. Test by walking the full path
    

---
  #### **Name**
Volumetric Lighting Setup
  #### **Description**
God rays, light shafts, and atmospheric scattering
  #### **When**
Adding atmosphere, visualizing light beams, creating mood
  #### **Example**
    // Volumetric lighting techniques by engine:
    
    SCREEN-SPACE VOLUMETRICS (cheap, limited):
      // Post-process effect
      // Good for: Uniform fog, simple shafts
      // Limitations: No shadows in volume, 2D artifacts
    
    RAYMARCHED VOLUMETRICS (expensive, accurate):
      // March rays through volume, sample shadows
      // Good for: Accurate shafts, shadow-aware
      // Limitations: Performance cost, noise
    
    // KEY PARAMETERS:
    
    1. Scattering Coefficient (how much light scatters)
       Low: 0.001 - subtle haze
       Medium: 0.01 - visible beams
       High: 0.1 - dense fog
    
    2. Extinction (how fast light fades)
       Balance with scattering for desired falloff
       High extinction + low scatter = dark fog
       Low extinction + high scatter = bright haze
    
    3. Anisotropy (scattering direction preference)
       0.0 = uniform (isotropic)
       0.7+ = forward scatter (bright toward light)
       Mie scattering for dust/fog: 0.5-0.8
    
    // OPTIMIZATION:
    - Render at half or quarter resolution
    - Limit ray march steps (32-64 typical)
    - Use temporal reprojection to reduce noise
    - Cull volumetrics outside camera frustum
    - Only enable on capable hardware (quality tier)
    

---
  #### **Name**
HDR and Tonemapping Pipeline
  #### **Description**
Managing high dynamic range through the render pipeline
  #### **When**
Setting up HDR rendering, color grading, handling bright lights
  #### **Example**
    // HDR Pipeline stages:
    
    1. RENDER IN HDR
       - Use floating point render targets (R16G16B16A16_Float)
       - Allow values > 1.0 for bright sources
       - Sun can be 100+ intensity in HDR
       - Preserve full range until tonemapping
    
    2. BLOOM EXTRACTION
       - Threshold based on luminance (typically > 1.0)
       - Bloom before tonemapping to preserve energy
       - Soft threshold for gradual falloff
    
    3. COLOR GRADING (in HDR)
       - LUT or curve adjustments
       - Work in log or HDR space
       - Lift/Gamma/Gain controls
    
    4. TONEMAPPING (HDR -> LDR)
       // Common operators:
       Reinhard:     x / (x + 1)
       Reinhard Ext: x * (1 + x/w^2) / (1 + x)
       ACES Filmic:  Industry standard, good rolloff
       Uncharted 2:  Nice highlight compression
       GT:           Neutral, no hue shift
    
       // ACES approximation:
       vec3 ACESFilm(vec3 x) {
         float a = 2.51;
         float b = 0.03;
         float c = 2.43;
         float d = 0.59;
         float e = 0.14;
         return clamp((x*(a*x+b))/(x*(c*x+d)+e), 0.0, 1.0);
       }
    
    5. OUTPUT TRANSFORM
       - Apply gamma (2.2 for sRGB displays)
       - Or use display-specific (HDR10, Dolby Vision)
    
    // EXPOSURE CONTROL:
    Manual: Fixed EV based on scene
    Auto: Histogram-based adaptation
    Hybrid: Auto with min/max limits
    

---
  #### **Name**
Emissive Materials as Light Sources
  #### **Description**
Using self-illuminating materials that contribute to lighting
  #### **When**
Neon signs, screens, lava, magical effects need to emit light
  #### **Example**
    // Emissive lighting approaches:
    
    1. VISUAL ONLY (no actual light contribution)
       - Just set material emission
       - Add separate point/spot light
       - Cheapest option, most control
       - Best for: Most situations
    
    2. BAKED EMISSION
       - Material contributes to lightmap bake
       - Good for: Static neon signs, always-on lights
       - Set emission intensity for indirect contribution
       - Unity: Emission > Realtime/Baked GI
    
    3. REALTIME AREA LIGHTS
       - True area light matching emissive shape
       - Expensive but accurate
       - Good for: Hero lights, cinematics
       - HDRP/UE5 support rectangular area lights
    
    // IMPLEMENTATION TIPS:
    
    // Match emissive intensity to light
    float emissiveIntensity = lightIntensity * emissiveScale;
    material.SetColor("_EmissionColor",
      baseColor * emissiveIntensity);
    
    // Fake area light falloff
    // Place point light slightly behind emissive surface
    // Larger radius, lower intensity for soft falloff
    
    // Bloom sells emission
    // Set emission intensity high enough to trigger bloom
    // Even if actual light contribution is separate
    
    // Flickering/animated emission
    float flicker = Mathf.PerlinNoise(Time.time * speed, 0);
    emission = baseEmission * Mathf.Lerp(minFlicker, 1.0, flicker);
    

## Anti-Patterns


---
  #### **Name**
Uniform Lighting Everywhere
  #### **Description**
Flat, even lighting across the entire scene with no contrast
  #### **Why**
Boring visuals, no focal points, washed out appearance, loses depth
  #### **Instead**
Create contrast. Dark makes light interesting. Use hero lighting for focus.

---
  #### **Name**
All Realtime All The Time
  #### **Description**
Using only realtime lights when baking would work
  #### **Why**
Massive performance waste. Realtime shadows are expensive. GI impossible in realtime on most hardware.
  #### **Instead**
Bake everything static. Reserve realtime for moving lights and dynamic shadows.

---
  #### **Name**
Max Resolution Lightmaps
  #### **Description**
Setting all lightmap resolutions to maximum
  #### **Why**
Explodes memory usage. Bake times become days. Diminishing returns past 32 texels/unit for most surfaces.
  #### **Instead**
Budget texels to importance. Hero areas high, background low. Profile memory.

---
  #### **Name**
Ignoring Light Probe Placement
  #### **Description**
Auto-generating probes without manual adjustment
  #### **Why**
Dynamic objects pop/swim through lighting. Probes inside geometry cause black objects.
  #### **Instead**
Manually verify probe placement. Dense at transitions. Test with dynamic object.

---
  #### **Name**
Skipping Reflection Probes
  #### **Description**
Relying only on skybox reflections
  #### **Why**
Interiors reflect sky. Metallic objects look wrong. Breaks visual coherence.
  #### **Instead**
Place reflection probes in each distinct space. Box projection for interiors.

---
  #### **Name**
Overbright Light Stacking
  #### **Description**
Multiple overlapping lights without considering additive brightness
  #### **Why**
Blown out areas. Incorrect exposure. HDR values spike causing bloom explosion.
  #### **Instead**
Plan light coverage. Check combined intensity. Use light groups for testing.

---
  #### **Name**
Wrong Color Space for Textures
  #### **Description**
Using sRGB textures for lighting data (lightmaps, probes)
  #### **Why**
Lighting calculations done in wrong space. Colors shift. Values incorrect.
  #### **Instead**
Lightmaps should be linear or RGBM encoded. Configure import settings correctly.

---
  #### **Name**
Shadow Distance Matches View Distance
  #### **Description**
Casting shadows as far as the camera can see
  #### **Why**
Wastes shadow map resolution. Distant shadows are invisible anyway.
  #### **Instead**
Shadow distance should match gameplay needs. Fade shadows at distance.

---
  #### **Name**
Ignoring Mobile Constraints
  #### **Description**
Designing lighting for PC/console without considering mobile
  #### **Why**
Mobile can't handle complex lighting. Realtime shadows are luxury. Probes are limited.
  #### **Instead**
Design for lowest target first. Add quality tiers. Test early on device.

---
  #### **Name**
One Global Ambient Color
  #### **Description**
Using single ambient color for entire game
  #### **Why**
Every area feels the same. Loses sense of place. Lighting feels flat.
  #### **Instead**
Per-area ambient settings. Use sky gradient. Blend between ambient zones.