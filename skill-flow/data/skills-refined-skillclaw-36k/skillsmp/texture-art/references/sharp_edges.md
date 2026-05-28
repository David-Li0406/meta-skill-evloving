# Texture Art - Sharp Edges

## Texture Baked Lighting Albedo

### **Id**
texture-baked-lighting-albedo
### **Summary**
Baked lighting in albedo causes double-lighting artifacts
### **Severity**
critical
### **Situation**
Creating base color/albedo maps with shadows, AO, or highlights baked in
### **Why**
  PBR engines calculate ALL lighting at runtime. When you bake lighting into albedo,
  the engine adds MORE lighting on top. Result: shadows are too dark, highlights are
  blown out, and the asset can never be relit correctly.
  
  This is called "double-dipping" - lighting applied twice. Common sources:
  - Photosourcing textures with strong shadows
  - Using diffuse maps from older non-PBR games
  - Painting highlights/shadows in Photoshop
  - Applying AO directly to base color in Substance
  
### **Solution**
  1. Use multiply AO on a SEPARATE layer in Substance (not baked into diffuse)
  2. Strip lighting from photo sources using frequency separation
  3. For older assets: extract AO, recreate clean albedo
  4. Check values: albedo should be 50-240 sRGB, evenly lit
  5. View albedo in isolation (no lighting) to verify cleanliness
  
### **Symptoms**
  - Shadows always visible regardless of light direction
  - Asset looks "dirty" or "muddy" in all lighting conditions
  - Cannot relight scene without re-texturing assets
  - AO appears darker than intended
  - Highlights baked into albedo create hot spots
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - Albedo values below 30 sRGB (too dark for natural materials)
  - Strong directional shadows visible in albedo
  - Using "diffuse" textures from pre-PBR era
  - Multiplying AO directly onto base color layer

## Texture Metallic Grayscale

### **Id**
texture-metallic-grayscale
### **Summary**
Grayscale metallic values break PBR physics
### **Severity**
critical
### **Situation**
Using metallic values between 0 and 1 (e.g., 0.5 metallic)
### **Why**
  Metallic is a BINARY physical property. At the molecular level, a material either
  conducts electrons (metal) or doesn't (dielectric). There's no "half metal" in nature.
  
  Using 0.5 metallic creates physically impossible behavior:
  - Fresnel calculations break (reflectivity curve is wrong)
  - Energy conservation fails (reflects wrong amount of light)
  - Creates "halo" artifacts around metallic-to-dielectric transitions
  - Looks fake because it doesn't match reality
  
  Exception: Transition zones need soft masks, but the VALUES are still 0 and 1.
  The gradual transition is in the MASK, not the metallic value itself.
  
### **Solution**
  1. Metallic map should be pure black (0) or pure white (1)
  2. Use anti-aliased edges for transitions (the edge is soft, not the value)
  3. For painted metal: metallic=0 where painted, metallic=1 where exposed
  4. For oxidized metal: still metallic=1, but different roughness/base color
  5. Test in engine: disable albedo, view metallic only - should be high contrast
  
### **Symptoms**
  - Metallic areas look "plastic" or "wrong"
  - Fresnel reflections don't match real metal
  - Edge transitions have halos or glow
  - Material looks different in different PBR engines
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - Metallic map has gradients or grayscale areas
  - Using roughness slider to fake "less metallic"
  - Metallic histogram shows values between 10-245

## Texture Normal Y Flip

### **Id**
texture-normal-y-flip
### **Summary**
DirectX vs OpenGL normal map Y-channel causes inverted lighting
### **Severity**
high
### **Situation**
Normal maps appear to have inverted bumps or shadows
### **Why**
  The green (Y) channel convention differs between graphics APIs:
  - DirectX (Y-): Bumps lit from top-left, Y points DOWN in tangent space
  - OpenGL (Y+): Bumps lit from top-left, Y points UP in tangent space
  
  Using the wrong convention makes bumps appear as dents. Light hits surfaces
  from the opposite expected direction. This is a DATA interpretation issue,
  not a visual preference.
  
  Engine defaults:
  - DirectX: Unreal Engine, CryEngine, Source, Frostbite
  - OpenGL: Unity, Godot, Blender, most web engines
  
