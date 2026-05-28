# Godot - Shaders

**Pages:** 15

---

## Reducing stutter from shader (pipeline) compilations — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/pipeline_compilations.html

**Contents:**
- Reducing stutter from shader (pipeline) compilations
- Pipeline precompilation monitors
- Pipeline precompilation features
- Pipeline precompilation instancing
- Shader baker
- User-contributed notes

Pipeline compilation, also commonly known as shader compilation, is an expensive operation required by the engine to be able to draw any kind of content with the GPU.

Shaders and materials in Godot go through several steps before they can be run by the GPU.

In more precise terms, shader compilation involves the translation of the GLSL code that Godot generates into an intermediate format that can be shared across systems (such as SPIR-V when using Vulkan). However, this format can't be used by the GPU directly.

Pipeline compilation is the step where the GPU driver converts the intermediate shader format (the result from shader compilation) to something the GPU can actually use for rendering. Drivers usually keep a cache of pipelines stored somewhere in the system to avoid repeating the process every time a game is run. This cache is usually deleted when the driver is updated.

Pipelines contain more information than just the shader code, which means that for each shader, there can be dozens of pipelines or more! This makes it difficult for an engine to compile them ahead of time, both because it would be very slow, and because it would take up a lot of memory. On top of that, this step can only be performed on the user's system and it is very tough to share the result between users unless they have the exact same hardware and driver version.

Before Godot 4.4, there was no solution to pipeline compilation other than generating them when an object shows up inside the camera's view, leading to the infamous shader stutter or hitches that only occur during the first playthrough. With Godot 4.4, new mechanisms have been introduced to mitigate stutters from pipeline compilation.

Ubershaders: Godot makes use of specialization constants, a feature that allows the driver to optimize a pipeline's code around a set of parameters such as lighting, shadow quality, etc. Specialization constants are used to optimize a shader by limiting unnecessary features. Changing a specialization constant requires recompiling the pipeline. Ubershaders are a special version of the shader that are able to change these constants while rendering, which means Godot can precompile just one pipeline ahead of time and compile the more optimized versions on the background during gameplay. This reduces the amount of pipelines that need to be created significantly.

Pipeline precompilation: By using ubershaders, the engine can precompile pipelines ahead of time in multiple places such as when meshes are loaded or when nodes are added to the scene. By being part of the resource loading process, pipelines can even be precompiled in multiple background threads if possible during loading screens or even gameplay.

Starting in Godot 4.4, Godot will detect which pipelines are needed and precompile them at load-time. This detection system is mostly automatic, but it relies on the RenderingServer seeing evidence of all shaders, meshes, or rendering features at load-time. For example, if you load a mesh and shader while the game is running, the pipeline for that mesh/shader combination won't be compiled until the mesh/shader is loaded. Similarly, things like enabling MSAA, or instancing a VoxelGI node while the game is running will trigger pipeline recompilations.

Compiling pipelines ahead of time is the main mechanism Godot uses to mitigate shader stutters, but it's not a perfect solution. Being aware of the situations that can lead to pipeline stutters can be very helpful, and the workarounds are pretty straightforward compared to previous versions. These workarounds may be less necessary over time with future versions of Godot as more detection techniques are implemented.

The Godot debugger offers monitors for tracking the amount of pipelines created by the game and the step that triggered their compilation. You can keep an eye on these monitors as the game runs to identify potential sources of shader stutters without having to wipe your driver cache every time you wish to test. Sudden increases of these values outside of loading screens can show up as hitches during gameplay the first time someone plays the game on their system. It is recommended you take a look at these monitors to identify possible sources of stutter for your players, as you might be unable to experience them yourself without deleting your driver cache or testing on a weaker system.

Pipeline compilations of one of the demo projects.

We can see the pipelines compiled during gameplay and verify which steps could possibly cause stuttters. Note that these values will only increase and never go down, as deleted pipelines are not tracked by these monitors and pipelines may be erased and recreated during gameplay.

Canvas: Compiled when drawing a 2D node. The engine does not currently feature precompilation for 2D elements and stutters will show up when the 2D node is drawn for the first time.

Mesh: Compiled as part of loading a 3D mesh and identifying what pipelines can be precompiled from its properties. These can lead to stutters if a mesh is loaded during gameplay, but they can be mitigated if the mesh is loaded by using a background thread. Modifiers that are part of nodes such as material overrides can't be compiled on this step.

Surface: Compiled when a frame is about to be drawn and 3D objects were instanced on the scene tree for the first time. This can also include compilation for nodes that aren't even visible on the scene tree. The stutter will occur only on the first frame the node is added to the scene, which won't result in an obvious stutter if it happens right after a loading screen.

Draw: Compiled on demand when a 3D object needs to be drawn and an ubershader was not precompiled ahead of time. The engine is unable to precompile this pipeline due to triggering a case that hasn't been covered yet or a modification that was done to the engine's code. Leads to stutters during gameplay. This is identical to Godot versions before 4.4. If you see compilations here, please let the developers know <https://github.com/godotengine/godot/issues> as this should never happen with the Ubershader system. Make sure to attach a minimal reproduction project when doing so.

Specialization: Compiled in the background during gameplay to optimize the framerate. Unable to cause stutters, but may result in reduced framerates if there are many happening per frame.

Godot offers a lot of rendering features that are not necessarily used by every game. Unfortunately, pipeline precompilation can't know ahead of time if a particular feature is used by a project. Some of these features can only be detected when a user adds a node to the scene or toggles a particular setting in the project or the environment. The pipeline precompilation system will keep track of these features as they're encountered for the first time and enable precompilation of them for any meshes or surfaces that are created afterwards.

If your game makes use of these features, make sure to have a scene that uses them as early as possible before loading the majority of the assets. This scene can be very simple and will do the job as long as it uses the features the game plans to use. It can even be rendered off-screen for at least one frame if necessary, e.g. by covering it with a ColorRect node or using a SubViewport located outside the window bounds.

You should also keep in mind that changing any of these features during gameplay will result in immediate stutters. Make sure to only change these features from configuration screens if necessary and insert loading screens and messages when the changes are applied.

MSAA Level: Enabled when the level of 3D MSAA is changed on the project settings. Unfortunately, different MSAA levels being used on different viewports will lead to stutters as the engine only keeps track of one level at a time to perform precompilation.

Reflection Probes: Enabled when a ReflectionProbe node is placed on the scene.

Separate Specular: Enabled when using effects like sub-surface scattering or a compositor effect that relies on sampling the specularity directly off the screen.

Motion Vectors: Enabled when using effects such as TAA, FSR2 or a compositor effect that requires motion vectors (such as motion blur).

Normal and Roughness: Enabled when using SDFGI, VoxelGI, screen-space reflections, SSAO, SSIL, or using the normal_roughness_buffer in a custom shader or CompositorEffect.

Lightmaps: Enabled when a LightmapGI node is placed on the scene and a node uses a baked lightmap.

VoxelGI: Enabled when a VoxelGI node is placed on the scene.

SDFGI: Enabled when the WorldEnvironment enables SDFGI.

Multiview: Enabled for XR projects.

16/32-bit Shadows: Enabled when the configuration of the depth precision of shadowmaps is changed on the project settings.

Omni Shadow Dual Paraboloid: Enabled when an omni light casts shadows and uses the dual paraboloid mode.

Omni Shadow Cubemap: Enabled when an omni light casts shadows and uses the cubemap mode (which is the default).

If you witness stutters during gameplay and the monitors report a sudden increase in compilations during the Surface step, it is very likely a feature was not enabled ahead of time. Ensuring that this effect is enabled while loading your game will likely mitigate the issue.

One common source of stutters in games is the fact that some effects are only instanced on the scene because of interactions that only happen during gameplay. For example, if you have a particle effect that is only added to the scene through a script when a player does an action. Even if the scene is preloaded, the engine might be unable to precompile the pipelines until the effect is added to the scene at least once.

Luckily, it's possible for Godot 4.4 and later to precompile these pipelines as long as the scene is instantiated at least once on the scene, even if it's completely invisible or outside of the camera's view.

Hidden bullet node attached to the player in one of the demo projects. This helps the engine precompile the effect's pipelines ahead of time.

If you're aware of any effects that are added to the scene dynamically during gameplay and are seeing sudden increases on the compilations monitor when these effects show up, a workaround is to attach a hidden version of the effect somewhere that is guaranteed to show up.

For example, if the player character is able to cause some sort of explosion, you can attach the effect as a child of the player as an invisible node. Make sure to disable the script attached to the hidden node or to hide any other nodes that could cause issues, which can be done by enabling Editable Children on the node.

Since Godot 4.5, you can choose to bake shaders on export to improve initial startup time. This will generally not resolve existing stutters, but it will reduce the time it takes to load the game for the first time. This is especially the case when using Direct3D 12 or Metal, which have significantly slower initial shader compilation times than Vulkan due to the conversion step required. Godot's own shaders use GLSL and SPIR-V, but Direct3D 12 and Metal use different formats.

The shader baker can only bake the source into the intermediate format (SPIR-V for Vulkan, DXIL for Direct3D 12, MIL for Metal). It cannot bake the intermediate format into the final pipeline, as this is dependent on the GPU driver and the hardware.

The shader baker is not a replacement for pipeline precompilation, but it aims to complement it.

When enabled, the shader baker will bundle compiled shader code into the PCK, which results in the shader compilation step being skipped entirely. The downside is that exporting will take slightly longer. The PCK file will be larger by a few megabytes.

The shader baker is disabled by default, but you can enable it in each export preset in the Export dialog by ticking the Shader Baker > Enabled export option.

Note that shader baking will only be able to export shaders for drivers supported by the platform the editor is currently running on:

The editor running on Windows can export shaders for Vulkan and Direct3D 12.

The editor running on macOS can export shaders for Vulkan and Metal.

The editor running on Linux can export shaders for Vulkan only.

The editor running on Android can export shaders for Vulkan only.

The shader baker will only export shaders that match the rendering/rendering_device/driver project setting for the target platform.

The shader baker is only supported for the Forward+ and Mobile renderers. It will have no effect if the project uses the Compatibility renderer, or for users who make use of the Compatibility fallback due to their hardware not supporting the Forward+ or Mobile renderer.

This also means the shader baker is not supported on the web platform, as the web platform only supports the Compatibility renderer.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Visual Shader plugins — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/plugins/editor/visual_shader_plugins.html

**Contents:**
- Visual Shader plugins
- User-contributed notes

Visual Shader plugins are used to create custom VisualShader nodes in GDScript.

The creation process is different from usual editor plugins. You do not need to create a plugin.cfg file to register it; instead, create and save a script file and it will be ready to use, provided the custom node is registered with class_name.

