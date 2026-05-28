# Brand Storytelling

## Patterns


---
  #### **Name**
The Brand Origin Story Framework
  #### **Description**
Craft a compelling founding narrative
  #### **When**
Creating or refining brand origin story
  #### **Example**
    ORIGIN STORY STRUCTURE:
    
    1. THE WORLD BEFORE (Status Quo)
       - What was the world like before your brand?
       - What problem existed?
       - What was frustrating/broken/missing?
    
    2. THE FOUNDER'S INSIGHT (Inciting Incident)
       - What did the founder(s) see that others missed?
       - What personal experience drove them?
       - What made them say "there has to be a better way"?
    
    3. THE STRUGGLE (Rising Action)
       - What obstacles did they face?
       - What did they sacrifice?
       - What moments almost broke them?
    
    4. THE BREAKTHROUGH (Climax)
       - What was the turning point?
       - What innovation/insight changed everything?
       - What proved the concept?
    
    5. THE TRANSFORMATION (Resolution)
       - How is the world different now?
       - What impact has been created?
       - What's still left to do?
    
    KEY ELEMENTS:
    - Specific details (dates, places, names)
    - Emotional truth (not just facts)
    - Stakes (what was at risk)
    - Human protagonists (not the company)
    

---
  #### **Name**
Customer Hero Journey
  #### **Description**
Turn customer success into narrative
  #### **When**
Creating case studies, testimonials, or customer stories
  #### **Example**
    CUSTOMER AS HERO:
    
    1. ORDINARY WORLD
       - Who is this customer?
       - What was their life/business like?
       - Make audience identify with them
    
    2. CALL TO ADVENTURE
       - What problem emerged?
       - Why couldn't they ignore it?
       - What was at stake?
    
    3. MEETING THE MENTOR (Your Brand)
       - How did they find you?
       - What made them trust you?
       - What guidance did you provide?
    
    4. TESTS AND TRIALS
       - What challenges remained?
       - What did implementation look like?
       - What obstacles were overcome?
    
    5. THE TRANSFORMATION
       - What changed?
       - Quantifiable results
       - Emotional transformation
       - New capabilities/confidence
    
    6. THE RETURN (Sharing Wisdom)
       - What would they tell others?
       - How do they see the future?
       - What's the recommendation?
    
    NOTE: Brand is mentor, not hero.
    Customer is protagonist.
    

---
  #### **Name**
Emotional Story Mapping
  #### **Description**
Map story elements to emotional journey
  #### **When**
Designing content for emotional impact
  #### **Example**
    EMOTIONAL ARC DESIGN:
    
    TARGET EMOTIONS (in sequence):
    1. Recognition → "That's me/my problem"
    2. Empathy → "I feel understood"
    3. Hope → "There might be a solution"
    4. Trust → "This seems credible"
    5. Desire → "I want this transformation"
    6. Confidence → "I can do this"
    7. Action → "I'm ready to start"
    
    STORY ELEMENTS THAT TRIGGER EACH:
    - Recognition: Specific pain points, relatable situations
    - Empathy: Vulnerability, shared struggles
    - Hope: Possibility, others' success
    - Trust: Proof, credibility, specifics
    - Desire: Vision of transformed state
    - Confidence: How-it-works, support available
    - Action: Clear next step, low barrier
    
    MAP YOUR CONTENT:
    For each piece, identify:
    - What emotion does this create?
    - What story element delivers it?
    - Where does it fit in the journey?
    

---
  #### **Name**
Story-to-Format Translation
  #### **Description**
Adapt core narrative to different formats
  #### **When**
Extending story across channels
  #### **Example**
    CORE STORY → FORMAT ADAPTATION:
    
    ONE STORY, MANY TELLINGS:
    
    LONG-FORM (Brand film, documentary):
    - Full narrative arc
    - All characters and subplots
    - Maximum emotional depth
    - 2-10 minutes
    
    MEDIUM (Case study, blog, social video):
    - Single thread from narrative
    - One character's journey
    - Key transformation moment
    - 30 seconds - 3 minutes
    
    SHORT (Social post, ad, snippet):
    - One powerful moment
    - Single emotion
    - Hook + payoff
    - 6-30 seconds
    
    MICRO (Headline, tagline, caption):
    - Essence of story
    - One line
    - Implication of full narrative
    
    PRINCIPLE:
    Every format should feel like part of the same story.
    Shorter versions hint at deeper story.
    Longer versions reward deeper engagement.
    

---
  #### **Name**
Story Consistency Framework
  #### **Description**
Maintain narrative coherence across touchpoints
  #### **When**
