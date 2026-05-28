# Art Consistency & Visual QA

## Patterns


---
  #### **Name**
Character Bible First
  #### **Description**
Create a comprehensive character documentation before any generation
  #### **When**
Starting work on a new character, beginning a series, or character lacks documentation
  #### **Example**
    CHARACTER BIBLE: Luna Silverfall
    ================================
    
    IDENTITY ANCHORS (use EXACT words every time):
    - Face: "heart-shaped face, large violet eyes, small upturned nose"
    - Hair: "silver twin-tails, waist-length, star-shaped hair clips"
    - Body: "petite build, 155cm, slender frame"
    - Outfit: "black sailor uniform with purple trim, knee-high boots"
    - Accessories: "crescent moon pendant, fingerless black gloves"
    
    STYLE DESCRIPTORS:
    - Art Style: "2D anime, cel-shaded, clean linework, soft shadows"
    - Color Palette: #7B68EE (violet), #C0C0C0 (silver), #000000, #FFD700
    - Lighting: "soft anime lighting, subtle rim light"
    
    PROMPT TEMPLATE:
    "Luna Silverfall, heart-shaped face, large violet eyes, silver twin-tails
    with star clips, black sailor uniform with purple trim, [ACTION], [SETTING],
    2D anime style, cel-shaded, soft anime lighting"
    
    REFERENCE IMAGES: [turnaround sheet link]
    

---
  #### **Name**
Turnaround Sheet Generation
  #### **Description**
Generate multi-view reference sheet before any other images
  #### **When**
New character without references, or existing character needs standardization
  #### **Example**
    TURNAROUND SHEET PROMPT:
    "character design sheet, multiple views, front view, side view,
    back view, 3/4 view, [CHARACTER DESCRIPTION],
    white background, consistent lighting, reference sheet layout,
    same character all views, anime style"
    
    OUTPUT: 4-6 views showing character from different angles
    USE: As reference for all future generations of this character
    

---
  #### **Name**
Pre-Generation Validation
  #### **Description**
Check all consistency requirements before generating
  #### **When**
Every single generation - no exceptions
  #### **Example**
    PRE-GENERATION CHECKLIST:
    [ ] Character bible exists and is loaded
    [ ] Prompt includes ALL identity anchors (exact wording)
    [ ] Style descriptors match series aesthetic
    [ ] Reference image available (turnaround or previous approved image)
    [ ] Color palette specified or implied in prompt
    [ ] Seed locked if continuing from previous generation
    [ ] Model appropriate for style (Flux for realism, etc.)
    
    If ANY checkbox is unchecked → FIX BEFORE GENERATING
    

---
  #### **Name**
Post-Generation QA
  #### **Description**
Rigorous visual comparison against references before approval
  #### **When**
After every generation, before showing to user or using in production
  #### **Example**
    POST-GENERATION QA CHECKLIST:
    
    FACE VERIFICATION:
    [ ] Eye color matches reference
    [ ] Eye shape matches reference
    [ ] Face shape matches reference
    [ ] Nose shape matches reference
    [ ] Expression appropriate for scene
    
    HAIR VERIFICATION:
    [ ] Color exact match (check in different lighting)
    [ ] Style matches (twintails are twintails, not ponytail)
    [ ] Length consistent
    [ ] Accessories present (hair clips, ribbons, etc.)
    
    OUTFIT VERIFICATION:
    [ ] All clothing items present
    [ ] Colors match reference
    [ ] Details preserved (trim, patterns, buttons)
    [ ] Accessories present (jewelry, gloves, etc.)
    
    BODY/PROPORTIONS:
    [ ] Height/build consistent with character
    [ ] Proportions match (head-to-body ratio)
    [ ] Pose anatomically sound
    
    STYLE VERIFICATION:
    [ ] Art style matches series (anime vs realistic vs cartoon)
    [ ] Line weight consistent
    [ ] Shading style matches
    [ ] Color saturation appropriate
    
    QUALITY CHECKS:
    [ ] No artifacts or glitches
    [ ] Hands rendered correctly (count fingers!)
    [ ] No floating elements or disconnected parts
    [ ] Background appropriate and not distracting
    
    VERDICT: [ ] APPROVED  [ ] REGENERATE (note issues)
    

---
  #### **Name**
Seed Locking for Series
  #### **Description**
Lock generation seed when making variations of same scene
  #### **When**
Creating multiple versions, iterating on a scene, or continuation shots
  #### **Example**
    SEED MANAGEMENT:
    
    1. First generation: Let seed be random, note it if result is good
    2. Variations: Keep SAME seed, change only ONE element
       - Same seed + different expression = consistent character, new emotion
       - Same seed + different pose = risky, may cause drift
    
    RULE: Change the smallest thing first
    - Expression only? Keep seed
    - New pose? May need new seed, regenerate until consistent
    - New outfit? Major change, expect inconsistency, multiple attempts
    
    NEVER change seed + prompt + model + settings simultaneously
    