This short tutorial will explain how to make a Perlin-3D noise node (original code from this GPU noise shaders plugin.

Create a Sprite2D and assign a ShaderMaterial to its material slot:

Assign VisualShader to the shader slot of the material:

Don't forget to change its mode to "CanvasItem" (if you are using a Sprite2D):

Create a script which derives from VisualShaderNodeCustom. This is all you need to initialize your plugin.

Save it and open the Visual Shader. You should see your new node type within the member's dialog under the Addons category (if you can't see your new node, try restarting the editor):

Place it on a graph and connect the required ports:

That is everything you need to do, as you can see it is easy to create your own custom VisualShader nodes!

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
# perlin_noise_3d.gd
@tool
extends VisualShaderNodeCustom
class_name VisualShaderNodePerlinNoise3D


func _get_name():
    return "PerlinNoise3D"


func _get_category():
    return "MyShaderNodes"


func _get_description():
    return "Classic Perlin-Noise-3D function (by Curly-Brace)"


func _init():
    set_input_port_default_value(2, 0.0)


func _get_return_icon_type():
    return VisualShaderNode.PORT_TYPE_SCALAR


func _get_input_port_count():
    return 4


func _get_input_port_name(port):
    match port:
        0:
            return "uv"
        1:
            return "offset"
        2:
            return "scale"
        3:
            return "time"


func _get_input_port_type(port):
    match port:
        0:
            return VisualShaderNode.PORT_TYPE_VECTOR_3D
        1:
            return VisualShaderNode.PORT_TYPE_VECTOR_3D
        2:
            return VisualShaderNode.PORT_TYPE_SCALAR
        3:
            return VisualShaderNode.PORT_TYPE_SCALAR


func _get_output_port_count():
    return 1


func _get_output_port_name(port):
    return "result"


func _get_output_port_type(port):
    return VisualShaderNode.PORT_TYPE_SCALAR


func _get_global_code(mode):
    return """
        vec3 mod289_3(vec3 x) {
            return x - floor(x * (1.0 / 289.0)) * 289.0;
        }

        vec4 mod289_4(vec4 x) {
            return x - floor(x * (1.0 / 289.0)) * 289.0;
        }

        vec4 permute(vec4 x) {
            return mod289_4(((x * 34.0) + 1.0) * x);
        }

        vec4 taylorInvSqrt(vec4 r) {
            return 1.79284291400159 - 0.85373472095314 * r;
        }

        vec3 fade(vec3 t) {
            return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
        }

        // Classic Perlin noise.
        float cnoise(vec3 P) {
            vec3 Pi0 = floor(P); // Integer part for indexing.
            vec3 Pi1 = Pi0 + vec3(1.0); // Integer part + 1.
            Pi0 = mod289_3(Pi0);
            Pi1 = mod289_3(Pi1);
            vec3 Pf0 = fract(P); // Fractional part for interpolation.
            vec3 Pf1 = Pf0 - vec3(1.0); // Fractional part - 1.0.
            vec4 ix = vec4(Pi0.x, Pi1.x, Pi0.x, Pi1.x);
            vec4 iy = vec4(Pi0.yy, Pi1.yy);
            vec4 iz0 = vec4(Pi0.z);
            vec4 iz1 = vec4(Pi1.z);

            vec4 ixy = permute(permute(ix) + iy);
            vec4 ixy0 = permute(ixy + iz0);
            vec4 ixy1 = permute(ixy + iz1);

            vec4 gx0 = ixy0 * (1.0 / 7.0);
            vec4 gy0 = fract(floor(gx0) * (1.0 / 7.0)) - 0.5;
            gx0 = fract(gx0);
            vec4 gz0 = vec4(0.5) - abs(gx0) - abs(gy0);
            vec4 sz0 = step(gz0, vec4(0.0));
            gx0 -= sz0 * (step(0.0, gx0) - 0.5);
            gy0 -= sz0 * (step(0.0, gy0) - 0.5);

            vec4 gx1 = ixy1 * (1.0 / 7.0);
            vec4 gy1 = fract(floor(gx1) * (1.0 / 7.0)) - 0.5;
            gx1 = fract(gx1);
            vec4 gz1 = vec4(0.5) - abs(gx1) - abs(gy1);
            vec4 sz1 = step(gz1, vec4(0.0));
            gx1 -= sz1 * (step(0.0, gx1) - 0.5);
            gy1 -= sz1 * (step(0.0, gy1) - 0.5);

            vec3 g000 = vec3(gx0.x, gy0.x, gz0.x);
            vec3 g100 = vec3(gx0.y, gy0.y, gz0.y);
            vec3 g010 = vec3(gx0.z, gy0.z, gz0.z);
            vec3 g110 = vec3(gx0.w, gy0.w, gz0.w);
            vec3 g001 = vec3(gx1.x, gy1.x, gz1.x);
            vec3 g101 = vec3(gx1.y, gy1.y, gz1.y);
            vec3 g011 = vec3(gx1.z, gy1.z, gz1.z);
            vec3 g111 = vec3(gx1.w, gy1.w, gz1.w);

            vec4 norm0 = taylorInvSqrt(vec4(dot(g000, g000), dot(g010, g010), dot(g100, g100), dot(g110, g110)));
            g000 *= norm0.x;
            g010 *= norm0.y;
            g100 *= norm0.z;
            g110 *= norm0.w;
            vec4 norm1 = taylorInvSqrt(vec4(dot(g001, g001), dot(g011, g011), dot(g101, g101), dot(g111, g111)));
            g001 *= norm1.x;
            g011 *= norm1.y;
            g101 *= norm1.z;
            g111 *= norm1.w;

            float n000 = dot(g000, Pf0);
            float n100 = dot(g100, vec3(Pf1.x, Pf0.yz));
            float n010 = dot(g010, vec3(Pf0.x, Pf1.y, Pf0.z));
            float n110 = dot(g110, vec3(Pf1.xy, Pf0.z));
            float n001 = dot(g001, vec3(Pf0.xy, Pf1.z));
            float n101 = dot(g101, vec3(Pf1.x, Pf0.y, Pf1.z));
            float n011 = dot(g011, vec3(Pf0.x, Pf1.yz));
            float n111 = dot(g111, Pf1);

            vec3 fade_xyz = fade(Pf0);
            vec4 n_z = mix(vec4(n000, n100, n010, n110), vec4(n001, n101, n011, n111), fade_xyz.z);
            vec2 n_yz = mix(n_z.xy, n_z.zw, fade_xyz.y);
            float n_xyz = mix(n_yz.x, n_yz.y, fade_xyz.x);
            return 2.2 * n_xyz;
        }
    """


func _get_code(input_vars, output_vars, mode, type):
    return output_vars[0] + " = cnoise(vec3((%s.xy + %s.xy) * %s, %s)) * 0.5 + 0.5;" % [input_vars[0], input_vars[1], input_vars[2], input_vars[3]]
```

---

## Shading reference — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/index.html

**Contents:**
- Shading reference

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Shaders — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/index.html

**Contents:**
- Shaders

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Particle shaders — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/particle_shader.html

**Contents:**
- Particle shaders
- Render modes
- Built-ins
- Global built-ins
- Start and Process built-ins
- Start built-ins
- Process built-ins
- Process functions
- User-contributed notes

Particle shaders are a special type of shader that runs before the object is drawn. They are used for calculating material properties such as color, position, and rotation. They are drawn with any regular material for CanvasItem or Spatial, depending on whether they are 2D or 3D.

Particle shaders are unique because they are not used to draw the object itself; they are used to calculate particle properties, which are then used by a CanvasItem or Spatial shader. They contain two processor functions: start() and process().

Unlike other shader types, particle shaders keep the data that was output the previous frame. Therefore, particle shaders can be used for complex effects that take place over multiple frames.

Particle shaders are only available with GPU-based particle nodes (GPUParticles2D and GPUParticles3D).

CPU-based particle nodes (CPUParticles2D and CPUParticles3D) are rendered on the GPU (which means they can use custom CanvasItem or Spatial shaders), but their motion is simulated on the CPU.

Do not clear previous data on restart.

Disable attractor force.

Ignore VELOCITY value.

Scale the particle's size for collisions.

Values marked as in are read-only. Values marked as out can optionally be written to and will not necessarily contain sensible values. Values marked as inout provide a sensible default value, and can optionally be written to. Samplers cannot be written to so they are not marked.

Global built-ins are available everywhere, including custom functions.

Global time since the engine has started, in seconds. It repeats after every 3,600 seconds (which can be changed with the rollover setting). It's affected by time_scale but not by pausing. If you need a TIME variable that is not affected by time scale, add your own global shader uniform and update it each frame.

A PI constant (3.141592). A ratio of a circle's circumference to its diameter and amount of radians in half turn.

A TAU constant (6.283185). An equivalent of PI * 2 and amount of radians in full turn.

An E constant (2.718281). Euler's number and a base of the natural logarithm.

These properties can be accessed from both the start() and process() functions.

Unique number since emission start.

Particle index (from total particles).

in mat4 EMISSION_TRANSFORM

Emitter transform (used for non-local systems).

Random seed used as base for random.

true when the particle is active, can be set false.

Particle color, can be written to and accessed in mesh's vertex function.

Particle velocity, can be modified.

Custom particle data. Accessible from shader of mesh as INSTANCE_CUSTOM.

Particle mass, intended to be used with attractors. Equals 1.0 by default.

Vector that enables the integration of supplementary user-defined data into the particle process shader. USERDATAX are six built-ins identified by number, X can be numbers between 1 and 6, for example USERDATA3.

in uint FLAG_EMIT_POSITION

A flag for using on the last argument of emit_subparticle() function to assign a position to a new particle's transform.

in uint FLAG_EMIT_ROT_SCALE

A flag for using on the last argument of emit_subparticle() function to assign the rotation and scale to a new particle's transform.

in uint FLAG_EMIT_VELOCITY

A flag for using on the last argument of emit_subparticle() function to assign a velocity to a new particle.

in uint FLAG_EMIT_COLOR

A flag for using on the last argument of emit_subparticle() function to assign a color to a new particle.

in uint FLAG_EMIT_CUSTOM

A flag for using on the last argument of emit_subparticle() function to assign a custom data vector to a new particle.

in vec3 EMITTER_VELOCITY

Velocity of the Particles2D (3D) node.

in float INTERPOLATE_TO_END

Value of interp_to_end (3D) property of Particles node.

Value of amount_ratio (3D) property of Particles node.

In order to use the COLOR variable in a StandardMaterial3D, set vertex_color_use_as_albedo to true. In a ShaderMaterial, access it with the COLOR variable.

in bool RESTART_POSITION

true if particle is restarted, or emitted without a custom position (i.e. this particle was created by emit_subparticle() without the FLAG_EMIT_POSITION flag).

in bool RESTART_ROT_SCALE

true if particle is restarted, or emitted without a custom rotation or scale (i.e. this particle was created by emit_subparticle() without the FLAG_EMIT_ROT_SCALE flag).

in bool RESTART_VELOCITY

true if particle is restarted, or emitted without a custom velocity (i.e. this particle was created by emit_subparticle() without the FLAG_EMIT_VELOCITY flag).

in bool RESTART_COLOR

true if particle is restarted, or emitted without a custom color (i.e. this particle was created by emit_subparticle() without the FLAG_EMIT_COLOR flag).

in bool RESTART_CUSTOM

true if particle is restarted, or emitted without a custom property (i.e. this particle was created by emit_subparticle() without the FLAG_EMIT_CUSTOM flag).

true if the current process frame is first for the particle.

true when the particle has collided with a particle collider.

in vec3 COLLISION_NORMAL

A normal of the last collision. If there is no collision detected it is equal to (0.0, 0.0, 0.0).

in float COLLISION_DEPTH

A length of normal of the last collision. If there is no collision detected it is equal to 0.0.

in vec3 ATTRACTOR_FORCE

A combined force of the attractors at the moment on that particle.

emit_subparticle() is currently the only custom function supported by particles shaders. It allows users to add a new particle with specified parameters from a sub-emitter. The newly created particle will only use the properties that match the flags parameter. For example, the following code will emit a particle with a specified position, velocity, and color, but unspecified rotation, scale, and custom value:

bool emit_subparticle (mat4 xform, vec3 velocity, vec4 color, vec4 custom, uint flags)

Emits a particle from a sub-emitter.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
mat4 custom_transform = mat4(1.0);
custom_transform[3].xyz = vec3(10.5, 0.0, 4.0);
emit_subparticle(custom_transform, vec3(1.0, 0.5, 1.0), vec4(1.0, 0.0, 0.0, 1.0), vec4(1.0), FLAG_EMIT_POSITION | FLAG_EMIT_VELOCITY | FLAG_EMIT_COLOR);
```

