# Art Consistency - Sharp Edges

## Gradual Face Drift

### **Id**
gradual-face-drift
### **Summary**
Character face slowly morphs across a series until unrecognizable
### **Severity**
critical
### **Situation**
Generating many images of same character over time without strict reference
### **Why**
  Each generation interprets the prompt slightly differently. Without a reference
  anchor, these small variations accumulate. By image 20, the character's face
  has drifted significantly from image 1. The human eye adapts to gradual change,
  so you don't notice until comparing first and last images side-by-side.
  
  This is the #1 consistency failure in AI art production.
  
### **Solution**
  PREVENTION:
  1. Create a "golden reference" portrait early and ALWAYS use it
  2. Use IP-Adapter with face reference at 0.7+ strength
  3. Or train a LoRA specifically for the character's face
  
  DETECTION:
  Compare every 5th image against the original reference.
  If drift is visible, you've already lost consistency.
  
  RECOVERY:
  Once drift has occurred, you cannot "correct back" gradually.
  You must either:
  - Regenerate all drifted images from scratch with reference
  - Accept two different "eras" of the character
  
### **Symptoms**
  - First and last image of series look like different characters
  - Eye shape gradually changes
  - Face shape rounds or sharpens over time
  - Commenters ask "is this the same character?"

## Hair Color Shift

### **Id**
hair-color-shift
### **Summary**
Hair color changes subtly between images, especially in different lighting
### **Severity**
high
### **Situation**
Character's hair appears different colors in various scenes
### **Why**
  "Blue hair" can mean navy, sky blue, teal, or cyan depending on model interpretation.
  Lighting affects perceived color - same blue looks purple in warm light.
  AI models don't have color constancy the way human perception does.
  Without explicit anchoring, each generation picks a slightly different blue.
  
### **Solution**
  PREVENTION:
  1. Use SPECIFIC color names: "sky blue" not "blue"
  2. Document exact hex code in character bible: "#87CEEB"
  3. Include lighting-neutral reference in every generation
  4. Specify "consistent hair color" in prompt for multi-character scenes
  
  LIGHTING ADJUSTMENT:
  If scene has warm lighting, you may need to compensate:
  "sky blue hair (not purple, maintain blue even in warm light)"
  
  BAD: "blue hair"
  GOOD: "sky blue hair #87CEEB, maintaining consistent blue hue"
  
### **Symptoms**
  - Hair looks blue in one image, purple in another
  - Indoor scenes shift hair toward amber/brown
  - Users comment on "hair color change"

## Outfit Detail Loss

### **Id**
outfit-detail-loss
### **Summary**
Character loses outfit details over generations - buttons disappear, trim vanishes
### **Severity**
high
### **Situation**
Complex outfits simplify over time, losing distinctive features
### **Why**
  AI models have limited "attention budget." Complex outfits with many details
  compete for attention with face, pose, and background. Small details like
  buttons, trim, patterns, and accessories get dropped when other elements
  are prioritized. The model "remembers" the general outfit but forgets specifics.
  
### **Solution**
  PREVENTION:
  1. List EVERY outfit element explicitly in prompt:
     "black sailor uniform with gold buttons, purple trim on collar and sleeves,
     crescent moon brooch on chest, fingerless black gloves"
  2. Increase outfit detail weight if using prompt weighting: (gold buttons:1.3)
  3. Use reference image with clear outfit visibility
  
  FOR COMPLEX OUTFITS:
  Generate outfit-focused images first (neutral pose, clear view of all details)
  Use these as reference for action shots
  
  NEVER: Assume the model will "remember" small details from previous images
  
### **Symptoms**
  - Buttons disappear in dynamic poses
  - Trim color changes or vanishes
  - Accessories (brooches, belts, jewelry) missing
  - Pattern complexity reduces (plaid becomes solid)

## Style Era Mixing

### **Id**
style-era-mixing
### **Summary**
Different art eras or styles accidentally mix in same series
### **Severity**
high
### **Situation**
"Anime" produces mix of 90s, 2000s, and modern anime aesthetics
### **Why**
  "Anime style" encompasses 50+ years of evolving aesthetics. 90s anime has
  distinct features (large eyes, angular faces, cel-shading) vs 2020s anime
  (softer features, gradient shading, different proportions). Without specific
  era/style anchoring, each generation may pick different influences.
  
### **Solution**
  PREVENTION:
  Be SPECIFIC about art style era and influences:
  
  BAD: "anime style"
  
  GOOD: "2020s anime style, soft cel-shading, rounded features, smooth gradients,
        influenced by Makoto Shinkai films, vibrant saturated colors"
  
  OR: "1990s anime style, sharp angular features, bold black outlines,
       hard cel-shading, Neon Genesis Evangelion aesthetic"
  
  STYLE REFERENCE:
  Use --sref (Midjourney) or style reference image to lock in specific aesthetic.
  Reference a SPECIFIC anime/artist, not general "anime."
  
