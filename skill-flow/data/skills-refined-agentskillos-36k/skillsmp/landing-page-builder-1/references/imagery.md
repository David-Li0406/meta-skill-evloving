# Imagery Strategy

Imagery is half the story. Every hero, feature card, and section needs intentional visuals.

## Image Roles by Section

| Section | Role | Format |
|---------|------|--------|
| Hero | Set mood, show outcome | Full-bleed, illustration, or product shot |
| Problem | Visualize pain (subtly) | Icons, abstract illustrations |
| Demo | Product in action | Screenshots, UI mockups, video |
| Benefits | Represent each outcome | Icons or small illustrations |
| Proof | Humanize trust | Headshots, company logos |
| CTA | Reinforce transformation | Echo hero visual |

## Sourcing Options

### Stock (Envato Elements)
For conventional imagery—people, workspaces, objects.

**Search tips:**
- ❌ "business" → ✅ "diverse team whiteboard brainstorm startup"
- ❌ "technology" → ✅ "developer laptop dark mode minimal desk"

### AI-Generated (Nano Banana Pro 3)
For unique illustrations, abstract visuals, or brand-specific imagery.

**Workflow:**
1. Generate prompts based on brand aesthetic + section needs
2. User generates images using prompts
3. User drops images into `/brand/images/`
4. Integrate images into components

## Prompt Output Format

For each image needed, provide:

```
SECTION: [Hero / Benefits / etc.]
PURPOSE: [Story this image tells]
PROMPT: [Detailed generation prompt]
STYLE NOTES: [Must match brand tokens]
FILENAME: [hero-main.webp]
DROP LOCATION: /brand/images/
```

## Prompt Formula

`[Subject] + [Action/State] + [Style] + [Mood] + [Colors from tokens]`

## Example Prompts by Aesthetic

### Glassmorphism
```
Abstract 3D glass shapes floating, soft gradients, blue and purple tones, 
minimal, depth of field, frosted translucent surfaces, studio lighting
```

### Neo-Brutalism
```
Bold geometric shapes, flat illustration, black outlines, clashing orange 
and pink, raw unpolished texture, risograph print style, grain overlay
```

### Dark Academia
```
Vintage library interior, warm candlelight, leather books, moody shadows, 
sepia and brown tones, film grain, soft focus edges
```

### Aurora / Gradient
```
Flowing silk fabric in motion, soft light, iridescent purple and teal 
gradients, dreamy ethereal atmosphere, subtle bokeh
```

### Tech / Minimal
```
Abstract data visualization, dark background, glowing cyan accent lines, 
particle network, depth of field, clean geometric forms
```

## Technical Requirements

| Spec | Requirement |
|------|-------------|
| Format | WebP preferred, PNG fallback |
| Hero | 1920w, 1280w, 640w srcset |
| Cards | 4:3 aspect ratio |
| Icons | 1:1, SVG when possible |
| Alt text | Descriptive, generated for each |
