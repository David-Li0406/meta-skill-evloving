# Brand Storytelling - Sharp Edges

## Brand As Hero

### **Id**
brand-as-hero
### **Summary**
Making the brand the protagonist instead of the customer
### **Severity**
critical
### **Situation**
  Creating stories where the brand saves the day, the brand is the
  hero, the brand's journey is the focus. Centering the brand in
  every narrative.
  
### **Why**
  Audiences don't care about brands. They care about themselves. When
  the brand is the hero, the customer is just a prop. This creates
  disconnection and feels like advertising. The most powerful stories
  put the customer at the center with the brand as guide/enabler.
  
### **Solution**
  HERO POSITIONING:
  
  THE CUSTOMER IS THE HERO:
  - They have the problem
  - They take the journey
  - They achieve the transformation
  - They get the credit
  
  THE BRAND IS THE MENTOR:
  - Yoda, not Luke
  - Gandalf, not Frodo
  - Provides tools, guidance, support
  - Enables the hero's success
  
  CHECK YOUR STORY:
  - Who is the protagonist?
  - Whose transformation matters?
  - Who gets the victory?
  - If brand → rewrite
  
  LANGUAGE SHIFT:
  From: "We help you achieve X"
  To: "You can achieve X"
  
  From: "Our product does Y"
  To: "With Y, you can..."
  
  # The hero is never the mentor
  
### **Symptoms**
  - \'"We, we, we" copy\'
  - Brand logo/name everywhere
  - Customer barely mentioned
  - Feels like boasting
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
^(We|Our brand|Our company|Our product).*(hero|protagonist|journey|transformation)
      ###### **Severity**
critical
    
---
      ###### **Pattern**
We (saved|helped|enabled|transformed|changed).*customer
      ###### **Severity**
high
    
---
      ###### **Pattern**
\b(we|our)\b.*\b(we|our)\b.*\b(we|our)\b
      ###### **Severity**
medium
      ###### **Note**
Three+ 'we/our' in same paragraph
  #### **Fix Template**
    Before: "We helped [customer] achieve [result]"
    After: "[Customer] achieved [result] using [tool/guidance]"
    

## Conflict Avoidance

### **Id**
conflict-avoidance
### **Summary**
Creating stories without real stakes or struggle
### **Severity**
high
### **Situation**
  Telling stories where everything is fine, the solution is easy, and
  there's no real tension or conflict. Sanitized, risk-free narratives.
  
### **Why**
  Conflict is what makes stories compelling. Without stakes, there's no
  tension. Without struggle, there's no satisfaction in resolution.
  Conflict-free stories are forgettable because they don't activate the
  emotional systems that make stories stick.
  
### **Solution**
  CONFLICT IS REQUIRED:
  
  IDENTIFY THE STAKES:
  - What could be lost?
  - What's at risk if nothing changes?
  - Why does this matter?
  - What's the cost of failure?
  
  SHOW THE STRUGGLE:
  - What obstacles exist?
  - What makes this hard?
  - What did the hero try that didn't work?
  - What moment almost broke them?
  
  TYPES OF CONFLICT:
  - External: market, competition, circumstances
  - Internal: doubt, fear, uncertainty
  - Interpersonal: skeptics, naysayers
  
  CONFLICT IN BRAND STORIES:
  - The problem before the solution
  - The doubts about trying something new
  - The challenges during adoption
  - The setbacks before success
  
  # No conflict = no story
  
### **Symptoms**
  - Everything is easy in your stories
  - No mention of challenges
  - Transformation feels unearned
  - Stories feel flat and forgettable
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
(story|narrative|case study)(?!.*(challenge|struggle|obstacle|problem|difficulty|setback))
      ###### **Severity**
high
      ###### **Note**
Story content without conflict keywords
    
---
      ###### **Pattern**
(success|win|achieve)(?!.*(despite|after|overcome|fought|tried))
      ###### **Severity**
medium
      ###### **Note**
Success without struggle context
  #### **Fix Template**
    Add conflict layer:
    1. What was the obstacle?
    2. What made it hard?
    3. What did they try that failed?
    4. What almost made them quit?
    

## Generic Storytelling

### **Id**
generic-storytelling
### **Summary**
Vague narratives that could apply to any brand
### **Severity**
high
### **Situation**
  Creating stories so generic they could have any brand name swapped in.
  No specific details, real names, actual numbers, or unique elements.
  
