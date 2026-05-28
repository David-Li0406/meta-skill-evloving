# Voxel Art Expert

## Patterns


---
  #### **Id**
palette-first-workflow
  #### **Name**
Palette-First Design
  #### **Description**
    Design your color palette before modeling a single voxel. The palette defines
    the entire visual identity and dramatically affects readability and mood.
    
  #### **When To Use**
Every voxel project, from the very beginning
  #### **Implementation**
    ## The Palette-First Approach
    
    ### Step 1: Define Palette Purpose
    ```
    READABILITY PALETTE (gameplay-focused):
    - High contrast between gameplay-relevant elements
    - Distinct hues for each material type
    - Limited colors (16-32) for clear silhouettes
    - Reserved colors for UI/highlight states
    
    MOOD PALETTE (aesthetic-focused):
    - Color temperature defines atmosphere
    - Gradients for lighting simulation
    - Earth tones vs saturated for era/setting
    - Accent colors for focal points only
    ```
    
    ### Step 2: Color Distribution Strategy
    ```
    MagicaVoxel 256-color allocation:
    
    RECOMMENDED SPLIT:
    - Base materials:    60-80 colors  (stone, wood, metal variants)
    - Skin/organic:      20-40 colors  (gradients for lighting)
    - Accent/glow:       10-20 colors  (emissive, highlights)
    - Environment:       40-60 colors  (foliage, water, sky)
    - Reserved:          20-40 colors  (future expansion)
    
    KEY RULE: Each material needs 3-5 color variants
    - Shadow tone (30% darker)
    - Mid tone (base color)
    - Highlight tone (30% lighter)
    - Optional: Ambient occlusion tone, reflection tone
    ```
    
    ### Step 3: Contrast for Readability
    ```
    WCAG-inspired contrast rules for voxels:
    
    Primary elements:   Minimum 4.5:1 contrast ratio
    Background elements: Minimum 2:1 contrast ratio
    
    In practice:
    - Player character: Bright, saturated colors
    - Enemies: Contrasting hue from player
    - Collectibles: Complementary or accent colors
    - Environment: Desaturated, lower contrast
    ```
    
    ### Step 4: Import/Export Palette
    ```
    MagicaVoxel:
      Palettes stored in /palette/ folder as 256x1 PNG
      Import: Drag PNG onto palette area
      Export: Right-click palette > Export
    
    Cross-project consistency:
      1. Create master palette PNG
      2. Share across all project files
      3. Update master, re-import to all
      4. Document color indices for scripting
    ```
    
  #### **Examples**
    
---
      ###### **Situation**
Retro game with limited palette
      ###### **Solution**
        ```
        # NES-inspired palette (26 colors)
        
        Skin tones:       3 colors (dark, mid, light)
        Hair:             3 colors (brown variants)
        Clothing primary: 4 colors (including shadow)
        Clothing accent:  3 colors
        Metal:            4 colors (dark to reflective)
        Environment:      6 colors (ground, foliage, sky)
        Effects:          3 colors (hit flash, glow, particle)
        
        # Result: Clear, readable characters with retro charm
        ```
        

---
  #### **Id**
resolution-scale-balance
  #### **Name**
Resolution and Scale Balance
  #### **Description**
    Choose the right voxel resolution for your model's screen size. Higher resolution
    is often WORSE because detail gets lost and performance suffers.
    
  #### **When To Use**
