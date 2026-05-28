# Product Photography Workflow

Generate professional commercial product images for advertising and e-commerce.

## Quick Start

```bash
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "[PRODUCT PROMPT]" \
  --size 2K \
  --aspect-ratio 1:1 \
  --output ~/Downloads/product.png
```

---

## Product Shot Types

### Hero Shot (White Background)

**Template:**
```
Professional commercial product photography,
[PRODUCT] as hero shot,
floating at slight dynamic angle on pure white seamless background,
soft studio lighting creating subtle shadow underneath,
every detail crisp and visible,
shot on medium format Hasselblad with macro lens,
photorealistic, ultra detailed, e-commerce advertising quality
```

**Example:**
```
Professional commercial product photography,
premium wireless over-ear headphones in matte black as hero shot,
floating at slight dynamic angle on pure white seamless background,
soft studio lighting creating subtle shadow underneath,
every detail crisp and visible including leather texture on earcups,
shot on medium format Hasselblad with macro lens,
photorealistic, ultra detailed, e-commerce advertising quality
```

### Lifestyle Context

**Template:**
```
Lifestyle product photography, [PRODUCT] in natural context,
being [USED/HELD/WORN] by [PERSON DESCRIPTION] in [ENVIRONMENT],
authentic candid moment, natural lighting,
product in sharp focus, shallow DOF on surroundings,
aspirational lifestyle setting,
photorealistic, ultra detailed, brand advertising quality
```

### Detail/Macro

**Template:**
```
Macro product photography, extreme close-up of [PRODUCT],
showcasing [SPECIFIC FEATURE/TEXTURE/DETAIL],
dramatic side lighting revealing surface quality,
[MATERIAL PROPERTIES: brushed metal, leather grain, fabric weave],
focus stacked for complete sharpness,
shot on 100mm macro lens,
photorealistic, ultra detailed, 8K resolution
```

### Flat Lay/Knolling

**Template:**
```
Professional flat lay product photography,
[PRODUCT] arranged with [COMPLEMENTARY ITEMS] on [SURFACE],
perfectly organized knolling arrangement,
shot directly from above, even lighting,
clean minimalist composition,
shot on medium format camera,
photorealistic, ultra detailed, editorial quality
```

### In Packaging

**Template:**
```
Product packaging photography, [PRODUCT] in premium packaging,
[PACKAGING DESCRIPTION: box, case, sleeve],
partially revealed showing product inside,
luxury unboxing presentation,
studio lighting highlighting packaging materials,
photorealistic, ultra detailed, retail advertising quality
```

---

## Product Categories

### Electronics

```
Product photography, [DEVICE: smartphone, laptop, watch],
sleek modern design, [COLOR/MATERIAL],
screen displaying [CONTENT] at perfect viewing angle,
studio lighting with subtle reflections,
floating with soft shadow on gradient background,
photorealistic, ultra detailed, Apple-style advertising
```

### Beauty/Cosmetics

```
Luxury cosmetics photography, [PRODUCT: lipstick, serum, perfume],
elegant glass/metal packaging catching light,
soft romantic lighting with subtle reflections,
[COMPLEMENTARY ELEMENTS: flowers, fabric, drops],
aspirational beauty aesthetic,
photorealistic, ultra detailed, beauty campaign quality
```

### Food & Beverage

```
Professional food photography, [DISH/DRINK],
[PLATING/PRESENTATION STYLE],
[GARNISHES AND PROPS],
dramatic lighting creating texture and depth,
steam/condensation for freshness (if applicable),
shot on medium format, 80mm f/4,
photorealistic, ultra detailed, restaurant menu quality
```

### Fashion/Apparel

```
Fashion product photography, [CLOTHING ITEM],
displayed on [MANNEQUIN/HANGER/FLAT LAY],
showing [KEY DETAILS: stitching, fabric texture, cut],
clean studio lighting,
professional e-commerce presentation,
photorealistic, ultra detailed, luxury retail quality
```

### Jewelry/Watches

```
Luxury jewelry photography, [PIECE: watch, ring, necklace],
macro detail showing [CRAFTSMANSHIP DETAILS],
dramatic lighting creating sparkle and reflections,
rich dark background for contrast,
focus stacked for complete sharpness,
photorealistic, ultra detailed, luxury brand advertising
```

---

## Lighting Setups

### Soft Box Setup
Clean, even lighting for most products:
```
soft box studio lighting, diffused key light,
subtle fill, clean professional look
```

### Dramatic/Moody
For luxury and premium feel:
```
dramatic single-source lighting, deep shadows,
highlighting product form and texture
```

### Backlit/Rim Light
For transparent products or silhouettes:
```
backlit product photography, rim lighting,
creating glowing halo effect around edges
```

### Light Painting
For complex reflective surfaces:
```
light-painted product photography,
multiple exposures combined for perfect reflections
```

---

## Background Options

| Background | Effect | Products |
|------------|--------|----------|
| Pure white | Clean, e-commerce | All |
| Gradient grey | Professional | Tech, luxury |
| Black | Premium, dramatic | Jewelry, watches |
| Colored | Brand identity | Lifestyle |
| Textured (marble, wood) | Lifestyle, editorial | Beauty, food |
| Environmental | Context, story | Lifestyle |

---

## Aspect Ratios

| Ratio | Use | Command |
|-------|-----|---------|
| 1:1 | E-commerce, social | `--aspect-ratio 1:1` |
| 4:3 | Standard product | `--aspect-ratio 4:3` |
| 3:4 | Tall products | `--aspect-ratio 3:4` |
| 16:9 | Banner, hero | `--aspect-ratio 16:9` |

---

## Common Issues

| Problem | Solution |
|---------|----------|
| Reflections wrong | Specify "controlled studio reflections" |
| Product floating oddly | Add "subtle shadow grounding product" |
| Wrong scale | Include size reference or specify dimensions |
| Material looks wrong | Describe material properties in detail |
| Too busy | Specify "clean minimal composition" |
