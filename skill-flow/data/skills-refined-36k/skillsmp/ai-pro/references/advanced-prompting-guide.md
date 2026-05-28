# Advanced Prompting Guide 2026

*Updated: January 22, 2026 - 15:18*

Mastering image generation in 2026 requires moving beyond simple descriptions to structural and technical prompting.

## 1. The 2026 Prompt Structure

A professional prompt should follow this hierarchy:
1.  **Subject**: The core element (be specific).
2.  **Action/Context**: What is happening and where.
3.  **Composition**: Camera angle, focal length, framing.
4.  **Lighting**: Time of day, light source, intensity.
5.  **Style/Aesthetic**: Artistic movement, film stock, or specific model flags.
6.  **Technical Specs**: Resolution, aspect ratio, model version.

### Example Template:
> `[Subject] [Action] in [Environment]. [Composition] shot, [Lighting]. Style inspired by [Artist/Aesthetic]. --ar [Ratio] --v [Version]`

---

## 2. Technical Keywords for 2026 Models

### Photography & Realism
- `8k native resolution`: Forces the model to use high-density latent spaces.
- `F-stop 1.2`: For deep bokeh and shallow depth of field.
- `Volumetric lighting`: Adds atmosphere and depth.
- `Ray-traced reflections`: For accurate glass and water behavior.

### Illustration & Design
- `Vector flat design`: For modern UI icons.
- `Risograph print style`: For textured, retro illustrations.
- `Isocetric 3D render`: For architectural and UI concepts.
- `Minimalist brutalism`: For bold, high-contrast layouts.

---

## 3. Handling Complex Elements

### Character Consistency (FLUX.2 / SD4)
To maintain consistency, use the **SREF (Style Reference)** or **CREF (Character Reference)** patterns:
- **Seed Locking**: Always use the same seed for variations.
- **Incremental Prompting**: Start with a base character and add accessories in subsequent prompts.
- **Reference URL**: Use `[Image URL] --cref` in compatible models.

### Text Rendering
Models like **FLUX.2 [pro]** and **Ideogram 3** (available via OpenRouter) are optimized for text.
- **Rule**: Wrap text in double quotes.
- **Prompt**: `"A neon sign that says 'GENESIS 2026' in a cyberpunk alleyway."`

---

## 4. Multi-Modal Iteration

In 2026, the best images come from multi-modal feedback loops:
1.  **Generate** a base image.
2.  **Analyze** it with Gemini 3 Pro (Vision).
3.  **Refine** the prompt based on what the vision model saw.
4.  **Inpaint/Edit** specific regions using the `--input` flag in our scripts.

---

## 5. Negative Prompting (The "Avoid" List)

While 2026 models have improved, some still benefit from negative prompts (especially SD4):
- `lowres, bad anatomy, bad hands, text error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, username, blurry.`

---

## 6. Model-Specific Flags (Common)

- `--ar 16:9`: Aspect ratio.
- `--v 8`: Model version (Midjourney).
- `--fast` / `--relax`: Execution speed (Midjourney/Flux).
- `--stylize 250`: Artistic weight.
