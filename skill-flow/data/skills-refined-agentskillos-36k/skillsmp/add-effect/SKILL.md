---
name: add-effect
description: This skill should be used when the user asks to "add a new effect", "create a transform effect", "implement a visual effect", "add a post-process shader", or when planning effect implementation. Provides the complete checklist of files to modify and commonly-missed steps.
---

# Adding a Transform Effect

Follow this checklist when adding a new transform effect to AudioJones. Each section lists required modifications with file paths relative to repository root.

## Checklist Overview

Transform effects require changes to 11 locations across 8 files. Three steps are commonly missed:

1. **TransformOrderConfig::order array** - Effect won't appear in reorder UI
2. **GetTransformCategory() case** - Effect shows "???" badge in pipeline list
3. **param_registry.cpp entries** - Modulatable parameters won't respond to LFOs/audio

## Phase 1: Config Header

Create `src/config/{effect_name}_config.h`:

```cpp
#ifndef {EFFECT_NAME}_CONFIG_H
#define {EFFECT_NAME}_CONFIG_H

struct {EffectName}Config {
    bool enabled = false;
    // Add effect-specific parameters with defaults
};

#endif
```

Use snake_case for filename, PascalCase for struct name.

## Phase 2: Effect Registration

Modify `src/config/effect_config.h`:

1. **Add include** at top with other config headers:
   ```cpp
   #include "{effect_name}_config.h"
   ```

2. **Add enum entry** in `TransformEffectType` before `TRANSFORM_EFFECT_COUNT`:
   ```cpp
   TRANSFORM_{EFFECT_NAME},
   ```

3. **Add name case** in `TransformEffectName()`:
   ```cpp
   case TRANSFORM_{EFFECT_NAME}: return "Effect Name";
   ```

4. **Add to order array** in `TransformOrderConfig::order` initialization:
   ```cpp
   TRANSFORM_{EFFECT_NAME}
   ```
   Place at end of array, before closing brace. **COMMONLY MISSED.**

5. **Add config member** to `EffectConfig` struct:
   ```cpp
   {EffectName}Config {effectName};
   ```

6. **Add enabled case** in `IsTransformEnabled()`:
   ```cpp
   case TRANSFORM_{EFFECT_NAME}: return e->{effectName}.enabled;
   ```

## Phase 3: Shader

Create `shaders/{effect_name}.fs`:

```glsl
#version 330

in vec2 fragTexCoord;
out vec4 finalColor;

uniform sampler2D texture0;
uniform vec2 resolution;
// Add effect-specific uniforms

void main() {
    vec2 uv = fragTexCoord;
    vec4 color = texture(texture0, uv);

    // Effect algorithm here

    finalColor = color;
}
```

## Phase 4: PostEffect Integration

Modify `src/render/post_effect.h`:

1. **Add shader member** in `PostEffect` struct:
   ```cpp
   Shader {effectName}Shader;
   ```

2. **Add uniform location members**:
   ```cpp
   int {effectName}ResolutionLoc;
   int {effectName}{ParamName}Loc;
   // One int per uniform
   ```

Modify `src/render/post_effect.cpp`:

3. **Load shader** in `LoadPostEffectShaders()`:
   ```cpp
   pe->{effectName}Shader = LoadShader(0, "shaders/{effect_name}.fs");
   ```

4. **Add to success check** (same function):
   ```cpp
   && pe->{effectName}Shader.id != 0
   ```

5. **Get uniform locations** in `GetShaderUniformLocations()`:
   ```cpp
   pe->{effectName}ResolutionLoc = GetShaderLocation(pe->{effectName}Shader, "resolution");
   pe->{effectName}{ParamName}Loc = GetShaderLocation(pe->{effectName}Shader, "{paramName}");
   ```

6. **Add to resolution uniforms** in `SetResolutionUniforms()` if shader uses resolution:
   ```cpp
   SetShaderValue(pe->{effectName}Shader, pe->{effectName}ResolutionLoc, res, SHADER_UNIFORM_VEC2);
   ```

7. **Unload shader** in `PostEffectUninit()`:
   ```cpp
   UnloadShader(pe->{effectName}Shader);
   ```

## Phase 5: Shader Setup

Modify `src/render/shader_setup.h`:

1. **Declare setup function**:
   ```cpp
   void Setup{EffectName}(PostEffect* pe);
   ```

Modify `src/render/shader_setup.cpp`:

2. **Add dispatch case** in `GetTransformEffect()`:
   ```cpp
   case TRANSFORM_{EFFECT_NAME}:
       return { &pe->{effectName}Shader, Setup{EffectName}, &pe->effects.{effectName}.enabled };
   ```

