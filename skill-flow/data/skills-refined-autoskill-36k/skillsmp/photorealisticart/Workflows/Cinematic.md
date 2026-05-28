# Cinematic Photography Workflow

Generate photorealistic movie stills and cinematic scenes.

## Quick Start

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "[CINEMATIC PROMPT]" \
  --size 2K \
  --aspect-ratio 21:9 \
  --output ~/Downloads/cinematic.png
```

---

## Cinematic Styles

### Modern Blockbuster

**Template:**
```
Cinematic still from modern blockbuster film,
[SUBJECT/CHARACTER] in [ACTION/SCENE],
dynamic composition with dramatic camera angle,
teal and orange color grade,
anamorphic lens with characteristic flare,
shallow depth of field with creamy bokeh,
film grain, high production value,
photorealistic, ultra detailed, IMAX quality
```

**Example:**
```
Cinematic still from modern blockbuster film,
female action hero in tactical gear sprinting through rain-soaked Tokyo street,
dynamic low angle composition,
neon signs reflecting off wet pavement,
teal and orange color grade,
anamorphic lens with characteristic oval bokeh and flare,
subtle film grain, high production value,
photorealistic, ultra detailed, IMAX quality
```

### Film Noir

**Template:**
```
Cinematic film noir still,
[CHARACTER: detective, femme fatale, gangster] in [SCENE],
dramatic chiaroscuro lighting with deep shadows,
single hard light source creating venetian blind shadows,
desaturated color palette or black and white,
shot on vintage Cooke anamorphic lens,
subtle film grain, 1940s Hollywood aesthetic,
photorealistic, ultra detailed, classic cinema quality
```

### Indie Drama

**Template:**
```
Intimate cinematic still from indie drama,
[CHARACTER] in [EMOTIONAL MOMENT/SITUATION],
soft natural lighting from practical sources,
muted color palette with earth tones,
35mm film aesthetic with organic grain,
shallow DOF creating intimacy,
quiet contemplative composition,
photorealistic, A24 film aesthetic, Sundance quality
```

### Sci-Fi/Dystopian

**Template:**
```
Cinematic still from sci-fi epic,
[CHARACTER/SCENE] in [FUTURISTIC ENVIRONMENT],
dramatic volumetric lighting through atmospheric haze,
blue and orange/cyan color palette,
practical lighting from screens and holograms,
anamorphic widescreen composition,
subtle lens flares and atmospheric effects,
photorealistic, ultra detailed, Blade Runner aesthetic
```

### Period Drama

**Template:**
```
Cinematic still from period drama set in [ERA],
[CHARACTER] in [SCENE/LOCATION],
authentic costume and set design,
natural candlelit/firelit atmosphere (or period-appropriate),
rich warm color palette,
shot on vintage glass with character,
soft romantic lighting,
photorealistic, ultra detailed, Oscar-worthy production design
```

### Horror/Thriller

**Template:**
```
Cinematic still from horror film,
[SUBJECT/SCENE] in [UNSETTLING ENVIRONMENT],
low-key lighting with deep blacks,
cold desaturated color palette,
unnerving composition with negative space,
subtle motion blur or grain adding tension,
practical effects, no CGI aesthetic,
photorealistic, ultra detailed, atmospheric horror
```

### Action/Thriller

**Template:**
```
Cinematic still from action thriller,
[CHARACTER] in [HIGH-STAKES MOMENT],
dynamic composition with motion and energy,
dramatic lighting with strong contrast,
teal shadows, orange highlights,
handheld aesthetic with subtle movement,
anamorphic widescreen with lens character,
photorealistic, ultra detailed, Bourne/Mission Impossible quality
```

---

## Color Grades by Genre

### Teal and Orange (Blockbuster)
```
teal and orange color grade,
warm skin tones against cool backgrounds,
complementary color contrast
```

### Desaturated (Drama)
```
muted desaturated color palette,
lifted blacks, reduced contrast,
natural earth tones
```

### High Contrast (Noir)
```
high contrast black and white,
deep blacks, bright highlights,
dramatic tonal range
```

### Neon/Cyberpunk
```
vibrant neon color palette,
magenta, cyan, and purple dominant,
high saturation night scenes
```

### Warm Period
```
warm sepia-tinted color grade,
golden candlelight tones,
rich amber and brown palette
```

### Cold/Horror
```
cold desaturated color grade,
blue-green shadows,
sickly undertones
```

---

## Camera and Lens Language

### Anamorphic Look
```
anamorphic lens, oval bokeh,
horizontal lens flares,
slight edge distortion,
2.39:1 widescreen aspect
```

### Vintage Glass
```
shot on vintage Cooke or Panavision glass,
organic flares, subtle aberration,
character in the rendering
```

### Modern Sharp
```
shot on modern Zeiss Master Primes,
clinically sharp, clean rendering,
minimal distortion
```

### Handheld Documentary
```
handheld documentary style,
subtle motion and shake,
immediate and visceral feel
```

---

## Composition Techniques

### Rule of Thirds with Tension
```
subject placed at intersection points,
negative space creating unease or anticipation
```

### Leading Lines
```
environmental lines drawing eye to subject,
architectural or natural leading lines
```

### Frame Within Frame
```
doorways, windows, mirrors creating nested frames,
adds depth and visual interest
```

### Dutch Angle
```
tilted frame creating unease,
disorientation for psychological effect
```

### Symmetry
```
centered symmetrical composition,
formality and power,
Wes Anderson or Kubrick style
```

---

## Aspect Ratios

| Ratio | Style | Command |
|-------|-------|---------|
| 21:9 | Ultra-wide cinematic | `--aspect-ratio 21:9` |
| 16:9 | Standard widescreen | `--aspect-ratio 16:9` |
| 2:3 | Classic film (vertical) | `--aspect-ratio 2:3` |
| 4:3 | Academy ratio, nostalgic | `--aspect-ratio 4:3` |

---

## Genre Reference Keywords

### By Director Style

| Director | Keywords |
|----------|----------|
| Nolan | IMAX, practical effects, deep blacks, epic scale |
| Fincher | Desaturated, precise composition, unsettling |
| Villeneuve | Vast scale, fog/atmosphere, minimal score feel |
| Wes Anderson | Symmetry, pastel palette, quirky staging |
| Kubrick | One-point perspective, cold precision |
| Spielberg | Warm lighting, wonder, classic Hollywood |
| A24 Films | Natural light, muted colors, intimate |

---

## Common Issues

| Problem | Solution |
|---------|----------|
| Looks like photo, not film | Add "film grain, anamorphic, cinematic lighting" |
| Wrong era feel | Specify exact color grade and lighting style |
| Too static | Add "dynamic composition, tension, movement" |
| Generic look | Reference specific director or film style |
| Over-processed | Add "natural, practical lighting, subtle grade" |