### **Solution**
  1. Know your target engine's convention BEFORE creating textures
  2. Substance Painter: Set export preset for target engine
  3. Fix existing: Invert green channel only in Photoshop/GIMP
  4. Test: Create simple hemisphere, light from top-right, verify shadow direction
  5. When in doubt: Bumps should appear to "pop out" when lit from above-left
  
### **Symptoms**
  - Surface details appear inverted (bumps look like dents)
  - Lighting looks "inside out" on normal-mapped surfaces
  - Textures look fine in one engine, broken in another
  - Hemispheres lit from below instead of above
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - Using Megascans (DirectX) in Unity (OpenGL) without flip
  - Mixing normal maps from different sources
  - Normal map "looks fine in Substance" but broken in engine

## Texture Normal Compression Artifacts

### **Id**
texture-normal-compression-artifacts
### **Summary**
Wrong compression format destroys normal map quality
### **Severity**
high
### **Situation**
Normal maps have blocky artifacts or lighting looks faceted
### **Why**
  Normal maps store PRECISE vector data, not visual color. Standard color compression
  (DXT1/BC1) uses 4:1 compression that creates 4x4 pixel blocks. These blocks create
  visible stepping on curved surfaces.
  
  The right format depends on platform:
  - BC5 (2-channel): Best quality, stores RG only, reconstruct B in shader
  - BC7: High quality RGB+A, 8 bits per pixel, slower to compress
  - DXT5/BC3: Acceptable, but artifacts on gradients
  - DXT1/BC1: NEVER use for normal maps
  
  Note: ASTC (mobile) and ETC2 (Android) have similar quality tiers.
  
### **Solution**
  1. Use BC5 compression for normal maps (most engines support)
  2. Unity: Normal map import type auto-selects correct compression
  3. Unreal: NormalMap compression setting uses BC5
  4. If BC5 unavailable: BC7 > BC3 > NEVER BC1
  5. Verify: Zoom in on compressed normal, check for 4x4 block patterns
  
### **Symptoms**
  - Curved surfaces look faceted or "stair-stepped"
  - Fine normal detail is lost or blocky
  - Lighting has visible square artifacts
  - Works fine in Substance, broken after engine import
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - Normal map using DXT1/BC1 compression
  - Normal map file size suspiciously small
  - "Automatic" compression without checking result

## Texture Mipmap Bleeding

### **Id**
texture-mipmap-bleeding
### **Summary**
Insufficient UV padding causes color bleeding at distance
### **Severity**
high
### **Situation**
Texture colors bleed between UV islands when viewed from distance
### **Why**
  Mipmaps are downsampled versions of textures. At each mip level, 4 pixels become 1.
  If UV islands are too close (insufficient padding), the downsampling picks up colors
  from neighboring islands.
  
  The math is brutal:
  - 2K texture with 2px padding: By mip5, the "gutter" is <1 pixel
  - 4K texture with 4px padding: By mip6, same problem
  - Result: "Dark seams" or "color halos" at medium-far distance
  
  Bilinear filtering makes it worse - it samples a 2x2 pixel area, so edges bleed
  even before mip issues appear.
  
### **Solution**
  1. Minimum padding by resolution:
     - 512: 2px, 1K: 4px, 2K: 8px, 4K: 16px
  2. Use "Dilation + Diffusion" in Substance Painter export
  3. Edge color should extend outward, not be transparent
  4. Test at lowest mip level: View > Show Mip Level in engine
  5. For texture atlases: 2x normal padding between elements
  
