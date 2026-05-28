# Real Time Content - Sharp Edges

## Sensitivity Blindspot

### **Id**
sensitivity-blindspot
### **Summary**
Publishing without sensitivity check in rush to be first
### **Severity**
critical
### **Situation**
  Racing to publish trend content without considering whether the
  trend is connected to tragedy, controversy, or sensitive topics.
  
### **Why**
  Speed kills (your brand). One insensitive post during a crisis can
  overshadow years of good marketing. Real-time doesn't mean
  thoughtless. Five minutes for sensitivity check is worth it.
  
### **Solution**
  SENSITIVITY CHECKPOINT:
  
  BEFORE EVERY POST, ASK:
  1. What's happening in the news right now?
  2. Could this trend be connected to tragedy?
  3. Is there any way this could be insensitive?
  4. What's the worst interpretation?
  5. Are there affected communities?
  
  RED FLAG TOPICS:
  - Active violence/tragedy
  - Political controversies
  - Cultural appropriation concerns
  - Health crises
  - Natural disasters
  - Death of public figures
  
  IF ANY CONCERN:
  - Delay publication
  - Get second opinion
  - When in doubt, don't
  
  # 5 minutes now > crisis later
  
### **Symptoms**
  - Social media backlash
  - Brand apology needed
  - \'"Read the room" criticism\'
  - Crisis management activated
### **Detection Pattern**
  #### **Intent**
    - publish.*trend
    - post.*trending
    - real-time.*content
    - newsjack
  #### **Context**
    - breaking news
    - trending now
    - viral moment
    - hashtag
  #### **Missing**
    - sensitivity check
    - appropriate
    - review.*content
    - crisis.*scan

## Forced Brand Connection

### **Id**
forced-brand-connection
### **Summary**
Jumping on trends that don't naturally fit brand
### **Severity**
high
### **Situation**
  Forcing brand into trending conversations where there's no natural
  connection, making the brand look desperate or out of touch.
  
### **Why**
  Audiences immediately sense forced connections. "What does [brand]
  have to do with this?" comments are death. Cringe is worse than
  silence. Not every trend is your trend.
  
### **Solution**
  BRAND FIT CHECK:
  
  NATURAL FIT CRITERIA:
  1. Relevance: Does this connect to what we do?
  2. Audience: Will our audience care about this?
  3. Value: Can we add something unique?
  4. Authenticity: Does this feel like us?
  5. Permission: Do we have "standing" here?
  
  IF YOU HAVE TO EXPLAIN THE CONNECTION:
  → It's forced. Skip it.
  
  GOOD FIT EXAMPLES:
  - Athletic brand + sports moment
  - Food brand + food trend
  - Tech brand + tech news
  - Any brand + genuinely universal moment
  
  BAD FIT EXAMPLES:
  - Insurance brand + meme trend
  - B2B software + pop culture moment
  - Any brand + tragedy "tribute"
  
  # Selective excellence > universal mediocrity
  
### **Symptoms**
  - \'"Why is [brand] here?" comments\'
  - Low engagement
  - Cringe perception
  - Brand dilution
### **Detection Pattern**
  #### **Intent**
    - respond to trend
    - jump on.*trending
    - capitalize on
    - ride the wave
  #### **Context**
    - trending topic
    - viral moment
    - cultural event
  #### **Missing**
    - brand fit
    - relevant.*brand
    - natural connection
    - makes sense for

## No Pre Built Systems

### **Id**
no-pre-built-systems
### **Summary**
Attempting real-time without pre-approved templates
### **Severity**
high
### **Situation**
  Trying to create and publish real-time content without pre-built
  systems for templates, approvals, and workflows.
  
### **Why**
  Real-time without systems = chaos. Every post requires full creative
  process, legal review, stakeholder approval. By the time you're done,
  the moment passed. Systems enable speed.
  