---

## Shader preprocessor — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shader_preprocessor.html

**Contents:**
- Shader preprocessor
- Why use a shader preprocessor?
- Directives
  - General syntax
  - #define
  - #undef
  - #if
  - #elif
  - #ifdef
  - #ifndef

In programming languages, a preprocessor allows changing the code before the compiler reads it. Unlike the compiler, the preprocessor does not care about whether the syntax of the preprocessed code is valid. The preprocessor always performs what the directives tell it to do. A directive is a statement starting with a hash symbol (#). It is not a keyword of the shader language (such as if or for), but a special kind of token within the language.

From Godot 4.0 onwards, you can use a shader preprocessor within text-based shaders. The syntax is similar to what most GLSL shader compilers support (which in turn is similar to the C/C++ preprocessor).

The shader preprocessor is not available in visual shaders. If you need to introduce preprocessor statements to a visual shader, you can convert it to a text-based shader using the Convert to Shader option in the VisualShader inspector resource dropdown. This conversion is a one-way operation; text shaders cannot be converted back to visual shaders.

Preprocessor directives do not use brackets ({}), but can use parentheses.

Preprocessor directives never end with semicolons (with the exception of #define, where this is allowed but potentially dangerous).

Preprocessor directives can span several lines by ending each line with a backslash (\). The first line break not featuring a backslash will end the preprocessor statement.

Syntax: #define <identifier> [replacement_code].

Defines the identifier after that directive as a macro, and replaces all successive occurrences of it with the replacement code given in the shader. Replacement is performed on a "whole words" basis, which means no replacement is performed if the string is part of another string (without any spaces or operators separating it).

Defines with replacements may also have one or more arguments, which can then be passed when referencing the define (similar to a function call).

If the replacement code is not defined, the identifier may only be used with #ifdef or #ifndef directives.

If the concatenation symbol (##) is present in the replacement code then it will be removed upon macro insertion, together with any space surrounding it, and join the surrounding words and arguments into a new token.

Compared to constants (const CONSTANT = value;), #define can be used anywhere within the shader (including in uniform hints). #define can also be used to insert arbitrary shader code at any location, while constants can't do that.

Defining a #define for an identifier that is already defined results in an error. To prevent this, use #undef <identifier>.

Syntax: #undef identifier

The #undef directive may be used to cancel a previously defined #define directive:

Without #undef in the above example, there would be a macro redefinition error.

Syntax: #if <condition>

The #if directive checks whether the condition passed. If it evaluates to a non-zero value, the code block is included, otherwise it is skipped.

To evaluate correctly, the condition must be an expression giving a simple floating-point, integer or boolean result. There may be multiple condition blocks connected by && (AND) or || (OR) operators. It may be continued by an #else block, but must be ended with the #endif directive.

Using the defined() preprocessor function, you can check whether the passed identifier is defined a by #define placed above that directive. This is useful for creating multiple shader versions in the same file. It may be continued by an #else block, but must be ended with the #endif directive.

The defined() function's result can be negated by using the ! (boolean NOT) symbol in front of it. This can be used to check whether a define is not set.

Be careful, as defined() must only wrap a single identifier within parentheses, never more:

In the shader editor, preprocessor branches that evaluate to false (and are therefore excluded from the final compiled shader) will appear grayed out. This does not apply to runtime if statements.

#if preprocessor versus if statement: Performance caveats

The shading language supports runtime if statements:

If the uniform is never changed, this behaves identical to the following usage of the #if preprocessor statement:

However, the #if variant can be faster in certain scenarios. This is because all runtime branches in a shader are still compiled and variables within those branches may still take up register space, even if they are never run in practice.

Modern GPUs are quite effective at performing "static" branching. "Static" branching refers to if statements where all pixels/vertices evaluate to the same result in a given shader invocation. However, high amounts of VGPRs (which can be caused by having too many branches) can still slow down shader execution significantly.

The #elif directive stands for "else if" and checks the condition passed if the above #if evaluated to false. #elif can only be used within an #if block. It is possible to use several #elif statements after an #if statement.

Like with #if, the defined() preprocessor function can be used:

Syntax: #ifdef <identifier>

This is a shorthand for #if defined(...). Checks whether the passed identifier is defined by #define placed above that directive. This is useful for creating multiple shader versions in the same file. It may be continued by an #else block, but must be ended with the #endif directive.

The processor does not support #elifdef as a shortcut for #elif defined(...). Instead, use the following series of #ifdef and #else when you need more than two branches:

Syntax: #ifndef <identifier>

This is a shorthand for #if !defined(...). Similar to #ifdef, but checks whether the passed identifier is not defined by #define before that directive.

This is the exact opposite of #ifdef; it will always match in situations where #ifdef would never match, and vice versa.

Defines the optional block which is included when the previously defined #if, #elif, #ifdef or #ifndef directive evaluates to false.

Used as terminator for the #if, #ifdef, #ifndef or subsequent #else directives.

Syntax: #error <message>

The #error directive forces the preprocessor to emit an error with optional message. For example, it's useful when used within #if block to provide a strict limitation of the defined value.

Syntax: #include "path"

The #include directive includes the entire content of a shader include file in a shader. "path" can be an absolute res:// path or relative to the current shader file. Relative paths are only allowed in shaders that are saved to .gdshader or .gdshaderinc files, while absolute paths can be used in shaders that are built into a scene/resource file.

You can create new shader includes by using the File > Create Shader Include menu option of the shader editor, or by creating a new ShaderInclude resource in the FileSystem dock.

Shader includes can be included from within any shader, or other shader include, at any point in the file.

When including shader includes in the global scope of a shader, it is recommended to do this after the initial shader_type statement.

You can also include shader includes from within the body a function. Please note that the shader editor is likely going to report errors for your shader include's code, as it may not be valid outside of the context that it was written for. You can either choose to ignore these errors (the shader will still compile fine), or you can wrap the include in an #ifdef block that checks for a define from your shader.

#include is useful for creating libraries of helper functions (or macros) and reducing code duplication. When using #include, be careful about naming collisions, as redefining functions or macros is not allowed.

#include is subject to several restrictions:

Only shader include resources (ending with .gdshaderinc) can be included. .gdshader files cannot be included by another shader, but a .gdshaderinc file can include other .gdshaderinc files.

Cyclic dependencies are not allowed and will result in an error.

To avoid infinite recursion, include depth is limited to 25 steps.

Example shader include file:

Example base shader (using the include file we created above):

Syntax: #pragma value

The #pragma directive provides additional information to the preprocessor or compiler.

Currently, it may have only one value: disable_preprocessor. If you don't need the preprocessor, use that directive to speed up shader compilation by excluding the preprocessor step.

Since Godot 4.4, you can check which renderer is currently used with the built-in defines CURRENT_RENDERER, RENDERER_COMPATIBILITY, RENDERER_MOBILE, and RENDERER_FORWARD_PLUS:

CURRENT_RENDERER is set to either 0, 1, or 2 depending on the current renderer.

RENDERER_COMPATIBILITY is always 0.

RENDERER_MOBILE is always 1.

RENDERER_FORWARD_PLUS is always 2.

As an example, this shader sets ALBEDO to a different color in each renderer:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (cpp):
```cpp
uniform sampler2D material0;

#define SAMPLE(N) vec4 tex##N = texture(material##N, UV)

void fragment() {
    SAMPLE(0);
    ALBEDO = tex0.rgb;
}
```

Example 2 (julia):
```julia
shader_type spatial;

// Notice the lack of semicolon at the end of the line, as the replacement text
// shouldn't insert a semicolon on its own.
// If the directive ends with a semicolon, the semicolon is inserted in every usage
// of the directive, even when this causes a syntax error.
#define USE_MY_COLOR
#define MY_COLOR vec3(1, 0, 0)

// Replacement with arguments.
// All arguments are required (no default values can be provided).
#define BRIGHTEN_COLOR(r, g, b) vec3(r + 0.5, g + 0.5, b + 0.5)

// Multiline replacement using backslashes for continuation:
#define SAMPLE(param1, param2, param3, param4) long_function_call( \
        param1, \
        param2, \
        param3, \
        param4 \
)

void fragment() {
#ifdef USE_MY_COLOR
    ALBEDO = MY_COLOR;
#endif
}
```

Example 3 (unknown):
```unknown
#define MY_COLOR vec3(1, 0, 0)

vec3 get_red_color() {
    return MY_COLOR;
}

#undef MY_COLOR
#define MY_COLOR vec3(0, 1, 0)

vec3 get_green_color() {
    return MY_COLOR;
}

// Like in most preprocessors, undefining a define that was not previously defined is allowed
// (and won't print any warning or error).
#undef THIS_DOES_NOT_EXIST
```

Example 4 (unknown):
```unknown
#define VAR 3
#define USE_LIGHT 0 // Evaluates to `false`.
#define USE_COLOR 1 // Evaluates to `true`.

#if VAR == 3 && (USE_LIGHT || USE_COLOR)
// Condition is `true`. Include this portion in the final shader.
#endif
```

---

## Sky shaders — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/sky_shader.html

**Contents:**
- Sky shaders
- Render modes
- Built-ins
- Global built-ins
- Sky built-ins
- User-contributed notes

Sky shaders are a special type of shader used for drawing sky backgrounds and for updating radiance cubemaps which are used for image-based lighting (IBL). Sky shaders only have one processing function, the sky() function.

There are three places the sky shader is used.

First the sky shader is used to draw the sky when you have selected to use a Sky as the background in your scene.

Second, the sky shader is used to update the radiance cubemap when using the Sky for ambient color or reflections.

Third, the sky shader is used to draw the lower res subpasses which can be used in the high-res background or cubemap pass.

In total, this means the sky shader can run up to six times per frame, however, in practice it will be much less than that because the radiance cubemap does not need to be updated every frame, and not all subpasses will be used. You can change the behavior of the shader based on where it is called by checking the AT_*_PASS booleans. For example:

When using the sky shader to draw a background, the shader will be called for all non-occluded fragments on the screen. However, for the background's subpasses, the shader will be called for every pixel of the subpass.

When using the sky shader to update the radiance cubemap, the sky shader will be called for every pixel in the cubemap. On the other hand, the shader will only be called when the radiance cubemap needs to be updated. The radiance cubemap needs to be updated when any of the shader parameters are updated. For example, if TIME is used in the shader, then the radiance cubemap will update every frame. The following list of changes force an update of the radiance cubemap:

POSITION is used and the camera position changes.

If any LIGHTX_* properties are used and any DirectionalLight3D changes.

If any uniform is changed in the shader.

If the screen is resized and either of the subpasses are used.

Try to avoid updating the radiance cubemap needlessly. If you do need to update the radiance cubemap each frame, make sure your Sky process mode is set to PROCESS_MODE_REALTIME.

Note that the process mode only affects the rendering of the radiance cubemap. The visible sky is always rendered by calling the fragment shader for every pixel. With complex fragment shaders, this can result in a high rendering overhead. If the sky is static (the conditions listed above are met) or changes slowly, running the full fragment shader every frame is not needed. This can be avoided by rendering the full sky into the radiance cubemap, and reading from this cubemap when rendering the visible sky. With a completely static sky, this means that it needs to be rendered only once.

The following code renders the full sky into the radiance cubemap and reads from that cubemap for displaying the visible sky:

This way, the complex calculations happen only in the cubemap pass, which can be optimized by setting the sky's process mode and the radiance size to get the desired balance between performance and visual fidelity.

Subpasses allow you to do more expensive calculations at a lower resolution to speed up your shaders. For example the following code renders clouds at a lower resolution than the rest of the sky:

Allows the shader to write to and access the half resolution pass.

Allows the shader to write to and access the quarter resolution pass.

If used, fog will not affect the sky.

Values marked as in are read-only. Values marked as out can optionally be written to and will not necessarily contain sensible values. Samplers cannot be written to so they are not marked.

Global built-ins are available everywhere, including in custom functions.

There are 4 LIGHTX lights, accessed as LIGHT0, LIGHT1, LIGHT2, and LIGHT3.

Global time since the engine has started, in seconds. It repeats after every 3,600 seconds (which can be changed with the rollover setting). It's affected by time_scale but not by pausing. If you need a TIME variable that is not affected by time scale, add your own global shader uniform and update it each frame.

Camera position, in world space.

Radiance cubemap. Can only be read from during background pass. Check !AT_CUBEMAP_PASS before using.

in bool AT_HALF_RES_PASS

true when rendering to half resolution pass.

in bool AT_QUARTER_RES_PASS

true when rendering to quarter resolution pass.

in bool AT_CUBEMAP_PASS

true when rendering to radiance cubemap.

in bool LIGHTX_ENABLED

true if LIGHTX is visible and in the scene. If false, other light properties may be garbage.

in float LIGHTX_ENERGY

Energy multiplier for LIGHTX.

in vec3 LIGHTX_DIRECTION

Direction that LIGHTX is facing.

Angular diameter of LIGHTX in the sky. Expressed in radians. For reference, the sun from earth is about .0087 radians (0.5 degrees).

A PI constant (3.141592). A ratio of a circle's circumference to its diameter and amount of radians in half turn.

A TAU constant (6.283185). An equivalent of PI * 2 and amount of radians in full turn.

An E constant (2.718281). Euler's number and a base of the natural logarithm.

Normalized direction of current pixel. Use this as your basic direction for procedural effects.

Screen UV coordinate for current pixel. Used to map a texture to the full screen.

Sphere UV. Used to map a panorama texture to the sky.

in vec4 HALF_RES_COLOR

Color value of corresponding pixel from half resolution pass. Uses linear filter.

in vec4 QUARTER_RES_COLOR

Color value of corresponding pixel from quarter resolution pass. Uses linear filter.

Output alpha value, can only be used in subpasses.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (cpp):
```cpp
shader_type sky;

void sky() {
    if (AT_CUBEMAP_PASS) {
        // Sets the radiance cubemap to a nice shade of blue instead of doing
        // expensive sky calculations
        COLOR = vec3(0.2, 0.6, 1.0);
    } else {
        // Do expensive sky calculations for background sky only
        COLOR = get_sky_color(EYEDIR);
    }
}
```

Example 2 (cpp):
```cpp
shader_type sky;

void sky() {
    if (AT_CUBEMAP_PASS) {
        vec3 dir = EYEDIR;

        vec4 col = vec4(0.0);

        // Complex color calculation

        COLOR = col.xyz;
        ALPHA = 1.0;
    } else {
        COLOR = texture(RADIANCE, EYEDIR).rgb;
    }
}
```

Example 3 (cpp):
```cpp
shader_type sky;
render_mode use_half_res_pass;

void sky() {
    if (AT_HALF_RES_PASS) {
        // Run cloud calculation for 1/4 of the pixels
        vec4 color = generate_clouds(EYEDIR);
        COLOR = color.rgb;
        ALPHA = color.a;
    } else {
        // At full resolution pass, blend sky and clouds together
        vec3 color = generate_sky(EYEDIR);
        COLOR = color + HALF_RES_COLOR.rgb * HALF_RES_COLOR.a;
    }
}
```

---

## Fog shaders — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/fog_shader.html

**Contents:**
- Fog shaders
- Built-ins
- Global built-ins
- Fog built-ins
- User-contributed notes

Fog shaders are used to define how fog is added (or subtracted) from a scene in a given area. Fog shaders are always used together with FogVolumes and volumetric fog. Fog shaders only have one processing function, the fog() function.

The resolution of the fog shaders depends on the resolution of the volumetric fog froxel grid. Accordingly, the level of detail that a fog shader can add depends on how close the FogVolume is to the camera.

Fog shaders are a special form of compute shader that is called once for every froxel that is touched by an axis aligned bounding box of the associated FogVolume. This means that froxels that just barely touch a given FogVolume will still be used.

Values marked as in are read-only. Values marked as out can optionally be written to and will not necessarily contain sensible values. Samplers cannot be written to so they are not marked.

Global built-ins are available everywhere, including in custom functions.

Global time since the engine has started, in seconds. It repeats after every 3,600 seconds (which can be changed with the rollover setting). It's affected by time_scale but not by pausing. If you need a TIME variable that is not affected by time scale, add your own global shader uniform and update it each frame.

A PI constant (3.141592). A ratio of a circle's circumference to its diameter and amount of radians in half turn.

A TAU constant (6.283185). An equivalent of PI * 2 and amount of radians in full turn.

An E constant (2.718281). Euler's number and a base of the natural logarithm.

All of the output values of fog volumes overlap one another. This allows FogVolumes to be rendered efficiently as they can all be drawn at once.

in vec3 WORLD_POSITION

Position of current froxel cell in world space.

in vec3 OBJECT_POSITION

Position of the center of the current FogVolume in world space.

3-dimensional UV, used to map a 3D texture to the current FogVolume.

Size of the current FogVolume when its shape has a size.

Signed distance field to the surface of the FogVolume. Negative if inside volume, positive otherwise.

Output base color value, interacts with light to produce final color. Only written to fog volume if used.

Output density value. Can be negative to allow subtracting one volume from another. Density must be used for fog shader to write anything at all.

Output emission color value, added to color during light pass to produce final color. Only written to fog volume if used.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Converting GLSL to Godot shaders — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html

**Contents:**
- Converting GLSL to Godot shaders
- GLSL
  - Shader programs
  - Vertex attributes
  - gl_Position
  - Varyings
  - Main
  - Macros
  - Variables
  - Coordinates

This document explains the differences between Godot's shading language and GLSL and gives practical advice on how to migrate shaders from other sources, such as Shadertoy and The Book of Shaders, into Godot shaders.

For detailed information on Godot's shading language, please refer to the Shading Language reference.

Godot uses a shading language based on GLSL with the addition of a few quality-of-life features. Accordingly, most features available in GLSL are available in Godot's shading language.

In GLSL, each shader uses a separate program. You have one program for the vertex shader and one for the fragment shader. In Godot, you have a single shader that contains a vertex and/or a fragment function. If you only choose to write one, Godot will supply the other.

Godot allows uniform variables and functions to be shared by defining the fragment and vertex shaders in one file. In GLSL, the vertex and fragment programs cannot share variables except when varyings are used.

In GLSL, you can pass in per-vertex information using attributes and have the flexibility to pass in as much or as little as you want. In Godot, you have a set number of input attributes, including VERTEX (position), COLOR, UV, UV2, NORMAL. Each shaders' page in the shader reference section of the documentation comes with a complete list of its vertex attributes.

gl_Position receives the final position of a vertex specified in the vertex shader. It is specified by the user in clip space. Typically, in GLSL, the model space vertex position is passed in using a vertex attribute called position and you handle the conversion from model space to clip space manually.

In Godot, VERTEX specifies the vertex position in model space at the beginning of the vertex function. Godot also handles the final conversion to clip space after the user-defined vertex function is run. If you want to skip the conversion from model to view space, you can set the render_mode to skip_vertex_transform. If you want to skip all transforms, set render_mode to skip_vertex_transform and set the PROJECTION_MATRIX to mat4(1.0) in order to nullify the final transform from view space to clip space.

Varyings are a type of variable that can be passed from the vertex shader to the fragment shader. In modern GLSL (3.0 and up), varyings are defined with the in and out keywords. A variable going out of the vertex shader is defined with out in the vertex shader and in inside the fragment shader.

In GLSL, each shader program looks like a self-contained C-style program. Accordingly, the main entry point is main. If you are copying a vertex shader, rename main to vertex and if you are copying a fragment shader, rename main to fragment.

The Godot shader preprocessor supports the following macros:

#if, #elif, #else, #endif, defined(), #ifdef, #ifndef

#include (only .gdshaderinc files and with a maximum depth of 25)

#pragma disable_preprocessor, which disables preprocessing for the rest of the file

GLSL has many built-in variables that are hard-coded. These variables are not uniforms, so they are not editable from the main program.

Output color for each pixel.

For full screen quads. For smaller quads, use UV.

Position of Vertex, output from Vertex Shader.

Size of Point primitive.

Position on point when drawing Point primitives.

True if front face of primitive.

gl_FragCoord in GLSL and FRAGCOORD in the Godot shading language use the same coordinate system. If using UV in Godot, the y-coordinate will be flipped upside down.

In GLSL, you can define the precision of a given type (float or int) at the top of the shader with the precision keyword. In Godot, you can set the precision of individual variables as you need by placing precision qualifiers lowp, mediump, and highp before the type when defining the variable. For more information, see the Shading Language reference.

Shadertoy is a website that makes it easy to write fragment shaders and create pure magic.

Shadertoy does not give the user full control over the shader. It handles all the input and uniforms and only lets the user write the fragment shader.

Shadertoy uses the webgl spec, so it runs a slightly different version of GLSL. However, it still has the regular types, including constants and macros.

The main point of entry to a Shadertoy shader is the mainImage function. mainImage has two parameters, fragColor and fragCoord, which correspond to COLOR and FRAGCOORD in Godot, respectively. These parameters are handled automatically in Godot, so you do not need to include them as parameters yourself. Anything in the mainImage function should be copied into the fragment function when porting to Godot.

In order to make writing fragment shaders straightforward and easy, Shadertoy handles passing a lot of helpful information from the main program into the fragment shader for you. A few of these have no equivalents in Godot because Godot has chosen not to make them available by default. This is okay because Godot gives you the ability to make your own uniforms. For variables whose equivalents are listed as "Provide with Uniform", users are responsible for creating that uniform themselves. The description gives the reader a hint about what they can pass in as a substitute.

Output color for each pixel.

For full screen quads. For smaller quads, use UV.

1.0 / SCREEN_PIXEL_SIZE

Can also pass in manually.

Time since shader started.

Time to render previous frame.

Time since that particular texture started.

Mouse position in pixel coordinates.

Current date, expressed in seconds.

iChannelResolution[4]

1.0 / TEXTURE_PIXEL_SIZE

Resolution of particular texture.

Godot provides only one built-in; user can make more.

fragCoord behaves the same as gl_FragCoord in GLSL and FRAGCOORD in Godot.

Similar to Shadertoy, The Book of Shaders provides access to a fragment shader in the web browser, with which the user may interact. The user is restricted to writing fragment shader code with a set list of uniforms passed in and with no ability to add additional uniforms.

For further help on porting shaders to various frameworks generally, The Book of Shaders provides a page on running shaders in various frameworks.

The Book of Shaders uses the webgl spec, so it runs a slightly different version of GLSL. However, it still has the regular types, including constants and macros.

The entry point for a Book of Shaders fragment shader is main, just like in GLSL. Everything written in a Book of Shaders main function should be copied into Godot's fragment function.

The Book of Shaders sticks closer to plain GLSL than Shadertoy does. It also implements fewer uniforms than Shadertoy.

Output color for each pixel.

For full screen quads. For smaller quads, use UV.

1.0 / SCREEN_PIXEL_SIZE

Can also pass in manually.

Time since shader started.

Mouse position in pixel coordinates.

The Book of Shaders uses the same coordinate system as GLSL.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using VisualShaders — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html

**Contents:**
- Using VisualShaders
- Creating a VisualShader
- Using the Visual Shader Editor
- Visual Shader node interface
- Visual Shader nodes
  - Expression node
  - Reroute node
  - Fresnel node
  - Boolean node
  - If node

VisualShaders are the visual alternative for creating shaders.

As shaders are inherently linked to visuals, the graph-based approach with previews of textures, materials, etc. offers a lot of additional convenience compared to purely script-based shaders. On the other hand, VisualShaders do not expose all features of the shader script and using both in parallel might be necessary for specific effects.

If you are not familiar with shaders, start by reading Introduction to shaders.

VisualShaders can be created in any ShaderMaterial. To begin using VisualShaders, create a new ShaderMaterial in an object of your choice.

Then assign a Shader resource to the Shader property.

Click on the new Shader resource and the Create Shader dialog will open automatically. Change the Type option to VisualShader in the dropdown, then give it a name.

Click on the visual shader you just created to open the Shader Editor. The layout of the Shader Editor comprises four parts, a file list on the left, the upper toolbar, the graph itself, and a material preview on the right that can be toggled off

From left to right in the toolbar:

The arrow can be used to toggle the files panel's visibility.

The File button opens a dropdown menu for saving, loading, and creating files.

The Add Node button displays a popup menu to let you add nodes to the shader graph.

The drop-down menu is the shader type: Vertex, Fragment and Light. Like for script shaders, it defines what built-in nodes will be available.

The following buttons and number input control the zooming level, grid snapping and distance between grid lines (in pixels).

The toggle controls if the graph minimap in the bottom right of the editor is visible or not.

The automatically arrange selected nodes button will try to organize any nodes you have selected as efficiently and cleanly as possible.

The Manage Varyings button opens a dropdown that lets you add or remove a varying.

The show generated code button shows shader code corresponding to your graph.

The toggle turns the material preview on or off.

The Online Docs button opens this documentation page in your web browser.

The last button allows you to put the shader editor in its own window, separate from the rest of the editor.

Although VisualShaders do not require coding, they share the same logic with script shaders. It is advised to learn the basics of both to have a good understanding of the shading pipeline.

The visual shader graph is converted to a script shader behind the scene, and you can see this code by pressing the last button in the toolbar. This can be convenient to understand what a given node does and how to reproduce it in scripts.

By default, every new VisualShader will have an output node. Every node connection ends at one of the output node's sockets. A node is the basic unit to create your shader. To add a new node, click on the Add Node button on the upper left corner or right click on any empty location in the graph, and a menu will pop up.

This popup has the following properties:

If you right-click on the graph, this menu will be called at the cursor position and the created node, in that case, will also be placed under that position; otherwise, it will be created at the graph's center.

It can be resized horizontally and vertically allowing more content to be shown. Size transform and tree content position are saved between the calls, so if you suddenly closed the popup you can easily restore its previous state.

The Expand All and Collapse All options in the drop-down option menu can be used to easily list the available nodes.

You can also drag and drop nodes from the popup onto the graph.

While the popup has nodes sorted in categories, it can seem overwhelming at first. Try to add some of the nodes, plug them in the output socket and observe what happens.

When connecting any scalar output to a vector input, all components of the vector will take the value of the scalar.

When connecting any vector output to a scalar input, the value of the scalar will be the average of the vector's components.

Visual shader nodes have input and output ports. The input ports are located on the left side of the node, and output ports are located on the right side of the node.

These ports are colored to differentiate type of port:

Scalar is a single value.

Vector is a set of values.

On or off, true or false.

A matrix, usually used to transform vertices.

A texture sampler. It can be used to sample textures.

All of the types are used in the calculations of vertices, fragments, and lights in the shader. For example: matrix multiplication, vector addition, or scalar division.

There are other types but these are the main ones.

Below are some special nodes that are worth knowing about. The list is not exhaustive and might be expanded with more nodes and examples.

The Expression node allows you to write Godot Shading Language (GLSL-like) expressions inside your visual shaders. The node has buttons to add any amount of required input and output ports and can be resized. You can also set up the name and type of each port. The expression you have entered will apply immediately to the material (once the focus leaves the expression text box). Any parsing or compilation errors will be printed to the Output tab. The outputs are initialized to their zero value by default. The node is located under the Special tab and can be used in all shader modes.

The possibilities of this node are almost limitless – you can write complex procedures, and use all the power of text-based shaders, such as loops, the discard keyword, extended types, etc. For example:

The Reroute node is used purely for organizational purposes. In a complicated shader with many nodes you may find that the paths between nodes can make things hard to read. Reroute, as its name suggests, allows you to adjust the path between nodes to make things easier to read. You can even have multiple reroute nodes for a single path, which can be used to make right angles.

To move a reroute node move your mouse cursor above it, and grab the handle that appears.

The Fresnel node is designed to accept normal and view vectors and produces a scalar which is the saturated dot product between them. Additionally, you can setup the inversion and the power of equation. The Fresnel node is great for adding a rim-like lighting effect to objects.

The Boolean node can be converted to Scalar or Vector to represent 0 or 1 and (0, 0, 0) or (1, 1, 1) respectively. This property can be used to enable or disable some effect parts with one click.

The If node allows you to setup a vector which will be returned the result of the comparison between a and b. There are three vectors which can be returned: a == b (in that case the tolerance parameter is provided as a comparison threshold – by default it is equal to the minimal value, i.e. 0.00001), a > b and a < b.

The Switch node returns a vector if the boolean condition is true or false. Boolean was introduced above. If you want to convert a vector to a true boolean, all components of the vector should be non-zero.

The Mesh Emitter node is used for emitting particles from mesh vertices. This is only available for shaders that are in Particles mode.

Keep in mind that not all 3D objects are mesh files. a glTF file can't be dragged and dropped into the graph. However, you can create an inherited scene from it, save the mesh in that scene as its own file, and use that.

You can also drag and drop obj files into the graph editor to add the node for that specific mesh, other mesh files will not work for this.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Screen-reading shaders — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html

**Contents:**
- Screen-reading shaders
- Introduction
- Screen texture
- Screen texture example
- Behind the scenes
- Back-buffer logic
- Depth texture
- Normal-roughness texture
- Redefining screen textures
- User-contributed notes

It is often desired to make a shader that reads from the same screen to which it's writing. 3D APIs, such as OpenGL or DirectX, make this very difficult because of internal hardware limitations. GPUs are extremely parallel, so reading and writing causes all sorts of cache and coherency problems. As a result, not even the most modern hardware supports this properly.

The workaround is to make a copy of the screen, or a part of the screen, to a back-buffer and then read from it while drawing. Godot provides a few tools that make this process easy.

Godot Shading language has a special texture to access the already rendered contents of the screen. It is used by specifying a hint when declaring a sampler2D uniform: hint_screen_texture. A special built-in varying SCREEN_UV can be used to obtain the UV relative to the screen for the current fragment. As a result, this canvas_item fragment shader results in an invisible object, because it only shows what lies behind:

textureLod is used here as we only want to read from the bottom mipmap. If you want to read from a blurred version of the texture instead, you can increase the third argument to textureLod and change the hint filter_nearest to filter_nearest_mipmap (or any other filter with mipmaps enabled). If using a filter with mipmaps, Godot will automatically calculate the blurred texture for you.

If the filter mode is not changed to a filter mode that contains mipmap in its name, textureLod with an LOD parameter greater than 0.0 will have the same appearance as with the 0.0 LOD parameter.

The screen texture can be used for many things. There is a special demo for Screen Space Shaders, that you can download to see and learn. One example is a simple shader to adjust brightness, contrast and saturation:

While this seems magical, it's not. In 2D, when hint_screen_texture is first found in a node that is about to be drawn, Godot does a full-screen copy to a back-buffer. Subsequent nodes that use it in shaders will not have the screen copied for them, because this ends up being inefficient. In 3D, the screen is copied after the opaque geometry pass, but before the transparent geometry pass, so transparent objects will not be captured in the screen texture.

As a result, in 2D, if shaders that use hint_screen_texture overlap, the second one will not use the result of the first one, resulting in unexpected visuals:

In the above image, the second sphere (top right) is using the same source for the screen texture as the first one below, so the first one "disappears", or is not visible.

In 2D, this can be corrected via the BackBufferCopy node, which can be instantiated between both spheres. BackBufferCopy can work by either specifying a screen region or the whole screen:

With correct back-buffer copying, the two spheres blend correctly:

In 3D, materials that use hint_screen_texture are considered transparent themselves and will not appear in the resulting screen texture of other materials. If you plan to instance a scene that uses a material with hint_screen_texture, you will need to use a BackBufferCopy node.

In 3D, there is less flexibility to solve this particular issue because the screen texture is only captured once. Be careful when using the screen texture in 3D as it won't capture transparent objects and may capture some opaque objects that are in front of the object using the screen texture.

You can reproduce the back-buffer logic in 3D by creating a Viewport with a camera in the same position as your object, and then use the Viewport's texture instead of the screen texture.

So, to make it clearer, here's how the backbuffer copying logic works in 2D in Godot:

If a node uses hint_screen_texture, the entire screen is copied to the back buffer before drawing that node. This only happens the first time; subsequent nodes do not trigger this.

If a BackBufferCopy node was processed before the situation in the point above (even if hint_screen_texture was not used), the behavior described in the point above does not happen. In other words, automatic copying of the entire screen only happens if hint_screen_texture is used in a node for the first time and no BackBufferCopy node (not disabled) was found before in tree-order.

BackBufferCopy can copy either the entire screen or a region. If set to only a region (not the whole screen) and your shader uses pixels not in the region copied, the result of that read is undefined (most likely garbage from previous frames). In other words, it's possible to use BackBufferCopy to copy back a region of the screen and then read the screen texture from a different region. Avoid this behavior!

For 3D shaders, it's also possible to access the screen depth buffer. For this, the hint_depth_texture hint is used. This texture is not linear; it must be converted using the inverse projection matrix.

The following code retrieves the 3D position below the pixel being drawn:

Normal-roughness texture is only supported in the Forward+ rendering method, not Mobile or Compatibility.

Similarly, the normal-roughness texture can be used to read the normals and roughness of objects rendered in the depth prepass. The normal is stored in the .xyz channels (mapped to the 0-1 range) while the roughness is stored in the .w channel.

The screen texture hints (hint_screen_texture, hint_depth_texture, and hint_normal_roughness_texture) can be used with multiple uniforms. For example, you may want to read from the texture multiple times with a different repeat flag or filter flag.

The following example shows a shader that reads the screen space normal with linear filtering, but reads the screen space roughness using nearest neighbor filtering.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (cpp):
```cpp
shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;

void fragment() {
    COLOR = textureLod(screen_texture, SCREEN_UV, 0.0);
}
```

Example 2 (cpp):
```cpp
shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;

uniform float brightness = 1.0;
uniform float contrast = 1.0;
uniform float saturation = 1.0;

void fragment() {
    vec3 c = textureLod(screen_texture, SCREEN_UV, 0.0).rgb;

    c.rgb = mix(vec3(0.0), c.rgb, brightness);
    c.rgb = mix(vec3(0.5), c.rgb, contrast);
    c.rgb = mix(vec3(dot(vec3(1.0), c.rgb) * 0.33333), c.rgb, saturation);

    COLOR.rgb = c;
}
```

Example 3 (cpp):
```cpp
uniform sampler2D depth_texture : hint_depth_texture, repeat_disable, filter_nearest;

void fragment() {
    float depth = textureLod(depth_texture, SCREEN_UV, 0.0).r;
    vec4 upos = INV_PROJECTION_MATRIX * vec4(SCREEN_UV * 2.0 - 1.0, depth, 1.0);
    vec3 pixel_position = upos.xyz / upos.w;
}
```

Example 4 (cpp):
```cpp
uniform sampler2D normal_roughness_texture : hint_normal_roughness_texture, repeat_disable, filter_nearest;

void fragment() {
    float screen_roughness = texture(normal_roughness_texture, SCREEN_UV).w;
    vec3 screen_normal = texture(normal_roughness_texture, SCREEN_UV).xyz;
    screen_normal = screen_normal * 2.0 - 1.0;
```

---

## Custom post-processing — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/custom_postprocessing.html

**Contents:**
- Custom post-processing
- Introduction
- Single pass post-processing
- Multi-pass post-processing
- User-contributed notes

Godot provides many post-processing effects out of the box, including Bloom, DOF, and SSAO, which are described in Environment and post-processing. However, advanced use cases may require custom effects. This article explains how to write your own custom effects.

The easiest way to implement a custom post-processing shader is to use Godot's built-in ability to read from the screen texture. If you're not familiar with this, you should read the Screen Reading Shaders Tutorial first.

Post-processing effects are shaders applied to a frame after Godot has rendered it. To apply a shader to a frame, create a CanvasLayer, and give it a ColorRect. Assign a new ShaderMaterial to the newly created ColorRect, and set the ColorRect's anchor preset to Full Rect:

Setting the anchor preset to Full Rect on the ColorRect node

Your scene tree will look something like this:

Another more efficient method is to use a BackBufferCopy to copy a region of the screen to a buffer and to access it in a shader script through a sampler2D using hint_screen_texture.

As of the time of writing, Godot does not support rendering to multiple buffers at the same time. Your post-processing shader will not have access to other render passes and buffers not exposed by Godot (such as depth or normal/roughness). You only have access to the rendered frame and buffers exposed by Godot as samplers.

For this demo, we will use this Sprite of a sheep.

Assign a new Shader to the ColorRect's ShaderMaterial. You can access the frame's texture and UV with a sampler2D using hint_screen_texture and the built-in SCREEN_UV uniforms.

Copy the following code to your shader. The code below is a hex pixelization shader by arlez80,

The sheep will look something like this:

Some post-processing effects like blurs are resource intensive. You can make them run a lot faster if you break them down in multiple passes. In a multipass material, each pass takes the result from the previous pass as an input and processes it.

To produce a multi-pass post-processing shader, you stack CanvasLayer and ColorRect nodes. In the example above, you use a CanvasLayer object to render a shader using the frame on the layer below. Apart from the node structure, the steps are the same as with the single-pass post-processing shader.

Your scene tree will look something like this:

As an example, you could write a full screen Gaussian blur effect by attaching the following pieces of code to each of the ColorRect nodes. The order in which you apply the shaders depends on the position of the CanvasLayer in the scene tree, higher means sooner. For this blur shader, the order does not matter.

Using the above code, you should end up with a full screen blur effect like below.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (sql):
```sql
shader_type canvas_item;

uniform vec2 size = vec2(32.0, 28.0);
// If you intend to read from mipmaps with `textureLod()` LOD values greater than `0.0`,
// use `filter_nearest_mipmap` instead. This shader doesn't require it.
uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;

void fragment() {
        vec2 norm_size = size * SCREEN_PIXEL_SIZE;
        bool less_than_half = mod(SCREEN_UV.y / 2.0, norm_size.y) / norm_size.y < 0.5;
        vec2 uv = SCREEN_UV + vec2(norm_size.x * 0.5 * float(less_than_half), 0.0);
        vec2 center_uv = floor(uv / norm_size) * norm_size;
        vec2 norm_uv = mod(uv, norm_size) / norm_size;
        center_uv += mix(vec2(0.0, 0.0),
                         mix(mix(vec2(norm_size.x, -norm_size.y),
                                 vec2(0.0, -norm_size.y),
                                 float(norm_uv.x < 0.5)),
                             mix(vec2(0.0, -norm_size.y),
                                 vec2(-norm_size.x, -norm_size.y),
                                 float(norm_uv.x < 0.5)),
                             float(less_than_half)),
                         float(norm_uv.y < 0.3333333) * float(norm_uv.y / 0.3333333 < (abs(norm_uv.x - 0.5) * 2.0)));

        COLOR = textureLod(screen_texture, center_uv, 0.0);
}
```

Example 2 (cpp):
```cpp
shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;

// Blurs the screen in the X-direction.
void fragment() {
    vec3 col = texture(screen_texture, SCREEN_UV).xyz * 0.16;
    col += texture(screen_texture, SCREEN_UV + vec2(SCREEN_PIXEL_SIZE.x, 0.0)).xyz * 0.15;
    col += texture(screen_texture, SCREEN_UV + vec2(-SCREEN_PIXEL_SIZE.x, 0.0)).xyz * 0.15;
    col += texture(screen_texture, SCREEN_UV + vec2(2.0 * SCREEN_PIXEL_SIZE.x, 0.0)).xyz * 0.12;
    col += texture(screen_texture, SCREEN_UV + vec2(2.0 * -SCREEN_PIXEL_SIZE.x, 0.0)).xyz * 0.12;
    col += texture(screen_texture, SCREEN_UV + vec2(3.0 * SCREEN_PIXEL_SIZE.x, 0.0)).xyz * 0.09;
    col += texture(screen_texture, SCREEN_UV + vec2(3.0 * -SCREEN_PIXEL_SIZE.x, 0.0)).xyz * 0.09;
    col += texture(screen_texture, SCREEN_UV + vec2(4.0 * SCREEN_PIXEL_SIZE.x, 0.0)).xyz * 0.05;
    col += texture(screen_texture, SCREEN_UV + vec2(4.0 * -SCREEN_PIXEL_SIZE.x, 0.0)).xyz * 0.05;
    COLOR.xyz = col;
}
```

Example 3 (cpp):
```cpp
shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;

// Blurs the screen in the Y-direction.
void fragment() {
    vec3 col = texture(screen_texture, SCREEN_UV).xyz * 0.16;
    col += texture(screen_texture, SCREEN_UV + vec2(0.0, SCREEN_PIXEL_SIZE.y)).xyz * 0.15;
    col += texture(screen_texture, SCREEN_UV + vec2(0.0, -SCREEN_PIXEL_SIZE.y)).xyz * 0.15;
    col += texture(screen_texture, SCREEN_UV + vec2(0.0, 2.0 * SCREEN_PIXEL_SIZE.y)).xyz * 0.12;
    col += texture(screen_texture, SCREEN_UV + vec2(0.0, 2.0 * -SCREEN_PIXEL_SIZE.y)).xyz * 0.12;
    col += texture(screen_texture, SCREEN_UV + vec2(0.0, 3.0 * SCREEN_PIXEL_SIZE.y)).xyz * 0.09;
    col += texture(screen_texture, SCREEN_UV + vec2(0.0, 3.0 * -SCREEN_PIXEL_SIZE.y)).xyz * 0.09;
    col += texture(screen_texture, SCREEN_UV + vec2(0.0, 4.0 * SCREEN_PIXEL_SIZE.y)).xyz * 0.05;
    col += texture(screen_texture, SCREEN_UV + vec2(0.0, 4.0 * -SCREEN_PIXEL_SIZE.y)).xyz * 0.05;
    COLOR.xyz = col;
}
```

---

## Advanced post-processing — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/advanced_postprocessing.html

**Contents:**
- Advanced post-processing
- Introduction
- Full screen quad
- Depth texture
- Example shader
- An optimization
- User-contributed notes

This tutorial describes an advanced method for post-processing in Godot. In particular, it will explain how to write a post-processing shader that uses the depth buffer. You should already be familiar with post-processing generally and, in particular, with the methods outlined in the custom post-processing tutorial.

One way to make custom post-processing effects is by using a viewport. However, there are two main drawbacks of using a Viewport:

The depth buffer cannot be accessed

The effect of the post-processing shader is not visible in the editor

To get around the limitation on using the depth buffer, use a MeshInstance3D with a QuadMesh primitive. This allows us to use a shader and to access the depth texture of the scene. Next, use a vertex shader to make the quad cover the screen at all times so that the post-processing effect will be applied at all times, including in the editor.

First, create a new MeshInstance3D and set its mesh to a QuadMesh. This creates a quad centered at position (0, 0, 0) with a width and height of 1. Set the width and height to 2 and enable Flip Faces. Right now, the quad occupies a position in world space at the origin. However, we want it to move with the camera so that it always covers the entire screen. To do this, we will bypass the coordinate transforms that translate the vertex positions through the difference coordinate spaces and treat the vertices as if they were already in clip space.

The vertex shader expects coordinates to be output in clip space, which are coordinates ranging from -1 at the left and bottom of the screen to 1 at the top and right of the screen. This is why the QuadMesh needs to have height and width of 2. Godot handles the transform from model to view space to clip space behind the scenes, so we need to nullify the effects of Godot's transformations. We do this by setting the POSITION built-in to our desired position. POSITION bypasses the built-in transformations and sets the vertex position in clip space directly.

In versions of Godot earlier than 4.3, this code recommended using POSITION = vec4(VERTEX, 1.0); which implicitly assumed the clip-space near plane was at 0.0. That code is now incorrect and will not work in versions 4.3+ as we use a "reversed-z" depth buffer now where the near plane is at 1.0.

Even with this vertex shader, the quad keeps disappearing. This is due to frustum culling, which is done on the CPU. Frustum culling uses the camera matrix and the AABBs of Meshes to determine if the Mesh will be visible before passing it to the GPU. The CPU has no knowledge of what we are doing with the vertices, so it assumes the coordinates specified refer to world positions, not clip space positions, which results in Godot culling the quad when we turn away from the center of the scene. In order to keep the quad from being culled, there are a few options:

Add the QuadMesh as a child to the camera, so the camera is always pointed at it

Set the Geometry property extra_cull_margin as large as possible in the QuadMesh

The second option ensures that the quad is visible in the editor, while the first option guarantees that it will still be visible even if the camera moves outside the cull margin. You can also use both options.

To read from the depth texture, we first need to create a texture uniform set to the depth buffer by using hint_depth_texture.

Once defined, the depth texture can be read with the texture() function.

Similar to accessing the screen texture, accessing the depth texture is only possible when reading from the current viewport. The depth texture cannot be accessed from another viewport to which you have rendered.

The values returned by depth_texture are between 1.0 and 0.0 (corresponding to the near and far plane, respectively, because of using a "reverse-z" depth buffer) and are nonlinear. When displaying depth directly from the depth_texture, everything will look almost black unless it is very close due to that nonlinearity. In order to make the depth value align with world or model coordinates, we need to linearize the value. When we apply the projection matrix to the vertex position, the z value is made nonlinear, so to linearize it, we multiply it by the inverse of the projection matrix, which in Godot, is accessible with the variable INV_PROJECTION_MATRIX.

Firstly, take the screen space coordinates and transform them into normalized device coordinates (NDC). NDC run -1.0 to 1.0 in x and y directions and from 0.0 to 1.0 in the z direction when using the Vulkan backend. Reconstruct the NDC using SCREEN_UV for the x and y axis, and the depth value for z.

This tutorial assumes the use of the Forward+ or Mobile renderers, which both use Vulkan NDCs with a Z-range of [0.0, 1.0]. In contrast, the Compatibility renderer uses OpenGL NDCs with a Z-range of [-1.0, 1.0]. For the Compatibility renderer, replace the NDC calculation with this instead:

You can also use the CURRENT_RENDERER and RENDERER_COMPATIBILITY built-in defines for a shader that will work in all renderers:

Convert NDC to view space by multiplying the NDC by INV_PROJECTION_MATRIX. Recall that view space gives positions relative to the camera, so the z value will give us the distance to the point.

Because the camera is facing the negative z direction, the position will have a negative z value. In order to get a usable depth value, we have to negate view.z.

The world position can be constructed from the depth buffer using the following code, using the INV_VIEW_MATRIX to transform the position from view space into world space.

Once we add a line to output to ALBEDO, we have a complete shader that looks something like this. This shader lets you visualize the linear depth or world space coordinates, depending on which line is commented out.

You can benefit from using a single large triangle rather than using a full screen quad. The reason for this is explained here. However, the benefit is quite small and only beneficial when running especially complex fragment shaders.

Set the Mesh in the MeshInstance3D to an ArrayMesh. An ArrayMesh is a tool that allows you to easily construct a Mesh from Arrays for vertices, normals, colors, etc.

Now, attach a script to the MeshInstance3D and use the following code:

The triangle is specified in normalized device coordinates. Recall, NDC run from -1.0 to 1.0 in both the x and y directions. This makes the screen 2 units wide and 2 units tall. In order to cover the entire screen with a single triangle, use a triangle that is 4 units wide and 4 units tall, double its height and width.

Assign the same vertex shader from above and everything should look exactly the same.

The one drawback to using an ArrayMesh over using a QuadMesh is that the ArrayMesh is not visible in the editor because the triangle is not constructed until the scene is run. To get around that, construct a single triangle Mesh in a modeling program and use that in the MeshInstance3D instead.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (sql):
```sql
shader_type spatial;
// Prevent the quad from being affected by lighting and fog. This also improves performance.
render_mode unshaded, fog_disabled;

void vertex() {
  POSITION = vec4(VERTEX.xy, 1.0, 1.0);
}
```

Example 2 (unknown):
```unknown
uniform sampler2D depth_texture : hint_depth_texture;
```

Example 3 (unknown):
```unknown
float depth = texture(depth_texture, SCREEN_UV).x;
```

Example 4 (cpp):
```cpp
void fragment() {
  float depth = texture(depth_texture, SCREEN_UV).x;
  vec3 ndc = vec3(SCREEN_UV * 2.0 - 1.0, depth);
}
```

---

## Making trees — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/making_trees.html

**Contents:**
- Making trees
- Start with a tree
- Paint with vertex colors
- Write a custom shader for the leaves
- Improving the shader
- User-contributed notes

This is a short tutorial on how to make trees and other types of vegetation from scratch.

The aim is to not focus on the modeling techniques (there are plenty of tutorials about that), but how to make them look good in Godot.

I took this tree from SketchFab:

https://sketchfab.com/models/ea5e6ed7f9d6445ba69589d503e8cebf

and opened it in Blender.

The first thing you may want to do is to use the vertex colors to paint how much the tree will sway when there is wind. Just use the vertex color painting tool of your favorite 3D modeling program and paint something like this:

This is a bit exaggerated, but the idea is that color indicates how much sway affects every part of the tree. This scale here represents it better:

This is an example of a shader for leaves:

This is a spatial shader. There is no front/back culling (so leaves can be seen from both sides), and alpha prepass is used, so there are less depth artifacts that result from using transparency (and leaves cast shadow). Finally, for the sway effect, world coordinates are recommended, so the tree can be duplicated, moved, etc. and it will still work together with other trees.

Here, the texture is read, as well as a transmission color, which is used to add some back-lighting to the leaves, simulating subsurface scattering.

This is the code to create the sway of the leaves. It's basic (just uses a sinewave multiplying by the time and axis position, but works well). Notice that the strength is multiplied by the color. Every axis uses a different small near 1.0 multiplication factor so axes don't appear in sync.

Finally, all that's left is the fragment shader:

And this is pretty much it.

The trunk shader is similar, except it does not write to the alpha channel (thus no alpha prepass is needed) and does not require transmission to work. Both shaders can be improved by adding normal mapping, AO and other maps.

There are many more resources on how to do this that you can read. Now that you know the basics, a recommended read is the chapter from GPU Gems3 about how Crysis does this (focus mostly on the sway code, as many other techniques shown there are obsolete):

https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch16.html

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
shader_type spatial;
render_mode depth_prepass_alpha, cull_disabled, world_vertex_coords;
```

Example 2 (unknown):
```unknown
uniform sampler2D texture_albedo : source_color;
uniform vec4 transmission : source_color;
```

Example 3 (cpp):
```cpp
uniform float sway_speed = 1.0;
uniform float sway_strength = 0.05;
uniform float sway_phase_len = 8.0;

void vertex() {
    float strength = COLOR.r * sway_strength;
    VERTEX.x += sin(VERTEX.x * sway_phase_len * 1.123 + TIME * sway_speed) * strength;
    VERTEX.y += sin(VERTEX.y * sway_phase_len + TIME * sway_speed * 1.12412) * strength;
    VERTEX.z += sin(VERTEX.z * sway_phase_len * 0.9123 + TIME * sway_speed * 1.3123) * strength;
}
```

Example 4 (cpp):
```cpp
void fragment() {
    vec4 albedo_tex = texture(texture_albedo, UV);
    ALBEDO = albedo_tex.rgb;
    ALPHA = albedo_tex.a;
    METALLIC = 0.0;
    ROUGHNESS = 1.0;
    SSS_TRANSMITTANCE_COLOR = transmission.rgba;
}
```

---

## Using a SubViewport as a texture — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/using_viewport_as_texture.html

**Contents:**
- Using a SubViewport as a texture
- Introduction
- Setting up the scene
- Setting up the SubViewport
- Applying the texture
- Making the planet texture
- Coloring the planet
- Making an ocean
- User-contributed notes

This tutorial will introduce you to using the SubViewport as a texture that can be applied to 3D objects. In order to do so, it will walk you through the process of making a procedural planet like the one below:

This tutorial does not cover how to code a dynamic atmosphere like the one this planet has.

This tutorial assumes you are familiar with how to set up a basic scene including: a Camera3D, a light source, a MeshInstance3D with a Primitive Mesh, and applying a StandardMaterial3D to the mesh. The focus will be on using the SubViewport to dynamically create textures that can be applied to the mesh.

In this tutorial, we'll cover the following topics:

How to use a SubViewport as a render texture

Mapping a texture to a sphere with equirectangular mapping

Fragment shader techniques for procedural planets

Setting a Roughness map from a Viewport Texture

Create a new scene and add the following nodes exactly as shown below.

Go into the the MeshInstance3D and make the mesh a SphereMesh

Click on the SubViewport node and set its size to (1024, 512). The SubViewport can actually be any size so long as the width is double the height. The width needs to be double the height so that the image will accurately map onto the sphere, as we will be using equirectangular projection, but more on that later.

Next disable 3D. We will be using a ColorRect to render the surface, so we don't need 3D either.

Select the ColorRect and in the inspector set the anchors preset to Full Rect. This will ensure that the ColorRect takes up the entire SubViewport.

Next, we add a Shader Material to the ColorRect (ColorRect > CanvasItem > Material > Material > New ShaderMaterial).

Basic familiarity with shading is recommended for this tutorial. However, even if you are new to shaders, all the code will be provided, so you should have no problem following along.

Click the dropdown menu button for the shader material and click / Edit. From here go to Shader > New Shader. give it a name and click "Create". click the shader in the inspector to open the shader editor. Delete the default code and add the following:

save the shader code, you'll see in the inspector that the above code renders a gradient like the one below.

Now we have the basics of a SubViewport that we render to and we have a unique image that we can apply to the sphere.

Now go into the MeshInstance3D and add a StandardMaterial3D to it. No need for a special Shader Material (although that would be a good idea for more advanced effects, like the atmosphere in the example above).

MeshInstance3D > GeometryInstance > Geometry > Material Override > New StandardMaterial3D

Then click the dropdown for the StandardMaterial3D and click "Edit"

Go to the "Resource" section and check the Local to scene box. Then, go to the "Albedo" section and click beside the "Texture" property to add an Albedo Texture. Here we will apply the texture we made. Choose "New ViewportTexture"

Click on the ViewportTexture you just created in the inspector, then click "Assign". Then, from the menu that pops up, select the Viewport that we rendered to earlier.

Your sphere should now be colored in with the colors we rendered to the Viewport.

Notice the ugly seam that forms where the texture wraps around? This is because we are picking a color based on UV coordinates and UV coordinates do not wrap around the texture. This is a classic problem in 2D map projection. Game developers often have a 2-dimensional map they want to project onto a sphere, but when it wraps around, it has large seams. There is an elegant workaround for this problem that we will illustrate in the next section.

So now, when we render to our SubViewport, it appears magically on the sphere. But there is an ugly seam created by our texture coordinates. So how do we get a range of coordinates that wrap around the sphere in a nice way? One solution is to use a function that repeats on the domain of our texture. sin and cos are two such functions. Let's apply them to the texture and see what happens. Replace the existing color code in the shader with the following:

Not too bad. If you look around, you can see that the seam has now disappeared, but in its place, we have pinching at the poles. This pinching is due to the way Godot maps textures to spheres in its StandardMaterial3D. It uses a projection technique called equirectangular projection, which translates a spherical map onto a 2D plane.

If you are interested in a little extra information on the technique, we will be converting from spherical coordinates into Cartesian coordinates. Spherical coordinates map the longitude and latitude of the sphere, while Cartesian coordinates are, for all intents and purposes, a vector from the center of the sphere to the point.

For each pixel, we will calculate its 3D position on the sphere. From that, we will use 3D noise to determine a color value. By calculating the noise in 3D, we solve the problem of the pinching at the poles. To understand why, picture the noise being calculated across the surface of the sphere instead of across the 2D plane. When you calculate across the surface of the sphere, you never hit an edge, and hence you never create a seam or a pinch point on the pole. The following code converts the UVs into Cartesian coordinates.

And if we use unit as an output COLOR value, we get:

Now that we can calculate the 3D position of the surface of the sphere, we can use 3D noise to make the planet. We will be using this noise function directly from a Shadertoy:

All credit goes to the author, Inigo Quilez. It is published under the MIT licence.

Now to use noise, add the following to the fragment function:

In order to highlight the texture, we set the material to unshaded.

You can see now that the noise indeed wraps seamlessly around the sphere. Although this looks nothing like the planet you were promised. So let's move onto something more colorful.

Now to make the planet colors. While there are many ways to do this, for now, we will stick with a gradient between water and land.

To make a gradient in GLSL, we use the mix function. mix takes two values to interpolate between and a third argument to choose how much to interpolate between them; in essence, it mixes the two values together. In other APIs, this function is often called lerp. However, lerp is typically reserved for mixing two floats together; mix can take any values whether it be floats or vector types.

The first color is blue for the ocean. The second color is a kind of reddish color (because all alien planets need red terrain). And finally, they are mixed together by n * 0.5 + 0.5. n smoothly varies between -1 and 1. So we map it into the 0-1 range that mix expects. Now you can see that the colors change between blue and red.

That is a little more blurry than we want. Planets typically have a relatively clear separation between land and sea. In order to do that, we will change the last term to smoothstep(-0.1, 0.0, n). And thus the whole line becomes:

What smoothstep does is return 0 if the third argument is below the first and 1 if the third argument is larger than the second and smoothly blends between 0 and 1 if the third number is between the first and the second. So in this line, smoothstep returns 0 whenever n is less than -0.1 and it returns 1 whenever n is above 0.

One more thing to make this a little more planet-y. The land shouldn't be so blobby; let's make the edges a little rougher. A trick that is often used in shaders to make rough looking terrain with noise is to layer levels of noise over one another at various frequencies. We use one layer to make the overall blobby structure of the continents. Then another layer breaks up the edges a bit, and then another, and so on. What we will do is calculate n with four lines of shader code instead of just one. n becomes:

And now the planet looks like:

One final thing to make this look more like a planet. The ocean and the land reflect light differently. So we want the ocean to shine a little more than the land. We can do this by passing a fourth value into the alpha channel of our output COLOR and using it as a Roughness map.

This line returns 0.3 for water and 1.0 for land. This means that the land is going to be quite rough, while the water will be quite smooth.

And then, in the material, under the "Metallic" section, make sure Metallic is set to 0 and Specular is set to 1. The reason for this is the water reflects light really well, but isn't metallic. These values are not physically accurate, but they are good enough for this demo.

Next, under the "Roughness" section set the roughness texture to a Viewport Texture pointing to our planet texture SubViewport. Finally, set the Texture Channel to Alpha. This instructs the renderer to use the alpha channel of our output COLOR as the Roughness value.

You'll notice that very little changes except that the planet is no longer reflecting the sky. This is happening because, by default, when something is rendered with an alpha value, it gets drawn as a transparent object over the background. And since the default background of the SubViewport is opaque, the alpha channel of the Viewport Texture is 1, resulting in the planet texture being drawn with slightly fainter colors and a Roughness value of 1 everywhere. To correct this, we go into the SubViewport and enable the "Transparent Bg" property. Since we are now rendering one transparent object on top of another, we want to enable blend_premul_alpha:

This pre-multiplies the colors by the alpha value and then blends them correctly together. Typically, when blending one transparent color on top of another, even if the background has an alpha of 0 (as it does in this case), you end up with weird color bleed issues. Setting blend_premul_alpha fixes that.

Now the planet should look like it is reflecting light on the ocean but not the land. move around the OmniLight3D in the scene so you can see the effect of the reflections on the ocean.

And there you have it. A procedural planet generated using a SubViewport.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (cpp):
```cpp
shader_type canvas_item;

void fragment() {
    COLOR = vec4(UV.x, UV.y, 0.5, 1.0);
}
```

Example 2 (unknown):
```unknown
COLOR.xyz = vec3(sin(UV.x * 3.14159 * 4.0) * cos(UV.y * 3.14159 * 4.0) * 0.5 + 0.5);
```

Example 3 (unknown):
```unknown
float theta = UV.y * 3.14159;
float phi = UV.x * 3.14159 * 2.0;
vec3 unit = vec3(0.0, 0.0, 0.0);

unit.x = sin(phi) * sin(theta);
unit.y = cos(theta) * -1.0;
unit.z = cos(phi) * sin(theta);
unit = normalize(unit);
```

Example 4 (unknown):
```unknown
vec3 hash(vec3 p) {
    p = vec3(dot(p, vec3(127.1, 311.7, 74.7)),
             dot(p, vec3(269.5, 183.3, 246.1)),
             dot(p, vec3(113.5, 271.9, 124.6)));

    return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
}

float noise(vec3 p) {
  vec3 i = floor(p);
  vec3 f = fract(p);
  vec3 u = f * f * (3.0 - 2.0 * f);

  return mix(mix(mix(dot(hash(i + vec3(0.0, 0.0, 0.0)), f - vec3(0.0, 0.0, 0.0)),
                     dot(hash(i + vec3(1.0, 0.0, 0.0)), f - vec3(1.0, 0.0, 0.0)), u.x),
                 mix(dot(hash(i + vec3(0.0, 1.0, 0.0)), f - vec3(0.0, 1.0, 0.0)),
                     dot(hash(i + vec3(1.0, 1.0, 0.0)), f - vec3(1.0, 1.0, 0.0)), u.x), u.y),
             mix(mix(dot(hash(i + vec3(0.0, 0.0, 1.0)), f - vec3(0.0, 0.0, 1.0)),
                     dot(hash(i + vec3(1.0, 0.0, 1.0)), f - vec3(1.0, 0.0, 1.0)), u.x),
                 mix(dot(hash(i + vec3(0.0, 1.0, 1.0)), f - vec3(0.0, 1.0, 1.0)),
                     dot(hash(i + vec3(1.0, 1.0, 1.0)), f - vec3(1.0, 1.0, 1.0)), u.x), u.y), u.z );
}
```

---