Before starting any voxel model
  #### **Implementation**
    ## Resolution Selection Framework
    
    ### The Fundamental Rule
    ```
    Visible voxel size on screen should be AT LEAST 1-2 pixels
    
    If camera distance makes voxels sub-pixel, you've over-detailed.
    ```
    
    ### Resolution Guidelines by Use Case
    ```
    ICONS/UI (always close-up):
      Resolution: 16x16x16 to 32x32x32
      Why: Every voxel visible, maximum charm
    
    GAME CHARACTERS (medium distance):
      Resolution: 24x24x48 to 48x48x96 (human proportions)
      Why: Silhouette readable, detail visible without noise
    
    ENVIRONMENT PROPS (variable distance):
      Resolution: 16x16x16 to 64x64x64
      Why: Must work at multiple distances
    
    LARGE BUILDINGS (far distance):
      Resolution: 64x64x64 to 128x128x128 max
      Why: Individual voxels not visible; focus on shape
    
    DESTRUCTIBLE TERRAIN (performance-critical):
      Resolution: 8x8x8 to 32x32x32 per chunk
      Why: Physics cost per voxel is significant
    ```
    
    ### The Screen Size Test
    ```
    Before finalizing resolution:
    
    1. Place model in actual game engine
    2. Position camera at TYPICAL gameplay distance
    3. Take screenshot at target resolution
    4. If individual voxels aren't distinct = too high res
    5. If model is blobby/unreadable = too low res
    
    SWEET SPOT: Each voxel = 2-4 screen pixels
    ```
    
    ### Character Proportions at Different Scales
    ```
    16-voxel tall character:
      Head:  4-5 voxels
      Torso: 5-6 voxels
      Legs:  6-7 voxels
      Arms:  1 voxel wide
    
    32-voxel tall character:
      Head:  8-10 voxels
      Torso: 10-12 voxels
      Legs:  12-14 voxels
      Arms:  2 voxels wide
    
    48-voxel tall character:
      Head:  12-15 voxels
      Torso: 15-18 voxels
      Legs:  18-21 voxels
      Arms:  3 voxels wide
    ```
    

---
  #### **Id**
silhouette-driven-modeling
  #### **Name**
Silhouette-Driven Modeling
  #### **Description**
    Voxels have limited resolution - the silhouette is your primary communication tool.
    Model for silhouette first, detail second.
    
  #### **When To Use**
All voxel character and prop design
  #### **Implementation**
    ## Silhouette-First Approach
    
    ### Why Silhouette Matters More in Voxels
    ```
    In traditional 3D:
      - Unlimited polygon resolution for curves
      - Textures add detail at any scale
      - Lighting creates form on smooth surfaces
    
    In voxels:
      - Fixed grid resolution limits curves
      - "Texture" is just more voxels
      - Stair-stepping breaks smooth lighting
    
    RESULT: The shape itself carries the message
    ```
    
    ### The Silhouette Test
    ```
    1. Fill your model with a single solid color
    2. View from all cardinal directions (6 views)
    3. View from all diagonal directions (8 views)
    4. Ask: "Can I identify this without color or detail?"
    
    If NO: Exaggerate the silhouette before adding detail
    ```
    
    ### Exaggeration Techniques
    ```
    HEADS: Make them 1.5-2x larger than realistic
      - Draws eye to face
      - More room for expression
      - Classic cartoon proportion
    
    HANDS: Make them 1.5x larger than realistic
      - Important for tool-using characters
      - Easier to animate visibly
    
    WEAPONS/TOOLS: Oversized relative to body
      - Must read at gameplay distance
      - Silhouette defines tool type
    
    SHOULDER WIDTH: Slightly exaggerate
      - Creates heroic proportions
      - Distinguishes from NPCs
    ```
    
    ### The Rayman Aesthetic
    ```
    A breakthrough in voxel character design:
    
    Instead of connected limbs:
      - Floating hands (no arms)
      - Floating feet (no legs, or short legs)
      - Focus detail on head, hands, torso
    
    Benefits:
      - Fewer voxels = better performance
      - No awkward arm/leg articulation
      - Cleaner silhouette in motion
      - Easier animation (fewer parts)
    
    Games using this: Crossy Road, many mobile voxel games
    ```
    

---
  #### **Id**
frame-by-frame-animation
  #### **Name**
Frame-by-Frame Voxel Animation
  #### **Description**
    Voxel animation uses stop-motion principles, not skeletal rigging. Each frame
    is a complete voxel model, creating a unique aesthetic but significant storage.
    
  #### **When To Use**
