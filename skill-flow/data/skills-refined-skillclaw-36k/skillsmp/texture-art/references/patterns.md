# Texture Art

## Patterns


---
  #### **Name**
PBR Base Color Guidelines
  #### **Description**
Create physically accurate albedo maps without baked lighting
  #### **When**
Creating base color/albedo textures for PBR materials
  #### **Example**
    # CORRECT Base Color Values (sRGB, no lighting):
    # - Darkest non-metal: ~50 sRGB (charcoal, asphalt)
    # - Lightest non-metal: ~240 sRGB (fresh snow, white paint)
    # - Most materials: 60-200 sRGB range
    
    # What base color SHOULD contain:
    # - Inherent color of the material
    # - Color variation (stains, dirt, color zones)
    # - NO shadows, NO highlights, NO ambient occlusion
    
    # Common materials reference:
    # Dry concrete: RGB(140, 135, 130), ~0.5 value
    # Wet concrete: RGB(80, 77, 75), ~0.3 value (darker when wet)
    # Rusted iron: RGB(140, 80, 60), warm orange-brown
    # Fresh steel: RGB(180, 180, 185), slight blue-cool tint
    # Wood (oak): RGB(160, 120, 80), warm yellow-brown
    # Grass: RGB(90, 130, 60), varies by health/type
    

---
  #### **Name**
Metallic Map Binary Rule
  #### **Description**
Metallic values must be 0 or 1, never in between
  #### **When**
Creating metallic maps for PBR materials
  #### **Example**
    # CORRECT: Binary metallic map
    # Pure metal surfaces: Metallic = 1 (255 in 8-bit)
    # Non-metal surfaces: Metallic = 0 (0 in 8-bit)
    
    # WHY binary? Physics.
    # Real materials are either metallic or dielectric at the molecular level.
    # There's no "half metal" in nature.
    
    # Common mistake: Using grayscale for "worn metal"
    # WRONG: Metallic = 0.7 for scratched paint on metal
    # RIGHT: Metallic = 1 where paint is gone, 0 where paint remains
    #        The TRANSITION is in the mask, not the value.
    
    # Edge cases that look like gray metallic but aren't:
    # - Oxidized metal: Still metallic=1, but rougher and different base color
    # - Painted metal: Metallic=0 on paint, metallic=1 on exposed metal
    # - Plated metal: Usually metallic=1 (chrome, gold plating)
    # - Brushed metal: Metallic=1 with anisotropic roughness
    

---
  #### **Name**
Roughness Variation for Realism
  #### **Description**
Use roughness variation to sell material believability
  #### **When**
Creating roughness maps that look convincing
  #### **Example**
    # The roughness map has MORE impact on realism than base color.
    # Human eyes subconsciously judge surface quality by reflections.
    
    # NEVER use flat roughness values. Real surfaces have variation:
    # - Fingerprints on glass: Localized roughness increase
    # - Wear patterns: Edges and high-contact areas get polished
    # - Weathering: Exposed areas get rougher over time
    # - Manufacturing: Tool marks, casting texture, grain
    
    # Reference values (0-1 scale):
    # Mirror/chrome: 0.0-0.1
    # Polished plastic: 0.1-0.3
    # Semi-gloss paint: 0.3-0.5
    # Brushed metal: 0.4-0.6
    # Matte plastic: 0.5-0.7
    # Rough concrete: 0.7-0.9
    # Fabric/cloth: 0.8-1.0
    
    # Pro tip: Add subtle noise (5-10% variation) to all roughness maps
    # Even "uniform" surfaces have micro-variation in reality
    

---
  #### **Name**
Edge Wear Physics
  #### **Description**
Apply wear and tear based on real-world physics
  #### **When**
Adding surface damage and weathering
  #### **Example**
    # Wear follows physics. Edges and protrusions wear first.
    # Substance Painter: Use curvature map + generators
    
    # Primary wear zones (high curvature, exposed):
    # 1. Corners and hard edges - paint chips, metal exposed
    # 2. High-contact areas - handles, buttons, grip zones
    # 3. Ground contact - bottom of objects, feet
    # 4. Movement zones - hinges, slides, pivots
    
    # Secondary wear (environmental):
    # 1. Water flow paths - vertical streaks, rust runs
    # 2. UV exposure - top surfaces fade, plastics yellow
    # 3. Gravity - dust/dirt accumulates in crevices (AO zones)
    # 4. Human contact - oils, fingerprints at grab points
    
    # Layering order in Substance Painter:
    # 1. Base material (clean version)
    # 2. Edge wear (curvature-based metal exposure)
    # 3. Cavity dirt (AO-based grime in crevices)
    # 4. Surface scratches (random + directional)
    # 5. Environmental effects (rust runs, water stains)
    # 6. Dust/debris (top-facing accumulation)
    

