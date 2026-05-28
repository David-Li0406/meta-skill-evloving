# Environment Art - Sharp Edges

## Envart Tiling Artifacts

### **Id**
envart-tiling-artifacts
### **Summary**
Visible texture tiling patterns destroying immersion
### **Severity**
high
### **Situation**
  Large surfaces show obvious repeating patterns. Players see the "grid"
  where textures tile. Especially visible on floors, walls, and terrain.
  
### **Why**
  Seamless textures still have recognizable features that repeat. Human
  pattern recognition is incredibly strong - we evolved to spot repeating
  patterns (predator camouflage detection). Without breaking techniques,
  tiling is always visible on large surfaces.
  
### **Solution**
  Multiple approaches (use together for best results):
  
  1. MACRO VARIATION LAYER: Overlay a large-scale grunge/color variation
     texture at 0.1x tiling rate. Blends via multiply or overlay.
  
  2. STOCHASTIC TILING: Shader that randomly offsets and rotates each
     tile. Requires handling seam blending at tile boundaries.
  
  3. VERTEX COLOR VARIATION: Paint vertex colors to blend between
     clean/dirty versions at random intervals.
  
  4. DETAIL NORMAL BREAK-UP: Add a micro-detail normal at 10x tiling
     that adds noise to the surface, hiding macro repetition.
  
  5. DECAL LAYERING: Strategic decal placement breaks pattern recognition.
     Dirt at corners, stains at random, damage where logical.
  
  6. UV ROTATION: Rotate UVs 90 degrees on alternating pieces. Same
     texture, different orientation hides repetition.
  
### **Symptoms**
  - I can see where the texture repeats
  - Grid pattern visible on floors
  - Walls look like wallpaper
  - Terrain has obvious squares
### **Detection Pattern**
tiling.*artifact|repeating.*texture|visible.*seam
### **Version Range**
all

## Envart Scale Inconsistency

### **Id**
envart-scale-inconsistency
### **Summary**
Assets at wrong scale break spatial believability
### **Severity**
critical
### **Situation**
  Door handles are fist-sized. Stairs are too steep to climb. Ceiling
  feels crushing. Props look toy-like or gigantic. "Something feels wrong"
  but can't articulate what.
  
### **Why**
  Without human reference during modeling, artists work to "feeling" rather
  than measurement. Each artist's intuition differs. Small errors compound:
  a door 10% too big means doorframe 10% too big, means wall 10% too big,
  means the whole building is wrong.
  
### **Solution**
  1. REFERENCE MANNEQUIN: Every scene needs a scale mannequin. Not hidden
     in a corner - visible in every viewport during work.
  
  2. REAL-WORLD MEASUREMENT: Measure actual objects. Your door at home is
     2.0-2.1m. Your ceiling is 2.4m. Your desk is 0.75m. Use these numbers.
  
  3. MODELING CHECKLIST: Before export, check:
     - Door: 2.1m tall, 0.9m wide
     - Step: 0.18m rise, 0.28m run
     - Ceiling: 2.4-3.0m from floor
     - Counter: 0.9m height
     - Handrail: 0.9-1.0m height
  
  4. FIRST-PERSON CAMERA TEST: Walk through in-engine at player eye height
     (1.7m). Does it feel right? Can you see over counters? Under tables?
  
  5. BLOCKOUT SIGN-OFF: Lock scale in blockout phase. Don't let production
     assets deviate. If blockout was wrong, fix it before art.
  
### **Symptoms**
  - Environment feels "off" but can't explain
  - Players report motion sickness (scale affects proprioception)
  - Animations don't fit (sitting through chairs, floating on beds)
  - Doorways feel too small/large
### **Detection Pattern**
scale.*wrong|proportion.*off|feels.*weird|too.*big|too.*small
### **Version Range**
all

## Envart Z Fighting

### **Id**
envart-z-fighting
### **Summary**
Flickering surfaces from co-planar geometry
### **Severity**
high
### **Situation**
  Two surfaces at the same position flicker between each other. Decals
  z-fight with base geometry. Overlapping modular pieces show seams
  that appear and disappear as camera moves.
  
### **Why**
  Depth buffers have finite precision. When two surfaces are at "the same"
  depth, floating-point rounding means the winner varies per-pixel and
  per-frame. The closer to camera, and the larger the near-far ratio,
  the worse it gets.
  
