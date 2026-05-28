# Environment Art

## Patterns


---
  #### **Name**
The Squint Test for Value Hierarchy
  #### **Description**
    Squint your eyes until details blur. Only large shapes and value contrasts remain.
    This reveals your true visual hierarchy. If you can't identify the focal point,
    neither can the player. The primary read (hero elements) should be highest contrast.
    Secondary reads support. Tertiary fills space without competing.
    
  #### **When**
Evaluating composition, identifying focal point issues, debugging unclear spaces
  #### **Example**
    // Value hierarchy checklist (squint test)
    // 1. Take screenshot of your scene
    // 2. Apply Gaussian blur (radius 20-50px) or squint
    // 3. Ask: Where does my eye go FIRST?
    // 4. Is that where gameplay needs attention?
    
    // Value distribution guide:
    // - Hero elements: 90-100% contrast against surroundings
    // - Secondary elements: 50-70% contrast
    // - Fill/background: 20-40% contrast
    
    // Common fix: Darken background, lighten focal point
    // Or: Add rim light to hero, reduce fill light on clutter
    

---
  #### **Name**
Power-of-2 Modular Grid System
  #### **Description**
    All modular assets snap to a power-of-2 grid (256, 512, 1024 units).
    Pivot points at the CORNER (0,0,0 in your DCC), not center.
    This ensures seamless snapping in-engine and eliminates gaps.
    Wall thickness matches the grid (32, 64 units).
    Floor pieces have mass - never paper-thin.
    
  #### **When**
Starting modular kit, planning asset dimensions, debugging snapping issues
  #### **Example**
    // Modular grid setup (Unreal uses cm, Unity uses m - convert!)
    // Base unit: 256 units (or 2.56m)
    // Half: 128 units
    // Quarter: 64 units
    
    // Asset dimensions:
    // Wall segment: 256w x 256h x 32d (power of 2!)
    // Floor tile: 256 x 256 x 32 (with thickness!)
    // Door frame: 128w x 256h x 32d
    // Stairs: 256 run x 128 rise (comfortable human scale)
    
    // Pivot placement in Maya/Blender:
    // 1. Model at origin
    // 2. Move mesh so CORNER sits at 0,0,0
    // 3. Export - pivot will be at corner
    // 4. In-engine: snap by pivot = perfect alignment
    

---
  #### **Name**
Hero, Unique, Modular, Dressing Hierarchy
  #### **Description**
    Four tiers of assets, each with a specific role:
    - HERO (5%): Unique focal points with most detail, custom textures. The set pieces.
    - UNIQUE (15%): Notable assets that catch eye but aren't centerpieces.
    - MODULAR (50%): Kit pieces that build structure. Versatile, tileable.
    - DRESSING (30%): Props that fill space and add life. Reusable, low-poly.
    Budget your time accordingly: 40% on hero/unique, 60% on modular/dressing.
    
  #### **When**
Planning asset list, allocating art time, reviewing environment completeness
  #### **Example**
    // Asset hierarchy for a medieval tavern:
    
    // HERO (1-2 assets, custom everything):
    // - Grand fireplace with animated embers
    // - Mounted dragon skull trophy
    
    // UNIQUE (3-5 assets, high detail):
    // - Carved wooden bar counter
    // - Stained glass window
    // - Ornate chandelier
    
    // MODULAR (kit pieces):
    // - Wall panels (wood, stone variants)
    // - Floor tiles (clean, dirty, damaged)
    // - Beams and support columns
    // - Window frames, door frames
    
    // DRESSING (small props, many instances):
    // - Mugs, plates, utensils
    // - Candles, lanterns
    // - Barrels, crates, sacks
    // - Hanging meats, dried herbs
    

---
  #### **Name**
Trim Sheets and Material Atlases
  #### **Description**
    A trim sheet is a texture atlas that tiles along one axis. It contains
    multiple surface treatments (clean, worn, damaged) in strips. One 2K
    trim sheet can texture an entire architectural style. UV mapping uses
    strips, not islands. This reduces draw calls and maintains consistent
    texel density across the entire environment.
    
  #### **When**
