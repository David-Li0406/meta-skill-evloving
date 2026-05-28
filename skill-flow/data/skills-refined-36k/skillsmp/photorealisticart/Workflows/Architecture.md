# Architecture Photography Workflow

Generate stunning photorealistic architectural images - exteriors, interiors, and real estate.

## Quick Start

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "[ARCHITECTURE PROMPT]" \
  --size 2K \
  --aspect-ratio 16:9 \
  --output ~/Downloads/architecture.png
```

---

## Architecture Types

### Exterior - Modern

**Template:**
```
Professional architectural photography, modern [BUILDING TYPE],
[ARCHITECTURAL STYLE: minimalist, brutalist, parametric, glass and steel],
[KEY DESIGN FEATURES],
shot during blue hour with interior lights glowing warmly,
dramatic sky with clouds adding interest,
perfectly corrected vertical lines,
shot on tilt-shift lens, 24mm TS-E f/11,
photorealistic, ultra detailed, Architectural Digest quality
```

**Example:**
```
Professional architectural photography, modern luxury residence,
minimalist glass and concrete design with cantilevered upper floor,
floor-to-ceiling windows, clean geometric lines,
shot during blue hour with interior lights glowing warmly,
dramatic sky with purple and orange clouds,
perfectly corrected vertical lines,
shot on tilt-shift lens, 24mm TS-E f/11,
photorealistic, ultra detailed, Architectural Digest quality
```

### Exterior - Historic/Classic

**Template:**
```
Professional architectural photography, [HISTORIC BUILDING],
[ARCHITECTURAL STYLE: Victorian, Gothic, Art Deco, Beaux-Arts],
[DISTINCTIVE FEATURES: columns, ornate details, façade],
[LIGHTING CONDITIONS: golden hour, dramatic clouds],
shot emphasizing symmetry and grandeur,
perfectly corrected perspective,
photorealistic, ultra detailed, heritage architecture quality
```

### Interior - Residential

**Template:**
```
Interior architecture photography, [ROOM TYPE: living room, kitchen, bedroom],
[DESIGN STYLE: modern, minimalist, Scandinavian, industrial],
[KEY FEATURES: furniture, art, materials],
natural light streaming through [WINDOW TYPE],
warm inviting atmosphere,
styled with [DECOR ELEMENTS],
shot on wide angle 17mm, HDR composite for balanced exposure,
photorealistic, ultra detailed, interior design magazine quality
```

### Interior - Commercial

**Template:**
```
Commercial interior architecture photography, [SPACE TYPE: lobby, office, restaurant],
[DESIGN CONCEPT AND STYLE],
[KEY ARCHITECTURAL FEATURES],
professional lighting design visible,
human activity suggesting scale and purpose,
shot on 24mm tilt-shift lens,
photorealistic, ultra detailed, commercial architecture portfolio
```

### Real Estate

**Template:**
```
Professional real estate photography, [PROPERTY TYPE],
[ROOM/VIEW DESCRIPTION],
bright and airy with natural daylight,
clean and staged for maximum appeal,
HDR balanced exposure showing interior and window views,
wide angle composition maximizing space perception,
photorealistic, ultra detailed, luxury real estate marketing
```

---

## Architectural Styles

### Modern/Contemporary
```
clean lines, floor-to-ceiling glass, open plan,
minimalist aesthetic, natural materials, indoor-outdoor flow
```

### Mid-Century Modern
```
post and beam construction, large windows, organic forms,
integration with nature, iconic furniture, warm wood tones
```

### Industrial
```
exposed brick, steel beams, concrete floors,
high ceilings, large windows, raw materials
```

### Art Deco
```
geometric patterns, bold colors, luxurious materials,
stepped forms, decorative metalwork, glamorous lighting
```

### Victorian/Historic
```
ornate detailing, crown moldings, period features,
bay windows, decorative plasterwork, heritage character
```

---

## Lighting Scenarios

### Blue Hour Exterior
Best for modern buildings with interior lighting:
```
shot during blue hour, interior lights glowing,
twilight sky providing even ambient light,
balance between interior warmth and cool exterior
```

### Golden Hour Exterior
Warm, inviting feel:
```
golden hour sunlight warming the façade,
long shadows creating depth and dimension,
dramatic clouds catching warm light
```

### Natural Light Interior
Authentic, airy feel:
```
natural daylight streaming through windows,
soft shadows, realistic light falloff,
no harsh artificial lighting
```

### Mixed Lighting Interior
Professional real estate/editorial:
```
HDR composite balancing window light and interior,
all areas properly exposed,
natural color temperature throughout
```

---

## Technical Considerations

### Correcting Verticals
Always specify to avoid distortion:
```
perfectly corrected vertical lines,
no perspective distortion,
shot on tilt-shift lens
```

### HDR for Interiors
Balance bright windows with darker interiors:
```
HDR composite for balanced exposure,
window views visible without blown highlights,
interior details preserved in shadows
```

### Wide Angle Without Distortion
```
wide angle 17-24mm maintaining natural perspective,
no barrel distortion,
edges of frame not stretched
```

---

## Aspect Ratios

| Ratio | Use | Command |
|-------|-----|---------|
| 16:9 | Exterior panoramic | `--aspect-ratio 16:9` |
| 4:3 | Interior rooms | `--aspect-ratio 4:3` |
| 3:2 | Balanced exterior | `--aspect-ratio 3:2` |
| 9:16 | Tall buildings, vertical | `--aspect-ratio 9:16` |
| 1:1 | Social media | `--aspect-ratio 1:1` |

---

## Common Issues

| Problem | Solution |
|---------|----------|
| Converging verticals | Specify "tilt-shift lens, corrected verticals" |
| Interior too dark | Add "HDR balanced exposure" |
| Windows blown out | Specify "window views visible" |
| Space looks small | Use "wide angle, maximize space perception" |
| Looks like render | Add imperfections: "lived-in, natural wear" |
| Wrong time of day | Specify exact lighting: "blue hour", "midday overcast" |
