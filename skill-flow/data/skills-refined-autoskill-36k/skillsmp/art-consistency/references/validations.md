# Art Consistency - Validations

## Generation Without Character Bible

### **Id**
missing-character-bible
### **Severity**
error
### **Type**
workflow
### **Condition**
generating character without documented reference
### **Message**
Attempting to generate character without a character bible. Consistency impossible.
### **Fix Action**
  Create character bible FIRST with:
  - Identity anchors (face, hair, body, outfit, accessories)
  - Style descriptors (art style, color palette, lighting)
  - Prompt template with exact wording
  - Reference images (turnaround sheet if possible)
  

## Generation Without Reference Image

### **Id**
missing-reference-image
### **Severity**
error
### **Type**
workflow
### **Condition**
generating established character without reference loaded
### **Message**
Generating established character without reference image. Drift guaranteed.
### **Fix Action**
  Load reference image before generation:
  - Upload turnaround sheet or approved previous image
  - Use IP-Adapter or image-to-image with reference
  - Or use trained LoRA with trigger word
  

## Vague Identity Descriptors

### **Id**
vague-prompt-identity
### **Severity**
warning
### **Type**
prompt_analysis
### **Pattern**
  - (?i)pretty (?:girl|woman|boy|man)
  - (?i)beautiful (?:girl|woman|boy|man)
  - (?i)cute (?:girl|woman|boy|man)
  - (?i)anime (?:girl|woman|boy|man|character)
  - (?i)(?:generic|normal|regular) (?:looking|appearance)
### **Message**
Prompt uses vague identity descriptors. Will produce inconsistent results.
### **Fix Action**
  Replace vague descriptors with SPECIFIC identity anchors:
  BAD: "pretty anime girl with blue hair"
  GOOD: "heart-shaped face, large sapphire blue eyes, small nose,
         sky blue twin-tails shoulder-length with ribbon clips"
  

## Vague Style Descriptors

### **Id**
vague-style-descriptor
### **Severity**
warning
### **Type**
prompt_analysis
### **Pattern**
  - (?i)^anime style$
  - (?i)^anime$
  - (?i)cartoon style
  - (?i)realistic style
  - (?i)artistic style
### **Message**
Prompt uses vague style descriptors. Art style will drift between generations.
### **Fix Action**
  Specify EXACT style characteristics:
  BAD: "anime style"
  GOOD: "90s anime cel-shading, bold black outlines,
         hard shadows, saturated colors, Studio Ghibli influence"
  

## Color Without Specification

### **Id**
color-without-specification
### **Severity**
warning
### **Type**
prompt_analysis
### **Pattern**
  - (?i)(?:blue|red|green|purple|silver|gold|pink) (?:hair|eyes|outfit|dress)
### **Message**
Color mentioned without specific shade. Colors will vary between generations.
### **Fix Action**
  Use specific color descriptors or hex codes in documentation:
  BAD: "blue eyes"
  GOOD: "deep sapphire blue eyes" or "eyes #1E90FF"
  
  Document exact color in character bible for reference.
  

## Synonym Usage Across Prompts

### **Id**
synonym-drift-risk
### **Severity**
warning
### **Type**
prompt_comparison
### **Description**
Detecting when same feature described with different words
### **Examples**
  - silver hair vs gray hair vs platinum hair vs white hair
  - twin-tails vs pigtails vs twintails
  - sailor uniform vs school uniform vs seifuku
### **Message**
Different words for same feature detected. Pick ONE term and use consistently.
### **Fix Action**
  Document canonical term in character bible.
  Use ONLY that term in all prompts.
  Never substitute synonyms.
  

## Facial Feature Drift

### **Id**
face-drift-check
### **Severity**
error
### **Type**
visual_comparison
### **Checks**
  - Eye color matches reference
  - Eye shape matches reference
  - Face shape matches reference (round, oval, heart, square)
  - Nose shape matches reference
### **Message**
Facial features do not match reference. Character identity compromised.
### **Fix Action**
  Do NOT approve. Regenerate with:
  - Stronger reference image influence (increase IP-Adapter strength)
  - More specific facial feature description in prompt
  - Different seed if pattern persists
  

## Hair Style/Color Drift

### **Id**
hair-drift-check
### **Severity**
error
### **Type**
visual_comparison
### **Checks**
  - Hair color exact match (compare in neutral lighting)
  - Hair style matches (ponytail vs twintails vs bob)
  - Hair length consistent
  - Hair accessories present and correct
### **Message**
Hair does not match reference. Visible consistency break.
### **Fix Action**
  Do NOT approve. Regenerate with:
  - Explicit hair description in prompt
  - Hair color in specific terms (not just "blue")
  - Accessories explicitly mentioned
  

## Outfit/Clothing Drift

### **Id**
outfit-drift-check
### **Severity**
error
### **Type**
visual_comparison
### **Checks**
  - All clothing items present
  - Clothing colors match
  - Clothing details preserved (trim, patterns, buttons)
  - Accessories present (jewelry, gloves, belts)
### **Message**
Outfit does not match reference. Character consistency broken.
### **Fix Action**
  Do NOT approve. Regenerate with:
  - Complete outfit description in prompt
  - Each accessory explicitly mentioned
  - Color specifications for each item
  

## Art Style Drift

### **Id**
style-drift-check
### **Severity**
warning
### **Type**
visual_comparison
### **Checks**
  - Art style matches series (anime vs realistic vs cartoon)
  - Line weight consistent with series
  - Shading style matches (cel-shaded vs soft gradient)
  - Color saturation appropriate
### **Message**
Art style drifting from series aesthetic.
### **Fix Action**
  Compare to series reference images.
  If drift detected:
  - Reinforce style descriptors in prompt
  - Use style reference image
  - Consider different model if style incompatible
  

## Quality Issues

### **Id**
quality-gate
### **Severity**
error
### **Type**
quality_check
### **Checks**
  - No visible artifacts or glitches
  - Hands rendered correctly (count: 5 fingers per hand)
  - No floating or disconnected elements
  - Anatomy physically possible
  - Face not distorted
### **Message**
Quality issues detected. Cannot approve for delivery.
### **Fix Action**
  Do NOT approve. Either:
  - Regenerate with different seed
  - Use inpainting to fix specific issues
  - Adjust prompt if issue is systematic
  

## Cross-Image Consistency Check

### **Id**
cross-image-consistency
### **Severity**
warning
### **Type**
series_comparison
### **Checks**
  - Character proportions consistent across images
  - Head-to-body ratio maintained
  - Art style consistent across series
  - Color palette consistent (check same colors in different images)
### **Message**
Inconsistency detected across series images.
### **Fix Action**
  Review all series images together.
  Identify the drift point.
  Regenerate divergent images with stronger reference.
  Consider retraining LoRA if drift is systematic.
  

## Multi-Character Scene Consistency

### **Id**
multi-character-consistency
### **Severity**
warning
### **Type**
scene_validation
### **Checks**
  - Each character matches their individual reference
  - Relative heights/proportions correct
  - Art style uniform across all characters
  - No style mixing between characters
### **Message**
Multi-character scene has consistency issues.
### **Fix Action**
  For multi-character scenes:
  - Generate characters separately if possible
  - Use composite/layering approach
  - Verify each character against their bible
  - Check relative proportions against size chart
  