### **Symptoms**
  - Dark seams appear at UV edges when viewed from distance
  - Colors from adjacent UV islands "leak" onto each other
  - Works fine up close, breaks at medium-far distance
  - LOD transitions show color popping
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - Padding less than 4 pixels on 2K textures
  - Transparent gutters instead of dilated edge colors
  - Atlas textures with minimal spacing between tiles

## Texture Srgb Data Maps

### **Id**
texture-srgb-data-maps
### **Summary**
Using sRGB color space for data textures corrupts values
### **Severity**
high
### **Situation**
Roughness, metallic, AO, or normal maps have wrong values in engine
### **Why**
  sRGB applies a gamma curve: linear 0.5 becomes sRGB ~0.73 (186 out of 255).
  Data maps (roughness, metallic, AO, height, normal) store LINEAR values.
  
  When a data map is saved/imported as sRGB:
  - A 0.5 roughness becomes ~0.73 in the shader
  - Normal map vectors get distorted (lighting is wrong)
  - AO/height values are curve-shifted
  
  This is one of the most common "my textures look different in engine" issues.
  
### **Solution**
  1. Export data maps WITHOUT sRGB (linear)
  2. Unity: Uncheck "sRGB (Color Texture)" on import
  3. Unreal: Set Compression to "Masks" or engine handles automatically
  4. Substance Painter: Correct by default for most exports
  5. Photoshop: Export as 8-bit with no color profile
  
### **Symptoms**
  - Roughness appears glossier or more matte than authored
  - Metallic transitions look different in engine
  - Normal map lighting is subtly "off"
  - Values in engine don't match Substance preview
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - All texture imports using same settings
  - Not verifying color space per texture type
  - PNG exports with embedded sRGB profile

## Texture Memory Explosion

### **Id**
texture-memory-explosion
### **Summary**
Unoptimized textures consume excessive VRAM
### **Severity**
high
### **Situation**
Game runs out of texture memory or has long load times
### **Why**
  Texture memory adds up fast:
  - 4K RGBA uncompressed: 64MB per texture
  - With 10 texture sets: 640MB just for one scene
  
  Common waste:
  - Using 4K when 1K would suffice (texel density mismatch)
  - Separate grayscale textures instead of channel packing
  - Unused alpha channels consuming memory
  - Not streaming lower mips for distant objects
  