Any animated voxel content
  #### **Implementation**
    ## Frame-by-Frame Animation Pipeline
    
    ### Why Not Skeletal Animation?
    ```
    Traditional skeletal issues in voxels:
      - Rotation causes voxel "swimming"
      - Scaling creates jagged artifacts
      - Blend weights meaningless on cubes
      - Loses the voxel charm
    
    Frame-by-frame advantages:
      - Perfect control over every voxel
      - Classic stop-motion aesthetic
      - Snappy, readable motion
      - No runtime deformation cost
    ```
    
    ### Key Frame Planning
    ```
    WALK CYCLE (8 frames typical):
      Frame 1: Contact (front foot down)
      Frame 2: Recoil (body dips)
      Frame 3: Passing (legs cross)
      Frame 4: High point (back foot lifts)
      Frame 5: Contact (opposite foot)
      Frames 6-8: Mirror of 1-4
    
    IDLE ANIMATION (4-8 frames):
      - Subtle breathing motion
      - Hold key poses for 2 frames (overlap effect)
      - Small head movements
      - Tool/weapon bob
    
    ATTACK (3-6 frames):
      Frame 1: Anticipation (wind-up)
      Frame 2-3: Action (strike)
      Frame 4-5: Follow-through
      Frame 6: Recovery
    ```
    
    ### Overlap and Delay Technique
    ```
    Traditional animation principle adapted:
    
    When hand reaches extreme position:
      - Hold for 2 frames before reversing
      - Body and legs continue moving
      - Creates "drag" feeling
    
    Implementation:
      Frame 4: Hand at left extreme, torso centered
      Frame 5: Hand at left extreme (held), torso moves right
      Frame 6: Hand starts right, torso at right extreme
    ```
    
    ### Storage and Performance Considerations
    ```
    Frame storage calculation:
      Model size: 32x32x32 = 32,768 voxels
      Frames per animation: 8
      Animations per character: 10
      Total voxels: 32,768 x 8 x 10 = 2.6 million voxels
    
    Optimization strategies:
      1. DELTA FRAMES: Store only changed voxels per frame
      2. SHARED PALETTES: All frames use same 256-color palette
      3. RLE COMPRESSION: Run-length encode empty space
      4. SPRITE SHEETS: For 2D games, render to sprite sheets
    
    Runtime approach:
      - Precompile animations to mesh sequences
      - Swap meshes per frame (model swapping)
      - Or: Use vertex animation textures (VAT)
    ```
    
    ### MagicaVoxel Animation Workflow
    ```
    Naming convention:
      character_idle_01.vox
      character_idle_02.vox
      character_walk_01.vox
      ...
    
    Quick preview in MagicaVoxel:
      1. Name files sequentially (walk1, walk2, walk3)
      2. Click through files quickly in file browser
      3. For accurate preview, export to Maya or use AniVoxel
    
    Export for game:
      1. Export each frame as OBJ
      2. Import to Blender as sequence
      3. Set up mesh swapping animation
      4. Export as FBX with shape keys or separate meshes
    ```
    

---
  #### **Id**
mesh-conversion-optimization
  #### **Name**
Voxel-to-Mesh Conversion
  #### **Description**
    Converting voxels to game-ready meshes requires understanding marching cubes,
    greedy meshing, and the tradeoffs between polygon count and visual fidelity.
    
  #### **When To Use**
