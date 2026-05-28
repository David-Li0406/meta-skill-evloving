# ai-brand-kit

## Patterns


---
  #### **Name**
AI Brand Guidelines Document
  #### **When**
Starting brand AI implementation or onboarding new AI tools
  #### **Structure**
    Create living document that AI tools can consume:
    
    ## Brand Essence (AI-Readable)
    - Core values: [3-5 specific, not generic]
    - Brand voice adjectives: [8-10 precise descriptors]
    - Anti-brand: [What we explicitly reject]
    - Target audience: [Psychographic, not demographic]
    
    ## Visual DNA
    - Color palette: [Exact hex codes + emotional purpose]
    - Typography: [Font names + usage contexts]
    - Visual style: [20 curated reference images]
    - Negative examples: [What to avoid + why]
    
    ## Voice Training Set
    - Best performing copy: [50+ examples by content type]
    - Voice spectrum: [Professional ↔ Casual scale by channel]
    - Forbidden phrases: [Explicit blocklist]
    - Tone variations: [Context-specific guidelines]
    
    ## Prompt Library Index
    - Visual generation prompts: [By use case]
    - Copywriting prompts: [By channel/format]
    - Brand consistency checkers: [Validation prompts]
    
    Format: Markdown with clear headers AI can parse. Include examples,
    not just descriptions. Make actionable, not inspirational.
    

---
  #### **Name**
Prompt Library Architecture
  #### **When**
Need reusable, versioned prompts for consistent AI generation
  #### **Structure**
    Build structured prompt repository:
    
    ## Directory Structure
    /prompts
      /visual
        /social-media
          instagram-post-v2.md
          linkedin-header-v1.md
        /marketing
          hero-image-v3.md
          product-shot-v1.md
      /copy
        /social
          twitter-thread-v4.md
          linkedin-post-v2.md
        /email
          welcome-sequence-v1.md
          newsletter-v3.md
      /brand-checking
        visual-consistency-v1.md
        voice-consistency-v2.md
    
    ## Prompt Template Format
    ```markdown
    # [Use Case] - v[Version]
    
    ## Purpose
    [What this generates and why]
    
    ## Base Prompt
    [Core reusable prompt text]
    
    ## Variables
    - {PRODUCT}: [Description/example]
    - {TONE}: [Options: professional|casual|urgent]
    - {CTA}: [Call to action text]
    
    ## Brand Context
    [Auto-injected brand guidelines]
    
    ## Negative Prompts
    [What to explicitly avoid]
    
    ## Quality Benchmarks
    - Reference 1: [Link to gold standard example]
    - Reference 2: [Link to gold standard example]
    
    ## Usage Examples
    [3-5 filled examples with results]
    
    ## Changelog
    - v2 (2024-03): Added negative prompts for gradient avoidance
    - v1 (2024-01): Initial version
    ```
    
    Version control in git. Tag major versions. Deprecate outdated prompts.
    

---
  #### **Name**
Visual Style Tuning Workflow
  #### **When**
Training AI image generators on your brand aesthetic
  #### **Steps**
    
---
      ###### **Step**
Curate brand anchor image set
      ###### **Details**
        Select 15-25 existing brand images that best capture your aesthetic.
        Include variety: product shots, lifestyle, graphics, UI screenshots.
        Each image should be high quality and clearly "on brand."
        
        Avoid: Stock photos, inconsistent styles, outdated assets.
        
    
---
      ###### **Step**
Create Midjourney style reference
      ###### **Details**
        Upload anchors to Midjourney. Use --sref parameter with image URLs.
        Test with 20+ diverse prompts to validate consistency.
        Document which sref values (0-1000) work best for your brand.
        
        Example: `--sref https://brand.com/anchor1.jpg --sref 500`
        
    
---
      ###### **Step**
Build DALL-E custom style
      ###### **Details**
        Use ChatGPT's DALL-E with detailed style instructions.
        Create Custom GPT with embedded brand guidelines.
        Include negative prompts in system instructions.
        Test across 10+ content types.
        
    
---
      ###### **Step**
Train Flux LoRA (advanced)
      ###### **Details**
        For maximum control, train Flux LoRA on 50-100 brand images.
        Requires technical setup but gives fine-grained style control.
        Host on Replicate or RunPod for team access.
        Version LoRA models by training date.
        
    
---
      ###### **Step**
Document prompt patterns
      ###### **Details**
        Record which prompt structures work best for your style.
        Note effective keywords, compositions, lighting terms.
        Build reusable prompt templates.
        Create negative prompt library.
        
    
---
      ###### **Step**