### **Why**
  Generic stories don't stick. "We helped businesses grow" is not a
  story. Specificity is what makes stories believable and memorable.
  Real names, exact numbers, specific details—these create credibility
  and memorability.
  
### **Solution**
  SPECIFICITY RULES:
  
  ADD REAL DETAILS:
  - Names: "Sarah, a marketing director in Austin..."
  - Numbers: "increased revenue by 47% in 3 months"
  - Dates: "In March 2024, everything changed..."
  - Places: "In their downtown Denver office..."
  - Quotes: "She said, 'I never thought this was possible'"
  
  GENERIC → SPECIFIC:
  Before: "A customer was struggling with marketing"
  After: "Rachel had tried 4 different agencies in 2 years.
          Her CAC was $180 and climbing. The board was asking questions."
  
  UNIQUENESS TEST:
  - Could a competitor tell this exact story?
  - Are there details only we could know?
  - Is there something distinctive here?
  
  IF TOO GENERIC:
  - Interview actual customers
  - Get real numbers
  - Find unique moments
  - Add texture and detail
  
  # Specificity = credibility = memorability
  
### **Symptoms**
  - Stories could be anyone's
  - No names, numbers, dates
  - Vague "some customers" language
  - Nothing memorable or unique
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
\b(a customer|some customers|many|several|one company)\b
      ###### **Severity**
high
      ###### **Note**
Generic 'a customer' language
    
---
      ###### **Pattern**
(story|case study)(?!.*(\d{1,3}%|\$\d|[A-Z][a-z]+ [A-Z][a-z]+|20\d{2}|January|February|March|April|May|June|July|August|September|October|November|December))
      ###### **Severity**
high
      ###### **Note**
No specifics: numbers, names, or dates
    
---
      ###### **Pattern**
\b(improved|increased|better|more)\b(?!.*\d)
      ###### **Severity**
medium
      ###### **Note**
Claims without quantification
  #### **Fix Template**
    Add specificity checklist:
    □ Real name (first name minimum)
    □ Exact number (47%, $12k, 3 months)
    □ Specific date or timeframe
    □ Direct quote from customer
    □ Unique detail only you would know
    

## Story Without Stakes

### **Id**
story-without-stakes
### **Summary**
Narratives where nothing meaningful is at risk
### **Severity**
high
### **Situation**
  Telling stories where the outcome doesn't really matter, the hero
  has nothing to lose, and success or failure is inconsequential.
  
### **Why**
  Stakes create engagement. When nothing is at risk, why should anyone
  care? The higher the stakes, the more invested the audience becomes.
  This doesn't mean every story needs life-or-death—but something
  meaningful must be on the line.
  
### **Solution**
  DEFINE THE STAKES:
  
  LEVELS OF STAKES:
  1. Personal: reputation, confidence, identity
  2. Professional: job, career, success
  3. Financial: money, resources, viability
  4. Relational: team, partnerships, trust
  5. Existential: survival, meaning, purpose
  
  MAKE STAKES CLEAR:
  - What happens if the hero fails?
  - What's the cost of inaction?
  - Why does this matter to them personally?
  - What would they lose?
  
  EXAMPLE:
  Low stakes: "A company wanted to improve marketing"
  High stakes: "If Sarah's campaign failed, the startup
                would miss runway and she'd have to lay off
                the team she'd spent 2 years building"
  
  STAKES IN BRAND STORIES:
  - Business survival
  - Career consequences
  - Personal reputation
  - Team impact
  - Customer disappointment
  
  # If nothing's at risk, it's not a story
  
### **Symptoms**
  - Audience doesn't care about outcome
  - Success feels trivial
  - No emotional investment
  - \'"So what?" reaction\'
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
(story|narrative)(?!.*(risk|stake|lose|fail|consequence|cost|jeopardy))
      ###### **Severity**
high
      ###### **Note**
No stakes mentioned in story
    
---
      ###### **Pattern**
\b(success|win|achieve)\b(?!.*(would have|could have|almost|nearly))
      ###### **Severity**
medium
      ###### **Note**
Success without alternative outcome shown
  #### **Fix Template**
    Define stakes:
    "If [hero] failed, they would have [specific consequence]"
    "Without this, [hero] risked [personal/professional/financial loss]"
    