---
  #### **Name**
Texel Density Consistency
  #### **Description**
Maintain consistent pixel density across all scene assets
  #### **When**
UV mapping and texture resolution planning
  #### **Example**
    # Texel density = pixels per unit of 3D space
    # Inconsistent TD = some objects look blurry, others sharp
    
    # Common standards:
    # Third-person games (TLoU, GoW): 512 px/m (5.12 px/cm)
    # First-person games (CoD, Halo): 1024 px/m (10.24 px/cm)
    # VR (close inspection): 2048 px/m (20.48 px/cm)
    
    # Calculating texture size from TD:
    # Object is 2m x 2m, TD target is 512 px/m
    # Texture size = 2m * 512 px/m = 1024 pixels
    # Use 1024x1024 texture
    
    # When to BREAK consistency (intentionally):
    # - First-person weapons: 2-4x higher TD (player stares at them)
    # - Hero assets: Higher TD for narrative focus
    # - Background props: Lower TD is acceptable
    # - UI/inspectable items: Highest TD
    
    # Blender addon: "Texel Density Checker"
    # Substance Painter: View > Texel Density
    

---
  #### **Name**
Normal Map Baking Best Practices
  #### **Description**
Bake normal maps without common artifacts
  #### **When**
Baking high-poly detail to low-poly mesh
  #### **Example**
    # Core baking settings for clean normals:
    
    # 1. USE A CAGE (don't rely on ray distance alone)
    # - Cage = slightly inflated low-poly that defines ray origin
    # - Gives precise control over projection direction
    # - Essential for hard edges and mechanical parts
    
    # 2. Ray distance settings:
    # - Frontal distance: Just enough to reach high-poly surface
    # - Rear distance: Usually smaller than frontal
    # - Too large = captures neighboring geometry (bleeding)
    # - Too small = misses detail (black spots)
    
    # 3. Match by mesh name:
    # - Name convention: HighPoly_PartName, LowPoly_PartName
    # - Prevents neighboring parts from baking onto each other
    
    # 4. Triangulate before export:
    # - Ensures consistent triangulation between apps
    # - Avoids "broken normals" from quad diagonal flipping
    
    # 5. Tangent space matching:
    # - Export with same tangent basis as game engine
    # - Substance Painter preset for Unity/Unreal handles this
    
    # Common artifacts and fixes:
    # - Wavy normals: Increase cage size or use averaged normals
    # - Black spots: Increase ray distance
    # - Bleeding: Use match by name or reduce ray distance
    # - Faceted look: Smooth low-poly normals before bake
    

---
  #### **Name**
Channel Packing for Optimization
  #### **Description**
Combine grayscale maps into RGB channels
  #### **When**
Optimizing texture memory and draw calls
  #### **Example**
    # Channel packing: 3 grayscale maps in 1 RGB texture
    # Reduces texture samples and memory by 3x
    
    # Common packing schemes:
    # ORM (Unreal standard):
    #   R = Ambient Occlusion
    #   G = Roughness (best compression in green channel)
    #   B = Metallic
    
    # RMA (alternative):
    #   R = Roughness
    #   G = Metallic
    #   B = Ambient Occlusion
    
    # MADS (for complex materials):
    #   R = Metallic
    #   G = AO
    #   B = Detail mask
    #   A = Smoothness (inverted roughness)
    
    # CRITICAL: Use LINEAR color space, NOT sRGB
    # - These are data maps, not color
    # - sRGB will corrupt the values
    # - Uncheck "sRGB" in Unity import settings
    # - Use BC7 or DXT5 compression (not DXT1 for alpha)
    
    # In shader, unpack with single sample:
    # float3 orm = texture(ormMap, uv).rgb;
    # float ao = orm.r;
    # float roughness = orm.g;
    # float metallic = orm.b;
    

---
  #### **Name**
Trim Sheet Workflow
  #### **Description**
Create modular texture sheets for environment art
  #### **When**