Exporting voxel models for game engines
  #### **Implementation**
    ## Mesh Conversion Methods
    
    ### Method 1: Naive/Cubic Export
    ```
    Every voxel = 12 triangles (6 faces x 2 tris)
    
    32x32x32 solid cube = 32,768 voxels = 393,216 triangles
    (Unusable for real-time!)
    
    When to use:
      - Never for filled volumes
      - Only for single-voxel effects
    ```
    
    ### Method 2: Face Culling
    ```
    Only render external faces (faces not touching other voxels)
    
    32x32x32 hollow shell = ~6,000 visible faces = ~12,000 triangles
    (Much better, but still not optimized)
    
    MagicaVoxel uses this by default for OBJ export
    ```
    
    ### Method 3: Greedy Meshing (RECOMMENDED)
    ```
    Combine adjacent coplanar faces into larger quads
    
    How it works:
      1. Find largest rectangle of same-color voxels
      2. Merge into single quad
      3. Repeat for remaining faces
    
    Result:
      32x32x32 with greedy = 100-500 triangles (varies by complexity)
      95%+ reduction from face culling!
    
    Tools that support greedy meshing:
      - Optivox (dedicated voxel optimizer)
      - Avoyd Voxel Editor
      - Custom scripts (0fps.net has reference implementation)
    
    Limitation:
      - All merged voxels must be SAME material/color
      - Different colors = different quads
    ```
    
    ### Method 4: Marching Cubes (Smooth Voxels)
    ```
    Creates smooth surfaces from voxel data
    
    Pros:
      - Rounded, organic shapes
      - Good for terrain
      - Natural-looking results
    
    Cons:
      - Loses blocky voxel aesthetic
      - Can create artifacts at sharp edges
      - Higher polygon count
      - Coplanar face issues (see sharp-edges)
    
    MagicaVoxel: Export > Marching Cubes option
    
    Best for:
      - Terrain that should look natural
      - Organic shapes (clouds, rocks)
      - When you DON'T want the voxel look
    ```
    
    ### Optimization Pipeline (Recommended)
    ```
    1. Export from MagicaVoxel as OBJ (face culled)
    2. Import to Blender
    3. Apply Limited Dissolve (merge coplanar)
    4. Apply Decimate modifier (for LODs)
    5. Export as FBX/glTF
    
    Blender optimization script:
      bpy.ops.mesh.dissolve_limited(angle_limit=0.0001)
      bpy.ops.mesh.tris_to_quads()
    
    Expected results:
      Original:      10,000 triangles
      After dissolve: 500-2,000 triangles
      LOD1 (50%):    250-1,000 triangles
      LOD2 (25%):    125-500 triangles
    ```
    

---
  #### **Id**
destructible-voxel-design
  #### **Name**
Destructible Voxel Systems
  #### **Description**
    Designing voxel content for destruction requires understanding structural
    integrity, chunk management, and physics performance.
    
  #### **When To Use**
Teardown-style destruction, mining games, building games
  #### **Implementation**
    ## Destructible Voxel Architecture
    
    ### Teardown's Approach (Lessons Learned)
    ```
    Key insight from Dennis Gustafsson:
      "Destructible voxels are easier than polygons because
       they're so much easier to work with for physics."
    
    Implementation:
      - Multiple small voxel volumes, not one giant volume
      - Each volume can translate independently
      - 8-bit color palette per material
      - Ray marching for rendering (not polygon conversion)
    
    Why multiple volumes:
      - Local translation when piece breaks off
      - Chunk-based physics simulation
      - Memory management (load/unload chunks)
    ```
    
    ### Structural Integrity Basics
    ```
    The problem:
      - Remove support voxels, structure should collapse
      - But computing full structural analysis is expensive
    
    Teardown's compromise:
      - Small structures: Accurate structural integrity
      - Large structures: Simplified approximation
      - Reason: Computational cost doesn't scale
    
    For your game:
      Option 1: Simple connectivity (cheap)
        - Flood fill from ground
        - Disconnected = falls
    
      Option 2: Stress simulation (expensive)
        - Weight flows through structure
        - Overloaded supports break
        - More realistic but costly
    
      Option 3: Teardown hybrid
        - Simple for large
        - Detailed for small pieces
        - Threshold determines cutoff
    ```
    
    ### Chunk-Based World Management
    ```
    Don't store as single volume:
      - 512x512x256 world = 67 million voxels
      - Too large for memory
      - Can't update efficiently
    
    Chunk approach:
      - Divide into 32x32x32 chunks
      - Only load visible chunks
      - Regenerate mesh when chunk modified
    
    Chunk modification workflow:
      1. Player destroys voxel
      2. Identify affected chunk
      3. Update chunk voxel data
      4. Flag chunk for re-mesh
      5. Regenerate mesh (background thread)
      6. Swap old mesh for new
    
    Target: <1ms for re-mesh (from Fugl developer)
    ```
    
    ### Material Properties for Destruction
    ```
    8-bit palette approach (per voxel):
      Bits 0-5: Color index (64 colors)
      Bits 6-7: Material type (4 types)
    
    Material types affect:
      - Destruction resistance (hits to break)
      - Debris behavior (crumble vs shatter)
      - Sound on impact
      - Physics properties (density, friction)
    
    Example materials:
      Type 0: Stone  (high resistance, crumble)
      Type 1: Wood   (medium resistance, splinter)
      Type 2: Metal  (high resistance, dent then break)
      Type 3: Glass  (low resistance, shatter)
    ```
    