### **Solution**
  1. OFFSET DECALS: Decals should be 0.01-0.1 units off the surface.
     Use polygon offset in shader if supported.
  
  2. AVOID CO-PLANAR: Modular pieces shouldn't share the same plane.
     Inset wall panels by 2-4 units. Offset trim by 1-2 units.
  
  3. CAMERA SETTINGS: Push near clip plane as far as possible (0.1m not
     0.001m). Pull far clip in (1000m not 100000m).
  
  4. 32-BIT DEPTH: If available, use 32-bit depth buffer instead of 24-bit.
     Significant precision improvement.
  
  5. REVERSED-Z: Reverse depth buffer (1 at near, 0 at far) for better
     precision distribution. Most modern engines support this.
  
  6. MERGE GEOMETRY: If two planes must touch, merge them into one mesh.
     No depth test within a single triangle.
  
### **Symptoms**
  - Flickering surfaces
  - Decals appear to "swim" on surfaces
  - Seams appear/disappear with camera movement
  - Visual noise on distant co-planar objects
### **Detection Pattern**
z-fight|flicker|co-?planar|depth.*fight
### **Version Range**
all

## Envart Collision Mismatch

### **Id**
envart-collision-mismatch
### **Summary**
Physics collision doesn't match visual geometry
### **Severity**
critical
### **Situation**
  Player gets stuck on invisible geometry. Bullets hit nothing visible.
  Player walks through seemingly solid objects. Grenades bounce off air.
  AI navigation fails near complex geometry.
  
### **Why**
  Collision meshes are often auto-generated and not validated. High-poly
  visuals with simplified collision leave gaps. LOD switches change visual
  but not collision. Some platforms can't handle concave collision.
  
### **Solution**
  1. EXPLICIT COLLISION MESHES: Create simple collision geo by hand for
     hero and modular assets. Don't trust auto-generation.
  
  2. COLLISION VISUALIZATION: Enable collision view in-engine. Walk
     through and verify visually before shipping.
  
  3. CONVEX DECOMPOSITION: If engine requires convex collision, break
     complex shapes into convex pieces. Test the seams.
  
  4. COLLISION NAMING: Use consistent naming (_collision, _UCX) so
     pipeline correctly identifies collision geo.
  
  5. LOD COLLISION: Higher LODs should NOT have higher-detail collision.
     Collision is LOD-independent.
  
  6. PLAYTEST PROTOCOL: Every environment needs a collision walkthrough.
     Hug every wall. Jump on every surface. Throw projectiles at edges.
  
### **Symptoms**
  - I got stuck on nothing
  - Invisible walls
  - Walking through solid objects
  - Projectiles hit invisible barriers
  - AI pathing failures near complex geo
### **Detection Pattern**
collision.*mismatch|stuck.*invisible|walk.*through|hit.*nothing
### **Version Range**
all

## Envart Draw Call Explosion

### **Id**
envart-draw-call-explosion
### **Summary**
Too many draw calls killing frame rate
### **Severity**
critical
### **Situation**
  Frame rate tanks in dense environments. GPU profiler shows draw call
  count in thousands. Modular environments especially affected. Each
  unique material/mesh combination adds draw calls.
  
### **Why**
  Each material instance on each mesh is a draw call. 100 props with 10
  materials each = potentially 1000 draw calls. Modular environments
  multiply this: 500 wall pieces x unique materials = GPU stall.
  
### **Solution**
  1. MATERIAL ATLASING: One material per kit. Trim sheets, texture atlases.
     500 modular pieces, 1 material = batchable.
  
  2. MESH MERGING: Combine static geo in-engine. Unreal: Merge Actors.
     Unity: Static Batching. Trade memory for draw calls.
  
  3. INSTANCING: Same mesh + same material = 1 draw call with instancing.
     Enable GPU instancing on materials. Use instanced foliage.
  
  4. LOD AGGRESSIVENESS: Aggressive LOD reduces both poly count AND draw
     calls (simpler meshes = more batching opportunity).
  
  5. OCCLUSION CULLING: Don't draw what's not visible. Bake occlusion.
     Use manual occluder volumes in complex areas.
  
  6. HIERARCHICAL DETAIL: Group props into "set dressing islands" that
     cull as a unit. One bounds check instead of 50.
  
  7. MATERIAL COMPLEXITY: Simpler shaders draw faster. Background assets
     don't need 20-layer materials.
  
