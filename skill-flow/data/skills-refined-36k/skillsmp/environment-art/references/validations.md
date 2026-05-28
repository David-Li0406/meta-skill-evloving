# Environment Art - Validations

## Non-Power-of-2 Texture Dimensions

### **Id**
envart-non-pot-texture
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - size["\s:=]+\[?\s*\d*[13579]\d*\s*[,x]\s*\d+
  - width["\s:=]+\d*[13579]\d+[^\d]
  - height["\s:=]+\d*[13579]\d+[^\d]
  - resolution["\s:=]+\d*[13579]\d+
### **Message**
  Texture dimensions should be power-of-2 (256, 512, 1024, 2048, 4096).
  Non-POT textures waste memory due to GPU padding and may cause mipmap artifacts.
  
### **Fix Action**
Resize textures to nearest power-of-2 dimensions (e.g., 1000x1000 -> 1024x1024)
### **Applies To**
  - *.meta
  - *.asset
  - *.uasset
  - *.json
  - *.yaml
  - *.xml

## Oversized Textures

### **Id**
envart-excessive-texture-size
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?:4096|8192)\s*[,x]\s*(?:4096|8192)
  - size["\s:=]+8192
  - maxSize["\s:=]+8192
### **Message**
  4K+ textures should be reserved for hero assets only. Most props and modular
  pieces should use 1K-2K textures. Check if this resolution is necessary.
  
### **Fix Action**
Consider reducing to 2048x2048 unless this is a hero asset or trim sheet
### **Applies To**
  - *.meta
  - *.asset
  - *.json
  - *.yaml

## Missing LOD Configuration

### **Id**
envart-no-lod-defined
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - LODGroup["\s:=]+None
  - enableLOD["\s:=]+false
  - lodCount["\s:=]+1[^\d]
  - NumLODs["\s:=]+1[^\d]
### **Message**
  Static meshes should have multiple LOD levels defined for performance.
  Single LOD assets don't scale with distance, wasting GPU resources.
  
### **Fix Action**
Generate LOD levels: LOD0 (full), LOD1 (50%), LOD2 (25%), LOD3 (10%)
### **Applies To**
  - *.meta
  - *.asset
  - *.uasset
  - *.fbx.meta

## Missing Collision on Static Mesh

### **Id**
envart-collision-disabled
### **Severity**
error
### **Type**
regex
### **Pattern**
  - generateColliders["\s:=]+false
  - collisionEnabled["\s:=]+false
  - bEnableCollision["\s:=]+false
  - hasCollision["\s:=]+false
### **Message**
  Static meshes without collision can cause gameplay issues - players walking
  through walls, projectiles passing through objects, AI navigation failures.
  
### **Fix Action**
Enable collision or create explicit collision mesh for static environment assets
### **Applies To**
  - *.meta
  - *.asset
  - *.uasset

## Uncompressed Textures

### **Id**
envart-uncompressed-texture
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - compression["\s:=]+(?:None|Uncompressed|RGBA32)
  - textureFormat["\s:=]+RGBA32
  - CompressionSettings["\s:=]+TC_Default\s*$
### **Message**
  Uncompressed textures waste significant memory. Most textures should use
  BC/DXT compression (desktop) or ASTC/ETC (mobile).
  
### **Fix Action**
Enable texture compression: BC7/BC1 for color, BC5 for normals
### **Applies To**
  - *.meta
  - *.asset
  - *.uasset

## Mipmaps Disabled

### **Id**
envart-missing-mipmaps
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - generateMipMaps["\s:=]+false
  - mipmapEnabled["\s:=]+false
  - MipGenSettings["\s:=]+TMGS_NoMipmaps
  - useMipMap["\s:=]+0
### **Message**
  Mipmaps should be enabled for 3D textures. Without mipmaps, textures shimmer
  at distance (aliasing) and waste GPU bandwidth sampling full-res at all distances.
  
### **Fix Action**
Enable mipmap generation unless this is a UI or 2D sprite texture
### **Applies To**
  - *.meta
  - *.asset
  - *.uasset

## Too Many Materials on Mesh

### **Id**
envart-excessive-material-count
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - materialCount["\s:=]+(?:[5-9]|[1-9]\d+)
  - Materials\.Length["\s:=]+(?:[5-9]|[1-9]\d+)
  - numMaterials["\s:=]+(?:[5-9]|[1-9]\d+)
### **Message**
  Meshes with 5+ materials increase draw calls. Consider using texture atlases
  or trim sheets to reduce material count for better batching.
  
### **Fix Action**
Consolidate materials using atlases; aim for 1-3 materials per mesh
### **Applies To**
  - *.meta
  - *.asset
  - *.fbx.meta

## Inconsistent Lightmap Resolution

### **Id**
envart-lightmap-resolution-mismatch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - lightmapResolution["\s:=]+(?:4|8|16)[^\d]
  - LightmapRes["\s:=]+(?:4|8|16)[^\d]
### **Message**
  Very low lightmap resolution (4-16) may cause light bleeding and poor shadow
  quality. Minimum 32 for small props, 64-128 for modular pieces, 256+ for large surfaces.
  
### **Fix Action**
Increase lightmap resolution to at least 32, or higher for visible surfaces
### **Applies To**
  - *.meta
  - *.asset
  - *.uasset

## Static Batching Not Enabled

### **Id**
envart-static-batching-disabled
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - staticBatchingEnabled["\s:=]+false
  - bEnableStaticMesh["\s:=]+false
  - staticFlags["\s:=]+0
### **Message**
  Static environment meshes should use static batching for reduced draw calls.
  Enable static batching flags on non-moving environment geometry.
  
### **Fix Action**
Enable static batching/static mesh flags for immobile environment assets
### **Applies To**
  - *.meta
  - *.asset
  - *.unity
  - *.prefab

## Occlusion Culling Not Configured

### **Id**
envart-no-occlusion
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - occlusionCulling["\s:=]+false
  - bUseAsOccluder["\s:=]+false
  - occluderEnabled["\s:=]+false
### **Message**
  Large environment meshes (walls, floors, large props) should participate in
  occlusion culling to prevent rendering of hidden geometry.
  
### **Fix Action**
Enable occluder flags on large blocking geometry (walls, floors, pillars)
### **Applies To**
  - *.meta
  - *.asset
  - *.uasset
  - *.prefab

## Single-Sided Geometry Warning

### **Id**
envart-single-sided-geo
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - doubleSided["\s:=]+false
  - twoSided["\s:=]+false
  - cullMode["\s:=]+Back
### **Message**
  Single-sided geometry is correct for performance but ensure walls and
  enclosed spaces have thickness. Paper-thin walls cause light bleeding.
  
### **Fix Action**
Verify walls have thickness (32+ units) or enable double-sided for foliage/cloth
### **Applies To**
  - *.mat
  - *.material
  - *.uasset

## Mesh Without Vertex Colors

### **Id**
envart-missing-vertex-colors
### **Severity**
info
### **Type**
regex
### **Pattern**
  - hasVertexColors["\s:=]+false
  - vertexColorCount["\s:=]+0
  - ImportVertexColors["\s:=]+false
### **Message**
  Consider using vertex colors for material variation (dirt, wear, wetness)
  without additional texture cost. Especially useful for modular pieces.
  
### **Fix Action**
Enable vertex color import if using vertex-based material variation
### **Applies To**
  - *.meta
  - *.fbx.meta

## Very High Polygon Count

### **Id**
envart-excessive-poly-count
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - triangleCount["\s:=]+(?:\d{6,})
  - polyCount["\s:=]+(?:\d{6,})
  - numTriangles["\s:=]+(?:\d{6,})
### **Message**
  Meshes with 1M+ triangles are expensive. Ensure proper LOD setup and
  consider if this density is visible at gameplay distances.
  
### **Fix Action**
Add aggressive LODs or reduce base polygon count if not hero asset
### **Applies To**
  - *.meta
  - *.asset
  - *.fbx.meta

## UV Channel Configuration Issue

### **Id**
envart-unoptimized-uv
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - generateSecondaryUV["\s:=]+false.*lightmap
  - lightmapUVChannel["\s:=]+-1
  - hasLightmapUVs["\s:=]+false
### **Message**
  Lightmapped meshes need a second UV channel for lightmap UVs.
  Without dedicated lightmap UVs, baking will produce artifacts.
  
### **Fix Action**
Generate secondary UVs for lightmapping or use UV2 in DCC tool
### **Applies To**
  - *.meta
  - *.fbx.meta
  - *.asset

## Expensive Alpha Blend on Environment

### **Id**
envart-alpha-blend-opaque
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - renderMode["\s:=]+(?:Transparent|Fade)
  - blendMode["\s:=]+Translucent
  - alphaBlend["\s:=]+true
### **Message**
  Transparent materials are expensive and don't write depth. Use alpha cutoff
  (alpha test) instead of alpha blend for foliage and masked surfaces.
  
### **Fix Action**
Switch from Transparent to Cutout/AlphaTest for foliage and fences
### **Applies To**
  - *.mat
  - *.material
  - *.uasset

## Material Without Normal Map

### **Id**
envart-missing-normal-map
### **Severity**
info
### **Type**
regex
### **Pattern**
  - normalMap["\s:=]+null
  - _BumpMap["\s:=]+\{\s*\}
  - hasNormalTexture["\s:=]+false
### **Message**
  Environment materials typically benefit from normal maps for surface detail.
  Ensure normal maps are assigned unless intentionally flat (stylized art).
  
### **Fix Action**
Add normal map texture or explicitly note if flat style is intentional
### **Applies To**
  - *.mat
  - *.material

## Extreme Draw Distance Configuration

### **Id**
envart-excessive-draw-distance
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - cullingDistance["\s:=]+(?:\d{5,})
  - maxDrawDistance["\s:=]+(?:\d{5,})
  - farClip["\s:=]+100000
### **Message**
  Very high draw distances (10000+ units) can hurt performance and depth buffer
  precision. Most environment assets should cull at reasonable distances.
  
### **Fix Action**
Set appropriate cull distances: props (5000), structures (10000), terrain (far)
### **Applies To**
  - *.meta
  - *.asset
  - *.uasset
  - *.prefab