---
  #### **Id**
game-engine-integration
  #### **Name**
Game Engine Export Pipeline
  #### **Description**
    Complete workflow for getting voxel art into Unity, Unreal, and Godot with
    proper materials, collision, and optimization.
    
  #### **When To Use**
Exporting voxel assets for game engines
  #### **Implementation**
    ## Export Pipeline by Engine
    
    ### MagicaVoxel to Unity
    ```
    STEP 1: Export from MagicaVoxel
      Format: OBJ (includes MTL and PNG palette)
      Settings: Default (face culled)
    
    STEP 2: Optimize in Blender (optional but recommended)
      - Import OBJ
      - Apply Limited Dissolve
      - Create LODs with Decimate modifier
      - Export as FBX
    
    STEP 3: Unity Import Settings
      Model:
        - Scale Factor: 1 (if modeled at correct scale)
        - Import Normals: Import
        - Generate Lightmap UVs: YES (important!)
    
      Materials:
        - Create new Material
        - Base Map: Use exported palette PNG
        - Ensure: Unlit or appropriate shader
    
    STEP 4: Collision
      - Generate Colliders: Mesh Collider (static)
      - For dynamic: Create simplified box/capsule
    ```
    
    ### MagicaVoxel to Unreal Engine
    ```
    STEP 1: Export as OBJ or FBX
      OBJ for static meshes
      FBX if need hierarchy
    
    STEP 2: Import to Unreal
      Import Settings:
        - Convert Scene: ON
        - Import Normals: Import Normals and Tangents
        - Auto Generate Collision: ON (simple)
    
    STEP 3: Material Setup
      1. Create Material Instance
      2. Base Color: Sample palette texture
      3. For crisp voxels: Disable mip maps on texture
      4. Nearest neighbor filtering (no blur)
    
    STEP 4: LOD Setup
      - Import LOD meshes with _LOD0, _LOD1, etc. suffix
      - Or generate in Unreal (less control)
      - Set LOD distances based on screen percentage
    ```
    
    ### MagicaVoxel to Godot
    ```
    STEP 1: Export as glTF (preferred) or OBJ
      glTF preserves more material data
    
    STEP 2: Blender Intermediate (recommended)
      - Import to Blender
      - Optimize mesh
      - Export as glTF (.glb)
    
    STEP 3: Godot Import
      Import dock settings:
        - Generate Collision: Convex (dynamic) or Trimesh (static)
        - Generate Lightmap UV: ON
    
    STEP 4: Material
      - Godot auto-creates material from glTF
      - Modify: Set texture filter to Nearest (no blur)
      - For pixel-perfect: Disable mipmaps
    ```
    
    ### Texture Settings for Crisp Voxels
    ```
    The cardinal sin: Blurry voxels from texture filtering
    
    FIX in all engines:
      - Filter Mode: Point (Nearest Neighbor)
      - Generate Mipmaps: OFF
      - Compression: None or Lossless
    
    Without this, voxel edges blur together at angles
    ```
    

## Anti-Patterns


---
  #### **Id**
overdetailing-small-scale
  #### **Name**