### **Symptoms**
  - Low FPS in dense areas
  - GPU bound (CPU waiting on GPU)
  - Draw call count in profiler > 2000
  - Frame time spikes when looking at detailed areas
### **Detection Pattern**
draw.*call|batch.*fail|too.*many.*materials|fps.*drop
### **Version Range**
all

## Envart Over Cluttering

### **Id**
envart-over-cluttering
### **Summary**
Too much detail destroys visual readability
### **Severity**
high
### **Situation**
  Every surface has detail. Every corner has props. The eye has nowhere
  to rest. Important gameplay elements get lost. Screenshots look noisy.
  Players report feeling overwhelmed or anxious.
  
### **Why**
  "Horror vacui" - fear of empty space - leads to filling every gap. Each
  artist adds "just one more thing." Without clear hierarchy, visual noise
  accumulates. What should be supporting detail becomes competing noise.
  
### **Solution**
  1. THE SQUINT TEST: Blur your eyes. Is there a clear focal point? If not,
     remove detail until there is.
  
  2. 80/20 RULE: 80% of player attention goes to 20% of the space. That 20%
     gets the detail. The other 80% supports it.
  
  3. NEGATIVE SPACE: Empty space is design. The gap between props is as
     important as the props. Let walls breathe.
  
  4. DETAIL BUDGET: Set a prop budget per square meter. Kitchen: 5 props/m2.
     Hallway: 1 prop/m2. Stick to it.
  
  5. HIERARCHY ENFORCEMENT: Mark each prop as Primary, Secondary, or Fill.
     If ratio isn't 1:3:6, you have too many primaries.
  
  6. REMOVE THEN ADD: Start with nothing. Add only what's necessary. It's
     easier to add than remove (sunk cost fallacy).
  
  7. PLAYTESTER EYES: Watch new players. Where do they look? If they miss
     critical info, remove clutter around it.
  
### **Symptoms**
  - I can't find the [objective]
  - Screenshots look messy
  - Players report fatigue in detailed areas
  - Gameplay elements get lost
### **Detection Pattern**
too.*much.*detail|cluttered|can.*t.*find|visual.*noise
### **Version Range**
all

## Envart Pivot Origin

### **Id**
envart-pivot-origin
### **Summary**
Wrong pivot points break modular snapping
### **Severity**
critical
### **Situation**
  Modular pieces don't snap together cleanly. Small gaps appear between
  wall segments. Floor tiles offset by tiny amounts. Artists spend hours
  manually adjusting positions that should auto-align.
  
### **Why**
  Game engines import pivot points based on model origin (0,0,0) in the
  DCC tool. If your mesh isn't positioned correctly relative to origin,
  the in-engine pivot will be wrong. Center pivot = center snapping, not
  corner snapping. Modular kits MUST have corner pivots.
  
### **Solution**
  1. CORNER PIVOT WORKFLOW:
     - Model asset at any location
     - Move mesh so bottom-left-front corner is at origin (0,0,0)
     - Do NOT move pivot (pivot stays at origin)
     - Export - engine receives mesh with corner at pivot
  
  2. DCC SETUP: In Maya/Max/Blender, make the grid visible and snap
     vertices to grid before export. Use power-of-2 grid size.
  
  3. VALIDATION SCRIPT: Write export validation that checks:
     - Asset bounding box starts at or near origin
     - Dimensions are power-of-2 friendly
     - No geometry in negative coordinates
  
  4. IN-ENGINE TEST: Drop two pieces side by side. Snap by pivot.
     Zero gap = correct. Any gap = pivot is wrong.
  
  5. PIVOT CONVENTION: Document your convention. All walls: bottom-left.
     All floors: center. All props: base center. Consistency is key.
  
### **Symptoms**
  - Gaps between modular pieces
  - Pieces overlap when snapped
  - Manual adjustment constantly needed
  - The pivot is in the wrong place
### **Detection Pattern**
pivot.*wrong|snap.*not.*work|gap.*between|modular.*offset
### **Version Range**
all

## Envart Memory Budget