Scaling storytelling across team/content
  #### **Example**
    STORY BIBLE ELEMENTS:
    
    1. CORE NARRATIVE
       - One-paragraph summary
       - Key characters (brand, customer archetypes)
       - Central conflict
       - Transformation promise
    
    2. STORY PILLARS
       - 3-5 themes that express brand story
       - Example stories for each pillar
       - Content types that fit each pillar
    
    3. VOICE AND TONE
       - How the narrator speaks
       - Brand as character (personality)
       - What language fits/doesn't fit
    
    4. STORY RULES
       - What we always include
       - What we never do
       - How we handle sensitive topics
       - Character behaviors and limits
    
    5. PROOF POINTS
       - Specific facts that support story
       - Customer examples
       - Data that validates narrative
    
    CONSISTENCY CHECK:
    Before publishing, ask:
    "Does this feel like the same story?"
    "Would someone recognize our narrative?"
    
    TECHNICAL IMPLEMENTATION:
    ```typescript
    // Story bible validation
    interface StoryBible {
      coreNarrative: string;
      pillars: StoryPillar[];
      voiceRules: VoiceRule[];
      proofPoints: ProofPoint[];
    }
    
    function validateStoryConsistency(
      content: string,
      bible: StoryBible
    ): ValidationResult {
      const checks = [
        checkPillarAlignment(content, bible.pillars),
        checkVoiceCompliance(content, bible.voiceRules),
        checkProofPointUsage(content, bible.proofPoints)
      ];
      return aggregateResults(checks);
    }
    ```
    
    TRADEOFFS:
    ✓ Pros: Scalable consistency, team alignment, brand protection
    ✗ Cons: Can feel rigid, may stifle creativity, requires maintenance
    ⚖ Balance: Update bible quarterly based on what's working
    

---
  #### **Name**
AI-Assisted Story Mining
  #### **Description**
Use AI to extract stories from customer conversations
  #### **When**
Scaling customer story collection
  #### **Example**
    AUTOMATED STORY EXTRACTION:
    
    1. COLLECT RAW MATERIAL
       - Customer interviews (transcripts)
       - Support tickets (resolution stories)
       - Reviews and testimonials
       - Sales calls and demos
    
    2. AI EXTRACTION PROMPT
       ```
       Extract potential customer stories from this transcript:
    
       For each story, identify:
       - HERO: Who is the customer? (name, role, company)
       - PROBLEM: What challenge did they face? (specific pain)
       - STAKES: What was at risk? (consequences)
       - JOURNEY: What did they try? (obstacles)
       - SOLUTION: How did [product] help? (specific feature/benefit)
       - TRANSFORMATION: What changed? (before/after, emotions)
       - PROOF: What numbers/results? (quantifiable impact)
    
       Flag stories with:
       - High emotional content
       - Specific details (names, numbers, dates)
       - Clear transformation
       - Universal resonance
       ```
    
    3. HUMAN CURATION
       - AI extracts 10-20 story fragments
       - Human selects 2-3 strongest
       - Verify facts with customer
       - Shape into narrative structure
    
    4. IMPLEMENTATION CODE
       ```typescript
       interface StoryFragment {
         hero: string;
         problem: string;
         stakes: string;
         journey: string[];
         solution: string;
         transformation: {
           before: string;
           after: string;
           emotion: string;
         };
         proof: {
           metric: string;
           value: number;
         }[];
         emotionalScore: number; // AI-assessed
         specificityScore: number; // AI-assessed
       }
    
       async function extractStories(
         transcript: string
       ): Promise<StoryFragment[]> {
         const prompt = buildExtractionPrompt(transcript);
         const response = await ai.generate(prompt);
         const fragments = parseStoryFragments(response);
         return fragments
           .filter(f => f.emotionalScore > 0.7)
           .filter(f => f.specificityScore > 0.6)
           .sort((a, b) => b.emotionalScore - a.emotionalScore);
       }
       ```
    
    TRADEOFFS:
    ✓ Pros: Scalable, finds patterns humans miss, unbiased extraction
    ✗ Cons: May miss nuance, needs human verification, can feel mechanical
    ⚖ Balance: AI extracts, humans curate and craft final narrative
    

## Anti-Patterns


---
  #### **Name**
Brand as Hero
  #### **Description**
Making the brand the protagonist of every story
  #### **Why**
Audiences don't care about brands; they care about themselves
  #### **Instead**
Brand is guide/mentor. Customer is hero.

---
  #### **Name**
Feature Story
  #### **Description**
Listing features dressed up as "story"
  #### **Why**
Features aren't narrative; they're information
  #### **Instead**
Show features through transformation story.

---
  #### **Name**
Conflict Avoidance
  #### **Description**
Stories without stakes or struggle
  #### **Why**
Conflict is what makes stories interesting
  #### **Instead**
Embrace the problem. Show the struggle.

---
  #### **Name**
Generic Journey
  #### **Description**
Vague, could-be-any-brand storytelling
  #### **Why**
Generic stories don't stick or differentiate
  #### **Instead**
Specificity. Details. Real names and numbers.

---
  #### **Name**
Happy-Only Stories
  #### **Description**
Refusing to show challenges or failures
  #### **Why**
Too-perfect stories feel fake and unrelatable
  #### **Instead**
Include struggle. Show authentic challenges.

---
  #### **Name**
Story Without Stakes
  #### **Description**
Narratives where nothing is at risk
  #### **Why**
No stakes = no tension = no engagement
  #### **Instead**
Make clear what could be lost.