Texturing modular kits, optimizing material count, maintaining consistency
  #### **Example**
    // Trim sheet layout (2048x2048 example):
    //
    // [   Clean metal strip   ] 256px height
    // [   Rusty metal strip   ] 256px height
    // [   Edge/trim detail    ] 128px height
    // [   Rivets/bolts strip  ] 128px height
    // [   Worn wood strip     ] 256px height
    // [   Clean wood strip    ] 256px height
    // [   Stone/concrete      ] 512px height
    // [   Damage/grunge       ] 256px height
    
    // UV mapping rules:
    // - Horizontal UVs stretch across sheet (0-1 U, tiles)
    // - Vertical UVs sample specific strip (fixed V position)
    // - Keep texel density: 512 px/m for hero, 256 px/m for background
    
    // Master material setup:
    // - One material, one draw call
    // - Vertex color for variation (R=dirt, G=wear, B=damage)
    

---
  #### **Name**
Color Scripting for Mood
  #### **Description**
    Create a "color script" before building - a sequence of color keys showing
    the emotional journey through your space. Warm colors advance, cool recede.
    Saturated colors draw attention; desaturated colors support. Limit palette
    to 3-4 dominant hues. Use complementary accents sparingly for maximum impact.
    The color script IS your mood blueprint.
    
  #### **When**
Planning environment mood, establishing emotional beats, debugging flat feelings
  #### **Example**
    // Color script for a horror hospital level:
    
    // ENTRANCE (false safety):
    // - Dominant: Warm white (6500K fluorescent)
    // - Secondary: Pale green (hospital walls)
    // - Accent: Red (exit signs, blood hints)
    
    // CORRIDOR (growing dread):
    // - Dominant: Sickly yellow-green
    // - Secondary: Deep shadow blacks
    // - Accent: Flickering warm orange (broken lights)
    
    // OPERATING ROOM (climax):
    // - Dominant: Cold surgical blue-white
    // - Secondary: Rust red (old blood, decay)
    // - Accent: Harsh white (spotlight on table)
    
    // Color scripting workflow:
    // 1. Sketch level as simple rectangles
    // 2. Paint dominant color for each area
    // 3. Add emotional notes (safe, tense, terrifying)
    // 4. Use as reference during blockout AND final pass
    

---
  #### **Name**
Vertex Color Variation System
  #### **Description**
    Vertex colors provide free texture variation at zero memory cost.
    Paint R, G, B, A channels to blend materials, add weathering, or
    create AO. In materials, use vertex color to lerp between clean/dirty,
    snow/ground, wet/dry. High-poly models during bake, then transfer to
    low-poly. Breaks tiling without additional textures.
    
  #### **When**
Breaking up texture tiling, adding weathering, material transitions
  #### **Example**
    // Vertex color channel convention:
    // R = Dirt/grime amount (0=clean, 1=dirty)
    // G = Wear/damage amount (0=new, 1=worn)
    // B = Wetness/moisture (0=dry, 1=wet)
    // A = AO or height blend factor
    
    // Material setup (Unreal/Unity):
    //
    // BaseColor = lerp(CleanAlbedo, DirtyAlbedo, VertexColor.R)
    // Roughness = lerp(CleanRough, WornRough, VertexColor.G)
    // Normal = lerp(BaseNormal, DamageNormal, VertexColor.G)
    
    // Workflow:
    // 1. Create mesh with enough vertices to paint (add loops!)
    // 2. Paint vertex colors in DCC or in-engine
    // 3. Bake vertex AO for free shadowing
    // 4. Export with vertex colors enabled
    

---
  #### **Name**
Environmental Storytelling Staging
  #### **Description**
    Every prop placement tells a story. Don't decorate - STAGE. Ask: Who was here?
    What were they doing? What happened? Cluster props into "story vignettes" -
    small scenes that imply narrative without exposition. Use the rule of 3:
    3 related props form a scene (coffee cup + newspaper + reading glasses = person
    was here, reading, left suddenly).
    
  #### **When**
Set dressing phase, adding narrative depth, making spaces feel lived-in
  #### **Example**
    // Story vignette examples:
    
    // "Hasty escape" vignette:
    // - Overturned chair (facing door)
    // - Spilled coffee mug (liquid decal)
    // - Open newspaper (mid-article)
    // - Keys on floor (dropped, not placed)
    
    // "Last stand" vignette:
    // - Barricaded door (furniture stacked)
    // - Scattered ammunition boxes
    // - Bloody handprint (on wall, at shoulder height)
    // - Radio (on, static - implies calling for help)
    
    // Staging rules:
    // 1. Props face consistent direction (implies person's position)
    // 2. Damage patterns tell sequence (blood trail shows movement)
    // 3. Personal items reveal character (family photo = motivation)
    // 4. Anachronisms jar - keep era consistent
    // 5. Less is more - 3 deliberate props > 30 random ones
    