Building modular environment pieces
  #### **Example**
    # Trim sheets: Texture atlases that tile along one axis
    # Perfect for: Architectural trim, pipes, panels, frames
    
    # Workflow (reversed from traditional):
    # 1. Plan texture layout FIRST
    # 2. Model modular pieces
    # 3. UV map TO the existing texture (not the reverse)
    
    # Trim sheet layout tips:
    # - Keep segments divisible by 10 (easy UV mapping math)
    # - Horizontal strips for architectural trim
    # - Include: edges, corners, transitions, fill patterns
    # - Leave 4-8 pixel gutters between strips
    
    # UV mapping to trim sheets:
    # - Scale UV shells to match texel density
    # - Align UVs to texture pixels (avoid sub-pixel bleeding)
    # - Mirror/flip UVs to maximize texture coverage
    # - Can overlap UVs for repeating elements
    
    # In Substance Painter:
    # - Create trim sheet as 2D texture project
    # - Use tile sampler + blend for procedural strips
    # - Export at 2K or 4K (shared across many assets)
    
    # Memory efficiency:
    # 1x 4K trim sheet < 20x 512x512 unique textures
    # Massive reduction in texture variety needs
    

---
  #### **Name**
Color ID Masking Workflow
  #### **Description**
Use material ID maps for efficient masking
  #### **When**
Setting up masks for complex assets in Substance Painter
  #### **Example**
    # Color ID maps: Flat colors that define material zones
    # Baked from vertex colors or material assignments
    
    # Setup in modeling app:
    # 1. Assign distinct materials to different zones
    # 2. Use pure colors: Red, Green, Blue, Cyan, Magenta, Yellow
    # 3. Avoid similar colors (compression will merge them)
    # 4. Each material = one selection mask in Painter
    
    # Baking in Substance Painter:
    # - Color Source: "Material Color" or "Vertex Color"
    # - Anti-aliasing: x1 (sharp edges for masking)
    # - Resolution: Same as other maps
    
    # Using ID masks:
    # - Right-click layer > Add mask with color selection
    # - Pick color with eyedropper
    # - Instant selection of that material zone
    
    # Pro tips:
    # - Use standard legacy materials, not PBR (3ds Max)
    # - Keep UV islands large enough to avoid bleeding
    # - ID maps don't need high resolution - 1K often enough
    # - Can combine with generators for edge wear on specific parts
    

---
  #### **Name**
DirectX vs OpenGL Normal Maps
  #### **Description**
Handle normal map Y-channel differences between engines
  #### **When**
Porting textures between engines or from external sources
  #### **Example**
    # The green (Y) channel is INVERTED between conventions:
    # - DirectX (Y-): Unreal Engine, CryEngine, 3ds Max
    # - OpenGL (Y+): Unity, Blender, Maya, Modo, Marmoset
    
    # Visual test: Bumps lit from top-left in your engine?
    # - If bumps look inverted (lit from bottom), flip green channel
    
    # Fixing in Substance Painter:
    # - Export settings > Normal Map Format > DirectX or OpenGL
    # - Choose based on target engine
    
    # Fixing in Photoshop/GIMP:
    # - Select Green channel only
    # - Image > Adjustments > Invert (Ctrl+I)
    
    # Fixing in engine:
    # Unity: Usually works, but check "Flip Green Channel" if needed
    # Unreal: Expects DirectX by default, import setting available
    
    # When using Megascans/external libraries:
    # - Check documentation for their convention
    # - Megascans: DirectX format
    # - Many free libraries: OpenGL format
    

---
  #### **Name**
UV Padding for Mipmap Safety
  #### **Description**
Prevent mipmap bleeding with proper edge padding
  #### **When**
Finalizing textures for production
  #### **Example**
    # Mipmap bleeding: Colors from adjacent UV islands leak in at distance
    # Cause: Bilinear filtering samples beyond UV island edges
    
    # Padding requirements by resolution:
    # - 512x512: Minimum 2 pixels
    # - 1024x1024: Minimum 4 pixels
    # - 2048x2048: Minimum 4-8 pixels
    # - 4096x4096: Minimum 8-16 pixels
    
    # Rule of thumb: padding = 2^(mip_levels - 1)
    # For 2K with 11 mip levels: 2^10 = 1024? No, practical is 8-16px
    
    # In Substance Painter:
    # - File > Export > Padding: "Dilation + Diffusion"
    # - Dilation extends edge colors outward
    # - Set at least 8 pixels for 2K textures
    
    # In Photoshop:
    # - Use "Solidify" filter (free plugin)
    # - Or manually: Select UV island, expand selection, fill with edge color
    
    # Texture atlas special case:
    # - Atlases need INTERNAL padding between elements
    # - 2x the normal padding between atlas tiles
    # - Consider using texture arrays instead for cleaner mips
    

