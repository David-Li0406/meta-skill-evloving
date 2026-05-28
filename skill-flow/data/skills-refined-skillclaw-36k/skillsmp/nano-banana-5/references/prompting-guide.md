# Nano Banana PRO Prompting Guide

## Core Philosophy

Nano Banana PRO is a **"Thinking" model**. It doesn't just match keywords—it understands intent, physics, and composition. Stop using "tag soups" (e.g., `dog, park, 4k, realistic`) and start acting like a Creative Director.

## The Golden Rules

### 1. Edit, Don't Re-roll
If an image is 80% correct, don't regenerate from scratch. Ask for specific changes:
- "Change the lighting to sunset and make the text neon blue"
- "Move the subject to the left and add more negative space"

### 2. Use Natural Language
Talk to the model like briefing a human artist.

❌ **Bad:** `cool car, neon, city, night, 8k`

✅ **Good:** `A cinematic wide shot of a futuristic sports car speeding through a rainy Tokyo street at night. The neon signs reflect off the wet pavement and the car's metallic chassis.`

### 3. Be Specific and Descriptive
Define subject, setting, lighting, and mood explicitly:

- **Subject:** Instead of "a woman," say "a sophisticated elderly woman wearing a vintage Chanel-style suit"
- **Materiality:** Describe textures—"matte finish," "brushed steel," "soft velvet," "crumpled paper"
- **Lighting:** "soft golden hour light," "harsh overhead fluorescent," "dramatic rim lighting"

### 4. Provide Context (The "Why")
Context helps the model make logical artistic decisions:
- "Create an image of a sandwich **for a Brazilian high-end gourmet cookbook**" → Model infers professional plating, shallow depth of field, perfect lighting

## The ICS Framework

For any image request, define:

| Element | Description | Examples |
|---------|-------------|----------|
| **I**mage Type | What kind of visual | Product photo, infographic, UI mockup, illustration, logo, sticker |
| **C**ontent | Specific elements | Data sources, text, brand elements, objects, people |
| **S**tyle | Visual approach | Photorealistic, minimalist, retro, corporate, hand-drawn, anime |

## Prompt Templates by Category

### 1. Photorealistic Scenes

**Template:**
```
A photorealistic [shot type] of [subject], [action or expression], set in [environment]. The scene is illuminated by [lighting description], creating a [mood] atmosphere. Captured with a [camera/lens details], emphasizing [key textures and details]. [Aspect ratio].
```

**Example:**
```
A photorealistic close-up portrait of an elderly Japanese ceramicist with deep, sun-etched wrinkles and a warm, knowing smile. He is carefully inspecting a freshly glazed tea bowl. The setting is his rustic, sun-drenched workshop. The scene is illuminated by soft, golden hour light streaming through a window, highlighting the fine texture of the clay. Captured with an 85mm portrait lens, resulting in a soft, blurred background (bokeh). The overall mood is serene and masterful. Vertical portrait orientation.
```

### 2. Stylized Illustrations & Stickers

**Template:**
```
A [style] sticker of a [subject], featuring [key characteristics] and a [color palette]. The design should have [line style] and [shading style]. The background must be [white/transparent].
```

**Example:**
```
A kawaii-style sticker of a happy red panda wearing a tiny bamboo hat. It's munching on a green bamboo leaf. The design features bold, clean outlines, simple cel-shading, and a vibrant color palette. The background must be white.
```

### 3. Text Rendering (Logos, Signage)

**Template:**
```
Create a [image type] for [brand/concept] with the text "[exact text]" in a [font style]. The design should be [style description], with a [color scheme].
```

**Example:**
```
Create a modern, minimalist logo for a coffee shop called 'The Daily Grind'. The text should be in a clean, bold, sans-serif font. The color scheme is black and white. Put the logo in a circle. Use a coffee bean in a clever way.
```

**Tips for text:**
- Put exact text in quotes
- Specify font style descriptively (serif, sans-serif, handwritten, technical)
- PRO model has SOTA text rendering—use it for any text-heavy output

### 4. Product Mockups & Commercial Photography

**Template:**
```
A high-resolution, studio-lit product photograph of a [product description] on a [background surface]. The lighting is a [lighting setup] to [purpose]. The camera angle is a [angle] to showcase [feature]. Ultra-realistic, with sharp focus on [key detail]. [Aspect ratio].
```

**Example:**
```
A high-resolution, studio-lit product photograph of a minimalist ceramic coffee mug in matte black, presented on a polished concrete surface. The lighting is a three-point softbox setup designed to create soft, diffused highlights and eliminate harsh shadows. The camera angle is a slightly elevated 45-degree shot to showcase its clean lines. Ultra-realistic, with sharp focus on the steam rising from the coffee. Square image.
```

### 5. Infographics & Data Visualization

**Template:**
```
Create a [style] infographic about [topic]. Include [specific sections/data]. The design should be [visual style] with [color palette]. Ensure all text is legible and [specific text requirements].
```

**Example:**
```
Create a clean, modern infographic summarizing the key financial highlights from an earnings report. Include charts for 'Revenue Growth' and 'Net Income', and highlight the CEO's key quote in a stylized pull-quote box.
```

