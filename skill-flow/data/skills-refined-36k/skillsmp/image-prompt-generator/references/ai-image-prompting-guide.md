# AI Image Generation Prompting Guide

A condensed reference for professional asset production using modern AI image models.

---

## Golden Rules of Prompting

### 1. Edit, Don't Re-roll
If an image is 80% correct, don't regenerate from scratch. Request specific changes conversationally.

**Example:** "That's great, but change the lighting to sunset and make the text neon blue."

### 2. Use Natural Language & Full Sentences
Brief the model like a human artist. Use proper grammar and descriptive adjectives.

| ❌ Bad | ✅ Good |
|--------|---------|
| "Cool car, neon, city, night, 8k" | "A cinematic wide shot of a futuristic sports car speeding through a rainy Tokyo street at night. The neon signs reflect off the wet pavement and the car's metallic chassis." |

### 3. Be Specific and Descriptive

- **Subject:** Instead of "a woman," say "a sophisticated elderly woman wearing a vintage chanel-style suit"
- **Materiality:** Describe textures—"matte finish," "brushed steel," "soft velvet," "crumpled paper"
- **Setting:** Define location, time of day, weather
- **Lighting:** Specify mood and light source
- **Mood:** Emotional tone of the image

### 4. Provide Context (The "Why" or "For Whom")
Context helps the model make logical artistic decisions.

**Example:** "Create an image of a sandwich for a Brazilian high-end gourmet cookbook."
*(Model infers: professional plating, shallow depth of field, perfect lighting)*

---

## Capability Reference

### Text Rendering & Infographics

**Best Practices:**
- Use "compress" for dense text/PDFs into visual aids
- Specify style: "polished editorial," "technical diagram," or "hand-drawn whiteboard"
- Put exact text in quotes

**Example Prompts:**

```
Earnings Report Infographic:
"Generate a clean, modern infographic summarizing the key financial highlights from this earnings report. Include charts for 'Revenue Growth' and 'Net Income', and highlight the CEO's key quote in a stylized pull-quote box."
```

```
Retro Infographic:
"Make a retro, 1950s-style infographic about the history of the American diner. Include distinct sections for 'The Food,' 'The Jukebox,' and 'The Decor.' Ensure all text is legible and stylized to match the period."
```

```
Technical Diagram:
"Create an orthographic blueprint that describes this building in plan, elevation, and section. Label the 'North Elevation' and 'Main Entrance' clearly in technical architectural font. Format 16:9."
```

```
Whiteboard Summary:
"Summarize the concept of 'Transformer Neural Network Architecture' as a hand-drawn whiteboard diagram suitable for a university lecture. Use different colored markers for the Encoder and Decoder blocks, and include legible labels for 'Self-Attention' and 'Feed Forward'."
```

---

### Character Consistency & Thumbnails

**Best Practices:**
- **Identity Locking:** State "Keep the person's facial features exactly the same as Image 1"
- Describe expression/action changes while maintaining identity
- Combine subjects with bold graphics and text in a single pass

**Example Prompts:**

```
Viral Thumbnail:
"Design a viral video thumbnail using the person from Image 1. 
Face Consistency: Keep the person's facial features exactly the same as Image 1, but change their expression to look excited and surprised. 
Action: Pose the person on the left side, pointing their finger towards the right side of the frame. 
Subject: On the right side, place a high-quality image of a delicious avocado toast. 
Graphics: Add a bold yellow arrow connecting the person's finger to the toast. 
Text: Overlay massive, pop-style text in the middle: 'Done in 3 mins!'. Use a thick white outline and drop shadow. 
Background: A blurred, bright kitchen background. High saturation and contrast."
```

```
Group Character Story:
"Create a funny 10-part story with these 3 fluffy friends going on a tropical vacation. The story is thrilling throughout with emotional highs and lows and ends in a happy moment. Keep the attire and identity consistent for all 3 characters, but their expressions and angles should vary throughout all 10 images."
```

```
Brand Asset Generation:
"Create 9 stunning fashion shots as if they're from an award-winning fashion editorial. Use this reference as the brand style but add nuance and variety to the range so they convey a professional design touch. Please generate nine images, one at a time."
```

---

### Advanced Editing & Restoration

**Best Practices:**
- Use semantic instructions (no manual masking needed)
- Describe changes naturally
- Test physics understanding with complex requests

**Example Prompts:**