## Anti-Patterns


---
  #### **Name**
Baked Lighting in Albedo
  #### **Description**
Including shadows, AO, or highlights in base color map
  #### **Why**
    Double-dipping: Baked lighting + engine lighting = wrong results.
    Shadows in albedo create permanent dark areas regardless of light direction.
    Makes relighting impossible without re-texturing everything.
    
  #### **Instead**
    Keep base color PURE - only inherent surface color.
    Use separate AO map applied in shader or combined pass.
    Let the engine handle all lighting calculations.
    

---
  #### **Name**
Grayscale Metallic Values
  #### **Description**
Using 0.3, 0.5, 0.7 metallic values for "partial metal"
  #### **Why**
    Physics doesn't work that way. Materials are metallic or dielectric.
    Grayscale metallic creates physically impossible reflections.
    Leads to halo artifacts and energy loss in PBR shaders.
    
  #### **Instead**
    Binary metallic: 0 or 1 only.
    Use mask with hard/soft edges for paint-over-metal effects.
    Blend roughness and base color, not metallic value.
    

---
  #### **Name**
Ignoring Texel Density
  #### **Description**
Not checking pixel density across scene assets
  #### **Why**
    Creates visual inconsistency: hero prop blurry, background crate sharp.
    Breaks immersion - players notice subconsciously.
    Wastes memory: high-res on distant objects, low-res on close ones.
    
  #### **Instead**
    Set project-wide TD standard (512 or 1024 px/m).
    Use TD checker tools before finalizing UVs.
    Intentionally break TD only for hero assets.
    

---
  #### **Name**
Flat Roughness Maps
  #### **Description**
Using uniform roughness values without variation
  #### **Why**
    Real surfaces have micro-variation even when they look uniform.
    Flat roughness looks synthetic and "CG".
    Misses opportunity for storytelling through wear patterns.
    
  #### **Instead**
    Add subtle noise (5-10%) to base roughness.
    Include wear patterns: edges polish, crevices get rougher.
    Use reference photos to match real-world variation.
    

---
  #### **Name**
Baking Without Cage
  #### **Description**
Relying solely on ray distance for normal map baking
  #### **Why**
    Ray distance is trial-and-error and inconsistent across parts.
    Hard edges and mechanical parts get projection errors.
    Leads to wavy normals and bleeding between parts.
    
  #### **Instead**
    Create cage mesh (inflated low-poly) for ray origins.
    Use "match by mesh name" to isolate parts.
    Cage gives predictable, art-directable projection.
    

---
  #### **Name**
sRGB on Data Maps
  #### **Description**
Saving roughness/metallic/AO/normal maps as sRGB
  #### **Why**
    sRGB gamma encoding corrupts linear data.
    Values get shifted: 0.5 roughness becomes ~0.73 in engine.
    Normal maps especially break - lighting looks wrong.
    
  #### **Instead**
    Export all non-color maps as LINEAR.
    In Unity: Uncheck "sRGB (Color Texture)" for data maps.
    In Unreal: Compression settings handle this automatically.
    

---
  #### **Name**
Insufficient UV Padding
  #### **Description**
Using 1-2 pixel padding on high-res textures
  #### **Why**
    Mipmap levels need exponentially more padding.
    At MIP4, a 2-pixel padding is consumed by filtering.
    Results in color bleeding visible at medium-far distances.
    
  #### **Instead**
    Minimum 4 pixels for 1K, 8 pixels for 2K, 16 pixels for 4K.
    Use dilation + diffusion in export settings.
    Test at lowest mip level to verify no bleeding.
    

---
  #### **Name**
Compressing Normal Maps as DXT1
  #### **Description**
Using RGB compression (DXT1/BC1) for normal maps
  #### **Why**
    DXT1 compression creates severe block artifacts.
    Normal maps encode precise vector data - artifacts = wrong lighting.
    Visible as "stair-stepping" on curved surfaces.
    
  #### **Instead**
    Use BC5 (two-channel, high quality) for normal maps.
    Or BC7 if alpha channel needed.
    Accept larger file size for normal map quality.
    