# Advanced Prompting Techniques

## Artistic References

Reference specific artists, art movements, or styles to guide output.

**Example:**

```prompt
Create an image in the style of Vincent van Gogh's "Starry Night," but replace the village with a futuristic cityscape. Maintain the swirling, expressive brushstrokes and vibrant color palette of the original, emphasizing deep blues and bright yellows. The city should have tall, glowing skyscrapers that blend seamlessly with the swirling sky.
```

## Blending Concepts

Combine different ideas, themes, or artistic styles.

**Example:**

```prompt
Illustrate "The Last Supper" by Leonardo da Vinci, but reimagine it with robots in a futuristic setting. Maintain the composition and dramatic lighting of the original painting, but replace the apostles with various types of androids and cyborgs. The table should be a long, sleek metal surface with holographic displays. In place of bread and wine, have the robots interfacing with glowing data streams.
```

**Multi-style fusion:**

```prompt
Create an image that fuses the precision of M.C. Escher's impossible geometries with the bold colors and shapes of Wassily Kandinsky's abstract compositions. The subject should be a surreal cityscape where buildings seamlessly transform into musical instruments. Use Escher's techniques to create paradoxical perspectives and interconnected structures, but render them in Kandinsky's vibrant, non-representational style. Incorporate musical notations and abstract shapes that flow through the scene, connecting the architectural elements. The color palette should be rich and varied, with particular emphasis on deep blues, vibrant reds, and golden yellows.
```

## Temporal Narratives

Convey time passing or story unfolding within a single image.

**Example:**

```prompt
Illustrate the life cycle of a monarch butterfly in a single, continuous image. Divide the canvas into four seamlessly blending sections, each representing a stage of the butterfly's life.

Start on the left with a milkweed plant where tiny eggs are visible on the underside of a leaf. As we move right, show the caterpillar stage with the larva feeding on milkweed leaves. In the third section, depict the chrysalis stage, with the green and gold-flecked pupa hanging from a branch.

Finally, on the right side, show the fully formed adult butterfly emerging, with its wings gradually opening to reveal the iconic orange and black pattern. Use a soft, natural color palette dominated by greens and oranges. The background should subtly shift from spring to summer as we move from left to right, with changing foliage and lighting to indicate the passage of time.
```

## Unusual Perspectives

Challenge FLUX.1 with unique viewpoints.

**Bug's-eye view:**

```prompt
Illustrate a "bug's-eye view" of a picnic in a lush garden. The perspective should be from ground level, looking up at towering blades of grass and wildflowers that frame the scene. In the distance, show the underside of a red and white checkered picnic blanket with the silhouettes of picnic foods and human figures visible through the semi-transparent fabric. Include a few ants in the foreground carrying crumbs, and a ladybug climbing a blade of grass. The lighting should be warm and dappled, as if filtering through leaves.
```

## Mood and Atmosphere

Describe emotional tone to generate images with desired feel.

**Cozy/nostalgic:**

```prompt
Depict a cozy, warmly lit bookstore cafe on a rainy evening. The atmosphere should be inviting and nostalgic, with soft yellow lighting from vintage lamps illuminating rows of well-worn books. Show patrons reading in comfortable armchairs, steam rising from their coffee cups. The large front window should reveal a glistening wet street outside, with blurred lights from passing cars. Emphasize the contrast between the warm interior and the cool, rainy exterior.
```

## Dynamic and Active Language

Use verbs and action-oriented descriptions.

**Before:**

```prompt
A mountain peak.
```

**After:**

```prompt
A majestic mountain peak emerging through swirling morning mist, with golden sunrise light catching the crystalline ice formations.
```

## Common Mistakes to Avoid

### Incorrect Syntax

**Don't use:** Stable Diffusion syntax like `(best quality, ultra-detailed)` or `++`

**Use instead:** "Highly detailed and vibrant"

### Overcomplicating

**Don't:** List every tiny detail
**Do:** Focus on essential elements

**Before:**

```prompt
A beautiful sunset with a nice mountain range and some trees and a river and a few birds flying in the sky.
```

**After:**

```prompt
A vibrant orange and pink sunset over a snow-capped mountain range with a calm river in the foreground.
```

### "White Background" Issue

**Avoid:** Using "white background" phrase in FLUX.1 [dev] variant - causes fuzzy outputs

**Note:** This issue only affects [dev], not [schnell]