### **Solution**
  PRE-BUILD THESE:
  
  1. TEMPLATE LIBRARY:
     - Visual templates in brand style
     - Copy frameworks for common scenarios
     - Platform-specific formats ready
     - All pre-approved
  
  2. APPROVAL MATRIX:
     - What can go out without approval
     - What needs quick review
     - What needs full process
     - Who approves what
  
  3. ASSET LIBRARY:
     - Brand elements ready to use
     - Product imagery
     - Character/mascot variations
     - AI prompt templates
  
  4. WORKFLOW:
     - Clear roles (who does what)
     - Response timeframes
     - Escalation paths
     - Coverage for key moments
  
  BUILD BEFORE YOU NEED IT.
  
### **Symptoms**
  - Missed moments
  - Slow response time
  - Inconsistent output
  - Team scrambling
### **Detection Pattern**
  #### **Intent**
    - real-time content
    - rapid response
    - quick.*publish
    - trend.*respond
  #### **Context**
    - launch.*program
    - set up.*capability
    - build.*system
  #### **Missing**
    - template
    - pre-approved
    - framework
    - workflow.*ready

## Stale Real Time

### **Id**
stale-real-time
### **Summary**
Publishing hours or days after moment has passed
### **Severity**
high
### **Situation**
  Completing content creation after the trend has peaked, publishing
  when the moment is already stale.
  
### **Why**
  Late real-time content is worse than no content. Shows you're trying
  to be relevant but failing. Screams "we're slow." Most trends peak
  in 2-6 hours; if you miss that window, skip it.
  
### **Solution**
  TIMING RULES:
  
  HOT MOMENTS (2-6 hour window):
  - Viral memes
  - Breaking culture moments
  - Surprise news
  → If you can't publish within window, skip
  
  WARM MOMENTS (same day):
  - Planned events
  - Anticipated announcements
  - Award shows, sports events
  → Can take a bit longer if angle is unique
  
  COLD MOMENTS (1+ day):
  - Only if adding significant value
  - \'"Hot take" opportunity\'
  - Contrarian/different perspective
  → Usually better to skip
  
  DECISION FRAMEWORK:
  Before starting: "Will this still be relevant when we finish?"
  If no → Don't start
  
### **Symptoms**
  - \'"This is so yesterday" comments\'
  - Low engagement
  - Out of touch perception
  - Wasted effort
### **Detection Pattern**
  #### **Intent**
    - publish.*trend
    - post about
    - respond to
  #### **Context**
    - yesterday
    - last night
    - few hours ago
    - earlier today
  #### **Missing**
    - still relevant
    - timing.*check
    - trend.*current
    - moment.*active

## Every Trend Response

### **Id**
every-trend-response
### **Summary**
Feeling obligated to respond to every trending topic
### **Severity**
medium
### **Situation**
  Treating every trend as an opportunity, exhausting team and
  diluting brand by responding to everything.
  
### **Why**
  Most trend responses are mediocre. Better to do 1 great execution
  than 10 forgettable ones. Team burnout is real. Selective excellence
  builds reputation.
  
### **Solution**
  SELECTION CRITERIA:
  
  MUST HAVE ALL:
  - Natural brand connection
  - Audience relevance
  - Time to execute well
  - Unique angle to add
  - No sensitivity concerns
  
  PRIORITIZATION:
  Tier 1: Perfect fit + high impact → Full effort
  Tier 2: Good fit + medium impact → Quick execution
  Tier 3: Marginal fit → Skip
  
  WEEKLY QUOTA:
  - Not every day needs trend content
  - 2-3 great executions/week > 10 mediocre
  - Quality builds reputation
  
  PERMISSION TO SKIP:
  "This isn't our moment" is a valid decision
  
### **Symptoms**
  - Team exhaustion
  - Declining quality
  - Forced content
  - Diminishing returns