## Feature Story Confusion

### **Id**
feature-story-confusion
### **Summary**
Listing features disguised as storytelling
### **Severity**
medium
### **Situation**
  Dressing up a feature list with narrative language but without actual
  story structure—no character, no journey, no transformation.
  
### **Why**
  Features aren't stories. "Our AI-powered platform with real-time
  analytics" is information, not narrative. Stories have characters who
  want something, face obstacles, and transform. Features are just
  descriptions.
  
### **Solution**
  FEATURES → STORIES:
  
  FEATURES ARE PLOT DEVICES, NOT PLOT:
  - The feature is what enables transformation
  - The story is the transformation itself
  - Feature is mentioned, not centered
  
  TRANSLATION:
  Feature: "Real-time analytics dashboard"
  Story: "Sarah used to spend Fridays pulling reports. Now
          she opens her dashboard Monday morning and knows
          exactly where to focus. Last month she caught a
          problem before it cost them $50k."
  
  STORY STRUCTURE CHECK:
  □ Is there a character?
  □ Do they want something?
  □ Is there an obstacle?
  □ Is there a transformation?
  □ Does feature enable (not star in) the story?
  
  IF IT'S FEATURE-FOCUSED:
  - Add a human
  - Add a before/after
  - Show impact on their life
  - Feature becomes tool in their journey
  
  # Features are props, not protagonists
  
### **Symptoms**
  - \'"Story" is really a feature list\'
  - No human in the narrative
  - No before/after
  - Feels like specs with adjectives
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
\b(feature|capability|function|tool).*\b(feature|capability|function|tool).*\b(feature|capability|function|tool)\b
      ###### **Severity**
high
      ###### **Note**
Multiple features without human context
    
---
      ###### **Pattern**
(real-time|AI-powered|automated|integrated|advanced).*\b(dashboard|analytics|platform|system)\b(?!.*\b(she|he|they|customer|user)\b)
      ###### **Severity**
high
      ###### **Note**
Tech jargon without human protagonist
  #### **Fix Template**
    Convert feature list to story:
    1. Who uses this feature? (add name)
    2. What were they doing before? (before state)
    3. What changed when they got it? (transformation)
    4. How do they feel now? (emotion)
    

## Happy Only Stories

### **Id**
happy-only-stories
### **Summary**
Refusing to show any struggle, failure, or challenge
### **Severity**
medium
### **Situation**
  Creating relentlessly positive narratives where everything is easy,
  everyone is happy, and there are no setbacks or difficulties.
  
### **Why**
  Too-perfect stories feel fake. Audiences are skeptical of narratives
  without shadows. Including authentic struggle makes success more
  meaningful and makes the story more believable.
  
### **Solution**
  AUTHENTIC STRUGGLE:
  
  INCLUDE:
  - Initial doubts and skepticism
  - Setbacks during implementation
  - Moments of frustration
  - What almost didn't work
  - What they learned from challenges
  
  DON'T:
  - Invent problems for drama
  - Exaggerate negatives
  - Dwell on failures
  - Be relentlessly negative
  
  BALANCE:
  - Acknowledge the challenge
  - Show the struggle
  - Celebrate the victory
  - Make success feel earned
  
  EXAMPLE:
  Fake: "Everything was perfect from day one"
  Real: "The first month was rough. Adoption was slower
         than expected. But by month two, something clicked..."
  
  # Perfect is suspicious
  
### **Symptoms**
  - Everything is too easy
  - No mention of challenges
  - Feels like advertising
  - Audience skepticism
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
\b(perfect|flawless|seamless|effortless|easy|simple)\b.*\b(experience|implementation|onboarding|setup)\b
      ###### **Severity**
medium
      ###### **Note**
Too-perfect language
    
---
      ###### **Pattern**
(testimonial|case study)(?!.*(initial|first|challenge|concern|hesitat|worry|doubt))
      ###### **Severity**
medium
      ###### **Note**
No mention of initial doubts or challenges
  #### **Fix Template**
    Add authentic struggle:
    "At first, [concern/doubt]. But [what changed]."
    "The first [timeframe] was [challenge]. Then [breakthrough]."
    

## Narrative Inconsistency

