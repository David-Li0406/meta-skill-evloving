# AI Ad Creative

## Patterns


---
  #### **Name**
The Creative Testing Matrix
  #### **Description**
Systematic approach to testing creative variables
  #### **When**
Planning a creative testing roadmap
  #### **Example**
    TEST ONE VARIABLE AT A TIME:
    
    VARIABLE HIERARCHY (test in order):
    1. Hook (first 3 seconds) - Highest impact
    2. Message/Value prop - What you're selling
    3. Visual style - How it looks
    4. CTA - What action to take
    5. Format - Static vs. video vs. carousel
    
    TESTING MATRIX EXAMPLE:
    Hook variants: 5 different opening lines
    × Message variants: 3 value propositions
    = 15 combinations
    
    Don't test 15 simultaneously—too expensive, too noisy.
    Instead: Test 5 hooks with best message, find winner.
    Then: Test 3 messages with winning hook.
    Then: Combine winners and scale.
    

---
  #### **Name**
The UGC-Style AI Ad
  #### **Description**
Generate ads that feel organic, not produced
  #### **When**
Creating ads for social platforms where native content wins
  #### **Example**
    UGC (User Generated Content) style wins because it:
    - Feels authentic, not "salesy"
    - Matches platform content
    - Lower production = more volume
    
    AI UGC APPROACHES:
    
    1. DIGITAL HUMAN TESTIMONIAL:
       HeyGen/Synthesia avatar gives "testimonial"
       Script: Problem → Discovery → Result
       Setting: Home, office, casual
    
    2. AI-GENERATED "REAL" IMAGERY:
       Midjourney/Flux product-in-use images
       Style: iPhone photo, not studio shot
       Imperfect = authentic
    
    3. AI VOICEOVER + FOOTAGE:
       AI-generated stock-style footage
       ElevenLabs natural-sounding voice
       Feels like customer story
    
    KEY: Lower production quality intentionally.
    Overly polished = clearly an ad = skip.
    

---
  #### **Name**
Platform-Native Creative
  #### **Description**
Optimize creative for each platform's context
  #### **When**
Running ads across multiple platforms
  #### **Example**
    PLATFORM REQUIREMENTS:
    
    META (Facebook/Instagram):
    - First frame must hook (autoplay muted)
    - Text overlay (sound-off viewing)
    - 4:5 portrait for feed
    - Native, organic feel
    - UGC style outperforms
    
    TIKTOK:
    - Vertical 9:16 mandatory
    - First second is everything
    - Trending audio/format references
    - Creator style, not brand style
    - Hook patterns: "POV", "Wait for it", "Nobody asked but"
    
    GOOGLE/YOUTUBE:
    - 5 seconds to survive skip
    - Clear product/benefit early
    - Sound-on assumed
    - Multiple duration cuts
    
    LINKEDIN:
    - Professional context
    - Authority > fun
    - Thought leadership style
    - Native video performs better
    
    Don't resize—recreate for each platform.
    

---
  #### **Name**
Creative Fatigue Management
  #### **Description**
Systematic creative refresh strategy
  #### **When**
Managing ongoing ad accounts
  #### **Example**
    FATIGUE SIGNALS:
    - CTR declining over 2+ weeks
    - CPM increasing (same audience)
    - Frequency above 3
    - Comment sentiment shifting negative
    
    REFRESH CADENCE (guidelines):
    - High spend: New variants every 1-2 weeks
    - Medium spend: New variants every 2-4 weeks
    - Low spend: New variants monthly
    
    AI ADVANTAGE:
    Traditional: 1 new creative takes 1-2 weeks
    AI: 10 new creatives in 1 day
    
    REFRESH STRATEGY:
    Week 1: Test 10 new variants at low spend
    Week 2: Kill losers, scale winners
    Week 3: Generate 10 more variants
    Continuous: Never stop testing
    
    Always have 20+ concepts in pipeline.
    

---
  #### **Name**
Conversion Element Hierarchy
  #### **Description**
Prioritize elements that drive conversions
  #### **When**
Designing ads for direct response
  #### **Example**
    HIERARCHY OF CONVERSION ELEMENTS:
    
    1. HOOK (40% of ad effectiveness)
       - Pattern interrupt visual
       - Curiosity-inducing statement
       - "Wait, what?" moment
       - First 1-3 seconds
    
    2. PROMISE (30% of effectiveness)
       - Clear transformation
       - Benefit-focused (not feature)
       - Specific > vague
       - "You will [achieve X]"
    
    3. PROOF (20% of effectiveness)
       - Social proof
       - Authority signals
       - Results/numbers
       - "10,000 customers"
    
    4. CTA (10% of effectiveness)
       - Clear next step
       - Low friction
       - Urgency if authentic
       - "Start free trial"
    
    AI PROMPT ENCODING:
    "Create ad image with [attention-grabbing hook element],
    prominently featuring [specific benefit/transformation],
    including [proof element], with clear [CTA button/text]"
    

---
  #### **Name**
Batch Variant Generation
  #### **Description**
Generate many ad variants efficiently
  #### **When**
Need high volume of creative variants for testing
  #### **Example**
    BATCH WORKFLOW:
    
    Step 1: DEFINE VARIANT MATRIX
    - Hook types: 5 options
    - Visual styles: 3 options
    - Formats: 3 options (static, video, carousel)
    = 45 potential combinations
    
    Step 2: TEMPLATE PROMPTS
    "[STYLE] ad for [PRODUCT] featuring [HOOK_TYPE],
    [VISUAL_STYLE], optimized for [PLATFORM]"
    
    Step 3: BATCH GENERATE
    - Run all static image variants (15-20 min)
    - Run all video variants (1-2 hours)
    - QA as batch, flag outliers
    
    Step 4: ORGANIZE
    - Naming convention: Product_Hook_Style_Platform_v1
    - Export at correct specs
    - Ready for upload
    
    Step 5: STRUCTURED TESTING
    - Upload batch to platform
    - Equal budget distribution
    - Let data decide winners
    
    TARGET: 20+ variants per test cycle.
    

## Anti-Patterns


---
  #### **Name**
Beauty Over Performance
  #### **Description**
Optimizing for aesthetics instead of conversion
  #### **Why**
Pretty ads that don't convert are worthless
  #### **Instead**
Optimize for hook and conversion. Test "ugly" variants too.

---
  #### **Name**
Platform Homogeneity
  #### **Description**
Using same creative across all platforms
  #### **Why**
Each platform has different content expectations
  #### **Instead**
Create platform-native versions. Different vibes for different platforms.

---
  #### **Name**
Testing Too Few Variants
  #### **Description**
Testing 2-3 variants instead of 10+
  #### **Why**
Not enough volume to find outlier winners
  #### **Instead**
AI enables volume. Generate 20, test 20, find the winner.

---
  #### **Name**
Set and Forget
  #### **Description**
Not refreshing creative regularly
  #### **Why**
Creative fatigue is real; performance degrades over time
  #### **Instead**
Continuous refresh. Always have new variants in pipeline.

---
  #### **Name**
Copy-Paste Winners
  #### **Description**
Using same winning creative too long
  #### **Why**
Fatigue + competition + algorithm = declining performance
  #### **Instead**
Learn WHY it won. Create variations. Evolve the concept.

---
  #### **Name**
Ignoring Platform Context
  #### **Description**
Creating generic ads without platform consideration
  #### **Why**
Each platform has different user expectations and formats
  #### **Instead**
Native creative for each platform. Study top performers.