### **Detection Pattern**
  #### **Intent**
    - respond to.*trend
    - post about.*trending
    - react to.*every
  #### **Context**
    - multiple trends
    - all.*trending
    - every.*moment
    - daily.*content
  #### **Missing**
    - selective
    - prioritize
    - filter.*trends
    - choose.*best

## Copying Competitors

### **Id**
copying-competitors
### **Summary**
Replicating how competitors responded to trend
### **Severity**
medium
### **Situation**
  Seeing competitor's trend response and copying the approach rather
  than finding unique angle.
  
### **Why**
  Second-to-market with same idea = derivative. Audiences notice.
  Your brand should have unique perspective. If you can't add
  something different, you're just noise.
  
### **Solution**
  FIND YOUR ANGLE:
  
  IF COMPETITOR WENT FIRST:
  1. Can we do opposite/contrarian?
  2. Can we add our unique perspective?
  3. Can we go deeper/longer-form?
  4. Can we address different audience?
  5. Is there uncovered angle?
  
  IF NO UNIQUE ANGLE:
  → Skip this one. Wait for next trend.
  
  YOUR DIFFERENTIATOR:
  - Brand voice (how you say it)
  - Brand expertise (what you know)
  - Brand assets (what you have)
  - Brand community (who you reach)
  
  Use your differentiators, not competitor's playbook.
  
### **Symptoms**
  - \'"They did what [competitor] did" comments\'
  - Lower engagement than competitor
  - Derivative perception
  - Missed opportunity for uniqueness
### **Detection Pattern**
  #### **Intent**
    - like.*competitor
    - similar to.*brand
    - saw.*[brand].*do
    - copy.*approach
  #### **Context**
    - trending
    - viral moment
    - trend response
  #### **Missing**
    - unique angle
    - our perspective
    - differentiate
    - brand twist

## Meme Misuse

### **Id**
meme-misuse
### **Summary**
Using meme format incorrectly
### **Severity**
medium
### **Situation**
  Using a meme format without understanding its origin, meaning, or
  correct usage, resulting in cringe.
  
### **Why**
  Meme literacy matters. Using format wrong signals you don't
  understand internet culture. If you have to explain why it's funny,
  you've failed. Meme misuse is screenshot-worthy cringe.
  