### **Id**
narrative-inconsistency
### **Summary**
Different stories that contradict each other
### **Severity**
medium
### **Situation**
  Telling different origin stories, changing the brand narrative,
  contradicting previous testimonials or case studies.
  
### **Why**
  Consistency builds trust. When stories contradict, audiences notice
  and trust erodes. The brand story should be one story told many ways,
  not multiple incompatible stories.
  
### **Solution**
  STORY CONSISTENCY:
  
  CORE NARRATIVE (immutable):
  - Origin story facts
  - Founding principles
  - Key milestones
  - Core transformation promise
  
  VARIATIONS (acceptable):
  - Different customer stories
  - Different angles of same story
  - Platform-specific adaptations
  - Audience-specific emphasis
  
  CONTRADICTIONS (never):
  - Different founding dates
  - Conflicting origin stories
  - Incompatible value claims
  - Changing who did what
  
  STORY BIBLE:
  - Document the definitive narrative
  - Track what's been told
  - Review for consistency
  - Update centrally
  
  # One story, many tellings
  
### **Symptoms**
  - Wait, I thought they said...
  - Different versions floating around
  - Team tells different stories
  - Eroding credibility
### **Detection Pattern**
  #### **Type**
cross_reference
  #### **Triggers**
    
---
      ###### **Pattern**
founded.*\b(19|20)\d{2}\b
      ###### **Severity**
critical
      ###### **Note**
Check founding date consistency across content
      ###### **Action**
Compare all mentions of founding date
    
---
      ###### **Pattern**
(origin|founding|started|began).*story
      ###### **Severity**
high
      ###### **Note**
Flag for story bible review
      ###### **Action**
Verify against documented core narrative
  #### **Fix Template**
    Create story bible entry:
    1. Document canonical version
    2. Note acceptable variations
    3. Flag contradictions for team review
    4. Update all instances to align
    

## Telling Not Showing

### **Id**
telling-not-showing
### **Summary**
Describing instead of demonstrating
### **Severity**
medium
### **Situation**
  Telling the audience what to think ("We're innovative") instead of
  showing them through story and letting them conclude.
  
### **Why**
  "Show don't tell" is storytelling fundamentals. Telling breeds
  skepticism; showing creates believers. When you say "we're
  innovative," it's a claim. When you show innovation in action,
  it's evidence.
  
### **Solution**
  SHOW DON'T TELL:
  
  TELLING → SHOWING:
  "We're customer-focused"
  → Story of employee who flew across country for one customer
  
  "Our product is easy to use"
  → Story of customer who set up in 10 minutes
  
  "We have great support"
  → Story of support rep who stayed late to solve problem
  
  TECHNIQUE:
  - Identify claims you're making
  - Find stories that demonstrate claims
  - Let audience reach conclusion themselves
  - Remove the claim, keep the story
  
  THE TEST:
  If you removed all adjectives, would the audience
  still understand what you're communicating?
  
  # Don't tell me you're funny—make me laugh
  
### **Symptoms**
  - Lots of claims, few stories
  - Adjective-heavy copy
  - Audience skepticism
  - \'"Says who?" reaction\'
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
\b(innovative|best|leading|premier|world-class|revolutionary|game-changing|cutting-edge)\b(?!.*\b(example|story|case|instance)\b)
      ###### **Severity**
high
      ###### **Note**
Claims without supporting story
    
---
      ###### **Pattern**
(We are|Our company is|Known for being).*(innovative|customer-focused|easy|fast|reliable)
      ###### **Severity**
high
      ###### **Note**
Direct claims instead of demonstration
  #### **Fix Template**
    Replace claim with story:
    Claim: "We're customer-focused"
    Story: "[Employee] flew to [city] to help [customer] with [problem].
            Spent [timeframe] until issue resolved."
    

## Story Data Divorce

### **Id**
story-data-divorce
### **Summary**
Stories without evidence or data without narrative
### **Severity**
low
### **Situation**
  Either telling emotional stories without proof, or presenting data
  without narrative context. The two divorced from each other.
  
### **Why**
  Stories need data for credibility. Data needs story for meaning.
  Together they're powerful. Apart they're incomplete. Emotion drives
  engagement; proof drives belief.
  
