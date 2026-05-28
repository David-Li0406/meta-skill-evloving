# Prompt Engineering for Creatives

## Patterns


---
  #### **Name**
The Prompt Architecture Framework
  #### **Description**
Universal structure for prompts across modalities
  #### **When**
Starting any prompt for any AI creative tool
  #### **Example**
    Universal prompt structure:
    
    1. SUBJECT: What is the main focus?
    2. CONTEXT: Environment, setting, situation
    3. STYLE: Aesthetic, genre, reference
    4. TECHNICAL: Quality, format, specifications
    5. MODIFIERS: Adjustments, negatives, constraints
    
    IMAGE example:
    "A cyberpunk street vendor [subject] selling neon-lit fruits
    at night [context], in the style of Blade Runner and Ghost
    in the Shell [style], cinematic lighting, 8K, detailed [technical],
    no text, no watermark [modifiers]"
    
    VIDEO example:
    "Camera slowly pushes in [motion] on a samurai [subject]
    standing in cherry blossom rain [context], Kurosawa style,
    black and white [style], 24fps, film grain [technical]"
    
    AUDIO example:
    "90s trip-hop instrumental [genre] with vinyl crackle [style],
    mellow beats, jazzy piano samples, downtempo [descriptors],
    2 minutes, suitable for background [technical]"
    

---
  #### **Name**
Model-Specific Language Maps
  #### **Description**
Adjust vocabulary for each AI model's training
  #### **When**
Switching between different AI tools
  #### **Example**
    MIDJOURNEY language:
    - Responds to: aesthetic words, artist names, era references
    - Strong words: ethereal, cinematic, trending on artstation
    - Version matters: --v 6 has different responses than --v 5
    
    DALL-E language:
    - Responds to: clear descriptions, concept words
    - Less artistic interpretation, more literal
    - Strong words: "digital art of", "photograph of"
    
    FLUX language:
    - Responds to: specific details, exact descriptions
    - Very prompt-adherent—say exactly what you want
    - Strong words: detailed, high quality, specific poses
    
    STABLE DIFFUSION language:
    - Responds to: LoRA triggers, style tokens
    - Requires negative prompts for quality
    - Strong words: masterpiece, best quality, highly detailed
    
    VEO3/SORA language:
    - Responds to: action words, camera directions
    - Scene descriptions over shot descriptions
    - Strong words: tracking shot, seamless, continuous
    
    Build cheat sheets for each model you use regularly.
    

---
  #### **Name**
The Negative Prompt Strategy
  #### **Description**
Specify what you DON'T want to improve results
  #### **When**
AI outputs have consistent unwanted elements
  #### **Example**
    Common negative prompts by modality:
    
    IMAGE negatives:
    "blurry, low quality, distorted, deformed, watermark, text,
    signature, extra limbs, bad anatomy, worst quality, jpeg
    artifacts, out of frame, cropped, ugly"
    
    VIDEO negatives:
    "static, frozen, glitchy, artifacts, morphing, inconsistent,
    jumpy, unnatural motion, distorted faces"
    
    AUDIO negatives:
    "distorted, clipping, lo-fi, amateur, off-key, noise"
    
    AVATAR negatives:
    "uncanny, robotic, stiff, unnatural expressions, bad lip sync"
    
    Build your negative prompt library from failures.
    When something goes wrong, add it to negatives for next time.
    

---
  #### **Name**
The Iteration Protocol
  #### **Description**
Systematic prompt refinement process
  #### **When**
First generations aren't meeting expectations
  #### **Example**
    ITERATION LOOP:
    
    Step 1: BASELINE
    - Generate with simple prompt
    - Note what works and what doesn't
    - Identify biggest gap from vision
    
    Step 2: ISOLATE
    - Test single changes
    - One element at a time
    - "Does this word change the output?"
    
    Step 3: AMPLIFY
    - Double down on what works
    - Add synonyms of effective terms
    - Increase specificity on working elements
    
    Step 4: SUBTRACT
    - Remove elements that don't affect output
    - Shorter prompts are more controllable
    - Each word should earn its place
    
    Step 5: DOCUMENT
    - Record final prompt
    - Note what specific words accomplish
    - Add to library for future use
    
    RULE: Never iterate randomly. Hypothesis → Test → Learn.
    

---
  #### **Name**
Prompt Library Architecture
  #### **Description**
Build reusable prompt components
  #### **When**
Creating prompts you'll use repeatedly
  #### **Example**
    LIBRARY STRUCTURE:
    
    1. STYLE PREFIXES: Reusable style definitions
       brand_style_v3: "clean minimalist design, soft natural lighting,
       white and light blue color palette, premium product feel, "
    
    2. TECHNICAL SUFFIXES: Quality and format specs
       high_quality_photo: ", professional photography, 8K resolution,
       sharp focus, high detail, color-graded"
    
    3. NEGATIVE TEMPLATES: Anti-pattern collections
       avoid_artifacts: "no blur, no distortion, no watermark, no text"
    
    4. TASK TEMPLATES: Full prompt structures
       product_hero: "{product} on {surface}, {brand_style_v3},
       {high_quality_photo}, {avoid_artifacts}"
    
    USAGE:
    product_hero.format(product="silver watch", surface="marble")
    
    Build once, reuse infinitely. Version as you improve.
    

---
  #### **Name**
Few-Shot for Creative
  #### **Description**
Use examples to guide AI understanding
  #### **When**
Describing something too complex for words
  #### **Example**
    FEW-SHOT TECHNIQUES:
    
    1. REFERENCE IMAGES (where supported):
       - Upload example images
       - "In the style of [uploaded image]"
       - Image weight vs. text weight adjustable
    
    2. ARTIST REFERENCES:
       - "In the style of [Artist Name]"
       - Combine: "Hayao Miyazaki meets Blade Runner"
       - Eras work too: "1970s poster art"
    
    3. EXISTING WORKS:
       - "Like [specific artwork/film/song]"
       - "The cinematography of [Director]"
       - "The sound of [Band] circa [Year]"
    
    4. DESCRIPTION CHAINS:
       - Generate description of reference
       - Use description as prompt
       - Iterate on description
    
    When words fail, examples succeed.
    

## Anti-Patterns


---
  #### **Name**
Prompt Dumping
  #### **Description**
Stuffing every possible keyword into prompts
  #### **Why**
Overwhelming prompts confuse models; signals interfere
  #### **Instead**
Prioritize. Test individual words. Remove non-contributors.

---
  #### **Name**
Copy-Paste Prompting
  #### **Description**
Using prompts without understanding them
  #### **Why**
Context matters; prompts are model and use-case specific
  #### **Instead**
Deconstruct borrowed prompts. Understand each element.

---
  #### **Name**
Model Agnosticism
  #### **Description**
Using same prompt across different models
  #### **Why**
Each model interprets differently; same prompt ≠ same output
  #### **Instead**
Adapt prompts to model. Build model-specific libraries.

---
  #### **Name**
Random Iteration
  #### **Description**
Changing multiple things randomly hoping for improvement
  #### **Why**
Can't learn what works; wastes time; no systematic progress
  #### **Instead**
Change one thing at a time. Document what each change does.

---
  #### **Name**
Ignoring Negatives
  #### **Description**
Only specifying what you want, not what you don't
  #### **Why**
Models add defaults—often unwanted elements
  #### **Instead**
Build comprehensive negative prompts. Update from failures.

---
  #### **Name**
Single-Shot Expectations
  #### **Description**
Expecting perfect results from first prompt
  #### **Why**
AI generation is probabilistic; first try rarely best
  #### **Instead**
Plan for iteration. Generate variations. Select and refine.