Establish quality gates
      ###### **Details**
        Define what "on brand" means measurably.
        Create comparison grid with gold standards.
        Set approval workflow for new AI assets.
        Track style drift over time.
        

---
  #### **Name**
Voice Training Methodology
  #### **When**
Teaching AI to write in your brand voice across contexts
  #### **Steps**
    
---
      ###### **Step**
Gather voice corpus
      ###### **Details**
        Collect 50-100 examples of your best brand writing.
        Organize by context: social, email, docs, ads, support.
        Include variety: short/long, formal/casual, urgent/evergreen.
        
        Quality over quantity but need volume for pattern detection.
        
    
---
      ###### **Step**
Extract voice patterns
      ###### **Details**
        Use Claude/GPT to analyze corpus and identify:
        - Sentence structure patterns (short/long, simple/complex)
        - Common opening/closing patterns
        - Recurring phrases or formulations
        - Punctuation style (em-dashes, semicolons, etc.)
        - Vocabulary level and technical density
        - Use of questions, imperatives, statements
        
        Create structured voice profile document.
        
    
---
      ###### **Step**
Build context-specific prompts
      ###### **Details**
        Don't use generic "brand voice" - create prompts for each context:
        
        - Twitter: [Voice characteristics + platform constraints]
        - Email newsletter: [Voice + format + CTA patterns]
        - Product docs: [Voice + clarity + technical level]
        - Support: [Voice + empathy + problem-solving]
        - LinkedIn: [Voice + professionalism + thought leadership]
        
        Each prompt embeds relevant corpus examples.
        
    
---
      ###### **Step**
Create anti-voice guidelines
      ###### **Details**
        Explicitly state what NOT to write:
        - Forbidden phrases: "delighted to announce", "game-changer"
        - Banned structures: "In today's world of X..."
        - Tone violations: Corporate jargon, excessive exclamations
        
        Negative examples teach as much as positive ones.
        
    
---
      ###### **Step**
Build Custom GPT / Claude Project
      ###### **Details**
        Create dedicated AI assistant with:
        - System instructions with voice guidelines
        - Corpus examples in knowledge base
        - Context-specific prompt templates
        - Brand terminology glossary
        
        Train team to use this vs generic ChatGPT.
        
    
---
      ###### **Step**
Quality benchmark and iterate
      ###### **Details**
        Generate 20+ examples across contexts.
        Compare against corpus gold standards.
        A/B test with team: "Which sounds more like us?"
        Refine prompts based on misses.
        Version voice guidelines as brand evolves.
        

---
  #### **Name**
Asset Variation System
  #### **When**
Need to generate multiple on-brand variations efficiently
  #### **Structure**
    Build system for controlled variation within brand constraints:
    
    ## Variation Dimensions
    Define what CAN vary while staying on brand:
    
    - Color: Primary palette variations, accent swaps
    - Composition: 3-4 approved layout structures
    - Imagery: Style-consistent image categories
    - Copy: Tone spectrum by context (formal ↔ casual)
    - Format: Dimensions/aspect ratios by channel
    
    ## Constraint System
    Define what MUST stay consistent:
    
    - Logo usage and clear space
    - Typography hierarchy and font pairings
    - Voice principles (even as tone varies)
    - Visual style references (same aesthetic DNA)
    
    ## Variation Prompts
    Create prompts with controlled randomness:
    
    ```
    Generate Instagram post with:
    - Style: {BRAND_STYLE_REF}
    - Color: {random: primary_palette}
    - Composition: {random: [layout_1, layout_2, layout_3]}
    - Subject: {PRODUCT}
    - Must include: {BRAND_ELEMENTS}
    - Never include: {BRAND_NEGATIVES}
    ```
    
    ## Batch Generation
    Use variation prompts to generate 10-20 options.
    Team selects best 2-3. Refine winners. Archive losers.
    
    ## Version Control
    Track which variations perform best.
    Retire low performers from rotation.
    Update prompts based on learnings.
    

---
  #### **Name**
Brand Consistency Checker
  #### **When**
