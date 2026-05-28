# PhotoRealisticArt - Extended Context

**Advanced techniques for generating stunning photorealistic images with AI.**

---

## Table of Contents

1. [Understanding Photorealism](#understanding-photorealism)
2. [Model Selection Guide](#model-selection-guide)
3. [Advanced Prompting Techniques](#advanced-prompting-techniques)
4. [Genre-Specific Guides](#genre-specific-guides)
5. [Post-Processing](#post-processing)
6. [Troubleshooting](#troubleshooting)
7. [Reference Image Workflows](#reference-image-workflows)

---

## Understanding Photorealism

### What Makes an Image Look Real

1. **Lighting Consistency** - Single coherent light source, proper shadow direction
2. **Depth of Field** - Realistic focus falloff, bokeh characteristics
3. **Texture Detail** - Skin pores, fabric weave, surface imperfections
4. **Color Accuracy** - Natural skin tones, environmental color cast
5. **Perspective** - Proper lens distortion, vanishing points
6. **Imperfections** - Dust, scratches, asymmetry, natural randomness

### The Uncanny Valley

Avoid these telltale AI artifacts:

| Issue | Cause | Solution |
|-------|-------|----------|
| Waxy skin | Over-smoothing | Add "skin texture, pores, fine details" |
| Floating objects | Poor grounding | Specify "standing on, sitting in, resting on" |
| Weird hands | Training data | Add "anatomically correct hands" or crop |
| Plastic hair | Simplified rendering | Add "individual hair strands, natural texture" |
| Dead eyes | Expression issues | Specify "catchlights, natural gaze, warm expression" |
| Over-saturation | HDR processing | Add "natural colors, realistic tones" |

---

## Model Selection Guide

### nano-banana-pro (Gemini 3 Pro)

**Best for:** Portraits, lifestyle, natural scenes

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "..." \
  --size 2K \
  --aspect-ratio 16:9
```

**Strengths:**
- Excellent skin tones and textures
- Natural lighting interpretation
- Good at complex scenes
- Multi-reference image support

**Limitations:**
- Occasionally misses small details
- Text rendering inconsistent

### gpt-image-1 (OpenAI)

**Best for:** Complex compositions, text, specific objects

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model gpt-image-1 \
  --prompt "..." \
  --size 1536x1024
```

**Strengths:**
- Excellent instruction following
- Good at text in images
- Consistent object placement

**Limitations:**
- Fixed size options only
- Can look slightly processed

### flux (Replicate)

**Best for:** Artistic photorealism, stylized realism

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model flux \
  --prompt "..." \
  --size 16:9
```

**Strengths:**
- Good artistic interpretation
- Consistent quality
- Fast generation

---

## Advanced Prompting Techniques

### The Layered Prompt Structure

```
[TECHNICAL SETUP]
[SUBJECT DESCRIPTION]
[ENVIRONMENT/CONTEXT]
[LIGHTING SPECIFICATION]
[MOOD/ATMOSPHERE]
[QUALITY AMPLIFIERS]
```

### Technical Setup Keywords

**Camera Bodies:**
```
shot on Canon EOS R5, Nikon Z9, Sony A7R V,
Phase One XF IQ4, Hasselblad X2D, Leica SL3
```

**Lenses:**
```
85mm f/1.2 portrait lens, 24-70mm f/2.8 zoom,
100mm macro lens, 70-200mm f/2.8 telephoto,
35mm f/1.4 prime, 14mm f/2.8 ultra-wide
```

**Settings:**
```
f/1.4 shallow DOF, f/8 sharp throughout,
1/500 frozen action, long exposure motion blur,
ISO 100 clean image, ISO 6400 atmospheric grain
```

### Subject Description Best Practices

**Faces:**
```
GOOD: "woman with light olive skin, dark brown eyes, subtle laugh lines,
       natural auburn hair with golden highlights"

BAD: "beautiful woman" (too vague, inconsistent results)
```

**Age Indicators:**
```
early 20s, mid 30s, late 40s, elderly with dignified wrinkles
```

**Expression:**
```
subtle genuine smile, thoughtful contemplative gaze,
confident direct eye contact, warm welcoming expression
```

### Environment Anchoring

Always ground subjects in their environment:

```
GOOD: "standing confidently in modern glass office, city skyline visible
       through floor-to-ceiling windows behind"

BAD: "in an office" (floating, undefined space)
```

### Lighting Specifications

**Three-Point Lighting (Studio):**
```
professional three-point lighting setup:
key light from 45 degrees camera left creating soft shadows,
fill light reducing contrast,
rim light from behind separating subject from background
```

**Natural Light:**
```
soft natural window light from camera right,
golden hour sunlight streaming through trees,
overcast day providing even diffused lighting
```

**Dramatic/Cinematic:**
```
single hard light source from above creating dramatic shadows,
chiaroscuro lighting reminiscent of Caravaggio,
practical neon lights reflecting on wet surfaces
```

---

## Genre-Specific Guides

### Portrait Photography

**Executive/Corporate:**
```
Professional executive portrait, [PERSON DESCRIPTION],
wearing tailored [ATTIRE] in corporate colors,
confident posture, direct eye contact with subtle smile,
shot in modern corner office with city view,
studio lighting with softbox key light,
shallow DOF f/2.0, 85mm lens,
photorealistic, ultra detailed, 8K UHD, corporate headshot
```

**Editorial/Fashion:**
```
High-fashion editorial portrait, [MODEL DESCRIPTION],
dramatic pose showcasing [CLOTHING/ACCESSORY],
dramatic studio lighting with strong shadows,
shot on medium format Hasselblad,
shallow DOF with creamy bokeh,
photorealistic, ultra detailed, Vogue magazine quality
```

**Environmental Portrait:**
```
Environmental portrait of [PERSON], [PROFESSION/CONTEXT],
naturally posed in their [WORKPLACE/ENVIRONMENT],
authentic expression showing passion for their craft,
natural lighting from [SOURCE],
shot on Sony A7R IV, 35mm f/2.0,
photorealistic, documentary photography style
```

### Landscape Photography

**Golden Hour:**
```
Breathtaking landscape of [LOCATION],
golden hour sunlight casting long shadows,
dramatic clouds catching warm orange and pink light,
foreground interest with [ELEMENT],
shot on Sony A7R IV, 16-35mm at 24mm f/11,
focus stacked for infinite depth of field,
photorealistic, ultra detailed, 8K UHD, National Geographic quality
```

**Blue Hour/Night:**
```
Serene blue hour landscape of [LOCATION],
twilight sky with gradient from deep blue to orange horizon,
city lights beginning to glow in distance,
long exposure smoothing water/clouds,
shot on tripod, 15 second exposure,
photorealistic, ultra detailed, fine art landscape
```

**Dramatic Weather:**
```
Dramatic landscape of [LOCATION] during storm,
dark ominous clouds with break letting light through,
rays of light illuminating [FOCAL POINT],
wind-swept [VEGETATION/ELEMENTS],
photorealistic, ultra detailed, weather photography
```

### Product Photography

**Hero Shot:**
```
Professional product photography, [PRODUCT] as hero shot,
floating at slight angle on pure white seamless background,
soft studio lighting with subtle shadows,
every detail visible and sharp,
shot on medium format camera with macro lens,
photorealistic, ultra detailed, commercial advertising quality
```

**Lifestyle Context:**
```
Lifestyle product photography, [PRODUCT] in natural setting,
being used by [PERSON DESCRIPTION] in [ENVIRONMENT],
natural lighting, authentic moment,
shallow DOF with product in sharp focus,
photorealistic, ultra detailed, aspirational advertising
```

**Detail/Texture:**
```
Macro product photography, extreme close-up of [PRODUCT],
showing [SPECIFIC DETAIL/TEXTURE/FEATURE],
dramatic side lighting revealing surface texture,
focus stacked for complete sharpness,
photorealistic, ultra detailed, 8K resolution
```

### Architecture Photography

**Exterior:**
```
Professional architectural photography, [BUILDING TYPE],
[ARCHITECTURAL STYLE] design,
shot during blue hour with interior lights glowing,
dramatic sky with clouds,
perfectly corrected verticals,
shot on tilt-shift lens, 24mm TS-E,
photorealistic, ultra detailed, Architectural Digest quality
```

**Interior:**
```
Interior architecture photography, [ROOM TYPE],
[STYLE] design with [KEY FEATURES],
natural light streaming through large windows,
carefully staged with [FURNITURE/DECOR],
HDR composite for balanced exposure,
photorealistic, ultra detailed, interior design magazine quality
```

### Cinematic Stills

**Film Noir:**
```
Cinematic film noir still, [SUBJECT] in [SCENE],
dramatic chiaroscuro lighting, deep shadows,
shot on vintage Cooke anamorphic lens,
subtle film grain, desaturated color palette,
photorealistic, ultra detailed, 1940s Hollywood aesthetic
```

**Modern Blockbuster:**
```
Cinematic still from modern action film,
[SUBJECT] in [ACTION/SCENE],
dynamic composition with dramatic angles,
teal and orange color grade,
shallow DOF, anamorphic lens flare,
photorealistic, ultra detailed, IMAX quality
```

**Indie Drama:**
```
Intimate cinematic still from indie drama,
[SUBJECT] in [EMOTIONAL MOMENT],
soft natural lighting, muted color palette,
35mm film aesthetic with subtle grain,
shallow DOF creating intimacy,
photorealistic, A24 film aesthetic
```

---

## Post-Processing

### Background Removal

For transparent backgrounds:

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "..." \
  --remove-bg \
  --output ~/Downloads/transparent.png
```

### Thumbnail with Background

Create both transparent and thumbnail versions:

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "..." \
  --thumbnail \
  --output ~/Downloads/image.png
```

Creates:
- `image.png` (transparent)
- `image-thumb.png` (with #0a0a0f background)

### Adding Custom Background

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "..." \
  --remove-bg \
  --add-bg "#ffffff" \
  --output ~/Downloads/white-bg.png
```

---

## Troubleshooting

### Common Issues and Solutions

| Problem | Solution |
|---------|----------|
| Skin looks plastic | Add "skin texture, pores, subsurface scattering" |
| Eyes look dead | Add "catchlights in eyes, natural gaze" |
| Lighting inconsistent | Specify single light source direction |
| Background distracting | Add "clean background, soft bokeh" |
| Too saturated | Add "natural colors, realistic tones" |
| Lack of depth | Add specific DOF "f/2.0, shallow depth of field" |
| Generic looking | Add specific camera/lens "shot on Canon R5, 85mm f/1.2" |
| Wrong time of day | Specify "golden hour", "midday sun", "overcast" |

### Iteration Strategy

1. **First attempt:** Full detailed prompt
2. **If too artificial:** Add texture/imperfection keywords
3. **If composition wrong:** Be more specific about framing
4. **If lighting off:** Specify exact light source and direction
5. **If still wrong:** Try different model

---

## Reference Image Workflows

### Character Consistency

Use multiple reference images to maintain character consistency:

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "The person from the reference images, now wearing formal attire,
            standing in an elegant ballroom, golden chandeliers above,
            warm ambient lighting, photorealistic, ultra detailed" \
  --reference-image ~/ref/face1.jpg \
  --reference-image ~/ref/face2.jpg \
  --reference-image ~/ref/face3.jpg \
  --size 2K \
  --aspect-ratio 3:4
```

### Style Transfer

Reference an image style while changing subject:

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "Modern architecture building in the exact photographic style
            of the reference image, same lighting quality, color treatment,
            and composition approach, photorealistic" \
  --reference-image ~/ref/style-reference.jpg \
  --size 2K \
  --aspect-ratio 16:9
```

### API Limits for References

- Up to 5 human reference images
- Up to 6 object reference images
- Maximum 14 total references per request

---

## Quality Checklist

Before finalizing any photorealistic image:

- [ ] Lighting is consistent and directional
- [ ] Shadows fall in correct direction
- [ ] Skin tones look natural (not orange or grey)
- [ ] Eyes have catchlights and natural expression
- [ ] Hands/fingers look anatomically correct
- [ ] Text (if any) is legible
- [ ] Background supports but doesn't distract
- [ ] Overall color palette feels natural
- [ ] Depth of field matches camera settings described
- [ ] No obvious AI artifacts (extra limbs, melted objects)

---

## Integration with Other Skills

### Art Skill
PhotoRealisticArt uses the same `Generate.ts` tool as the Art skill but with different prompting approaches optimized for realism rather than illustration.

### Blog Skill
Generate photorealistic blog headers and featured images:
```
User: "Create a photorealistic header for my blog post about remote work"
-> Uses PhotoRealisticArt Lifestyle prompt
-> Places in ~/Downloads for review
```
