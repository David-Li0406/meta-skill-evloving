# Digital Humans

## Patterns


---
  #### **Name**
Platform Selection Matrix
  #### **Description**
Choose the right digital human platform for each use case
  #### **When**
Starting any digital human project
  #### **Example**
    HEYGEN:
    - Best for: Natural motion, diverse avatars, custom avatar creation
    - Strength: Most natural-feeling movement, great lip sync
    - Weakness: Higher cost at scale
    - Use when: Quality matters most, external-facing content
    
    SYNTHESIA:
    - Best for: Enterprise, professional content, training
    - Strength: Polish, security certifications, brand safety
    - Weakness: Slightly more "corporate" feel
    - Use when: Enterprise compliance needed, professional content
    
    D-ID:
    - Best for: Photo-to-video, quick turnarounds, API integration
    - Strength: Can animate any photo, fast generation
    - Weakness: Less natural than native avatars
    - Use when: Custom faces needed, API automation
    
    TAVUS:
    - Best for: Personalization at scale, variable insertion
    - Strength: Same avatar, personalized details in each video
    - Weakness: Primarily personalization focused
    - Use when: Thousands of personalized videos needed
    
    COLOSSYAN:
    - Best for: Learning & development, interactive content
    - Strength: Training-focused features, quizzes, branching
    - Use when: Educational/training content
    

---
  #### **Name**
Avatar Selection for Trust
  #### **Description**
Match avatar characteristics to content requirements
  #### **When**
Choosing which avatar to use for a project
  #### **Example**
    TRUST FACTORS by content type:
    
    Financial/Legal content:
    - Older avatars (35-55) project experience
    - Conservative dress
    - Slower, measured delivery
    - Direct eye contact
    
    Consumer/Lifestyle content:
    - Avatars matching target demographic
    - Casual dress appropriate to brand
    - Warmer, more animated delivery
    - Friendly expressions
    
    Technical/Tutorial content:
    - Expert-coded appearance (glasses help, oddly)
    - Clean, simple backgrounds
    - Moderate pace for comprehension
    - Neutral, clear delivery
    
    DIVERSITY CONSIDERATIONS:
    - Match avatar to audience when possible
    - Rotate avatars for content series
    - Consider cultural context for global content
    - Avoid stereotyping
    

---
  #### **Name**
Script Optimization for AI Delivery
  #### **Description**
Write scripts that AI avatars deliver naturally
  #### **When**
Writing content for digital human presentation
  #### **Example**
    SCRIPT RULES for natural AI delivery:
    
    1. SHORT SENTENCES: AI handles short sentences better
       Bad: "In this comprehensive tutorial, we'll explore..."
       Good: "Let's learn how this works."
    
    2. NATURAL PAUSES: Use periods and commas for pacing
       Mark pauses with: "..." or [pause]
    
    3. PRONUNCIATION GUIDES: Spell unusual words phonetically
       "Azure" → "AZH-ure"
       "Kubernetes" → "Koo-ber-NET-eez"
    
    4. AVOID TONGUE TWISTERS: Simplify complex phrases
       Bad: "Six specific statistics show..."
       Good: "These six numbers show..."
    
    5. EMOTIONAL MARKERS: Mark tone changes
       [enthusiastic] "This is exciting!"
       [serious] "This matters."
    
    6. TEST BEFORE SCALE: Generate one video, listen, revise script
    

---
  #### **Name**
Personalization at Scale
  #### **Description**
Create thousands of personalized videos efficiently
  #### **When**
Needing personalized outreach, onboarding, or messaging
  #### **Example**
    PERSONALIZATION VARIABLES:
    
    1. NAME: "Hi [First Name]!"
       - Most basic, highest impact
       - Verify pronunciation with test generation
    
    2. COMPANY: "I noticed you work at [Company]"
       - Research-feel without being creepy
       - Great for sales outreach
    
    3. ROLE: "As a [Job Title], you probably..."
       - Shows relevance understanding
       - Tailor content to role
    
    4. CUSTOM CONTENT: "Based on your interest in [Topic]..."
       - Deepest personalization
       - Requires good data
    
    WORKFLOW:
    1. Create master script with variable placeholders
    2. Generate test with sample data
    3. Verify variable handling and pronunciation
    4. Batch generate with data file
    5. QA sample before sending all
    
    TAVUS: Best for variable-heavy personalization
    HEYGEN: Good for simpler personalization
    