### **Solution**
  1. Channel pack: ORM (Occlusion, Roughness, Metallic) in one texture
  2. Match resolution to texel density needs (don't over-res)
  3. Use texture streaming for large scenes
  4. Remove unused alpha channels
  5. Audit: Calculate total texture memory budget and allocate
  
### **Symptoms**
  - Out of VRAM warnings/crashes
  - Texture streaming hitches and pop-in
  - Long level load times
  - Low framerates with memory pressure
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - Separate 2K textures for AO, Roughness, Metallic (should be one ORM)
  - 4K textures on small props
  - No texture LOD/streaming system

## Texture Baking Ray Distance

### **Id**
texture-baking-ray-distance
### **Summary**
Wrong ray distance causes bake artifacts and bleeding
### **Severity**
high
### **Situation**
Normal map bake has black spots, bleeding from neighboring geometry, or wavy artifacts
### **Why**
  Normal map baking shoots rays from low-poly to high-poly. The ray distance controls
  how far rays travel. Problems:
  
  - Too short: Rays don't reach high-poly surface = black spots
  - Too long: Rays hit neighboring geometry = wrong normals bleed in
  - No cage: Ray direction is inconsistent at hard edges = wavy normals
  
  Substance Painter visualizes this with the cage preview, but many artists skip it.
  
### **Solution**
  1. USE A CAGE MESH (copy of low-poly, slightly inflated)
  2. Enable cage visualization before baking
  3. Adjust until cage fully envelops high-poly
  4. Use "match by mesh name" to isolate parts
  5. Frontal distance: Just enough to reach high-poly
  6. If artifacts persist: Reduce rear distance or split mesh
  
### **Symptoms**
  - Black spots where rays missed high-poly
  - Details from neighboring parts baked onto wrong surface
  - Wavy/wobbly normals on flat surfaces
  - Bake looks different than high-poly
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - Baking without cage mesh
  - Very large ray distance values
  - Not using match by mesh name
  - "It worked on simpler models" but fails on complex

## Texture Texel Density Mismatch

### **Id**
texture-texel-density-mismatch
### **Summary**
Inconsistent texel density makes some assets look blurry
### **Severity**
medium
### **Situation**
Some objects look crisp while others look blurry in the same scene
### **Why**
  Texel density = pixels per unit of world space. If one object has 2x the texel density
  of another, it will appear 2x sharper. This destroys visual cohesion.
  
  Common causes:
  - Different artists using different standards
  - Not checking TD before finalizing UVs
  - Reusing textures at different scales
  - Over-detailing hero assets, under-detailing environment
  
### **Solution**
  1. Establish project TD standard: 512px/m (third person) or 1024px/m (first person)
  2. Check TD in Blender (TD Checker addon) or Substance before export
  3. Intentional TD breaks only for hero assets (2x for weapons, etc.)
  4. Document exceptions in style guide
  5. Review all assets at distance to catch inconsistencies
  
### **Symptoms**
  - Some objects noticeably blurrier than neighbors
  - Detail level inconsistent across scene
  - Close inspection reveals some assets are "undercooked"
  - Texture resolution doesn't match object importance
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - No documented TD standard
  - Artists working independently without coordination
  - Reusing textures at arbitrary scales

## Texture Tiling Seams

### **Id**
texture-tiling-seams
### **Summary**
Visible seams when tiling textures
### **Severity**
medium
### **Situation**
Tiling textures show visible lines where edges meet
### **Why**
  Tileable textures require edge pixels to perfectly match opposite edge pixels.
  Common issues:
  - Offset filter used but not blended at seams
  - Different lighting/value at edges vs center
  - Hard elements that cross the boundary
  - Compression artifacts at edges
  
### **Solution**
  1. Use make-seamless tools: Photoshop offset + clone, Substance Designer
  2. Check ALL four corners (wrap both X and Y)
  3. Blur/blend seams, don't just clone stamp
  4. Avoid placing recognizable features near edges
  5. Test: Tile 3x3 at low zoom to spot patterns and seams
  
### **Symptoms**
  - Visible grid lines when texture is tiled
  - Repeating patterns become obvious
  - Value/color shifts at tile boundaries
  - Works at 1x but breaks when tiled
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - Quick offset filter without seam blending
  - Never testing tiled version
  - Distinct features placed at texture edges

## Texture Height Vs Normal Confusion

### **Id**
texture-height-vs-normal-confusion
### **Summary**
Misusing height maps where normal maps are needed
### **Severity**
medium
### **Situation**
Using height maps for real-time rendering detail
### **Why**
  Height maps and normal maps serve different purposes:
  - Height map: Grayscale displacement, actual geometry change
  - Normal map: RGB surface angle, lighting trick only
  
  Height maps in shaders require:
  - Tessellation (expensive) for actual displacement
  - Parallax Occlusion Mapping for faked depth
  - Both are much more expensive than normal maps
  
  Using height where normal is expected = no visual effect or crashes.
  
### **Solution**
  1. Convert height to normal for standard bump mapping
  2. Use height only for: tessellation, parallax, or as blend mask
  3. Normal map = 90% of use cases, height = special cases
  4. If parallax: Combine height + normal for best result
  5. Substance can convert height to normal automatically
  
### **Symptoms**
  - Expected bump detail not visible
  - Shader crashes or errors
  - Massive performance hit from tessellation
  - Height map connected to normal input = flat surface
### **Detection Pattern**

### **Version Range**
*
### **Red Flags**
  - Connecting height to normal map slot
  - Using height for all detail (overkill)
  - Not generating normal from height for standard rendering