### **Symptoms**
  - Some images look "90s anime," others look "modern isekai"
  - Line weight varies dramatically between images
  - Shading style inconsistent (hard vs soft)
  - Color palette saturation varies

## Proportion Instability

### **Id**
proportion-instability
### **Summary**
Character height, body proportions, head size varies between images
### **Severity**
high
### **Situation**
Same character looks taller/shorter or has different body type across series
### **Why**
  Without explicit proportion anchoring, models interpret descriptions differently.
  "Petite" might mean 145cm in one generation and 160cm in another.
  Camera angle changes compound this - low angle makes characters look taller.
  Head-to-body ratio (important for anime style) drifts without explicit control.
  
### **Solution**
  PREVENTION:
  1. Specify EXACT proportions in character bible:
     "petite build, 152cm, 5.5 head-to-body ratio (chibi-influenced proportions)"
  
  2. Create size comparison reference if multiple characters:
     Generate image with all characters at neutral pose showing relative heights
  
  3. For consistent head size, specify:
     "large head proportions typical of anime, 1:5 head to body ratio"
  
  CAMERA ANGLE COMPENSATION:
  Low angle shots will make character appear taller.
  Note expected appearance in different camera angles.
  
### **Symptoms**
  - Character looks tall in one image, short in another
  - Head size varies (larger in some, smaller in others)
  - Body type seems to change (slender vs athletic)
  - Multi-character scenes show wrong relative heights

## Seed Dependency Trap

### **Id**
seed-dependency-trap
### **Summary**
Relying on seed to maintain consistency, then model update breaks everything
### **Severity**
high
### **Situation**
Same prompt + seed produces different results after model version change
### **Why**
  Seeds only ensure reproducibility within the SAME model version.
  When Flux, Midjourney, or Stable Diffusion updates, seed behavior changes.
  Your carefully curated seeds become useless overnight.
  All consistency work based on "I found a good seed" is fragile.
  
### **Solution**
  PREVENTION:
  Seeds are SUPPLEMENTARY, not primary consistency method.
  Primary consistency must come from:
  - Character bible with explicit descriptions
  - Reference images (turnaround sheets)
  - Trained LoRA (survives model updates if retrained)
  
  SEED USAGE:
  Use seeds for short-term iteration within a session.
  Don't rely on seeds for long-term series consistency.
  Always maintain reference images that are model-independent.
  
  WHEN MODEL UPDATES:
  - Your LoRAs need retraining
  - Test all prompts against references
  - Seeds will produce different results (expected)
  - Reference images remain valid (use for comparison)
  
### **Symptoms**
  - My prompt stopped working after the update
  - Same seed produces visibly different character
  - Entire series becomes inconsistent with new images

## Close Enough Cascade

### **Id**
close-enough-cascade
### **Summary**
Accepting small inconsistencies that compound into major problems
### **Severity**
critical
### **Situation**
Approving images with minor issues to save time, creating consistency debt
### **Why**
  "The eyes are slightly different but it's fine" - approved.
  Next image, eyes drift a bit more - "still fine."
  By image 10, the eyes are completely different from image 1.
  Each "close enough" approval shifts the baseline, accelerating drift.
  
  This is consistency DEBT - and like technical debt, it compounds with interest.
  
### **Solution**
  THE HARD RULE:
  If it doesn't match the reference, it doesn't ship.
  Regenerating takes 30 seconds. Fixing a series takes hours.
  
  PRACTICAL APPROACH:
  1. First few images: Be EXTREMELY strict. Establish baseline.
  2. Have reference open side-by-side during every QA.
  3. If you're saying "close enough," you're already drifting.
  
  TIME MATH:
  - Regenerate now: 30 seconds
  - Fix 20 drifted images later: 10+ minutes each
  - Redo entire series: Hours
  - Explain to client why character changed: Priceless (and painful)
  
  STOPPING CRITERION:
  If the same issue appears 3+ times, it's not bad luck - your prompt needs fixing.
  Stop generating and fix the system.
  
### **Symptoms**
  - Internal voice says "it's fine, nobody will notice"
  - Comparing to previous approved image instead of original reference
  - QA checklist has "close enough" notes
  - Series quality degrades over time

## Multi Character Chaos

### **Id**
multi-character-chaos
### **Summary**
Multi-character scenes blend features between characters
### **Severity**
high
### **Situation**
Character A gets Character B's eyes, or styles merge
### **Why**
  When generating multiple characters in one image, models struggle to keep
  distinct features separate. Prompt attention is divided. Characters in
  proximity may "blend" features - eyes, hair color, or style elements swap.
  The more similar the characters, the worse the blending.
  