---
  #### **Name**
Scale Reference and Human Metrics
  #### **Description**
    Include human-scale reference at EVERY stage. A door is 2.1m tall. A step is
    18cm rise, 28cm run. A ceiling is 2.4-3m. Eye height is 1.7m. Without these,
    environments feel "off" in ways players can't articulate. Use mannequin
    references during blockout. Test navigation paths with actual player capsule.
    
  #### **When**
Blockout phase, scale validation, debugging "feels wrong" feedback
  #### **Example**
    // Human metrics reference sheet (all in meters):
    
    // Vertical measurements:
    // Average eye height: 1.7m
    // Door height: 2.1m (minimum), 2.4m (comfortable)
    // Ceiling height: 2.4m (cramped), 3.0m (normal), 4.0m+ (grand)
    // Step rise: 0.15-0.20m
    // Handrail height: 0.9-1.0m
    // Counter/table height: 0.9m (standing), 0.75m (sitting)
    // Chair seat: 0.45m
    
    // Horizontal measurements:
    // Door width: 0.9m (single), 1.5m (double)
    // Corridor width: 1.2m (tight), 2.0m (comfortable)
    // Stair run: 0.28m per step
    // Combat space: 4m x 4m minimum per combatant
    
    // Validation workflow:
    // 1. Drop mannequin/capsule in scene
    // 2. Walk through at player speed
    // 3. Check sightlines at eye height (not camera height!)
    // 4. Test: Can I take cover here? See over this? Fit through that?
    

---
  #### **Name**
Composition Rules for Environment Framing
  #### **Description**
    Apply classical composition to 3D spaces. Rule of thirds for focal placement.
    Leading lines guide the eye (floor patterns, beams, pipes). Framing elements
    (doorways, arches, windows) direct attention. Foreground, midground, background
    layers create depth. The camera IS the player's eye - compose for their view.
    
  #### **When**
Blocking out key vistas, placing hero assets, designing memorable moments
  #### **Example**
    // Composition techniques for environments:
    
    // RULE OF THIRDS:
    // - Place hero prop at 1/3 or 2/3 point, not center
    // - Horizon at 1/3 (emphasize sky) or 2/3 (emphasize ground)
    
    // LEADING LINES:
    // - Floor tile patterns point to objective
    // - Pipes/cables along ceiling guide to exit
    // - Blood trail leads to discovery
    // - Light beams cut through darkness to goal
    
    // FRAMING:
    // - Doorway frames the vista beyond
    // - Arch creates "picture frame" for hero moment
    // - Columns create rhythm and direct eye movement
    
    // DEPTH LAYERS:
    // - Foreground: Silhouette elements, frame the view
    // - Midground: Playable space, interactive elements
    // - Background: Context, vistas, skybox, establishes scale
    
    // Vista checklist:
    // [ ] Clear focal point (squint test passes)
    // [ ] Leading lines present
    // [ ] Foreground/background separation
    // [ ] Human scale reference visible
    // [ ] Reward for looking (detail worth discovering)
    

---
  #### **Name**
Biome Visual Language
  #### **Description**
    Each biome needs a consistent visual vocabulary: color palette, material set,
    silhouette language, vegetation style, atmospheric properties. Document this
    as a "biome bible." When assets cross biomes, blend them at transition zones.
    Biome consistency is what makes large worlds feel cohesive, not chaotic.
    
  #### **When**