**Example with real-time data (requires Google Search tool):**
```
Visualize the current weather forecast for the next 5 days in San Francisco as a clean, modern weather chart. Add a visual on what I should wear each day.
```

### 6. Minimalist & Negative Space Design

**Template:**
```
A minimalist composition featuring a single [subject] positioned in the [position] of the frame. The background is a vast, empty [color] canvas, creating significant negative space. Soft, subtle lighting. [Aspect ratio].
```

**Example:**
```
A minimalist composition featuring a single, delicate red maple leaf positioned in the bottom-right of the frame. The background is a vast, empty off-white canvas, creating significant negative space for text. Soft, diffused lighting from the top left. Square image.
```

### 7. Sequential Art & Storyboards

**Template:**
```
Create a [N]-panel comic/storyboard in a [style]. Feature [characters]. The story should [narrative arc]. Keep identity consistent throughout but vary angles and expressions. [Aspect ratio per panel].
```

**Example:**
```
Make a 3 panel comic in a gritty, noir art style with high-contrast black and white inks. Put the character in a humorous scene.
```

### 8. Character Consistency (Multiple Images)

PRO supports up to 14 reference images (6 high-fidelity, 5 humans).

**Template:**
```
[Upload reference images]
Using the person from Image 1, create [scene description]. Face Consistency: Keep the person's facial features exactly the same as Image 1, but change their expression to [expression]. [Additional scene details].
```

**Example:**
```
Design a viral video thumbnail using the person from Image 1. Face Consistency: Keep the person's facial features exactly the same as Image 1, but change their expression to look excited and surprised. Action: Pose the person on the left side, pointing their finger towards the right side of the frame. Subject: On the right side, place a high-quality image of a delicious avocado toast. Graphics: Add a bold yellow arrow connecting the person's finger to the toast. Text: Overlay massive, pop-style text: '3分钟搞定!' Use a thick white outline and drop shadow.
```

## Advanced Techniques

### Structural Control (Sketch-to-Image)

Upload hand-drawn sketches, wireframes, or grid layouts to control composition:

```
Create a high-end magazine advertisement for a luxury perfume brand called 'Nebula' based on this hand-drawn sketch. Keep the exact layout of the bottle and text placement, but render it in a photorealistic style with a galaxy-themed background.
```

### 2D to 3D Translation

```
Turn the 'This is Fine' dog meme into a photorealistic 3D render. Keep the composition identical but make the dog look like a plush toy and the fire look like realistic flames.
```

### Floor Plan to Interior Design

```
Based on the uploaded 2D floor plan, generate a professional interior design presentation board in a single image. Layout: A collage with one large main image at the top (wide-angle perspective of the living area), and three smaller images below. Style: Modern Minimalist with warm oak wood flooring. Quality: Photorealistic rendering, soft natural lighting.
```

### Thinking Process

PRO uses reasoning ("Thinking") for complex prompts. It generates interim "thought images" to refine composition before the final output. You can access these thoughts in the API response for debugging.

## Photography & Lighting Keywords

### Shot Types
- Extreme close-up, close-up, medium shot, full shot, wide shot, aerial shot
- Low angle, high angle, eye level, Dutch angle, over-the-shoulder
- Tracking shot, establishing shot, POV shot

### Lighting
- Natural light, golden hour, blue hour, overcast
- Studio lighting, three-point lighting, rim lighting, backlighting
- Hard light, soft light, diffused light, dramatic shadows
- Neon, ambient, candlelight, spotlight

### Camera/Lens
- 24mm wide angle, 35mm standard, 50mm normal, 85mm portrait, 135mm telephoto
- Shallow depth of field, deep focus, bokeh, tilt-shift
- Film grain, motion blur, long exposure

## Resolution & Aspect Ratio Guide

| Use Case | Aspect Ratio | Recommended Size |
|----------|--------------|------------------|
| Social media square | 1:1 | 1K-2K |
| Instagram portrait | 4:5 | 1K-2K |
| YouTube thumbnail | 16:9 | 2K |
| Website hero | 16:9 or 21:9 | 2K-4K |
| Print/poster | 3:4 or 4:3 | 4K |
| Mobile wallpaper | 9:16 | 2K |
| Logo | 1:1 | 1K |

## Common Mistakes to Avoid

1. **Tag soup prompts** - Lists of keywords without narrative structure
2. **Vague subjects** - "A person" vs "A determined young athlete in racing gear"
3. **Missing lighting** - Always specify light source and quality
4. **Ignoring composition** - Describe where elements should be positioned
5. **Re-rolling instead of editing** - Use multi-turn to refine, not restart
6. **Wrong model choice** - Use PRO for text-heavy or professional work

## Quick Reference: Prompt Modifiers

### Quality
- Ultra-realistic, hyper-detailed, photorealistic, 8K, sharp focus
- Masterpiece, professional quality, award-winning

### Mood
- Serene, dramatic, mysterious, playful, elegant, gritty, whimsical

### Style
- Minimalist, vintage, retro, futuristic, cyberpunk, steampunk
- Anime, cartoon, watercolor, oil painting, digital art
- Corporate, editorial, documentary, cinematic

### Materials
- Glass, metal, wood, fabric, leather, ceramic, marble
- Matte, glossy, textured, smooth, rough, weathered
