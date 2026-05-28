---
name: generate-storyboard
description: Generate a storyboard with ComfyUI image prompts from the script. Use after script.md exists in the project folder.
disable-model-invocation: true
allowed-tools: Read, Write, Glob
---

# Generate Storyboard with Image Prompts

Read the script.md and generate a detailed storyboard with ComfyUI-ready image prompts.

## Steps

1. Read `script.md` to get the scenes
2. Generate a storyboard with ~12 scenes (one per ~5 seconds)
3. Create detailed image prompts for each scene
4. Save as `storyboard.md` in the current folder

## Storyboard Structure

```markdown
# Storyboard: [Title]

## Style Guide
- **Art style:** [e.g., cinematic photorealistic, anime, 3D render]
- **Color palette:** [e.g., warm tones, neon cyberpunk, pastel]
- **Lighting:** [e.g., dramatic, soft natural, studio]
- **Consistent elements:** [character descriptions to keep consistent]

---

## Scene 1 (0:00 - 0:05)
**Visual Description:** [What happens in the scene]
**Camera:** [Shot type - close-up, wide, zoom in/out, pan]
**Prompt:** "[Detailed ComfyUI prompt]"
**Negative:** "ugly, blurry, low quality, distorted, deformed, extra limbs"
**Text Overlay:** [Any on-screen text]
**Audio:** [VO line or SFX]

---

## Scene 2 (0:05 - 0:10)
...continue for all scenes...

---

## Prompt Consistency Notes
- Character: [Describe main character for consistency across scenes]
- Setting: [Recurring location details]
- Style suffix: [Add to all prompts for consistency]
```

## ComfyUI Prompt Guidelines

Write prompts that work well with Stable Diffusion / SDXL:

### Good Prompt Structure
```
[subject], [action/pose], [setting/background], [lighting], [style], [quality tags]
```

### Example Prompts
- "orange tabby cat wearing NASA spacesuit, sitting in spaceship cockpit, control panels with glowing buttons, dramatic cinematic lighting, photorealistic, 8k, highly detailed"
- "young woman with red hair, surprised expression, holding glowing crystal, dark cave background, volumetric light rays, fantasy art style, trending on artstation"

### Quality Tags to Include
- For realism: "photorealistic, 8k, highly detailed, professional photography"
- For art: "digital art, trending on artstation, concept art, highly detailed"
- For anime: "anime style, studio ghibli, vibrant colors, clean lines"

### Things to Specify
- Subject details (age, clothing, expression, pose)
- Environment/background
- Lighting (golden hour, dramatic, soft, neon)
- Camera angle (close-up, wide shot, low angle)
- Art style
- Quality modifiers

### Keep Consistent
- Same character description across all scenes
- Same style tags across all prompts
- Same quality modifiers

## Output

Save the storyboard to `storyboard.md` and confirm with the user.
