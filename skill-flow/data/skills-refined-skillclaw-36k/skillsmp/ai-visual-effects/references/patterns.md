# AI Visual Effects

## Patterns


---
  #### **Name**
AI Upscaling Decision Tree
  #### **Description**
Choose the right upscaler for each use case
  #### **When**
Upscaling AI-generated images or video
  #### **Example**
    UPSCALING TOOLS AND USE CASES:
    
    MAGNIFIC AI:
    - Best for: Images, creative enhancement
    - Strength: "Reimagines" detail, not just enlarges
    - Use when: You want added detail, style enhancement
    - Careful: May change content unexpectedly
    
    TOPAZ GIGAPIXEL (Images):
    - Best for: Photos, realistic images
    - Strength: Clean, reliable, fast
    - Use when: You need faithful upscaling
    - Best option for most image upscaling
    
    TOPAZ VIDEO AI:
    - Best for: Video upscaling
    - Strength: Temporal consistency, multiple models
    - Use when: Upscaling AI video or traditional footage
    - Industry standard for video
    
    REAL-ESRGAN:
    - Best for: Anime, illustrations
    - Strength: Clean lines, good for stylized content
    - Use when: Upscaling illustrated content
    - Free, runs locally
    
    WORKFLOW:
    Low-res AI output → Select appropriate upscaler → Upscale →
    Review for artifacts → Touch up if needed → Export
    

---
  #### **Name**
AI-Traditional Compositing
  #### **Description**
Integrate AI elements into real footage
  #### **When**
Combining AI-generated content with traditional video
  #### **Example**
    COMPOSITING WORKFLOW:
    
    1. MATCH LIGHTING:
       - Analyze real footage lighting direction/quality
       - Generate AI element with matching lighting prompt
       - Or: Adjust in post (color, shadows)
    
    2. EDGE QUALITY:
       - AI edges often need refinement
       - Rotoscope clean edges with AI assist
       - Feather edges to match depth of field
    
    3. COLOR MATCH:
       - Pull color palette from real footage
       - Apply to AI element as grade
       - Match contrast, saturation, hue
    
    4. MOTION MATCH:
       - Track camera motion from real footage
       - Apply to AI element position/scale
       - Add appropriate motion blur
    
    5. GRAIN AND TEXTURE:
       - Match film grain or sensor noise
       - Add subtle texture overlay
       - Helps sell the integration
    
    RULE: It's easier to generate AI to match footage
    than to adjust footage to match AI.
    

---
  #### **Name**
Artifact Fixing Workflow
  #### **Description**
Fix common AI generation artifacts
  #### **When**
AI output has visible issues
  #### **Example**
    COMMON ARTIFACTS AND FIXES:
    
    WEIRD HANDS/FINGERS:
    - Inpaint with specific hand reference
    - Generate hands separately, composite
    - Crop to avoid hands if possible
    
    FACE ISSUES:
    - Face-specific inpainting
    - Use face restoration AI (GFPGAN, CodeFormer)
    - Match original reference if available
    
    TEXT/WATERMARKS:
    - Inpaint to remove
    - Content-aware fill
    - Generate without text prompt, add text in post
    
    CONSISTENCY BREAKS:
    - Identify consistent frames
    - Use as reference for fixing breaks
    - Interpolation for video
    
    EDGE ARTIFACTS:
    - Outpaint to give clean crop
    - Feather edges for compositing
    - Vignette to hide edge issues
    
    TOOL: ComfyUI with ControlNet for most fixes.
    Allows precise control over what changes.
    

---
  #### **Name**
ComfyUI Production Workflows
  #### **Description**
Use ComfyUI for advanced AI VFX
  #### **When**
Need precise control over AI generation/modification
  #### **Example**
    KEY COMFYUI WORKFLOWS:
    
    1. CONTROLNET COMPOSITING:
       - Use depth/edge maps from real footage
       - Generate AI elements that match geometry
       - Perfect integration with scene
    
    2. INPAINTING PIPELINE:
       - Mask specific areas
       - Generate replacement content
       - Blend seamlessly
    
    3. BATCH PROCESSING:
       - Process multiple frames consistently
       - Maintain temporal coherence
       - Video-to-video workflows
    
    4. STYLE TRANSFER:
       - Apply consistent style across footage
       - IP-Adapter for style reference
       - LoRA for specific aesthetics
    
    5. UPSCALE + ENHANCE:
       - Multi-pass upscaling
       - Detail enhancement
       - Tiled processing for large images
    
    ADVANTAGE: Reproducible, parameterized, automatable.
    Same workflow runs on different inputs consistently.
    

---
  #### **Name**
Color Consistency System
  #### **Description**
Maintain color consistency across AI assets
  #### **When**
Multiple AI assets must feel unified
  #### **Example**
    COLOR CONSISTENCY WORKFLOW:
    
    1. ESTABLISH LOOK:
       - Grade hero asset to final look
       - Export LUT (Look-Up Table)
       - This is the reference
    
    2. APPLY TO ALL:
       - Apply LUT to all assets
       - Adjust individual assets as needed
       - Maintain shadow, midtone, highlight relationships
    
    3. WHITE BALANCE MATCH:
       - Sample white/gray from hero
       - Match across all assets
       - Critical for realistic feel
    
    4. CONTRAST MATCH:
       - Measure contrast ratio of hero
       - Adjust others to match
       - Use waveform for precision
    
    5. SATURATION MATCH:
       - Vibrance and saturation levels
       - Color intensity should match
       - Especially skin tones
    
    TOOL: DaVinci Resolve for best color tools.
    Or: Premiere Lumetri for simpler workflows.
    

## Anti-Patterns


---
  #### **Name**
Over-Upscaling
  #### **Description**
Upscaling low-quality source expecting miracles
  #### **Why**
"Enhance!" only works in movies—AI can't invent real detail
  #### **Instead**
Generate at highest resolution possible. Upscale is last resort.

---
  #### **Name**
Ignoring Context
  #### **Description**
Fixing elements without considering surrounding context
  #### **Why**
Fixes that don't match context look worse than original problems
  #### **Instead**
Match lighting, color, grain of surrounding content.

---
  #### **Name**
Default Settings
  #### **Description**
Using default settings without understanding impact
  #### **Why**
Each tool/setting is situational; defaults rarely optimal
  #### **Instead**
Learn what each parameter does. Adjust for specific content.

---
  #### **Name**
Destructive Editing
  #### **Description**
Making changes that can't be undone
  #### **Why**
Iteration is the method; need to try different approaches
  #### **Instead**
Non-destructive workflow. Save originals. Layer adjustments.

---
  #### **Name**
Pixel Peeping
  #### **Description**
Obsessing over artifacts no viewer will notice
  #### **Why**
Final use context matters; most artifacts invisible at viewing distance
  #### **Instead**
Review at final output size/format. Fix what matters.

---
  #### **Name**
Tool Worship
  #### **Description**
Believing one tool solves everything
  #### **Why**
Different problems need different tools
  #### **Instead**
Build toolkit. Match tool to problem. Combine approaches.