### **Id**
envart-memory-budget
### **Summary**
Textures and meshes exceeding memory budget
### **Severity**
high
### **Situation**
  Level fails to load on target platform. Texture streaming stutters.
  Out of memory crashes. VRAM budget exceeded. Console certification
  fails due to memory usage.
  
### **Why**
  Art teams work on powerful workstations. What runs on 32GB + 12GB VRAM
  doesn't run on a console with 8GB unified. Each 4K texture is 64MB
  uncompressed. Meshes with millions of triangles add up. No one tracks
  budget until it's too late.
  
### **Solution**
  1. PLATFORM BUDGETS: Know your target early:
     - PS5/Xbox Series: ~5GB for textures, ~2GB for meshes (rough)
     - PS4/Xbox One: ~2GB textures, ~1GB meshes
     - Mobile: ~256MB textures, ~128MB meshes
     - Set level budgets from these.
  
  2. TEXTURE SIZE DISCIPLINE:
     - Hero assets: 2K (2048x2048)
     - Secondary: 1K (1024x1024)
     - Props: 512x512
     - Background: 256x256
     - Trim sheets: 2K shared across kit
  
  3. STREAMING PRIORITY: Not everything needs full-res at once. Background
     elements can stream in lower. Prioritize what's close.
  
  4. LOD MESH REDUCTION: LOD0 full poly. LOD1 50%. LOD2 25%. LOD3 10%.
     Aggressive transition distances.
  
  5. SHARED RESOURCES: One dirt decal atlas, not 50 dirt decals. One sky
     HDRI, not per-level. One foliage atlas per biome.
  
  6. PROFILING ROUTINE: Check memory usage weekly during production. Don't
     wait for end. Overages caught early are fixable.
  
### **Symptoms**
  - Out of memory crashes
  - Texture pop-in/streaming issues
  - Console certification failures
  - Slow level loading
### **Detection Pattern**
memory.*budget|out.*of.*memory|texture.*too.*large|VRAM
### **Version Range**
all

## Envart Non Power Of 2

### **Id**
envart-non-power-of-2
### **Summary**
Non-power-of-2 textures causing waste and artifacts
### **Severity**
medium
### **Situation**
  Textures sized 1000x1000 or 2000x1500. GPU padding wastes memory.
  Mipmap generation fails or produces artifacts. Compression formats
  don't work correctly. Older hardware refuses to load.
  
### **Why**
  GPUs are optimized for power-of-2 dimensions (256, 512, 1024, 2048).
  Non-POT textures get padded to next POT, wasting memory. Some compression
  formats (BC/DXT) require POT or multiple-of-4. Mipmaps halve dimensions -
  non-POT creates odd sizes.
  
### **Solution**
  1. ALWAYS POT: 256, 512, 1024, 2048, 4096. No exceptions. Non-square is
     fine (1024x512) as long as both dimensions are POT.
  
  2. VALIDATION SCRIPT: Check texture dimensions on export/import. Flag
     any non-POT textures.
  
  3. RESIZE, DON'T PAD: If source is 1000x1000, resize to 1024x1024. Don't
     let the engine pad it (you control quality loss, not the engine).
  
  4. TRIM SHEET PLANNING: Design trim sheets to POT from the start. Not
     "whatever fits" - exactly 2048x2048 with planned strip heights.
  
  5. ATLAS OPTIMIZATION: Pack atlases to exactly fill POT dimensions.
     Wasted atlas space = wasted memory.
  
### **Symptoms**
  - Unexplained memory usage
  - Mipmap artifacts
  - Compression failures
  - "Texture dimensions not supported" errors
### **Detection Pattern**
non.*power.*of.*2|texture.*size|mipmap.*artifact|padding
### **Version Range**
all

## Envart Skybox Seams

### **Id**
envart-skybox-seams
### **Summary**
Visible seams in skybox at cube edges
### **Severity**
medium
### **Situation**
  When looking up or at horizon, visible lines appear at skybox cube
  edges. Seams are more visible at certain times of day. Clouds don't
  wrap correctly. Stars show obvious grid.
  
### **Why**
  Cubemap skyboxes have 6 faces that must align perfectly. Any color
  difference at edges is visible. Filtering at edges can sample the wrong
  face. Procedural elements (clouds, stars) may not tile across edges.
  
