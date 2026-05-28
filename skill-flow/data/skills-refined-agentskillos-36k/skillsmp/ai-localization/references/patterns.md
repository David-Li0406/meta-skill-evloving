# AI Localization

## Patterns


---
  #### **Name**
The Localization Spectrum
  #### **Description**
Match localization approach to content type
  #### **When**
Deciding how to localize different content
  #### **Example**
    SPECTRUM FROM LIGHT TO HEAVY:
    
    1. MACHINE TRANSLATION (lightest)
       - Internal docs, low-stakes content
       - AI translation, no human review
       - Fast, cheap, acceptable quality
    
    2. AI + REVIEW
       - Customer-facing informational content
       - AI translation + native speaker review
       - Standard approach for most content
    
    3. TRANSCREATION
       - Marketing headlines, taglines, emotional content
       - Human creative adaptation, not translation
       - "What would we say in this culture?"
    
    4. RECREATION (heaviest)
       - Cultural-specific campaigns
       - Start from scratch for each market
       - Local creative team creates
    
    RULE: Marketing content = usually transcreation or recreation.
    Documentation = usually AI + review.
    Match investment to content importance.
    

---
  #### **Name**
AI Voice Localization
  #### **Description**
Localize video with AI voice dubbing
  #### **When**
Need video content in multiple languages quickly
  #### **Example**
    WORKFLOW:
    
    Step 1: TRANSCRIBE original audio
       - Descript, Whisper, or similar
       - Clean transcript of all speech
    
    Step 2: TRANSLATE script
       - AI translation (DeepL, Claude)
       - Human review for nuance
    
    Step 3: TIME ADJUSTMENT
       - Some languages are longer (German, Spanish)
       - Some are shorter (Chinese, Japanese)
       - Adjust script or pacing to fit
    
    Step 4: AI VOICE GENERATION
       - ElevenLabs for voice cloning
       - Or: Match voice type (gender, age, tone)
       - Generate in target language
    
    Step 5: SYNC AND MIX
       - Align new audio with video
       - Adjust lip sync if needed (HeyGen feature)
       - Mix with original music/SFX
    
    Result: Localized video in hours, not weeks.
    

---
  #### **Name**
Visual Localization Checklist
  #### **Description**
Adapt visual elements for different markets
  #### **When**
Localizing imagery and video
  #### **Example**
    VISUAL LOCALIZATION CHECKS:
    
    TEXT IN IMAGES:
    □ All text extracted and translated
    □ Text expansion accounted for (German: +30%)
    □ Right-to-left layout for Arabic, Hebrew
    □ Font supports target language characters
    
    CULTURAL SYMBOLS:
    □ Colors checked for cultural meaning
       - White = mourning in some Asian cultures
       - Red = luck in China, danger in West
    □ Gestures verified (thumbs up = offensive in some cultures)
    □ Religious symbols reviewed
    □ Number meanings checked (4 = death in Chinese)
    
    PEOPLE AND REPRESENTATION:
    □ Diverse representation appropriate for market
    □ Modesty standards for conservative markets
    □ Age expectations for certain products
    □ Local models if budget allows (AI can help)
    
    LEGAL REQUIREMENTS:
    □ Required disclaimers for market
    □ Regulatory compliance checked
    □ Data privacy statements updated
    

---
  #### **Name**
Simultaneous Multi-Market Launch
  #### **Description**
Launch content in all markets at once
  #### **When**
Need global synchronization
  #### **Example**
    WORKFLOW FOR 10+ LANGUAGE LAUNCH:
    
    WEEK 1: PREPARATION
    - Finalize source content
    - Create localization matrix (what goes where)
    - Assign languages to translators/reviewers
    - Set up QA process
    
    WEEK 2: TRANSLATION (parallel)
    - AI translation of all content (Day 1)
    - Human review all languages (Days 2-4)
    - Cultural adaptation flagged items (Days 3-5)
    
    WEEK 3: PRODUCTION (parallel)
    - Generate localized images (all markets)
    - Generate localized video (all markets)
    - Generate localized audio (all markets)
    
    WEEK 4: QA AND LAUNCH
    - Market-by-market QA
    - Platform uploads
    - Synchronized go-live
    
    AI ADVANTAGE: Translation and generation happen in parallel.
    Traditional: 10 languages = 10x time
    AI: 10 languages = 1x time + review overhead
    

---
  #### **Name**
Continuous Localization
  #### **Description**
Keep content synchronized across languages
  #### **When**
Content is frequently updated
  #### **Example**
    CONTINUOUS LOCALIZATION SYSTEM:
    
    1. SOURCE OF TRUTH: English (or primary language)
       - All updates happen in source first
       - Changes trigger localization workflow
    
    2. CHANGE DETECTION:
       - Track what changed (paragraphs, phrases)
       - Only translate changes, not full document
    
    3. TRANSLATION MEMORY:
       - Store approved translations
       - Reuse for consistency
       - AI suggestions use memory as context
    
    4. AUTOMATED PIPELINE:
       - Change detected → AI translation
       - → Human review queue
       - → Approval → Publication
    
    5. TERMINOLOGY DATABASE:
       - Company-specific terms
       - Product names
       - Consistent across all content
    
    TOOLS: Phrase, Lokalise, Crowdin integrate this workflow.
    AI accelerates, humans approve.
    

## Anti-Patterns


---
  #### **Name**
Translation-Only Thinking
  #### **Description**
Treating localization as just translation
  #### **Why**
Culture, legal, and context are as important as words
  #### **Instead**
Full cultural review. Visual adaptation. Local compliance check.

---
  #### **Name**
One Global Creative
  #### **Description**
Using same creative with translated text everywhere
  #### **Why**
Imagery, tone, and messaging may not resonate locally
  #### **Instead**
Market-specific adaptation. Local creative when important.

---
  #### **Name**
AI Without Review
  #### **Description**
Publishing AI translation without native review
  #### **Why**
AI makes mistakes that native speakers catch instantly
  #### **Instead**
Always human review for external content. Even if brief.

---
  #### **Name**
Ignoring Text Expansion
  #### **Description**
Not accounting for languages that use more space
  #### **Why**
German is ~30% longer than English; layouts break
  #### **Instead**
Design for expansion. 20-30% buffer in layouts.

---
  #### **Name**
Cultural Assumptions
  #### **Description**
Assuming your cultural understanding is correct
  #### **Why**
Cultural intuition is often wrong for unfamiliar markets
  #### **Instead**
Local market review. Ask, don't assume.

---
  #### **Name**
Forgetting Legal
  #### **Description**
Not checking local regulatory requirements
  #### **Why**
Different countries have different disclosure requirements
  #### **Instead**
Legal review checklist for each market. Especially for ads.