---
  #### **Name**
Style Reference Anchoring
  #### **Description**
Use reference images to lock in visual style across generations
  #### **When**
Working on a series, maintaining consistent aesthetic, or matching existing art
  #### **Example**
    STYLE REFERENCE METHODS:
    
    1. IP-Adapter: Upload reference → generates with similar style
       - Good for: Pose, composition, overall vibe
       - Set control strength: 0.6-0.8 for style, 0.3-0.5 for loose inspiration
    
    2. LoRA/Kontext: Train on 4-8 character images
       - Good for: Character identity across many generations
       - Trigger word: "[character_name]" in every prompt
    
    3. Style Reference URL (Midjourney): --sref [image_url]
       - Good for: Art style consistency
       - Style weight: 100 default, 50-150 range
    
    4. Image-to-Image: Start from approved image
       - Good for: Variations on existing scene
       - Strength: 0.3-0.5 to keep most of original
    

---
  #### **Name**
Progressive Disclosure for Complex Characters
  #### **Description**
Build character consistency gradually through staged generation
  #### **When**
Complex character design, or establishing new character identity
  #### **Example**
    STAGED CHARACTER ESTABLISHMENT:
    
    Stage 1: Face/Portrait (5-10 generations)
    - Generate close-up portraits until face is consistent
    - Lock in exact facial feature descriptions
    - Create "golden reference" portrait
    
    Stage 2: Full Body (5-10 generations)
    - Use Stage 1 face as reference
    - Establish body proportions
    - Lock in outfit details
    
    Stage 3: Turnaround Sheet
    - Generate multi-view sheet using Stage 1+2 references
    - Verify consistency across all angles
    
    Stage 4: Action Poses
    - Only after Stages 1-3 are locked
    - Use turnaround as reference
    - QA each generation against sheet
    
    DO NOT skip stages. Rushing causes compounding drift.
    

## Anti-Patterns


---
  #### **Name**
Generate and Hope
  #### **Description**
Generating images without reference or documentation and hoping they match
  #### **Why**
    Without explicit anchors, every generation interprets the character differently.
    Small variations compound across images. By image 10, the character is
    unrecognizable compared to image 1.
    
  #### **Instead**
Create character bible FIRST, then generate with references

---
  #### **Name**
Vague Prompts
  #### **Description**
Using non-specific descriptors like "pretty girl" or "anime style"
  #### **Why**
    "Pretty" means different things to different models. "Anime" covers thousands
    of distinct styles. Vague prompts give the model permission to vary, and it will.
    
  #### **Instead**
    Use EXACT descriptors: "heart-shaped face, large violet eyes, small upturned nose"
    Specify style: "90s anime cel-shading with hard shadows" not "anime style"
    

---
  #### **Name**
Synonym Substitution
  #### **Description**
Using different words for the same feature across prompts
  #### **Why**
    "Silver hair" vs "gray hair" vs "platinum hair" vs "white hair" will produce
    different results. The model doesn't know these are supposed to be the same.
    
  #### **Instead**
Pick ONE term and use it EXACTLY every time. Document in character bible.

---
  #### **Name**
Skipping QA
  #### **Description**
Approving generated images without systematic review
  #### **Why**
    Small drifts are easy to miss but accumulate. The human eye adapts to gradual
    changes. By the time drift is obvious, you have 50 inconsistent images.
    
  #### **Instead**
Use QA checklist for EVERY image. No exceptions. No "close enough."

---
  #### **Name**
Close Enough Thinking
  #### **Description**
Accepting images with minor inconsistencies because regenerating takes time
  #### **Why**
    "The eyes are a bit different but it's fine" → Next image eyes drift more →
    By end of series, character has completely different eyes. Technical debt
    compounds faster in visual content than in code.
    
  #### **Instead**
    Regenerate until it matches. If matching is too hard, your prompt needs work.
    Fix the system, not the symptom.
    

---
  #### **Name**
Reference-Free Continuation
  #### **Description**
Generating new images of established character without loading references
  #### **Why**
    Even if you remember the character perfectly, you'll describe them slightly
    differently each time. Your memory drifts too. Only references are stable.
    
  #### **Instead**
ALWAYS have reference image loaded or linked when generating character

---
  #### **Name**
Multi-Variable Changes
  #### **Description**
Changing multiple things at once (pose + outfit + background + lighting)
  #### **Why**
    When multiple variables change, you can't tell what caused any inconsistency.
    Debugging becomes impossible. You lose the ability to iterate systematically.
    
  #### **Instead**
Change ONE thing at a time. Verify consistency. Then change the next thing.

---
  #### **Name**
Trust Previous Success
  #### **Description**
Assuming a prompt that worked before will work identically again
  #### **Why**
    Model updates, random seeds, and context differences can change outputs.
    What worked yesterday might drift today. Every generation needs verification.
    
  #### **Instead**
QA every generation against references, even with "proven" prompts