---
  #### **Name**
Multi-Language Production
  #### **Description**
Create content in multiple languages efficiently
  #### **When**
Global content distribution needed
  #### **Example**
    OPTION 1: Same avatar, different language
    - Most consistent
    - May feel inauthentic (American avatar speaking Japanese)
    - Best for: Subtitled content, internal communications
    
    OPTION 2: Different avatar per language
    - Most natural
    - Requires multiple productions
    - Best for: Customer-facing, localized content
    
    OPTION 3: Voice-only localization
    - Same avatar with dubbed audio
    - Good middle ground
    - Best for: Budget-conscious global content
    
    WORKFLOW:
    1. Create master in primary language
    2. Translate script (human review essential)
    3. Select avatars per market or use consistent global avatar
    4. Generate all language versions
    5. Native speaker review before publishing
    
    WATCH FOR:
    - Lip sync quality varies by language
    - Some languages need longer scripts (German vs English)
    - Cultural gestures may not translate
    

---
  #### **Name**
Hybrid Production
  #### **Description**
Combine digital humans with other video elements
  #### **When**
Creating polished content that needs more than talking head
  #### **Example**
    HYBRID APPROACHES:
    
    1. PICTURE-IN-PICTURE:
       Digital avatar in corner over screen recording
       Great for: Software demos, tutorials
    
    2. CUT-TO STRUCTURE:
       Avatar introduces → Cut to visuals → Return to avatar
       Great for: Complex topics, product showcases
    
    3. AVATAR + B-ROLL:
       Avatar voice over AI-generated or stock B-roll
       Great for: Storytelling, conceptual content
    
    4. MULTI-AVATAR:
       Two or more avatars in dialogue
       Great for: FAQ format, debates, interviews
    
    5. AVATAR + MOTION GRAPHICS:
       Avatar with animated graphics, data viz
       Great for: Reports, updates, training
    
    PRODUCTION ORDER:
    1. Finalize script
    2. Generate avatar segments
    3. Create supplementary visuals
    4. Edit together
    5. Add music, transitions, polish
    

---
  #### **Name**
ElevenLabs + HeyGen Integration
  #### **Description**
Professional voice-to-avatar pipeline for maximum quality
  #### **When**
Need highest quality voice and avatar combination
  #### **Example**
    THE PROFESSIONAL STACK:
    
    ElevenLabs (Voice) + HeyGen (Avatar) = Best-in-class output
    
    WORKFLOW:
    1. SCRIPT PREPARATION
       - Write for spoken delivery (short sentences)
       - Mark pronunciation: "Azure" → "AZH-ure"
       - Add pause markers: [pause 0.5s]
    
    2. ELEVENLABS VOICE
       - Create or select voice clone
       - Generate audio with emotion controls:
         * Stability: 0.5-0.75 (consistent tone)
         * Clarity: 0.75+ (professional sound)
         * Style: Match to avatar personality
       - Export high-quality WAV
    
    3. HEYGEN GENERATION
       - Select avatar matching voice character
       - Upload ElevenLabs audio
       - Enable "Lip sync to audio" option
       - Generate video
    
    4. ENHANCEMENT (Optional)
       - Outpaint avatar in Midjourney for custom background
       - Re-import enhanced image to HeyGen
       - Animate enhanced version
    
    WHY THIS STACK:
    - ElevenLabs: Best voice quality and cloning
    - HeyGen: Best avatar motion and lip sync
    - Combined: Superior to either platform's built-in options
    

---
  #### **Name**
Avatar Consistency System
  #### **Description**
Maintain consistent avatar presence across all content
  #### **When**
