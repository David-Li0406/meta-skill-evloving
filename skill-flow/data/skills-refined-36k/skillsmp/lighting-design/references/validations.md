# Lighting Design - Validations

## Extreme Lightmap Resolution

### **Id**
lighting-extreme-lightmap-resolution
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - lightmapResolution\s*[=:]\s*[5-9]\d{2}
  - lightmapResolution\s*[=:]\s*\d{4,}
  - Light\s*Map\s*Resolution["\s:]*[5-9]\d{2}
  - Light\s*Map\s*Resolution["\s:]*\d{4,}
### **Message**
Very high lightmap resolution (512+). This will increase bake time and memory significantly.
### **Fix Action**
Reserve high resolution (256-512) for hero surfaces only. Use 32-128 for most geometry.
### **Applies To**
  - *.unity
  - *.prefab
  - *.asset
  - *.uasset
  - *.ini

## Zero Lightmap UV Padding

### **Id**
lighting-zero-lightmap-padding
### **Severity**
error
### **Type**
regex
### **Pattern**
  - packMargin\s*[=:]\s*0(?:\.0+)?(?!\d)
  - Pack\s*Margin["\s:]*0(?:\.0+)?(?!\d)
### **Message**
Lightmap UV pack margin is 0. This causes visible seams between UV islands.
### **Fix Action**
Set pack margin to at least 2-4 texels worth (0.01-0.02 at typical resolutions).
### **Applies To**
  - *.unity
  - *.prefab
  - *.asset

## Excessive Shadow Distance

### **Id**
lighting-excessive-shadow-distance
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - shadowDistance\s*[=:]\s*\d{4,}
  - Shadow\s*Distance["\s:]*\d{4,}
  - ShadowMaxDistance\s*[=:]\s*\d{4,}
### **Message**
Shadow distance over 1000 units. This spreads shadow map resolution thin and impacts performance.
### **Fix Action**
Reduce shadow distance to match actual gameplay needs. Use fog to hide shadow pop-out.
### **Applies To**
  - *.unity
  - *.asset
  - *.ini
  - *.uasset

## Zero Shadow Bias

### **Id**
lighting-zero-shadow-bias
### **Severity**
error
### **Type**
regex
### **Pattern**
  - shadowBias\s*[=:]\s*0(?:\.0+)?(?!\d)
  - normalBias\s*[=:]\s*0(?:\.0+)?(?!\d)
  - ShadowDepthBias\s*[=:]\s*0(?:\.0+)?(?!\d)
### **Message**
Shadow bias is 0. This causes shadow acne (dotted patterns on surfaces).
### **Fix Action**
Set shadow bias to 0.05-0.1 and normal bias to 0.4-1.0. Tune for minimal peter-panning.
### **Applies To**
  - *.unity
  - *.prefab
  - *.asset
  - *.uasset

## Single Shadow Cascade Outdoor

### **Id**
lighting-single-shadow-cascade
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - shadowCascadeCount\s*[=:]\s*1(?!\d)
  - shadowCascades\s*[=:]\s*1(?!\d)
  - NumDynamicShadowCascades\s*[=:]\s*1(?!\d)
### **Message**
Only 1 shadow cascade configured. Outdoor scenes benefit from 2-4 cascades for quality distribution.
### **Fix Action**
Use 2-4 cascades for directional light. Tune cascade distances based on gameplay range.
### **Applies To**
  - *.unity
  - *.asset
  - *.ini
  - *.uasset

## Extreme Light Intensity

### **Id**
lighting-extreme-intensity
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - intensity\s*[=:]\s*\d{3,}
  - lightIntensity\s*[=:]\s*\d{3,}
  - Intensity\s*[=:]\s*\d{3,}
### **Message**
Light intensity over 100. Unless using physical light units, this may cause blown-out lighting.
### **Fix Action**
Review intensity in context of HDR pipeline. If using arbitrary units, keep most lights 0.5-3.
### **Applies To**
  - *.unity
  - *.prefab
  - *.asset
  - *.uasset
  - *.gd
  - *.tscn

## Pure Saturated Light Color

### **Id**
lighting-pure-color-light
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - color\s*[=:]\s*(?:Color\()?(?:1\.0,\s*0\.0,\s*0\.0|0\.0,\s*1\.0,\s*0\.0|0\.0,\s*0\.0,\s*1\.0)
  - LightColor\s*[=:]\s*\(R=(?:255|1\.0),G=0,B=0\)
  - LightColor\s*[=:]\s*\(R=0,G=(?:255|1\.0),B=0\)
  - LightColor\s*[=:]\s*\(R=0,G=0,B=(?:255|1\.0)\)
### **Message**
Pure saturated color light (pure red, green, or blue). This rarely looks natural.
### **Fix Action**
Use color temperatures for natural light (2700K-6500K). Desaturate for realistic appearance.
### **Applies To**
  - *.unity
  - *.prefab
  - *.asset
  - *.uasset
  - *.tscn

## Missing Reflection Probe in Interior

### **Id**
lighting-missing-reflection-probe
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ReflectionProbe
### **Message**
Check if reflection probes are present for interior spaces. Without them, interiors reflect the skybox.
### **Fix Action**
Add ReflectionProbe components in each distinct interior space with box projection enabled.
### **Applies To**
  - *.unity

## Potential Probe Inside Geometry

### **Id**
lighting-probe-inside-geometry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - LightProbeGroup
  - lightProbes
### **Message**
Review light probe placement. Auto-generated probes may be inside walls, causing black lighting.
### **Fix Action**
Manually inspect probe positions. Remove probes inside geometry. Add probes at lighting transitions.
### **Applies To**
  - *.unity
  - *.prefab

## Realtime Point Light Shadows

### **Id**
lighting-realtime-point-shadow
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - shadowType\s*[=:]\s*(?:Hard|Soft)(?:.*pointLight|point)
  - castShadows\s*[=:]\s*true(?:.*pointLight|point)
  - Point.*Shadow.*Type\s*[=:]\s*(?:Shadow|Raytraced)
### **Message**
Point light with realtime shadows enabled. This is expensive (6 shadow maps per light).
### **Fix Action**
Consider: baked shadows, only shadow from key point lights, or shadow-less fill lights.
### **Applies To**
  - *.unity
  - *.prefab
  - *.asset
  - *.uasset

## Many Realtime Lights

### **Id**
lighting-many-realtime-lights
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - lightType\s*[=:]\s*(?:Point|Spot)
### **Message**
Check realtime light count. Many realtime lights impact performance, especially with shadows.
### **Fix Action**
Use baked lighting where possible. Limit realtime to moving objects and key lights.
### **Applies To**
  - *.unity
  - *.prefab

## High Light Bounce Count

### **Id**
lighting-high-bounce-count
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - bounces\s*[=:]\s*[5-9]
  - bounces\s*[=:]\s*\d{2,}
  - NumIndirectLightingBounces\s*[=:]\s*[5-9]
  - NumSkyLightingBounces\s*[=:]\s*[5-9]
### **Message**
Light bounce count over 4. Higher bounces have diminishing returns and exponential bake time.
### **Fix Action**
2-3 bounces captures most indirect lighting. Only increase for very specific needs.
### **Applies To**
  - *.unity
  - *.asset
  - *.uasset
  - *.ini

## Bloom Threshold at Maximum

### **Id**
lighting-bloom-threshold-one
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - bloomThreshold\s*[=:]\s*1(?:\.0+)?(?!\d)
  - threshold\s*[=:]\s*1(?:\.0+)?(?:\s*//.*bloom)?
### **Message**
Bloom threshold at 1.0. If scene values are LDR (max 1.0), bloom won't appear.
### **Fix Action**
Set threshold relative to scene luminance. For HDR, 1.0-2.0. For LDR, 0.8-0.9.
### **Applies To**
  - *.unity
  - *.asset
  - *.cs
  - *.shader

## Missing Exposure Configuration

### **Id**
lighting-exposure-not-configured
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - exposure\s*[=:]\s*(?:null|None|0(?:\.0+)?)
### **Message**
Exposure may not be configured. Without proper exposure, HDR scenes will look incorrect.
### **Fix Action**
Set up exposure (auto or fixed) appropriate for scene brightness range.
### **Applies To**
  - *.unity
  - *.asset

## Realtime GI on Mobile Build

### **Id**
lighting-mobile-realtime-gi
### **Severity**
error
### **Type**
regex
### **Pattern**
  - realtimeGI\s*[=:]\s*true(?:.*mobile)?
  - UpdateGI\s*[=:]\s*true
### **Message**
Realtime GI detected which may be targeting mobile. This is too expensive for most mobile devices.
### **Fix Action**
Use fully baked lighting for mobile. Update probe data only at level load if needed.
### **Applies To**
  - *.unity
  - *.asset

## Volumetric Effects on Mobile

### **Id**
lighting-mobile-volumetrics
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - volumetric(?:Fog|Lighting|Clouds)\s*[=:]\s*true
  - VolumetricFog\s*[=:]\s*true
### **Message**
Volumetric effects enabled. These are typically too expensive for mobile platforms.
### **Fix Action**
Disable volumetrics on mobile quality tier. Use simple fog and particle effects instead.
### **Applies To**
  - *.unity
  - *.asset
  - *.uasset

## Manual Gamma Conversion in Lighting Shader

### **Id**
lighting-manual-gamma-in-shader
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pow\s*\([^,]+,\s*2\.2\s*\)
  - pow\s*\([^,]+,\s*0\.454
  - pow\s*\([^,]+,\s*1\.0\s*/\s*2\.2
### **Message**
Manual gamma conversion in shader. Ensure this is intentional and matches your color space settings.
### **Fix Action**
Use engine's linear/gamma workflow. Manual conversion should only be for specific cases.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl
  - *.cginc

## Light Direction Normalize in Fragment

### **Id**
lighting-normalize-in-fragment
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - normalize\s*\(\s*lightDir
  - normalize\s*\(\s*_WorldSpaceLightPos
### **Message**
Normalizing light direction per-pixel. For directional lights, this can be done once in vertex shader.
### **Fix Action**
For directional lights, normalize in vertex shader and interpolate. Point/spot need per-pixel.
### **Applies To**
  - *.shader
  - *.hlsl
  - *.glsl
  - *.cginc

## Missing Lightmass Importance Volume

### **Id**
lighting-unreal-no-importance-volume
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - LightmassImportanceVolume
### **Message**
Check for Lightmass Importance Volume. Without it, light baking quality suffers outside playable area.
### **Fix Action**
Add LightmassImportanceVolume covering all playable areas to focus bake quality.
### **Applies To**
  - *.umap
  - *.uasset

## Lumen Quality Settings

### **Id**
lighting-unreal-lumen-quality
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - LumenSceneLightingQuality\s*[=:]\s*(?:Low|Preview)
  - LumenReflectionsQuality\s*[=:]\s*(?:Low|Preview)
### **Message**
Lumen quality set to Low/Preview. Fine for development, ensure quality is set for final.
### **Fix Action**
Set appropriate Lumen quality for target platform. Test on target hardware.
### **Applies To**
  - *.ini
  - *.uasset

## SDFGI Without Bounds

### **Id**
lighting-godot-sdfgi-bounds
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - sdfgi_enabled\s*[=:]\s*true
### **Message**
SDFGI enabled. Ensure SDFGI bounds are properly configured for your scene size.
### **Fix Action**
Adjust SDFGI cascade sizes and max distance to match scene dimensions.
### **Applies To**
  - *.tscn
  - *.tres
  - *.gd

## Godot OmniLight Shadows

### **Id**
lighting-godot-omni-shadow
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - OmniLight3D(?:.*\n)*.*shadow_enabled\s*[=:]\s*true
### **Message**
OmniLight with shadows enabled. Point light shadows are expensive (6 renders per light).
### **Fix Action**
Limit shadowed omni lights. Consider SpotLight for directional shadows instead.
### **Applies To**
  - *.tscn
  - *.tres

## Three.js Shadow Without Bias

### **Id**
lighting-threejs-no-shadow-bias
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - castShadow\s*=\s*true(?:(?!bias).)*$
  - shadow\.(?!.*bias)
### **Message**
Shadow casting enabled but no bias configured. Default bias may cause shadow acne.
### **Fix Action**
Set light.shadow.bias = -0.0001 to -0.001 (adjust based on scene scale).
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## Three.js Default Shadow Map Size

### **Id**
lighting-threejs-shadow-map-size
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - castShadow\s*=\s*true(?:(?!mapSize).)*$
### **Message**
Shadow enabled but map size not configured. Default 512 may be too low for quality.
### **Fix Action**
Set light.shadow.mapSize.width/height = 1024 or 2048 for better quality.
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## Light Without Falloff/Attenuation

### **Id**
lighting-no-falloff
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - range\s*[=:]\s*(?:Infinity|0(?:\.0+)?)
  - attenuation\s*[=:]\s*(?:None|0)
### **Message**
Light without proper falloff/attenuation. Infinite range lights are unrealistic and can impact performance.
### **Fix Action**
Set appropriate range based on light intensity. Use inverse-square falloff for realism.
### **Applies To**
  - *.unity
  - *.prefab
  - *.asset
  - *.tscn
  - *.js
  - *.ts