Designing open worlds, creating multiple distinct areas, establishing visual identity
  #### **Example**
    // Biome bible example - "Corrupted Forest":
    
    // COLOR PALETTE:
    // - Dominant: Deep purple-black (corruption)
    // - Secondary: Sickly yellow-green (dying foliage)
    // - Accent: Bioluminescent cyan (fungal growths)
    // - Avoid: Healthy greens, warm browns
    
    // MATERIALS:
    // - Trees: Blackened bark, glowing veins
    // - Ground: Cracked earth, purple ooze pools
    // - Rocks: Crystalline corruption growths
    // - Foliage: Wilted, twisted, sparse
    
    // SILHOUETTES:
    // - Trees: Twisted, grasping, no healthy curves
    // - Rocks: Sharp, crystalline, unnatural geometry
    // - Creatures: Corrupted versions of normal fauna
    
    // ATMOSPHERE:
    // - Fog: Low-lying, purple-tinted, volumetric
    // - Particles: Spores, ash, glowing motes
    // - Lighting: Dim ambient, harsh bioluminescence
    // - Skybox: Overcast, sickly green tinge
    
    // TRANSITION TO HEALTHY FOREST:
    // - 50m blend zone
    // - Corruption lessens gradually
    // - Colors shift from purple to natural
    // - Mix of healthy and corrupted assets
    

## Anti-Patterns


---
  #### **Name**
Centering Everything
  #### **Description**
Placing hero assets dead center of the composition
  #### **Why**
    Creates static, boring compositions. The eye has nowhere to travel.
    Real-world spaces have asymmetry. Centered compositions feel artificial
    and like game levels, not real places.
    
  #### **Instead**
    Use rule of thirds. Place heroes at 1/3 points. Create visual tension
    through asymmetry. Let one side be heavier than the other.
    

---
  #### **Name**
Uniform Detail Distribution
  #### **Description**
Spreading detail evenly across all surfaces
  #### **Why**
    Exhausts the eye. No rest areas, no focal points. Everything competes
    for attention, so nothing wins. Also wastes performance budget.
    
  #### **Instead**
    Hero areas get 80% of the detail budget. Secondary 15%. Fill 5%.
    Create visual "breathing room" with simple surfaces.
    

---
  #### **Name**
Scale-less Blockout
  #### **Description**
Gray-boxing without human reference metrics
  #### **Why**
    Without scale reference, artists build to "feeling" which varies wildly.
    Doorways end up 3m tall, steps too steep to animate, ceilings crushing.
    These proportions cement before anyone notices.
    
  #### **Instead**
    Drop a mannequin in EVERY blockout. Test navigation. Measure everything
    against human metrics. Fix scale issues in blockout, not production.
    

---
  #### **Name**
One Material Per Asset
  #### **Description**
Creating unique materials for each modular piece
  #### **Why**
    Destroys batching. A 500-piece kit with 500 materials = 500 draw calls.
    Also guarantees visual inconsistency as each piece develops independently.
    
  #### **Instead**
    Trim sheets and atlases. One master material per kit. Vertex colors for
    variation. 5-10 materials should cover an entire biome.
    

---
  #### **Name**
Ignoring Negative Space
  #### **Description**
Filling every corner with props and detail
  #### **Why**
    Creates visual noise. Players can't read the space. Important elements
    get lost. "Horror vacui" - fear of empty space - is an amateur mistake.
    
  #### **Instead**
    Let walls breathe. Use empty space to frame filled space. Negative space
    IS a design element. The pause between notes makes music.
    

---
  #### **Name**
Texture-Only Storytelling
  #### **Description**
Relying on textures (decals, overlays) instead of 3D staging
  #### **Why**
    Decals are flat. Players in 3D space need 3D narrative. A blood decal
    is less impactful than a blood trail leading to a slumped body. Texture
    storytelling breaks at oblique angles.
    
  #### **Instead**
    Stage 3D vignettes. Use props with physics (fallen chair, not chair decal).
    Decals support 3D storytelling, they don't replace it.
    

---
  #### **Name**
Copy-Paste Without Variation
  #### **Description**
Duplicating assets without rotation, scale, or material variation
  #### **Why**
    Human brains are pattern-detection machines. Identical repeated elements
    scream "fake" and break immersion. Even 5% variation hides repetition.
    
  #### **Instead**
    Rotate Z (90, 180, 270). Scale 95-105%. Vertex color variation. Mirror
    some instances. Random prop swaps within category.
    

---
  #### **Name**
Art Before Gameplay
  #### **Description**
Finalizing art before gameplay is locked
  #### **Why**
    Gameplay changes break art. Level design adjusts, your hero prop is now
    in a wall. Cover spots move, your pristine surface needs holes. Art
    rework is the most expensive rework.
    
  #### **Instead**
    Wait for gameplay lock. Use blockout that's cheap to change. Stage art
    production to follow gameplay milestones. Accept iteration is the job.
    