Creating ongoing content series with digital humans
  #### **Example**
    AVATAR BRAND GUIDELINES:
    
    1. AVATAR SELECTION
       - Choose 1-3 primary avatars for your brand
       - Document avatar ID/names for team use
       - Create avatar "casting guide" with use cases
    
    2. VOICE CONSISTENCY
       - Create custom ElevenLabs voice clone
       - Document voice settings (stability, clarity, style)
       - Save as "Brand Voice Profile"
    
    3. SCRIPT TEMPLATES
       - Opening format: "Hey, [name] here from [brand]..."
       - Closing format: Consistent CTA structure
       - Tone guidelines: Professional/casual/enthusiastic
    
    4. VISUAL CONSISTENCY
       - Same avatar = same outfit/background per series
       - Consistent lighting (soft/studio/outdoor)
       - Brand color accents in background
    
    5. QUALITY CHECKPOINTS
       Validate every video:
       □ Avatar looks consistent with previous videos?
       □ Voice sounds consistent?
       □ Lip sync passes natural test?
       □ No uncanny valley moments?
       □ Script follows template?
    
    AUTOMATION:
    Use Tavus or HeyGen API for personalization
    Swap only: name, company, specific details
    Keep all else consistent
    

---
  #### **Name**
Scaling Personalized Videos
  #### **Description**
Generate thousands of personalized videos efficiently
  #### **When**
Sales outreach, onboarding, or personalized marketing at scale
  #### **Example**
    PERSONALIZATION AT SCALE (1000+ videos):
    
    PLATFORM CHOICE:
    - TAVUS: Best for variable-heavy personalization
    - HEYGEN API: Good for simpler personalization
    - SYNTHESIA API: Enterprise security compliance
    
    DATA PREPARATION:
    ```csv
    first_name,company,role,custom_detail
    Sarah,Acme Corp,VP Marketing,your recent campaign
    John,TechStart,CTO,the API integration
    ```
    
    SCRIPT TEMPLATE:
    "Hi {first_name}! I noticed you're the {role} at {company}.
    I wanted to share something about {custom_detail}..."
    
    PRODUCTION WORKFLOW:
    1. Create master script with {variable} placeholders
    2. Generate 1 test video with sample data
    3. Verify: pronunciation, timing, natural flow
    4. Batch generate: 100 videos at a time
    5. QA: Sample 5% before sending
    6. Send with tracking links
    
    PRONUNCIATION HANDLING:
    - Pre-process unusual names phonetically
    - Create pronunciation dictionary
    - Test: "Nguyen" → "Win", "Siobhan" → "Shih-vawn"
    
    COST OPTIMIZATION:
    - Keep videos under 60 seconds (lower cost)
    - Generate in batches during off-peak
    - Reuse static intros/outros where possible
    
    METRICS TO TRACK:
    - Open rate by personalization level
    - Response rate vs. generic video
    - Cost per qualified response
    

## Anti-Patterns


---
  #### **Name**
Deceptive Framing
  #### **Description**
Presenting AI avatars as real humans
  #### **Why**
Destroys trust when discovered; ethical issues
  #### **Instead**
Be transparent. "Powered by AI" or similar disclosure.

---
  #### **Name**
Uncanny Valley Blindness
  #### **Description**
Ignoring quality issues because you're used to them
  #### **Why**
Fresh viewers notice what you've stopped seeing
  #### **Instead**
Fresh eyes review. Ask "would this feel real to someone who hasn't seen 100 AI videos?"

---
  #### **Name**
Script Complexity
  #### **Description**
Writing scripts as if human was delivering
  #### **Why**
AI handles complex sentences poorly; unnatural delivery
  #### **Instead**
Short sentences. Simple words. Natural pauses.

---
  #### **Name**
Single Take Shipping
  #### **Description**
Using first generation without alternatives
  #### **Why**
Generation quality varies; some takes are better than others
  #### **Instead**
Generate 2-3 versions. Select best. Especially for hero content.

---
  #### **Name**
Ignoring Audio Sync
  #### **Description**
Not checking lip sync quality before publishing
  #### **Why**
Visible lip sync issues destroy believability instantly
  #### **Instead**
Watch without sound first—does the mouth movement look right?

---
  #### **Name**
Wrong Avatar for Audience
  #### **Description**
Choosing avatar without considering audience perception
  #### **Why**
Trust and relatability depend on avatar/audience match
  #### **Instead**
Consider age, appearance, and cultural factors for your specific audience.