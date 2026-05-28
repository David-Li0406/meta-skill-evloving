# AI Creative Director

## Patterns


---
  #### **Name**
The AI Production Pipeline
  #### **Description**
Standard workflow for multi-tool AI productions
  #### **When**
Creating any campaign or production using multiple AI tools
  #### **Example**
    PHASE 1: CREATIVE FOUNDATION
    ├── Brief: What are we making? For whom? Why?
    ├── References: Visual, audio, and tonal references
    ├── Constraints: Brand guidelines, technical specs, budget
    └── Approval: Stakeholder sign-off before production
    
    PHASE 2: ASSET GENERATION
    ├── Images: AI-generate key visuals (Midjourney, Flux)
    ├── Video: AI-generate motion content (Veo3, Runway)
    ├── Audio: AI-generate music/sound (Suno, ElevenLabs)
    ├── Presenters: AI-generate digital humans (HeyGen)
    └── Each asset reviewed against brief before proceeding
    
    PHASE 3: ENHANCEMENT
    ├── Upscaling: Quality enhancement (Topaz, Magnific)
    ├── VFX: Compositing, effects (After Effects, AI VFX)
    ├── Color: Consistent grading across assets
    └── Audio: Mixing, mastering, sync
    
    PHASE 4: ASSEMBLY
    ├── Edit: Combine assets into final deliverables
    ├── Localize: Multi-language versions if needed
    ├── Format: Platform-specific versions
    └── QA: Final quality check against brief
    
    PHASE 5: DELIVERY
    ├── Export: Correct formats for each destination
    ├── Document: Record what worked for future
    └── Handoff: To marketing for distribution
    

---
  #### **Name**
Brand Consistency System
  #### **Description**
Maintain consistent look across AI-generated assets
  #### **When**
Creating multiple assets that must feel unified
  #### **Example**
    THE BRAND LOCK:
    
    1. STYLE PROMPT PREFIX: Standard opening for all prompts
       "In [Brand] style: [detailed description of visual language]"
       Use for: ALL image and video generation
    
    2. COLOR ENFORCEMENT: Specify exact palette
       "Color palette: primary #HEX, secondary #HEX..."
       Post-process to correct any drift
    
    3. REFERENCE LOCKS: Approved reference images
       Use as IP-Adapter or style references
       "Like [reference image]" consistency
    
    4. VOICE LOCK: Consistent audio identity
       Same AI voice settings across all audio
       Same music style/tempo/mood
    
    5. AVATAR LOCK: Consistent digital human
       Same avatar for entire campaign
       Same wardrobe, setting, delivery style
    
    ENFORCEMENT:
    - Style guide document with approved examples
    - QA checklist against style guide
    - Side-by-side comparison before approval
    

---
  #### **Name**
Scale Production Template
  #### **Description**
Create many variations efficiently
  #### **When**
Need dozens or hundreds of similar assets
  #### **Example**
    BATCH PRODUCTION WORKFLOW:
    
    1. HERO FIRST: Create and perfect one hero asset
       - Iterate until approved
       - Document exact settings and prompts
       - This is the reference for all variations
    
    2. VARIATION MATRIX: Define what changes
       - What stays same (brand, style, quality)
       - What varies (subject, color, copy, format)
       - Create matrix: 5 subjects × 4 formats = 20 assets
    
    3. TEMPLATE PROMPTS: Parameterized prompt templates
       "[BRAND_PREFIX] [SUBJECT_VAR] in [SETTING_VAR], [SUFFIX]"
       - Fill variables from matrix
       - Batch generate
    
    4. BATCH GENERATION: Run all at once
       - Parallel generation where possible
       - Monitor for consistency drift
       - Flag outliers for regeneration
    
    5. BATCH QA: Review as grid
       - Compare all variations side by side
       - Identify inconsistencies
       - Regenerate failures, not full batch
    
    6. BATCH EXPORT: Automated naming and formatting
       - Consistent file naming convention
       - Auto-export to correct formats
       - Organize in asset management system
    

---
  #### **Name**
Tool Selection Decision Tree
  #### **Description**
Choose the right AI tool for each creative task
  #### **When**