3. **Implement setup function**:
   ```cpp
   void Setup{EffectName}(PostEffect* pe) {
       const {EffectName}Config* cfg = &pe->effects.{effectName};
       SetShaderValue(pe->{effectName}Shader, pe->{effectName}{ParamName}Loc,
                      &cfg->{paramName}, SHADER_UNIFORM_FLOAT);
   }
   ```

## Phase 6: UI Panel

Modify `src/ui/imgui_effects.cpp`:

1. **Add category mapping** in `GetTransformCategory()` switch statement. Match the category to whichever `Draw*Category()` function contains your UI controls. **COMMONLY MISSED.**

Modify `src/ui/imgui_effects_{category}.cpp`:

1. **Add section state** at file top with other static bools:
   ```cpp
   static bool section{EffectName} = false;
   ```

2. **Add helper function** before the appropriate `Draw*Category()`:
   ```cpp
   static void Draw{Category}{EffectName}(EffectConfig* e, const ModSources* modSources, const ImU32 categoryGlow)
   {
       if (DrawSectionBegin("Effect Name", categoryGlow, &section{EffectName})) {
           const bool wasEnabled = e->{effectName}.enabled;
           ImGui::Checkbox("Enabled##{id}", &e->{effectName}.enabled);
           if (!wasEnabled && e->{effectName}.enabled) { MoveTransformToEnd(&e->transformOrder, TRANSFORM_{EFFECT_NAME}); }
           if (e->{effectName}.enabled) {
               ModulatableSlider("Param", &e->{effectName}.param, "effectName.param", "%.2f", modSources);
           }
           DrawSectionEnd();
       }
   }
   ```

3. **Add helper call** in the orchestrator with spacing:
   ```cpp
   ImGui::Spacing();
   Draw{Category}{EffectName}(e, modSources, categoryGlow);
   ```

   Use `ModulatableSlider` for parameters that should respond to modulation.
   Use `ModulatableSliderAngleDeg` for angular parameters (displays degrees, stores radians).

## Phase 7: Preset Serialization

Modify `src/config/preset.cpp`:

1. **Add JSON macro** with other config macros:
   ```cpp
   NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE_WITH_DEFAULT({EffectName}Config, enabled, {param1}, {param2})
   ```

2. **Add to_json entry** in `to_json(json& j, const EffectConfig& e)`:
   ```cpp
   if (e.{effectName}.enabled) { j["{effectName}"] = e.{effectName}; }
   ```

3. **Add from_json entry** in `from_json(const json& j, EffectConfig& e)`:
   ```cpp
   e.{effectName} = j.value("{effectName}", e.{effectName});
   ```

## Phase 8: Parameter Registration (if modulatable)

Modify `src/automation/param_registry.cpp`:

1. **Add to PARAM_TABLE**:
   ```cpp
   {"{effectName}.{param}", {{min}f, {max}f}},
   ```

2. **Add to targets array** (search for `float* targets[]`):
   ```cpp
   &effects->{effectName}.{param},
   ```

Entries in PARAM_TABLE and targets array must be at matching indices. **COMMONLY MISSED.**

For angular parameters, use the constants from `ui_units.h`:
- `ROTATION_SPEED_MAX` for speed fields (radians/second)
- `ROTATION_OFFSET_MAX` for angle/twist fields (radians)

## Verification

After implementation, verify:

- [ ] Effect appears in transform order pipeline
- [ ] Effect shows correct category badge (not "???")
- [ ] Effect can be reordered via drag-drop
- [ ] Enabling effect adds it to the pipeline list
- [ ] UI controls modify effect in real-time
- [ ] Preset save/load preserves settings
- [ ] Modulation routes to registered parameters (if applicable)
- [ ] Build succeeds with no warnings

## File Summary

| File | Changes |
|------|---------|
| `src/config/{effect}_config.h` | Create config struct |
| `src/config/effect_config.h` | Include, enum, name, order array, member, IsTransformEnabled case |
| `shaders/{effect}.fs` | Create fragment shader |
| `src/render/post_effect.h` | Shader and uniform location members |
| `src/render/post_effect.cpp` | Load, check, locations, resolution, unload |
| `src/render/shader_setup.h` | Declare Setup function |
| `src/render/shader_setup.cpp` | Dispatch case and Setup implementation |
| `src/ui/imgui_effects.cpp` | GetTransformCategory case |
| `src/ui/imgui_effects_{category}.cpp` | Section state and UI controls |
| `src/config/preset.cpp` | JSON macro, to_json, from_json |
| `src/automation/param_registry.cpp` | PARAM_TABLE and targets entries |
