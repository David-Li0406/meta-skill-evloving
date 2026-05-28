# Texture Art - Validations

## Non-Binary Metallic Value

### **Id**
texture-metallic-non-binary
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - metallic\s*[=:]\s*0\.[1-9]
  - metallic\s*[=:]\s*0\.\d[1-9]
  - Metallic\s*=\s*0\.[1-9]
  - _Metallic\s*,\s*Range\s*\(\s*0\s*,\s*1\s*\)
### **Message**
Metallic should be binary (0 or 1), not a continuous value. Grayscale metallic breaks PBR physics.
### **Fix Action**
Use 0 for non-metals and 1 for metals. Use masking for transitions, not intermediate values.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl
  - *.mat
  - *.json

## AO Multiplied into Albedo

### **Id**
texture-albedo-ao-multiply
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - albedo\s*\*=?\s*ao
  - baseColor\s*\*=?\s*ambientOcclusion
  - diffuse\s*\*=?\s*occlusion
  - color\.rgb\s*\*=?\s*ao
### **Message**
Multiplying AO into albedo bakes shadows into the texture, causing double-lighting in PBR.
### **Fix Action**
Keep AO separate. Apply AO to ambient/indirect lighting only, not to albedo texture.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl
  - *.cginc

## Roughness Imported as sRGB

### **Id**
texture-srgb-roughness-import
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - sRGB.*[Rr]oughness
  - sRGBTexture.*roughness
  - gamma.*[Rr]oughness
### **Message**
Roughness maps must be imported as LINEAR, not sRGB. Gamma encoding corrupts the values.
### **Fix Action**
Import roughness maps with sRGB disabled. In Unity, uncheck 'sRGB (Color Texture)' for data maps.
### **Applies To**
  - *.meta
  - *.import
  - *.json

## Normal Map Imported as sRGB

### **Id**
texture-normal-srgb-import
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - "textureType":\s*0.*".*[Nn]ormal"
  - sRGB.*[Nn]ormal[Mm]ap
### **Message**
Normal maps must be imported as LINEAR and use proper normal map compression (BC5).
### **Fix Action**
Set texture type to 'Normal map' in Unity or use Normalmap compression in Unreal.
### **Applies To**
  - *.meta
  - *.import
  - *.json

## BC1/DXT1 Compression on Normal Map

### **Id**
texture-dxt1-normal
### **Severity**
error
### **Type**
regex
### **Pattern**
  - DXT1.*[Nn]ormal
  - BC1.*[Nn]ormal
  - textureCompression.*=.*0.*[Nn]ormal
  - RGB.*[Cc]ompression.*[Nn]ormal
### **Message**
BC1/DXT1 compression creates severe artifacts on normal maps. Use BC5 or BC7.
### **Fix Action**
Use BC5 (two-channel) or BC7 for normal maps. Accept larger file size for quality.
### **Applies To**
  - *.meta
  - *.import
  - *.json

## Separate Grayscale Data Textures