### **Solution**
  1. HDRI CAPTURE: Use spherical HDRI projected to cubemap. Natural scenes
     don't have edges. Re-project at highest quality.
  
  2. EDGE SAMPLING: Enable seamless cubemap sampling in shader. Most
     engines have this option - ensure it's on.
  
  3. PROCEDURAL WRAPPING: Procedural clouds/stars must wrap. Test by
     rotating 90 degrees on each axis - seams should never appear.
  
  4. MANUAL TOUCH-UP: In Photoshop, manually paint over seam areas across
     unfolded cubemap. Match colors exactly.
  
  5. HIGHER RESOLUTION: Seams are more visible in low-res cubemaps. 4K
     per face minimum for production. 8K for hero moments.
  
  6. AVOID SKYBOX FOCUS: If seam fixing is hard, don't let players look
     directly at it. Use terrain/geometry to obscure horizon.
  
### **Symptoms**
  - Visible lines in sky
  - Seams at cube edges
  - Clouds cutting off at edges
  - Stars showing grid pattern
### **Detection Pattern**
skybox.*seam|cube.*edge|sky.*line|visible.*edge
### **Version Range**
all

## Envart Lightmap Bleeding

### **Id**
envart-lightmap-bleeding
### **Summary**
Light bleeding through walls in baked lighting
### **Severity**
high
### **Situation**
  Light from outside appears inside. Dark rooms have unexplained bright
  spots on walls. Colors from adjacent areas bleed through. Shadows have
  bright halos.
  
### **Why**
  Lightmap UV islands need padding to prevent texture filtering from
  sampling adjacent islands. If padding is insufficient, the lightmap
  bake bleeds across UV boundaries. Also, geometry without thickness
  allows light through.
  
### **Solution**
  1. UV ISLAND PADDING: Minimum 4 texels padding at lowest mip level.
     For 512 lightmap, that's about 0.8% UV space per edge.
  
  2. GEOMETRY THICKNESS: Walls must have thickness (32+ units). Single-
     sided planes are never lightmap-safe.
  
  3. LIGHTMASS SETTINGS (Unreal): Increase Lightmass UV padding, reduce
     indirect lighting smoothness near corners.
  
  4. BLOCKING VOLUMES: Add invisible blocking geometry to prevent
     light from sources that shouldn't reach areas.
  
  5. LIGHTMAP RESOLUTION: Higher resolution reduces apparent bleeding.
     But also increases memory and bake time.
  
  6. MANUAL OVERRIDE: For problem areas, use light channels or manual
     lighting masks to isolate light influence.
  
### **Symptoms**
  - Light appearing through solid walls
  - Unexplained bright spots in dark rooms
  - Color bleeding from adjacent areas
  - Shadows with bright edges
### **Detection Pattern**
light.*bleed|light.*through.*wall|lightmap.*issue|bake.*artifact
### **Version Range**
all

## Envart Vertex Density Insufficient

### **Id**
envart-vertex-density-insufficient
### **Summary**
Not enough vertices for vertex color painting
### **Severity**
medium
### **Situation**
  Vertex color painting is blocky, not smooth. Transitions between painted
  areas are harsh. Low-poly meshes can't hold enough vertex color data
  for smooth blending.
  
### **Why**
  Vertex colors interpolate linearly between vertices. If vertices are far
  apart, the interpolation is visible as banding. More vertices = smoother
  gradients. But more vertices = more memory and draw cost.
  
### **Solution**
  1. TESSELLATION FOR PAINTING: Add edge loops specifically for vertex
     color resolution. Paint, then bake to texture if needed.
  
  2. TEXTURE FALLBACK: For smooth gradients on low-poly, use a texture
     instead of vertex colors. Vertex colors for broad variation,
     texture for fine gradients.
  
  3. STRATEGIC DENSITY: Add vertices where color transitions happen (base
     of walls, edges of weathering zones) not uniformly.
  
  4. VERTEX AO DENSITY: Vertex AO needs vertices in shadow casters.
     Corners need extra vertices for proper darkening.
  
  5. HYBRID APPROACH: Coarse variation via vertex color, fine variation
     via procedural texture. Combine in material.
  
### **Symptoms**
  - Blocky vertex color painting
  - Visible interpolation banding
  - Can't paint fine detail
  - AO looks faceted
### **Detection Pattern**
vertex.*color.*blocky|paint.*interpolation|banding
### **Version Range**
all