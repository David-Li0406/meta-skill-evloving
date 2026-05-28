# Portrait Photography Workflow

Generate stunning photorealistic portraits - from executive headshots to editorial fashion.

## Quick Start

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "[PORTRAIT PROMPT]" \
  --size 2K \
  --aspect-ratio 3:4 \
  --output ~/Downloads/portrait.png
```

---

## Portrait Types

### Executive/Corporate Headshot

**Template:**
```
Professional executive portrait, [AGE] [GENDER] [ETHNICITY] professional,
[HAIR DESCRIPTION], [EYE COLOR], [FACIAL FEATURES],
wearing tailored [ATTIRE COLOR] [ATTIRE TYPE],
confident posture with shoulders squared to camera,
direct eye contact with subtle confident smile,
studio lighting: softbox key light from 45 degrees,
subtle fill light, rim light separating from background,
neutral grey gradient background,
shallow DOF f/2.0, 85mm portrait lens,
photorealistic, ultra detailed, 8K UHD, professional headshot
```

**Example:**
```
Professional executive portrait, mid-40s woman with warm olive skin,
shoulder-length dark brown hair with natural waves, hazel eyes,
wearing tailored navy blazer over white silk blouse,
confident posture with shoulders squared to camera,
direct eye contact with subtle confident smile,
studio lighting: softbox key light from 45 degrees,
subtle fill light, rim light separating from background,
neutral grey gradient background,
shallow DOF f/2.0, 85mm portrait lens,
photorealistic, ultra detailed, 8K UHD, professional headshot
```

### Editorial Fashion

**Template:**
```
High-fashion editorial portrait, [MODEL DESCRIPTION],
dramatic [POSE] showcasing [CLOTHING/JEWELRY],
[MAKEUP/STYLING DETAILS],
shot in [ENVIRONMENT/SET],
[LIGHTING SETUP],
shot on Hasselblad medium format, 80mm f/2.8,
dramatic composition with negative space,
photorealistic, ultra detailed, Vogue magazine quality
```

### Environmental Portrait

**Template:**
```
Environmental portrait, [PERSON DESCRIPTION],
[PROFESSION/ROLE] in their natural element,
authentically posed in [SPECIFIC WORKPLACE/SETTING],
natural expression showing [EMOTION/CHARACTER],
[LIGHTING: usually natural or practical],
shot on Sony A7R IV, 35mm f/2.0,
contextual background telling their story,
photorealistic, documentary photography style
```

### Casual/Lifestyle

**Template:**
```
Lifestyle portrait, [PERSON DESCRIPTION],
relaxed natural pose [ACTION/POSITION],
wearing [CASUAL ATTIRE],
in [RELATABLE ENVIRONMENT],
soft natural lighting from [SOURCE],
candid authentic moment,
shallow DOF f/2.8, 50mm lens,
photorealistic, ultra detailed, lifestyle photography
```

---

## Lighting Setups

### Rembrandt Lighting
Classic portrait lighting with triangle of light under eye:
```
Rembrandt lighting setup, key light 45 degrees to side and above,
creating characteristic triangle of light on shadow-side cheek
```

### Butterfly/Paramount
Glamorous, minimizes wrinkles:
```
Butterfly lighting, key light directly above and in front,
creating butterfly-shaped shadow under nose, glamour style
```

### Split Lighting
Dramatic, mysterious:
```
Split lighting, key light at 90 degrees,
illuminating exactly half the face, dramatic contrast
```

### Broad vs Short
Emphasize or slim the face:
```
Broad lighting, illuminated side facing camera (emphasizes face width)
Short lighting, shadow side facing camera (slims face)
```

---

## Aspect Ratios for Portraits

| Ratio | Use | Command |
|-------|-----|---------|
| 3:4 | Classic portrait | `--aspect-ratio 3:4` |
| 4:5 | Instagram portrait | `--aspect-ratio 4:5` |
| 2:3 | Full body, editorial | `--aspect-ratio 2:3` |
| 1:1 | Square headshot | `--aspect-ratio 1:1` |

---

## Common Issues

| Problem | Fix |
|---------|-----|
| Stiff pose | Add "natural relaxed pose, authentic moment" |
| Dead eyes | Add "genuine expression, catchlights, warm gaze" |
| Plastic skin | Add "natural skin texture, pores, fine lines" |
| Wrong ethnicity | Be more specific in description |
| Generic face | Add unique features, specific age, character |