Validating AI-generated content meets brand standards
  #### **Implementation**
    Create AI-powered brand validation system:
    
    ## Visual Consistency Checker
    Prompt for image validation:
    
    ```
    You are a brand consistency validator for {BRAND}.
    
    Brand Guidelines:
    - Color palette: {COLORS}
    - Typography: {FONTS}
    - Visual style: {STYLE_DESCRIPTION}
    - Must avoid: {NEGATIVES}
    
    Analyze this image and check:
    1. Color usage: In palette? Proportions correct?
    2. Typography: Approved fonts? Proper hierarchy?
    3. Style: Matches brand aesthetic? Reference images?
    4. Violations: Any forbidden elements?
    5. Overall: Brand-aligned? (1-10 score)
    
    Output: Pass/Fail + specific issues + suggestions
    ```
    
    ## Copy Consistency Checker
    Prompt for text validation:
    
    ```
    You are a brand voice validator for {BRAND}.
    
    Voice Guidelines:
    - Tone: {TONE_DESCRIPTION}
    - Forbidden phrases: {BLOCKLIST}
    - Example corpus: {EXAMPLES}
    
    Analyze this copy:
    "{TEXT_TO_CHECK}"
    
    Check:
    1. Voice match: Sounds like brand? (1-10)
    2. Forbidden phrases: Any violations?
    3. Tone appropriateness: Right for {CONTEXT}?
    4. Improvements: Specific suggestions to strengthen
    
    Output: Pass/Fail + issues + rewrite suggestions
    ```
    
    ## Automated Workflow
    Integrate checkers into approval flow:
    
    1. AI generates content
    2. Auto-run consistency checker
    3. If Pass: Send to human review
    4. If Fail: Show issues, suggest fixes, regenerate
    5. Track failure patterns to improve base prompts
    
    ## Feedback Loop
    When humans override checker (approve "fails" or reject "passes"),
    capture feedback to refine validation prompts.
    

---
  #### **Name**
Multi-Channel Brand Deployment
  #### **When**
Launching brand across multiple AI-powered channels
  #### **Strategy**
    Coordinate consistent brand rollout across AI touchpoints:
    
    ## Channel Inventory
    Map all AI-enabled brand touchpoints:
    
    - Social: Twitter/X, LinkedIn, Instagram, TikTok
    - Email: Newsletters, campaigns, transactional
    - Content: Blog, docs, landing pages
    - Support: Chatbots, help articles, FAQs
    - Ads: Google, Meta, LinkedIn
    - Internal: Slack bots, notion, docs
    
    ## Context Mapping
    For each channel, define:
    
    - Voice variation: How does brand tone adapt?
    - Visual requirements: Dimensions, format, style
    - Prompt templates: Channel-specific generation prompts
    - Quality benchmarks: Gold standard examples
    - Approval workflow: Who reviews before publish?
    
    ## Rollout Sequence
    Don't launch everywhere simultaneously:
    
    1. Start with 1-2 high-impact channels
    2. Generate 20+ examples, refine prompts
    3. Run for 2-4 weeks, gather feedback
    4. Update prompts based on learnings
    5. Expand to next channel tier
    6. Cross-pollinate learnings
    
    ## Consistency Monitoring
    As you scale across channels:
    
    - Weekly brand audits across channels
    - Track style drift metrics
    - User perception surveys
    - A/B test variations within brand
    - Update central brand guidelines
    - Sync prompt libraries across channels
    

---
  #### **Name**
Brand Evolution Management
  #### **When**
Brand needs to evolve while maintaining AI consistency
  #### **Process**
    Manage brand changes without breaking AI systems:
    
    ## Version Your Brand
    Treat brand like code:
    
    - v1.0: Initial brand launch
    - v1.1: Minor refinements (color tweaks, voice adjustments)
    - v2.0: Major evolution (rebrand, new positioning)
    
    ## Changelog Everything
    Document what changed and why:
    
    ```markdown
    # Brand v2.0 - March 2024
    
    ## Visual Changes
    - Updated color palette: Warmer tones (old cold blues)
    - New typography: Inter → Geist Sans
    - Simplified logo: Removed gradient
    
    ## Voice Changes
    - Tone: More conversational, less corporate
    - Removed: Jargon, buzzwords
    - Added: Humor, personality
    
    ## AI Impact
    - Update all Midjourney srefs with new color palette
    - Retrain DALL-E custom GPT on new visual examples
    - Update voice corpus with recent best writing
    - Deprecate old prompt templates (archive in /archive)
    - Create v2 prompts in /prompts/v2
    ```
    
    ## Migration Strategy
    Don't flip switch overnight:
    
    1. Create parallel v2 prompt library
    2. Generate examples with both v1 and v2
    3. A/B test with team and users
    4. Gradually shift traffic to v2
    5. Archive v1 (don't delete - might need to reference)
    6. Update all AI training (GPTs, Claude Projects, etc.)
    
    ## Backward Compatibility
    Some systems might still need v1:
    
    - Keep v1 prompts available but deprecated
    - Document which systems use which version
    - Set sunset date for v1 retirement
    - Migrate systems incrementally
    