Starting any AI creative project
  #### **Example**
    DECISION TREE:
    
    IMAGES:
    ├── Need photorealism? → Flux or Imagen
    ├── Need artistic style? → Midjourney
    ├── Need text in image? → Ideogram or Flux
    ├── Need control (pose, depth)? → Stable Diffusion + ControlNet
    └── Need batch consistency? → Same model + same settings + same seed base
    
    VIDEO:
    ├── Need photorealistic humans? → Veo3
    ├── Need stylized/artistic? → Runway Gen-3
    ├── Need complex physics/action? → Sora
    ├── Need quick iterations? → Kling or Pika
    └── Need talking heads? → Digital Humans (HeyGen/Synthesia)
    
    AUDIO:
    ├── Need songs with vocals? → Suno
    ├── Need high-production instrumentals? → Udio
    ├── Need background/commercial music? → Soundraw
    ├── Need sound effects? → ElevenLabs SFX
    └── Need voice? → Voiceover skill or ElevenLabs
    
    PRESENTERS:
    ├── Need natural motion? → HeyGen
    ├── Need enterprise/compliance? → Synthesia
    ├── Need custom face? → D-ID
    └── Need personalization at scale? → Tavus
    
    Start with use case, not tool preference.
    

---
  #### **Name**
Quality Control at Scale
  #### **Description**
Maintain quality standards across high-volume production
  #### **When**
Creating more assets than can be individually reviewed
  #### **Example**
    TIERED QC SYSTEM:
    
    TIER 1: HERO ASSETS (100% human review)
    - Main campaign images and video
    - Customer-facing key visuals
    - Any asset used at large scale
    Review: Frame-by-frame, multiple reviewers
    
    TIER 2: SUPPORTING ASSETS (sampling review)
    - Variations and adaptations
    - Secondary placements
    - Short-lived assets
    Review: 20% sample, full batch if issues found
    
    TIER 3: AUTOMATED ASSETS (AI-assisted QC)
    - High-volume personalized content
    - Test variations
    - Internal use
    Review: Automated checks + exception flagging
    
    QC CHECKLIST (all tiers):
    □ On-brand (style, color, tone)
    □ No artifacts (weird hands, faces, text)
    □ Correct format and resolution
    □ Matches brief requirements
    □ No offensive/inappropriate elements
    □ Text/audio accurate (if applicable)
    

---
  #### **Name**
Workflow Documentation System
  #### **Description**
Record successful workflows for replication
  #### **When**
Creating repeatable AI production capability
  #### **Example**
    WORKFLOW DOCUMENTATION:
    
    For each production, document:
    
    1. BRIEF: What was requested, requirements
    2. TOOLS USED: Which AI tools, which settings
    3. PROMPTS: Exact prompts that worked (with variations noted)
    4. PROCESS: Step-by-step workflow
    5. ASSETS: Links to final approved assets
    6. LEARNINGS: What worked, what didn't, what to do differently
    7. TIME: How long each phase took
    8. COST: Compute and subscription costs
    
    FORMAT: Workflow template in Notion/Airtable
    - Searchable by project type, tools used, client
    - Include before/after prompt iterations
    - Tag by success level
    
    VALUE: Each documented workflow makes next production faster.
    Team leverage: Anyone can replicate successful workflows.
    

## Anti-Patterns


---
  #### **Name**
Tool-First Thinking
  #### **Description**
Choosing tools before understanding the creative problem
  #### **Why**
Wrong tool selection wastes time and produces suboptimal results
  #### **Instead**
Brief first. Requirements first. Then match tools to needs.

---
  #### **Name**
Hero-Only Production
  #### **Description**
Only creating single hero assets when scale is needed
  #### **Why**
AI enables scale—single assets underutilize capability
  #### **Instead**
Design for scale from start. Template prompts. Batch workflows.

---
  #### **Name**
Inconsistency Tolerance
  #### **Description**
Accepting visual inconsistency across AI-generated assets
  #### **Why**
Inconsistency destroys brand; looks unprofessional
  #### **Instead**
Build consistency systems. QA as a set, not individuals.

---
  #### **Name**
Undocumented Workflows
  #### **Description**
Not recording what worked for successful productions
  #### **Why**
Reinventing wheel each time; no organizational learning
  #### **Instead**
Document every production. Build workflow library.

---
  #### **Name**
Human Bottleneck
  #### **Description**
Manual steps that could be automated or batched
  #### **Why**
AI enables speed—manual steps negate the advantage
  #### **Instead**
Automate repetitive steps. Batch where possible. Reserve human judgment for creative decisions.

---
  #### **Name**
Single-Tool Dependency
  #### **Description**
Using only one AI tool for everything
  #### **Why**
Each tool has strengths and weaknesses; missing capabilities
  #### **Instead**
Multi-tool orchestration. Match tool to task.