### **Id**
texture-unpacked-orm
### **Severity**
error
### **Type**
regex
### **Pattern**
  - tex2D\s*\(\s*_RoughnessMap
  - texture\s*\(\s*u_roughnessMap
  - SAMPLE_TEXTURE2D\s*\(\s*_MetallicMap
  - Roughness.*Map.*Metallic.*Map.*AO.*Map
### **Message**
Using separate textures for roughness/metallic/AO wastes memory. Channel pack into ORM.
### **Fix Action**
Pack Occlusion, Roughness, Metallic into RGB of single texture. Sample once, unpack in shader.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl
  - *.cginc

## Hardcoded Texture Resolution

### **Id**
texture-hardcoded-resolution
### **Severity**
error
### **Type**
regex
### **Pattern**
  - texelSize\s*=\s*1\.0\s*/\s*(?:512|1024|2048|4096)
  - (?:512|1024|2048|4096)\.0\s*,\s*(?:512|1024|2048|4096)\.0
  - resolution\s*=\s*(?:512|1024|2048|4096)
### **Message**
Hardcoded texture resolution breaks when texture size changes. Use texture properties.
### **Fix Action**
Use _TexelSize uniform (Unity) or GetDimensions() to get texture size dynamically.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl
  - *.cginc

## Data Texture Missing Linear Flag

### **Id**
texture-missing-linear-flag
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \[NoScaleOffset\].*(?:Roughness|Metallic|AO|Height|Mask)
  - (?:roughness|metallic|occlusion).*"2D".*\{\}
### **Message**
Data textures (roughness/metallic/AO) may be using sRGB. Verify linear color space.
### **Fix Action**
Add [Linear] attribute or ensure texture import settings are correct.
### **Applies To**
  - *.shader

## Texture Sampling Without Mipmap Consideration

### **Id**
texture-no-mipmap-consideration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - tex2D\s*\([^)]+\)\s*\.[rgba](?!\s*;)
  - texture\s*\([^)]+\)\s*\.\w+\s*[+\-\*]
### **Message**
Complex texture sampling may have mipmap artifacts. Consider mip level or anisotropic filtering.
### **Fix Action**
For detail textures, use textureGrad or textureLod. For UI, disable mipmaps.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl

## Sampling Full Resolution When Not Needed

### **Id**
texture-full-res-everywhere
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - textureLod\s*\([^,]+,\s*[^,]+,\s*0\.0\s*\)
  - tex2Dlod\s*\([^,]+,\s*float4\s*\([^,]+,\s*[^,]+,\s*0\s*,\s*0\s*\)
### **Message**
Forcing mip level 0 (full resolution) everywhere wastes bandwidth. Let GPU choose mip.
### **Fix Action**
Use standard texture() unless you specifically need highest mip. For blur/DOF, sample higher mips.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl
  - *.cginc

## Potential UV Padding Issue

### **Id**
texture-missing-padding-export
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - padding.*=.*[01](?:\s|$)
  - dilation.*=.*(?:0|false)
  - edge.*extend.*false
### **Message**
Low or disabled texture padding may cause mipmap bleeding at UV seams.
### **Fix Action**
Use at least 8 pixels padding for 2K textures. Enable dilation/edge extension on export.
### **Applies To**
  - *.json
  - *.sbsar
  - *.spp

## Detail Texture Without Tiling Parameters

### **Id**
texture-detail-without-tiling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - detailMap|DetailMap|detail_map
  - _DetailAlbedoMap.*"2D"
  - detail.*texture.*sample
### **Message**
Detail textures typically need tiling parameters. Verify detail UV scaling is exposed.
### **Fix Action**
Add tiling/offset parameters for detail textures. Common scale: 2-10x base UVs.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.mat

## Manual Gamma Correction

### **Id**
texture-gamma-manual-correction
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pow\s*\([^,]+,\s*2\.2\s*\)
  - pow\s*\([^,]+,\s*1\.0\s*/\s*2\.2
  - pow\s*\([^,]+,\s*0\.454
  - LinearToGamma|GammaToLinear
### **Message**
Manual gamma correction suggests color space confusion. Let hardware/engine handle sRGB.
### **Fix Action**
Use proper sRGB texture import and framebuffer settings. Avoid manual gamma in shaders.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl
  - *.cginc

## Incorrect Normal Map Unpacking

### **Id**
texture-normal-incorrect-unpack
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - normal\s*=\s*texture\s*\([^)]+\)\s*\.rgb
  - normal\.rgb\s*=\s*tex2D
  - normalMap\s*\*\s*2\s*-\s*1
### **Message**
Normal map unpacking may not handle compression format. Verify BC5/DXT5nm handling.
### **Fix Action**
Use engine-provided UnpackNormal functions that handle different compression formats.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl
  - *.cginc

## Uncompressed Texture Import

### **Id**
texture-uncompressed-import
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - compression.*=.*(?:none|uncompressed|0)
  - textureCompression.*=.*3
  - "format":\s*"RGBA32"
### **Message**
Uncompressed textures use 4-8x more memory. Use compression unless absolutely needed.
### **Fix Action**
Use BC7/BC5 for quality, BC1/BC3 for size. Only skip compression for UI elements requiring pixel-perfect.
### **Applies To**
  - *.meta
  - *.import
  - *.json

## Potentially Oversized Texture Resolution

### **Id**
texture-oversized-resolution
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - maxTextureSize.*=.*8192
  - 8192\s*x\s*8192
  - "width":\s*8192
### **Message**
8K textures consume massive memory. Verify this resolution is actually needed for texel density.
### **Fix Action**
Calculate required resolution from texel density. Most assets need 1K-2K max.
### **Applies To**
  - *.meta
  - *.import
  - *.json

## Non-Standard ORM Texture Naming

### **Id**
texture-orm-naming
### **Severity**
info
### **Type**
regex
### **Pattern**
  - _(?:ao|AO|occlusion)(?:\.|\s|$)
  - _(?:rough|ROUGH|roughness)(?:\.|\s|$)
  - _(?:metal|METAL|metallic)(?:\.|\s|$)
### **Message**
Consider combining AO, Roughness, Metallic into single ORM texture for efficiency.
### **Fix Action**
Pack into ORM: Red=AO, Green=Roughness, Blue=Metallic. Reduces texture samples by 3x.
### **Applies To**
  - *.shader
  - *.mat
  - *.json

## Texture Reference Without Fallback

### **Id**
texture-missing-fallback
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (?:sampler2D|Texture2D)\s+\w+\s*;
  - "MainTex".*"2D".*\{\}
### **Message**
Texture properties should have sensible defaults in case texture is missing.
### **Fix Action**
Provide default texture: white for albedo, (0.5,0.5,1) for normal, 0.5 for roughness.
### **Applies To**
  - *.shader

## Anisotropic Filtering Not Configured

### **Id**
texture-aniso-not-set
### **Severity**
info
### **Type**
regex
### **Pattern**
  - anisoLevel.*=.*0
  - anisotropicFiltering.*=.*0
### **Message**
Textures viewed at oblique angles (floors, walls) benefit from anisotropic filtering.
### **Fix Action**
Enable aniso level 4-16 for surfaces viewed at angles. Minimal performance cost.
### **Applies To**
  - *.meta
  - *.import

## Large Texture Without Streaming

### **Id**
texture-missing-streaming
### **Severity**
info
### **Type**
regex
### **Pattern**
  - streamingMipmaps.*=.*0.*(?:4096|8192)
  - "enableStreaming":\s*false
### **Message**
Large textures should use mipmap streaming to reduce initial memory load.
### **Fix Action**
Enable streaming mipmaps for 2K+ textures. Set streaming priority based on asset importance.
### **Applies To**
  - *.meta
  - *.import
  - *.json