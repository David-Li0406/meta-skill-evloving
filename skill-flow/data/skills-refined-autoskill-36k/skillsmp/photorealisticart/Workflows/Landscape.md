# Landscape Photography Workflow

Generate breathtaking photorealistic landscape and nature images.

## Quick Start

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "[LANDSCAPE PROMPT]" \
  --size 2K \
  --aspect-ratio 16:9 \
  --output ~/Downloads/landscape.png
```

---

## Landscape Types

### Golden Hour

**Template:**
```
Breathtaking landscape photograph of [LOCATION/SCENE],
golden hour sunlight casting long warm shadows,
dramatic clouds catching orange, pink, and purple light,
[FOREGROUND ELEMENT] providing depth and interest,
[MIDGROUND DETAILS],
[BACKGROUND/HORIZON],
shot on Sony A7R IV, 16-35mm at 24mm f/11,
focus stacked for infinite depth of field,
photorealistic, ultra detailed, 8K UHD, National Geographic quality
```

**Example:**
```
Breathtaking landscape photograph of Norwegian fjord,
golden hour sunlight casting long warm shadows on mountain peaks,
dramatic clouds catching orange, pink, and purple light,
wooden fishing boat in foreground providing scale,
calm reflective water in midground,
snow-capped mountains and glacier in background,
shot on Sony A7R IV, 16-35mm at 24mm f/11,
focus stacked for infinite depth of field,
photorealistic, ultra detailed, 8K UHD, National Geographic quality
```

### Blue Hour/Twilight

**Template:**
```
Serene blue hour landscape of [LOCATION],
twilight sky with deep blue to orange gradient on horizon,
[LIGHT SOURCES: city lights, stars, moon],
long exposure [DURATION] smoothing water/clouds,
[COMPOSITIONAL ELEMENTS],
shot on tripod, [SETTINGS],
photorealistic, ultra detailed, fine art landscape photography
```

### Dramatic Weather

**Template:**
```
Dramatic landscape of [LOCATION] during [WEATHER EVENT],
[SKY DESCRIPTION: storm clouds, lightning, breaking light],
[WEATHER EFFECTS: wind, rain, mist, fog],
[FOCAL POINT illuminated by break in clouds],
raw natural power captured in the moment,
shot on weather-sealed camera,
photorealistic, ultra detailed, storm photography
```

### Mountain/Alpine

**Template:**
```
Majestic alpine landscape, [MOUNTAIN RANGE/PEAK],
[SEASON: snow-covered, autumn colors, summer wildflowers],
[WEATHER/SKY CONDITIONS],
[FOREGROUND: alpine lake, meadow, trail],
dramatic scale and depth,
shot on medium format camera, 45mm f/8,
photorealistic, ultra detailed, adventure photography
```

### Coastal/Ocean

**Template:**
```
Stunning coastal landscape, [SPECIFIC LOCATION],
[WATER CONDITIONS: crashing waves, calm sea, tide pools],
[ROCK FORMATIONS, CLIFFS, BEACH],
[SKY AND LIGHTING CONDITIONS],
long exposure [X seconds] creating silky water effect,
shot on tripod with ND filter,
photorealistic, ultra detailed, seascape photography
```

### Forest/Woodland

**Template:**
```
Atmospheric forest landscape, [FOREST TYPE],
[LIGHTING: rays of light through canopy, misty morning, dappled shade],
[SEASON INDICATORS: fall colors, spring blooms, winter frost],
depth created by layered trees receding,
rich green tones and earth colors,
shot on [CAMERA], 35mm f/5.6,
photorealistic, ultra detailed, nature photography
```

---

## Technical Settings

### Recommended Settings by Scene

| Scene | Aperture | Focal Length | Other |
|-------|----------|--------------|-------|
| Wide vista | f/11 | 16-24mm | Focus stack |
| Intimate | f/5.6-8 | 35-50mm | Single focus |
| Telephoto compress | f/8-11 | 100-200mm | Tripod essential |
| Long exposure | f/11-16 | Any | ND filter, 10-30sec |

### Composition Keywords

```
leading lines, rule of thirds, foreground interest,
layered depth, frame within frame, negative space,
S-curve, diagonal tension, golden spiral
```

---

## Aspect Ratios

| Ratio | Use | Command |
|-------|-----|---------|
| 16:9 | Cinematic panorama | `--aspect-ratio 16:9` |
| 21:9 | Ultra-wide epic | `--aspect-ratio 21:9` |
| 3:2 | Classic landscape | `--aspect-ratio 3:2` |
| 4:3 | Balanced scenic | `--aspect-ratio 4:3` |
| 1:1 | Instagram, minimalist | `--aspect-ratio 1:1` |

---

## Time of Day Effects

| Time | Light Quality | Best For |
|------|--------------|----------|
| Blue hour (pre-dawn) | Cool, ethereal | Cityscapes, moody |
| Golden hour (sunrise) | Warm, soft, long shadows | Most landscapes |
| Midday | Harsh, flat | Avoid (or use clouds) |
| Golden hour (sunset) | Warm, dramatic | Most landscapes |
| Blue hour (dusk) | Cool gradient | City lights, stars |
| Night | Dark, point lights | Astro, cityscapes |

---

## Common Mistakes

| Problem | Solution |
|---------|----------|
| No focal point | Add clear subject or leading lines |
| Empty foreground | Add rocks, flowers, water, path |
| Boring sky | Wait for clouds, use golden hour |
| Flat looking | Add depth layers: fore/mid/background |
| Over-saturated | Specify "natural colors" |