### **Solution**
  MARRY STORY AND DATA:
  
  STORY + DATA:
  "Sarah grew revenue by 47%"
  + "She finally felt confident presenting to the board"
  = Complete
  
  DATA → STORY:
  - Who does this number represent?
  - What did their journey look like?
  - What does this mean for them personally?
  
  STORY → DATA:
  - What's the proof?
  - Can you quantify the transformation?
  - What's the before/after numbers?
  
  INTEGRATION:
  "When Sarah started, her CAC was $180 and climbing.
   Twelve weeks later, she'd cut it to $95. But the
   real win? She stopped dreading board meetings."
  
  # Story for emotion. Data for proof.
  
### **Symptoms**
  - All emotion, no proof
  - All data, no humanity
  - Unbelievable stories
  - Meaningless metrics
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
(story|testimonial)(?!.*(\d{1,3}%|\$\d+|[0-9]+ months|[0-9]+x))
      ###### **Severity**
medium
      ###### **Note**
Story without quantifiable proof
    
---
      ###### **Pattern**
(\d{1,3}%|\$\d+|increased by \d)(?!.*\b(she|he|they|customer)\b)
      ###### **Severity**
medium
      ###### **Note**
Data without human context
  #### **Fix Template**
    Integrate story + data:
    "[Customer name] [emotional transformation].
     The numbers: [specific metrics with timeframe]."
    

## Transformation Missing

### **Id**
transformation-missing
### **Summary**
Stories without clear before/after change
### **Severity**
medium
### **Situation**
  Telling narratives that don't show transformation—stories that go
  nowhere, where the character ends up the same as they started.
  
### **Why**
  Transformation is the payoff. Without change, what was the point?
  The audience needs to see and feel the difference the journey made.
  This is what makes stories satisfying and inspiring.
  
### **Solution**
  CLEAR TRANSFORMATION:
  
  BEFORE STATE:
  - Specific situation
  - Pain points
  - Limitations
  - Emotional state
  
  AFTER STATE:
  - What changed
  - New capabilities
  - Results achieved
  - Emotional transformation
  
  TRANSFORMATION TYPES:
  - Capability: Can now do what they couldn't
  - Understanding: Now knows what they didn't
  - Feeling: Confidence, relief, excitement
  - Results: Measurable outcomes
  
  THE GAP:
  The bigger the gap between before and after,
  the more powerful the story.
  
  MAKE IT EXPLICIT:
  "Before: Sarah dreaded Mondays"
  "After: Sarah starts each week excited"
  
  # No transformation = no story
  
### **Symptoms**
  - Stories go nowhere
  - No clear before/after
  - Audience confused about point
  - Unsatisfying narrative
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
(story|narrative|case study)(?!.*(before|after|used to|now|changed|transformed|went from))
      ###### **Severity**
high
      ###### **Note**
No before/after transformation language
    
---
      ###### **Pattern**
\b(success|result|outcome)\b(?!.*(before|previously|initially|started))
      ###### **Severity**
medium
      ###### **Note**
Result without baseline context
  #### **Fix Template**
    Add transformation framework:
    "Before: [Customer] was [state/feeling/situation]
     After: [Customer] is now [new state/feeling/situation]
     The shift: [what specifically changed]"
    

## Corporate Speak Story

### **Id**
corporate-speak-story
### **Summary**
Using jargon and buzzwords instead of human language
### **Severity**
medium
### **Situation**
  Writing stories filled with corporate language: "leverage synergies,"
  "drive outcomes," "optimize workflows." Language that sounds like
  a press release, not a human being.
  
### **Why**
  Stories are human. Jargon creates distance. When you say "leveraged
  our platform to optimize their workflow," you're not telling a story—
  you're writing a feature announcement. Real humans don't talk like that.
  
### **Solution**
  HUMAN LANGUAGE TEST:
  
  WOULD A HUMAN SAY THIS?
  - "Leveraged synergies" → NO
  - "Started using the tool" → YES
  - "Optimize workflows" → MAYBE
  - "Get more done in less time" → YES
  
  TRANSLATION:
  Corporate: "Leveraged our platform to drive outcomes"
  Human: "Used the tool and hit their goals"
  
  Corporate: "Optimized their go-to-market strategy"
  Human: "Figured out how to sell better"
  
  Corporate: "Enhanced operational efficiency"
  Human: "Got the work done faster"
  
  THE READ-ALOUD TEST:
  If you wouldn't say it to your friend over coffee, don't write it.
  
  COPY-PASTE FIX:
  ```javascript
  const jargonMap = {
    "leverage": "use",
    "utilize": "use",
    "optimize": "improve",
    "synergy": "working together",
    "drive outcomes": "get results",
    "facilitate": "help",
    "implement": "start using",
    "execute": "do"
  };
  
  function humanizeStory(text) {
    let human = text;
    for (const [jargon, plain] of Object.entries(jargonMap)) {
      human = human.replace(new RegExp(jargon, 'gi'), plain);
    }
    return human;
  }
  ```
  