Over-Detailing at Small Scale
  #### **Description**
    Adding detail that won't be visible at the camera distance the asset will
    be viewed from. This wastes voxels, increases polygon count, and often
    makes the model LESS readable.
    
  #### **Why Bad**
    - Detail becomes visual noise at distance
    - Increases polygon count for no benefit
    - Reduces silhouette clarity
    - Wastes artist time
    - Can make characters look "dirty" or cluttered
    
  #### **What To Do Instead**
    1. Always test at actual gameplay camera distance
    2. Use color variation instead of geometry for detail
    3. Follow the 2-4 pixel per voxel rule
    4. Exaggerate important features, simplify unimportant ones
    5. "Would I see this at 50% zoom?" If no, remove it.
    

---
  #### **Id**
ignoring-palette-design
  #### **Name**
Using Random Colors
  #### **Description**
    Picking colors without a cohesive palette plan, leading to muddy,
    unreadable, or jarring visual results.
    
  #### **Why Bad**
    - Lacks visual cohesion
    - Makes silhouettes harder to read
    - Limits reuse across models
    - Professional voxel art always uses curated palettes
    - Makes material identification difficult
    
  #### **What To Do Instead**
    1. Design palette BEFORE modeling
    2. Limit to 16-64 colors for consistency
    3. Group colors by material type
    4. Include shadow/highlight variants per color
    5. Reference classic palettes (NES, CGA, custom curated)
    

---
  #### **Id**
mesh-export-without-optimization
  #### **Name**
Exporting Without Mesh Optimization
  #### **Description**
    Exporting voxel models directly to game engines without applying greedy
    meshing or face optimization, resulting in massive polygon counts.
    
  #### **Why Bad**
    - 10x-100x more polygons than necessary
    - Kills game performance
    - Larger file sizes
    - Slower load times
    - Can't have many voxel objects on screen
    
  #### **What To Do Instead**
    1. Use Optivox or Avoyd for automatic greedy meshing
    2. Or import to Blender and apply Limited Dissolve
    3. Create proper LOD chain
    4. Test polygon count before shipping
    5. Target: <1000 tris for small props, <5000 for characters
    

---
  #### **Id**
animation-storage-explosion
  #### **Name**
Ignoring Animation Storage Costs
  #### **Description**
    Creating many animation frames without considering the exponential storage
    and memory costs of frame-by-frame voxel animation.
    
  #### **Why Bad**
    - Each frame is a full copy of the model
    - 8-frame walk cycle = 8x storage of static model
    - 10 animations = 80x storage
    - Mobile games can't handle this
    - Increases load times dramatically
    
  #### **What To Do Instead**
    1. Plan animation count before production
    2. Use delta compression (store only changes)
    3. Consider sprite sheet rendering for mobile
    4. Limit frame count (4-6 frames often enough)
    5. Share animations across similar characters
    

---
  #### **Id**
marching-cubes-for-blocky
  #### **Name**
Using Marching Cubes for Blocky Aesthetic
  #### **Description**
    Using marching cubes export when you want to preserve the blocky voxel look,
    destroying the intentional aesthetic.
    
  #### **Why Bad**
    - Removes the voxel charm
    - Looks like generic low-poly 3D
    - Higher polygon count than necessary
    - Introduces mesh artifacts
    - Defeats the purpose of voxel art
    
  #### **What To Do Instead**
    1. Use standard OBJ export for blocky look
    2. Apply greedy meshing to optimize
    3. Only use marching cubes for terrain or organic shapes
    4. If smooth is needed, consider starting with traditional 3D instead
    

---
  #### **Id**
ignoring-camera-distance
  #### **Name**
Designing Without Camera Context
  #### **Description**
    Creating voxel models without considering the actual camera distance and
    resolution they'll be viewed at in the final game.
    
  #### **Why Bad**
    - Detail invisible at gameplay distance
    - Models may be too small or too large
    - Voxels become sub-pixel (wastes resolution)
    - Visual identity gets lost
    
  #### **What To Do Instead**
    1. Set up test scene with actual game camera
    2. Model at visible resolution only
    3. Test frequently at final view distance
    4. Adjust model resolution based on screen size
    