### **Solution**
  MEME USAGE CHECKLIST:
  
  BEFORE USING MEME:
  □ Research the origin
  □ Understand the format
  □ Check current usage
  □ Verify still relevant (not dead)
  □ Confirm appropriateness
  
  CORRECT USAGE:
  - Follow format structure exactly
  - Add brand twist, not format change
  - Timing matters (don't be late)
  - Self-awareness helps
  
  WHEN IN DOUBT:
  - Ask someone under 30
  - Check KnowYourMeme.com
  - Look at recent examples
  - If still unsure, skip
  
  # Meme misuse = internet cringe hall of fame
  
### **Symptoms**
  - \'"They did it wrong" comments\'
  - Format correction replies
  - Screenshot mockery
  - Cringe reputation
### **Detection Pattern**
  #### **Intent**
    - use.*meme
    - meme format
    - trending meme
    - viral format
  #### **Context**
    - create content
    - post.*meme
    - jump on
  #### **Missing**
    - research.*format
    - verify.*usage
    - check.*origin
    - understand.*context

## No Monitoring After

### **Id**
no-monitoring-after
### **Summary**
Publishing and walking away
### **Severity**
medium
### **Situation**
  Publishing real-time content and not monitoring response, missing
  engagement opportunities or problems.
  
### **Why**
  Real-time content creates real-time conversation. If you're not
  there to engage, you miss the value. Also: problems can emerge
  that need quick response.
  
### **Solution**
  POST-PUBLISH MONITORING:
  
  FIRST HOUR:
  - Monitor comments actively
  - Respond to engagement
  - Watch for problems
  - Share internally if going well
  
  FIRST DAY:
  - Track performance metrics
  - Continue engagement
  - Flag any issues
  - Document learnings
  
  ENGAGEMENT RESPONSE:
  - Reply to comments quickly
  - Engage authentically
  - Don't over-brand responses
  - Know when to stop
  
  PROBLEM RESPONSE:
  - Watch for negative sentiment
  - Quick escalation if needed
  - Don't delete/hide unless serious
  - Learn for next time
  
### **Symptoms**
  - Missed engagement opportunities
  - Unaddressed problems escalate
  - Lost conversation momentum
  - No learning captured
### **Detection Pattern**
  #### **Intent**
    - publish.*content
    - post.*trend
    - go live
  #### **Context**
    - real-time
    - trending
    - viral
  #### **Missing**
    - monitor
    - track.*response
    - watch.*comments
    - engage.*after

## Approval Bottleneck

### **Id**
approval-bottleneck
### **Summary**
Requiring full approval process for all real-time content
### **Severity**
medium
### **Situation**
  Routing all real-time content through standard approval process,
  killing speed and missing moments.
  
### **Why**
  Standard approval: 2-3 days. Trend window: 2-6 hours. The math
  doesn't work. Real-time requires pre-approved frameworks and
  expedited paths.
  
### **Solution**
  TIERED APPROVAL:
  
  TIER 1: PRE-APPROVED (no approval needed)
  - Uses pre-approved templates
  - Within defined topic boundaries
  - No claims or commitments
  - Published by approved team members
  
  TIER 2: QUICK APPROVAL (30 min max)
  - Minor variations from template
  - New but safe topic
  - One approver required
  - Slack/message approval ok
  
  TIER 3: EXPEDITED (2 hours max)
  - New creative
  - Sensitive topic
  - Multiple approvers
  - Still faster than normal
  
  TIER 4: FULL PROCESS (skip real-time)
  - Legal claims
  - Controversy potential
  - Major commitments
  - Not appropriate for real-time
  
  PRE-DEFINE which content fits which tier.
  
### **Symptoms**
  - Consistently missing moments
  - Frustrated team
  - Slow-to-market reputation
  - Approval as excuse
### **Detection Pattern**
  #### **Intent**
    - real-time.*approval
    - get approved
    - approval.*process
  #### **Context**
    - trending
    - urgent
    - quick.*response
  #### **Missing**
    - expedited
    - pre-approved
    - fast track
    - tier.*system

## Ai Generation Delays

### **Id**
ai-generation-delays
### **Summary**
Slow AI generation blocking real-time workflow
### **Severity**
low
### **Situation**
  AI image/video generation taking too long, causing missed timing
  windows for trend content.
  
### **Why**
  AI generation can take minutes. Queue waits can add more. In
  real-time, minutes matter. Need strategies to work around
  generation delays.
  
### **Solution**
  AI SPEED STRATEGIES:
  
  1. PARALLEL GENERATION:
     - Generate multiple options simultaneously
     - Don't wait for one to finish
     - Select best from batch
  
  2. TEMPLATE LIBRARY:
     - Pre-generated assets for common scenarios
     - Quick modification vs full generation
     - Fill-in-blank approach
  
  3. FASTEST MODELS:
     - Turbo/fast versions for real-time
     - Save quality models for planned content
     - Know your tool speeds
  
  4. HYBRID APPROACH:
     - AI-assist, human finish
     - Quick generation + manual refinement
     - Don't wait for perfect
  
  5. PLATFORM SELECTION:
     - Some platforms faster than others
     - Queue times vary
     - Have backup options
  
  # Speed over perfection for real-time
  
### **Symptoms**
  - Waiting on generation
  - Missed timing windows
  - Over-relying on single tool
  - Perfectionism killing speed
### **Detection Pattern**
  #### **Intent**
    - generate.*image
    - create.*visual
    - AI.*content
  #### **Context**
    - real-time
    - urgent
    - trending
  #### **Missing**
    - parallel.*generation
    - template.*library
    - fast.*model
    - backup.*option