```
Object Removal:
"Remove the tourists from the background of this photo and fill the space with logical textures (cobblestones and storefronts) that match the surrounding environment."
```

```
Colorization:
"Colorize this manga panel. Use a vibrant anime style palette. Ensure the lighting effects on the energy beams are glowing neon blue and the character's outfit is consistent with their official colors."
```

```
Localization:
"Take this concept and localize it to a Tokyo setting, including translating the tagline into Japanese. Change the background to a bustling Shibuya street at night."
```

```
Seasonal Control:
"Turn this scene into winter time. Keep the house architecture exactly the same, but add snow to the roof and yard, and change the lighting to a cold, overcast afternoon."
```

---

### Dimensional Translation (2D ↔ 3D)

**Example Prompts:**

```
Floor Plan to Interior Design:
"Based on the uploaded 2D floor plan, generate a professional interior design presentation board in a single image. 
Layout: A collage with one large main image at the top (wide-angle perspective of the living area), and three smaller images below (Master Bedroom, Home Office, and a 3D top-down floor plan). 
Style: Apply a Modern Minimalist style with warm oak wood flooring and off-white walls across ALL images. 
Quality: Photorealistic rendering, soft natural lighting."
```

```
2D to 3D Meme:
"Turn the 'This is Fine' dog meme into a photorealistic 3D render. Keep the composition identical but make the dog look like a plush toy and the fire look like realistic flames."
```

---

### High-Resolution & Textures

**Best Practices:**
- Explicitly request resolution (2K or 4K)
- Describe high-fidelity details (imperfections, surface textures)

**Example Prompts:**

```
4K Texture:
"Harness native high-fidelity output to craft a breathtaking, atmospheric environment of a mossy forest floor. Command complex lighting effects and delicate textures, ensuring every strand of moss and beam of light is rendered in pixel-perfect resolution suitable for a 4K wallpaper."
```

```
Deconstructed Product:
"Create a hyper-realistic infographic of a gourmet cheeseburger, deconstructed to show the texture of the toasted brioche bun, the seared crust of the patty, and the glistening melt of the cheese. Label each layer with its flavor profile."
```

---

### Storyboarding & Sequential Art

**Example Prompt:**

```
Commercial Storyboard:
"Create an addictively intriguing 9-part story with 9 images featuring a woman and man in an award-winning luxury luggage commercial. The story should have emotional highs and lows, ending on an elegant shot of the woman with the logo. The identity of the woman and man and their attire must stay consistent throughout but they can and should be seen from different angles and distances. Please generate images one at a time. Make sure every image is in a 16:9 landscape format."
```

---

### Structural Control & Layout

**Best Practices:**
- Upload sketches to define text/object placement
- Use wireframes for UI mockups
- Use grids for tile-based or pixel art generation

**Example Prompts:**

```
Sketch to Ad:
"Create an ad for a [product] following this sketch."
```

```
Wireframe to UI:
"Create a mock-up for a [product] following these guidelines."
```

```
Pixel Art:
"Generate a pixel art sprite of a unicorn that fits perfectly into this 64x64 grid image. Use high contrast colors."
```

```
Sprite Sheet:
"Sprite sheet of a woman doing a backflip on a drone, 3x3 grid, sequence, frame by frame animation, square aspect ratio. Follow the structure of the attached reference image exactly."
```

---

## Prompt Structure Template

```
[SUBJECT]: Detailed description of main subject with specific attributes
[SETTING]: Location, environment, time of day
[LIGHTING]: Light source, mood, shadows
[STYLE]: Artistic style, medium, reference
[COMPOSITION]: Camera angle, framing, aspect ratio
[DETAILS]: Textures, materials, specific elements
[CONTEXT]: Purpose, audience, use case
[FORMAT]: Resolution, dimensions if needed
```

---

## Quick Reference: Prompt Modifiers

| Category | Examples |
|----------|----------|
| **Lighting** | golden hour, dramatic shadows, soft diffused light, neon glow, overcast |
| **Style** | cinematic, editorial, technical diagram, hand-drawn, photorealistic |
| **Texture** | matte finish, brushed steel, soft velvet, crumpled paper, weathered wood |
| **Composition** | wide shot, close-up, bird's eye view, dutch angle, symmetrical |
| **Mood** | energetic, serene, dramatic, playful, sophisticated |
| **Quality** | 4K, high-fidelity, pixel-perfect, professional grade |