### **Symptoms**
  - Sounds like a press release
  - No one talks like this in real life
  - Buzzword bingo
  - Reader's eyes glaze over
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
\b(leverage|synerg|optimize|facilitate|implement|execute|drive|enhance|enable|empower)\b
      ###### **Severity**
medium
      ###### **Note**
Corporate jargon detected
    
---
      ###### **Pattern**
\b(strategic|holistic|robust|scalable|agile|innovative)\b.*\b(solution|platform|framework)\b
      ###### **Severity**
medium
      ###### **Note**
Buzzword + buzzword combination
  #### **Fix Template**
    Replace jargon with human language:
    1. Read story aloud
    2. Where do you stumble? That's jargon.
    3. Replace with what you'd say to a friend
    4. Verify: Would a 12-year-old understand this?
    

## Missing Sensory Details

### **Id**
missing-sensory-details
### **Summary**
Stories without sensory or emotional texture
### **Severity**
low
### **Situation**
  Telling stories that are all facts and no feeling. No description of
  what it looked like, sounded like, felt like. Pure information delivery
  without the details that make stories vivid.
  
### **Why**
  Sensory details activate the brain differently than abstract facts.
  "Sarah was frustrated" is abstract. "Sarah threw her laptop charger
  across the room" is concrete. The second creates a movie in the
  reader's mind. That's what makes stories memorable.
  
### **Solution**
  ADD SENSORY TEXTURE:
  
  TYPES OF DETAILS:
  1. Visual: What did it look like?
     - "The dashboard showed red everywhere"
     - "Three rejected proposals sat in her inbox"
  
  2. Auditory: What did it sound like?
     - "The Slack notification wouldn't stop pinging"
     - "Her team went quiet when she walked in"
  
  3. Kinesthetic: What did it feel like physically?
     - "She slumped in her chair"
     - "He paced the conference room"
  
  4. Emotional: What did it feel like emotionally?
     - "The knot in her stomach tightened"
     - "Relief washed over him"
  
  5. Temporal: When/how long?
     - "It was 11pm on a Friday"
     - "After six straight hours of calls"
  
  BEFORE (abstract):
  "The marketing director was stressed about the campaign."
  
  AFTER (sensory):
  "At 2am, Sarah was still at her desk, the office dark except
  for her screen. The campaign launched in 6 hours and the
  conversion tracking still wasn't working. Her coffee had
  gone cold an hour ago."
  
  IMPLEMENTATION:
  For each story beat, ask:
  - Where were they? (setting)
  - What time was it? (temporal)
  - What could you see? (visual)
  - What did they do physically? (kinesthetic)
  - How did their body react? (physiological)
  
  COPY-PASTE TEMPLATE:
  [Character] was [location] at [time]. [Visual detail]. [Physical action].
  [Emotional indicator]. [What was at stake].
  
### **Symptoms**
  - Stories feel flat
  - Hard to visualize
  - Purely informational
  - Not immersive
### **Detection Pattern**
  #### **Type**
content_analysis
  #### **Triggers**
    
---
      ###### **Pattern**
(story|narrative)(?!.*(looked|felt|saw|heard|noticed|realized|desk|office|room|screen|phone))
      ###### **Severity**
low
      ###### **Note**
Abstract story without sensory details
    
---
      ###### **Pattern**
\b(frustrated|excited|worried|happy|sad)\b(?!.*(because|when|as|while))
      ###### **Severity**
low
      ###### **Note**
Emotion stated but not shown through detail
  #### **Fix Template**
    Add one sensory detail per story beat:
    □ Where were they? (place)
    □ When was it? (time of day, day of week)
    □ What could you see? (visual detail)
    □ What did they physically do? (action)
    □ How did their body feel? (sensation)
    