### **Solution**
  PREVENTION:
  1. Make characters MAXIMALLY distinct:
     - Different hair colors AND styles
     - Contrasting outfits (not both in school uniforms)
     - Varied heights/builds
  
  2. Position distinctly in prompt:
     "(left: Luna, silver twintails, blue eyes) and (right: Kai, black spiky hair, green eyes)"
  
  3. Use character-specific LoRAs if available
  
  ALTERNATIVE APPROACH:
  Generate characters separately, composite in post-processing.
  This guarantees each character matches their reference.
  
  VERIFICATION:
  Check EACH character against THEIR individual reference.
  It's not enough that "the image looks good."
  
### **Symptoms**
  - Character A has Character B's eye color
  - Hair styles partially merge
  - One character's outfit elements appear on another
  - Characters look more similar than they should

## Lora Overtraining

### **Id**
lora-overtraining
### **Summary**
LoRA trained too long becomes rigid, can't handle new poses/expressions
### **Severity**
medium
### **Situation**
Character LoRA only produces one expression/pose, ignoring prompt
### **Why**
  Overfit LoRA has "memorized" training images rather than learning the character.
  It defaults to the most common pose/expression in training data.
  Prompt instructions for new poses are ignored or weakly applied.
  The character looks correct but can't act.
  
### **Solution**
  PREVENTION (during training):
  - Use 15-30 diverse images (multiple poses, expressions, angles)
  - Don't overtrain (watch validation loss)
  - Include variety in training set:
    * Front, 3/4, side, back views
    * Multiple expressions (neutral, happy, sad, angry)
    * Different poses (standing, sitting, action)
  
  DETECTION:
  Test LoRA with unusual prompts:
  "character crying" - does it change expression?
  "character jumping" - does it change pose?
  If it stays static, LoRA is overfit.
  
  RECOVERY:
  Retrain with more diverse dataset and shorter training.
  Lower LoRA weight (0.6-0.8) to allow more prompt influence.
  
### **Symptoms**
  - Character always has same expression regardless of prompt
  - Pose doesn't change even when explicitly requested
  - "Smiling" prompt still produces neutral face
  - LoRA "overpowers" other prompt elements

## Ip Adapter Identity Leak

### **Id**
ip-adapter-identity-leak
### **Summary**
IP-Adapter bleeds reference identity into wrong elements
### **Severity**
medium
### **Situation**
Background elements or other characters take on reference's features
### **Why**
  IP-Adapter doesn't perfectly isolate the target subject. At high strength,
  it can influence the entire image. Background elements may take on color
  schemes from the reference. Other characters may inherit facial features.
  The reference "leaks" beyond its intended scope.
  
### **Solution**
  PREVENTION:
  1. Use moderate strength: 0.5-0.7 for most cases
  2. Use face-specific IP-Adapter variants when available
  3. Mask the target region if possible
  4. For multi-character: Generate separately and composite
  
  DETECTION:
  Check non-character elements:
  - Does background have unexpected colors?
  - Do other characters share features with reference?
  - Are objects styled like the character?
  
  MITIGATION:
  Lower IP-Adapter strength until leak stops.
  Trade-off: lower strength = less character consistency.
  Find the minimum strength that maintains identity.
  
### **Symptoms**
  - Background takes on reference character's color scheme
  - Other characters look like reference
  - Objects styled to match character aesthetic
  - Everything looks like [character]

## Video Frame Drift

### **Id**
video-frame-drift
### **Summary**
Character changes appearance mid-video despite consistent prompts
### **Severity**
critical
### **Situation**
AI-generated video shows character morphing during playback
### **Why**
  Video generation processes frames with some independence.
  Each frame has small variations that accumulate into visible morphing.
  Fast motion and scene changes increase drift likelihood.
  Current video models have less consistency than image models.
  
### **Solution**
  PREVENTION:
  1. Use models with explicit temporal consistency (some video models have this)
  2. Reduce video length - shorter clips = less drift
  3. Avoid rapid motion that requires major frame-to-frame changes
  4. Use image-to-video with strong reference image
  
  KEYFRAME APPROACH:
  1. Generate keyframes as still images (use full consistency workflow)
  2. QA each keyframe against references
  3. Use interpolation/video model only for between-frames
  4. This anchors the video to verified-consistent keyframes
  
  POST-PROCESSING:
  If drift occurs, may need to regenerate segments.
  Inpainting video frames is possible but tedious.
  
### **Symptoms**
  - Face morphs during video
  - Hair color shifts mid-scene
  - Outfit changes between cuts
  - "Uncanny valley" feeling from subtle shifting